from typing import Optional

from aiogram import Bot, Router
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from dishka import FromDishka

from src.application.dto import TelegramUserDto
from src.application.use_cases.user.commands.blocking import (
    SetBotBlockedStatus,
    SetBotBlockedStatusDto,
)
from src.infrastructure.services.bot_registry import BotRegistry

# For only ChatType.PRIVATE (app/bot/filters/private.py)

router = Router(name=__name__)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_unblocked(
    member: ChatMemberUpdated,
    bot: Bot,
    user: Optional[TelegramUserDto],
    set_bot_blocked_status: FromDishka[SetBotBlockedStatus],
) -> None:
    if not user:
        return

    # (Re)starting a bot makes it the one the user is reached through.
    await set_bot_blocked_status.system(SetBotBlockedStatusDto(user.id, False, bot_id=bot.id))


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def on_blocked(
    member: ChatMemberUpdated,
    bot: Bot,
    user: Optional[TelegramUserDto],
    set_bot_blocked_status: FromDishka[SetBotBlockedStatus],
    bots: FromDishka[BotRegistry],
) -> None:
    if not user:
        return

    # Blocking a bot the user no longer uses doesn't make them unreachable.
    if bots.for_user(user).id != bot.id:
        return

    await set_bot_blocked_status.system(SetBotBlockedStatusDto(user.id, True))
