"""Contracts for the 2045 ideology model (issues #470 and #469).

Structure only, per #271: these assert the shape of the data and the boundaries the author set, never a
rule or a number. The four parties are the author's decision of 2026-10-15; the Reality Tunnel portraits
are marked PROPOSAL until he adopts them.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from strategy_game.ideology_framework import (
    DATA_DIR,
    EVIDENCE_IDS,
    STANCE_AXES,
    load_parties,
    load_tunnels,
    validate,
)

PARTIES_PATH = DATA_DIR / "un_parties_2045.json"

#: Names the author cites as fictional *inspirations*. They may appear only where the disclaimer lives.
REAL_NAMES = ("Unabomber", "Linkola", "Yudkowsky")
DISCLAIMER_KEYS = ("inspiration", "references", "note")


def _walk(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _walk(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


class PartyRosterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.parties = load_parties()
        cls.document = json.loads(PARTIES_PATH.read_text(encoding="utf-8"))

    def test_the_four_parties_are_the_authors_decision(self) -> None:
        self.assertEqual(self.document["status"], "author_canon")
        self.assertEqual(self.document["author_decision_date"], "2026-10-15")
        self.assertEqual(
            {party.label for party in self.parties},
            {"Libertarian Accelerationist Party", "True Humans Party",
             "Unity, Security and Stability Party", "The Noosphere"},
        )

    def test_every_party_answers_all_four_stance_axes_from_the_vocabulary(self) -> None:
        vocabulary = self.document["stance_vocabulary"]
        for party in self.parties:
            for axis in STANCE_AXES:
                with self.subTest(party=party.identifier, axis=axis):
                    value = party.stances.get(axis)
                    self.assertIn(value, vocabulary[axis])

    def test_every_party_is_internally_plural(self) -> None:
        for party in self.parties:
            with self.subTest(party=party.identifier):
                self.assertGreaterEqual(len(party.internal_currents), 2)

    def test_the_allegations_stay_allegations(self) -> None:
        for party in (p for p in self.parties if p.identifier == "libertarian_accelerationist"):
            for item in party.raw["uncertainties"]:
                with self.subTest(claim=item["id"]):
                    self.assertEqual(item["status"], "in_world_allegation_not_confirmed")
        noosphere = next(p for p in self.parties if p.identifier == "noosphere")
        self.assertEqual(
            noosphere.raw["uncertainties"][0]["status"],
            "the_partys_conviction_not_confirmed_objective_truth",
        )

    def test_the_extremist_position_is_recorded_as_not_endorsed(self) -> None:
        true_humans = next(p for p in self.parties if p.identifier == "true_humans")
        self.assertEqual(true_humans.raw["depicted_as"], "extremist political position, not endorsed")

    def test_no_real_person_appears_in_any_2045_record(self) -> None:
        """The real-person policy, enforced: cited names live only where the disclaimer lives."""
        for path, text in _walk(self.document):
            for name in REAL_NAMES:
                if name in text:
                    with self.subTest(path=path, name=name):
                        self.assertTrue(
                            any(allowed in path for allowed in DISCLAIMER_KEYS),
                            f"{name} appears at {path}, outside an inspiration or reference field",
                        )

    def test_the_reconciliation_is_named(self) -> None:
        reconciles = self.document["reconciles"]
        self.assertEqual(reconciles["legacy_register"], "data/world/un_parties.yaml")
        self.assertIn("D8", reconciles["queue_row"])


class FrameworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.tunnels = load_tunnels()

    def test_the_model_is_well_formed(self) -> None:
        self.assertEqual(validate(), ())

    def test_every_tunnel_reads_the_same_evidence(self) -> None:
        self.assertGreaterEqual(len(self.tunnels), 4)
        for tunnel in self.tunnels:
            for evidence in EVIDENCE_IDS:
                with self.subTest(tunnel=tunnel.identifier, evidence=evidence):
                    self.assertTrue(tunnel.reading(evidence).strip())

    def test_each_tunnel_names_a_signifier_chain_and_a_frontier(self) -> None:
        for tunnel in self.tunnels:
            with self.subTest(tunnel=tunnel.identifier):
                self.assertTrue(tunnel.nodal_points)
                self.assertTrue(tunnel.floating_signifiers)
                self.assertTrue(tunnel.equivalential_chain)
                self.assertTrue(tunnel.frontier)

    def test_the_portraits_are_marked_as_proposals(self) -> None:
        document = json.loads((DATA_DIR / "reality_tunnels.json").read_text(encoding="utf-8"))
        self.assertTrue(document["status"].startswith("PROPOSAL"))


if __name__ == "__main__":
    unittest.main()
