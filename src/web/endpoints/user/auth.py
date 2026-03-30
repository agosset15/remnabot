import json
from datetime import datetime, timedelta, timezone
from typing import Optional

import httpx
from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, HTTPException, Response, Depends
from jose import jwt, JWTError
from pydantic import BaseModel
from redis.asyncio import Redis

from src.application.common.dao import UserDao
from src.application.common.cryptography import Cryptographer
from src.application.dto import UserDto
from src.core.config import AppConfig
from src.core.enums import Locale, Role
from src.web.dependencies.auth import get_current_user

router = APIRouter()

JWKS_URL = "https://oauth.telegram.org/.well-known/jwks.json"
JWKS_CACHE_KEY = "telegram:jwks"
JWKS_CACHE_TTL = 3600


async def _get_jwks(redis: Redis) -> dict:
    cached = await redis.get(JWKS_CACHE_KEY)
    if cached:
        return json.loads(cached)

    async with httpx.AsyncClient() as client:
        resp = await client.get(JWKS_URL)
        resp.raise_for_status()
        jwks = resp.json()

    await redis.setex(JWKS_CACHE_KEY, JWKS_CACHE_TTL, json.dumps(jwks))
    return jwks


async def _validate_telegram_id_token(id_token: str, client_id: int, redis: Redis) -> dict:
    jwks = await _get_jwks(redis)

    try:
        claims = jwt.decode(
            id_token,
            jwks,
            algorithms=["RS256"],
            audience=str(client_id),
        )
    except JWTError as e:
        raise ValueError(f"Invalid id_token: {e}")

    if claims.get("iss") != "https://oauth.telegram.org":
        raise ValueError("Invalid issuer")

    return claims


def _create_session_jwt(telegram_id: int, secret: str, expire_hours: int) -> str:
    payload = {
        "sub": str(telegram_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=expire_hours),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


class UserResponse(BaseModel):
    telegram_id: int
    username: Optional[str]
    name: str
    role: str
    language: str
    points: int
    personal_discount: int
    is_trial_available: bool


class TelegramAuthRequest(BaseModel):
    id_token: str


class AuthResponse(BaseModel):
    ok: bool
    user: UserResponse


def _to_user_response(user: UserDto) -> UserResponse:
    return UserResponse(
        telegram_id=user.telegram_id,
        username=user.username,
        name=user.name,
        role=str(user.role),
        language=str(user.language),
        points=user.points,
        personal_discount=user.personal_discount,
        is_trial_available=user.is_trial_available,
    )


@router.post("/telegram")
@inject
async def login_telegram(
    body: TelegramAuthRequest,
    response: Response,
    user_dao: FromDishka[UserDao] = ...,
    config: FromDishka[AppConfig] = ...,
    cryptographer: FromDishka[Cryptographer] = ...,
    redis: FromDishka[Redis] = ...,
) -> AuthResponse:
    try:
        claims = await _validate_telegram_id_token(body.id_token, config.tg_client_id, redis)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    telegram_id: int = claims["id"]
    name: str = claims.get("name", "")
    username: Optional[str] = claims.get("preferred_username")

    user = await user_dao.get_by_telegram_id(telegram_id)

    if user is None:
        referral_code = cryptographer.generate_short_code(telegram_id)
        user = await user_dao.create(
            UserDto(
                telegram_id=telegram_id,
                name=name,
                username=username,
                role=Role.USER,
                language=Locale(config.default_locale),
                referral_code=referral_code,
            )
        )

    if user.is_blocked:
        raise HTTPException(status_code=403, detail="User is blocked")

    if user.name != name or user.username != username:
        user.name = name
        user.username = username
        await user_dao.update(user)

    token = _create_session_jwt(
        telegram_id, config.jwt_secret.get_secret_value(), config.jwt_expire_hours
    )
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=60 * 60 * config.jwt_expire_hours,
    )

    return AuthResponse(ok=True, user=_to_user_response(user))


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie(key="session")
    return {"ok": True}


@router.get("/me")
@inject
async def get_me(
    current_user: UserDto = Depends(get_current_user),
) -> UserResponse:
    return _to_user_response(current_user)
