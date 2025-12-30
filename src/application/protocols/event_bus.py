from typing import Any, Callable, Protocol, Type

from src.application.events.base import BaseEvent


class EventPublisher(Protocol):
    async def publish(self, event: BaseEvent) -> None: ...


class EventSubscriber(
    Protocol
): ...  # def subscribe(self, event_type: Type[BaseEvent], handler: Callable[..., Any]) -> None: ...
