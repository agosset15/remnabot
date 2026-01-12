from dataclasses import dataclass

from aiogram import Bot
from aiogram_dialog import BgManagerFactory, ShowMode, StartMode
from loguru import logger

from src.application.common import Interactor, Notifier
from src.application.common.dao import UserDao
from src.application.dto import UserDto
from src.telegram.states import MainMenu


@dataclass(frozen=True)
class RedirectMenuDto:
    telegram_id: int


class RedirectMenu(Interactor[RedirectMenuDto, None]):
    def __init__(
        self,
        user_dao: UserDao,
        bot: Bot,
        bg_manager_factory: BgManagerFactory,
        notifier: Notifier,
    ) -> None:
        self.user_dao = user_dao
        self.bot = bot
        self.bg_manager_factory = bg_manager_factory
        self.notifier = notifier

    async def _execute(self, actor: UserDto, data: RedirectMenuDto) -> None:
        user = await self.user_dao.get_by_telegram_id(data.telegram_id)

        if user is None:
            logger.warning(f"User with telegram_id '{data.telegram_id}' not found for redirection")
            return

        if user.is_privileged:
            await self.notifier.notify_user(user, i18n_key="ntf-error.lost-context")
            logger.debug(f"Skipping redirection for privileged user '{data.telegram_id}'")
            return

        await self.notifier.notify_user(user, i18n_key="ntf-error.lost-context-restart")

        bg_manager = self.bg_manager_factory.bg(
            bot=self.bot,
            user_id=data.telegram_id,
            chat_id=data.telegram_id,
        )
        await bg_manager.start(
            state=MainMenu.MAIN,
            mode=StartMode.RESET_STACK,
            show_mode=ShowMode.DELETE_AND_SEND,
        )
        logger.info(f"Redirected user '{data.telegram_id}' to main menu")
