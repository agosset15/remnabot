import re

from loguru import logger

from src.application.common import BotService, EmailSender, TranslatorHub
from src.application.common.mailer import Mailer
from src.application.dto import SubscriptionDto, UserDto
from src.core.config import AppConfig
from src.core.enums import PurchaseType
from src.core.utils.i18n_helpers import i18n_format_device_limit

_HTML_TAG_RE = re.compile(r"<[^>]+>")


class SmtpMailerImpl(Mailer):
    """Renders FTL email templates and dispatches them via the shared EmailSender."""

    def __init__(
        self,
        config: AppConfig,
        email_sender: EmailSender,
        i18n_hub: TranslatorHub,
        bot_service: BotService,
    ) -> None:
        self._email_sender = email_sender
        self._i18n_hub = i18n_hub
        self._i18n = i18n_hub.get_translator_by_locale(config.default_locale)
        self._bot_service = bot_service

    @property
    def is_enabled(self) -> bool:
        return self._email_sender.is_enabled

    def _ready(self, user: UserDto) -> bool:
        if not self._email_sender.is_enabled:
            logger.warning(f"Mailer disabled; skip email for '{user.log}'")
            return False
        if not user.email:
            logger.warning(f"No email for '{user.log}'; skip email")
            return False
        return True

    async def send_success_purchase(
        self,
        user: UserDto,
        subscription: SubscriptionDto,
        purchase_type: PurchaseType,
    ) -> None:
        if not self._ready(user):
            return

        bot_url = await self._bot_service.get_referral_url(user.referral_code)
        purchase_type_value = purchase_type.value
        device_key, device_kwargs = i18n_format_device_limit(subscription.device_limit)

        await self._email_sender.send(
            to=user.email,
            subject=self._i18n.get(
                "email-success-purchase.title", purchase_type=purchase_type_value
            ),
            body=self._i18n.get(
                "email-success-purchase.message",
                subscription_url=subscription.url,
                bot_url=bot_url,
                purchase_type=purchase_type_value,
            ),
            html=self._i18n.get(
                "email-success-purchase.message-html",
                subscription_url=subscription.url,
                bot_url=bot_url,
                expire_date=subscription.expire_at.strftime("%d.%m.%Y"),
                devices=self._i18n.get(device_key, **device_kwargs),
                plan_name=subscription.plan_snapshot.name,
                purchase_type=purchase_type_value,
            ),
        )
        logger.info(f"Sent success-purchase email to '{user.email}'")

    async def send_failed_purchase(self, user: UserDto) -> None:
        if not self._ready(user):
            return

        bot_url = await self._bot_service.get_referral_url(user.referral_code)

        await self._email_sender.send(
            to=user.email,
            subject=self._i18n.get("email-failed-purchase.title"),
            body=self._i18n.get("email-failed-purchase.message", bot_url=bot_url),
            html=self._i18n.get("email-failed-purchase.message-html", bot_url=bot_url),
        )
        logger.info(f"Sent failed-purchase email to '{user.email}'")

    async def send_connect_telegram(self, user: UserDto) -> None:
        if not self._ready(user):
            return

        bot_url = await self._bot_service.get_referral_url(user.referral_code)

        await self._email_sender.send(
            to=user.email,
            subject=self._i18n.get("email-connect-telegram.title"),
            body=self._i18n.get("email-connect-telegram.message", bot_url=bot_url),
            html=self._i18n.get("email-connect-telegram.message-html", bot_url=bot_url),
        )
        logger.info(f"Sent connect-telegram email to '{user.email}'")

    async def send_custom_message(self, user: UserDto, body: str) -> None:
        if not self._ready(user):
            return

        bot_url = await self._bot_service.get_referral_url(user.referral_code)

        await self._email_sender.send(
            to=user.email,
            subject=self._i18n.get("email-custom-message.title"),
            body=_HTML_TAG_RE.sub("", body).strip(),
            html=self._i18n.get("email-custom-message.message-html", body=body, bot_url=bot_url),
        )
        logger.info(f"Sent custom email to '{user.email}'")

    async def send_notification(self, user: UserDto, body: str) -> None:
        if not self._ready(user):
            return

        i18n = self._i18n_hub.get_translator_by_locale(user.language)
        bot_url = await self._bot_service.get_referral_url(user.referral_code)
        plain_body = _HTML_TAG_RE.sub("", body).strip()

        await self._email_sender.send(
            to=user.email,
            subject=i18n.get("email-notification.title"),
            body=i18n.get("email-notification.message", body=plain_body, bot_url=bot_url),
            html=i18n.get("email-notification.message-html", body=body, bot_url=bot_url),
        )
        logger.info(f"Sent notification email to '{user.email}'")
