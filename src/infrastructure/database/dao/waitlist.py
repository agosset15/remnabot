from typing import Awaitable, Set, cast

from adaptix import Retort
from loguru import logger
from redis.asyncio import Redis

from src.application.common.dao import WaitlistDao
from src.infrastructure.redis.keys import WaitlistKey


class WaitlistDaoImpl(WaitlistDao):
    def __init__(self, redis: Redis, retort: Retort):
        self.redis = redis
        self.retort = retort

    async def is_in_waitlist(self, telegram_id: int) -> bool:
        raw_key = self.retort.dump(WaitlistKey())
        is_member = await cast("Awaitable[int]", self.redis.sismember(raw_key, str(telegram_id)))

        if is_member:
            logger.debug(f"User '{telegram_id}' found in waitlist")
        else:
            logger.debug(f"User '{telegram_id}' not found in waitlist")

        return bool(is_member)

    async def add_to_waitlist(self, telegram_id: int) -> None:
        raw_key = self.retort.dump(WaitlistKey())
        await cast("Awaitable[int]", self.redis.sadd(raw_key, str(telegram_id)))
        logger.debug(f"User '{telegram_id}' added to waitlist")

    async def get_waitlist_members(self) -> list[int]:
        raw_key = self.retort.dump(WaitlistKey())
        members = await cast("Awaitable[Set[bytes]]", self.redis.smembers(raw_key))
        logger.debug(f"Retrieved '{len(members)}' users from waitlist")
        return [int(m) for m in members]

    async def clear_waitlist(self) -> None:
        raw_key = self.retort.dump(WaitlistKey())
        await self.redis.delete(raw_key)
        logger.debug("Waitlist cleared")
