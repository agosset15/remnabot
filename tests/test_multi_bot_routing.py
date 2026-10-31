"""Multi-bot glue: which bot handles an update, which bot a user is bound to, and which
bot outgoing messages / webhooks go through. Pure mocks, no DB / Redis / Telegram."""

import asyncio
from types import SimpleNamespace
from typing import Any, Optional
from unittest.mock import AsyncMock, MagicMock

import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import SecretStr

from src.application.dto import UserDto
from src.application.dto.message_payload import MediaDescriptorDto
from src.application.use_cases.user.commands.blocking import (
    SetBotBlockedStatus,
    SetBotBlockedStatusDto,
)
from src.application.use_cases.user.commands.registration import (
    UpdateUserProfile,
    UpdateUserProfileDto,
)
from src.core.utils.converters import user_name_clean
from src.infrastructure.services.bot_registry import BotRegistry, derive_secret_token
from src.infrastructure.services.notification import NotificationService
from src.infrastructure.services.webhook import WebhookService
from src.telegram.routers.extra.member import on_blocked, on_unblocked
from src.web.endpoints.telegram import TelegramWebhookEndpoint

SECRET = "primary-secret"
PRIMARY_ID = 111
EXTRA_ID = 222
TELEGRAM_ID = 5


class FakeBot:
    """Stands in for aiogram.Bot: only ``id`` and awaited calls are needed."""

    def __init__(self, bot_id: int) -> None:
        self.id = bot_id
        self.calls: list[Any] = []
        self.get_webhook_info = AsyncMock(return_value="info")
        self.send_message = AsyncMock(return_value=SimpleNamespace(message_id=1))
        self.send_photo = AsyncMock(return_value=SimpleNamespace(message_id=1))
        self.delete_message = AsyncMock()

    async def __call__(self, method: Any) -> bool:
        self.calls.append(method)
        return True


@pytest.fixture
def bots() -> tuple[FakeBot, FakeBot]:
    return FakeBot(PRIMARY_ID), FakeBot(EXTRA_ID)


@pytest.fixture
def registry(bots: tuple[FakeBot, FakeBot]) -> BotRegistry:
    return BotRegistry(list(bots), primary_secret=SECRET)  # type: ignore[arg-type]


def _uow() -> MagicMock:
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=False)
    uow.commit = AsyncMock()
    return uow


def _user(**kwargs: Any) -> UserDto:
    data: dict[str, Any] = {
        "id": 1,
        "telegram_id": TELEGRAM_ID,
        "name": user_name_clean("Tester", TELEGRAM_ID),
        "username": "tester",
    }
    data.update(kwargs)
    return UserDto(**data)


# --- webhook endpoint ---------------------------------------------------------------------


class _RegistryProvider(Provider):
    def __init__(self, registry: BotRegistry) -> None:
        super().__init__()
        self._registry = registry

    @provide(scope=Scope.APP)
    def registry(self) -> BotRegistry:
        return self._registry


@pytest.fixture
async def webhook(registry: BotRegistry):
    seen: list[tuple[int, int]] = []

    async def feed_update(bot: Any, update: Any) -> None:
        # Record the bot passed in and the bot visible through the registry context.
        seen.append((bot.id, registry.current.id))

    dispatcher = MagicMock()
    dispatcher.feed_update = AsyncMock(side_effect=feed_update)
    endpoint = TelegramWebhookEndpoint(dispatcher)

    app = FastAPI()
    endpoint.register(app, "/webhook")
    container = make_async_container(_RegistryProvider(registry))
    setup_dishka(container, app)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:

        async def post(secret: Optional[str]) -> int:
            headers = {"X-Telegram-Bot-Api-Secret-Token": secret} if secret is not None else {}
            response = await client.post("/webhook", json={"update_id": 1}, headers=headers)
            await asyncio.gather(*endpoint._feed_update_tasks)
            return response.status_code

        yield post, seen

    await container.close()


@pytest.mark.parametrize("secret", [None, "", "wrong"])
async def test_webhook_rejects_missing_or_unknown_secret(webhook, secret):
    post, seen = webhook
    assert await post(secret) == 401
    assert seen == []


async def test_webhook_routes_update_to_bot_owning_the_secret(webhook):
    post, seen = webhook
    assert await post(SECRET) == 200
    assert await post(derive_secret_token(SECRET, EXTRA_ID)) == 200
    # Each update is fed with its own bot, and BotRegistry.current follows it.
    assert seen == [(PRIMARY_ID, PRIMARY_ID), (EXTRA_ID, EXTRA_ID)]


# --- user <-> bot binding -----------------------------------------------------------------


def _update_profile(user: UserDto, bot_id: Optional[int]) -> tuple[UpdateUserProfile, Any]:
    dao = MagicMock()
    dao.update = AsyncMock(side_effect=lambda u: u)
    use_case = UpdateUserProfile(uow=_uow(), user_dao=dao, config=MagicMock(locales=[]))
    data = UpdateUserProfileDto(
        user=user,
        username=user.username,
        full_name="Tester",
        language_code=None,
        telegram_id=TELEGRAM_ID,
        bot_id=bot_id,
    )
    return use_case, (dao, data)


async def test_profile_switches_bot_and_clears_blocked_flag():
    user = _user(bot_id=PRIMARY_ID, is_bot_blocked=True)
    use_case, (dao, data) = _update_profile(user, EXTRA_ID)

    result = await use_case.system(data)

    assert result.bot_id == EXTRA_ID
    assert result.is_bot_blocked is False
    dao.update.assert_awaited_once()


@pytest.mark.parametrize("bot_id", [None, PRIMARY_ID])
async def test_profile_untouched_without_bot_change(bot_id):
    user = _user(bot_id=PRIMARY_ID)
    use_case, (dao, data) = _update_profile(user, bot_id)

    result = await use_case.system(data)

    assert result.bot_id == PRIMARY_ID
    dao.update.assert_not_awaited()


def _blocking() -> tuple[SetBotBlockedStatus, MagicMock]:
    dao = MagicMock()
    dao.set_bot_blocked_status = AsyncMock()
    dao.set_bot_id = AsyncMock()
    return SetBotBlockedStatus(uow=_uow(), user_dao=dao), dao


async def test_unblock_via_bot_rebinds_user():
    use_case, dao = _blocking()
    await use_case.system(SetBotBlockedStatusDto(1, False, bot_id=EXTRA_ID))
    dao.set_bot_blocked_status.assert_awaited_once_with(1, False)
    dao.set_bot_id.assert_awaited_once_with(1, EXTRA_ID)


@pytest.mark.parametrize("is_blocked,bot_id", [(True, EXTRA_ID), (False, None)])
async def test_block_or_unknown_bot_keeps_binding(is_blocked, bot_id):
    use_case, dao = _blocking()
    await use_case.system(SetBotBlockedStatusDto(1, is_blocked, bot_id=bot_id))
    dao.set_bot_id.assert_not_awaited()


# --- my_chat_member router ----------------------------------------------------------------


async def test_unblocking_a_bot_binds_user_to_it(bots):
    _, extra = bots
    set_status = MagicMock()
    set_status.system = AsyncMock()

    await on_unblocked(MagicMock(), extra, _user(bot_id=PRIMARY_ID), set_status)  # type: ignore[arg-type]

    set_status.system.assert_awaited_once_with(SetBotBlockedStatusDto(1, False, bot_id=EXTRA_ID))


async def test_blocking_the_users_bot_marks_blocked(bots, registry):
    _, extra = bots
    set_status = MagicMock()
    set_status.system = AsyncMock()

    await on_blocked(MagicMock(), extra, _user(bot_id=EXTRA_ID), set_status, registry)  # type: ignore[arg-type]

    set_status.system.assert_awaited_once_with(SetBotBlockedStatusDto(1, True))


async def test_blocking_an_old_bot_is_ignored(bots, registry):
    primary, _ = bots
    set_status = MagicMock()
    set_status.system = AsyncMock()

    await on_blocked(MagicMock(), primary, _user(bot_id=EXTRA_ID), set_status, registry)  # type: ignore[arg-type]

    set_status.system.assert_not_awaited()


# --- webhook setup ------------------------------------------------------------------------


async def test_setup_webhooks_registers_every_bot_with_its_own_secret(bots, registry):
    config = MagicMock()
    config.bot.webhook_url.return_value = SecretStr("https://example.com/webhook")
    config.bot.drop_pending_updates = False
    config.bot.reset_webhook = False
    dao = MagicMock()
    dao.is_hash_exists = AsyncMock(return_value=False)
    dao.clear_all_hashes = AsyncMock()
    dao.save_hash = AsyncMock()
    cryptographer = MagicMock()
    cryptographer.get_hash.side_effect = lambda d: repr(sorted(d.items()))

    service = WebhookService(dao, registry, config, cryptographer)
    result = await service.setup_webhooks(["message"])

    primary, extra = bots
    assert [bot.id for bot, _ in result] == [PRIMARY_ID, EXTRA_ID]
    assert primary.calls[0].secret_token == SECRET
    assert extra.calls[0].secret_token == derive_secret_token(SECRET, EXTRA_ID)
    saved_for = [c.args[0] for c in dao.save_hash.await_args_list]
    assert saved_for == [PRIMARY_ID, EXTRA_ID]


# --- notifications ------------------------------------------------------------------------


def _notifier(registry: BotRegistry, media_resolver: Any = None) -> NotificationService:
    service = object.__new__(NotificationService)
    service.bots = registry
    service.media_resolver = media_resolver
    service._prepare_reply_markup = MagicMock(return_value=None)  # type: ignore[method-assign]
    service._render_payload_text = MagicMock(return_value="hi")  # type: ignore[method-assign]
    return service


@pytest.mark.parametrize("bot_id,expected", [(EXTRA_ID, 1), (None, 0), (999, 0)])
async def test_user_notification_goes_through_users_bot(bots, registry, bot_id, expected):
    payload = MagicMock(is_text=True, delete_after=None)

    await _notifier(registry)._send_message(_user(bot_id=bot_id), payload)

    target = bots[expected]
    other = bots[1 - expected]
    target.send_message.assert_awaited_once()
    assert target.send_message.await_args.kwargs["chat_id"] == TELEGRAM_ID
    other.send_message.assert_not_awaited()


async def test_delete_notification_defaults_to_current_bot(bots, registry):
    primary, extra = bots
    service = _notifier(registry)

    with BotRegistry.use(extra):  # type: ignore[arg-type]
        await service.delete_notification(TELEGRAM_ID, 7)

    extra.delete_message.assert_awaited_once_with(chat_id=TELEGRAM_ID, message_id=7)
    primary.delete_message.assert_not_awaited()


class _Resolver:
    def __init__(self, cached: Optional[str], resolved: Any) -> None:
        self._cached = cached
        self._resolved = resolved
        self.remembered: list[Any] = []

    async def cached(self, file_id: str, bot: Any) -> Optional[str]:
        return self._cached

    def lock(self, bot: Any, file_id: str) -> Any:
        return asyncio.Lock()

    async def resolve(self, file_id: str, bot: Any) -> Any:
        return self._resolved

    async def remember(self, file_id: str, bot: Any, message: Any) -> None:
        self.remembered.append((file_id, bot.id, message))


async def test_send_media_uses_cached_file_id(bots, registry):
    _, extra = bots
    resolver = _Resolver(cached="extra-fid", resolved=None)
    media = MediaDescriptorDto(kind="file_id", value="fid")

    await _notifier(registry, resolver)._send_media(extra, extra.send_photo, media, TELEGRAM_ID)

    extra.send_photo.assert_awaited_once_with(TELEGRAM_ID, "extra-fid")
    assert resolver.remembered == []


async def test_send_media_reupload_is_remembered(bots, registry):
    _, extra = bots
    upload = object()  # stands in for a BufferedInputFile
    resolver = _Resolver(cached=None, resolved=upload)
    media = MediaDescriptorDto(kind="file_id", value="fid")

    message = await _notifier(registry, resolver)._send_media(
        extra, extra.send_photo, media, TELEGRAM_ID
    )

    extra.send_photo.assert_awaited_once_with(TELEGRAM_ID, upload)
    assert resolver.remembered == [("fid", EXTRA_ID, message)]


async def test_send_media_own_file_id_is_not_remembered(bots, registry):
    primary, _ = bots
    resolver = _Resolver(cached=None, resolved="fid")
    media = MediaDescriptorDto(kind="file_id", value="fid")

    await _notifier(registry, resolver)._send_media(primary, primary.send_photo, media, TELEGRAM_ID)

    assert resolver.remembered == []
