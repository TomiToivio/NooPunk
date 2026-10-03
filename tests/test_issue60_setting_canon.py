"""Guard for the newest author-specified setting canon (§33.14, issue #60).

`317805f` consolidated §33 from issue #60 ten minutes after the author posted the
stargate / SETI / Mars-ruins canon, and missed it. The scenario module recorded the
facts while the canonical ledger did not — the inverse of the usual drift, and worse,
because §26 makes the rulebook the place a setting decision is written down.

So this guard does two things a single-file check cannot:

1. asserts each author-specified fact is recorded in `RULEBOOK.md`;
2. asserts the rulebook and the playable scenario **agree**, since a fact recorded in
   only one of them is exactly the drift that happened.

Cross-document assertions match CONCEPTS, not exact strings: the rulebook is prose and
the scenario is room text, so they legitimately word the same fact differently
("five ET civilizations contacted on Earth" vs "five civilizations were contacted on
Earth"). A per-document regex set per concept keeps the check real without pinning one
document's phrasing into the other.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from text_game.prefall import prefall_world

RULEBOOK = "RULEBOOK.md"

#: Each author-specified fact, with the alternations that satisfy it in prose. These
#: are concept checks: any one alternative means the fact is present.
FACTS: dict[str, tuple[str, ...]] = {
    "stargates": (r"stargates?",),
    "built by the zookeepers": (r"zookeepers",),
    "billions of years old": (r"billions of years ago",),
    "gates explain some UAP traffic": (r"some (?:of the (?:observed )?)?uap traffic",),
    "gates do not explain all of it": (
        r"do(?:es)? not explain all",
        r"they do not explain",
        r"also observed using warp drives",
        r"remaining warp-drive uap traffic they do not explain",
    ),
    "warp-drive UAPs": (r"warp drives?",),
    "crash-retrieval material": (r"crash[- ]retrieval material",),
    "ancient ruins on Mars": (r"ancient ruins",),
    "Mars life": (r"pre-existing life", r"life, and evidence"),
    "prior non-human civilization on Mars": (r"prior non-human civilization",),
    "Mars Eldrich": (r"mars eldrich",),
    "SETI interstellar detection": (r"interstellar radio signals?",),
    "seventh detected ET civilization": (r"seventh detected (?:et|extraterrestrial) civilization",),
    "five contacted on Earth": (
        r"five et civilizations contacted on earth",
        r"five civilizations were contacted on earth",
    ),
    "extinct/vanished sixth from ruins": (r"extinct or vanished sixth", r"sixth .{0,30}ruins"),
    "no scientific consensus": (
        r"no scientific consensus",
        r"no consensus",
        r"remains unsettled",
    ),
    "noetics contested": (r"noetics",),
    "plasmoids contested": (r"plasmoids",),
    "constructs contested": (r"constructs",),
}

#: Facts the scenario states that the rulebook legitimately does not restate.
SCENARIO_ONLY = ("mars eldrich", "20xx")

_YEAR_RE = re.compile(r"\b20[3-9]\d\b")


def normalised(relative: str) -> str:
    """Emphasis-stripped, whitespace-collapsed, lowercased document text.

    Emphasis removal is not cosmetic: the rulebook writes key terms in ``**bold**``,
    so a phrase assertion written against the rendered text fails on correct prose.
    """
    text = (ROOT / relative).read_text(encoding="utf-8")
    text = re.sub(r"[*`]", "", text)
    return " ".join(text.split()).casefold()


def scenario_text() -> str:
    world = prefall_world()
    parts = [room.description for room in world.rooms.values()]
    parts += [item.description for item in world.items.values()]
    return " ".join(parts).casefold()


def has_concept(text: str, concept: str) -> bool:
    return any(re.search(pattern, text) for pattern in FACTS[concept])


class RulebookRecordsTheCanonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = normalised(RULEBOOK)
        self.section = self.text.split("33.14", 1)[1]

    def test_the_newest_canon_subsection_exists(self) -> None:
        self.assertIn("33.14", self.text)

    def test_every_author_specified_fact_is_recorded(self) -> None:
        for concept in FACTS:
            with self.subTest(concept=concept):
                self.assertTrue(
                    has_concept(self.section, concept),
                    f"RULEBOOK.md §33.14 does not record: {concept}",
                )

    def test_no_dates_beyond_20xx_are_assigned(self) -> None:
        """AGENTS.md §6: the year is 20XX unless the author says otherwise."""
        offenders = [m.group(0) for m in _YEAR_RE.finditer(self.section)]
        self.assertEqual(offenders, [], f"§33.14 assigns concrete years: {offenders}")

    def test_the_count_is_seven_and_not_inflated(self) -> None:
        self.assertIn("seventh", self.section)
        self.assertIn("seven", self.section)
        for inflated in ("eight civilizations", "ten detected", "nine civilizations"):
            with self.subTest(inflated=inflated):
                self.assertNotIn(inflated, self.section)


class RulebookAndScenarioAgreeTests(unittest.TestCase):
    """A fact recorded in only one place is the drift that actually happened."""

    def setUp(self) -> None:
        self.rulebook_section = normalised(RULEBOOK).split("33.14", 1)[1]
        self.scenario = scenario_text()

    def test_shared_facts_appear_in_both_documents(self) -> None:
        for concept in FACTS:
            with self.subTest(concept=concept):
                self.assertTrue(
                    has_concept(self.rulebook_section, concept),
                    f"missing from rulebook §33.14: {concept}",
                )
                self.assertTrue(
                    has_concept(self.scenario, concept),
                    f"missing from the scenario: {concept}",
                )

    def test_scenario_only_facts_are_still_in_the_scenario(self) -> None:
        for fact in SCENARIO_ONLY:
            with self.subTest(fact=fact):
                self.assertIn(fact, self.scenario)

    def test_neither_document_inflates_the_count(self) -> None:
        for label, text in (("rulebook", self.rulebook_section), ("scenario", self.scenario)):
            with self.subTest(document=label):
                self.assertIn("seventh", text)
                self.assertNotIn("ten detected", text)
                self.assertNotIn("eight civilizations", text)


class AntiInventionTests(unittest.TestCase):
    """The addition records canon; it must not author more of it."""

    def setUp(self) -> None:
        self.section = normalised(RULEBOOK).split("33.14", 1)[1]

    def test_no_new_named_entities_were_introduced(self) -> None:
        for invented in ("federation", "empire", "republic", "the council", "directorate"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, self.section)

    def test_the_subsection_adds_no_mechanics(self) -> None:
        """Setting facts only: no dice, no new statistics."""
        for mechanic in ("damage", "initiative", "armour", "armor", "attribute", "skill check"):
            with self.subTest(mechanic=mechanic):
                self.assertNotIn(mechanic, self.section)

    def test_the_classification_dispute_is_left_unresolved(self) -> None:
        self.assertIn("dispute", self.section)
        self.assertNotIn("are civilizations", self.section)
        self.assertNotIn("are not civilizations", self.section)


if __name__ == "__main__":
    unittest.main()
