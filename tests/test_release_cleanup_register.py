"""The release clean-up register, pinned (issue #421 item 3).

The packaging guard reports; this test keeps its findings from drifting. If the quarantined EP-derived
paths stop being flagged, or the guard starts erroring, this fails instead of the register quietly
becoming false. It runs the guard as a subprocess so it tests the same entry point a release would use.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "tools" / "release_packaging_guard.py"

#: The EP-derived artefacts the register lists; each must be flagged as quarantined in the release set.
#: The last two were added in #421's follow-up: the modules that exercise the EP2 prototype import the
#: quarantined code directly, so they are inside the same boundary — and before the two globs existed,
#: a public-mode bundle of them returned no quarantine finding at all.
QUARANTINED = (
    "src/eclipse_phase_homebrew/__init__.py",
    "src/eclipse_phase_homebrew/core.py",
    "src/eclipse_phase_homebrew/embodiment.py",
    "src/eclipse_phase_homebrew/interactions.py",
    "src/concordia_runtime/ep2_adapter.py",
    "src/concordia_runtime/ep2_session.py",
    "scripts/ep2_concordia_smoke.py",
    "tests/test_ep2_session.py",
    "tests/test_issue60_ep2_interactions.py",
)


class ReleaseCleanupRegisterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = subprocess.run(
            [sys.executable, str(GUARD), "--mode", "audit"],
            cwd=ROOT, capture_output=True, text=True, timeout=300,
        )
        cls.output = cls.result.stdout + cls.result.stderr

    def test_the_guard_passes_with_no_errors(self) -> None:
        self.assertIn("PASS:", self.output, self.output[-2000:])
        self.assertIn("0 error(s)", self.output, self.output[-2000:])

    def test_every_quarantined_path_is_reported_as_such(self) -> None:
        for path in QUARANTINED:
            with self.subTest(path=path):
                self.assertIn(path, self.output, f"{path} is no longer flagged by the guard")
                self.assertIn("quarantined-path-in-release-set", self.output)

    def test_the_register_document_lists_the_same_paths(self) -> None:
        register = ROOT / "docs" / "licenses" / "RELEASE_CLEANUP_AUDIT.md"
        text = register.read_text(encoding="utf-8")
        for path in QUARANTINED:
            with self.subTest(path=path):
                self.assertIn(f"`{path}`", text, f"{path} is missing from the register")


if __name__ == "__main__":
    unittest.main()
