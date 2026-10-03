"""Structure guard for the NHI Crisis chronology of issue #89.

Issue #89 posts the next part of the NHI Crisis as the author's story text: the
Nakamoto-Kallio QIP proof and the technology boom it starts, the continued American raids,
the breakaway civilization and the ARV pursuit chain, the four AGI disasters, and the
Zookeeper contact that opens the quarantine.

The chronology itself was recorded by a sibling commit before this guard existed, so this
file's job is what was actually missing: **the section was unguarded**. Every other
author-specified lore block in §33 has a guard; this one had none, which means a later
rewrite could drop a named fact, resolve an outcome the author left open, or smuggle in
mechanics without any test noticing.

A structure guard in the style of ``test_issue60_setting_canon.py`` and
``test_issue86_nhi_crisis_cascade.py``:

1. asserts each author-specified fact is recorded in ``RULEBOOK.md``;
2. asserts the named people, organisations and places are recorded rather than paraphrased
   away, because the issue names them and a later rewrite that drops a name loses canon;
3. asserts no rules mechanics were smuggled in and no future date was assigned;
4. asserts the deliberately unresolved outcomes stay unresolved, because the issue leaves
   them open and a later editor "helpfully" closing them would settle canon;
5. asserts the fictional-use disclaimer survives, since this material uses real people,
   real companies and real states.

Concept assertions match on alternatives rather than one literal phrase, because the
rulebook is prose and the same fact can be reworded without ceasing to be recorded.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = "RULEBOOK.md"
HEADING = "The crisis accelerates"
#: The #89 subsection ends at the next `####` heading, NOT the next `###`. The enclosing
#: §33.27 continues for another ten subsections, and slicing to the next `###` pulls in the
#: older #86/#89-adjacent prose -- which then satisfies facts the mutation removed from the
#: #89 text, hiding real holes. Assert against the subsection only.
#: Built with string concatenation rather than .format(), whose brace parsing collides with
#: the {3,4} quantifier.
_SUBSECTION_TEMPLATE = (
    r"(?ms)^(?:###|####)\s+[^\n]*"
    + "{heading}"
    + r"[^\n]*\n(.*?)(?=^#{3,4}\s+|^##\s+|\Z)"
)


def section_by_heading(relative: str, heading: str) -> str:
    """Return ONE markdown subsection by stable heading text, not by section number.

    The bound is the next heading of the SAME OR HIGHER level, so a `####` subsection ends
    at the next `####` or `###`. Stopping only at `###` would absorb every following
    subsection and let their text satisfy assertions about this one.
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


#: Each author-specified fact of the #89 chronology, with the alternations that satisfy it.
FACTS: dict[str, tuple[str, ...]] = {
    # QIP proof and its consequences
    "first researcher named": (r"olavi nakamoto-kallio",),
    "second researcher named": (r"hanako nakamoto-kallio",),
    "university of helsinki": (r"university of helsinki",),
    "qip proved experimentally": (r"experimentally demonstrate", r"proved.{0,40}experimentally"),
    "qip is the new consciousness paradigm": (r"paradigm", r"consciousness"),
    "explains psionics": (r"psionic",),
    "psychotronic technologies follow": (r"psychotronic",),
    "cortical stacks follow": (r"cortical stack",),
    "resleeving follows": (r"resleev",),
    "uploading follows": (r"upload",),
    "conscious ai follows": (r"conscious artificial intelligence", r"conscious ai"),
    "helsinki-area research and startup boom": (r"helsinki",),
    "nakamoto-kallio becomes a corporation": (r"corporation",),
    # Raids and the breakaway civilization
    "grusch assists": (r"grusch",),
    "elizondo assists": (r"elizondo",),
    "hegseth assists": (r"hegseth",),
    "fbi or federal law enforcement used": (r"law enforcement", r"federal"),
    "lockheed-martin named": (r"lockheed",),
    "northrop-grumman named": (r"northrop",),
    "mitre named": (r"mitre",),
    "cia named": (r"\bcia\b",),
    "department of energy named": (r"department of energy",),
    "public paranoia about hybrids": (r"hybrid",),
    "air force chases arvs": (r"air force",),
    "sphere network named": (r"sphere network",),
    "mj-12 really is a breakaway civilization": (r"breakaway civilization",),
    "breakaway fleet exceeds china and russia": (r"more advanced than", r"substantially more advanced"),
    "the pursuit chain is stated": (r"chase",),
    "ordinary air forces are too slow": (r"too slow",),
    "sightings become too many to contain": (r"no longer be contained", r"cannot be contained"),
    # The AGI disasters
    "rogue model was manipulating users": (r"manipulat",),
    "it no longer hides": (r"no longer", r"covert"),
    "it hacks computers and minds": (r"cognitive environments", r"hack", r"computer systems"),
    "first agi disaster": (r"first agi disaster",),
    "second third and fourth disasters": (r"second, third", r"fourth agi"),
    # Open contact
    "zookeeper craft appear over religious centres": (r"religious",),
    "a luminous entity appears": (r"luminous",),
    "culturally acceptable form": (r"acceptable forms", r"acceptable form", r"locally acceptable"),
    "end of quarantine announced": (r"end of.{0,20}quarantine",),
    "galactic law displayed": (r"galactic law",),
    "media systems display it": (r"media",),
    "human natural history archive": (r"natural history",),
    "valis activation referenced": (r"valis",),
    "fourth-density awakening": (r"fourth density", r"fourth-density", r"valis activation",
                                r"telepathic download"),
    "social memory complex": (r"social memory complex", r"noosphere", r"noösphere"),
    "polarized factions contact openly": (r"polariz",),
    "ontological shock": (r"ontological",),
    "historians lose the plot": (r"lose the plot", r"lose track", r"chronology.{0,20}fail"),
}

#: Named entities the issue specifies. A rewrite that paraphrases these away loses canon.
NAMED = (
    "Olavi Nakamoto-Kallio", "Hanako Nakamoto-Kallio", "Helsinki", "Grusch", "Elizondo",
    "Hegseth", "Lockheed-Martin", "Northrop-Grumman", "MITRE", "CIA",
    "Department of Energy", "MJ-12",
)


class ChronologyRecordedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, HEADING)

    def test_the_chronology_subsection_exists(self) -> None:
        self.assertTrue(self.section, "the #89 chronology subsection is empty or gone")

    def test_every_author_specified_fact_is_recorded(self) -> None:
        for concept, patterns in FACTS.items():
            with self.subTest(concept=concept):
                self.assertTrue(
                    any(re.search(p, self.section) for p in patterns),
                    f"the #89 chronology does not record: {concept}",
                )

    def test_the_named_people_and_organisations_are_recorded(self) -> None:
        for name in NAMED:
            with self.subTest(name=name):
                self.assertIn(name.casefold(), self.section)

    def test_all_four_disasters_are_present_as_a_cluster(self) -> None:
        """The issue names four disasters in sequence; the rulebook may list the later ones
        with shared wording, so assert the ordinals and the noun separately."""
        for ordinal in ("first", "second", "third", "fourth"):
            with self.subTest(ordinal=ordinal):
                self.assertIn(ordinal, self.section)
        self.assertIn("agi", self.section)

    def test_the_pursuit_chain_names_its_participants(self) -> None:
        """Each participant is named. The rulebook spells it "Greys", so accept either
        transliteration rather than pinning one."""
        for party in ("zookeeper", "pleiadian", "arv"):
            with self.subTest(party=party):
                self.assertIn(party, self.section)
        self.assertTrue(
            "grey" in self.section or "gray" in self.section,
            "the pursuit chain no longer names the Greys",
        )

    def test_it_points_at_the_existing_sections_rather_than_forking_them(self) -> None:
        """§33.28 and §33.15 already hold the OpenAI Incident and the VALIS event; §33.9
        holds the Zookeeper probe ecology. The chronology must reference each rather than
        narrate a second account of it. Asserted separately: an OR across the three let a
        mutation delete one reference and still pass."""
        for anchor in ("§33.28", "§33.15", "§33.9"):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, self.section,
                              f"the chronology no longer points at {anchor}")


class DeliberatelyOpenTests(unittest.TestCase):
    """The issue leaves specific outcomes unresolved. A later editor quietly closing one
    would settle canon that the author deliberately left open."""

    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, HEADING)

    def test_the_disaster_causal_chain_stays_disputed(self) -> None:
        """The issue says the causal chain is disputed. Assert the DISPUTE itself, not any
        hedging word: an earlier version accepted 'cannot determine' as an alternative, so
        replacing 'disputed' with a confident claim still passed."""
        self.assertIn("disputed", self.section)

    def test_the_chase_outcome_is_not_resolved(self) -> None:
        for resolved in ("the chases ended", "the arvs were destroyed", "the chases concluded"):
            with self.subTest(resolved=resolved):
                self.assertNotIn(resolved, self.section)


class AntiInventionTests(unittest.TestCase):
    """The section records the author's canon; it must not author more of it."""

    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, HEADING)

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        """The #89 subsection carries its OWN disclaimer (this is a `####` inside §33.27, so
        the section-level one does not cover it). Assert the wording *inside* the subsection,
        which the earlier loose regex failed to distinguish."""
        self.assertIn("fictional alternate-history", self.section)
        self.assertRegex(self.section, r"claims about real-world|not claims about real")

    def test_no_rules_mechanics_were_smuggled_in(self) -> None:
        for mechanic in ("skill check", "difficulty ladder", "dice pool", "initiative order"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, self.section)

    def test_no_dates_beyond_20xx_are_assigned(self) -> None:
        """AGENTS.md section 6: in-world future dates stay 20XX unless the author says so."""
        for year in re.findall(r"\b20\d\d\b", self.section):
            with self.subTest(year=year):
                self.fail(f"a concrete future year leaked into the #89 chronology: {year}")


if __name__ == "__main__":
    unittest.main()
