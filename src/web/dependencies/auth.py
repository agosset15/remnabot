from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Cookie, HTTPException
from jose import jwt

from src.application.common.dao import UserDao
from src.application.dto import UserDto
from src.core.config import AppConfig


@inject
async def get_current_user(
    user_dao: FromDishka[UserDao],
    config: FromDishka[AppConfig],
    session: str | None = Cookie(default=None),
) -> UserDto:
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(session, config.jwt_secret.get_secret_value(), algorithms=["HS256"])
        telegram_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid session")

    user = await user_dao.get_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if user.is_blocked:
        raise HTTPException(status_code=403, detail="User is blocked")
    return user
