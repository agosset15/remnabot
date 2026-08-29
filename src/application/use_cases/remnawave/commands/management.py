from dataclasses import dataclass
from datetime import timedelta

from loguru import logger

from src.application.common import Interactor
from src.application.common.dao import SettingsDao, SubscriptionDao, UserDao
from src.application.common.policy import Permission, PermissionPolicy
from src.application.common.remnawave import Remnawave
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.core.config import AppConfig
from src.core.enums import SubscriptionStatus
from src.core.exceptions import CooldownError, PermissionDeniedError
from src.core.types import RemnaUserDto
from src.core.utils.time import datetime_now


@dataclass(frozen=True)
class DeleteUserDeviceDto:
    user_id: int
    hwid: str


class DeleteUserDevice(Interactor[DeleteUserDeviceDto, bool]):
    required_permission = Permission.PUBLIC

    def __init__(
        self,
        subscription_dao: SubscriptionDao,
        remnawave: Remnawave,
        settings_dao: SettingsDao,
        uow: UnitOfWork,
    ) -> None:
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave
        self.settings_dao = settings_dao
        self.uow = uow

    async def _execute(self, actor: UserDto, data: DeleteUserDeviceDto) -> bool:
        is_self = data.user_id == actor.id
        if not is_self and not PermissionPolicy.has_permission(actor, Permission.USER_EDITOR):
            logger.warning(
                f"{actor.log} denied deleting device of foreign user '{data.user_id}' "
                f"without USER_EDITOR"
            )
            raise PermissionDeniedError()

        settings = await self.settings_dao.get()
        extra = settings.extra.device_single_reset

        if not extra.enabled:
            raise ValueError("Single device reset is disabled")

        current_subscription = await self.subscription_dao.get_current(data.user_id)
        if not current_subscription:
            raise ValueError(f"Subscription for user_id '{data.user_id}' not found")

        if extra.cooldown_hours > 0 and current_subscription.device_single_reset_at:
            available_at = current_subscription.device_single_reset_at + timedelta(
                hours=extra.cooldown_hours
            )
            if datetime_now() < available_at:
                raise CooldownError(available_at)

        async with self.uow:
            remaining_devices = await self.remnawave.delete_device(
                current_subscription.user_remna_id,
                data.hwid,
            )
            await self.remnawave.drop_connections(current_subscription.user_remna_id)
            current_subscription.device_single_reset_at = datetime_now()
            await self.subscription_dao.update(current_subscription)
            await self.uow.commit()

        logger.info(f"{actor.log} Deleted device '{data.hwid}' for user_id '{data.user_id}'")
        return bool(remaining_devices)


class DeleteUserAllDevices(Interactor[None, None]):
    required_permission = Permission.PUBLIC

    def __init__(
        self,
        subscription_dao: SubscriptionDao,
        remnawave: Remnawave,
        settings_dao: SettingsDao,
        uow: UnitOfWork,
    ) -> None:
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave
        self.settings_dao = settings_dao
        self.uow = uow

    async def _execute(self, actor: UserDto, data: None) -> None:
        settings = await self.settings_dao.get()
        extra = settings.extra.device_all_reset

        if not extra.enabled:
            raise ValueError("All devices reset is disabled")

        current_subscription = await self.subscription_dao.get_current(actor.id)
        if not current_subscription:
            raise ValueError(
                f"User '{actor.remna_name}' has no active subscription or device limit unlimited"
            )

        if extra.cooldown_hours > 0 and current_subscription.device_all_reset_at:
            available_at = current_subscription.device_all_reset_at + timedelta(
                hours=extra.cooldown_hours
            )
            if datetime_now() < available_at:
                raise CooldownError(available_at)

        async with self.uow:
            await self.remnawave.delete_all_devices(current_subscription.user_remna_id)
            await self.remnawave.drop_connections(current_subscription.user_remna_id)
            current_subscription.device_all_reset_at = datetime_now()
            await self.subscription_dao.update(current_subscription)
            await self.uow.commit()

        logger.info(f"{actor.log} Deleted all devices and dropped connections")


class ResetUserTraffic(Interactor[int, None]):
    required_permission = Permission.USER_EDITOR

    def __init__(
        self,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        remnawave: Remnawave,
    ) -> None:
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave

    async def _execute(self, actor: UserDto, user_id: int) -> None:
        target_user = await self.user_dao.get_by_id(user_id)
        if not target_user:
            raise ValueError(f"User '{user_id}' not found")

        subscription = await self.subscription_dao.get_current(target_user.id)
        if not subscription:
            raise ValueError(f"Subscription for user '{target_user.remna_name}' not found")

        try:
            await self.remnawave.reset_traffic(subscription.user_remna_id)
        except Exception as e:
            logger.error(
                f"Failed to reset traffic in Remnawave for user '{target_user.remna_name}': {e}"
            )
            raise

        logger.info(f"{actor.log} Reset traffic for user '{target_user.id}'")


class ReissueSubscription(Interactor[None, None]):
    required_permission = Permission.PUBLIC

    def __init__(
        self,
        subscription_dao: SubscriptionDao,
        remnawave: Remnawave,
        settings_dao: SettingsDao,
        uow: UnitOfWork,
    ) -> None:
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave
        self.settings_dao = settings_dao
        self.uow = uow

    async def _execute(self, actor: UserDto, data: None) -> None:
        settings = await self.settings_dao.get()
        extra = settings.extra.link_reset

        if not extra.enabled:
            raise ValueError("Subscription link reset is disabled")

        current_subscription = await self.subscription_dao.get_current(actor.id)
        if not current_subscription:
            raise ValueError(f"No active subscription for user '{actor.remna_name}'")

        if extra.cooldown_hours > 0 and current_subscription.link_reset_at:
            available_at = current_subscription.link_reset_at + timedelta(
                hours=extra.cooldown_hours
            )
            if datetime_now() < available_at:
                raise CooldownError(available_at)

        async with self.uow:
            await self.remnawave.revoke_subscription(current_subscription.user_remna_id)
            current_subscription.link_reset_at = datetime_now()
            await self.subscription_dao.update(current_subscription)
            await self.uow.commit()

        logger.info(f"{actor.log} Reissued subscription")


class ReissueUserSubscription(Interactor[int, None]):
    required_permission = Permission.USER_EDITOR

    def __init__(
        self, user_dao: UserDao, subscription_dao: SubscriptionDao, remnawave: Remnawave
    ) -> None:
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave

    async def _execute(self, actor: UserDto, user_id: int) -> None:
        target_user = await self.user_dao.get_by_id(user_id)
        if not target_user:
            raise ValueError(f"User '{user_id}' not found")

        current_subscription = await self.subscription_dao.get_current(target_user.id)

        if not current_subscription:
            raise ValueError(f"No active subscription for user '{target_user.remna_name}'")

        await self.remnawave.revoke_subscription(current_subscription.user_remna_id)

        logger.info(f"{actor.log} Reissued subscription for user '{target_user.id}'")


class ToggleLteSquad(Interactor[RemnaUserDto, None]):
    required_permission = Permission.USER_EDITOR

    def __init__(self, remnawave: Remnawave, config: AppConfig) -> None:
        self.remnawave = remnawave
        self.config = config

    async def _execute(self, actor: UserDto, data: RemnaUserDto) -> None:
        lte_squad_uuid = self.config.remnawave.lte_squad_uuid
        if not lte_squad_uuid:
            return

        internal_squads = {s.uuid for s in data.active_internal_squads}

        if data.status == SubscriptionStatus.LIMITED:
            if lte_squad_uuid not in internal_squads:
                return
            internal_squads.discard(lte_squad_uuid)
            await self.remnawave.update_user_internal_squads(data.uuid, list(internal_squads))
            logger.info(f"Excluded user '{data.uuid}' from LTE squad")
        else:
            if lte_squad_uuid in internal_squads:
                return
            internal_squads.add(lte_squad_uuid)
            await self.remnawave.update_user_internal_squads(data.uuid, list(internal_squads))
            logger.info(f"Returned user '{data.uuid}' to LTE squad")


class RestoreUsersToLteSquad(Interactor[None, None]):
    required_permission = None

    def __init__(
        self,
        remnawave: Remnawave,
        config: AppConfig,
        subscription_dao: SubscriptionDao,
    ) -> None:
        self.remnawave = remnawave
        self.config = config
        self.subscription_dao = subscription_dao

    async def _execute(self, actor: UserDto, data: None) -> None:
        lte_squad_uuid = self.config.remnawave.lte_squad_uuid
        if not lte_squad_uuid:
            return

        excluded = await self.subscription_dao.get_active_excluded_from_squad(lte_squad_uuid)
        if not excluded:
            logger.info("RestoreUsersToLteSquad: no excluded users found")
            return

        logger.info(f"RestoreUsersToLteSquad: restoring {len(excluded)} user(s) to LTE squad")
        restored = 0
        for sub in excluded:
            try:
                squads = [*sub.internal_squads, lte_squad_uuid]
                await self.remnawave.update_user_internal_squads(sub.user_remna_id, squads)
                restored += 1
            except Exception as exc:
                logger.error(f"RestoreUsersToLteSquad: failed for '{sub.user_remna_id}': {exc}")

        logger.info(f"RestoreUsersToLteSquad: restored {restored}/{len(excluded)}")
