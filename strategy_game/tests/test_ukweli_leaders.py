"""Executable contracts for the Ukweli leader roster (issue #326).

Code-only, per `AGENTS.md` and issue #271. These exercise the **roster and its validator** -- the
dynasty's eras, the twelve seats, the declared blanks and the referential integrity to the records
that already exist -- and not any lore wording.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_ukweli_leaders.py"
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game import leaders as ldr  # noqa: E402
from strategy_game.leaders import (  # noqa: E402
    ERAS,
    PORTFOLIOS,
    ROSTER_FORMAT,
    LeaderRoster,
    RosterError,
    load_card_identifiers,
    load_local_leaders,
    load_ukweli_leaders,
    roster_from_dict,
)


class ShippedRosterTests(unittest.TestCase):
    """The packaged roster is readable and self-consistent."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roster = load_ukweli_leaders()

    def test_loads_and_declares_its_format(self) -> None:
        self.assertEqual(self.roster.format, ROSTER_FORMAT)

    def test_off_vocabulary_is_clean(self) -> None:
        self.assertEqual(self.roster.off_vocabulary(), ())

    def test_a_foreign_document_is_refused_by_the_loader(self) -> None:
        raw = json.loads(ldr.DATA_PATH.read_text(encoding="utf-8"))
        raw["format"] = "noopunk.strategy_game.something_else"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "roster.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(RosterError):
                load_ukweli_leaders(path)

    def test_non_object_json_root_is_refused_cleanly(self) -> None:
        for raw in ([], None, "not a roster", 42):
            with self.subTest(root=raw), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "roster.json"
                path.write_text(json.dumps(raw), encoding="utf-8")
                with self.assertRaisesRegex(RosterError, "must contain a JSON object"):
                    load_ukweli_leaders(path)

    def test_round_trip_is_lossless_for_the_validator(self) -> None:
        again = roster_from_dict(self.roster.to_dict())
        self.assertEqual(again.off_vocabulary(), ())

    def test_marks_itself_a_proposal(self) -> None:
        self.assertIn("PROPOSAL", self.roster.status)


class DynastyEraTests(unittest.TestCase):
    """Uranus and Mercury are historical and invocable; only Mars is present."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roster = load_ukweli_leaders()

    def test_three_generations_present(self) -> None:
        self.assertEqual(
            set(self.roster.people),
            {"sir_uranus_eldrich", "sir_mercury_eldrich", "sir_mars_eldrich"},
        )

    def test_every_era_is_a_declared_era(self) -> None:
        for person in self.roster.people.values():
            self.assertIn(person.era, ERAS, person.person_ref)

    def test_uranus_and_mercury_are_historical_and_not_agentic(self) -> None:
        for ref in ("sir_uranus_eldrich", "sir_mercury_eldrich"):
            person = self.roster.people[ref]
            self.assertEqual(person.era, "historical", ref)
            self.assertFalse(person.is_agentic, ref)

    def test_only_mars_is_present(self) -> None:
        present = [p.person_ref for p in self.roster.people.values() if p.is_agentic]
        self.assertEqual(present, ["sir_mars_eldrich"])
        self.assertEqual(len(self.roster.historical()), 2)

    def test_mars_is_a_patron_and_not_automatically_a_council_seat(self) -> None:
        mars = self.roster.people["sir_mars_eldrich"]
        self.assertFalse(mars.holds_council_seat)
        self.assertIn("independent patron", mars.role)

    def test_1964_stays_peaceful_and_cpu_led(self) -> None:
        mercury = self.roster.people["sir_mercury_eldrich"]
        invariants = " ".join(mercury.canon_invariants).lower()
        self.assertIn("1964", invariants)
        self.assertIn("peaceful", invariants)
        self.assertIn("cpu-led", invariants)

    def test_historical_generations_carry_no_live_card(self) -> None:
        for person in self.roster.historical():
            self.assertEqual(person.card_ref, "", person.person_ref)

    def test_every_person_distinguishes_evidence_classes(self) -> None:
        for person in self.roster.people.values():
            self.assertTrue(person.evidence_classes, person.person_ref)
            self.assertTrue(person.must_not_assert, person.person_ref)


class SeatTests(unittest.TestCase):
    """Twelve seats, four per faction, four portfolios, and none of them filled."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roster = load_ukweli_leaders()

    def test_twelve_seats_four_per_faction(self) -> None:
        self.assertEqual(len(self.roster.seats), 12)
        for faction in ldr.FACTION_IDS:
            self.assertEqual(len(self.roster.seats_for(faction)), 4, faction)

    def test_every_portfolio_is_one_of_the_four(self) -> None:
        for seat in self.roster.seats:
            self.assertIn(seat.portfolio, PORTFOLIOS, seat.leader_ref)

    def test_each_faction_covers_all_four_portfolios_exactly_once(self) -> None:
        for faction in ldr.FACTION_IDS:
            got = sorted(s.portfolio for s in self.roster.seats_for(faction))
            self.assertEqual(got, sorted(PORTFOLIOS), faction)

    def test_no_seat_is_filled_because_inventing_people_is_forbidden(self) -> None:
        self.assertEqual(self.roster.undeclared_people(), ())
        self.assertEqual(len(self.roster.unfilled_seats()), 12)

    def test_every_seat_is_marked_for_author_specification(self) -> None:
        for seat in self.roster.seats:
            self.assertIn("requires author specification", seat.todo, seat.leader_ref)

    def test_every_seat_has_an_institutional_tie(self) -> None:
        for seat in self.roster.seats:
            self.assertTrue(seat.institutional_tie, seat.leader_ref)


class ReuseTests(unittest.TestCase):
    """The roster annotates existing records and duplicates nothing."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roster = load_ukweli_leaders()
        cls.local = load_local_leaders()
        cls.cards = load_card_identifiers()

    def test_every_seat_references_an_existing_leader_record(self) -> None:
        for seat in self.roster.seats:
            self.assertIn(seat.leader_ref, self.local, seat.leader_ref)

    def test_seat_portfolios_agree_with_the_existing_records(self) -> None:
        for seat in self.roster.seats:
            self.assertEqual(seat.portfolio, self.local[seat.leader_ref]["portfolio"], seat.leader_ref)

    def test_the_roster_invents_no_new_leader_id(self) -> None:
        seat_ids = {s.leader_ref for s in self.roster.seats}
        self.assertEqual(seat_ids, set(self.local))

    def test_mars_references_the_landed_canonical_card(self) -> None:
        mars = self.roster.people["sir_mars_eldrich"]
        self.assertIn(mars.card_ref, self.cards)
        self.assertEqual(mars.card_ref, "sir_mars_eldrich")

    def test_the_roster_does_not_duplicate_mars_as_a_seat(self) -> None:
        for seat in self.roster.seats:
            self.assertNotEqual(seat.person, "sir_mars_eldrich", seat.leader_ref)

    def test_independent_npcs_are_a_declared_blank(self) -> None:
        self.assertEqual(self.roster.independent_npcs.get("entries"), [])
        self.assertIn("requires author specification", self.roster.independent_npcs.get("todo", ""))

    def test_naming_conflict_is_surfaced_and_not_resolved(self) -> None:
        note = self.roster.naming_note
        self.assertEqual(note.get("data_id"), "ulp")
        self.assertIn("LFP", note.get("setting_doc_name", ""))
        self.assertIn("requires author specification", note.get("todo", ""))


class NoNewStatisticTests(unittest.TestCase):
    """Issue #326 and #356 forbid a second, incompatible statistical system."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roster = load_ukweli_leaders()

    def test_no_seat_or_person_carries_a_numeric_statistic(self) -> None:
        forbidden = ldr._NUMERIC_FORBIDDEN
        for record in list(self.roster.seats) + list(self.roster.people.values()):
            for key in record.detail:
                self.assertFalse(any(bad in key for bad in forbidden), key)

    def test_the_existing_skill_field_is_not_restated_or_extended(self) -> None:
        for seat in self.roster.seats:
            self.assertNotIn("skill", seat.to_dict())

    def test_no_hegemony_or_influence_track_is_introduced(self) -> None:
        blob = json.dumps(self.roster.to_dict()).lower()
        for term in ("hegemony_score", "influence_track", "power_track", "victory_points"):
            self.assertNotIn(term, blob)


class HookEdgeTests(unittest.TestCase):
    """Hooks draw on a generation; edges name only known parties."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.roster = load_ukweli_leaders()

    def test_five_candidate_interactions_are_kept(self) -> None:
        self.assertEqual(len(self.roster.hooks), 5)

    def test_every_hook_names_a_known_generation(self) -> None:
        for hook in self.roster.hooks:
            self.assertIn(hook["drawn_from"], self.roster.people, hook["id"])

    def test_historical_hooks_are_drawn_from_historical_people(self) -> None:
        for hook in self.roster.hooks:
            person = self.roster.people[hook["drawn_from"]]
            self.assertEqual(hook["era"], person.era, hook["id"])

    def test_edges_name_only_known_endpoints(self) -> None:
        known = set(self.roster.people) | set(ldr.FACTION_IDS) | set(ldr.EXTERNAL_REFS)
        for edge in self.roster.edges:
            self.assertIn(edge["a"], known)
            self.assertIn(edge["b"], known)

    def test_the_bargain_is_an_inherited_obligation_in_both_directions(self) -> None:
        kinds = {(e["a"], e["b"]): e for e in self.roster.edges}
        edge = kinds[("sir_mercury_eldrich", "cpu")]
        self.assertEqual(edge["kind"], "inherited_obligation")
        self.assertIn("both directions", edge["note"])


class ValidatorTests(unittest.TestCase):
    """The validator reports rather than raises."""

    def setUp(self) -> None:
        self.roster = load_ukweli_leaders()

    def _mutated(self, mutate) -> LeaderRoster:
        raw = json.loads(ldr.DATA_PATH.read_text(encoding="utf-8"))
        mutate(raw)
        return roster_from_dict(raw)

    def test_an_agentic_historical_person_is_reported(self) -> None:
        def mutate(raw):
            raw["dynasty"][0]["holds_council_seat"] = True
        bad = self._mutated(mutate)
        self.assertTrue(any("historical person" in p for p in bad.off_vocabulary()))

    def test_an_unknown_portfolio_is_reported(self) -> None:
        def mutate(raw):
            raw["seats"]["cpu"][0]["portfolio"] = "nonsense"
        bad = self._mutated(mutate)
        self.assertTrue(any("portfolio" in p for p in bad.off_vocabulary()))

    def test_a_third_seat_missing_is_reported(self) -> None:
        def mutate(raw):
            raw["seats"]["cpu"].pop()
        bad = self._mutated(mutate)
        self.assertTrue(any("four seats" in p for p in bad.off_vocabulary()))

    def test_a_filled_seat_is_surfaced_as_an_undeclared_person(self) -> None:
        def mutate(raw):
            raw["seats"]["cpu"][0]["person"] = "invented_person"
        bad = self._mutated(mutate)
        self.assertIn("cpu1", bad.undeclared_people())

    def test_a_dangling_edge_is_reported(self) -> None:
        def mutate(raw):
            raw["relationships"]["edges"][0]["b"] = "nowhere"
        bad = self._mutated(mutate)
        self.assertTrue(any("unknown" in p for p in bad.off_vocabulary()))

    def test_an_undeclared_hook_reference_is_reported(self) -> None:
        def mutate(raw):
            raw["event_hooks"]["hooks"][0]["id"] = "renamed"
        bad = self._mutated(mutate)
        self.assertTrue(any("not declared" in p for p in bad.off_vocabulary()))


class ScopeDirectiveTests(unittest.TestCase):
    """The strategy game stays standalone (issues #282/#299)."""

    def test_the_module_does_not_import_laclaugpt(self) -> None:
        source = Path(ldr.__file__).read_text(encoding="utf-8")
        self.assertNotIn("laclaugpt", source.lower())

    def test_the_module_needs_no_optional_dependency(self) -> None:
        source = Path(ldr.__file__).read_text(encoding="utf-8")
        for banned in ("pandas", "numpy", "networkx", "requests"):
            self.assertNotIn(f"import {banned}", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
