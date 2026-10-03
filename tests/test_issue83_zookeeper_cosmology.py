"""Regression guard for issue #83 lore in RULEBOOK.md."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"


def text() -> str:
    """Whitespace-collapsed rulebook text.

    The rulebook is hard-wrapped at ~90 columns, so a phrase that reads as one
    string in the document is often split across a newline. Reading the raw file
    made assertions fail against text that was present and correct:

        ``**one transition in the development of planetary`` / ``consciousness**``

    Only whitespace is collapsed. Markdown emphasis is deliberately LEFT INTACT,
    because several assertions in this module legitimately require it (for example
    ``"Earth's quarantine was deliberately **porous**"``), so stripping ``*`` would
    break correct expectations in the other direction.
    """
    raw = RULEBOOK.read_text(encoding="utf-8")
    return " ".join(raw.split())


class Issue83LoreTests(unittest.TestCase):
    def test_zoo_origin_and_zookeepers(self) -> None:
        t = text()
        for s in (
            "The early Milky Way was violent",
            "Zookeepers",
            # The probe ecology is canon as "a galaxy-wide network of ancient **Von
            # Neumann probes**" (§33.9). The guard previously required the literal
            # "Zookeeper Von Neumann probes", which was never written that way;
            # asserting the network of probes is the concept it was guarding.
            "network of ancient **Von Neumann probes**",
            "Earth's quarantine was deliberately **porous**",
            "Life must be allowed to continue evolving",
        ):
            self.assertIn(s, t)

    def test_human_offshoots_and_hybridization(self) -> None:
        t = text()
        for s in (
            "The **Pleiadians are human**",
            "Atlantis",
            "A major Grey lineage consists of **future humans**",
            "human–NHI hybridization program",
            "MJ-12",
            "human breakaway civilization",
        ):
            self.assertIn(s, t)

    def test_valis_noosphere_and_fourth_density(self) -> None:
        t = text()
        for s in (
            "VALIS event",
            "Noösphere becomes consciously active",
            "One Universe movement",
            "25 / 25 / 50 pattern",
            "Fourth Density",
        ):
            self.assertIn(s, t)

    def test_galactic_ecology_and_nonhuman_minds(self) -> None:
        t = text()
        for s in (
            "multiple independent waves of panspermia",
            "Plasmoids",
            "dolphins",
            "intelligence, consciousness, civilization, and technological power are different things",
            "Dyson swarms exist",
            "Kardashev scale",
        ):
            self.assertIn(s, t)

    def test_multiple_ufo_ontologies(self) -> None:
        t = text()
        for s in (
            "ontological disclosure",
            "cryptoterrestrials",
            "extratempestrials",
            "Temporals",
            "Ecologies",
            "Liminals",
        ):
            self.assertIn(s, t)

    def test_remaining_issue83_clarifications(self) -> None:
        t = text()
        for s in (
            "slow-dipper candidates",
            "amoeboid / slime-mold-like starfaring species",
            "ETI / Bracewell-probe threat",
            '"Nazi Zookeepers" theory is not cosmic truth',
            "one transition in the development of planetary consciousness",
            "Lockheed Martin",
            "Sam Altman's body is never recovered",
        ):
            self.assertIn(s, t)

    def test_uncertainty_and_fiction_framing(self) -> None:
        t = text()
        self.assertIn("The setting becomes stranger after contact, not simpler.", t)
        self.assertIn("No single taxonomy should explain every UAP, NHI, PSI, or mythic phenomenon.", t)
        self.assertIn("alternate-history fictional uses of real people, organizations, and countries", t)


if __name__ == "__main__":
    unittest.main()
