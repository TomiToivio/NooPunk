"""The rules constitution is enforced, not just written down (#1006).

A governance document that nothing checks is a wish. These tests make the constitution fail loudly when it is
contradicted:

* a layer may not claim a status it cannot evidence (a path that exists),
* an "implemented" layer must name a test that exists,
* the vanilla profile may not contain an overlay,
* an overlay may not grow its own attribute set, skill list or difficulty ladder,
The repository forbids tests on prose, lore or wording, so this file deliberately checks **data and code**: the
JSON's claims against the filesystem, the profiles, and what overlay source files are allowed to contain. It does
not assert anything about how the constitution is phrased.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = ROOT / "data" / "rules" / "rules_constitution.json"
STATUSES = {"implemented", "partial", "planned", "data-only"}
OVERLAY_DIRS = ("mods/noopunk",)


def load() -> dict:
    return json.loads(CONSTITUTION.read_text())


def layers(data: dict):
    for group in data["layers"].values():
        yield from group


class TheDocumentItself(unittest.TestCase):
    def test_the_constitution_is_locked_and_names_its_issue(self):
        data = load()
        self.assertTrue(data["locked"])
        self.assertEqual(data["issue"], 1006)
        self.assertEqual(data["precedence"][0], "cwn", "CWN must win where sources disagree")

    def test_the_author_statement_is_quoted_verbatim(self):
        data = load()
        statement = data["author_statement"]
        self.assertIn("all CWN rules", statement)
        self.assertIn("many SWN rules", statement)
        self.assertIn("on top of plain vanilla", statement)



class StatusesAreEvidenced(unittest.TestCase):
    def test_every_status_is_one_of_the_four(self):
        for layer in layers(load()):
            with self.subTest(layer=layer["id"]):
                self.assertIn(layer["status"], STATUSES)

    def test_implemented_and_partial_layers_point_at_files_that_exist(self):
        for layer in layers(load()):
            if layer["status"] in {"implemented", "partial", "data-only"}:
                self.assertTrue(layer["paths"], f"{layer['id']} claims {layer['status']} with no paths")
            for path in layer["paths"] + layer["tests"]:
                with self.subTest(layer=layer["id"], path=path):
                    self.assertTrue((ROOT / path).exists(), f"{layer['id']} references a missing file: {path}")

    def test_implemented_layers_name_a_test_that_exists(self):
        for layer in layers(load()):
            if layer["status"] == "implemented":
                with self.subTest(layer=layer["id"]):
                    self.assertTrue(layer["tests"], f"{layer['id']} claims implemented with no test")
                    for path in layer["tests"]:
                        self.assertTrue((ROOT / path).exists())

    def test_planned_layers_have_no_paths(self):
        """A planned module with files is a module whose status is lying."""
        for layer in layers(load()):
            if layer["status"] == "planned":
                with self.subTest(layer=layer["id"]):
                    self.assertEqual(layer["paths"], [])


class Profiles(unittest.TestCase):
    def test_vanilla_contains_the_core_and_nothing_else(self):
        data = load()
        vanilla = data["profiles"]["vanilla-cwn"]["layers"]
        self.assertEqual(vanilla, ["cwn-core"])

    def test_the_minimum_profile_is_cwn_plus_psionics(self):
        data = load()
        self.assertEqual(data["profiles"]["minimum-playable"]["layers"], ["cwn-core", "swn-psionics"])

    def test_every_profile_layer_exists(self):
        data = load()
        ids = {layer["id"] for layer in layers(data)}
        for name, profile in data["profiles"].items():
            for layer_id in profile["layers"]:
                with self.subTest(profile=name, layer=layer_id):
                    self.assertIn(layer_id, ids)


class OverlaysAreOverlays(unittest.TestCase):
    """An overlay asks the core for a roll. It does not own dice, attributes or difficulty bands."""

    ATTRIBUTE_SET = re.compile(r"\b(STRENGTH|DEXTERITY|CONSTITUTION|INTELLIGENCE|WISDOM|CHARISMA)\b")
    DEFINES_ATTRIBUTES = re.compile(r"(?i)const\s+\w*(attributes|skills)\w*\s*[:=]|(attributes|skills)\s*:=\s*\[")
    DIFFICULTY_TABLE = re.compile(r"(?i)\b(easy|routine|hard|very_hard|heroic)\b\s*[:=]\s*(6|8|10|12|14)")

    def overlay_files(self):
        for directory in OVERLAY_DIRS:
            yield from sorted((ROOT / directory).glob("*.gd"))

    def test_an_overlay_does_not_define_an_attribute_set(self):
        for path in self.overlay_files():
            text = path.read_text(errors="ignore")
            with self.subTest(file=path.name):
                self.assertIsNone(self.DEFINES_ATTRIBUTES.search(text),
                                  f"{path.name} declares its own attributes/skills; that is a core, not an overlay")

    def test_an_overlay_does_not_define_its_own_difficulty_bands(self):
        for path in self.overlay_files():
            text = path.read_text(errors="ignore")
            with self.subTest(file=path.name):
                self.assertIsNone(self.DIFFICULTY_TABLE.search(text),
                                  f"{path.name} re-declares CWN difficulty bands")

    def test_overlays_do_not_import_each_other(self):
        names = [p.stem for p in self.overlay_files()]
        for path in self.overlay_files():
            text = path.read_text(errors="ignore")
            for other in names:
                if other == path.stem:
                    continue
                with self.subTest(file=path.name, other=other):
                    self.assertNotIn(f'"{other}', text,
                                     f"{path.name} depends on {other}: overlays must be independently loadable")


if __name__ == "__main__":
    unittest.main()
