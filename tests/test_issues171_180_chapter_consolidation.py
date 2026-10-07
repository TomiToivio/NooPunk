"""Structure guard for the #171–#180 chapter consolidation (follow-up to #181).

PR #181 landed the lore and the field catalogs. This guard pins the follow-up
deltas — the physical harm ladder, the top-level equipment vocabulary, the
expanded Pauli–Jung/Atmanspacher detail in the Psychic chapter, and the
subsystem cross-references — and, just as importantly, pins that the
author-owned reservations were not crossed (equipment statistics stay
undefined; psi powers stay capabilities; deep hacking stays deferred; Seity
stays parked).

It asserts structure and presence only; it does not constrain wording.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


def flat(relative: str) -> str:
    """Whitespace-collapsed, lowercased text, so wrapping cannot hide a term."""
    text = (ROOT / relative).read_text(encoding="utf-8")
    return " ".join(text.split()).lower()


def rulebook_section(number: int) -> str:
    """Return one numbered top-level RULEBOOK section, preserving its local text."""
    text = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
    match = re.search(
        rf"^## {number}\. .*?(?=^## \d+\. |\Z)",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"RULEBOOK section {number} not found")
    return match.group(0)


class HarmLadderTests(unittest.TestCase):
    def test_wound_ladder_exists(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("## 51. physical harm: a light ladder", text)
        for state in ("scratched", "wounded", "critical", "down"):
            with self.subTest(state=state):
                self.assertIn(state, text)

    def test_harm_rules_stay_non_numeric(self) -> None:
        section = rulebook_section(51).lower()
        self.assertIn("consequence vocabulary", section)
        self.assertIn("explicit design questions", section)
        self.assertNotRegex(section, r"\b\d+d\d+\b")
        self.assertNotRegex(
            section,
            r"\b(?:damage|armor|armour|hp|health)\s*(?:=|:|\+|-)\s*\d+\b",
        )


class EquipmentListTests(unittest.TestCase):
    def test_top_level_equipment_list(self) -> None:
        text = flat("RULEBOOK.md")
        self.assertIn("## 52. equipment (list)", text)
        for category in ("weapons", "armor and protection", "tools, sensors and vehicles"):
            with self.subTest(category=category):
                self.assertIn(category, text)


class PsychicDepthTests(unittest.TestCase):
    def test_atmanspacher_depth_added(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("structural vs induced correlations", text)
        self.assertIn("coincidence", text)
        self.assertIn("dissociation", text)

    def test_categorial_state_classes(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        for cls in ("categorial", "non-categorial", "acategorial", "psychoid"):
            with self.subTest(cls=cls):
                self.assertIn(cls, text)

    def test_still_grounded_in_existing_engine(self) -> None:
        text = flat("rulebook/6_PSYCHIC.md")
        self.assertIn("capabilities", text)
        self.assertIn("stat + skill + 1d10", text)


class CrossReferenceTests(unittest.TestCase):
    def test_subsystem_pointers_exist(self) -> None:
        cyber = flat("rulebook/5_CYBERNETIC.md")
        self.assertIn("where things live", cyber)
        self.assertIn("9_field_catalogs.md", cyber)
        self.assertIn("respawn button", cyber)

    def test_physical_chapter_points_at_canon(self) -> None:
        phys = flat("rulebook/3_PHYSICAL.md")
        self.assertIn("§51", phys)
        self.assertIn("§52", phys)
        self.assertIn("9_field_catalogs.md", phys)


class SectionNumberingTests(unittest.TestCase):
    """§40.4's subsections must not collide with a §44 (the pre-existing 44.4.x typo)."""

    def test_no_misnumbered_40_4_subsections(self) -> None:
        text = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
        self.assertNotIn("#### 44.4.1", text)
        self.assertIn("#### 40.4.1", text)


class ReservationsPreservedTests(unittest.TestCase):
    """The chapter consolidation must not have crossed the author-owned reservations."""

    def test_equipment_statistics_still_undefined(self) -> None:
        self.assertIn("equipment statistics remain undefined",
                      flat("rulebook/5_CYBERNETIC.md"))
        self.assertIn("not statistics", flat("RULEBOOK.md"))

    def test_deep_hacking_still_deferred(self) -> None:
        self.assertIn("deep hacking remains a separate deferred subsystem",
                      flat("rulebook/5_CYBERNETIC.md"))

    def test_seity_still_parked(self) -> None:
        self.assertIn("not active rules",
                      flat("rulebook/9_FIELD_CATALOGS.md"))

    def test_agents_md_records_the_scope(self) -> None:
        self.assertIn("issues #171–#180 add", flat("AGENTS.md"))

    def test_agents_md_still_reserves_numeric_statistics(self) -> None:
        self.assertIn("equipment statistics", flat("AGENTS.md"))


if __name__ == "__main__":
    unittest.main()
