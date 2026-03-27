from dataclasses import dataclass

from loguru import logger
from remnapy import RemnawaveSDK
from remnapy.models import DeleteUserAllHwidDeviceRequestDto

from src.application.common import Interactor
from src.application.common.dao import SubscriptionDao
from src.application.common.policy import Permission
from src.application.common.remnawave import Remnawave
from src.application.dto import UserDto
from src.core.config import AppConfig
from src.core.enums import SubscriptionStatus
from src.core.types import RemnaUserDto


@dataclass(frozen=True)
class DeleteUserDeviceDto:
    telegram_id: int
    hwid: str


class DeleteUserDevice(Interactor[DeleteUserDeviceDto, bool]):
    required_permission = Permission.PUBLIC

    def __init__(self, subscription_dao: SubscriptionDao, remnawave: Remnawave):
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave

    async def _execute(self, actor: UserDto, data: DeleteUserDeviceDto) -> bool:
        current_subscription = await self.subscription_dao.get_current(data.telegram_id)

        if not current_subscription:
            raise ValueError(f"Subscription for user '{data.telegram_id}' not found")

        remaining_devices = await self.remnawave.delete_device(
            current_subscription.user_remna_id,
            data.hwid,
        )

        logger.info(f"{actor.log} Deleted device '{data.hwid}' for user '{data.telegram_id}'")
        return bool(remaining_devices)


class DeleteUserAllDevices(Interactor[None, None]):
    required_permission = Permission.PUBLIC

    def __init__(self, subscription_dao: SubscriptionDao, remnawave_sdk: RemnawaveSDK) -> None:
        self.subscription_dao = subscription_dao
        self.remnawave_sdk = remnawave_sdk

    async def _execute(self, actor: UserDto, data: None) -> None:
        current_subscription = await self.subscription_dao.get_current(actor.telegram_id)

        if not current_subscription:
            raise ValueError(
                f"User '{actor.telegram_id}' has no active subscription or device limit unlimited"
            )

        result = await self.remnawave_sdk.hwid.delete_all_hwid_user(
            DeleteUserAllHwidDeviceRequestDto(user_uuid=current_subscription.user_remna_id)
        )

        logger.info(f"{actor.log} Deleted all devices ({result.total})")


class ResetUserTraffic(Interactor[int, None]):
    required_permission = Permission.USER_EDITOR

    def __init__(
        self,
        subscription_dao: SubscriptionDao,
        remnawave_sdk: RemnawaveSDK,
    ):
        self.subscription_dao = subscription_dao
        self.remnawave_sdk = remnawave_sdk

    async def _execute(self, actor: UserDto, data: int) -> None:
        subscription = await self.subscription_dao.get_current(data)
        if not subscription:
            raise ValueError(f"Subscription for user '{data}' not found")

        try:
            await self.remnawave_sdk.users.reset_user_traffic(subscription.user_remna_id)
        except Exception as e:
            logger.error(f"Failed to reset traffic in Remnawave for user '{data}': {e}")
            raise

        logger.info(f"{actor.log} Reset traffic for user '{data}'")


class ReissueSubscription(Interactor[None, None]):
    required_permission = Permission.PUBLIC

    def __init__(self, subscription_dao: SubscriptionDao, remnawave: Remnawave) -> None:
        self.subscription_dao = subscription_dao
        self.remnawave = remnawave

    async def _execute(self, actor: UserDto, data: None) -> None:
        current_subscription = await self.subscription_dao.get_current(actor.telegram_id)

        if not current_subscription:
            raise ValueError(f"No active subscription for user '{actor.telegram_id}'")

        await self.remnawave.revoke_subscription(current_subscription.user_remna_id)

        logger.info(f"{actor.log} Reissued subscription")


class ToggleLteSquad(Interactor[RemnaUserDto, None]):
    required_permission = Permission.USER_EDITOR

    def __init__(
        self, remnawave: Remnawave, config: AppConfig, subscription_dao: SubscriptionDao
    ) -> None:
        self.remnawave = remnawave
        self.config = config
        self.subscription_dao = subscription_dao

    async def _execute(self, actor: UserDto, data: RemnaUserDto) -> None:
        if not self.config.remnawave.lte_squad_uuid:
            return

        internal_squads = {s.uuid for s in data.active_internal_squads}
        lte_squad_uuid = self.config.remnawave.lte_squad_uuid

        if lte_squad_uuid in internal_squads:
            internal_squads.discard(lte_squad_uuid)
            await self.remnawave.reset_traffic(data.uuid)
        elif data.status == SubscriptionStatus.ACTIVE:
            internal_squads.add(lte_squad_uuid)

        await self.remnawave.update_user_internal_squads(data.uuid, list(internal_squads))
        logger.info(f"Toggled LTE squad for user '{data.uuid}'")
