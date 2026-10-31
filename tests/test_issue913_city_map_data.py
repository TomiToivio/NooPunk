"""#913: the Helsinki map is data, so the data needs a guard outside Godot.

`godot/tests/test_helsinki_913.gd` proves the behaviour: two nodes at the start, the rest absent, travel,
save and restore. This file proves the *data contract* underneath it, in the CI job that runs Python —
so a node flipped to `requires: []`, an id that drifts away from the issue's stable vocabulary, a
coordinate off the panel, or a place with no declared artwork fails without anyone opening Godot.

It also closes the gap #913 leaves open between the map and #908's image pipeline: every node must name
its illustration, and that artwork must exist in `images/manifest.json` — as a pending request while it
does not exist yet, as an approved asset once it does. A place with no entry is art debt nobody can see.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "world" / "helsinki_locations.json"
MANIFEST = ROOT / "images" / "manifest.json"

STARTERS = ("home_helsinginkatu", "unsa_hq_ratakatu")
EARLY = ("olutravintola_putki", "university_of_helsinki", "kurvi")
UNDERGROUND = "unsa_underground"

#: Words that would mean speculative scenery leaked into ordinary Helsinki (#908's rule, in prose).
SCI_FI_WORDS = ("hovering", "flying car", "saucer", "neon", "skyline", "megastructure",
                "spaceship", "starship")


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


def nodes() -> dict[str, dict]:
    return {str(node["id"]): node for node in load()["nodes"]}


def manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


class ShapeTests(unittest.TestCase):
    def test_the_map_is_helsinki_and_starts_at_home(self):
        data = load()
        self.assertEqual(data.get("start"), "home_helsinginkatu")

    def test_the_issue_s_stable_ids_all_exist(self):
        present = nodes()
        for node_id in STARTERS + EARLY + (UNDERGROUND,):
            with self.subTest(node=node_id):
                self.assertIn(node_id, present, "the issue names this id; a rename orphans saves")

    def test_ids_are_unique_snake_case(self):
        ids = [str(node["id"]) for node in load()["nodes"]]
        self.assertEqual(len(ids), len(set(ids)))
        for node_id in ids:
            self.assertEqual(node_id, node_id.lower(), node_id)
            self.assertNotIn(" ", node_id)

    def test_every_node_has_label_text_actions_and_placement(self):
        for node_id, node in nodes().items():
            with self.subTest(node=node_id):
                for field in ("name", "district", "description", "actions", "map_position",
                              "illustration"):
                    self.assertIn(field, node, f"{node_id} is missing {field}")
                self.assertTrue(str(node["name"]).strip())
                self.assertTrue(node["actions"])

    def test_map_positions_are_normalised_pairs(self):
        for node_id, node in nodes().items():
            with self.subTest(node=node_id):
                position = node["map_position"]
                self.assertEqual(len(position), 2, f"{node_id}: expected [x, y]")
                for value in position:
                    self.assertTrue(0.0 <= float(value) <= 1.0, f"{node_id}: {position}")

    def test_home_is_east_of_the_office(self):
        """Helsinginkatu is in Kallio, Ratakatu in Punavuori: the map must not mirror the city."""
        table = nodes()
        self.assertGreater(float(table["home_helsinginkatu"]["map_position"][0]),
                           float(table["unsa_hq_ratakatu"]["map_position"][0]))


class SpoilerTests(unittest.TestCase):
    def test_only_the_two_starters_are_ungated(self):
        open_nodes = [node_id for node_id, node in nodes().items()
                      if not node.get("requires")]
        self.assertEqual(sorted(open_nodes), sorted(STARTERS))

    def test_the_start_is_a_starter(self):
        self.assertIn(load()["start"], STARTERS)

    def test_early_follow_ups_need_a_named_flag(self):
        table = nodes()
        for node_id in EARLY:
            with self.subTest(node=node_id):
                requires = table[node_id].get("requires") or []
                self.assertTrue(requires, f"{node_id} would appear on the opening map")
                for flag in requires:
                    self.assertTrue(str(flag).strip(), f"{node_id} has a blank requirement")

    def test_the_underground_waits_for_clearance(self):
        deep = nodes()[UNDERGROUND]
        requires = [str(flag) for flag in deep.get("requires") or []]
        self.assertTrue(requires, "the bunker must not be reachable without a story milestone")
        self.assertTrue(any("clearance" in flag or "underground" in flag for flag in requires),
                        f"expected an explicit clearance gate, found {requires}")

    def test_the_starters_say_the_pc_arrived_yesterday(self):
        home = str(nodes()["home_helsinginkatu"]["description"]).lower()
        self.assertIn("yesterday", home)
        self.assertIn("helsinginkatu", home)

    def test_the_office_names_its_overlapping_authorities(self):
        summary = str(nodes()["unsa_hq_ratakatu"]["description"]).lower()
        for word in ("suojelupoliisi", "europol", "unsa"):
            self.assertIn(word, summary, f"the HQ description should name {word}")

    def test_no_speculative_scenery_in_any_description(self):
        for node_id, node in nodes().items():
            with self.subTest(node=node_id):
                text = str(node["description"]).lower()
                for word in SCI_FI_WORDS:
                    self.assertNotIn(word, text, f"{node_id} describes {word!r} in ordinary Helsinki")


class ArtDebtTests(unittest.TestCase):
    """#913 asks for artwork in the right image class with provenance; #908 keeps the ledger."""

    def test_every_node_names_an_illustration_in_the_location_class(self):
        for node_id, node in nodes().items():
            with self.subTest(node=node_id):
                path = str(node["illustration"])
                self.assertTrue(path.startswith("res://images/locations/"),
                                f"{node_id}: {path!r} belongs in the locations class")
                self.assertTrue(path.endswith(".png"), f"{node_id}: {path!r}")

    def test_every_node_s_artwork_is_in_the_manifest(self):
        if not MANIFEST.exists():
            self.skipTest("no image manifest in this tree")
        listed = {str(entry.get("id", "")) for entry in manifest().get("assets", [])}
        listed |= {str(entry.get("id", "")) for entry in manifest().get("pending", [])}
        for node_id, node in nodes().items():
            with self.subTest(node=node_id):
                stem = Path(str(node["illustration"]).removeprefix("res://images/")).stem
                self.assertIn(stem, listed,
                              f"{stem} is required by {node_id} but missing from images/manifest.json")

    def test_the_manifest_agrees_with_the_node_path(self):
        pending = {str(entry.get("id", "")): entry for entry in manifest().get("pending", [])}
        approved = {str(entry.get("id", "")): entry for entry in manifest().get("assets", [])}
        for node_id, node in nodes().items():
            stem = Path(str(node["illustration"]).removeprefix("res://images/")).stem
            entry = approved.get(stem) or pending.get(stem)
            with self.subTest(node=node_id):
                self.assertIsNotNone(entry, f"{stem} is not in the manifest")
                self.assertEqual(entry["target_path"] if "target_path" in entry else entry["path"],
                                 node["illustration"],
                                 f"{stem}: the manifest and the map disagree about the path")

    def test_location_art_claims_no_unsolicited_science_fiction(self):
        for entry in manifest().get("pending", []) + manifest().get("assets", []):
            if not str(entry.get("category", "")).startswith("locations"):
                continue
            with self.subTest(asset=entry.get("id")):
                self.assertFalse(entry.get("sci_fi_motifs"),
                                 f"{entry.get('id')}: Helsinki location art stays ordinary")

    def test_no_location_art_is_approved_before_it_exists(self):
        """An approved asset with no bytes is refused by the #908 validator; keep the two consistent."""
        for entry in manifest().get("assets", []):
            if not str(entry.get("category", "")).startswith("locations"):
                continue
            with self.subTest(asset=entry.get("id")):
                path = ROOT / "images" / str(entry["path"]).removeprefix("res://images/")
                self.assertTrue(path.is_file(), f"{entry.get('id')}: approved but not committed")


if __name__ == "__main__":
    unittest.main()
