import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import httpx
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException, Response
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from redis.asyncio import Redis

from src.application.common.cryptography import Cryptographer
from src.application.common.dao import UserDao
from src.application.common.mailer import Mailer
from src.application.dto import UserDto
from src.application.use_cases.user.commands.registration import (
    GetOrCreateTelegramUser,
    GetOrCreateTelegramUserDto,
)
from src.core.config import AppConfig
from src.core.enums import JwtTyp, Locale, Role
from src.infrastructure.redis.key_builder import serialize_storage_key
from src.infrastructure.redis.keys import EmailOtpKey
from src.web.dependencies.auth import get_current_user

router = APIRouter()

JWKS_URL = "https://oauth.telegram.org/.well-known/jwks.json"
JWKS_CACHE_KEY = "telegram:jwks"
JWKS_CACHE_TTL = 3600

OTP_TTL = 600  # seconds — how long a code is valid
OTP_RESEND_COOLDOWN = 60  # seconds — minimum gap between re-sends


class UserResponse(BaseModel):
    telegram_id: Optional[int]
    email: Optional[str]
    username: Optional[str]
    name: str
    role: str
    language: str
    points: int
    personal_discount: int
    is_trial_available: bool


class AuthResponse(BaseModel):
    ok: bool
    user: UserResponse


# ------------------------------------------------------------------
# Telegram auth
# ------------------------------------------------------------------


class TelegramAuthRequest(BaseModel):
    id_token: str


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


def _set_session_cookie(
    response: Response,
    *,
    sub: int,
    typ: str,
    secret: str,
    expire_hours: int,
) -> None:
    payload = {
        "sub": str(sub),
        "typ": typ,
        "exp": datetime.now(timezone.utc) + timedelta(hours=expire_hours),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=60 * 60 * expire_hours,
    )


def _to_user_response(user: UserDto) -> UserResponse:
    return UserResponse(
        telegram_id=user.telegram_id,
        email=user.email,
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
    get_or_create_user: FromDishka[GetOrCreateTelegramUser],
    config: FromDishka[AppConfig],
    cryptographer: FromDishka[Cryptographer],
    redis: FromDishka[Redis],
) -> AuthResponse:
    try:
        claims = await _validate_telegram_id_token(body.id_token, config.tg_client_id, redis)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    telegram_id: int = claims["id"]
    name: str = claims.get("name", "")
    username: Optional[str] = claims.get("preferred_username")

    user = await get_or_create_user.system(
        GetOrCreateTelegramUserDto(
            telegram_id=telegram_id, full_name=name, username=username, language_code=None
        )
    )

    if user.is_blocked:
        raise HTTPException(status_code=403, detail="User is blocked")

    _set_session_cookie(
        response,
        sub=telegram_id,
        typ=JwtTyp.TELEGRAM_ID,
        secret=config.jwt_secret.get_secret_value(),
        expire_hours=config.jwt_expire_hours,
    )

    return AuthResponse(ok=True, user=UserResponse.model_validate(user, from_attributes=True))


# ------------------------------------------------------------------
# Email OTP auth
# ------------------------------------------------------------------


class EmailOtpRequest(BaseModel):
    email: EmailStr


class EmailOtpVerifyRequest(BaseModel):
    email: EmailStr
    code: str


def _generate_otp() -> str:
    """Return a cryptographically random 6-digit string."""
    return f"{secrets.randbelow(1_000_000):06d}"


@router.post("/email/request-otp")
@inject
async def request_email_otp(
    body: EmailOtpRequest,
    mailer: FromDishka[Mailer],
    redis: FromDishka[Redis],
) -> dict:
    """
    Send a one-time password to the provided email address.

    Rate-limited: a new code can only be requested once every
    ``OTP_RESEND_COOLDOWN`` seconds.
    """
    email = str(body.email).lower()
    otp_key = serialize_storage_key(EmailOtpKey(email=email))

    remaining_ttl = await redis.ttl(otp_key)
    if remaining_ttl > OTP_TTL - OTP_RESEND_COOLDOWN:
        wait = remaining_ttl - (OTP_TTL - OTP_RESEND_COOLDOWN)
        raise HTTPException(
            status_code=429,
            detail=f"Please wait {wait} seconds before requesting another code",
        )

    code = _generate_otp()
    await redis.setex(otp_key, OTP_TTL, code)

    try:
        await mailer.send_otp(email, code)
    except Exception:
        # Remove the stored code so the user can retry immediately
        await redis.delete(otp_key)
        raise HTTPException(status_code=502, detail="Failed to send verification email")

    return {"ok": True}


@router.post("/email/verify")
@inject
async def verify_email_otp(
    body: EmailOtpVerifyRequest,
    response: Response,
    user_dao: FromDishka[UserDao],
    config: FromDishka[AppConfig],
    cryptographer: FromDishka[Cryptographer],
    redis: FromDishka[Redis],
) -> AuthResponse:
    """
    Verify a one-time password and issue a session cookie.

    Creates the user account on first login if one does not yet exist.
    """
    email = str(body.email).lower()
    otp_key = serialize_storage_key(EmailOtpKey(email=email))

    stored_code: Optional[bytes] = await redis.get(otp_key)
    if stored_code is None:
        raise HTTPException(status_code=400, detail="No active verification code for this email")

    if stored_code.decode() != body.code.strip():
        raise HTTPException(status_code=400, detail="Invalid verification code")

    # Invalidate the OTP immediately after a successful check
    await redis.delete(otp_key)

    user = await user_dao.get_by_email(email)

    if user is None:
        referral_code = cryptographer.generate_short_code(email)
        user = await user_dao.create(
            UserDto(
                email=email,
                name=email,
                role=Role.USER,
                language=Locale(config.default_locale),
                referral_code=referral_code,
            )
        )

    if user.is_blocked:
        raise HTTPException(status_code=403, detail="User is blocked")

    _set_session_cookie(
        response,
        sub=user.id,  # ty: ignore[invalid-argument-type]
        typ=JwtTyp.USER_ID,
        secret=config.jwt_secret.get_secret_value(),
        expire_hours=config.jwt_expire_hours,
    )

    return AuthResponse(ok=True, user=UserResponse.model_validate(user, from_attributes=True))


# ------------------------------------------------------------------
# Common
# ------------------------------------------------------------------


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie(key="session")
    return {"ok": True}


@router.get("/me")
@inject
async def get_me(
    current_user: Annotated[UserDto, Depends(get_current_user)],
) -> UserResponse:
    return UserResponse.model_validate(current_user, from_attributes=True)
