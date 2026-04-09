from dataclasses import dataclass
from typing import Optional

from loguru import logger

from src.application.common import Interactor
from src.application.common.dao import UserDao
from src.application.common.policy import Permission
from src.application.dto import UserDto
from src.core.constants import REMNASHOP_PREFIX


@dataclass(frozen=True)
class SearchUsersDto:
    query: Optional[str] = None
    forward_from_id: Optional[int] = None
    forward_sender_name: Optional[str] = None
    is_forwarded_from_bot: bool = False


class SearchUsers(Interactor[SearchUsersDto, list[UserDto]]):
    required_permission = Permission.USER_SEARCH

    def __init__(self, user_dao: UserDao):
        self.user_dao = user_dao

    async def _execute(self, actor: UserDto, data: SearchUsersDto) -> list[UserDto]:
        if self._is_forwarded_from_real_user(data):
            return await self._search_by_forward(data)

        if data.query:
            return await self._search_by_query(data.query.strip().removeprefix("@"))

        return []

    def _is_forwarded_from_real_user(self, data: SearchUsersDto) -> bool:
        return (
            bool(data.forward_from_id or data.forward_sender_name)
            and not data.is_forwarded_from_bot
        )

    async def _search_by_forward(self, data: SearchUsersDto) -> list[UserDto]:
        if data.forward_from_id:
            user = await self.user_dao.get_by_telegram_id(data.forward_from_id)
            if user:
                logger.info(f"Search by forwarded message, found user '{data.forward_from_id}'")
                return [user]
            logger.warning(f"Search by forwarded message, user '{data.forward_from_id}' not found")

        if data.forward_sender_name:
            sender_name = data.forward_sender_name.strip()
            users = await self.user_dao.get_by_partial_name(sender_name)
            logger.info(f"Search by forwarded name '{sender_name}', found '{len(users)}' users")
            return users

        return []

    async def _search_by_query(self, query: str) -> list[UserDto]:
        if query.isdigit():
            return await self._search_by_numeric_id(int(query))

        if query.startswith(REMNASHOP_PREFIX):
            return await self._search_by_remnashop_id(query)

        return await self._search_by_name_or_email(query)

    async def _search_by_numeric_id(self, numeric_id: int) -> list[UserDto]:
        results = []
        results.extend(await self._find_by_telegram_id(numeric_id))
        results.extend(await self._find_by_user_id(numeric_id))
        return results

    async def _search_by_remnashop_id(self, query: str) -> list[UserDto]:
        try:
            numeric_id = int(query.split("_", maxsplit=1)[1])
        except (IndexError, ValueError):
            logger.warning(f"Failed to parse Remnashop ID from query '{query}'")
            return []

        results = []
        results.extend(await self._find_by_telegram_id(numeric_id))
        results.extend(await self._find_by_user_id(numeric_id))
        return results

    async def _search_by_name_or_email(self, name: str) -> list[UserDto]:
        results = []
        results.extend(await self.user_dao.get_by_partial_name(name))
        results.append(await self.user_dao.get_by_email(name))
        logger.info(f"Searched users by partial name '{name}', found '{len(results)}' users")
        return results

    async def _find_by_telegram_id(self, numeric_id: int) -> list[UserDto]:
        user = await self.user_dao.get_by_telegram_id(numeric_id)
        if user:
            logger.info(f"Searched by Telegram ID '{numeric_id}', user found")
            return [user]
        logger.warning(f"Searched by Telegram ID '{numeric_id}', user not found")
        return []

    async def _find_by_user_id(self, numeric_id: int) -> list[UserDto]:
        user = await self.user_dao.get_by_id(numeric_id)
        if user:
            logger.info(f"Searched by user ID '{numeric_id}', user found")
            return [user]
        logger.warning(f"Searched by user ID '{numeric_id}', user not found")
        return []
