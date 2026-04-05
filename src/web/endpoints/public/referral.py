from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.application.common.dao import UserDao

router = APIRouter()


class ReferralNameResponse(BaseModel):
    name: str


@router.get("/referral/{code}")
@inject
async def get_referral_name(
    code: str,
    user_dao: FromDishka[UserDao],
) -> ReferralNameResponse:
    user = await user_dao.get_by_referral_code(code)
    if not user:
        raise HTTPException(status_code=404, detail="Referral not found")
    return ReferralNameResponse(name=user.name)
