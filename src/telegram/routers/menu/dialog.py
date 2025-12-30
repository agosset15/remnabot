from aiogram_dialog import Dialog
from aiogram_dialog.widgets.kbd import Button, Row

from src.core.enums import BannerName, MessageEffectId
from src.telegram.states import MainMenu
from src.telegram.widgets import Banner, Effect, I18nFormat, IgnoreUpdate
from src.telegram.window import Window

from .getters import menu_getter

menu = Window(
    Banner(BannerName.MENU),
    Effect(MessageEffectId.PARTY),
    I18nFormat("msg-test"),
    Row(
        Button(
            text=I18nFormat("btn-test"),
            id="trial",
        ),
    ),
    IgnoreUpdate(),
    state=MainMenu.MAIN,
    getter=menu_getter,
)

router = Dialog(menu)
