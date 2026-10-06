"""Acceptance guard for issue #159: the canonical NoöPunk skill list.

Issue #159 supersedes the long-standing "the final Skill list is deferred" state:
it locks the universal Skill list — each Skill's governing attribute, whether it may be
attempted untrained, the field-specialization rule, and the psionic disciplines — in
``rulebook/9_SKILLS.md`` and ``data/rules/skills.json``.

In the style of ``test_issue60_setting_canon.py``, this module asserts structure, not
prose polish: that the artifact exists and is reachable, that every Skill carries the
attributes the issue requires, that the deferred list is genuinely closed, and that the
overlaps the issue names are resolved rather than left ambiguous.

Uses only the standard library: CI installs ``requirements.txt`` and nothing else.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = (ROOT / "rulebook" / "9_SKILLS.md").read_text(encoding="utf-8")
DATA = json.loads((ROOT / "data" / "rules" / "skills.json").read_text(encoding="utf-8"))
RULEBOOK = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
CORE = json.loads((ROOT / "data" / "rules" / "core.json").read_text(encoding="utf-8"))
AGENTS = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

BASE_STATS = ("FIT", "REF", "INT", "SOC", "CYB", "PSY")
SKILLS = {s["name"]: s for s in DATA["skills"]}

#: The exact Skill names the issue's design sections establish. A rename is drift.
EXPECTED_SKILLS = (
    "Administrate", "Athletics", "Connect", "Deceive", "Exotic Skill", "Fray",
    "Free Fall", "Guns", "Hardware", "Infosec", "Interface", "Kinesics", "Know",
    "Lead", "Medicine", "Melee", "Perceive", "Perform", "Pilot", "Program", "Provoke",
    "Research", "Sneak", "Survival", "Talk", "Trade", "Unarmed", "Work",
    "Telepathy", "Clairvoyance", "Psychokinesis", "Noöspace", "Precognition",
    "Psychic Defence",
)

#: The six psionic disciplines that replace the generic Psi placeholder.
PSI_SKILLS = ("Telepathy", "Clairvoyance", "Psychokinesis", "Noöspace",
              "Precognition", "Psychic Defence")


class ArtifactTests(unittest.TestCase):
    def test_the_chapter_exists_and_is_linked_from_the_rulebook(self) -> None:
        self.assertTrue((ROOT / "rulebook" / "9_SKILLS.md").exists(),
                        "rulebook/9_SKILLS.md is missing")
        self.assertIn("rulebook/9_SKILLS.md", RULEBOOK,
                      "the rulebook no longer points at the skill chapter")

    def test_the_machine_readable_artifact_parses_and_names_its_issue(self) -> None:
        self.assertEqual(DATA["source_issue"], 159)
        self.assertEqual(DATA["scale"], {"min": 1, "max": 10})

    def test_core_json_no_longer_says_the_skill_list_is_deferred(self) -> None:
        """The whole point of #159: the deferred state is closed and redirected."""
        self.assertEqual(CORE["skills"]["final_list"], "data/rules/skills.json")
        self.assertNotEqual(CORE["skills"]["final_list"], "deferred")

    def test_agents_md_no_longer_blanket_reserves_the_skill_list(self) -> None:
        self.assertIn("issue #159", AGENTS)
        self.assertNotIn("the universal Skill list remains explicitly deferred", AGENTS)


class SkillListTests(unittest.TestCase):
    def test_every_expected_skill_is_present_and_nothing_extra(self) -> None:
        self.assertEqual(set(SKILLS), set(EXPECTED_SKILLS),
                         "the universal skill list drifted from what #159 defines")

    def test_every_skill_has_a_governing_attribute(self) -> None:
        for name, skill in SKILLS.items():
            with self.subTest(skill=name):
                self.assertIn(skill["attribute"],
                              BASE_STATS + ("variable",),
                              f"{name} has an unknown or missing attribute")

    def test_every_skill_states_its_trained_status(self) -> None:
        """The issue requires the list to say which Skills are trained only."""
        for name, skill in SKILLS.items():
            with self.subTest(skill=name):
                self.assertIsInstance(skill["trained"], bool,
                                      f"{name} does not state trained vs untrained")

    def test_both_trained_and_untrained_categories_are_populated(self) -> None:
        trained = [n for n, s in SKILLS.items() if s["trained"]]
        untrained = [n for n, s in SKILLS.items() if not s["trained"]]
        self.assertTrue(trained, "no trained-only skills were recorded")
        self.assertTrue(untrained, "no untrained-attemptable skills were recorded")

    def test_untrained_skills_are_the_broad_everyday_ones(self) -> None:
        for name in ("Athletics", "Sneak", "Perceive", "Talk"):
            with self.subTest(skill=name):
                self.assertFalse(SKILLS[name]["trained"], f"{name} should be attemptable untrained")

    def test_hard_disciplines_require_training(self) -> None:
        for name in ("Pilot", "Medicine", "Infosec", "Program", "Guns"):
            with self.subTest(skill=name):
                self.assertTrue(SKILLS[name]["trained"], f"{name} must require training")

    def test_attribute_spread_covers_all_six_stats(self) -> None:
        """The issue's second design principle: make the six attributes mechanically important."""
        used = {s["attribute"] for s in DATA["skills"]}
        for stat in ("FIT", "REF", "INT", "SOC", "CYB", "PSY"):
            with self.subTest(stat=stat):
                self.assertIn(stat, used, f"no skill uses {stat}")


class SpecializationTests(unittest.TestCase):
    def test_the_field_skills_are_marked(self) -> None:
        fielded = {s["name"] for s in DATA["skills"] if s.get("field")}
        self.assertEqual(fielded, set(DATA["field_skills"]))

    def test_the_field_skill_set_is_the_issue_s(self) -> None:
        self.assertEqual(
            set(DATA["field_skills"]),
            {"Exotic Skill", "Hardware", "Know", "Medicine", "Pilot", "Perform", "Work"},
        )

    def test_related_field_modifier_is_minus_one(self) -> None:
        self.assertEqual(DATA["related_field_modifier"], -1)
        self.assertEqual(DATA["untrained_modifier"], -1)

    def test_the_chapter_states_the_related_unrelated_rule(self) -> None:
        self.assertIn("related", CHAPTER.lower())
        self.assertIn("unrelated", CHAPTER.lower())


class PsionicsTests(unittest.TestCase):
    def test_the_generic_psi_placeholder_is_replaced_by_disciplines(self) -> None:
        for name in PSI_SKILLS:
            with self.subTest(skill=name):
                self.assertIn(name, SKILLS, f"psi discipline missing: {name}")

    def test_psi_disciplines_require_a_capability_source(self) -> None:
        for name in PSI_SKILLS:
            with self.subTest(skill=name):
                self.assertIn("requires", SKILLS[name])

    def test_the_small_psi_set_is_compact(self) -> None:
        """The issue asks for the smallest useful set, not dozens of micro-skills."""
        psi = [n for n, s in SKILLS.items() if s.get("psi")]
        self.assertEqual(len(psi), 6, f"expected 6 psi disciplines, found {sorted(psi)}")

    def test_psychotronics_is_not_a_psionic_skill(self) -> None:
        self.assertNotIn("Psychotronics", SKILLS)
        self.assertIn("Psychotronics", SKILLS["Hardware"].get("fields_example", []))


class OverlapResolutionTests(unittest.TestCase):
    """The issue lists the overlaps it wants resolved, not left ambiguous."""

    def test_the_four_overlap_clusters_are_resolved(self) -> None:
        for key in ("social_cluster", "technical_cluster", "knowledge_cluster",
                    "work_vs_dedicated"):
            with self.subTest(cluster=key):
                self.assertIn(key, DATA["overlap_resolutions"])

    def test_first_aid_is_folded_into_medicine(self) -> None:
        self.assertNotIn("First Aid", SKILLS)
        self.assertIn("Emergency Care", SKILLS["Medicine"].get("fields_example", []))

    def test_law_is_a_know_field(self) -> None:
        self.assertNotIn("Law", SKILLS)
        self.assertIn("Law", SKILLS["Know"].get("fields_example", []))

    def test_tactics_is_not_a_separate_skill(self) -> None:
        self.assertNotIn("Tactics", SKILLS)


class AcademyAlignmentTests(unittest.TestCase):
    """#159 must review #158 (UNSA Academy) for the Skills it needs."""

    def test_the_academy_alignment_exists_and_names_158(self) -> None:
        self.assertIn("unsa_academy_alignment", DATA)
        self.assertEqual(DATA["unsa_academy_alignment"]["source_issue"], 158)

    def test_the_academy_needs_map_onto_real_skills(self) -> None:
        """Every mapped target must name a real universal skill or a Know/Medicine field."""
        valid = set(SKILLS)
        for need, target in DATA["unsa_academy_alignment"]["map"].items():
            with self.subTest(need=need):
                head = target.split(" (")[0].split(" / ")[0].split(" + ")[0].strip()
                self.assertIn(head, valid, f"{need} maps to an unknown skill: {target}")

    def test_no_skill_per_academy_need(self) -> None:
        """The issue's warning: do not create several skills that solve one scene."""
        for banned in ("Tactics", "Police Procedure", "Forensics", "Interrogation",
                       "Surveillance", "Investigation", "Intelligence Analysis",
                       "Counterintelligence", "First Aid"):
            with self.subTest(skill=banned):
                self.assertNotIn(banned, SKILLS, f"{banned} should be a Know/Medicine field, not a skill")


class DeferralTests(unittest.TestCase):
    def test_mechanics_stay_deferred(self) -> None:
        """#159 locks the skill list, not the mechanics that use it."""
        for item in ("combat resolution, damage, defence procedure",
                     "hacking / cyberspace procedures",
                     "psionic powers, sleights, their effects and resolution"):
            with self.subTest(item=item):
                self.assertIn(item, DATA["deferred"])

    def test_the_chapter_defers_rather_than_invents(self) -> None:
        self.assertIn("does not define", CHAPTER)
        for phrase in ("combat resolution", "psionic powers"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, CHAPTER)


if __name__ == "__main__":
    unittest.main()
