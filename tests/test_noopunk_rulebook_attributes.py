"""Keep `noopunk/rulebook/RULEBOOK.md` and `noopunk/game/data/attributes.json` from drifting (#835).

The issue's requirement 4 is explicit: *"Rulebook and Godot must use the same table and definitions. No
independent tabletop-vs-game inventions; if keeping a small machine-readable table is helpful, reference
it explicitly from the rulebook, avoiding multiple conflicting copies."*

`attributes.json` says of itself that it is "the machine-readable copy of the character sheet rules in
noopunk/rulebook/RULEBOOK.md". Nothing checked that claim, so the two could diverge silently — the
Godot tests only ever read the JSON, and a human reading the rulebook would have no signal.

This test reads the markdown tables back and compares them with the JSON.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "noopunk" / "rulebook" / "RULEBOOK.md"
DATA = ROOT / "noopunk" / "game" / "data" / "attributes.json"

MINUS = "\u2212"          # the typographic minus the rulebook uses
SPANS = ("\u2013", "\u2014", "-")   # en dash, em dash, hyphen


def _cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def _table(markdown: str, header_hint: str) -> list[list[str]]:
    """Rows of the first markdown table whose header line contains `header_hint`."""
    lines = markdown.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and header_hint.lower() in line.lower():
            rows: list[list[str]] = []
            for row in lines[i + 2:]:       # skip header and its separator
                if not row.strip().startswith("|"):
                    break
                rows.append(_cells(row))
            return rows
    return []


def _int(text: str) -> int:
    return int(text.replace(MINUS, "-").replace("+", "").replace("**", "").strip())


class RulebookMatchesGameData(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.markdown = RULEBOOK.read_text(encoding="utf-8")
        cls.flat = cls.markdown.replace(MINUS, "-")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_rulebook_and_json_exist(self) -> None:
        self.assertTrue(RULEBOOK.exists(), "the rulebook is missing")
        self.assertTrue(DATA.exists(), "the machine-readable table is missing")

    def test_generation_bands_match(self) -> None:
        rows = _table(self.markdown, "3d6")
        self.assertEqual(len(rows), 7, f"expected 7 generation bands in the rulebook, got {len(rows)}")
        seen = []
        for span, value in ((r[0], r[1]) for r in rows):
            dash = next(d for d in SPANS if d in span)
            low, _, high = span.partition(dash)
            seen.append({"min": _int(low), "max": _int(high), "value": _int(value)})
        self.assertEqual(seen, self.data["bands"],
                         "the rulebook's 3d6 table disagrees with data/attributes.json")

    def test_attribute_names_and_definitions_match(self) -> None:
        rows = _table(self.markdown, "attribute")
        self.assertEqual(len(rows), 7, f"expected 7 attributes in the rulebook, got {len(rows)}")
        seen = [{"name": r[0].replace("**", "").strip(), "definition": r[1].strip()} for r in rows]
        expected = [{"name": a["name"], "definition": a["definition"]} for a in self.data["attributes"]]
        self.assertEqual(seen, expected,
                         "the rulebook's attribute list disagrees with data/attributes.json")

    def test_exactly_seven_attributes(self) -> None:
        self.assertEqual(len(self.data["attributes"]), 7)
        self.assertEqual(len({a["name"] for a in self.data["attributes"]}), 7,
                         "attribute names must be unique")

    def test_difficulty_labels_match(self) -> None:
        rows = _table(self.markdown, "target")
        seen = [{"target": _int(r[0]), "label": r[1].strip()} for r in rows]
        self.assertEqual(seen, self.data["difficulty"],
                         "the rulebook's difficulty table disagrees with data/attributes.json")

    def test_human_range_and_transhuman_threshold(self) -> None:
        self.assertEqual(self.data["human_range"], {"min": -3, "max": 3})
        self.assertEqual(self.data["transhuman"]["above"], 3)
        self.assertIn("legitimate basic-human score", self.flat,
                      "the rulebook no longer says -3 is legal for every attribute")

    def test_every_reachable_total_lands_in_the_human_range(self) -> None:
        for total in range(3, 19):
            band = next((b for b in self.data["bands"] if b["min"] <= total <= b["max"]), None)
            if band is None:
                self.fail(f"3d6 total {total} has no band")
                continue
            self.assertGreaterEqual(band["value"], self.data["human_range"]["min"])
            self.assertLessEqual(band["value"], self.data["human_range"]["max"])

    def test_no_resolution_mechanic_was_invented(self) -> None:
        # The issue forbids choosing 2d6/d20/3d6 for the difficulty targets; the placeholder must stay.
        self.assertIn("No resolution mechanic has been specified", self.flat)


if __name__ == "__main__":
    unittest.main()
