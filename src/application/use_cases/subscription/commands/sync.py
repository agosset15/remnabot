from loguru import logger
from remnapy import RemnawaveSDK
from remnapy.exceptions import NotFoundError

from src.application.common import Interactor, Remnawave
from src.application.common.dao import SubscriptionDao, UserDao
from src.application.common.policy import Permission
from src.application.common.uow import UnitOfWork
from src.application.dto import RemnaSubscriptionDto, UserDto
from src.application.use_cases.remnawave.commands.synchronization import (
    SyncRemnaUser,
    SyncRemnaUserDto,
)
from src.application.use_cases.subscription.queries.match import (
    MatchSubscription,
    MatchSubscriptionDto,
)
from src.core.enums import SubscriptionStatus


class CheckSubscriptionSyncState(Interactor[int, bool]):
    required_permission = Permission.USER_SYNC

    def __init__(
        self,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        remnawave_sdk: RemnawaveSDK,
        match_subscription: MatchSubscription,
    ):
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.remnawave_sdk = remnawave_sdk
        self.match_subscription = match_subscription

    async def _execute(self, actor: UserDto, user_id: int) -> bool:
        target_user = await self.user_dao.get_by_id(user_id)
        if not target_user:
            raise ValueError(f"User '{user_id}' not found")

        bot_sub = await self.subscription_dao.get_current(user_id)

        try:
            if target_user.email is not None:
                results = await self.remnawave_sdk.users.get_users_by_email(email=target_user.email)
            else:
                results = await self.remnawave_sdk.users.get_users_by_telegram_id(
                    telegram_id=str(target_user.telegram_id)
                )
            remna_sub = RemnaSubscriptionDto.from_remna_user(results[0]) if results else None
        except NotFoundError:
            remna_sub = None

        if not remna_sub and not bot_sub:
            raise ValueError(f"{actor.log} No subscription data found to check for '{user_id}'")

        if await self.match_subscription.system(MatchSubscriptionDto(bot_sub, remna_sub)):
            logger.info(f"{actor.log} Subscription data for '{user_id}' is consistent")
            return False

        logger.info(f"{actor.log} Inconsistency detected for user '{user_id}'")
        return True


class SyncSubscriptionFromRemnawave(Interactor[int, None]):
    required_permission = Permission.USER_SYNC

    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        remnawave_sdk: RemnawaveSDK,
        remnawave: Remnawave,
        sync_remna_user: SyncRemnaUser,
    ):
        self.uow = uow
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.remnawave_sdk = remnawave_sdk
        self.remnawave = remnawave
        self.sync_remna_user = sync_remna_user

    async def _execute(self, actor: UserDto, user_id: int) -> None:
        async with self.uow:
            target_user = await self.user_dao.get_by_id(user_id)
            if not target_user:
                raise ValueError(f"User '{user_id}' not found")

            subscription = await self.subscription_dao.get_current(user_id)

            try:
                if target_user.email is not None:
                    results = await self.remnawave_sdk.users.get_users_by_email(
                        email=target_user.email
                    )
                else:
                    results = await self.remnawave_sdk.users.get_users_by_telegram_id(
                        telegram_id=str(target_user.telegram_id)
                    )
                remna_user = results[0] if results else None
            except NotFoundError:
                remna_user = None

            if not remna_user:
                if subscription:
                    await self.subscription_dao.update_status(
                        subscription.id,  # type: ignore[arg-type]
                        SubscriptionStatus.DELETED,
                    )
                await self.user_dao.clear_current_subscription(user_id)
                logger.info(
                    f"{actor.log} Deleted subscription for '{user_id}' "
                    f"because it missing in Remnawave"
                )
            else:
                await self.sync_remna_user.system(SyncRemnaUserDto(remna_user, creating=False))
                logger.info(
                    f"{actor.log} Synchronized subscription from remnapy for user '{user_id}'"
                )

            await self.uow.commit()


class SyncSubscriptionFromRemnashop(Interactor[int, None]):
    required_permission = Permission.USER_SYNC

    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        remnawave: Remnawave,
        sync_remna_user: SyncRemnaUser,
    ):
        self.uow = uow
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave
        self.sync_remna_user = sync_remna_user

    async def _execute(self, actor: UserDto, user_id: int) -> None:
        async with self.uow:
            target_user = await self.user_dao.get_by_id(user_id)
            if not target_user:
                raise ValueError(f"User '{user_id}' not found")

            subscription = await self.subscription_dao.get_current(user_id)

            if not subscription:
                remna_users = await self.remnawave.get_user_by_telegram_id(target_user.telegram_id)

                if not remna_users:
                    return

                await self.remnawave.delete_user(remna_users[0].uuid)
                logger.info(
                    f"{actor.log} Deleted user '{remna_users[0].uuid}' from remnapy "
                    f"due to missing local subscription"
                )
            else:
                remna_user = await self.remnawave.get_user_by_uuid(subscription.user_remna_id)

                if remna_user:
                    await self.remnawave.update_user(
                        user=target_user,
                        uuid=subscription.user_remna_id,
                        subscription=subscription,
                    )
                    logger.info(
                        f"{actor.log} Updated user '{user_id}' in Remnawave with local data"
                    )
                else:
                    created_user = await self.remnawave.create_user(
                        user=target_user,
                        subscription=subscription,
                    )
                    await self.sync_remna_user.system(
                        SyncRemnaUserDto(created_user, creating=False)
                    )
                    logger.info(
                        f"{actor.log} Recreated user '{user_id}' in Remnawave with local data"
                    )

            await self.uow.commit()
