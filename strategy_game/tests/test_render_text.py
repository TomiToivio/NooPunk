"""Tests for the text renderer / interface spike (issue #347).

Executable-code tests only, per #271: they exercise the provider seam, the determinism of the
rendered text, the pinned view model it must not widen, and the §7a import guard.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from strategy_game.characters import load_character_cards
from strategy_game.core import Asset, Faction, Leader, Location, WorldState
from strategy_game.render.text import (
    FORBIDDEN_INFERENCE_KEYS,
    RENDER_SCHEMA_VERSION,
    TextMapProvider,
    render_board_text,
    render_roster_text,
    state_from_local_slice,
)
from strategy_game.view import board_view

REPO = Path(__file__).resolve().parents[2]
PINNED_BOARD_KEYS = {"schema_version", "locations", "network_nodes", "network_edges", "assets"}


def _keys(obj: object) -> set[str]:
    """Every mapping key anywhere in a payload."""
    found: set[str] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            found.add(str(key))
            found |= _keys(value)
    elif isinstance(obj, list):
        for item in obj:
            found |= _keys(item)
    return found


class ProviderTests(unittest.TestCase):
    def test_the_provider_fills_the_reserved_map_seam(self) -> None:
        provider = TextMapProvider()
        self.assertTrue(hasattr(provider, "describe"))
        payload = provider.describe(WorldState())
        self.assertEqual(payload["schema_version"], RENDER_SCHEMA_VERSION)
        self.assertEqual(
            set(payload),
            {"schema_version", "world_schema_version", "locations", "network_nodes", "network_edges", "assets"},
        )

    def test_the_provider_infers_no_borders_travel_control_or_ownership(self) -> None:
        payload = TextMapProvider().describe(state_from_local_slice())
        for key in FORBIDDEN_INFERENCE_KEYS:
            self.assertNotIn(key, _keys(payload), f"renderer invented {key!r}")

    def test_the_board_projection_is_not_widened(self) -> None:
        self.assertEqual(set(board_view(WorldState())), PINNED_BOARD_KEYS)


class RenderTests(unittest.TestCase):
    def test_rendering_is_deterministic(self) -> None:
        self.assertEqual(render_board_text(state_from_local_slice()), render_board_text(state_from_local_slice()))

    def test_every_location_and_route_appears(self) -> None:
        state = state_from_local_slice()
        text = render_board_text(state)
        self.assertIn("locations:", text)
        self.assertIn("routes", text)
        for location in state.locations:
            self.assertIn(location.label, text)
        for edge in state.edges:
            self.assertIn(edge.source, text)
            self.assertIn(edge.target, text)

    def test_the_empty_scaffold_says_so(self) -> None:
        self.assertIn("empty scaffold board", render_board_text(WorldState()))

    def test_the_local_slice_adapter_copies_declared_content_only(self) -> None:
        state = state_from_local_slice()
        self.assertEqual(len(state.locations), 8)
        self.assertEqual(len(state.edges), 7)
        self.assertEqual(len(state.factions), 3)
        self.assertEqual(len(state.leaders), 12)
        self.assertTrue(all(edge.layer == "route" for edge in state.edges))

    def test_assets_and_leaders_render_with_labels_not_ids(self) -> None:
        state = WorldState(
            locations=[Location(identifier="civic", label="Civic Centre")],
            factions=[Faction(identifier="cpu", name="Communist Party")],
            assets=[Asset(identifier="a1", label="Printing press", location_id="civic", owner_faction_id="cpu")],
            leaders=[Leader(identifier="cpu1", name="CPU Chair", attributes={"politics": "chair"})],
        )
        text = render_board_text(state)
        self.assertIn("Printing press at Civic Centre, held by Communist Party", text)
        self.assertIn("CPU Chair [cpu1]", text)

    def test_the_card_faces_never_print_gm_notes(self) -> None:
        roster = load_character_cards()
        text = render_roster_text(roster)
        self.assertIn("cards [" + RENDER_SCHEMA_VERSION + "]", text)
        for card in roster:
            if card.gm_notes:
                self.assertNotIn(card.gm_notes, text)


class CommandLineTests(unittest.TestCase):
    def _run(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "strategy_game.render", *args],
            cwd=REPO, capture_output=True, text=True, timeout=180,
        )

    def test_default_run_draws_the_local_slice(self) -> None:
        done = self._run()
        self.assertEqual(done.returncode, 0, done.stderr[-500:])
        self.assertIn("board [", done.stdout)
        self.assertIn("locations:", done.stdout)

    def test_empty_run_draws_the_scaffold(self) -> None:
        done = self._run("--empty")
        self.assertEqual(done.returncode, 0, done.stderr[-500:])
        self.assertIn("empty scaffold board", done.stdout)

    def test_json_mode_is_the_provider_payload(self) -> None:
        done = self._run("--json")
        self.assertEqual(done.returncode, 0, done.stderr[-500:])
        payload = json.loads(done.stdout)
        self.assertEqual(payload["schema_version"], RENDER_SCHEMA_VERSION)
        # The payload renames nothing: its own schema_version is the renderer's, and the world's
        # travels as world_schema_version, so the board keys are the pinned ones minus that name.
        self.assertEqual(
            set(payload) - {"schema_version", "world_schema_version"},
            PINNED_BOARD_KEYS - {"schema_version"},
        )

    def test_cards_flag_appends_the_roster(self) -> None:
        done = self._run("--empty", "--cards")
        self.assertEqual(done.returncode, 0, done.stderr[-500:])
        self.assertIn("cards [", done.stdout)


class OfflineImportTests(unittest.TestCase):
    """VISION.md §7a: runnable from source, offline, no account, no service, no model client.

    A subprocess whose ``sys.path`` carries no third-party distributions must still import every
    crossover module. That is a code assertion, so #271 permits it — and it is the one test that
    mechanically protects the "buildable and runnable from source" requirement.
    """

    def test_crossover_modules_import_without_site_packages(self) -> None:
        script = (
            "import sys;"
            "sys.path = [p for p in sys.path"
            " if 'site-packages' not in p and 'dist-packages' not in p];"
            "import strategy_game.core, strategy_game.view, strategy_game.characters,"
            " strategy_game.tabletop, strategy_game.render;"
            "print('ok')"
        )
        env = dict(os.environ)
        env["PYTHONPATH"] = str(REPO)
        done = subprocess.run(
            [sys.executable, "-c", script], cwd=REPO, capture_output=True, text=True, timeout=180, env=env,
        )
        self.assertEqual(done.returncode, 0, done.stderr[-600:])
        self.assertIn("ok", done.stdout)


if __name__ == "__main__":
    unittest.main()
