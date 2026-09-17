from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException
from pydantic import SecretStr

from src.application.use_cases.auth.commands.password_reset import (
    RequestPasswordReset,
    RequestPasswordResetDto,
    ResetPassword,
    ResetPasswordDto,
)
from src.core.enums import Locale
from src.core.exceptions import EmailDeliveryDisabledError

CRYPT_KEY = "A6i+WajSI/d5sA7AK9pvXSOMaQpGk4gApBrPMw7rgRA="


def _config() -> SimpleNamespace:
    return SimpleNamespace(crypt_key=SecretStr(CRYPT_KEY))


def _uow() -> MagicMock:
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=False)
    uow.commit = AsyncMock()
    return uow


def _user(**kwargs) -> SimpleNamespace:
    data = {
        "id": 7,
        "email": "user@example.com",
        "is_email_verified": True,
        "is_blocked": False,
        "password_hash": "scrypt$old",
        "language": Locale.RU,
    }
    data.update(kwargs)
    return SimpleNamespace(**data)


def _auth_session() -> AsyncMock:
    session = AsyncMock()
    session.try_start_password_reset_cooldown.return_value = True
    return session


def _email_sender() -> MagicMock:
    sender = MagicMock()
    sender.is_enabled = True
    sender.send = AsyncMock()
    return sender


def _web_service(url: str = "https://cabinet.example") -> MagicMock:
    service = MagicMock()
    service.reset_password.side_effect = (
        lambda token: f"{url}/my/reset-password?token={token}" if url else None
    )
    return service


def _request_use_case(
    translator_hub,
    user=None,
    auth_session=None,
    email_sender=None,
    web_service=None,
) -> tuple[RequestPasswordReset, AsyncMock, MagicMock]:
    user_dao = AsyncMock()
    user_dao.get_by_email.return_value = user
    auth_session = auth_session or _auth_session()
    email_sender = email_sender or _email_sender()
    use_case = RequestPasswordReset(
        config=_config(),
        user_dao=user_dao,
        auth_session=auth_session,
        email_sender=email_sender,
        i18n_hub=translator_hub,
        web_service=web_service or _web_service(),
    )
    return use_case, auth_session, email_sender


async def test_disabled_email_delivery_raises(translator_hub):
    sender = _email_sender()
    sender.is_enabled = False
    use_case, _, _ = _request_use_case(translator_hub, user=_user(), email_sender=sender)

    with pytest.raises(EmailDeliveryDisabledError):
        await use_case.system(RequestPasswordResetDto(email="user@example.com"))


@pytest.mark.parametrize(
    "user",
    [
        None,
        _user(is_blocked=True),
        _user(is_email_verified=False),
        _user(email=None),
    ],
    ids=["unknown", "blocked", "unverified", "no-email"],
)
async def test_no_mail_for_ineligible_user(translator_hub, user):
    use_case, auth_session, sender = _request_use_case(translator_hub, user=user)

    await use_case.system(RequestPasswordResetDto(email="user@example.com"))

    sender.send.assert_not_awaited()
    auth_session.store_password_reset_token.assert_not_awaited()


async def test_cooldown_blocks_second_request(translator_hub):
    auth_session = _auth_session()
    auth_session.try_start_password_reset_cooldown.return_value = False
    use_case, _, sender = _request_use_case(translator_hub, user=_user(), auth_session=auth_session)

    await use_case.system(RequestPasswordResetDto(email="user@example.com"))

    sender.send.assert_not_awaited()


async def test_sends_link_to_cabinet_and_stores_token(translator_hub):
    use_case, auth_session, sender = _request_use_case(translator_hub, user=_user())

    await use_case.system(RequestPasswordResetDto(email="user@example.com"))

    auth_session.store_password_reset_token.assert_awaited_once()
    token_hash, user_id, ttl = auth_session.store_password_reset_token.await_args.args
    assert len(token_hash) == 64
    assert user_id == 7
    assert ttl == 1800

    kwargs = sender.send.await_args.kwargs
    assert kwargs["to"] == "user@example.com"
    assert "https://cabinet.example/my/reset-password?token=" in kwargs["body"]
    assert "https://cabinet.example/my/reset-password?token=" in kwargs["html"]
    assert "30" in kwargs["body"]


async def test_missing_cabinet_url_rolls_back(translator_hub):
    web_service = MagicMock()
    web_service.reset_password.return_value = None
    use_case, auth_session, sender = _request_use_case(
        translator_hub, user=_user(), web_service=web_service
    )

    with pytest.raises(EmailDeliveryDisabledError):
        await use_case.system(RequestPasswordResetDto(email="user@example.com"))

    auth_session.revoke_password_reset_token.assert_awaited_once()
    auth_session.clear_password_reset_cooldown.assert_awaited_once()
    sender.send.assert_not_awaited()


async def test_send_failure_releases_token_and_cooldown(translator_hub):
    sender = _email_sender()
    sender.send.side_effect = RuntimeError("smtp down")
    use_case, auth_session, _ = _request_use_case(translator_hub, user=_user(), email_sender=sender)

    with pytest.raises(RuntimeError):
        await use_case.system(RequestPasswordResetDto(email="user@example.com"))

    auth_session.revoke_password_reset_token.assert_awaited_once()
    auth_session.clear_password_reset_cooldown.assert_awaited_once()


def _reset_use_case(user=None, consumed_user_id=7) -> tuple[ResetPassword, AsyncMock, MagicMock]:
    user_dao = AsyncMock()
    user_dao.get_by_id.return_value = user
    user_dao.update.side_effect = lambda dto: dto
    auth_session = AsyncMock()
    auth_session.consume_password_reset_token.return_value = consumed_user_id
    hasher = MagicMock()
    hasher.hash.return_value = "scrypt$new"
    use_case = ResetPassword(
        config=_config(),
        uow=_uow(),
        user_dao=user_dao,
        auth_session=auth_session,
        password_hasher=hasher,
    )
    return use_case, auth_session, hasher


async def test_reset_sets_password_and_revokes_sessions():
    user = _user()
    use_case, auth_session, hasher = _reset_use_case(user=user)

    updated = await use_case.system(ResetPasswordDto(token="t" * 20, new_password="newpass123"))

    hasher.hash.assert_called_once_with("newpass123")
    assert updated.password_hash == "scrypt$new"
    auth_session.revoke_all_user_tokens.assert_awaited_once_with(7)


async def test_reset_with_unknown_token_is_rejected():
    use_case, _, _ = _reset_use_case(consumed_user_id=None)

    with pytest.raises(HTTPException) as exc:
        await use_case.system(ResetPasswordDto(token="t" * 20, new_password="newpass123"))

    assert exc.value.status_code == 400


async def test_reset_for_blocked_user_is_forbidden():
    use_case, _, _ = _reset_use_case(user=_user(is_blocked=True))

    with pytest.raises(HTTPException) as exc:
        await use_case.system(ResetPasswordDto(token="t" * 20, new_password="newpass123"))

    assert exc.value.status_code == 403
