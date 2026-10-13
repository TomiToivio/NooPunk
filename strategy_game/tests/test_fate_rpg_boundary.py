"""Completion tests for the Fate-based RPG layer (issue #389): attribution, TAGs, boundary.

Executable-code tests only, per #271. These cover the acceptance items the first slice left open —
the attribution the module points at, the shared typed tag vocabulary, the adapter boundary to the
unbuilt strategy layer, and the netrunning example — and they are written so they can fail.
"""
from __future__ import annotations

import os
import subprocess
import sys
import unittest
from pathlib import Path
from random import Random

from strategy_game.rpg import attribution
from strategy_game.rpg.boundary import (
    BOUNDARY_SCHEMA_VERSION,
    NOT_THIS_LAYER,
    PAYLOAD_KEYS,
    SHEET_KEYS,
    BoundaryError,
    LeaderRpgLayer,
)
from typing import cast

from strategy_game.rpg.fate import (
    Action,
    Character,
    Resolution,
    ResourceError,
    demo_investigation,
    demo_netrunning,
)
from strategy_game.characters import TAG_KINDS, Tag
from strategy_game.core import WorldState

REPO = Path(__file__).resolve().parents[2]


class AttributionTests(unittest.TestCase):
    def test_the_fate_attribution_and_unofficial_notice_exist(self) -> None:
        self.assertIn("Evil Hat Productions", attribution.FATE_ATTRIBUTION)
        self.assertIn("Creative Commons Attribution 3.0", attribution.FATE_ATTRIBUTION)
        self.assertIn("not sponsored or endorsed", attribution.UNOFFICIAL_NOTICE)
        self.assertTrue(attribution.REUSE_BASIS)

    def test_the_upstream_licences_are_kept_apart(self) -> None:
        licences = attribution.REFERENCE_LICENCES
        self.assertEqual(licences["fate_core_srd"]["licence"], "CC BY 3.0")
        self.assertIn("NC-SA", licences["transhumanitys_fate"]["licence"])
        self.assertIn("NC-SA", licences["eclipse_phase_2e"]["licence"])
        for key in ("fate_core_srd", "transhumanitys_fate", "eclipse_phase_2e"):
            self.assertTrue(licences[key]["role"], key)

    def test_the_distribution_licence_is_left_to_the_author(self) -> None:
        """The layer must not pick a licence: that decision is the author's (issue #200)."""
        self.assertIn("author's decision", attribution.DISTRIBUTION_DECISION)
        self.assertIn("#200", attribution.DISTRIBUTION_DECISION)


class SharedTagTests(unittest.TestCase):
    def test_character_tags_use_the_shared_vocabulary(self) -> None:
        actor = Character(
            "a", "Agent", ["Focused"],
            tags=(Tag("belief", "the commons against the enclosures"),
                  Tag("competence", "forensic reconstruction"),
                  Tag("equipment", "secure BCI")),
        )
        self.assertEqual(actor.tags_of_kind("competence")[0].value, "forensic reconstruction")
        self.assertEqual(len(actor.tags_of_kind("belief")), 1)
        self.assertEqual(actor.tags_of_kind("asset"), ())

    def test_the_tag_kinds_are_the_shared_ones(self) -> None:
        self.assertEqual(
            TAG_KINDS, ("belief", "competence", "equipment", "relationship", "asset", "goal")
        )

    def test_a_bare_string_tag_is_refused(self) -> None:
        with self.assertRaises(ResourceError):
            Character("a", "Agent", [], tags=("not a typed tag",))  # type: ignore[arg-type]

    def test_a_duplicate_tag_is_refused(self) -> None:
        with self.assertRaises(ResourceError):
            Character("a", "Agent", [], tags=(Tag("belief", "x"), Tag("belief", "x")))

    def test_an_unknown_tag_kind_is_refused_by_the_vocabulary(self) -> None:
        with self.assertRaises(ValueError):
            Tag("mood", "brooding")


class BoundaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.agent = Character("agent-1", "Field Investigator", ["Precognitive Impressions"],
                               skills={"Technology": 2, "Psi": 1}, natural_psi=True,
                               psi_abilities=["precognitive_impressions"])
        self.layer = LeaderRpgLayer([self.agent])

    def test_the_layer_fills_the_reserved_leader_rpg_seam(self) -> None:
        self.assertTrue(hasattr(self.layer, "describe"))
        payload = self.layer.describe(WorldState())
        self.assertEqual(payload["schema_version"], BOUNDARY_SCHEMA_VERSION)
        self.assertLessEqual(set(payload), set(PAYLOAD_KEYS))

    def test_the_port_is_satisfied_even_without_a_world_state(self) -> None:
        self.assertEqual(set(self.layer.describe().keys()), set(PAYLOAD_KEYS))

    def test_the_payload_carries_nothing_strategic(self) -> None:
        """Check keys, not prose: the payload *declares* what is excluded, so the words appear."""
        payload = self.layer.describe()
        forbidden_keys = {"victory", "score", "treasury", "upkeep", "turn", "economy",
                          "faction_actions", "resources", "modifiers"}
        self.assertFalse(forbidden_keys & set(payload), payload.keys())
        for sheet in payload["characters"]:
            self.assertFalse(forbidden_keys & set(sheet), sheet.keys())

    def test_the_layer_declares_what_it_is_not(self) -> None:
        payload = self.layer.describe()
        self.assertEqual(tuple(payload["excluded"]), NOT_THIS_LAYER)
        for forbidden in NOT_THIS_LAYER:
            self.assertFalse(hasattr(self.layer, forbidden.replace(" ", "_")))

    def test_a_sheet_exposes_exactly_the_declared_keys(self) -> None:
        self.assertEqual(set(self.layer.sheet("agent-1")), set(SHEET_KEYS))

    def test_resolution_is_deterministic_from_a_seed(self) -> None:
        first = self.layer.resolve("agent-1", Action.OVERCOME, "Technology", 2, seed=11)
        second = self.layer.resolve("agent-1", Action.OVERCOME, "Technology", 2, seed=11)
        self.assertEqual(first, second)
        self.assertEqual(first.total - first.difficulty, first.shifts)
        self.assertEqual(len(first.dice), 4)

    def test_different_seeds_can_differ(self) -> None:
        rolls = {self.layer.resolve("agent-1", Action.OVERCOME, "Psi", 1, seed=s).dice for s in range(6)}
        self.assertGreater(len(rolls), 1)

    def test_unknown_characters_are_refused(self) -> None:
        with self.assertRaises(BoundaryError):
            self.layer.sheet("nobody")
        with self.assertRaises(BoundaryError):
            self.layer.resolve("nobody", Action.OVERCOME, "Technology", 1, seed=1)

    def test_duplicate_character_ids_are_refused(self) -> None:
        with self.assertRaises(BoundaryError):
            LeaderRpgLayer([self.agent, Character("agent-1", "Twin", [])])


class SeparationTests(unittest.TestCase):
    """The RPG layer must not drag the unapproved strategy or political layers in behind it."""

    def test_the_rpg_modules_import_none_of_the_unapproved_layers(self) -> None:
        """Source-level, because the package ``__init__`` imports its own vocabulary modules.

        Importing ``strategy_game.rpg.fate`` executes ``strategy_game/__init__.py``, whose pinned
        ``__all__`` pulls in the data-only political vocabulary — so a runtime module list would
        accuse the layer of a dependency it does not have. The claim that matters is checkable
        statically: these two modules import none of the strategy or political machinery.
        """
        import re
        from strategy_game.rpg import boundary, fate

        forbidden = ("politics", "political", "cyber", "local_slice", "global_slice", "faction_creation")
        for module in (fate, boundary):
            source = Path(module.__file__).read_text(encoding="utf-8")
            for line in source.splitlines():
                if not re.match(r"^\s*(from|import)\s", line):
                    continue
                for name in forbidden:
                    self.assertNotIn(name, line, f"{module.__name__}: {line.strip()}")

        # The one deliberate dependency is the shared tag vocabulary, and it is named on purpose.
        fate_source = Path(fate.__file__).read_text(encoding="utf-8")
        self.assertIn("from ..characters import Tag", fate_source)

    def test_the_rpg_layer_imports_without_third_party_distributions(self) -> None:
        script = (
            "import sys;"
            "sys.path = [p for p in sys.path"
            " if 'site-packages' not in p and 'dist-packages' not in p];"
            "import strategy_game.rpg.fate, strategy_game.rpg.boundary;"
            "print('ok')"
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(REPO)
        done = subprocess.run([sys.executable, "-c", script], cwd=REPO,
                              capture_output=True, text=True, timeout=180, env=env)
        self.assertEqual(done.returncode, 0, done.stderr[-400:])
        self.assertIn("ok", done.stdout)


class ScenarioTests(unittest.TestCase):
    def test_the_investigation_resolves_a_cyber_and_a_psi_check_on_one_engine(self) -> None:
        scene = demo_investigation(3)
        cyber = cast(Resolution, scene["cyber"])
        psi = cast(Resolution, scene["psi"])
        self.assertEqual(cyber.action, Action.OVERCOME)
        self.assertEqual(psi.action, Action.CREATE_ADVANTAGE)
        self.assertEqual(scene, demo_investigation(3))

    def test_the_netrunning_example_requires_a_foothold_first(self) -> None:
        scene = demo_netrunning(5)
        access = cast(Resolution, scene["access"])
        intrusion = cast(Resolution, scene["intrusion"])
        self.assertTrue(scene["access_required"])
        self.assertEqual(access.action, Action.CREATE_ADVANTAGE)
        self.assertEqual(intrusion.action, Action.OVERCOME)
        self.assertIn("#344", str(scene["note"]))
        self.assertEqual(scene, demo_netrunning(5))

    def test_the_same_engine_resolves_both_scenes(self) -> None:
        for scene in (demo_investigation(1), demo_netrunning(1)):
            for key in ("cyber", "psi", "access", "intrusion"):
                if key in scene:
                    outcome = cast(Resolution, scene[key])
                    self.assertEqual(len(outcome.dice), 4)
                    self.assertIsInstance(outcome.outcome.value, str)


if __name__ == "__main__":
    unittest.main()
