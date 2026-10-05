"""Structure guard for the disclosure-cascade lore of issue #86.

Issue #86 posts the NHI Crisis opening as the author's story text: the AI ideological
fracture, China's transformation, the geopolitical collapse, the American and Chinese
announcements, the Kapustin Jar auction, the raid on the Legacy Program, and the wave of
national disclosures that followed. A sibling commit landed the *opening* (the sections up
to the American and Chinese presentations); this guard covers the rest.

A structure guard in the style of ``test_issue60_setting_canon.py``:

1. asserts each author-specified fact of the cascade is recorded in ``RULEBOOK.md``;
2. asserts the named people and places are recorded rather than paraphrased away, because
   the issue names them and a later rewrite that drops a name loses canon;
3. asserts the section adds no rules mechanics and assigns no dates beyond 20XX;
4. asserts the fictional-use disclaimer survives, since this section uses real people and
   real states, and the disclaimer is what keeps that from being a real-world claim.

Concept assertions match on alternatives rather than one literal phrase, because the
rulebook is prose and the same fact can be worded on a later edit without ceasing to be
recorded.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
#: Issue #98 moved the narrative-heavy disclosure cascade out of the canonical rulebook
#: into this archive, so the guard reads the archive rather than RULEBOOK.md.
RULEBOOK = "docs/archive/NARRATIVE_TIMELINE_VARIANTS.md"
HEADING = "The Kapustin Jar auction and the global disclosure cascade"


def flat(relative: str) -> str:
    raw = (ROOT / relative).read_text(encoding="utf-8")
    return " ".join(re.sub(r"[*\x60]", "", raw).split())


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


#: Each author-specified fact of the disclosure cascade, with the alternations that
#: satisfy it in prose. Any one alternative means the fact is recorded.
FACTS: dict[str, tuple[str, ...]] = {
    "kapustin jar is the russian roswell": (r"russian roswell",),
    "saparov is the accidental dictator of astrakhan": (r"accidental military dictator",),
    "saparov killed almazbek": (r"almazbek",),
    "saparov commanded the 73rd guards": (r"73rd\s+guards",),
    "soviet alien technology left in the bunker": (r"secret laboratory", r"bunker"),
    "the collection was auctioned": (r"highest bidder", r"auction"),
    "the auction raised 37.5 billion dollars": (r"37\.5\s*billion",),
    "saparov levitated a scientist": (r"levitat",),
    "the antigravity belt demonstration": (r"antigravity belt",),
    "buyers arrived from europe": (r"swedish aerospace", r"german intelligence", r"austrian"),
    "raids on lockheed martin and northrop grumman": (r"northrop grumman",),
    "the deep underground military base": (r"deep underground military base",),
    "the base descends from mj-12": (r"mj-12",),
    "grusch and elizondo identified the target": (r"grusch", r"elizondo"),
    "hegseth planned the operation": (r"hegseth",),
    "delta force flew in": (r"delta force",),
    "the search warrant at the door": (r"search warrant", r"warrant"),
    "brazil disclosed attacks on humans": (r"attacking\s+humans", r"injured"),
    "colares is the famous case": (r"colares",),
    "varginha crash and living humanoid": (r"varginha",),
    "brazil: amazonian traditions and dmt": (r"dimethyltryptamine", r"dmt"),
    "brazil: both consciousness and technology": (r"both consciousness-related", r"consciousness-related and physical"),
    "the chupa-chupa is cryptozoological": (r"chupa-chupa",),
    "peru: nazca mummies are real": (r"nazca",),
    "peru: the tridactyls": (r"tridactyl",),
    "peru: underground cities": (r"underground tridactyl cities",),
    "peru classifies them cryptoterrestrial": (r"cryptoterrestrial",),
    "the nordic five disclose together": (r"nordic",),
    "the nordic team existed since the 1930s": (r"ghost fliers",),
    "hard evidence since the ghost rockets of 1946": (r"ghost rockets",),
    "isotope ratios are extraterrestrial": (r"isotope ratios",),
    "the ghost rockets were transmedium": (r"transmedium",),
    "hessdalen lights are plasmoids": (r"hessdalen",),
    "mystery drones are conflated with russian drones": (r"mystery drones",),
    "villarroel: anomalous objects in 1950s orbit": (r"orbital", r"in earth orbit", r"orbit"),
    "cardena, parker, marcusson-clavertz: psi results": (r"marcusson-clavertz",),
    "eu and un level teams are formed": (r"united nations",),
    "egypt: the hall of records": (r"hall of records",),
    "india: vimanas and siddhis": (r"vimanas",),
    "france released scientific evidence": (r"france",),
    "the cascade never harmonises": (r"no single human disclosure narrative", r"plural", r"contradict"),
}

#: People and places the issue names. A rewrite that paraphrases these away loses canon.
NAMED = (
    "Saparov", "Almazbek", "Kapustin Jar", "Astrakhan", "Grusch", "Elizondo", "Hegseth",
    "Colares", "Varginha", "Nazca", "Tridactyl", "Hessdalen", "Villarroel", "Cardena",
    "Parker", "Marcusson-Clavertz", "Hall of Records", "Vimana",
)

#: The Nordic heads of government and team members the issue names.
NORDIC_NAMES = (
    "Stubb", "Kristersson", "Støre", "Fredriksen", "Frostadóttir",
    "Romppainen", "Falk", "Haugland", "Vestergaard", "Þórðarson",
)


class CascadeRecordedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, HEADING)

    def test_the_cascade_subsection_exists(self) -> None:
        self.assertTrue(self.section, "the disclosure-cascade subsection is empty or gone")

    def test_every_author_specified_fact_is_recorded(self) -> None:
        for concept, patterns in FACTS.items():
            with self.subTest(concept=concept):
                self.assertTrue(
                    any(re.search(p, self.section, re.I) for p in patterns),
                    f"the cascade section does not record: {concept}",
                )

    def test_the_named_people_and_places_are_recorded(self) -> None:
        for name in NAMED:
            with self.subTest(name=name):
                self.assertIn(name.casefold(), self.section)

    def test_the_nordic_delegations_are_named(self) -> None:
        for name in NORDIC_NAMES:
            with self.subTest(name=name):
                self.assertIn(name.casefold(), self.section)

    def test_the_auction_outcome_names_the_three_buyers(self) -> None:
        for buyer in ("swedish aerospace", "german intelligence", "austrian"):
            with self.subTest(buyer=buyer):
                self.assertIn(buyer, self.section)


class AntiInventionTests(unittest.TestCase):
    """The addition records the author's canon; it must not author more of it."""

    def setUp(self) -> None:
        self.section = section_by_heading(RULEBOOK, HEADING)

    def test_no_rules_mechanics_were_smuggled_in(self) -> None:
        for mechanic in ("skill check", "initiative", "difficulty ladder", "dice pool"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, self.section)

    def test_no_dates_beyond_20xx_are_assigned(self) -> None:
        """AGENTS.md section 6: in-world future dates stay 20XX unless the author says
        otherwise. Historical years the author names (1930s, 1946, 1983) are fine; a
        concrete future year is not."""
        tail = self.section.split("nhi crisis")[-1]
        for year in re.findall(r"\b20\d\d\b", tail):
            with self.subTest(year=year):
                self.fail(f"a concrete future year leaked into the cascade section: {year}")

    def test_the_fictional_use_disclaimer_survives(self) -> None:
        self.assertIn("fictional alternate-history lore", self.section)
        self.assertIn("not claims about real-world", self.section)

    def test_the_cascade_is_not_harmonised_into_one_narrative(self) -> None:
        """The issue is explicit that disclosure is plural; a later edit must not resolve
        the contradictions into a single authoritative account."""
        self.assertIn("no single human disclosure narrative", self.section)

    def test_the_psi_findings_are_not_called_proof_of_a_theory(self) -> None:
        """The repo keeps epistemic tiers apart: an in-setting result is not a claim that
        a real-world theory is true."""
        self.assertNotIn("proves that psi is real", self.section)


if __name__ == "__main__":
    unittest.main()
