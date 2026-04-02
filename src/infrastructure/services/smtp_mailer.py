import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger

from src.application.common import TranslatorHub
from src.application.common.mailer import Mailer
from src.application.dto import SubscriptionDto, UserDto
from src.application.services import BotService
from src.core.config import AppConfig


class SmtpMailerImpl(Mailer):
    """SMTP-based mailer that sends transactional emails via stdlib smtplib."""

    def __init__(
        self,
        config: AppConfig,
        i18n_hub: TranslatorHub,
        bot_service: BotService,
    ) -> None:
        self._config = config.smtp
        self._i18n = i18n_hub.get_translator_by_locale(config.default_locale)
        self._bot_service = bot_service
        logger.info(
            "SmtpMailer initialized: host={host} port={port} tls={tls} ssl={ssl}",
            host=self._config.host,
            port=self._config.port,
            tls=self._config.use_tls,
            ssl=self._config.use_ssl,
        )

    async def send_otp(self, email: str, code: str) -> None:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = self._i18n.get("email-otp.title")
        msg.attach(MIMEText(self._i18n.get("email-otp.message", code=code), "plain", "utf-8"))
        msg.attach(MIMEText(self._i18n.get("email-otp.message-html", code=code), "html", "utf-8"))
        await self._dispatch(email, msg)

    async def send_success_purchase(self, user: UserDto, subscription: SubscriptionDto) -> None:
        bot_url = await self._bot_service.get_connect_web_url(user.referral_code)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = self._i18n.get("email-success-purchase.title")
        msg.attach(
            MIMEText(
                self._i18n.get(
                    "email-success-purchase.message",
                    subscription_url=subscription.url,
                    bot_url=bot_url,
                ),
                "plain",
                "utf-8",
            )
        )
        msg.attach(
            MIMEText(
                self._i18n.get(
                    "email-success-purchase.message-html",
                    subscription_url=subscription.url,
                    bot_url=bot_url,
                    expire_date=subscription.expire_at.strftime("%d.%m.%Y"),
                    devices=subscription.device_limit,
                    plan_name=subscription.plan_snapshot.name,
                ),
                "html",
                "utf-8",
            )
        )
        await self._dispatch(user.email, msg)

    async def send_failed_purchase(self, user: UserDto) -> None:
        pass  # TODO: implement

    async def _dispatch(self, email: str, msg: MIMEMultipart) -> None:
        """Offload the blocking SMTP call to a thread executor."""
        msg["From"] = f'"KaGo VPS" <{self._config.sender or self._config.username}>'
        msg["To"] = email
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_sync, email, msg)

    def _send_sync(self, email: str, msg: MIMEMultipart) -> None:
        sender = msg["From"]
        try:
            with self._open_smtp_connection() as smtp:
                smtp.sendmail(sender, email, msg.as_string())
            logger.info("Email sent to {email}", email=email)
        except smtplib.SMTPException as exc:
            logger.error("Failed to send email to {email}: {exc}", email=email, exc=exc)
            raise

    def _open_smtp_connection(self) -> smtplib.SMTP:
        cfg = self._config
        if cfg.use_ssl:
            smtp = smtplib.SMTP_SSL(cfg.host, cfg.port, timeout=cfg.timeout)
        else:
            smtp = smtplib.SMTP(cfg.host, cfg.port, timeout=cfg.timeout)
            if cfg.use_tls:
                smtp.starttls()

        if cfg.username:
            smtp.login(cfg.username, cfg.password.get_secret_value())

        return smtp
