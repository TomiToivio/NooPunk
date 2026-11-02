"""The discourse model reaches a player (#1042).

`ideology.py` owns the rules and its own tests. This file covers the seam that was missing: a seeded
world a recruit can read in game, with the layers printed separately rather than merged.

Written with `unittest`: CI discovers with `unittest` and does not install pytest.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mud"))

from nopunk_mud.ideology import Discourse, IdeologyError  # noqa: E402
from nopunk_mud.ideology_seed import (  # noqa: E402
    render_actor,
    render_overview,
    render_pair,
    seed_discourse,
    viewer_scope,
)


class TheSeed(unittest.TestCase):
    def test_the_seed_builds_a_world(self):
        discourse = seed_discourse()
        self.assertGreaterEqual(len(discourse.actors), 3)
        self.assertTrue(discourse.statements)
        self.assertTrue(viewer_scope())

    def test_every_seeded_statement_names_a_real_actor_and_concept(self):
        discourse = seed_discourse()
        for statement in discourse.statements:
            self.assertIn(statement.actor, discourse.actors)
            self.assertIn(statement.concept, discourse.concepts)


class WhatAPlayerReads(unittest.TestCase):
    def test_a_rumour_is_printed_as_a_rumour(self):
        text = render_actor(seed_discourse(), "romppainen")
        self.assertIn("rumour", text)
        self.assertIn("NOT evidence", text)

    def test_positions_on_all_claims_and_on_evidence_are_printed_separately(self):
        text = render_actor(seed_discourse(), "romppainen")
        self.assertIn("positions (all claims)", text)
        self.assertIn("positions (evidence only)", text)

    def test_a_secret_relationship_is_withheld_with_its_count(self):
        text = render_actor(seed_discourse(), "watcher")
        self.assertIn("relationships withheld", text)
        self.assertNotIn("somebody hired him", text)

    def test_overview_names_the_contested_signifier(self):
        text = render_overview(seed_discourse())
        self.assertIn("Contested signifiers", text)
        self.assertIn("unsa", text)

    def test_agreement_and_trust_are_reported_side_by_side(self):
        text = render_pair(seed_discourse(), "romppainen", "unsa_command")
        self.assertIn("ideological overlap", text)
        self.assertIn("personal trust", text)
        self.assertIn("do not imply each other", text)

    def test_an_unknown_actor_is_refused_with_a_pointer(self):
        text = render_actor(seed_discourse(), "nobody")
        self.assertIn("Use 'dossier' for the list", text)


class Persistence(unittest.TestCase):
    def test_the_world_round_trips(self):
        discourse = seed_discourse()
        restored = Discourse.from_dict(discourse.to_dict())
        self.assertEqual(restored.to_dict(), discourse.to_dict())

    def test_an_unknown_concept_is_refused_by_the_model(self):
        from nopunk_mud.ideology import Statement

        discourse = seed_discourse()
        with self.assertRaises(IdeologyError):
            discourse.articulate(
                Statement(actor="romppainen", concept="no-such-concept", stance="support")
            )


if __name__ == "__main__":
    unittest.main()
