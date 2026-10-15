"""The executable discourse reader, and the boundaries the author set (#469, #470).

Unittest, not pytest: the repository's CI step is
`python3 -m unittest discover -s strategy_game/tests -p "test_*.py"`, which does not collect
pytest-style functions -- so the original four checks never ran. They are preserved here, plus the
author's boundaries as contracts.
"""

from __future__ import annotations

import json
import pathlib
import unittest
from pathlib import Path

from strategy_game.un_political_discourse import (
    relation_between,
    majority_reaction,
    DATA_PATH,
    load_un_political_discourse,
    interpret_event,
)

#: Names the author cites as fictional *inspirations*. None may appear in the 2045 records.
REAL_NAMES = ("Unabomber", "Linkola", "Yudkowsky")


def _walk(node, path=""):
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _walk(value, f"{path}.{key}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, f"{path}[{index}]")
    elif isinstance(node, str):
        yield path, node


class ReaderTests(unittest.TestCase):
    """The four checks from the original file, unchanged in intent."""

    def test_reader_exposes_distinct_perspectives(self) -> None:
        view = interpret_event("confederacy_harvest_offer")
        parties = load_un_political_discourse()["parties"]
        self.assertEqual(len(view["party_readings"]), len(parties))
        self.assertEqual(len({p["party_id"] for p in view["party_readings"]}), len(view["party_readings"]))
        self.assertTrue(all(p["stance"] for p in view["party_readings"]))
        self.assertEqual(view["event"]["status"], "observed")

    def test_unknown_event_is_not_invented(self) -> None:
        with self.assertRaises(KeyError):
            interpret_event("invented-event")

    def test_loader_allows_future_party_additions(self) -> None:
        import tempfile

        payload = load_un_political_discourse()
        newcomer = json.loads(json.dumps(payload["parties"][0]))
        newcomer["id"] = "future_party"
        payload["parties"].append(newcomer)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "extra.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(len(load_un_political_discourse(path)["parties"]), len(payload["parties"]))

    def test_loader_rejects_duplicate_ids(self) -> None:
        import tempfile

        payload = load_un_political_discourse()
        payload["parties"].append(dict(payload["parties"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_un_political_discourse(path)


class BoundaryTests(unittest.TestCase):
    """The author's boundaries, asserted rather than assumed."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_un_political_discourse()
        cls.raw = DATA_PATH.read_text(encoding="utf-8")

    def test_the_four_parties_are_the_authors_decision(self) -> None:
        self.assertEqual(
            [party["id"] for party in self.data["parties"]],
            ["libertarian_accelerationist", "true_humans", "unity_security_stability", "noosphere"],
        )
        self.assertIs(self.data["simulation_rules_approved"], False)

    def test_every_party_reads_every_stance_dimension(self) -> None:
        dimensions = self.data["stance_dimensions"]
        for party in self.data["parties"]:
            for dimension in dimensions:
                with self.subTest(party=party["id"], dimension=dimension):
                    self.assertTrue(party["stances"].get(dimension))

    def test_every_party_carries_a_reality_tunnel_that_may_change(self) -> None:
        for party in self.data["parties"]:
            with self.subTest(party=party["id"]):
                tunnel = party["reality_tunnel"]
                self.assertTrue(tunnel["interpretation"])
                self.assertIn(tunnel["evidence_status"], self.data["epistemic_statuses"])
                self.assertIs(tunnel["may_change_with_evidence"], True)

    def test_no_real_person_appears_in_any_2045_record(self) -> None:
        """A name cited as fictional inspiration must never leak into a faction's record."""
        for path, text in _walk(self.data):
            for name in REAL_NAMES:
                if name in text:
                    with self.subTest(path=path, name=name):
                        self.fail(f"{name} appears at {path} in the 2045 discourse record")

    def test_the_extremist_position_is_marked_not_endorsed(self) -> None:
        """The runtime data must carry the marking, not only the register prose."""
        true_humans = next(p for p in self.data["parties"] if p["id"] == "true_humans")
        marking = str(true_humans.get("depicted_as", "")).lower()
        self.assertIn("not endorsed", marking)
        self.assertIn("fictional", marking)
        self.assertIn("extermination", str(true_humans.get("policy", "")).lower())
        register = pathlib.Path("data/world/un_parties.yaml").read_text(encoding="utf-8").lower()
        self.assertIn("not endorsed", register, "the register must carry the same marking")




class DiscourseModelTests(unittest.TestCase):
    """The alliance/schism/belief-change model (#469) and the fields #470 asks each faction for."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.data = load_un_political_discourse()

    def test_relations_use_the_declared_vocabulary_and_name_their_basis(self) -> None:
        states = self.data["relation_states"]
        self.assertGreaterEqual(len(self.data["relations"]), 4)
        for relation in self.data["relations"]:
            with self.subTest(pair=relation["between"]):
                self.assertIn(relation["state"], states)
                self.assertTrue(str(relation.get("basis", "")).strip())
                self.assertIs(relation.get("may_change_with_evidence"), True)
                self.assertEqual(len(set(relation["between"])), 2)

    def test_relations_join_declared_parties_only(self) -> None:
        identifiers = {party["id"] for party in self.data["parties"]}
        for relation in self.data["relations"]:
            for identifier in relation["between"]:
                with self.subTest(identifier=identifier):
                    self.assertIn(identifier, identifiers)

    def test_every_party_records_its_internal_schism_lines(self) -> None:
        for party in self.data["parties"]:
            with self.subTest(party=party["id"]):
                self.assertTrue(party.get("schism_lines"), "a party without schism lines is not plural")
                self.assertTrue(party.get("internal_currents"))

    def test_every_event_carries_the_unaligned_majority_reading(self) -> None:
        """The issue asks for the majority's contrasting reaction; the reader used to omit it."""
        for event in self.data["example_events"]:
            with self.subTest(event=event["id"]):
                self.assertTrue(str(event.get("majority_reaction", "")).strip())

    def test_the_endgame_space_stays_open(self) -> None:
        space = self.data["endgame_space"]
        self.assertGreaterEqual(len(space), 4)
        self.assertIn("peaceful cohabitation", space)
        self.assertIn("disintegration", space)

    def test_the_integration_links_name_the_other_issues(self) -> None:
        joined = " ".join(str(v) for v in self.data["integration"].values())
        for reference in ("#346", "#338", "#468", "#461"):
            with self.subTest(reference=reference):
                self.assertIn(reference, joined)

    def test_the_readers_answer_and_refuse_correctly(self) -> None:
        relation = relation_between("true_humans", "noosphere")
        assert relation is not None
        self.assertEqual(relation["state"], "rivalry")
        self.assertIsNone(relation_between("true_humans", "true_humans"))
        self.assertTrue(majority_reaction("verified_psi_service"))
        with self.assertRaises(KeyError):
            majority_reaction("invented-event")

    def test_the_model_still_approves_no_mechanic(self) -> None:
        """The prohibition may be *stated* in prose; it may not appear as code.

        Scanning raw text was the wrong test: the module documents the refusal
        ("no opinion scores, persuasion probabilities") and that prose tripped the guard.
        Parsing the module and checking its identifiers asserts the boundary the guard
        was actually for.
        """
        import ast

        self.assertIs(self.data["simulation_rules_approved"], False)
        source = (DATA_PATH.parent.parent / "un_political_discourse.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        identifiers = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                identifiers.add(node.id.lower())
            elif isinstance(node, ast.Attribute):
                identifiers.add(node.attr.lower())
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                identifiers.add(node.name.lower())
        for banned in ("probabilit", "score", "strength", "effect"):
            with self.subTest(token=banned):
                offending = sorted(i for i in identifiers if banned in i)
                self.assertEqual(offending, [], f"mechanical identifier(s) in the discourse module: {offending}")

    def test_the_relations_are_marked_as_a_proposal(self) -> None:
        """Allies and antagonists are D21's undecided question; the data must say so."""
        self.assertEqual(self.data.get("relations_status"), "proposal_pending_author_review")


if __name__ == "__main__":
    unittest.main()
