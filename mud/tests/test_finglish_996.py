"""Canonical Finglish, historical catalogue compatibility and spoiler-safe dictionary."""
from __future__ import annotations
from nopunk_mud.i18n import Translator, pending_finnish
from nopunk_mud.lexicon import lookup, PUBLIC_TERMS

def test_historical_locale_does_not_change_canonical_output(tmp_path):
    (tmp_path / "fi.json").write_text('{"ui.greet": "Tomi original äö"}', encoding="utf-8")
    (tmp_path / "en.json").write_text('{"ui.greet": "Hello", "ui.other": "Moi, agent."}', encoding="utf-8")
    assert Translator("en", directory=tmp_path).text("ui.greet") == "Tomi original äö"
    assert Translator("fi", directory=tmp_path).text("ui.greet") == "Tomi original äö"
    assert Translator(directory=tmp_path).text("ui.other") == "Moi, agent."
    assert pending_finnish({"en": {"ui.other": "x"}, "fi": {}}) == []

def test_public_dictionary_is_searchable_and_spoiler_safe():
    # Tomi's GLOSSARY.md headword is "Wallah"; the earlier hand-coded list had "Wallah!" (#1000).
    assert "Wallah" in lookup()
    assert "I swear!" in lookup("Mä vannon!")
    assert "Stadi:" in lookup("Stadi")
    assert "No public dictionary entry" in lookup("unpublished")
    public = " ".join(t.word + " " + t.meaning for t in PUBLIC_TERMS).casefold()
    for spoiler in ("noösphere", "pleiadian", "zookeeper", "classified", "psychotronic"):
        assert spoiler not in public
