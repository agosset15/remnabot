from datetime import timedelta
from enum import StrEnum

from loguru import logger
from remnapy.models.webhook import HwidUserDeviceDto, NodeDto

from src.application.common import EventPublisher
from src.application.common.dao import SubscriptionDao, UserDao
from src.application.common.uow import UnitOfWork
from src.application.dto import SubscriptionDto, UserDto
from src.application.events import (
    NodeConnectionLostEvent,
    NodeConnectionRestoredEvent,
    NodeTrafficReachedEvent,
    SubscriptionExpiredEvent,
    SubscriptionExpiresEvent,
    SubscriptionLimitedEvent,
    UserDeviceAddedEvent,
    UserDeviceDeletedEvent,
    UserFirstConnectionEvent,
)
from src.application.events.system import SubscriptionRevokedEvent
from src.application.events.user import SubscriptionExpiredAgoEvent
from src.application.use_cases.remnawave.commands.management import ToggleLteSquad
from src.application.use_cases.remnawave.commands.synchronization import (
    SyncRemnaUser,
    SyncRemnaUserDto,
)
from src.core.constants import DATETIME_FORMAT, IMPORTED_TAG
from src.core.enums import SubscriptionStatus
from src.core.types import RemnaUserDto
from src.core.utils.converters import country_code_to_flag
from src.core.utils.i18n_helpers import (
    i18n_format_bytes_to_unit,
    i18n_format_device_limit,
    i18n_format_expire_time,
)
from src.core.utils.i18n_keys import ByteUnitKey
from src.core.utils.time import datetime_now, get_traffic_reset_delta

_EXPIRATION_GRACE_PERIOD = timedelta(days=3)


class RemnaWebhookService:
    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        event_bus: EventPublisher,
        sync_user: SyncRemnaUser,
        toggle_lte_squad: ToggleLteSquad,
    ) -> None:
        self.uow = uow
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.event_bus = event_bus
        self.sync_user = sync_user
        self.toggle_lte_squad = toggle_lte_squad

    # -------------------------------------------------------------------------
    # Public entry points
    # -------------------------------------------------------------------------

    async def handle_user_event(self, event: str, remna_user: RemnaUserDto) -> None:
        logger.debug(f"Received user event '{event}'")

        if not remna_user.telegram_id and not remna_user.email:
            logger.debug(
                f"Skipping event for RemnaUser '{remna_user.username}': "
                "telegram_id and email are both empty"
            )
            return

        if event in {RemnaUserEvent.CREATED, RemnaUserEvent.MODIFIED}:
            await self._handle_sync_event(event, remna_user)
            return

        user = await self.user_dao.get_by_telegram_id_or_email(
            remna_user.telegram_id, remna_user.email
        )
        if not user:
            logger.warning(
                f"Local user not found with telegram_id='{remna_user.telegram_id}' "
                f"or email='{remna_user.email}'"
            )
            return

        current_subscription = await self.subscription_dao.get_current(user.id)
        if not current_subscription:
            logger.warning(
                f"Current subscription not found for user '{user.id}'; aborting event '{event}'"
            )
            return

        await self._dispatch_user_event(event, remna_user, user, current_subscription)

    async def handle_device_event(
        self,
        event: str,
        remna_user: RemnaUserDto,
        device: HwidUserDeviceDto,
    ) -> None:
        logger.info(f"Received device event '{event}' for RemnaUser '{remna_user.telegram_id}'")

        if not remna_user.telegram_id:
            return

        user = await self.user_dao.get_by_telegram_id(remna_user.telegram_id)
        if not user:
            logger.warning(f"Local user not found for telegram_id '{remna_user.telegram_id}'")
            return

        await self._dispatch_device_event(event, user, device)

    async def handle_node_event(self, event: str, node: NodeDto) -> None:
        logger.info(f"Received node event '{event}' for node '{node.name}'")

        node_event_map = {
            RemnaNodeEvent.CONNECTION_LOST.value: NodeConnectionLostEvent,
            RemnaNodeEvent.CONNECTION_RESTORED.value: NodeConnectionRestoredEvent,
            RemnaNodeEvent.TRAFFIC_NOTIFY.value: NodeTrafficReachedEvent,
        }

        event_class = node_event_map.get(event)
        if not event_class:
            logger.warning(f"Unhandled node event '{event}' for node '{node.name}'")
            return

        await self.event_bus.publish(
            event_class(
                country=country_code_to_flag(code=node.country_code),
                name=node.name,
                address=node.address,
                port=node.port,
                traffic_used=i18n_format_bytes_to_unit(node.traffic_used_bytes),
                traffic_limit=i18n_format_bytes_to_unit(node.traffic_limit_bytes),
                last_status_message=node.last_status_message,
                last_status_change=(
                    node.last_status_change.strftime(DATETIME_FORMAT)
                    if node.last_status_change
                    else None
                ),
            )
        )

    # -------------------------------------------------------------------------
    # User event dispatchers
    # -------------------------------------------------------------------------

    async def _dispatch_user_event(
        self,
        event: str,
        remna_user: RemnaUserDto,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        if event == RemnaUserEvent.DELETED:
            await self._handle_delete_event(user, remna_user)

        elif event in {
            RemnaUserEvent.REVOKED,
            RemnaUserEvent.ENABLED,
            RemnaUserEvent.DISABLED,
            RemnaUserEvent.LIMITED,
            RemnaUserEvent.EXPIRED,
        }:
            await self._handle_status_event(event, remna_user, user, current_subscription)

        elif event == RemnaUserEvent.TRAFFIC_RESET:
            await self._handle_traffic_reset_event(remna_user, current_subscription)

        elif event == RemnaUserEvent.EXPIRED_24_HOURS_AGO:
            await self._handle_expired_ago_event(user, current_subscription)

        elif event in _EXPIRES_IN_DAYS:
            await self._handle_expires_soon_event(event, user, current_subscription)

        elif event == RemnaUserEvent.FIRST_CONNECTED:
            await self._handle_first_connection_event(remna_user, user, current_subscription)

        else:
            logger.warning(f"Unhandled user event '{event}' for user '{user.id}'")

    async def _dispatch_device_event(
        self,
        event: str,
        user: UserDto,
        device: HwidUserDeviceDto,
    ) -> None:
        device_event_map = {
            RemnaUserHwidDevicesEvent.ADDED.value: UserDeviceAddedEvent,
            RemnaUserHwidDevicesEvent.DELETED.value: UserDeviceDeletedEvent,
        }

        event_class = device_event_map.get(event)
        if not event_class:
            logger.warning(f"Unhandled device event '{event}' for user '{user.id}'")
            return

        await self.event_bus.publish(
            event_class(
                user_id=user.id,
                telegram_id=user.telegram_id,
                username=user.username,
                name=user.name,
                hwid=device.hwid,
                platform=device.platform,
                device_model=device.device_model,
                os_version=device.os_version,
                user_agent=device.user_agent,
            )
        )

    # -------------------------------------------------------------------------
    # User event handlers
    # -------------------------------------------------------------------------

    async def _handle_sync_event(self, event: str, remna_user: RemnaUserDto) -> None:
        if event == RemnaUserEvent.CREATED and remna_user.tag != IMPORTED_TAG:
            logger.debug(
                f"Ignoring RemnaUser '{remna_user.telegram_id}': not tagged as '{IMPORTED_TAG}'"
            )
            return

        logger.debug(f"Syncing user '{remna_user.telegram_id}' on event '{event}'")
        await self.sync_user.system(
            SyncRemnaUserDto(remna_user=remna_user, creating=(event == RemnaUserEvent.CREATED))
        )

    async def _handle_delete_event(self, user: UserDto, remna_user: RemnaUserDto) -> None:
        logger.debug(f"Processing deletion for user '{user.id}'")
        async with self.uow:
            subscription = await self.subscription_dao.get_by_remna_id(remna_user.uuid)
            if not subscription:
                logger.warning(
                    f"Subscription not found for UUID '{remna_user.uuid}'; delete aborted"
                )
                return

            subscription.status = SubscriptionStatus.DELETED
            await self.subscription_dao.update(subscription)

            await self._unlink_current_subscription_if_needed(user, subscription)
            await self.uow.commit()

        logger.info(f"Deletion processed for subscription '{remna_user.uuid}'")

    async def _handle_status_event(
        self,
        event: str,
        remna_user: RemnaUserDto,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        await self.sync_user.system(SyncRemnaUserDto(remna_user=remna_user, creating=False))

        if event == RemnaUserEvent.LIMITED:
            await self._publish_limited_event(remna_user, user, current_subscription)
            await self.toggle_lte_squad.system(remna_user)

        elif event == RemnaUserEvent.EXPIRED:
            await self._publish_expired_event_if_recent(remna_user, user, current_subscription)

        elif event == RemnaUserEvent.REVOKED:
            await self._publish_revoked_event(remna_user, user, current_subscription)

    async def _handle_traffic_reset_event(
        self,
        remna_user: RemnaUserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        if current_subscription.current_status == SubscriptionStatus.LIMITED:
            await self.toggle_lte_squad.system(remna_user)

    async def _handle_expired_ago_event(
        self,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        await self.event_bus.publish(
            SubscriptionExpiredAgoEvent(
                user=user,
                is_trial=current_subscription.is_trial,
                day=1,
            )
        )

    async def _handle_expires_soon_event(
        self,
        event: str,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        await self.event_bus.publish(
            SubscriptionExpiresEvent(
                day=_EXPIRES_IN_DAYS[event],
                user=user,
                is_trial=current_subscription.is_trial,
            )
        )

    async def _handle_first_connection_event(
        self,
        remna_user: RemnaUserDto,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        await self.event_bus.publish(
            UserFirstConnectionEvent(
                user_id=user.id,
                telegram_id=user.telegram_id,
                email=user.email,
                username=user.username,
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

    # -------------------------------------------------------------------------
    # Event publishers
    # -------------------------------------------------------------------------

    async def _publish_limited_event(
        self,
        remna_user: RemnaUserDto,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        await self.event_bus.publish(
            SubscriptionLimitedEvent(
                user=user,
                is_trial=current_subscription.is_trial,
                traffic_strategy=current_subscription.traffic_limit_strategy,
                reset_time=i18n_format_expire_time(
                    get_traffic_reset_delta(current_subscription.traffic_limit_strategy)
                ),
            )
        )

    async def _publish_expired_event_if_recent(
        self,
        remna_user: RemnaUserDto,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        if remna_user.expire_at + _EXPIRATION_GRACE_PERIOD < datetime_now():
            logger.debug(
                f"Skipping expiration notification for '{remna_user.telegram_id}': "
                "more than 3 days have passed since expiry"
            )
            return

        await self.event_bus.publish(
            SubscriptionExpiredEvent(user=user, is_trial=current_subscription.is_trial)
        )

    async def _publish_revoked_event(
        self,
        remna_user: RemnaUserDto,
        user: UserDto,
        current_subscription: SubscriptionDto,
    ) -> None:
        await self.event_bus.publish(
            SubscriptionRevokedEvent(
                user_id=user.id,
                telegram_id=user.telegram_id,
                username=user.username,
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

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    async def _unlink_current_subscription_if_needed(
        self, user: UserDto, deleted_subscription: SubscriptionDto
    ) -> None:
        current_subscription = await self.subscription_dao.get_current(user.id)
        if not current_subscription:
            return

        if current_subscription.user_remna_id != deleted_subscription.user_remna_id:
            logger.debug(
                f"Deleted subscription '{deleted_subscription.user_remna_id}' "
                f"is not current for user '{user.id}'; skipping unlink"
            )
            return

        await self.user_dao.clear_current_subscription(user.id)
        logger.debug(f"Unlinked current subscription for user '{user.id}'")


# ---------------------------------------------------------------------------
# Event enums
# ---------------------------------------------------------------------------


class RemnaUserEvent(StrEnum):
    CREATED = "user.created"
    MODIFIED = "user.modified"
    DELETED = "user.deleted"
    REVOKED = "user.revoked"
    DISABLED = "user.disabled"
    ENABLED = "user.enabled"
    LIMITED = "user.limited"
    EXPIRED = "user.expired"

    TRAFFIC_RESET = "user.traffic_reset"
    NOT_CONNECTED = "user.not_connected"
    FIRST_CONNECTED = "user.first_connected"
    BANDWIDTH_USAGE_THRESHOLD_REACHED = "user.bandwidth_usage_threshold_reached"

    EXPIRES_IN_72_HOURS = "user.expires_in_72_hours"
    EXPIRES_IN_48_HOURS = "user.expires_in_48_hours"
    EXPIRES_IN_24_HOURS = "user.expires_in_24_hours"
    EXPIRED_24_HOURS_AGO = "user.expired_24_hours_ago"


_EXPIRES_IN_DAYS: dict[str, int] = {
    RemnaUserEvent.EXPIRES_IN_72_HOURS: 3,
    RemnaUserEvent.EXPIRES_IN_48_HOURS: 2,
    RemnaUserEvent.EXPIRES_IN_24_HOURS: 1,
}


class RemnaUserHwidDevicesEvent(StrEnum):
    ADDED = "user_hwid_devices.added"
    DELETED = "user_hwid_devices.deleted"


class RemnaNodeEvent(StrEnum):
    CREATED = "node.created"
    MODIFIED = "node.modified"
    DISABLED = "node.disabled"
    ENABLED = "node.enabled"
    DELETED = "node.deleted"
    CONNECTION_LOST = "node.connection_lost"
    CONNECTION_RESTORED = "node.connection_restored"
    TRAFFIC_NOTIFY = "node.traffic_notify"


class RemnaServiceEvent(StrEnum):
    PANEL_STARTED = "service.panel_started"
    LOGIN_ATTEMPT_FAILED = "service.login_attempt_failed"
    LOGIN_ATTEMPT_SUCCESS = "service.login_attempt_success"


class RemnaCrmEvent(StrEnum):
    INFRA_BILLING_NODE_PAYMENT_IN_7_DAYS = "crm.infra_billing_node_payment_in_7_days"
    INFRA_BILLING_NODE_PAYMENT_IN_48HRS = "crm.infra_billing_node_payment_in_48hrs"
    INFRA_BILLING_NODE_PAYMENT_IN_24HRS = "crm.infra_billing_node_payment_in_24hrs"
    INFRA_BILLING_NODE_PAYMENT_DUE_TODAY = "crm.infra_billing_node_payment_due_today"
    INFRA_BILLING_NODE_PAYMENT_OVERDUE_24HRS = "crm.infra_billing_node_payment_overdue_24hrs"
    INFRA_BILLING_NODE_PAYMENT_OVERDUE_48HRS = "crm.infra_billing_node_payment_overdue_48hrs"
    INFRA_BILLING_NODE_PAYMENT_OVERDUE_7_DAYS = "crm.infra_billing_node_payment_overdue_7_days"
