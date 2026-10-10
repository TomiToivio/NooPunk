"""Compatibility guard: issue #144 supersedes issue #108 UNHSS / Firewall naming."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
FACTIONS = (ROOT / "FACTIONS.md").read_text(encoding="utf-8")
ORG = (ROOT / "data" / "world" / "organizations.yaml").read_text(encoding="utf-8")


def _canon_prose(document: str) -> str:
    """The canonical prose, excluding the Change ledger section.

    The ledger (§27) legitimately *quotes* superseded tokens to record the change, so it
    must not be scanned for them. Exclude only that section's span: a naive
    ``split("## 27. Change ledger")[0]`` also drops everything AFTER the ledger, which
    hides the later chapters (§33, §39) where stale prose actually survived.
    """
    before, sep, rest = document.partition("## 27. Change ledger")
    if not sep:
        return document
    after = rest.partition("\n## ")[2]  # resume at the next `## ` heading (§28)
    return before + after


class Issue108SupersededBy144Tests(unittest.TestCase):
    def test_unsa_is_the_canonical_successor(self):
        self.assertIn("United Nations Security Administration (UNSA)", BOOK)
        self.assertIn("supersedes the UNHSS / Firewall naming", BOOK)
        self.assertIn("## Default Helsinki / UNSA affiliation", FACTIONS)

    def test_default_pc_is_unsa_agent(self):
        self.assertIn("belongs to and works for UNSA", BOOK)
        self.assertIn("default: newly graduated UNSA agent on first assignment", ORG)
        self.assertIn("multi_faction_membership: true", ORG)

    def test_unsa_keeps_the_broad_human_security_mission(self):
        for phrase in (
            "law-enforcement", "intelligence", "counterintelligence",
            "scientific research", "civil-defence", "disaster relief",
            "planetary defence", "Wallfacer",
        ):
            self.assertIn(phrase.lower(), BOOK.lower())

    def test_machine_readable_model_uses_unsa(self):
        self.assertIn("UNSA:", ORG)
        self.assertIn("canonical_name: United Nations Security Administration", ORG)
        self.assertNotIn("\nUNHSS:", ORG)


class NoStaleInWorldUnhssTests(unittest.TestCase):
    """The rename must reach the canonical prose, not only the data files.

    PR #149 was rebased to a single file before merge, so the ``RULEBOOK.md`` half of
    the rename never landed: three live in-world uses of ``UNHSS`` survived next to the
    new UNSA section, leaving the book contradicting itself. Pin them out.

    The one legitimate occurrence is the supersession note, which has to *quote* the old
    name to say it is superseded; that line is exempted explicitly.
    """

    def test_rulebook_has_no_in_world_unhss(self):
        # The Change ledger (§27) and the §38 supersession note must QUOTE the old name to
        # record/deny it, so both are exempt; every other mention is live canon.
        prose = _canon_prose(BOOK)
        stale = [
            line for line in prose.splitlines()
            if "UNHSS" in line and "supersedes the UNHSS" not in line
        ]
        self.assertEqual(stale, [], f"stale in-world UNHSS survived in RULEBOOK.md: {stale}")

    def test_factions_md_marks_unhss_as_superseded(self):
        # FACTIONS.md may name it only while saying it is replaced.
        for line in FACTIONS.splitlines():
            if "UNHSS" in line:
                with self.subTest(line=line):
                    self.assertIn("replaces", line)


if __name__ == "__main__":
    unittest.main()
