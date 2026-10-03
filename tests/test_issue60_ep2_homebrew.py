"""Issue #60: tests for the EP2 homebrew Concordia prototype."""

from __future__ import annotations

from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime.ep2_adapter import resolve_ep2_action
from eclipse_phase_homebrew import EP2Character, EP2PoolState, PoolKind, PoolSpend, resolve_test


class EP2HomebrewTests(unittest.TestCase):
    def test_basic_d100_success_and_failure(self) -> None:
        self.assertTrue(resolve_test(target=60, roll=42).success)
        self.assertFalse(resolve_test(target=60, roll=73).success)

    def test_33_66_superior_success_rule(self) -> None:
        self.assertEqual(resolve_test(target=90, roll=40).superior_successes, 1)
        self.assertEqual(resolve_test(target=90, roll=70).superior_successes, 2)

    def test_critical_doubles_and_absolute_00_99(self) -> None:
        self.assertTrue(resolve_test(target=30, roll=22).critical_success)
        self.assertTrue(resolve_test(target=0, roll=0).critical_success)
        self.assertTrue(resolve_test(target=100, roll=99).critical_failure)

    def test_defaulting_suppresses_critical_success(self) -> None:
        result = resolve_test(target=50, roll=22, defaulted=True)
        self.assertTrue(result.success)
        self.assertFalse(result.critical_success)

    def test_modifiers_are_capped_at_sixty(self) -> None:
        result = resolve_test(target=40, modifier=999, roll=90)
        self.assertEqual(result.modifier, 60)
        self.assertEqual(result.target, 100)
        self.assertTrue(result.success)

    def test_pool_spend_consumes_point_and_adds_twenty(self) -> None:
        pools = EP2PoolState(maximum={PoolKind.INSIGHT: 2}, current={PoolKind.INSIGHT: 2})
        result = resolve_test(target=50, roll=65, pools=pools,
                              pool_kind=PoolKind.INSIGHT, pool_spend=PoolSpend.ADD_20)
        self.assertTrue(result.success)
        self.assertEqual(pools.current[PoolKind.INSIGHT], 1)

    def test_flip_flop(self) -> None:
        pools = EP2PoolState(maximum={PoolKind.FLEX: 1})
        result = resolve_test(target=50, roll=73, pools=pools,
                              pool_kind=PoolKind.FLEX, pool_spend=PoolSpend.FLIP_FLOP)
        self.assertEqual(result.roll, 37)
        self.assertTrue(result.success)

    def test_concordia_adapter_uses_skill(self) -> None:
        character = EP2Character(name="prototype", skills={"Infosec": 65}, aptitudes={"COG": 20})
        result = resolve_ep2_action(character=character,
                                    action={"skill": "Infosec", "aptitude": "COG"}, roll=50)
        self.assertTrue(result["success"])
        self.assertEqual(result["character"], "prototype")

    def test_concordia_adapter_defaults_to_aptitude(self) -> None:
        character = EP2Character(name="prototype", skills={}, aptitudes={"REF": 25})
        result = resolve_ep2_action(character=character,
                                    action={"skill": "Guns", "aptitude": "REF"}, roll=20)
        self.assertTrue(result["defaulted"])
        self.assertTrue(result["success"])

    def test_license_and_provenance_docs_exist(self) -> None:
        self.assertTrue((ROOT / "docs/licenses/ECLIPSE_PHASE_HOMEBREW.md").exists())
        self.assertTrue((ROOT / "docs/sources/EP2_HOME_BREW_SOURCES.md").exists())


if __name__ == "__main__":
    unittest.main()
