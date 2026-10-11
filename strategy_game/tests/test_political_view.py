"""Runtime contracts for the Layer II rendering hook (issue #282).

`political.py` owns the political vocabulary and `test_political_contracts.py` guards it: role and
mode value sets, serialization, provenance separation, structural queries, the no-numeric
invariant and the no-LaclauGPT-import isolation. **None of that is repeated here.**

What was missing was a *view*. `view.py` rendered `WorldState` only, so a `PoliticalField` had
nothing to draw from it. This file pins `political_view` and nothing else.

Executable-code contracts only, per AGENTS.md's code-only testing policy. Two properties matter
most:

* **the hook takes the field explicitly.** Integrating Layer II into `WorldState` is a Gate D
  decision that has not been made, so the rendering hook must not reach into the world state to
  find a field -- that would perform the integration by the back door.
* **absence stays absent.** A tie with no recorded `mode` and a signifier with no recorded `role`
  must render as `None`, not be filled in with a plausible default.
"""
import ast
import inspect
import json
import textwrap
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game.core import Faction, Location, WorldState  # noqa: E402
from strategy_game.political import (  # noqa: E402
    Articulation,
    CommunicativeTie,
    Demand,
    Frontier,
    PoliticalField,
    PoliticalFormation,
    PowerMode,
    Signifier,
    SignifierRole,
)
from strategy_game.view import board_view, political_view  # noqa: E402

#: Key tokens that would mean a metric leaked into the rendered panel.
METRIC_TOKENS = ("score", "strength", "stability", "confidence", "threshold", "cost",
                 "power", "level", "weight", "reach", "influence")


def empty_field() -> PoliticalField:
    return PoliticalField()


def populated_field() -> PoliticalField:
    """A small, entirely illustrative field. No real actor, party or place appears."""
    return PoliticalField(
        demands=[Demand("d1", "An example demand")],
        signifiers=[Signifier("s1", "An example signifier", SignifierRole.EMPTY)],
        articulations=[Articulation("s1", "d1")],
        frontiers=[Frontier("fr1", "s1", ["d1"], [])],
        ties=[CommunicativeTie("fo1", "fo2", PowerMode.SWITCHING)],
        formations=[PoliticalFormation("fo1", "An example formation", ["s1"])],
    )


class PanelShapeTests(unittest.TestCase):
    def test_the_panel_exposes_the_expected_sections(self):
        self.assertEqual(
            set(political_view(populated_field())),
            {"schema_version", "signifiers", "demands", "formations", "frontiers",
             "articulations", "ties"},
        )

    def test_an_empty_field_renders_every_section_empty(self):
        view = political_view(empty_field())
        self.assertEqual(view["schema_version"], "political-1")
        for key in ("signifiers", "demands", "formations", "frontiers", "articulations", "ties"):
            self.assertEqual(view[key], [], key)

    def test_the_panel_carries_the_fields_own_schema_version(self):
        self.assertEqual(political_view(PoliticalField(schema_version="political-9"))["schema_version"],
                         "political-9")

    def test_the_panel_mirrors_the_field(self):
        view = political_view(populated_field())
        self.assertEqual(view["signifiers"][0],
                         {"id": "s1", "label": "An example signifier", "role": "empty"})
        self.assertEqual(view["demands"][0], {"id": "d1", "text": "An example demand"})
        self.assertEqual(view["articulations"][0], {"signifier_id": "s1", "demand_id": "d1"})
        self.assertEqual(view["formations"][0],
                         {"id": "fo1", "label": "An example formation", "signifier_ids": ["s1"]})
        self.assertEqual(view["frontiers"][0],
                         {"id": "fr1", "signifier_id": "s1",
                          "included_demand_ids": ["d1"], "excluded_demand_ids": []})

    def test_a_frontier_keeps_its_two_sides_separate(self):
        field = PoliticalField(frontiers=[Frontier("fr1", "s1", ["d1"], ["d2", "d3"])])
        frontier = political_view(field)["frontiers"][0]
        self.assertEqual(frontier["included_demand_ids"], ["d1"])
        self.assertEqual(frontier["excluded_demand_ids"], ["d2", "d3"])

    def test_the_panel_is_json_serializable(self):
        json.dumps(political_view(populated_field()))


class AbsenceStaysAbsentTests(unittest.TestCase):
    """A recorded absence must never be rendered as a plausible default."""

    def test_an_unrecorded_signifier_role_renders_as_none(self):
        self.assertIsNone(political_view(PoliticalField(signifiers=[Signifier("s1", "x")]))
                          ["signifiers"][0]["role"])

    def test_an_unrecorded_power_mode_renders_as_none(self):
        self.assertIsNone(political_view(PoliticalField(ties=[CommunicativeTie("a", "b")]))
                          ["ties"][0]["mode"])

    def test_a_recorded_role_and_mode_render_as_their_declared_labels(self):
        view = political_view(PoliticalField(
            signifiers=[Signifier("s1", "x", SignifierRole.NODAL)],
            ties=[CommunicativeTie("a", "b", PowerMode.PROGRAMMING)],
        ))
        self.assertEqual(view["signifiers"][0]["role"], "nodal")
        self.assertEqual(view["ties"][0]["mode"], "programming")


class GateDBoundaryTests(unittest.TestCase):
    """The hook must render a passed-in field, not perform the integration itself."""

    def test_the_hook_takes_the_field_as_an_argument(self):
        parameters = list(inspect.signature(political_view).parameters)
        self.assertEqual(parameters, ["field"])

    def test_the_world_state_is_not_read_by_the_hook(self):
        """Structural, not textual: the docstring may *discuss* the world state freely."""
        tree = ast.parse(textwrap.dedent(inspect.getsource(political_view)))
        function = next(node for node in ast.walk(tree)
                        if isinstance(node, ast.FunctionDef) and node.name == "political_view")
        self.assertNotIn(
            "WorldState",
            {node.id for node in ast.walk(function) if isinstance(node, ast.Name)},
            "the hook must not name WorldState",
        )
        # Every attribute read must root on the `field` parameter or on a name bound *inside*
        # this function (the comprehension variables). Anything else would be reaching outside it.
        bound = {"field"} | {
            node.id for node in ast.walk(function)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
        }
        receivers = {
            node.value.id for node in ast.walk(function)
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name)
        }
        self.assertTrue(receivers <= bound,
                        f"the hook reads attributes from {receivers - bound}")

    def test_the_hook_works_without_any_world_state(self):
        # No WorldState is constructed here at all: the hook is standalone by construction.
        self.assertEqual(political_view(empty_field())["demands"], [])

    def test_the_board_view_does_not_render_political_records(self):
        """Layer II is not wired into WorldState, so it cannot appear on the board yet."""
        state = WorldState(factions=[Faction("f1", "Example faction")],
                           locations=[Location("loc1", "Helsinki", 60.17, 24.94)])
        self.assertEqual([n["type"] for n in board_view(state)["network_nodes"]], ["faction"])


class NoMetricTests(unittest.TestCase):
    def test_no_metric_shaped_key_appears_in_the_panel(self):
        view = political_view(populated_field())
        for section, rows in view.items():
            if not isinstance(rows, list):
                continue
            for row in rows:
                for key in row:
                    for token in METRIC_TOKENS:
                        with self.subTest(section=section, key=key, token=token):
                            self.assertNotIn(token, key)

    def test_the_panel_carries_no_numeric_quantity(self):
        def scalars(value):
            if isinstance(value, dict):
                for item in value.values():
                    yield from scalars(item)
            elif isinstance(value, (list, tuple)):
                for item in value:
                    yield from scalars(item)
            else:
                yield value

        for value in scalars(political_view(populated_field())):
            with self.subTest(value=value):
                self.assertNotIsInstance(value, (int, float))


class NonMutationTests(unittest.TestCase):
    def test_the_panel_does_not_mutate_the_field(self):
        field = populated_field()
        before = field.to_dict()
        political_view(field)
        self.assertEqual(field.to_dict(), before)

    def test_the_panel_copies_its_lists(self):
        """A rendered row must not alias the field's own list."""
        field = PoliticalField(frontiers=[Frontier("fr1", "s1", ["d1"], [])])
        frontier = political_view(field)["frontiers"][0]
        frontier["included_demand_ids"].append("d2")
        self.assertEqual(field.frontiers[0].included_demand_ids, ["d1"])

    def test_the_panel_is_deterministic(self):
        field = populated_field()
        self.assertEqual(political_view(field), political_view(field))


if __name__ == "__main__":
    unittest.main()
