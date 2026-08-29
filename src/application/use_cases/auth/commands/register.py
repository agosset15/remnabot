from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.application.common import Interactor
from src.application.common.dao import UserDao
from src.application.common.password_hasher import PasswordHasher
from src.application.common.uow import UnitOfWork
from src.application.dto import UserDto
from src.application.use_cases.user.commands.web_registration import (
    RegisterWebUser,
    RegisterWebUserDto,
)
from src.core.config import AppConfig
from src.core.enums import AuthType


@dataclass
class RegisterEmailUserDto:
    email: str
    password: str
    name: Optional[str] = None
    referral_code: Optional[str] = None


class RegisterEmailUser(Interactor[RegisterEmailUserDto, UserDto]):
    required_permission = None

    def __init__(
        self,
        config: AppConfig,
        uow: UnitOfWork,
        user_dao: UserDao,
        password_hasher: PasswordHasher,
        register_web_user: RegisterWebUser,
    ) -> None:
        self.config = config
        self.uow = uow
        self.user_dao = user_dao
        self.password_hasher = password_hasher
        self.register_web_user = register_web_user

    async def _execute(self, actor: UserDto, data: RegisterEmailUserDto) -> UserDto:
        existing = await self.user_dao.get_by_email(data.email)
        if existing:
            if existing.password_hash:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
                )
            # Account created without a password (e.g. email set by an admin):
            # registration acts as a first-time password set that claims it.
            return await self._set_password(existing, data.password)

        referral_code = data.referral_code
        if referral_code and not await self.user_dao.get_by_referral_code(referral_code):
            referral_code = None

        new_user = UserDto(
            telegram_id=None,
            auth_type=AuthType.EMAIL,
            email=data.email,
            password_hash=self.password_hasher.hash(data.password),
            username=None,
            name=data.name or data.email.split("@")[0],
            language=self.config.default_locale,
        )

        try:
            return await self.register_web_user.system(
                RegisterWebUserDto(user=new_user, referral_code=referral_code)
            )
        except IntegrityError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            ) from e

    async def _set_password(self, user: UserDto, password: str) -> UserDto:
        user.password_hash = self.password_hasher.hash(password)
        user.auth_type = AuthType.EMAIL
        async with self.uow:
            updated = await self.user_dao.update(user)
            if not updated:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found during registration",
                )
            await self.uow.commit()
        return updated
