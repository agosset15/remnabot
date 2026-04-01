from typing import Protocol, runtime_checkable


@runtime_checkable
class Mailer(Protocol):
    """Protocol for sending transactional emails."""

    async def send_otp(self, email: str, code: str) -> None:
        """Send a one-time password code to the given email address."""
        ...
