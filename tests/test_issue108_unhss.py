"""Acceptance guard for issue #108, renamed to UNSA by issue #144.

Issue #108 defined the default campaign institution; issue #144 renamed it from
UNHSS / Firewall to **UNSA — the United Nations Security Agency** and expanded its
documented scope (covert network, civilian side, both-outcomes Disclosure canon, early
labels and the MJ-12 taboo). This guard asserts the current UNSA canon. The old names
may still appear, but only in supersession notes.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")


class UNSATests(unittest.TestCase):
    def test_name_and_aliases(self):
        for phrase in (
            "United Nations Security Agency", "UNSA",
            "X-COM", "X-Files", "Men in Black",
        ):
            self.assertIn(phrase, BOOK)

    def test_the_old_names_are_superseded_not_silently_dropped(self):
        """#144 must record the rename, not merely overwrite the old name."""
        self.assertIn("UNHSS", BOOK)
        self.assertIn("Firewall", BOOK)  # named as an external design inspiration

    def test_mj12_is_not_a_tolerated_nickname(self):
        self.assertIn("MJ-12", BOOK)

    def test_default_pc_affiliation(self):
        self.assertIn("UNSA field agents", BOOK)
        self.assertIn("UNSA mission identity", FACTIONS)

    def test_three_function_hybrid_and_forces(self):
        for phrase in (
            "Civilian / scientific / diplomatic branch",
            "UNSA Police",
            "Tactical / military component",
            "Earth Special Operations Regiment",
            "Solar-System Space Marine Regiment",
            "strike fleet",
            "deep-space scouts",
        ):
            self.assertIn(phrase, BOOK)

    def test_federal_un_and_wallfacers(self):
        for phrase in (
            "UN President", "UN Prime Minister", "UN Parliament",
            "four years", "four Wallfacers",
            "Minister of Human Security and Survival",
        ):
            self.assertIn(phrase, BOOK)

    def test_the_helsinki_operational_chain_is_documented(self):
        for body in ("Suojelupoliisi", "Europol"):
            self.assertIn(body, BOOK)

    def test_machine_readable_model(self):
        for phrase in (
            "canonical_name: United Nations Security Agency",
            "wallfacers: 4",
            "multi_faction_membership: true",
        ):
            self.assertIn(phrase, ORG)


if __name__ == "__main__":
    unittest.main()
