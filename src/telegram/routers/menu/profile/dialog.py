from aiogram_dialog import Dialog
from aiogram_dialog.widgets.input import MessageInput
from magic_filter import F

from src.core.enums import BannerName
from src.telegram.keyboards import back_main_menu_button
from src.telegram.states import Profile
from src.telegram.widgets import Banner, I18nFormat, IgnoreUpdate
from src.telegram.widgets.kbd import Button, Row, SwitchTo
from src.telegram.window import Window

from .getters import email_code_getter, profile_getter
from .handlers import on_code_input, on_code_resend, on_email_input

profile = Window(
    Banner(BannerName.MENU),
    I18nFormat(
        "msg-profile-main",
        email=F["email"],
        has_email=F["has_email"],
        is_email_verified=F["is_email_verified"],
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-profile.email-set", has_email=F["has_email"]),
            id="email_set",
            state=Profile.EMAIL_INPUT,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-profile.email-confirm"),
            id="email_confirm",
            state=Profile.EMAIL_CODE,
            when=(F["has_email"] | F["has_pending_email"]) & ~F["is_email_verified"],
        ),
    ),
    *back_main_menu_button,
    IgnoreUpdate(),
    state=Profile.MAIN,
    getter=profile_getter,
)

email_input = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-profile-email-input", has_email=F["has_email"]),
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
    getter=profile_getter,
)

email_code = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-profile-email-code", email=F["pending_email"]),
    Row(
        Button(
            text=I18nFormat("btn-profile.code-resend"),
            id="code_resend",
            on_click=on_code_resend,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back.general"),
            id="back",
            state=Profile.MAIN,
        ),
    ),
    MessageInput(func=on_code_input),
    IgnoreUpdate(),
    state=Profile.EMAIL_CODE,
    getter=email_code_getter,
)

router = Dialog(
    profile,
    email_input,
    email_code,
)
