"""Narrative tags and scene contracts: the only addition to the CWN core (#1178).

The failure modes this pins are the ones that would make tags a second game: a tag that grants a
number, a clue that promotes itself, a scene kind that quietly becomes a minigame, or "Astral" being
accepted because it is in a vocabulary list somewhere.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.world.narrative_tags import (
    ClueTag,
    GoalTag,
    NarrativeTagError,
    NarrativeTags,
    PersonalityTag,
    SocialTag,
)
from src.world.scenes import (
    DEFERRED_SCENE_KINDS,
    IMPLEMENTED_SCENE_KINDS,
    PROPOSED_SCENE_KINDS,
    SCENE_CONTRACTS,
    Scene,
    SceneError,
    validate_scene,
)


def clue(tag_id: str = "clue.ticket", **kwargs) -> ClueTag:
    base = {"register": "claimed", "source_ref": "doc.witness", "strength": "core"}
    base.update(kwargs)
    return ClueTag(tag_id, "A tram ticket timestamp", "case.1178", **base)


class TagFamiliesAreFour(unittest.TestCase):
    def test_the_four_families_validate(self) -> None:
        tags = NarrativeTags()
        tags.add(SocialTag("soc.owe", "Owes a favour", "faction.europol", relation="owe", valence=2))
        tags.add(GoalTag("goal.close", "Close the case", "pc.rookie", horizon="episode"))
        tags.add(clue())
        tags.add(PersonalityTag("per.rookie", "Procedural", "pc.rookie", trait="procedural"))
        self.assertEqual(
            {tag.kind for tag in tags.tags.values()},
            {"social", "goal", "clue", "personality"},
        )

    def test_tags_carry_no_rating(self) -> None:
        """A clue is a statement, not a modifier — the CWN core keeps the numbers."""
        self.assertFalse(hasattr(clue(), "rating"))
        self.assertFalse(hasattr(SocialTag("soc.x", "Member", "faction.a"), "rating"))


class Provenance(unittest.TestCase):
    def test_an_observed_clue_must_name_its_source(self) -> None:
        with self.assertRaises(NarrativeTagError):
            ClueTag("clue.x", "Un sourced", "case.1", register="observed")

    def test_a_claim_is_not_promoted_by_time_alone(self) -> None:
        tags = NarrativeTags()
        tags.add(clue())
        with self.assertRaises(NarrativeTagError):
            tags.verify("clue.ticket", authority="")
        self.assertEqual(tags.get("clue.ticket").register, "claimed")
        verified = tags.verify("clue.ticket", authority="scene.lab_report")
        self.assertEqual(verified.register, "observed")
        self.assertEqual(verified.source_ref, "scene.lab_report")

    def test_contradictions_must_resolve(self) -> None:
        tags = NarrativeTags()
        with self.assertRaises(NarrativeTagError):
            tags.add(clue("clue.a", contradicts=("clue.missing",)))
        tags.add(clue("clue.b"))
        tags.add(clue("clue.a", contradicts=("clue.b",)))
        self.assertEqual(tags.contradictions(), (("clue.a", "clue.b"),))

    def test_a_clue_cannot_contradict_itself(self) -> None:
        with self.assertRaises(NarrativeTagError):
            clue("clue.a", contradicts=("clue.a",))


class SceneContracts(unittest.TestCase):
    def test_five_kinds_are_implemented_and_astral_is_deferred(self) -> None:
        self.assertEqual(IMPLEMENTED_SCENE_KINDS, ("Social", "Investigation", "Exploration", "Action", "Cyber"))
        self.assertEqual(set(SCENE_CONTRACTS), set(IMPLEMENTED_SCENE_KINDS))
        self.assertEqual(DEFERRED_SCENE_KINDS, ("Astral",))

    def test_every_contract_names_cwn_material_and_refuses_a_minigame(self) -> None:
        for kind, contract in SCENE_CONTRACTS.items():
            self.assertTrue(contract.resolution, kind)
            self.assertTrue(contract.refuses.startswith("no"), kind)
            self.assertTrue(contract.core_rule, kind)
            self.assertIn("Astral", "".join(DEFERRED_SCENE_KINDS))

    def test_action_scenes_are_finnish_police_procedure(self) -> None:
        rule = SCENE_CONTRACTS["Action"].core_rule.lower()
        for word in ("arrest", "pursuit", "containment"):
            self.assertIn(word, rule)
        self.assertNotIn("tactical", rule)

    def test_investigation_never_gates_a_core_clue_behind_a_roll(self) -> None:
        rule = SCENE_CONTRACTS["Investigation"].core_rule
        self.assertIn("never gated behind a roll", rule)
        self.assertIn("no investigation-point economy", SCENE_CONTRACTS["Investigation"].refuses)


class SceneValidation(unittest.TestCase):
    def test_astral_and_proposed_kinds_are_refused(self) -> None:
        with self.assertRaises(SceneError):
            Scene("scene.x", "Astral", "Dream")
        for kind in PROPOSED_SCENE_KINDS:
            with self.assertRaises(SceneError):
                Scene("scene.y", kind, "Proposed")

    def test_social_scene_needs_a_social_or_personality_tag(self) -> None:
        tags = NarrativeTags()
        tags.add(clue())
        scene = Scene("scene.s", "Social", "Interview at Kurvi", tag_refs=("clue.ticket",))
        with self.assertRaises(SceneError):
            validate_scene(scene, tags=tags)
        tags.add(PersonalityTag("per.npc", "Guarded", "npc.driver", trait="guarded"))
        validate_scene(Scene("scene.s", "Social", "Interview", tag_refs=("per.npc",)), tags=tags)

    def test_investigation_scene_needs_a_core_clue(self) -> None:
        tags = NarrativeTags()
        tags.add(clue("clue.weak", strength="supporting"))
        with self.assertRaises(SceneError):
            validate_scene(Scene("scene.i", "Investigation", "Search", tag_refs=("clue.weak",)), tags=tags)
        tags.add(clue("clue.core"))
        validate_scene(Scene("scene.i", "Investigation", "Search", tag_refs=("clue.core",)), tags=tags)

    def test_action_scene_needs_a_location(self) -> None:
        tags = NarrativeTags()
        with self.assertRaises(SceneError):
            validate_scene(Scene("scene.a", "Action", "Chase"), tags=tags)
        validate_scene(
            Scene("scene.a", "Action", "Chase", location_refs=("loc.kurvi",)), tags=tags
        )

    def test_a_scene_cannot_cite_an_unknown_tag_twice_or_at_all(self) -> None:
        tags = NarrativeTags()
        tags.add(clue())
        with self.assertRaises(NarrativeTagError):
            validate_scene(Scene("scene.i", "Investigation", "Search", tag_refs=("clue.none",)), tags=tags)
        with self.assertRaises(SceneError):
            Scene("scene.i", "Investigation", "Search", tag_refs=("clue.ticket", "clue.ticket"))


if __name__ == "__main__":
    unittest.main()
