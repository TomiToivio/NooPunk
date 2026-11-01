"""The author-led design workflow must stay linked and singular (#989).

`design/README.md` is the single source of truth; `AGENTS.md` points at it. The risk this guards is not that
someone deletes the workflow but that the link rots, or that a second copy grows somewhere and drifts.

`unittest.TestCase`, not bare `def test_*()`: CI runs `python -m unittest discover`, which collects nothing
from module-level functions. A policy guard that never runs in the pipeline that gates the merge is not a
guard.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "design" / "README.md"
AGENTS = ROOT / "AGENTS.md"

#: Every document type the workflow defines. Collapsing any of these changes the content model.
DOCUMENT_TYPES = (
    "Day", "Character", "Mission", "Interaction", "Storyline",
    "Missions", "Location", "Rules", "Encounters", "Events",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def top_sections(text: str, count: int) -> list[str]:
    """The first ``count`` top-level sections, split on ``# `` headings."""
    parts = re.split(r"(?m)^# ", text)
    return [part for part in parts[:count + 1] if part.strip()]


class DesignWorkflowPolicyTests(unittest.TestCase):
    def test_the_canonical_workflow_exists(self) -> None:
        self.assertTrue(DESIGN.exists(), "design/README.md is the single source of truth and must exist")
        self.assertGreater(DESIGN.stat().st_size, 0)

    def test_the_workflow_states_all_three_steps(self) -> None:
        body = read(DESIGN).lower()
        self.assertIn("design document", body, "step 1: Tomi writes a design document")
        self.assertIn("issue", body, "step 2: Tomi opens an issue from that document")
        self.assertIn("implement", body, "step 3: agents implement that document")

    def test_every_document_type_is_defined(self) -> None:
        body = read(DESIGN)
        missing = [kind for kind in DOCUMENT_TYPES if not re.search(rf"\b{kind}\b", body)]
        self.assertEqual(missing, [], f"document types not defined in design/README.md: {missing}")

    def test_day_and_storyline_stay_distinct(self) -> None:
        """Day events follow world time; the storyline follows the player. Collapsing them is a content bug."""
        body = read(DESIGN).lower()
        self.assertIn("day", body)
        self.assertIn("storyline", body)
        self.assertIn("regardless", body, "day events must be described as independent of player progress")
        self.assertIn("progress", body, "the storyline must be described as progression-gated")

    def test_root_agents_opens_with_the_design_workflow(self) -> None:
        """The workflow must be the first thing an agent reads, not a footnote."""
        sections = top_sections(read(AGENTS), 1)
        opening = sections[0] if sections else ""
        self.assertIn("#989", opening, "the design workflow must be the opening section of AGENTS.md")
        self.assertIn("design/README.md", opening, "the opening section must link the source of truth")

    def test_the_workflow_is_binding_and_singular(self) -> None:
        agents = read(AGENTS)
        self.assertIn("design/README.md", agents)
        self.assertRegex(agents, r"(?i)binding|mandatory",
                         "the workflow must be stated as binding, not advisory")
        # The authority may be stated either way; what matters is that AGENTS.md names one place.
        self.assertRegex(agents, r"(?i)single source of truth|and \*\*only\*\* there",
                         "AGENTS.md must say where the authority lives")

    def test_document_types_are_defined_in_one_place_only(self) -> None:
        """AGENTS.md must point at design/README.md for the types rather than restating them."""
        self.assertRegex(read(AGENTS), r"(?i)(defined in|only there|and \*\*only\*\* there)",
                         "AGENTS.md must defer the document types to design/README.md")

    def test_the_boundaries_are_stated_near_the_workflow(self) -> None:
        agents = read(AGENTS)
        for needle, why in (
            ("English only", "agents write English only"),
            ("Finnish", "Tomi's Finnish is preserved verbatim"),
            ("Evennia", "the Python Evennia MUD is the runtime"),
            ("Cities Without Number", "CWN remains the rules foundation"),
        ):
            self.assertIn(needle, agents, f"AGENTS.md must state the boundary: {why}")

    def test_no_other_file_declares_a_competing_workflow(self) -> None:
        """Only design/README.md may *define* the workflow.

        A summary that links back to it is how an agent finds the source, and is allowed. A summary that
        restates the three steps *without* linking is a second workflow waiting to drift out of sync.
        """
        offenders = []
        for path in ROOT.rglob("*.md"):
            if path.parts[0] in {"legacy", ".git"} or "node_modules" in path.parts:
                continue
            if path.resolve() == DESIGN.resolve():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            lowered = text.lower()
            if "design/README.md" in text:
                continue
            if "design document" in lowered and "agents implement" in lowered and "issue" in lowered:
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual(offenders, [],
                         "these files restate the design workflow instead of linking it: "
                         + ", ".join(offenders))


if __name__ == "__main__":
    unittest.main()
