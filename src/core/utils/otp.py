import secrets

OTP_TTL = 600
OTP_RESEND_COOLDOWN = 60


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"
