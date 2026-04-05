from dataclasses import dataclass

from loguru import logger

from src.application.common import Interactor, Notifier, TranslatorRunner
from src.application.common.dao import UserDao
from src.application.common.policy import Permission
from src.application.dto import MessagePayloadDto, UserDto
from src.application.services import BotService
from src.telegram.keyboards import get_contact_support_keyboard


@dataclass(frozen=True)
class SendMessageToUserDto:
    user_id: int
    payload: MessagePayloadDto


class SendMessageToUser(Interactor[SendMessageToUserDto, bool]):
    required_permission = Permission.USER_EDITOR

    def __init__(
        self,
        user_dao: UserDao,
        notifier: Notifier,
        bot_service: BotService,
        i18n: TranslatorRunner,
    ):
        self.user_dao = user_dao
        self.notifier = notifier
        self.bot_service = bot_service
        self.i18n = i18n

    async def _execute(self, actor: UserDto, data: SendMessageToUserDto) -> bool:
        target_user = await self.user_dao.get_by_id(data.user_id)
        if not target_user or not target_user.telegram_id:
            raise ValueError(f"User '{data.user_id}' not found or has no telegram id")

        support_url = self.bot_service.get_support_url(text=self.i18n.get("message.help"))
        data.payload.reply_markup = get_contact_support_keyboard(support_url)
        message = await self.notifier.notify_user(user=target_user, payload=data.payload)

        if message:
            logger.info(f"{actor.log} Sent message to user '{data.telegram_id}'")
            return True

        logger.warning(f"{actor.log} Failed to send message to user '{data.telegram_id}'")
        return False
