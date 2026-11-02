"""DA, DNA and SNA stay three different things (#1042).

The issue's acceptance criteria are behavioural, so these tests are too: contradictory positions,
an unknown stance that is not neutral, identity reconciliation, fog of war, disagreement that is not
a friendship score, provenance that survives a fiction event, and persistence.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud.discourse import (  # noqa: E402
    Actor,
    DiscourseProfile,
    Event,
    SocialModelError,
    SocialWorld,
    render_actor_list,
    render_dossier,
)


def world() -> SocialWorld:
    w = SocialWorld()
    w.add_actor(Actor("romppainen", name="Dr. Harri Romppainen", aliases=["Harri"]))
    w.add_actor(Actor("witness", name="Woman in a raincoat"))
    w.add_actor(Actor("watcher", name="Man by the van"))
    w.add_actor(Actor("unsa", kind="organisation", name="UNSA"))
    w.profiles["romppainen"] = DiscourseProfile(
        actor="romppainen",
        values=["curiosity", "accountability"],
        demands=["the case is documented"],
        signifiers=["paper first"],
        uncertainty={"psi": "he will not say whether he believes it"},
    )
    return w


class ContradictionIsNotAnAverage(unittest.TestCase):
    def test_two_opposite_statements_are_both_kept(self):
        w = world()
        w.ingest(Event(id="e1", at="2026-11-01T10:00:00Z", kind="statement", actor="witness",
                       concept="van", polarity=-2, source="evidence", text="the van was there"))
        w.ingest(Event(id="e2", at="2026-11-01T11:00:00Z", kind="statement", actor="witness",
                       concept="van", polarity=2, source="evidence", text="no van, I misremembered"))
        stance = w.stance("witness", "van")
        self.assertIsNone(stance["value"], "opposites must not average into a middle")
        self.assertEqual(len(stance["conflicts"]), 1)
        self.assertEqual(len([p for p in w.positions if p.concept == "van"]), 2)

    def test_an_unasked_actor_has_no_stance_rather_than_a_neutral_one(self):
        w = world()
        stance = w.stance("witness", "psi")
        self.assertTrue(stance["unknown"])
        self.assertIsNone(stance["value"], "unknown is not 0 and not 'neutral'")

    def test_a_single_claim_reports_its_value_and_its_source(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="statement", actor="watcher", concept="unsa",
                       polarity=-1, source="evidence"))
        stance = w.stance("watcher", "unsa")
        self.assertEqual(stance["value"], -1)
        self.assertFalse(stance["unknown"])
        self.assertEqual(stance["sources"], ["evidence"])


class ProvenanceIsLoadBearing(unittest.TestCase):
    def test_a_fiction_claim_does_not_overwrite_an_evidence_claim(self):
        w = world()
        w.ingest(Event(id="e1", at="t1", kind="statement", actor="witness", concept="van",
                       polarity=-2, source="evidence"))
        w.ingest(Event(id="e2", at="t2", kind="statement", actor="witness", concept="van",
                       polarity=2, source="fiction", text="an LLM-generated rumour"))
        stance = w.stance("witness", "van")
        self.assertIsNone(stance["value"])
        self.assertEqual(stance["sources"], ["evidence", "fiction"])
        self.assertTrue(stance["conflicts"], "the disagreement must be visible, not smoothed")

    def test_an_unknown_source_is_refused(self):
        w = world()
        with self.assertRaises(SocialModelError):
            w.ingest(Event(id="e1", at="t", kind="statement", actor="witness",
                           concept="van", polarity=1, source="vibes"))


class IdentityReconciliation(unittest.TestCase):
    def test_the_same_person_under_two_names_is_one_actor(self):
        w = world()
        w.add_actor(Actor("witness", name="Woman in a raincoat", aliases=["the woman"]))
        self.assertEqual(w.resolve("the woman"), "witness")
        self.assertEqual(w.resolve("WOMAN IN A RAINCOAT"), "witness")

    def test_an_ambiguous_name_is_refused_rather_than_guessed(self):
        w = world()
        w.add_actor(Actor("other", name="Woman in a raincoat"))
        with self.assertRaises(SocialModelError):
            w.resolve("woman in a raincoat")

    def test_events_survive_reconciliation(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="statement", actor="witness", concept="badge",
                       polarity=1, source="evidence"))
        w.add_actor(Actor("witness", name="Woman in a raincoat", aliases=["coat"]))
        self.assertEqual(len([p for p in w.positions if p.actor == "witness"]), 1)


class FogOfWar(unittest.TestCase):
    def test_a_tie_the_viewer_cannot_know_is_hidden(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="contact", actor="watcher", other="unsa",
                       tie="obligation", other_known_by=["romppainen"]))
        seen_by_recruit = w.dossier("watcher", viewer="recruit")
        seen_by_romppainen = w.dossier("watcher", viewer="romppainen")
        self.assertEqual(seen_by_recruit["ties"], [])
        self.assertEqual(len(seen_by_romppainen["ties"]), 1)

    def test_a_dossier_reports_only_the_concepts_that_were_observed(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="statement", actor="witness", concept="badge",
                       polarity=1, source="evidence"))
        dossier = w.dossier("witness")
        self.assertIn("badge", dossier["stances"])
        self.assertNotIn("psi", dossier["stances"])


class NetworkIsTyped(unittest.TestCase):
    def test_the_graph_has_kinds_and_no_affinity(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="contact", actor="romppainen", other="witness",
                       tie="affiliation"))
        graph = w.network("romppainen", depth=1)
        self.assertEqual(graph["edges"][0]["kind"], "affiliation")
        self.assertNotIn("weight", graph["edges"][0])
        self.assertNotIn("hostility", json.dumps(graph))

    def test_two_npcs_can_disagree_without_any_score_changing(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="statement", actor="witness", concept="van", polarity=-2))
        w.ingest(Event(id="e2", at="t", kind="statement", actor="watcher", concept="van", polarity=2))
        self.assertEqual(w.stance("witness", "van")["value"], -2)
        self.assertEqual(w.stance("watcher", "van")["value"], 2)
        self.assertEqual(w.actors["witness"].kind, "person")


class Persistence(unittest.TestCase):
    def test_a_world_round_trips_through_json(self):
        w = world()
        w.ingest(Event(id="e1", at="t", kind="statement", actor="witness", concept="van", polarity=-1))
        w.ingest(Event(id="e2", at="t", kind="affiliation", actor="romppainen", concept="unsa",
                       role="SSA"))
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "world.json")
            w.save(path)
            restored = SocialWorld.load(path)
        self.assertEqual(restored.to_dict(), w.to_dict())
        self.assertEqual(restored.stance("witness", "van")["value"], -1)

    def test_reingesting_the_same_event_changes_nothing(self):
        w = world()
        event = Event(id="e1", at="t", kind="statement", actor="witness", concept="van", polarity=-1)
        w.ingest(event)
        w.ingest(event)
        self.assertEqual(len(w.positions), 1)


class PlayingIt(unittest.TestCase):
    """The in-game surface: what a recruit actually reads."""

    def test_the_seed_world_loads_and_renders_a_dossier(self):
        from nopunk_mud.social_seed import seed_world

        w = seed_world()
        text = render_dossier(w, "Romppainen")
        self.assertIn("Dr. Harri Romppainen", text)
        self.assertIn("curiosity", text)

    def test_a_conflict_is_shown_rather_than_averaged(self):
        from nopunk_mud.social_seed import seed_world

        text = render_dossier(seed_world(), "Romppainen")
        self.assertIn("CONFLICT", text, "the fiction rumour must not silently become a position")

    def test_an_unknown_name_lists_instead_of_guessing(self):
        from nopunk_mud.social_seed import seed_world

        text = render_dossier(seed_world(), "Somebody Nobody Met")
        self.assertIn("Use 'dossier' for the list", text)

    def test_a_tie_the_recruit_was_not_told_about_stays_hidden(self):
        from nopunk_mud.social_seed import seed_world

        w = seed_world()
        self.assertIn("none you have been told about", render_dossier(w, "Man by the van"))
        self.assertIn("unsa", render_dossier(w, "Man by the van", viewer="romppainen"))

    def test_the_actor_list_names_everyone_on_record(self):
        from nopunk_mud.social_seed import seed_world

        text = render_actor_list(seed_world())
        for name in ("Romppainen", "Woman in a raincoat", "UNSA"):
            self.assertIn(name, text)


if __name__ == "__main__":
    unittest.main()
