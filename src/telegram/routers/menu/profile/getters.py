from typing import Any

from aiogram_dialog import DialogManager
from dishka.integrations.aiogram_dialog import inject

from src.application.dto import UserDto


@inject
async def profile_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        "email": user.email or False,
        "email_set": bool(user.email),
    }


@inject
async def email_input_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        "email_set": bool(user.email),
    }


@inject
async def otp_getter(
    dialog_manager: DialogManager,
    **kwargs: Any,
) -> dict[str, Any]:
    pending_email = dialog_manager.dialog_data.get("pending_email", "")
    return {
        "pending_email": pending_email,
    }
