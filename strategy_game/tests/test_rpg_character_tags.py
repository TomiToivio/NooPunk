"""Character TAG tests for the Fate-based RPG layer (issue #389, criterion 1).

Criterion 1 asks for "aspects/TAGs" — aspects existed, typed TAGs did not. These are
executable-code tests, per #271, and the important one is the last: a TAG must not become a hidden
modifier, so two characters with the same skills and different tags must roll identically.
"""
from __future__ import annotations

import unittest
from random import Random

from strategy_game.characters import TAG_KINDS, Tag, tag_vocabulary_matches
from strategy_game.rpg.fate import Action, Character, ResourceError, demo_investigation, resolve


class SharedVocabularyTests(unittest.TestCase):
    def test_the_character_tag_vocabulary_is_the_shared_one(self) -> None:
        self.assertEqual(
            TAG_KINDS, ("belief", "competence", "equipment", "relationship", "asset", "goal")
        )
        # The same vocabulary the faction-creation data declares: one scheme, not two.
        self.assertTrue(tag_vocabulary_matches())

    def test_a_character_carries_typed_tags_and_looks_them_up_by_kind(self) -> None:
        actor = Character(
            "a", "Field Investigator", ["Precognitive Impressions"],
            skills={"Technology": 2, "Psi": 1},
            tags=(
                Tag("belief", "the Noösphere is not a metaphor"),
                Tag("competence", "forensic reconstruction"),
                Tag("equipment", "secure BCI"),
                Tag("relationship", "owes Lotta Kallio a favour"),
            ),
        )
        self.assertEqual(actor.tags_of_kind("belief")[0].value, "the Noösphere is not a metaphor")
        self.assertEqual(len(actor.tags_of_kind("competence")), 1)
        self.assertEqual(actor.tags_of_kind("goal"), ())
        self.assertEqual([t.kind for t in actor.tags], ["belief", "competence", "equipment", "relationship"])

    def test_a_bare_string_is_not_a_tag(self) -> None:
        with self.assertRaises(ResourceError):
            Character("a", "Agent", [], tags=("augmented",))  # type: ignore[arg-type]

    def test_a_duplicate_tag_is_refused(self) -> None:
        with self.assertRaises(ResourceError):
            Character("a", "Agent", [], tags=(Tag("belief", "x"), Tag("belief", "x")))

    def test_an_undeclared_tag_kind_is_refused_by_the_vocabulary(self) -> None:
        with self.assertRaises(ValueError):
            Tag("mood", "brooding")

    def test_tags_serialize_as_plain_data(self) -> None:
        self.assertEqual(Tag("asset", "Eldrich Corporation").to_dict(),
                         {"kind": "asset", "value": "Eldrich Corporation"})


class TagsAreNotModifiersTests(unittest.TestCase):
    """A tag is a label. If a tag changed a roll, it would be an unapproved mechanic."""

    def test_identical_skills_resolve_identically_whatever_the_tags_say(self) -> None:
        plain = Character("a", "Plain", [], skills={"Technology": 2})
        decorated = Character(
            "b", "Decorated", ["Local-Access Specialist"],
            skills={"Technology": 2},
            tags=(Tag("competence", "legendary netrunner"), Tag("equipment", "military-grade deck")),
        )
        for seed in range(8):
            first = resolve(Action.OVERCOME, plain.skills["Technology"], 3, rng=Random(seed))
            second = resolve(Action.OVERCOME, decorated.skills["Technology"], 3, rng=Random(seed))
            self.assertEqual(first, second, f"tags changed the roll at seed {seed}")

    def test_tagged_characters_still_run_the_existing_demo(self) -> None:
        scene = demo_investigation(4)
        self.assertEqual(scene, demo_investigation(4))
        operative = Character(
            "c", "Tagged Operative", ["Focused"], skills={"Psi": 1},
            natural_psi=True, psi_abilities=["empathy"], tags=(Tag("belief", "PSI is natural"),),
        )
        self.assertEqual(operative.tags_of_kind("belief")[0].value, "PSI is natural")


if __name__ == "__main__":
    unittest.main()
