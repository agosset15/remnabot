from fastapi import APIRouter

from src.core.constants import API_V1

from .checkout import router as checkout_router
from .gateways import router as gateways_router
from .plans import router as plans_router

public_router = APIRouter(prefix=API_V1, tags=["public"])
public_router.include_router(plans_router, prefix="/plans")
public_router.include_router(gateways_router, prefix="/gateways")
public_router.include_router(checkout_router)
