"""Contract tests for the #1164 Astral graph and PSI permission add-on."""

import unittest
from pathlib import Path

from src.rules.astral import (
    PSI_MATRIX,
    AstralEdge,
    AstralError,
    AstralGraph,
    AstralMode,
    AstralNode,
    AstralState,
    PermissionStatus,
    PsiTarget,
    PsiVerb,
    activate,
    authorize,
    permission,
)
from src.rules.swn_psionics import Psychic


class MatrixTest(unittest.TestCase):
    def test_every_cell_is_present_and_grants_no_clue(self):
        self.assertEqual(len(PSI_MATRIX), len(PsiVerb) * len(PsiTarget))
        self.assertTrue(
            all(not cell.grants_investigation_clue for cell in PSI_MATRIX.values())
        )

    def test_default_is_denied_and_scripted_is_not_a_player_action(self):
        self.assertIs(
            permission(PsiVerb.MANIFEST, PsiTarget.PERSON).status,
            PermissionStatus.DENIED,
        )
        self.assertIs(
            permission(PsiVerb.IMPRINT, PsiTarget.MATTER).status,
            PermissionStatus.SCRIPTED,
        )
        self.assertIs(
            permission("not-a-verb", "person").status, PermissionStatus.DENIED
        )

    def test_shield_self_and_project_astral_are_active(self):
        self.assertIs(
            permission(PsiVerb.SHIELD, PsiTarget.SELF).status, PermissionStatus.ACTIVE
        )
        self.assertIs(
            permission(PsiVerb.PROJECT, PsiTarget.ASTRAL).status,
            PermissionStatus.ACTIVE,
        )


class AuthorizeTest(unittest.TestCase):
    def test_unlock_is_required_even_for_an_active_cell(self):
        action = authorize(PsiVerb.SHIELD, PsiTarget.SELF)
        self.assertFalse(action.permitted)
        self.assertIn("unlock", action.reason)

    def test_astral_target_needs_projection(self):
        action = authorize(PsiVerb.PERCEIVE, PsiTarget.ASTRAL, unlocked=True)
        self.assertFalse(action.permitted)
        projected = AstralState(mode=AstralMode.PROJECTED, anchor="physical:home")
        self.assertTrue(
            authorize(
                PsiVerb.PERCEIVE, PsiTarget.ASTRAL, state=projected, unlocked=True
            ).permitted
        )

    def test_person_contact_needs_consent(self):
        self.assertFalse(
            authorize(PsiVerb.CONTACT, PsiTarget.PERSON, unlocked=True).permitted
        )
        self.assertTrue(
            authorize(
                PsiVerb.CONTACT, PsiTarget.PERSON, unlocked=True, consent=True
            ).permitted
        )

    def test_manifest_person_is_denied(self):
        action = authorize(PsiVerb.MANIFEST, PsiTarget.PERSON, unlocked=True)
        self.assertFalse(action.permitted)
        self.assertFalse(action.scripted_only)


class ProjectionTest(unittest.TestCase):
    def _psychic(self) -> Psychic:
        return Psychic(wisdom=14, constitution=10, disciplines={"Metapsionics": 1})

    def test_projection_commits_one_effort_and_keeps_the_body_anchor(self):
        psychic = self._psychic()
        before = psychic.free
        state = AstralState()
        state.project(
            anchor="physical:kurvi-home", realm="astral:kurvi", psychic=psychic
        )
        self.assertIs(state.mode, AstralMode.PROJECTED)
        self.assertEqual(state.anchor, "physical:kurvi-home")
        self.assertEqual(psychic.free, before - 1)

    def test_projection_requires_an_anchor_and_realm(self):
        psychic = self._psychic()
        with self.assertRaises(AstralError):
            AstralState().project(anchor="", realm="astral:kurvi", psychic=psychic)
        with self.assertRaises(AstralError):
            AstralState().project(anchor="physical:home", realm="", psychic=psychic)

    def test_return_and_snapshot_roundtrip(self):
        state = AstralState()
        state.project(
            anchor="physical:home", realm="astral:kurvi", psychic=self._psychic()
        )
        state.current_node = "astral.kurvi.echo"
        restored = AstralState.from_snapshot(state.snapshot())
        self.assertEqual(restored.snapshot(), state.snapshot())
        restored.return_to_body()
        self.assertIs(restored.mode, AstralMode.EMBODIED)
        self.assertEqual(restored.anchor, "physical:home")

    def test_link_boxes_cap_at_three_and_do_not_kill(self):
        state = AstralState()
        state.project(
            anchor="physical:home", realm="astral:kurvi", psychic=self._psychic()
        )
        state.tick_scene()
        state.tick_scene()
        state.tick_scene()
        state.tick_scene()
        self.assertEqual(state.link_boxes, 3)
        self.assertTrue(state.link_lost)

    def test_bad_link_state_is_rejected(self):
        with self.assertRaises(AstralError):
            AstralState(link_boxes=4)


class GraphTest(unittest.TestCase):
    def _graph(self) -> AstralGraph:
        return AstralGraph(
            nodes={
                "astral.kurvi": AstralNode(
                    "astral.kurvi", "Kurvi", visibility="public"
                ),
                "astral.echo": AstralNode(
                    "astral.echo",
                    "Echo",
                    visibility="gm_secret",
                    unlock_act=3,
                    density=4,
                ),
                "astral.deep": AstralNode(
                    "astral.deep",
                    "Deep",
                    visibility="discovered",
                    unlock_act=4,
                    density=5,
                ),
            },
            edges=(
                AstralEdge("astral.kurvi", "astral.echo", gate="act3"),
                AstralEdge("astral.kurvi", "astral.deep"),
            ),
        )

    def test_gm_secret_node_is_invisible_until_both_gates_open(self):
        graph = self._graph()
        self.assertFalse(graph.visible("astral.echo", act=2))
        self.assertFalse(graph.visible("astral.echo", act=3))
        self.assertTrue(graph.visible("astral.echo", act=3, discovered={"astral.echo"}))
        self.assertEqual(graph.neighbors("astral.kurvi", act=2), ())

    def test_travel_needs_a_visible_adjacent_node_and_open_gate(self):
        graph = self._graph()
        self.assertFalse(
            graph.traverse(
                "astral.kurvi", "astral.echo", act=3, discovered={"astral.echo"}
            )
        )
        self.assertTrue(
            graph.traverse(
                "astral.kurvi",
                "astral.echo",
                act=3,
                discovered={"astral.echo"},
                unlocked_gates={"act3"},
            )
        )
        self.assertFalse(graph.traverse("astral.kurvi", "astral.deep", act=1))
        self.assertTrue(graph.traverse("astral.kurvi", "astral.deep", act=4))

    def test_dangling_edge_is_rejected(self):
        with self.assertRaises(AstralError):
            AstralGraph(
                nodes={"a": AstralNode("a", "A")}, edges=(AstralEdge("a", "missing"),)
            )


class BoundaryTest(unittest.TestCase):
    def test_module_has_no_investigation_import(self):
        source = Path(__file__).resolve().parents[1] / "src" / "rules" / "astral.py"
        text = source.read_text(encoding="utf-8")
        self.assertNotIn("from .investigation", text)
        self.assertNotIn("import investigation", text)

    def test_activation_commits_once_and_reuses_the_key(self):
        psychic = Psychic(wisdom=12, constitution=12, disciplines={"Telepathy": 0})
        first = activate(
            PsiVerb.SHIELD,
            PsiTarget.SELF,
            psychic=psychic,
            key="shield",
            unlocked=True,
            discipline="Telepathy",
        )
        self.assertTrue(first.permitted)
        second = activate(
            PsiVerb.SHIELD,
            PsiTarget.SELF,
            psychic=psychic,
            key="shield",
            unlocked=True,
            discipline="Telepathy",
        )
        self.assertFalse(second.permitted)
        self.assertIn("unique", second.reason)


if __name__ == "__main__":
    unittest.main()
