"""#1261: the Astral Body MVP — state, perception filters, targeting eligibility.

The author update withdraws "no astral combat" and replaces it with a narrower claim: the Astral Body
has presence, can be attacked and can attack, while the body stays put. These tests pin the parts that
are structural. They deliberately do **not** test an astral damage bridge, because that bridge is not
approved and must not exist yet.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.world.scenes import SceneFrame, SceneError, run_astral_scene  # noqa: E402
from src.rules.astral_body import (  # noqa: E402
    ASTRAL_DAMAGE_BRIDGE_APPROVED,
    AstralBodyError,
    Combatant,
    Embodiment,
    EntryTrigger,
    PerceptionMode,
    Projection,
    TargetKind,
    apply_astral_damage,
    astral_can_target,
    begin_projection,
    can_perceive,
    detect_by_esp,
    physical_can_target,
    requires_authored_transition,
    unlocked_disciplines,
)


def projection(**kw) -> Projection:
    base = dict(actor_id="tony.german", body_location="loc.sornainen_home",
                trigger=EntryTrigger.SLEEP)
    base.update(kw)
    return begin_projection(**base)


class EntryTests(unittest.TestCase):
    def test_only_scripted_triggers_start_a_projection(self):
        for trigger in ("sleep", "nde", "psychotronic", "authored"):
            self.assertEqual(begin_projection("a", "loc.x", trigger).trigger.value, trigger)

    def test_projection_at_will_is_not_a_trigger(self):
        with self.assertRaises(AstralBodyError) as caught:
            begin_projection("a", "loc.x", "will")
        self.assertIn("scene-triggered", str(caught.exception))

    def test_a_projection_needs_a_body_location(self):
        with self.assertRaises(AstralBodyError):
            begin_projection("a", "  ", "sleep")


class IdentityTests(unittest.TestCase):
    def test_the_physical_body_does_not_move(self):
        p = projection(astral_location="astral.stair")
        p.shift_mode(PerceptionMode.TIME_SPACE, authored=True)
        self.assertEqual(p.body_location, "loc.sornainen_home")

    def test_returning_restores_the_embodied_state(self):
        p = projection()
        self.assertEqual(p.embodiment, Embodiment.PROJECTED)
        p.return_to_body()
        self.assertEqual(p.embodiment, Embodiment.RETURNED)
        self.assertEqual(p.body_location, "loc.sornainen_home")

    def test_returning_twice_changes_nothing(self):
        p = projection()
        p.return_to_body()
        p.return_to_body()
        self.assertEqual(p.embodiment, Embodiment.RETURNED)

    def test_one_actor_one_projection(self):
        p = projection()
        self.assertEqual(p.actor_id, "tony.german")


class PerceptionTests(unittest.TestCase):
    def test_embodied_perception_sees_the_physical_world(self):
        self.assertTrue(can_perceive(Embodiment.EMBODIED, None, TargetKind.PHYSICAL))
        self.assertFalse(can_perceive(Embodiment.EMBODIED, None, TargetKind.ASTRAL_AGENT))

    def test_near_physical_astral_sight_is_fallible(self):
        seen = projection().sees(TargetKind.PHYSICAL)
        self.assertTrue(seen.allowed)
        self.assertFalse(seen.reliable, "near-physical astral representation is not line of sight")

    def test_time_space_denies_direct_physical_observation(self):
        p = projection(astral_location="astral.symbolic_corridor")
        p.shift_mode(PerceptionMode.TIME_SPACE, authored=True)
        self.assertFalse(p.sees(TargetKind.PHYSICAL))

    def test_time_space_still_perceives_agents_and_symbols(self):
        p = projection(astral_location="astral.symbolic_corridor")
        p.shift_mode(PerceptionMode.TIME_SPACE, authored=True)
        self.assertTrue(p.sees(TargetKind.ASTRAL_AGENT))
        self.assertTrue(p.sees(TargetKind.SYMBOL))

    def test_a_returned_projector_sees_no_astral_agents(self):
        p = projection()
        p.return_to_body()
        self.assertFalse(p.sees(TargetKind.ASTRAL_AGENT))


class ActionRightsTests(unittest.TestCase):
    def test_a_projector_cannot_take_an_ordinary_physical_action(self):
        self.assertFalse(projection().may_take_physical_action())

    def test_the_returned_actor_can_act_physically_again(self):
        p = projection()
        p.return_to_body()
        self.assertTrue(p.may_take_physical_action())

    def test_a_projected_body_cannot_speak_to_material_witnesses(self):
        self.assertFalse(projection().may_speak_to_material())


class ModeTests(unittest.TestCase):
    def test_switching_mode_needs_an_authored_transition(self):
        p = projection(astral_location="astral.stair")
        with self.assertRaises(AstralBodyError):
            p.shift_mode(PerceptionMode.TIME_SPACE)
        p.shift_mode(PerceptionMode.TIME_SPACE, authored=True)
        self.assertEqual(p.mode, PerceptionMode.TIME_SPACE)

    def test_the_two_modes_are_different_modes(self):
        self.assertTrue(requires_authored_transition(PerceptionMode.SPACE_TIME,
                                                      PerceptionMode.TIME_SPACE))
        self.assertFalse(requires_authored_transition(PerceptionMode.SPACE_TIME,
                                                       PerceptionMode.SPACE_TIME))

    def test_time_space_does_not_accept_a_physical_coordinate_as_its_location(self):
        with self.assertRaises(AstralBodyError):
            begin_projection("a", "loc.sornainen_home", "sleep",
                             mode=PerceptionMode.TIME_SPACE,
                             astral_location="loc.sornainen_home")


class TargetingTests(unittest.TestCase):
    def test_astral_attack_requires_both_parties_astrally_present(self):
        p = projection()
        self.assertTrue(astral_can_target(p, Combatant("npc.predator", physically_present=False,
                                                        astrally_present=True)))
        self.assertFalse(astral_can_target(p, Combatant("npc.sleeper", physically_present=True)))

    def test_an_embodied_actor_cannot_make_an_astral_attack(self):
        p = projection()
        p.return_to_body()
        with self.assertRaises(AstralBodyError):
            astral_can_target(p, Combatant("npc.x", False, True))

    def test_a_hidden_projection_cannot_be_shot(self):
        target = Combatant("tony.german", physically_present=False, astrally_present=True)
        self.assertFalse(physical_can_target(True, target))

    def test_a_visible_apparition_is_still_not_tangible(self):
        target = Combatant("tony.german", physically_present=False, astrally_present=True,
                           manifestation="visible")
        allowed = physical_can_target(True, target)
        self.assertFalse(allowed)
        self.assertIn("not tangible", allowed.reason)

    def test_an_ordinary_person_can_still_be_shot(self):
        target = Combatant("npc.suspect", physically_present=True)
        self.assertTrue(physical_can_target(True, target))

    def test_esp_may_reveal_a_projector(self):
        p = projection()
        self.assertTrue(detect_by_esp(True, p))
        self.assertFalse(detect_by_esp(False, p))

    def test_manifestation_is_a_channel_choice(self):
        p = projection()
        p.manifest()
        self.assertEqual(p.manifestation, "visible")
        with self.assertRaises(AstralBodyError):
            p.manifest(channel="smell")


class NotYetImplementedTests(unittest.TestCase):
    def test_the_astral_damage_bridge_is_not_approved(self):
        self.assertFalse(ASTRAL_DAMAGE_BRIDGE_APPROVED)

    def test_astral_damage_refuses_to_invent_a_health_rule(self):
        with self.assertRaises(AstralBodyError) as caught:
            apply_astral_damage("tony.german", 3)
        self.assertIn("not approved", str(caught.exception))

    def test_a_projection_grants_no_discipline(self):
        self.assertEqual(unlocked_disciplines(projection()), ())

    def test_memories_and_interpretations_are_recorded_separately(self):
        p = projection()
        p.record("a figure stood at the foot of the bed", "I think it was my father")
        self.assertEqual(len(p.memories), 1)
        self.assertEqual(len(p.interpretations), 1)

    def test_a_returned_projector_cannot_add_new_astral_memories(self):
        p = projection()
        p.return_to_body()
        with self.assertRaises(AstralBodyError):
            p.record("something else")


class AstralSceneTests(unittest.TestCase):
    """An astral scene runs without an Astral graph — the MVP #1261 asks for."""

    def setUp(self) -> None:
        self.frame = SceneFrame(id="scene.oobe", title="Out of body", scene_type="Astral")

    def test_the_scene_runs_and_says_it_is_not_a_map(self):
        result = run_astral_scene(self.frame, projection(), facts=("the room is both right and wrong",))
        self.assertTrue(result.passed)
        self.assertTrue(any("non-navigable" in note for note in result.notes))
        self.assertIn("the room is both right and wrong", result.facts)

    def test_a_returned_projector_has_no_astral_scene(self):
        p = projection()
        p.return_to_body()
        with self.assertRaises(SceneError):
            run_astral_scene(self.frame, p)

    def test_time_space_refuses_a_physical_observation(self):
        p = projection(astral_location="astral.symbolic_corridor")
        p.shift_mode(PerceptionMode.TIME_SPACE, authored=True)
        result = run_astral_scene(self.frame, p, observes_physical=True)
        self.assertFalse(result.passed)
        self.assertIn("physical observation is unavailable", result.notes[0])

    def test_space_time_allows_a_fallible_observation(self):
        result = run_astral_scene(self.frame, projection(), observes_physical=True)
        self.assertTrue(result.passed)
        self.assertTrue(any("fallible" in fact for fact in result.facts))

    def test_a_dream_is_witnessed_without_its_source_being_revealed(self):
        result = run_astral_scene(self.frame, projection(), dream_of="npc.harri")
        self.assertTrue(any("source stays unstated" in note for note in result.notes))

    def test_the_wrong_scene_type_is_refused(self):
        social = SceneFrame(id="scene.chat", title="Chat", scene_type="Social")
        with self.assertRaises(SceneError):
            run_astral_scene(social, projection())


class DocsTests(unittest.TestCase):
    def test_the_astral_tabletop_procedure_exists(self):
        doc = ROOT / "docs/tabletop/ASTRAL_1261.md"
        text = doc.read_text(encoding="utf-8")
        self.assertIn("perception contract", text.lower())
        self.assertIn("NONCANONICAL", text)
        self.assertIn("AWAITING APPROVAL", text)

    def test_the_corporation_note_exists_and_marks_its_undecided_questions(self):
        text = (ROOT / "docs/world/PSI_CORPORATIONS_1261.md").read_text(encoding="utf-8")
        self.assertIn("Mannerheim–Yamamoto", text)
        self.assertIn("author decision", text)
        self.assertIn("TBD", text)


if __name__ == "__main__":
    unittest.main()
