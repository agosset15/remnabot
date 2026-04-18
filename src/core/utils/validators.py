from typing import Optional

from src.core.constants import EMAIL_PATTERN, URL_PATTERN, USERNAME_PATTERN


def is_valid_url(text: str) -> bool:
    return bool(URL_PATTERN.match(text))


def is_valid_username(text: str) -> bool:
    return bool(USERNAME_PATTERN.match(text))


def is_valid_email(text: str) -> bool:
    if len(text) > 255:
        return False
    return bool(EMAIL_PATTERN.match(text))


def is_valid_int(value: Optional[str]) -> bool:
    if value is None:
        return False
    try:
        int(value)
        return True
    except (TypeError, ValueError):
        return False


def parse_int(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None
