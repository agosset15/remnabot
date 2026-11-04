from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from aiogram.enums import ContentType
from aiogram.types import Chat, FSInputFile, Message, PhotoSize, RichBlockPhoto, RichMessage
from aiogram_dialog.api.entities import MediaAttachment, OldMessage

from src.telegram import message_manager as mm
from src.telegram.window import NewMessageWithEffect

VOID_TAGS = {"br", "hr", "img"}


class _TagBalance(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: Any) -> None:
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: Any) -> None:
        pass

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unexpected </{tag}>, open: {self.stack}")
        else:
            self.stack.pop()


def _menu_data(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "telegram_id": 123456789,
        "email": "user@example.com",
        "pending_email": False,
        "has_pending_email": False,
        "email_state": "verified",
        "web_cabinet_url": 0,
        "name": "Alex",
        "personal_discount": 0,
        "show_personal_discount": False,
        "purchase_discount": 0,
        "show_purchase_discount": False,
        "is_trial": False,
        "status": "ACTIVE",
        "traffic_limit": "100 GB",
        "device_limit": "3",
        "expire_time": "29 days",
        "expire_unix": 1_900_000_000,
        "reset_time": "2 days",
        "traffic_strategy": "NO_RESET",
        "trial_available": False,
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize(
    "overrides",
    [
        {},
        {"expire_unix": 0},
        {"status": "EXPIRED", "is_trial": True},
        {"status": "LIMITED", "traffic_strategy": "RESET"},
        {"status": "DISABLED"},
        {"status": None, "trial_available": True, "email_state": "missing", "email": False},
        {"email_state": "unverified", "has_pending_email": True, "pending_email": "n@e.com"},
        {"show_personal_discount": True, "personal_discount": 15},
    ],
)
def test_main_menu_rich_renders_balanced_html(ru, overrides: dict[str, Any]) -> None:
    text = ru.get("msg-main-menu-rich", **_menu_data(**overrides))

    assert "!empty!" not in text
    parser = _TagBalance()
    parser.feed(text)
    assert not parser.errors, parser.errors
    assert not parser.stack, parser.stack


def test_main_menu_rich_active_shows_expiry_time(ru) -> None:
    text = ru.get("msg-main-menu-rich", **_menu_data())

    assert '<tg-time unix="1900000000" format="D">' in text
    assert "<code>123456789</code>" in text


def test_main_menu_rich_unlimited_hides_expiry_row(ru) -> None:
    text = ru.get("msg-main-menu-rich", **_menu_data(expire_unix=0))

    assert "<tg-time" not in text


def _new_message(media: MediaAttachment | None, *, is_rich: bool = True) -> NewMessageWithEffect:
    return NewMessageWithEffect(
        chat=Chat(id=1, type="private"),
        text="<p>hi</p>",
        is_rich=is_rich,
        rich_media=media,
    )


def _old_message(content_type: ContentType) -> OldMessage:
    return OldMessage(
        chat=Chat(id=1, type="private"),
        message_id=10,
        media_id=None,
        media_uniq_id=None,
        content_type=content_type,
    )


async def test_build_rich_message_embeds_banner_and_reuses_file_id(tmp_path: Path) -> None:
    mm._rich_media_cache.clear()
    banner = tmp_path / "menu.jpg"
    banner.write_bytes(b"jpg")
    media = MediaAttachment(type=ContentType.PHOTO, path=banner)
    manager = mm.MessageManager()
    bot = SimpleNamespace()

    first = await manager._build_rich_message(bot, _new_message(media))  # type: ignore[arg-type]
    assert first.html == '<img src="tg://photo?id=banner"/><p>hi</p>'
    assert first.media is not None
    assert isinstance(first.media[0].media.media, FSInputFile)

    sent = Message.model_construct(
        rich_message=RichMessage(
            blocks=[
                RichBlockPhoto(
                    photo=[PhotoSize(file_id="FILE", file_unique_id="U", width=1, height=1)]
                )
            ]
        )
    )
    manager._remember_rich_media(_new_message(media), sent)

    second = await manager._build_rich_message(bot, _new_message(media))  # type: ignore[arg-type]
    assert second.media is not None
    assert second.media[0].media.media == "FILE"
    mm._rich_media_cache.clear()


async def test_build_rich_message_without_banner() -> None:
    rich = await mm.MessageManager()._build_rich_message(
        SimpleNamespace(),  # type: ignore[arg-type]
        _new_message(None),
    )
    assert rich.html == "<p>hi</p>"
    assert rich.media is None


@pytest.mark.parametrize(
    ("old_type", "new_is_rich", "expected"),
    [
        (ContentType.RICH_MESSAGE, True, True),
        (ContentType.TEXT, True, False),
        (ContentType.RICH_MESSAGE, False, False),
        (ContentType.TEXT, False, True),
    ],
)
def test_can_edit_only_within_same_kind(
    old_type: ContentType, new_is_rich: bool, expected: bool
) -> None:
    manager = mm.MessageManager()
    new_message = _new_message(None, is_rich=new_is_rich)

    assert manager._can_edit(new_message, _old_message(old_type)) is expected
