import uuid
from typing import Optional
from urllib.parse import urlparse

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from src.application.common.cryptography import Cryptographer
from src.application.common.dao import (
    PaymentGatewayDao,
    PlanDao,
    SubscriptionDao,
    TransactionDao,
    UserDao,
)
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.dto.plan import PlanSnapshotDto
from src.application.dto.transaction import PriceDetailsDto, TransactionDto
from src.application.services.bot import BotService
from src.application.use_cases.gateways.queries.providers import GetPaymentGatewayInstance
from src.core.config import AppConfig
from src.core.enums import Locale, PaymentGatewayType, PurchaseType, Role, TransactionStatus

router = APIRouter()


class CheckoutRequest(BaseModel):
    plan_id: int
    duration_days: int
    gateway_type: str
    email: EmailStr
    return_url: str


class CheckoutResponse(BaseModel):
    payment_url: Optional[str]
    payment_id: str


class PaymentStatusResponse(BaseModel):
    status: TransactionStatus
    subscription_url: Optional[str] = None
    bot_url: Optional[str] = None


def _validate_return_url(return_url: str, origins: list[str]) -> None:
    allowed = [o for o in origins if o]
    if not allowed:
        return

    parsed = urlparse(return_url)
    origin = f"{parsed.scheme}://{parsed.netloc}"

    if origin not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"return_url origin '{origin}' is not in the allowed origins list",
        )


@router.post("/checkout")
@inject
async def checkout(
    body: CheckoutRequest,
    plan_dao: FromDishka[PlanDao],
    gateway_dao: FromDishka[PaymentGatewayDao],
    transaction_dao: FromDishka[TransactionDao],
    user_dao: FromDishka[UserDao],
    uow: FromDishka[UnitOfWork],
    cryptographer: FromDishka[Cryptographer],
    get_payment_gateway_instance: FromDishka[GetPaymentGatewayInstance],
    config: FromDishka[AppConfig],
) -> CheckoutResponse:
    _validate_return_url(body.return_url, list(config.origins))

    try:
        gateway_type = PaymentGatewayType(body.gateway_type.upper())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Unknown gateway type: {body.gateway_type}")

    plan = await plan_dao.get_by_id(body.plan_id)
    if not plan or not plan.is_active:
        raise HTTPException(status_code=404, detail="Plan not found or inactive")

    duration = plan.get_duration(body.duration_days)
    if not duration:
        raise HTTPException(
            status_code=404,
            detail=f"Duration {body.duration_days} days not found for this plan",
        )

    gateway = await gateway_dao.get_by_type(gateway_type)
    if not gateway or not gateway.is_active:
        raise HTTPException(
            status_code=400, detail=f"Payment gateway '{gateway_type}' is not available"
        )

    price = next((p.price for p in duration.prices if p.currency == gateway.currency), None)
    if price is None:
        raise HTTPException(
            status_code=400,
            detail=f"No price in currency '{gateway.currency}' for this plan/duration",
        )

    email = str(body.email).lower()
    user = await user_dao.get_by_email(email)

    if user is None:
        referral_code = cryptographer.generate_short_code(email)
        async with uow:
            user = await user_dao.create(
                UserDto(
                    email=email,
                    name=email,
                    role=Role.USER,
                    language=Locale(config.default_locale),
                    referral_code=referral_code,
                )
            )
            await uow.commit()

    plan_snapshot = PlanSnapshotDto.from_plan(plan, body.duration_days)
    pricing = PriceDetailsDto(
        original_amount=price,
        discount_percent=0,
        final_amount=price,
    )

    gateway_instance = await get_payment_gateway_instance.system(gateway_type)

    if pricing.is_free:
        payment_id = uuid.uuid4()
        transaction = TransactionDto(
            payment_id=payment_id,
            user_id=user.id,  # ty: ignore[invalid-argument-type]
            status=TransactionStatus.PENDING,
            purchase_type=PurchaseType.NEW,
            gateway_type=gateway_type,
            pricing=pricing,
            currency=gateway.currency,
            plan_snapshot=plan_snapshot,
        )
        async with uow:
            await transaction_dao.create(transaction)
            await uow.commit()
        return CheckoutResponse(payment_url=None, payment_id=str(payment_id))

    payment = await gateway_instance.handle_create_payment(
        amount=pricing.final_amount,
        details=f"{plan.name} - {body.duration_days} days",
    )

    transaction = TransactionDto(
        payment_id=payment.id,
        user_id=user.id,  # ty: ignore[invalid-argument-type]
        status=TransactionStatus.PENDING,
        purchase_type=PurchaseType.NEW,
        gateway_type=gateway_type,
        pricing=pricing,
        currency=gateway.currency,
        plan_snapshot=plan_snapshot,
    )
    async with uow:
        await transaction_dao.create(transaction)
        await uow.commit()

    return CheckoutResponse(
        payment_url=payment.url,
        payment_id=str(payment.id),
    )


@router.get("/payment/{payment_id}/status")
@inject
async def get_payment_status(
    payment_id: str,
    transaction_dao: FromDishka[TransactionDao],
    user_dao: FromDishka[UserDao],
    subscription_dao: FromDishka[SubscriptionDao],
    bot_service: FromDishka[BotService],
) -> PaymentStatusResponse:
    try:
        pid = uuid.UUID(payment_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payment_id format")

    transaction = await transaction_dao.get_by_payment_id(pid)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if not transaction.is_completed:
        return PaymentStatusResponse(status=transaction.status)

    user = await user_dao.get_by_id(transaction.user_id)
    if not user:
        return PaymentStatusResponse(status=transaction.status)

    subscription = await subscription_dao.get_by_user_id(user.id)  # ty: ignore[invalid-argument-type]
    subscription_url = subscription.url if subscription else None

    bot_url = await bot_service.get_connect_web_url(user.referral_code)

    return PaymentStatusResponse(
        status=transaction.status,
        subscription_url=subscription_url,
        bot_url=bot_url,
    )
