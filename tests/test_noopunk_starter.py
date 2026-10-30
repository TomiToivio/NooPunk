"""The single NoöPunk starter: canonical paths, no duplicate project, no imported rule systems (#827).

Guard rails, not gameplay tests. If the canonical artefacts move, if a second Godot prototype appears,
or if an undecided rule system is quietly imported into the new game, this fails.
"""
from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
NOOPUNK = ROOT / "noopunk"
RULEBOOK = NOOPUNK / "rulebook" / "RULEBOOK.md"
GAME = NOOPUNK / "game"
START_HERE = NOOPUNK / "START_HERE.md"
CONTRACT = GAME / "data" / "attributes.json"


class CanonicalPathTest(unittest.TestCase):
    def test_the_two_canonical_artefacts_exist(self) -> None:
        for path in (RULEBOOK, START_HERE, CONTRACT, GAME / "project.godot",
                     GAME / "character_creation.tscn", GAME / "tests" / "character_test.gd",
                     GAME / "tests" / "smoke.gd"):
            self.assertTrue(path.exists(), path)

    def test_start_here_names_both_paths_and_the_workflow(self) -> None:
        text = START_HERE.read_text(encoding="utf-8")
        self.assertIn("noopunk/rulebook/RULEBOOK.md", text)
        self.assertIn("noopunk/game/", text)
        self.assertIn("child issue", text.lower())
        self.assertIn("character_test.gd", text)

    def test_there_is_exactly_one_new_starter(self) -> None:
        # #827 forbids alternative prototypes: the earlier `restart/` tree was absorbed into `noopunk/`.
        self.assertFalse((ROOT / "restart").exists())
        projects = [p for p in ROOT.rglob("project.godot")
                    if "legacy" not in p.parts and "archive" not in p.parts and ".godot" not in p.parts]
        self.assertEqual(sorted(str(p.relative_to(ROOT)) for p in projects),
                         ["noopunk/game/project.godot", "project.godot"])

    def test_the_new_project_is_isolated_from_the_legacy_one(self) -> None:
        self.assertTrue((NOOPUNK / ".gdignore").exists())
        legacy = (ROOT / "project.godot").read_text(encoding="utf-8")
        self.assertNotIn("noopunk/game", legacy)
        self.assertIn("res://character_creation.tscn",
                      (GAME / "project.godot").read_text(encoding="utf-8"))


class OneTableTest(unittest.TestCase):
    """Rulebook and game must not drift (#835 requirement 4)."""

    def test_the_rulebook_quotes_the_bands_the_game_reads(self) -> None:
        import json

        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        # The book uses a typographic minus; compare on one form so the table can be typeset properly.
        text = RULEBOOK.read_text(encoding="utf-8").replace("\u2212", "-")
        for band in contract["generation"]["bands"]:
            low, high, value = band["low"], band["high"], band["value"]
            span = f"{low}" if low == high else f"{low}–{high}"
            shown = f"{value:+d}" if value else "0"
            self.assertIn(span, text, f"the rulebook is missing the {span} band")
            self.assertIn(shown, text, f"the rulebook is missing the {shown} value")
        for entry in contract["difficulty"]:
            self.assertIn(entry["label"], text)

    def test_the_contract_points_back_at_the_rulebook(self) -> None:
        import json

        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertIn("RULEBOOK.md", contract["_note"])

    def test_the_seven_attributes_are_the_authors_and_match(self) -> None:
        import json

        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        self.assertEqual(contract["attributes"],
                         ["Fitness", "Reflexes", "Cognition", "Cyber", "Awareness", "Agency", "Empathy"])
        for name in contract["attributes"]:
            self.assertIn(f"**{name}**", RULEBOOK.read_text(encoding="utf-8"), name)


class NothingUndecidedWasDecidedTest(unittest.TestCase):
    def test_no_resolution_mechanic_was_chosen(self) -> None:
        contract = self._contract()
        undecided = " ".join(contract["undecided"]).lower()
        self.assertIn("resolution", undecided)
        for path in (GAME / "attribute_roll.gd", GAME / "character_creation.gd"):
            source = path.read_text(encoding="utf-8").lower()
            for die in ("randi_range(1, 20)", "randi_range(1, 10)", "d20", "2d6"):
                self.assertNotIn(die, source, f"{path.name} picked a resolution die")

    def test_no_legacy_rule_system_was_imported(self) -> None:
        forbidden = ("hit_points", "hp_max", "inventory", "strain", "psionic", "skill_rank",
                     "experience", "initiative", "damage")
        for path in (GAME / "attribute_roll.gd", GAME / "character_creation.gd", GAME / "main.gd"):
            lines = [line for line in path.read_text(encoding="utf-8").splitlines()
                     if not line.lstrip().startswith("#")]
            source = "\n".join(lines).lower()
            for word in forbidden:
                self.assertNotIn(word, source, f"{path.name} imports {word!r}")

    def _contract(self) -> dict:
        import json

        return json.loads(CONTRACT.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
