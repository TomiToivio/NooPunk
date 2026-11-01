"""Language policy enforcement (#980/#981): Finnish-first, agents English-only."""
from __future__ import annotations

import pytest

from nopunk_mud.localization import Entry, Localization, LocalizationError


def test_finnish_missing_falls_back_visibly():
    loc = Localization()
    loc.add_english("hq.greeting", "Welcome to UNSA Helsinki.")
    rendered = loc.render("hq.greeting")
    assert rendered.fallback
    assert rendered.text == "[EN] Welcome to UNSA Helsinki."
    assert rendered.locale == "en"


def test_tomi_finnish_is_rendered_verbatim():
    loc = Localization()
    loc.add_english("hq.greeting", "Welcome to UNSA Helsinki.")
    loc.set_finnish("hq.greeting", "Tervetuloa UNSA Helsinkiin, kundi.", author="tomi")
    rendered = loc.render("hq.greeting")
    assert not rendered.fallback
    assert rendered.text == "Tervetuloa UNSA Helsinkiin, kundi."


def test_an_agent_may_not_author_finnish():
    loc = Localization()
    loc.add_english("hq.greeting", "Welcome.")
    with pytest.raises(LocalizationError):
        loc.set_finnish("hq.greeting", "Tervetuloa.", author="agent")


def test_english_cannot_overwrite_finnish():
    loc = Localization()
    loc.set_finnish("k", "Minä olen Tony.", author="tomi")
    loc.add_english("k", "I am Tony.")
    assert loc.render("k").text == "Minä olen Tony."
    assert loc.render("k", "en").text == "I am Tony."


def test_utf8_round_trip_preserves_finnish():
    loc = Localization()
    loc.set_finnish("k", "Ääniä öisessä kaupungissa: å, ä, ö.", author="tomi")
    again = Localization.from_json(loc.to_json())
    assert again.render("k").text == "Ääniä öisessä kaupungissa: å, ä, ö."


def test_loaded_finnish_must_be_tomi_authored():
    with pytest.raises(LocalizationError):
        Localization.from_json('{"k": {"en": "x", "fi": "x", "author_fi": "agent"}}')


def test_unknown_key_and_missing_english_are_errors():
    loc = Localization()
    with pytest.raises(LocalizationError):
        loc.render("missing")
    loc.set_finnish("fi_only", "Vain suomeksi.", author="tomi")
    with pytest.raises(LocalizationError):
        loc.render("fi_only", "en")


def test_entry_status_tracks_awaiting_tomi():
    loc = Localization()
    entry = loc.add_english("k", "placeholder")
    assert entry.status == "english_placeholder"
    assert loc.set_finnish("k", "valmis", author="tomi").status == "tomi_finnish"
