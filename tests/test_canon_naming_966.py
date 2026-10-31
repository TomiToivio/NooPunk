"""Canon naming is decided once (#966).

Two spellings travelled through the documents: the agency as UNHA and as UNSA, and the Pleiadian biologics as
"Pleyadian". Both issues that raised them recorded the choice (UNSA, Pleiadian) but no check enforced it, so the
old spellings kept reappearing in newly written prose.

`legacy/` is frozen on purpose and is not scanned: those files are a record, not canon.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNED = ("*.md", "*.py", "*.gd", "*.json", "*.tscn")
FORBIDDEN = {
    "UNHA": r"\bUNHA\b",
    "Pleyadian": r"\bPleyadian",
    "Pleyades": r"\bPleyades\b",
}


#: The guard has to name what it forbids, so it does not scan itself.
SELF = Path(__file__).resolve()


def _offenders() -> dict[str, list[str]]:
    hits: dict[str, list[str]] = {}
    for pattern in SCANNED:
        for path in ROOT.rglob(pattern):
            if path == SELF or "legacy" in path.parts or ".git" in path.parts:
                continue
            if "node_modules" in path.parts:
                continue
            try:
                text = path.read_text(errors="ignore")
            except OSError:
                continue
            for name, needle in FORBIDDEN.items():
                if re.search(needle, text):
                    hits.setdefault(name, []).append(str(path.relative_to(ROOT)))
    return hits


class CanonNaming(unittest.TestCase):
    def test_no_retired_spellings_outside_legacy(self):
        hits = _offenders()
        self.assertEqual(hits, {}, f"retired spellings still in canon: {hits}")

    def test_the_chosen_spellings_are_the_ones_in_use(self):
        """A guard that only forbids the old words would pass on an empty repository."""
        corpus = "\n".join(
            path.read_text(errors="ignore")
            for path in (ROOT / "docs" / "world").glob("*.md")
        )
        self.assertIn("UNSA", corpus)
        self.assertIn("Pleiadian", corpus)


if __name__ == "__main__":
    unittest.main()
