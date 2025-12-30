from typing import Protocol, runtime_checkable

from src.application.dto import SettingsDTO


@runtime_checkable
class SettingsDAO(Protocol):
    async def get(self) -> SettingsDTO: ...

    async def update(self, dto: SettingsDTO) -> SettingsDTO: ...

    async def create_default(self) -> SettingsDTO: ...
