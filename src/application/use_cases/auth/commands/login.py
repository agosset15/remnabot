from dataclasses import dataclass

from fastapi import HTTPException, status

from src.application.common import Interactor
from src.application.common.dao import UserDao
from src.application.common.password_hasher import PasswordHasher
from src.application.dto import UserDto


@dataclass
class LoginEmailUserDto:
    email: str
    password: str


class LoginEmailUser(Interactor[LoginEmailUserDto, UserDto]):
    required_permission = None

    def __init__(self, user_dao: UserDao, password_hasher: PasswordHasher) -> None:
        self.user_dao = user_dao
        self.password_hasher = password_hasher

    async def _execute(self, actor: UserDto, data: LoginEmailUserDto) -> UserDto:
        user = await self.user_dao.get_by_email(data.email)
        invalid = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

        if not user:
            # Run a dummy verify to keep timing uniform whether the email exists.
            self.password_hasher.verify(data.password, "")
            raise invalid

        if user.password_hash:
            if not self.password_hasher.verify(data.password, user.password_hash):
                raise invalid
        else:
            # Passwordless first login: a user created with an email but no password
            # (e.g. by an admin) may sign in once with an empty password. They should
            # set a password afterwards.
            if data.password:
                raise invalid

        if user.is_blocked:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is blocked")
        return user
