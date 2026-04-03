from dataclasses import dataclass
from typing import Optional

from loguru import logger

from src.application.common import Interactor
from src.application.common.dao import ReferralDao, SubscriptionDao, TransactionDao, UserDao
from src.application.common.policy import Permission
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto


@dataclass
class ConnectWebUserDto:
    telegram_user: UserDto
    referral_code: str


class ConnectWebUser(Interactor[ConnectWebUserDto, Optional[UserDto]]):
    required_permission = Permission.PUBLIC

    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        transaction_dao: TransactionDao,
        referral_dao: ReferralDao,
    ) -> None:
        self.uow = uow
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.transaction_dao = transaction_dao
        self.referral_dao = referral_dao

    async def _execute(self, actor: UserDto, data: ConnectWebUserDto) -> Optional[UserDto]:
        web_user = await self.user_dao.get_by_referral_code(data.referral_code)

        if not web_user:
            logger.warning(f"Connect web: no user found for referral_code='{data.referral_code}'")
            return None

        if self._is_already_connected(web_user, data.telegram_user):
            logger.debug(f"Connect web: {web_user.log} is already connected")
            return web_user

        telegram_user = data.telegram_user

        async with self.uow:
            if self._has_substantial_data(telegram_user):
                await self._full_merge(web_user, telegram_user)
            else:
                await self._simple_connect(web_user, telegram_user)
            await self.uow.commit()

        logger.info(f"Connect web: {telegram_user.log} → merged into web user id='{web_user.id}'")
        return await self.user_dao.get_by_id(web_user.id)  # ty: ignore[invalid-argument-type]

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
        return user.is_trial_available

    # ──────────────────────────────────────────────────────────────────────────
    # Connect strategies
    # ──────────────────────────────────────────────────────────────────────────

    async def _simple_connect(self, web_user: UserDto, telegram_user: UserDto) -> None:
        """Attach telegram_id to the web account and remove the empty stub record."""
        web_user.telegram_id = telegram_user.telegram_id
        web_user.username = telegram_user.username

        if web_user.name == web_user.email:
            web_user.name = telegram_user.name

        await self.user_dao.update(web_user)
        await self.user_dao.delete(telegram_user.telegram_id)  # ty: ignore[invalid-argument-type]

        logger.debug(
            f"Simple connect: telegram_id='{telegram_user.telegram_id}' "
            f"attached to web user id='{web_user.id}'"
        )

    async def _full_merge(self, web_user: UserDto, telegram_user: UserDto) -> None:
        """
        Merge all data from the Telegram user into the web account.

        Order of operations matters: FKs referencing telegram_user must be
        re-pointed before the record can be deleted.
        """
        self._apply_merged_fields(web_user, telegram_user)

        # Detach current_subscription_id so the FK to subscriptions can be re-pointed
        await self.user_dao.clear_current_subscription(
            telegram_user.telegram_id  # ty: ignore[invalid-argument-type]
        )

        await self.subscription_dao.reassign_to_user(
            from_user_id=telegram_user.id,  # ty: ignore[invalid-argument-type]
            to_user_id=web_user.id,  # ty: ignore[invalid-argument-type]
        )
        await self.transaction_dao.reassign_to_user(
            from_user_id=telegram_user.id,  # ty: ignore[invalid-argument-type]
            to_user_id=web_user.id,  # ty: ignore[invalid-argument-type]
        )
        await self.referral_dao.reassign_referrer(
            from_user_id=telegram_user.id,  # ty: ignore[invalid-argument-type]
            to_user_id=web_user.id,  # ty: ignore[invalid-argument-type]
        )
        await self.referral_dao.reassign_referred(
            from_user_id=telegram_user.id,  # ty: ignore[invalid-argument-type]
            to_user_id=web_user.id,  # ty: ignore[invalid-argument-type]
        )

        await self.user_dao.update(web_user)
        await self.user_dao.delete(telegram_user.telegram_id)  # ty: ignore[invalid-argument-type]

        logger.debug(
            f"Full merge: telegram user id='{telegram_user.id}' "
            f"consolidated into web user id='{web_user.id}'"
        )

    @staticmethod
    def _apply_merged_fields(web_user: UserDto, telegram_user: UserDto) -> None:
        """Merge scalar fields from telegram_user into web_user."""
        web_user.telegram_id = telegram_user.telegram_id
        web_user.username = telegram_user.username
        web_user.points += telegram_user.points
        web_user.role = max(web_user.role, telegram_user.role)
        web_user.personal_discount = max(
            web_user.personal_discount, telegram_user.personal_discount
        )
        web_user.purchase_discount = max(
            web_user.purchase_discount, telegram_user.purchase_discount
        )
        web_user.is_trial_available = (
            web_user.is_trial_available or telegram_user.is_trial_available
        )

        if web_user.name == web_user.email:
            web_user.name = telegram_user.name
