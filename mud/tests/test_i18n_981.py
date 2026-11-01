"""Legacy source storage tests under the single canonical Finglish policy (#996)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from nopunk_mud.i18n import (
    DEFAULT_LOCALE,
    FALLBACK_LOCALE,
    I18nError,
    Translator,
    load_catalogue,
    pending_finnish,
    validate_catalogue,
)

LOCALE_DIR = Path(__file__).resolve().parents[1] / "nopunk_mud" / "locale"


def test_the_shipped_catalogues_load_and_are_valid() -> None:
    catalogues = {loc: load_catalogue(loc) for loc in ("fi", "en")}
    assert catalogues["en"], "the English working text must exist"
    assert validate_catalogue(catalogues) == [], "the shipped catalogues must satisfy the contract"


def test_historical_finnish_backlog_is_retired() -> None:
    catalogues = {loc: load_catalogue(loc) for loc in ("fi", "en")}
    pending = pending_finnish(catalogues)
    assert pending == [], "canonical Finglish never requires a separate Finnish translation"


def test_canonical_resolver_uses_original_source_without_translation_backlog() -> None:
    translator = Translator(DEFAULT_LOCALE)
    assert translator.text("ui.prompt.default") == "What do you do?"
    assert translator.missing == []
    assert translator.has("ui.prompt.default") is True


def test_a_known_key_in_the_players_locale_does_not_record_a_gap(tmp_path) -> None:
    (tmp_path / "en.json").write_text(json.dumps({"a.key": "English"}), encoding="utf-8")
    (tmp_path / "fi.json").write_text(json.dumps({"a.key": "Suomi"}), encoding="utf-8")
    translator = Translator(DEFAULT_LOCALE, directory=tmp_path)
    assert translator.text("a.key") == "Suomi"
    assert translator.missing == []


def test_an_unknown_key_raises_rather_than_showing_a_blank() -> None:
    translator = Translator(DEFAULT_LOCALE)
    with pytest.raises(I18nError):
        translator.text("nope.not_a_key")
    with pytest.raises(I18nError):
        translator.text("malformed")


def test_fields_are_interpolated() -> None:
    translator = Translator(DEFAULT_LOCALE)
    assert translator.text("combat.attack.hit", actor="A", target="B", damage=9) == "A hits B for 9 damage."


def test_trauma_and_shock_have_player_facing_strings() -> None:
    translator = Translator(DEFAULT_LOCALE)
    assert "multiplied" in translator.text("combat.trauma", rating=3)
    assert "shock" in translator.text("combat.shock", target="B", shock=2)


def test_historical_catalogues_are_not_mandatory_distinct_localizations() -> None:
    assert validate_catalogue({"en": {"a.key": "Same"}, "fi": {"a.key": "Same"}}) == []


def test_a_malformed_key_or_empty_string_is_rejected(tmp_path) -> None:
    (tmp_path / "fi.json").write_text(json.dumps({}), encoding="utf-8")
    (tmp_path / "en.json").write_text(json.dumps({"Bad Key": "x"}), encoding="utf-8")
    with pytest.raises(I18nError, match="invalid key"):
        load_catalogue("en", directory=tmp_path)
    (tmp_path / "en.json").write_text(json.dumps({"a.key": "   "}), encoding="utf-8")
    with pytest.raises(I18nError, match="invalid content"):
        load_catalogue("en", directory=tmp_path)
    with pytest.raises(I18nError, match="unknown historical catalogue"):
        load_catalogue("de")


def test_catalogue_round_trips_non_ascii_encoding(tmp_path) -> None:
    (tmp_path / "en.json").write_text(json.dumps({"a.key": "Helsinki: ä ö å"}), encoding="utf-8")
    (tmp_path / "fi.json").write_text(json.dumps({}), encoding="utf-8")
    assert load_catalogue("en", directory=tmp_path)["a.key"] == "Helsinki: ä ö å"


def test_the_module_contains_no_translation_machinery() -> None:
    """No machine translation, no LLM, no network: the policy is that agents do not translate Finnish."""
    source = (Path(__file__).resolve().parents[1] / "nopunk_mud" / "i18n.py").read_text(encoding="utf-8")
    for forbidden in ("requests", "httpx", "openai", "ollama", "translate(", "googletrans"):
        assert forbidden not in source, f"{forbidden} has no place in the content contract"
