from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.services import AccessService
from src.application.use_cases.settings import GetSettings


@inject
async def access_getter(
    dialog_manager: DialogManager,
    access_service: FromDishka[AccessService],
    get_settings: FromDishka[GetSettings],
    **kwargs: Any,
) -> dict[str, Any]:
    settings = await get_settings()
    modes = await access_service.get_available_access_modes()

    return {
        "purchases_allowed": settings.access.purchases_allowed,
        "registration_allowed": settings.access.registration_allowed,
        "access_mode": settings.access.mode,
        "modes": modes,
    }


@inject
async def conditions_getter(
    dialog_manager: DialogManager,
    get_settings: FromDishka[GetSettings],
    **kwargs: Any,
) -> dict[str, Any]:
    settings = await get_settings()

    return {
        "rules": settings.requirements.rules_required,
        "channel": settings.requirements.channel_required,
    }
