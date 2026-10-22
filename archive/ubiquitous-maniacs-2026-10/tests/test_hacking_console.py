"""Tests for the interactive hacking console in play.py.

Tests verify that:
1. All 9 hacking actions are reachable through the console menu
2. Helper functions (_select_tool, _select_aspect, _render_hacking_map) work
3. The console integrates correctly with GameState and LayeredHackingSession
4. Terminal state applies transfer to RPG state
"""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import patch

import pytest

from src.hacking import LayeredHackingSession
from src.rpg import load_character
from src.game import GameState

ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_narkkari.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1.json"
HACKING_SCENARIO = ROOT / "data/hacking/sleeping_patient.json"


def make_state(seed: int = 42) -> GameState:
    state = GameState.from_files(CHARACTER, SCENARIO, seed=seed)
    state.start()
    return state


def make_hacking_session(seed: int = 42) -> LayeredHackingSession:
    char = load_character(CHARACTER)
    return LayeredHackingSession.from_json(char, HACKING_SCENARIO)


# ── Helper function tests ──────────────────────────────────────


def test_select_tool_returns_none_for_zero():
    """_select_tool palauttaa None kun pelaaja valitsee 0 (ei työkalua)."""
    import play

    snapshot = {
        "tools": [
            {"id": "ufab_diagnostic_deck", "label": "UFABin diagnostiikkadekki",
             "layers": ["cybernetic"], "actions": ["observe"], "bonus": 1},
        ]
    }
    with patch("builtins.input", return_value="0"):
        result = play._select_tool(snapshot, "observe")
    assert result is None


def test_save_loader_resolves_day_2_scenario_automatically(tmp_path):
    import play

    day_2 = ROOT / "data/rpg/scenarios/day_2_kiimaiset_poliisit.json"
    state = GameState.from_files(CHARACTER, day_2, seed=42)
    save_path = tmp_path / "day_2.json"
    state.save_to_file(save_path)

    assert play.scenario_path_for_save(save_path) == day_2


def test_completed_day_1_advances_to_day_2_without_losing_state():
    import play

    day_1 = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"
    day_1_character = ROOT / "data/rpg/characters/romppainen_day_1.md"
    state = GameState.from_files(day_1_character, day_1, seed=42)
    state.rpg.state.current_scene = "d1_complete"
    state.rpg.state.campaign_flags["noosphere_contact"] = True

    assert play.advance_campaign_if_ready(state)
    assert state.rpg.scenario.id == "day_2_kiimaiset_poliisit"
    assert state.rpg.state.campaign_flags["noosphere_contact"] is True


def test_select_tool_returns_tool_id():
    """_select_tool palauttaa työkalun ID:n kun pelaaja valitsee sen."""
    import play

    snapshot = {
        "tools": [
            {"id": "ufab_diagnostic_deck", "label": "UFABin diagnostiikkadekki",
             "layers": ["cybernetic"], "actions": ["observe"], "bonus": 1},
            {"id": "tanaka_grounding_protocol", "label": "Tanakan grounding-protokolla",
             "layers": ["psychic", "biological"], "actions": ["defend"], "bonus": 1},
        ]
    }
    with patch("builtins.input", return_value="2"):
        result = play._select_tool(snapshot, "defend")
    assert result == "tanaka_grounding_protocol"


def test_select_tool_returns_none_for_empty():
    """_select_tool palauttaa None kun ei työkaluja."""
    import play

    snapshot = {"tools": []}
    result = play._select_tool(snapshot, "observe")
    assert result is None


def test_select_aspect_returns_none_when_no_aspects():
    """_select_aspect palauttaa None kun hahmolla ei ole aspekteja."""
    import play

    char = load_character(CHARACTER)
    # Varmista että hahmolla ei ole aspekteja tässä testissä
    char.aspects = set()
    snapshot = {"aspects": []}
    result = play._select_aspect(snapshot, char)
    assert result is None


def test_select_aspect_returns_none_when_no_fate_points():
    """_select_aspect palauttaa None kun ei Fate-pisteitä."""
    import play

    char = load_character(CHARACTER)
    char.aspects = {"Test Aspect"}
    char.resources["fate_points"] = 0
    snapshot = {"aspects": []}
    result = play._select_aspect(snapshot, char)
    assert result is None


def test_select_aspect_returns_aspect_name():
    """_select_aspect palauttaa aspektin nimen kun valitaan."""
    import play

    char = load_character(CHARACTER)
    char.aspects = {"Hidden Depths"}
    char.resources["fate_points"] = 3
    snapshot = {"aspects": ["Hacking Advantage"]}
    with patch("builtins.input", return_value="1"):
        result = play._select_aspect(snapshot, char)
    # Sekä hahmon että session aspektit yhdistetään, ja lajitellaan
    # "Hacking Advantage" < "Hidden Depths" aakkosjärjestyksessä
    assert result == "Hacking Advantage"


def test_render_hacking_map_shows_nodes():
    """_render_hacking_map näyttää solmut ja nykyisen solmun merkinnän."""
    import play

    snapshot = {
        "known_nodes": [
            {"id": "clinical_terminal", "layer": "cybernetic", "access": "CONTACT",
             "description": "Kulunut vihreä pääte", "vulnerabilities": ["night_shift_session"]},
        ],
        "current_node": "clinical_terminal",
        "discovered_edges": [],
        "resonance_options": [],
    }
    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        play._render_hacking_map(snapshot)
    output = fake_out.getvalue()
    assert "clinical_terminal" in output
    assert "cybernetic" in output
    assert "CONTACT" in output
    assert "night_shift_session" in output
    assert "◀" in output  # nykyisen solmun merkki


def test_render_hacking_map_shows_resonance_options():
    """_render_hacking_map näyttää resonanssivaihtoehdot."""
    import play

    snapshot = {
        "known_nodes": [
            {"id": "clinical_terminal", "layer": "cybernetic", "access": "CONTACT",
             "description": "", "vulnerabilities": []},
        ],
        "current_node": "clinical_terminal",
        "discovered_edges": [],
        "resonance_options": [
            {"target": "ufab_80mg_concentration", "edge_type": "implant_brain_interface",
             "target_layer": "biological", "target_known": False},
        ],
    }
    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        play._render_hacking_map(snapshot)
    output = fake_out.getvalue()
    assert "implant_brain_interface" in output
    assert "biological" in output
    assert "paljastamaton" in output


def test_render_hacking_map_shows_edges():
    """_render_hacking_map näyttää löydetyt kaaret."""
    import play

    snapshot = {
        "known_nodes": [],
        "current_node": "a",
        "discovered_edges": [
            {"source": "clinical_terminal", "target": "pilgrim_tanaka_implant",
             "edge_type": "network_connection"},
        ],
        "resonance_options": [],
    }
    with patch("sys.stdout", new=io.StringIO()) as fake_out:
        play._render_hacking_map(snapshot)
    output = fake_out.getvalue()
    assert "clinical_terminal" in output
    assert "pilgrim_tanaka_implant" in output
    assert "network_connection" in output


# ── Console integration tests ───────────────────────────────────


def test_hacking_console_menu_has_all_nine_actions():
    """Konsolivalikossa näkyy kaikki 9 toimintoa + poistumistoiminto."""
    import play

    state = make_state()
    state.hacking.available = True

    # Simuloi: heti kun valinta kysytään, valitse 0 (poistu)
    with patch("builtins.input", side_effect=["0"]), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    # Kaikki 9 toimintoa näkyvät valikossa
    assert "[1] Observe" in output
    assert "[2] Create access" in output
    assert "[3] Exploit" in output
    assert "[4] Resonate" in output
    assert "[5] Create advantage" in output
    assert "[6] Defend" in output
    assert "[7] Overcome" in output
    assert "[8] Attack" in output
    assert "[9] Retreat" in output
    assert "[0] Takaisin peliin" in output


def test_hacking_console_shows_verkkokartta():
    """Konsoli näyttää verkkokartan solmuineen."""
    import play

    state = make_state()
    state.hacking.available = True

    with patch("builtins.input", side_effect=["0"]), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "VERKKOKARTTA" in output
    assert "Solmut:" in output


def test_hacking_console_observe_action_works():
    """Observe-toiminto toimii konsolin kautta."""
    import play

    state = make_state()
    state.hacking.available = True

    # Syöte: valitse 1 (observe), valitse node 1, ei työkalua (0),
    # ei invokointia (0), automaattinen heitto (Enter), sitten poistu (0)
    inputs = ["1", "1", "0", "0", "", "0"]
    with patch("builtins.input", side_effect=inputs), \
         patch("sys.stdout", new=io.StringIO()):
        play.run_hacking_console(state)

    # State pitäisi olla päivittynyt
    assert state.hacking.attempts >= 1


def test_hacking_console_retreat_action_works():
    """Retreat-toiminto (9) toimii konsolin kautta."""
    import play

    state = make_state()
    state.hacking.available = True

    # Syöte: valitse 9 (retreat), Enter tulokselle, Enter päättymiselle
    inputs = ["9", "", ""]
    with patch("builtins.input", side_effect=inputs), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "Irrottauduit" in output or "retreat" in output.lower()


def test_hacking_console_shows_terminal_state():
    """Kun sessio on päättynyt, konsoli näyttää sen ja siirtää seuraukset."""
    import play

    state = make_state()
    state.hacking.available = True

    # Pakota sessio päätökseen
    session = play.get_or_create_hacking_session(state)
    session.status = "completed"

    with patch("builtins.input", side_effect=[""]), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "Sessio on päättynyt" in output


def test_hacking_console_shows_aspects_when_active():
    """Konsoli näyttää aktiiviset aspektit kun niitä on."""
    import play

    state = make_state()
    state.hacking.available = True

    session = play.get_or_create_hacking_session(state)
    session.aspects.add("Test Advantage")

    with patch("builtins.input", side_effect=["0"]), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "Aktiiviset aspektit" in output
    assert "Test Advantage" in output


def test_hacking_console_create_advantage_requires_name():
    """Create advantage -toiminto vaatii aspektin nimen."""
    import play

    state = make_state()
    state.hacking.available = True

    # Syöte: valitse 5 (create advantage), valitse node 1,
    # tyhjä nimi (Enter) → virheilmoitus, Enter, sitten poistu
    inputs = ["5", "1", "", "", "0"]
    with patch("builtins.input", side_effect=inputs), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "Aspektin nimi puuttuu" in output


def test_hacking_console_invalid_choice_handled():
    """Epäkelpo valinta käsitellään oikein."""
    import play

    state = make_state()
    state.hacking.available = True

    # Syöte: epäkelpo valinta "x", Enter, sitten poistu "0"
    inputs = ["x", "", "0"]
    with patch("builtins.input", side_effect=inputs), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "Epäkelpo valinta" in output


def test_hacking_console_not_available_shows_message():
    """Kun hacking ei ole saatavilla, näytetään viesti."""
    import play

    state = make_state()
    state.hacking.available = False

    with patch("builtins.input", side_effect=[""]), \
         patch("sys.stdout", new=io.StringIO()) as fake_out:
        play.run_hacking_console(state)
    output = fake_out.getvalue()
    assert "Psykotroniikka ei ole vielä saatavilla" in output


# ── Full action coverage via session API ───────────────────────


def test_all_nine_actions_callable_from_session():
    """Varmista että kaikki 9 toimintoa ovat kutsuttavissa LayeredHackingSessionista."""
    session = make_hacking_session()

    # 1. Observe (entry node, should succeed with high roll)
    result = session.observe("clinical_terminal", roll=4)
    assert result.action.value == "observe"

    # 2. Create access (self-to-self on entry node)
    result = session.create_access("clinical_terminal", "clinical_terminal", roll=4)
    assert result.action.value == "create_access"

    # 3. Exploit (now has Access level)
    result = session.exploit("clinical_terminal", roll=4)
    assert result.action.value == "exploit"

    # 5. Create advantage
    result = session.create_advantage("clinical_terminal", "Test Edge", roll=4)
    assert result.action.value == "create_advantage"

    # 6. Defend
    result = session.defend("clinical_terminal", roll=4)
    assert result.action.value == "defend"

    # 7. Overcome
    result = session.overcome("clinical_terminal", roll=4)
    assert result.action.value == "overcome"

    # 8. Attack (requires Access level — clinical_terminal has it now)
    result = session.attack("clinical_terminal", roll=4)
    assert result.action.value == "attack"

    # 9. Retreat
    result = session.retreat()
    assert result.action.value == "retreat"
    assert session.is_terminal


def test_resonate_action_with_cross_layer():
    """Resonate-toiminto toimii cross-layer-kaaren kautta.

    Cross-layer-kaaret ovat hidden-solmujen välillä. Pelaajan pitää
    ensin paljastaa hidden-solmu observe-toiminnolla, saavuttaa
    Contact-taso, ja vasta sitten resonoida toiseen kerrokseen.
    """
    session = make_hacking_session()

    # 1. Observe clinical_terminal → paljastaa pilgrim_tanaka_implant (naapuri)
    session.observe("clinical_terminal", roll=4)
    assert "pilgrim_tanaka_implant" in session.known_nodes

    # 2. Create access clinical_terminal → pilgrim_tanaka_implant (Contact-taso)
    session.create_access("clinical_terminal", "pilgrim_tanaka_implant", roll=4)
    assert session.access.get("pilgrim_tanaka_implant") is not None

    # 3. Resonate pilgrim_tanaka_implant → ufab_80mg_concentration (implant_brain_interface)
    #    Tämä on cross-layer: cybernetic → biological
    assert session.graph.has_edge("pilgrim_tanaka_implant", "ufab_80mg_concentration")
    edge = session.graph.edges["pilgrim_tanaka_implant", "ufab_80mg_concentration"]
    assert edge["edge_type"] == "implant_brain_interface"

    result = session.resonate("pilgrim_tanaka_implant", "ufab_80mg_concentration", roll=4)
    assert result.action.value == "resonate"
    assert result.success
    assert "ufab_80mg_concentration" in session.known_nodes
