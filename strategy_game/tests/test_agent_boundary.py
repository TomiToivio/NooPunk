"""Executable contracts for the #304 proposal/controller boundary (step 1 of its sequence).

Code-only, per AGENTS.md and #271: every assertion below exercises runtime behaviour of
``strategy_game.controllers``, ``capabilities`` or the CLI. There is deliberately **no** assertion
about the wording of a document, a rule, canon or lore. The one structural guard here pins the
*boundary*, not a mechanic: a proposal is a record, and recording must not move authoritative state.

The five contracts the design comment on #304 asked for, and where they live:

(a) recording succeeds with no ollama/concordia, and world/table state stay byte-identical
    -> :class:`RecordingMutabilityTests` (in-process and in a subprocess with the adapters blocked);
(b) a proposal whose ``leader_id`` has no controller authorisation is refused
    -> :class:`AuthorizationTests`;
(c) recording then replaying imports no optional adapter
    -> :class:`RecordingMutabilityTests` and :class:`NoOptionalAdapterTests`;
(d) ``strategy_game.__all__`` and the CI-pinned ``python -m strategy_game`` key set are unchanged
    -> :class:`PinnedApiTests`;
(e) capability probing still behaves
    -> :class:`CapabilityProbeTests`.
"""
import dataclasses
import inspect
import json
import subprocess
import sys
import textwrap
import typing
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game import capabilities  # noqa: E402
from strategy_game.controllers import (  # noqa: E402
    APPROVED_ACTION_CODES,
    CONTROLLER_ADAPTERS,
    PENDING_AUTHOR_RULINGS,
    AdapterNotImplementedError,
    AssignmentConflict,
    Controller,
    ControllerRegistry,
    MoveProposal,
    NullAgentProvider,
    ProposalError,
    ProposalLog,
    ProposalRecorder,
    ScriptedAgentProvider,
    ScriptedMove,
    UnauthorizedProposalError,
    available_controller_adapters,
    controller_from_adapter,
    default_controllers,
    registry_for,
)
from strategy_game.core import Event, Faction, Leader, WorldState  # noqa: E402
from strategy_game.provenance import ProvenanceKind  # noqa: E402
from strategy_game.tabletop.dice import parse_notation, roll  # noqa: E402
from strategy_game.tabletop.serialization import TableState  # noqa: E402

#: The exact pinned top-level API (#282). A widening here is what these tests exist to catch.
PINNED_TOP_LEVEL_ALL = [
    "WorldState",
    "Provenance",
    "ProvenanceKind",
    "PoliticalField",
    "SignifierRole",
    "PowerMode",
]

#: The exact key set the CI smoke step pins for ``python -m strategy_game``.
PINNED_VIEW_KEYS = {"schema_version", "locations", "network_nodes", "network_edges", "assets"}

#: Field-name fragments a declared quantity would use. MoveProposal declares none of them.
METRIC_TOKENS = ("score", "strength", "influence", "threshold", "weight", "probability", "rating",
                 "cost", "power", "level")

#: Makes ``ollama`` and ``concordia`` unimportable, simulating "not installed" without touching the
#: environment. Raising from ``find_spec`` is what makes ``capabilities.is_available`` report False
#: (it catches ImportError), which is the realistic absence the boundary must survive.
_ADAPTER_BLOCKER = (
    "import importlib.abc, sys\n"
    "class _AdapterBlocker(importlib.abc.MetaPathFinder):\n"
    "    def find_spec(self, name, path=None, target=None):\n"
    "        if name.split('.')[0] in ('ollama', 'concordia'):\n"
    "            raise ModuleNotFoundError(name + ' is simulated absent')\n"
    "        return None\n"
    "sys.meta_path.insert(0, _AdapterBlocker())\n"
)


def populated() -> WorldState:
    """A small, entirely illustrative state. No real actor, party or place appears."""
    return WorldState(
        leaders=[Leader("leader-one", "First illustrative leader")],
        factions=[Faction("faction-one", "First illustrative faction", "leader-one")],
        events=[Event("event-one", "An illustrative event", "author:TBD")],
    )


def table() -> TableState:
    """A table with one seeded roll, so "the table did not move" is a meaningful assertion."""
    state = TableState()
    state.rolls.record(roll(parse_notation("2d6"), seed=1, label="illustrative"))
    return state


def scripted(controller_id: str = "scripted-one") -> ScriptedAgentProvider:
    return ScriptedAgentProvider(
        controller_id,
        script=(
            ScriptedMove("leader-one", "example-action", target_id="faction-one",
                         rationale="Illustrative declaration."),
        ),
    )


def run_blocked(body: str) -> subprocess.CompletedProcess:
    """Run ``body`` in a fresh interpreter where ollama/concordia cannot be imported."""
    return subprocess.run(
        [sys.executable, "-c", _ADAPTER_BLOCKER + textwrap.dedent(body)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )


class MoveProposalContractTests(unittest.TestCase):
    def test_the_container_defaults_provenance_to_unknown(self):
        """An unclassified origin must stay visibly unknown, never read as fact."""
        self.assertIs(MoveProposal("c", "l").provenance.kind, ProvenanceKind.UNKNOWN)

    def test_a_leader_id_is_required(self):
        for bad in ("", "   ", None):
            with self.subTest(leader_id=bad):
                with self.assertRaises(ProposalError):
                    MoveProposal("c", bad)

    def test_no_action_set_is_assumed(self):
        """No action set is approved, so the code must not invent one -- and must not refuse."""
        self.assertEqual(APPROVED_ACTION_CODES, ())
        recorder = ProposalRecorder(registry_for((scripted(),)))
        proposal = MoveProposal("scripted-one", "leader-one", action_code="anything-the-author-likes")
        recorder.record(proposal, )  # an open code is accepted: there is no approved closed set
        self.assertEqual(recorder.entries[0].action_code, "anything-the-author-likes")

    def test_the_declared_fields_are_open_strings_and_resource_names(self):
        proposal = MoveProposal(
            "c", "l", action_code="code", target_id="target",
            resources=["resource-a", "resource-b"], rationale="free text",
        )
        self.assertEqual(proposal.resources, ("resource-a", "resource-b"))
        self.assertEqual(proposal.target_id, "target")
        self.assertEqual(proposal.rationale, "free text")

    def test_the_container_declares_no_numeric_field(self):
        """A quantity would be an economy; none is approved (mirrors the political-layer guard)."""
        hints = typing.get_type_hints(MoveProposal)
        for declared in dataclasses.fields(MoveProposal):
            with self.subTest(field=declared.name):
                self.assertNotIn(hints[declared.name], (int, float))

    def test_the_container_declares_no_metric_shaped_field(self):
        names = [declared.name for declared in dataclasses.fields(MoveProposal)]
        for token in METRIC_TOKENS:
            with self.subTest(token=token):
                self.assertEqual([name for name in names if token in name], [])

    def test_a_proposal_round_trips_through_plain_json(self):
        original = MoveProposal(
            "c", "l", action_code="code", target_id="target",
            resources=("resource-a",), rationale="free text",
        )
        restored = MoveProposal.from_dict(json.loads(json.dumps(original.to_dict())))
        self.assertEqual(restored, original)
        self.assertEqual(set(original.to_dict()),
                         {"controller_id", "leader_id", "action_code", "target_id",
                          "resources", "rationale", "provenance"})

    def test_the_log_round_trips_and_keeps_its_order(self):
        log = ProposalLog()
        log.append(MoveProposal("c", "l1", action_code="first"))
        log.append(MoveProposal("c", "l2", action_code="second"))
        restored = ProposalLog.from_dict(json.loads(json.dumps(log.to_dict())))
        self.assertEqual([entry.action_code for entry in restored.entries], ["first", "second"])


class ControllerProtocolTests(unittest.TestCase):
    def test_each_provider_conforms_to_the_controller_protocol(self):
        for provider in (NullAgentProvider(), scripted()):
            with self.subTest(provider=type(provider).__name__):
                self.assertIsInstance(provider, Controller)

    def test_the_controller_protocol_goes_beyond_the_signature_seam(self):
        """``ports.AgentProvider`` is signature-only; the real controller adds behaviour."""
        from strategy_game import ports

        self.assertFalse(hasattr(ports.AgentProvider, "propose"))
        for attribute in ("controller_id", "controls", "propose"):
            self.assertTrue(hasattr(Controller, attribute), attribute)

    def test_the_null_provider_proposes_nothing_and_commands_nothing(self):
        null = NullAgentProvider()
        self.assertIsNone(null.propose(WorldState(), leader_id="leader-one"))
        self.assertFalse(null.controls("leader-one"))
        defaults = default_controllers()
        self.assertEqual([type(controller) for controller in defaults], [NullAgentProvider])
        self.assertEqual([controller.controller_id for controller in defaults], ["null"])

    def test_the_scripted_provider_is_deterministic(self):
        script = (ScriptedMove("l1", "a"), ScriptedMove("l1", "b"), ScriptedMove("l2", "c"))

        def drive():
            provider = ScriptedAgentProvider("c", script=script)
            return [
                provider.propose(WorldState(), leader_id="l1"),
                provider.propose(WorldState(), leader_id="l1"),
                provider.propose(WorldState(), leader_id="l2"),
                provider.propose(WorldState(), leader_id="l1"),
            ]

        def payload(proposals):
            return [None if proposal is None else proposal.to_dict() for proposal in proposals]

        first, second = drive(), drive()
        self.assertEqual(payload(first), payload(second))
        # the script is exhausted, not cycled: the fourth call for l1 has no line left
        self.assertIsNone(first[-1])
        self.assertEqual([p.action_code for p in first[:3]], ["a", "b", "c"])

    def test_a_scripted_proposal_states_its_origin(self):
        proposal = scripted().propose(WorldState(), leader_id="leader-one")
        self.assertIsNotNone(proposal)
        assert proposal is not None  # narrow for the type checker; the assert above already proves it
        self.assertIs(proposal.provenance.kind, ProvenanceKind.GENERATED)
        self.assertEqual(proposal.provenance.source, "scripted:scripted-one")

    def test_a_provider_is_interchangeable_regardless_of_who_drives_it(self):
        """An LLM controller and a human controller must be indistinguishable to the recorder."""
        registry = registry_for((scripted(),))
        recorder = ProposalRecorder(registry)
        for driver in (scripted(), scripted()):
            proposal = driver.propose(WorldState(), leader_id="leader-one")
            recorder.record(proposal)
        self.assertEqual([p.controller_id for p in recorder.entries],
                         ["scripted-one", "scripted-one"])


class AuthorizationTests(unittest.TestCase):
    def test_an_authorised_proposal_is_accepted(self):
        recorder = ProposalRecorder(registry_for((scripted(),)))
        recorded = recorder.record(MoveProposal("scripted-one", "leader-one"))
        self.assertEqual(recorded.leader_id, "leader-one")
        self.assertEqual(len(recorder.entries), 1)

    def test_a_proposal_for_another_controllers_leader_is_refused(self):
        recorder = ProposalRecorder(registry_for((scripted(),)))
        with self.assertRaises(UnauthorizedProposalError):
            recorder.record(MoveProposal("someone-else", "leader-one"))
        self.assertEqual(recorder.entries, ())

    def test_a_proposal_for_an_unassigned_leader_is_refused(self):
        recorder = ProposalRecorder(ControllerRegistry())
        with self.assertRaises(UnauthorizedProposalError):
            recorder.record(MoveProposal("scripted-one", "leader-one"))
        self.assertEqual(recorder.entries, ())

    def test_a_leader_has_at_most_one_authoritative_controller(self):
        registry = ControllerRegistry()
        registry.assign("first", "leader-one")
        registry.assign("first", "leader-one")  # idempotent for the same pair
        with self.assertRaises(AssignmentConflict):
            registry.assign("second", "leader-one")

    def test_the_registry_answers_authorisation_directly(self):
        registry = registry_for((scripted(),))
        self.assertTrue(registry.authorizes("scripted-one", "leader-one"))
        self.assertFalse(registry.authorizes("other", "leader-one"))
        self.assertEqual(registry.controller_of("leader-one"), "scripted-one")
        self.assertEqual(registry.leaders_of("scripted-one"), ("leader-one",))
        self.assertIsNone(registry.controller_of("nobody"))

    def test_a_recorder_needs_an_authority(self):
        with self.assertRaises(ProposalError):
            ProposalRecorder(object())


class RecordingMutabilityTests(unittest.TestCase):
    """The core of #304's boundary: recording stores data and applies nothing."""

    def test_recording_leaves_authoritative_state_byte_identical(self):
        world, table_state = populated(), table()
        world_before, table_before = world.to_json(), table_state.to_json()

        registry = registry_for((scripted(),))
        recorder = ProposalRecorder(registry)
        recorder.record(scripted().propose(world, leader_id="leader-one"))
        recorder.record(MoveProposal("scripted-one", "leader-one", action_code="another"))

        self.assertEqual(world.to_json(), world_before)
        self.assertEqual(table_state.to_json(), table_before)
        # nothing was appended to the world's event stream either
        self.assertEqual([event.identifier for event in world.events], ["event-one"])

    def test_the_recorder_has_no_state_handle_at_all(self):
        """A stronger guarantee than a promise: it cannot apply a proposal it is never given."""
        self.assertEqual(list(inspect.signature(ProposalRecorder.record).parameters),
                         ["self", "proposal"])
        recorder = ProposalRecorder(registry_for((scripted(),)))
        self.assertEqual(list(inspect.signature(ProposalRecorder.__init__).parameters),
                         ["self", "registry"])
        for forbidden in ("world", "world_state", "state", "table", "table_state"):
            self.assertFalse(hasattr(recorder, forbidden), forbidden)

    def test_recording_mutates_only_the_recorders_own_log(self):
        recorder = ProposalRecorder(registry_for((scripted(),)))
        before = recorder.to_dict()
        recorder.record(MoveProposal("scripted-one", "leader-one"))
        self.assertEqual(before, {"entries": []})
        self.assertEqual(len(recorder.entries), 1)

    def test_recording_then_replaying_imports_no_optional_adapter(self):
        before = set(sys.modules)
        world = populated()
        recorder = ProposalRecorder(registry_for((scripted(),)))
        recorder.record(scripted().propose(world, leader_id="leader-one"))
        replayed = recorder.replay()
        self.assertEqual([p.to_dict() for p in replayed], [p.to_dict() for p in recorder.entries])

        added_roots = {name.split(".")[0] for name in set(sys.modules) - before}
        self.assertEqual(added_roots & set(capabilities.OPTIONAL_ADAPTERS), set())

    def test_replaying_reconstructs_the_same_proposals_without_a_provider(self):
        recorder = ProposalRecorder(registry_for((scripted(),)))
        recorder.record(MoveProposal("scripted-one", "leader-one", action_code="code",
                                      rationale="free text"))
        # Rebuild from the serialized log alone -- no provider, no state, no model.
        restored = ProposalRecorder.from_dict(
            json.loads(json.dumps(recorder.to_dict())), recorder._registry
        )
        self.assertEqual(restored.replay(), recorder.replay())


class NoOptionalAdapterTests(unittest.TestCase):
    def test_the_package_imports_no_optional_adapter(self):
        import importlib

        module = importlib.import_module("strategy_game.controllers")
        self.assertTrue(hasattr(module, "MoveProposal"))
        for name in capabilities.OPTIONAL_ADAPTERS:
            with self.subTest(adapter=name):
                self.assertFalse(name in sys.modules and getattr(sys.modules[name], "__file__", None) is None)

    def test_recording_succeeds_with_the_adapters_absent_and_moves_nothing(self):
        result = run_blocked(
            '''
            import json, sys
            from strategy_game import capabilities
            from strategy_game.controllers import (MoveProposal, ProposalRecorder,
                                                   ScriptedAgentProvider, ScriptedMove, registry_for)
            from strategy_game.core import Leader, Faction, WorldState
            from strategy_game.tabletop.serialization import TableState

            world = WorldState(leaders=[Leader("l1", "X")], factions=[Faction("f1", "Y", "l1")])
            table_state = TableState()
            world_before, table_before = world.to_json(), table_state.to_json()

            provider = ScriptedAgentProvider("c1", script=(ScriptedMove("l1", "act"),))
            recorder = ProposalRecorder(registry_for((provider,)))
            recorder.record(provider.propose(world, leader_id="l1"))
            recorder.record(MoveProposal("c1", "l1", action_code="second"))
            replayed = recorder.replay()

            print(json.dumps({
                "ollama_available": capabilities.is_available("ollama"),
                "concordia_available": capabilities.is_available("concordia"),
                "world_identical": world.to_json() == world_before,
                "table_identical": table_state.to_json() == table_before,
                "recorded": len(recorder.entries),
                "replay_matches": [p.to_dict() for p in replayed] == [p.to_dict() for p in recorder.entries],
                "imported_optional": sorted(m for m in sys.modules
                                            if m.split(".")[0] in ("ollama", "concordia")),
            }))
            '''
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        # the blocker actually hid the adapters -- the guard checks itself
        self.assertFalse(payload["ollama_available"])
        self.assertFalse(payload["concordia_available"])
        # and the boundary still worked, moving nothing
        self.assertEqual(payload["recorded"], 2)
        self.assertTrue(payload["replay_matches"])
        self.assertTrue(payload["world_identical"])
        self.assertTrue(payload["table_identical"])
        self.assertEqual(payload["imported_optional"], [])

    def test_the_adapter_seam_never_imports_and_degrades(self):
        for name in CONTROLLER_ADAPTERS:
            with self.subTest(adapter=name):
                before = set(sys.modules)
                if capabilities.is_available(name):
                    with self.assertRaises(AdapterNotImplementedError):
                        controller_from_adapter(name)
                else:
                    self.assertIsNone(controller_from_adapter(name))
                added_roots = {m.split(".")[0] for m in set(sys.modules) - before}
                self.assertEqual(added_roots & set(capabilities.OPTIONAL_ADAPTERS), set())

    def test_an_undeclared_adapter_name_is_refused(self):
        with self.assertRaises(ValueError):
            controller_from_adapter("openai")

    def test_the_seam_reads_only_from_the_declared_set(self):
        for name in CONTROLLER_ADAPTERS:
            self.assertIn(name, capabilities.OPTIONAL_ADAPTERS)

    def test_the_boundary_declares_what_it_did_not_invent(self):
        """The refusals are data, so a later reader does not have to trust prose."""
        self.assertTrue(PENDING_AUTHOR_RULINGS)
        joined = " ".join(PENDING_AUTHOR_RULINGS)
        for topic in ("action set", "resolution", "Game Master", "hidden-information", "multiplayer",
                      "Tarot"):
            self.assertIn(topic, joined, topic)


class CapabilityProbeTests(unittest.TestCase):
    def test_available_adapters_covers_the_declared_set(self):
        available = capabilities.available_adapters()
        self.assertEqual(set(available), set(capabilities.OPTIONAL_ADAPTERS))
        self.assertTrue(all(isinstance(value, bool) for value in available.values()))

    def test_missing_adapters_is_the_complement(self):
        available = capabilities.available_adapters()
        self.assertEqual(set(capabilities.missing_adapters()),
                         {name for name, present in available.items() if not present})

    def test_is_available_is_false_for_a_nonexistent_module(self):
        self.assertFalse(capabilities.is_available("noopunk_definitely_absent_module"))
        self.assertTrue(capabilities.is_available("json"))

    def test_require_still_refuses_an_undeclared_name(self):
        with self.assertRaises(ValueError):
            capabilities.require("openai")

    def test_the_controller_probe_covers_its_own_declared_set(self):
        probe = available_controller_adapters()
        self.assertEqual(set(probe), set(CONTROLLER_ADAPTERS))
        for name, present in probe.items():
            self.assertEqual(present, capabilities.is_available(name), name)

    def test_probing_imports_nothing(self):
        before = set(sys.modules)
        capabilities.available_adapters()
        capabilities.missing_adapters()
        available_controller_adapters()
        added_roots = {m.split(".")[0] for m in set(sys.modules) - before}
        self.assertEqual(added_roots & set(capabilities.OPTIONAL_ADAPTERS), set())


class PinnedApiTests(unittest.TestCase):
    """The new subpackage must not widen the already-pinned public shape (#282/#347)."""

    def test_strategy_game_all_is_unchanged(self):
        import strategy_game

        self.assertEqual(list(strategy_game.__all__), PINNED_TOP_LEVEL_ALL)

    def test_the_new_package_does_not_widen_the_top_level_api(self):
        import strategy_game

        for name in ("MoveProposal", "ProposalRecorder", "Controller", "ControllerRegistry",
                     "NullAgentProvider", "ScriptedAgentProvider"):
            with self.subTest(name=name):
                self.assertNotIn(name, strategy_game.__all__)
                self.assertFalse(hasattr(strategy_game, name))

    def test_importing_strategy_game_does_not_import_the_boundary_package(self):
        result = subprocess.run(
            [sys.executable, "-c",
             "import sys, strategy_game; print('strategy_game.controllers' in sys.modules)"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "False")

    def test_the_packages_own_all_is_exact_and_resolvable(self):
        import strategy_game.controllers as boundary

        self.assertEqual(len(boundary.__all__), len(set(boundary.__all__)))
        for name in boundary.__all__:
            self.assertTrue(hasattr(boundary, name), name)

    def test_python_m_strategy_game_key_set_is_unchanged(self):
        result = subprocess.run([sys.executable, "-m", "strategy_game"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(set(json.loads(result.stdout)), PINNED_VIEW_KEYS)

    def test_the_package_demo_runs_deterministically_without_a_model(self):
        first = subprocess.run([sys.executable, "-m", "strategy_game.controllers"],
                               cwd=ROOT, capture_output=True, text=True, check=False)
        second = subprocess.run([sys.executable, "-m", "strategy_game.controllers"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        payload = json.loads(first.stdout)
        self.assertTrue(payload["world_state_unchanged_by_recording"])
        self.assertTrue(payload["replay_matches_record"])
        self.assertEqual(payload["null_proposals"], [None, None])
        self.assertEqual(payload["controllers"]["scripted-example"]["leaders"],
                         ["leader-one", "leader-two"])


if __name__ == "__main__":
    unittest.main()
