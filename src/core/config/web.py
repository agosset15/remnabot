import re
from typing import Optional

from pydantic import SecretStr, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from src.core.constants import DOMAIN_REGEX

from .base import BaseConfig


class WebConfig(BaseConfig, env_prefix="WEB_"):
    domain: Optional[SecretStr] = None
    referral_via_domain: bool = False

    @property
    def base_url(self) -> Optional[str]:
        if not self.domain:
            return None
        return f"https://{self.domain.get_secret_value()}"

    @field_validator("domain")
    @classmethod
    def validate_domain(cls, field: Optional[SecretStr], info: FieldValidationInfo) -> Optional[SecretStr]:
        if field is None:
            return None
        if not re.match(DOMAIN_REGEX, field.get_secret_value()):
            raise ValueError("WEB_DOMAIN has invalid format")
        return field
