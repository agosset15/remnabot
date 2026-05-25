from pathlib import Path

from src.infrastructure.services.i18n import LayeredFileStorage


def write_ftl(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf8")


def test_default_key_is_resolved(tmp_path):
    write_ftl(tmp_path / "defaults/ru/messages.ftl", "msg-hello = Hello from default\n")
    write_ftl(tmp_path / "user/ru/custom.ftl", "# empty\n")

    storage = LayeredFileStorage(
        user_translations_dir=tmp_path / "user",
        default_translations_dir=tmp_path / "defaults",
    )
    storage.set_locales_map({"ru": ("ru",)})
    translators = list(storage.get_translators_for_language("ru"))

    assert any(t.get("msg-hello") == "Hello from default" for t in translators)


def test_custom_key_overrides_default(tmp_path):
    write_ftl(tmp_path / "defaults/ru/messages.ftl", "msg-hello = Hello from default\n")
    write_ftl(tmp_path / "user/ru/custom.ftl", "msg-hello = Custom hello\n")

    storage = LayeredFileStorage(
        user_translations_dir=tmp_path / "user",
        default_translations_dir=tmp_path / "defaults",
    )
    storage.set_locales_map({"ru": ("ru",)})
    translators = list(storage.get_translators_for_language("ru"))

    # custom translator comes first — its result must win
    assert translators[0].get("msg-hello") == "Custom hello"


def test_missing_custom_ftl_does_not_crash(tmp_path):
    write_ftl(tmp_path / "defaults/ru/messages.ftl", "msg-hello = Hello\n")
    # no user/ru/custom.ftl

    storage = LayeredFileStorage(
        user_translations_dir=tmp_path / "user",
        default_translations_dir=tmp_path / "defaults",
    )
    storage.set_locales_map({"ru": ("ru",)})
    translators = list(storage.get_translators_for_language("ru"))

    assert any(t.get("msg-hello") == "Hello" for t in translators)


def test_key_not_in_custom_falls_back_to_default(tmp_path):
    write_ftl(tmp_path / "defaults/ru/messages.ftl", "msg-new = New key\n")
    write_ftl(tmp_path / "user/ru/custom.ftl", "msg-old = Old custom\n")

    storage = LayeredFileStorage(
        user_translations_dir=tmp_path / "user",
        default_translations_dir=tmp_path / "defaults",
    )
    storage.set_locales_map({"ru": ("ru",)})
    translators = list(storage.get_translators_for_language("ru"))

    results = [t.get("msg-new") for t in translators]
    assert "New key" in results


def test_has_translator_for_root_locale(tmp_path):
    write_ftl(tmp_path / "defaults/ru/messages.ftl", "msg-x = X\n")
    write_ftl(tmp_path / "user/ru/custom.ftl", "# empty\n")

    storage = LayeredFileStorage(
        user_translations_dir=tmp_path / "user",
        default_translations_dir=tmp_path / "defaults",
    )
    assert storage.has_translator("ru")


def test_fallback_to_user_dir_when_defaults_missing(tmp_path):
    # local dev: assets.default/ does not exist
    write_ftl(tmp_path / "user/ru/messages.ftl", "msg-hello = Hello\n")
    write_ftl(tmp_path / "user/ru/custom.ftl", "# empty\n")

    storage = LayeredFileStorage(
        user_translations_dir=tmp_path / "user",
        default_translations_dir=tmp_path / "missing_defaults",
    )
    storage.set_locales_map({"ru": ("ru",)})
    translators = list(storage.get_translators_for_language("ru"))

    assert any(t.get("msg-hello") == "Hello" for t in translators)
