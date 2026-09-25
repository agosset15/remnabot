from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource

from src.core.config import AppConfig
from src.core.enums import SentryComponent
from src.core.logger import setup_logger
from src.core.sentry import setup_sentry

from .broker import broker


def scheduler() -> TaskiqScheduler:
    config = AppConfig.get()
    setup_logger(config)
    setup_sentry(config, SentryComponent.SCHEDULER)

    scheduler = TaskiqScheduler(
        broker=broker,
        sources=[LabelScheduleSource(broker)],
    )

    return scheduler
