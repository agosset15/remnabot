import asyncio
from typing import Any, Coroutine

from loguru import logger


def create_safe_task(coro: Coroutine[Any, Any, Any]) -> asyncio.Task:
    task = asyncio.create_task(coro)

    def _log_result(task: asyncio.Task) -> None:
        try:
            task.result()
        except Exception as e:
            logger.exception("Background task failed", exc=e)

    task.add_done_callback(_log_result)
    return task
