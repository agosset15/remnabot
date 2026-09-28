"""Sentry wiring: config gating, secret scrubbing and PII gating.

No network is involved — the transport is replaced with a collector.
"""

import json
from typing import Any

import pytest
import sentry_sdk

from src.core import sentry as sentry_module
from src.core.config import AppConfig
from src.core.enums import SentryComponent

DSN = "https://public@localhost/1"


def _config(**overrides: Any) -> AppConfig:
    return AppConfig(_env_file=None, sentry=overrides)  # type: ignore[arg-type]


@pytest.fixture(autouse=True)
def _teardown_client() -> Any:
    yield
    sentry_sdk.get_global_scope().set_client(None)
    sentry_module._secrets = ()


def _collect() -> list[str]:
    payloads: list[str] = []

    def capture_envelope(envelope: Any) -> None:
        for item in envelope.items:
            payloads.append(json.dumps(item.payload.json, default=str))

    client = sentry_sdk.get_client()
    client.transport.capture_envelope = capture_envelope  # type: ignore[union-attr]
    return payloads


def test_disabled_without_dsn() -> None:
    config = _config()

    assert config.sentry.enabled is False
    assert sentry_module.setup_sentry(config, SentryComponent.WEB) is False
    assert sentry_module.is_enabled() is False
    assert sentry_module.capture_exception(ValueError("ignored")) is None


def test_disabled_with_placeholder_dsn() -> None:
    assert _config(dsn="change_me").sentry.enabled is False


def test_invalid_sample_rate_rejected() -> None:
    with pytest.raises(ValueError):
        _config(dsn=DSN, traces_sample_rate=1.5)


def test_secrets_are_scrubbed_from_events() -> None:
    config = _config(dsn=DSN)
    assert sentry_module.setup_sentry(config, SentryComponent.WEB) is True
    payloads = _collect()

    token = config.bot.token.get_secret_value()
    sentry_module.capture_exception(ValueError(f"leaked token: {token}"))
    sentry_sdk.flush(2)

    body = "\n".join(payloads)
    assert token not in body
    assert sentry_module.FILTERED in body


def test_user_payload_hides_pii_by_default() -> None:
    sentry_module.setup_sentry(_config(dsn=DSN), SentryComponent.WEB)

    assert sentry_module.user_payload(1, "nick", "Real Name") == {"id": "1"}
    assert sentry_module.user_payload(None) is None


def test_user_payload_includes_pii_when_opted_in() -> None:
    sentry_module.setup_sentry(_config(dsn=DSN, send_default_pii=True), SentryComponent.WEB)

    assert sentry_module.user_payload(1, "nick", "Real Name") == {
        "id": "1",
        "username": "nick",
        "name": "Real Name",
    }
