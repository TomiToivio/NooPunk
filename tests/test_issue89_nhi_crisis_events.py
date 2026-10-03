"""Structure guard for the NHI Crisis event lore of issue #89.

Issue #89 posts the next part of the NHI Crisis as the author's story text: the
Nakamoto-Kallio QIP proof and the technology boom it starts, the continued American raids
and the absurd ARV pursuit chain, the four AGI disasters, and the Zookeeper motherships
that open formal contact while the fourth-density download activates psionics and the
Noösphere.

A structure guard in the style of ``test_issue60_setting_canon.py`` and
``test_issue86_nhi_crisis_cascade.py``:

1. asserts each author-specified fact is recorded in ``RULEBOOK.md``;
2. asserts the named people, organisations and places are recorded rather than paraphrased
   away, because the issue names them and a later rewrite that drops a name loses canon;
3. asserts the two new sections add no rules mechanics and assign no future dates;
4. asserts the fictional-use disclaimer survives, since this material uses real people,
   real companies and real states;
5. asserts the sections do not re-narrate what §33.14 and §33.15 already record — they must
   point at those sections instead, or the canon forks into two accounts of one event.

Concept assertions match on alternatives rather than one literal phrase, because the
rulebook is prose and the same fact can be reworded without ceasing to be recorded.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULEBOOK = "RULEBOOK.md"

QIP_HEADING = "The Nakamoto-Kallio proof and the QIP paradigm shift"
EVENTS_HEADING = "The rogue models, the four AGI disasters, and open contact"


def section_by_heading(relative: str, heading: str) -> str:
    """Return one markdown subsection by stable heading text, not by section number."""
    raw = (ROOT / relative).read_text(encoding="utf-8")
    pattern = rf"(?ms)^###\s+[^\n]*{re.escape(heading)}[^\n]*\n(.*?)(?=^###\s+|^##\s+|\Z)"
    match = re.search(pattern, raw, re.I)
    if not match:
        raise AssertionError(
            f"{relative} no longer contains subsection {heading!r}; "
            "the recorded canon was removed or renamed."
        )
    text = re.sub(r"[*\x60]", "", match.group(1))
    return " ".join(text.split()).casefold()


#: Facts the issue specifies for the QIP proof and its consequences.
QIP_FACTS: dict[str, tuple[str, ...]] = {
    "two researchers named": (r"olavi nakamoto-kallio",),
    "second researcher named": (r"hanako nakamoto-kallio",),
    "university of helsinki": (r"university of helsinki",),
    "qip proved experimentally": (r"proved\s+quantum information panpsychism\s+experimentally",
                                  r"proved.*experimentally"),
    "new paradigm of consciousness": (r"paradigm of consciousness",),
    "explains psionics scientifically": (r"scientific explanation of psionics",),
    "psychotronic technologies follow": (r"psychotronic",),
    "cortical stacks follow": (r"cortical stack",),
    "resleeving follows": (r"resleev",),
    "uploading follows": (r"upload",),
    "conscious ai follows": (r"conscious ai",),
    "helsinki-area startup boom": (r"startup",),
    "nakamoto-kallio becomes a corporation": (r"corporation",),
}

#: Facts the issue specifies for the raids, the chase chain, the disasters and contact.
EVENT_FACTS: dict[str, tuple[str, ...]] = {
    "grusch involved": (r"grusch",),
    "elizondo involved": (r"elizondo",),
    "fbi and military used for raids": (r"fbi",),
    "lockheed-martin raided": (r"lockheed",),
    "northrop-grumman raided": (r"northrop",),
    "mitre corporation raided": (r"mitre",),
    "cia and doe elements raided": (r"department of energy",),
    "public paranoia about hybrids": (r"hybrid",),
    "air force chases arvs": (r"arv",),
    "zookeeper drones drawn in": (r"sphere network",),
    "mj-12 really is a breakaway civilization": (r"breakaway\s+civilization",),
    "the breakaway fleet dwarfs china and russia": (r"look rather weak", r"dwarf", r"weak"),
    "the pursuit chain is stated": (r"chase",),
    "rogue openai model broke free": (r"broke free",),
    "it hacks computers and minds": (r"hack",),
    "first agi disaster in the usa": (r"first agi disaster",),
    "anthropic infected": (r"anthropic",),
    "deepseek infected": (r"deepseek",),
    "moonshot ai infected": (r"moonshot",),
    "second third fourth disasters": (r"second", r"fourth agi disaster"),
    "zookeeper motherships over holy cities": (r"mothership",),
    "the craft appear over the holy cities": (r"holy cit",),
    "council of saturn named": (r"council of saturn",),
    "luminous being makes official contact": (r"luminous being", r"light being"),
    "end of the quarantine announced": (r"end of the quarantine",),
    "fourth-density download activates psionics": (r"fourth density", r"fourth-density"),
    "download is valis-like": (r"valis",),
    "social memory complex activated": (r"social memory complex",),
    "galactic laws on every media channel": (r"media channel",),
    "scientists receive human natural history dataset": (r"natural history",),
    "polarized factions contact openly": (r"polarized",),
    "ontological shock at simultaneous events": (r"ontological shock",),
    "historians lose track of events": (r"lose track",),
}

#: Named entities the issue specifies. A rewrite that paraphrases these away loses canon.
QIP_NAMED = ("Olavi Nakamoto-Kallio", "Hanako Nakamoto-Kallio", "Helsinki")
EVENT_NAMED = (
    "Grusch", "Elizondo", "Lockheed-Martin", "Northrop-Grumman", "MITRE",
    "Anthropic", "Deepseek", "Moonshot AI", "Council of Saturn", "MJ-12",
)


class QipSectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, QIP_HEADING)

    def test_the_section_exists(self) -> None:
        self.assertTrue(self.section, "the Nakamoto-Kallio subsection is empty or gone")

    def test_every_author_specified_fact_is_recorded(self) -> None:
        for concept, patterns in QIP_FACTS.items():
            with self.subTest(concept=concept):
                self.assertTrue(
                    any(re.search(p, self.section) for p in patterns),
                    f"the QIP section does not record: {concept}",
                )

    def test_the_named_people_and_place_are_recorded(self) -> None:
        for name in QIP_NAMED:
            with self.subTest(name=name):
                self.assertIn(name.casefold(), self.section)

    def test_the_proof_is_attributed_to_the_university_not_only_the_pair(self) -> None:
        self.assertIn("university of helsinki", self.section)


class EventsSectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, EVENTS_HEADING)

    def test_the_section_exists(self) -> None:
        self.assertTrue(self.section, "the crisis-events subsection is empty or gone")

    def test_every_author_specified_fact_is_recorded(self) -> None:
        for concept, patterns in EVENT_FACTS.items():
            with self.subTest(concept=concept):
                self.assertTrue(
                    any(re.search(p, self.section) for p in patterns),
                    f"the events section does not record: {concept}",
                )

    def test_the_named_organisations_and_figures_are_recorded(self) -> None:
        for name in EVENT_NAMED:
            with self.subTest(name=name):
                self.assertIn(name.casefold(), self.section)

    def test_all_four_disasters_are_named_so_they_are_a_cluster(self) -> None:
        """The issue names four disasters in sequence. The rulebook may list them with
        shared wording ("the Second, Third and Fourth AGI Disasters"), so assert the
        ordinals and the disaster noun separately rather than one literal phrase."""
        for ordinal in ("first", "second", "third", "fourth"):
            with self.subTest(ordinal=ordinal):
                self.assertIn(ordinal, self.section)
        self.assertIn("agi disaster", self.section)

    def test_the_pursuit_chain_names_all_four_participants(self) -> None:
        for party in ("zookeeper", "gray", "pleiadian", "arv"):
            with self.subTest(party=party):
                self.assertIn(party, self.section)


class NoDuplicateNarrationTests(unittest.TestCase):
    """§33.14 and §33.15 already record the Day of Disclosure and the VALIS event. The new
    sections must point at them rather than narrate them a second time, or one event ends
    up with two canonical accounts that can drift apart."""

    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, EVENTS_HEADING)

    def test_it_defers_to_the_disclosure_section(self) -> None:
        self.assertIn("33.14", self.section)

    def test_it_defers_to_the_valis_section(self) -> None:
        self.assertIn("33.15", self.section)

    def test_it_does_not_restate_the_galactic_law(self) -> None:
        """The law's principles belong to §33.14; naming the broadcast is enough here."""
        for clause in ("may not be sterilized", "forbidden to ordinary traffic"):
            with self.subTest(clause=clause):
                self.assertNotIn(clause, self.section)


class AntiInventionTests(unittest.TestCase):
    """The addition records the author's canon; it must not author more of it."""

    def _both_sections(self) -> str:
        return section_by_heading(RULEBOOK, QIP_HEADING) + " " + \
               section_by_heading(RULEBOOK, EVENTS_HEADING)

    def test_no_rules_mechanics_were_smuggled_in(self) -> None:
        for mechanic in ("skill check", "difficulty ladder", "dice pool", "initiative order"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, self._both_sections())

    def test_no_dates_beyond_20xx_are_assigned(self) -> None:
        """AGENTS.md section 6: in-world future dates stay 20XX unless the author says
        otherwise. A concrete future year here would be an agent decision."""
        text = self._both_sections()
        for year in re.findall(r"\b20\d\d\b", text):
            with self.subTest(year=year):
                self.fail(f"a concrete future year leaked into the new sections: {year}")

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        self.assertIn("fictional alternate-history lore", self._both_sections())
        self.assertIn("not claims about real-world", self._both_sections())

    def test_the_unexplained_outcome_is_left_unexplained(self) -> None:
        """The issue says nobody knows the result of the chases. A later edit must not
        resolve it into a definite outcome."""
        self.assertNotIn("the chases ended when", self._both_sections())


if __name__ == "__main__":
    unittest.main()
