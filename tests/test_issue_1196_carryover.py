"""Carry-over psionics (#1196 §2-§5) and graph runtime wiring (#1196 §6)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from console.world_session import WorldSession, WorldSessionError  # noqa: E402
from rules.psi_access import Grant, PsiAccessError, device_grant  # noqa: E402
from rules.psi_edges import (  # noqa: E402
    EDGE_SOURCES,
    Citation,
    EdgeGrants,
    FocusLevel,
    MutantTemplate,
    MutationCatalogue,
    MutationEntry,
    PsiEdgeError,
    PsychicTrainingFocus,
    active_grants,
    assert_mutant_is_npc,
    require_device,
    validate_edge,
)
from rules.swn_psionics import Psychic  # noqa: E402


def citation(quote: str = "the printed sentence") -> Citation:
    return Citation(source="CWN p. 1", page="1", quote=quote)


def world_payload() -> dict:
    return {
        "format": "noopunk.world.graphs",
        "version": 1,
        "physical": {
            "graph_type": "physical",
            "nodes": [
                {"id": "loc.street", "label": "Kurvi street", "kind": "street"},
                {"id": "loc.stair", "label": "Stairwell", "kind": "room"},
            ],
            "edges": [{"source": "loc.street", "target": "loc.stair", "kind": "door"}],
            "occupants": {"pc.rookie": "loc.street"},
        },
        "cyber": {
            "graph_type": "cyber",
            "nodes": [
                {"id": "cyber.camera", "label": "Camera", "device_type": "camera",
                 "physical_location": "loc.stair", "actions": ["observe"]},
            ],
            "edges": [],
            "avatars": {},
        },
        "social": {
            "graph_type": "social",
            "nodes": [
                {"id": "pc.rookie", "label": "Rookie", "kind": "character"},
                {"id": "npc.falk", "label": "Falk", "kind": "character"},
            ],
            "edges": [{"source": "pc.rookie", "target": "npc.falk", "score": 1,
                       "kind": "colleague"}],
        },
        "story": {
            "graph_type": "story",
            "nodes": [
                {"id": "series.one", "label": "Series one", "kind": "series"},
                {"id": "episode.one", "label": "Episode one", "kind": "episode",
                 "parent_id": "series.one"},
                {"id": "scene.briefing", "label": "Briefing", "kind": "scene",
                 "parent_id": "episode.one", "scene_types": ["social"]},
            ],
            "edges": [
                {"source": "series.one", "target": "episode.one"},
                {"source": "episode.one", "target": "scene.briefing"},
            ],
        },
    }


class EdgeTests(unittest.TestCase):
    def test_known_edges_come_from_their_own_book(self):
        self.assertEqual(EDGE_SOURCES["Mentalist"], "Ashes Without Number")
        self.assertEqual(EDGE_SOURCES["Spellcaster"], "Cities Without Number")

    def test_an_unknown_edge_is_refused_rather_than_assumed(self):
        with self.assertRaises(PsiEdgeError):
            EdgeGrants(edge="Warlock")

    def test_an_edge_may_not_grant_a_forbidden_discipline(self):
        problems = validate_edge(EdgeGrants(edge="Spellcaster", disciplines=("Precognition",)))
        self.assertTrue(any("may not grant" in p for p in problems))

    def test_a_partial_psychic_restriction_is_respected(self):
        psychic = Psychic(wisdom=10, constitution=10, disciplines={"Telepathy": 1},
                          restricted_discipline="Telepathy")
        problems = validate_edge(
            EdgeGrants(edge="Mentalist", disciplines=("Telekinesis",)), psychic=psychic
        )
        self.assertTrue(any("restricted to Telepathy" in p for p in problems))

    def test_two_edges_may_not_advance_the_same_discipline(self):
        problems = validate_edge(
            EdgeGrants(edge="Mentalist", disciplines=("Telepathy",)),
            existing=[EdgeGrants(edge="Mentalist", disciplines=("Telepathy",))],
        )
        self.assertTrue(any("already taken" in p for p in problems))

    def test_a_second_psionic_progress_track_is_refused(self):
        psychic = Psychic(wisdom=10, constitution=10, disciplines={"Telepathy": 1})
        problems = validate_edge(
            EdgeGrants(edge="Mentalist", resource="psi", grants_technique_progress=True),
            psychic=psychic,
        )
        self.assertTrue(any("second psionic progress track" in p for p in problems))

    def test_a_clean_mentalist_is_admissible(self):
        self.assertEqual(validate_edge(EdgeGrants(edge="Mentalist")), [])


class DeviceGrantTests(unittest.TestCase):
    def test_a_grant_is_active_only_while_its_device_is_carried(self):
        grants = (device_grant("see in the dark", source="implant.ocular"),)
        self.assertEqual(active_grants([], grants), ())
        self.assertEqual(active_grants(["implant.ocular"], grants), grants)

    def test_require_device_refuses_a_device_that_grants_nothing(self):
        with self.assertRaises(PsiEdgeError):
            require_device((device_grant("x", source="implant.a"),), "implant.b")

    def test_a_grant_is_still_never_a_selectable_option(self):
        with self.assertRaises(PsiAccessError):
            Grant(ability="Precognition", source="implant.a", selectable=True)


class FocusTests(unittest.TestCase):
    def test_a_focus_level_demands_a_quotation(self):
        with self.assertRaises(PsiEdgeError):
            FocusLevel(level=1, benefit="+1 Effort", citation=citation(quote="  "))

    def test_a_focus_may_not_leave_the_player_disciplines(self):
        with self.assertRaises(PsiEdgeError):
            PsychicTrainingFocus(discipline="Precognition",
                                 levels=(FocusLevel(1, "+1 Effort", citation()),))

    def test_a_quoted_focus_inside_telepathy_is_valid(self):
        focus = PsychicTrainingFocus(
            discipline="Telepathy",
            levels=(FocusLevel(1, "bonus psychic skill", citation()),),
        )
        self.assertEqual(focus.benefit_at(1), "bonus psychic skill")

    def test_levels_must_be_ordered_and_unique(self):
        with self.assertRaises(PsiEdgeError):
            PsychicTrainingFocus(
                discipline="Telepathy",
                levels=(FocusLevel(2, "b", citation()), FocusLevel(1, "a", citation())),
            )


class MutantTemplateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.catalogue = MutationCatalogue(
            [MutationEntry(id="mut.extra_joint", effect="bends further",
                           citation=citation())]
        )

    def test_an_untranscribed_mutation_is_refused(self):
        with self.assertRaises(PsiEdgeError):
            MutantTemplate(npc="npc.x", mutations=("mut.ghost",), catalogue=self.catalogue)

    def test_a_template_built_from_a_quoted_catalogue_is_valid(self):
        template = MutantTemplate(npc="npc.x", mutations=("mut.extra_joint",),
                                  catalogue=self.catalogue)
        self.assertFalse(template.ancestry_known)
        self.assertEqual(template.psi_discipline, "")

    def test_an_empty_catalogue_cannot_produce_a_mutant(self):
        with self.assertRaises(PsiEdgeError):
            MutantTemplate(npc="npc.x", mutations=("mut.anything",),
                           catalogue=MutationCatalogue())

    def test_mutant_can_be_a_pc(self):
        template = MutantTemplate(npc="npc.x", mutations=("mut.extra_joint",),
                                  catalogue=self.catalogue)
        assert_mutant_is_npc(template, is_player=False)
        assert_mutant_is_npc(template, is_player=True)


class WorldSessionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.session = WorldSession.from_dict(world_payload())

    def test_one_actor_one_sheet(self):
        self.session.register("pc.rookie", "sheet.rookie")
        with self.assertRaises(WorldSessionError):
            self.session.register("pc.other", "sheet.rookie")

    def test_an_actor_may_not_be_rebound_to_a_different_sheet(self):
        self.session.register("pc.rookie", "sheet.rookie")
        with self.assertRaises(WorldSessionError):
            self.session.register("pc.rookie", "sheet.impostor")

    def test_an_unmapped_actor_is_refused_rather_than_inferred(self):
        with self.assertRaises(WorldSessionError):
            self.session.sheet_for("pc.nobody")

    def test_identity_reads_the_same_actor_across_views(self):
        self.session.register("pc.rookie", "sheet.rookie")
        seen = self.session.identity("pc.rookie")
        self.assertEqual(seen["physical"], "loc.street")
        self.assertTrue(seen["social"])
        self.assertEqual(seen["sheet"], "sheet.rookie")

    def test_look_reports_devices_attached_to_the_place(self):
        self.session.register("pc.rookie", "sheet.rookie")
        self.session.move("pc.rookie", "loc.stair")
        seen = self.session.look("pc.rookie")
        self.assertEqual(seen["devices"], ("cyber.camera",))

    def test_an_impossible_route_is_refused(self):
        self.session.register("pc.rookie", "sheet.rookie")
        with self.assertRaises(WorldSessionError):
            self.session.move("pc.rookie", "loc.moon")

    def test_the_story_graph_offers_the_entry_scene(self):
        self.session.enter_scene("series.one")
        self.assertIn("episode.one", self.session.scenes_available())

    def test_an_unknown_scene_is_refused(self):
        with self.assertRaises(WorldSessionError):
            self.session.enter_scene("scene.ghost")


if __name__ == "__main__":
    unittest.main()
