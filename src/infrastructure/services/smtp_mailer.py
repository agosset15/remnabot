import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger

from src.application.common.mailer import Mailer
from src.core.config import AppConfig


class SmtpMailerImpl(Mailer):
    """SMTP-based mailer that sends transactional emails via stdlib smtplib."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config.smtp
        logger.info(
            "SmtpMailer initialized: host={host} port={port} tls={tls} ssl={ssl}",
            host=self._config.host,
            port=self._config.port,
            tls=self._config.use_tls,
            ssl=self._config.use_ssl,
        )

    async def send_otp(self, email: str, code: str) -> None:
        """Build and dispatch the OTP email in a thread executor to keep the event loop free."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._send_otp_sync, email, code)

    def _build_message(self, to: str, code: str) -> MIMEMultipart:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "Your verification code"
        msg["From"] = self._config.sender or self._config.username
        msg["To"] = to

        plain = (
            f"Your verification code is: {code}\n\n"
            "The code is valid for 10 minutes. Do not share it with anyone."
        )
        html = (
            "<p>Your verification code is:</p>"
            f"<h2 style='letter-spacing:4px'>{code}</h2>"
            "<p>The code is valid for <strong>10 minutes</strong>. "
            "Do not share it with anyone.</p>"
        )

        msg.attach(MIMEText(plain, "plain", "utf-8"))
        msg.attach(MIMEText(html, "html", "utf-8"))
        return msg

    def _send_otp_sync(self, email: str, code: str) -> None:
        msg = self._build_message(email, code)
        sender = msg["From"]
        cfg = self._config

        try:
            if cfg.use_ssl:
                with smtplib.SMTP_SSL(cfg.host, cfg.port, timeout=cfg.timeout) as smtp:
                    if cfg.username:
                        smtp.login(cfg.username, cfg.password.get_secret_value())
                    smtp.sendmail(sender, email, msg.as_string())
            else:
                with smtplib.SMTP(cfg.host, cfg.port, timeout=cfg.timeout) as smtp:
                    if cfg.use_tls:
                        smtp.starttls()
                    if cfg.username:
                        smtp.login(cfg.username, cfg.password.get_secret_value())
                    smtp.sendmail(sender, email, msg.as_string())

            logger.info("OTP email sent to {email}", email=email)

        except smtplib.SMTPException as exc:
            logger.error("Failed to send OTP email to {email}: {exc}", email=email, exc=exc)
            raise
