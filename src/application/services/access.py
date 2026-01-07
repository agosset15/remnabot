from aiogram.types import CallbackQuery, TelegramObject
from aiogram_dialog.utils import remove_intent_id
from loguru import logger

from src.application.common import Notifier
from src.application.common.dao import SettingsDao, UserDao, WaitlistDao
from src.application.dto import SettingsDto, UserDto

# from src.application.services import ReferralService
from src.core.constants import PURCHASE_PREFIX
from src.core.enums import AccessMode


class AccessService:
    def __init__(
        self,
        user_dao: UserDao,
        waitlist_dao: WaitlistDao,
        settings_dao: SettingsDao,
        # referral_service: ReferralService,
        notifier: Notifier,
    ) -> None:
        self.user_dao = user_dao
        self.waitlist_dao = waitlist_dao
        self.settings_dao = settings_dao
        # self.referral_service = referral_service
        self.notifier = notifier

    async def check_user_access(self, telegram_id: int, event: TelegramObject) -> bool:
        user = await self.user_dao.get_by_telegram_id(telegram_id)
        settings = await self.settings_dao.get()

        if not user:
            return await self._handle_new_user(telegram_id, event, settings)

        if user.is_blocked:
            logger.info(f"Access denied for user '{telegram_id}' because they are blocked")
            return False

        if user.is_privileged:
            return True

        # проверка запрета покупок
        if self._is_purchase_action(event) and not settings.access.purchases_allowed:
            return await self._handle_purchase_denied(user)

        # проверка общего режима доступа
        if settings.access.mode == AccessMode.RESTRICTED:
            logger.info(f"Access denied for user '{telegram_id}' due to restricted mode")
            return False

        return True

    async def get_available_access_modes(self) -> list[AccessMode]:
        settings = await self.settings_dao.get()
        current_mode = settings.access.mode
        available = [mode for mode in AccessMode if mode != current_mode]
        logger.debug(f"Retrieved available access modes excluding current '{current_mode}'")
        return available

    async def notify_and_clear_waitlist(self) -> None:
        waiting_users = await self.waitlist_dao.get_waitlist_members()

        if not waiting_users:
            logger.debug("No users in waitlist to notify")
            return

        logger.info(f"Notifying '{len(waiting_users)}' users about access opening")

        # for user_id in waiting_users:
        #     try:
        #         await self.notifier.send_access_opened(user_id)
        #     except Exception as e:
        #         logger.error(f"Failed to notify user '{user_id}': {e}")

        await self.waitlist_dao.clear_waitlist()
        logger.info("Access waitlist has been cleared")

    async def _handle_new_user(
        self, telegram_id: int, event: TelegramObject, settings: SettingsDto
    ) -> bool:
        mode = settings.access.mode

        # проверка реферальной системы
        # if mode == AccessMode.INVITED:
        #     is_referral = await self.referral_service.is_referral_event(event, telegram_id)
        #     if is_referral:
        #         logger.info(f"Access allowed for referral event for user '{telegram_id}'")
        #         return True

        # запрет регистрации в определенных режимах
        if (
            mode in (AccessMode.INVITED, AccessMode.RESTRICTED)
            or not settings.access.registration_allowed
        ):
            logger.info(f"Access denied for new user '{telegram_id}' with mode '{mode}'")
            return False

        return True

    async def _handle_purchase_denied(self, user: UserDto) -> bool:
        logger.info(f"Access denied for user '{user.telegram_id}' for purchase action")

        if not await self.waitlist_dao.is_in_waitlist(user.telegram_id):
            await self.waitlist_dao.add_to_waitlist(user.telegram_id)
            logger.info(f"User '{user.telegram_id}' added to waitlist")

        return False

    def _is_purchase_action(self, event: TelegramObject) -> bool:
        if not isinstance(event, CallbackQuery) or not event.data:
            return False

        callback_data = remove_intent_id(event.data)
        if callback_data[-1].startswith(PURCHASE_PREFIX):
            logger.debug(f"Detected purchase action: {callback_data}")
            return True

        return False
