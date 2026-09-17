from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException, status

from src.application.common import Interactor, TranslatorHub
from src.application.common.dao import UserDao
from src.application.common.dao.auth import AuthSessionDao
from src.application.common.email_sender import EmailSender
from src.application.common.password_hasher import PasswordHasher
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.services import WebService
from src.application.use_cases.auth._codes import (
    generate_password_reset_token,
    hash_password_reset_token,
    hash_reset_email,
)
from src.core.config import AppConfig
from src.core.constants import (
    PASSWORD_RESET_REQUEST_COOLDOWN_SECONDS,
    PASSWORD_RESET_TOKEN_TTL_SECONDS,
)
from src.core.exceptions import EmailDeliveryDisabledError


@dataclass
class RequestPasswordResetDto:
    email: str


class RequestPasswordReset(Interactor[RequestPasswordResetDto, None]):
    """Email a password reset link.

    Never reveals whether the address belongs to an account: every outcome that
    is not a configuration failure returns ``None`` silently, so the endpoint
    can always answer 200 and the flow cannot be used to enumerate users.
    """

    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        user_dao: UserDao,
        auth_session: AuthSessionDao,
        email_sender: EmailSender,
        i18n_hub: TranslatorHub,
        web_service: WebService,
    ) -> None:
        self.config = config
        self.user_dao = user_dao
        self.auth_session = auth_session
        self.email_sender = email_sender
        self.i18n_hub = i18n_hub
        self.web_service = web_service

    async def _execute(self, actor: UserDto, data: RequestPasswordResetDto) -> None:
        if not self.email_sender.is_enabled:
            raise EmailDeliveryDisabledError("Email delivery is not configured")

        key = self.config.crypt_key.get_secret_value()
        email_hash = hash_reset_email(data.email, key)

        started = await self.auth_session.try_start_password_reset_cooldown(
            email_hash, PASSWORD_RESET_REQUEST_COOLDOWN_SECONDS
        )
        if not started:
            return None

        user = await self.user_dao.get_by_email(data.email)
        if not user or not user.email or user.is_blocked or not user.is_email_verified:
            return None

        token = generate_password_reset_token()
        token_hash = hash_password_reset_token(token, key)
        await self.auth_session.store_password_reset_token(
            token_hash, user.id, PASSWORD_RESET_TOKEN_TTL_SECONDS
        )

        link = self.web_service.reset_password(token)
        if not link:
            await self.auth_session.revoke_password_reset_token(token_hash)
            await self.auth_session.clear_password_reset_cooldown(email_hash)
            raise EmailDeliveryDisabledError("Web cabinet URL is not configured")

        minutes = PASSWORD_RESET_TOKEN_TTL_SECONDS // 60
        i18n = self.i18n_hub.get_translator_by_locale(user.language)

        try:
            await self.email_sender.send(
                to=user.email,
                subject=i18n.get("email-password-reset.title"),
                body=i18n.get("email-password-reset.message", link=link, minutes=minutes),
                html=i18n.get("email-password-reset.message-html", link=link, minutes=minutes),
            )
        except Exception:
            # Drop the unusable token and let the user retry immediately instead
            # of serving out a cooldown they never got a mail for.
            await self.auth_session.revoke_password_reset_token(token_hash)
            await self.auth_session.clear_password_reset_cooldown(email_hash)
            raise

        return None


@dataclass
class ResetPasswordDto:
    token: str
    new_password: str


class ResetPassword(Interactor[ResetPasswordDto, UserDto]):
    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        uow: UnitOfWork,
        user_dao: UserDao,
        auth_session: AuthSessionDao,
        password_hasher: PasswordHasher,
    ) -> None:
        self.config = config
        self.uow = uow
        self.user_dao = user_dao
        self.auth_session = auth_session
        self.password_hasher = password_hasher

    async def _execute(self, actor: UserDto, data: ResetPasswordDto) -> UserDto:
        token_hash = hash_password_reset_token(data.token, self.config.crypt_key.get_secret_value())
        # GETDEL: the token is single-use even if two requests race.
        user_id: Optional[int] = await self.auth_session.consume_password_reset_token(token_hash)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )

        user = await self.user_dao.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )
        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")

        user.password_hash = self.password_hasher.hash(data.new_password)

        async with self.uow:
            updated = await self.user_dao.update(user)
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found during password reset",
                )
            await self.uow.commit()

        await self.auth_session.revoke_all_user_tokens(user.id)
        return updated
