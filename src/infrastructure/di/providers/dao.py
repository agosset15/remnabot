from adaptix import ExtraSkip, P, Retort, dumper, loader, name_mapping
from adaptix._internal.provider.loc_stack_filtering import OriginSubclassLSC
from dishka import Provider, Scope, provide
from pydantic import SecretStr

from src.application.protocols.dao import SettingsDAO, UserDAO, WebhookDAO
from src.core.enums import ReferralLevel
from src.infrastructure.database.dao import SettingsDAOImpl, UserDAOImpl, WebhookDAOImpl
from src.infrastructure.redis.key_builder import StorageKey, serialize_storage_key


class DaoProvider(Provider):
    scope = Scope.APP

    webhook = provide(source=WebhookDAOImpl, provides=WebhookDAO)

    settings = provide(source=SettingsDAOImpl, provides=SettingsDAO, scope=Scope.REQUEST)
    user = provide(source=UserDAOImpl, provides=UserDAO, scope=Scope.REQUEST)

    @provide
    def get_retort(self) -> Retort:
        retort = Retort(
            recipe=[
                loader(
                    dict[ReferralLevel, int],
                    lambda data: {ReferralLevel(int(k)): v for k, v in data.items()},
                ),
                dumper(OriginSubclassLSC(StorageKey), serialize_storage_key),
                name_mapping(extra_in=ExtraSkip()),
                loader(P[SecretStr], SecretStr),
                dumper(P[SecretStr], lambda v: v.get_secret_value()),
            ]
        )

        return retort
