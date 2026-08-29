from typing import Final

from src.application.common import Interactor

from .commands.management import (
    DeleteUserAllDevices,
    DeleteUserDevice,
    ReissueSubscription,
    ReissueUserSubscription,
    ResetUserTraffic,
    RestoreUsersToLteSquad,
    ToggleLteSquad,
)
from .commands.synchronization import SyncAllUsersFromBot, SyncAllUsersFromPanel, SyncRemnaUser
from .queries.squads import GetExternalSquads, GetInternalSquads

REMNAWAVE_USE_CASES: Final[tuple[type[Interactor], ...]] = (
    SyncAllUsersFromBot,
    SyncAllUsersFromPanel,
    SyncRemnaUser,
    DeleteUserDevice,
    DeleteUserAllDevices,
    ResetUserTraffic,
    ReissueSubscription,
    ReissueUserSubscription,
    ToggleLteSquad,
    RestoreUsersToLteSquad,
    GetInternalSquads,
    GetExternalSquads,
)
