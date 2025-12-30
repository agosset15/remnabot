from dataclasses import dataclass, field
from typing import Optional

from pydantic import SecretStr

from src.core.constants import T_ME
from src.core.enums import (
    AccessMode,
    Currency,
    ReferralAccrualStrategy,
    ReferralLevel,
    ReferralRewardStrategy,
    ReferralRewardType,
    SystemNotificationType,
    UserNotificationType,
)
from src.core.types import NotificationType

from .base import TrackableDTO


def get_default_notifications() -> dict[str, bool]:
    system_keys = {ntf.value: True for ntf in SystemNotificationType}
    user_keys = {ntf.value: True for ntf in UserNotificationType}
    return {**system_keys, **user_keys}


@dataclass(kw_only=True)
class AccessSettingsDTO:
    mode: AccessMode = AccessMode.PUBLIC
    registration_allowed: bool = True
    purchases_allowed: bool = True

    def can_register(self) -> bool:
        if self.mode == AccessMode.RESTRICTED:
            return False
        return self.registration_allowed


@dataclass(kw_only=True)
class RequirementSettingsDTO:
    rules_required: bool = False
    channel_required: bool = False

    rules_link: SecretStr = SecretStr("https://telegram.org/tos/")
    channel_id: Optional[int] = None
    channel_link: SecretStr = SecretStr("@remna_shop")

    @property
    def channel_has_username(self) -> bool:
        return self.channel_link.get_secret_value().startswith("@")

    @property
    def get_url_channel_link(self) -> str:
        if self.channel_has_username:
            return f"{T_ME}{self.channel_link.get_secret_value()[1:]}"
        else:
            return self.channel_link.get_secret_value()


@dataclass(kw_only=True)
class NotificationsSettingsDTO:
    settings: dict[str, bool] = field(default_factory=get_default_notifications)

    def is_enabled(self, ntf_type: NotificationType) -> bool:
        return self.settings.get(ntf_type, True)

    def toggle(self, ntf_type: NotificationType) -> None:
        self.settings[ntf_type] = not self.is_enabled(ntf_type)


@dataclass(kw_only=True)
class ReferralRewardSettingsDTO:
    type: ReferralRewardType = ReferralRewardType.EXTRA_DAYS
    strategy: ReferralRewardStrategy = ReferralRewardStrategy.AMOUNT
    config: dict[ReferralLevel, int] = field(default_factory=lambda: {ReferralLevel.FIRST: 5})

    @property
    def is_identical(self) -> bool:
        values = list(self.config.values())
        return len(values) <= 1 or all(v == values[0] for v in values)

    @property
    def is_points(self) -> bool:
        return self.type == ReferralRewardType.POINTS

    @property
    def is_extra_days(self) -> bool:
        return self.type == ReferralRewardType.EXTRA_DAYS


@dataclass(kw_only=True)
class ReferralSettingsDTO:
    enable: bool = True
    level: ReferralLevel = ReferralLevel.FIRST
    accrual_strategy: ReferralAccrualStrategy = ReferralAccrualStrategy.ON_FIRST_PAYMENT
    reward: ReferralRewardSettingsDTO = field(default_factory=ReferralRewardSettingsDTO)


@dataclass(kw_only=True)
class SettingsDTO(TrackableDTO):
    default_currency: Currency = Currency.XTR
    access: AccessSettingsDTO = field(default_factory=AccessSettingsDTO)
    requirements: RequirementSettingsDTO = field(default_factory=RequirementSettingsDTO)
    notifications: NotificationsSettingsDTO = field(default_factory=NotificationsSettingsDTO)
    referral: ReferralSettingsDTO = field(default_factory=ReferralSettingsDTO)
