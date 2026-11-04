from typing import Optional

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import (
    FSInputFile,
    InputMediaAnimation,
    InputMediaPhoto,
    InputRichMessage,
    InputRichMessageMedia,
    Message,
    RichBlockAnimation,
    RichBlockPhoto,
    URLInputFile,
)
from aiogram_dialog.api.entities import MediaAttachment, NewMessage, OldMessage
from aiogram_dialog.manager.message_manager import SEND_METHODS
from aiogram_dialog.manager.message_manager import MessageManager as MessageManagerProtocol
from loguru import logger

RICH_MEDIA_ID = "banner"

# Banner path/url -> Telegram file_id, so the banner is uploaded only once per process.
_rich_media_cache: dict[str, str] = {}


def _is_rich(new_message: NewMessage) -> bool:
    return bool(getattr(new_message, "is_rich", False))


def _rich_media(new_message: NewMessage) -> Optional[MediaAttachment]:
    return getattr(new_message, "rich_media", None)


def _media_key(media: MediaAttachment) -> Optional[str]:
    if media.path:
        return str(media.path)
    return media.url


class MessageManager(MessageManagerProtocol):
    # Plain <-> rich transitions are done by delete + send:
    # editMessageText does not document converting a message between the two kinds.
    def _can_edit(self, new_message: NewMessage, old_message: OldMessage) -> bool:
        had_rich = old_message.content_type == ContentType.RICH_MESSAGE
        if had_rich != _is_rich(new_message):
            return False
        return super()._can_edit(new_message, old_message)

    async def _build_rich_message(self, bot: Bot, new_message: NewMessage) -> InputRichMessage:
        html = new_message.text or ""
        media = _rich_media(new_message)

        if not media:
            return InputRichMessage(html=html)

        key = _media_key(media)
        source: str | FSInputFile | URLInputFile
        if media.file_id:
            source = media.file_id.file_id
        elif key and key in _rich_media_cache:
            source = _rich_media_cache[key]
        else:
            source = await self.get_media_source(media, bot)  # type: ignore[assignment]

        input_media: InputMediaPhoto | InputMediaAnimation
        if media.type == ContentType.ANIMATION:
            input_media = InputMediaAnimation(media=source)
            tag = f'<video src="tg://video?id={RICH_MEDIA_ID}"></video>'
        else:
            input_media = InputMediaPhoto(media=source)
            tag = f'<img src="tg://photo?id={RICH_MEDIA_ID}"/>'

        return InputRichMessage(
            html=tag + html,
            media=[InputRichMessageMedia(id=RICH_MEDIA_ID, media=input_media)],
        )

    def _remember_rich_media(self, new_message: NewMessage, message: Message) -> None:
        media = _rich_media(new_message)
        if not media or not message.rich_message:
            return

        key = _media_key(media)
        if not key or key in _rich_media_cache:
            return

        for block in message.rich_message.blocks:
            if isinstance(block, RichBlockPhoto) and block.photo:
                _rich_media_cache[key] = block.photo[-1].file_id
                return
            if isinstance(block, RichBlockAnimation):
                _rich_media_cache[key] = block.animation.file_id
                return

        logger.debug(f"No media block found in rich message to cache for '{key}'")

    async def send_text(self, bot: Bot, new_message: NewMessage) -> Message:
        if _is_rich(new_message):
            message = await bot.send_rich_message(
                chat_id=new_message.chat.id,
                rich_message=await self._build_rich_message(bot, new_message),
                message_thread_id=new_message.thread_id,
                business_connection_id=new_message.business_connection_id,
                reply_markup=new_message.reply_markup,
                protect_content=new_message.protect_content,
                message_effect_id=getattr(new_message, "message_effect_id", None),
            )
            self._remember_rich_media(new_message, message)
            return message

        return await bot.send_message(
            new_message.chat.id,
            text=new_message.text,  # type: ignore[arg-type]
            message_thread_id=new_message.thread_id,
            business_connection_id=new_message.business_connection_id,
            reply_markup=new_message.reply_markup,
            parse_mode=new_message.parse_mode,
            link_preview_options=new_message.link_preview_options,
            message_effect_id=getattr(new_message, "message_effect_id", None),
        )

    async def edit_text(
        self,
        bot: Bot,
        new_message: NewMessage,
        old_message: OldMessage,
    ) -> Message:
        if not _is_rich(new_message):
            return await super().edit_text(bot, new_message, old_message)

        message = await bot.edit_message_text(
            message_id=old_message.message_id,
            chat_id=old_message.chat.id,
            business_connection_id=new_message.business_connection_id,
            rich_message=await self._build_rich_message(bot, new_message),
            reply_markup=new_message.reply_markup,  # type: ignore[arg-type]
        )
        if isinstance(message, Message):
            self._remember_rich_media(new_message, message)
            return message
        raise RuntimeError("editMessageText returned no message for a chat message")

    async def send_media(self, bot: Bot, new_message: NewMessage) -> Message:
        method = getattr(bot, SEND_METHODS[new_message.media.type], None)  # type: ignore[union-attr]

        if not method:
            raise ValueError(
                f"ContentType {new_message.media.type} is not supported",  # type: ignore[union-attr]
            )

        return await method(  # type: ignore[no-any-return]
            new_message.chat.id,
            await self.get_media_source(new_message.media, bot),  # type: ignore[arg-type]
            message_thread_id=new_message.thread_id,
            business_connection_id=new_message.business_connection_id,
            caption=new_message.text,
            reply_markup=new_message.reply_markup,
            parse_mode=new_message.parse_mode,
            message_effect_id=getattr(new_message, "message_effect_id", None),
            **new_message.media.kwargs,  # type: ignore[union-attr]
        )
