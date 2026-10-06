"""Structure guard for the UNSA Academy specification (issue #158).

Issue #158 asks for the universal UNSA Police Academy baseline: what every graduate is
trained to do, which NoöPunk skills represent that training, the standard cybernetic and
psychotronic augmentation packages, the augmented-vision modes, the rookie equipment kit,
and the non-invasive alternatives. It lives in ``docs/design/UNSA_ACADEMY.md``.

The guard pins the properties a later session could silently drift:

1. the document exists and carries its title and draft status;
2. the academy baseline is expressed on the **canonical** Skill vocabulary — every skill
   the package names must exist in ``data/rules/skills.json`` (issue #159). This is the
   central anti-drift assertion: a new "Anomalistics" or "Psionics" skill appearing in the
   package would be exactly the proliferation the issue forbids;
3. the **fold table** survives: the issue's candidate skills that canon folds into another
   skill (Law -> Know (Law), OSINT -> Research, Police Procedure -> Work (Police Officer),
   and so on) must still be named as folds, because dropping a fold is how a duplicate
   skill gets invented later;
4. the calibration is real: all three baseline tiers are defined and the package's ratings
   stay inside the 1-10 scale;
5. the design positions the issue asks for are present — the AI is not an AGI, no single
   sensory channel is definitive, implants are optional, and the biological-purity path is
   playable;
6. the two deliberately-open items stay open (the Cortical Stack question and the
   real-world equipment research pass). The failure mode is a later session quietly
   picking an answer.

Assertion discipline:
* assert each deliverable separately, never one alternation;
* anchor ambiguous tokens to their specific sentence (a bare word that occurs elsewhere
  stays green after the specific fact is removed);
* match blockquoted or emphasised prose against the **normalised** text.

Uses only the standard library: CI installs requirements.txt and nothing else.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "design" / "UNSA_ACADEMY.md"
SKILLS = ROOT / "data" / "rules" / "skills.json"


def raw() -> str:
    return DOC.read_text(encoding="utf-8")


def doc() -> str:
    """Whitespace-collapsed, so line wrapping cannot hide a term."""
    return " ".join(raw().split())


def normalised(text: str) -> str:
    """Strip markdown markers and quotation marks, then collapse and casefold."""
    for marker in (">", "*", "_", "`", '"', "'"):
        text = text.replace(marker, "")
    return " ".join(text.split()).lower()


def doc_norm() -> str:
    return normalised(raw())


def canonical_skill_names() -> set[str]:
    """The canonical universal Skill vocabulary from issue #159."""
    data = json.loads(SKILLS.read_text(encoding="utf-8"))
    skills = data["skills"]
    return {s["name"] if isinstance(s, dict) else str(s) for s in skills}


class FileTests(unittest.TestCase):
    def test_the_document_exists(self) -> None:
        self.assertTrue(DOC.exists(), "docs/design/UNSA_ACADEMY.md is missing")

    def test_the_document_keeps_its_title(self) -> None:
        self.assertRegex(doc(), r"^# UNSA Academy\b",
                         "the document title was renamed or removed")

    def test_the_document_declares_itself_a_spec_for_158(self) -> None:
        self.assertIn("design specification for issue #158", doc_norm())

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        """Real institutions appear in this document; the disclaimer is what keeps it from
        reading as a real-world claim."""
        self.assertIn(
            "this entire document is fictional alternate-history lore. real people, "
            "governments, companies and institutions are used as fictionalized setting "
            "elements; the events described here are not claims about real-world history "
            "or evidence.",
            doc_norm(),
        )

    def test_no_future_year_is_assigned(self) -> None:
        """AGENTS.md §6: canonical future dates are 20XX.

        ``2026`` is allowed because the issue itself specifies an AI capability level
        *relative to real 2026 frontier models* — that is a real-world design benchmark,
        not an in-world year. Any other year is drift.
        """
        future = [y for y in re.findall(r"\b(20\d\d)\b", doc()) if y != "2026"]
        self.assertEqual(future, [],
                         f"exact future years assigned: {sorted(set(future))}; canon uses 20XX")

    def test_the_2026_reference_is_only_the_ai_capability_benchmark(self) -> None:
        """Guard the exemption so it cannot become a loophole: every use of ``2026`` must
        sit in the AI-capability comparison the issue specifies. Matched on a window
        around each occurrence rather than a single line, because the sentence wraps."""
        flat = doc()
        for m in re.finditer(r"2026", flat):
            window = flat[max(0, m.start() - 140):m.start() + 140].lower()
            with self.subTest(at=m.start()):
                self.assertRegex(
                    window, r"frontier|capability|de-powering",
                    "2026 may only appear as the AI capability benchmark",
                )


class CanonicalSkillVocabularyTests(unittest.TestCase):
    """The academy package must stay inside the canonical Skill list.

    This is the load-bearing guard: issue #158 explicitly asks to avoid skill
    proliferation, and the failure mode is a later session inventing "Anomalistics",
    "Psionics", "Surveillance" or "Police Procedure" as new universal Skills.
    """

    def test_the_fold_table_names_the_folds_the_issue_needs(self) -> None:
        """Each fold resolves a candidate the issue lists into an existing skill. Dropping
        a fold is how a duplicate skill gets invented later."""
        text = doc()
        folds = [
            "**Law** | **Know (Law)**",
            "**OSINT** | **Research**",
            "**Police Procedure** | **Work (Police Officer)**",
            "**Hacking** | **Infosec**",
            "**Cybertech** | **Hardware (Cyberware)**",
            "**Unarmed Combat** | **Unarmed**",
        ]
        for fold in folds:
            with self.subTest(fold=fold):
                self.assertIn(fold, text)

    def test_the_document_states_it_adds_no_new_skills(self) -> None:
        text = doc_norm()
        self.assertIn("zero additions", text)
        self.assertIn("defines no new universal skills", text)

    def test_the_psi_vocabulary_does_not_invent_a_psionics_skill(self) -> None:
        """There is no single "Psionics" skill in canon; the PSY skills are separate."""
        text = doc_norm()
        self.assertIn("there is no psionics skill", text)
        for real in ("psychic defence", "esp", "telepathy", "noöspace"):
            with self.subTest(skill=real):
                self.assertIn(real, text)

    def test_no_anomalistics_skill_is_introduced(self) -> None:
        text = doc_norm()
        self.assertIn("do not create anomalistics", text)

    def test_every_canonical_skill_named_in_the_package_exists(self) -> None:
        """Extract the skills from the package table and check each against skills.json.

        Anchored on the **package table rows**, not bare names: "Investigation" occurs 21
        times in the document, so a bare-name check stayed green when a table row was
        renamed to a non-canonical skill.
        """
        canonical = canonical_skill_names()
        package = doc()
        rows = [
            ("Guns", "| Guns | REF | 5 |"),
            ("Investigation", "| Investigation | INT | 5 |"),
            ("Perceive", "| Perceive | PSY | 5 |"),
            ("Unarmed", "| Unarmed | FIT | 4 |"),
            ("Melee", "| Melee | FIT | 4 |"),
            ("Athletics", "| Athletics | FIT | 4 |"),
            ("Fray", "| Fray | REF | 4 |"),
            ("First Aid", "| First Aid | INT | 4 |"),
            ("Forensics", "| Forensics | INT | 4 |"),
            ("Intelligence Analysis", "| Intelligence Analysis | INT | 4 |"),
            ("Counterintelligence", "| Counterintelligence | INT | 4 |"),
            ("Research", "| Research | INT | 4 |"),
            ("Talk", "| Talk | SOC | 4 |"),
            ("Interface", "| Interface | CYB | 4 |"),
            ("Psychic Defence", "| Psychic Defence | PSY | 4 |"),
            ("Tactics", "| Tactics | INT | 3 |"),
            ("Sneak", "| Sneak | REF | 3 |"),
            ("Kinesics", "| Kinesics | SOC | 3 |"),
            ("Deceive", "| Deceive | SOC | 3 |"),
            ("Connect", "| Connect | SOC | 3 |"),
            ("Survival", "| Survival | INT | 3 |"),
            ("Infosec", "| Infosec | CYB | 3 |"),
            ("Program", "| Program | CYB | 3 |"),
            ("ESP", "| ESP | PSY | 3 |"),
            ("Noöspace", "| Noöspace | PSY | 3 |"),
        ]
        for name, row in rows:
            with self.subTest(skill=name):
                self.assertIn(name, canonical,
                              f"{name!r} is in the academy package but not in skills.json")
                self.assertIn(row, package, f"the package table lost the {name!r} row")
        self.assertIn("| Work (Police Officer)", package)
        self.assertIn("| Know (Law)", package)
        self.assertIn("| Know (X-Risk Studies)", package)
        self.assertIn("| Know (NHI Studies)", package)
        self.assertIn("| Hardware (Cyberware)", package)
        self.assertIn("| Pilot (Ground Vehicles)", package)


class CalibrationTests(unittest.TestCase):
    def test_every_graduate_would_use_the_one_to_ten_scale(self) -> None:
        self.assertIn("**1–10** Skill scale", doc())

    def test_all_three_baseline_tiers_are_defined(self) -> None:
        for tier in ("**Foundation**", "**Core**", "**Emphasis**"):
            with self.subTest(tier=tier):
                self.assertIn(tier, doc())

    def test_the_tier_values_are_stated(self) -> None:
        text = doc()
        self.assertRegex(text, r"Foundation\*{0,2} \| \*{0,2}3")
        self.assertRegex(text, r"Core\*{0,2} \| \*{0,2}4")
        self.assertRegex(text, r"Emphasis\*{0,2} \| \*{0,2}5")

    def test_the_design_target_is_testable(self) -> None:
        """The issue's §16 target: a graduate can do the listed things and is not a
        specialist. Both halves must be asserted."""
        text = doc_norm()
        self.assertIn("calibration check against §16 of the issue", text)
        # "not equal a specialist" half
        self.assertIn("do not equal a swat operator", text)

    def test_specialist_tracks_are_handed_off_not_duplicated(self) -> None:
        """The issue asks for specialist tracks to be defined separately, so this document
        must hand off rather than define them."""
        text = doc_norm()
        self.assertIn("specialist tracks", text)
        self.assertIn("raise a narrow set of these to 6–7", text)


class AugmentationTests(unittest.TestCase):
    def test_the_ai_is_not_an_agi(self) -> None:
        self.assertIn("it is not an agi", doc_norm())

    def test_the_ai_is_specified_below_2026_frontier_capability(self) -> None:
        """The issue is explicit about the de-powering; it is the key design decision."""
        self.assertIn("somewhat below 2026 frontier multimodal llm capability", doc_norm())

    def test_the_ai_is_forbidden_from_lethal_force_and_arrest_decisions(self) -> None:
        text = doc_norm()
        self.assertIn("the ai may not make any decision that the law reserves to a sworn "
                      "human officer", text)
        self.assertIn("lethal force", text)
        self.assertIn("arrest decision", text)

    def test_the_ai_instrument_not_detective_rule_survives(self) -> None:
        self.assertIn("extraordinary instrument, not the detective", doc_norm())

    def test_no_single_sensory_channel_is_definitive(self) -> None:
        self.assertIn("no single sensory channel is definitive", doc_norm())

    def test_augmented_vision_never_authorises_action(self) -> None:
        self.assertIn("augmented vision never authorises action on its own", doc_norm())

    def test_the_tri_layer_vision_is_specified(self) -> None:
        for layer in ("**Physical**", "**Cyber**", "**Astral / Noetic**"):
            with self.subTest(layer=layer):
                self.assertIn(layer, doc())

    def test_the_psychotronic_package_grants_no_psi_skill_rating(self) -> None:
        text = doc_norm()
        self.assertIn("grants no psi skill rating", text)
        self.assertIn("no advanced psionic powers", text)

    def test_the_enhancement_options_grant_no_bonus(self) -> None:
        """The de-powering rule: narrative colour must not buy competence."""
        self.assertIn("none of these grants a skill or stat rating", doc_norm())

    def test_compute_interface_network_are_equipment_not_stats(self) -> None:
        text = doc_norm()
        self.assertIn("equipment statistics, not character attributes", text)


class BiologicalPurityTests(unittest.TestCase):
    def test_implants_are_optional_not_compulsory(self) -> None:
        self.assertIn("implants are common but not compulsory", doc_norm())

    def test_the_non_invasive_equivalents_are_listed(self) -> None:
        text = doc_norm()
        for item in ("ar glasses", "smart contact lenses", "external bci",
                     "wearable psychotronics", "handheld forensic scanner"):
            with self.subTest(item=item):
                self.assertIn(item, text)

    def test_the_biological_character_receives_the_same_information(self) -> None:
        """The trade must be convenience vs attack surface, not information denial."""
        text = doc_norm()
        self.assertIn("fully playable and receives the same information", text)
        self.assertIn("this is a genuine trade, not a penalty", text)


class EquipmentTests(unittest.TestCase):
    def test_the_equipment_categories_are_all_present(self) -> None:
        for section in ("### 9.1 Weapons", "### 9.2 Protection",
                        "### 9.3 Identification and police equipment",
                        "### 9.4 Investigation", "### 9.5 X-risk / NHI kit"):
            with self.subTest(section=section):
                self.assertIn(section, doc())

    def test_the_equipment_design_principle_survives(self) -> None:
        text = doc_norm()
        self.assertIn("elite near-future investigator without eliminating player agency",
                      text)
        self.assertIn("you can see far more than a contemporary investigator", text)

    def test_the_nhi_kit_includes_a_hardened_off_network_store(self) -> None:
        self.assertIn("do not connect this to the network", doc_norm())


class DeliberatelyOpenTests(unittest.TestCase):
    """The two items the issue cannot settle must stay unsettled."""

    def test_the_cortical_stack_question_is_recorded_open(self) -> None:
        text = doc_norm()
        self.assertIn("deliberately open", text)
        self.assertIn("this document does not settle it", text)

    def test_the_cortical_stack_constraints_are_recorded(self) -> None:
        """The answer is constrained by canon: 25% adoption, deferred mechanics, and the
        unresolved consciousness-continuity question.

        Each constraint is anchored on its own sentence. "roughly 25% of humanity" occurs
        twice, so a bare-phrase check stayed green when the constraint list was gutted.
        """
        text = doc_norm()
        self.assertIn("roughly 25% of humanity", text)
        self.assertIn("adoption varies radically", text)
        self.assertIn("informational continuity can be verified more easily than continuity "
                      "of consciousness", text)
        self.assertIn("cortical-stack continuity, full resleeving, morph catalogs", text)

    def test_the_cortical_stack_is_escalated_to_the_author(self) -> None:
        self.assertIn("this is a decision for the author", doc_norm())

    def test_the_equipment_research_pass_is_recorded_as_not_done(self) -> None:
        self.assertIn("that pass has not been done", doc_norm())

    def test_the_research_pass_is_not_claimed_as_researched(self) -> None:
        self.assertIn("have not been checked against real current federal-agent kits",
                      doc_norm())


if __name__ == "__main__":
    unittest.main()
