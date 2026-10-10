"""Phase B tests: the deterministic simulation core for issue #40.

These are BEHAVIOUR tests: code, so the properties that matter must be *executed*. (The
sibling ``test_issue40_simulation_spec.py``, which asserted specification text, was removed
under issue #271.)

* state is exactly the reduction of the event log (no side channel);
* replays are byte-identical, and a branch from the same prefix is identical to
  its parent at that point;
* ``turn`` orders the log, not ``timestamp`` — pinned by giving events
  deliberately contradictory timestamps;
* appends are idempotent and the log is append-only;
* synthetic and empirical data cannot be pulled out as one another;
* the reducer refuses to invent mechanics: an unknown action still enters history,
  and nothing derived is computed.

Fixture vocabulary only. Per ``AGENTS.md`` §1/§4 no faction, institution, region
or social mechanic is real here; ids are marked ``fixture:`` and the engine accepts
any relation string precisely so nothing in this file constrains the author's
vocabulary.

Run: python3 -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simulation import (  # noqa: E402
    Event,
    EventLogError,
    EventValidationError,
    ReducerError,
    Simulation,
    append,
    assert_append_only,
    connect,
    count_events,
    fixture_id,
    is_fixture_id,
    list_events,
    list_exchanges_for_export,
    list_simulations,
    order_key,
    reduce_events,
    replay,
    replay_digest,
)


def _event(**overrides) -> Event:
    payload = dict(
        simulation_id="sim-test",
        turn=0,
        actor=fixture_id("resident-a"),
        action_type="communicate",
        source="tabletop",
        synthetic=True,
        content="fixture utterance",
    )
    payload.update(overrides)
    return Event.create(**payload)


class EnvelopeTests(unittest.TestCase):
    def test_required_fields_are_enforced(self) -> None:
        for missing in ("simulation_id", "actor", "action_type"):
            with self.subTest(missing=missing):
                payload = dict(
                    simulation_id="s", turn=0, actor="a", action_type="x",
                    source="system", synthetic=True,
                )
                payload[missing] = ""
                with self.assertRaises(EventValidationError):
                    Event.create(**payload)

    def test_unknown_source_is_rejected(self) -> None:
        with self.assertRaises(EventValidationError):
            _event(source="telepathy")

    def test_synthetic_must_be_an_explicit_bool(self) -> None:
        """Not defaulted, not inferred — the boundary states it."""
        with self.assertRaises(EventValidationError):
            _event(synthetic="yes")  # type: ignore[arg-type]

    def test_unknown_visibility_is_rejected(self) -> None:
        with self.assertRaises(EventValidationError):
            _event(visibility="secret")

    def test_event_id_is_deterministic_from_content(self) -> None:
        self.assertEqual(_event().event_id, _event().event_id)

    def test_identical_acts_in_one_turn_stay_distinct(self) -> None:
        """Same content twice in a turn must not collapse into one event."""
        first = _event(occurrence=0)
        second = _event(occurrence=1)
        self.assertNotEqual(first.event_id, second.event_id)

    def test_content_change_changes_the_id(self) -> None:
        self.assertNotEqual(_event(content="a").event_id, _event(content="b").event_id)

    def test_round_trip_through_json_preserves_identity(self) -> None:
        event = _event()
        self.assertEqual(Event.from_dict(json.loads(event.to_json())), event)

    def test_missing_payload_field_is_reported(self) -> None:
        payload = _event().to_dict()
        del payload["actor"]
        with self.assertRaises(EventValidationError):
            Event.from_dict(payload)

    def test_ordering_key_is_turn_not_timestamp(self) -> None:
        """Contradictory timestamps must not affect order."""
        late_turn_early_stamp = _event(turn=5, timestamp="2026-01-01T00:00:00Z")
        early_turn_late_stamp = _event(turn=1, timestamp="2099-01-01T00:00:00Z")
        ordered = sorted([late_turn_early_stamp, early_turn_late_stamp], key=order_key)
        self.assertEqual([e.turn for e in ordered], [1, 5])

    def test_public_communication_flag(self) -> None:
        self.assertTrue(_event().is_public_communication())
        self.assertFalse(_event(visibility="private").is_public_communication())


class ReducerTests(unittest.TestCase):
    def _log(self) -> list[Event]:
        a, b = fixture_id("resident-a"), fixture_id("org-b")
        return [
            Event.create(simulation_id="s1", turn=0, actor=a, action_type="communicate",
                         source="tabletop", synthetic=True, content="hi", location="square"),
            Event.create(simulation_id="s1", turn=1, actor=a, action_type="mention",
                         source="tabletop", synthetic=True, target=b, content="names b"),
            Event.create(simulation_id="s1", turn=1, actor=b, action_type="observe",
                         source="system", synthetic=True, location="square"),
        ]

    def test_state_derives_entities_relations_and_activity(self) -> None:
        state = reduce_events(self._log())
        self.assertEqual(state.simulation_id, "s1")
        self.assertEqual(state.event_count, 3)
        self.assertEqual(state.last_turn, 1)
        self.assertIn(fixture_id("resident-a"), state.entities)
        self.assertIn(fixture_id("org-b"), state.entities)
        self.assertEqual(
            state.relations[(fixture_id("resident-a"), "mention", fixture_id("org-b"))], 1
        )

    def test_reduction_is_deterministic(self) -> None:
        self.assertEqual(replay_digest(self._log()), replay_digest(self._log()))

    def test_state_dict_is_stable_across_replays(self) -> None:
        first = json.dumps(reduce_events(self._log()).as_dict(), sort_keys=True)
        second = json.dumps(reduce_events(self._log()).as_dict(), sort_keys=True)
        self.assertEqual(first, second)

    def test_set_like_fields_are_sorted_for_stability(self) -> None:
        """A set rendered unordered would make replays differ."""
        a = fixture_id("resident-a")
        events = [
            Event.create(simulation_id="s1", turn=t, actor=a, action_type="observe",
                         source="system", synthetic=True, location=place)
            for t, place in enumerate(["zeta", "alpha", "mid"])
        ]
        state = reduce_events(events)
        self.assertEqual(state.as_dict()["locations"][a], ["alpha", "mid", "zeta"])

    def test_public_communications_exclude_private_ones(self) -> None:
        a = fixture_id("resident-a")
        events = [
            Event.create(simulation_id="s1", turn=0, actor=a, action_type="communicate",
                         source="tabletop", synthetic=True, content="public one"),
            Event.create(simulation_id="s1", turn=1, actor=a, action_type="communicate",
                         source="tabletop", synthetic=True, content="private one",
                         visibility="private"),
        ]
        contents = [c["content"] for c in reduce_events(events).public_communications]
        self.assertEqual(contents, ["public one"])

    def test_unknown_action_type_is_history_but_not_a_relation(self) -> None:
        """The reducer must not require a canonical action vocabulary."""
        a = fixture_id("resident-a")
        event = Event.create(simulation_id="s1", turn=0, actor=a,
                             action_type="author_invented_verb", source="tabletop",
                             synthetic=True, target=fixture_id("other"))
        state = reduce_events([event])
        self.assertEqual(state.event_count, 1)
        self.assertEqual(state.relations, {})

    def test_no_derived_mechanics_are_computed(self) -> None:
        """Storing an unspecified quantity would invent a mechanic (spec §2.2)."""
        payload = json.dumps(reduce_events(self._log()).as_dict()).lower()
        for invented in ("power", "legitimacy", "cohesion", "trust", "influence", "score"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, payload)

    def test_reducing_across_runs_is_refused(self) -> None:
        events = self._log()
        events.append(
            Event.create(simulation_id="OTHER", turn=2, actor="x", action_type="observe",
                         source="system", synthetic=True)
        )
        with self.assertRaises(ReducerError):
            reduce_events(events)

    def test_mixing_synthetic_and_empirical_events_is_refused(self) -> None:
        events = self._log()
        events.append(
            Event.create(simulation_id="s1", turn=2, actor="x", action_type="observe",
                         source="system", synthetic=False)
        )
        with self.assertRaises(ReducerError):
            reduce_events(events)

    def test_replay_matches_direct_reduction(self) -> None:
        events = self._log()
        self.assertEqual(replay("s1", events).as_dict(), reduce_events(events).as_dict())
        self.assertEqual(replay_digest(events), replay_digest(events))


class EventLogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "sim.sqlite"
        self.connection = connect(self.path)
        self.addCleanup(self.connection.close)
        self.addCleanup(self.tmp.cleanup)

    def test_append_and_read_back_in_canonical_order(self) -> None:
        events = [
            _event(turn=2, content="third"),
            _event(turn=0, content="first"),
            _event(turn=1, content="second"),
        ]
        self.assertEqual(append(self.connection, *events), 3)
        turns = [event.turn for event in list_events(self.connection, "sim-test")]
        self.assertEqual(turns, [0, 1, 2])

    def test_append_is_idempotent(self) -> None:
        event = _event()
        self.assertEqual(append(self.connection, event), 1)
        self.assertEqual(append(self.connection, event), 0, "duplicate must be skipped")
        self.assertEqual(count_events(self.connection, "sim-test"), 1)

    def test_log_survives_reopening(self) -> None:
        append(self.connection, _event())
        reopened = connect(self.path)
        self.addCleanup(reopened.close)
        self.assertEqual(count_events(reopened, "sim-test"), 1)

    def test_log_is_append_only(self) -> None:
        append(self.connection, _event(turn=0), _event(turn=1), _event(turn=2))
        assert_append_only(self.connection)
        self.connection.execute("DELETE FROM events WHERE seq = 2")
        self.connection.commit()
        with self.assertRaises(EventLogError):
            assert_append_only(self.connection)

    def test_runs_are_listed_with_span_and_synthetic_flag(self) -> None:
        append(self.connection, _event(turn=0), _event(turn=3))
        runs = list_simulations(self.connection)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["event_count"], 2)
        self.assertEqual(runs[0]["first_turn"], 0)
        self.assertEqual(runs[0]["last_turn"], 3)
        self.assertTrue(runs[0]["synthetic"])
        self.assertFalse(runs[0]["mixed_synthetic"])

    def test_export_refuses_to_pass_synthetic_data_as_empirical(self) -> None:
        """The structural half of the simulation/empirical rule (spec §5)."""
        append(self.connection, _event())
        with self.assertRaises(EventLogError):
            list_exchanges_for_export(self.connection, "sim-test", synthetic=False)

    def test_export_returns_public_communications_of_a_synthetic_run(self) -> None:
        append(
            self.connection,
            _event(turn=0, content="public"),
            _event(turn=1, content="hidden", visibility="private"),
        )
        exported = list_exchanges_for_export(self.connection, "sim-test", synthetic=True)
        self.assertEqual([e.content for e in exported], ["public"])

    def test_export_of_unknown_run_is_empty_not_an_error(self) -> None:
        self.assertEqual(
            list_exchanges_for_export(self.connection, "nope", synthetic=True), []
        )


class EngineTests(unittest.TestCase):
    def _sim(self) -> Simulation:
        return Simulation(simulation_id="sim-fixture", source="tabletop")

    def test_run_is_synthetic_by_construction(self) -> None:
        with self.assertRaises(ValueError):
            Simulation(simulation_id="s", synthetic=False)

    def test_emit_uses_the_run_source_not_the_actor(self) -> None:
        """Provenance is set by the boundary; an actor cannot claim another view."""
        sim = self._sim()
        event = sim.emit(actor=fixture_id("a"), action_type="communicate", content="x")
        self.assertEqual(event.source, "tabletop")
        self.assertTrue(event.synthetic)

    def test_turn_advances_and_events_land_in_the_right_turn(self) -> None:
        sim = self._sim()

        def actor(**_: object):
            return [dict(actor=fixture_id("a"), action_type="communicate", content="c")]

        sim.run([actor], turns=3)
        self.assertEqual([e.turn for e in sim.events], [0, 1, 2])
        self.assertEqual(sim.turn, 3)

    def test_identical_decisions_in_a_turn_both_land(self) -> None:
        sim = self._sim()

        def actor(**_: object):
            return [dict(actor=fixture_id("a"), action_type="communicate", content="same")] * 2

        sim.run([actor], turns=1)
        ids = {e.event_id for e in sim.events}
        self.assertEqual(len(sim.events), 2)
        self.assertEqual(len(ids), 2, "identical acts must not collapse")

    def test_actor_may_abstain(self) -> None:
        sim = self._sim()
        sim.run([lambda **_: []], turns=2)
        self.assertEqual(sim.events, [])
        self.assertEqual(sim.turn, 2)

    def test_state_is_always_the_reduction_of_the_log(self) -> None:
        sim = self._sim()

        def actor(**_: object):
            return [dict(actor=fixture_id("a"), action_type="communicate", content="c")]

        sim.run([actor], turns=2)
        self.assertEqual(sim.state.as_dict(), reduce_events(sim.events).as_dict())

    def test_replay_of_a_saved_run_reproduces_the_state(self) -> None:
        sim = self._sim()

        def actor(**_: object):
            return [dict(actor=fixture_id("a"), action_type="mention",
                         target=fixture_id("b"), content="c")]

        sim.run([actor], turns=3)
        replayed = replay(sim.simulation_id, sim.events)
        self.assertEqual(replayed.as_dict(), sim.state.as_dict())


class BranchTests(unittest.TestCase):
    def _run(self) -> Simulation:
        sim = Simulation(simulation_id="sim-origin", source="tabletop")

        def actor(**_: object):
            return [dict(actor=fixture_id("a"), action_type="communicate", content="c")]

        sim.run([actor], turns=4)
        return sim

    def test_branch_shares_the_prefix_state_exactly(self) -> None:
        """A counterfactual must start from a provably identical state."""
        origin = self._run()
        branch = origin.branch(through_turn=1)

        def prefix_state(events: list) -> dict:
            # Reduce under each log's own run id, then drop it: run identity
            # legitimately differs (a branch *is* a different run), and every other
            # field must be identical -- which is the actual claim.
            payload = reduce_events(events).as_dict()
            payload.pop("simulation_id")
            return payload

        self.assertEqual(
            prefix_state([e for e in origin.events if e.turn <= 1]),
            prefix_state(branch.events),
        )
        self.assertEqual(len(branch.events), 2, "prefix through turn 1 is two events")
        self.assertNotEqual(branch.simulation_id, origin.simulation_id)

    def test_branch_has_its_own_identity_and_lineage(self) -> None:
        origin = self._run()
        branch = origin.branch(through_turn=1)
        self.assertNotEqual(branch.simulation_id, origin.simulation_id)
        self.assertEqual(branch.branch_of, "sim-origin")
        self.assertEqual(branch.lineage()["branch_of"], "sim-origin")

    def test_branch_advances_from_the_divergence_point(self) -> None:
        origin = self._run()
        branch = origin.branch(through_turn=1)
        self.assertEqual(branch.turn, 2)
        branch.emit(actor=fixture_id("c"), action_type="communicate", content="different")
        self.assertEqual(branch.events[-1].turn, 2)

    def test_branches_diverge_from_each_other(self) -> None:
        origin = self._run()
        left = origin.branch(through_turn=1)
        right = origin.branch(through_turn=1)
        left.emit(actor=fixture_id("a"), action_type="communicate", content="LEFT")
        right.emit(actor=fixture_id("a"), action_type="observe", location="RIGHT")
        self.assertNotEqual(replay_digest(left.events), replay_digest(right.events))

    def test_branch_beyond_the_log_is_refused(self) -> None:
        origin = self._run()
        with self.assertRaises(ValueError):
            origin.branch(through_turn=99)


class FixtureMarkingTests(unittest.TestCase):
    def test_fixture_ids_are_visibly_marked(self) -> None:
        """Nothing in the core may look like author-specified setting content."""
        self.assertTrue(is_fixture_id(fixture_id("resident-a")))
        self.assertFalse(is_fixture_id("Kokkola"))

    def test_fixture_relations_are_not_declared_canonical(self) -> None:
        from simulation import FIXTURE_RELATIONS

        import re

        source = (ROOT / "src" / "simulation" / "engine.py").read_text(encoding="utf-8")
        self.assertIn("NOT a canonical vocabulary", source)
        # A bare `RELATIONS = (` would be a declared vocabulary. Match the
        # assignment itself rather than a substring, which otherwise matches
        # `FIXTURE_RELATIONS = (`.
        declared = re.findall(r"(?m)^\s*([A-Z_]+)\s*=\s*\(", source)
        self.assertEqual(
            [name for name in declared if "RELATION" in name],
            ["FIXTURE_RELATIONS"],
            "only the fixture relation tuple may be declared; a canonical "
            "vocabulary must not appear before the author confirms DEFER-2",
        )
        for relation in FIXTURE_RELATIONS:
            with self.subTest(relation=relation):
                self.assertIn(relation, FIXTURE_RELATIONS)


if __name__ == "__main__":
    unittest.main()
