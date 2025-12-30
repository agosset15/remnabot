from dishka import AnyOf, Provider, Scope, alias, provide

from src.application.protocols import Cryptographer, EventPublisher, EventSubscriber, Notifier
from src.application.services import NotificationService
from src.infrastructure.services import CryptographerImpl
from src.infrastructure.services.event_bus import EventBusImpl


class ServicesProvider(Provider):
    scope = Scope.APP

    cryptographer = provide(source=CryptographerImpl, provides=Cryptographer)

    event_bus = provide(EventBusImpl, scope=Scope.APP)

    publisher = alias(source=EventBusImpl, provides=EventPublisher)
    subscriber = alias(source=EventBusImpl, provides=EventSubscriber)

    notification = provide(
        NotificationService,
        scope=Scope.REQUEST,
        provides=AnyOf[Notifier, NotificationService],
    )
