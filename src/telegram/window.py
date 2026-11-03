from dataclasses import dataclass
from typing import Any, Optional

from aiogram_dialog import DialogManager, DialogProtocol
from aiogram_dialog import Window as WindowProtocol
from aiogram_dialog.api.entities import MediaAttachment, NewMessage
from aiogram_dialog.widgets.text import Text

from src.core.config import AppConfig
from src.core.constants import CONFIG_KEY


@dataclass
class NewMessageWithEffect(NewMessage):
    message_effect_id: Optional[str] = None
    # When True, `text` holds rich HTML and is sent via sendRichMessage.
    # The window media (banner) is embedded into the rich message as `rich_media`.
    is_rich: bool = False
    rich_media: Optional[MediaAttachment] = None


class Window(WindowProtocol):
    """
    Project window.

    Pass `rich=` with a text widget that renders Bot API rich HTML
    (https://core.telegram.org/bots/api#rich-html-style) to render the window
    as a rich message. The regular text widgets stay as the fallback used when
    `BOT_USE_RICH_MESSAGES=false`.
    """

    def __init__(self, *widgets: Any, rich: Optional[Text] = None, **kwargs: Any) -> None:
        super().__init__(*widgets, **kwargs)
        self.rich_text = rich

    def _is_rich(self, manager: DialogManager) -> bool:
        if self.rich_text is None:
            return False
        config: AppConfig = manager.middleware_data[CONFIG_KEY]
        return config.bot.use_rich_messages

    async def render_text(self, data: dict, manager: DialogManager) -> str:
        if self.rich_text is not None and self._is_rich(manager):
            return await self.rich_text.render_text(data, manager)
        return await super().render_text(data, manager)

    async def render(self, dialog: DialogProtocol, manager: DialogManager) -> NewMessage:
        new_message = await super().render(dialog, manager)
        is_rich = self._is_rich(manager)

        return NewMessageWithEffect(
            chat=new_message.chat,
            thread_id=new_message.thread_id,
            business_connection_id=new_message.business_connection_id,
            text=new_message.text,
            reply_markup=new_message.reply_markup,
            parse_mode=new_message.parse_mode,
            protect_content=new_message.protect_content,
            show_mode=new_message.show_mode,
            media=None if is_rich else new_message.media,
            link_preview_options=None if is_rich else new_message.link_preview_options,
            message_effect_id=getattr(manager, "message_effect_id", None),
            is_rich=is_rich,
            rich_media=new_message.media if is_rich else None,
        )
