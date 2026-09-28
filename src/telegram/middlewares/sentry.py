from typing import Any, Awaitable, Callable, Optional

import sentry_sdk
from aiogram.types import CallbackQuery, Message, TelegramObject
from aiogram.types import User as AiogramUser

from src.core.enums import MiddlewareEventType
from src.core.sentry import is_enabled, user_payload

from .base import EventTypedMiddleware


class SentryMiddleware(EventTypedMiddleware):
    """Gives every update its own Sentry scope with user and update context.

    Without the isolation scope, concurrently handled updates would share (and
    overwrite) each other's user/tag data on the global scope.
    """

    __event_types__ = [
        MiddlewareEventType.MESSAGE,
        MiddlewareEventType.CALLBACK_QUERY,
        MiddlewareEventType.AIOGD_UPDATE,
        MiddlewareEventType.INLINE_QUERY,
        MiddlewareEventType.PRE_CHECKOUT_QUERY,
        MiddlewareEventType.MY_CHAT_MEMBER,
    ]

    async def middleware_logic(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        if not is_enabled():
            return await handler(event, data)

        aiogram_user: Optional[AiogramUser] = self._get_aiogram_user(data)
        update_type = type(event).__name__

        with sentry_sdk.isolation_scope() as scope:
            scope.set_tag("source", "telegram")
            scope.set_tag("update_type", update_type)
            scope.set_user(
                user_payload(
                    telegram_id=aiogram_user.id if aiogram_user else None,
                    username=aiogram_user.username if aiogram_user else None,
                    name=aiogram_user.full_name if aiogram_user else None,
                )
            )
            scope.set_transaction_name(self._transaction_name(event, update_type))
            scope.add_breadcrumb(
                category="telegram",
                message=f"Handling {update_type}",
                level="info",
                data=self._breadcrumb_data(event),
            )

            return await handler(event, data)

    @staticmethod
    def _transaction_name(event: TelegramObject, update_type: str) -> str:
        if isinstance(event, CallbackQuery) and event.data:
            return f"callback_query:{event.data.split(':', 1)[0]}"

        if isinstance(event, Message) and event.text and event.text.startswith("/"):
            return f"command:{event.text.split()[0]}"

        return update_type

    @staticmethod
    def _breadcrumb_data(event: TelegramObject) -> dict[str, Any]:
        # Callback data is control-flow, not user content — safe without PII opt-in.
        if isinstance(event, CallbackQuery):
            return {"callback_data": event.data}

        if isinstance(event, Message):
            return {"content_type": event.content_type}

        return {}
