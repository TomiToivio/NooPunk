"""Every mod declares its implementation, its printed procedure and its gap (#1080).

ADR_1054 lists what a mod must declare. This test holds the registry to that list: paths that exist,
a tabletop procedure that exists or a recorded reason why there is none, and a report that says out
loud how many mods still have no printed procedure. The mutations at the end are the important ones —
a validator that has never been given a broken registry is a validator nobody has checked.
"""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_mod_activation as contract  # noqa: E402


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "data" / "mods" / "registry.json").read_text(encoding="utf-8"))
        self.corpus = contract.test_corpus()

    def test_the_shipped_registry_passes(self):
        errors, _, rows = contract.audit(self.data, self.corpus)
        self.assertEqual(errors, [])
        self.assertTrue(rows)

    def test_every_mod_declares_its_implementation(self):
        for mod in self.data["mods"]:
            with self.subTest(mod=mod["name"]):
                self.assertIn("implementation", mod)

    def test_a_mod_without_a_printed_procedure_records_the_gap(self):
        for mod in self.data["mods"]:
            with self.subTest(mod=mod["name"]):
                self.assertTrue(mod.get("tabletop_procedure") or mod.get("tabletop_gap"),
                                "silence is not a decision")

    def test_the_report_counts_what_is_actually_implemented(self):
        _, _, rows = contract.audit(self.data, self.corpus)
        implemented = [r for r in rows if r["implemented"]]
        self.assertEqual(len(implemented), sum(1 for m in self.data["mods"] if m["implementation"]))
        self.assertLess(len(implemented), len(rows) + 1)

    def test_the_tool_exits_zero_on_the_shipped_registry(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools" / "check_mod_activation.py"), "--check"],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("have a printed procedure", result.stdout)


class BrokenRegistryTests(unittest.TestCase):
    """The validator, given something to complain about."""

    def setUp(self):
        self.data = json.loads((ROOT / "data" / "mods" / "registry.json").read_text(encoding="utf-8"))
        self.corpus = contract.test_corpus()

    def test_a_missing_implementation_path_is_an_error(self):
        data = copy.deepcopy(self.data)
        data["mods"][0]["implementation"] = ["mods/noopunk/not_a_module.gd"]
        errors, _, _ = contract.audit(data, self.corpus)
        self.assertTrue(any("does not exist" in e for e in errors), errors)

    def test_a_missing_tabletop_procedure_is_an_error(self):
        data = copy.deepcopy(self.data)
        data["mods"][0]["tabletop_procedure"] = "docs/tabletop/NOT_THERE.md"
        data["mods"][0]["tabletop_gap"] = None
        errors, _, _ = contract.audit(data, self.corpus)
        self.assertTrue(any("tabletop" in e for e in errors), errors)

    def test_silence_about_the_procedure_is_an_error(self):
        data = copy.deepcopy(self.data)
        data["mods"][0].pop("tabletop_procedure", None)
        data["mods"][0].pop("tabletop_gap", None)
        errors, _, _ = contract.audit(data, self.corpus)
        self.assertTrue(any("no recorded gap" in e for e in errors), errors)

    def test_an_old_schema_is_an_error(self):
        data = copy.deepcopy(self.data)
        data["schema"] = 1
        errors, _, _ = contract.audit(data, self.corpus)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
