from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.methods import SetWebhook
from aiogram.types import WebhookInfo
from loguru import logger

from src.application.common import Cryptographer
from src.application.common.dao import WebhookDao
from src.core.config import AppConfig
from src.core.utils.time import datetime_now

from .bot_registry import BotRegistry


class WebhookService:
    def __init__(
        self,
        webhook_dao: WebhookDao,
        bots: BotRegistry,
        config: AppConfig,
        cryptographer: Cryptographer,
    ) -> None:
        self.webhook_dao = webhook_dao
        self.bots = bots
        self.config = config
        self.cryptographer = cryptographer

    async def setup_webhooks(self, allowed_updates: list[str]) -> list[tuple[Bot, WebhookInfo]]:
        return [(bot, await self.setup_webhook(bot, allowed_updates)) for bot in self.bots.all()]

    async def delete_webhooks(self) -> None:
        for bot in self.bots.all():
            await self.delete_webhook(bot)

    async def setup_webhook(self, bot: Bot, allowed_updates: list[str]) -> WebhookInfo:
        safe_url = self.config.bot.safe_webhook_url(domain=self.config.domain)

        webhook_request = SetWebhook(
            url=self.config.bot.webhook_url(domain=self.config.domain).get_secret_value(),
            allowed_updates=allowed_updates,
            drop_pending_updates=self.config.bot.drop_pending_updates,
            secret_token=self.bots.secret_for(bot),
        )

        webhook_hash = self.cryptographer.get_hash(webhook_request.model_dump(exclude_unset=True))

        if await self.webhook_dao.is_hash_exists(bot.id, webhook_hash):
            if not self.config.bot.reset_webhook:
                logger.info(f"Webhook setup skipped for bot '{bot.id}', hash matches")
                return await bot.get_webhook_info()

        if not await bot(webhook_request):
            logger.error(f"Failed to set webhook for bot '{bot.id}' on URL '{safe_url}'")
            raise RuntimeError(f"Could not set webhook for bot '{bot.id}'")

        await self.webhook_dao.clear_all_hashes(bot.id)
        await self.webhook_dao.save_hash(bot.id, webhook_hash)

        logger.info(f"Webhook set successfully for bot '{bot.id}' to URL '{safe_url}'")
        return await bot.get_webhook_info()

    async def delete_webhook(self, bot: Bot) -> None:
        if not self.config.bot.reset_webhook:
            logger.debug(f"Webhook reset disabled in config for bot '{bot.id}'")
            return

        if await bot.delete_webhook():
            await self.webhook_dao.clear_all_hashes(bot.id)
            logger.info(f"Webhook deleted successfully for bot '{bot.id}'")
        else:
            logger.error(f"Failed to delete webhook for bot '{bot.id}'")

    def has_error(self, bot: Bot, webhook_info: WebhookInfo) -> bool:
        if not webhook_info.last_error_message or webhook_info.last_error_date is None:
            return False

        is_new = self._is_new_error(error_time=webhook_info.last_error_date)
        if is_new:
            logger.warning(f"Recent webhook error detected for bot '{bot.id}'")

        return is_new

    def _is_new_error(self, error_time: datetime, tolerance: int = 1) -> bool:
        current_time = datetime_now()
        time_difference = current_time - error_time
        return time_difference <= timedelta(seconds=tolerance)
