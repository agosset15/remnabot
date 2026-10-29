from typing import Any

from aiogram_dialog import DialogManager

from src.application.dto import TelegramUserDto


async def profile_getter(
    dialog_manager: DialogManager,
    user: TelegramUserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        "email": user.email or False,
        "has_email": bool(user.email),
        "is_email_verified": user.is_email_verified,
        "pending_email": user.pending_email or False,
        "has_pending_email": bool(user.pending_email),
    }


async def email_code_getter(
    dialog_manager: DialogManager,
    user: TelegramUserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    pending_email = (
        user.pending_email or dialog_manager.dialog_data.get("pending_email") or user.email or ""
    )
    return {
        "pending_email": pending_email,
    }
