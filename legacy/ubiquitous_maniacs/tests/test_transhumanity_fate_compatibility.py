from pathlib import Path

from src.rpg import (
    TRANSHUMANITY_FATE_SKILLS,
    load_character,
    load_scenario,
    validate_transhumanity_fate_skill_profile,
)

ROOT = Path(__file__).resolve().parents[1]


def test_transhumanity_fate_has_24_skills_not_25() -> None:
    assert len(TRANSHUMANITY_FATE_SKILLS) == 24
    assert len(set(TRANSHUMANITY_FATE_SKILLS)) == 24


def test_day_1_romppainen_uses_25_points_and_valid_fate_columns() -> None:
    character = load_character(ROOT / "data/rpg/characters/romppainen_narkkari.md")
    validate_transhumanity_fate_skill_profile(character, expected_points=25)


def test_active_day_1_checks_only_use_transhumanity_fate_skills() -> None:
    scenario = load_scenario(ROOT / "data/rpg/scenarios/day_1.json")
    used = {
        interaction.check.skill
        for scene in scenario.scenes.values()
        for interaction in scene.interactions.values()
        if interaction.check and interaction.check.skill
    }
    assert used <= set(TRANSHUMANITY_FATE_SKILLS)


def test_arrival_and_entanglement_checks_use_v01_skills() -> None:
    scenario = load_scenario(ROOT / "data/rpg/scenarios/day_1_arrival_and_entanglement.json")
    used = {
        interaction.check.skill
        for scene in scenario.scenes.values()
        for interaction in scene.interactions.values()
        if interaction.check and interaction.check.skill
    }
    assert used <= set(TRANSHUMANITY_FATE_SKILLS)


def test_arrival_and_entanglement_romppainen_has_valid_v01_profile() -> None:
    character = load_character(ROOT / "data/rpg/characters/romppainen_day_1.md")
    validate_transhumanity_fate_skill_profile(character, expected_points=25)
