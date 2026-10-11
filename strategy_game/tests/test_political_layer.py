"""Runtime contracts for the Layer II political vocabulary (issue #282).

Executable-code contracts only, per AGENTS.md's code-only testing policy: nothing here asserts
the wording of a document, a rule, canon or lore. It pins the behaviour of `politics.py`, the
`WorldState` collections it feeds, and the two rendering hooks in `view.py`.

Two properties matter more than the rest:

* **the political layer is additive.** A state with no political records must render exactly as
  it did before this layer existed, because three already-merged test files pin `board_view`'s
  key set, its node field set and the fact that `network_nodes[0]` is the first faction.
* **one graph, not two.** A political relation is an ordinary `NetworkEdge`; there is no second
  edge type, and the scaffold must never require an optional dependency to load or view the
  political field.
"""
import dataclasses
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game import capabilities  # noqa: E402
from strategy_game.core import NetworkEdge, WorldState  # noqa: E402
from strategy_game.politics import (  # noqa: E402
    POLITICAL_NODE_KINDS,
    RELATION_LAYERS,
    SIGNIFIER_KINDS,
    Demand,
    Formation,
    Frontier,
    PoliticalNodeKind,
    RelationLayer,
    Signifier,
    SignifierKind,
    political_node_kind_of,
)
from strategy_game.provenance import ProvenanceKind  # noqa: E402
from strategy_game.view import board_view, political_view  # noqa: E402


def declared() -> WorldState:
    """A small, entirely illustrative state. No real actor, party or place appears."""
    return WorldState(
        demands=[Demand("d1", "An example demand")],
        signifiers=[Signifier("s1", "An example signifier", SignifierKind.EMPTY)],
        formations=[Formation("fo1", "An example formation")],
        frontiers=[Frontier("fr1", "An example frontier")],
        edges=[
            NetworkEdge("s1", "d1", RelationLayer.ARTICULATION.value),
            NetworkEdge("s1", "fr1", RelationLayer.ANTAGONISM.value),
        ],
    )


class VocabularyContractTests(unittest.TestCase):
    def test_the_declared_kinds_match_their_enums(self):
        self.assertEqual(set(SIGNIFIER_KINDS), {k.value for k in SignifierKind})
        self.assertEqual(set(POLITICAL_NODE_KINDS), {k.value for k in PoliticalNodeKind})
        self.assertEqual(set(RELATION_LAYERS), {l.value for l in RelationLayer})

    def test_the_declared_labels_are_stable(self):
        """These strings are a serialization contract: a saved snapshot must reload unchanged.

        Pinned exactly, because a rename would silently reinterpret every stored record -- and
        because a test written against the enum members alone follows a rename instead of
        catching it.
        """
        self.assertEqual(set(SIGNIFIER_KINDS),
                         {"unspecified", "nodal", "floating", "empty"})
        self.assertEqual(set(POLITICAL_NODE_KINDS),
                         {"demand", "signifier", "formation", "frontier"})
        self.assertEqual(set(RELATION_LAYERS),
                         {"articulation", "equivalence", "antagonism", "communication"})

    def test_the_three_theory_labels_are_present(self):
        for label in ("nodal", "floating", "empty"):
            self.assertIn(label, SIGNIFIER_KINDS)

    def test_an_unclassified_signifier_stays_unspecified(self):
        """The theory's label is the author's interpretation, so no silent default to `nodal`."""
        self.assertIs(Signifier("s1", "x").kind, SignifierKind.UNSPECIFIED)

    def test_the_default_signifier_kind_serializes_as_unspecified(self):
        """The stored value is what matters: an unread signifier must not *save* as `nodal`.

        Asserting the enum member alone cannot catch a renamed value, because the member keeps
        its name while the snapshot silently changes meaning.
        """
        payload = Signifier("s1", "x").to_dict()
        self.assertEqual(payload["kind"], "unspecified")
        self.assertNotEqual(payload["kind"], "nodal")

    def test_an_unrecognised_kind_falls_back_to_unspecified(self):
        restored = Signifier.from_dict({"identifier": "s1", "label": "x", "kind": "nonsense"})
        self.assertIs(restored.kind, SignifierKind.UNSPECIFIED)

    def test_a_string_kind_is_accepted_and_normalised(self):
        self.assertIs(Signifier("s1", "x", "floating").kind, SignifierKind.FLOATING)


class ProvenanceContractTests(unittest.TestCase):
    def test_every_political_record_defaults_to_unknown_provenance(self):
        for record in (Demand("d", "x"), Signifier("s", "x"), Formation("f", "x"), Frontier("r", "x")):
            with self.subTest(record=type(record).__name__):
                self.assertIs(record.provenance.kind, ProvenanceKind.UNKNOWN)

    def test_a_declared_provenance_is_kept_and_kind_is_not_upgraded(self):
        record = Demand("d", "x", provenance="author:TBD")
        self.assertEqual(record.provenance.source, "author:TBD")
        self.assertIs(record.provenance.kind, ProvenanceKind.UNKNOWN)

    def test_serialized_provenance_is_plain_scalars(self):
        payload = declared().to_dict()["demands"][0]["provenance"]
        self.assertEqual(set(payload), {"kind", "source", "note"})
        json.dumps(payload)


class SerializationContractTests(unittest.TestCase):
    def test_the_new_collections_default_to_empty(self):
        state = WorldState()
        self.assertEqual(
            (state.demands, state.signifiers, state.formations, state.frontiers),
            ([], [], [], []),
        )

    def test_round_trip_preserves_the_political_layer(self):
        original = declared()
        self.assertEqual(WorldState.from_json(original.to_json()), original)

    def test_round_trip_preserves_a_signifier_kind(self):
        state = WorldState(signifiers=[Signifier("s1", "x", SignifierKind.FLOATING)])
        restored = WorldState.from_json(state.to_json())
        self.assertIs(restored.signifiers[0].kind, SignifierKind.FLOATING)

    def test_round_trip_preserves_non_ascii_labels(self):
        state = WorldState(signifiers=[Signifier("s1", "Kansan tahto — Noösphere")])
        self.assertIn("Noösphere", state.to_json())
        self.assertEqual(WorldState.from_json(state.to_json()).signifiers[0].label,
                         "Kansan tahto — Noösphere")

    def test_an_older_snapshot_without_the_political_section_still_loads(self):
        legacy = json.dumps({"schema_version": "scaffold-1"})
        self.assertEqual(WorldState.from_json(legacy), WorldState())

    def test_political_json_is_deterministic(self):
        state = declared()
        self.assertEqual(state.to_json(), state.to_json())

    def test_collections_are_not_shared_between_instances(self):
        first, second = WorldState(), WorldState()
        first.demands.append(Demand("d1", "x"))
        self.assertEqual(second.demands, [])


class BoardViewAdditivityTests(unittest.TestCase):
    """The political layer must not disturb the already-pinned board contract."""

    def test_the_board_key_set_is_unchanged(self):
        self.assertEqual(
            set(board_view(declared())),
            {"schema_version", "locations", "network_nodes", "network_edges", "assets"},
        )

    def test_a_political_free_state_renders_no_extra_nodes(self):
        self.assertEqual(board_view(WorldState())["network_nodes"], [])

    def test_factions_are_still_emitted_first(self):
        from strategy_game.core import Faction
        state = declared()
        state.factions.append(Faction("f1", "Example faction"))
        self.assertEqual(board_view(state)["network_nodes"][0]["type"], "faction")

    def test_political_records_appear_as_typed_nodes(self):
        nodes = board_view(declared())["network_nodes"]
        self.assertEqual([n["type"] for n in nodes],
                         ["demand", "signifier", "formation", "frontier"])

    def test_political_nodes_carry_the_node_fields_only(self):
        nodes = board_view(declared())["network_nodes"]
        for node in nodes:
            with self.subTest(node=node["id"]):
                self.assertEqual(set(node), {"id", "label", "type"})

    def test_political_relations_appear_as_ordinary_edges(self):
        edges = board_view(declared())["network_edges"]
        for edge in edges:
            self.assertEqual(set(edge), {"source", "target", "layer"})
        self.assertEqual([e["layer"] for e in edges],
                         [RelationLayer.ARTICULATION.value, RelationLayer.ANTAGONISM.value])

    def test_the_board_view_does_not_mutate_its_state(self):
        state = declared()
        before = state.to_dict()
        board_view(state)
        self.assertEqual(state.to_dict(), before)


class PoliticalViewContractTests(unittest.TestCase):
    def test_the_panel_exposes_the_expected_sections(self):
        self.assertEqual(
            set(political_view(declared())),
            {"schema_version", "signifier_kinds", "demands", "formations", "frontiers", "relations"},
        )

    def test_the_panel_is_empty_for_a_political_free_state(self):
        view = political_view(WorldState())
        for key in ("signifier_kinds", "demands", "formations", "frontiers", "relations"):
            self.assertEqual(view[key], [], key)

    def test_the_panel_mirrors_the_state(self):
        view = political_view(declared())
        self.assertEqual(view["signifier_kinds"][0],
                         {"id": "s1", "label": "An example signifier",
                          "kind": SignifierKind.EMPTY.value})
        self.assertEqual(view["demands"][0], {"id": "d1", "label": "An example demand",
                                              "claimant_id": None})

    def test_the_panel_lists_only_declared_political_relations(self):
        state = declared()
        state.edges.append(NetworkEdge("x", "y", "something-else"))
        layers = [r["layer"] for r in political_view(state)["relations"]]
        self.assertNotIn("something-else", layers)

    def test_the_panel_exposes_display_fields_only(self):
        """No strength, score, confidence, threshold or cost: this layer has no approved rules."""
        view = political_view(declared())
        for section, rows in view.items():
            if not isinstance(rows, list):
                continue
            for row in rows:
                for key in row:
                    with self.subTest(section=section, key=key):
                        self.assertNotIn(
                            key,
                            {"score", "strength", "stability", "confidence", "threshold", "cost",
                             "power", "level", "value", "weight"},
                        )

    def test_the_panel_is_json_serializable(self):
        json.dumps(political_view(declared()))

    def test_the_panel_does_not_mutate_its_state(self):
        state = declared()
        before = state.to_dict()
        political_view(state)
        self.assertEqual(state.to_dict(), before)


class LookupHelperTests(unittest.TestCase):
    def test_the_helper_resolves_each_kind(self):
        state = declared()
        for identifier, kind in (("d1", "demand"), ("s1", "signifier"),
                                 ("fo1", "formation"), ("fr1", "frontier")):
            with self.subTest(identifier=identifier):
                self.assertEqual(political_node_kind_of(identifier, state), kind)

    def test_the_helper_returns_none_for_an_unknown_identifier(self):
        self.assertIsNone(political_node_kind_of("nope", declared()))

    def test_the_helper_tolerates_a_state_without_the_layer(self):
        self.assertIsNone(political_node_kind_of("d1", object()))


class NoOptionalDependencyTests(unittest.TestCase):
    def test_loading_and_viewing_the_political_layer_needs_no_optional_adapter(self):
        """`no LLM required to load/view world state` applies to Layer II too."""
        before = set(capabilities.available_adapters())
        state = declared()
        WorldState.from_json(state.to_json())
        board_view(state)
        political_view(state)
        self.assertEqual(set(capabilities.available_adapters()), before)

    def test_the_module_imports_no_adapter(self):
        import strategy_game.politics as politics
        source = Path(politics.__file__).read_text(encoding="utf-8")
        for adapter in capabilities.OPTIONAL_ADAPTERS:
            with self.subTest(adapter=adapter):
                self.assertNotIn(f"import {adapter}", source)


class NoScoringSurfaceTests(unittest.TestCase):
    """No political *record* may grow a numeric field (issue #282's hard boundary).

    The panel test pins the rendering hook's display fields; that leaves the records
    themselves unguarded, and a `Demand.score` added by a later pass would reach the panel
    only if the panel chose to read it. So this checks the dataclasses directly.

    Coverage is **discovered, not listed**: a hand-written record list goes stale exactly
    when a new record appears, which is when a score is most likely to arrive with it.
    """

    #: Field names that would mean a score, a strength or a threshold had been invented.
    FORBIDDEN_TOKENS = (
        "score", "strength", "weight", "salience", "momentum", "progress", "power",
        "cost", "threshold", "confidence", "rating", "budget", "stake", "influence",
    )

    def _records(self) -> tuple[type, ...]:
        from strategy_game import politics

        return tuple(sorted(
            (obj for obj in vars(politics).values()
             if isinstance(obj, type) and dataclasses.is_dataclass(obj)
             and obj.__module__ == politics.__name__),
            key=lambda cls: cls.__name__,
        ))

    def test_the_record_discovery_finds_the_declared_records(self):
        names = {cls.__name__ for cls in self._records()}
        self.assertEqual(names, {"Demand", "Signifier", "Formation", "Frontier"})

    def test_no_political_record_declares_a_numeric_field(self):
        for record in self._records():
            for spec in dataclasses.fields(record):
                with self.subTest(record=record.__name__, field=spec.name):
                    # String comparison: `from __future__ import annotations` means
                    # `spec.type` is the annotation *text*, not the resolved type.
                    self.assertNotIn(spec.type, ("int", "float", "complex"),
                                     f"{record.__name__}.{spec.name} is numeric; the scaffold "
                                     "stores no strength, weight or score")

    def test_no_political_field_name_suggests_a_score(self):
        for record in self._records():
            for spec in dataclasses.fields(record):
                tokens = set(spec.name.lower().split("_"))
                for word in self.FORBIDDEN_TOKENS:
                    with self.subTest(record=record.__name__, field=spec.name, token=word):
                        self.assertNotIn(word, tokens)

    def test_the_module_exposes_no_scoring_api(self):
        from strategy_game import politics

        for name in ("score", "rate", "weigh", "strengthen", "salience", "influence_of"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(politics, name))


if __name__ == "__main__":
    unittest.main()
