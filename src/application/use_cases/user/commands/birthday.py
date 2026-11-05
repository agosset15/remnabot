"""Birthday greetings.

Telegram only exposes a user's birthdate through ``getChat`` (``ChatFullInfo.birthdate``),
never in updates, so it is cached on the user row:

- ``SyncUserBirthdates`` (hourly) re-fetches the birthdate of users whose cached value is
  older than ``BIRTHDATE_SYNC_INTERVAL_DAYS``, in throttled batches.
- ``CongratulateBirthdayUsers`` (daily) picks users whose cached birthday is today,
  re-checks it live, and grants ``BIRTHDAY_GIFT_DAYS`` to their subscription once a year.
"""

import asyncio
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter
from loguru import logger

from src.application.common import BotService, EventPublisher, Interactor, Remnawave
from src.application.common.dao import SettingsDao, SubscriptionDao, UserDao
from src.application.common.uow import UnitOfWork
from src.application.dto import BirthdateDto, UserDto
from src.application.events import BirthdayGreetingEvent
from src.core.constants import (
    BIRTHDATE_REQUEST_DELAY,
    BIRTHDATE_SYNC_BATCH_SIZE,
    BIRTHDATE_SYNC_INTERVAL_DAYS,
    BIRTHDAY_GIFT_DAYS,
)
from src.core.enums import BirthdayGift, SubscriptionStatus
from src.core.utils.time import datetime_now


def birthday_dates(today: date) -> list[tuple[int, int]]:
    """(day, month) pairs celebrated today. Feb 29 birthdays move to Feb 28 in common years."""
    dates = [(today.day, today.month)]
    if today.month == 2 and today.day == 28:
        try:
            date(today.year, 2, 29)
        except ValueError:
            dates.append((29, 2))
    return dates


@dataclass(frozen=True)
class _FetchResult:
    ok: bool  # False: transient failure, keep the cached value
    birthdate: Optional[BirthdateDto] = None


async def _fetch_birthdate(bot_service: BotService, user: UserDto) -> _FetchResult:
    """Birthdate from the user's Telegram profile, retrying once after flood control."""
    if user.telegram_id is None:
        return _FetchResult(ok=True)
    for _ in range(2):
        try:
            return _FetchResult(
                ok=True,
                birthdate=await bot_service.get_birthdate(user.telegram_id, user.bot_id),
            )
        except TelegramRetryAfter as error:
            logger.warning(f"getChat flood control, sleeping '{error.retry_after}'s")
            await asyncio.sleep(error.retry_after)
        except TelegramAPIError as error:
            # Chat not found / bot blocked / deactivated: nothing to read for this user.
            logger.debug(f"{user.log} Birthdate unavailable: '{error}'")
            return _FetchResult(ok=True)
        except Exception as error:
            logger.warning(f"{user.log} Failed to fetch birthdate: '{error}'")
            return _FetchResult(ok=False)
    return _FetchResult(ok=False)


class SyncUserBirthdates(Interactor[None, int]):
    required_permission = None

    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        settings_dao: SettingsDao,
        bot_service: BotService,
    ) -> None:
        self.uow = uow
        self.user_dao = user_dao
        self.settings_dao = settings_dao
        self.bot_service = bot_service

    async def _execute(self, actor: UserDto, data: None) -> int:
        settings = await self.settings_dao.get()
        if not settings.extra.birthday_greeting:
            logger.debug("Birthday greetings are disabled, skipping birthdate sync")
            return 0

        now = datetime_now()
        stale_before = now - timedelta(days=BIRTHDATE_SYNC_INTERVAL_DAYS)

        async with self.uow:
            users = await self.user_dao.get_birthdate_sync_batch(
                stale_before=stale_before,
                limit=BIRTHDATE_SYNC_BATCH_SIZE,
            )

        if not users:
            logger.debug("No users need a birthdate sync")
            return 0

        synced = 0
        found = 0
        for user in users:
            result = await _fetch_birthdate(self.bot_service, user)
            if result.ok:
                await self._store(user, result.birthdate, datetime_now())
                synced += 1
                found += result.birthdate is not None
            await asyncio.sleep(BIRTHDATE_REQUEST_DELAY)

        logger.info(
            f"Birthdate sync: '{synced}'/'{len(users)}' users synced, '{found}' with a birthdate"
        )
        return synced

    async def _store(
        self, user: UserDto, birthdate: Optional[BirthdateDto], synced_at: datetime
    ) -> None:
        async with self.uow:
            await self.user_dao.set_birthdate(
                user_id=user.id,
                day=birthdate.day if birthdate else None,
                month=birthdate.month if birthdate else None,
                synced_at=synced_at,
            )
            await self.uow.commit()


class CongratulateBirthdayUsers(Interactor[None, int]):
    required_permission = None

    def __init__(
        self,
        uow: UnitOfWork,
        user_dao: UserDao,
        subscription_dao: SubscriptionDao,
        settings_dao: SettingsDao,
        remnawave: Remnawave,
        bot_service: BotService,
        event_publisher: EventPublisher,
    ) -> None:
        self.uow = uow
        self.user_dao = user_dao
        self.subscription_dao = subscription_dao
        self.settings_dao = settings_dao
        self.remnawave = remnawave
        self.bot_service = bot_service
        self.event_publisher = event_publisher

    async def _execute(self, actor: UserDto, data: None) -> int:
        settings = await self.settings_dao.get()
        if not settings.extra.birthday_greeting:
            logger.info("Birthday greetings are disabled, skipping")
            return 0

        today = datetime_now().date()
        dates = birthday_dates(today)

        async with self.uow:
            users = await self.user_dao.get_birthday_users(dates, today.year)

        if not users:
            logger.debug(f"No birthdays on '{today}'")
            return 0

        logger.info(f"Found '{len(users)}' birthday candidates on '{today}'")

        congratulated = 0
        for user in users:
            try:
                if await self._congratulate(user, dates, today.year):
                    congratulated += 1
            except Exception:
                logger.exception(f"{user.log} Failed to congratulate on birthday")
            await asyncio.sleep(BIRTHDATE_REQUEST_DELAY)

        logger.info(f"Birthday greetings sent to '{congratulated}'/'{len(users)}' users")
        return congratulated

    async def _congratulate(self, user: UserDto, dates: list[tuple[int, int]], year: int) -> bool:
        # The cache may be up to a week old: confirm the birthday is still set and still today.
        result = await _fetch_birthdate(self.bot_service, user)
        if not result.ok:
            logger.warning(f"{user.log} Could not confirm birthdate, skipping for now")
            return False

        birthdate = result.birthdate
        if birthdate is None or (birthdate.day, birthdate.month) not in dates:
            logger.info(f"{user.log} Birthday is no longer today, updating cache")
            async with self.uow:
                await self.user_dao.set_birthdate(
                    user_id=user.id,
                    day=birthdate.day if birthdate else None,
                    month=birthdate.month if birthdate else None,
                    synced_at=datetime_now(),
                )
                await self.uow.commit()
            return False

        async with self.uow:
            claimed = await self.user_dao.claim_birthday_gift(user.id, year)
            await self.uow.commit()

        if not claimed:
            logger.info(f"{user.log} Birthday gift for '{year}' already granted")
            return False

        try:
            gift = await self._grant_gift(user)
        except Exception:
            # Undo the claim so a re-run can retry the grant.
            async with self.uow:
                await self.user_dao.release_birthday_gift(user.id, year)
                await self.uow.commit()
            raise

        await self.event_publisher.publish(
            BirthdayGreetingEvent(
                user=user,
                gift=gift,
                days=BIRTHDAY_GIFT_DAYS if gift == BirthdayGift.DAYS else 0,
            )
        )
        logger.info(f"{user.log} Birthday greeting sent (gift '{gift}')")
        return True

    async def _grant_gift(self, user: UserDto) -> BirthdayGift:
        async with self.uow:
            subscription = await self.subscription_dao.get_current(user.id)

            if not subscription or subscription.status == SubscriptionStatus.DELETED:
                return BirthdayGift.NONE

            if subscription.is_unlimited:
                return BirthdayGift.UNLIMITED

            # An expired subscription is extended from now, so the gift is actually usable.
            base = max(subscription.expire_at, datetime_now())
            subscription.expire_at = base + timedelta(days=BIRTHDAY_GIFT_DAYS)
            if subscription.status == SubscriptionStatus.EXPIRED:
                subscription.status = SubscriptionStatus.ACTIVE

            await self.remnawave.update_user(
                user=user,
                num_id=subscription.user_remna_num_id,
                subscription=subscription,
            )
            await self.subscription_dao.update(subscription)
            await self.uow.commit()

        logger.info(
            f"{user.log} Added '{BIRTHDAY_GIFT_DAYS}' birthday days, "
            f"new expire '{subscription.expire_at}'"
        )
        return BirthdayGift.DAYS
