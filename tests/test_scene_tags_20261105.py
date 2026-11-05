import unittest

from src.rules.scene_tags import ClueTag, GoalTag, PersonalityTag, SocialTag
from src.rules.goals import Goal
from src.rules.investigation import Clue, ClueKind
from src.world.graphs import Relationship


class SceneTagsTest(unittest.TestCase):
    def test_uses_authoritative_tag_records(self):
        self.assertIs(SocialTag, Relationship)
        self.assertIs(GoalTag, Goal)
        self.assertIs(ClueTag, Clue)
        self.assertEqual(SocialTag("a", "b", -4).score, -4)
        self.assertEqual(GoalTag("g", "pc", "character", "solve case", "short").horizon, "short")
        self.assertEqual(ClueTag("cl", "scene", ClueKind.CORE, "Notice", "a receipt").fact,
                         "a receipt")

    def test_personality_is_descriptive_only(self):
        tag = PersonalityTag("agent", "refuses to abandon witnesses", "episode-1")
        self.assertEqual(tag.trait, "refuses to abandon witnesses")
        self.assertFalse(hasattr(tag, "modifier"))
        with self.assertRaises(ValueError):
            PersonalityTag("agent", "")


if __name__ == "__main__":
    unittest.main()
