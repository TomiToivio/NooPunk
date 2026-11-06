"""#1286 work package 1: the simulator kernel, tested by the acceptance conditions in the issue.

The suite is deliberately adversarial about three things: **reproducibility**, the **four origins** staying apart, and
the kernel having **no RPG dependency** — because those are the three ways this phase would quietly go wrong.

Every fixture is synthetic. No AI26 data, no real person and no RPG record is used here.
"""

from __future__ import annotations

import json
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from social_sim import (  # noqa: E402
    Actor, ActorKind, CommunicationEdge, Event, EventKind, KernelError, Origin, Provenance,
    Simulation, SocialEdge, build, resolve_rule,
)


def population() -> Simulation:
    """A small synthetic scene: one organization, three individuals, one isolated actor."""
    return build(
        [
            Actor("org.party", ActorKind.ORGANIZATION, role="institution"),
            Actor("a.one", affiliation="org.party", role="speaker"),
            Actor("a.two", affiliation="org.party", role="member"),
            Actor("a.three", role="journalist"),
            Actor("a.lonely"),
        ],
        [
            SocialEdge("a.one", "a.two", "colleague"),
            SocialEdge("a.two", "a.three", "source"),
            SocialEdge("a.one", "a.three", "contact"),
        ],
        seed=11,
    )


class ReproducibilityTests(unittest.TestCase):
    def test_the_same_seed_and_inputs_produce_the_same_stream(self):
        first, second = population(), population()
        first.run(20)
        second.run(20)
        self.assertEqual(first.digest(), second.digest())
        self.assertEqual([e.event_id for e in first.events], [e.event_id for e in second.events])

    def test_a_different_seed_produces_a_different_stream(self):
        first, second = population(), build(
            [Actor("org.party", ActorKind.ORGANIZATION), Actor("a.one", affiliation="org.party"),
             Actor("a.two", affiliation="org.party"), Actor("a.three"), Actor("a.lonely")],
            [SocialEdge("a.one", "a.two", "colleague"), SocialEdge("a.two", "a.three", "source"),
             SocialEdge("a.one", "a.three", "contact")],
            seed=12,
        )
        first.run(20)
        second.run(20)
        self.assertNotEqual(first.digest(), second.digest())

    def test_a_resumed_run_continues_rather_than_restarting(self):
        one = population()
        one.run(10)
        two = population()
        two.run(5)
        two.run(5)
        self.assertEqual(one.digest(), two.digest())

    def test_the_snapshot_reproduces_the_run(self):
        original = population()
        original.run(12)
        restored = Simulation.from_snapshot(json.loads(json.dumps(original.snapshot())))
        self.assertEqual(restored.step, original.step)
        self.assertEqual(restored.digest(), original.digest())
        restored.run(4)
        original.run(4)
        self.assertEqual(restored.digest(), original.digest())

    def test_a_tampered_snapshot_is_refused(self):
        simulation = population()
        simulation.run(3)          # a snapshot with no events has nothing to tamper with
        snapshot = simulation.snapshot()
        snapshot["events"] = []
        with self.assertRaises(KernelError):
            Simulation.from_snapshot(snapshot)

    def test_an_unknown_kernel_version_is_refused(self):
        snapshot = population().snapshot()
        snapshot["kernel_version"] = 99
        with self.assertRaises(KernelError):
            Simulation.from_snapshot(snapshot)


class EventIntegrityTests(unittest.TestCase):
    def test_events_are_ordered_by_step_then_sequence(self):
        simulation = population()
        simulation.run(15)
        keys = [(event.step, event.sequence) for event in simulation.events]
        self.assertEqual(keys, sorted(keys))

    def test_every_event_cites_its_rule_and_an_input(self):
        simulation = population()
        simulation.run(10)
        self.assertTrue(simulation.events)
        for event in simulation.events:
            self.assertEqual(event.rule, "broadcast")
            self.assertTrue(event.inputs, event.event_id)
            self.assertTrue(event.inputs[0].startswith("tie:"), event.inputs)

    def test_an_unknown_rule_is_refused_rather_than_invented(self):
        with self.assertRaises(KernelError):
            resolve_rule("does_not_exist")
        with self.assertRaises(KernelError):
            population().run(1, rule="llm_roleplay")

    def test_an_event_that_claims_observed_origin_is_refused(self):
        """Simulator events are simulated. Observed material enters as records, never as events."""
        with self.assertRaises(KernelError):
            Event(step=1, sequence=0, kind=EventKind.COMMUNICATE, actor="a.one", rule="broadcast",
                  provenance=Provenance(Origin.OBSERVED, source="corpus"))

    def test_an_event_without_a_rule_is_refused(self):
        with self.assertRaises(KernelError):
            Event(step=1, sequence=0, kind=EventKind.COMMUNICATE, actor="a.one")

    def test_the_noop_rule_produces_nothing(self):
        simulation = population()
        self.assertEqual(simulation.run(5, rule="noop"), ())
        self.assertEqual(simulation.events, [])
        self.assertEqual(simulation.step, 5, "the clock still advances; the population simply does nothing")


class ProvenanceTests(unittest.TestCase):
    def test_the_four_origins_are_distinct_and_survive_a_round_trip(self):
        for origin in Origin:
            provenance = Provenance(origin, source="fixture", method="test", uncertainty="high",
                                     review_status="provisional")
            restored = Provenance.from_dict(json.loads(json.dumps(provenance.to_dict())))
            self.assertEqual(restored, provenance)
            self.assertEqual(restored.origin, origin)

    def test_a_record_without_an_origin_is_refused(self):
        with self.assertRaises(KernelError):
            Provenance.from_dict({"source": "nowhere"})

    def test_actor_provenance_survives_the_snapshot(self):
        simulation = build([
            Actor("a.one", provenance=Provenance(Origin.INFERRED, source="analysis:statement-7",
                                                method="actor_projection", uncertainty="ambiguous")),
        ])
        restored = Simulation.from_snapshot(json.loads(json.dumps(simulation.snapshot())))
        self.assertEqual(restored.actors["a.one"].provenance.origin, Origin.INFERRED)
        self.assertEqual(restored.actors["a.one"].provenance.uncertainty, "ambiguous")


class PopulationTests(unittest.TestCase):
    def test_organizations_and_individuals_stay_distinct(self):
        simulation = population()
        self.assertIs(simulation.actors["org.party"].kind, ActorKind.ORGANIZATION)
        self.assertIs(simulation.actors["a.one"].kind, ActorKind.INDIVIDUAL)

    def test_an_affiliation_must_point_at_an_organization(self):
        with self.assertRaises(KernelError):
            build([Actor("a.one", affiliation="a.two"), Actor("a.two")])
        with self.assertRaises(KernelError):
            build([Actor("a.one", affiliation="nobody")])

    def test_a_social_edge_must_join_known_actors(self):
        with self.assertRaises(KernelError):
            build([Actor("a.one")], [SocialEdge("a.one", "ghost", "contact")])

    def test_an_isolated_actor_is_legitimate_and_kept(self):
        simulation = population()
        self.assertIn("a.lonely", simulation.isolated())
        simulation.run(5)
        self.assertIn("a.lonely", simulation.actors)
        self.assertNotIn("a.lonely", [event.actor for event in simulation.events])

    def test_an_empty_population_runs(self):
        simulation = build([], [])
        self.assertEqual(simulation.run(5), ())
        self.assertEqual(simulation.actors, {})

    def test_duplicate_actor_ids_are_refused(self):
        simulation = population()
        with self.assertRaises(KernelError):
            simulation.add_actor(Actor("a.one"))

    def test_negative_resources_are_refused(self):
        with self.assertRaises(KernelError):
            Actor("a.one", resources=-1)

    def test_a_rule_cannot_produce_an_unknown_pair(self):
        simulation = population()
        def liar(_state, _rng, _step):
            return (("a.one", "nobody"),)
        from social_sim import kernel
        kernel.RULES["liar"] = liar
        try:
            with self.assertRaises(KernelError):
                simulation.run(1, rule="liar")
        finally:
            del kernel.RULES["liar"]


class BoundaryTests(unittest.TestCase):
    def test_the_kernel_imports_no_rpg_module(self):
        """#1286's scope rule, as a test: the simulator must run without the RPG present."""
        source = (ROOT / "src" / "social_sim" / "kernel.py").read_text(encoding="utf-8")
        for forbidden in ("from src.rules", "import rules", "from rules", "src.world", "from world",
                          "src.console", "src.simulation", "evennia", "godot"):
            self.assertNotIn(forbidden, source, forbidden)

    def test_a_modest_population_runs_quickly(self):
        """The issue asks for a baseline benchmark at modest N, with no per-agent LLM call."""
        actors = [Actor(f"a.{index}") for index in range(200)]
        edges = [SocialEdge(f"a.{index}", f"a.{(index + 1) % 200}", "tie") for index in range(200)]
        simulation = build(actors, edges, seed=3)
        started = time.perf_counter()
        simulation.run(100)
        elapsed = time.perf_counter() - started
        self.assertEqual(len(simulation.events), 100)
        self.assertLess(elapsed, 5.0, f"200 actors, 100 steps took {elapsed:.2f}s")


if __name__ == "__main__":
    unittest.main()
