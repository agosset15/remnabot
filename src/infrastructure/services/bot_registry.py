import hashlib
import hmac
import secrets
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Optional, Union

from aiogram import Bot

from src.core.constants import T_ME

# Id of the bot handling the current Telegram update. Set by the webhook endpoint and by
# an outer dispatcher middleware; unset in web/taskiq contexts (falls back to primary).
_current_bot_id: ContextVar[Optional[int]] = ContextVar("current_bot_id", default=None)


def derive_secret_token(primary_secret: str, bot_id: int) -> str:
    """Webhook secret for an extra bot, derived from ``BOT_SECRET_TOKEN``.

    Hex output satisfies Telegram's ``secret_token`` charset (A-Z, a-z, 0-9, _, -).
    """
    return hmac.new(
        primary_secret.encode("utf-8"),
        str(bot_id).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


class BotRegistry:
    """All configured Telegram bots. The first one is the primary bot."""

    def __init__(self, bots: list[Bot], primary_secret: str) -> None:
        if not bots:
            raise ValueError("BotRegistry requires at least one bot")

        self._bots: dict[int, Bot] = {}
        for bot in bots:
            self._bots[bot.id] = bot

        self._primary = bots[0]
        self._secrets: dict[int, str] = {
            bot.id: primary_secret
            if bot is self._primary
            else derive_secret_token(primary_secret, bot.id)
            for bot in bots
        }
        self._usernames: dict[int, str] = {}

    @property
    def primary(self) -> Bot:
        return self._primary

    @property
    def current(self) -> Bot:
        """Bot handling the current update, or the primary bot outside of one."""
        return self.resolve(_current_bot_id.get())

    @property
    def is_multi(self) -> bool:
        return len(self._bots) > 1

    @property
    def ids(self) -> list[int]:
        return list(self._bots)

    def all(self) -> list[Bot]:
        return list(self._bots.values())

    def get(self, bot_id: Optional[int]) -> Optional[Bot]:
        if bot_id is None:
            return None
        return self._bots.get(bot_id)

    def resolve(self, bot_id: Optional[int]) -> Bot:
        return self.get(bot_id) or self._primary

    def for_user(self, user: Any) -> Bot:
        """Bot the user last interacted with (primary if unknown or no longer configured)."""
        return self.resolve(getattr(user, "bot_id", None))

    def secret_for(self, bot: Union[Bot, int]) -> str:
        bot_id = bot if isinstance(bot, int) else bot.id
        return self._secrets[bot_id]

    def by_secret(self, secret: str) -> Optional[Bot]:
        found: Optional[Bot] = None
        for bot_id, expected in self._secrets.items():
            # Compare against every secret to keep timing independent of the match position.
            if secrets.compare_digest(secret, expected) and found is None:
                found = self._bots[bot_id]
        return found

    async def username(self, bot: Optional[Bot] = None) -> Optional[str]:
        bot = bot or self.current
        if bot.id not in self._usernames:
            me = await bot.get_me()
            if me.username:
                self._usernames[bot.id] = me.username
        return self._usernames.get(bot.id)

    async def url(self, bot: Optional[Bot] = None) -> str:
        return f"{T_ME}{await self.username(bot)}"

    @staticmethod
    @contextmanager
    def use(bot: Optional[Bot]) -> Iterator[None]:
        """Mark ``bot`` as the current bot for the enclosed code."""
        token = _current_bot_id.set(bot.id if bot is not None else None)
        try:
            yield
        finally:
            _current_bot_id.reset(token)

    async def close(self) -> None:
        for bot in self._bots.values():
            await bot.session.close()
