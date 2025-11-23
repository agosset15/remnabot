from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fluentogram import TranslatorRunner
from loguru import logger

from src.core.config import AppConfig
from src.core.utils.formatters import (
    format_username_to_url,
    i18n_format_device_limit,
    i18n_format_expire_time,
    i18n_format_traffic_limit,
)
from src.core.enums import TransactionStatus
from src.infrastructure.database.models.dto import UserDto
from src.services.plan import PlanService
from src.services.remnawave import RemnawaveService
from src.services.subscription import SubscriptionService
from src.services.transaction import TransactionService
from src.services.user import UserService


@inject
async def menu_getter(
    dialog_manager: DialogManager,
    config: AppConfig,
    user: UserDto,
    i18n: FromDishka[TranslatorRunner],
    plan_service: FromDishka[PlanService],
    subscription_service: FromDishka[SubscriptionService],
    **kwargs: Any,
) -> dict[str, Any]:
    plan = await plan_service.get_trial_plan()
    has_used_trial = await subscription_service.has_used_trial(user)
    support_username = config.bot.support_username.get_secret_value()
    support_link = format_username_to_url(support_username, i18n.get("contact-support-help"))

    base_data = {
        "user_id": str(user.telegram_id),
        "user_name": user.name,
        "personal_discount": user.personal_discount,
        "support": support_link,
        "has_subscription": user.has_subscription,
        "miniapp_url": config.bot.mini_app_url.get_secret_value(),
    }

    subscription = user.current_subscription

    if not subscription:
        base_data.update(
            {
                "status": None,
                "is_trial": False,
                "trial_available": not has_used_trial and plan,
                "has_device_limit": False,
                "connetable": False,
            }
        )
        return base_data

    base_data.update(
        {
            "status": subscription.status,
            "type": subscription.get_subscription_type,
            "traffic_limit": i18n_format_traffic_limit(subscription.traffic_limit),
            "device_limit": i18n_format_device_limit(subscription.device_limit),
            "expire_time": i18n_format_expire_time(subscription.expire_at),
            "is_trial": subscription.is_trial,
            "has_device_limit": subscription.has_devices_limit if subscription.is_active else False,
            "connetable": subscription.is_active,
            "subscription_url": subscription.url,
        }
    )

    return base_data


@inject
async def devices_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    remnawave_service: FromDishka[RemnawaveService],
    **kwargs: Any,
) -> dict[str, Any]:
    if not user.current_subscription:
        raise ValueError(f"Current subscription for user '{user.telegram_id}' not found")

    devices = await remnawave_service.get_devices_user(user)

    formatted_devices = [
        {
            "hwid": device.hwid,
            "platform": device.platform,
            "device_model": device.device_model,
            "user_agent": device.user_agent,
        }
        for device in devices
    ]

    return {
        "current_count": len(devices),
        "max_count": i18n_format_device_limit(user.current_subscription.device_limit),
        "devices": formatted_devices,
        "devices_empty": len(devices) == 0,
    }


@inject
async def invite_getter(
    dialog_manager: DialogManager,
    user: UserDto,
    transaction_service: FromDishka[TransactionService],
    user_service: FromDishka[UserService],
    **kwargs: Any,
) -> dict[str, Any]:
    logger.debug(f"Now user {user.id} has {len(user.referrals)} referrals")
    user = await user_service.get_referrals(user.telegram_id)
    logger.debug(f"And now user {user.id} has {len(user.referrals)} referrals")
    payments = len(await transaction_service.get_by_referrer_and_status(user.referrals, TransactionStatus.COMPLETED))
    bot_username = (await dialog_manager.event.bot.get_me()).username

    return {
        "referral_count": len(user.referrals),
        "referral_payments": payments,
        "referral_earned": user.purchase_discount if user.purchase_discount > user.personal_discount else user.personal_discount,
        "referral_link": f"https://t.me/{bot_username}?start=ref-{user.telegram_id}",
    }

@inject
async def invited_users_getter(
        dialog_manager: DialogManager,
        user: UserDto,
        user_service: FromDishka[UserService],
        **kwargs: Any
) -> dict[str, Any]:
    user = await user_service.get_referrals(user.telegram_id)
    return {
        "invited_users": "• " + '\n• '.join([ref.name for ref in user.referrals]),
        "invited_user_count": len(user.referrals),
    }
