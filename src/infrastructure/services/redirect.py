from aiogram_dialog import BaseDialogManager, BgManagerFactory, ShowMode, StartMode
from loguru import logger

from src.application.common import Redirect
from src.application.common.dao import UserDao
from src.core.constants import TARGET_USER_ID
from src.core.enums import PurchaseType
from src.telegram.states import DashboardUser, MainMenu, Subscription

from .bot_registry import BotRegistry


class RedirectImpl(Redirect):
    def __init__(
        self,
        bots: BotRegistry,
        bg_manager_factory: BgManagerFactory,
        user_dao: UserDao,
    ) -> None:
        self.bots = bots
        self.bg_manager_factory = bg_manager_factory
        self.user_dao = user_dao

    async def _bg(self, telegram_id: int) -> BaseDialogManager:
        # Redirects are fired from background tasks: route through the user's own bot,
        # since that is where their dialog stack lives and the only bot they can receive from.
        user = await self.user_dao.get_by_telegram_id(telegram_id)
        return self.bg_manager_factory.bg(
            bot=self.bots.for_user(user),
            user_id=telegram_id,
            chat_id=telegram_id,
        )

    async def to_main_menu(self, telegram_id: int) -> None:
        bg_manager = await self._bg(telegram_id)

        await bg_manager.start(
            state=MainMenu.MAIN,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"User '{telegram_id}' redirected to main menu")

    async def to_user_editor(self, telegram_id: int, target_user_id: int) -> None:
        bg_manager = await self._bg(telegram_id)

        await bg_manager.start(
            state=DashboardUser.MAIN,
            data={TARGET_USER_ID: target_user_id},
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"User '{telegram_id}' redirected to user editor")

    async def to_success_trial(self, telegram_id: int) -> None:
        bg_manager = await self._bg(telegram_id)

        await bg_manager.start(
            state=Subscription.TRIAL,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"User '{telegram_id}' redirected to success trial")

    async def to_success_payment(self, telegram_id: int, purchase_type: PurchaseType) -> None:
        bg_manager = await self._bg(telegram_id)

        await bg_manager.start(
            state=Subscription.SUCCESS,
            data={"purchase_type": purchase_type},
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"User '{telegram_id}' redirected to success payment")

    async def to_failed_payment(self, telegram_id: int) -> None:
        bg_manager = await self._bg(telegram_id)

        await bg_manager.start(
            state=Subscription.FAILED,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"User '{telegram_id}' redirected to failed payment")
