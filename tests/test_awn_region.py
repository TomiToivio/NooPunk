"""The two-level world model of #1045: collapse is per region, and the world keeps running.

The tests pin the five rules the module exists to enforce, because each one is easy to lose in a
refactor and impossible to notice at a table until a session plays as if the whole planet ended.
"""
import json
import unittest

from src.rules.awn_region import (
    LADDER,
    RegionError,
    RegionEvent,
    RegionLedger,
    RegionState,
    transition_allowed,
)


def _state(region="helsinki", date="2026-03-01", **overrides):
    fields = {
        "physical_infrastructure": "functioning",
        "public_safety": "functioning",
        "supplies": "functioning",
        "communications": "functioning",
    }
    fields.update(overrides)
    return RegionState(region=region, date=date, **fields)


class FunctioningRegionTests(unittest.TestCase):
    def test_a_functioning_region_activates_no_overlay(self):
        state = _state()
        self.assertTrue(state.is_functioning)
        self.assertEqual(state.active_overlays(), (),
                         "ordinary CWN: no scarcity bookkeeping, no stress, no site hazards")

    def test_after_the_fall_activates_the_p0_overlays(self):
        state = _state(supplies="after_the_fall")
        self.assertFalse(state.is_functioning)
        self.assertEqual(state.active_overlays(),
                         ("privation_strain", "site_hazards", "travel_and_supplies"))

    def test_emergency_activates_only_privation(self):
        self.assertEqual(_state(public_safety="emergency").active_overlays(), ("privation_strain",))

    def test_an_anomaly_overlay_is_additive_and_independent_of_material_collapse(self):
        state = _state(anomaly="persistent")
        self.assertEqual(state.active_overlays(), ("anomaly_response",),
                         "a functioning city can still have a breached undercity")


class TransitionRuleTests(unittest.TestCase):
    def test_collapse_may_skip_rungs_and_recovery_may_not(self):
        self.assertTrue(transition_allowed("functioning", "after_the_fall"),
                        "a breach can drop a region in one event")
        self.assertTrue(transition_allowed("after_the_fall", "emergency"))
        self.assertFalse(transition_allowed("after_the_fall", "functioning"),
                         "recovery is earned one rung at a time")
        self.assertFalse(transition_allowed("emergency", "emergency"),
                         "a no-op transition is not a change")

    def test_the_ladder_order_is_the_severity_order(self):
        self.assertEqual(LADDER, ("functioning", "recovering", "emergency", "after_the_fall"))

    def test_a_transition_without_a_cause_is_refused(self):
        with self.assertRaises(RegionError):
            RegionEvent(date="2026-04-01", region="helsinki", axis="supplies",
                        to="emergency", cause="   ")

    def test_a_transition_without_an_axis_is_refused(self):
        ledger = RegionLedger()
        ledger.record(_state())
        with self.assertRaises(RegionError):
            ledger.transition(RegionEvent(date="2026-04-01", region="helsinki", axis=None,
                                          to=None, cause="a convoy was lost"))

    def test_a_recovery_that_skips_rungs_is_refused(self):
        ledger = RegionLedger()
        ledger.record(_state(supplies="after_the_fall"))
        with self.assertRaises(RegionError):
            ledger.transition(RegionEvent(date="2026-04-01", region="helsinki", axis="supplies",
                                          to="functioning", cause="the harbour reopened"))
        climbed = ledger.transition(RegionEvent(
            date="2026-04-01", region="helsinki", axis="supplies",
            to="emergency", cause="the harbour reopened"))
        self.assertEqual(climbed.axis("supplies"), "emergency")

    def test_a_state_change_without_a_recorded_event_is_refused(self):
        ledger = RegionLedger()
        ledger.record(_state())
        with self.assertRaises(RegionError):
            ledger.record(_state(date="2026-04-01", supplies="emergency"))

    def test_dates_are_monotonic_in_the_ledger(self):
        ledger = RegionLedger()
        ledger.record(_state(date="2026-05-01"))
        with self.assertRaises(RegionError):
            ledger.record(_state(date="2026-04-01"))


class WorldAggregateTests(unittest.TestCase):
    def _world(self):
        ledger = RegionLedger()
        ledger.record(_state("helsinki", "2026-03-01"))
        ledger.record(_state("tampere", "2026-03-01"))
        ledger.record(_state("kainuu", "2026-03-01", supplies="after_the_fall",
                             public_safety="emergency", anomaly="sporadic"))
        return ledger

    def test_the_world_aggregates_regions_instead_of_being_a_second_state(self):
        summary = self._world().world_at("2026-03-01")
        self.assertEqual(summary["regions"], 3)
        self.assertEqual(summary["by_worst_material_axis"]["functioning"], 2)
        self.assertEqual(summary["by_worst_material_axis"]["after_the_fall"], 1)
        self.assertEqual(summary["functioning"], ["helsinki", "tampere"])
        self.assertFalse(summary["treats_collapse_as_global"],
                         "a crisis campaign is a run of events, not a scripted apocalypse")

    def test_state_at_reads_the_version_in_force(self):
        ledger = self._world()
        ledger.transition(RegionEvent(date="2026-06-01", region="tampere", axis="supplies",
                                      to="emergency", cause="rail strike"))
        before = ledger.state_at("tampere", "2026-05-01")
        after = ledger.state_at("tampere", "2026-06-01")
        assert before is not None and after is not None
        self.assertEqual(before.axis("supplies"), "functioning")
        self.assertEqual(after.axis("supplies"), "emergency")

    def test_the_ledger_round_trips_through_json(self):
        ledger = self._world()
        ledger.transition(RegionEvent(date="2026-06-01", region="tampere", axis="supplies",
                                      to="emergency", cause="rail strike"))
        again = RegionLedger.from_dict(json.loads(json.dumps(ledger.to_dict())))
        self.assertEqual(again.to_dict(), ledger.to_dict())


class ValidationTests(unittest.TestCase):
    def test_unknown_axis_values_are_refused(self):
        with self.assertRaises(RegionError):
            _state(supplies="apocalyptic")
        with self.assertRaises(RegionError):
            _state(anomaly="haunted")
        with self.assertRaises(RegionError):
            _state(governance="junta")
        with self.assertRaises(RegionError):
            _state(ontological_shock="total")

    def test_a_state_needs_a_region_and_a_date(self):
        with self.assertRaises(RegionError):
            _state(region="")
        with self.assertRaises(RegionError):
            _state(date="")

    def test_governance_can_be_contested_without_leaving_the_ladder(self):
        ledger = RegionLedger()
        ledger.record(_state())
        state = ledger.transition(RegionEvent(
            date="2026-04-01", region="helsinki", axis="governance", to="contested",
            cause="the council lost quorum"))
        self.assertEqual(state.axis("governance"), "contested")
        self.assertFalse(state.is_functioning)


if __name__ == "__main__":
    unittest.main()
