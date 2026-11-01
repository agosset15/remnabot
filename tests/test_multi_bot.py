import hashlib
import hmac
import time
from types import SimpleNamespace
from typing import Any, Optional
from unittest.mock import AsyncMock
from urllib.parse import urlencode

import pytest
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.methods import GetFile
from aiogram.types import BufferedInputFile, File, Message, PhotoSize
from pydantic import ValidationError

from src.application.use_cases.auth._telegram import verify_telegram_webapp_init_data_any
from src.core.config.bot import BotConfig
from src.infrastructure.services.bot_registry import BotRegistry, derive_secret_token
from src.infrastructure.services.media_resolver import MediaResolver

PRIMARY_TOKEN = "111:primary-token"
EXTRA_TOKEN = "222:extra-token"
SECRET = "primary-secret"


def _bot_config(**overrides: Any) -> BotConfig:
    values: dict[str, Any] = {
        "token": PRIMARY_TOKEN,
        "secret_token": SECRET,
        "owner_id": 1,
        "support_username": "support_bot",
    }
    values.update(overrides)
    return BotConfig(**values)


@pytest.fixture
def registry() -> BotRegistry:
    return BotRegistry([Bot(PRIMARY_TOKEN), Bot(EXTRA_TOKEN)], primary_secret=SECRET)


# --- config -------------------------------------------------------------------------------


def test_extra_tokens_default_to_single_bot():
    config = _bot_config(extra_tokens="")
    assert config.all_tokens == [PRIMARY_TOKEN]
    assert config.all_ids == [111]


def test_extra_tokens_are_parsed_in_order():
    config = _bot_config(extra_tokens=f" {EXTRA_TOKEN} , 333:third ,")
    assert config.all_tokens == [PRIMARY_TOKEN, EXTRA_TOKEN, "333:third"]
    assert config.all_ids == [111, 222, 333]


@pytest.mark.parametrize("extra", ["not-a-token", "abc:def", f"{PRIMARY_TOKEN}"])
def test_extra_tokens_reject_invalid_or_duplicate(extra: str):
    with pytest.raises(ValidationError):
        _bot_config(extra_tokens=extra)


# --- registry -----------------------------------------------------------------------------


def test_primary_keeps_configured_secret_and_extra_gets_derived(registry: BotRegistry):
    primary, extra = registry.all()
    assert registry.primary is primary
    assert registry.secret_for(primary) == SECRET
    assert registry.secret_for(extra) == derive_secret_token(SECRET, 222)
    assert registry.secret_for(extra) != SECRET


def test_derived_secret_matches_telegram_charset():
    secret = derive_secret_token(SECRET, 222)
    assert 1 <= len(secret) <= 256
    assert all(c.isalnum() or c in "_-" for c in secret)


def test_by_secret_identifies_bot(registry: BotRegistry):
    primary, extra = registry.all()
    assert registry.by_secret(SECRET) is primary
    assert registry.by_secret(derive_secret_token(SECRET, 222)) is extra
    assert registry.by_secret("wrong") is None
    assert registry.by_secret("") is None


def test_for_user_falls_back_to_primary(registry: BotRegistry):
    primary, extra = registry.all()
    assert registry.for_user(SimpleNamespace(bot_id=222)) is extra
    assert registry.for_user(SimpleNamespace(bot_id=None)) is primary
    assert registry.for_user(SimpleNamespace(bot_id=999)) is primary  # removed bot
    assert registry.for_user(SimpleNamespace()) is primary  # TempUserDto has no bot_id
    assert registry.for_user(None) is primary


def test_current_follows_context(registry: BotRegistry):
    primary, extra = registry.all()
    assert registry.current is primary
    with BotRegistry.use(extra):
        assert registry.current is extra
        with BotRegistry.use(primary):
            assert registry.current is primary
        assert registry.current is extra
    assert registry.current is primary


def test_registry_flags(registry: BotRegistry):
    assert registry.is_multi
    assert registry.ids == [111, 222]
    single = BotRegistry([Bot(PRIMARY_TOKEN)], primary_secret=SECRET)
    assert not single.is_multi


# --- media resolver -----------------------------------------------------------------------


class _FakeRedis:
    def __init__(self) -> None:
        self.data: dict[str, str] = {}

    async def get(self, key: str) -> Optional[str]:
        return self.data.get(key)

    async def set(self, key: str, value: str, ex: Optional[int] = None) -> None:
        self.data[key] = value


def _owned_by(bot: Bot, file_id: str) -> None:
    async def get_file(requested: str) -> File:
        if requested != file_id:
            raise TelegramBadRequest(method=GetFile(file_id=requested), message="wrong file_id")
        return File(file_id=requested, file_unique_id="u", file_path="photos/p.jpg")

    async def download_file(path: str) -> Any:
        return SimpleNamespace(read=lambda: b"image-bytes")

    bot.get_file = AsyncMock(side_effect=get_file)  # type: ignore[method-assign]
    bot.download_file = AsyncMock(side_effect=download_file)  # type: ignore[method-assign]


async def test_media_resolver_single_bot_is_passthrough():
    bot = Bot(PRIMARY_TOKEN)
    bot.get_file = AsyncMock()  # type: ignore[method-assign]
    resolver = MediaResolver(BotRegistry([bot], SECRET), _FakeRedis())  # type: ignore[arg-type]

    assert await resolver.resolve("fid", bot) == "fid"
    bot.get_file.assert_not_called()


async def test_media_resolver_own_file_is_cached(registry: BotRegistry):
    primary, extra = registry.all()
    _owned_by(primary, "fid")
    _owned_by(extra, "other")
    resolver = MediaResolver(registry, _FakeRedis())  # type: ignore[arg-type]

    assert await resolver.resolve("fid", primary) == "fid"
    assert await resolver.cached("fid", primary) == "fid"


async def test_media_resolver_reuploads_foreign_file_and_remembers(registry: BotRegistry):
    primary, extra = registry.all()
    _owned_by(primary, "fid")
    _owned_by(extra, "other")
    resolver = MediaResolver(registry, _FakeRedis())  # type: ignore[arg-type]

    resolved = await resolver.resolve("fid", extra)
    assert isinstance(resolved, BufferedInputFile)
    assert resolved.filename == "p.jpg"

    sent = Message.model_validate(
        {
            "message_id": 1,
            "date": int(time.time()),
            "chat": {"id": 5, "type": "private"},
            "photo": [PhotoSize(file_id="extra-fid", file_unique_id="u", width=1, height=1)],
        }
    )
    await resolver.remember("fid", extra, sent)
    assert await resolver.cached("fid", extra) == "extra-fid"
    assert await resolver.resolve("fid", extra) == "extra-fid"


# --- web auth -----------------------------------------------------------------------------


def _signed_init_data(bot_token: str) -> str:
    fields = {"auth_date": str(int(time.time())), "user": '{"id": 5, "first_name": "A"}'}
    data_check_string = "\n".join(f"{k}={fields[k]}" for k in sorted(fields))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


def test_webapp_init_data_accepted_from_any_configured_bot():
    tokens = [PRIMARY_TOKEN, EXTRA_TOKEN]
    assert verify_telegram_webapp_init_data_any(_signed_init_data(PRIMARY_TOKEN), tokens)
    assert verify_telegram_webapp_init_data_any(_signed_init_data(EXTRA_TOKEN), tokens)
    assert not verify_telegram_webapp_init_data_any(_signed_init_data("333:other"), tokens)
