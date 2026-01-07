from aiogram import Router
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from dishka import FromDishka

from src.application.dto import UserDto
from src.application.use_cases.user import SetBotBlockedStatus, SetBotBlockedStatusDto

# For only ChatType.PRIVATE (app/bot/filters/private.py)

router = Router(name=__name__)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def on_unblocked(
    member: ChatMemberUpdated,
    user: UserDto,
    set_bot_blocked_status: FromDishka[SetBotBlockedStatus],
) -> None:
    await set_bot_blocked_status(SetBotBlockedStatusDto(user, False))


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def on_blocked(
    member: ChatMemberUpdated,
    user: UserDto,
    set_bot_blocked_status: FromDishka[SetBotBlockedStatus],
) -> None:
    await set_bot_blocked_status(SetBotBlockedStatusDto(user, True))
