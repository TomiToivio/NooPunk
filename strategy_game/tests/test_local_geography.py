"""Executable contracts for the Ukweli local-geography record (issue #324).

Code-only, per `AGENTS.md` and issue #271. These exercise the **record and its validator** - the island
set, the single exclusion island, the naming registers and the still-open relations - and not any
prose. Almost every test below mutates a copy of the real record and demands that the specific defect
is *reported*, so a passing run means the shape was genuinely checked rather than assumed.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_local_geography.py"
"""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import local_geography as lg  # noqa: E402
from strategy_game.local_geography import (  # noqa: E402
    ACCESS_CLASSES,
    BOARD_PATH,
    DATA_PATH,
    GEOGRAPHY_FORMAT,
    GEOGRAPHY_VERSION,
    NODE_BUDGET,
    GeographyError,
    geography_from_dict,
    load_local_geography,
)


def _raw() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _board() -> dict:
    return json.loads(BOARD_PATH.read_text(encoding="utf-8"))


class ShippedRecordTests(unittest.TestCase):
    """The packaged record is readable and self-consistent."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_loads_and_declares_its_format(self) -> None:
        self.assertEqual(self.geography.format, GEOGRAPHY_FORMAT)
        self.assertEqual(self.geography.version, GEOGRAPHY_VERSION)

    def test_problems_are_empty(self) -> None:
        self.assertEqual(self.geography.problems(), ())

    def test_no_scale_is_approved(self) -> None:
        self.assertFalse(self.geography.numeric_scale_approved)

    def test_a_foreign_document_is_refused_by_the_loader(self) -> None:
        raw = _raw()
        raw["format"] = "noopunk.strategy_game.something_else"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "geography.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(GeographyError):
                load_local_geography(path)

    def test_a_missing_board_is_reported_by_the_loader(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(GeographyError):
                load_local_geography(board_path=Path(tmp) / "absent.json")

    def test_round_trip_is_lossless_for_the_validator(self) -> None:
        again = geography_from_dict(self.geography.to_dict(), _board())
        self.assertEqual(again.problems(), ())


class BoardCrossCheckTests(unittest.TestCase):
    """The record reads the live board rather than restating it."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_the_board_is_within_the_stated_node_envelope(self) -> None:
        low, high = NODE_BUDGET
        self.assertTrue(low <= len(self.geography.places) <= high)

    def test_every_declared_board_island_exists_on_the_board(self) -> None:
        on_board = {place.identifier for place in self.geography.places}
        for island in self.geography.islands:
            if island.on_playable_board:
                self.assertIn(island.identifier, on_board, island.identifier)

    def test_exactly_one_island_is_closed(self) -> None:
        self.assertEqual(len(self.geography.exclusion_islands), 1)

    def test_the_board_islands_match_the_declared_islands(self) -> None:
        declared = {island.identifier for island in self.geography.islands}
        on_board = {place.identifier for place in self.geography.board_islands}
        self.assertEqual(on_board, declared)

    def test_the_closed_board_node_is_the_declared_exclusion_island(self) -> None:
        declared = {island.identifier for island in self.geography.exclusion_islands}
        closed = {place.identifier for place in self.geography.board_exclusions}
        self.assertEqual(closed, declared)

    def test_every_access_class_is_a_declared_class(self) -> None:
        for place in self.geography.places:
            self.assertIn(place.access, ACCESS_CLASSES, place.identifier)


class IslandGapTests(unittest.TestCase):
    """The gaps issue #324 and #325 name are closed, and the closures are checked."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_the_board_carries_at_least_three_islands(self) -> None:
        """#325 'suggested initial state: 1 city + 3-4 islands'; #324 'multiple islands'."""
        self.assertGreaterEqual(len(self.geography.board_islands), 3)

    def test_the_exclusion_island_is_on_the_board(self) -> None:
        identifiers = {place.identifier for place in self.geography.board_islands}
        self.assertIn("exclusion_island", identifiers)

    def test_the_exclusion_island_is_the_restricted_one(self) -> None:
        place = self.geography.place("exclusion_island")
        self.assertIsNotNone(place)
        assert place is not None
        self.assertEqual(place.access, "restricted")
        self.assertTrue(place.is_exclusion)

    def test_the_other_islands_are_open(self) -> None:
        for place in self.geography.board_islands:
            if place.identifier != "exclusion_island":
                self.assertEqual(place.access, "open", place.identifier)

    def test_a_board_with_no_closed_island_is_reported(self) -> None:
        board = _board()
        for location in board["locations"]:
            location["access"] = "open"
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("board's closed nodes do not match" in p for p in problems))

    def test_two_declared_exclusion_islands_are_reported(self) -> None:
        raw = _raw()
        raw["islands"][0]["access"] = "prohibited"
        board = _board()
        board["locations"][5]["access"] = "prohibited"
        problems = geography_from_dict(raw, board).problems()
        self.assertTrue(any("exactly one restricted" in p for p in problems))

    def test_two_exclusion_islands_are_reported(self) -> None:
        board = _board()
        for location in board["locations"]:
            if location["id"] == "airfield_island":
                location["access"] = "prohibited"
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("board's closed nodes do not match" in p for p in problems))

    def test_a_board_beyond_the_node_cap_is_reported(self) -> None:
        board = _board()
        board["locations"].append({"id": "extra", "label": "Extra", "island": False, "access": "open"})
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("stated envelope" in p for p in problems))

    def test_an_island_absent_from_the_board_is_reported(self) -> None:
        board = _board()
        board["locations"] = [x for x in board["locations"] if x["id"] != "outer_island"]
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("absent from the board" in p for p in problems))


class NamingTests(unittest.TestCase):
    """The state-name conflict is closed as a register mapping, and never invented."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_the_official_name_is_declared_and_sourced(self) -> None:
        register = self.geography.name_register
        assert register is not None
        self.assertEqual(register.official, "People's Republic of Ukweli")
        self.assertTrue(register.official_source)

    def test_the_everyday_and_informal_registers_are_kept_apart(self) -> None:
        register = self.geography.name_register
        assert register is not None
        self.assertIn("Ukweli", register.everyday)
        self.assertEqual(register.informal, "Republic of Ukweli")
        self.assertTrue(register.register_mapping_recorded)

    def test_an_unsourced_official_name_is_reported(self) -> None:
        raw = _raw()
        raw["state_names"]["official_source"] = ""
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("without a cited source" in p for p in problems))

    def test_an_empty_official_name_is_reported(self) -> None:
        raw = _raw()
        raw["state_names"]["official"] = "   "
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("official name of the state is empty" in p for p in problems))

    def test_the_party_label_conflict_is_surfaced_and_not_resolved(self) -> None:
        labels = self.geography.unresolved_party_labels()
        self.assertEqual([label["id"] for label in labels], ["ulp"])
        self.assertEqual(labels[0]["data_name"], "Ukweli Libertarian Party")
        self.assertIn("LFP", labels[0]["setting_doc_name"])
        self.assertIn("requires author specification", labels[0]["todo"])


class OpenRelationTests(unittest.TestCase):
    """The island relation is carried as options, never silently settled."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_the_island_relation_is_declared_and_open(self) -> None:
        relation = self.geography.relation("eldrich_island_freedom_colony")
        self.assertIsNotNone(relation)
        assert relation is not None
        self.assertFalse(relation.resolved)
        self.assertEqual(relation.ruling_source, "")

    def test_the_island_relation_offers_the_three_options(self) -> None:
        relation = self.geography.relation("eldrich_island_freedom_colony")
        assert relation is not None
        self.assertEqual(len(relation.options), 3)
        self.assertTrue(any(option.startswith("same place") for option in relation.options))

    def test_a_silently_resolved_relation_is_reported(self) -> None:
        raw = _raw()
        raw["relations"][0]["resolved"] = True
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("without a cited author ruling" in p for p in problems))

    def test_an_unresolved_relation_without_options_is_reported(self) -> None:
        raw = _raw()
        raw["relations"][0]["options"] = []
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("declares no options" in p for p in problems))


class PendingDecisionTests(unittest.TestCase):
    """Every open question says why it is open."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_the_record_carries_open_decisions(self) -> None:
        self.assertTrue(self.geography.pending_decisions)

    def test_every_open_decision_states_its_reason(self) -> None:
        for decision in self.geography.pending_decisions:
            self.assertTrue(decision.why_not_decided, decision.identifier)
            self.assertTrue(decision.container_instead, decision.identifier)

    def test_a_decision_without_a_reason_is_reported(self) -> None:
        raw = _raw()
        raw["pending_author_decisions"][0]["why_not_decided"] = ""
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("must say WHY it is open" in p for p in problems))


class NoStatisticTests(unittest.TestCase):
    """No ordered or numeric quantity may appear anywhere in the record."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_no_forbidden_token_appears_among_the_record_keys(self) -> None:
        blob = json.dumps(self.geography.to_dict()).lower()
        for term in ("hegemony_score", "influence_track", "power_track", "victory_points"):
            self.assertNotIn(term, blob)

    def test_raising_the_scale_flag_is_reported(self) -> None:
        raw = _raw()
        raw["numeric_scale_approved"] = True
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("numeric_scale_approved is true" in p for p in problems))

    def test_a_numeric_looking_field_is_reported(self) -> None:
        raw = _raw()
        raw["party_labels"][0]["influence_rating"] = "high"
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("numeric-looking field" in p for p in problems))


class ScopeDirectiveTests(unittest.TestCase):
    """The strategy game stays standalone (issues #282/#299)."""

    def test_the_module_does_not_import_laclaugpt(self) -> None:
        source = Path(lg.__file__).read_text(encoding="utf-8")
        self.assertNotIn("laclaugpt", source.lower())

    def test_the_module_needs_no_optional_dependency(self) -> None:
        source = Path(lg.__file__).read_text(encoding="utf-8")
        for banned in ("pandas", "numpy", "networkx", "requests"):
            self.assertNotIn(f"import {banned}", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
