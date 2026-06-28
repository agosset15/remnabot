from typing import Optional

from pydantic import SecretStr, field_validator, model_validator

from src.core.utils.validators import is_valid_domain

from .base import BaseConfig


class WebConfig(BaseConfig, env_prefix="WEB_"):
    enabled: bool = False
    cabinet_url: str = ""
    domain: Optional[SecretStr] = None
    referral_via_domain: bool = False

    @property
    def base_url(self) -> Optional[str]:
        if not self.domain:
            return None
        return f"https://{self.domain.get_secret_value()}"

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, field: Optional[SecretStr]) -> Optional[SecretStr]:
        if field is None:
            return None
        if not is_valid_domain(field.get_secret_value()):
            raise ValueError("WEB_DOMAIN has invalid format")
        return field

    @model_validator(mode="after")
    def ignore_referral_via_domain_without_domain(self) -> "WebConfig":
        # referral_via_domain only makes sense with a configured WEB_DOMAIN:
        # without one there is no web base URL to build referral links from,
        # so the flag is ignored (forced off).
        if self.domain is None:
            self.referral_via_domain = False
        return self
