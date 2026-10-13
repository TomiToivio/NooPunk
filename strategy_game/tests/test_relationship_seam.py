"""Tests for the RPG-relationship–to–strategic-consequence seam (issue #323).

Executable-code tests only (#271): they exercise the boundary — that it is signature-only, that its
default source declares nothing rather than zero, that it *reuses* the council layer instead of
re-implementing it, and that it applies nothing and pulls in no RPG-layer code.
"""
from __future__ import annotations

import json
import subprocess
import sys
import typing
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:  # pragma: no cover - import bootstrap, mirrors the sibling test modules
    sys.path.insert(0, str(ROOT))

from strategy_game.council import load_council  # noqa: E402
from strategy_game.relationship_seam import (  # noqa: E402
    APPLIED,
    MECHANICS_OWNER,
    SEAM_ID,
    SEAM_METHODS,
    NullRelationshipSource,
    RPGRelationshipSource,
    strategic_consequence_view,
)
from strategy_game.relationships import RelationshipSet  # noqa: E402


class _EchoSource:
    """A source that echoes a declared mapping. It resolves nothing — it only returns names."""

    def __init__(self, states: dict[str, str], edge_ids: tuple[str, ...]) -> None:
        self._states = dict(states)
        self._edge_ids = tuple(edge_ids)

    def relationship_states(self, owner_id: str) -> dict[str, str]:
        return dict(self._states)

    def declared_edge_ids(self, owner_id: str) -> tuple[str, ...]:
        return self._edge_ids


class SignatureOnlyTests(unittest.TestCase):
    def test_the_protocol_declares_exactly_the_two_read_methods(self) -> None:
        self.assertEqual(SEAM_METHODS, ("relationship_states", "declared_edge_ids"))
        for name in SEAM_METHODS:
            with self.subTest(method=name):
                self.assertTrue(hasattr(RPGRelationshipSource, name))

    def test_the_null_source_satisfies_the_protocol(self) -> None:
        self.assertIsInstance(NullRelationshipSource(), RPGRelationshipSource)

    def test_the_null_source_declares_nothing_rather_than_zero(self) -> None:
        source = NullRelationshipSource()
        self.assertEqual(source.relationship_states("anyone"), {})
        self.assertEqual(source.declared_edge_ids("anyone"), ())
        # Nothing numeric is returned: absence is UNMODELLED, not a neutral-zero edge.
        self.assertFalse(
            any(isinstance(value, (int, float)) for value in source.relationship_states("x").values())
        )

    def test_an_echo_source_returns_only_the_names_it_was_given(self) -> None:
        source = _EchoSource({"mentor": "indebted"}, ("edge_a",))
        self.assertEqual(source.relationship_states("x"), {"mentor": "indebted"})
        self.assertEqual(source.declared_edge_ids("x"), ("edge_a",))
        self.assertIsInstance(source, RPGRelationshipSource)


class ConsequenceViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.council = load_council()
        self.example = self.council.worked_example_council()
        self.mission = self.example.missions[0]
        self.edges = RelationshipSet()

    def test_the_view_reuses_the_council_reading_and_adds_the_seam_metadata(self) -> None:
        council_reading = self.council.strategic_consequences(self.mission, self.edges)
        view = strategic_consequence_view(self.council, self.mission, self.edges)
        for key, value in council_reading.items():
            with self.subTest(key=key):
                self.assertEqual(view[key], value)
        self.assertEqual(view["seam"], SEAM_ID)
        self.assertIs(view["applied"], False)
        self.assertEqual(view["mechanics_owner"], MECHANICS_OWNER)

    def test_the_view_applies_nothing(self) -> None:
        view = strategic_consequence_view(self.council, self.mission, self.edges)
        self.assertIs(view["applied"], APPLIED)
        self.assertIs(view["applied"], False)
        self.assertIn("nothing is applied", json.dumps(view))

    def test_the_view_carries_the_source_read_and_never_a_number(self) -> None:
        source = _EchoSource({"mentor": "indebted"}, ("edge_a",))
        view = strategic_consequence_view(self.council, self.mission, self.edges, source=source)
        self.assertEqual(view["source_states"], {"mentor": "indebted"})
        self.assertEqual(view["source_edge_ids"], ["edge_a"])
        for key, value in view["source_states"].items():
            with self.subTest(key=key):
                self.assertNotIsInstance(value, (int, float))

    def test_the_view_does_not_mutate_its_inputs(self) -> None:
        before = json.dumps(self.mission.to_dict(), sort_keys=True)
        strategic_consequence_view(self.council, self.mission, self.edges)
        self.assertEqual(json.dumps(self.mission.to_dict(), sort_keys=True), before)
        self.assertEqual(len(self.edges), 0)

    def test_the_view_is_json_serializable(self) -> None:
        json.dumps(strategic_consequence_view(self.council, self.mission, self.edges))


class NoRPGDependencyTests(unittest.TestCase):
    """The seam is a boundary: it must not pull the RPG layer (#389) into the strategy load path."""

    def test_importing_and_using_the_seam_imports_no_rpg_layer(self) -> None:
        code = (
            "import sys, strategy_game.relationship_seam as s;"
            "from strategy_game.council import load_council;"
            "from strategy_game.relationships import RelationshipSet;"
            "c = load_council(); m = c.worked_example_council().missions[0];"
            "s.strategic_consequence_view(c, m, RelationshipSet());"
            "print(sorted(x for x in sys.modules if x.startswith('strategy_game.rpg')))"
        )
        result = subprocess.run(
            [sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "[]", f"the seam pulled in the RPG layer: {result.stdout}")

    def test_the_module_source_imports_nothing_from_the_rpg_package(self) -> None:
        import strategy_game.relationship_seam as seam

        text = Path(seam.__file__).read_text(encoding="utf-8")
        self.assertNotIn("from .rpg", text)
        self.assertNotIn("from strategy_game.rpg", text)
        self.assertNotIn("import rpg", text)


if __name__ == "__main__":
    unittest.main()
