# -*- coding: utf-8 -*-
"""Guard for the #95 author-statement sources that were still missing from the rulebook.

Issue #95 is the author's own statement of what NoöPunk is. The author moved it into
``RULEBOOK.md`` (commit ``2b33446``, §2.1–§2.6). That integration covered the substance but
omitted several **named sources** the issue lists, which this guard pins:

* the **LaclauGPT Phase 1 paper** link in §2.1;
* the AI-spectrum names in §2.2 — **Ben Goertzel**'s *A Cosmist Manifesto*, **Timnit Gebru**
  and **Émile P. Torres** on the **TESCREAL** bundle, and **Nate Soares** / **Eliezer
  Yudkowsky**'s *If Anyone Builds It, Everyone Dies*.

It is a structure guard in the style of ``test_issue60_setting_canon.py``: it asserts the
issue's own named sources are recorded, without inventing anything the issue did not say.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = "RULEBOOK.md"


def read() -> str:
    return (ROOT / RULEBOOK).read_text(encoding="utf-8")


def section2() -> str:
    """Body of §2 (from '## 2.' up to '## 3.')."""
    text = read()
    marker = "## 2. Current project description"
    if marker not in text:
        return ""
    body = text.split(marker, 1)[1]
    nxt = re.search(r"(?m)^## 3\. ", body)
    return body[: nxt.start()] if nxt else body


def flat() -> str:
    text = re.sub(r"[>*_`]", " ", read())
    return " ".join(text.split()).lower()


def flat2() -> str:
    text = re.sub(r"[>*_`]", " ", section2())
    return " ".join(text.split()).lower()


class LaclauGptReferenceTests(unittest.TestCase):
    def test_the_phase_1_paper_is_linked(self) -> None:
        text = read()
        self.assertIn("LaclauGPT", text)
        self.assertIn(
            "github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md", text
        )


class AiSpectrumSourceTests(unittest.TestCase):
    """Issue #95 names specific works for each current; all three must be recorded."""

    def test_the_accelerationist_and_cosmist_sources(self) -> None:
        text = flat()
        self.assertIn("kurzweil", text)
        self.assertIn("singularity is nearer", text)
        self.assertIn("goertzel", text)
        self.assertIn("cosmist manifesto", text)

    def test_the_critical_ai_sources_and_tescreal(self) -> None:
        text = flat()
        self.assertIn("gebru", text)
        self.assertIn("torres", text)
        self.assertIn("tescreal", text)

    def test_the_existential_risk_sources(self) -> None:
        text = flat()
        self.assertIn("soares", text)
        self.assertIn("yudkowsky", text)
        self.assertIn("if anyone builds it", text)

    def test_the_full_spectrum_statement_is_kept(self) -> None:
        self.assertIn("full ideological spectrum", flat())


class NoInventionTests(unittest.TestCase):
    def test_the_additions_add_no_mechanics(self) -> None:
        text = flat2()
        for mechanic in ("2d6", "hit point", "initiative", "skill check"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, text)

    def test_the_issue_95_substance_survived(self) -> None:
        """The author's statement itself must still be present, not replaced."""
        text = flat2()
        for concept in ("laclau", "castells", "lindgren", "noösphere", "portmanteau",
                        "cortical stacks", "core design identity"):
            with self.subTest(concept=concept):
                self.assertIn(concept, text)


if __name__ == "__main__":
    unittest.main()
