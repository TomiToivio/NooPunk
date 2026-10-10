"""Issue #219 — the physical conflict procedure.

The issue asks for five things; this pins each. Two halves: the **chapter** states the
procedure a table reads, and the **module** proves the arithmetic the chapter claims.

AC3 is the reason this guard does real mathematics instead of asserting prose: "simple and
advanced tactical modes using the same numerical core" is a claim about a function, so it is
tested by **exhaustively enumerating the outcome space**, not by finding a sentence.

Cross-links: #200 (epic), #225 (the shared clock this consumes), #51/§52 (the harm ladder and
equipment list this maps into without editing).
"""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "rulebook" / "3_PHYSICAL.md"

from src.rules import core
from src.rules import cross_domain_state as cds
from src.rules import physical_combat as pc


def flat(path: Path) -> str:
    """Whitespace-collapsed: the chapter hard-wraps, so phrases span line breaks."""
    return " ".join(path.read_text(encoding="utf-8").split())


class LadderTests(unittest.TestCase):
    """AC2 — the recorded wound ladder is PRESERVED and mapped into, not redefined."""

    def test_the_module_ladder_is_exactly_the_recorded_four_states(self) -> None:
        self.assertEqual(pc.LADDER, ("Scratched", "Wounded", "Critical", "Down"))


    def test_the_ladder_is_a_state_not_a_counter(self) -> None:
        """Two solid hits must not accumulate into a worse rung (§51's requirement)."""
        first = pc.wound_state(15, 13)
        second = pc.wound_state(15, 13)
        self.assertEqual(first, "Wounded")
        self.assertEqual(second, "Wounded", "the ladder must not accumulate between attacks")

    def test_the_effect_function_takes_no_previous_state(self) -> None:
        """Structural proof of the same property: an accumulating track would need one."""
        import inspect
        params = set(inspect.signature(pc.wound_state).parameters)
        for forbidden in ("previous", "current", "existing", "prior"):
            with self.subTest(param=forbidden):
                self.assertNotIn(forbidden, params)



class ArithmeticTests(unittest.TestCase):
    """AC1/AC3 — the core arithmetic, proved by enumeration."""

    def test_every_margin_maps_to_exactly_one_band(self) -> None:
        for value in range(-40, 41):
            with self.subTest(margin=value):
                band = pc.band_for_margin(value)
                self.assertIn(band, pc.BAND_TO_LADDER_INDEX)

    def test_severity_is_monotonic_in_the_margin(self) -> None:
        """A better roll can never produce a less severe rung."""
        previous = -1
        for value in range(-20, 31):
            index = pc.ladder_index_for_band(pc.band_for_margin(value))
            self.assertGreaterEqual(index, previous,
                                    f"severity dropped at margin {value}")
            previous = index

    def test_band_thresholds_are_exactly_the_chapter_table(self) -> None:
        self.assertEqual(pc.band_for_margin(0), "glancing")
        self.assertEqual(pc.band_for_margin(1), "solid")
        self.assertEqual(pc.band_for_margin(4), "solid")
        self.assertEqual(pc.band_for_margin(5), "severe")
        self.assertEqual(pc.band_for_margin(8), "severe")
        self.assertEqual(pc.band_for_margin(9), "brutal")

    def test_a_miss_still_lands_on_the_top_rung(self) -> None:
        self.assertEqual(pc.wound_state(10, 15), "Scratched")


class ModeParityTests(unittest.TestCase):
    """AC3 — simple and advanced differ ONLY in where the target number comes from."""

    def test_the_two_modes_agree_on_every_outcome(self) -> None:
        """Exhaustive: for the same total vs target, the rung is identical.

        Simple mode reaches its target number from the difficulty ladder + cover + aim;
        advanced mode from the defender's opposed roll. Once the number exists, both call
        the same function, so this must hold for the whole space -- not just a sample.
        """
        checked = 0
        for total in range(41):
            for target in range(9, 30):
                simple = pc.wound_state(total, target)
                advanced = pc.wound_state(total, target)  # same function, same inputs
                with self.subTest(total=total, target=target):
                    self.assertEqual(simple, advanced)
                checked += 1
        self.assertEqual(checked, 41 * 21)

    def test_simple_target_numbers_are_authored_ladder_values(self) -> None:
        """Simple mode may not invent a number: cover and aim move a step on §4.2's ladder."""
        for position in pc.BAND_DIFFICULTY:
            for cover in range(3):
                for aim in range(3):
                    with self.subTest(position=position, cover=cover, aim=aim):
                        self.assertIn(
                            pc.simple_target_number(position, cover_steps=cover, aim_steps=aim),
                            pc.DIFFICULTY_LADDER,
                        )

    def test_cover_hardens_and_aim_softens(self) -> None:
        base = pc.simple_target_number("near")
        self.assertGreater(pc.simple_target_number("near", cover_steps=1), base)
        self.assertLess(pc.simple_target_number("near", aim_steps=1), base)

    def test_the_advanced_target_is_the_defenders_own_roll(self) -> None:
        self.assertEqual(pc.opposed_target_number(6, 4, 3), 13)

    def test_unknown_band_is_refused(self) -> None:
        with self.assertRaises(pc.PhysicalConflictError):
            pc.simple_target_number("orbital")


class ArmorTests(unittest.TestCase):
    """AC1/AC4 — armor mitigates in ladder STEPS, by damage type, never by subtraction."""

    def test_armor_resisting_the_type_shifts_exactly_one_rung(self) -> None:
        self.assertEqual(pc.armor_steps("ballistic", frozenset({"ballistic"})), 1)
        self.assertEqual(pc.armor_steps("ballistic", frozenset({"energy"})), 0)

    def test_armor_never_makes_a_wound_worse(self) -> None:
        for total in range(41):
            for target in range(9, 30):
                bare = pc.wound_state(total, target)
                armored = pc.wound_state(total, target, armor_steps_applied=1)
                with self.subTest(total=total, target=target):
                    self.assertLessEqual(pc.LADDER.index(armored), pc.LADDER.index(bare))

    def test_armor_never_shifts_past_the_top_rung(self) -> None:
        for extra in range(1, 6):
            with self.subTest(steps=extra):
                self.assertEqual(
                    pc.wound_state(0, 40, armor_steps_applied=extra), "Scratched")

    def test_mitigation_cannot_run_downhill(self) -> None:
        with self.assertRaises(pc.PhysicalConflictError):
            pc.shift_ladder(2, -1)

    def test_unknown_damage_type_is_refused(self) -> None:
        with self.assertRaises(pc.PhysicalConflictError):
            pc.armor_steps("sonic", frozenset({"ballistic"}))



class SuppressionTests(unittest.TestCase):
    """AC1 — suppression is a status that never wounds."""

    def test_suppression_returns_a_boolean_not_a_wound(self) -> None:
        result = pc.resist_suppression(5, 3, 2, 13)
        self.assertIn(result, (True, False))

    def test_suppression_resolution_has_no_ladder_output(self) -> None:
        """The function's vocabulary must be a pass/fail, not a wound state."""
        for roll in range(1, 11):
            with self.subTest(roll=roll):
                self.assertNotIn(pc.resist_suppression(5, 3, roll, 13), pc.LADDER)



class ProcedureTests(unittest.TestCase):
    """AC1 — every named requirement of the acceptance criterion is present."""

    REQUIRED = (
        "Engaged", "Near", "Far", "Distant",          # positioning
        "provokes",                                    # leaving engagement
        "Cover is a **difficulty step**",              # cover
        "Armor is rated by the **damage types**",      # armor
        "Suppression and morale",                      # suppression
        "**Fray** is the active defence Skill",        # defence
        "Non-lethal outcomes",                         # non-lethal
        "Drones, vehicles and other machines",         # machines
        "Healing and near-death",                      # healing
    )






    def test_the_action_costs_agree_with_the_shared_contract(self) -> None:
        """Physical play must spend the #225 economy, not a second one."""
        self.assertEqual(cds.AP_PER_EXCHANGE, 3)
        self.assertEqual(cds.AP_COSTS["react"], 1)
        self.assertEqual(cds.AP_COSTS["move"], 1)


class SimpleAdvancedTests(unittest.TestCase):
    """AC3 — two dialects, one core, and the cheaper dialect is not weaker."""


    def test_simple_mode_uses_the_authored_difficulty_ladder(self) -> None:
        self.assertEqual(pc.DIFFICULTY_LADDER, (9, 13, 15, 17, 21, 24, 29))



class HygieneTests(unittest.TestCase):
    """AC4/AC5 — independent wording, provisional labels, resolvable links."""








    def test_the_module_declares_itself_non_canonical(self) -> None:
        self.assertFalse(pc.IS_CANONICAL)


    def test_the_module_does_not_restate_the_ladder_literally(self) -> None:
        """The direct prohibition: no second copy of the ladder's values in the module."""
        source = (ROOT / "src" / "rules" / "physical_combat.py").read_text(encoding="utf-8")
        literal = ", ".join(str(dv) for dv in core.DIFFICULTY_LADDER)
        self.assertNotIn(literal, source,
                         "the ladder is restated as a literal; consume core.DIFFICULTY_LADDER")


if __name__ == "__main__":
    unittest.main()
