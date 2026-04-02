from typing import Protocol, runtime_checkable

from src.application.dto import SubscriptionDto, UserDto


@runtime_checkable
class Mailer(Protocol):
    """Protocol for sending transactional emails."""

    async def send_otp(self, email: str, code: str) -> None: ...

    async def send_success_purchase(self, user: UserDto, subscription: SubscriptionDto) -> None: ...

    async def send_failed_purchase(self, user: UserDto) -> None: ...
