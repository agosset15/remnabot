from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from magic_filter import F

from src.core.enums import BannerName
from src.telegram.keyboards import back_main_menu_button
from src.telegram.routers.extra.test import show_dev_popup
from src.telegram.states import (
    Dashboard,
    DashboardAccess,
    DashboardBroadcast,
    DashboardImporter,
    DashboardRemnashop,
    DashboardRemnawave,
    DashboardStatistics,
    DashboardUsers,
)
from src.telegram.widgets import Banner, I18nFormat, IgnoreUpdate

from .getters import dashboard_getter

dashboard = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-dashboard-main"),
    Row(
        Start(
            text=I18nFormat("btn-dashboard.statistics"),
            id="statistics",
            state=DashboardStatistics.MAIN,
        ),
        Start(
            text=I18nFormat("btn-dashboard.users"),
            id="users",
            state=DashboardUsers.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard.broadcast"),
            id="broadcast",
            state=DashboardBroadcast.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Button(
            text=I18nFormat("btn-dashboard.promocodes"),
            id="promocodes",
            on_click=show_dev_popup,
            # state=DashboardPromocodes.MAIN,
            # mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard.access"),
            id="access",
            state=DashboardAccess.MAIN,
            mode=StartMode.RESET_STACK,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard.remnawave"),
            id="remnawave",
            state=DashboardRemnawave.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        Start(
            text=I18nFormat("btn-dashboard.remnashop"),
            id="remnashop",
            state=DashboardRemnashop.MAIN,
            mode=StartMode.RESET_STACK,
        ),
        when=F["remnashop_accessible"],
    ),
    Row(
        Start(
            text=I18nFormat("btn-dashboard.importer"),
            id="importer",
            state=DashboardImporter.MAIN,
        ),
        when=F["importer_accessible"],
    ),
    *back_main_menu_button,
    IgnoreUpdate(),
    state=Dashboard.MAIN,
    getter=dashboard_getter,
)

router = Dialog(dashboard)
