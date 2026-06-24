from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

from src.application.use_cases.remnawave.commands.management import (
    RestoreUsersToLteSquad,
    ToggleLteSquad,
)
from src.core.enums import SubscriptionStatus


def _config(lte_uuid):
    return SimpleNamespace(remnawave=SimpleNamespace(lte_squad_uuid=lte_uuid))


def _remna_user(status, squad_uuids):
    return SimpleNamespace(
        uuid=uuid4(),
        status=status,
        active_internal_squads=[SimpleNamespace(uuid=u) for u in squad_uuids],
    )


async def test_toggle_noop_when_lte_uuid_unset():
    remna = AsyncMock()
    toggle = ToggleLteSquad(remnawave=remna, config=_config(None))

    await toggle.system(_remna_user(SubscriptionStatus.LIMITED, []))

    remna.update_user_internal_squads.assert_not_called()


async def test_toggle_excludes_when_limited_and_in_squad():
    lte, other = uuid4(), uuid4()
    remna = AsyncMock()
    toggle = ToggleLteSquad(remnawave=remna, config=_config(lte))
    user = _remna_user(SubscriptionStatus.LIMITED, [lte, other])

    await toggle.system(user)

    remna.update_user_internal_squads.assert_awaited_once()
    target_uuid, squads = remna.update_user_internal_squads.await_args.args
    assert target_uuid == user.uuid
    assert lte not in squads
    assert other in squads


async def test_toggle_noop_when_limited_and_already_excluded():
    lte = uuid4()
    remna = AsyncMock()
    toggle = ToggleLteSquad(remnawave=remna, config=_config(lte))

    await toggle.system(_remna_user(SubscriptionStatus.LIMITED, [uuid4()]))

    remna.update_user_internal_squads.assert_not_called()


async def test_toggle_restores_when_active_and_excluded():
    lte, other = uuid4(), uuid4()
    remna = AsyncMock()
    toggle = ToggleLteSquad(remnawave=remna, config=_config(lte))

    await toggle.system(_remna_user(SubscriptionStatus.ACTIVE, [other]))

    _, squads = remna.update_user_internal_squads.await_args.args
    assert lte in squads
    assert other in squads


async def test_toggle_noop_when_active_and_already_in_squad():
    lte = uuid4()
    remna = AsyncMock()
    toggle = ToggleLteSquad(remnawave=remna, config=_config(lte))

    await toggle.system(_remna_user(SubscriptionStatus.ACTIVE, [lte]))

    remna.update_user_internal_squads.assert_not_called()


async def test_restore_appends_lte_for_each_excluded_subscription():
    lte = uuid4()
    remna = AsyncMock()
    sub_a = SimpleNamespace(user_remna_id=uuid4(), internal_squads=[uuid4()])
    sub_b = SimpleNamespace(user_remna_id=uuid4(), internal_squads=[])
    dao = AsyncMock()
    dao.get_active_excluded_from_squad.return_value = [sub_a, sub_b]
    restore = RestoreUsersToLteSquad(remnawave=remna, config=_config(lte), subscription_dao=dao)

    await restore.system()

    assert remna.update_user_internal_squads.await_count == 2
    for call in remna.update_user_internal_squads.await_args_list:
        assert lte in call.args[1]


async def test_restore_noop_when_lte_uuid_unset():
    remna = AsyncMock()
    dao = AsyncMock()
    restore = RestoreUsersToLteSquad(remnawave=remna, config=_config(None), subscription_dao=dao)

    await restore.system()

    dao.get_active_excluded_from_squad.assert_not_called()
