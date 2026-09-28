from typing import Any, Optional

from dishka import AsyncContainer
from loguru import logger
from taskiq import TaskiqMessage, TaskiqResult
from taskiq.abc.middleware import TaskiqMiddleware

from src.application.common import EventPublisher
from src.application.events import ErrorEvent
from src.core.config import AppConfig
from src.core.sentry import capture_exception as sentry_capture_exception


class ErrorMiddleware(TaskiqMiddleware):
    async def on_error(
        self,
        message: TaskiqMessage,
        result: TaskiqResult[Any],
        exception: BaseException,
    ) -> None:
        logger.error(f"Task '{message.task_name}' error: {exception}")

        sentry_capture_exception(
            exception,
            tags={
                "source": "taskiq",
                "task_name": message.task_name,
            },
            contexts={
                "taskiq_task": {
                    "task_id": message.task_id,
                    "task_name": message.task_name,
                    "labels": message.labels,
                }
            },
            fingerprint=["taskiq", message.task_name, type(exception).__name__],
        )

        container: Optional[AsyncContainer] = self.broker.custom_dependency_context.get(
            AsyncContainer
        )

        if not container:
            logger.error("Dishka container not found in taskiq broker context")
            return

        try:
            config = await container.get(AppConfig)
            event_publisher = await container.get(EventPublisher)
            error_event = ErrorEvent(**config.build.data, exception=exception)
            await event_publisher.publish(error_event)
        except Exception as e:
            logger.error(f"Failed to publish error event: {e}")
