"""Executable contracts for the issue #569 similarity audit.

Code-only, per `AGENTS.md` and issue #271. The audit is the item the rights matrix left open
(*"a complete repository-wide similarity audit remains outstanding"*), so its arithmetic is pinned
here on **synthetic** corpora — the real books are not in the repository and must not be.

What is asserted:

* normalisation is deterministic and punctuation/case insensitive, so a copied sentence is found even
  after reformatting;
* a shared run of `N` words is a hit and a paraphrase is not, which is the difference between a
  similarity audit and the name/keyword ban the rights matrix correctly refuses;
* a hit that also exists in the CC0 corpus is classified **attributable**, not blocked-only — the
  distinction that stops the audit from either excusing copying or crying wolf;
* the report never carries the matched text, only the location and the count.

Run:
    python -m unittest discover -s tests -p "test_audit_without_number_expression.py"
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import audit_without_number_expression as audit  # noqa: E402

SOURCE = (
    "A character has six attributes ranging from three to eighteen reflecting a range "
    "from the minimum viable capacity for a playable character to the maximum normal."
)
PARAPHRASE = (
    "Player characters carry six stats spanning three to eighteen, from the weakest viable "
    "build up to the strongest ordinary human."
)


def tree_with(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp(prefix="wn-audit-"))
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


class NormalisationTests(unittest.TestCase):
    def test_words_strips_case_and_punctuation(self) -> None:
        self.assertEqual(audit.words("Roll 2d6, add SKILL!"), ["roll", "2d6", "add", "skill"])

    def test_shingles_are_a_set_of_the_requested_length(self) -> None:
        tokens = "one two three four five six".split()
        self.assertEqual(len(audit.shingles(tokens, 3)), 4)
        self.assertEqual(audit.shingles(tokens[:2], 3), set())


class DetectionTests(unittest.TestCase):
    def test_a_copied_run_is_found_and_a_paraphrase_is_not(self) -> None:
        corpus = audit.Corpus()
        corpus.add("blocked-book", SOURCE)
        copied = tree_with({"docs/copied.md": "Intro.\n\n" + SOURCE + "\n"})
        paraphrased = tree_with({"docs/own.md": PARAPHRASE})

        self.assertTrue(audit.scan_file(copied / "docs/copied.md", corpus, copied))
        self.assertEqual(audit.scan_file(paraphrased / "docs/own.md", corpus, paraphrased), [])

    def test_the_finding_points_at_the_right_line(self) -> None:
        corpus = audit.Corpus()
        corpus.add("blocked-book", SOURCE)
        root = tree_with({"a.md": "line one\nline two\n" + SOURCE + "\n"})
        findings = audit.scan_file(root / "a.md", corpus, root)
        self.assertTrue(findings)
        self.assertEqual(findings[0].line, 3)
        self.assertEqual(findings[0].matched_words, audit.SHINGLE_WORDS)

    def test_quarantined_paths_are_classified(self) -> None:
        corpus = audit.Corpus()
        corpus.add("blocked-book", SOURCE)
        root = tree_with({"docs/archive/old.md": SOURCE})
        report = audit.audit(corpus, None, root)
        self.assertEqual(report["first_party"]["hits"], 0)
        self.assertGreater(report["quarantined"]["hits"], 0)
        self.assertEqual(report["quarantined"]["files"][0]["path"], "docs/archive/old.md")
        self.assertTrue(report["clean"])


class AttributionTests(unittest.TestCase):
    def test_a_hit_that_is_also_cc0_is_attributable_not_blocked(self) -> None:
        blocked = audit.Corpus()
        blocked.add("blocked-book", SOURCE)
        cc0 = audit.Corpus()
        cc0.add("cc0-srd", SOURCE)
        root = tree_with({"src/borrowed.md": SOURCE})

        report = audit.audit(blocked, cc0, root)
        self.assertEqual(report["first_party"]["hits"], report["first_party"]["attributable"])
        self.assertEqual(report["first_party"]["blocked_only"], 0)
        self.assertTrue(report["clean"])

    def test_a_blocked_only_hit_is_not_clean(self) -> None:
        blocked = audit.Corpus()
        blocked.add("blocked-book", SOURCE)
        root = tree_with({"src/copied.md": SOURCE})
        report = audit.audit(blocked, audit.Corpus(), root)
        self.assertEqual(report["first_party"]["blocked_only"], report["first_party"]["hits"])
        self.assertFalse(report["clean"])


class ReportShapeTests(unittest.TestCase):
    def test_the_report_never_carries_the_matched_text(self) -> None:
        blocked = audit.Corpus()
        blocked.add("blocked-book", SOURCE)
        root = tree_with({"src/copied.md": SOURCE})
        report = audit.audit(blocked, None, root)
        rendered = audit.format_report(report)
        for word in ("attributes", "eighteen", "viable"):
            self.assertNotIn(word, rendered.lower())

    def test_the_audit_is_deterministic(self) -> None:
        blocked = audit.Corpus()
        blocked.add("blocked-book", SOURCE)
        root = tree_with({"src/a.md": SOURCE, "src/b.md": PARAPHRASE})
        self.assertEqual(audit.audit(blocked, None, root), audit.audit(blocked, None, root))


if __name__ == "__main__":
    unittest.main()
