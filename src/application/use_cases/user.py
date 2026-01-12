from dataclasses import dataclass
from typing import Optional, Self

from aiogram.types import ChatMemberUpdated
from aiogram.types import User as AiogramUser
from loguru import logger

from src.application.common import Cryptographer, EventPublisher, Interactor
from src.application.common.dao import UserDao
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.events import UserRegisteredEvent
from src.core.config import AppConfig
from src.core.enums import Locale, Role


@dataclass(frozen=True)
class GetOrCreateUserDto:
    telegram_id: int
    username: Optional[str]
    full_name: str
    language_code: Optional[str]
    event_type: str

    @classmethod
    def from_aiogram(cls, user: AiogramUser, event_type: str) -> Self:
        return cls(
            telegram_id=user.id,
            username=user.username,
            full_name=user.full_name,
            language_code=user.language_code,
            event_type=event_type,
        )


@dataclass(frozen=True)
class SetBotBlockedStatusDto:
    telegram_id: int
    is_blocked: bool


class GetOrCreateUser(Interactor[GetOrCreateUserDto, Optional[UserDto]]):
    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        config: AppConfig,
        cryptographer: Cryptographer,
        event_publisher: EventPublisher,
    ) -> None:
        self.uow = uow
        self.user_dao = user_dao
        self.config = config
        self.cryptographer = cryptographer
        self.event_publisher = event_publisher

    async def _execute(self, actor: UserDto, data: GetOrCreateUserDto) -> Optional[UserDto]:
        async with self.uow:
            user = await self.user_dao.get_by_telegram_id(data.telegram_id)
            if user:
                return user

            if data.event_type == ChatMemberUpdated.__name__:
                logger.debug(
                    f"Skipping user creation for '{data.telegram_id}' "
                    f"due to '{ChatMemberUpdated.__name__}' event"
                )
                return None

            user_dto = self._create_user_dto(data)
            user = await self.user_dao.create(user_dto)
            await self.uow.commit()

        await self._publish_event(user)
        logger.info(f"New user '{user.telegram_id}' created")
        return user

    def _create_user_dto(self, data: GetOrCreateUserDto) -> UserDto:
        is_owner = data.telegram_id == self.config.bot.owner_id

        if data.language_code in self.config.locales:
            locale = Locale(data.language_code)
        else:
            locale = self.config.default_locale

        return UserDto(
            telegram_id=data.telegram_id,
            username=data.username,
            referral_code=self.cryptographer.generate_short_code(data.telegram_id),
            name=data.full_name,
            role=Role.OWNER if is_owner else Role.USER,
            language=locale,
        )

    async def _publish_event(self, user: UserDto) -> None:
        await self.event_publisher.publish(
            UserRegisteredEvent(
                telegram_id=user.telegram_id,
                username=user.username,
                name=user.name,
            )
        )


class SetBotBlockedStatus(Interactor[SetBotBlockedStatusDto, None]):
    def __init__(self, uow: UnitOfWork, user_dao: UserDao) -> None:
        self.uow = uow
        self.user_dao = user_dao

    async def _execute(self, actor: UserDto, data: SetBotBlockedStatusDto) -> None:
        async with self.uow:
            await self.user_dao.set_bot_blocked_status(data.telegram_id, data.is_blocked)
            await self.uow.commit()

        logger.info(f"Set bot blocked status for user '{data.telegram_id}' to '{data.is_blocked}'")
