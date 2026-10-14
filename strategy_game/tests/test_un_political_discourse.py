"""The executable discourse reader, and the boundaries the author set (#469, #470).

Unittest, not pytest: the repository's CI step is
`python3 -m unittest discover -s strategy_game/tests -p "test_*.py"`, which does not collect
pytest-style functions -- so the original four checks never ran. They are preserved here, plus the
author's boundaries as contracts.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from strategy_game.un_political_discourse import (
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
        true_humans = next(p for p in self.data["parties"] if p["id"] == "true_humans")
        policy = json.dumps(true_humans, ensure_ascii=False).lower()
        self.assertIn("not endorsed", policy)
        self.assertIn("fictional", policy)


if __name__ == "__main__":
    unittest.main()
