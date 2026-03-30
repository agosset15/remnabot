from decimal import Decimal
from typing import Optional

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.application.common.dao import SettingsDao
from src.application.dto import UserDto
from src.application.use_cases.user.queries.plans import GetAvailablePlans, GetAvailableTrial
from src.web.dependencies.auth import get_current_user

router = APIRouter()


class PlanDurationResponse(BaseModel):
    days: int
    price: Decimal
    currency: str


class PlanResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    type: str
    is_trial: bool
    traffic_limit: int
    device_limit: int
    durations: list[PlanDurationResponse]


class TrialPlanResponse(BaseModel):
    id: int
    name: str
    duration_days: int
    traffic_limit: int
    device_limit: int


class TrialResponse(BaseModel):
    available: bool
    plan: Optional[TrialPlanResponse]


@router.get("")
@inject
async def get_plans(
    get_available_plans: FromDishka[GetAvailablePlans],
    settings_dao: FromDishka[SettingsDao],
    current_user: UserDto = Depends(get_current_user),
) -> list[PlanResponse]:
    plans = await get_available_plans(actor=current_user, data=current_user)
    settings = await settings_dao.get()
    default_currency = settings.default_currency

    result = []
    for plan in plans:
        durations = []
        for duration in plan.durations:
            price = next((p.price for p in duration.prices if p.currency == default_currency), None)
            if price is not None:
                durations.append(
                    PlanDurationResponse(
                        days=duration.days,
                        price=price,
                        currency=str(default_currency),
                    )
                )

        result.append(
            PlanResponse(
                id=plan.id,  # ty: ignore[invalid-argument-type]
                name=plan.name,
                description=plan.description,
                type=str(plan.type),
                is_trial=plan.is_trial,
                traffic_limit=plan.traffic_limit,
                device_limit=plan.device_limit,
                durations=durations,
            )
        )

    return result


@router.get("/trial")
@inject
async def get_trial_plan(
    get_available_trial: FromDishka[GetAvailableTrial],
    current_user: UserDto = Depends(get_current_user),
) -> TrialResponse:
    if not current_user.is_trial_available:
        return TrialResponse(available=False, plan=None)

    plan = await get_available_trial(actor=current_user, data=current_user)
    if plan is None:
        return TrialResponse(available=False, plan=None)

    duration_days = plan.durations[0].days if plan.durations else 0

    return TrialResponse(
        available=True,
        plan=TrialPlanResponse(
            id=plan.id,  # ty: ignore[invalid-argument-type]
            name=plan.name,
            duration_days=duration_days,
            traffic_limit=plan.traffic_limit,
            device_limit=plan.device_limit,
        ),
    )
