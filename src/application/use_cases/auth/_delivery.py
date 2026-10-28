from typing import Optional

from loguru import logger

from src.application.common import Notifier, TranslatorHub
from src.application.common.email_sender import EmailSender
from src.application.dto import MessagePayloadDto, UserDto
from src.core.enums import Locale


async def deliver_email_code(
    *,
    email_sender: EmailSender,
    notifier: Optional[Notifier],
    i18n_hub: TranslatorHub,
    locale: Locale,
    target_email: str,
    code: str,
    minutes: int,
    link: Optional[str],
    user: Optional[UserDto] = None,
) -> bool:
    """Send a one-time code by email and, when linked, mirror it into Telegram.

    Email delivery errors propagate: the caller must not persist the code when the
    message never left. Telegram is a best-effort duplicate, so its failures are
    logged and swallowed.
    """
    i18n = i18n_hub.get_translator_by_locale(user.language if user else locale)

    has_link = "yes" if link else "no"
    kwargs = {"code": code, "minutes": minutes, "link": link or "", "has_link": has_link}

    await email_sender.send(
        to=target_email,
        subject=i18n.get("email-verification.title", code=code),
        body=i18n.get("email-verification.message", **kwargs),
        html=i18n.get("email-verification.message-html", **kwargs),
    )

    if notifier is None or user is None or user.telegram_id is None:
        return False

    try:
        await notifier.notify_user(
            user,
            payload=MessagePayloadDto(
                i18n_key="ntf-auth.login-code",
                i18n_kwargs=kwargs,
                delete_after=None,
            ),
        )
    except Exception as e:
        logger.warning(f"Failed to mirror email code to Telegram for user '{user.id}': {e}")
        return False

    return True
