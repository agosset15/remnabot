from dataclasses import dataclass

from loguru import logger
from pydantic import SecretStr

from src.application.common import Interactor, Notifier
from src.application.common.dao import SettingsDao
from src.application.common.uow import UnitOfWork
from src.application.dto import SettingsDto, UserDto
from src.core.constants import T_ME
from src.core.enums import AccessMode, AccessRequirements
from src.core.types import NotificationType
from src.core.utils.validators import is_valid_url, is_valid_username


@dataclass(frozen=True)
class ToggleNotificationDto:
    user: UserDto
    notification_type: NotificationType


@dataclass(frozen=True)
class UpdateChannelRequirementDto:
    user: UserDto
    input_text: str


@dataclass(frozen=True)
class UpdateRulesRequirementDto:
    user: UserDto
    input_text: str


@dataclass(frozen=True)
class ToggleConditionRequirementDto:
    user: UserDto
    condition_type: AccessRequirements


@dataclass(frozen=True)
class ChangeAccessModeDto:
    user: UserDto
    mode: AccessMode


class GetSettings(Interactor[None, SettingsDto]):
    def __init__(self, dao: SettingsDao, uow: UnitOfWork) -> None:
        self.dao = dao
        self.uow = uow

    async def __call__(self, data: None = None) -> SettingsDto:
        async with self.uow:
            return await self.dao.get()


class ToggleNotification(Interactor[ToggleNotificationDto, SettingsDto]):
    def __init__(self, dao: SettingsDao, uow: UnitOfWork) -> None:
        self.dao = dao
        self.uow = uow

    async def __call__(self, data: ToggleNotificationDto) -> SettingsDto:
        async with self.uow:
            settings = await self.dao.get()
            settings.notifications.toggle(data.notification_type)
            updated = await self.dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.user.log} Toggled notification '{data.notification_type}'")
        return updated


class ChangeAccessMode(Interactor[ChangeAccessModeDto, None]):
    def __init__(self, settings_dao: SettingsDao, uow: UnitOfWork) -> None:
        self.settings_dao = settings_dao
        self.uow = uow

    async def __call__(self, data: ChangeAccessModeDto) -> None:
        async with self.uow:
            settings = await self.settings_dao.get()
            settings.access.mode = data.mode
            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.user.log} Toggled purchases allowed to '{data.mode}'")


class TogglePurchases(Interactor[UserDto, None]):
    def __init__(self, settings_dao: SettingsDao, uow: UnitOfWork) -> None:
        self.settings_dao = settings_dao
        self.uow = uow

    async def __call__(self, data: UserDto) -> None:
        settings = await self.settings_dao.get()
        new_state = not settings.access.purchases_allowed
        settings.access.purchases_allowed = new_state

        async with self.uow:
            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.log} toggled purchases allowed to '{new_state}'")


class ToggleRegistration(Interactor[UserDto, None]):
    def __init__(self, settings_dao: SettingsDao, uow: UnitOfWork) -> None:
        self.settings_dao = settings_dao
        self.uow = uow

    async def __call__(self, data: UserDto) -> None:
        settings = await self.settings_dao.get()
        new_state = not settings.access.registration_allowed
        settings.access.registration_allowed = new_state

        async with self.uow:
            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.log} Toggled registration allowed to '{new_state}'")


class ToggleConditionRequirement(Interactor[ToggleConditionRequirementDto, None]):
    def __init__(self, settings_dao: SettingsDao, uow: UnitOfWork) -> None:
        self.settings_dao = settings_dao
        self.uow = uow

    async def __call__(self, data: ToggleConditionRequirementDto) -> None:
        settings = await self.settings_dao.get()

        if data.condition_type == AccessRequirements.RULES:
            settings.requirements.rules_required = not settings.requirements.rules_required
            new_state = settings.requirements.rules_required
        elif data.condition_type == AccessRequirements.CHANNEL:
            settings.requirements.channel_required = not settings.requirements.channel_required
            new_state = settings.requirements.channel_required
        else:
            logger.error(
                f"{data.user.log} Tried to toggle unknown condition '{data.condition_type}'"
            )
            return

        async with self.uow:
            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.user.log} Toggled '{data.condition_type}' to '{new_state}'")


class UpdateRulesRequirement(Interactor[UpdateRulesRequirementDto, bool]):
    def __init__(self, settings_dao: SettingsDao, uow: UnitOfWork, notifier: Notifier) -> None:
        self.settings_dao = settings_dao
        self.uow = uow
        self.notifier = notifier

    async def __call__(self, data: UpdateRulesRequirementDto) -> bool:
        input_text = data.input_text.strip()

        if not is_valid_url(input_text):
            logger.warning(f"{data.user.log} Provided invalid rules link format: '{input_text}'")
            await self.notifier.notify_user(data.user, i18n_key="ntf-access-invalid-link")
            return False

        settings = await self.settings_dao.get()
        settings.requirements.rules_link = SecretStr(input_text)

        async with self.uow:
            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.user.log} Successfully updated rules link to '{input_text}'")
        await self.notifier.notify_user(data.user, i18n_key="ntf-access-link-saved")
        return True


class UpdateChannelRequirement(Interactor[UpdateChannelRequirementDto, None]):
    def __init__(self, settings_dao: SettingsDao, uow: UnitOfWork, notifier: Notifier) -> None:
        self.settings_dao = settings_dao
        self.uow = uow
        self.notifier = notifier

    async def __call__(self, data: UpdateChannelRequirementDto) -> None:
        input_text = data.input_text.strip()
        settings = await self.settings_dao.get()

        if input_text.isdigit() or (input_text.startswith("-") and input_text[1:].isdigit()):
            await self._handle_id_input(input_text, settings)
            await self.notifier.notify_user(data.user, i18n_key="ntf-access-id-saved")
        elif is_valid_username(input_text) or input_text.startswith(T_ME):
            await self._handle_link_input(input_text, settings)
            await self.notifier.notify_user(data.user, i18n_key="ntf-access-link-saved")

        else:
            logger.warning(f"{data.user.log} Provided invalid channel format: '{input_text}'")
            await self.notifier.notify_user(data.user, i18n_key="ntf-access-channel-invalid")

        async with self.uow:
            await self.settings_dao.update(settings)
            await self.uow.commit()

        logger.info(f"{data.user.log} Updated channel requirement")

    async def _handle_id_input(self, text: str, settings: SettingsDto) -> None:
        channel_id = int(text)
        if not text.startswith("-100") and not text.startswith("-"):
            channel_id = int(f"-100{text}")

        settings.requirements.channel_id = channel_id
        logger.debug(f"Parsed channel ID '{channel_id}' from input")

    async def _handle_link_input(self, text: str, settings: SettingsDto) -> None:
        settings.requirements.channel_link = SecretStr(text)
        logger.debug(f"Parsed channel link '{text}' from input")
