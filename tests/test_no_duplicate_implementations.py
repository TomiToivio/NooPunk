"""Guards against the failure mode this repository keeps producing: two agents, one feature, two files.

Nothing here checks style. Each test asserts that a feature has **one** home, and fails when a second one appears —
because a duplicate does not announce itself, it arrives as a reasonable-looking parallel implementation and is
discovered three weeks later when the two disagree.

If a test here fails, the answer is almost never "register the new path". It is to decide which implementation is
canonical, delete the other, and record the decision in `docs/DUPLICATION_AUDIT.md`.

**Why these are `unittest` classes and not bare functions.** The root suite runs
`python -m unittest discover -s tests -p "test_*.py"`, which collects `unittest.TestCase` subclasses only. This
file was originally written as five bare `def test_*()` functions: correct assertions, 5 passing under pytest,
and **0 tests collected** by the command CI actually runs. The guard against duplicate work was green by
absence — it had never executed in CI. Anything added here must live in a `unittest.TestCase` or it is a
comment with extra steps.
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


class OneHomePerFeatureTests(unittest.TestCase):
    """Every feature has exactly one implementation, or a written reason why not."""

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
        self.assertFalse(
            unexplained,
            f"new duplicate module names: {unexplained}. Decide which is canonical, delete the other, or add "
            f"a justified entry to KNOWN_COLLISIONS and docs/DUPLICATION_AUDIT.md.")

    def test_every_known_collision_has_a_written_reason(self):
        for name, reason in KNOWN_COLLISIONS.items():
            self.assertGreater(len(reason), 60, f"{name}: the reason is too short to be a decision")
        audit = ROOT / "docs/DUPLICATION_AUDIT.md"
        self.assertTrue(audit.is_file(), "KNOWN_COLLISIONS must be mirrored in docs/DUPLICATION_AUDIT.md")
        text = audit.read_text(encoding="utf-8")
        for name in KNOWN_COLLISIONS:
            self.assertIn(name, text, f"{name} is in the allowlist but not in the audit")


class OneCanonicalDocumentTests(unittest.TestCase):
    """Several agents have written the same audit. Exactly one may claim to be canonical per family."""

    #: Document families that have genuinely produced competing files, each answering one question.
    #:
    #: Deliberately *not* `*PARITY*`: `CWN_SRD_PARITY_AUDIT_858.md` (Godot SRD evidence for #858) and
    #: `PORTABLE_RULES_PARITY.md` (portable rulebook ↔ Python contract for #1053) both say "parity" and answer
    #: different questions. A family is a question, not a word in a filename — matching on the word produced
    #: exactly the false positive this repository keeps making.
    FAMILIES = ("*COVERAGE*", "*DUPLICATION_AUDIT*")

    def test_one_document_per_family_claims_canonical(self):
        for family in self.FAMILIES:
            with self.subTest(family=family):
                docs = sorted((ROOT / "docs").rglob(family))
                canonical = []
                for path in docs:
                    text = path.read_text(encoding="utf-8", errors="ignore")
                    if re.search(r"canonical", text, re.IGNORECASE) and "pointer" not in text[:400].lower():
                        canonical.append(path.name)
                self.assertLessEqual(
                    len(canonical), 1,
                    f"more than one {family} document claims to be canonical: {canonical}")


if __name__ == "__main__":
    unittest.main()
