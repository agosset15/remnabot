from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.application.common import Notifier
from src.application.common.dao import UserDao
from src.application.dto import MessagePayloadDto, UserDto
from src.application.use_cases.user.commands.email_otp import (
    RequestEmailOtp,
    RequestEmailOtpDto,
    VerifyEmailOtp,
    VerifyEmailOtpDto,
)
from src.application.use_cases.user.commands.profile_edit import (
    SetUserEmail,
    SetUserEmailDto,
)
from src.core.constants import USER_KEY
from src.core.exceptions import (
    OtpCooldownError,
    OtpExpiredError,
    OtpInvalidError,
    OtpSendError,
)
from src.core.utils.validators import is_valid_email
from src.telegram.states import Profile


@inject
async def on_email_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    notifier: FromDishka[Notifier],
    user_dao: FromDishka[UserDao],
    request_otp: FromDishka[RequestEmailOtp],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    raw = (message.text or "").strip().lower()

    if not is_valid_email(raw):
        await notifier.notify_user(user, i18n_key="ntf-profile.email-invalid")
        return

    if raw == (user.email or "").lower():
        await notifier.notify_user(user, i18n_key="ntf-profile.email-same")
        return

    existing = await user_dao.get_by_email(raw)
    if existing and existing.id != user.id:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-duplicate")
        return

    try:
        await request_otp.system(RequestEmailOtpDto(email=raw))
    except OtpCooldownError as exc:
        await notifier.notify_user(
            user,
            payload=MessagePayloadDto(
                i18n_key="ntf-profile.email-otp-cooldown",
                i18n_kwargs={"seconds": exc.seconds},
            ),
        )
        return
    except OtpSendError:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-send-failed")
        return
    except ValueError:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-invalid")
        return

    dialog_manager.dialog_data["pending_email"] = raw
    await notifier.notify_user(user, i18n_key="ntf-profile.email-otp-sent")
    await dialog_manager.switch_to(state=Profile.EMAIL_OTP)


@inject
async def on_otp_input(
    message: Message,
    widget: MessageInput,
    dialog_manager: DialogManager,
    notifier: FromDishka[Notifier],
    verify_otp: FromDishka[VerifyEmailOtp],
    set_user_email: FromDishka[SetUserEmail],
) -> None:
    dialog_manager.show_mode = ShowMode.EDIT
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    pending = dialog_manager.dialog_data.get("pending_email")

    if not pending:
        await dialog_manager.switch_to(state=Profile.MAIN)
        return

    code = (message.text or "").strip()

    try:
        await verify_otp.system(VerifyEmailOtpDto(email=pending, code=code))
    except OtpExpiredError:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-otp-expired")
        return
    except OtpInvalidError:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-otp-invalid")
        return

    try:
        await set_user_email.system(SetUserEmailDto(user_id=user.id, email=pending))
    except ValueError as exc:
        logger.warning(f"{user.log} Failed to set email '{pending}': {exc}")
        if "already used" in str(exc):
            await notifier.notify_user(user, i18n_key="ntf-profile.email-duplicate")
            return
        await notifier.notify_user(user, i18n_key="ntf-profile.email-invalid")
        return

    dialog_manager.dialog_data.pop("pending_email", None)
    await notifier.notify_user(user, i18n_key="ntf-profile.email-changed")
    await dialog_manager.switch_to(state=Profile.MAIN)


@inject
async def on_resend_otp(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    notifier: FromDishka[Notifier],
    request_otp: FromDishka[RequestEmailOtp],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    pending = dialog_manager.dialog_data.get("pending_email")

    if not pending:
        await dialog_manager.switch_to(state=Profile.EMAIL_INPUT)
        return

    try:
        await request_otp.system(RequestEmailOtpDto(email=pending))
    except OtpCooldownError as exc:
        await notifier.notify_user(
            user,
            payload=MessagePayloadDto(
                i18n_key="ntf-profile.email-otp-cooldown",
                i18n_kwargs={"seconds": exc.seconds},
            ),
        )
        return
    except OtpSendError:
        await notifier.notify_user(user, i18n_key="ntf-profile.email-send-failed")
        return

    await notifier.notify_user(user, i18n_key="ntf-profile.email-otp-sent")
