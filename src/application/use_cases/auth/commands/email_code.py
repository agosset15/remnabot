import hmac
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.exc import IntegrityError

from src.application.common import Interactor, Notifier, TranslatorHub
from src.application.common.dao import UserDao
from src.application.common.dao.auth import AuthSessionDao
from src.application.common.email_sender import EmailSender
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.use_cases.auth._codes import (
    build_magic_link,
    check_email_resend_cooldown,
    decode_magic_token,
    generate_email_verification_code,
    hash_email_verification_code,
)
from src.application.use_cases.auth._delivery import deliver_email_code
from src.application.use_cases.user.commands.web_registration import (
    RegisterWebUser,
    RegisterWebUserDto,
)
from src.core.config import AppConfig
from src.core.constants import (
    EMAIL_LOGIN_CODE_MAX_ATTEMPTS,
    EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS,
)
from src.core.enums import AuthType
from src.core.exceptions import EmailDeliveryDisabledError
from src.core.utils.time import datetime_now


@dataclass
class RequestEmailCodeDto:
    email: str
    referral_code: Optional[str] = None


@dataclass
class EmailCodeRequested:
    expires_at: datetime


class RequestEmailCode(Interactor[RequestEmailCodeDto, EmailCodeRequested]):
    """Issue a login/verification code for an email address, authenticated or not.

    Unknown addresses do not get an account yet: the code lives in Redis and the
    user row is created only once the code (or its magic link) is confirmed.
    """

    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        uow: UnitOfWork,
        user_dao: UserDao,
        auth_session: AuthSessionDao,
        email_sender: EmailSender,
        notifier: Notifier,
        i18n_hub: TranslatorHub,
    ) -> None:
        self.config = config
        self.uow = uow
        self.user_dao = user_dao
        self.auth_session = auth_session
        self.email_sender = email_sender
        self.notifier = notifier
        self.i18n_hub = i18n_hub

    async def _execute(self, actor: UserDto, data: RequestEmailCodeDto) -> EmailCodeRequested:
        if not self.email_sender.is_enabled:
            raise EmailDeliveryDisabledError("Email delivery is not configured")

        minutes = self.config.email.verification_code_ttl_minutes
        now = datetime_now()
        expires_at = now + timedelta(minutes=minutes)

        user = await self.user_dao.get_by_email(data.email)
        if user is None:
            user = await self.user_dao.get_by_pending_email(data.email)

        if user is not None and user.is_blocked:
            # Never tell the caller whether the address exists or is blocked.
            logger.info(f"Email code requested for blocked user '{user.id}', skipping delivery")
            return EmailCodeRequested(expires_at=expires_at)

        if user is not None:
            check_email_resend_cooldown(
                user.email_verification_expires_at,
                minutes,
                EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS,
                now,
            )
        else:
            pending = await self.auth_session.get_email_login_code(data.email)
            if pending:
                check_email_resend_cooldown(
                    _parse_expires_at(pending.get("expires_at")),
                    minutes,
                    EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS,
                    now,
                )

        code = generate_email_verification_code()
        link = build_magic_link(self.config, data.email, code, expires_at)

        # Send first: a failed delivery must not persist a code or start a cooldown.
        await deliver_email_code(
            email_sender=self.email_sender,
            notifier=self.notifier,
            i18n_hub=self.i18n_hub,
            locale=self.config.default_locale,
            target_email=data.email,
            code=code,
            minutes=minutes,
            link=link,
            user=user,
        )

        code_hash = hash_email_verification_code(code, self.config.crypt_key.get_secret_value())

        if user is not None:
            user.email_verification_code_hash = code_hash
            user.email_verification_expires_at = expires_at
            async with self.uow:
                updated = await self.user_dao.update(user)
                if not updated:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="User not found during email code request",
                    )
                await self.uow.commit()
        else:
            await self.auth_session.store_email_login_code(
                data.email,
                {
                    "code_hash": code_hash,
                    "expires_at": expires_at.isoformat(),
                    "referral_code": data.referral_code,
                },
                ttl=minutes * 60,
            )

        await self.auth_session.reset_email_code_attempts(data.email)
        return EmailCodeRequested(expires_at=expires_at)


@dataclass
class LoginWithEmailCodeDto:
    email: str
    code: str


class LoginWithEmailCode(Interactor[LoginWithEmailCodeDto, UserDto]):
    """Exchange an email code for an authenticated user.

    Any code delivered to an address also proves ownership of it, so a successful
    login marks the email verified and promotes a pending address.
    """

    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        uow: UnitOfWork,
        user_dao: UserDao,
        auth_session: AuthSessionDao,
        register_web_user: RegisterWebUser,
    ) -> None:
        self.config = config
        self.uow = uow
        self.user_dao = user_dao
        self.auth_session = auth_session
        self.register_web_user = register_web_user

    async def _execute(self, actor: UserDto, data: LoginWithEmailCodeDto) -> UserDto:
        attempts = await self.auth_session.incr_email_code_attempts(
            data.email, ttl=self.config.email.verification_code_ttl_minutes * 60
        )
        if attempts > EMAIL_LOGIN_CODE_MAX_ATTEMPTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many invalid codes, request a new one",
            )

        incoming_hash = hash_email_verification_code(
            data.code, self.config.crypt_key.get_secret_value()
        )

        user = await self.user_dao.get_by_email(data.email)
        if user is None:
            user = await self.user_dao.get_by_pending_email(data.email)

        if user is not None:
            return await self._login_existing(user, incoming_hash)
        return await self._register_new(data.email, incoming_hash)

    async def _login_existing(self, user: UserDto, incoming_hash: str) -> UserDto:
        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")

        if not user.email_verification_code_hash or not user.email_verification_expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code was not requested"
            )
        if user.email_verification_expires_at < datetime_now():
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="Code has expired")
        if not hmac.compare_digest(incoming_hash, user.email_verification_code_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")

        if user.pending_email:
            existing = await self.user_dao.get_by_email(user.pending_email)
            if existing and existing.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )
            user.email = user.pending_email

        email = user.email
        user.pending_email = None
        user.is_email_verified = True
        user.email_verification_code_hash = None
        user.email_verification_expires_at = None

        async with self.uow:
            updated = await self.user_dao.update(user)
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found during email code login",
                )
            await self.uow.commit()

        if email:
            await self.auth_session.reset_email_code_attempts(email)
        return updated

    async def _register_new(self, email: str, incoming_hash: str) -> UserDto:
        pending = await self.auth_session.get_email_login_code(email)
        if not pending or not pending.get("code_hash"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Code was not requested"
            )

        expires_at = _parse_expires_at(pending.get("expires_at"))
        if expires_at is not None and expires_at < datetime_now():
            await self.auth_session.revoke_email_login_code(email)
            raise HTTPException(status_code=status.HTTP_410_GONE, detail="Code has expired")

        if not hmac.compare_digest(incoming_hash, str(pending["code_hash"])):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")

        referral_code = pending.get("referral_code")
        if referral_code and not await self.user_dao.get_by_referral_code(str(referral_code)):
            referral_code = None

        new_user = UserDto(
            telegram_id=None,
            auth_type=AuthType.EMAIL,
            email=email,
            password_hash=None,
            username=None,
            name=email.split("@")[0],
            language=self.config.default_locale,
            is_email_verified=True,
        )

        try:
            created = await self.register_web_user.system(
                RegisterWebUserDto(user=new_user, referral_code=referral_code)
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            ) from e

        await self.auth_session.revoke_email_login_code(email)
        await self.auth_session.reset_email_code_attempts(email)

        if created.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
        return created


@dataclass
class LoginWithMagicLinkDto:
    token: str


class LoginWithMagicLink(Interactor[LoginWithMagicLinkDto, UserDto]):
    """Same flow as a typed code: the magic link carries the code in a signed token."""

    required_permission = None

    def __init__(self, config: AppConfig, login_with_email_code: LoginWithEmailCode) -> None:
        self.config = config
        self.login_with_email_code = login_with_email_code

    async def _execute(self, actor: UserDto, data: LoginWithMagicLinkDto) -> UserDto:
        if self.config.jwt_secret is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT secret not configured",
            )

        email, code = decode_magic_token(data.token, self.config.jwt_secret.get_secret_value())
        return await self.login_with_email_code.system(
            LoginWithEmailCodeDto(email=email, code=code)
        )


def _parse_expires_at(value: Any) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None
