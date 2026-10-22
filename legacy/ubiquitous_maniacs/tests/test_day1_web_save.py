from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.game.day1_web_save import FORMAT, from_dict, to_dict
from src.hacking import LayeredHackingSession
from src.rpg import RPGSession, load_character, load_scenario, session_to_dict
from src.sim.social import SocialSimulation
from src.social import load_people_records, load_relationship_records


ROOT = Path(__file__).parents[1]
CHARACTER = ROOT / "data/rpg/characters/romppainen_day_1.md"
SCENARIO = ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json"
HACKING = ROOT / "data/hacking/sleeping_patient.json"


def source_data() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    return (
        load_people_records(ROOT / "data/lab_people.csv"),
        load_relationship_records(ROOT / "data/lab_relationships.csv"),
    )


def test_integrated_day_1_save_round_trip_preserves_all_live_modules() -> None:
    character = load_character(CHARACTER)
    rpg = RPGSession(character, load_scenario(SCENARIO), seed=1601)
    people, relationships = source_data()
    social = SocialSimulation.from_lab_data(people, relationships)
    social.interact("sven_olof_romppainen", "ingrid_falk", "flirt")
    hacking = LayeredHackingSession.from_json(character, HACKING)
    hacking.observe("clinical_terminal", roll=4)

    document = to_dict(rpg, social, 0, hacking, False)
    restored = from_dict(
        json.loads(json.dumps(document)), CHARACTER, SCENARIO, people, relationships
    )

    assert document["format"] == FORMAT
    assert restored.rpg.seed == 1601
    assert restored.social.get_relationship("sven_olof_romppainen", "ingrid_falk") == 4
    assert restored.social.history()[0]["action"] == "flirt"
    assert "pilgrim_tanaka_implant" in restored.hacking.known_nodes
    assert restored.hacking.history == hacking.history
    assert restored.hacking.actor is restored.rpg.character
    assert restored.hacking_applied is False


def test_legacy_rpg_only_save_remains_loadable() -> None:
    rpg = RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), seed=7)
    people, relationships = source_data()

    restored = from_dict(session_to_dict(rpg), CHARACTER, SCENARIO, people, relationships)

    assert restored.rpg.seed == 7
    assert restored.social.state()["tick"] == 0
    assert restored.hacking is None
    assert restored.social_effects == 0


def test_integrated_save_rejects_unknown_version_and_invalid_transfer_marker() -> None:
    rpg = RPGSession(load_character(CHARACTER), load_scenario(SCENARIO), seed=1)
    people, relationships = source_data()
    social = SocialSimulation.from_lab_data(people, relationships)
    document = to_dict(rpg, social, 0, None, False)

    document["version"] = 99
    with pytest.raises(ValueError, match="Unsupported"):
        from_dict(document, CHARACTER, SCENARIO, people, relationships)

    document["version"] = 1
    document["hacking_applied"] = True
    with pytest.raises(ValueError, match="missing hacking"):
        from_dict(document, CHARACTER, SCENARIO, people, relationships)
