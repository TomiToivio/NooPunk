"""Issue #60: opposed interaction and harm-state tests."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclipse_phase_homebrew import (
    EP2HarmState,
    resolve_combat_attack,
    resolve_hack_action,
    resolve_opposed_test,
    resolve_social_action,
)


class EP2InteractionTests(unittest.TestCase):
    def test_success_beats_failure(self) -> None:
        result = resolve_opposed_test(
            attacker_target=60, defender_target=40,
            attacker_roll=50, defender_roll=70,
        )
        self.assertTrue(result.attacker_wins)

    def test_stronger_success_degree_wins(self) -> None:
        result = resolve_opposed_test(
            attacker_target=90, defender_target=90,
            attacker_roll=70, defender_roll=40,
        )
        self.assertEqual(result.attacker.degree, "two_superior_successes")
        self.assertEqual(result.defender.degree, "superior_success")
        self.assertEqual(result.winner, "attacker")

    def test_equal_degree_uses_higher_successful_roll(self) -> None:
        result = resolve_opposed_test(
            attacker_target=80, defender_target=80,
            attacker_roll=55, defender_roll=44,
        )
        self.assertEqual(result.winner, "attacker")

    def test_exact_tie_favors_status_quo(self) -> None:
        result = resolve_opposed_test(
            attacker_target=80, defender_target=80,
            attacker_roll=42, defender_roll=42,
        )
        self.assertEqual(result.winner, "defender")

    def test_damage_crossing_threshold_adds_wounds(self) -> None:
        harm = EP2HarmState(
            durability=40, wound_threshold=8, lucidity=30, trauma_threshold=6
        )
        self.assertEqual(harm.apply_damage(7), 0)
        self.assertEqual(harm.apply_damage(2), 1)
        self.assertEqual(harm.wounds, 1)
        self.assertEqual(harm.damage, 9)

    def test_stress_crossing_threshold_adds_trauma(self) -> None:
        harm = EP2HarmState(
            durability=40, wound_threshold=8, lucidity=12, trauma_threshold=4
        )
        self.assertEqual(harm.apply_stress(9), 2)
        self.assertEqual(harm.traumas, 2)
        self.assertFalse(harm.overwhelmed)
        harm.apply_stress(3)
        self.assertTrue(harm.overwhelmed)

    def test_combat_only_applies_damage_on_attacker_win(self) -> None:
        harm = EP2HarmState(
            durability=20, wound_threshold=5, lucidity=20, trauma_threshold=5
        )
        hit = resolve_combat_attack(
            attacker_target=70, defender_target=30, damage=6,
            defender_harm=harm, attacker_roll=50, defender_roll=80,
        )
        self.assertTrue(hit.effect_applied)
        self.assertEqual(hit.threshold_events, 1)
        self.assertEqual(harm.damage, 6)

        miss = resolve_combat_attack(
            attacker_target=20, defender_target=70, damage=99,
            defender_harm=harm, attacker_roll=80, defender_roll=50,
        )
        self.assertFalse(miss.effect_applied)
        self.assertEqual(harm.damage, 6)

    def test_social_and_mesh_are_deterministic_structured_contests(self) -> None:
        social = resolve_social_action(
            attacker_target=65, defender_target=50,
            attacker_roll=45, defender_roll=70,
        )
        mesh = resolve_hack_action(
            attacker_target=70, defender_target=60,
            attacker_roll=55, defender_roll=75,
        )
        self.assertTrue(social.effect_applied)
        self.assertTrue(mesh.effect_applied)
        self.assertEqual(social.kind, "social")
        self.assertEqual(mesh.kind, "mesh")


if __name__ == "__main__":
    unittest.main()
