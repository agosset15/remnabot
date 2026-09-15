from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from src.application.dto import UserDto
from src.application.use_cases.auth.commands import telegram as telegram_module
from src.application.use_cases.auth.commands.telegram import (
    LinkTelegram,
    LinkTelegramData,
    _TelegramIdentity,
)
from src.core.utils.time import datetime_now

IDENTITY = _TelegramIdentity(id=555, name="Tg User", username="tg_user")


def _uow() -> MagicMock:
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=False)
    uow.commit = AsyncMock()
    return uow


def _sub(sub_id: int, remna_num_id: int, days: int) -> SimpleNamespace:
    return SimpleNamespace(
        id=sub_id,
        user_remna_num_id=remna_num_id,
        expire_at=datetime_now() + timedelta(days=days),
    )


def _use_case(**overrides) -> LinkTelegram:
    kwargs = {
        "config": MagicMock(),
        "uow": _uow(),
        "user_dao": AsyncMock(),
        "subscription_dao": AsyncMock(),
        "transaction_dao": AsyncMock(),
        "referral_dao": AsyncMock(),
        "remnawave": AsyncMock(),
        "redis": MagicMock(),
    }
    kwargs.update(overrides)
    return LinkTelegram(**kwargs)  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _stub_id_token(monkeypatch):
    """Skip JWKS fetch / JWT verification: every test drives the same identity."""
    monkeypatch.setattr(telegram_module, "_verify_id_token", AsyncMock(return_value=IDENTITY))


def _actor(**kwargs) -> UserDto:
    data = {"id": 1, "name": "web", "email": "web@example.com", "telegram_id": None}
    data.update(kwargs)
    return UserDto(**data)


async def test_merge_syncs_every_panel_user_not_just_the_surviving_one():
    """The donor's non-surviving subscriptions must still receive the survivor's email."""
    actor = _actor()
    donor = _actor(id=2, name="tg", email=None, telegram_id=IDENTITY.id)
    subs = [_sub(10, 1000, days=30), _sub(20, 2000, days=5)]

    user_dao = AsyncMock()
    user_dao.get_by_telegram_id.return_value = donor
    user_dao.update.return_value = actor
    user_dao.get_by_id.return_value = actor

    subscription_dao = AsyncMock()
    subscription_dao.get_all_by_user.return_value = subs

    remnawave = AsyncMock()
    use_case = _use_case(user_dao=user_dao, subscription_dao=subscription_dao, remnawave=remnawave)

    await use_case(actor, LinkTelegramData(id_token="token"))

    synced = {call.kwargs["num_id"] for call in remnawave.sync_user_identity.await_args_list}
    assert synced == {1000, 2000}
    assert all(
        call.kwargs["user"].email == "web@example.com"
        for call in remnawave.sync_user_identity.await_args_list
    )
    # The latest-expiring subscription becomes the survivor's current one.
    user_dao.set_current_subscription_by_id.assert_awaited_once_with(1, 10)
    user_dao.delete.assert_awaited_once_with(2)


async def test_plain_link_syncs_panel_identity():
    """Linking without a donor must still push telegram_id to the panel."""
    actor = _actor()
    linked = _actor(telegram_id=IDENTITY.id)

    user_dao = AsyncMock()
    user_dao.get_by_telegram_id.return_value = None
    user_dao.update.return_value = linked

    subscription_dao = AsyncMock()
    subscription_dao.get_all_by_user.return_value = [_sub(10, 1000, days=30)]

    remnawave = AsyncMock()
    use_case = _use_case(user_dao=user_dao, subscription_dao=subscription_dao, remnawave=remnawave)

    await use_case(actor, LinkTelegramData(id_token="token"))

    remnawave.sync_user_identity.assert_awaited_once_with(user=linked, num_id=1000)


@pytest.mark.parametrize(
    "credential",
    [
        {"email": "tg@example.com"},
        {"pending_email": "tg@example.com"},
        {"password_hash": "hashed"},
    ],
)
async def test_donor_with_own_credentials_is_never_merged(credential):
    """A donor holding credentials is a real account, not a mergeable Telegram shell."""
    donor = _actor(id=2, name="tg", telegram_id=IDENTITY.id, **{"email": None, **credential})

    user_dao = AsyncMock()
    user_dao.get_by_telegram_id.return_value = donor
    use_case = _use_case(user_dao=user_dao)

    with pytest.raises(HTTPException) as exc:
        await use_case(_actor(), LinkTelegramData(id_token="token"))

    assert exc.value.status_code == 409
    user_dao.delete.assert_not_awaited()


async def test_merge_aborts_when_survivor_row_vanishes():
    """A failed survivor update must roll back instead of committing a half-merge."""
    donor = _actor(id=2, name="tg", email=None, telegram_id=IDENTITY.id)

    user_dao = AsyncMock()
    user_dao.get_by_telegram_id.return_value = donor
    user_dao.update.return_value = None

    uow = _uow()
    use_case = _use_case(user_dao=user_dao, uow=uow)

    with pytest.raises(HTTPException) as exc:
        await use_case(_actor(), LinkTelegramData(id_token="token"))

    assert exc.value.status_code == 404
    uow.commit.assert_not_awaited()
