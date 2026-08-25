import hashlib
import hmac
import time
from typing import Any
from urllib.parse import parse_qsl

import jwt
from jwt import PyJWKSet

from src.core.constants import TELEGRAM_AUTH_MAX_AGE_SECONDS, TELEGRAM_OIDC_ISSUER


def decode_telegram_id_token(id_token: str, jwks: dict[str, Any], bot_id: int) -> dict[str, Any]:
    """Verify and decode a Telegram Login OIDC ``id_token``.

    Validates the RS256 signature against ``jwks`` and checks the ``iss``/``aud``/
    ``exp`` claims. Raises ``ValueError`` on any failure.

    See https://core.telegram.org/bots/telegram-login
    """
    try:
        header = jwt.get_unverified_header(id_token)
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Malformed id_token: {e}") from e

    kid = header.get("kid")
    signing_key = None
    for key in PyJWKSet.from_dict(jwks).keys:
        if kid is None or key.key_id == kid:
            signing_key = key
            break
    if signing_key is None:
        raise ValueError("No matching signing key for id_token")

    try:
        return jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            audience=str(bot_id),
            issuer=TELEGRAM_OIDC_ISSUER,
            options={"require": ["exp", "iss", "aud"], "verify_sub": False},
        )
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid id_token: {e}") from e


def parse_webapp_init_data(init_data: str) -> dict[str, str]:
    return dict(parse_qsl(init_data, keep_blank_values=True))


def verify_telegram_webapp_init_data(init_data: str, bot_token: str) -> bool:
    fields = parse_webapp_init_data(init_data)
    telegram_hash = fields.pop("hash", "")
    if not telegram_hash:
        return False

    auth_date = int(fields.get("auth_date", 0))
    if int(time.time()) - auth_date > TELEGRAM_AUTH_MAX_AGE_SECONDS:
        return False

    data_check_string = "\n".join(f"{k}={fields[k]}" for k in sorted(fields))
    secret_key = hmac.new(b"WebAppData", bot_token.encode("utf-8"), hashlib.sha256).digest()
    expected = hmac.new(
        secret_key,
        data_check_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, telegram_hash)
