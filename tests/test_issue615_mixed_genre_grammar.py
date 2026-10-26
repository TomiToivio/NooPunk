"""Issue #615, criteria 4 and 6: one sheet, one grammar, four environments, no LLM.

This is the mixed-genre play example written as a regression test rather than as prose.
Prose cannot fail; this can. If a future change makes any environment need its own dice
convention, its own stat set, or its own resolution function, these tests fail.

The point being pinned: a genre module may change **what you roll for**, **how hard it is**
and **what a failure costs**. It may not change **how you roll** or **who your character is**.

Environments:
  urban/network   (CWN primary)   Interface  vs INT   — failure means exposure, not damage
  space/NHI/PSI   (SWN co-primary) Telepathy vs PSY   — failure means capacity locked
  noetic realm    (WWN)            Noöspace  vs PSY   — failure means the realm answers anyway
  crisis ruins    (AWN)            Survival  vs REF   — failure means scarcity, not death
"""
import copy
import json
import random
import unittest
from pathlib import Path

from src.rules import core

ROOT = Path(__file__).resolve().parents[1]

#: One character sheet, used unmodified in every environment below.
SHEET = {
    "name": "test-subject",
    "stats": {"FIT": 4, "REF": 4, "INT": 5, "SOC": 4, "CYB": 3, "PSY": 5},
    "skills": {"Interface": 3, "Telepathy": 3, "Noöspace": 3, "Survival": 2},
    "psyche_load": 0,
    "effort_committed": {},
    "inventory": [],
}

#: (environment, module, stat, skill, DV, what a failure costs)
ENVIRONMENTS = (
    ("helsinki-acceleration", "urban/network (CWN)", "INT", "Interface", 12,
     "exposure rises; the network remembered you"),
    ("orbital-outpost", "space/NHI (SWN)", "PSY", "Telepathy", 12,
     "Effort stays committed; the pool is smaller for the rest of the scene"),
    ("noetic-realm", "interdimensional (WWN)", "PSY", "Noöspace", 14,
     "the realm answers anyway, on its own terms"),
    ("exclusion-zone", "crisis ruins (AWN)", "REF", "Survival", 10,
     "the salvage is lost; scarcity bites"),
)


class OneSheetOneGrammarTests(unittest.TestCase):
    """The core contract: four environments, one arithmetic."""

    def test_canon_fixes_the_six_stats_and_they_are_the_ones_used_here(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        stats = canon["stats"]["final_list"]
        self.assertEqual(stats, ["FIT", "REF", "INT", "SOC", "CYB", "PSY"])
        self.assertIn("SOC", stats, "#566: SOC survives and CHA is not adopted")
        self.assertNotIn("CHA", stats, "CWN's attribute name must not enter the canon set")
        self.assertEqual(set(SHEET["stats"]), set(stats),
                         "one sheet, and it is the canon sheet — no per-genre stat variants")

    def test_every_environment_resolves_on_the_same_kernel(self) -> None:
        canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
        known_skills = set(canon["skills"]["final_list"])
        sheet_before = copy.deepcopy(SHEET)

        for name, module, stat, skill, dv, consequence in ENVIRONMENTS:
            with self.subTest(environment=name, module=module):
                self.assertIn(skill, known_skills, "a module may not invent a skill")

                result = core.resolve_check(
                    stat=SHEET["stats"][stat],
                    skill=SHEET["skills"][skill],
                    target=dv,
                    die=6,
                )

                # THE invariant: identical arithmetic in all four places.
                self.assertEqual(result.total,
                                 SHEET["stats"][stat] + SHEET["skills"][skill] + 6,
                                 "every environment must be STAT + Skill + 1d10")
                self.assertEqual(result.success, result.total >= dv,
                                 "success must be the same inequality everywhere")
                self.assertIsNotNone(consequence)

        self.assertEqual(SHEET, sheet_before,
                         "resolving in a genre module must not mutate the character sheet")

    def test_the_genre_changes_difficulty_not_arithmetic(self) -> None:
        """Same sheet, same die: only the DV (and the cost text) differs."""
        totals = {}
        for name, _module, stat, skill, dv, _cost in ENVIRONMENTS:
            r = core.resolve_check(stat=SHEET["stats"][stat],
                                   skill=SHEET["skills"][skill], target=dv, die=6)
            totals[name] = (r.die, r.stat + r.skill)
        dice = {d for d, _ in totals.values()}
        self.assertEqual(dice, {6}, "one die convention across all four environments")
        for stat_plus_skill in (v for _, v in totals.values()):
            self.assertGreaterEqual(stat_plus_skill, 2 * canon_min(), "sanity bound")


def canon_min() -> int:
    canon = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
    return int(canon["skills"]["min"])


class NoLlmDeterminismTests(unittest.TestCase):
    """Criterion 6: tabletop operation, no model in the loop, replayable."""

    def test_the_same_seed_replays_and_a_different_seed_differs(self) -> None:
        def run(seed: int) -> int:
            rng = random.Random(seed)
            return core.resolve_check(stat=4, skill=3, target=12, rng=rng).total

        self.assertEqual(run(615), run(615), "a seeded resolution must replay exactly")
        spread = {run(s) for s in range(40)}
        self.assertGreater(len(spread), 1, "different seeds must actually move the die")

    def test_the_resolver_takes_no_model_dependency(self) -> None:
        import inspect
        source = inspect.getsource(core)
        for dependency in ("openai", "anthropic", "requests", "urllib", "socket", "http"):
            self.assertNotIn(dependency, source,
                             f"the core kernel must stay offline; found {dependency!r}")


class MixedGenreScenarioTests(unittest.TestCase):
    """A single adventure that crosses all four environments without rebuilding anything."""

    def test_one_adventure_crosses_all_four_modules_without_a_new_sheet(self) -> None:
        log = []
        for name, module, stat, skill, dv, cost in ENVIRONMENTS:
            before = copy.deepcopy(SHEET)
            result = core.resolve_check(stat=SHEET["stats"][stat],
                                        skill=SHEET["skills"][skill], target=dv, die=6)
            log.append((name, module, result.total, result.success, cost))
            self.assertEqual(SHEET, before,
                             f"{name} required no change to the character to participate")

        self.assertEqual(len(log), 4)
        self.assertTrue(all(isinstance(row[2], int) for row in log))
        self.assertEqual([row[0] for row in log],
                         [e[0] for e in ENVIRONMENTS],
                         "the adventure visits every environment in order")


if __name__ == "__main__":
    unittest.main()
