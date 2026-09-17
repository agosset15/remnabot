import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from src.core.constants import EMAIL_VERIFICATION_CODE_LENGTH, PASSWORD_RESET_TOKEN_BYTES


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


def generate_password_reset_token() -> str:
    return secrets.token_urlsafe(PASSWORD_RESET_TOKEN_BYTES)


def hash_password_reset_token(token: str, key: str) -> str:
    payload = f"{token}:{key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def hash_reset_email(email: str, key: str) -> str:
    """Keyed digest of an email, used as the cooldown key so Redis stores no addresses."""
    payload = f"{email}:{key}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()
