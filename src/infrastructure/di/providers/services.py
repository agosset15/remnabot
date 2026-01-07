from dishka import AnyOf, Provider, Scope, alias, provide

from src.application.common import Cryptographer, EventPublisher, EventSubscriber, Notifier
from src.application.services import (
    AccessService,
    CommandService,
    NotificationService,
    ReferralService,
    WebhookService,
)
from src.infrastructure.services import CryptographerImpl, EventBusImpl


class ServicesProvider(Provider):
    scope = Scope.APP

    cryptographer = provide(source=CryptographerImpl, provides=Cryptographer)

    event_bus = provide(EventBusImpl)
    publisher = alias(source=EventBusImpl, provides=EventPublisher)
    subscriber = alias(source=EventBusImpl, provides=EventSubscriber)

    command = provide(source=CommandService)
    webhook = provide(source=WebhookService)

    notification = provide(
        NotificationService,
        scope=Scope.REQUEST,
        provides=AnyOf[Notifier, NotificationService],
    )

    access = provide(source=AccessService, scope=Scope.REQUEST)
    referral = provide(source=ReferralService, scope=Scope.REQUEST)
