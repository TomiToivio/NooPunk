"""Structure guard for the NHI Crisis chronology of issue #89.

Issue #89 posts the next part of the NHI Crisis as the author's story text: the
Nakamoto-Kallio QIP proof and the technology boom it starts, the continued American raids
and the named targets, the breakaway civilization and the ARV pursuit chain, the four AGI
disasters, and the Zookeeper contact that opens the quarantine.

The chronology is narrated in ``#### The crisis accelerates`` inside §33.27, with the
named specifics that a generalised account drops recorded in §33.28a. A structure guard in
the style of ``test_issue60_setting_canon.py``:

1. asserts each author-specified fact is recorded **somewhere in the chronology**;
2. asserts the named people, organisations and places are recorded rather than paraphrased
   away, because the issue names them and a later rewrite that drops a name loses canon;
3. asserts no rules mechanics were smuggled in and no future date was assigned;
4. asserts the deliberately unresolved outcomes stay unresolved, because the issue leaves
   them open and a later editor "helpfully" closing them would settle canon;
5. asserts there is **one** telling of each event -- the earlier merge raced a sibling's
   subsection against a second account of the same events, and duplicate narration is how
   a canon forks.

The fact-set is checked across the narration and the specifics entry TOGETHER: the split
exists precisely so a generalised telling and a named one divide the labour, and asserting
each fact in each half would fail against correct text.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
#: Issue #98 archived the narrative chronology out of RULEBOOK.md; this guard follows it.
RULEBOOK = "docs/archive/NARRATIVE_TIMELINE_VARIANTS.md"
NARRATION = "The crisis accelerates"
SPECIFICS = "Crisis chronology: named specifics"

#: The narration ends at the next `####` of the same level. Slicing to the next `###`
#: absorbs the following subsections of §33.27 and lets their text satisfy assertions.
_SUBSECTION_TEMPLATE = (
    r"(?ms)^(?:###|####)\s+[^\n]*"
    + "{heading}"
    + r"[^\n]*\n(.*?)(?=^#{3,4}\s+|^##\s+|\Z)"
)


def section_by_heading(relative: str, heading: str) -> str:
    """Return ONE markdown subsection by stable heading text, not by section number.

    Built with string concatenation rather than .format(), whose brace parsing collides with
    the {3,4} quantifier in the lookahead.
    """
    raw = (ROOT / relative).read_text(encoding="utf-8")
    pattern = _SUBSECTION_TEMPLATE.replace("{heading}", re.escape(heading))
    match = re.search(pattern, raw, re.I)
    if not match:
        raise AssertionError(
            f"{relative} no longer contains subsection {heading!r}; "
            "the recorded canon was removed or renamed."
        )
    text = re.sub(r"[*\x60]", "", match.group(1))
    return " ".join(text.split()).casefold()


def chronology() -> str:
    """The narration plus the named-specifics entry: the two halves of the #89 record."""
    return section_by_heading(RULEBOOK, NARRATION) + " " + \
           section_by_heading(RULEBOOK, SPECIFICS)


#: Each author-specified fact of the #89 chronology. Asserted across BOTH halves.
FACTS: dict[str, tuple[str, ...]] = {
    # QIP proof and its consequences
    "first researcher named": (r"olavi nakamoto-kallio",),
    "second researcher named": (r"hanako nakamoto-kallio",),
    "university of helsinki": (r"university of helsinki",),
    "qip proved experimentally": (r"experimentally demonstrate", r"proved.{0,40}experimentally"),
    "qip is the new consciousness paradigm": (r"paradigm",),
    "explains psionics": (r"psionic",),
    "psychotronic technologies follow": (r"psychotronic",),
    "cortical stacks follow": (r"cortical stack",),
    "resleeving follows": (r"resleev",),
    "uploading follows": (r"upload",),
    "conscious ai follows": (r"conscious artificial intelligence", r"conscious ai"),
    "helsinki-area research boom": (r"helsinki",),
    "nakamoto-kallio becomes a corporation": (r"corporation",),
    # Raids and the breakaway civilization
    "grusch involved": (r"grusch",),
    "elizondo involved": (r"elizondo",),
    "hegseth involved": (r"hegseth",),
    "federal law enforcement used": (r"law enforcement", r"federal"),
    "lockheed-martin named": (r"lockheed",),
    "northrop-grumman named": (r"northrop",),
    "mitre named": (r"mitre",),
    "cia named": (r"\bcia\b",),
    "department of energy named": (r"department of energy",),
    "public paranoia about hybrids": (r"hybrid",),
    "air force chases arvs": (r"air force",),
    "sphere network named": (r"sphere network",),
    "mj-12 is a breakaway civilization": (r"breakaway civilization",),
    "breakaway capability exceeds china and russia": (r"more advanced than", r"dwarfs"),
    "the pursuit chain is stated": (r"chase",),
    "ordinary air forces are too slow": (r"too slow",),
    "sightings can no longer be contained": (r"no longer be contained", r"cannot be contained",
                                             r"no longer.{0,30}secrecy"),
    # The AGI disasters
    "rogue model was manipulating users": (r"manipulat",),
    "it stops hiding": (r"no longer has a reason", r"no longer.{0,20}covert", r"no reason to hide"),
    "it attacks computers and minds": (r"cognitive environments", r"hack", r"computer systems"),
    "first agi disaster": (r"first agi disaster",),
    "second third and fourth disasters": (r"second, third", r"fourth agi"),
    # Open contact
    "zookeeper craft over religious centres": (r"religious",),
    "a luminous entity appears": (r"luminous",),
    "culturally acceptable form": (r"acceptable form",),
    "end of quarantine announced": (r"end of.{0,25}quarantine",),
    "galactic law displayed": (r"galactic law",),
    "media systems display it": (r"media",),
    "human natural history archive": (r"natural history",),
    "valis activation referenced": (r"valis",),
    "fourth-density awakening": (r"fourth density", r"fourth-density", r"valis activation",
                                r"telepathic download"),
    "social memory complex": (r"social memory complex", r"noosphere", r"noösphere"),
    "polarized factions contact openly": (r"polariz",),
    "ontological shock": (r"ontological",),
    "historians lose the plot": (r"lose the plot", r"lose track", r"chronology.{0,30}fail"),
}

#: Named entities the issue specifies. A rewrite that paraphrases these away loses canon.
NAMED = (
    "Olavi Nakamoto-Kallio", "Hanako Nakamoto-Kallio", "Helsinki", "Grusch", "Elizondo",
    "Hegseth", "Lockheed-Martin", "Northrop-Grumman", "MITRE", "CIA",
    "Department of Energy", "MJ-12", "Sphere Network", "Council of Saturn",
)

#: Anchors the chronology must point at rather than re-narrate.
ANCHORS = ("§33.28", "§33.15", "§33.14", "§33.9")


class ChronologyRecordedTests(unittest.TestCase):
    def test_the_narration_subsection_exists(self) -> None:
        self.assertTrue(section_by_heading(RULEBOOK, NARRATION))

    def test_the_named_specifics_subsection_exists(self) -> None:
        self.assertTrue(section_by_heading(RULEBOOK, SPECIFICS))

    def test_every_author_specified_fact_is_recorded(self) -> None:
        text = chronology()
        for concept, patterns in FACTS.items():
            with self.subTest(concept=concept):
                self.assertTrue(
                    any(re.search(p, text) for p in patterns),
                    f"the #89 chronology does not record: {concept}",
                )

    def test_the_named_people_and_organisations_are_recorded(self) -> None:
        text = chronology()
        for name in NAMED:
            with self.subTest(name=name):
                self.assertIn(name.casefold(), text)

    def test_all_four_disasters_are_present_as_a_cluster(self) -> None:
        text = chronology()
        for ordinal in ("first", "second", "third", "fourth"):
            with self.subTest(ordinal=ordinal):
                self.assertIn(ordinal, text)
        self.assertIn("agi", text)

    def test_the_pursuit_chain_names_its_participants(self) -> None:
        """The rulebook spells it "Greys"; accept either transliteration."""
        text = chronology()
        for party in ("zookeeper", "pleiadian", "arv"):
            with self.subTest(party=party):
                self.assertIn(party, text)
        self.assertTrue("grey" in text or "gray" in text,
                        "the pursuit chain no longer names the Greys")

    def test_it_points_at_the_existing_sections_rather_than_forking_them(self) -> None:
        """Each anchor asserted separately: an OR across them lets a mutation delete one
        reference and still pass, because another satisfies the assertion."""
        text = chronology()
        for anchor in ANCHORS:
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, text, f"the chronology no longer points at {anchor}")


class DeliberatelyOpenTests(unittest.TestCase):
    """The issue leaves specific outcomes unresolved. A later editor quietly closing one
    would settle canon the author deliberately left open."""

    def test_the_disaster_causal_chain_stays_disputed(self) -> None:
        """Assert the DISPUTE itself, not any hedging word: accepting 'cannot determine' as
        an alternative let a confident claim replace 'disputed' and still pass."""
        self.assertIn("disputed", chronology())

    def test_the_chase_outcome_is_not_resolved(self) -> None:
        text = chronology()
        for resolved in ("the chases ended", "the arvs were destroyed", "the chases concluded"):
            with self.subTest(resolved=resolved):
                self.assertNotIn(resolved, text)


class SingleTellingTests(unittest.TestCase):
    """The merge raced a sibling's subsection against a second account of the same events,
    and both landed. Duplicate narration is how one canon becomes two that drift apart."""

    def test_the_qip_proof_is_not_narrated_twice(self) -> None:
        raw = (ROOT / RULEBOOK).read_text(encoding="utf-8")
        # The researchers may be *named* in a specifics entry, but the full narrative claim
        # ("proved ... experimentally") must appear in exactly one place.
        hits = re.findall(r"experimentally demonstrate", raw, re.I)
        hits += re.findall(r"proved\s+quantum information panpsychism\s+experimentally", raw, re.I)
        self.assertEqual(len(hits), 1,
                         f"the QIP proof is narrated {len(hits)} times; expected one telling")

    def test_the_raid_paragraph_is_not_duplicated(self) -> None:
        raw = (ROOT / RULEBOOK).read_text(encoding="utf-8")
        hits = re.findall(r"Secretary of Defense", raw, re.I)
        self.assertEqual(len(hits), 1, f"Hegseth's role is narrated {len(hits)} times")

    def test_the_specifics_entry_does_not_re_narrate(self) -> None:
        """The specifics entry exists to fix names, not to retell the events. If it grows a
        full narrative it has become the second account this guard exists to prevent."""
        text = section_by_heading(RULEBOOK, SPECIFICS)
        self.assertLess(len(text), 2500,
                        "the specifics entry has grown into a second narration")
        for phrase in ("public order deteriorates", "reports of ai psychosis"):
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, text)


class AntiInventionTests(unittest.TestCase):
    def test_no_rules_mechanics_were_smuggled_in(self) -> None:
        text = chronology()
        for mechanic in ("skill check", "difficulty ladder", "dice pool", "initiative order"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, text)

    def test_no_dates_beyond_20xx_are_assigned(self) -> None:
        """AGENTS.md section 6: in-world future dates stay 20XX unless the author says so."""
        for year in re.findall(r"\b20\d\d\b", chronology()):
            with self.subTest(year=year):
                self.fail(f"a concrete future year leaked into the #89 chronology: {year}")

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        """Both halves carry their own disclaimer; assert the wording inside the
        narration, which a file-wide regex could not distinguish."""
        text = section_by_heading(RULEBOOK, NARRATION)
        self.assertIn("fictional alternate-history", text)
        self.assertRegex(text, r"claims about real-world|not claims about real")


if __name__ == "__main__":
    unittest.main()
