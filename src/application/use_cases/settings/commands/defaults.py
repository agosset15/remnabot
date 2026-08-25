from loguru import logger

from src.application.common import Interactor
from src.application.common.dao import SettingsDao
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.core.config import AppConfig


class CreateDefaultSettings(Interactor[None, None]):
    required_permission = None

    def __init__(self, uow: UnitOfWork, settings_dao: SettingsDao) -> None:
        self.uow = uow
        self.settings_dao = settings_dao

    async def _execute(self, actor: UserDto, data: None) -> None:
        async with self.uow:
            if await self.settings_dao.exists():
                return

            await self.settings_dao.create_default()
            await self.uow.commit()

        logger.info("Created default settings")


class ApplyConfigNotificationRoutes(Interactor[None, None]):
    """Seed notification routes from BOT_notifications_* config at startup.

    When BOT_notifications_chat_id is set, config is authoritative: the shared
    chat and the per-category thread ids (user/node/bot) are applied onto the
    system notification routes and the default_route on every startup. When it is
    unset, routes are left untouched (managed via the admin dashboard).
    """

    required_permission = None

    def __init__(self, uow: UnitOfWork, settings_dao: SettingsDao, config: AppConfig) -> None:
        self.uow = uow
        self.settings_dao = settings_dao
        self.config = config

    async def _execute(self, actor: UserDto, data: None) -> None:
        bot = self.config.bot
        if bot.notifications_chat_id is None:
            return

        async with self.uow:
            settings = await self.settings_dao.get()
            changed = settings.notifications.apply_config_routes(
                bot.notifications_chat_id,
                user_thread_id=bot.notifications_user_thread_id,
                node_thread_id=bot.notifications_node_thread_id,
                bot_thread_id=bot.notifications_bot_thread_id,
            )

            if not changed:
                return

            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(
            f"Applied config notification routes (chat={bot.notifications_chat_id}, "
            f"user_thread={bot.notifications_user_thread_id}, "
            f"node_thread={bot.notifications_node_thread_id}, "
            f"bot_thread={bot.notifications_bot_thread_id})"
        )
