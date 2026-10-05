from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Issue51DesignArchitectureTests(unittest.TestCase):
    def test_gns_priority_is_explicit(self) -> None:
        text = read("docs/archive/DESIGN_PRINCIPLES.md")
        self.assertIn("Narrativist experience + Simulationist world + Gamist friction", text)
        self.assertIn("The Veil", text)

    def test_four_system_attribute_tags_are_canonical(self) -> None:
        """AGENTS.md §4 states the direction; the archived rulebook holds the model.

        The four-system attribute-tag model is still the canonical character
        direction (AGENTS.md §4), so the guard is not retired — only re-pointed,
        because the rulebook that carried the model body is now archived.
        """
        agents = read("AGENTS.md")
        for name in ("Physical", "Social", "Psychic", "Cybernetic"):
            with self.subTest(name=name):
                self.assertIn(name, agents)
        text = read("docs/archive/RULEBOOK.md")
        self.assertIn("Attributes are tags", text)
        self.assertIn("multiple attribute tags", text)

    def test_absent_system_is_not_low_score(self) -> None:
        text = read("docs/archive/RULEBOOK.md")
        self.assertIn("Absence is not the same as a low score", text)
        self.assertIn("non-conscious AI", text)
        self.assertIn("no meaningful Psychic participation", text)

    def test_concordia_architecture_records_hybrid_npc_tiers(self) -> None:
        text = read("docs/archive/CONCORDIA_ARCHITECTURE.md")
        self.assertIn("Mesa / rule agents", text)
        self.assertIn("Lightweight interactive NPCs", text)
        self.assertIn("Persistent Concordia / LLM agents", text)
        self.assertIn("promoted", text)

    def test_multiplayer_keeps_server_authoritative(self) -> None:
        text = read("docs/archive/CONCORDIA_ARCHITECTURE.md")
        self.assertIn("authoritative simulation state", text)
        self.assertIn("Streamlit", text)
        self.assertIn("FastAPI + WebSockets", text)
        self.assertIn("The UI is a client. The NoöPunk simulation is the game.", text)

    def test_agents_no_longer_freeze_six_attribute_list(self) -> None:
        """#51 superseded the old six; #131 later locked a NEW six by author decision.

        The original point was that agents must not freeze an attribute list on
        their own initiative. That still holds: AGENTS.md must record the list as an
        *author* decision, and must keep the generation procedure and the universal
        Skill list explicitly open.
        """
        text = read("AGENTS.md")
        self.assertIn("Issue #131", text)
        self.assertIn("locks the universal base STAT list", text)
        self.assertIn("FIT / REF / INT / SOC / CYB / PSY", text)
        # the still-open parts must keep reading as open
        self.assertIn("still **not locked**", text)


if __name__ == "__main__":
    unittest.main()
