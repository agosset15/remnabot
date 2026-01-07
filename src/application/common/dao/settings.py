from typing import Protocol, runtime_checkable

from src.application.dto import SettingsDto


@runtime_checkable
class SettingsDao(Protocol):
    async def get(self) -> SettingsDto: ...

    async def update(self, settings: SettingsDto) -> SettingsDto: ...

    async def create_default(self) -> SettingsDto: ...
