import asyncio
from pathlib import PurePosixPath
from typing import Optional, Union, cast

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, Message
from loguru import logger
from redis.asyncio import Redis

from src.infrastructure.redis.key_builder import build_key

from .bot_registry import BotRegistry

MEDIA_FILE_PREFIX = "media_file"
MEDIA_FILE_TTL = 60 * 60 * 24 * 30  # file_ids are stable; refresh monthly


class MediaResolver:
    """Makes Telegram ``file_id``s usable across bots.

    A ``file_id`` is only valid for the bot that received the file. When media has to be
    sent through another bot, it is downloaded with the bot that owns it and uploaded
    again; the resulting ``file_id`` is cached per target bot so this happens once.
    """

    def __init__(self, bots: BotRegistry, redis: Redis) -> None:
        self.bots = bots
        self.redis = redis
        self._locks: dict[str, asyncio.Lock] = {}

    @staticmethod
    def _key(bot: Bot, file_id: str) -> str:
        return build_key(MEDIA_FILE_PREFIX, bot.id, file_id)

    def lock(self, bot: Bot, file_id: str) -> asyncio.Lock:
        """Serialize first sends of a file through a bot so it is re-uploaded only once."""
        return self._locks.setdefault(self._key(bot, file_id), asyncio.Lock())

    async def cached(self, file_id: str, bot: Bot) -> Optional[str]:
        """``file_id`` usable by ``bot`` if already known, without calling Telegram."""
        if not self.bots.is_multi:
            return file_id
        return cast(Optional[str], await self.redis.get(self._key(bot, file_id)))

    async def resolve(self, file_id: str, bot: Bot) -> Union[str, BufferedInputFile]:
        cached = await self.cached(file_id, bot)
        if cached:
            return cached

        key = self._key(bot, file_id)

        if await self._is_owned_by(file_id, bot):
            await self.redis.set(key, file_id, ex=MEDIA_FILE_TTL)
            return file_id

        for owner in self.bots.all():
            if owner.id == bot.id:
                continue
            upload = await self._download(file_id, owner)
            if upload is not None:
                logger.info(f"Re-uploading media '{file_id}' from bot '{owner.id}' to '{bot.id}'")
                return upload

        # Unknown owner (e.g. file too big for getFile): let Telegram decide.
        return file_id

    async def remember(self, file_id: str, bot: Bot, message: Optional[Message]) -> None:
        """Cache the target bot's own ``file_id`` taken from the message it just sent."""
        if not self.bots.is_multi or message is None:
            return

        new_file_id = self.extract_file_id(message)
        if new_file_id:
            await self.redis.set(self._key(bot, file_id), new_file_id, ex=MEDIA_FILE_TTL)

    @staticmethod
    def extract_file_id(message: Message) -> Optional[str]:
        if message.photo:
            return message.photo[-1].file_id
        for media in (message.video, message.document, message.animation):
            if media is not None:
                return media.file_id
        return None

    @staticmethod
    async def _is_owned_by(file_id: str, bot: Bot) -> bool:
        try:
            await bot.get_file(file_id)
            return True
        except TelegramBadRequest:
            return False

    @staticmethod
    async def _download(file_id: str, bot: Bot) -> Optional[BufferedInputFile]:
        try:
            file = await bot.get_file(file_id)
        except TelegramBadRequest:
            return None

        if not file.file_path:
            return None

        data = await bot.download_file(file.file_path)
        if data is None:
            return None

        return BufferedInputFile(data.read(), filename=PurePosixPath(file.file_path).name)
