from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from fastapi import HTTPException, status
from loguru import logger

from src.application.common import Notifier
from src.application.dto import TelegramUserDto
from src.application.use_cases.auth.commands.email import (
    ChangeEmail,
    ChangeEmailDto,
    ConfirmEmailVerification,
    ConfirmEmailVerificationDto,
    RequestEmailVerification,
    RequestEmailVerificationDto,
)
from src.core.constants import USER_KEY
from src.core.exceptions import EmailDeliveryDisabledError
from src.core.utils.validators import is_valid_email
from src.telegram.states import Profile


async def _notify_request_error(
    notifier: Notifier, user: TelegramUserDto, error: HTTPException
) -> None:
    if error.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-cooldown")
    elif error.status_code == status.HTTP_409_CONFLICT:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-duplicate")
    else:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-invalid")


async def _request_code(
    notifier: Notifier,
    user: TelegramUserDto,
    request_verification: RequestEmailVerification,
) -> bool:
    try:
        await request_verification(user, RequestEmailVerificationDto())
    except EmailDeliveryDisabledError:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-disabled")
        return False
    except HTTPException as e:
        await _notify_request_error(notifier, user, e)
        return False
    except Exception as e:
        logger.error(f"{user.log} Failed to send email verification code: {e}")
        await notifier.notify_user(user, i18n_key="ntf-profile.email-send-failed")
        return False

    await notifier.notify_user(user, i18n_key="ntf-profile.email-code-sent")
    return True


@inject
async def on_email_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    notifier: FromDishka[Notifier],
    change_email: FromDishka[ChangeEmail],
    request_verification: FromDishka[RequestEmailVerification],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: TelegramUserDto = dialog_manager.middleware_data[USER_KEY]
    email = (message.text or "").strip().lower()

    if not is_valid_email(email):
        await notifier.notify_user(user, i18n_key="ntf-profile.email-invalid")
        return

    if email == (user.email or "").lower() and user.is_email_verified:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-same")
        return

    try:
        await change_email(user, ChangeEmailDto(email=email))
    except HTTPException as e:
        await _notify_request_error(notifier, user, e)
        return

    if not await _request_code(notifier, user, request_verification):
        return

    dialog_manager.dialog_data["pending_email"] = email
    await dialog_manager.switch_to(state=Profile.EMAIL_CODE)


@inject
async def on_code_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    notifier: FromDishka[Notifier],
    confirm_verification: FromDishka[ConfirmEmailVerification],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: TelegramUserDto = dialog_manager.middleware_data[USER_KEY]
    code = (message.text or "").strip()

    try:
        await confirm_verification(user, ConfirmEmailVerificationDto(code=code))
    except HTTPException as e:
        if e.status_code == status.HTTP_410_GONE:
            await notifier.notify_user(user, i18n_key="ntf-profile.email-code-expired")
        elif e.status_code == status.HTTP_409_CONFLICT:
            await notifier.notify_user(user, i18n_key="ntf-profile.email-duplicate")
        else:
            await notifier.notify_user(user, i18n_key="ntf-profile.email-code-invalid")
        return

    dialog_manager.dialog_data.pop("pending_email", None)
    await notifier.notify_user(user, i18n_key="ntf-profile.email-confirmed")
    await dialog_manager.switch_to(state=Profile.MAIN)


@inject
async def on_code_resend(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    notifier: FromDishka[Notifier],
    request_verification: FromDishka[RequestEmailVerification],
) -> None:
    user: TelegramUserDto = dialog_manager.middleware_data[USER_KEY]

    if not (user.pending_email or user.email):
        await dialog_manager.switch_to(state=Profile.EMAIL_INPUT)
        return

    await _request_code(notifier, user, request_verification)
