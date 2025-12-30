from aiogram.types import BufferedInputFile
from dishka.integrations.taskiq import FromDishka, inject

from src.infrastructure.taskiq.broker import broker


@broker.task
@inject
async def send_error_task() -> None:
    raise ValueError()
