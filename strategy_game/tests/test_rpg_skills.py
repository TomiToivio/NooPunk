"""Executable contracts for the crossover's two skill layers and its five seats (#482).

Code only, per `AGENTS.md` and issue #271: these exercise behaviour -- the dice, the context that
selects a skill list, the refusals, the resource spends, the seat structure and the one-action turn --
and never whether a document says a particular thing.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_rpg_skills.py"
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from random import Random

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game.characters import Tag  # noqa: E402
from strategy_game.rpg.fate import Action, Character, ResourceError  # noqa: E402
from strategy_game.rpg.roster import (  # noqa: E402
    AGENT_SEAT_COUNT,
    RosterError,
    Seat,
    SeatKind,
    TurnLedger,
    default_seats,
)
from strategy_game.rpg.scene import Scene  # noqa: E402
from strategy_game.rpg.skills import (  # noqa: E402
    INDIVIDUAL_SKILL_NAMES,
    INDIVIDUAL_SKILLS,
    ActionContext,
    SkillLayerError,
    capabilities_of,
    check,
    individual_skill,
    require_capability,
    skill_names,
    specialist_supplement,
    validate_skill,
)

#: A stand-in strategic roster for the tests. The *proposal* lives in
#: ``strategy_game/data/strategic_skills.json``; these tests must not depend on its contents, because
#: that roster is awaiting author approval and may change without breaking the layer's contract.
TEST_ROSTER = {"fieldcraft": object(), "statecraft": object(), "warcraft": object()}


def sheet(**overrides: object) -> Character:
    base: dict[str, object] = {
        "id": "agent-1",
        "name": "Field Agent",
        "aspects": ["Local-Access Specialist"],
        "skills": {"COG": 3, "INT": 2, "REF": 1, "SAV": 2, "SOM": 1, "WIL": 0},
        "strategic_skills": {"fieldcraft": 2, "statecraft": 1},
        "refresh": 4,
        "fate_points": 4,
    }
    base.update(overrides)
    return Character(**base)  # type: ignore[arg-type]


class IndividualSkillTests(unittest.TestCase):
    def test_the_six_are_the_ones_the_issue_names_and_nothing_else(self) -> None:
        self.assertEqual(INDIVIDUAL_SKILL_NAMES, ("COG", "INT", "REF", "SAV", "SOM", "WIL"))
        self.assertEqual(
            [(s.key, s.name) for s in INDIVIDUAL_SKILLS],
            [("COG", "Cognition"), ("INT", "Intuition"), ("REF", "Reflexes"),
             ("SAV", "Savvy"), ("SOM", "Somatics"), ("WIL", "Willpower")],
        )

    def test_every_skill_carries_a_scope_not_only_a_name(self) -> None:
        for skill in INDIVIDUAL_SKILLS:
            self.assertTrue(skill.meaning.strip(), skill.key)

    def test_a_skill_is_found_by_abbreviation_or_by_name(self) -> None:
        self.assertIs(individual_skill("cog"), individual_skill("Cognition"))
        self.assertEqual(individual_skill("SOM").key, "SOM")
        with self.assertRaises(SkillLayerError):
            individual_skill("Somatics+")  # Somatics is one broad skill, not a specialisation

    def test_the_six_are_ratings_on_the_one_fate_ladder_not_a_second_layer(self) -> None:
        """Issue #482: used as Fate-rated skills, not percentile attributes and not an extra layer."""
        actor = sheet()
        for name in INDIVIDUAL_SKILL_NAMES:
            self.assertIsInstance(actor.skills[name], int)
        self.assertFalse(hasattr(actor, "aptitudes"), "a second attribute scale was reintroduced")


class ContextSelectionTests(unittest.TestCase):
    def test_each_context_reads_its_own_list(self) -> None:
        self.assertEqual(skill_names(ActionContext.INDIVIDUAL), INDIVIDUAL_SKILL_NAMES)
        self.assertEqual(skill_names(ActionContext.FACTION_AGENT), ())
        self.assertEqual(skill_names(ActionContext.FACTION_AGENT, strategic_roster=TEST_ROSTER),
                         ("fieldcraft", "statecraft", "warcraft"))

    def test_an_individual_action_may_not_read_a_strategic_skill(self) -> None:
        with self.assertRaises(SkillLayerError) as raised:
            validate_skill(ActionContext.INDIVIDUAL, "statecraft", strategic_roster=TEST_ROSTER)
        self.assertIn("faction-agent", str(raised.exception))

    def test_a_faction_mission_may_not_read_an_individual_skill(self) -> None:
        with self.assertRaises(SkillLayerError) as raised:
            validate_skill(ActionContext.FACTION_AGENT, "COG", strategic_roster=TEST_ROSTER)
        self.assertIn("individual skill", str(raised.exception))

    def test_a_faction_mission_with_no_roster_is_refused_as_pending(self) -> None:
        """The roster is a proposal: with nothing approved, nothing is checked and nothing is guessed."""
        with self.assertRaises(SkillLayerError) as raised:
            validate_skill(ActionContext.FACTION_AGENT, "statecraft")
        self.assertIn("not approved", str(raised.exception))

    def test_an_unknown_name_is_refused_rather_than_rated_at_zero(self) -> None:
        with self.assertRaises(SkillLayerError):
            validate_skill(ActionContext.INDIVIDUAL, "Burglary")
        with self.assertRaises(SkillLayerError):
            validate_skill(ActionContext.FACTION_AGENT, "nonsense", strategic_roster=TEST_ROSTER)

    def test_validation_returns_the_canonical_name(self) -> None:
        self.assertEqual(validate_skill(ActionContext.INDIVIDUAL, "cognition"), "COG")
        self.assertEqual(
            validate_skill(ActionContext.FACTION_AGENT, "statecraft", strategic_roster=TEST_ROSTER),
            "statecraft",
        )


class ContextResolutionTests(unittest.TestCase):
    def test_an_individual_check_reads_the_individual_rating(self) -> None:
        actor = sheet()
        result = check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 2, rng=Random(3))
        self.assertEqual(result.resolution.skill, 3)
        self.assertEqual(result.resolution.total - result.resolution.difficulty, result.resolution.shifts)

    def test_a_faction_check_reads_the_strategic_rating(self) -> None:
        actor = sheet()
        result = check(actor, ActionContext.FACTION_AGENT, Action.CREATE_ADVANTAGE, "fieldcraft", 1,
                       rng=Random(3), strategic_roster=TEST_ROSTER)
        self.assertEqual(result.resolution.skill, 2)

    def test_a_zero_rating_in_the_read_layer_is_zero_not_the_other_layer(self) -> None:
        """The namespaces are independent: a strong strategic rating buys nothing in a scene."""
        actor = sheet(skills={"COG": 0}, strategic_skills={"fieldcraft": 4})
        individual = check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 0, rng=Random(1))
        self.assertEqual(individual.resolution.skill, 0)
        strategic = check(actor, ActionContext.FACTION_AGENT, Action.OVERCOME, "fieldcraft", 0,
                          rng=Random(1), strategic_roster=TEST_ROSTER)
        self.assertEqual(strategic.resolution.skill, 4)

    def test_the_same_character_and_kernel_serve_both_layers(self) -> None:
        actor = sheet()
        individual = check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "SAV", 1, rng=Random(9))
        strategic = check(actor, ActionContext.FACTION_AGENT, Action.OVERCOME, "statecraft", 1,
                          rng=Random(9), strategic_roster=TEST_ROSTER)
        self.assertEqual(type(individual), type(strategic))
        self.assertEqual(individual.resolution.dice, strategic.resolution.dice)

    def test_every_action_resolves_in_both_contexts(self) -> None:
        actor = sheet()
        for action in Action:
            for context, skill, roster in (
                (ActionContext.INDIVIDUAL, "REF", None),
                (ActionContext.FACTION_AGENT, "fieldcraft", TEST_ROSTER),
            ):
                result = check(actor, context, action, skill, 1, rng=Random(4),
                               strategic_roster=roster)
                self.assertEqual(result.resolution.action, action)

    def test_an_invocation_spends_one_fate_point_and_adds_two(self) -> None:
        actor = sheet(fate_points=1)
        result = check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 1, rng=Random(2),
                       invoked_aspect="Local-Access Specialist")
        self.assertEqual(actor.fate_points, 0)
        bare = check(sheet(fate_points=1), ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 1,
                     rng=Random(2))
        self.assertEqual(result.resolution.total, bare.resolution.total + 2)

    def test_an_invocation_without_a_fate_point_is_refused(self) -> None:
        actor = sheet(fate_points=0)
        with self.assertRaises(ResourceError):
            check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 1, rng=Random(2),
                  invoked_aspect="Local-Access Specialist")

    def test_a_refused_skill_name_rolls_no_dice(self) -> None:
        actor = sheet()
        before = actor.fate_points
        with self.assertRaises(SkillLayerError):
            check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "statecraft", 1, rng=Random(2),
                  invoked_aspect="Local-Access Specialist", strategic_roster=TEST_ROSTER)
        self.assertEqual(actor.fate_points, before, "validation precedes any spend or roll")

    def test_seeded_checks_replay(self) -> None:
        first = check(sheet(), ActionContext.INDIVIDUAL, Action.OVERCOME, "INT", 2, rng=Random(11))
        second = check(sheet(), ActionContext.INDIVIDUAL, Action.OVERCOME, "INT", 2, rng=Random(11))
        self.assertEqual(first, second)


class RefreshAndStressTests(unittest.TestCase):
    def test_refresh_raises_the_balance_to_the_baseline(self) -> None:
        actor = sheet(fate_points=0, refresh=4)
        self.assertEqual(actor.refresh_to_baseline(), 4)

    def test_refresh_never_lowers_a_higher_balance(self) -> None:
        actor = sheet(fate_points=6, refresh=4)
        self.assertEqual(actor.refresh_to_baseline(), 6)

    def test_a_negative_refresh_is_refused(self) -> None:
        with self.assertRaises(ResourceError):
            sheet(refresh=-1)

    def test_strategic_ratings_are_validated_like_individual_ones(self) -> None:
        with self.assertRaises(ResourceError):
            sheet(strategic_skills={"fieldcraft": -2})


class SpecialistSupplementTests(unittest.TestCase):
    def test_a_narrow_speciality_rides_on_a_broad_skill_as_a_tag(self) -> None:
        actor = sheet(tags=(Tag("competence", "COG: forensic reconstruction"),))
        self.assertEqual(specialist_supplement(actor, "COG"), ("COG: forensic reconstruction",))
        self.assertEqual(specialist_supplement(actor, "SAV"), ())

    def test_a_stunt_naming_the_skill_is_reported_too(self) -> None:
        actor = sheet(stunts=["REF: off-hand shooting"])
        self.assertEqual(specialist_supplement(actor, "Reflexes"), ("REF: off-hand shooting",))

    def test_a_speciality_grants_no_bonus_by_itself(self) -> None:
        """A tag that moved a roll would be an unapproved mechanic; the supplement is a reading list."""
        plain = sheet()
        decorated = sheet(tags=(Tag("competence", "COG: forensic reconstruction"),),
                          stunts=["COG: read the room"])
        for seed in range(5):
            self.assertEqual(
                check(plain, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 2, rng=Random(seed)).resolution,
                check(decorated, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 2, rng=Random(seed)).resolution,
            )

    def test_a_speciality_does_not_become_a_seventh_skill(self) -> None:
        with self.assertRaises(SkillLayerError):
            validate_skill(ActionContext.INDIVIDUAL, "forensic reconstruction")


class SeatStructureTests(unittest.TestCase):
    def test_the_roster_is_one_leader_and_four_agents(self) -> None:
        seats = default_seats("leader-1", ("a1", "a2", "a3", "a4"))
        self.assertEqual(len(seats), 1 + AGENT_SEAT_COUNT)
        self.assertEqual(sum(seat.kind is SeatKind.LEADER for seat in seats), 1)
        self.assertEqual(sum(seat.kind is SeatKind.AGENT for seat in seats), AGENT_SEAT_COUNT)

    def test_every_seat_acts_for_the_faction_not_as_an_individual(self) -> None:
        for seat in default_seats("leader-1", ("a1", "a2", "a3", "a4")):
            self.assertIs(seat.context, ActionContext.FACTION_AGENT)

    def test_a_roster_of_another_size_is_an_author_decision_not_a_silent_one(self) -> None:
        for agents in ((), ("a1",), ("a1", "a2", "a3"), ("a1", "a2", "a3", "a4", "a5")):
            with self.assertRaises(RosterError):
                default_seats("leader-1", agents)

    def test_a_character_holds_one_seat(self) -> None:
        with self.assertRaises(RosterError):
            default_seats("a1", ("a1", "a2", "a3", "a4"))
        with self.assertRaises(RosterError):
            default_seats("leader-1", ("a1", "a1", "a3", "a4"))

    def test_a_leader_seat_needs_a_character(self) -> None:
        with self.assertRaises(RosterError):
            default_seats("  ", ("a1", "a2", "a3", "a4"))


class OneActionPerTurnTests(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = TurnLedger(default_seats("leader-1", ("a1", "a2", "a3", "a4")))

    def test_every_seat_starts_available(self) -> None:
        self.assertEqual(len(self.ledger.seats_available), 5)

    def test_a_seat_acts_once_and_is_then_spent(self) -> None:
        self.assertEqual(self.ledger.declare("agent_2", statement="investigate the testimony"), "a2")
        self.assertNotIn("agent_2", self.ledger.seats_available)
        with self.assertRaises(RosterError) as raised:
            self.ledger.declare("agent_2")
        self.assertIn("already acted", str(raised.exception))

    def test_the_leader_and_each_agent_act_independently(self) -> None:
        for seat in ("leader", "agent_1", "agent_2", "agent_3", "agent_4"):
            self.ledger.declare(seat)
        self.assertEqual(self.ledger.seats_available, ())
        with self.assertRaises(RosterError):
            self.ledger.declare("leader")

    def test_the_limit_is_per_character_not_per_seat(self) -> None:
        """Issue #482 words the limit per character, so two seats cannot double a character's turn."""
        seats = default_seats("leader-1", ("a1", "a2", "a3", "a4"))
        ledger = TurnLedger(seats + (Seat("extra", SeatKind.AGENT, "a1"),))
        ledger.declare("agent_1")
        with self.assertRaises(RosterError) as raised:
            ledger.declare("extra")
        self.assertIn("per character", str(raised.exception))

    def test_an_unknown_seat_is_refused(self) -> None:
        with self.assertRaises(RosterError):
            self.ledger.declare("agent_9")

    def test_the_next_turn_clears_the_ledger_and_keeps_the_seats(self) -> None:
        self.ledger.declare("leader")
        self.assertEqual(self.ledger.next_turn(), 1)
        self.assertEqual(len(self.ledger.seats_available), 5)
        self.assertEqual(self.ledger.declare("leader"), "leader-1")

    def test_seats_without_a_loaded_sheet_are_reported_not_invented(self) -> None:
        loaded = {"a1": sheet(id="a1", name="One")}
        self.assertEqual(self.ledger.characters_without_a_sheet(loaded), ("a2", "a3", "a4", "leader-1"))

    def test_a_ledger_needs_seats(self) -> None:
        with self.assertRaises(RosterError):
            TurnLedger(())


class CapabilityGateTests(unittest.TestCase):
    """#482 names capability gating by name: a gated move without the capability is refused."""

    def test_a_capability_reads_from_the_shared_competence_vocabulary(self) -> None:
        actor = sheet(tags=(Tag("competence", "netrunner"), Tag("belief", "the commons")))
        self.assertEqual(capabilities_of(actor), ("netrunner",))
        self.assertNotIn("the commons", capabilities_of(actor))

    def test_a_gated_action_without_the_capability_is_refused_before_any_dice(self) -> None:
        actor = sheet()
        before = actor.fate_points
        with self.assertRaises(SkillLayerError) as raised:
            check(actor, ActionContext.FACTION_AGENT, Action.OVERCOME, "fieldcraft", 2, rng=Random(3),
                  strategic_roster=TEST_ROSTER, required_capability="netrunner")
        self.assertIn("netrunner", str(raised.exception))
        self.assertEqual(actor.fate_points, before, "the gate precedes any spend")

    def test_the_same_action_proceeds_with_the_capability(self) -> None:
        actor = sheet(tags=(Tag("competence", "netrunner"),))
        result = check(actor, ActionContext.FACTION_AGENT, Action.OVERCOME, "fieldcraft", 2,
                       rng=Random(3), strategic_roster=TEST_ROSTER, required_capability="netrunner")
        self.assertEqual(result.resolution.skill, 2)

    def test_an_ungated_action_needs_no_capability(self) -> None:
        self.assertTrue(check(sheet(), ActionContext.INDIVIDUAL, Action.OVERCOME, "SAV", 1,
                              rng=Random(3)).resolution.succeeds is not None)

    def test_an_empty_gate_name_is_refused_rather_than_treated_as_ungated(self) -> None:
        with self.assertRaises(SkillLayerError):
            require_capability(sheet(), "   ")

    def test_a_capability_gate_does_not_read_a_belief_as_a_capability(self) -> None:
        actor = sheet(tags=(Tag("belief", "netrunner"),))
        with self.assertRaises(SkillLayerError):
            require_capability(actor, "netrunner")


class SceneFeatureTests(unittest.TestCase):
    """A context-checked action gets the approved kernel's scene features, not just its dice."""

    def test_a_tracked_scene_aspect_supplies_a_free_invocation(self) -> None:
        actor = sheet()
        scene = Scene()
        scene.create_aspect("Organised Witnesses", free_invocations=1)
        result = check(actor, ActionContext.FACTION_AGENT, Action.CREATE_ADVANTAGE, "statecraft", 1,
                       rng=Random(5), scene=scene, invoked_aspect="Organised Witnesses", free=True,
                       strategic_roster=TEST_ROSTER)
        self.assertTrue(result.free)
        self.assertEqual(scene.aspects["Organised Witnesses"].free_invocations, 0)
        self.assertEqual(actor.fate_points, 4, "a free invocation spends no Fate point")

    def test_a_reroll_is_available_and_recorded(self) -> None:
        actor = sheet()
        result = check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 1, rng=Random(8),
                       invoked_aspect="Local-Access Specialist", reroll=True)
        self.assertTrue(result.rerolled)
        self.assertEqual(actor.fate_points, 3)

    def test_a_denied_permission_raises_before_the_roll(self) -> None:
        actor = sheet()
        with self.assertRaises(ResourceError):
            check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "COG", 1, rng=Random(1),
                  permitted=False)

    def test_resolution_happens_against_the_actor_not_a_copy_of_the_sheet(self) -> None:
        """The invoker is the actor: stress marked by a scene must land on the real sheet."""
        actor = sheet()
        check(actor, ActionContext.INDIVIDUAL, Action.OVERCOME, "SOM", 1, rng=Random(2),
              invoked_aspect="Local-Access Specialist")
        self.assertEqual(actor.fate_points, 3)
        self.assertEqual(actor.physical_stress, [False, False])


class ProposedRosterDataTests(unittest.TestCase):
    """The roster in ``data/strategic_skills.json`` is a proposal, and it must behave like one."""

    def setUp(self) -> None:
        from strategy_game.strategic_skills import load_strategic_roster, mapping_rows
        self.roster = load_strategic_roster()
        self.rows = mapping_rows()

    def test_the_proposal_loads_and_carries_seven_skills(self) -> None:
        self.assertEqual(len(self.roster), 7)
        for skill in self.roster.values():
            self.assertTrue(skill.definition.strip(), skill.id)
            self.assertTrue(skill.mission_kinds, skill.id)

    def test_every_mapping_row_lands_on_a_proposed_skill(self) -> None:
        self.assertTrue(self.rows)
        for row in self.rows:
            self.assertIn(row.proposed, self.roster, row.source_skill)

    def test_the_proposal_says_it_is_a_proposal(self) -> None:
        """A file that stopped declaring itself a proposal would be claiming an approval it has not."""
        import json
        from pathlib import Path
        from strategy_game import strategic_skills
        data = json.loads(Path(strategic_skills.DATA_PATH).read_text(encoding="utf-8"))
        self.assertIn("PROPOSAL", str(data["status"]).upper())
        self.assertFalse(data["provenance"]["approved"])

    def test_the_proposed_roster_drives_a_faction_check(self) -> None:
        actor = sheet(strategic_skills={"statecraft": 3})
        result = check(actor, ActionContext.FACTION_AGENT, Action.OVERCOME, "statecraft", 1,
                       rng=Random(6), strategic_roster=self.roster)
        self.assertEqual(result.resolution.skill, 3)
        self.assertEqual(result.resolution.total - result.resolution.difficulty, result.resolution.shifts)

    def test_the_roster_still_refuses_an_individual_skill(self) -> None:
        with self.assertRaises(SkillLayerError):
            validate_skill(ActionContext.FACTION_AGENT, "COG", strategic_roster=self.roster)

    def test_the_reference_column_round_trips_and_is_shape_checked(self) -> None:
        """The reference column is loader-validated data, not prose: a bare string is refused."""
        import copy
        import json
        from pathlib import Path

        from strategy_game import strategic_skills
        from strategy_game.strategic_skills import StrategicRosterError, roster_from_dict

        for skill in self.roster.values():
            for name in skill.terra_invicta_missions:
                self.assertIsInstance(name, str)
                self.assertTrue(name.strip(), skill.id)
            self.assertIn("terra_invicta_missions", skill.to_dict())

        data = json.loads(Path(strategic_skills.DATA_PATH).read_text(encoding="utf-8"))
        broken = copy.deepcopy(data)
        broken["strategic_skills"][0]["terra_invicta_missions"] = "Control Nation"
        with self.assertRaises(StrategicRosterError):
            roster_from_dict(broken)

    def test_the_reference_model_records_what_was_verified_and_what_was_not(self) -> None:
        """A reference whose gaps are not recorded reads as though everything in it were checked."""
        import json
        from pathlib import Path

        from strategy_game import strategic_skills
        model = json.loads(Path(strategic_skills.DATA_PATH).read_text(encoding="utf-8"))["terra_invicta_model"]
        self.assertTrue(model["verified"])
        self.assertTrue(model["unverified"])
        self.assertTrue(model["not_reproduced"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
