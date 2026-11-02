"""Tests for the duplication audit and rules parity probe (#1053, #1054).

These pin the things that must stay true regardless of how the layers are later consolidated:

* the canonical CWN arithmetic (`attribute_modifier`, `save_target`) keeps the values the rules produce;
* every layer that implements `attribute_modifier` still agrees with the canonical one;
* both audit tools remain runnable, so the reports can be regenerated rather than hand-edited.

Deliberately *not* asserted: that `save_target`'s call contracts disagree across layers. They do today, and
`docs/RULES_PARITY_1053.md` reports it — but a test that fails the moment someone fixes the duplication would
punish the fix. Consolidation is tracked in #1053, not enforced here.
"""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import duplication_audit
import rules_parity_probe


def _load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module  # dataclasses look the module up while building
    spec.loader.exec_module(module)
    return module


class CanonicalArithmetic(unittest.TestCase):
    """The rules themselves, pinned against the book's bands rather than against another copy."""

    @classmethod
    def setUpClass(cls):
        cls.core = _load("src/rules/wn_core.py", "_t_wn_core")

    def test_attribute_modifier_bands(self):
        # CWN: 3 → −2, 4–7 → −1, 8–13 → 0, 14–17 → +1, 18 → +2.
        expected = {3: -2, 4: -1, 7: -1, 8: 0, 13: 0, 14: 1, 17: 1, 18: 2}
        for score, modifier in expected.items():
            with self.subTest(score=score):
                self.assertEqual(self.core.attribute_modifier(score), modifier)

    def test_attribute_modifier_rejects_out_of_range(self):
        for score in (2, 19):
            with self.subTest(score=score), self.assertRaises(ValueError):
                self.core.attribute_modifier(score)

    def test_save_target_is_sixteen_minus_level_minus_best_modifier(self):
        for level in range(1, 11):
            with self.subTest(level=level):
                target = self.core.save_target("physical", level=level,
                                               modifiers={"strength": 0, "constitution": 0})
                self.assertEqual(target, 16 - level)


class LayerAgreement(unittest.TestCase):
    """Every implementation of a rule must answer the same as the canonical one."""

    def test_attribute_modifier_agrees_in_every_layer(self):
        modules = rules_parity_probe.load_all()
        self.assertGreaterEqual(len([m for m in modules.values() if not isinstance(m, Exception)]), 3,
                                "expected to find several rules implementations to compare")

        comparison = rules_parity_probe.probe_attribute_modifiers(modules)
        reference = "src/rules/wn_core.py"
        self.assertIn(reference, comparison["table"])
        base = comparison["table"][reference]

        for relative, row in comparison["table"].items():
            if relative == reference or "_import" in row:
                continue
            differing = {score: value for score, value in row.items() if value != base.get(score)}
            with self.subTest(layer=relative):
                self.assertEqual(differing, {}, f"{relative} disagrees with the canonical attribute_modifier")


class AuditToolsRun(unittest.TestCase):
    """The reports are generated, so the generators have to keep working."""

    def test_duplication_audit_finds_the_known_duplicates(self):
        data = duplication_audit.build()
        names = {entry["name"] for entry in data["python_duplicates"]}
        for expected in ("attribute_modifier", "skill_check", "save_target"):
            with self.subTest(rule=expected):
                self.assertIn(expected, names)
        self.assertGreater(data["totals"]["redundant_copies"], 0)

    def test_duplication_audit_counts_only_module_level_rules(self):
        # A method called `to_dict` on two different classes is not a duplicated rule, and counting it as one
        # produced a headline number no reviewer should have trusted.
        data = duplication_audit.build()
        names = {entry["name"] for entry in data["python_duplicates"]}
        self.assertFalse(names & duplication_audit.GENERIC_NAMES)

    def test_parity_probe_compares_every_save_category(self):
        modules = rules_parity_probe.load_all()
        saves = rules_parity_probe.probe_saves(modules)
        self.assertTrue(saves)
        for relative, row in saves.items():
            with self.subTest(layer=relative):
                self.assertTrue(any(key.startswith("Luck/") for key in row),
                                "the Luck save is easy to forget because it has no attributes")


if __name__ == "__main__":
    unittest.main()
