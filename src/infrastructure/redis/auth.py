import json
from typing import Any, Optional

from redis.asyncio import Redis

from src.infrastructure.redis.key_builder import serialize_storage_key
from src.infrastructure.redis.keys import (
    EmailCodeAttemptsKey,
    EmailLoginCodeKey,
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

    async def store_email_login_code(self, email: str, payload: dict[str, Any], ttl: int) -> None:
        key = serialize_storage_key(EmailLoginCodeKey(email=email))
        await self.redis.setex(key, ttl, json.dumps(payload))

    async def get_email_login_code(self, email: str) -> Optional[dict[str, Any]]:
        key = serialize_storage_key(EmailLoginCodeKey(email=email))
        raw = await self.redis.get(key)
        if raw is None:
            return None
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None

    async def revoke_email_login_code(self, email: str) -> None:
        key = serialize_storage_key(EmailLoginCodeKey(email=email))
        await self.redis.delete(key)

    async def incr_email_code_attempts(self, email: str, ttl: int) -> int:
        key = serialize_storage_key(EmailCodeAttemptsKey(email=email))
        attempts = await self.redis.incr(key)
        if attempts == 1:
            await self.redis.expire(key, ttl)
        return int(attempts)

    async def reset_email_code_attempts(self, email: str) -> None:
        key = serialize_storage_key(EmailCodeAttemptsKey(email=email))
        await self.redis.delete(key)
