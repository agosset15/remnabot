from typing import Protocol, runtime_checkable

from src.application.dto import SubscriptionDto, UserDto
from src.core.enums import PurchaseType


@runtime_checkable
class Mailer(Protocol):
    """High-level transactional email sender.

    Renders localized FTL templates and dispatches them through the shared
    low-level ``EmailSender`` (single SMTP configuration: ``EmailConfig``).
    """

    @property
    def is_enabled(self) -> bool: ...

    async def send_success_purchase(
        self, user: UserDto, subscription: SubscriptionDto, purchase_type: PurchaseType
    ) -> None: ...

    async def send_failed_purchase(self, user: UserDto) -> None: ...

    async def send_connect_telegram(self, user: UserDto) -> None: ...

    async def send_custom_message(self, user: UserDto, body: str) -> None: ...

    async def send_notification(self, user: UserDto, body: str) -> None: ...
