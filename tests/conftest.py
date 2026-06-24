"""Shared pytest fixtures.

These tests are intentionally lightweight: pure logic and use cases exercised
with mocks, plus the real TranslatorHub so email templates are actually rendered.
No database / Redis / SMTP is required.
"""

import os

# Provide a minimal, valid configuration via env vars BEFORE importing any
# `src` module, so `AppConfig.get()` (called at import time in parts of the
# infrastructure layer) succeeds without relying on a local `.env` file.
# `setdefault` keeps any real values the developer already exported.
os.environ.setdefault("APP_DOMAIN", "example.com")
os.environ.setdefault("APP_CRYPT_KEY", "A6i+WajSI/d5sA7AK9pvXSOMaQpGk4gApBrPMw7rgRA=")
os.environ.setdefault("BOT_TOKEN", "123456:test-token")
os.environ.setdefault("BOT_SECRET_TOKEN", "test-secret-token")
os.environ.setdefault("BOT_OWNER_ID", "1")
os.environ.setdefault("BOT_SUPPORT_USERNAME", "support_bot")
os.environ.setdefault("REMNAWAVE_TOKEN", "test-remnawave-token")
os.environ.setdefault("REMNAWAVE_WEBHOOK_SECRET", "test-webhook-secret")
os.environ.setdefault("DATABASE_PASSWORD", "test-db-password")

import pytest  # noqa: E402
from adaptix import Retort  # noqa: E402

from src.core.constants import ASSETS_DIR  # noqa: E402
from src.core.enums import Locale  # noqa: E402
from src.infrastructure.services import TranslatorHubImpl  # noqa: E402
from src.infrastructure.services.i18n import LayeredFileStorage  # noqa: E402

_TRANSLATIONS_DIR = ASSETS_DIR / "translations"


@pytest.fixture(scope="session")
def translator_hub() -> TranslatorHubImpl:
    """Real TranslatorHub loaded from the project's RU translations."""
    storage = LayeredFileStorage(
        user_translations_dir=_TRANSLATIONS_DIR,
        default_translations_dir=_TRANSLATIONS_DIR,
    )
    locale = Locale.RU
    return TranslatorHubImpl(
        {locale: (locale,)},
        root_locale=locale,
        storage=storage,
        retort=Retort(),
    )


@pytest.fixture
def ru(translator_hub):
    """RU translator runner."""
    return translator_hub.get_translator_by_locale(Locale.RU)
