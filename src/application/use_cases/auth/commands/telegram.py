import json
from dataclasses import dataclass
from typing import Any, cast

import httpx
from fastapi import HTTPException, status
from loguru import logger
from redis.asyncio import Redis
from remnapy.exceptions import NotFoundError
from sqlalchemy.exc import IntegrityError

from src.application.common import Interactor, Remnawave
from src.application.common.dao import ReferralDao, SubscriptionDao, TransactionDao, UserDao
from src.application.common.policy import Permission
from src.application.common.uow import UnitOfWork
from src.application.dto import SubscriptionDto, UserDto
from src.application.use_cases.auth._telegram import (
    decode_telegram_id_token,
    parse_webapp_init_data,
    verify_telegram_webapp_init_data,
)
from src.application.use_cases.user.commands.web_registration import (
    RegisterWebUser,
    RegisterWebUserDto,
)
from src.core.config import AppConfig
from src.core.constants import (
    TELEGRAM_JWKS_CACHE_KEY,
    TELEGRAM_JWKS_CACHE_TTL,
)
from src.core.enums import AuthType


@dataclass
class TelegramAuthData:
    """A Telegram Login OIDC id_token (a signed JWT) to authenticate with."""

    id_token: str


@dataclass
class _TelegramIdentity:
    id: int
    name: str
    username: "str | None"


async def _fetch_telegram_jwks(redis: Redis, jwks_url: str) -> dict[str, Any]:
    """Return Telegram's OIDC signing keys, cached in Redis."""
    cached = await redis.get(TELEGRAM_JWKS_CACHE_KEY)
    if cached:
        return cast("dict[str, Any]", json.loads(cached))

    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.get(jwks_url)
        resp.raise_for_status()
        jwks = cast("dict[str, Any]", resp.json())

    await redis.setex(TELEGRAM_JWKS_CACHE_KEY, TELEGRAM_JWKS_CACHE_TTL, json.dumps(jwks))
    return jwks


async def _verify_id_token(id_token: str, config: AppConfig, redis: Redis) -> _TelegramIdentity:
    """Validate an id_token and extract the Telegram identity from its claims."""
    try:
        jwks = await _fetch_telegram_jwks(redis, config.bot.jwks_url)
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch Telegram JWKS: {e}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to reach Telegram identity provider",
        ) from e

    try:
        claims = decode_telegram_id_token(id_token, jwks, config.bot.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e

    raw_id = claims.get("id") or claims.get("sub")
    if raw_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="id_token missing subject"
        )
    return _TelegramIdentity(
        id=int(raw_id),
        name=str(claims.get("name", "")),
        username=claims.get("preferred_username"),
    )


async def _get_or_create_telegram_user(
    user_dao: UserDao,
    register_web_user: RegisterWebUser,
    config: AppConfig,
    identity: _TelegramIdentity,
) -> UserDto:
    user = await user_dao.get_by_telegram_id(identity.id)
    if user:
        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
        return user

    new_user = UserDto(
        telegram_id=identity.id,
        auth_type=AuthType.TELEGRAM,
        username=identity.username,
        name=identity.name or str(identity.id),
        language=config.default_locale,
    )

    try:
        return await register_web_user.system(RegisterWebUserDto(user=new_user))
    except IntegrityError as e:
        existing = await user_dao.get_by_telegram_id(identity.id)
        if existing:
            return existing
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User creation conflict"
        ) from e


class AuthenticateTelegram(Interactor[TelegramAuthData, UserDto]):
    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        user_dao: UserDao,
        register_web_user: RegisterWebUser,
        redis: Redis,
    ) -> None:
        self.config = config
        self.user_dao = user_dao
        self.register_web_user = register_web_user
        self.redis = redis

    async def _execute(self, actor: UserDto, data: TelegramAuthData) -> UserDto:
        identity = await _verify_id_token(data.id_token, self.config, self.redis)
        return await _get_or_create_telegram_user(
            self.user_dao, self.register_web_user, self.config, identity
        )


class AuthenticateTelegramWebApp(Interactor[str, UserDto]):
    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        user_dao: UserDao,
        register_web_user: RegisterWebUser,
    ) -> None:
        self.config = config
        self.user_dao = user_dao
        self.register_web_user = register_web_user

    async def _execute(self, actor: UserDto, data: str) -> UserDto:
        bot_token = self.config.bot.token.get_secret_value()
        if not verify_telegram_webapp_init_data(data, bot_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Telegram WebApp init data",
            )

        fields = parse_webapp_init_data(data)
        raw_user = fields.get("user")
        if not raw_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing user in init data",
            )
        user_payload = json.loads(raw_user)

        name_parts = [str(user_payload.get("first_name", ""))]
        if user_payload.get("last_name"):
            name_parts.append(str(user_payload["last_name"]))

        identity = _TelegramIdentity(
            id=int(user_payload["id"]),
            name=" ".join(part for part in name_parts if part).strip(),
            username=user_payload.get("username"),
        )
        return await _get_or_create_telegram_user(
            self.user_dao, self.register_web_user, self.config, identity
        )


@dataclass
class LinkTelegramData:
    """A Telegram Login OIDC id_token to link to the current account."""

    id_token: str


class LinkTelegram(Interactor[LinkTelegramData, UserDto]):
    required_permission = Permission.PUBLIC

    def __init__(
        self,
        config: AppConfig,
        uow: UnitOfWork,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        transaction_dao: TransactionDao,
        referral_dao: ReferralDao,
        remnawave: Remnawave,
        redis: Redis,
    ) -> None:
        self.config = config
        self.uow = uow
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.transaction_dao = transaction_dao
        self.referral_dao = referral_dao
        self.remnawave = remnawave
        self.redis = redis

    async def _execute(self, actor: UserDto, data: LinkTelegramData) -> UserDto:
        identity = await _verify_id_token(data.id_token, self.config, self.redis)

        if actor.telegram_id == identity.id:
            return actor

        if actor.telegram_id is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already linked to a different Telegram account",
            )

        existing = await self.user_dao.get_by_telegram_id(identity.id)
        # A donor is only mergeable when it is a Telegram-only shell. Any of its own
        # credentials -- a confirmed email, an email change awaiting confirmation, or a
        # password -- means it is a real second account, and merging would silently
        # destroy them along with the donor row.
        if existing and (existing.email or existing.pending_email or existing.password_hash):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Already linked to a different Telegram account",
            )
        if existing and existing.id != actor.id:
            return await self._merge(actor, existing, identity)

        actor.telegram_id = identity.id
        if identity.username is not None:
            actor.username = identity.username

        async with self.uow:
            updated = await self.user_dao.update(actor)
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found during Telegram link",
                )
            await self.uow.commit()

        # The panel still holds the pre-link identity (no telegram_id), so push it there
        # too -- otherwise only a merge would ever sync it.
        await self._sync_panel_identity(updated)
        return updated

    async def _merge(self, actor: UserDto, donor: UserDto, identity: _TelegramIdentity) -> UserDto:
        """
        Merge a Telegram-only account (donor) into the current web account (actor).

        The web account survives because the session is bound to it. The donor's
        subscriptions, transactions and referrals are re-pointed to the survivor
        before the donor is deleted (otherwise its subscriptions would cascade
        away with it), and the subscription that expires latest across both
        accounts becomes the survivor's current one.
        """
        async with self.uow:
            await self.subscription_dao.reassign_to_user(donor.id, actor.id)
            await self.transaction_dao.reassign_to_user(donor.id, actor.id)
            await self.referral_dao.reassign_user(donor.id, actor.id)

            await self.user_dao.delete(donor.id)

            actor.telegram_id = identity.id
            if identity.username is not None:
                actor.username = identity.username
            if not await self.user_dao.update(actor):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found during Telegram link",
                )

            subscriptions = await self.subscription_dao.get_all_by_user(actor.id)
            surviving = max(subscriptions, key=lambda sub: sub.expire_at) if subscriptions else None
            if surviving is not None:
                await self.user_dao.set_current_subscription_by_id(actor.id, surviving.id)

            await self.uow.commit()

        logger.info(
            f"Telegram link merge: donor id='{donor.id}' merged into survivor id='{actor.id}'"
        )

        updated = await self.user_dao.get_by_id(actor.id) or actor
        await self._sync_panel_identity(updated, subscriptions)
        return updated

    async def _sync_panel_identity(
        self, user: UserDto, subscriptions: "list[SubscriptionDto] | None" = None
    ) -> None:
        """
        Push the linked identity to every RemnaWave user the account owns.

        Each subscription is a separate panel user, so syncing only the current one
        would leave the rest -- typically the donor's -- without the survivor's email
        and telegram_id. Best-effort: the link is already committed, so a panel user
        missing from the panel must not fail it.
        """
        if subscriptions is None:
            subscriptions = await self.subscription_dao.get_all_by_user(user.id)

        for subscription in subscriptions:
            try:
                await self.remnawave.sync_user_identity(
                    user=user, num_id=subscription.user_remna_num_id
                )
            except NotFoundError:
                logger.warning(
                    f"RemnaWave user '{subscription.user_remna_num_id}' "
                    f"not found while syncing Telegram link"
                )
