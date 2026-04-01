from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter
from pydantic import BaseModel

from src.application.common.dao import PaymentGatewayDao

router = APIRouter()


class PublicGatewayResponse(BaseModel):
    type: str
    currency: str


@router.get("")
@inject
async def get_public_gateways(
    gateway_dao: FromDishka[PaymentGatewayDao],
) -> list[PublicGatewayResponse]:
    gateways = await gateway_dao.get_active()
    return [
        PublicGatewayResponse(
            type=str(gw.type),
            currency=str(gw.currency),
        )
        for gw in gateways
    ]
