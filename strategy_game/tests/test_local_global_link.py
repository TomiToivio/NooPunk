"""Executable contracts for the local-to-global link record (issue #322).

Code-only, per `AGENTS.md` and issue #271. These exercise the **link record and its validator**: every
link is a tendency rather than a membership, every link names which of the six quantities it plausibly
touches, and **no link binds to a global roster count** - which is the whole point of the record, given
that the 4 / 7 / 11 question is open.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_local_global_link.py"
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

from strategy_game import local_global_link as lgl  # noqa: E402
from strategy_game.local_global_link import (  # noqa: E402
    DATA_PATH,
    LINK_FORMAT,
    LINK_VERSION,
    LOCAL_PARTY_IDS,
    LinkError,
    link_from_dict,
    load_local_global_link,
)
from strategy_game.quantities import QUANTITY_IDS  # noqa: E402


def _raw() -> dict:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


class ShippedRecordTests(unittest.TestCase):
    """The packaged record is readable and self-consistent."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.link = load_local_global_link()

    def test_loads_and_declares_its_format(self) -> None:
        self.assertEqual(self.link.format, LINK_FORMAT)
        self.assertEqual(self.link.version, LINK_VERSION)

    def test_problems_are_empty(self) -> None:
        self.assertEqual(self.link.problems(), ())

    def test_no_scale_is_approved(self) -> None:
        self.assertFalse(self.link.numeric_scale_approved)

    def test_every_local_party_has_a_link(self) -> None:
        for party in LOCAL_PARTY_IDS:
            self.assertTrue(self.link.for_party(party), party)

    def test_a_foreign_document_is_refused_by_the_loader(self) -> None:
        raw = _raw()
        raw["format"] = "noopunk.strategy_game.something_else"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "link.json"
            path.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(LinkError):
                load_local_global_link(path)

    def test_round_trip_is_lossless_for_the_validator(self) -> None:
        again = link_from_dict(self.link.to_dict())
        self.assertEqual(again.problems(), ())


class RosterCountTests(unittest.TestCase):
    """The link names currents and never a roster size - the 4 / 7 / 11 question stays open."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.link = load_local_global_link()

    def test_the_record_asserts_no_roster_count(self) -> None:
        self.assertFalse(self.link.roster_count_asserted)

    def test_no_key_in_the_record_binds_to_a_roster_size(self) -> None:
        payload = self.link.to_dict()
        # The only roster-shaped top-level key is the *flag*, and it is false rather than a number.
        self.assertFalse(payload["roster_count_asserted"])
        for key, value in payload.items():
            if any(token in str(key).lower() for token in ("roster_count", "roster_size")):
                self.assertEqual(key, "roster_count_asserted")
                self.assertIs(value, False)
        # No link carries a roster-shaped field at all.
        for link in payload["links"]:
            for key in link:
                for token in ("roster_count", "roster_size", "faction_count", "party_count"):
                    self.assertNotIn(token, str(key).lower(), key)

    def test_asserting_a_roster_count_is_reported(self) -> None:
        raw = _raw()
        raw["roster_count_asserted"] = True
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("may not assert a count" in p for p in problems))

    def test_a_link_field_naming_a_roster_size_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["roster_size"] = "seven"
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("binds the link to a global roster size" in p for p in problems))

    def test_the_record_names_currents_rather_than_a_count(self) -> None:
        currents = self.link.currents()
        self.assertTrue(currents)
        for current in currents:
            self.assertIsInstance(current, str)


class TendencyNotMembershipTests(unittest.TestCase):
    """A link is a tendency; membership is never forced by a global network."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.link = load_local_global_link()

    def test_every_link_is_a_tendency(self) -> None:
        for link in self.link.links:
            self.assertTrue(link.is_tendency, link.global_current)
            self.assertFalse(link.membership)

    def test_no_link_applies_an_effect(self) -> None:
        for link in self.link.links:
            self.assertFalse(link.declared_not_enforced, link.global_current)

    def test_a_membership_claim_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["membership"] = True
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("membership is true" in p for p in problems))

    def test_a_declared_effect_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["declared_not_enforced"] = True
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("declared_not_enforced is true" in p for p in problems))

    def test_an_unknown_local_party_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["local_party"] = "someone_else"
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("is not one of the local party ids" in p for p in problems))

    def test_a_party_without_a_link_is_reported(self) -> None:
        raw = _raw()
        raw["links"] = [x for x in raw["links"] if x["local_party"] != "uip"]
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("uip: no link is declared" in p for p in problems))


class QuantityTests(unittest.TestCase):
    """A link names WHICH of the six quantities it touches, without collapsing them."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.link = load_local_global_link()

    def test_every_touched_quantity_is_one_of_the_six(self) -> None:
        self.assertTrue(self.link.quantities_touched())
        for quantity in self.link.quantities_touched():
            self.assertIn(quantity, QUANTITY_IDS, quantity)

    def test_a_link_naming_no_quantity_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["quantities_touched"] = []
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("names no quantity" in p for p in problems))

    def test_an_unknown_quantity_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["quantities_touched"] = ["influence"]
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("is not one of the six quantities" in p for p in problems))

    def test_a_quantity_both_touched_and_immovable_is_reported(self) -> None:
        raw = _raw()
        raw["links"][0]["cannot_move"] = list(raw["links"][0]["quantities_touched"])
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("both touched and cannot_move" in p for p in problems))


class ShockIntakeTests(unittest.TestCase):
    """Global developments enter locally; the local layer never simulates the globe."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.link = load_local_global_link()

    def test_the_local_layer_does_not_simulate_international_politics(self) -> None:
        self.assertFalse(self.link.shock_intake.get("simulates_international_politics"))

    def test_local_research_is_recorded_as_adoption(self) -> None:
        self.assertTrue(self.link.shock_intake.get("local_research_is_adoption"))

    def test_claiming_a_global_simulation_is_reported(self) -> None:
        raw = _raw()
        raw["shock_intake"]["simulates_international_politics"] = True
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("out of scope" in p for p in problems))

    def test_dropping_the_adoption_rule_is_reported(self) -> None:
        raw = _raw()
        raw["shock_intake"]["local_research_is_adoption"] = False
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("adoption of global technology" in p for p in problems))


class PendingDecisionTests(unittest.TestCase):
    """The roster-count question is carried open, with its reason."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.link = load_local_global_link()

    def test_the_roster_count_question_is_open_and_explained(self) -> None:
        open_ids = {d["id"] for d in self.link.unresolved_decisions()}
        self.assertIn("global_roster_count", open_ids)
        for decision in self.link.pending_decisions:
            self.assertTrue(str(decision["why_not_decided"]).strip(), decision["id"])

    def test_a_decision_without_a_reason_is_reported(self) -> None:
        raw = _raw()
        raw["pending_author_decisions"][0]["why_not_decided"] = ""
        problems = link_from_dict(raw).problems()
        self.assertTrue(any("must say WHY it is open" in p for p in problems))


class ScopeDirectiveTests(unittest.TestCase):
    """The strategy game stays standalone (issues #282/#299)."""

    def test_the_module_does_not_import_laclaugpt(self) -> None:
        source = Path(lgl.__file__).read_text(encoding="utf-8")
        self.assertNotIn("laclaugpt", source.lower())

    def test_the_module_needs_no_optional_dependency(self) -> None:
        source = Path(lgl.__file__).read_text(encoding="utf-8")
        for banned in ("pandas", "numpy", "networkx", "requests"):
            self.assertNotIn(f"import {banned}", source)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
