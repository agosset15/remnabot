from typing import Optional

from redis.asyncio import Redis

from src.infrastructure.redis.key_builder import serialize_storage_key
from src.infrastructure.redis.keys import (
    PasswordResetCooldownKey,
    PasswordResetTokenKey,
    RefreshTokenKey,
    UserTokensKey,
)


class RedisAuthRepository:
    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def store_refresh_token(self, token: str, user_id: int, ttl: int) -> None:
        token_key = serialize_storage_key(RefreshTokenKey(token=token))
        user_set_key = serialize_storage_key(UserTokensKey(user_id=user_id))
        await self.redis.setex(token_key, ttl, str(user_id))
        await self.redis.sadd(user_set_key, token)  # type: ignore[misc]
        await self.redis.expire(user_set_key, ttl)

    async def get_user_id_by_refresh_token(self, token: str) -> Optional[int]:
        key = serialize_storage_key(RefreshTokenKey(token=token))
        value = await self.redis.get(key)
        if value is None:
            return None
        return int(value)

    async def revoke_refresh_token(self, token: str) -> None:
        token_key = serialize_storage_key(RefreshTokenKey(token=token))
        value = await self.redis.getdel(token_key)
        if value is not None:
            user_set_key = serialize_storage_key(UserTokensKey(user_id=int(value)))
            await self.redis.srem(user_set_key, token)  # type: ignore[misc]

    async def get_and_revoke_refresh_token(self, token: str) -> Optional[int]:
        token_key = serialize_storage_key(RefreshTokenKey(token=token))
        value = await self.redis.getdel(token_key)
        if value is None:
            return None
        user_id = int(value)
        user_set_key = serialize_storage_key(UserTokensKey(user_id=user_id))
        await self.redis.srem(user_set_key, token)  # type: ignore[misc]
        return user_id

    async def revoke_all_user_tokens(self, user_id: int) -> None:
        user_set_key = serialize_storage_key(UserTokensKey(user_id=user_id))
        tokens = await self.redis.smembers(user_set_key)  # type: ignore[misc]
        if tokens:
            token_keys = [serialize_storage_key(RefreshTokenKey(token=t)) for t in tokens]
            await self.redis.delete(*token_keys)
        await self.redis.delete(user_set_key)

    async def store_password_reset_token(self, token_hash: str, user_id: int, ttl: int) -> None:
        key = serialize_storage_key(PasswordResetTokenKey(token_hash=token_hash))
        await self.redis.setex(key, ttl, str(user_id))

    async def consume_password_reset_token(self, token_hash: str) -> Optional[int]:
        key = serialize_storage_key(PasswordResetTokenKey(token_hash=token_hash))
        value = await self.redis.getdel(key)
        if value is None:
            return None
        return int(value)

    async def revoke_password_reset_token(self, token_hash: str) -> None:
        key = serialize_storage_key(PasswordResetTokenKey(token_hash=token_hash))
        await self.redis.delete(key)

    async def try_start_password_reset_cooldown(self, email_hash: str, ttl: int) -> bool:
        key = serialize_storage_key(PasswordResetCooldownKey(email_hash=email_hash))
        return bool(await self.redis.set(key, "1", ex=ttl, nx=True))

    async def clear_password_reset_cooldown(self, email_hash: str) -> None:
        key = serialize_storage_key(PasswordResetCooldownKey(email_hash=email_hash))
        await self.redis.delete(key)
