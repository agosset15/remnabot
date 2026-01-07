from __future__ import annotations

from typing import Optional, Sequence, cast

from adaptix import Retort
from adaptix.conversion import ConversionRetort
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy import ColumnElement, and_, any_, case, delete, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.application.common.dao import PlanDao
from src.application.dto import PlanDto
from src.core.enums import PlanAvailability
from src.infrastructure.database.models import Plan, PlanDuration


class PlanDaoImpl(PlanDao):
    def __init__(
        self,
        session: AsyncSession,
        retort: Retort,
        conversion_retort: ConversionRetort,
        redis: Redis,
    ) -> None:
        self.session = session
        self.retort = retort
        self.conversion_retort = conversion_retort
        self.redis = redis

        self._convert_to_dto = self.conversion_retort.get_converter(Plan, PlanDto)
        self._convert_to_dto_list = self.conversion_retort.get_converter(list[Plan], list[PlanDto])

    async def create(self, plan: PlanDto) -> PlanDto:
        plan_data = self.retort.dump(plan)
        db_plan = Plan(**plan_data)

        self.session.add(db_plan)
        await self.session.flush()

        logger.debug(f"New plan '{plan.name}' created with '{len(plan.durations)}' durations")
        return self._convert_to_dto(db_plan)

    async def get_by_id(self, plan_id: int) -> Optional[PlanDto]:
        stmt = (
            select(Plan)
            .where(Plan.id == plan_id)
            .options(selectinload(Plan.durations).selectinload(PlanDuration.prices))
        )
        db_plan = await self.session.scalar(stmt)

        if db_plan:
            logger.debug(f"Plan '{plan_id}' found")
            return self._convert_to_dto(db_plan)

        logger.debug(f"Plan '{plan_id}' not found")
        return None

    async def get_by_name(self, name: str) -> Optional[PlanDto]:
        stmt = (
            select(Plan)
            .where(Plan.name == name)
            .options(selectinload(Plan.durations).selectinload(PlanDuration.prices))
        )
        db_plan = await self.session.scalar(stmt)

        if db_plan:
            logger.debug(f"Plan with name '{name}' found")
            return self._convert_to_dto(db_plan)

        logger.debug(f"Plan with name '{name}' not found")
        return None

    async def get_available_for_user(
        self,
        telegram_id: int,
        availability: PlanAvailability = PlanAvailability.ALL,
    ) -> Sequence[PlanDto]:
        stmt = (
            select(Plan)
            .where(Plan.is_active == True)  # noqa: E712
            .where(Plan.availability == availability)
            .where(
                or_(
                    Plan.allowed_user_ids.any(telegram_id == Plan.allowed_user_ids.column_valued()),
                    func.cardinality(Plan.allowed_user_ids) == 0,
                )
            )
            .options(selectinload(Plan.durations).selectinload(PlanDuration.prices))
            .order_by(Plan.order_index.asc())
        )
        result = await self.session.scalars(stmt)
        db_plans = list(result.all())

        logger.debug(f"Retrieved '{len(db_plans)}' plans available for user '{telegram_id}'")
        return self._convert_to_dto_list(db_plans)

    async def get_trial_available_for_user(self, telegram_id: int) -> Optional[PlanDto]:
        user_is_allowed = cast(ColumnElement[bool], telegram_id == any_(Plan.allowed_user_ids))
        priority = case(
            (
                and_(
                    Plan.availability == PlanAvailability.ALLOWED,
                    user_is_allowed,
                ),
                4,
            ),
            (
                Plan.availability == PlanAvailability.INVITED,
                3,
            ),
            (
                Plan.availability == PlanAvailability.NEW,
                2,
            ),
            (
                Plan.availability == PlanAvailability.ALL,
                1,
            ),
            else_=0,
        )

        stmt = (
            select(Plan)
            .where(Plan.is_active == True)  # noqa: E712
            .where(Plan.is_trial == True)  # noqa: E712
            .where(
                or_(
                    Plan.availability != PlanAvailability.ALLOWED,
                    user_is_allowed,
                )
            )
            .order_by(priority.desc(), Plan.order_index.asc())
            .limit(1)
            .options(selectinload(Plan.durations).selectinload(PlanDuration.prices))
        )

        db_plan = await self.session.scalar(stmt)

        if db_plan:
            logger.debug(f"Best trial plan '{db_plan.id}' selected for user '{telegram_id}'")
            return self._convert_to_dto(db_plan)

        logger.debug(f"No trial plan available for user '{telegram_id}'")
        return None

    async def get_all_active(self) -> Sequence[PlanDto]:
        stmt = (
            select(Plan)
            .where(Plan.is_active == True)  # noqa: E712
            .options(selectinload(Plan.durations).selectinload(PlanDuration.prices))
            .order_by(Plan.order_index.asc())
        )
        result = await self.session.scalars(stmt)
        db_plans = list(result.all())

        logger.debug(f"Retrieved '{len(db_plans)}' active plans")
        return self._convert_to_dto_list(db_plans)

    async def update_status(self, plan_id: int, is_active: bool) -> Optional[PlanDto]:
        stmt = update(Plan).where(Plan.id == plan_id).values(is_active=is_active).returning(Plan)
        db_plan = await self.session.scalar(stmt)

        if db_plan:
            logger.debug(f"Active status for plan '{plan_id}' set to '{is_active}'")
            return self._convert_to_dto(db_plan)

        logger.warning(f"Failed to update status for plan '{plan_id}': plan not found")
        return None

    async def delete(self, plan_id: int) -> bool:
        stmt = delete(Plan).where(Plan.id == plan_id).returning(Plan.id)
        result = await self.session.execute(stmt)
        deleted_id = result.scalar_one_or_none()

        if deleted_id:
            logger.debug(f"Plan '{plan_id}' and related data deleted")
            return True

        logger.debug(f"Plan '{plan_id}' not found for deletion")
        return False
