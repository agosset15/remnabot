from src.application.dto import UserDto


def _user(**kwargs) -> UserDto:
    data = {"id": 1, "name": "tester"}
    data.update(kwargs)
    return UserDto(**data)


def test_has_only_email_true_for_email_only_user():
    assert _user(email="a@b.com", telegram_id=None).has_only_email is True


def test_has_only_email_false_when_telegram_present():
    assert _user(email="a@b.com", telegram_id=123).has_only_email is False


def test_has_only_email_false_without_email():
    assert _user(email=None, telegram_id=None).has_only_email is False
