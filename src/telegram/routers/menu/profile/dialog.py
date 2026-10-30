from aiogram_dialog.widgets.input import MessageInput
from magic_filter import F

from src.core.enums import BannerName
from src.telegram.states import MainMenu, Profile
from src.telegram.widgets import Banner, I18nFormat, IgnoreUpdate
from src.telegram.widgets.kbd import Button, Row, SwitchTo
from src.telegram.window import Window

from .getters import email_code_getter, profile_getter
from .handlers import on_code_input, on_code_resend, on_email_input

email_input = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-profile-email-input", has_email=F["has_email"]),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back.general"),
            id="back",
            state=MainMenu.MAIN,
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
            state=MainMenu.MAIN,
        ),
    ),
    MessageInput(func=on_code_input),
    IgnoreUpdate(),
    state=Profile.EMAIL_CODE,
    getter=email_code_getter,
)

