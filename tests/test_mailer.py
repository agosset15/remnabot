from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.core.enums import Locale, PurchaseType
from src.infrastructure.services.smtp_mailer import SmtpMailerImpl


@pytest.fixture
def email_sender() -> MagicMock:
    sender = MagicMock()
    sender.is_enabled = True
    sender.send = AsyncMock()
    return sender


@pytest.fixture
def bot_service() -> MagicMock:
    service = MagicMock()
    service.get_referral_url = AsyncMock(return_value="https://t.me/bot?start=ref")
    return service


@pytest.fixture
def mailer(translator_hub, email_sender, bot_service) -> SmtpMailerImpl:
    config = SimpleNamespace(default_locale=Locale.RU)
    return SmtpMailerImpl(
        config=config,
        email_sender=email_sender,
        i18n_hub=translator_hub,
        bot_service=bot_service,
    )


def _user(**kwargs) -> SimpleNamespace:
    data = {
        "email": "user@example.com",
        "referral_code": "ref",
        "language": Locale.RU,
        "log": "[user]",
    }
    data.update(kwargs)
    return SimpleNamespace(**data)


def _subscription() -> SimpleNamespace:
    return SimpleNamespace(
        url="https://sub.example/abc",
        expire_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
        device_limit=5,
        plan_snapshot=SimpleNamespace(name="Pro"),
    )


def test_is_enabled_delegates_to_email_sender(mailer, email_sender):
    email_sender.is_enabled = False
    assert mailer.is_enabled is False
    email_sender.is_enabled = True
    assert mailer.is_enabled is True


async def test_does_not_send_when_email_disabled(mailer, email_sender):
    email_sender.is_enabled = False
    await mailer.send_failed_purchase(_user())
    email_sender.send.assert_not_called()


async def test_does_not_send_when_user_has_no_email(mailer, email_sender):
    await mailer.send_failed_purchase(_user(email=None))
    email_sender.send.assert_not_called()


async def test_success_purchase_renders_and_sends(mailer, email_sender):
    await mailer.send_success_purchase(_user(), _subscription(), PurchaseType.NEW)

    email_sender.send.assert_awaited_once()
    kwargs = email_sender.send.await_args.kwargs
    assert kwargs["to"] == "user@example.com"
    assert kwargs["subject"]
    assert kwargs["body"]
    assert "sub.example/abc" in kwargs["html"]
    assert "Pro" in kwargs["html"]


async def test_notification_plain_body_strips_html(mailer, email_sender):
    await mailer.send_notification(_user(), "<b>Hello</b> <i>world</i>")

    kwargs = email_sender.send.await_args.kwargs
    assert "<b>" not in kwargs["body"]
    assert "Hello" in kwargs["body"]
    assert "<b>Hello</b>" in kwargs["html"]
