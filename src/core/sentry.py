"""Sentry wiring: SDK initialization and thin, no-op-safe capture helpers.

``setup_sentry()`` must be called *after* :func:`src.core.logger.setup_logger`,
because ``setup_logger`` calls ``logger.remove()`` — which would drop the sinks
installed by ``LoguruIntegration``.
"""

import asyncio
from typing import Any, Final, Literal, Optional

import sentry_sdk
from loguru import logger
from pydantic import BaseModel, SecretStr
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.loguru import LoguruIntegration
from sentry_sdk.types import Event, Hint

from src.__version__ import __version__
from src.core.config import AppConfig
from src.core.enums import LogLevel, SentryComponent

SentryLevel = Literal["fatal", "critical", "error", "warning", "info", "debug"]

FILTERED: Final[str] = "[Filtered]"
MIN_SECRET_LENGTH: Final[int] = 8
MAX_SCRUB_DEPTH: Final[int] = 12

_LOGURU_LEVELS: Final[dict[LogLevel, int]] = {
    LogLevel.NOTSET: 0,
    LogLevel.DEBUG: 10,
    LogLevel.INFO: 20,
    LogLevel.WARN: 30,
    LogLevel.WARNING: 30,
    LogLevel.ERROR: 40,
    LogLevel.CRITICAL: 50,
    LogLevel.FATAL: 50,
}

_secrets: tuple[str, ...] = ()


def _to_loguru_level(level: LogLevel) -> int:
    return _LOGURU_LEVELS.get(level, 20)


def _collect_secrets(model: BaseModel, depth: int = 0) -> set[str]:
    """Walk a pydantic config tree and gather every ``SecretStr`` value."""
    secrets: set[str] = set()

    if depth > MAX_SCRUB_DEPTH:
        return secrets

    for value in dict(model).values():
        if isinstance(value, SecretStr):
            raw = value.get_secret_value().strip()
            if len(raw) >= MIN_SECRET_LENGTH:
                secrets.add(raw)
        elif isinstance(value, BaseModel):
            secrets |= _collect_secrets(value, depth + 1)

    return secrets


def _scrub(value: Any, depth: int = 0) -> Any:
    """Replace known secret substrings anywhere inside an event payload."""
    if depth > MAX_SCRUB_DEPTH:
        return value

    if isinstance(value, str):
        for secret in _secrets:
            if secret in value:
                value = value.replace(secret, FILTERED)
        return value

    if isinstance(value, dict):
        return {key: _scrub(item, depth + 1) for key, item in value.items()}

    if isinstance(value, list):
        return [_scrub(item, depth + 1) for item in value]

    if isinstance(value, tuple):
        return tuple(_scrub(item, depth + 1) for item in value)

    return value


def _before_send(event: Event, hint: Hint) -> Optional[Event]:
    scrubbed: Event = _scrub(event)
    return scrubbed


def _resolve_release(config: AppConfig) -> str:
    if config.sentry.release:
        return config.sentry.release

    version = config.build.tag or config.build.commit or __version__
    return f"remnashop@{version}"


def setup_sentry(config: AppConfig, component: SentryComponent) -> bool:
    """Initialize the Sentry SDK for one process. Returns ``False`` when disabled."""
    global _secrets

    if not config.sentry.enabled:
        logger.info("Sentry is disabled (SENTRY_DSN is not set)")
        return False

    _secrets = tuple(sorted(_collect_secrets(config), key=len, reverse=True))
    release = _resolve_release(config)

    sentry_sdk.init(
        dsn=config.sentry.dsn.get_secret_value() if config.sentry.dsn else None,
        environment=config.sentry.environment,
        release=release,
        sample_rate=config.sentry.sample_rate,
        traces_sample_rate=config.sentry.traces_sample_rate,
        profiles_sample_rate=config.sentry.profiles_sample_rate,
        send_default_pii=config.sentry.send_default_pii,
        attach_stacktrace=config.sentry.attach_stacktrace,
        max_breadcrumbs=config.sentry.max_breadcrumbs,
        shutdown_timeout=config.sentry.shutdown_timeout,
        debug=config.sentry.debug,
        in_app_include=["src"],
        ignore_errors=[asyncio.CancelledError, KeyboardInterrupt],
        before_send=_before_send,
        before_send_transaction=_before_send,
        integrations=[
            AsyncioIntegration(),
            LoguruIntegration(
                level=_to_loguru_level(config.sentry.level),
                event_level=_to_loguru_level(config.sentry.event_level),
            ),
        ],
        # stdlib logging is funnelled into loguru by InterceptHandler, so leaving
        # LoggingIntegration on would report every record twice.
        disabled_integrations=[LoggingIntegration()],
    )

    sentry_sdk.set_tag("component", component.value)
    sentry_sdk.set_tag("bot_id", config.bot.id)
    sentry_sdk.set_context(
        "build",
        {
            "time": config.build.time,
            "branch": config.build.branch,
            "commit": config.build.commit,
            "tag": config.build.tag,
            "version": __version__,
        },
    )

    logger.info(f"Sentry initialized for '{component.value}' (release '{release}')")
    return True


def is_enabled() -> bool:
    client = sentry_sdk.get_client()
    return bool(client) and client.is_active()


def user_payload(
    telegram_id: Optional[int],
    username: Optional[str] = None,
    name: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    """Build a Sentry user payload; identifying fields require SENTRY_SEND_DEFAULT_PII."""
    if telegram_id is None:
        return None

    user: dict[str, Any] = {"id": str(telegram_id)}

    if is_enabled() and sentry_sdk.get_client().should_send_default_pii():
        user["username"] = username
        user["name"] = name

    return user


def set_user(
    telegram_id: Optional[int],
    username: Optional[str] = None,
    name: Optional[str] = None,
) -> None:
    """Attach the current Telegram user to the active Sentry scope."""
    if not is_enabled():
        return

    sentry_sdk.set_user(user_payload(telegram_id, username, name))


def capture_exception(
    exception: BaseException,
    *,
    tags: Optional[dict[str, Any]] = None,
    contexts: Optional[dict[str, dict[str, Any]]] = None,
    extras: Optional[dict[str, Any]] = None,
    user: Optional[dict[str, Any]] = None,
    level: SentryLevel = "error",
    fingerprint: Optional[list[str]] = None,
) -> Optional[str]:
    """Send an exception to Sentry. No-op (returns ``None``) when Sentry is off."""
    if not is_enabled():
        return None

    with sentry_sdk.new_scope() as scope:
        scope.level = level

        if fingerprint:
            scope.fingerprint = fingerprint

        for key, value in (tags or {}).items():
            scope.set_tag(key, value)

        for key, value in (contexts or {}).items():
            scope.set_context(key, value)

        for key, value in (extras or {}).items():
            scope.set_extra(key, value)

        if user:
            scope.set_user(user)

        return sentry_sdk.capture_exception(exception)


def capture_message(
    message: str,
    *,
    level: SentryLevel = "info",
    tags: Optional[dict[str, Any]] = None,
    extras: Optional[dict[str, Any]] = None,
) -> Optional[str]:
    if not is_enabled():
        return None

    with sentry_sdk.new_scope() as scope:
        for key, value in (tags or {}).items():
            scope.set_tag(key, value)

        for key, value in (extras or {}).items():
            scope.set_extra(key, value)

        return sentry_sdk.capture_message(message, level=level)


def add_breadcrumb(
    message: str,
    *,
    category: str = "app",
    level: SentryLevel = "info",
    data: Optional[dict[str, Any]] = None,
) -> None:
    if not is_enabled():
        return

    sentry_sdk.add_breadcrumb(
        category=category,
        message=message,
        level=level,
        data=data or {},
    )


async def flush(timeout: Optional[float] = None) -> None:
    """Flush pending events without blocking the event loop."""
    if not is_enabled():
        return

    await asyncio.to_thread(sentry_sdk.flush, timeout)
