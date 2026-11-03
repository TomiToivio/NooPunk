"""The WWN coverage register must stay true to the tree (#1101).

The register is curated; the claims inside it are not. This gate runs the audit's
`--check`, which re-reads every claimed module/procedure, every test path and the
rendered report, so a refactor that moves a procedure cannot leave the matrix
lying. It deliberately does not judge rules correctness — that is the page-cited
queue, not a test.
"""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WwnCoverageRegisterTests(unittest.TestCase):
    def test_the_register_and_report_are_current(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/wwn_coverage_audit_1101.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("94 rows", result.stdout)


if __name__ == "__main__":
    unittest.main()
