"""The contract and the kernel must agree.

`src/rules/wn_core.py` is the implementation; `data/rules/wn_core.json` is the readable contract that states
the same numbers. Two sources of truth is exactly how a band drifts — one gets edited, the other does not, and
the documentation keeps describing the old arithmetic. These tests compare them instead of trusting either.

They also pin the *shape* of the core to the Without Number baseline adopted by #620, so a later edit to one
number fails here rather than in a session six weeks from now.
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import unittest  # noqa: E402

from rules import (  # noqa: E402
    cwn_advancement,
    cwn_attack_modifiers,
    cwn_combat_actions,
    cwn_encumbrance,
    cwn_major_injury,
    cwn_strain,
    wn_core,
)

CONTRACT = json.loads((ROOT / "data" / "rules" / "wn_core.json").read_text(encoding="utf-8"))


class ContractAgreesWithKernelTests(unittest.TestCase):
    def test_every_attribute_score_maps_to_the_documented_modifier(self) -> None:
        table = {int(k): v for k, v in CONTRACT["stats"]["modifier_table"].items()}
        for score in range(CONTRACT["stats"]["min"], CONTRACT["stats"]["max"] + 1):
            with self.subTest(score=score):
                self.assertEqual(wn_core.attribute_modifier(score), table[score])

    def test_the_attribute_bounds_match(self) -> None:
        self.assertEqual(wn_core.ATTRIBUTE_MIN, CONTRACT["stats"]["min"])
        self.assertEqual(wn_core.ATTRIBUTE_MAX, CONTRACT["stats"]["max"])

    def test_the_difficulty_ladder_matches(self) -> None:
        documented = {int(k): v for k, v in CONTRACT["skill_check"]["difficulties"].items()}
        kernel = {
            wn_core.DIFFICULTY_SIMPLE: "Simple",
            wn_core.DIFFICULTY_SIGNIFICANT: "Significant",
            wn_core.DIFFICULTY_EXPERT: "Expert",
            wn_core.DIFFICULTY_MASTER: "Master",
            wn_core.DIFFICULTY_EXTREME: "Extreme",
        }
        self.assertEqual(kernel, documented)

    def test_the_check_dice_match(self) -> None:
        self.assertEqual(wn_core.SKILL_CHECK_DICE, CONTRACT["skill_check"]["dice_count"])
        self.assertEqual(wn_core.SKILL_CHECK_FACES, CONTRACT["skill_check"]["dice_sides"])

    def test_the_situational_and_aid_bounds_match(self) -> None:
        self.assertEqual(wn_core.SITUATIONAL_MIN, CONTRACT["modifiers"]["situational_min"])
        self.assertEqual(wn_core.SITUATIONAL_MAX, CONTRACT["modifiers"]["situational_max"])
        self.assertEqual(wn_core.AID_BONUS_MAX, CONTRACT["modifiers"]["aid_bonus_max"])

    def test_the_base_modifier_cap_matches(self) -> None:
        self.assertEqual(wn_core.MODIFIER_CAP, CONTRACT["stats"]["base_modifier_cap"])


class KernelBehaviourTests(unittest.TestCase):
    """The arithmetic the contract describes, asserted through the kernel with exact dice."""

    def test_two_d6_plus_modifier_plus_skill(self) -> None:
        result = wn_core.skill_check(
            attribute_score=14, skill_level=2, difficulty=10, dice=(5, 3)
        )
        self.assertEqual(result.attribute_modifier, 1)
        # 5 + 3 + 1 (modifier) + 2 (skill)
        self.assertEqual(sum(result.dice) + result.attribute_modifier + result.skill_level, 11)

    def test_situational_is_clamped_not_trusted(self) -> None:
        high = wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                   situational=99, dice=(1, 1))
        self.assertEqual(high.situational, CONTRACT["modifiers"]["situational_max"])
        low = wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                  situational=-99, dice=(6, 6))
        self.assertEqual(low.situational, CONTRACT["modifiers"]["situational_min"])

    def test_a_negative_skill_level_is_refused(self) -> None:
        with self.assertRaises(wn_core.WnError):
            wn_core.skill_check(attribute_score=10, skill_level=-1, difficulty=8, dice=(3, 3))

    def test_a_bad_die_face_is_refused(self) -> None:
        for bad in ((0, 3), (7, 3)):
            with self.subTest(dice=bad):
                with self.assertRaises(Exception):
                    wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8, dice=bad)

    def test_a_seed_replays_and_a_different_seed_does_not(self) -> None:
        import random

        def rolls(seed: int) -> list[tuple[int, int]]:
            return [
                tuple(wn_core.skill_check(attribute_score=10, skill_level=1, difficulty=8,
                                          rng=random.Random(seed)).dice)
                for _ in range(4)
            ]

        self.assertEqual(rolls(42), rolls(42))
        self.assertNotEqual(rolls(42), rolls(43))


if __name__ == "__main__":
    unittest.main()


class StrainContractTests(unittest.TestCase):
    """Strain's numbers live in the contract too; a change to one must fail here."""

    def test_recovery_rate_matches(self) -> None:
        self.assertEqual(CONTRACT["strain"]["recovery_per_night"], cwn_strain.RECOVERY_PER_NIGHT)

    def test_the_maximum_is_the_constitution_score(self) -> None:
        self.assertEqual(CONTRACT["strain"]["maximum"], "Constitution score")
        self.assertEqual(cwn_strain.MAXIMUM_ATTRIBUTE, "Constitution")

    def test_the_rest_requirement_matches(self) -> None:
        self.assertEqual(CONTRACT["strain"]["recovery_conditions"],
                         "warm, fed, comfortable, at least 8 uninterrupted hours of sleep")
        self.assertEqual(cwn_strain.REST_HOURS_REQUIRED, 8.0)


class AdvancementContractTests(unittest.TestCase):
    def test_the_level_range_matches(self) -> None:
        self.assertEqual(cwn_advancement.MIN_LEVEL, CONTRACT["advancement"]["min_level"])
        self.assertEqual(cwn_advancement.MAX_LEVEL, CONTRACT["advancement"]["max_level"])

    def test_both_xp_tables_match(self) -> None:
        for track in ("fast", "slow"):
            with self.subTest(track=track):
                documented = {int(k): v for k, v in CONTRACT["advancement"]["xp"][track].items()}
                self.assertEqual(dict(cwn_advancement.XP_FOR_LEVEL[track]), documented)

    def test_skill_point_costs_match(self) -> None:
        documented = {int(k): v for k, v in CONTRACT["advancement"]["skill_point_cost"].items()}
        self.assertEqual(dict(cwn_advancement.SKILL_POINT_COST), documented)

    def test_skill_level_gates_match(self) -> None:
        documented = {int(k): v for k, v in CONTRACT["advancement"]["skill_min_character_level"].items()}
        self.assertEqual(dict(cwn_advancement.SKILL_MIN_CHARACTER_LEVEL), documented)

    def test_attribute_boost_gates_match(self) -> None:
        documented = {int(k): v for k, v in CONTRACT["advancement"]["attribute_boost_min_character_level"].items()}
        self.assertEqual(dict(cwn_advancement.ATTRIBUTE_BOOST_MIN_CHARACTER_LEVEL), documented)

    def test_focus_levels_and_third_edge_match(self) -> None:
        self.assertEqual(list(cwn_advancement.FOCUS_LEVELS), CONTRACT["advancement"]["focus_levels"])
        self.assertEqual(cwn_advancement.THIRD_EDGE_LEVEL, CONTRACT["advancement"]["third_edge_level"])

    def test_points_per_level_match(self) -> None:
        self.assertEqual(cwn_advancement.SKILL_POINTS_PER_LEVEL,
                         CONTRACT["advancement"]["skill_points_per_level"])
        self.assertEqual(cwn_advancement.EDUCATED_BONUS_POINTS,
                         CONTRACT["advancement"]["educated_bonus"])


class MajorInjuryContractTests(unittest.TestCase):
    def test_the_table_rows_match(self) -> None:
        documented = {int(k): v for k, v in CONTRACT["combat"]["major_injury"]["rows"].items()}
        kernel = {roll: outcome.id for roll, outcome in cwn_major_injury.MAJOR_INJURY_TABLE.items()}
        self.assertEqual(kernel, documented)

    def test_the_clamp_matches(self) -> None:
        clamp = CONTRACT["combat"]["major_injury"]["clamp"]
        self.assertEqual(cwn_major_injury.MIN_ROLL, clamp["min"])
        self.assertEqual(cwn_major_injury.MAX_ROLL, clamp["max"])


class EncumbranceContractTests(unittest.TestCase):
    def test_the_overload_step_matches(self) -> None:
        step = CONTRACT["encumbrance"]["overload_step"]
        self.assertEqual(cwn_encumbrance.OVERLOAD_READIED_BONUS, step["readied"])
        self.assertEqual(cwn_encumbrance.OVERLOAD_STOWED_BONUS, step["stowed"])

    def test_the_speed_factors_match(self) -> None:
        speed = CONTRACT["encumbrance"]["speed"]
        self.assertEqual(cwn_encumbrance.BASE_MOVE_METRES, speed["base_metres"])
        self.assertAlmostEqual(cwn_encumbrance.HEAVY_LOAD_SPEED_FACTOR, speed["heavy_factor"])
        self.assertAlmostEqual(cwn_encumbrance.OVERLOADED_SPEED_FACTOR, speed["overloaded_factor"])

    def test_bundles_and_kilograms_match(self) -> None:
        self.assertEqual(cwn_encumbrance.BUNDLE_SIZE, CONTRACT["encumbrance"]["bundle_size"])
        self.assertEqual(cwn_encumbrance.KILOGRAMS_PER_TEN_POINTS,
                         CONTRACT["encumbrance"]["kilograms_per_ten_points"])


class AttackModifierContractTests(unittest.TestCase):
    def test_the_modifier_table_matches(self) -> None:
        documented = CONTRACT["combat"]["attack_modifiers"]["table"]
        self.assertEqual(dict(cwn_attack_modifiers.ATTACK_MODIFIER_TABLE), documented)

    def test_the_impossible_circumstances_match(self) -> None:
        documented = CONTRACT["combat"]["attack_modifiers"]["impossible"]
        self.assertEqual(dict(cwn_attack_modifiers.IMPOSSIBLE_CIRCUMSTANCES), documented)


class CombatActionContractTests(unittest.TestCase):
    def test_the_action_allowance_matches(self) -> None:
        actions = CONTRACT["combat"]["actions"]
        self.assertEqual(cwn_combat_actions.MAIN_ACTIONS_PER_ROUND, actions["main_per_round"])
        self.assertEqual(cwn_combat_actions.MOVE_ACTIONS_PER_ROUND, actions["move_per_round"])
        self.assertEqual(cwn_combat_actions.ON_TURN_LIMITED, actions["on_turn_limited"])
        self.assertEqual(cwn_combat_actions.INSTANT_LIMITED, actions["instant_limited"])

    def test_the_maneuver_numbers_match(self) -> None:
        actions = CONTRACT["combat"]["actions"]
        self.assertEqual(cwn_combat_actions.SNAP_ATTACK_PENALTY, actions["snap_attack_penalty"])
        self.assertEqual(cwn_combat_actions.SWARM_PER_OTHER_HIT, actions["swarm"]["per_other_hit"])
        self.assertEqual(cwn_combat_actions.SWARM_PER_OTHER_DAMAGE, actions["swarm"]["per_other_damage"])
        self.assertEqual(cwn_combat_actions.SWARM_MAX_OTHER_ASSAILANTS,
                         actions["swarm"]["max_other_assailants"])
        self.assertEqual(cwn_combat_actions.CHARGE_TO_HIT_BONUS, actions["charge"]["to_hit"])
        self.assertEqual(cwn_combat_actions.CHARGE_AC_PENALTY, actions["charge"]["ac_penalty"])
        self.assertAlmostEqual(cwn_combat_actions.CHARGE_MIN_DISTANCE_METRES,
                               actions["charge"]["min_distance_metres"])
        self.assertEqual(cwn_combat_actions.TOTAL_DEFENSE_AC_BONUS,
                         actions["total_defense"]["ac_bonus"])
