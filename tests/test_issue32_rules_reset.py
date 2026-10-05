# -*- coding: utf-8 -*-
"""Regression tests for issue #32: the Luhmannian four-system rules reset.

These are STRUCTURE guards, in the style of ``test_design_principles.py``. They
assert that the reset is recorded consistently across the documents and that the
superseded legacy material was *superseded, not deleted*. They deliberately do NOT constrain
mechanics: the memo is exploratory and #32 forbids finalizing dice, skills,
attributes, combat, or character creation.

What is protected here:

* the memo exists and answers the ten questions the issue asks;
* the memo contains 2-4 candidate attribute structures and selects none;
* the memo keeps the later metaphysical layers modular;
* the superseded legacy documents carry a superseded header and are still present (the repo
  treats old material as warehouse -- never delete);
* the README and the published site state that NoöPunk is developing an
  original rules system, and no document offers another RPG as the chassis.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MEMO = "docs/archive/RULES_RESET_MEMO.md"
#: Documents that must record the reset direction.
#:
#: These were historically `CWN_DOCS`, guarding that the superseded external-chassis
#: material was marked rather than deleted. The author has since removed that
#: material (commit e017274 deleted `docs/CWN_CHASSIS.md`) and removed the chassis
#: policy from `AGENTS.md`/`DESIGN_PRINCIPLES.md`, so there is nothing left to keep
#: as superseded warehouse. What survives of the guard is that both remaining
#: documents record the reset direction, which is what is asserted below.
LEGACY_DOCS = ("docs/archive/RULES_RESET_MEMO.md", "docs/archive/RULEBOOK.md")

#: The four Luhmannian systems, as named by the issue.
SYSTEMS = ("social", "physical", "psychic", "cybernetic")

#: Documents that must record the new direction.
DIRECTION_DOCS = ("README.md", "docs/index.html")

#: Games the issue forbids substituting as the chassis.
FORBIDDEN_CHASSIS = (
    "cyberpunk 2020",
    "cy_borg",
    "the sprawl",
    "fate",
    "pbta",
    "powered by the apocalypse",
    "brp",
    "year zero",
    "dungeons & dragons",
    "d&d",
)


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalised(relative: str) -> str:
    """Lowercased, whitespace-collapsed, markup-stripped text.

    Blockquote markers (``>``) and emphasis (``*``) survive whitespace collapsing
    and split sentences in multi-line callouts, which would hide a phrase that is
    plainly there when rendered. Strip them so the guard tests meaning, not
    raw markdown.
    """
    text = re.sub(r"[>*_`]", " ", read(relative))
    return " ".join(text.split()).lower()


class ResetMemoTests(unittest.TestCase):
    def test_memo_exists(self) -> None:
        self.assertTrue((ROOT / MEMO).exists(), f"{MEMO} is missing")

    def test_memo_names_all_four_systems(self) -> None:
        text = normalised(MEMO)
        for system in SYSTEMS:
            with self.subTest(system=system):
                self.assertIn(system, text)

    def test_memo_answers_the_ten_questions(self) -> None:
        """The issue lists ten questions the memo must answer.

        Checked structurally: the memo must name each topic the questions cover,
        so a memo that silently drops one is caught.
        """
        text = normalised(MEMO)
        for topic in (
            "what each system represents in play",
            "crossing domains",
            "minimum number of numbers",
            "undefined",
            "structurally different",
            "layering later material",
        ):
            with self.subTest(topic=topic):
                self.assertIn(topic, text)

    def test_memo_proposes_multiple_structures_and_selects_none(self) -> None:
        """A structural check that the candidates are plural and unselected."""
        text = read(MEMO)
        structures = re.findall(r"^### Structure ([A-D])\b", text, re.M)
        self.assertGreaterEqual(
            len(structures), 2, "the memo must propose at least two structures"
        )
        self.assertLessEqual(
            len(structures), 4, "the issue asks for 2-4 structures, no more"
        )
        lowered = text.lower()
        self.assertTrue(
            "none is selected" in lowered or "not selected" in lowered,
            "the memo must state that no structure is selected",
        )
        # It must not announce a winner.
        for phrase in ("the chosen structure is", "we select structure", "the winner is"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, lowered)

    def test_memo_keeps_later_metaphysics_modular(self) -> None:
        text = normalised(MEMO)
        for layer in ("law of one", "noösphere", "psionics"):
            with self.subTest(layer=layer):
                self.assertIn(layer, text)
        self.assertIn("coupling", text)

    def test_memo_states_it_finalizes_no_mechanics(self) -> None:
        text = normalised(MEMO)
        self.assertIn("nothing here is finalized", text)


class LegacySupersededNotDeletedTests(unittest.TestCase):
    """The reset supersedes obsolete chassis documents; it must not delete them."""

    def test_legacy_documents_still_exist(self) -> None:
        for doc in LEGACY_DOCS:
            with self.subTest(doc=doc):
                self.assertTrue((ROOT / doc).exists(), f"{doc} was deleted")
        self.assertTrue(
            (ROOT / "docs/archive/GAME_DESIGN_MEMO.md").exists(),
            "the #31 memo must survive the #32 reset",
        )

    def test_legacy_documents_record_the_reset(self) -> None:
        """Both legacy documents must record the reset in their opening header.

        The reset now *removes* the obsolete external-chassis material rather than
        marking it superseded, and the surviving documents are headed "ORIGINAL
        RULES RESET". Asserting the literal word "superseded" therefore tested a
        wording the author replaced. Accept either the current header wording or an
        explicit superseded marker, so the guard tests that the reset is recorded
        rather than which synonym was chosen.
        """
        for doc in LEGACY_DOCS:
            with self.subTest(doc=doc):
                head = normalised(doc)[:1200]
                self.assertTrue(
                    "original rules reset" in head
                    or "original rules system" in head
                    or "superseded" in head,
                    f"{doc} does not record the reset direction in its header",
                )

    def test_rulebook_still_holds_the_current_rules_in_force(self) -> None:
        """The reset records a direction; it does not silently repeal the rules."""
        head = normalised("docs/archive/RULEBOOK.md")[:1600]
        self.assertIn("remain in force only until the author revises them", head)

    def test_licensing_boundary_survives(self) -> None:
        """Dropping the chassis must not drop the licensing caution."""
        text = normalised("README.md")
        self.assertIn("design references", text)
        self.assertIn("attribution-noncommercial-sharealike", text)
        self.assertIn("not affiliated with or endorsed by posthuman studios", text)


class OriginalSystemDirectionTests(unittest.TestCase):
    def test_documents_state_the_current_rules_direction(self) -> None:
        """Issue #111 restores and specifies the independent-system direction."""
        # The repo spells the game "NoöPunk"; a sibling guard accepts either
        # spelling (test_issue78 does the same). Asserting only the ASCII form
        # tested wording the README never used.
        self.assertRegex(
            normalised("README.md"),
            r"independent no(?:ö|o)punkt? rules system|independent noöpunk rules system",
        )
        self.assertIn("1–10 stat", normalised("README.md"))
        with self.subTest(doc="docs/index.html"):
            self.assertIn("rulebook", normalised("docs/index.html"))

    def test_no_document_substitutes_another_rpg_as_the_chassis(self) -> None:
        """#32 forbids replacing the legacy chassis with another existing RPG's chassis.

        Scoped to a chassis claim, so a genuine design *reference* (the three
        balance poles) does not trip it.
        """
        docs = DIRECTION_DOCS + (MEMO,)
        for doc in docs:
            text = normalised(doc)
            for game in FORBIDDEN_CHASSIS:
                with self.subTest(doc=doc, game=game):
                    self.assertNotIn(
                        f"{game} as the chassis",
                        text,
                        f"{doc} substitutes {game} as the chassis",
                    )
                    self.assertNotIn(
                        f"chassis is {game}",
                        text,
                        f"{doc} substitutes {game} as the chassis",
                    )

    def test_memo_does_not_modify_the_protected_invariants(self) -> None:
        """AGENTS.md and DESIGN_PRINCIPLES.md are author-owned; the memo flags it.

        The rules-source invariant is build-enforced there, so the reset cannot
        be made coherent unilaterally. The memo must say so rather than quietly
        editing them.
        """
        # normalised() strips underscores, so match the document name loosely.
        text = normalised(MEMO)
        self.assertIn("agents.md", text)
        self.assertRegex(text, r"design.?principles.?md")
        self.assertIn("invariant", text)


if __name__ == "__main__":
    unittest.main()
