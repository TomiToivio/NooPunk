"""Executable contracts for the shared strategic-project engine and its research instance (#506).

Code only, per ``AGENTS.md`` and issue #271: these exercise the engine's behaviour — the clock, the
capacity ledger, the one Fate kernel the check goes through, the refusals, the completion writes and
the save/load round trip — and never whether a document says a particular thing.

Run:
    python -m unittest discover -s strategy_game/tests -p "test_research_projects.py"
"""
from __future__ import annotations

import io
import json
import random
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from random import Random
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from strategy_game.campaign import (
    Campaign,
    CampaignError,
    CampaignFaction,
    load_campaign,
    save_campaign,
)
from strategy_game.campaign.state import campaign_from_dict
from strategy_game.projects import (
    TUNING_CLOCK_BASE_SEGMENTS,
    TUNING_CLOCK_MAX_SEGMENTS,
    TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY,
    TUNING_STYLE_BONUS_SEGMENTS,
    Allocation,
    FactionCapacity,
    Prerequisites,
    ProgressCause,
    ProjectClock,
    ProjectError,
    ProjectResult,
    ProjectStage,
    StrategicProject,
    advance_project,
    clock_for_difficulty,
    complete_project,
    pause_project,
    project_from_dict,
    reassign_project,
    resume_project,
    unsatisfied_prerequisites,
)
from strategy_game.research import (
    RESEARCH_LEAD_SKILL,
    RESEARCH_PROJECT_KINDS,
    RESEARCH_RESOURCE_KIND,
    Capability,
    ResearchProject,
    ResearchYield,
    TechNode,
    capability_from_dict,
    complete_research,
    prohibitions_for,
    research_project_from_dict,
    rpg_options,
)
from strategy_game.research_slice import (
    ARCHIVE_ID,
    ARTEFACT_ID,
    CASE_ID,
    CLUE_ID,
    DEMO_SEED,
    EQUIPMENT_ID,
    FACTION_ID,
    LAB_ID,
    LEADER_ID,
    NODE_MANUFACTURE,
    NODE_UNDERSTANDING,
    OPTION_ID,
    PROJECT_ARCHIVE,
    PROJECT_ARTEFACT,
    PROJECT_TRANSFER,
    archive_access_project,
    build_campaign,
    declared_nodes,
    main,
    reverse_engineering_project,
    run_demo,
    technology_transfer_project,
)
from strategy_game.rpg.skills import (
    ActionContext,
    SkillLayerError,
    validate_skill,
)
from strategy_game.strategic_skills import load_strategic_roster


def roster() -> dict[str, object]:
    """The proposal roster, loaded exactly as the game loads it."""
    return dict(load_strategic_roster())


def fixture() -> Campaign:
    """The slice's noncanonical fixture campaign: one leader, four agents, one case, one ledger."""
    return build_campaign()


def ledger(campaign: Campaign) -> FactionCapacity:
    return campaign.capacities[FACTION_ID]


def add(campaign: Campaign, project: StrategicProject) -> Campaign:
    """Declare a project on the campaign and return the campaign, so calls chain."""
    campaign.projects[project.project_id] = project
    return campaign


def guaranteed_project(
    campaign: Campaign,
    *,
    project_id: str = "p-guaranteed",
    lead_id: str = "a-1",
    work: int = 12,
    difficulty: int = 1,
    stage: ProjectStage = ProjectStage.UNDERSTANDING,
    node_id: str = "",
) -> ResearchProject:
    """A project whose lead's SCIENCE check **cannot fail**.

    ``skill - difficulty = 5`` is the threshold at which even the worst four Fate dice still leave
    positive shifts, so the check is out of the way and a test can isolate what the **capacity** does.
    It is a fixture, not a balance claim: no character in play is rated this way.
    """
    campaign.sheets[lead_id].strategic_skills[RESEARCH_LEAD_SKILL] = 6 + difficulty - 1
    return ResearchProject(
        project_id=project_id,
        faction_id=FACTION_ID,
        title="A programme whose lead cannot fail",
        kind="basic_science",
        lead_id=lead_id,
        lead_skill=RESEARCH_LEAD_SKILL,
        lead_difficulty=difficulty,
        clock=ProjectClock(work),
        resource_kind=RESEARCH_RESOURCE_KIND,
        stage=stage,
        node_id=node_id,
        domain_tags=("Engineering",),
    )


def ready_project(
    *, project_id: str = "p-guaranteed", work: int = 12, difficulty: int = 1, held: bool = True
) -> tuple[Campaign, ResearchProject]:
    """A fixture campaign with one cannot-fail project, its artefact in hand, nothing committed."""
    campaign = fixture()
    project = guaranteed_project(campaign, project_id=project_id, work=work, difficulty=difficulty)
    add(campaign, project)
    if held:
        campaign.faction().resources.append(ARTEFACT_ID)
    return campaign, project


class ProjectClockTests(unittest.TestCase):
    def test_work_can_only_be_added_and_never_removed(self) -> None:
        clock = ProjectClock(10)
        self.assertEqual(clock.add(4), 4)
        self.assertEqual(clock.filled, 4)
        with self.assertRaises(ProjectError):
            clock.add(-1)
        self.assertEqual(clock.filled, 4)

    def test_a_clock_never_fills_past_its_total(self) -> None:
        clock = ProjectClock(5)
        self.assertEqual(clock.add(9), 5)
        self.assertTrue(clock.is_complete)
        self.assertEqual(clock.remaining, 0)
        self.assertEqual(clock.add(3), 0)

    def test_a_corrupt_snapshot_is_refused_rather_than_clamped(self) -> None:
        with self.assertRaises(ProjectError):
            ProjectClock.from_dict({"work_required": 4, "filled": 5})
        with self.assertRaises(ProjectError):
            ProjectClock.from_dict({"work_required": 0, "filled": 0})

    def test_the_clock_round_trips(self) -> None:
        clock = ProjectClock(12, 7)
        self.assertEqual(ProjectClock.from_dict(clock.to_dict()), clock)
        self.assertEqual(ProjectClock.from_dict(json.loads(json.dumps(clock.to_dict()))), clock)

    def test_difficulty_defines_the_total_work_and_the_total_stays_finite(self) -> None:
        segments = [clock_for_difficulty(d).work_required for d in range(20)]
        self.assertEqual(segments, sorted(segments))  # harder never means less work
        self.assertTrue(all(s >= 1 for s in segments))
        self.assertLessEqual(max(segments), TUNING_CLOCK_MAX_SEGMENTS)
        self.assertEqual(
            clock_for_difficulty(1).work_required,
            TUNING_CLOCK_BASE_SEGMENTS + TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY,
        )
        self.assertEqual(clock_for_difficulty(2).work_required, 12)  # issue #506's own example
        with self.assertRaises(ProjectError):
            clock_for_difficulty(-1)

    def test_the_tuning_constants_are_named_as_tuning_and_not_as_canon(self) -> None:
        module = sys.modules[ProjectClock.__module__]
        for name in (
            "TUNING_CLOCK_BASE_SEGMENTS",
            "TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY",
            "TUNING_CLOCK_MAX_SEGMENTS",
            "TUNING_STYLE_BONUS_SEGMENTS",
        ):
            self.assertTrue(hasattr(module, name), name)
        self.assertEqual(TUNING_STYLE_BONUS_SEGMENTS, 1)


class FactionCapacityTests(unittest.TestCase):
    def test_allocation_is_a_membership_change_that_can_be_replaced_and_released(self) -> None:
        book = FactionCapacity("f", {"research": 4})
        book.allocate("p-1", "research", 3)
        self.assertEqual(book.allocated("p-1"), 3)
        self.assertEqual(book.free("research"), 1)
        book.allocate("p-1", "research", 1)  # replaced, not added
        self.assertEqual(book.allocated("p-1"), 1)
        self.assertEqual(book.release("p-1"), 1)
        self.assertEqual(book.allocated("p-1"), 0)
        self.assertEqual(book.free("research"), 4)

    def test_an_over_commitment_is_refused_and_the_shortage_is_visible(self) -> None:
        book = FactionCapacity("f", {"research": 3})
        book.allocate("p-1", "research", 3)
        with self.assertRaises(ProjectError):
            book.allocate("p-2", "research", 2)
        self.assertEqual(book.free("research"), 0)
        self.assertEqual(book.allocated("p-2"), 0)  # the refused allocation did not half-apply

    def test_a_ledger_may_not_be_built_already_over_committed(self) -> None:
        with self.assertRaises(ProjectError):
            FactionCapacity("f", {"research": 1}, [Allocation("p-1", "research", 2)])
        with self.assertRaises(ProjectError):
            FactionCapacity(
                "f", {"research": 1},
                [Allocation("p-1", "research", 1), Allocation("p-1", "research", 1)],
            )

    def test_a_ledger_names_its_faction_and_needs_one(self) -> None:
        with self.assertRaises(ProjectError):
            FactionCapacity("")
        with self.assertRaises(ProjectError):
            FactionCapacity("f", {"research": -1})

    def test_the_ledger_round_trips(self) -> None:
        book = FactionCapacity("f", {"research": 4, "personnel": 2}, [Allocation("p", "research", 3)])
        payload = json.loads(json.dumps(book.to_dict()))
        self.assertEqual(FactionCapacity.from_dict(payload), book)


class KernelIntegrationTests(unittest.TestCase):
    """The project check is the one Fate kernel's faction-agent check. There is no second engine."""

    def test_the_check_is_a_faction_agent_check_and_needs_the_proposed_roster(self) -> None:
        campaign, _ = ready_project()
        with self.assertRaises(SkillLayerError) as caught:
            advance_project(campaign, "p-guaranteed", rng=Random(1), turn=1)
        self.assertIn("roster", str(caught.exception))
        result = advance_project(campaign, "p-guaranteed", rng=Random(1), turn=1, roster=roster())
        self.assertIsNotNone(result.outcome)

    def test_a_project_naming_an_individual_skill_is_refused_before_any_dice(self) -> None:
        campaign = fixture()
        project = StrategicProject(
            project_id="p-individual",
            faction_id=FACTION_ID,
            title="A task declared on the wrong layer",
            kind="organize",
            lead_id="a-2",
            lead_skill="COG",
            lead_difficulty=1,
            clock=ProjectClock(4),
            resource_kind="personnel",
            stage=ProjectStage.DEPLOYMENT,
        )
        add(campaign, project)
        ledger(campaign).allocate("p-individual", "personnel", 2)
        rng = Random(3)
        before = rng.getstate()
        with self.assertRaises(SkillLayerError):
            advance_project(campaign, "p-individual", rng=rng, turn=1, roster=roster())
        self.assertEqual(rng.getstate(), before)  # refused before any dice
        self.assertEqual(project.clock.filled, 0)

    def test_the_proposal_roster_is_used_as_a_proposal_and_not_promoted(self) -> None:
        proposed = roster()
        self.assertIn(RESEARCH_LEAD_SKILL, proposed)
        self.assertEqual(
            validate_skill(ActionContext.FACTION_AGENT, RESEARCH_LEAD_SKILL,
                           strategic_roster=proposed),
            RESEARCH_LEAD_SKILL,
        )
        with self.assertRaises(SkillLayerError):
            validate_skill(ActionContext.FACTION_AGENT, RESEARCH_LEAD_SKILL)

    def test_the_capability_gate_refuses_the_mission_before_any_dice(self) -> None:
        campaign, project = ready_project()
        project.required_capability = "netrunner"
        rng = Random(5)
        before = rng.getstate()
        with self.assertRaises(SkillLayerError) as caught:
            advance_project(campaign, "p-guaranteed", rng=rng, turn=1, roster=roster())
        self.assertIn("netrunner", str(caught.exception))
        self.assertEqual(rng.getstate(), before)
        self.assertEqual(project.clock.filled, 0)

    def test_domain_tags_are_reported_and_never_rated(self) -> None:
        """A matched domain TAG is visible and moves nothing: no bonus, no penalty."""
        campaign, project = ready_project()
        project.domain_tags = ("Engineering", "Forensics", "Parapsychology")
        result = advance_project(campaign, "p-guaranteed", rng=Random(9), turn=1, roster=roster())
        self.assertEqual(result.domain_tags_matched, ("Engineering", "Parapsychology"))
        self.assertEqual(result.domain_tags_missing, ("Forensics",))

        other_campaign, other_project = ready_project()
        other_project.domain_tags = ("Engineering", "Forensics", "Parapsychology")
        plain = advance_project(other_campaign, "p-guaranteed", rng=Random(9), turn=1, roster=roster())
        self.assertEqual(result.progress_added, plain.progress_added)
        self.assertEqual(result.outcome, plain.outcome)


class AdvanceProjectTests(unittest.TestCase):
    def test_a_failed_check_yields_zero_progress(self) -> None:
        """The issue's first acceptance criterion, on a check that cannot succeed."""
        campaign, _ = ready_project(difficulty=12)
        ledger(campaign).allocate("p-guaranteed", RESEARCH_RESOURCE_KIND, 3)
        # the rating the fixture helper installed would clear difficulty 12; this lead cannot
        campaign.sheets["a-1"].strategic_skills[RESEARCH_LEAD_SKILL] = 2
        result = advance_project(campaign, "p-guaranteed", rng=Random(4), turn=1, roster=roster())
        self.assertIs(result.cause, ProgressCause.CHECK_FAILED)
        self.assertEqual(result.progress_added, 0)
        self.assertEqual(result.filled, 0)
        self.assertFalse(result.completed)
        self.assertIsNotNone(result.outcome)
        assert result.outcome is not None  # narrowed for the reader and the type checker
        self.assertEqual(result.outcome.value, "failure")
        self.assertIn("preserved", result.notes[0])

    def test_a_tie_takes_no_segments_and_says_why(self) -> None:
        seen: set[str] = set()
        for seed in range(80):
            campaign, _ = ready_project(project_id="p-tie", difficulty=5)
            # science 4 against difficulty 5: shifts are the dice sum minus one, so a tie is reachable
            campaign.sheets["a-1"].strategic_skills[RESEARCH_LEAD_SKILL] = 4
            ledger(campaign).allocate("p-tie", RESEARCH_RESOURCE_KIND, 3)
            result = advance_project(campaign, "p-tie", rng=Random(seed), turn=1, roster=roster())
            seen.add(result.cause.value)
            if result.cause is ProgressCause.TIE:
                self.assertEqual(result.progress_added, 0)
                self.assertIn("minor cost", result.notes[0])
                self.assertEqual(result.throughput, 3)  # committed, and still worth nothing
                return
        self.fail(f"no tie in eighty seeds; causes seen: {sorted(seen)}")

    def test_a_successful_turn_adds_exactly_the_committed_capacity(self) -> None:
        for seed in range(120):
            campaign, _ = ready_project()
            ledger(campaign).allocate("p-guaranteed", RESEARCH_RESOURCE_KIND, 3)
            result = advance_project(campaign, "p-guaranteed", rng=Random(seed), turn=1, roster=roster())
            if result.outcome is not None and result.outcome.value == "success":
                self.assertEqual(result.progress_added, 3)
                self.assertEqual(result.throughput, 3)
                return
        self.fail("no plain success in one hundred and twenty seeds")

    def test_progress_scales_with_allocated_faction_capacity(self) -> None:
        """Institutional resources decide the scale: the same dice, less capacity, more turns."""

        def turns_at(capacity: int) -> int:
            campaign, _ = ready_project(project_id=f"p-{capacity}")
            ledger(campaign).allocate(f"p-{capacity}", RESEARCH_RESOURCE_KIND, capacity)
            rng = Random(42)  # the same dice sequence at every capacity
            for turn in range(1, 40):
                advance_project(campaign, f"p-{capacity}", rng=rng, turn=turn, roster=roster())
                if campaign.projects[f"p-{capacity}"].clock.is_complete:
                    return turn
            self.fail("the clock never filled")

        one, two, three = turns_at(1), turns_at(2), turns_at(3)
        # twelve segments, and a style success is worth exactly one more than the commitment
        self.assertTrue(3 <= three <= 4, three)
        self.assertTrue(4 <= two <= 6, two)
        self.assertTrue(6 <= one <= 12, one)
        self.assertLessEqual(three, two)
        self.assertLessEqual(two, one)
        self.assertLess(three, one)

    def test_a_difficulty_defined_clock_completes_in_three_to_five_turns(self) -> None:
        """The issue's 3-5 turn clock, at the capacity the slice commits."""
        campaign = add(fixture(), reverse_engineering_project())
        campaign.faction().resources.append(ARTEFACT_ID)
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        self.assertEqual(campaign.projects[PROJECT_ARTEFACT].clock.work_required, 12)
        rng = Random(2024)
        for turn in range(1, 20):
            advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=turn, roster=roster())
            if campaign.projects[PROJECT_ARTEFACT].clock.is_complete:
                self.assertTrue(3 <= turn <= 5, turn)
                return
        self.fail("the clock never filled")

    def test_a_success_with_nothing_committed_advances_nothing(self) -> None:
        campaign, _ = ready_project()
        result = advance_project(campaign, "p-guaranteed", rng=Random(2), turn=1, roster=roster())
        self.assertIs(result.cause, ProgressCause.NO_CAPACITY)
        self.assertEqual(result.progress_added, 0)
        self.assertEqual(result.outcome.value, "success")
        self.assertIn("institutional resources", result.notes[0])

    def test_the_style_bonus_never_replaces_institutional_capacity(self) -> None:
        """A special success with no committed resource is still zero work."""
        for seed in range(140):
            campaign, _ = ready_project()
            result = advance_project(campaign, "p-guaranteed", rng=Random(seed), turn=1, roster=roster())
            if result.outcome is not None and result.outcome.value == "success_with_style":
                self.assertIs(result.cause, ProgressCause.NO_CAPACITY)
                self.assertEqual(result.progress_added, 0)
                return
        self.fail("no success with style in one hundred and forty seeds")

    def test_the_style_bonus_is_one_segment_on_top_of_the_commitment(self) -> None:
        for seed in range(120):
            campaign, _ = ready_project(project_id="p-style", work=20)
            ledger(campaign).allocate("p-style", RESEARCH_RESOURCE_KIND, 3)
            result = advance_project(campaign, "p-style", rng=Random(seed), turn=1, roster=roster())
            if result.outcome is not None and result.outcome.value == "success_with_style":
                self.assertEqual(result.progress_added, 3 + TUNING_STYLE_BONUS_SEGMENTS)
                self.assertEqual(result.throughput, 3)
                return
        self.fail("no success with style in one hundred and twenty seeds")

    def test_no_progress_is_ever_lost_across_a_run(self) -> None:
        """Monotone by construction: the clock only ever fills, and only a pass fills it."""
        campaign = add(fixture(), reverse_engineering_project())
        campaign.faction().resources.append(ARTEFACT_ID)
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 2)
        filled = 0
        rng = Random(17)
        for turn in range(1, 9):
            result = advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=turn, roster=roster())
            self.assertGreaterEqual(result.filled, filled)
            self.assertEqual(result.progress_added, result.filled - filled)
            if result.cause not in (ProgressCause.ADVANCED, ProgressCause.COMPLETED):
                self.assertEqual(result.progress_added, 0)
            filled = result.filled
        self.assertEqual(campaign.projects[PROJECT_ARTEFACT].clock.filled, filled)
        self.assertGreater(filled, 0)
        self.assertEqual(campaign.projects[PROJECT_ARTEFACT].history[-1]["filled"], filled)

    def test_completion_is_idempotent_and_rolls_no_dice_again(self) -> None:
        campaign, project = ready_project(work=4)
        ledger(campaign).allocate("p-guaranteed", RESEARCH_RESOURCE_KIND, 4)
        advance_project(campaign, "p-guaranteed", rng=Random(8), turn=1, roster=roster())
        self.assertTrue(project.clock.is_complete)
        filled = project.clock.filled
        log = list(project.history)
        notes = len(campaign.campaign_notes)

        rng = Random(11)
        before = rng.getstate()
        repeat = advance_project(campaign, "p-guaranteed", rng=rng, turn=2, roster=roster())
        self.assertIs(repeat.cause, ProgressCause.ALREADY_COMPLETE)
        self.assertEqual(repeat.progress_added, 0)
        self.assertEqual(repeat.filled, filled)
        self.assertIsNone(repeat.outcome)
        self.assertEqual(rng.getstate(), before)  # a closed programme rolls nothing
        self.assertEqual(project.history, log)  # and its log is closed
        self.assertEqual(len(campaign.campaign_notes), notes)

    def test_an_unstarted_project_without_its_prerequisite_is_refused(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        self.assertEqual(
            unsatisfied_prerequisites(campaign, campaign.projects[PROJECT_ARTEFACT]),
            (ARTEFACT_ID,),
        )
        with self.assertRaises(ProjectError) as caught:
            advance_project(campaign, PROJECT_ARTEFACT, rng=Random(1), turn=1, roster=roster())
        self.assertIn(ARTEFACT_ID, str(caught.exception))
        self.assertEqual(campaign.projects[PROJECT_ARTEFACT].clock.filled, 0)
        self.assertFalse(campaign.projects[PROJECT_ARTEFACT].paused)

    def test_prerequisites_are_read_from_the_books_that_already_hold_them(self) -> None:
        """A resource id, a completed node: the two kinds, and nothing else."""
        campaign, project = ready_project()
        project.requires = Prerequisites(resource_ids=(ARTEFACT_ID,), node_ids=(NODE_UNDERSTANDING,))
        self.assertEqual(unsatisfied_prerequisites(campaign, project), (NODE_UNDERSTANDING,))
        campaign.capabilities[NODE_UNDERSTANDING] = declared_nodes()[NODE_UNDERSTANDING]
        self.assertEqual(unsatisfied_prerequisites(campaign, project), ())
        self.assertEqual(campaign.structural_problems(), ())

    def test_a_lost_prerequisite_interrupts_the_project_and_resuming_continues_it(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        campaign.faction().resources.append(ARTEFACT_ID)
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        rng = Random(3)
        advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=1, roster=roster())
        held = campaign.projects[PROJECT_ARTEFACT].clock.filled
        self.assertGreater(held, 0)

        campaign.faction().resources.remove(ARTEFACT_ID)  # the specimen is reclaimed
        interrupted = advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=2, roster=roster())
        self.assertIs(interrupted.cause, ProgressCause.PAUSED)
        self.assertEqual(interrupted.progress_added, 0)
        self.assertEqual(interrupted.filled, held)
        self.assertTrue(campaign.projects[PROJECT_ARTEFACT].paused)
        self.assertIn(ARTEFACT_ID, campaign.projects[PROJECT_ARTEFACT].pause_reasons[0])

        again = advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=3, roster=roster())
        self.assertIs(again.cause, ProgressCause.PAUSED)
        self.assertEqual(again.filled, held)

        campaign.faction().resources.append(ARTEFACT_ID)
        resume_project(campaign, PROJECT_ARTEFACT)
        resumed = advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=4, roster=roster())
        self.assertIsNot(resumed.cause, ProgressCause.PAUSED)
        self.assertGreaterEqual(resumed.filled, held)

    def test_a_pause_states_its_reason_or_is_refused(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        with self.assertRaises(ProjectError):
            pause_project(campaign, PROJECT_ARTEFACT, "   ")
        pause_project(campaign, PROJECT_ARTEFACT, "the review board stopped the programme")
        result = advance_project(campaign, PROJECT_ARTEFACT, rng=Random(1), turn=1, roster=roster())
        self.assertIs(result.cause, ProgressCause.PAUSED)
        self.assertIn("review board", result.notes[0])
        resume_project(campaign, PROJECT_ARTEFACT)
        with self.assertRaises(ProjectError):  # the artefact is still missing
            advance_project(campaign, PROJECT_ARTEFACT, rng=Random(1), turn=2, roster=roster())

    def test_reassignment_keeps_the_clock_and_refuses_a_stranger(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        campaign.faction().resources.append(ARTEFACT_ID)
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        advance_project(campaign, PROJECT_ARTEFACT, rng=Random(3), turn=1, roster=roster())
        filled = campaign.projects[PROJECT_ARTEFACT].clock.filled
        with self.assertRaises(ProjectError):
            reassign_project(campaign, PROJECT_ARTEFACT, "nobody")
        reassign_project(campaign, PROJECT_ARTEFACT, LEADER_ID)
        project = campaign.projects[PROJECT_ARTEFACT]
        self.assertEqual(project.lead_id, LEADER_ID)
        self.assertEqual(project.clock.filled, filled)
        self.assertEqual(project.detail["reassigned_from"], ["a-1"])
        self.assertEqual(project.clock.work_required, 12)  # the difficulty, not the lead, sets the work

    def test_an_unknown_project_or_a_missing_lead_is_refused(self) -> None:
        campaign = fixture()
        with self.assertRaises(ProjectError):
            advance_project(campaign, "no-such-project", rng=Random(1), turn=1, roster=roster())
        add(campaign, reverse_engineering_project())
        campaign.projects[PROJECT_ARTEFACT].lead_id = "ghost"
        with self.assertRaises(ProjectError):
            advance_project(campaign, PROJECT_ARTEFACT, rng=Random(1), turn=1, roster=roster())

    def test_a_project_without_a_ledger_cannot_draw_on_capacity(self) -> None:
        campaign, _ = ready_project()
        campaign.capacities.clear()
        with self.assertRaises(ProjectError):
            advance_project(campaign, "p-guaranteed", rng=Random(1), turn=1, roster=roster())

    def test_the_result_report_round_trips_and_is_self_consistent(self) -> None:
        campaign, _ = ready_project()
        ledger(campaign).allocate("p-guaranteed", RESEARCH_RESOURCE_KIND, 2)
        result = advance_project(campaign, "p-guaranteed", rng=Random(6), turn=1, roster=roster())
        self.assertEqual(ProjectResult.from_dict(result.to_dict()), result)
        self.assertEqual(campaign.projects["p-guaranteed"].history[0], result.to_dict())
        with self.assertRaises(ProjectError):
            ProjectResult.from_dict({**result.to_dict(), "schema_version": "project-result-9"})
        with self.assertRaises(ProjectError):
            ProjectResult.from_dict({**result.to_dict(), "cause": "made-up"})
        with self.assertRaises(ProjectError):
            ProjectResult.from_dict({**result.to_dict(), "outcome": "triumph"})
        with self.assertRaises(ProjectError):
            ProjectResult(
                project_id="p", turn=1, cause=ProgressCause.CHECK_FAILED, lead_id="a",
                resource_kind="research", progress_added=2, filled=2, work_required=4,
                completed=False, throughput=2,
            )

    def test_a_project_serialises_and_the_loader_narrows_to_the_research_type(self) -> None:
        project = reverse_engineering_project()
        payload = json.loads(json.dumps(project.to_dict()))
        loaded = project_from_dict(payload)
        self.assertIsInstance(loaded, StrategicProject)
        self.assertEqual(loaded.to_dict(), project.to_dict())
        self.assertIsInstance(research_project_from_dict(payload), ResearchProject)
        archive = archive_access_project()
        archive_payload = json.loads(json.dumps(archive.to_dict()))
        self.assertIsInstance(project_from_dict(archive_payload), StrategicProject)
        with self.assertRaises(ProjectError):
            research_project_from_dict(archive_payload)

    def test_a_project_must_declare_what_it_is_and_what_it_draws_on(self) -> None:
        with self.assertRaises(ProjectError):
            StrategicProject(
                project_id="p", faction_id=FACTION_ID, title="", kind="organize", lead_id="a-2",
                lead_skill="stewardship", lead_difficulty=1, clock=ProjectClock(2),
                resource_kind="personnel", stage=ProjectStage.DEPLOYMENT,
            )
        with self.assertRaises(ProjectError):
            StrategicProject(
                project_id="p", faction_id=FACTION_ID, title="A task", kind="organize",
                lead_id="a-2", lead_skill="stewardship", lead_difficulty=1, clock=ProjectClock(2),
                resource_kind="personnel", stage="not-a-stage",  # type: ignore[arg-type]
            )
        with self.assertRaises(ProjectError):
            StrategicProject(
                project_id="p", faction_id=FACTION_ID, title="A task", kind="organize",
                lead_id="a-2", lead_skill="stewardship", lead_difficulty=1, clock=ProjectClock(2),
                resource_kind="personnel", stage=ProjectStage.DEPLOYMENT, paused=True,
            )


class CompleteProjectTests(unittest.TestCase):
    def test_completion_requires_the_difficulty_defined_total_work(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        with self.assertRaises(ProjectError) as caught:
            complete_project(campaign, PROJECT_ARTEFACT, turn=1)
        self.assertIn("total work", str(caught.exception))
        campaign.projects[PROJECT_ARTEFACT].clock.add(11)
        with self.assertRaises(ProjectError):
            complete_project(campaign, PROJECT_ARTEFACT, turn=1)

    def test_completion_grants_the_resources_once_and_writes_one_note(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        campaign.projects[PROJECT_ARTEFACT].clock.add(12)
        first = complete_project(campaign, PROJECT_ARTEFACT, turn=1)
        self.assertTrue(first.applied)
        self.assertEqual(first.resource_ids, (LAB_ID,))
        self.assertIn(LAB_ID, campaign.faction().resources)
        notes = [n for n in campaign.campaign_notes if n["kind"] == "project_completion"]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["provenance"]["kind"], "simulated")
        self.assertEqual(notes[0]["turn"], 1)

        second = complete_project(campaign, PROJECT_ARTEFACT, turn=2)
        self.assertFalse(second.applied)
        self.assertEqual(second.note_index, first.note_index)
        self.assertEqual(
            len([n for n in campaign.campaign_notes if n["kind"] == "project_completion"]), 1
        )
        self.assertEqual(campaign.faction().resources.count(LAB_ID), 1)


class ResearchCompletionTests(unittest.TestCase):
    def completed(self, project: StrategicProject) -> Campaign:
        campaign = add(fixture(), project)
        project.clock.add(project.clock.work_required)
        project.completed_on_turn = 1
        return campaign

    def test_completion_grants_exactly_one_stage_and_never_a_later_one(self) -> None:
        campaign = self.completed(reverse_engineering_project())
        completion = complete_research(
            campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=1, case_id=CASE_ID
        )
        self.assertIs(completion.stage, ProjectStage.UNDERSTANDING)
        self.assertEqual(sorted(campaign.capabilities), [NODE_UNDERSTANDING])
        self.assertEqual(completion.equipment_id, "")  # understanding is not a device
        self.assertNotIn(NODE_MANUFACTURE, campaign.capabilities)
        self.assertEqual(completion.resource_ids, (LAB_ID,))

    def test_the_mundane_transfer_grants_manufacture_and_not_understanding(self) -> None:
        campaign = self.completed(technology_transfer_project())
        completion = complete_research(
            campaign, PROJECT_TRANSFER, declared_nodes()[NODE_MANUFACTURE], turn=1, case_id=CASE_ID
        )
        self.assertIs(completion.stage, ProjectStage.MANUFACTURE)
        self.assertEqual(completion.equipment_id, EQUIPMENT_ID)
        self.assertEqual(completion.clue_id, "")
        self.assertEqual(completion.option_id, "")
        self.assertNotIn(NODE_UNDERSTANDING, campaign.capabilities)
        self.assertIn(EQUIPMENT_ID, campaign.sheets["a-3"].gear)

    def test_the_payoff_reaches_the_rpg_layer_and_is_granted_once(self) -> None:
        campaign = self.completed(reverse_engineering_project())
        lead = campaign.sheets["a-1"]
        completion = complete_research(
            campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=1, case_id=CASE_ID
        )
        self.assertTrue(completion.capability_granted)
        self.assertEqual(
            [t.value for t in lead.tags_of_kind("competence") if t.value == "xeno-engineering"],
            ["xeno-engineering"],
        )
        self.assertIn(CLUE_ID, campaign.intelligence_ids)
        self.assertIn(CLUE_ID, campaign.faction().intelligence_ids)
        self.assertIn(CLUE_ID, campaign.cases[CASE_ID].evidence_ids)
        options = rpg_options(campaign)
        self.assertEqual([o.option_id for o in options], [OPTION_ID])
        self.assertEqual(options[0].capability, "xeno-engineering")
        self.assertEqual(options[0].stage, ProjectStage.UNDERSTANDING)

        again = complete_research(
            campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=2, case_id=CASE_ID
        )
        self.assertFalse(again.applied)
        self.assertEqual(again.note_index, completion.note_index)
        self.assertEqual(campaign.intelligence_ids.count(CLUE_ID), 1)
        self.assertEqual(campaign.cases[CASE_ID].evidence_ids.count(CLUE_ID), 1)
        self.assertEqual(len(campaign.capabilities), 1)
        self.assertEqual(
            [t.value for t in lead.tags_of_kind("competence")].count("xeno-engineering"), 1
        )
        self.assertEqual(
            len([n for n in campaign.campaign_notes if n["kind"] == "research_completion"]), 1
        )

    def test_a_capability_cannot_be_granted_before_what_it_requires(self) -> None:
        campaign = self.completed(reverse_engineering_project())
        node = TechNode(
            node_id="prototype",
            label="A drive prototype",
            stage=ProjectStage.PROTOTYPE,
            requires=Prerequisites(node_ids=(NODE_UNDERSTANDING,)),
        )
        campaign.tech_nodes["prototype"] = node
        with self.assertRaises(ProjectError) as caught:
            complete_research(campaign, PROJECT_ARTEFACT, node, turn=1)
        self.assertIn(NODE_UNDERSTANDING, str(caught.exception))
        self.assertNotIn("prototype", campaign.capabilities)

    def test_a_capability_the_world_does_not_declare_is_refused(self) -> None:
        campaign = self.completed(reverse_engineering_project())
        undeclared = TechNode(
            node_id="invented", label="An invented technology", stage=ProjectStage.MANUFACTURE
        )
        with self.assertRaises(ProjectError):
            complete_research(campaign, PROJECT_ARTEFACT, undeclared, turn=1)
        different = TechNode(
            node_id=NODE_UNDERSTANDING, label="A different record", stage=ProjectStage.UNDERSTANDING
        )
        with self.assertRaises(ProjectError):
            complete_research(campaign, PROJECT_ARTEFACT, different, turn=1)
        with self.assertRaises(ProjectError):
            complete_research(campaign, PROJECT_ARTEFACT, turn=1)  # no node named at all

    def test_a_capability_round_trips_through_the_loader(self) -> None:
        node = declared_nodes()[NODE_UNDERSTANDING]
        self.assertEqual(capability_from_dict(node.to_dict()), node)
        self.assertEqual(TechNode.from_dict(node.to_dict()), Capability.from_dict(node.to_dict()))
        self.assertEqual(node.branch, "alien_derived")
        self.assertEqual(node.hybrid_of, ("quantumpunk",))
        self.assertIs(node.stage, ProjectStage.UNDERSTANDING)

    def test_prohibitions_are_reported_and_enforce_nothing(self) -> None:
        campaign = self.completed(reverse_engineering_project())
        node = declared_nodes()[NODE_UNDERSTANDING]
        self.assertEqual(
            prohibitions_for(campaign, node, faction_id=FACTION_ID),
            ("doctrine:butlerian-retrenchment",),
        )
        self.assertEqual(prohibitions_for(campaign, declared_nodes()[NODE_MANUFACTURE],
                                          faction_id=FACTION_ID), ())
        completion = complete_research(
            campaign, PROJECT_ARTEFACT, node, turn=1, case_id=CASE_ID
        )
        self.assertEqual(completion.prohibitions, ("doctrine:butlerian-retrenchment",))
        self.assertTrue(completion.applied)  # the contradiction is a report, not a gate
        self.assertEqual(len(campaign.capabilities), 1)

    def test_the_clue_needs_its_case_and_the_completion_needs_its_project(self) -> None:
        campaign = self.completed(reverse_engineering_project())
        with self.assertRaises(ProjectError):
            complete_research(
                campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=1,
                case_id="no-case",
            )
        with self.assertRaises(ProjectError):
            complete_research(
                campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_MANUFACTURE], turn=1
            )
        with self.assertRaises(ProjectError):
            complete_research(campaign, "no-project", declared_nodes()[NODE_UNDERSTANDING], turn=1)

    def test_an_unfilled_programme_has_nothing_to_resolve(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        with self.assertRaises(ProjectError):
            complete_research(
                campaign, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=1
            )

    def test_the_research_kinds_are_declared_and_the_record_stays_free_text(self) -> None:
        self.assertEqual(len(RESEARCH_PROJECT_KINDS), 7)
        self.assertEqual(RESEARCH_PROJECT_KINDS["reverse_engineering"], "Reverse engineering")
        self.assertEqual(
            RESEARCH_PROJECT_KINDS["technology_transfer"], "Technology transfer / industrialization"
        )


class ResearchProjectTypeTests(unittest.TestCase):
    def test_a_non_science_project_is_not_a_research_project(self) -> None:
        with self.assertRaises(ProjectError) as caught:
            ResearchProject(
                project_id="p-admin", faction_id=FACTION_ID, title="An organising programme",
                kind="organize", lead_id="a-2", lead_skill="stewardship", lead_difficulty=1,
                clock=ProjectClock(4), resource_kind="personnel", stage=ProjectStage.DEPLOYMENT,
                domain_tags=("Logistics",),
            )
        self.assertIn("science", str(caught.exception).lower())

    def test_the_same_task_is_a_perfectly_good_project_on_the_same_engine(self) -> None:
        campaign = add(fixture(), archive_access_project())
        project = campaign.projects[PROJECT_ARCHIVE]
        self.assertIsInstance(project, StrategicProject)
        self.assertNotIsInstance(project, ResearchProject)
        self.assertEqual(project.lead_skill, "stewardship")
        self.assertEqual(project.node_id, "")
        ledger(campaign).allocate(PROJECT_ARCHIVE, "personnel", 3)
        result = advance_project(campaign, PROJECT_ARCHIVE, rng=Random(1), turn=1, roster=roster())
        self.assertGreaterEqual(result.progress_added, 0)

    def test_research_without_domain_tags_is_valid(self) -> None:
        project = ResearchProject(
            project_id="p-no-tags", faction_id=FACTION_ID, title="General research",
            kind="basic_science", lead_id="a-1", lead_skill=RESEARCH_LEAD_SKILL,
            lead_difficulty=2, clock=ProjectClock(4), resource_kind=RESEARCH_RESOURCE_KIND,
            stage=ProjectStage.UNDERSTANDING,
        )
        self.assertEqual(project.domain_tags, ())
        self.assertEqual(project.lead_skill, RESEARCH_LEAD_SKILL)
        restored = research_project_from_dict(project.to_dict())
        self.assertEqual(restored.domain_tags, ())

    def test_a_yield_is_ids_into_vocabularies_that_already_exist(self) -> None:
        self.assertTrue(ResearchYield().is_empty())
        yield_ = ResearchYield(capability="x", option="o", equipment="e", clue="c")
        self.assertEqual(ResearchYield.from_dict(json.loads(json.dumps(yield_.to_dict()))), yield_)
        self.assertFalse(yield_.is_empty())


class SliceTests(unittest.TestCase):
    def test_the_mission_is_the_only_writer_that_hands_over_the_artefact(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        with self.assertRaises(ProjectError) as caught:
            advance_project(campaign, PROJECT_ARTEFACT, rng=Random(1), turn=1, roster=roster())
        self.assertIn("apply_mission_outcome", str(caught.exception))

    def test_the_slice_reproduces_the_documented_run(self) -> None:
        """The eleven turns of :data:`DEMO_SEED`, derived from the engine rather than asserted."""
        report = run_demo(seed=DEMO_SEED)
        turns = [
            (step["turn"], step.get("project_id"), step.get("cause"), step.get("progress_added"),
             step.get("filled"))
            for step in report["steps"] if step["step"] == "project_turn"
        ]
        self.assertEqual(
            turns,
            [
                (1, PROJECT_ARTEFACT, "check_failed", 0, 0),
                (2, PROJECT_ARTEFACT, "advanced", 3, 3),
                (3, PROJECT_ARTEFACT, "advanced", 4, 7),
                (4, PROJECT_ARTEFACT, "advanced", 4, 11),
                (5, PROJECT_ARTEFACT, "completed", 1, 12),
                (6, PROJECT_ARCHIVE, "advanced", 3, 3),
                (7, PROJECT_ARCHIVE, "advanced", 4, 7),
                (8, PROJECT_ARCHIVE, "completed", 3, 10),
                (9, PROJECT_TRANSFER, "advanced", 4, 4),
                (10, PROJECT_TRANSFER, "advanced", 4, 8),
                (11, PROJECT_TRANSFER, "completed", 2, 10),
            ],
        )
        self.assertEqual(report["steps"][0]["step"], "mission_outcome")
        self.assertEqual(report["steps"][0]["resources_gained"], [ARTEFACT_ID])
        self.assertEqual(report["turns"], 11)
        self.assertEqual(report["structural_problems"], [])
        self.assertTrue(report["save"]["reload_identical"])
        self.assertEqual(report["programmes"][PROJECT_ARTEFACT]["stalled_turns"], [1])

    def test_the_run_shows_failure_and_that_it_costs_only_the_turn(self) -> None:
        report = run_demo(seed=DEMO_SEED)
        stalled = [
            s for s in report["steps"] if s["step"] == "project_turn" and s["progress_added"] == 0
        ]
        self.assertEqual(len(stalled), 1)
        self.assertEqual(stalled[0]["cause"], "check_failed")
        self.assertIn("no progress this round", stalled[0]["notes"][0])
        self.assertEqual(stalled[0]["filled"], 0)
        self.assertEqual(stalled[0]["outcome"], "failure")
        self.assertEqual(stalled[0]["turn"], 1)

    def test_the_alien_and_the_mundane_example_are_different_stages(self) -> None:
        report = run_demo(seed=DEMO_SEED)
        self.assertEqual(
            report["stages_kept_separate"][NODE_UNDERSTANDING], ProjectStage.UNDERSTANDING.value
        )
        self.assertEqual(
            report["stages_kept_separate"][NODE_MANUFACTURE], ProjectStage.MANUFACTURE.value
        )
        completions = {c["project_id"]: c for c in report["completions"]}
        self.assertEqual(completions[PROJECT_ARTEFACT]["equipment_id"], "")
        self.assertEqual(completions[PROJECT_ARTEFACT]["clue_id"], CLUE_ID)
        self.assertEqual(completions[PROJECT_ARTEFACT]["stage"], "scientific_understanding")
        self.assertEqual(completions[PROJECT_TRANSFER]["equipment_id"], EQUIPMENT_ID)
        self.assertEqual(completions[PROJECT_TRANSFER]["stage"], "reproducible_manufacture")
        self.assertIn(EQUIPMENT_ID, report["sheets_gear"]["a-3"])
        self.assertIn("xeno-engineering", report["sheets_with_new_capabilities"]["a-1"])
        self.assertEqual(report["held_capabilities"], sorted([NODE_MANUFACTURE, NODE_UNDERSTANDING]))

    def test_the_non_research_task_uses_another_lead_skill_and_produces_no_capability(self) -> None:
        report = run_demo(seed=DEMO_SEED)
        project = archive_access_project()
        self.assertEqual(project.lead_skill, "stewardship")
        self.assertEqual(project.resource_kind, "personnel")
        self.assertEqual(project.node_id, "")
        self.assertEqual(report["generic_completion"]["project_id"], PROJECT_ARCHIVE)
        self.assertEqual(report["generic_completion"]["resource_ids"], [ARCHIVE_ID])
        self.assertNotIn(ARCHIVE_ID, report["held_capabilities"])
        self.assertEqual(report["programmes"][PROJECT_ARCHIVE]["clock"]["filled"], 10)
        self.assertIn(ARCHIVE_ID, report["faction_resources"])
        self.assertIn(LAB_ID, report["faction_resources"])
        self.assertIn(ARTEFACT_ID, report["faction_resources"])

    def test_the_faction_that_would_not_do_this_is_told_so(self) -> None:
        report = run_demo(seed=DEMO_SEED)
        completion = next(
            c for c in report["completions"] if c["node_id"] == NODE_UNDERSTANDING
        )
        self.assertEqual(completion["prohibitions"], ["doctrine:butlerian-retrenchment"])

    def test_save_load_preserves_the_run_and_the_loaded_model_keeps_going(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        campaign.faction().resources.append(ARTEFACT_ID)
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        rng = Random(DEMO_SEED)
        for turn in (1, 2, 3):
            advance_project(campaign, PROJECT_ARTEFACT, rng=rng, turn=turn, roster=roster())
        self.assertEqual(campaign.projects[PROJECT_ARTEFACT].clock.filled, 7)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "campaign.json"
            save_campaign(campaign, path)
            loaded = load_campaign(path)
            self.assertEqual(loaded.to_json(), campaign.to_json())
            self.assertEqual(loaded.projects[PROJECT_ARTEFACT].clock.filled, 7)
            self.assertEqual(
                loaded.projects[PROJECT_ARTEFACT].history,
                campaign.projects[PROJECT_ARTEFACT].history,
            )
            self.assertEqual(loaded.capacities[FACTION_ID].allocated(PROJECT_ARTEFACT), 3)
            result = advance_project(loaded, PROJECT_ARTEFACT, rng=rng, turn=4, roster=roster())
            self.assertGreater(result.filled, 7)

    def test_a_reloaded_run_can_be_resolved_the_same_way_twice(self) -> None:
        campaign = add(fixture(), reverse_engineering_project())
        campaign.faction().resources.append(ARTEFACT_ID)
        ledger(campaign).allocate(PROJECT_ARTEFACT, RESEARCH_RESOURCE_KIND, 3)
        campaign.projects[PROJECT_ARTEFACT].clock.add(12)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "campaign.json"
            save_campaign(campaign, path)
            loaded = load_campaign(path)
        first = complete_research(
            loaded, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=1, case_id=CASE_ID
        )
        second = complete_research(
            loaded, PROJECT_ARTEFACT, declared_nodes()[NODE_UNDERSTANDING], turn=2, case_id=CASE_ID
        )
        self.assertTrue(first.applied)
        self.assertFalse(second.applied)
        self.assertEqual(loaded.to_dict()["capabilities"], loaded.to_dict()["capabilities"])

    def test_the_snapshot_declares_the_same_schema_marker_as_the_campaign_model(self) -> None:
        payload = fixture().to_dict()
        for key in ("projects", "tech_nodes", "capabilities", "capacities"):
            self.assertIn(key, payload)
        self.assertEqual(payload["schema_version"], "campaign-save-1")

    def test_a_snapshot_written_before_the_project_books_still_loads(self) -> None:
        """Compatible growth keeps the marker: an older payload loads with the new books empty."""
        campaign = fixture()
        payload = campaign.to_dict()
        for key in ("projects", "tech_nodes", "capabilities", "capacities"):
            payload.pop(key)
        restored = campaign_from_dict(json.loads(json.dumps(payload)))
        self.assertEqual(restored.projects, {})
        self.assertEqual(restored.capacities, {})
        self.assertEqual(
            restored.factions[FACTION_ID].resources, campaign.factions[FACTION_ID].resources
        )

    def test_the_shared_model_reports_a_project_that_cannot_be_played(self) -> None:
        campaign = fixture()
        campaign.factions["rival"] = CampaignFaction(
            identifier="rival", name="A faction with no ledger", leader_id="", member_ids=[]
        )
        orphan = StrategicProject(
            project_id="p-orphan", faction_id="rival", title="A rival's programme", kind="organize",
            lead_id="a-2", lead_skill="stewardship", lead_difficulty=1, clock=ProjectClock(4),
            resource_kind="personnel", stage=ProjectStage.DEPLOYMENT,
        )
        add(campaign, orphan)
        problems = campaign.structural_problems()
        self.assertEqual(len(problems), 1)
        self.assertIn("capacity ledger", problems[0])
        orphan.lead_id = "ghost"
        self.assertIn("ghost", " | ".join(campaign.structural_problems()))
        # and the model refuses to be built around a project of a faction it does not have at all
        orphan.faction_id = "nowhere"
        with self.assertRaises(CampaignError):
            Campaign(
                faction_id=FACTION_ID, leader_id=LEADER_ID, sheets=campaign.sheets,
                factions=campaign.factions, projects={"p-orphan": orphan},
            )

    def test_the_shared_model_reports_a_capability_granted_before_its_requirement(self) -> None:
        campaign = fixture()
        understanding = declared_nodes()[NODE_UNDERSTANDING]
        prototype = TechNode(
            node_id="prototype", label="A drive prototype", stage=ProjectStage.PROTOTYPE,
            requires=Prerequisites(node_ids=(NODE_UNDERSTANDING,)),
        )
        # a held stage the world's data does not declare is refused outright
        with self.assertRaises(CampaignError):
            Campaign(
                faction_id=FACTION_ID, leader_id=LEADER_ID, sheets=campaign.sheets,
                factions=campaign.factions, tech_nodes={NODE_UNDERSTANDING: understanding},
                capabilities={"undeclared": understanding},
            )
        # a held stage whose declared requirement is not held is reported
        campaign.tech_nodes = {NODE_UNDERSTANDING: understanding, "prototype": prototype}
        campaign.capabilities = {"prototype": prototype}
        problems = " | ".join(campaign.structural_problems())
        self.assertIn("requires node", problems)
        self.assertIn(NODE_UNDERSTANDING, problems)

    def test_the_entrypoint_prints_a_json_report(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = main(["--seed", str(DEMO_SEED)])
        self.assertEqual(code, 0)
        report = json.loads(buffer.getvalue())
        self.assertEqual(report["schema"], "noopunk.strategy_game.research_slice")
        self.assertTrue(report["save"]["reload_identical"])
        self.assertEqual(report["seed"], DEMO_SEED)


def _without_the_temp_path(report: dict[str, Any]) -> dict[str, Any]:
    """The run report with the snapshot's temp path removed, so two runs are comparable."""
    stable = json.loads(json.dumps(report))
    stable["save"].pop("path", None)
    return stable


class DeterminismTests(unittest.TestCase):
    def test_the_same_seed_gives_the_same_run(self) -> None:
        first = _without_the_temp_path(run_demo(seed=DEMO_SEED))
        second = _without_the_temp_path(run_demo(seed=DEMO_SEED))
        self.assertEqual(json.dumps(first, sort_keys=True), json.dumps(second, sort_keys=True))

    def test_a_different_seed_gives_different_dice(self) -> None:
        runs = [run_demo(seed=seed) for seed in range(6)]
        timelines = {json.dumps([s.get("progress_added") for s in r["steps"]]) for r in runs}
        self.assertGreater(len(timelines), 1)

    def test_the_report_carries_the_seed_it_replayed(self) -> None:
        report = run_demo(seed=7)
        self.assertEqual(report["seed"], 7)
        turns = [s for s in report["steps"] if s["step"] == "project_turn"]
        self.assertTrue(all(s["seed"] == 7 for s in turns if s["seed"] is not None))

    def test_an_unseeded_generator_reports_no_seed_rather_than_inventing_one(self) -> None:
        campaign, _ = ready_project()
        ledger(campaign).allocate("p-guaranteed", RESEARCH_RESOURCE_KIND, 2)
        result = advance_project(
            campaign, "p-guaranteed", rng=random.Random(), turn=1, roster=roster()
        )
        self.assertIsNone(result.seed)


if __name__ == "__main__":
    unittest.main()
