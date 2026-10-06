"""Structure guard for the investigation-fantasy specification (issue #162).

Issue #162 captures the default NoöPunk player fantasy and investigation loop: the
distributed investigative cell (field investigator, partner, controller, embedded AI), the
four layers of a crime scene, the NHI detection-and-classification protocol, the
lethal-force doctrine, and the Orion-associated Men in Black. It lives in
``docs/design/INVESTIGATION_FANTASY.md``.

The guard pins the properties a later session could silently drift:

1. the document exists and carries its title and draft status;
2. all **four cell roles** exist with their defining functions — this is the architecture
   the whole loop rests on;
3. the **four layers** of the crime scene exist and map onto canonical Skills only;
4. the **anti-trivialisation rules** survive: NHI detection is never an instant answer, no
   single channel is definitive, and the AI is not an AGI. These are the rules that keep
   the genre from collapsing, and a later "helpful" simplification is the failure mode;
5. the **lethal-force doctrine** survives intact — NHI status is not grounds for lethal
   force, and the question is harm, not humanity;
6. the **Orion Men in Black** are antagonists and are explicitly distinguished from the
   UNSA nickname (a conflation this guard blocks);
7. the **open items stay open**: the NCAP's numbers and the Cortical Stack coupling are
   escalated, not settled.

Assertion discipline:
* assert each property separately, never one alternation;
* anchor ambiguous tokens to their specific sentence, because a bare word that occurs
  elsewhere stays green after the specific fact is removed;
* match blockquoted or emphasised prose against the **normalised** text.

Uses only the standard library: CI installs requirements.txt and nothing else.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "design" / "INVESTIGATION_FANTASY.md"
SKILLS = ROOT / "data" / "rules" / "skills.json"


def raw() -> str:
    return DOC.read_text(encoding="utf-8")


def doc() -> str:
    return " ".join(raw().split())


def normalised(text: str) -> str:
    for marker in (">", "*", "_", "`", '"', "'"):
        text = text.replace(marker, "")
    return " ".join(text.split()).lower()


def doc_norm() -> str:
    return normalised(raw())


def canonical_skill_names() -> set[str]:
    data = json.loads(SKILLS.read_text(encoding="utf-8"))
    return {s["name"] if isinstance(s, dict) else str(s) for s in data["skills"]}


class FileTests(unittest.TestCase):
    def test_the_document_exists(self) -> None:
        self.assertTrue(DOC.exists(), "docs/design/INVESTIGATION_FANTASY.md is missing")

    def test_the_document_keeps_its_title(self) -> None:
        self.assertRegex(doc(), r"^# Investigation fantasy\b")

    def test_the_document_declares_itself_a_spec_for_162(self) -> None:
        self.assertIn("design specification for issue #162", doc_norm())

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        self.assertIn(
            "this entire document is fictional alternate-history lore. real people, "
            "governments, companies and institutions are used as fictionalized setting "
            "elements; the events described here are not claims about real-world history "
            "or evidence.",
            doc_norm(),
        )

    def test_the_reference_works_are_declared_prompts_not_imports(self) -> None:
        """The issue names Blade Runner, The X-Files, Ubik and others. Using them as design
        prompts is fine; importing their material is not."""
        text = doc_norm()
        self.assertIn("nothing is imported from them", text)
        self.assertIn("no characters, factions, terminology, mechanics or text", text)

    def test_no_future_year_is_assigned(self) -> None:
        """AGENTS.md §6: canonical future dates are 20XX.

        Two legitimate exceptions, both real-world design references rather than in-world
        years: ``2026`` is the AI-capability benchmark the issue specifies, and ``2077`` is
        part of the title *Cyberpunk 2077*. Any other year is drift, and this test also
        asserts the exceptions are not used anywhere else.
        """
        years = re.findall(r"\b(20\d\d)\b", doc())
        unexpected = [y for y in years if y not in ("2026", "2077")]
        self.assertEqual(unexpected, [],
                         f"exact future years assigned: {sorted(set(unexpected))}; canon uses 20XX")
        # The 2077 occurrences must be the game title.
        self.assertEqual(doc().count("Cyberpunk 2077"), years.count("2077"),
                         "2077 may only appear as part of the title 'Cyberpunk 2077'")


class PitchTests(unittest.TestCase):
    def test_the_core_role_is_named(self) -> None:
        """Anchored on the refusal sentence, not the bare phrase: "post-Singularity
        anomalous-threat investigator" also occurs in the pitch, so a bare-phrase check
        stayed green when the core-role definition itself was replaced. Matched on the
        normalised text because the sentence carries emphasis markers."""
        self.assertIn("it is a post-singularity anomalous-threat investigator", doc_norm())

    def test_the_document_refuses_the_generic_cyberpunk_adventurer(self) -> None:
        self.assertIn("not a generic cyberpunk adventurer", doc_norm())

    def test_the_compact_pitch_is_present(self) -> None:
        text = doc_norm()
        self.assertIn("cyberpunk paranormal-investigation rpg", text)


class CellArchitectureTests(unittest.TestCase):
    """The four roles of the distributed investigative cell."""

    def test_all_four_roles_have_their_own_sections(self) -> None:
        for section in ("### 3.1 Player character", "### 3.2 Partner",
                        "### 3.3 Controller", "### 3.4 Embedded AI agent"):
            with self.subTest(section=section):
                self.assertIn(section, doc())

    def test_the_player_is_the_protagonist(self) -> None:
        """Every other role exists to inform the decision, never to replace it."""
        self.assertIn("the player is always the one who decides", doc_norm())

    def test_the_partner_is_a_reality_anchor(self) -> None:
        """The defining capability: the partner corrects a compromised perception."""
        text = doc_norm()
        self.assertIn("sanity/reality anchor", text)
        self.assertIn("there is no doorway", text)

    def test_the_partner_is_not_an_oracle(self) -> None:
        """A partner who is always right is the AI problem in a human costume."""
        self.assertIn("the partner must not be an oracle", doc_norm())

    def test_the_controller_can_be_compromised(self) -> None:
        """The controller is a possible source of false confirmation, which is what makes
        the Orion antagonism mechanically meaningful."""
        text = doc_norm()
        self.assertIn("also a source of uncertainty", text)
        self.assertIn("a compromised controller can supply a false confirmation", text)

    def test_the_controller_supervises_several_agents(self) -> None:
        self.assertIn("one controller supervises several agents", doc_norm())

    def test_the_ai_is_not_an_agi_and_is_not_the_detective(self) -> None:
        text = doc_norm()
        self.assertIn("it must not be an agi", text)
        self.assertIn("extraordinary instrument, not the detective", text)

    def test_the_ai_cannot_conclude_hostility(self) -> None:
        """The issue's own worked example: "consistent with" is allowed, "shoot them" is
        not."""
        self.assertIn("therefore this person is an orion operative", doc_norm())
        self.assertIn("it must not conclude", doc_norm())


class FourLayerTests(unittest.TestCase):
    def test_all_four_layers_are_named(self) -> None:
        for layer in ("**Physical**", "**Cyber**", "**Social**", "**Psychic / Noöspace**"):
            with self.subTest(layer=layer):
                self.assertIn(layer, doc())

    def test_the_scene_exists_across_all_four_simultaneously(self) -> None:
        self.assertIn("the same crime scene exists simultaneously across all four layers",
                      doc_norm())

    def test_the_layers_map_to_canonical_systems_not_a_new_ontology(self) -> None:
        text = doc_norm()
        self.assertIn("adds no fifth layer and no new ontology", text)
        self.assertIn("rulebook.md §36", text)

    def test_the_layer_skill_map_uses_canonical_skills(self) -> None:
        """Every skill the layer table names must exist in skills.json.

        Anchored on the **table rows** in §2, not on bare names: a check that only looked
        for "Infosec" and "Interface" anywhere in the document stayed green when a table
        row was renamed to a non-canonical skill. The rows are the map.
        """
        canonical = canonical_skill_names()
        table = doc()
        rows = [
            "| **Physical** |",
            "| **Cyber** |",
            "| **Social** |",
            "| **Psychic / Noöspace** |",
        ]
        for row in rows:
            with self.subTest(row=row):
                self.assertIn(row, table)
        # The four rows together must name exactly the canonical skills they use.
        for skill in ("Perceive", "Investigation", "Forensics", "First Aid", "Medicine",
                      "Infosec", "Interface", "Program", "Hardware", "Research", "Talk",
                      "Kinesics", "Connect", "Deceive", "Provoke", "Counterintelligence",
                      "Intelligence Analysis", "Psychic Defence", "ESP", "Telepathy",
                      "Noöspace"):
            with self.subTest(skill=skill):
                self.assertIn(f"**{skill}**", table,
                              f"the layer map no longer names {skill!r}")
                self.assertIn(skill, canonical,
                              f"{skill!r} is named in the layer map but not in skills.json")
        for invented in ("Netrunning", "Anomalistics", "Surveillance", "Psionics"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, table,
                                 f"{invented!r} is not a canonical skill and must not appear")


class AntiTrivialisationTests(unittest.TestCase):
    """The rules that keep advanced technology from solving the game.

    Highest-value part of the guard: the failure mode is a later session adding a sensor
    that identifies the answer, which would collapse the entire genre.
    """

    def test_nhi_detection_is_not_an_instant_answer_button(self) -> None:
        self.assertIn("nhi detection is not an instant-answer button", doc_norm())

    def test_the_question_is_never_simply_is_this_nhi(self) -> None:
        text = doc_norm()
        self.assertIn("the question is never is this nhi", text)
        self.assertIn("what kind of agent is this, what is controlling it, and is it "
                      "actually hostile", text)

    def test_the_false_positive_categories_are_listed(self) -> None:
        """The list is what makes a positive reading falsifiable."""
        text = doc_norm()
        for cause in ("human psychics", "transhumans", "uploaded humans", "hybrids",
                      "possession", "remote control", "deliberate sensor spoofing",
                      "orion operations", "damaged or compromised sensors"):
            with self.subTest(cause=cause):
                self.assertIn(cause, text)

    def test_a_sensor_result_is_evidence_not_a_verdict(self) -> None:
        text = doc_norm()
        self.assertIn("evidence item with a confidence value, not a verdict", text)
        self.assertIn("name at least one alternative explanation", text)

    def test_the_design_principle_to_preserve_is_stated(self) -> None:
        text = doc_norm()
        self.assertIn("deepen investigation rather than trivialise it", text)
        self.assertIn("which version of reality is actually true", text)
        self.assertIn("triangulate reality before acting", text)

    def test_the_principle_is_an_acceptance_test(self) -> None:
        """The two sentences must be framed as a test for future subsystems, not a motto."""
        self.assertIn("acceptance test for every future subsystem", doc_norm())


class ProtocolTests(unittest.TestCase):
    def test_the_ncap_is_proposed_with_a_formal_name(self) -> None:
        text = doc_norm()
        self.assertIn("nonhuman cognition assessment protocol", text)
        self.assertIn("ontological interview", text)

    def test_the_nickname_is_not_the_canonical_name(self) -> None:
        """The setting may use the nickname in dialogue; the rulebook's own vocabulary
        must not be the proprietary one."""
        self.assertIn("not the canonical name", doc_norm())

    def test_no_single_channel_is_definitive(self) -> None:
        self.assertIn("no single channel is definitive", doc_norm())

    def test_the_investigative_sequence_is_stated(self) -> None:
        self.assertIn(
            "detection → suspicion → examination → classification → authorisation",
            doc_norm(),
        )

    def test_authorisation_is_a_human_legal_decision(self) -> None:
        """A test result must never authorise anything."""
        self.assertIn("authorisation step is a human legal decision, never a test result",
                      doc_norm())

    def test_the_protocol_must_be_able_to_be_wrong(self) -> None:
        self.assertIn("false positives and contested legal status are desirable", doc_norm())
        self.assertIn("must be able to be wrong", doc_norm())


class LethalForceTests(unittest.TestCase):
    """The setting's most important normative rule."""

    def test_nhi_status_alone_is_not_grounds_for_lethal_force(self) -> None:
        self.assertIn("nhi status alone is not grounds for lethal force", doc_norm())

    def test_the_question_is_harm_not_humanity(self) -> None:
        text = doc_norm()
        self.assertIn("is this entity committing or imminently threatening serious harm",
                      text)
        self.assertIn("not: is this entity human", text)

    def test_the_triangulation_doctrine_is_stated(self) -> None:
        text = doc_norm()
        self.assertIn("never authorise lethal force solely from augmented perception", text)
        self.assertIn("two or more channels", text)

    def test_the_confirmation_channels_are_listed(self) -> None:
        text = doc_norm()
        for channel in ("physical evidence", "partner observation", "cyber evidence",
                        "psychic evidence", "controller intelligence",
                        "formal cognition testing"):
            with self.subTest(channel=channel):
                self.assertIn(channel, text)

    def test_the_entity_categories_are_listed(self) -> None:
        """The doctrine only means something if the non-human population is diverse."""
        text = doc_norm()
        for kind in ("benign nhi", "neutral nhi", "artificial persons", "awakened humans",
                     "entities with incomprehensible motives", "hostile nhi"):
            with self.subTest(kind=kind):
                self.assertIn(kind, text)

    def test_the_polarization_link_is_made(self) -> None:
        """The doctrine ties to the Law-of-One Polarization axis (§9.3), which is what
        stops it being a free-floating ethical gesture."""
        text = doc_norm()
        self.assertIn("polarization", text)
        self.assertIn("service-to-self", text)
        self.assertIn("sustained meaningful action", text)


class AttackTests(unittest.TestCase):
    """The player is a target; the cell architecture exists to survive it."""

    def test_the_attack_forms_are_listed(self) -> None:
        text = doc_norm()
        for attack in ("psychic attack", "psychotronic attack", "hallucination",
                       "memory manipulation", "sensor spoofing", "false ar overlay",
                       "implanted thoughts", "dream intrusion",
                       "communications spoofing"):
            with self.subTest(attack=attack):
                self.assertIn(attack, text)

    def test_the_key_theme_survives(self) -> None:
        text = doc_norm()
        self.assertIn("advanced technology does not remove uncertainty", text)
        self.assertIn("more dimensions in which uncertainty can attack you", text)

    def test_the_hud_warning_example_is_present(self) -> None:
        text = doc_norm()
        self.assertIn("psi intrusion detected", text)
        self.assertIn("recommendation: avoid irreversible decisions", text)

    def test_intrusion_is_a_contested_check_against_psychic_defence(self) -> None:
        text = doc_norm()
        self.assertIn("contested check", text)
        self.assertIn("psychic defence", text)

    def test_a_compromised_feed_degrades_quality_not_a_number(self) -> None:
        """The design rule that keeps triangulation meaningful."""
        self.assertIn("degrades information quality, it does not simply subtract a number",
                      doc_norm())


class OrionTests(unittest.TestCase):
    def test_the_player_organisation_is_not_the_men_in_black(self) -> None:
        self.assertIn("do not make the player organization simply the men in black",
                      doc_norm())

    def test_the_men_in_black_are_orion_associated_antagonists(self) -> None:
        text = doc_norm()
        self.assertIn("associated with the orion group", text)
        self.assertIn("recurring antagonists", text)

    def test_the_antagonist_capabilities_are_listed(self) -> None:
        text = doc_norm()
        for cap in ("extremely convincing credentials", "memory interference",
                    "psychic pressure", "sensor spoofing", "command-channel manipulation",
                    "fabrication of evidence"):
            with self.subTest(cap=cap):
                self.assertIn(cap, text)

    def test_the_provoke_into_attacking_peaceful_nhi_hook_survives(self) -> None:
        self.assertIn("attempts to provoke humans into attacking peaceful nhi", doc_norm())

    def test_the_paranoia_statement_survives(self) -> None:
        self.assertIn("even valid-looking institutional orders may be compromised",
                      doc_norm())

    def test_the_unsa_nickname_is_distinguished_from_the_antagonists(self) -> None:
        """§38 says UNSA personnel are nicknamed "Men in Black" and that "MJ-12" is not an
        acceptable nickname. Conflating that nickname with the Orion antagonists is a real
        misreading, and this guard blocks it."""
        text = doc_norm()
        self.assertIn("different in-world thing from the unsa nickname", text)
        self.assertIn("mj-12", text)


class CampaignTests(unittest.TestCase):
    def test_the_default_chain_is_the_canonical_one(self) -> None:
        text = doc_norm()
        self.assertIn("european-level agency", text)
        self.assertIn("helsinki field office", text)
        self.assertIn("pc + partner + controller + embedded forensic ai", text)

    def test_the_document_says_the_chain_is_already_canon(self) -> None:
        """It builds on §38 and FACTIONS.md; it must not present the chain as new."""
        self.assertIn("this is already canon", doc_norm())

    def test_the_world_stays_blurry_outside_europe(self) -> None:
        self.assertIn("do not overbuild the world", doc_norm())


class OpenItemsTests(unittest.TestCase):
    """The two items that must stay open."""

    def test_the_open_items_are_enumerated(self) -> None:
        self.assertIn("does not settle", doc_norm())

    def test_the_cortical_stack_coupling_is_escalated(self) -> None:
        """This document's ethics depend on the stakes of death, which UNSA_ACADEMY §10
        records as open. The coupling must be stated."""
        text = doc_norm()
        self.assertIn("cortical stack question", text)
        self.assertIn("both escalate that decision to the author", text)

    def test_the_ncap_mechanics_are_left_to_a_rules_pass(self) -> None:
        text = doc_norm()
        self.assertIn("exact mechanical formulation of the ncap", text)
        self.assertIn("that is a rules pass", text)

    def test_the_document_promotes_nothing_by_itself(self) -> None:
        self.assertIn("promotes nothing here to hard setting canon by itself", doc_norm())


if __name__ == "__main__":
    unittest.main()
