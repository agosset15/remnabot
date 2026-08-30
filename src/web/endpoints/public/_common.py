import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Annotated, Optional
from urllib.parse import urlparse

import jwt
from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, HTTPException, Request, Response, status

from src.application.common.dao import UserDao
from src.application.common.dao.auth import AuthSessionDao
from src.application.dto import UserDto
from src.core.config import AppConfig
from src.core.constants import ACCESS_TOKEN_TTL_SECONDS, REFRESH_TOKEN_TTL_SECONDS
from src.web.schemas import AuthResponse


def _normalize_decimal_str(value: Decimal) -> str:
    if value == value.to_integral():
        return str(int(value))
    normalized = value.quantize(Decimal("0.01")).normalize()
    return format(normalized, "f")


def _allowed_return_hosts(config: AppConfig) -> set[str]:
    hosts: set[str] = {config.domain.get_secret_value().lower()}

    if config.web.domain:
        hosts.add(config.web.domain.get_secret_value().lower())

    if config.web.cabinet_url:
        cabinet_host = urlparse(config.web.cabinet_url.strip()).hostname
        if cabinet_host:
            hosts.add(cabinet_host.lower())

    for origin in config.origins:
        origin_host = urlparse(origin.strip()).hostname
        if origin_host:
            hosts.add(origin_host.lower())

    return hosts


def resolve_return_url(return_url: Optional[str], config: AppConfig) -> Optional[str]:
    """Validate a client-supplied post-checkout redirect URL.

    Only https URLs pointing at a host we own are accepted; anything else is
    rejected so the gateway cannot be used as an open redirect.
    """
    if not return_url:
        return None

    parsed = urlparse(return_url.strip())

    if parsed.scheme != "https" or not parsed.hostname:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="return_url must be an absolute https URL",
        )

    if parsed.hostname.lower() not in _allowed_return_hosts(config):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="return_url host is not allowed",
        )

    return parsed.geturl()


def generate_access_token(user_id: int, key: str) -> tuple[str, datetime]:
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(seconds=ACCESS_TOKEN_TTL_SECONDS)
    token = jwt.encode({"sub": user_id, "iat": now, "exp": exp}, key, algorithm="HS256")
    return token, exp


def decode_access_token(token: str, key: str) -> int:
    payload = jwt.decode(token, key, algorithms=["HS256"], options={"verify_sub": False})
    try:
        return int(payload["sub"])
    except (KeyError, TypeError, ValueError) as e:
        raise jwt.InvalidTokenError("Invalid 'sub' claim") from e


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=ACCESS_TOKEN_TTL_SECONDS,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=REFRESH_TOKEN_TTL_SECONDS,
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie("access_token", httponly=True, secure=True, samesite="lax")
    response.delete_cookie("refresh_token", httponly=True, secure=True, samesite="lax")


async def issue_session(
    user: UserDto,
    config: AppConfig,
    auth_session: AuthSessionDao,
) -> tuple[str, str, AuthResponse]:
    if config.jwt_secret is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT secret not configured",
        )
    access_token, expires_at = generate_access_token(user.id, config.jwt_secret.get_secret_value())
    refresh_token = secrets.token_urlsafe(32)
    refresh_expires_at = datetime.now(tz=timezone.utc) + timedelta(
        seconds=REFRESH_TOKEN_TTL_SECONDS
    )
    await auth_session.store_refresh_token(
        token=refresh_token,
        user_id=user.id,
        ttl=REFRESH_TOKEN_TTL_SECONDS,
    )
    return (
        access_token,
        refresh_token,
        AuthResponse(
            expires_at=expires_at,
            refresh_expires_at=refresh_expires_at,
        ),
    )


# NOTE: The `FromDishka[...] = None` defaults are a required workaround for the
# dishka-fastapi integration: FastAPI inspects the signature and needs a default for
# non-path/query params, while dishka overwrites the value at call time. The `None`
# is never observed at runtime; the `type: ignore[assignment]` silences the mismatch.
@inject
async def _get_current_user(
    request: Request,
    user_dao: FromDishka[UserDao] = None,  # type: ignore[assignment]
    config: FromDishka[AppConfig] = None,  # type: ignore[assignment]
) -> UserDto:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        if config.jwt_secret is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT secret not configured",
            )
        user_id = decode_access_token(token, config.jwt_secret.get_secret_value())
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    user = await user_dao.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.is_blocked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
    return user


CurrentUser = Annotated[UserDto, Depends(_get_current_user)]
