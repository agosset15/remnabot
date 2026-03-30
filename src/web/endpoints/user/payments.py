from datetime import datetime
from decimal import Decimal
from typing import Optional

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.application.common.dao import PaymentGatewayDao, PlanDao, SettingsDao, TransactionDao
from src.application.dto import PlanSnapshotDto, UserDto
from src.application.services.pricing import PricingService
from src.application.use_cases.gateways.commands.payment import (
    CreatePayment,
    CreatePaymentDto,
    ProcessPayment,
    ProcessPaymentDto,
)
from src.application.use_cases.subscription.commands.purchase import (
    ActivateTrialSubscription,
    ActivateTrialSubscriptionDto,
)
from src.application.use_cases.user.queries.plans import GetAvailableTrial
from src.core.enums import PaymentGatewayType, PurchaseType, TransactionStatus
from src.web.dependencies.auth import get_current_user

router = APIRouter()


class GatewayResponse(BaseModel):
    type: str
    currency: str
    currency_symbol: str


class CreatePaymentRequest(BaseModel):
    plan_id: int
    duration_days: int
    gateway_type: str
    purchase_type: str


class CreatePaymentResponse(BaseModel):
    payment_id: str
    redirect_url: Optional[str]
    is_free: bool


class TransactionResponse(BaseModel):
    payment_id: str
    status: str
    purchase_type: str
    gateway_type: str
    currency: str
    currency_symbol: str
    original_amount: Decimal
    final_amount: Decimal
    discount_percent: int
    plan_name: str
    plan_duration_days: int
    created_at: Optional[datetime]


@router.get("/gateways")
@inject
async def get_gateways(
    payment_gateway_dao: FromDishka[PaymentGatewayDao],
    current_user: UserDto = Depends(get_current_user),
) -> list[GatewayResponse]:
    gateways = await payment_gateway_dao.get_active()
    return [
        GatewayResponse(
            type=str(g.type),
            currency=str(g.currency),
            currency_symbol=g.currency.symbol,
        )
        for g in gateways
    ]


@router.post("/create")
@inject
async def create_payment(
    settings_dao: FromDishka[SettingsDao],
    plan_dao: FromDishka[PlanDao],
    payment_gateway_dao: FromDishka[PaymentGatewayDao],
    pricing_service: FromDishka[PricingService],
    create_payment_uc: FromDishka[CreatePayment],
    process_payment_uc: FromDishka[ProcessPayment],
    body: CreatePaymentRequest,
    current_user: UserDto = Depends(get_current_user),
) -> CreatePaymentResponse:
    settings = await settings_dao.get()
    if not settings.access.payments_allowed:
        raise HTTPException(status_code=403, detail="Payments are currently disabled")

    plan = await plan_dao.get_by_id(body.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    duration = plan.get_duration(body.duration_days)
    if not duration:
        raise HTTPException(status_code=400, detail="Duration not found for this plan")

    try:
        gateway_type = PaymentGatewayType(body.gateway_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid gateway type")

    gateway = await payment_gateway_dao.get_by_type(gateway_type)
    if not gateway or not gateway.is_active:
        raise HTTPException(status_code=400, detail="Payment gateway not available")

    try:
        purchase_type = PurchaseType(body.purchase_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid purchase type")

    price = duration.get_price(gateway.currency)
    pricing = pricing_service.calculate(current_user, price, gateway.currency)
    plan_snapshot = PlanSnapshotDto.from_plan(plan, body.duration_days)

    try:
        result = await create_payment_uc(
            actor=current_user,
            data=CreatePaymentDto(
                plan_snapshot=plan_snapshot,
                pricing=pricing,
                purchase_type=purchase_type,
                gateway_type=gateway_type,
            ),
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if pricing.is_free:
        await process_payment_uc.system(
            ProcessPaymentDto(
                payment_id=result.id,
                new_transaction_status=TransactionStatus.COMPLETED,
            )
        )

    return CreatePaymentResponse(
        payment_id=str(result.id),
        redirect_url=str(result.url) if result.url else None,
        is_free=pricing.is_free,
    )


@router.post("/trial")
@inject
async def activate_trial(
    get_available_trial: FromDishka[GetAvailableTrial],
    activate_trial_subscription: FromDishka[ActivateTrialSubscription],
    current_user: UserDto = Depends(get_current_user),
) -> dict:
    if not current_user.is_trial_available:
        raise HTTPException(status_code=400, detail="Trial is not available for this user")

    plan = await get_available_trial.system(current_user)
    if plan is None:
        raise HTTPException(status_code=404, detail="No trial plan available")

    if not plan.durations:
        raise HTTPException(status_code=404, detail="Trial plan has no duration configured")

    duration = plan.durations[0]
    plan_snapshot = PlanSnapshotDto.from_plan(plan, duration.days)

    try:
        await activate_trial_subscription.system(
            ActivateTrialSubscriptionDto(user=current_user, plan=plan_snapshot)
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Failed to activate trial")

    return {"ok": True, "message": "Trial activated"}


@router.get("/history")
@inject
async def get_payment_history(
    transaction_dao: FromDishka[TransactionDao],
    current_user: UserDto = Depends(get_current_user),
) -> list[TransactionResponse]:
    transactions = await transaction_dao.get_by_user(current_user.telegram_id)

    result = []
    for tx in transactions:
        if tx.is_test:
            continue
        if tx.status not in (TransactionStatus.COMPLETED, TransactionStatus.CANCELED):
            continue

        plan_snapshot = tx.plan_snapshot
        result.append(
            TransactionResponse(
                payment_id=str(tx.payment_id),
                status=str(tx.status),
                purchase_type=str(tx.purchase_type),
                gateway_type=str(tx.gateway_type),
                currency=str(tx.currency),
                currency_symbol=tx.currency.symbol,
                original_amount=tx.pricing.original_amount,
                final_amount=tx.pricing.final_amount,
                discount_percent=tx.pricing.discount_percent,
                plan_name=plan_snapshot.name,
                plan_duration_days=plan_snapshot.duration,
                created_at=tx.created_at,
            )
        )

    return result
