from typing import Optional

from dishka.integrations.fastapi import inject, FromDishka
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.application.dto import UserDto
from src.application.services.bot import BotService
from src.application.use_cases.statistics.queries.users import GetUserStatistics
from src.web.dependencies.auth import get_current_user

router = APIRouter()


class ReferralResponse(BaseModel):
    referral_url: str
    referrals_level_1: int
    referrals_level_2: int
    reward_points: int
    reward_days: int
    referrer_username: Optional[str]
    referrer_telegram_id: Optional[int]


@router.get("")
@inject
async def get_referral(
    current_user: UserDto = Depends(get_current_user),
    get_user_statistics: FromDishka[GetUserStatistics] = ...,
    bot_service: FromDishka[BotService] = ...,
) -> ReferralResponse:
    try:
        stats = await get_user_statistics.system(current_user.telegram_id)
    except Exception as e:
        raise HTTPException(status_code=503, detail="Failed to load referral statistics")

    referral_url = await bot_service.get_referral_url(current_user.referral_code)

    return ReferralResponse(
        referral_url=referral_url,
        referrals_level_1=stats.referrals_level_1,
        referrals_level_2=stats.referrals_level_2,
        reward_points=stats.reward_points,
        reward_days=stats.reward_days,
        referrer_username=stats.referrer_username,
        referrer_telegram_id=stats.referrer_telegram_id,
    )
