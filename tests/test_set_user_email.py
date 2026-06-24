from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.use_cases.user.commands.profile_edit import SetUserEmail, SetUserEmailDto


def _uow() -> MagicMock:
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=False)
    uow.commit = AsyncMock()
    return uow


def _target(**kwargs) -> SimpleNamespace:
    data = {"id": 10, "email": None, "telegram_id": 123}
    data.update(kwargs)
    return SimpleNamespace(**data)


async def test_invalid_email_raises():
    dao = AsyncMock()
    dao.get_by_id.return_value = _target()
    use_case = SetUserEmail(uow=_uow(), user_dao=dao)

    with pytest.raises(ValueError):
        await use_case.system(SetUserEmailDto(10, "not-an-email"))


async def test_set_valid_email_normalizes_and_updates():
    dao = AsyncMock()
    target = _target(email=None)
    dao.get_by_id.return_value = target
    dao.get_by_email.return_value = None
    uow = _uow()
    use_case = SetUserEmail(uow=uow, user_dao=dao)

    await use_case.system(SetUserEmailDto(10, "User@Example.COM"))

    assert target.email == "user@example.com"
    dao.update.assert_awaited_once_with(target)
    uow.commit.assert_awaited_once()


async def test_clear_email_without_telegram_raises():
    dao = AsyncMock()
    dao.get_by_id.return_value = _target(telegram_id=None, email="a@b.com")
    use_case = SetUserEmail(uow=_uow(), user_dao=dao)

    with pytest.raises(ValueError):
        await use_case.system(SetUserEmailDto(10, None))


async def test_clear_email_with_telegram_ok():
    dao = AsyncMock()
    target = _target(telegram_id=123, email="a@b.com")
    dao.get_by_id.return_value = target
    use_case = SetUserEmail(uow=_uow(), user_dao=dao)

    await use_case.system(SetUserEmailDto(10, None))

    assert target.email is None
    dao.update.assert_awaited_once()


async def test_duplicate_email_raises():
    dao = AsyncMock()
    dao.get_by_id.return_value = _target(id=10, email=None)
    dao.get_by_email.return_value = SimpleNamespace(id=99)  # belongs to another user
    use_case = SetUserEmail(uow=_uow(), user_dao=dao)

    with pytest.raises(ValueError):
        await use_case.system(SetUserEmailDto(10, "dup@example.com"))
