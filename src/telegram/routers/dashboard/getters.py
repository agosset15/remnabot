from typing import Any

from aiogram_dialog import DialogManager

from src.application.dto import UserDto
from src.core.exceptions import PermissionDenied


async def dashboard_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    **kwargs: Any,
) -> dict[str, Any]:
    if not user.is_privileged:
        raise PermissionDenied

    return {
        "remnashop_accessible": user.is_dev,
        "importer_accessible": user.is_root,
    }
