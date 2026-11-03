"""Guards against the failure mode this repository keeps producing: two agents, one feature, two files.

Nothing here checks style. Each test asserts that a feature has **one** home, and fails when a second one
appears — because a duplicate does not announce itself, it arrives as a reasonable-looking parallel
implementation and is discovered three weeks later when the two disagree.

These are `unittest.TestCase` methods on purpose: the root CI runs
`python -m unittest discover -s tests`, which does not collect bare pytest functions. A guard that only
runs when someone remembers to invoke pytest is not a guard.

If a test here fails, the answer is almost never "register the new path". It is to decide which
implementation is canonical, delete the other, and record the decision in `docs/DUPLICATION_AUDIT.md`.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Directories that hold gameplay code. Tests, docs and data are excluded on purpose.
CODE_ROOTS = ("src/rules", "src/console", "mud/nopunk_mud", "portable_noopunk")

#: Collisions that are **known and explained**. Each one is a different subsystem that happens to share a
#: filename, or a deliberately kept second implementation with a migration plan. Adding an entry here is a
#: decision that must also be recorded in `docs/DUPLICATION_AUDIT.md`.
KNOWN_COLLISIONS = {
    "cwn_core": "src/rules is canonical (ADR 1054); mud/nopunk_mud/cwn_core.py is a second kernel used only by "
                "the parity probes in tools/. Merge deferred: the MUD's campaign engine imports it. Audit entry.",
    "social": "Different subsystems: src/rules/social.py is the provisional #220 social procedures "
              "(IS_CANONICAL = False); mud/nopunk_mud/social.py is the #1008 rank/reputation overlay. "
              "Rename one before either grows.",
    "session": "Different layers: src/console/session.py is the portable case session; mud/nopunk_mud/session.py "
               "is the Evennia adapter over CampaignEngine. Not duplicates; the names are the problem.",
}


def _py_files():
    for root in CODE_ROOTS:
        base = ROOT / root
        if base.is_dir():
            yield from sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)


class DuplicationGuards(unittest.TestCase):
    def test_only_one_console_entry_point_exists(self):
        """One playable text front end. A second one silently forks the rules it calls."""
        candidates = [p for p in _py_files()
                      if re.search(r"class\s+(Console|CaseSession)\b",
                                   p.read_text(encoding="utf-8", errors="ignore"))]
        names = sorted(str(p.relative_to(ROOT)) for p in candidates)
        self.assertLessEqual(len(candidates), 1,
                             f"more than one console/session implementation: {names}")

    def test_only_one_campaign_model_is_live(self):
        """`solo_campaign.py` is a deprecated shim; anything new must use `campaign/engine.py`."""
        engines = [p for p in _py_files()
                   if "campaign" in p.name.lower() or "campaign" in str(p.parent).lower()]
        live = [p for p in engines if "solo_campaign" not in p.name]
        self.assertTrue(live, "the live campaign engine has disappeared")
        solo = ROOT / "mud/nopunk_mud/solo_campaign.py"
        if solo.is_file():
            self.assertIn("DEPRECATED", solo.read_text(encoding="utf-8"),
                          "solo_campaign.py must stay marked deprecated or be deleted")

    def test_only_one_generated_cwn_coverage_report(self):
        """Several agents wrote coverage reports in one day. One generated report survives."""
        reports = sorted(p.name for p in (ROOT / "docs/rules").glob("CWN_COVERAGE_*.md"))
        self.assertEqual(reports, ["CWN_COVERAGE_1068.md"],
                         f"expected exactly the canonical CWN coverage report, found {reports}")
        strays = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "docs").rglob("*COVERAGE_AUDIT*"))
        self.assertEqual(strays, [], f"retired hand-written coverage audits reappeared: {strays}")

    def test_only_one_tool_generates_a_cwn_coverage_report(self):
        """`cwn_parity_audit.py` owns the report; a second writer is a second definition of coverage."""
        writers = []
        for path in sorted((ROOT / "tools").glob("*.py")):
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "CWN_COVERAGE" in text and "write_text" in text:
                writers.append(path.name)
        self.assertEqual(writers, ["cwn_parity_audit.py"],
                         f"more than one tool writes a CWN coverage report: {writers}")
        self.assertFalse((ROOT / "tools/cwn_1068_coverage.py").exists(),
                         "the retired second coverage generator reappeared")
        self.assertFalse((ROOT / "tools/check_cwn_compliance.py").read_text(encoding="utf-8")
                         .find("CWN_COMPLIANCE_MATRIX_950") >= 0,
                         "the retired second matrix renderer reappeared in check_cwn_compliance.py")

    def test_retired_duplicate_audits_stay_deleted(self):
        retired = (
            "docs/rules/CWN_COMPLIANCE_MATRIX_950.md",
            "docs/rules/CWN_COVERAGE_AUDIT_1068.md",
            "data/rules/cwn_tabletop_audit_1068.json",
            "tools/cwn_1068_coverage.py",
        )
        present = [path for path in retired if (ROOT / path).exists()]
        self.assertEqual(present, [], f"retired duplicate artifacts reappeared: {present}")

    def test_a_rule_module_does_not_exist_twice_under_two_roots(self):
        """The same rule in `src/rules` and again under `mud/` is the classic drift.

        A new collision fails this test. A known one passes only because it is written down above, with a
        reason — an allowlist that nobody has to justify is how the duplicates win.
        """
        names: dict[str, list[str]] = {}
        for path in _py_files():
            stem = path.stem
            if stem.startswith("test_") or stem == "__init__":
                continue
            names.setdefault(stem, []).append(str(path.relative_to(ROOT)))
        duplicates = {k: v for k, v in names.items() if len(v) > 1}
        unexplained = {k: v for k, v in duplicates.items() if k not in KNOWN_COLLISIONS}
        self.assertEqual(unexplained, {},
                         f"new duplicate module names: {unexplained}. Decide which is canonical, delete the "
                         f"other, or add a justified entry to KNOWN_COLLISIONS and docs/DUPLICATION_AUDIT.md.")

    def test_every_known_collision_has_a_written_reason(self):
        for name, reason in KNOWN_COLLISIONS.items():
            self.assertGreater(len(reason), 60, f"{name}: the reason is too short to be a decision")
        audit = ROOT / "docs/DUPLICATION_AUDIT.md"
        self.assertTrue(audit.is_file(), "KNOWN_COLLISIONS must be mirrored in docs/DUPLICATION_AUDIT.md")
        text = audit.read_text(encoding="utf-8")
        for name in KNOWN_COLLISIONS:
            self.assertIn(name, text, f"{name} is in the allowlist but not in the audit")


if __name__ == "__main__":
    unittest.main()
