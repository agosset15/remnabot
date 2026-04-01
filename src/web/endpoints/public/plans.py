from decimal import Decimal
from typing import Optional

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.common.dao import PlanDao, SettingsDao

router = APIRouter()


class PublicPlanDurationResponse(BaseModel):
    days: int
    price: Decimal
    currency: str


class PublicPlanResponse(BaseModel):
    id: int
    public_code: Optional[str]
    name: str
    description: Optional[str]
    type: str
    traffic_limit: int
    device_limit: int
    is_trial: bool
    durations: list[PublicPlanDurationResponse]


@router.get("")
@inject
async def get_public_plans(
    plan_dao: FromDishka[PlanDao],
    settings_dao: FromDishka[SettingsDao],
) -> list[PublicPlanResponse]:
    plans = await plan_dao.get_active_plans()
    settings = await settings_dao.get()
    default_currency = settings.default_currency

    result = []
    for plan in plans:
        if plan.is_trial:
            continue

        durations = []
        for duration in plan.durations:
            price = next((p.price for p in duration.prices if p.currency == default_currency), None)
            if price is not None:
                durations.append(
                    PublicPlanDurationResponse(
                        days=duration.days,
                        price=price,
                        currency=str(default_currency),
                    )
                )

        result.append(
            PublicPlanResponse(
                id=plan.id,  # ty: ignore[invalid-argument-type]
                public_code=plan.public_code,
                name=plan.name,
                description=plan.description,
                type=str(plan.type),
                traffic_limit=plan.traffic_limit,
                device_limit=plan.device_limit,
                is_trial=plan.is_trial,
                durations=durations,
            )
        )

    return result
