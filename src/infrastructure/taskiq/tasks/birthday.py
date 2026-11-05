from dishka.integrations.taskiq import FromDishka, inject

from src.application.use_cases.user.commands.birthday import (
    CongratulateBirthdayUsers,
    SyncUserBirthdates,
)
from src.infrastructure.taskiq.broker import broker


# Hourly batches spread the weekly re-fetch of every user's birthdate across the day.
@broker.task(schedule=[{"cron": "15 * * * *"}], retry_on_error=False)
@inject(patch_module=True)
async def sync_birthdates_task(
    sync_user_birthdates: FromDishka[SyncUserBirthdates],
) -> None:
    await sync_user_birthdates.system()


# 09:00 UTC (12:00 MSK): still the same calendar day from UTC-9 to UTC+14.
@broker.task(schedule=[{"cron": "0 9 * * *"}], retry_on_error=False)
@inject(patch_module=True)
async def congratulate_birthdays_task(
    congratulate_birthday_users: FromDishka[CongratulateBirthdayUsers],
) -> None:
    await congratulate_birthday_users.system()
