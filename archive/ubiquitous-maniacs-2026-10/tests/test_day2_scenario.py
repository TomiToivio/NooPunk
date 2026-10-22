"""Tests for Day 2 — Kiimaiset Poliisit scenario."""

from pathlib import Path

from src.rpg import load_scenario

SCENARIO_PATH = Path("data/rpg/scenarios/day_2_kiimaiset_poliisit.json")


def _load():
    return load_scenario(SCENARIO_PATH)


# ── Structure tests ────────────────────────────────────────────


def test_scenario_loads():
    s = _load()
    assert s.id == "day_2_kiimaiset_poliisit"


def test_has_5_scenes():
    s = _load()
    assert len(s.scenes) == 5


def test_entry_scene_is_helsinki_arrival():
    s = _load()
    assert s.entry_scene == "d2_helsinki_arrival"


def test_terminal_scene_is_d2_complete():
    s = _load()
    assert "d2_complete" in s.terminal_scenes


def test_all_scene_ids_present():
    s = _load()
    expected = {"d2_helsinki_arrival", "d2_precinct", "d2_case_scene",
                "d2_trauma_scene", "d2_complete"}
    assert set(s.scenes.keys()) == expected


def test_all_next_scenes_resolve():
    s = _load()
    for scene in s.scenes.values():
        for inter in scene.interactions.values():
            outcomes = list(inter.outcomes.values())
            if inter.automatic_outcome is not None:
                outcomes.append(inter.automatic_outcome)
            for outcome in outcomes:
                if outcome.next_scene is not None:
                    assert outcome.next_scene in s.scenes, \
                        f"Unknown next_scene {outcome.next_scene} from {inter.id}"


# ── Scene content tests ────────────────────────────────────────


def test_helsinki_arrival_has_2_interactions():
    s = _load()
    scene = s.scenes["d2_helsinki_arrival"]
    assert len(scene.interactions) == 2
    assert "d2_check_mirror" in scene.interactions
    assert "d2_skip_mirror" in scene.interactions


def test_precinct_has_3_interactions():
    s = _load()
    scene = s.scenes["d2_precinct"]
    assert len(scene.interactions) == 3
    assert "d2_flirt_ingrid" in scene.interactions
    assert "d2_read_case" in scene.interactions
    assert "d2_greet_lotta" in scene.interactions


def test_case_scene_has_3_interactions():
    s = _load()
    scene = s.scenes["d2_case_scene"]
    assert len(scene.interactions) == 3
    assert "d2_push_memory" in scene.interactions
    assert "d2_deflect_joke" in scene.interactions
    assert "d2_honest" in scene.interactions


def test_trauma_scene_has_3_interactions():
    s = _load()
    scene = s.scenes["d2_trauma_scene"]
    assert len(scene.interactions) == 3
    assert "d2_face_trauma" in scene.interactions
    assert "d2_resist_trauma" in scene.interactions
    assert "d2_flee_trauma" in scene.interactions


def test_complete_scene_has_1_interaction():
    s = _load()
    scene = s.scenes["d2_complete"]
    assert len(scene.interactions) == 1
    assert "d2_end_day" in scene.interactions


# ── Dramatic arc tests ────────────────────────────────────────


def test_flirt_ingrid_has_skill_check():
    s = _load()
    inter = s.scenes["d2_precinct"].interactions["d2_flirt_ingrid"]
    assert inter.check is not None
    assert inter.check.attribute == "Charisma"
    assert inter.check.skill == "Rapport"


def test_push_memory_has_willpower_check():
    s = _load()
    inter = s.scenes["d2_case_scene"].interactions["d2_push_memory"]
    assert inter.check is not None
    assert inter.check.attribute == "Willpower"
    assert inter.check.skill == "Will"
    assert inter.check.difficulty == 4


def test_face_trauma_has_high_difficulty():
    s = _load()
    inter = s.scenes["d2_trauma_scene"].interactions["d2_face_trauma"]
    assert inter.check is not None
    assert inter.check.difficulty == 5
    assert "Hidden Depths" in inter.check.bonus_aspects


def test_face_trauma_critical_success_grants_integration():
    s = _load()
    from src.rpg.models import ResultTier
    inter = s.scenes["d2_trauma_scene"].interactions["d2_face_trauma"]
    outcome = inter.outcomes[ResultTier.CRITICAL_SUCCESS]
    assert outcome.set_flags.get("d2_outcome") == "integration"
    assert outcome.set_flags.get("d2_trauma_accepted") is True
    assert "kiimainen_poliisi_active" in outcome.remove_conditions
    assert outcome.next_scene == "d2_complete"


def test_face_trauma_catastrophic_failure_grants_breakdown():
    s = _load()
    from src.rpg.models import ResultTier
    inter = s.scenes["d2_trauma_scene"].interactions["d2_face_trauma"]
    outcome = inter.outcomes[ResultTier.CATASTROPHIC_FAILURE]
    assert outcome.set_flags.get("d2_outcome") == "breakdown"
    assert "psychic_break" in outcome.add_conditions


def test_resist_trauma_damage_relationships():
    s = _load()
    from src.rpg.models import ResultTier
    inter = s.scenes["d2_trauma_scene"].interactions["d2_resist_trauma"]
    outcome = inter.outcomes[ResultTier.SUCCESS]
    assert outcome.relationship_changes.get("lotta_kallio", 0) < 0
    assert outcome.relationship_changes.get("ingrid_falk", 0) < 0


def test_honest_answer_grants_relationship_boost():
    s = _load()
    inter = s.scenes["d2_case_scene"].interactions["d2_honest"]
    assert inter.automatic_outcome is not None
    assert inter.automatic_outcome.relationship_changes.get("lotta_kallio", 0) > 0
    assert inter.automatic_outcome.relationship_changes.get("ingrid_falk", 0) > 0


def test_greet_lotta_is_automatic():
    s = _load()
    inter = s.scenes["d2_precinct"].interactions["d2_greet_lotta"]
    assert inter.check is None
    assert inter.automatic_outcome is not None


def test_flee_trauma_is_automatic():
    s = _load()
    inter = s.scenes["d2_trauma_scene"].interactions["d2_flee_trauma"]
    assert inter.check is None
    assert inter.automatic_outcome is not None
    assert inter.automatic_outcome.set_flags.get("d2_outcome") == "fled"


def test_end_day_sets_completion_flags():
    s = _load()
    inter = s.scenes["d2_complete"].interactions["d2_end_day"]
    assert inter.automatic_outcome is not None
    assert inter.automatic_outcome.set_flags.get("day_2_complete") is True
    assert inter.automatic_outcome.set_flags.get("day_3_available") is True


# ── All paths lead to d2_complete ─────────────────────────────


def test_all_trauma_paths_lead_to_complete():
    s = _load()
    inter = s.scenes["d2_trauma_scene"].interactions["d2_face_trauma"]
    for outcome in inter.outcomes.values():
        assert outcome.next_scene == "d2_complete"


def test_all_case_paths_lead_to_trauma():
    s = _load()
    for inter in s.scenes["d2_case_scene"].interactions.values():
        outcomes = list(inter.outcomes.values())
        if inter.automatic_outcome is not None:
            outcomes.append(inter.automatic_outcome)
        for outcome in outcomes:
            assert outcome.next_scene == "d2_trauma_scene"


def test_all_precinct_paths_lead_to_case():
    s = _load()
    for inter in s.scenes["d2_precinct"].interactions.values():
        outcomes = list(inter.outcomes.values())
        if inter.automatic_outcome is not None:
            outcomes.append(inter.automatic_outcome)
        for outcome in outcomes:
            assert outcome.next_scene == "d2_case_scene"


def test_all_arrival_paths_lead_to_precinct():
    s = _load()
    for inter in s.scenes["d2_helsinki_arrival"].interactions.values():
        assert inter.automatic_outcome is not None
        assert inter.automatic_outcome.next_scene == "d2_precinct"