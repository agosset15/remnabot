from typing import Optional

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from loguru import logger

from src.application.common import TranslatorHub
from src.core.config import AppConfig
from src.core.enums import Command, Locale

from .bot_registry import BotRegistry


class CommandService:
    def __init__(
        self,
        bots: BotRegistry,
        config: AppConfig,
        translator_hub: TranslatorHub,
    ) -> None:
        self.bots = bots
        self.config = config
        self.translator_hub = translator_hub

    async def setup_commands(self) -> None:
        for bot in self.bots.all():
            await self._setup_commands(bot)

    async def delete_commands(self) -> None:
        for bot in self.bots.all():
            await self._delete_commands(bot)

    async def _setup_commands(self, bot: Bot) -> None:
        if not self.config.bot.setup_commands:
            logger.debug("Bot commands setup is disabled")
            await self._delete_commands(bot)
            return

        locales: list[Optional[Locale]] = list(self.config.locales) + [None]

        for lang in locales:
            display_lang = lang if lang else "default"

            i18n = self.translator_hub.get_translator_by_locale(
                locale=lang or self.config.default_locale
            )

            commands = [
                BotCommand(
                    command=cmd.value.command,
                    description=i18n.get(cmd.value.description),
                )
                for cmd in Command
            ]

            success = await bot.set_my_commands(
                commands=commands,
                scope=BotCommandScopeAllPrivateChats(),
                language_code=lang,
            )

            if success:
                cmd_list = [c.command for c in commands]
                logger.info(
                    f"Commands set for bot '{bot.id}' language '{display_lang}': '{cmd_list}'"
                )
            else:
                logger.error(f"Failed to set commands for bot '{bot.id}' language '{display_lang}'")

    async def _delete_commands(self, bot: Bot) -> None:
        locales: list[Optional[str]] = list(self.config.locales) + [None]

        for lang in locales:
            display_lang = lang if lang else "default"

            success = await bot.delete_my_commands(
                scope=BotCommandScopeAllPrivateChats(),
                language_code=lang,
            )

            if success:
                logger.info(f"Commands deleted for bot '{bot.id}' language '{display_lang}'")
            else:
                logger.error(
                    f"Failed to delete commands for bot '{bot.id}' language '{display_lang}'"
                )
