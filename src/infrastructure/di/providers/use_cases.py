from dishka import Provider, Scope, provide

from src.application.use_cases.menu import GetMenuData
from src.application.use_cases.settings import (
    ChangeAccessMode,
    GetSettings,
    ToggleConditionRequirement,
    ToggleNotification,
    TogglePurchases,
    ToggleRegistration,
    UpdateChannelRequirement,
    UpdateRulesRequirement,
)
from src.application.use_cases.user import GetOrCreateUser, SetBotBlockedStatus


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_menu_data = provide(GetMenuData)

    get_or_create_user = provide(GetOrCreateUser)
    set_bot_blocked_status = provide(SetBotBlockedStatus)

    get_settings = provide(GetSettings)
    toggle_notification = provide(ToggleNotification)
    change_accessmode = provide(ChangeAccessMode)
    toggle_purchases = provide(TogglePurchases)
    toggle_registration = provide(ToggleRegistration)
    toggle_condition_requirement = provide(ToggleConditionRequirement)
    update_rules_requirement = provide(UpdateRulesRequirement)
    update_channel_requirement = provide(UpdateChannelRequirement)
