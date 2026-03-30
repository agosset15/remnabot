from fastapi import APIRouter

from .auth import router as auth_router
from .payments import router as payments_router
from .plans import router as plans_router
from .profile import router as profile_router
from .referral import router as referral_router

user_router = APIRouter(prefix="/api/user")
user_router.include_router(auth_router, prefix="/auth", tags=["auth"])
user_router.include_router(profile_router, prefix="/profile", tags=["profile"])
user_router.include_router(plans_router, prefix="/plans", tags=["plans"])
user_router.include_router(payments_router, prefix="/payments", tags=["payments"])
user_router.include_router(referral_router, prefix="/referral", tags=["referral"])
