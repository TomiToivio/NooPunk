"""One rule, one implementation — the duplicates that parallel agent work left behind (#1097).

Three pairs of modules implemented the same SRD procedure twice, and by the time anyone looked the copies
had already drifted: the Stressed chrome syndrome was worth +3 in one module and +5 in the other, and the
SRD says +5. These tests are the mechanical form of "merge duplicates, then keep them merged":

* **wages / lifestyles** — the numbers live in `data/rules/cwn/*.json`; `rules.cwn_lifestyles` is the only
  reader that *decides* anything, and the MUD adapter delegates to it;
* **overcasting** — one arithmetic (`cwn_magic.overcast_total`) and one table (`cwn_magic.OVERCAST_TABLE`),
  which `cwn_spells` and `EffortPool.overcast_roll` both go through;
* **Alienation** — one syndrome table (`cwn_cyberware.SYNDROMES`), which the optional `cwn_alienation`
  module reads rather than restates.

Each test asserts *identity or equality between two modules*, not a number: a number can be copied, an
equality cannot be satisfied by a second transcription that drifts.
"""

from __future__ import annotations

import inspect
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import (  # noqa: E402
    cwn_alienation, cwn_attack_modifiers, cwn_cyberware, cwn_lifestyles, cwn_magic, cwn_spells,
)
from rules.wn_core import attribute_modifier  # noqa: E402


class WagesHaveOneReaderTests(unittest.TestCase):
    def test_the_wage_table_exists_once_in_data_and_once_in_code(self) -> None:
        on_disk = json.loads((ROOT / "data/rules/cwn/common_wages.json").read_text(encoding="utf-8"))
        self.assertEqual(cwn_lifestyles.COMMON_WAGES, on_disk["wages"])
        source = inspect.getsource(cwn_lifestyles)
        self.assertNotIn("unskilled_street_laborer\"", source,
                         "the wage table must be loaded from data/, not transcribed into the module")

    def test_the_mud_economy_module_delegates(self) -> None:
        from mud.nopunk_mud.cwn import economy

        # `is` would fail on a real wart: the MUD imports `src.rules.*` while this suite imports
        # `rules.*`, so the same file can be a different module object. The values must still be one.
        self.assertEqual(economy.wages(), cwn_lifestyles.COMMON_WAGES)
        self.assertEqual(economy.daily_wage("bodyguard"),
                         cwn_lifestyles.wage("competent_street_bodyguard"))

    def test_the_lifestyle_rows_exist_once(self) -> None:
        on_disk = json.loads((ROOT / "data/rules/cwn/lifestyles.json").read_text(encoding="utf-8"))
        self.assertEqual(cwn_lifestyles.LIFESTYLE_COSTS,
                         {row["id"]: row["monthly_cost"] for row in on_disk["levels"]})


class OvercastingHasOneImplementationTests(unittest.TestCase):
    def test_the_spell_corpus_rolls_through_the_magic_module(self) -> None:
        for die, skill, con, commits in ((1, 0, 10, False), (11, 2, 14, True), (20, 1, 18, False)):
            self.assertEqual(
                cwn_spells.overcast_roll(die=die, cast_skill=skill, constitution=con,
                                         commits_for_day=commits),
                cwn_magic.overcast_total(die=die, cast_skill=skill,
                                         constitution_mod=attribute_modifier(con),
                                         day_commitment=commits))

    def test_the_pool_and_the_standalone_total_agree(self) -> None:
        pool = cwn_magic.EffortPool(maximum=6)
        result = pool.overcast_roll(13, cast_skill=2, constitution_mod=1, day_commitment=False)
        self.assertEqual(result["total"], cwn_magic.overcast_total(die=13, cast_skill=2, constitution_mod=1))

    def test_the_bands_come_from_one_table(self) -> None:
        for total in range(1, 30):
            canonical = cwn_magic.overcast_result(total)
            published = cwn_spells.overcast_outcome(total)
            self.assertEqual(canonical["strain"], published["strain"], total)
            low, high, consequence = next(row for row in cwn_magic.OVERCAST_TABLE
                                          if row[2] == canonical["consequence"])
            self.assertEqual(published["band"], f"{low}-{high}" if high else f"{low}+")

    def test_the_spell_module_does_not_restate_the_table(self) -> None:
        source = inspect.getsource(cwn_spells)
        self.assertNotIn('"unconscious for one minute", "strain": 4', source)
        self.assertNotIn('"band": "5-8"', source)


class AttackModifiersHaveOneTableTests(unittest.TestCase):
    def test_the_module_loads_the_data_table(self) -> None:
        """Two byte-identical copies today; the point is that tomorrow there is one."""
        on_disk = json.loads((ROOT / "data/rules/wn_core.json").read_text(encoding="utf-8"))
        table = on_disk["combat"]["attack_modifiers"]["table"]
        self.assertEqual(cwn_attack_modifiers.ATTACK_MODIFIER_TABLE, table)
        source = inspect.getsource(cwn_attack_modifiers)
        self.assertNotIn('"target_half_cover": -2', source,
                         "the table must be loaded from data/, not transcribed into the module")


class AlienationHasOneTableTests(unittest.TestCase):
    def test_the_optional_module_reads_the_base_rules_table(self) -> None:
        self.assertEqual({name: row["max_bonus"] for name, row in cwn_alienation.SYNDROMES.items()},
                         {name: row["bonus"] for name, row in cwn_cyberware.SYNDROMES.items()})

    def test_stressed_is_worth_five_points_everywhere(self) -> None:
        """The drift this merge found: one module said +3, the SRD and cwn_cyberware say +5."""
        self.assertEqual(cwn_alienation.SYNDROMES["stressed"]["max_bonus"], 5)
        self.assertEqual(cwn_cyberware.SYNDROMES["stressed"]["bonus"], 5)

    def test_installing_chrome_costs_the_same_by_either_name(self) -> None:
        for strain, nerve in ((0.25, False), (1.0, False), (1.5, True), (2.0, False)):
            self.assertEqual(cwn_alienation.system_cost(strain, nerve=nerve),
                             cwn_cyberware.alienation_for_system(strain, nerve=nerve))

    def test_therapy_drops_the_same_point_by_either_name(self) -> None:
        for current, floor in ((5, 0), (5, 4), (3, 3), (9, 2)):
            self.assertEqual(cwn_alienation.Alienation(wisdom=12, score=current, floor=floor)
                             .therapy_week()["score"],
                             cwn_cyberware.therapy_week(current, floor))

    def test_the_base_rules_do_not_depend_on_the_optional_rule(self) -> None:
        self.assertNotIn("cwn_alienation", inspect.getsource(cwn_cyberware))


if __name__ == "__main__":
    unittest.main()
