from typing import Any, Protocol


class Notifier(Protocol):
    async def system_notify(self, payload: Any) -> None: ...
