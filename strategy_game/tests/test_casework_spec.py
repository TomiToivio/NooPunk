"""The case declaration and its gates (issue #502, Phase 1): executable contracts only.

These tests exercise behaviour — a declaration that cannot be played, a cyber path that does not
exist, a psi capability a character does not carry, a clue no action can yield. They do not assert
the scenario's prose and they do not freeze a canon sentence: per ``AGENTS.md``, creative text is
reviewed editorially and in play, not by CI.
"""
from __future__ import annotations

import unittest

from strategy_game.campaign.state import Campaign
from strategy_game.casework import kallio
from strategy_game.casework.session import CaseSession, CaseworkError
from strategy_game.casework.spec import (
    DIFFICULTY_BANDS,
    ActionSpec,
    CaseFile,
    CaseSpecError,
    CheckSpec,
    ClueSpec,
    FindingSpec,
    ResolutionSpec,
    SceneSpec,
    band_difficulty,
)
from strategy_game.rpg.fate import Action, Character
from strategy_game.rpg.skills import SkillLayerError, require_capability


def _minimal_scene(action: ActionSpec) -> SceneSpec:
    return SceneSpec("s", "Scene", "Somewhere", "Prose.", (action,))


class DifficultyBandTests(unittest.TestCase):
    def test_band_names_map_to_the_fate_ladder(self) -> None:
        self.assertEqual(band_difficulty("Average"), 1)
        self.assertEqual(band_difficulty("fair"), 2)
        self.assertEqual(band_difficulty("Good"), 3)
        self.assertEqual(set(DIFFICULTY_BANDS), {
            "Mediocre", "Average", "Fair", "Good", "Great", "Superb", "Fantastic"
        })

    def test_an_off_ladder_band_is_refused(self) -> None:
        with self.assertRaises(CaseSpecError):
            band_difficulty("Impossible")


class DeclarationTests(unittest.TestCase):
    def test_the_packaged_case_is_structurally_sound(self) -> None:
        self.assertEqual(kallio.CASE.structural_problems(), ())
        self.assertEqual(len(kallio.CASE.scenes), 5)
        self.assertEqual(len(kallio.CASE.resolutions), 3)
        self.assertEqual(len(kallio.CASE.chain), 3)

    def test_every_chain_fragment_is_obtainable_by_more_than_one_action(self) -> None:
        for fragment in kallio.CASE.chain:
            routes = [
                (scene.id, action.id)
                for scene in kallio.CASE.scenes
                for action in scene.actions
                if fragment in action.gives
            ]
            self.assertGreaterEqual(
                len(routes), 2,
                f"{fragment!r} has only one route {routes}; a clue must not depend on one check",
            )

    def test_a_scene_with_no_actions_is_refused(self) -> None:
        with self.assertRaises(CaseSpecError):
            SceneSpec("empty", "Empty", "Nowhere", "Nothing happens.", ())

    def test_an_action_that_changes_nothing_is_refused(self) -> None:
        with self.assertRaises(CaseSpecError):
            ActionSpec("noop", "Nothing", "Nothing at all.")

    def test_a_clue_no_action_yields_is_reported(self) -> None:
        action = ActionSpec(
            "a", "Look", "You look.", gives=("known",), check=CheckSpec(Action.OVERCOME, "COG", "Fair")
        )
        case = CaseFile(
            id="c",
            title="C",
            core_question="Q?",
            hook="H",
            era="after_crisis",
            era_label="2045",
            scenes=(_minimal_scene(action),),
            clues=(
                ClueSpec("known", "Known", "It is known."),
                ClueSpec("orphan", "Orphan", "Nothing yields it."),
            ),
            findings=(FindingSpec("f", "F", "F.", ("known",), partial_min=1),),
            resolutions=(
                ResolutionSpec("r", "R", "R.", "SAV", "Average", requires_finding="f", objective="O"),
                ResolutionSpec("r2", "R2", "R2.", "WIL", "Average", objective="O2"),
            ),
            chain=("known", "orphan"),
        )
        problems = case.structural_problems()
        self.assertTrue(any("orphan" in problem for problem in problems), problems)

    def test_a_resolution_naming_an_unknown_finding_is_reported(self) -> None:
        action = ActionSpec("a", "Look", "You look.", gives=("known",))
        case = CaseFile(
            id="c",
            title="C",
            core_question="Q?",
            hook="H",
            era="after_crisis",
            era_label="2045",
            scenes=(_minimal_scene(action),),
            clues=(ClueSpec("known", "Known", "It is known."),),
            findings=(FindingSpec("f", "F", "F.", ("known",)),),
            resolutions=(
                ResolutionSpec("r", "R", "R.", "SAV", "Average", requires_finding="nope", objective="O"),
                ResolutionSpec("r2", "R2", "R2.", "WIL", "Average", objective="O2"),
            ),
            chain=("known",),
        )
        self.assertTrue(
            any("unknown finding" in problem for problem in case.structural_problems())
        )

    def test_validate_raises_on_a_broken_case(self) -> None:
        action = ActionSpec("a", "Look", "You look.", gives=("known",))
        case = CaseFile(
            id="c",
            title="C",
            core_question="Q?",
            hook="H",
            era="after_crisis",
            era_label="2045",
            scenes=(_minimal_scene(action),),
            clues=(ClueSpec("known", "Known", "It is known."),),
            findings=(FindingSpec("f", "F", "F.", ("missing",)),),
            resolutions=(
                ResolutionSpec("r", "R", "R.", "SAV", "Average", objective="O"),
                ResolutionSpec("r2", "R2", "R2.", "WIL", "Average", objective="O2"),
            ),
            chain=("known",),
        )
        with self.assertRaises(CaseSpecError):
            case.validate()


class CampaignTests(unittest.TestCase):
    def test_the_pc_is_the_leader_and_four_agents_hold_the_other_seats(self) -> None:
        campaign = kallio.build_campaign()
        leader = campaign.leader_view()
        agents = campaign.agent_views()
        self.assertEqual(leader.identifier, kallio.LEADER_ID)
        self.assertEqual(tuple(agent.identifier for agent in agents), kallio.AGENT_IDS)
        self.assertEqual(campaign.roster_report()["unfilled_seats"], 0)
        self.assertEqual(campaign.structural_problems(), ())

    def test_the_case_record_is_on_the_campaign_so_evidence_has_somewhere_to_go(self) -> None:
        campaign = kallio.build_campaign()
        self.assertIn(kallio.CASE_ID, campaign.cases)
        case = campaign.cases[kallio.CASE_ID]
        self.assertEqual(case.investigator, kallio.LEADER_ID)
        self.assertEqual(case.partner, "laura_falk")
        self.assertEqual(set(case.domain_leads), {
            "physical", "cybernetic", "social", "psychic_noospace"
        })

    def test_a_session_refuses_a_campaign_without_the_case(self) -> None:
        campaign = kallio.build_campaign()
        campaign.cases.clear()
        with self.assertRaises(CaseworkError):
            CaseSession(kallio.CASE, campaign, seed=1)

    def test_a_session_refuses_a_campaign_without_a_leader(self) -> None:
        campaign = Campaign()
        with self.assertRaises(CaseworkError):
            CaseSession(kallio.CASE, campaign, seed=1)


class GateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = kallio.build_session(seed=1)

    def test_the_local_only_mesh_refuses_a_remote_path_and_permits_a_field_port(self) -> None:
        remote = self.session.probe_access(
            "local_only", "after_crisis", "remote_public_service"
        )
        self.assertFalse(remote["possible"])
        self.assertIn("isolated or local-only", remote["reason"])
        local = self.session.probe_access(
            "local_only", "after_crisis", "field_netrunner", local_presence=True
        )
        self.assertTrue(local["possible"])
        without_presence = self.session.probe_access(
            "local_only", "after_crisis", "field_netrunner", local_presence=False
        )
        self.assertFalse(without_presence["possible"])

    def test_a_social_tie_is_not_an_access_path(self) -> None:
        with self.assertRaises(ValueError):
            self.session.probe_access("local_only", "after_crisis", "social_tie")

    def test_the_psi_gate_refuses_a_character_without_the_capability(self) -> None:
        agent = self.session.campaign.sheets["laura_univaara"]
        with self.assertRaises(SkillLayerError):
            require_capability(agent, "TELEPATH")
        witness = self.session.campaign.sheets[kallio.WITNESS_ID]
        require_capability(witness, "TELEPATH")
        self.assertTrue(witness.natural_psi)

    def test_a_witness_without_the_capability_makes_the_reading_unavailable(self) -> None:
        campaign = self.session.campaign
        stripped = Character(
            id=kallio.WITNESS_ID,
            name="Aino Rautio",
            aspects=["No longer psi-capable in this fixture"],
            skills={"WIL": 2},
        )
        campaign.sheets[kallio.WITNESS_ID] = stripped
        session = CaseSession(kallio.CASE, campaign, seed=1)
        session.act("harri_romppainen", "read_the_duty_log")
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        session.end_scene()
        session.act("sebastian_virtanen", "read_the_stairwell")
        session.end_scene()
        psi_actions = [item for item in session.actions() if item["id"] == "supervise_the_reading"]
        self.assertEqual(len(psi_actions), 1)
        self.assertFalse(psi_actions[0]["available"])
        self.assertIn("TELEPATH", psi_actions[0]["reason"])

    def test_the_cyber_action_is_offered_only_once_its_prerequisite_is_held(self) -> None:
        session = self.session
        session.act("harri_romppainen", "read_the_duty_log")
        session.end_scene()
        session.act("laura_falk", "interview_nila")
        session.end_scene()
        offered = {item["id"]: item for item in session.actions()}
        self.assertTrue(offered["pull_the_mesh_log"]["available"])

        fresh = kallio.build_session(seed=1)
        fresh.end_scene()
        fresh.act("laura_falk", "interview_nila")
        fresh.end_scene()
        blocked = {item["id"]: item for item in fresh.actions()}["pull_the_mesh_log"]
        self.assertFalse(blocked["available"])
        self.assertIn("requires", blocked["reason"])


if __name__ == "__main__":
    unittest.main()
