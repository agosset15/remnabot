from datetime import datetime
from typing import Optional

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.application.common.dao import SubscriptionDao
from src.application.dto import UserDto
from src.application.use_cases.remnawave.commands.management import (
    DeleteUserAllDevices,
    DeleteUserDevice,
    DeleteUserDeviceDto,
    ReissueSubscription,
)
from src.application.use_cases.user.queries.profile import (
    GetUserDevices,
    GetUserProfileSubscription,
)
from src.web.dependencies.auth import get_current_user

router = APIRouter()


class SubscriptionResponse(BaseModel):
    status: str
    is_trial: bool
    expire_at: datetime
    url: str
    traffic_limit: int
    device_limit: int
    plan_name: str
    is_expired: bool


class ProfileResponse(BaseModel):
    telegram_id: int
    username: Optional[str]
    name: str
    points: int
    personal_discount: int
    is_trial_available: bool
    referral_code: str
    subscription: Optional[SubscriptionResponse]


class SubscriptionDetailResponse(BaseModel):
    status: str
    is_trial: bool
    expire_at: datetime
    url: str
    traffic_limit: int
    device_limit: int
    used_traffic_bytes: int
    internal_squads: list[str]
    last_connected_node: Optional[str]
    plan_name: str


class DeviceResponse(BaseModel):
    hwid: str
    platform: Optional[str]
    device_model: Optional[str]
    os_version: Optional[str]
    user_agent: Optional[str]


class DevicesResponse(BaseModel):
    devices: list[DeviceResponse]
    current_count: int
    max_count: int


@router.get("")
@inject
async def get_profile(
    subscription_dao: FromDishka[SubscriptionDao],
    current_user: UserDto = Depends(get_current_user),
) -> ProfileResponse:
    subscription = await subscription_dao.get_current(current_user.id)

    sub_response: Optional[SubscriptionResponse] = None
    if subscription is not None:
        sub_response = SubscriptionResponse(
            status=str(subscription.current_status),
            is_trial=subscription.is_trial,
            expire_at=subscription.expire_at,
            url=subscription.url,
            traffic_limit=subscription.traffic_limit,
            device_limit=subscription.device_limit,
            plan_name=subscription.plan_snapshot.name,
            is_expired=subscription.is_expired,
        )

    return ProfileResponse(
        telegram_id=current_user.telegram_id,
        username=current_user.username,
        name=current_user.name,
        points=current_user.points,
        personal_discount=current_user.personal_discount,
        is_trial_available=current_user.is_trial_available,
        referral_code=current_user.referral_code,
        subscription=sub_response,
    )


@router.get("/subscription")
@inject
async def get_subscription_detail(
    get_user_profile_subscription: FromDishka[GetUserProfileSubscription],
    current_user: UserDto = Depends(get_current_user),
) -> SubscriptionDetailResponse:
    try:
        result = await get_user_profile_subscription.system(current_user.telegram_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Subscription service unavailable")

    used_traffic_bytes: int = getattr(result.remna_user, "used_traffic_bytes", 0) or 0
    internal_squads = [s.name for s in (result.remna_user.active_internal_squads or [])]

    return SubscriptionDetailResponse(
        status=str(result.subscription.current_status),
        is_trial=result.subscription.is_trial,
        expire_at=result.subscription.expire_at,
        url=result.subscription.url,
        traffic_limit=result.subscription.traffic_limit,
        device_limit=result.subscription.device_limit,
        used_traffic_bytes=used_traffic_bytes,
        internal_squads=internal_squads,
        last_connected_node=result.last_node_name,
        plan_name=result.subscription.plan_snapshot.name,
    )


@router.get("/subscription/devices")
@inject
async def get_devices(
    get_user_devices: FromDishka[GetUserDevices],
    current_user: UserDto = Depends(get_current_user),
) -> DevicesResponse:
    try:
        result = await get_user_devices.system(current_user.telegram_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Subscription service unavailable")

    devices = [
        DeviceResponse(
            hwid=d.hwid,
            platform=getattr(d, "platform", None),
            device_model=getattr(d, "device_model", None),
            os_version=getattr(d, "os_version", None),
            user_agent=getattr(d, "user_agent", None),
        )
        for d in result.devices
    ]

    return DevicesResponse(
        devices=devices,
        current_count=result.current_count,
        max_count=result.max_count,
    )


@router.delete("/subscription/devices/{hwid}")
@inject
async def delete_device(
    hwid: str,
    delete_user_device: FromDishka[DeleteUserDevice],
    current_user: UserDto = Depends(get_current_user),
) -> dict:
    try:
        await delete_user_device(
            actor=current_user,
            data=DeleteUserDeviceDto(user_id=current_user.id, hwid=hwid),
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Subscription service unavailable")

    return {"ok": True}


@router.delete("/subscription/devices")
@inject
async def delete_all_devices(
    delete_user_all_devices: FromDishka[DeleteUserAllDevices],
    current_user: UserDto = Depends(get_current_user),
) -> dict:
    try:
        await delete_user_all_devices(actor=current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Subscription service unavailable")

    return {"ok": True}


@router.post("/subscription/reissue")
@inject
async def reissue_subscription(
    reissue: FromDishka[ReissueSubscription],
    current_user: UserDto = Depends(get_current_user),
) -> dict:
    try:
        await reissue(actor=current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=503, detail="Subscription service unavailable")

    return {"ok": True}
