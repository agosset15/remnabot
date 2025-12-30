from dishka import Provider, Scope, provide

from src.application.use_cases import CommandUseCase, SettingsUseCase, UserUseCase, WebhookUseCase


class UseCasesProvider(Provider):
    scope = Scope.APP

    command = provide(source=CommandUseCase)
    webhook = provide(source=WebhookUseCase)
    user = provide(UserUseCase, scope=Scope.REQUEST)
    settings = provide(SettingsUseCase, scope=Scope.REQUEST)
