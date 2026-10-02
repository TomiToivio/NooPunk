from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from simulation.sqlite_store import connect, list_events
from text_game.actions import parse_command
from text_game.actors import ConcordiaTextController, PatrolController
from text_game.engine import GameEngine
from text_game.model import FIXTURE_PREFIX, fixture_world
from text_game.persistence import load_game, save_game


HUMAN = FIXTURE_PREFIX + "human"
GREETER = FIXTURE_PREFIX + "greeter"
WANDERER = FIXTURE_PREFIX + "wanderer"
LLM_CONTACT = FIXTURE_PREFIX + "llm-contact"
LLM_PLAYER = FIXTURE_PREFIX + "llm-player"


class FakeModel:
    def __init__(self, responses: list[str]) -> None:
        self.responses = iter(responses)

    def sample_text(self, prompt: str = "") -> str:
        return next(self.responses)


class Issue51TextGameTests(unittest.TestCase):
    def test_parser_supports_mud_aliases(self) -> None:
        action = parse_command(HUMAN, "n")
        self.assertEqual(action.verb, "go")
        self.assertEqual(action.args, ("north",))
        self.assertEqual(parse_command(HUMAN, "i").verb, "inventory")

    def test_direct_route_can_complete_fixture_adventure(self) -> None:
        engine = GameEngine(fixture_world())
        engine.execute(parse_command(HUMAN, "north"))
        result = engine.execute(parse_command(HUMAN, "take fixture token"))
        self.assertTrue(result.completed)
        self.assertEqual(engine.world.adventure.completed_by, HUMAN)

    def test_second_route_can_complete_fixture_adventure(self) -> None:
        engine = GameEngine(fixture_world())
        engine.execute(parse_command(HUMAN, "east"))
        engine.execute(parse_command(HUMAN, "north"))
        result = engine.execute(parse_command(HUMAN, "take fixture token"))
        self.assertTrue(result.completed)

    def test_inventory_and_drop(self) -> None:
        engine = GameEngine(fixture_world())
        engine.execute(parse_command(HUMAN, "north"))
        engine.execute(parse_command(HUMAN, "take fixture token"))
        self.assertIn(FIXTURE_PREFIX + "token", engine.world.actors[HUMAN].inventory)
        engine.execute(parse_command(HUMAN, 'drop "fixture token"'))
        self.assertNotIn(FIXTURE_PREFIX + "token", engine.world.actors[HUMAN].inventory)

    def test_scripted_npc_dialogue(self) -> None:
        engine = GameEngine(fixture_world())
        result = engine.execute(parse_command(HUMAN, f"talk {GREETER} hello"))
        self.assertIn("goal can be reached", result.text)
        communications = [e for e in engine.events if e.action_type == "communicate"]
        self.assertEqual(len(communications), 2)

    def test_dumb_agent_uses_same_action_interface(self) -> None:
        world = fixture_world()
        controller = PatrolController(
            route={
                FIXTURE_PREFIX + "hub": "east",
                FIXTURE_PREFIX + "side": "west",
            }
        )
        engine = GameEngine(world, controllers={WANDERER: controller})
        engine.run_background_once()
        self.assertEqual(world.actors[WANDERER].room_id, FIXTURE_PREFIX + "side")
        self.assertEqual(engine.events[-1].action_type, "move")

    def test_llm_npc_conversation_is_logged_but_not_resolved_by_model(self) -> None:
        controller = ConcordiaTextController(FakeModel(["Fixture reply."]))
        engine = GameEngine(fixture_world(), controllers={LLM_CONTACT: controller})
        engine.execute(parse_command(HUMAN, "east"))
        result = engine.execute(parse_command(HUMAN, f"talk {LLM_CONTACT} hello"))
        self.assertIn("Fixture reply.", result.text)
        self.assertEqual(engine.events[-1].source, "concordia")
        self.assertEqual(engine.events[-1].action_type, "communicate")

    def test_llm_player_submits_same_action_object(self) -> None:
        controller = ConcordiaTextController(FakeModel(["go west"]))
        engine = GameEngine(fixture_world(), controllers={LLM_PLAYER: controller})
        results = engine.run_background_once()
        self.assertEqual(len(results), 1)
        self.assertEqual(engine.world.actors[LLM_PLAYER].room_id, FIXTURE_PREFIX + "hub")
        self.assertEqual(engine.events[-1].source, "concordia")

    def test_free_text_intent_translation_returns_structured_action(self) -> None:
        controller = ConcordiaTextController(FakeModel(["go north"]))
        engine = GameEngine(fixture_world())
        action = controller.interpret_intent(
            actor_id=HUMAN,
            intent="head toward the objective room",
            context=engine.context_for(HUMAN),
        )
        self.assertEqual(action.verb, "go")
        result = engine.execute(action)
        self.assertIn("Fixture Goal Room", result.text)

    def test_llm_gm_narrates_without_mutating_state(self) -> None:
        controller = ConcordiaTextController(FakeModel(["A brief fixture narration."]))
        engine = GameEngine(fixture_world(), gm_controller=controller)
        before = engine.world.to_dict()
        result = engine.execute(parse_command(HUMAN, "look"))
        narration = engine.gm_narration(result)
        self.assertEqual(narration, "A brief fixture narration.")
        self.assertEqual(before, engine.world.to_dict())

    def test_save_load_preserves_world_turn_and_events(self) -> None:
        engine = GameEngine(fixture_world())
        engine.execute(parse_command(HUMAN, "east"))
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "save.json"
            save_game(engine, path)
            restored = load_game(path)
        self.assertEqual(restored.turn, engine.turn)
        self.assertEqual(restored.world.to_dict(), engine.world.to_dict())
        self.assertEqual(
            [event.to_dict() for event in restored.events],
            [event.to_dict() for event in engine.events],
        )

    def test_sqlite_event_log_receives_same_events(self) -> None:
        connection = connect(":memory:")
        engine = GameEngine(fixture_world(), connection=connection)
        engine.execute(parse_command(HUMAN, "look"))
        stored = list_events(connection, engine.simulation_id)
        self.assertEqual(len(stored), len(engine.events))
        self.assertEqual(stored[0].event_id, engine.events[0].event_id)

    def test_fixture_world_is_explicitly_noncanonical(self) -> None:
        world = fixture_world()
        for identifier in [*world.rooms, *world.items, *world.actors, world.adventure.adventure_id]:
            self.assertTrue(identifier.startswith(FIXTURE_PREFIX))

    def test_prototype_does_not_require_graphics_or_web_frameworks(self) -> None:
        import text_game.engine as module
        source = Path(module.__file__).read_text(encoding="utf-8").lower()
        for forbidden in ("streamlit", "fastapi", "websocket", "godot", "pygame"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
