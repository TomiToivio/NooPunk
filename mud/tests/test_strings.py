"""The language contract is executable, not advisory (#980, #981).

These tests exist because "agents must never write Finnish" is the kind of rule that decays into a comment
nobody reads. Each one pins a way the contract could be broken.
"""
import json

import pytest
from nopunk_mud import strings


def _catalogue() -> strings.StringCatalogue:
    catalogue = strings.StringCatalogue()
    catalogue.define("scene.helsinki.street", "The tram grinds past the steissi.")
    return catalogue


class TestAgentNeverWritesFinnish:
    def test_an_english_placeholder_carrying_finnish_is_refused(self) -> None:
        catalogue = strings.StringCatalogue()
        with pytest.raises(strings.StringError):
            catalogue.add(strings.StringEntry(
                key="scene.bad", en="working text", fi="Älä kirjoita suomea",
                status=strings.ENGLISH_PLACEHOLDER))

    def test_the_refusal_names_the_rule(self) -> None:
        catalogue = strings.StringCatalogue()
        with pytest.raises(strings.StringError, match="must not contain Finnish"):
            catalogue.add(strings.StringEntry(key="scene.bad", en="x", fi="kyllä"))

    def test_finnish_may_only_arrive_through_the_tomi_path(self) -> None:
        catalogue = _catalogue()
        entry = catalogue.finish("scene.helsinki.street", "Ratikka rämisee steissin ohi.")
        assert entry.status == strings.TOMI_FINNISH
        assert entry.fi.startswith("Ratikka")

    def test_a_tomi_string_without_finnish_is_refused(self) -> None:
        catalogue = strings.StringCatalogue()
        with pytest.raises(strings.StringError):
            catalogue.add(strings.StringEntry(key="scene.empty", en="x", status=strings.TOMI_FINNISH))


class TestMixedBuildsAreVisible:
    def test_finnish_is_preferred_when_it_exists(self) -> None:
        catalogue = _catalogue()
        catalogue.finish("scene.helsinki.street", "Ratikka rämisee steissin ohi.")
        shown = catalogue.resolve("scene.helsinki.street", "fi")
        assert shown.text.startswith("Ratikka")
        assert shown.fell_back is False

    def test_english_is_shown_and_flagged_before_tomi_writes(self) -> None:
        shown = _catalogue().resolve("scene.helsinki.street", "fi")
        assert shown.fell_back is True
        assert shown.text.startswith("The tram")

    def test_the_work_queue_lists_what_tomi_owes(self) -> None:
        catalogue = _catalogue()
        catalogue.define("scene.two", "Second line")
        catalogue.finish("scene.two", "Toinen rivi")
        assert catalogue.pending_finnish() == ["scene.helsinki.street"]

    def test_coverage_counts_the_mix(self) -> None:
        catalogue = _catalogue()
        catalogue.define("scene.two", "Second line")
        catalogue.finish("scene.two", "Toinen rivi")
        assert catalogue.coverage() == {"total": 2, "finnish_written": 1,
                                        "awaiting_tomi": 1, "percent_finnish": 50.0}


class TestFallbackNeverOverwritesFinnish:
    def test_showing_english_leaves_the_finnish_intact(self) -> None:
        catalogue = _catalogue()
        catalogue.finish("scene.helsinki.street", "Ratikka rämisee.")
        catalogue.resolve("scene.helsinki.street", "fi")   # falls back? no - Finnish exists
        assert catalogue.entry("scene.helsinki.street").fi == "Ratikka rämisee."

    def test_a_missing_finnish_is_not_backfilled_from_english(self) -> None:
        catalogue = _catalogue()
        shown = catalogue.resolve("scene.helsinki.street", "fi")
        assert shown.fell_back is True
        assert catalogue.entry("scene.helsinki.street").fi == ""

    def test_an_english_placeholder_is_never_promoted_to_finnish(self) -> None:
        catalogue = _catalogue()
        catalogue.resolve("scene.helsinki.street", "fi")
        assert catalogue.entry("scene.helsinki.street").status == strings.ENGLISH_PLACEHOLDER


class TestKeysSurviveLocalization:
    def test_keys_are_language_neutral(self) -> None:
        catalogue = strings.StringCatalogue()
        with pytest.raises(strings.StringError):
            catalogue.define("scene.Älä", "no")

    def test_a_key_is_unique(self) -> None:
        catalogue = _catalogue()
        with pytest.raises(strings.StringError):
            catalogue.define("scene.helsinki.street", "again")

    def test_an_unknown_key_is_an_error_not_an_empty_string(self) -> None:
        with pytest.raises(strings.StringError):
            _catalogue().resolve("scene.nope", "fi")

    def test_an_unsupported_locale_is_refused(self) -> None:
        with pytest.raises(strings.StringError):
            _catalogue().resolve("scene.helsinki.street", "sv")


class TestUtf8:
    def test_finnish_letters_survive_a_round_trip(self, tmp_path) -> None:
        catalogue = _catalogue()
        catalogue.finish("scene.helsinki.street", "Ääniä, öitä, šokki, žanri.")
        path = tmp_path / "strings.json"
        catalogue.save(path)
        reloaded = strings.StringCatalogue.load(path)
        assert reloaded.entry("scene.helsinki.street").fi == "Ääniä, öitä, šokki, žanri."

    def test_json_is_written_as_utf8_not_escaped(self) -> None:
        catalogue = _catalogue()
        catalogue.finish("scene.helsinki.street", "Ääniä")
        text = catalogue.to_json()
        assert "Ääniä" in text
        assert "\\u00c4" not in text

    def test_a_save_keeps_status_and_queue_across_a_reload(self, tmp_path) -> None:
        catalogue = _catalogue()
        catalogue.define("scene.two", "Second line")
        path = tmp_path / "strings.json"
        catalogue.save(path)
        reloaded = strings.StringCatalogue.load(path)
        assert reloaded.pending_finnish() == ["scene.helsinki.street", "scene.two"]
        assert json.loads(path.read_text(encoding="utf-8"))["format"] == "nopunk-strings-v1"
