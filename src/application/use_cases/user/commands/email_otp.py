from dataclasses import dataclass

from loguru import logger
from redis.asyncio import Redis

from src.application.common import Interactor
from src.application.common.mailer import Mailer
from src.application.common.policy import Permission
from src.application.dto import UserDto
from src.core.exceptions import (
    OtpCooldownError,
    OtpExpiredError,
    OtpInvalidError,
    OtpSendError,
)
from src.core.utils.otp import OTP_RESEND_COOLDOWN, OTP_TTL, generate_otp
from src.core.utils.validators import is_valid_email
from src.infrastructure.redis.key_builder import serialize_storage_key
from src.infrastructure.redis.keys import EmailOtpKey


@dataclass(frozen=True)
class RequestEmailOtpDto:
    email: str


class RequestEmailOtp(Interactor[RequestEmailOtpDto, None]):
    """Generate a 6-digit code, store it in Redis with TTL, and send via mailer."""

    required_permission = Permission.PUBLIC

    def __init__(self, redis: Redis, mailer: Mailer) -> None:
        self.redis = redis
        self.mailer = mailer

    async def _execute(self, actor: UserDto, data: RequestEmailOtpDto) -> None:
        email = data.email.strip().lower()
        if not is_valid_email(email):
            raise ValueError(f"Invalid email '{data.email}'")

        otp_key = serialize_storage_key(EmailOtpKey(email=email))
        ttl = await self.redis.ttl(otp_key)
        if ttl > OTP_TTL - OTP_RESEND_COOLDOWN:
            raise OtpCooldownError(seconds=ttl - (OTP_TTL - OTP_RESEND_COOLDOWN))

        code = generate_otp()
        await self.redis.setex(otp_key, OTP_TTL, code)

        try:
            await self.mailer.send_otp(email, code)
        except Exception as exc:
            await self.redis.delete(otp_key)
            logger.error(f"Failed to send OTP to '{email}': {exc}")
            raise OtpSendError() from exc

        logger.info(f"OTP requested for '{email}'")


@dataclass(frozen=True)
class VerifyEmailOtpDto:
    email: str
    code: str


class VerifyEmailOtp(Interactor[VerifyEmailOtpDto, None]):
    """Verify a 6-digit code against the value stored in Redis. Deletes it on success."""

    required_permission = Permission.PUBLIC

    def __init__(self, redis: Redis) -> None:
        self.redis = redis

    async def _execute(self, actor: UserDto, data: VerifyEmailOtpDto) -> None:
        email = data.email.strip().lower()
        otp_key = serialize_storage_key(EmailOtpKey(email=email))

        stored = await self.redis.get(otp_key)
        if stored is None:
            raise OtpExpiredError()

        stored_str = stored.decode() if isinstance(stored, bytes) else stored
        if stored_str != data.code.strip():
            raise OtpInvalidError()

        await self.redis.delete(otp_key)
        logger.info(f"OTP verified for '{email}'")
