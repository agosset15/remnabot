from dataclasses import dataclass
from typing import Optional, Self

from aiogram.types import User as AiogramUser
from loguru import logger

from src.application.common import Cryptographer, EventPublisher, Interactor
from src.application.common.dao import UserDao
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.events import UserRegisteredEvent
from src.core.config import AppConfig
from src.core.enums import Locale, UserRole


@dataclass(frozen=True)
class GetOrCreateUserDto:
    telegram_id: int
    username: Optional[str]
    full_name: str
    language_code: Optional[str]

    @classmethod
    def from_aiogram(cls, user: AiogramUser) -> Self:
        return cls(
            telegram_id=user.id,
            username=user.username,
            full_name=user.full_name,
            language_code=user.language_code,
        )


@dataclass(frozen=True)
class SetBotBlockedStatusDto:
    user: UserDto
    is_blocked: bool


class GetOrCreateUser(Interactor[GetOrCreateUserDto, UserDto]):
    def __init__(
        self,
        dao: UserDao,
        uow: UnitOfWork,
        config: AppConfig,
        cryptographer: Cryptographer,
        event_publisher: EventPublisher,
    ) -> None:
        self.dao = dao
        self.uow = uow
        self.config = config
        self.cryptographer = cryptographer
        self.event_publisher = event_publisher

    async def __call__(self, data: GetOrCreateUserDto) -> UserDto:
        async with self.uow:
            user = await self.dao.get_by_telegram_id(data.telegram_id)
            if user:
                return user

            user_dto = self._create_user_dto(data)
            user = await self.dao.create(user_dto)
            await self.uow.commit()

        await self._publish_event(user)
        logger.info(f"New user '{user.telegram_id}' created")
        return user

    def _create_user_dto(self, data: GetOrCreateUserDto) -> UserDto:
        is_root = data.telegram_id == self.config.bot.dev_id

        if data.language_code in self.config.locales:
            locale = Locale(data.language_code)
        else:
            locale = self.config.default_locale

        return UserDto(
            telegram_id=data.telegram_id,
            username=data.username,
            referral_code=self.cryptographer.generate_short_code(data.telegram_id),
            name=data.full_name,
            role=UserRole.ROOT if is_root else UserRole.USER,
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
    def __init__(self, dao: UserDao, uow: UnitOfWork) -> None:
        self.dao = dao
        self.uow = uow

    async def __call__(self, data: SetBotBlockedStatusDto) -> None:
        async with self.uow:
            await self.dao.set_bot_blocked_status(data.user.telegram_id, data.is_blocked)
            await self.uow.commit()

        logger.info(
            f"Bot blocked status for user '{data.user.telegram_id}' set to '{data.is_blocked}'"
        )
