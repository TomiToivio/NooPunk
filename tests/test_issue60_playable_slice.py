"""Tests for the playable character-sheet seam (#60 milestone items 4-11).

The point of these tests is that the *playable loop* resolves through the EP2
kernel. So they assert behaviour through the engine's own verbs rather than only
calling the sheet module directly, and every stochastic case injects its roll so a
failure means a bug rather than an unlucky seed.

Two invariants get explicit guards because they are easy to erode later:

* an actor **without** a sheet keeps playing exactly as before (nothing removed);
* a mistyped or missing value is an **error**, never a silent default - a defaulted
  modifier changes a mechanical outcome.
"""

from __future__ import annotations

import random
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclipse_phase_homebrew import PoolKind
from text_game.actions import parse_command
from text_game.engine import GameEngine
from text_game.model import FIXTURE_PREFIX, ActorState, fixture_world
from text_game.persistence import load_game, save_game
from text_game.sheet import (
    CharacterSheet,
    SheetError,
    fixture_sheets,
    resolve_sheet_test,
)

HUMAN = FIXTURE_PREFIX + "human"
GREETER = FIXTURE_PREFIX + "greeter"
WANDERER = FIXTURE_PREFIX + "wanderer"


class SheetModelTests(unittest.TestCase):
    def test_sheet_rejects_impossible_ratings(self) -> None:
        with self.assertRaises(SheetError):
            CharacterSheet(name="x", skills={"Perceive": 101})
        with self.assertRaises(SheetError):
            CharacterSheet(name="x", aptitudes={"COG": -1})

    def test_sheet_rejects_a_blank_name(self) -> None:
        with self.assertRaises(SheetError):
            CharacterSheet(name="   ")

    def test_unknown_skill_is_refused_not_defaulted_to_zero(self) -> None:
        """A missing skill must not become a made-up number."""
        sheet = CharacterSheet(name="x", skills={"Perceive": 50}, aptitudes={"COG": 40})
        with self.assertRaises(SheetError):
            sheet.target_for(skill="DoesNotExist")

    def test_defaulting_uses_aptitude_and_flags_the_test(self) -> None:
        sheet = CharacterSheet(name="x", aptitudes={"COG": 40})
        target, defaulted = sheet.target_for(skill="Missing", aptitude="COG")
        self.assertEqual(target, 40)
        self.assertTrue(defaulted)

    def test_known_skill_is_not_flagged_as_defaulted(self) -> None:
        sheet = CharacterSheet(name="x", skills={"Perceive": 55}, aptitudes={"COG": 40})
        target, defaulted = sheet.target_for(skill="Perceive")
        self.assertEqual(target, 55)
        self.assertFalse(defaulted)

    def test_sheet_round_trips_through_a_dict(self) -> None:
        sheet = fixture_sheets()[HUMAN]
        sheet.harm.apply_damage(9)
        sheet.pools.spend(PoolKind.INSIGHT)
        self.assertEqual(CharacterSheet.from_dict(sheet.to_dict()).to_dict(), sheet.to_dict())

    def test_fixture_sheets_are_non_canonical(self) -> None:
        """Fixture data must not be mistakable for setting material."""
        for sheet in fixture_sheets().values():
            with self.subTest(sheet=sheet.name):
                self.assertIn("fixture", sheet.name.casefold())


class DeterministicResolutionTests(unittest.TestCase):
    """Reproducibility: an injected roll is the only randomness."""

    def setUp(self) -> None:
        self.sheet = fixture_sheets()[HUMAN]

    def test_injected_roll_decides_the_outcome(self) -> None:
        self.assertTrue(resolve_sheet_test(self.sheet, skill="Perceive", roll=40).succeeded)
        self.assertFalse(resolve_sheet_test(self.sheet, skill="Perceive", roll=95).succeeded)

    def test_same_seed_gives_the_same_result(self) -> None:
        first = resolve_sheet_test(self.sheet, skill="Perceive", rng=random.Random(7))
        second = resolve_sheet_test(self.sheet, skill="Perceive", rng=random.Random(7))
        self.assertEqual(first.detail["result"], second.detail["result"])

    def test_different_seeds_can_differ(self) -> None:
        rolls = {
            resolve_sheet_test(self.sheet, skill="Perceive", rng=random.Random(seed)).detail["result"]["roll"]
            for seed in range(12)
        }
        self.assertGreater(len(rolls), 1, "seeded rolls should not all be identical")

    def test_unknown_kind_is_refused(self) -> None:
        with self.assertRaises(SheetError):
            resolve_sheet_test(self.sheet, kind="telepathy", skill="Perceive")


class CombatTests(unittest.TestCase):
    def test_winning_applies_damage_and_wounds_to_the_defender(self) -> None:
        attacker = fixture_sheets()[HUMAN]
        defender = fixture_sheets()[WANDERER]
        resolution = resolve_sheet_test(
            attacker, kind="combat", skill="Perceive", modifier=40,
            defender_sheet=defender, defender_skill="Perceive",
            defender_roll=90, roll=20, damage=7,
        )
        self.assertTrue(resolution.succeeded)
        self.assertEqual(defender.harm.damage, 7)
        self.assertEqual(defender.harm.wounds, 1, "crossing the wound threshold must record a wound")

    def test_losing_applies_no_damage(self) -> None:
        attacker = fixture_sheets()[HUMAN]
        defender = fixture_sheets()[WANDERER]
        resolution = resolve_sheet_test(
            attacker, kind="combat", skill="Perceive", modifier=-40,
            defender_sheet=defender, defender_skill="Perceive",
            defender_roll=5, roll=95, damage=7,
        )
        self.assertFalse(resolution.succeeded)
        self.assertEqual(defender.harm.damage, 0)

    def test_combat_requires_defender_harm_state(self) -> None:
        attacker = fixture_sheets()[HUMAN]
        bare = CharacterSheet(name="bare", skills={"Perceive": 50})
        with self.assertRaises(SheetError):
            resolve_sheet_test(
                attacker, kind="combat", skill="Perceive", roll=20,
                defender_sheet=bare, defender_skill="Perceive", damage=5,
            )

    def test_opposed_kinds_need_a_defender(self) -> None:
        attacker = fixture_sheets()[HUMAN]
        for kind in ("social", "mesh", "combat"):
            with self.subTest(kind=kind), self.assertRaises(SheetError):
                resolve_sheet_test(attacker, kind=kind, skill="Persuade", roll=20)

    def test_social_and_mesh_apply_no_invented_effect(self) -> None:
        """The kernel resolves the contest; it does not invent a consequence."""
        attacker = fixture_sheets()[HUMAN]
        defender = fixture_sheets()[GREETER]
        for kind in ("social", "mesh"):
            with self.subTest(kind=kind):
                resolution = resolve_sheet_test(
                    attacker, kind=kind, skill="Persuade", modifier=40, roll=10,
                    defender_sheet=defender, defender_skill="Persuade", defender_roll=90,
                )
                self.assertTrue(resolution.succeeded)
                self.assertEqual(resolution.detail["result"]["effect_amount"], 0)


class EngineVerbTests(unittest.TestCase):
    """The milestone is a *playable* loop, so these drive the engine's own verbs."""

    def setUp(self) -> None:
        self.engine = GameEngine(world=fixture_world())

    def run_cmd(self, command: str):
        return self.engine.execute(parse_command(HUMAN, command))

    def test_sheet_verb_shows_the_character_sheet(self) -> None:
        text = self.run_cmd("sheet").text
        self.assertIn("Aptitudes", text)
        self.assertIn("Pools", text)
        self.assertIn("Harm", text)

    def test_skill_test_resolves_through_the_kernel(self) -> None:
        text = self.run_cmd("test skill Perceive roll 40").text
        self.assertIn("success", text)

    def test_roll_is_injected_so_the_engine_call_is_reproducible(self) -> None:
        first = GameEngine(world=fixture_world()).execute(
            parse_command(HUMAN, "test skill Perceive roll 40")).text
        second = GameEngine(world=fixture_world()).execute(
            parse_command(HUMAN, "test skill Perceive roll 40")).text
        self.assertEqual(first, second)

    def test_social_test_against_an_actor_in_the_room(self) -> None:
        """Only the attacker's roll is injectable via the verb, so assert the
        *resolution happened* rather than a fixed winner."""
        text = self.run_cmd("test social Persuade vs greeter roll 20").text
        self.assertIn("social:", text)
        self.assertTrue("you win" in text or "you lose" in text)

    def test_social_outcome_is_decided_by_the_kernel_not_the_verb(self) -> None:
        """With both rolls fixed, the winner is a property of the mechanics."""
        attacker = fixture_sheets()[HUMAN]
        defender = fixture_sheets()[GREETER]
        win = resolve_sheet_test(
            attacker, kind="social", skill="Persuade", roll=5,
            defender_sheet=defender, defender_skill="Persuade", defender_roll=95,
        )
        lose = resolve_sheet_test(
            attacker, kind="social", skill="Persuade", roll=95,
            defender_sheet=defender, defender_skill="Persuade", defender_roll=5,
        )
        self.assertTrue(win.succeeded)
        self.assertFalse(lose.succeeded)

    def test_combat_persists_damage_in_world_state(self) -> None:
        """Both rolls are pinned, so this asserts a mechanic rather than luck.

        It caught a genuine flake: with only the attacker's roll injected, whether
        the attack landed depended on a random defender roll, so the assertion passed
        or failed by chance. Injecting the defender's roll too makes it deterministic.
        """
        self.run_cmd(
            "test combat Perceive vs greeter defence Persuade damage 7 roll 30 defenderroll 90"
        )
        stored = self.engine.world.actors[GREETER].sheet["harm"]["damage"]
        self.assertEqual(stored, 7, "damage must survive the call, not just be reported")

    def test_combat_is_fully_reproducible_with_both_rolls_pinned(self) -> None:
        def run() -> str:
            engine = GameEngine(world=fixture_world())
            return engine.execute(parse_command(
                HUMAN,
                "test combat Perceive vs greeter defence Persuade damage 7 roll 30 defenderroll 90",
            )).text

        self.assertEqual(run(), run())

    def test_a_lost_contest_leaves_the_defender_undamaged(self) -> None:
        self.run_cmd(
            "test combat Perceive vs greeter defence Persuade damage 7 roll 95 defenderroll 5"
        )
        self.assertEqual(self.engine.world.actors[GREETER].sheet["harm"]["damage"], 0)

    def test_a_test_emits_an_event(self) -> None:
        before = len(self.engine.events)
        self.run_cmd("test skill Perceive roll 40")
        self.assertEqual(len(self.engine.events), before + 1)
        self.assertEqual(self.engine.events[-1].action_type, "test")

    def test_short_actor_and_item_names_resolve(self) -> None:
        """Fixture ids are prefixed; the player should not have to type the prefix."""
        self.run_cmd("north")
        self.assertIn("Taken", self.run_cmd("take token").text)
        self.assertIn("fixture token", self.run_cmd("inventory").text)

    def test_ambiguous_short_name_is_refused(self) -> None:
        world = fixture_world()
        world.actors["other:greeter"] = ActorState("other:greeter", "Other greeter", FIXTURE_PREFIX + "hub")
        world.actors["other:greeter"].sheet = fixture_sheets()[GREETER].to_dict()
        engine = GameEngine(world=world)
        with self.assertRaises(ValueError) as caught:
            engine.execute(parse_command(HUMAN, "test social Persuade vs greeter roll 20"))
        self.assertIn("mbiguous", str(caught.exception))


class RefusalTests(unittest.TestCase):
    """A silent default would change a mechanical result, so these must raise."""

    def setUp(self) -> None:
        self.engine = GameEngine(world=fixture_world())

    def attempt(self, command: str) -> str:
        try:
            self.engine.execute(parse_command(HUMAN, command))
        except ValueError as exc:
            return str(exc)
        return ""

    def test_missing_skill_name_is_refused(self) -> None:
        self.assertIn("skill name", self.attempt("test skill"))

    def test_unknown_kind_is_refused(self) -> None:
        self.assertIn("unknown test kind", self.attempt("test telepathy Perceive"))

    def test_non_integer_modifier_is_refused(self) -> None:
        self.assertIn("integer", self.attempt("test skill Perceive modifier x"))

    def test_opposed_test_without_opponent_is_refused(self) -> None:
        self.assertIn("needs an opponent", self.attempt("test social Persuade"))

    def test_unknown_opponent_is_refused(self) -> None:
        self.assertNotEqual(self.attempt("test social Persuade vs ghost roll 20"), "")

    def test_unknown_skill_is_refused(self) -> None:
        self.assertNotEqual(self.attempt("test skill Nonexistent roll 20"), "")

    def test_unknown_verb_is_still_refused(self) -> None:
        self.assertIn("Unknown command verb", self.attempt("teleport home"))


class AdditiveTests(unittest.TestCase):
    """Nothing was removed: sheet-free actors and sheet-free worlds still work."""

    def test_sheet_free_world_is_unchanged(self) -> None:
        world = fixture_world(with_sheets=False)
        for actor in world.actors.values():
            with self.subTest(actor=actor.actor_id):
                self.assertIsNone(actor.sheet)

    def test_sheet_free_actor_can_still_play(self) -> None:
        engine = GameEngine(world=fixture_world(with_sheets=False))
        self.assertIn("Fixture Hub", engine.execute(parse_command(HUMAN, "look")).text)

    def test_sheet_free_actor_is_refused_a_test_but_is_told_why(self) -> None:
        engine = GameEngine(world=fixture_world(with_sheets=False))
        with self.assertRaises(ValueError) as caught:
            engine.execute(parse_command(HUMAN, "test skill Perceive"))
        self.assertIn("no character sheet", str(caught.exception))

    def test_actor_state_round_trips_with_and_without_a_sheet(self) -> None:
        for with_sheet in (True, False):
            with self.subTest(with_sheet=with_sheet):
                world = fixture_world(with_sheets=with_sheet)
                actor = world.actors[HUMAN]
                restored = ActorState.from_dict(actor.to_dict())
                self.assertEqual(restored.to_dict(), actor.to_dict())

    def test_every_pre_existing_actor_field_survives(self) -> None:
        """The #51 fields must not be displaced by the sheet."""
        actor = fixture_world().actors[HUMAN]
        payload = actor.to_dict()
        for field in ("actor_id", "label", "room_id", "controller", "inventory", "dialogue"):
            with self.subTest(field=field):
                self.assertIn(field, payload)


class PersistenceTests(unittest.TestCase):
    def test_save_and_load_preserve_sheet_and_harm(self) -> None:
        engine = GameEngine(world=fixture_world())
        engine.execute(parse_command(HUMAN, "test combat Perceive vs greeter defence Persuade damage 9 roll 30"))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "save.json"
            save_game(engine, path)
            restored = load_game(path)
        self.assertEqual(
            restored.world.actors[GREETER].sheet["harm"]["damage"],
            engine.world.actors[GREETER].sheet["harm"]["damage"],
        )
        self.assertIsNotNone(restored.world.actors[HUMAN].sheet)

    def test_sheet_free_save_still_loads(self) -> None:
        """A save written before the sheet existed must keep working."""
        engine = GameEngine(world=fixture_world(with_sheets=False))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "save.json"
            save_game(engine, path)
            restored = load_game(path)
        self.assertIsNone(restored.world.actors[HUMAN].sheet)


class RoomIsolationTests(unittest.TestCase):
    def test_a_test_cannot_target_someone_in_another_room(self) -> None:
        engine = GameEngine(world=fixture_world())
        # The LLM contact is in the side room, not the hub.
        with self.assertRaises(ValueError):
            engine.execute(parse_command(HUMAN, "test social Persuade vs llm-contact roll 20"))

    def test_the_kernel_is_the_only_resolver(self) -> None:
        """The engine must not resolve mechanics itself; it delegates."""
        source = (ROOT / "src" / "text_game" / "engine.py").read_text(encoding="utf-8")
        self.assertIn("resolve_sheet_test", source)
        # No second dice mechanic hiding in the playable loop.
        self.assertNotIn("randint", source)


if __name__ == "__main__":
    unittest.main()
