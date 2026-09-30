# -*- coding: utf-8 -*-
"""Regression tests for issue #22 — the CWN-modified skill system (tabletop only).

The author decision is **Skills = MODIFY**: NoöPunk adopts the Cities Without Number
SRD's level-0..4 trained-skill structure and standard skill list as a starting
chassis, with two renames and specialization deferred.

These tests pin the author-specified surface of that decision and, just as
importantly, pin what must **not** have been imported. #22 deliberately excludes the
adjacent CWN subsystems (character-creation picks, XP, level gating, Foci), so a
later reader cannot mistake this conversion for a broader port.

Run: python3 -m unittest discover -s tests -p 'test_*.py'
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RULEBOOK = ROOT / "RULEBOOK.md"
AGENTS = ROOT / "AGENTS.md"
POLICY = ROOT / "docs" / "CWN_CHASSIS.md"
CORE_JSON = ROOT / "data" / "rules" / "core.json"
GODOT_ADAPTER = ROOT / "src" / "godot" / "core_rules.gd"
CONCORDIA_MECHANICS = ROOT / "src" / "concordia_runtime" / "mechanics.py"

#: The Cities Without Number SRD standard list, with NoöPunk's two renames applied.
#: Order follows the SRD page (Heal -> Medical sits where Heal did; Know -> Science
#: where Know did).
EXPECTED_SKILLS = [
    "Administer", "Connect", "Drive", "Exert", "Fix", "Medical", "Science",
    "Lead", "Notice", "Perform", "Program", "Punch", "Shoot", "Sneak",
    "Stab", "Survive", "Talk", "Trade", "Work",
]

#: Renamed away from the SRD. Neither may survive as a NoöPunk skill name.
RETIRED_SKILL_NAMES = ["Heal", "Know"]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(path: Path) -> str:
    """Lowercased, whitespace-collapsed, emphasis stripped."""
    return " ".join(_text(path).replace("*", "").split()).lower()


def _skills_section() -> str:
    text = _text(RULEBOOK)
    return text[text.index("### 5.3 Skills"):text.index("### 5.4")]


def _flat_section(heading: str, next_heading: str) -> str:
    """Flattened, lowercased, emphasis-stripped body between two headings."""
    text = _text(RULEBOOK).replace("*", "")
    body = text[text.index(heading):text.index(next_heading)]
    return " ".join(body.split()).lower()


def _bullet_names(section: str) -> list[str]:
    """Skill names from the `- **Name** — ...` list entries."""
    return re.findall(r"^- \*\*([A-Z][A-Za-z]*)\*\* — ", section, re.M)


class SkillScaleTests(unittest.TestCase):
    """Level-0..4 for trained skills; unskilled outside the numbering."""

    def test_chassis_matrix_marks_skills_modify(self) -> None:
        text = _text(POLICY)
        status = text[text.index("### Review status"):text.index("## NoöPunk decisions")]
        rows = {}
        for line in status.splitlines():
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip().replace("*", "") for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0]:
                rows[cells[0].lower()] = cells[1].upper()
        self.assertEqual(rows.get("skills"), "MODIFY")

    def test_modify_reason_states_the_author_conditions(self) -> None:
        """The matrix note itself must carry the four conditions of the decision."""
        text = _flat(POLICY)
        self.assertIn("level-0..4", text)
        self.assertIn("heal renamed medical", text)
        self.assertIn("know renamed science", text)
        self.assertIn("specialization mechanics deferred", text)

    def test_trained_scale_is_zero_through_four(self) -> None:
        flat = _flat(RULEBOOK)
        for level in ("level-0", "level-1", "level-2", "level-3", "level-4"):
            with self.subTest(level=level):
                self.assertIn(level, flat)
        # the intro phrase wraps a blockquote marker in the source, so match the
        # two halves rather than the joined sentence
        self.assertIn("trained skill scale of level-0 through", flat)
        self.assertIn("level-4", flat)

    def test_unskilled_is_outside_the_numbered_levels(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("unskilled is not level-0", flat)
        self.assertIn("not a numbered level at all", flat)

    def test_each_level_contributes_its_numeric_value(self) -> None:
        flat = _flat(RULEBOOK)
        for level, modifier in (("level-0", "+0"), ("level-1", "+1"),
                                ("level-2", "+2"), ("level-3", "+3"),
                                ("level-4", "+4")):
            with self.subTest(level=level):
                self.assertIn(f"{level}: {modifier}", flat)

    def test_unskilled_keeps_minus_one_and_blocking(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("-1 if the attempt is allowed, otherwise blocked", flat)
        self.assertIn("-1 unskilled modifier", flat)
        self.assertIn("applied exactly once", flat)
        self.assertIn("blocked before rolling", flat)
        self.assertIn("no dice are rolled", flat)

    def test_check_structure_names_attribute_plus_skill(self) -> None:
        """#25 later converted the die: 2d6, skill level, then attribute."""
        flat = _flat(RULEBOOK)
        self.assertIn(
            "2d6 + relevant skill level + relevant attribute modifier", flat
        )


class SkillListTests(unittest.TestCase):
    """The initial list is the SRD standard list with exactly two renames."""

    def test_the_list_is_exactly_the_srd_list_with_two_renames(self) -> None:
        names = _bullet_names(_skills_section())
        self.assertEqual(
            names, EXPECTED_SKILLS,
            "the initial NoöPunk skill list drifted from the SRD list + two renames",
        )

    def test_heal_is_renamed_medical(self) -> None:
        section = _skills_section()
        self.assertIn("**Medical**", section)
        self.assertIn("Heal → Medical", _text(RULEBOOK))

    def test_know_is_renamed_science(self) -> None:
        section = _skills_section()
        self.assertIn("**Science**", section)
        self.assertIn("Know → Science", _text(RULEBOOK))

    def test_retired_names_are_not_skills(self) -> None:
        """Heal/Know may appear only as the thing renamed away, never as a skill."""
        section = _skills_section()
        for retired in RETIRED_SKILL_NAMES:
            with self.subTest(retired=retired):
                self.assertNotRegex(
                    section, rf"^- \*\*{retired}\*\*", 
                    f"{retired} is still listed as a NoöPunk skill",
                )

    def test_no_other_skill_was_renamed_or_added(self) -> None:
        """Every SRD name except Heal/Know must survive verbatim."""
        names = set(_bullet_names(_skills_section()))
        for srd_name in ("Administer", "Connect", "Drive", "Exert", "Fix", "Lead",
                         "Notice", "Perform", "Program", "Punch", "Shoot", "Sneak",
                         "Stab", "Survive", "Talk", "Trade", "Work"):
            with self.subTest(skill=srd_name):
                self.assertIn(srd_name, names)

    def test_list_is_declared_a_first_pass(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("do not casually rename, split, merge, or add other skills", flat)
        self.assertIn("review the list bit by bit later", flat)


class SkillMeaningTests(unittest.TestCase):
    """Medical and Science inherit the CWN roles of Heal and Know."""

    def test_medical_keeps_the_heal_role(self) -> None:
        section = _flat(RULEBOOK)
        for duty in ("cure diseases", "stabilize the critically injured",
                     "treat psychological disorders", "diagnose illnesses"):
            with self.subTest(duty=duty):
                self.assertIn(duty, section)

    def test_science_keeps_the_know_role(self) -> None:
        section = _flat(RULEBOOK)
        for duty in ("academic or scientific fields", "recall relevant history",
                     "rare or esoteric topics"):
            with self.subTest(duty=duty):
                self.assertIn(duty, section)

    def test_medical_and_science_declare_their_inherited_role(self) -> None:
        text = _text(RULEBOOK)
        self.assertIn("Inherits the role of CWN **Heal**", text)
        self.assertIn("Inherits the role of CWN **Know**", text)

    def test_no_adjacent_medical_or_science_subsystem_was_invented(self) -> None:
        """The meanings must stay functional, not grow into subsystems.

        Scoped to the skills section: "surgery rules" and similar phrases already
        appear in #17's cyberspace exclusion list, which is a different subsystem.
        """
        section = _flat_section("### 5.3 Skills", "### 5.4")
        for forbidden in ("cyberware installation rule", "surgery rule",
                          "research subsystem", "psychotherapy subsystem",
                          "disease table"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, section)


class SpecializationDeferredTests(unittest.TestCase):
    """Specialties are documented as future design, with no mechanics invented."""

    def test_specialties_are_marked_future_design(self) -> None:
        flat = _flat(RULEBOOK)
        self.assertIn("specialties", flat)
        self.assertIn("future design, not a rule", flat)

    def test_examples_are_given_as_examples_only(self) -> None:
        text = _text(RULEBOOK)
        self.assertIn("Science (Biotech)", text)
        self.assertIn("Work (Lawyer)", text)

    def test_every_specialty_question_is_left_open(self) -> None:
        flat = _flat(RULEBOOK)
        for question in (
            "whether specialties are mandatory or optional",
            "whether they give modifiers",
            "whether they restrict what a broad skill can do",
            "whether work always requires a profession",
            "whether science always requires a field",
            "how specialties are bought or advanced",
            "whether specialties have their own levels",
            "whether other skills use specialties",
        ):
            with self.subTest(question=question):
                self.assertIn(question, flat)

    def test_work_profession_is_not_automatic_canon(self) -> None:
        """CWN's 'pick a profession' must not silently become the rule."""
        flat = _flat(RULEBOOK)
        self.assertIn("not automatically canonical", flat)
        self.assertIn("pick a particular profession", flat)
        self.assertIn("exact specialty/subtype mechanism is deferred", flat)


class NotImportedTests(unittest.TestCase):
    """The adjacent CWN subsystems must NOT have come along with the skill list."""

    def test_character_creation_acquisition_rules_are_absent(self) -> None:
        flat = _flat(RULEBOOK)
        for forbidden in ("the first time a skill is picked", "second time it is picked",
                          "no character can begin play with skills above level-1"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, flat)

    def test_advancement_and_level_gating_are_absent(self) -> None:
        flat = _flat(RULEBOOK)
        for forbidden in ("minimum experience level", "xp cost", "experience point"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, flat)

    def test_foci_and_background_picks_are_absent(self) -> None:
        flat = _flat(RULEBOOK)
        for forbidden in ("some foci also grant", "from their backgrounds as described",
                          "background skill pick"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, flat)

    def test_no_fixed_skill_to_attribute_table(self) -> None:
        """#22 explicitly refuses to bind skills to attributes."""
        flat = _flat(RULEBOOK)
        self.assertIn("skills are not bound to a fixed attribute", flat)
        self.assertIn("attribute", flat)
        self.assertIn("relevant to the action", flat)


class UnchangedSystemsTests(unittest.TestCase):
    """The task changes skills only."""

    def test_attributes_and_generation_are_untouched(self) -> None:
        flat = _flat(RULEBOOK)
        for code in ("fitness (fit)", "reflexes (ref)", "intelligence (int)",
                     "charisma (cha)", "cybernetics (cyb)", "psyche (psy)"):
            with self.subTest(attribute=code):
                self.assertIn(code, flat)
        self.assertIn("| 3 | -3 |", flat)
        self.assertIn("| 18 | +3 |", flat)

    def test_difficulty_ladder_is_the_cwn_ladder(self) -> None:
        """#22 pinned the old ladder; #25 superseded it for skill checks."""
        flat = _flat(RULEBOOK)
        for target in (6, 8, 10, 12):
            with self.subTest(difficulty=target):
                self.assertIn(f"| {target} |", flat)
        self.assertIn("14+", flat)
        self.assertIn("total = 2d6", flat)

    def test_the_cyberspace_framework_is_now_withdrawn(self) -> None:
        """#22 pinned #17's modifiers as live. #25 withdrew them, so this guard
        now pins the withdrawal instead of the framework."""
        flat = _flat(RULEBOOK)
        for modifier in ("bci", "compute", "connection", "infosec"):
            with self.subTest(modifier=modifier):
                self.assertIn(modifier, flat)
        self.assertIn("withdrawn from active canonical rules", flat)

    def test_core_json_gained_no_skill_schema(self) -> None:
        """The two pre-existing unskilled keys are #11's, not a #22 skill schema."""
        canon = json.loads(_text(CORE_JSON))
        pre_existing = {"unskilled_penalty", "trained_only_without_skill"}
        for key in canon:
            if key in pre_existing:
                continue
            with self.subTest(key=key):
                lowered = key.lower()
                for forbidden in ("skill", "medical", "science", "specialt"):
                    self.assertNotIn(
                        forbidden, lowered,
                        f"data/rules/core.json gained {key!r}; #22 ports nothing",
                    )
        # the pre-existing unskilled contract survives unchanged
        self.assertEqual(canon["unskilled_penalty"], -1)
        self.assertEqual(canon["trained_only_without_skill"], "blocked")

    def test_runtimes_gained_no_skill_implementation(self) -> None:
        for path in (GODOT_ADAPTER, CONCORDIA_MECHANICS):
            with self.subTest(path=path.name):
                flat = _flat(path)
                for forbidden in ("medical", "science", "skill_level", "specialty"):
                    self.assertNotIn(forbidden, flat,
                                     f"{path.name} gained a #22 skill mechanic")


class DocCoherenceTests(unittest.TestCase):
    """Every doc that described the old scale now describes the current one."""

    def test_no_doc_claims_four_skill_levels(self) -> None:
        for doc in (RULEBOOK, AGENTS, ROOT / "README.md",
                    ROOT / "docs" / "GODOT_ARCHITECTURE.md",
                    ROOT / "docs" / "CONCORDIA_ARCHITECTURE.md"):
            with self.subTest(doc=doc.name):
                self.assertNotIn("four canonical skill levels", _flat(doc))
                self.assertNotIn("four tabletop skill levels", _flat(doc))

    def test_no_doc_claims_level_zero_means_unskilled(self) -> None:
        for doc in (RULEBOOK, AGENTS):
            with self.subTest(doc=doc.name):
                flat = _flat(doc)
                self.assertNotIn("0 unskilled, 1 basic", flat)
                self.assertNotIn("skill level 0 it is either", flat)

    def test_agents_reserved_list_forbids_new_skills(self) -> None:
        flat = _flat(AGENTS)
        self.assertIn("additional skills", flat)
        self.assertIn("skill-to-attribute bindings", flat)
        self.assertIn("skill specialties", flat)

    def test_chassis_precedence_list_uses_the_current_scale(self) -> None:
        flat = _flat(POLICY)
        self.assertIn("level-0..4 trained skill scale", flat)
        self.assertNotIn("skill levels 0–3", _text(POLICY))


if __name__ == "__main__":
    unittest.main()
