"""The faction turn engine enforces procedure, not invented tables (#1043).

These tests are about *legality and auditability*: who may act, in what order, what a refusal looks
like, and whether the log can explain a finished round. The numbers (costs, income, hit points) are
scenario data in every case — if a test ever needed a rulebook constant, the design would be wrong.
"""
import json
import unittest

from src.rules.swn_faction_engine import (
    Asset,
    Attribute,
    Faction,
    FactionEngine,
    FactionEngineError,
    FactionProfile,
    Goal,
    GoalKind,
)


def profile(identifier: str, *, force=2, cunning=2, wealth=2, credits=10, hp=8, income=3,
            goal: Goal | None = None) -> FactionProfile:
    return FactionProfile(faction=Faction(identifier, credits), force=force, cunning=cunning,
                          wealth=wealth, hp=hp, max_hp=hp, goal=goal, income=income)


def engine_with(*profiles: FactionProfile) -> FactionEngine:
    engine = FactionEngine()
    for item in profiles:
        engine.register(item)
    return engine


class AttributeTests(unittest.TestCase):
    def test_ratings_are_banded(self):
        with self.assertRaises(FactionEngineError):
            profile("unsa", force=0)
        with self.assertRaises(FactionEngineError):
            profile("unsa", cunning=9)
        self.assertEqual(profile("unsa", force=8).attribute(Attribute.FORCE), 8)

    def test_income_and_hit_points_are_validated(self):
        with self.assertRaises(FactionEngineError):
            profile("unsa", income=-1)
        with self.assertRaises(FactionEngineError):
            FactionProfile(faction=Faction("unsa", 5), force=2, cunning=2, wealth=2, hp=9, max_hp=8)


class TurnOrderTests(unittest.TestCase):
    def test_highest_attribute_acts_first(self):
        engine = engine_with(profile("unsa", force=2), profile("zookeepers", cunning=7),
                             profile("orion", wealth=5))
        self.assertEqual(engine.order(), ["zookeepers", "orion", "unsa"])

    def test_ties_are_broken_deterministically_not_randomly(self):
        engine = engine_with(profile("b", force=4), profile("a", force=4))
        self.assertEqual(engine.order(), ["a", "b"])
        self.assertEqual(engine.order(), ["a", "b"], "repeated calls must agree")

    def test_the_tiebreak_attribute_is_configurable(self):
        engine = FactionEngine(order_tiebreak="wealth")
        engine.register(profile("wide", force=5, wealth=1))
        engine.register(profile("rich", force=5, wealth=6))
        self.assertEqual(engine.order(), ["rich", "wide"])

    def test_defeated_factions_drop_out_of_the_order(self):
        engine = engine_with(profile("unsa", force=6), profile("wrecked", force=1))
        engine.damage("wrecked", 8)
        self.assertEqual(engine.order(), ["unsa"])


class LegalityTests(unittest.TestCase):
    def test_one_action_per_faction_per_turn(self):
        engine = engine_with(profile("unsa"), profile("zookeepers"))
        engine.act("unsa", "expand")
        with self.assertRaises(FactionEngineError):
            engine.act("unsa", "move")
        engine.act("zookeepers", "repair")
        self.assertFalse(engine.action_available("unsa"))

    def test_unknown_actions_and_targets_are_refused(self):
        engine = engine_with(profile("unsa"), profile("zookeepers"))
        with self.assertRaises(FactionEngineError):
            engine.act("unsa", "summon")
        with self.assertRaises(FactionEngineError):
            engine.act("unsa", "attack", target="ghosts")
        with self.assertRaises(FactionEngineError):
            engine.act("unsa", "attack", target="unsa")

    def test_a_defeated_faction_cannot_act(self):
        engine = engine_with(profile("unsa"))
        engine.damage("unsa", 8)
        with self.assertRaises(FactionEngineError):
            engine.act("unsa", "expand")

    def test_purchase_is_the_turn_action_and_must_be_affordable(self):
        engine = engine_with(profile("unsa", credits=10))
        asset = Asset("cells", "unsa", "helsinki", hp=4, max_hp=4)
        engine.purchase("unsa", asset, cost=6)
        self.assertEqual(engine.profile("unsa").faction.credits, 4, "cost is spent, not ignored")
        with self.assertRaises(FactionEngineError):
            engine.purchase("unsa", Asset("more", "unsa", "helsinki", 4, 4), cost=1)

    def test_unaffordable_purchase_leaves_no_trace(self):
        engine = engine_with(profile("unsa", credits=3))
        with self.assertRaises(FactionEngineError):
            engine.purchase("unsa", Asset("cells", "unsa", "helsinki", 4, 4), cost=9)
        self.assertEqual(engine.profile("unsa").faction.assets, {})
        self.assertEqual(engine.audit()[-1]["event"], "faction.registered")


class RoundTests(unittest.TestCase):
    def test_income_lands_and_actions_reset(self):
        engine = engine_with(profile("unsa", credits=0, income=5))
        engine.act("unsa", "expand")
        summary = engine.end_round()
        self.assertEqual(summary["unsa"], {"income": 5, "credits": 5})
        self.assertTrue(engine.action_available("unsa"), "a new round grants a new action")
        self.assertEqual(engine.round, 2)

    def test_a_defeated_faction_earns_nothing(self):
        engine = engine_with(profile("wrecked", credits=2, income=4))
        engine.damage("wrecked", 8)
        summary = engine.end_round()
        self.assertEqual(summary["wrecked"], {"income": 0, "credits": 2})

    def test_audit_explains_a_round(self):
        engine = engine_with(profile("unsa", credits=10))
        engine.purchase("unsa", Asset("cells", "unsa", "helsinki", 4, 4), cost=4)
        engine.end_round()
        events = [(entry["round"], entry["event"]) for entry in engine.audit()]
        self.assertEqual(events[0], (1, "faction.registered"))
        self.assertIn((1, "faction.purchased"), events)
        self.assertIn((1, "round.closed"), events)
        purchased = next(entry for entry in engine.audit() if entry["event"] == "faction.purchased")
        self.assertEqual((purchased["asset"], purchased["cost"], purchased["credits"]), ("cells", 4, 6))

    def test_the_engine_serialises_for_persistence(self):
        engine = engine_with(profile("unsa", goal=Goal(GoalKind.IDEOLOGICAL, "public disclosure")))
        payload = json.loads(engine.to_json())
        self.assertEqual(payload["factions"]["unsa"]["goal"]["target"], "public disclosure")
        self.assertEqual(payload["round"], 1)


class GoalTests(unittest.TestCase):
    def test_progress_is_bounded_and_completes_once(self):
        goal = Goal(GoalKind.COMMERCIAL, "the harbour contract", needed=2)
        self.assertFalse(goal.advance())
        self.assertTrue(goal.advance())
        self.assertTrue(goal.advance(), "extra progress does not overshoot")
        self.assertEqual(goal.progress, 2)

    def test_invalid_goals_are_refused(self):
        with self.assertRaises(FactionEngineError):
            Goal(GoalKind.MILITARY, " ")
        with self.assertRaises(FactionEngineError):
            Goal(GoalKind.MILITARY, "the docks", progress=3, needed=2)


class CwnIndependenceTests(unittest.TestCase):
    def test_the_engine_holds_no_cwn_or_character_state(self):
        engine = engine_with(profile("unsa"))
        payload = json.loads(engine.to_json())
        self.assertEqual(set(payload), {"round", "acted", "log", "factions"})
        self.assertEqual(set(payload["factions"]["unsa"]),
                         {"force", "cunning", "wealth", "hp", "max_hp", "income", "credits", "goal"})


if __name__ == "__main__":
    unittest.main()
