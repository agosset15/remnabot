from collections.abc import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram_dialog import BgManagerFactory
from dishka import Provider, Scope, from_context, provide
from loguru import logger

from src.core.config import AppConfig


def _normalize_proxy_url(url: str) -> str:
    # aiohttp_socks doesn't recognize the socks5h/socks4a schemes; aiogram always
    # resolves DNS remotely (rdns=True), so they're equivalent to socks5/socks4.
    if url.startswith("socks5h://"):
        return url.replace("socks5h://", "socks5://", 1)
    if url.startswith("socks4a://"):
        return url.replace("socks4a://", "socks4://", 1)
    return url


class BotProvider(Provider):
    scope = Scope.APP

    bg_manager_factory = from_context(provides=BgManagerFactory)

    @provide
    async def get_bot(self, config: AppConfig) -> AsyncIterable[Bot]:
        logger.debug("Initializing Bot instance")

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

        session = AiohttpSession(**session_kwargs) if session_kwargs else None

        async with Bot(
            token=config.bot.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            session=session,
        ) as bot:
            yield bot
