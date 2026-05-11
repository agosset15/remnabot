from aiogram_dialog import Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo
from magic_filter import F

from src.core.enums import BannerName
from src.telegram.keyboards import back_main_menu_button
from src.telegram.states import Profile
from src.telegram.widgets import Banner, I18nFormat, IgnoreUpdate
from src.telegram.window import Window

from .getters import email_input_getter, otp_getter, profile_getter
from .handlers import on_email_input, on_otp_input, on_resend_otp

profile_main = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-profile-main", email=F["email"]),
    Row(
        SwitchTo(
            text=I18nFormat("btn-profile.email-set", email_set=F["email_set"]),
            id="email_set",
            state=Profile.EMAIL_INPUT,
        ),
    ),
    *back_main_menu_button,
    IgnoreUpdate(),
    state=Profile.MAIN,
    getter=profile_getter,
)

email_input = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-profile-email-input", email_set=F["email_set"]),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back.general"),
            id="back",
            state=Profile.MAIN,
        ),
    ),
    MessageInput(func=on_email_input),
    IgnoreUpdate(),
    state=Profile.EMAIL_INPUT,
    getter=email_input_getter,
)

email_otp = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-profile-email-otp"),
    Row(
        Button(
            text=I18nFormat("btn-profile.otp-resend"),
            id="otp_resend",
            on_click=on_resend_otp,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back.general"),
            id="back",
            state=Profile.MAIN,
        ),
    ),
    MessageInput(func=on_otp_input),
    IgnoreUpdate(),
    state=Profile.EMAIL_OTP,
    getter=otp_getter,
)

router = Dialog(
    profile_main,
    email_input,
    email_otp,
)
