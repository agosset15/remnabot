from dishka.integrations.taskiq import FromDishka, inject

from src.application.use_cases.remnawave import RestoreUsersToLteSquad
from src.infrastructure.taskiq.broker import broker


@broker.task(schedule=[{"cron": "0 0 * * *"}])
@inject(patch_module=True)
async def restore_users_to_lte_squad_task(
    restore_users: FromDishka[RestoreUsersToLteSquad],
) -> None:
    await restore_users.system()
