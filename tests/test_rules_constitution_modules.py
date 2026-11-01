"""Vanilla still runs with every overlay blocked — the executable half of the constitution (#1006).

The constitution says the minimum playable game is vanilla CWN + SWN psionics and that every NoöPunk
addition is an overlay. Prose cannot keep that promise, so this file does:

1. **Every rule module is classified exactly once**, and a baseline module never imports an overlay
   (`tools/rules_constitution_audit.py`, run here so CI sees it).
2. **The baseline runs in a subprocess whose import hook refuses every `noopunk-mod` module.** If the
   core ever grows a dependency on a mod, the test fails and names the module. A second test proves the
   hook bites, so the first cannot pass by importing nothing.
"""
from __future__ import annotations

import json
import subprocess
import sys
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "rules" / "rules_constitution.json"

sys.path.insert(0, str(ROOT / "tools"))
import rules_constitution_audit as audit  # noqa: E402


def _tiers() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))["module_tiers"]


class ConstitutionAuditTests(unittest.TestCase):
    def test_the_sources_are_ordered_cwn_first(self) -> None:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(data["precedence"][0], "CWN")
        self.assertEqual(data["minimum_playable"], ["CWN", "SWN"])

    def test_every_module_is_classified_exactly_once(self) -> None:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(audit.audit(data), [], "the constitution and the tree disagree")

    def test_the_vanilla_minimum_is_cwn_plus_swn_psionics(self) -> None:
        block = _tiers()
        self.assertEqual(block["vanilla_minimum"], ["cwn-core", "swn-companion"])
        tiers = {row["module"]: row["tier"] for row in block["modules"]}
        self.assertEqual(tiers["src/rules/swn_psionics.py"], "swn-companion")

    def test_the_baseline_is_the_largest_tier(self) -> None:
        """A constitution whose baseline is the smallest part would be a constitution about nothing."""
        tally = audit.counts(json.loads(REGISTRY.read_text(encoding="utf-8")))
        self.assertGreater(tally["cwn-core"], tally["noopunk-mod"])


VANILLA_SLICE = textwrap.dedent(
    '''
    """Run the CWN baseline with every overlay module blocked. Prints a JSON report."""
    import importlib.abc, json, sys

    BLOCKED = set(sys.argv[1].split(","))

    class RefuseOverlays(importlib.abc.MetaPathFinder):
        def find_spec(self, fullname, path=None, target=None):
            if fullname.rsplit(".", 1)[-1] in BLOCKED:
                raise ImportError(f"overlay blocked by the constitution: {fullname}")
            return None

    sys.meta_path.insert(0, RefuseOverlays())

    from src.rules.cwn_character import assign_array, effective_modifier
    from src.rules.wn_core import skill_check
    from src.rules.cwn_core import save_target, strain_maximum

    attributes = assign_array({"Strength": 14, "Dexterity": 12, "Constitution": 11,
                               "Intelligence": 10, "Wisdom": 9, "Charisma": 7})
    check = skill_check(attribute_score=attributes["Intelligence"], skill_level=1,
                        difficulty=8, dice=(3, 4))
    report = {
        "attributes": attributes,
        "strength_modifier": effective_modifier(attributes["Strength"]),
        "check_total": check.total,
        "check_success": check.success,
        "save_target_luck": save_target("Luck", level=1, attributes=attributes),
        "strain_maximum": strain_maximum(attributes["Constitution"]),
        "overlays_loaded": sorted(m for m in sys.modules if m.rsplit(".", 1)[-1] in BLOCKED),
    }
    print(json.dumps(report))
    '''
)


class VanillaPlayabilityTests(unittest.TestCase):
    def test_the_baseline_runs_with_every_overlay_blocked(self) -> None:
        block = _tiers()
        overlays = sorted(Path(row["module"]).stem for row in block["modules"]
                          if row["tier"] == block["overlay"])
        self.assertTrue(overlays, "the constitution must name the overlays it is blocking")

        completed = subprocess.run(
            [sys.executable, "-c", VANILLA_SLICE, ",".join(overlays)],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr[-2000:])
        report = json.loads(completed.stdout)

        self.assertEqual(report["attributes"]["Strength"], 14)
        self.assertEqual(report["strength_modifier"], 1)
        self.assertEqual(report["check_total"], 3 + 4 + 0 + 1)
        self.assertTrue(report["check_success"])
        self.assertEqual(report["save_target_luck"], 15, "16 minus level 1; Luck ignores attributes")
        self.assertEqual(report["strain_maximum"], report["attributes"]["Constitution"])
        self.assertEqual(report["overlays_loaded"], [], "a vanilla run loaded an overlay module")

    def test_an_overlay_really_is_blockable(self) -> None:
        """The hook must bite, or the test above proves only that nothing was imported."""
        block = _tiers()
        overlay = Path(next(r["module"] for r in block["modules"]
                            if r["tier"] == block["overlay"])).stem
        probe = textwrap.dedent(
            f'''
            import importlib.abc, sys
            class Refuse(importlib.abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname.rsplit(".", 1)[-1] == {overlay!r}:
                        raise ImportError("blocked")
            sys.meta_path.insert(0, Refuse())
            try:
                __import__("src.rules.{overlay}")
            except ImportError:
                print("blocked")
            else:
                print("loaded")
            '''
        )
        completed = subprocess.run([sys.executable, "-c", probe], cwd=ROOT,
                                   capture_output=True, text=True, timeout=60)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "blocked")


if __name__ == "__main__":
    unittest.main()
