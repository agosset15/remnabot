from typing import Optional, Union

from adaptix import Retort
from adaptix.conversion import impl_converter
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy import delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto import UserDTO
from src.application.protocols.dao import UserDAO
from src.core.constants import TTL_1H, TTL_6H
from src.core.enums import UserRole
from src.infrastructure.database.models import User
from src.infrastructure.redis.cache import invalidate_cache, provide_cache
from src.infrastructure.redis.keys import (
    USER_COUNT_PREFIX,
    USER_LIST_PREFIX,
    UserCacheKey,
    UserRoleKey,
)


class UserDAOImpl(UserDAO):
    def __init__(self, session: AsyncSession, retort: Retort, redis: Redis) -> None:
        self.session = session
        self.retort = retort
        self.redis = redis

    @staticmethod
    @impl_converter
    def _convert_to_dto(db_user: User) -> UserDTO: ...  # type: ignore[empty-body]

    @staticmethod
    @impl_converter
    def _convert_to_dto_list(db_users: list[User]) -> list[UserDTO]: ...  # type: ignore[empty-body]

    @invalidate_cache(key_builder=[USER_COUNT_PREFIX, USER_LIST_PREFIX])
    @invalidate_cache(key_builder=UserCacheKey)
    async def create(self, user: UserDTO) -> UserDTO:
        user_data = self.retort.dump(user)
        db_user = User(**user_data)

        self.session.add(db_user)
        await self.session.flush()

        logger.info(f"New user '{user.telegram_id}' created in database")
        return self._convert_to_dto(db_user)

    @provide_cache(ttl=TTL_1H, key_builder=UserCacheKey)
    async def get(self, telegram_id: int) -> Optional[UserDTO]:
        stmt = select(User).where(User.telegram_id == telegram_id)
        db_user = await self.session.scalar(stmt)

        if db_user:
            logger.debug(f"User '{telegram_id}' found in database")
            return self._convert_to_dto(db_user)

        logger.debug(f"User '{telegram_id}' not found")
        return None

    async def get_by_ids(self, telegram_ids: list[int]) -> list[UserDTO]:
        if not telegram_ids:
            return []

        stmt = select(User).where(User.telegram_id.in_(telegram_ids))
        result = await self.session.scalars(stmt)
        db_users = list(result.all())

        logger.debug(f"Retrieved '{len(db_users)}' users by ID list")
        return self._convert_to_dto_list(db_users)

    async def get_by_partial_name(self, query_name: str) -> list[UserDTO]:
        search_pattern = f"%{query_name}%"
        stmt = select(User).where(
            or_(
                User.name.ilike(search_pattern),
                User.username.ilike(search_pattern),
            )
        )
        result = await self.session.scalars(stmt)
        db_users = list(result.all())

        logger.debug(f"Found '{len(db_users)}' users matching query '{query_name}'")
        return self._convert_to_dto_list(db_users)

    @provide_cache(prefix=USER_LIST_PREFIX, ttl=TTL_1H)
    async def get_all(self, limit: int = 100, offset: int = 0) -> list[UserDTO]:
        stmt = select(User).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        db_users = list(result.all())

        logger.debug(
            f"Retrieved '{len(db_users)}' users from database "
            f"with limit '{limit}' and offset '{offset}'"
        )
        return self._convert_to_dto_list(db_users)

    async def exists(self, telegram_id: int) -> bool:
        stmt = select(select(User).where(User.telegram_id == telegram_id).exists())
        is_exists = await self.session.scalar(stmt) or False

        logger.debug(f"User '{telegram_id}' existence check: '{is_exists}'")
        return is_exists

    @invalidate_cache(key_builder=[USER_COUNT_PREFIX, USER_LIST_PREFIX])
    @invalidate_cache(key_builder=UserCacheKey)
    async def update(self, user: UserDTO) -> Optional[UserDTO]:
        if not user.changed_data:
            logger.debug(f"No changes detected for user '{user.telegram_id}', skipping update")
            return await self.get(user.telegram_id)

        stmt = (
            update(User)
            .where(User.telegram_id == user.telegram_id)
            .values(**user.changed_data)
            .returning(User)
        )
        db_user = await self.session.scalar(stmt)

        if db_user:
            logger.info(
                f"User '{user.telegram_id}' updated successfully with data '{user.changed_data}'"
            )
            return self._convert_to_dto(db_user)

        logger.warning(f"Failed to update user '{user.telegram_id}': user not found")
        return None

    @invalidate_cache(key_builder=[USER_COUNT_PREFIX, USER_LIST_PREFIX])
    @invalidate_cache(key_builder=UserCacheKey)
    async def delete(self, telegram_id: int) -> bool:
        stmt = delete(User).where(User.telegram_id == telegram_id).returning(User.id)
        result = await self.session.execute(stmt)
        deleted_id = result.scalar_one_or_none()

        if deleted_id:
            logger.info(f"User '{telegram_id}' deleted from database")
            return True

        logger.debug(f"User '{telegram_id}' not found for deletion")
        return False

    @provide_cache(prefix=USER_COUNT_PREFIX, ttl=TTL_6H)
    async def count(self) -> int:
        stmt = select(func.count()).select_from(User)
        total = await self.session.scalar(stmt) or 0

        logger.debug(f"Total users count requested: '{total}'")
        return total

    @provide_cache(ttl=TTL_1H, key_builder=UserRoleKey)
    async def filter_by_role(self, role: Union[UserRole, list[UserRole]]) -> list[UserDTO]:
        stmt = select(User)

        if isinstance(role, list):
            stmt = stmt.where(User.role.in_(role))
        else:
            stmt = stmt.where(User.role == role)

        result = await self.session.scalars(stmt)
        db_users = list(result.all())

        logger.debug(f"Filtered '{len(db_users)}' users with role '{role}'")
        return self._convert_to_dto_list(db_users)
