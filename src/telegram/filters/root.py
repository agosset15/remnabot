from typing import Any

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.application.dto.user import UserDTO
from src.core.config import AppConfig
from src.core.constants import CONFIG_KEY, USER_KEY


class RootFilter(BaseFilter):
    async def __call__(self, event: Message, **data: Any) -> bool:
        config: AppConfig = data[CONFIG_KEY]
        user: UserDTO = data[USER_KEY]
        return user.telegram_id == config.bot.dev_id
