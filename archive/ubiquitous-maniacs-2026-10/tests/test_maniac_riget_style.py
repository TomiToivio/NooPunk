"""Tests for Maniac/Riget stylistic features in play.py.

Tests verify:
1. COSMIC_OPENING exists with Maniac-style hypothesis/corollary structure
2. INSTITUTIONAL_OPENING exists and is shown at startup
3. UFAB_ADS list exists and contains Noöpunk's own diegetic advertisements
4. RAGNAROK_COMMENTS list exists and contains meta-commentary
5. play_game shows both openings at startup
6. render_scene can show UFAB ads and Ragnarök comments
7. Ads use Noöpunk's own brands, not Maniac's source-specific brands
8. Ad/comment rendering is deterministic (same seed + turn = same output)
"""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import patch

from src.game import GameState

ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"


def make_state(seed: int = 42) -> GameState:
    state = GameState.from_files(CHARACTER, SCENARIO, seed=seed)
    state.start()
    return state


# ── Constant existence tests ────────────────────────────────────


def test_institutional_opening_exists():
    """INSTITUTIONAL_OPENING on olemassa ja sisältää Noöpunkin oman äänen."""
    import play
    assert hasattr(play, "INSTITUTIONAL_OPENING")
    assert "16 Psyche" in play.INSTITUTIONAL_OPENING
    assert "C.G. Jung City" in play.INSTITUTIONAL_OPENING
    assert "vertikaaliseksi integraatioksi" in play.INSTITUTIONAL_OPENING


def test_cosmic_opening_exists():
    """COSMIC_OPENING on olemassa ja ei-tyhjä."""
    import play
    assert hasattr(play, "COSMIC_OPENING")
    assert len(play.COSMIC_OPENING) > 100


def test_cosmic_opening_has_hypothesis_corollary():
    """Kosminen kertoja käyttää Maniacin Hypothesis/Corollary-rakennetta."""
    import play
    text = play.COSMIC_OPENING
    assert "HYPOTEESI" in text
    assert "KOROLLAARI" in text


def test_cosmic_opening_mentions_16_psyche():
    """Kertoja mainitsee pelin sijainnin (16 Psyche)."""
    import play
    assert "16 Psyche" in play.COSMIC_OPENING
    assert "C.G. Jung" in play.COSMIC_OPENING


def test_ufab_ads_exist():
    """UFAB_ADS-lista on olemassa ja sisältää mainoksia."""
    import play
    assert hasattr(play, "UFAB_ADS")
    assert len(play.UFAB_ADS) >= 5


def test_ufab_ads_use_noopunk_brands():
    """Mainokset käyttävät Noöpunkin omia brändejä, eivät Maniacin brändejä."""
    import play
    ads_text = " ".join(play.UFAB_ADS)
    assert "UFAB" in ads_text
    # Noöpunkin omat brändät
    assert "UFAB Buddy" in ads_text or "Proxy Ystävä" in ads_text
    assert "Puhdas Menneisyys" in ads_text or "Toiveiden Rekisteri" in ads_text
    # Ei Maniacin brändejä
    for borrowed in ("AdBuddy", "Friend Proxy", "Milgrim Industries", "DOX STOP"):
        assert borrowed not in ads_text, f"Maniac-brand '{borrowed}' should not be in UFAB_ADS"


def test_ragnarok_comments_exist():
    """RAGNAROK_COMMENTS-lista on olemassa ja sisältaa kommentteja."""
    import play
    assert hasattr(play, "RAGNAROK_COMMENTS")
    assert len(play.RAGNAROK_COMMENTS) >= 5


def test_ragnarok_comments_contain_meta_commentary():
    """Ragnarökin kommentaarit ovat meta-tason kommentteja."""
    import play
    comments_text = " ".join(play.RAGNAROK_COMMENTS)
    assert "Ragnarök" in comments_text
    assert "Suomalainen" in comments_text or "suomalainen" in comments_text


# ── play_game integration tests ────────────────────────────────


def test_play_game_shows_both_openings():
    """play_game näyttää sekä INSTITUTIONAL_OPENINGin että COSMIC_OPENINGin."""
    import play

    state = make_state(seed=42)
    with patch("builtins.input", side_effect=["quit"]), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.play_game(state)
    output = fake_out.getvalue()
    assert "N Ö Ö P U N K" in output  # BANNER
    assert "vertikaaliseksi integraatioksi" in output  # INSTITUTIONAL_OPENING
    assert "HYPOTEESI" in output  # COSMIC_OPENING
    assert "Olet Sven-Olof" in output  # Perinteinen avaus


# ── render_scene ad/comment tests ──────────────────────────────


def test_render_scene_can_show_ufab_ad():
    """render_scene voi näyttää UFAB-mainoksen kun RNG osuu oikein."""
    import play

    found_ad = False
    for seed_val in range(100):
        state = make_state(seed=seed_val)
        state.perform_rpg_interaction("ask_android")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            play.render_scene(state)
        output = fake_out.getvalue()
        if "▌" in output:
            found_ad = True
            assert any(ad in output for ad in play.UFAB_ADS)
            break
    assert found_ad, "UFAB-mainos pitäisi näkyä jollakin siemenarvolla"


def test_render_scene_can_show_ragnarok_comment():
    """render_scene voi näyttää Ragnarök-kommentin kun RNG osuu oikein."""
    import play

    found_comment = False
    for seed_val in range(100):
        state = make_state(seed=seed_val)
        state.perform_rpg_interaction("ask_android")
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            play.render_scene(state)
        output = fake_out.getvalue()
        if "⟨Ragnarök⟩" in output:
            found_comment = True
            assert any(c in output for c in play.RAGNAROK_COMMENTS)
            break
    assert found_comment, "Ragnarök-kommentti pitäisi näkyä jollakin siemenarvolla"


def test_render_scene_ad_is_deterministic():
    """Sama siemen + turn tuottaa saman mainoksen / ei-mainoksen."""
    import play

    state1 = make_state(seed=42)
    state1.perform_rpg_interaction("ask_android")

    state2 = make_state(seed=42)
    state2.perform_rpg_interaction("ask_android")

    with patch("sys.stdout", new=io.StringIO()) as out1:
        play.render_scene(state1)
    with patch("sys.stdout", new=io.StringIO()) as out2:
        play.render_scene(state2)

    assert ("▌" in out1.getvalue()) == ("▌" in out2.getvalue())


def test_play_module_does_not_copy_source_specific_brands():
    """play.py ei suoraan kopioi Maniacin brändejä."""
    raw = (ROOT / "play.py").read_text(encoding="utf-8")
    for borrowed_brand in ("AdBuddy", "Friend Proxy", "Milgrim Industries", "DOX STOP"):
        assert borrowed_brand not in raw