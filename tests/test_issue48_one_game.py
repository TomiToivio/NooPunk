"""Guard for docs/NOOPUNK_AS_ONE_GAME.md (issue #48).

#48 revises #40's multi-product framing: NoöPunk is one computer RPG/simulation, not
a tabletop RPG plus a simulation plus a videogame. That is a *documentation*
correction, so these are STRUCTURE guards.

They deliberately do NOT remove the words "tabletop", "godot" or "concordia" from the
repository: the existing design-principles guard requires all three to remain, and
those words still name notation and runtime sequence. What this file checks is that
the revision is recorded, that the older documents point at it, and that nothing
claims separate products are maintained.

What is protected here:

* the canonical statement exists and is reachable from the README and AGENTS.md;
* it states the single-product rule and the one-rule-model principle;
* it records what #48 revises from #40 -- and what survives -- rather than silently
  contradicting a document delivered earlier;
* it records that Godot is deferred, while noting the existing scaffold is preserved;
* the older documents now defer to it instead of implying separate products;
* it does not fabricate the rulebook's unfinished mechanics or the worldbook.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

CANON = "docs/NOOPUNK_AS_ONE_GAME.md"

#: Documents that must now defer to the canonical statement.
REFERRING = ("README.md", "AGENTS.md", "docs/DESIGN_PRINCIPLES.md")


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def normalised(relative: str) -> str:
    text = read(relative)
    text = re.sub(r"[*`]", "", text)
    text = re.sub(r"(?m)^\s*>\s?", " ", text)
    return " ".join(text.split()).lower()


class CanonicalStatementTests(unittest.TestCase):
    def test_canonical_document_exists(self) -> None:
        self.assertTrue((ROOT / CANON).exists(), f"{CANON} is missing")

    def test_reader_can_find_it_from_the_readme(self) -> None:
        self.assertIn(CANON, read("README.md"))

    def test_reader_can_find_it_from_the_agent_rules(self) -> None:
        self.assertIn(CANON, read("AGENTS.md"))

    def test_states_the_single_product_rule(self) -> None:
        text = normalised(CANON)
        self.assertIn("there is only one noöpunk rpg/simulation", text)

    def test_states_the_guiding_definition(self) -> None:
        text = normalised(CANON)
        self.assertIn("one python rpg/social simulation", text)

    def test_states_llms_narrate_and_rules_resolve(self) -> None:
        text = normalised(CANON)
        self.assertIn("llms choose, interpret, converse and narrate. rules resolve", text)

    def test_states_one_rule_model_with_two_notations(self) -> None:
        text = normalised(CANON)
        self.assertIn("one rule model", text)
        self.assertIn("human-readable", text)


class RevisionIsRecordedTests(unittest.TestCase):
    """#48 revises #40; the revision must be visible, not silent."""

    def test_names_that_it_revises_issue_40(self) -> None:
        """The doc must name *what* it revises, not merely contain the word.

        A bare "revises" assertion passes even after the specific claim is replaced,
        because the word recurs elsewhere in the document. The property worth
        guarding is that the multi-product framing is named as the thing revised.
        """
        text = normalised(CANON)
        self.assertIn("#40", read(CANON))
        self.assertIn("revises the multi-product", text)
        self.assertIn("multi-product framing", text)

    def test_records_what_survives_from_issue_40(self) -> None:
        """A reader must be able to see the carried-forward spine, not just the change."""
        text = normalised(CANON)
        for kept in ("one shared world state + event log as the spine", "deterministic resolution"):
            with self.subTest(kept=kept):
                self.assertIn(kept, text)

    def test_records_that_the_implemented_core_is_unaffected(self) -> None:
        text = normalised(CANON)
        self.assertIn("src/simulation/", text)
        self.assertIn("unaffected", text)


class GodotDeferralTests(unittest.TestCase):
    def test_records_godot_as_deferred(self) -> None:
        text = normalised(CANON)
        self.assertIn("godot", text)
        self.assertIn("deferred", text)

    def test_records_that_the_existing_scaffold_is_preserved(self) -> None:
        """Deferral must not be read as permission to delete the scaffold."""
        text = normalised(CANON)
        self.assertIn("src/godot/", text)
        self.assertIn("preserved rather than deleted", text)

    def test_does_not_delete_the_runtime_words_elsewhere(self) -> None:
        """The design-principles guard requires all three words; deferral is not removal."""
        text = normalised("docs/DESIGN_PRINCIPLES.md")
        for runtime in ("tabletop", "godot", "concordia"):
            with self.subTest(runtime=runtime):
                self.assertIn(runtime, text)


class ReferringDocsTests(unittest.TestCase):
    def test_older_documents_defer_to_the_canonical_statement(self) -> None:
        for doc in REFERRING:
            with self.subTest(doc=doc):
                self.assertIn(
                    "NOOPUNK_AS_ONE_GAME.md",
                    read(doc),
                    f"{doc} does not point at the canonical single-product statement",
                )

    def test_agents_md_no_longer_implies_three_products(self) -> None:
        section = re.search(
            r"(?ms)^### 11\. One RPG, three runtimes.*?(?=\n### |\Z)", read("AGENTS.md")
        )
        self.assertIsNotNone(section, "AGENTS.md §11 not found")
        assert section is not None
        text = " ".join(section.group(0).split()).lower()
        self.assertIn("single game", text)
        self.assertIn("rather than three products", text)

    def test_design_principles_balance_two_is_reframed(self) -> None:
        text = normalised("docs/DESIGN_PRINCIPLES.md")
        self.assertIn("not about maintaining three products", text)


class AntiInventionTests(unittest.TestCase):
    """#48 lists many mechanics and a whole worldbook; none may be invented here."""

    def test_does_not_fabricate_the_worldbook(self) -> None:
        self.assertFalse(
            (ROOT / "WORLDBOOK.md").exists(),
            "WORLDBOOK.md is author-owned setting material and must not be invented "
            "by an agent (AGENTS.md §1)",
        )

    def test_says_the_worldbook_is_author_owned(self) -> None:
        text = normalised(CANON)
        self.assertIn("worldbook.md does not exist yet", text)
        self.assertIn("author-owned", text)

    def test_does_not_authorise_inventing_rulebook_mechanics(self) -> None:
        text = normalised(CANON)
        self.assertIn("does not license inventing the rulebook's unfinished mechanics", text)

    def test_does_not_introduce_numeric_mechanics(self) -> None:
        """#48 lists skills and stats as examples; the doc must not define them."""
        body = read(CANON)
        for invented in ("skill list is", "the attribute scale is", "damage is"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, body.lower())

    def test_existing_rulebook_is_not_rewritten_here(self) -> None:
        """Phase 1 is documentation reconciliation, not a rulebook edit."""
        text = normalised("RULEBOOK.md")
        self.assertIn("intentionally incomplete", text)


class CoreStillRunsWithoutConcordiaTests(unittest.TestCase):
    def test_says_the_game_must_not_require_concordia(self) -> None:
        """Otherwise the deferred-frontend rule would be contradicted by a hard dep."""
        text = normalised(CANON)
        self.assertIn("does not make concordia required to run the game", text)

    def test_phase_b_core_has_no_concordia_import(self) -> None:
        for name in ("events.py", "world_state.py", "engine.py", "sqlite_store.py"):
            with self.subTest(module=name):
                source = (ROOT / "src" / "simulation" / name).read_text(encoding="utf-8")
                self.assertNotIn("import concordia", source)


if __name__ == "__main__":
    unittest.main()
