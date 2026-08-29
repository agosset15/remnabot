"""add subscriptions.user_remna_num_id and backfill it from the panel by uuid

Adds the numeric Remnawave user id (`user.id`) alongside the existing
`user_remna_id` (UUID). The old remnapy (v2.7) client is still pinned, and the
panel returns both `id` and `uuid`, so this migration resolves every existing
subscription by its UUID against the live panel and stores the numeric id.

The column stays nullable here: this is only the data migration. Switching the
application code to the numeric identity (and enforcing NOT NULL / dropping the
UUID column) is a separate branch.

If the panel is unreachable at migrate time, individual lookups are skipped and
their rows are left NULL. To re-run the backfill after fixing connectivity:
`alembic downgrade -1 && alembic upgrade head`.
"""

import asyncio
import threading
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import context, op
from loguru import logger

revision: str = "0041"
down_revision: Union[str, None] = "0040"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


async def _fetch_panel_ids_async(uuids: list[str]) -> dict[str, int]:
    """Resolve {uuid: numeric id} by querying the Remnawave panel per user."""
    from httpx import AsyncClient, Timeout
    from remnapy import RemnawaveSDK
    from remnapy.exceptions import NotFoundError

    from src.core.config import AppConfig

    config = AppConfig.get().remnawave

    headers = {
        "Authorization": f"Bearer {config.token.get_secret_value()}",
        "X-Api-Key": config.caddy_token.get_secret_value(),
        "CF-Access-Client-Id": config.cf_client_id.get_secret_value(),
        "CF-Access-Client-Secret": config.cf_client_secret.get_secret_value(),
    }
    if not config.is_external:
        headers["x-forwarded-proto"] = "https"
        headers["x-forwarded-for"] = "127.0.0.1"

    mapping: dict[str, int] = {}
    client = AsyncClient(
        base_url=f"{config.url.get_secret_value()}/api",
        headers=headers,
        cookies=config.cookies,
        verify=True,
        timeout=Timeout(connect=15.0, read=25.0, write=10.0, pool=5.0),
    )
    try:
        sdk = RemnawaveSDK(client)
        for user_uuid in uuids:
            try:
                remna_user = await sdk.users.get_user_by_uuid(user_uuid)  # type: ignore[attr-defined]
            except NotFoundError:
                logger.warning(
                    f"[0041] user '{user_uuid}' not found on panel; leaving num id NULL"
                )
                continue
            except Exception as exc:  # noqa: BLE001
                logger.error(f"[0041] failed to fetch user '{user_uuid}': {exc}")
                continue
            mapping[str(user_uuid)] = remna_user.id
    finally:
        await client.aclose()

    return mapping


def _fetch_panel_ids(uuids: list[str]) -> dict[str, int]:
    """Drive the async panel lookup from Alembic's synchronous context.

    The migration already runs inside a live event loop (env.py drives it via
    ``asyncio.run``), so the async SDK is executed on a dedicated thread with its
    own loop to avoid nesting.
    """
    result: dict[str, object] = {}

    def runner() -> None:
        try:
            result["value"] = asyncio.run(_fetch_panel_ids_async(uuids))
        except BaseException as exc:  # noqa: BLE001
            result["error"] = exc

    thread = threading.Thread(target=runner, name="remna-num-id-backfill")
    thread.start()
    thread.join()

    if "error" in result:
        raise result["error"]  # type: ignore[misc]
    return result["value"]  # type: ignore[return-value]


def upgrade() -> None:
    op.add_column(
        "subscriptions",
        sa.Column("user_remna_num_id", sa.BigInteger(), nullable=True),
    )
    op.create_index(
        "ix_subscriptions_user_remna_num_id",
        "subscriptions",
        ["user_remna_num_id"],
        unique=False,
    )

    # Offline mode only emits DDL; there is no live connection to backfill.
    if context.is_offline_mode():
        logger.info("[0041] offline mode: skipping panel backfill")
        return

    bind = op.get_bind()
    rows = bind.execute(
        sa.text(
            "SELECT id, user_remna_id FROM subscriptions "
            "WHERE user_remna_id IS NOT NULL AND user_remna_num_id IS NULL"
        )
    ).fetchall()

    if not rows:
        logger.info("[0041] no subscriptions to backfill")
        return

    uuids = [str(row[1]) for row in rows]
    logger.info(f"[0041] backfilling numeric remna id for {len(uuids)} subscription(s)")

    panel_ids = _fetch_panel_ids(uuids)

    updated = 0
    for row in rows:
        sub_id, user_uuid = row[0], str(row[1])
        num_id = panel_ids.get(user_uuid)
        if num_id is None:
            continue
        bind.execute(
            sa.text(
                "UPDATE subscriptions SET user_remna_num_id = :num_id WHERE id = :sub_id"
            ),
            {"num_id": num_id, "sub_id": sub_id},
        )
        updated += 1

    left_null = len(uuids) - updated
    logger.info(
        f"[0041] backfill done: {updated}/{len(uuids)} updated, "
        f"{left_null} left NULL (not found / unreachable)"
    )
    if left_null:
        logger.warning(
            "[0041] some rows were left NULL; after fixing panel connectivity re-run with "
            "`alembic downgrade -1 && alembic upgrade head`"
        )


def downgrade() -> None:
    op.drop_index("ix_subscriptions_user_remna_num_id", table_name="subscriptions")
    op.drop_column("subscriptions", "user_remna_num_id")
