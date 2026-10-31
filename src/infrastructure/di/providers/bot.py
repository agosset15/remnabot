from collections.abc import AsyncIterable
from typing import Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram_dialog import BgManagerFactory
from dishka import Provider, Scope, from_context, provide
from loguru import logger

from src.core.config import AppConfig
from src.infrastructure.services.bot_registry import BotRegistry


def _normalize_proxy_url(url: str) -> str:
    # aiohttp_socks doesn't recognize the socks5h/socks4a schemes; aiogram always
    # resolves DNS remotely (rdns=True), so they're equivalent to socks5/socks4.
    if url.startswith("socks5h://"):
        return url.replace("socks5h://", "socks5://", 1)
    if url.startswith("socks4a://"):
        return url.replace("socks4a://", "socks4://", 1)
    return url


def _build_session(config: AppConfig) -> Optional[AiohttpSession]:
    session_kwargs: dict = {}
    if config.bot.proxy_url:
        logger.info("Using SOCKS5 proxy for Telegram")
        session_kwargs["proxy"] = _normalize_proxy_url(config.bot.proxy_url.get_secret_value())
    if config.bot.api_url:
        api_url = config.bot.api_url.get_secret_value()
        if config.bot.api_file_url:
            file_url = config.bot.api_file_url.get_secret_value()
            logger.info(f"Using custom Telegram Bot API server: {api_url} (file: {file_url})")
            session_kwargs["api"] = TelegramAPIServer(base=api_url, file=file_url)
        else:
            logger.info(f"Using custom Telegram Bot API server: {api_url}")
            session_kwargs["api"] = TelegramAPIServer.from_base(api_url)

    return AiohttpSession(**session_kwargs) if session_kwargs else None


class BotProvider(Provider):
    scope = Scope.APP

    bg_manager_factory = from_context(provides=BgManagerFactory)

    @provide
    async def get_bot_registry(self, config: AppConfig) -> AsyncIterable[BotRegistry]:
        tokens = config.bot.all_tokens
        logger.debug(f"Initializing '{len(tokens)}' Bot instance(s)")

        bots = [
            Bot(
                token=token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
                session=_build_session(config),
            )
            for token in tokens
        ]
        registry = BotRegistry(bots, primary_secret=config.bot.secret_token.get_secret_value())

        try:
            yield registry
        finally:
            await registry.close()

    @provide(scope=Scope.REQUEST)
    def get_bot(self, registry: BotRegistry) -> Bot:
        """Bot handling the current Telegram update; the primary bot elsewhere."""
        return registry.current
