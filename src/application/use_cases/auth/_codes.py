import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode

import jwt
from fastapi import HTTPException, status

from src.core.config import AppConfig
from src.core.constants import (
    EMAIL_VERIFICATION_CODE_LENGTH,
    MAGIC_LINK_PATH,
    MAGIC_LINK_PURPOSE,
)


def generate_email_verification_code() -> str:
    lower = 10 ** (EMAIL_VERIFICATION_CODE_LENGTH - 1)
    upper = (10**EMAIL_VERIFICATION_CODE_LENGTH) - 1
    return str(secrets.randbelow(upper - lower + 1) + lower)


def hash_email_verification_code(code: str, key: str) -> str:
    payload = f"{code}:{key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def check_email_resend_cooldown(
    expires_at: "datetime | None",
    ttl_minutes: int,
    cooldown_seconds: int,
    now: "datetime",
) -> None:
    if expires_at is None:
        return
    last_issued_at = expires_at - timedelta(minutes=ttl_minutes)
    if now < last_issued_at + timedelta(seconds=cooldown_seconds):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Please wait before requesting another code",
        )


def encode_magic_token(email: str, code: str, key: str, expires_at: "datetime") -> str:
    """Pack an email code into a signed single-use token for magic links.

    The code itself travels inside the token, so following the link is handled by
    the very same verification path as typing the code by hand.
    """
    return jwt.encode(
        {
            "sub": email,
            "code": code,
            "purpose": MAGIC_LINK_PURPOSE,
            "exp": expires_at,
        },
        key,
        algorithm="HS256",
    )


def decode_magic_token(token: str, key: str) -> tuple[str, str]:
    try:
        payload = jwt.decode(token, key, algorithms=["HS256"], options={"verify_sub": False})
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="Magic link has expired"
        ) from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid magic link"
        ) from e

    email = payload.get("sub")
    code = payload.get("code")
    if payload.get("purpose") != MAGIC_LINK_PURPOSE or not email or not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid magic link")
    return str(email), str(code)


def magic_link_base_url(config: AppConfig) -> Optional[str]:
    """Front-end origin the magic link should land on."""
    if config.web.cabinet_url:
        return config.web.cabinet_url.strip().rstrip("/")
    if config.web.base_url:
        return config.web.base_url
    domain = config.domain.get_secret_value()
    return f"https://{domain}" if domain else None


def build_magic_link(
    config: AppConfig, email: str, code: str, expires_at: "datetime"
) -> Optional[str]:
    """Build the one-click login/verification URL, or None when not configurable."""
    if config.jwt_secret is None:
        return None

    base_url = magic_link_base_url(config)
    if not base_url:
        return None

    token = encode_magic_token(email, code, config.jwt_secret.get_secret_value(), expires_at)
    return f"{base_url}{MAGIC_LINK_PATH}?{urlencode({'token': token})}"
