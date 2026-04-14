from dataclasses import dataclass
from typing import Optional

from loguru import logger

from src.application.common import EventPublisher, Interactor, Remnawave
from src.application.common.dao import ReferralDao, SubscriptionDao, TransactionDao, UserDao
from src.application.common.mailer import Mailer
from src.application.common.policy import Permission
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.events.system import UserConnectedWebEvent
from src.application.services import BotService
from src.core.enums import SubscriptionStatus
from src.core.utils.i18n_helpers import (
    i18n_format_bytes_to_unit,
    i18n_format_device_limit,
    i18n_format_expire_time,
)
from src.core.utils.i18n_keys import ByteUnitKey


@dataclass
class ConnectWebUserDto:
    telegram_user: UserDto
    referral_code: str


class ConnectWebUser(Interactor[ConnectWebUserDto, Optional[UserDto]]):
    required_permission = Permission.PUBLIC

    def __init__(
        self,
        uow: UnitOfWork,
        remnawave: Remnawave,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        transaction_dao: TransactionDao,
        referral_dao: ReferralDao,
        event_publisher: EventPublisher,
    ) -> None:
        self.uow = uow
        self.remnawave = remnawave
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.transaction_dao = transaction_dao
        self.referral_dao = referral_dao
        self.event_publisher = event_publisher

    async def _execute(self, actor: UserDto, data: ConnectWebUserDto) -> Optional[UserDto]:
        web_user = await self.user_dao.get_by_referral_code(data.referral_code)

        if not web_user:
            logger.warning(f"Connect web: no user found for referral_code='{data.referral_code}'")
            return None

        if self._is_already_connected(web_user, data.telegram_user):
            logger.debug(f"Connect web: {web_user.log} is already connected")
            return web_user

        telegram_user = data.telegram_user
        current_subscription = await self.subscription_dao.get_by_user_id(web_user.id)
        survivor, donor = self._pick_survivor(web_user, telegram_user)

        async with self.uow:
            if self._has_substantial_data(telegram_user):
                await self._full_merge(survivor, donor, web_user=web_user, telegram_user=telegram_user)
            else:
                await self._simple_connect(survivor, donor, web_user=web_user, telegram_user=telegram_user)
            await self.uow.commit()

        logger.info(
            f"Connect web: {telegram_user.log} -> merged into survivor id='{survivor.id}' "
            f"(older={'web' if survivor is web_user else 'telegram'})"
        )
        user = await self.user_dao.get_by_id(survivor.id)  # ty: ignore[invalid-argument-type]
        remna_user = await self.remnawave.update_user_metadata(
            user, current_subscription.user_remna_id
        )
        await self.event_publisher.publish(
            UserConnectedWebEvent(
                user_id=user.id,
                telegram_id=telegram_user.telegram_id,
                username=user.username,
                email=user.email,
                name=user.name,
                is_trial=current_subscription.is_trial,
                subscription_id=remna_user.uuid,
                subscription_status=SubscriptionStatus(remna_user.status),
                traffic_used=i18n_format_bytes_to_unit(
                    remna_user.used_traffic_bytes, min_unit=ByteUnitKey.MEGABYTE
                ),
                traffic_limit=i18n_format_bytes_to_unit(remna_user.traffic_limit_bytes),
                device_limit=i18n_format_device_limit(remna_user.hwid_device_limit),
                expire_time=i18n_format_expire_time(remna_user.expire_at),
            )
        )
        return user

    # ──────────────────────────────────────────────────────────────────────────
    # Decision helpers
    # ──────────────────────────────────────────────────────────────────────────

    @staticmethod
    def _is_already_connected(web_user: UserDto, telegram_user: UserDto) -> bool:
        """True when the web account already has a Telegram identity attached."""
        return (
            web_user.id == telegram_user.id  # same record
            or web_user.telegram_id is not None  # already linked to someone
        )

    @staticmethod
    def _has_substantial_data(user: UserDto) -> bool:
        """True when the Telegram user carries data worth merging."""
        return not user.is_trial_available

    @staticmethod
    def _pick_survivor(web_user: UserDto, telegram_user: UserDto) -> tuple[UserDto, UserDto]:
        """Return (survivor, donor). The older account (by created_at) survives."""
        web_ts = web_user.created_at
        tg_ts = telegram_user.created_at
        if web_ts is not None and tg_ts is not None and tg_ts < web_ts:
            return telegram_user, web_user
        return web_user, telegram_user

    # ──────────────────────────────────────────────────────────────────────────
    # Connect strategies
    # ──────────────────────────────────────────────────────────────────────────

    async def _simple_connect(
        self,
        survivor: UserDto,
        donor: UserDto,
        *,
        web_user: UserDto,
        telegram_user: UserDto,
    ) -> None:
        """Attach Telegram identity to the older account and remove the newer stub."""
        survivor.telegram_id = telegram_user.telegram_id
        survivor.username = telegram_user.username
        survivor.email = web_user.email

        if survivor.name == web_user.email:
            survivor.name = telegram_user.name

        await self._transfer_relations(survivor, donor)
        await self._delete_donor(donor)
        await self.user_dao.update(survivor)

        logger.debug(
            f"Simple connect: telegram_id='{telegram_user.telegram_id}' "
            f"attached to survivor id='{survivor.id}'"
        )

    async def _full_merge(
        self,
        survivor: UserDto,
        donor: UserDto,
        *,
        web_user: UserDto,
        telegram_user: UserDto,
    ) -> None:
        """
        Merge all data into the older account.

        All FK relations are re-pointed first, then the donor record is
        deleted to release unique constraints, and finally the survivor
        is updated with the merged fields.
        """
        self._apply_merged_fields(survivor, donor, web_user=web_user, telegram_user=telegram_user)

        await self._transfer_relations(survivor, donor)
        await self._delete_donor(donor)
        await self.user_dao.update(survivor)

        logger.debug(
            f"Full merge: donor id='{donor.id}' consolidated into survivor id='{survivor.id}'"
        )

    async def _transfer_relations(self, survivor: UserDto, donor: UserDto) -> None:
        """
        Re-point all FK relations from donor to survivor.

        Must be called before deleting donor to avoid FK violations.
        """
        # Clear current_subscription_id on donor so its FK to
        # subscriptions can be safely re-pointed to survivor.
        await self.user_dao.clear_current_subscription(
            donor.id  # ty: ignore[invalid-argument-type]
        )

        await self.subscription_dao.reassign_to_user(
            from_user_id=donor.id,  # ty: ignore[invalid-argument-type]
            to_user_id=survivor.id,  # ty: ignore[invalid-argument-type]
        )
        await self.transaction_dao.reassign_to_user(
            from_user_id=donor.id,  # ty: ignore[invalid-argument-type]
            to_user_id=survivor.id,  # ty: ignore[invalid-argument-type]
        )
        await self.referral_dao.reassign_referrer(
            from_user_id=donor.id,  # ty: ignore[invalid-argument-type]
            to_user_id=survivor.id,  # ty: ignore[invalid-argument-type]
        )
        await self.referral_dao.reassign_referred(
            from_user_id=donor.id,  # ty: ignore[invalid-argument-type]
            to_user_id=survivor.id,  # ty: ignore[invalid-argument-type]
        )

    async def _delete_donor(self, donor: UserDto) -> None:
        """Delete the donor account, choosing the right key based on what it has."""
        if donor.telegram_id is not None:
            await self.user_dao.delete(donor.telegram_id)  # ty: ignore[invalid-argument-type]
        else:
            await self.user_dao.delete_by_id(donor.id)  # ty: ignore[invalid-argument-type]

    @staticmethod
    def _apply_merged_fields(
        survivor: UserDto,
        donor: UserDto,
        *,
        web_user: UserDto,
        telegram_user: UserDto,
    ) -> None:
        """Merge scalar fields into the survivor."""
        survivor.telegram_id = telegram_user.telegram_id
        survivor.username = telegram_user.username
        survivor.email = web_user.email
        survivor.points += donor.points
        survivor.role = max(survivor.role, donor.role)
        survivor.personal_discount = max(survivor.personal_discount, donor.personal_discount)
        survivor.purchase_discount = max(survivor.purchase_discount, donor.purchase_discount)
        survivor.is_trial_available = survivor.is_trial_available or donor.is_trial_available

        if survivor.name == web_user.email:
            survivor.name = telegram_user.name


class NotifyNotConnectedWebUsers(Interactor[None, None]):
    """
    Weekly task: finds all web-only users registered in the last 7 days
    (has_only_email=True) and emails encouraging them to
    connect their Telegram account for subscription management.
    """

    required_permission = None

    def __init__(
        self,
        user_dao: UserDao,
        mailer: Mailer,
        bot_service: BotService,
    ) -> None:
        self.user_dao = user_dao
        self.mailer = mailer
        self.bot_service = bot_service

    async def _execute(self, actor: UserDto, data: None) -> None:
        users = await self.user_dao.get_new_web_only_users(days=7)

        logger.info(f"NotifyNotConnectedWebUsers: found {len(users)} candidate(s)")

        sent = 0
        for user in users:
            if not user.has_only_email or user.is_blocked:
                continue
            try:
                bot_url = await self.bot_service.get_connect_web_url(user.referral_code)
                await self.mailer.send_connect_telegram(user, bot_url)
                sent += 1
                logger.info(
                    f"NotifyNotConnectedWebUsers: sent email to user id='{user.id}' "
                    f"email='{user.email}'"
                )
            except Exception as exc:
                logger.error(
                    f"NotifyNotConnectedWebUsers: failed to send email to user "
                    f"id='{user.id}' email='{user.email}': {exc}"
                )

        logger.info(f"NotifyNotConnectedWebUsers: finished, sent {sent}/{len(users)} email(s)")
