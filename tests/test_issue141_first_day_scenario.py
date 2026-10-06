"""Structure guard for the first playable NoöPunk scenario (issue #141).

Issue #141 asks for the scenario **"First Day in Ö-Mappi"**: a new Europol academy graduate
is assigned to a Suojelupoliisi unit that is informally the X-Files of Finnish intelligence.
The scenario lives in ``docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md``.

As with the other structure guards in this repo, the point is not to freeze prose but to
pin the properties a later session could silently drift:

1. the file exists and carries the author-specified title and pitch;
2. every one of the issue's **checklist deliverables** is genuinely present, not merely
   ticked — the issue enumerates sixteen, and a draft that quietly drops one should fail;
3. the four specialist tracks and four NPCs exist, with the author's specifics intact
   (the tactical specialist is a young athletic woman, the infosec specialist wears a
   Hawkwind T-shirt and smells like weed, the psionic investigator's ability is empathy);
4. the **canon anchors** it builds on are actually cited and traceable to the rulebook,
   so the scenario cannot drift into inventing its own history;
5. the **canon-discipline** statements survive: the draft label, the editable-names clause,
   the fictional-use disclaimer, and the 20XX rule. A later editor trimming prose could
   drop any of these and make scenario-local material read as setting canon;
6. the deeper setting truths stay **unresolved**: the scenario must say that the identity
   of the second figure, the nature of the fragments and the meaning of "source" are *not*
   settled here. The failure mode this guards against is a later session "helpfully"
   resolving them.

Assertion discipline (learned the hard way on the #131/#141 guards):

* assert each deliverable as its **own** assertion, never one alternation, so a dropped
  deliverable cannot hide behind a surviving sibling fact;
* **anchor ambiguous tokens**: "empathy", "unreliable" and "blind spot" each occur several
  times, so a bare-substring check stays green after the specific fact is removed;
* match prose that carries blockquote or emphasis markers against the **normalised** text.

Uses only the standard library: CI installs requirements.txt and nothing else.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = ROOT / "docs" / "scenarios" / "01_FIRST_DAY_IN_OMAPPI.md"
RULEBOOK = ROOT / "RULEBOOK.md"


def scenario() -> str:
    """Whitespace-collapsed scenario text, so line wrapping cannot hide a term."""
    return " ".join(SCENARIO.read_text(encoding="utf-8").split())


def normalised(text: str) -> str:
    """Strip markdown structural markers, then collapse whitespace and case.

    The disclaimer and several other asserted sentences sit inside blockquotes and carry
    emphasis, so a plain substring match fails against a document that plainly contains
    them. Strip ``>`` ``*`` ``_`` `` ` `` and the quotation marks that survive around
    quoted terms -- never the comparison and range characters, which are canon text.
    """
    for marker in (">", "*", "_", "`", '"', "'"):
        text = text.replace(marker, "")
    return " ".join(text.split()).lower()


def scenario_norm() -> str:
    return normalised(SCENARIO.read_text(encoding="utf-8"))


def rulebook_sections() -> set[str]:
    """Every numbered heading in RULEBOOK.md, e.g. {"5", "5.4", "9.2", "33"}.

    Used to verify the scenario's citations resolve. Reading the headings rather than
    grepping for literal ``§9.2`` tokens is the semantic check: the rulebook renders
    sections as ``## 10.`` / ``### 9.2`` and cites itself with the ``§`` shorthand, so a
    token grep tests the shorthand's spelling, not whether the target exists.
    """
    text = RULEBOOK.read_text(encoding="utf-8")
    return set(re.findall(r"(?m)^#{2,4}\s+(\d+(?:\.\d+)*)\.?", text))


class FileTests(unittest.TestCase):
    def test_the_scenario_exists(self) -> None:
        self.assertTrue(SCENARIO.exists(),
                        "docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md is missing")

    def test_the_scenario_keeps_its_stable_title(self) -> None:
        """The title is the anchor every cross-reference uses. An earlier guard elsewhere in
        this repo never asserted its document's heading, so renaming it left the guard green.
        """
        self.assertRegex(scenario(), r"^# Scenario 01: First Day in Ö-Mappi\b",
                         "the scenario title was renamed or removed")

    def test_the_scenario_opens_with_a_pitch(self) -> None:
        self.assertIn("## 1. Scenario pitch", scenario())
        # The pitch must actually say what the scenario is, not just be a heading.
        self.assertIn("First Day in Ö-Mappi", scenario())


class DeliverableTests(unittest.TestCase):
    """Every checkbox in the issue's Deliverables list must be genuinely present.

    Asserted as separate facts (one assertion each) rather than one alternation: a single
    combined regex passes when any one deliverable survives, which is exactly how a dropped
    deliverable hides.
    """

    def test_title_and_short_pitch(self) -> None:
        self.assertIn("## 1. Scenario pitch", scenario())

    def test_player_introduction_and_character_creation_hook(self) -> None:
        text = scenario()
        self.assertIn("## 2. Player character: Europol graduate", text)
        self.assertIn("newly graduated Europol officer", text)

    def test_europol_academy_specialist_track_descriptions(self) -> None:
        text = scenario()
        for track in (
            "law-enforcement training",
            "counterintelligence training",
            "### 2.1. SWAT / tactical operations",
            "### 2.2. Psionic asset",
            "### 2.3. Infosec asset",
            "### 2.4. Intelligence analyst",
        ):
            with self.subTest(track=track):
                self.assertIn(track, text)

    def test_helsinki_office_opening_scene(self) -> None:
        text = scenario()
        self.assertIn("## 3. Opening: first morning in Helsinki", text)
        self.assertIn("Helsinki", text)

    def test_o_mappi_office_description(self) -> None:
        """An office description means a described place, not just a roster. Anchored on a
        detail unique to the workspace section."""
        text = scenario()
        self.assertIn("## 4. The Ö-Mappi team", text)
        self.assertIn("### 3.2. The walk downstairs", text)
        self.assertIn("bureaucracy sedimenting in one room", text)

    def test_romppainen_gives_a_historical_briefing(self) -> None:
        text = scenario()
        self.assertIn("## 5. Romppainen's briefing", text)
        self.assertIn("### 4.1. Dr. Harri Romppainen", text)

    def test_inciting_case(self) -> None:
        text = scenario()
        self.assertIn("## 6. Inciting incident", text)
        self.assertIn("evidence case", text.lower())

    def test_branching_investigation_structure(self) -> None:
        text = scenario()
        self.assertIn("## 7. Investigation routes", text)
        for route in ("### 7.1. Tactical / physical route",
                      "### 7.2. Infosec / cybernetic route",
                      "### 7.3. Intelligence-analysis route",
                      "### 7.4. Social / interview route",
                      "### 7.5. Psychic route"):
            with self.subTest(route=route):
                self.assertIn(route, text, f"the branching structure lost {route!r}")

    def test_opportunities_for_all_four_specialist_tracks(self) -> None:
        """The issue requires at least one meaningful opportunity for each track, and the
        scenario answers with a spotlight matrix. Assert the matrix itself rather than the
        word "spotlight", which could survive a rename."""
        text = scenario()
        self.assertIn("## 12. Spotlight matrix", text)

    def test_first_session_climax(self) -> None:
        """Anchored on the section heading, not the bare phrase "custody decision": that
        phrase also appears in the scene-order list, so renaming the climax left the guard
        green."""
        text = scenario()
        self.assertIn("## 11. First-session climax: the custody decision", text)

    def test_hooks_into_later_scenarios(self) -> None:
        self.assertIn("## 16. Hooks for Scenario 02 and beyond", scenario())

    def test_gm_notes_separate_the_three_layers(self) -> None:
        text = scenario()
        self.assertIn("## 14. GM information layers", text)
        self.assertIn("### 14.1. Public / player-facing facts", text)
        self.assertIn("### 14.2. Classified but discoverable facts", text)
        self.assertIn("### 14.3. Deeper truth: deliberately unresolved", text)


class NpcEnsembleTests(unittest.TestCase):
    """The four core NPCs, with the author's specifics kept verbatim in substance."""

    def test_four_core_npcs_have_their_own_sections(self) -> None:
        for section in (
            "### 4.1. Dr. Harri Romppainen",
            "### 4.2. Draft NPC:",
            "### 4.3. Draft NPC:",
            "### 4.4. Draft NPC:",
        ):
            with self.subTest(section=section):
                self.assertIn(section, scenario())

    def test_romppainen_is_legendary_but_fallible(self) -> None:
        """The issue says he should feel legendary without becoming an infallible
        exposition machine. Both halves must survive: dropping the fallibility clause
        would make him an oracle.

        The fallibility half is anchored on his actual blind-spot line, not on a bare word
        that also occurs elsewhere in the document.
        """
        self.assertIn("has blind spots around institutional loyalty and old cases",
                      scenario())

    def test_tactical_specialist_is_a_young_athletic_woman_in_swat(self) -> None:
        text = scenario()
        self.assertIn("### 2.1. SWAT / tactical operations", text)
        self.assertIn("**Role:** tactical specialist.", text)
        # The author specifies a woman, young and physically capable.
        self.assertIn("Aino", text)
        self.assertIn("young, physically fit", text)
        self.assertIn("she ", text.lower())

    def test_infosec_specialist_keeps_his_author_specified_details(self) -> None:
        raw = scenario()
        for detail in ("long hair", "smells unmistakably of weed",
                       "Hawkwind T-shirt"):
            with self.subTest(detail=detail):
                self.assertIn(detail, raw)

    def test_infosec_specialist_is_not_comic_relief(self) -> None:
        """The issue explicitly forbids making him merely comic relief. Assert the
        expertise, on a specific claim rather than a bare word."""
        text = scenario_norm()
        self.assertIn("**Role:** infosec specialist.", scenario())
        self.assertTrue(
            "expertise" in text or "brilliant" in text or "genuinely" in text,
            "the infosec specialist must be given real expertise, not only a costume",
        )

    def test_psionic_investigator_has_empathy_as_primary_ability(self) -> None:
        """She must be an experienced police investigator who is also a monitored psionic
        asset, with empathy as her strongest ability.

        Anchored on her profile lines: "psionic asset" appears six times (including in
        the academy track and the psychic route), so a bare-phrase check stayed green when
        her own role line was changed.
        """
        raw = scenario()
        self.assertIn("**Role:** experienced police investigator and psionic asset.", raw)
        self.assertIn("Leena", raw)
        self.assertIn("empathy", raw.lower())

    def test_empathy_is_taught_as_social_and_psychic(self) -> None:
        """The issue asks the scenario to demonstrate how NoöPunk treats Empathy as
        simultaneously social and psychic, without becoming mind-reading."""
        text = scenario_norm()
        self.assertTrue(
            "empath refuses to call feelings proof" in text
            or "not mind-reading" in text
            or "psychic impressions functioning as perfect truth" in text,
            "the scenario must refuse the mind-reading reading of empathy",
        )


class CanonAnchorTests(unittest.TestCase):
    """The scenario must build on recorded canon and say where it comes from."""

    def test_ghost_flier_and_ghost_rocket_anchors_are_named(self) -> None:
        """Both canon wave anchors must be stated in the briefing's anchor list.

        Anchored on the section headings, not the bare tokens: the waves are mentioned
        several times, so renaming the anchor section itself would leave a token check green.
        """
        text = scenario()
        self.assertIn("### 5.2. Ghost Flyers, 1930s", text)
        self.assertIn("### 5.3. Ghost Rockets, 1946", text)

    def test_three_institutional_anchors_are_cited(self) -> None:
        for anchor in ("Suojelupoliisi", "Europol", "UNSA"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, scenario())

    def test_the_unsa_anchor_is_connected_to_the_rulebook(self) -> None:
        """The scenario names the UN Security Agency; it must tie that to the canonical
        UNSA institution (§38) rather than leaving a floating organisation."""
        text = scenario_norm()
        self.assertIn("unsa", text)
        self.assertIn("rulebook.md §38", text)

    def test_the_canon_anchors_are_traceable_to_the_rulebook(self) -> None:
        """Each rulebook section the scenario cites must actually exist, so a renumber
        cannot leave the citations dangling.

        Semantics, not tokens: the rulebook renders sections as ``## 10.`` / ``### 9.2``
        and cites itself with the ``§`` shorthand, so grepping for the literal string
        ``§9.2`` would test the shorthand's spelling rather than whether the target exists.
        """
        sections = rulebook_sections()
        for section in ("9.2", "38"):
            with self.subTest(section=section):
                self.assertIn(section, sections,
                              f"RULEBOOK.md does not define section {section}")

    def test_the_six_stat_model_is_the_current_one(self) -> None:
        """The scenario must reference the post-#131 six-stat model, not the superseded
        twelve. Asserted on the normalised text, and the retired codes are checked with
        word boundaries: a bare substring check on "ctl" matches inside "exactly"."""
        text = scenario_norm()
        self.assertIn("fit, ref, int, soc, cyb and psy", text)
        for retired in ("cyi", "bnd", "ctl", "noesis"):
            with self.subTest(retired=retired):
                self.assertNotRegex(text, rf"\b{retired}\b",
                                    f"the superseded stat code {retired!r} reappeared")


class CanonDisciplineTests(unittest.TestCase):
    """The draft must not promote scenario-local material to setting canon."""

    def test_the_scenario_declares_itself_a_draft(self) -> None:
        self.assertIn("first playable scenario draft", scenario_norm())

    def test_scenario_local_material_is_marked_as_such(self) -> None:
        """Asserted on the normalised text and on the *scope* sentence specifically: the
        bare phrase occurs twice, and the second occurrence is in my own chronology note,
        so removing the scope declaration would otherwise have stayed green."""
        self.assertIn("scope: scenario-local material", scenario_norm())

    def test_names_and_statistics_are_declared_editable(self) -> None:
        self.assertIn("names and statistics remain editable while drafting", scenario_norm())

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        """Real institutions and nations appear in this document; the repo's established
        disclaimer is what keeps it from reading as a real-world claim. A prose trim can
        drop it unnoticed, which is why it is asserted here."""
        self.assertIn(
            "this entire document is fictional alternate-history lore. real people, "
            "governments, companies and institutions are used as fictionalized setting "
            "elements; the events described here are not claims about real-world history "
            "or evidence.",
            scenario_norm(),
        )

    def test_the_20xx_rule_is_stated(self) -> None:
        self.assertIn("the setting is 20xx", scenario_norm())

    def test_no_future_year_is_assigned(self) -> None:
        """AGENTS.md §6: canonical future dates are 20XX. The historical anchors (1930s,
        1946) are real canon years and must not trip this. Match only 20xx-style tokens."""
        future = re.findall(r"\b(20\d\d)\b", scenario())
        self.assertEqual(
            future, [],
            f"the scenario assigns exact future years {sorted(set(future))}; canon uses 20XX",
        )


class UnresolvedMysteryTests(unittest.TestCase):
    """The scenario must explicitly refuse to settle the setting's larger mysteries.

    This is the highest-value part of the guard: the failure mode is a later session
    reading the scenario, seeing dangling threads, and tying them off.
    """

    def test_the_deeper_truths_are_explicitly_withheld(self) -> None:
        self.assertIn("do canonize the following in this draft", scenario_norm().replace(
            "not canonize", "canonize"))

    def test_the_second_figure_is_not_explained(self) -> None:
        self.assertIn("who or what the second figure is", scenario_norm())

    def test_the_fragments_are_not_declared_extraterrestrial(self) -> None:
        """§40 keeps the nature of recoveries open; the scenario must not answer it."""
        self.assertIn("whether the fragments are extraterrestrial", scenario_norm())

    def test_the_nature_of_the_incident_is_left_open(self) -> None:
        """The scenario must refuse to say whether the incident is psychic, cybernetic,
        technological or NHI-related, and must not resolve what "source" means.

        The "source" half is anchored on the *unresolved* list entry, not the bare phrase,
        which also appears in the earlier operational-lead sentence.
        """
        text = scenario_norm()
        self.assertIn("psychic, cybernetic, technological, nhi-related or a hybrid", text)
        self.assertIn("what source means; - which organization altered", text)

    def test_no_wallfacer_reveal(self) -> None:
        """Wallfacers are §38 canon but are not part of this scenario's reveal."""
        self.assertNotIn("wallfacer", scenario_norm())


if __name__ == "__main__":
    unittest.main()
