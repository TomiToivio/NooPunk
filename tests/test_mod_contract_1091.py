"""The mod activation contract (#1091, ADR_1054 §2), enforced against the code it describes.

The registry says what each mod hooks, what state it owns, what it depends on, how it is switched off
and where its tabletop procedure lives. None of that is worth anything if it is only prose, so every
claim is checked against the files: a path must exist, a hook must appear in the implementation, an
off-switch must name something the code reads, and a mod with no printed procedure must say so out
loud. The mutations at the bottom are the real test — a validator that has never been handed a broken
registry has never been tested.
"""
import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from rules.mod_boundary import ModContractViolation, validate_registry  # noqa: E402
import check_mod_activation as tool  # noqa: E402

REGISTRY = ROOT / "data" / "mods" / "registry.json"


class ShippedRegistryTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.mods = self.data["mods"]

    def test_the_shipped_registry_satisfies_the_contract(self):
        self.assertEqual(validate_registry(self.mods, root=ROOT),
                         tuple(m["name"] for m in self.mods))

    def test_every_mod_declares_the_six_things(self):
        required = {"hooks", "state", "dependencies", "off_switch", "tabletop_procedure", "status"}
        for mod in self.mods:
            with self.subTest(mod=mod["name"]):
                self.assertTrue(required <= set(mod), f"missing {sorted(required - set(mod))}")

    def test_every_hook_is_a_callable_that_exists(self):
        for mod in self.mods:
            if mod["status"] != "implemented":
                continue
            text = "\n".join((ROOT / rel).read_text(encoding="utf-8", errors="ignore")
                             for rel in mod["implementation"])
            for hook in mod["hooks"]:
                with self.subTest(mod=mod["name"], hook=hook):
                    self.assertIn(hook.split(".")[-1], text)

    def test_a_documented_mod_names_no_code(self):
        documented = [m for m in self.mods if m["status"] == "documented"]
        self.assertTrue(documented, "at least one mod is documentation only; the schema must carry it")
        for mod in documented:
            self.assertEqual(mod["implementation"], [])

    def test_a_mod_without_a_procedure_records_the_gap(self):
        for mod in self.mods:
            with self.subTest(mod=mod["name"]):
                if mod["tabletop_procedure"]:
                    self.assertTrue((ROOT / mod["tabletop_procedure"]).is_file())
                else:
                    self.assertTrue(mod["tabletop_gap"].strip())

    def test_the_overlays_are_listed_and_point_at_real_files(self):
        overlays = self.data["overlays"]
        names = {m["name"] for m in self.mods}
        self.assertEqual({o["mod"] for o in overlays} - names, set())
        for overlay in overlays:
            with self.subTest(path=overlay["path"]):
                self.assertTrue((ROOT / overlay["path"]).is_file())
                self.assertIn(overlay["path"], (ROOT / "data/mods/registry.json").read_text()
                              .replace('"', "").replace("mods/", "mods/"))

    def test_the_tool_reports_and_exits_zero(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/check_mod_activation.py"), "--check"],
                                cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("have a printed procedure", result.stdout)


class BrokenContractTests(unittest.TestCase):
    """Give the validator something wrong to say."""

    def setUp(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.mods = copy.deepcopy(data["mods"])
        self.mod = self.mods[0]

    def assertViolation(self, needle: str):
        with self.assertRaises(ModContractViolation) as caught:
            validate_registry(self.mods, root=ROOT)
        self.assertIn(needle, str(caught.exception))

    def test_a_missing_declaration_is_refused(self):
        del self.mod["hooks"]
        self.assertViolation("does not declare")

    def test_a_hook_the_code_does_not_have_is_refused(self):
        self.mod["hooks"] = ["NoopunkPsyche.a_function_nobody_wrote"]
        self.assertViolation("appears in none")

    def test_an_implementation_path_that_does_not_exist_is_refused(self):
        self.mod["implementation"] = ["mods/noopunk/not_here.gd"]
        self.assertViolation("does not exist")

    def test_a_tabletop_procedure_that_does_not_exist_is_refused(self):
        self.mod["tabletop_procedure"] = "docs/tabletop/NOT_THERE.md"
        self.mod["tabletop_gap"] = None
        self.assertViolation("does not exist")

    def test_silence_about_a_missing_procedure_is_refused(self):
        self.mod["tabletop_procedure"] = None
        self.mod.pop("tabletop_gap", None)
        self.assertViolation("no recorded gap")

    def test_an_off_switch_nobody_reads_is_refused(self):
        self.mod["off_switch"] = {"kind": "flag", "name": "a_flag_no_code_reads"}
        self.assertViolation("not read by any implementation")

    def test_no_off_switch_needs_a_reason(self):
        self.mod["off_switch"] = {"kind": "none"}
        self.assertViolation("record the gap")

    def test_a_dependency_on_an_unknown_mod_is_refused(self):
        self.mod["dependencies"] = {"mods": ["a_mod_that_does_not_exist"], "contracts": [], "core": []}
        self.assertViolation("unknown mods")

    def test_a_dependency_contract_that_does_not_exist_is_refused(self):
        self.mod["dependencies"] = {"mods": [], "contracts": ["data/rules/nope.json"], "core": []}
        self.assertViolation("dependency does not exist")

    def test_documented_with_code_is_a_contradiction(self):
        documented = next(m for m in self.mods if m["status"] == "documented")
        documented["implementation"] = ["mud/nopunk_mud/social.py"]
        self.assertViolation("pick one")


class ReportTests(unittest.TestCase):
    def test_the_table_counts_what_the_registry_says(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        table = tool.rows(data, tool.test_corpus())
        self.assertEqual(len(table), len(data["mods"]))
        self.assertEqual(sum(1 for r in table if r["tabletop"]),
                         sum(1 for m in data["mods"] if m["tabletop_procedure"]))
        self.assertEqual(sum(1 for r in table if r["status"] == "implemented"),
                         sum(1 for m in data["mods"] if m["status"] == "implemented"))


if __name__ == "__main__":
    unittest.main()
