"""Komisario Lotta Kallion sosiaalisen solmun testit.

Lotta Kallio tunkeutuu psykotronisesti päivän 1 Tukholman-simulaatioon
etsiessään vuosikymmenten partneriaan. Ennen solmun lisäämistä `lotta_check`
ja `lotta_panic` -interaktioiden kohdistamat suhdemuutokset (`target:
lotta_kallio`) putosivat hiljaa, koska solmua ei ollut graafissa —
`_sync_social_from_rpg` jätti ne pending-tilaan ja `_record_npc_memories`
ohitti ne. Nämä testit varmistavat, että solmu on olemassa, suhteet ovat
kanonin mukaiset ja päivän 1 -suhdemuutokset aktivoituvat oikein.
"""

from __future__ import annotations

from pathlib import Path

from src.rpg import RPGSession, load_character, scenario_from_dict
from src.game import GameState
from src.game.social_graph import MultiDimensionalSocialGraph

ROOT = Path(__file__).resolve().parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_narkkari.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1.json"


def make_state(seed: int = 42) -> GameState:
    state = GameState.from_files(CHARACTER, SCENARIO, seed=seed)
    state.start()
    return state


# ── Solmu ja perussuhteet ──────────────────────────────────────────


def test_lotta_kallio_node_exists():
    """lotta_kallio-solmu on olemassa kanonin mukaisilla attribuuteilla."""
    state = make_state()
    assert "lotta_kallio" in state.social.graph
    node = state.social.graph.nodes["lotta_kallio"]
    assert node["name"] == "Komisario Lotta Kallio"
    assert node["role"] == "intelligence"
    assert node["mood"] == "alarmed"
    goals = node["goals"]
    assert any("kadonnut" in g for g in goals)
    assert any("Romppainen" in g for g in goals)


def test_lotta_to_romppainen_visible_relationship():
    """Kallio luottaa ja tuntee partnerinsa syvästi, pelkää hänen puolestaan."""
    state = make_state()
    rel = state.social.get_relationship("lotta_kallio", "romppainen")
    assert rel.trust == 2
    assert rel.familiarity == 3
    assert rel.fear == 1
    assert rel.suspicion == 1
    assert rel.authority == 2


def test_romppainen_to_lotta_visible_relationship():
    """Narkkari-Sven-Olof ei tunnista Kalliota: pelottava poliisi, sumea tuttuus."""
    state = make_state()
    rel = state.social.get_relationship("romppainen", "lotta_kallio")
    assert rel.trust == 0
    assert rel.familiarity == 1
    assert rel.suspicion == 1
    assert rel.fear == 1


def test_ragnarok_lotta_hidden_relationships():
    """Ragnarök ja Kallio havaitsevat toisensa piilokerroksessa."""
    state = make_state()
    # Reuna on olemassa ja piilossa
    assert state.social.graph.has_edge("ufab_ragnarok", "lotta_kallio")
    assert ("ufab_ragnarok", "lotta_kallio") in state.social._hidden_edges
    assert state.social.graph.has_edge("lotta_kallio", "ufab_ragnarok")
    assert ("lotta_kallio", "ufab_ragnarok") in state.social._hidden_edges
    r_to_l = state.social.get_relationship("ufab_ragnarok", "lotta_kallio")
    assert r_to_l.suspicion == 2


# ── Kanoninen eksplisiittinen muisti day_1.jsonissa ────────────────


def test_canonical_scenario_contains_explicit_lotta_memory():
    """day_1.jsonin lotta_panic kantaa eksplisiittistä Lotta-muistia."""
    from src.rpg import load_scenario

    scenario = load_scenario(SCENARIO)
    scene = scenario.scenes["d1_therapy_session"]
    interaction = scene.interactions["lotta_panic"]
    npc_events = [
        e for o in list(interaction.outcomes.values()) + [interaction.automatic_outcome]
        if o for e in o.events if e["type"] == "npc_memory"
    ]
    assert npc_events, "lotta_panic pitää sisältää npc_memory-tapahtuman"
    payload = npc_events[0]["payload"]
    assert payload["target"] == "lotta_kallio"
    assert "partner" in payload["tags"]
    assert payload["valence"] == -1


# ── Päästä-päähän: solmun olemassaolo aktivoi suhdemuutokset ────────


def _probe_scenario(event: dict) -> dict:
    return {
        "id": "lotta_probe",
        "title": "Lotta probe",
        "entry_scene": "room",
        "scenes": [{
            "id": "room",
            "title": "Room",
            "description": "A partner moment.",
            "location": "Test Annex",
            "interactions": [{
                "id": "trigger",
                "label": "Trigger",
                "outcome": {
                    "text": "A change is felt.",
                    "events": [event],
                },
            }],
        }],
    }


def test_relationship_change_to_lotta_now_applies():
    """Aiemmin pudonnut suhdemuutos lotta_kallioon aktivoituu nyt.

    Ennen solmun lisäämistä _sync_social_from_rpg jätti tällaisen
    GraphEffectin pending-tilaan (target not in graph). Nyt trust-muutos
    pitää heijastua sosiaaliseen graafiin asti.
    """
    character = load_character(CHARACTER)
    rpg = RPGSession(
        character,
        scenario_from_dict(_probe_scenario({
            "type": "relationship_change_requested",
            "payload": {"target": "lotta_kallio", "delta": 1, "dimension": "trust"},
        })),
        seed=42,
    )
    social = MultiDimensionalSocialGraph(seed=42)
    state = GameState(rpg, social)
    state._populate_default_social_graph()

    # Lähde on pelaaja (romppainen), kohde lotta_kallio: muutos kohdistuu
    # romppainen -> lotta_kallio -suhteeseen (trust 0 -> 1).
    assert state.social.get_relationship("romppainen", "lotta_kallio").trust == 0
    state.perform_rpg_interaction("trigger")
    assert state.social.get_relationship("romppainen", "lotta_kallio").trust == 1
    # Lottan oma luottamus partneriinsa (lotta -> romppainen) ei muutu.
    assert state.social.get_relationship("lotta_kallio", "romppainen").trust == 2


def test_explicit_lotta_memory_records_in_social_graph():
    """Eksplisiittinen npc_memory lotta_kalliolle tallentuu graafiin asti."""
    character = load_character(CHARACTER)
    rpg = RPGSession(
        character,
        scenario_from_dict(_probe_scenario({
            "type": "npc_memory",
            "payload": {
                "target": "lotta_kallio",
                "summary": "Partneri ei tunnistanut minua.",
                "valence": -1,
                "tags": ["partner", "misrecognition", "lotta"],
            },
        })),
        seed=42,
    )
    social = MultiDimensionalSocialGraph(seed=42)
    state = GameState(rpg, social)
    state._populate_default_social_graph()

    state.perform_rpg_interaction("trigger")

    memories = state.social.memories("lotta_kallio")
    probe = [m for m in memories if "partner" in m["tags"]]
    assert probe, "Eksplisiittinen npc_memory lotta_kalliolle pitää tallentua"
    assert probe[0]["summary"] == "Partneri ei tunnistanut minua."
    assert probe[0]["valence"] == -1