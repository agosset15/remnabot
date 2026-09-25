from typing import Optional

from pydantic import SecretStr, field_validator

from src.core.enums import LogLevel

from .base import BaseConfig


class SentryConfig(BaseConfig, env_prefix="SENTRY_"):
    dsn: Optional[SecretStr] = None
    environment: str = "production"
    release: Optional[str] = None

    # 0.0 disables performance tracing/profiling entirely (errors are still sent).
    traces_sample_rate: float = 0.0
    profiles_sample_rate: float = 0.0
    sample_rate: float = 1.0

    # Loguru bridge: `level` becomes breadcrumbs, `event_level` becomes Sentry issues.
    level: LogLevel = LogLevel.INFO
    event_level: LogLevel = LogLevel.ERROR

    # PII (Telegram ids, usernames, request bodies) is opt-in and off by default.
    send_default_pii: bool = False
    attach_stacktrace: bool = True
    max_breadcrumbs: int = 50
    shutdown_timeout: int = 5
    debug: bool = False

    @property
    def enabled(self) -> bool:
        if self.dsn is None:
            return False

        value = self.dsn.get_secret_value().strip()
        return bool(value) and value.lower() != "change_me"

    @field_validator("sample_rate", "traces_sample_rate", "profiles_sample_rate")
    @classmethod
    def validate_sample_rate(cls, field: float) -> float:
        if not 0.0 <= field <= 1.0:
            raise ValueError("Sentry sample rates must be between 0.0 and 1.0")

        return field
