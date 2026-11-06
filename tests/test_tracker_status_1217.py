"""#1217 line 19: the tracker's own status page cannot rot.

The page is generated from a manifest of evidence paths, so this test asserts the two things that could make it lie:
a row citing a file that no longer exists, and a rendered page that no longer matches the manifest.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import tracker_1217_status as status  # noqa: E402


class TrackerStatusTests(unittest.TestCase):
    def test_every_row_cites_evidence_that_exists(self):
        self.assertEqual(status.missing_evidence(), [],
                         "a tracker row cites a file that is gone; fix the row or the tree")

    def test_the_committed_page_matches_the_manifest(self):
        self.assertTrue(status.OUT.is_file(), "run python3 tools/tracker_1217_status.py")
        self.assertEqual(
            status.OUT.read_text(encoding="utf-8"), status.render(),
            "docs/design/TRACKER_1217_STATUS.md is stale; run python3 tools/tracker_1217_status.py",
        )

    def test_every_row_states_a_status_and_a_note(self):
        for item, state, _evidence, note in status.ROWS:
            self.assertIn(state, status.STATUS_ORDER, item)
            self.assertTrue(note.strip(), f"{item} needs a note saying what is missing")

    def test_a_blocked_row_names_its_decision(self):
        """'Blocked' is a claim about a decision, so the note must read like one."""
        blocked = [(item, note) for item, state, _e, note in status.ROWS if state == "BLOCKED"]
        self.assertTrue(blocked, "the tracker has blocked rows; if not, update this test")
        for item, note in blocked:
            self.assertTrue(
                any(word in note.lower() for word in ("author", "decision", "approv", "d71", "licence")),
                f"{item}: a blocked row must name the decision it waits on",
            )

    def test_the_deferred_row_is_the_astral_graph(self):
        deferred = [item for item, state, _e, _n in status.ROWS if state == "DEFERRED"]
        self.assertEqual(len(deferred), 1)
        self.assertIn("Astral", deferred[0])


if __name__ == "__main__":
    unittest.main()
