"""Executable contracts for the Ukweli map specification (issue #325, deliverable 3).

Code-only, per `AGENTS.md` and issue #271. These exercise the **specification and its validator** -- the
node budget, route well-formedness, connectivity, island reachability and the deliberate absence of a
restricted playable node -- plus an anti-drift check binding the diagram document to the shipped data.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_map_spec.py"
"""

from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import map_spec as ms  # noqa: E402
from strategy_game.map_spec import (  # noqa: E402
    NODE_MAX,
    NODE_MIN,
    MapSpecError,
    load_map_spec,
    map_spec_from_dict,
)

DOC = ROOT / "docs" / "world" / "UKWELI_MAP_SPECIFICATION.md"


class ShippedMapTests(unittest.TestCase):
    """The packaged scenario map satisfies its own specification."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_map_spec()

    def test_it_reads_and_declares_a_known_format(self) -> None:
        self.assertTrue(self.spec.format.startswith(ms.DATA_FORMAT_PREFIX))

    def test_problems_is_clean(self) -> None:
        self.assertEqual(self.spec.problems(), ())

    def test_the_node_budget_is_respected(self) -> None:
        self.assertTrue(NODE_MIN <= len(self.spec.locations) <= NODE_MAX)
        self.assertEqual(len(self.spec.locations), 8)

    def test_a_foreign_document_is_refused(self) -> None:
        raw = json.loads(Path(ms.DATA_PATH).read_text(encoding="utf-8"))
        raw["format"] = "something.else"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "s.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(MapSpecError):
                load_map_spec(path)

    def test_round_trip_preserves_validity(self) -> None:
        self.assertEqual(map_spec_from_dict(self.spec.to_dict()).problems(), ())


class NodeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_map_spec()

    def test_node_ids_are_unique_and_lowercase(self) -> None:
        ids = self.spec.node_ids
        self.assertEqual(len(ids), len(set(ids)))
        for node_id in ids:
            self.assertEqual(node_id, node_id.lower())

    def test_every_node_declares_tags(self) -> None:
        for loc in self.spec.locations:
            self.assertTrue(loc.tags, loc.id)

    def test_islands_are_flagged_and_declared(self) -> None:
        self.assertEqual(set(self.spec.island_ids), {"outer_island", "airfield_island"})

    def test_no_node_introduces_a_scale_shaped_field(self) -> None:
        for loc in self.spec.locations:
            self.assertNotIn("distance", loc.detail)
            self.assertNotIn("weight", loc.detail)
            for key in loc.detail:
                self.assertFalse(any(t in key.lower() for t in ms._SCALE_TOKENS), key)


class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_map_spec()

    def test_a_route_is_a_pair_of_declared_nodes(self) -> None:
        for a, b in self.spec.routes:
            self.assertIn(a, self.spec.node_ids)
            self.assertIn(b, self.spec.node_ids)

    def test_the_graph_is_connected(self) -> None:
        reached = set(self.spec.reachable_from(self.spec.node_ids[0]))
        self.assertEqual(reached, set(self.spec.node_ids))

    def test_every_island_is_reachable(self) -> None:
        for island_id in self.spec.island_ids:
            self.assertTrue(self.spec.neighbours(island_id), island_id)

    def test_the_two_hubs_and_the_four_leaves(self) -> None:
        """The diagram's degree claim, checked against the data rather than asserted."""
        self.assertEqual(len(self.spec.neighbours("civic")), 3)
        self.assertEqual(len(self.spec.neighbours("old_harbor")), 3)
        leaves = [n for n in self.spec.node_ids if len(self.spec.neighbours(n)) == 1]
        self.assertEqual(sorted(leaves),
                         ["airfield_island", "campus", "coast", "outer_island"])

    def test_the_route_count_matches_the_diagram(self) -> None:
        self.assertEqual(len(self.spec.routes), 7)

    def test_this_module_knows_no_distance_or_cost(self) -> None:
        source = Path(ms.__file__).read_text(encoding="utf-8").lower()
        for banned in ("distance =", "cost =", "weight =", "kilometre", "km)"):
            self.assertNotIn(banned, source, banned)


class RestrictedIslandTests(unittest.TestCase):
    """The deliberate absence: the restricted island is not a playable node."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_map_spec()

    def test_no_playable_node_is_marked_restricted(self) -> None:
        self.assertEqual(self.spec.restricted_node_ids, ())

    def test_the_specification_explains_the_absence(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("restricted", text.lower())
        self.assertIn("out of the playable node budget", text)

    def test_the_absence_is_not_an_oversight_because_the_budget_is_full(self) -> None:
        self.assertEqual(len(self.spec.locations), NODE_MAX)


class DiagramAntiDriftTests(unittest.TestCase):
    """The diagram may not drift from the data, and must not add a ninth node."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = load_map_spec()
        cls.text = DOC.read_text(encoding="utf-8")

    def test_the_specification_document_exists(self) -> None:
        self.assertTrue(DOC.is_file())

    def test_the_node_table_lists_exactly_the_declared_nodes(self) -> None:
        """Rows of the node table are the ones whose second column is yes/no (the island flag)."""
        listed = set(re.findall(r"^\|\s*`([a-z_]+)`\s*\|\s*\**(?:yes|no)\**\s*\|",
                                self.text, flags=re.MULTILINE))
        self.assertEqual(listed, set(self.spec.node_ids))

    def test_every_declared_node_appears_in_the_diagram(self) -> None:
        for node_id in self.spec.node_ids:
            self.assertIn(node_id, self.text, node_id)

    def test_the_document_claims_no_node_outside_the_budget(self) -> None:
        self.assertIn(str(NODE_MAX), self.text)
        self.assertNotIn("nine playable", self.text.lower())

    def test_the_document_leaves_the_restricted_decision_open(self) -> None:
        self.assertIn("open question", self.text.lower())


class MalformedRootTests(unittest.TestCase):
    """The map loader refuses a foreign root type with its own error, not an AttributeError."""

    def test_a_non_object_root_is_refused_cleanly(self) -> None:
        import tempfile

        for raw in ("[]", "null", '"map"', "7"):
            with self.subTest(root=raw), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "map.json"
                path.write_text(raw, encoding="utf-8")
                with self.assertRaisesRegex(ms.MapSpecError, "must contain a JSON object"):
                    ms.load_map_spec(path)


class ValidatorTests(unittest.TestCase):
    """The validator reports rather than raises."""

    def _mutated(self, mutate) -> "ms.MapSpec":
        raw = json.loads(Path(ms.DATA_PATH).read_text(encoding="utf-8"))
        mutate(raw)
        return map_spec_from_dict(raw)

    def test_a_ninth_node_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw["locations"].append(
            {"id": "ninth", "label": "Ninth", "tags": ["x"], "island": False}))
        self.assertTrue(any("budget" in p for p in bad.problems()))

    def test_a_dangling_route_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw["routes"].append(["civic", "nowhere"]))
        self.assertTrue(any("not a declared node" in p for p in bad.problems()))

    def test_a_self_loop_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw["routes"].append(["civic", "civic"]))
        self.assertTrue(any("self-loop" in p for p in bad.problems()))

    def test_a_duplicate_route_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw["routes"].append(["civic", "residential"]))
        self.assertTrue(any("duplicate route" in p for p in bad.problems()))

    def test_a_disconnected_node_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw.__setitem__(
            "routes", [r for r in raw["routes"] if "coast" not in r]))
        self.assertTrue(any("unreachable" in p for p in bad.problems()))

    def test_an_island_with_no_route_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw.__setitem__(
            "routes", [r for r in raw["routes"] if "airfield_island" not in r]))
        self.assertTrue(any("no route" in p for p in bad.problems()))

    def test_a_node_without_tags_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw["locations"][0].__setitem__("tags", []))
        self.assertTrue(any("no tags" in p for p in bad.problems()))

    def test_a_restricted_playable_node_is_reported(self) -> None:
        bad = self._mutated(lambda raw: raw["locations"][0].__setitem__(
            "tags", raw["locations"][0]["tags"] + ["restricted"]))
        self.assertTrue(any("declared restricted" in p for p in bad.problems()))


class ScopeTests(unittest.TestCase):
    def test_the_module_needs_no_optional_dependency(self) -> None:
        source = Path(ms.__file__).read_text(encoding="utf-8")
        for banned in ("numpy", "pandas", "requests", "ollama", "openai", "networkx"):
            self.assertNotIn(f"import {banned}", source)

    def test_the_module_imports_no_laclaugpt_code(self) -> None:
        self.assertNotIn("laclaugpt", Path(ms.__file__).read_text(encoding="utf-8").lower())

    def test_the_module_proposes_no_mechanic(self) -> None:
        source = Path(ms.__file__).read_text(encoding="utf-8").split('"""', 2)[-1]
        for banned in ("threshold", "win_condition", "turn_economy", "movement_cost"):
            self.assertNotIn(banned, source, banned)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
