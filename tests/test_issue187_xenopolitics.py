"""Structure guard for the #187 xenopolitics chapter (``rulebook/15_XENOPOLITICS.md``).

Why this exists: #187 asked for a *concise but substantial* xenopolitics section, and the
situation it describes is the setting's most ambiguity-sensitive material — the two NHI
blocs, the Law-of-One movement and the hybrid panic. Two failure modes are worth pinning
rather than hoping for:

1. **The chapter rots unlinked.** A chapter nobody links is a chapter nobody reads, and a
   later rename would leave the registry pointing at nothing. The other modular chapters are
   pinned this way; this one is pinned the same way.
2. **The chapter starts settling what the setting must keep open.** The deliverable is a
   *field of positions*, not a verdict, and it must not smuggle in statistics, dates or
   mechanics that ``AGENTS.md`` §4/§6 and the canonical-uncertainty rule (§33.32) leave open.

This guard asserts **structure and bound**, never wording: the chapter may be rewritten
freely as long as it exists, is linked by path, keeps a heading, states its scope bound, and
does not acquire the reserved artefacts.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = ROOT / "RULEBOOK.md"
CHAPTER = ROOT / "rulebook" / "15_XENOPOLITICS.md"


def flat(path: Path) -> str:
    """Chapter text with blockquote markers and wrapping removed.

    The chapters wrap prose at ~90 columns and carry several of the phrases this guard
    asserts inside blockquotes (``> **...**``). Collapse whitespace so a phrase split across
    a line wrap still matches, and drop ``>`` so a blockquoted phrase is found too.
    """
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^\s*>\s?", "", text)
    return re.sub(r"\s+", " ", text)


class XenopoliticsChapterTests(unittest.TestCase):
    def test_chapter_exists_with_its_heading(self) -> None:
        self.assertTrue(CHAPTER.exists(), "rulebook/15_XENOPOLITICS.md is missing")
        self.assertRegex(flat(CHAPTER), r"^# Xenopolitics\b",
                         "the chapter heading was renamed or removed")

    def test_chapter_is_linked_from_the_rulebook_by_path(self) -> None:
        """Pin the **path**, not the bare filename: a label alone satisfies a name match."""
        self.assertIn("rulebook/15_XENOPOLITICS.md",
                      RULEBOOK.read_text(encoding="utf-8"),
                      "RULEBOOK.md does not link rulebook/15_XENOPOLITICS.md")

    def test_chapter_states_its_scope_bound(self) -> None:
        """The chapter must keep its explicit 'what this does NOT define' section."""
        self.assertRegex(flat(CHAPTER), r"does NOT define")

    def test_chapter_keeps_both_blocs_and_the_sovereignty_question(self) -> None:
        """The issue's own spine: two blocs, the aid premise, and the central question."""
        text = flat(CHAPTER)
        self.assertRegex(text, r"Confederation")
        self.assertRegex(text, r"Orion")
        self.assertRegex(text, r"sovereignty")

    def test_chapter_defines_no_numeric_statistics(self) -> None:
        """A *stat block* is detected: a numeric column that is not a leading key column.

        Rationale: the reserved areas (`AGENTS.md` §4) forbid statistics. A legitimate gloss
        table may still lead with a numeric **key** (``| +10 | love |`` — the Affect scale),
        so a bare "all-numeric column" rule would false-positive on canon prose. What is
        forbidden here is a numeric column *other than the first* — the shape of a stat line
        (``| Grey | 7 | 12 |``, ``| type A | 87 |``) rather than a labelled scale.
        """
        offenders: list[str] = []
        columns: dict[int, list[str]] = {}
        rows_in_table = 0
        header_seen = False

        def flush() -> None:
            nonlocal columns, rows_in_table, header_seen
            if rows_in_table >= 2:
                for idx, cells in columns.items():
                    if idx == 0:
                        continue  # a leading key column may be numeric (a scale)
                    if len(cells) >= 2 and all(
                        c and re.fullmatch(r"[-−+]?\d+(?:[.,]\d+)?%?", c) for c in cells
                    ):
                        offenders.append(f"numeric column {idx}: {cells}")
            columns = {}
            rows_in_table = 0
            header_seen = False

        for line in CHAPTER.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                flush()
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) or not c for c in cells):
                continue  # markdown separator row
            if not header_seen:
                header_seen = True
                continue  # the first row is the header, never a data cell
            rows_in_table += 1
            for idx, cell in enumerate(cells):
                columns.setdefault(idx, []).append(cell)
        flush()

        self.assertEqual(offenders, [],
                         "the xenopolitics chapter must not tabulate statistics:\n  "
                         + "\n  ".join(offenders))

    def test_ledger_has_the_xenopolitics_section(self) -> None:
        """The chapter must also be discoverable from the ledger itself, not only the TOC.

        The `## N.` ledger is the primary reading surface; §40–§44 are the precedent for
        cross-chapter lore living there. A chapter reachable only through a TOC bullet is
        easy to miss, so pin the ledger section and its link back to the chapter.
        """
        text = RULEBOOK.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^## 53\. Xenopolitics after the NHI Crisis",
                         "RULEBOOK.md lost the §53 xenopolitics ledger section")
        self.assertIn("rulebook/15_XENOPOLITICS.md", text,
                      "the §53 ledger section must link the full chapter")

    def test_chapter_leaves_the_central_question_open(self) -> None:
        """The ambiguity is load-bearing: the chapter must not declare a verdict."""
        text = flat(CHAPTER)
        # It must name the canonical-uncertainty rule it is deferring to.
        self.assertRegex(text, r"§?\s*33\.32",
                         "the chapter must cite the canonical-uncertainty rule (§33.32)")

    def test_chapter_keeps_the_pre_fall_bound(self) -> None:
        """The #187 premise ('ASI holocaust') must not upgrade into a global Fall.

        `RULEBOOK.md` §33.1 (pre-Fall; Earth inhabited and central) and §33.28 (disasters
        'severe but uneven rather than a single planet-destroying Fall') bound how far the
        catastrophe may be read. This is the canon trap a naive reading of the issue walks
        straight into, so pin the reconciliation rather than trusting it to survive edits.
        """
        text = flat(CHAPTER)
        self.assertRegex(text, r"pre-Fall",
                         "the chapter must keep the pre-Fall bound (RULEBOOK.md §33.1)")
        self.assertRegex(text, r"§\s*33\.1\b",
                         "the chapter must cite §33.1 for the pre-Fall bound")
        self.assertRegex(text, r"§\s*33\.28",
                         "the chapter must cite §33.28 for the 'severe but uneven' scale")
        self.assertRegex(text, r"regional catastrophes",
                         "the chapter must state the regional-catastrophe reconciliation")

    def test_chapter_keeps_both_blocs_aid_genuine(self) -> None:
        """The issue's central premise: both sides genuinely help. Pin it verbatim."""
        self.assertRegex(flat(CHAPTER), r"both want Earth to remain a living world",
                         "the chapter must keep the 'both blocs want a living Earth' premise")


if __name__ == "__main__":
    unittest.main()
