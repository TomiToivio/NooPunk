"""Executable contracts for the Ukweli local-geography record (issue #324).

Code-only, per `AGENTS.md` and issue #271. These exercise the **record and its validator** - the island
set, the single exclusion island, the naming registers and the still-open relations - and not any
prose. Almost every test below mutates a copy of the real record or the real board and demands that the
specific defect is *reported*, so a passing run means the shape was genuinely checked rather than
assumed.

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

    def test_the_board_is_not_restated_from_the_record(self) -> None:
        """The places come from the board file, so their ids are the board's own ids."""
        board_ids = {item["id"] for item in _board()["locations"]}
        self.assertEqual(set(self.geography.board_ids), board_ids)

    def test_every_declared_playable_island_exists_on_the_board(self) -> None:
        for island in self.geography.board_islands:
            self.assertTrue(self.geography.on_board(island.identifier), island.identifier)

    def test_no_declared_off_board_island_exists_on_the_board(self) -> None:
        for island in self.geography.off_board_islands:
            self.assertFalse(self.geography.on_board(island.identifier), island.identifier)

    def test_the_board_marks_the_playable_islands(self) -> None:
        for island in self.geography.board_islands:
            place = self.geography.place(island.identifier)
            assert place is not None
            self.assertIs(place.island, True, island.identifier)

    def test_an_unrecorded_board_marker_stays_unknown(self) -> None:
        """Absence is unrecorded, never read as 'not an island'."""
        board = _board()
        for location in board["locations"]:
            location.pop("island", None)
        geography = geography_from_dict(_raw(), board)
        for place in geography.places:
            self.assertIsNone(place.island)
        self.assertEqual(geography.problems(), ())


class IslandGapTests(unittest.TestCase):
    """The gaps issue #324 and #325 name are closed as structure, and the closures are checked."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.geography = load_local_geography()

    def test_the_record_declares_three_islands(self) -> None:
        """#325 / the setting bible: one city plus 3-4 islands, one marked restricted."""
        low, high = self.geography.island_envelope
        self.assertTrue(low <= self.geography.island_count_declared <= high)
        self.assertGreaterEqual(self.geography.island_count_declared, 3)

    def test_the_exclusion_island_is_declared_and_restricted(self) -> None:
        island = self.geography.declared_island("exclusion_island")
        self.assertIsNotNone(island)
        assert island is not None
        self.assertEqual(island.access, "restricted")
        self.assertTrue(island.is_exclusion)

    def test_the_exclusion_island_is_recorded_off_the_board_with_a_reason(self) -> None:
        """It is canon, and it is not playable: the record says so instead of folding a node away."""
        island = self.geography.declared_island("exclusion_island")
        assert island is not None
        self.assertFalse(island.on_playable_board)
        self.assertTrue(island.absent_reason.strip())
        self.assertIn(island, self.geography.off_board_islands)

    def test_the_other_declared_islands_are_open(self) -> None:
        for island in self.geography.islands:
            if island.identifier != "exclusion_island":
                self.assertEqual(island.access, "open", island.identifier)

    def test_the_playable_island_count_matches_the_board(self) -> None:
        self.assertEqual(self.geography.island_count_on_board, len(self.geography.board_islands))
        self.assertEqual(self.geography.island_count_on_board, 2)

    def test_two_declared_exclusion_islands_are_reported(self) -> None:
        raw = _raw()
        raw["islands"][0]["access"] = "prohibited"
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("exactly one restricted" in p for p in problems))

    def test_an_unknown_access_class_is_reported(self) -> None:
        raw = _raw()
        raw["islands"][0]["access"] = "shut"
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("access 'shut' not in" in p for p in problems))

    def test_a_board_beyond_the_node_cap_is_reported(self) -> None:
        board = _board()
        board["locations"].append({"id": "extra", "label": "Extra", "island": False})
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("stated envelope" in p for p in problems))

    def test_an_island_declared_playable_but_absent_is_reported(self) -> None:
        board = _board()
        board["locations"] = [x for x in board["locations"] if x["id"] != "outer_island"]
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("absent from the board" in p for p in problems))

    def test_an_off_board_island_without_a_reason_is_reported(self) -> None:
        raw = _raw()
        raw["islands"][2]["absent_reason"] = ""
        problems = geography_from_dict(raw, _board()).problems()
        self.assertTrue(any("without a reason" in p for p in problems))

    def test_a_board_denying_a_declared_island_is_reported(self) -> None:
        board = _board()
        for location in board["locations"]:
            if location["id"] == "outer_island":
                location["island"] = False
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("denies island status" in p for p in problems))

    def test_a_board_marking_an_undeclared_island_is_reported(self) -> None:
        board = _board()
        for location in board["locations"]:
            if location["id"] == "civic":
                location["island"] = True
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("no island is declared for it" in p for p in problems))

    def test_a_board_access_marker_disagreeing_with_the_record_is_reported(self) -> None:
        board = _board()
        for location in board["locations"]:
            if location["id"] == "outer_island":
                location["access"] = "restricted"
        problems = geography_from_dict(_raw(), board).problems()
        self.assertTrue(any("declares access 'restricted'" in p for p in problems))


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

    def test_the_island_placement_question_is_carried_open(self) -> None:
        identifiers = {decision.identifier for decision in self.geography.pending_decisions}
        self.assertIn("restricted_island_placement", identifiers)

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

    def test_no_access_class_is_a_number(self) -> None:
        for access in ACCESS_CLASSES:
            self.assertIsInstance(access, str)


class CopySafetyTests(unittest.TestCase):
    """The fixtures above must not be mutating the shipped records."""

    def test_the_shipped_records_are_unchanged_by_the_suite(self) -> None:
        raw = _raw()
        board = _board()
        geography = load_local_geography()
        self.assertEqual(len(geography.places), len(board["locations"]))
        self.assertEqual(geography.problems(), ())
        self.assertEqual(json.loads(DATA_PATH.read_text(encoding="utf-8")), raw)


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
