"""Runtime contracts for the tabletop primitives (issue #347).

These tests assert **executable behaviour only**: dice arithmetic and determinism, card shape,
deck mechanics and reproducibility, board invariants, tarot placeholder discipline, the world-state
projection and snapshot serialization. Per ``AGENTS.md`` ("Automated tests policy: executable code
only") there is deliberately **no** assertion about rules, canon, lore, wording or design prose — the
primitives carry no rules to test, only contracts.

Run from the repository root:

    python -m unittest discover -s strategy_game/tests -p "test_*.py"
"""
from __future__ import annotations

import json
import random
import sys
import tempfile
import unittest
from dataclasses import fields
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from strategy_game import WorldState  # noqa: E402
from strategy_game.core import Faction, Leader, Location, NetworkEdge  # noqa: E402
from strategy_game.provenance import ProvenanceKind  # noqa: E402
from strategy_game.tabletop import (  # noqa: E402
    BOARD_LAYERS,
    TABLE_SCHEMA_VERSION,
    TAROT_USES,
    Board,
    BoardEdge,
    BoardError,
    BoardNode,
    BoardPiece,
    Card,
    CardError,
    CardRole,
    CardType,
    Deck,
    DeckError,
    DiceNotationError,
    DicePool,
    DuplicatePolicy,
    EdgeKind,
    Layout,
    RollLog,
    RollResult,
    TableState,
    TarotCard,
    TarotDraw,
    TarotUse,
    Zone,
    board_from_world,
    draw_tarot,
    load_table,
    parse_notation,
    roll,
    save_table,
    tarot_deck,
)


# --------------------------------------------------------------------------------------------------
# dice
# --------------------------------------------------------------------------------------------------
class DiceNotationTests(unittest.TestCase):
    def test_common_pools_parse(self):
        self.assertEqual(parse_notation("d6"), DicePool(1, 6, 0))
        self.assertEqual(parse_notation("2d6"), DicePool(2, 6, 0))
        self.assertEqual(parse_notation("3d8+1"), DicePool(3, 8, 1))
        self.assertEqual(parse_notation("1d20-2"), DicePool(1, 20, -2))

    def test_notation_is_case_and_space_tolerant(self):
        self.assertEqual(parse_notation(" 2D6 + 1 "), DicePool(2, 6, 1))

    def test_unapproved_resolution_syntax_is_refused(self):
        """A keep/reroll/explode string must not be silently read as a plain pool."""
        for text in ("4d6kh3", "2d6!", "3d6r1", "2d6*2", "d", "abc", "6", "d6 d6"):
            with self.subTest(text=text):
                with self.assertRaises(DiceNotationError):
                    parse_notation(text)

    def test_pool_bounds_are_arithmetic(self):
        pool = parse_notation("3d8+1")
        self.assertEqual(pool.min_total, 4)
        self.assertEqual(pool.max_total, 25)

    def test_notation_round_trips(self):
        for text in ("d6", "2d6", "3d8+1", "1d20-2"):
            with self.subTest(text=text):
                self.assertEqual(parse_notation(parse_notation(text).notation), parse_notation(text))

    def test_negative_modifier_keeps_its_sign_in_notation(self):
        self.assertEqual(parse_notation("2d6-1").notation, "2d6-1")

    def test_a_pool_needs_one_die_and_two_sides(self):
        with self.assertRaises(DiceNotationError):
            DicePool(count=0, sides=6)
        with self.assertRaises(DiceNotationError):
            DicePool(count=1, sides=1)


class DiceRollTests(unittest.TestCase):
    def test_a_seed_reproduces_a_roll_exactly(self):
        pool = parse_notation("4d6+2")
        first = roll(pool, seed=1234)
        second = roll(pool, seed=1234)
        self.assertEqual(first.dice, second.dice)
        self.assertEqual(first.total, second.total)

    def test_faces_stay_within_the_die(self):
        for seed in range(25):
            result = roll(parse_notation("6d10"), seed=seed)
            self.assertTrue(all(1 <= face <= 10 for face in result.dice))

    def test_total_is_the_sum_plus_the_modifier(self):
        result = roll(parse_notation("5d6+3"), seed=7)
        self.assertEqual(result.total, sum(result.dice) + 3)

    def test_breakdown_shows_every_face_and_the_total(self):
        result = roll(parse_notation("3d6+1"), seed=5)
        for face in result.dice:
            self.assertIn(str(face), result.breakdown)
        self.assertIn(str(result.total), result.breakdown)

    def test_an_injected_rng_is_used_and_shared(self):
        rng = random.Random(99)
        expected = [rng.randint(1, 6) for _ in range(4)]
        rng = random.Random(99)
        result = roll(parse_notation("d6"), rng=rng)
        self.assertEqual(result.dice, (expected[0],))

    def test_an_unseeded_roll_is_still_fully_recorded(self):
        """Live play needs unpredictability; auditability must survive it."""
        result = roll(parse_notation("2d6"))
        self.assertEqual(len(result.dice), 2)
        self.assertEqual(result.total, sum(result.dice))

    def test_a_result_rejects_the_wrong_number_of_faces(self):
        with self.assertRaises(DiceNotationError):
            RollResult(pool=parse_notation("2d6"), dice=(3,))

    def test_a_result_rejects_a_face_outside_the_die(self):
        with self.assertRaises(DiceNotationError):
            RollResult(pool=parse_notation("1d6"), dice=(7,))


class RollLogTests(unittest.TestCase):
    def test_the_log_replays_from_its_own_record(self):
        log = RollLog()
        for seed in (1, 2, 3):
            log.record(roll(parse_notation("2d6+1"), seed=seed))
        replayed = log.replay()
        self.assertEqual(len(replayed), 3)
        self.assertEqual([item.total for item in replayed], list(log.totals))
        self.assertEqual([item.dice for item in replayed], [item.dice for item in log.entries])

    def test_replay_does_not_depend_on_the_random_implementation(self):
        """A recorded roll is reproduced from its stored faces, so the RNG is not consulted."""
        log = RollLog()
        log.record(RollResult(pool=parse_notation("3d6"), dice=(6, 6, 6), seed=None))
        self.assertEqual(log.replay()[0].total, 18)

    def test_record_returns_the_result(self):
        log = RollLog()
        recorded = log.record(roll(parse_notation("d6"), seed=1))
        self.assertEqual(len(log), 1)
        self.assertIs(log.entries[0], recorded)

    def test_log_round_trips(self):
        log = RollLog()
        log.record(roll(parse_notation("2d6-1"), seed=42, label="check"))
        restored = RollLog.from_dict(json.loads(json.dumps(log.to_dict())))
        self.assertEqual(restored.to_dict(), log.to_dict())


# --------------------------------------------------------------------------------------------------
# cards
# --------------------------------------------------------------------------------------------------
class CardTests(unittest.TestCase):
    def test_a_card_needs_an_identifier_and_a_title(self):
        with self.assertRaises(CardError):
            Card(identifier="", card_type=CardType.EVENT, title="x")
        with self.assertRaises(CardError):
            Card(identifier="c1", card_type=CardType.EVENT, title="  ")

    def test_card_type_must_be_a_declared_type(self):
        with self.assertRaises(CardError):
            Card(identifier="c1", card_type="event", title="x")  # type: ignore[arg-type]

    def test_structured_fields_need_a_kind(self):
        with self.assertRaises(CardError):
            Card(identifier="c1", card_type=CardType.EVENT, title="x",
                 effects=({"note": "no kind"},))

    def test_structured_fields_must_be_mappings(self):
        with self.assertRaises(CardError):
            Card(identifier="c1", card_type=CardType.EVENT, title="x",
                 prerequisites=("not a mapping",))

    def test_structured_fields_must_be_json_serializable(self):
        with self.assertRaises(CardError):
            Card(identifier="c1", card_type=CardType.EVENT, title="x",
                 effects=({"kind": "unspecified", "payload": object()}))

    def test_structured_fields_are_carried_verbatim(self):
        effects = ({"kind": "unspecified", "note": "a later approved rule reads this"},)
        card = Card(identifier="c1", card_type=CardType.MISSION, title="x", effects=effects)
        self.assertEqual(card.effects, effects)

    def test_role_distinguishes_a_record_from_a_move(self):
        record = Card("c1", CardType.ORGANIZATION, "An organization")
        move = Card("c2", CardType.EVENT, "An event", role=CardRole.PLAYABLE_MOVE)
        self.assertFalse(record.is_playable_move)
        self.assertTrue(move.is_playable_move)

    def test_an_unrecorded_origin_stays_unknown(self):
        self.assertIs(Card("c1", CardType.EVENT, "x").provenance.kind, ProvenanceKind.UNKNOWN)

    def test_card_round_trips(self):
        card = Card(
            identifier="c9",
            card_type=CardType.IDEOLOGY,
            title="A signifier card",
            role=CardRole.PLAYABLE_MOVE,
            text="content",
            art_ref="art/c9.svg",
            tags=("a", "b"),
            owner_id="f1",
            prerequisites=({"kind": "unspecified"},),
            effects=({"kind": "unspecified"},),
        )
        self.assertEqual(Card.from_dict(json.loads(json.dumps(card.to_dict()))), card)


# --------------------------------------------------------------------------------------------------
# decks
# --------------------------------------------------------------------------------------------------
def _card(card_id: str, card_type: CardType = CardType.EVENT) -> Card:
    return Card(identifier=card_id, card_type=card_type, title=f"Card {card_id}")


class DeckTests(unittest.TestCase):
    def test_a_duplicate_identifier_is_dropped_by_default(self):
        deck = Deck.from_cards("d1", [_card("a"), _card("a"), _card("b")])
        self.assertEqual(deck.card_ids_in(Zone.DECK), ("a", "b"))

    def test_refuse_policy_rejects_a_duplicate(self):
        with self.assertRaises(DeckError):
            Deck.from_cards("d1", [_card("a"), _card("a")], duplicate_policy=DuplicatePolicy.REFUSE)

    def test_allow_policy_keeps_two_copies_of_one_record(self):
        """A normal card game holds several copies of one card: one record, two physical cards."""
        deck = Deck.from_cards("d1", [_card("a"), _card("a")], duplicate_policy=DuplicatePolicy.ALLOW)
        self.assertEqual(deck.card_ids_in(Zone.DECK), ("a", "a"))
        self.assertEqual(len(deck.cards), 1)

    def test_a_seed_reproduces_a_shuffle(self):
        def order(seed: int) -> tuple[str, ...]:
            deck = Deck.from_cards("d1", [_card(str(i)) for i in range(10)])
            return deck.shuffle(seed=seed)

        self.assertEqual(order(3), order(3))
        self.assertEqual(sorted(order(3)), sorted(order(4)))

    def test_drawing_moves_a_card_and_logs_it(self):
        deck = Deck.from_cards("d1", [_card("a"), _card("b")])
        drawn = deck.draw(1, seed=1)
        self.assertEqual(len(drawn), 1)
        self.assertEqual(deck.zone_of(drawn[0].identifier), Zone.HAND)
        entry = deck.history[-1]
        self.assertEqual(entry.card_id, drawn[0].identifier)
        self.assertEqual(entry.from_zone, Zone.DECK.value)
        self.assertEqual(entry.to_zone, Zone.HAND.value)
        self.assertEqual(entry.remaining_in_source, 1)

    def test_a_seeded_draw_is_reproducible(self):
        def draw_ids(seed: int) -> tuple[str, ...]:
            deck = Deck.from_cards("d1", [_card(str(i)) for i in range(8)])
            deck.shuffle(seed=11)
            return tuple(card.identifier for card in deck.draw(3, seed=seed))

        self.assertEqual(draw_ids(5), draw_ids(5))

    def test_drawing_more_than_remains_raises(self):
        deck = Deck.from_cards("d1", [_card("a")])
        with self.assertRaises(DeckError):
            deck.draw(2, seed=1)

    def test_drawing_a_non_positive_count_raises(self):
        deck = Deck.from_cards("d1", [_card("a")])
        with self.assertRaises(DeckError):
            deck.draw(0, seed=1)

    def test_place_is_not_a_random_draw(self):
        """A persistent board entity is placed, not dealt: no log entry, no RNG use."""
        deck = Deck.from_cards("d1", [_card("city"), _card("org")])
        deck.place("city", Zone.HAND)
        self.assertEqual(deck.zone_of("city"), Zone.HAND)
        self.assertEqual(deck.history, [])

    def test_discard_and_recycle_move_cards_back(self):
        deck = Deck.from_cards("d1", [_card("a"), _card("b")])
        deck.shuffle(seed=1)
        drawn = deck.draw(2, seed=2)
        for card in drawn:
            deck.discard(card.identifier)
        self.assertEqual(len(deck.card_ids_in(Zone.DISCARD)), 2)
        deck.recycle()
        self.assertEqual(deck.card_ids_in(Zone.DISCARD), ())
        self.assertEqual(len(deck.card_ids_in(Zone.DECK)), 2)

    def test_an_unknown_card_is_refused(self):
        deck = Deck.from_cards("d1", [_card("a")])
        with self.assertRaises(DeckError):
            deck.discard("nope")
        with self.assertRaises(DeckError):
            deck.zone_of("nope")

    def test_a_deck_needs_an_identifier(self):
        with self.assertRaises(DeckError):
            Deck(identifier=" ")

    def test_deck_round_trips_with_zones_and_history(self):
        deck = Deck.from_cards("d1", [_card("a"), _card("b"), _card("c")])
        deck.shuffle(seed=4)
        deck.draw(2, seed=5)
        restored = Deck.from_dict(json.loads(json.dumps(deck.to_dict())))
        self.assertEqual(restored.to_dict(), deck.to_dict())
        self.assertEqual(restored.card_ids_in(Zone.HAND), deck.card_ids_in(Zone.HAND))


# --------------------------------------------------------------------------------------------------
# board
# --------------------------------------------------------------------------------------------------
class BoardTests(unittest.TestCase):
    def test_the_reserved_layer_names_are_the_four_overlay_suggestions(self):
        self.assertEqual(BOARD_LAYERS, ("physical", "cyber", "astral", "social"))

    def test_a_node_needs_an_identifier(self):
        with self.assertRaises(BoardError):
            BoardNode(identifier="", label="x")

    def test_duplicate_node_identifiers_are_refused(self):
        board = Board()
        board.add_node(BoardNode("n1", "one"))
        with self.assertRaises(BoardError):
            board.add_node(BoardNode("n1", "again"))

    def test_an_edge_to_a_missing_node_is_refused(self):
        board = Board()
        board.add_node(BoardNode("n1", "one"))
        with self.assertRaises(BoardError):
            board.add_edge(BoardEdge("e1", "n1", "n2"))

    def test_a_self_link_is_refused(self):
        with self.assertRaises(BoardError):
            BoardEdge("e1", "n1", "n1")

    def test_a_piece_on_a_missing_node_is_refused(self):
        board = Board()
        board.add_node(BoardNode("n1", "one"))
        with self.assertRaises(BoardError):
            board.add_piece(BoardPiece("p1", "n2"))

    def test_neighbours_are_found_in_both_directions(self):
        board = Board.from_records(
            [BoardNode("a", "A"), BoardNode("b", "B"), BoardNode("c", "C")],
            [BoardEdge("e1", "a", "b"), BoardEdge("e2", "c", "a")],
        )
        self.assertEqual(board.neighbors("a"), ("b", "c"))

    def test_neighbours_can_be_filtered_by_layer_and_kind(self):
        board = Board.from_records(
            [BoardNode("a", "A"), BoardNode("b", "B"), BoardNode("c", "C")],
            [
                BoardEdge("e1", "a", "b", EdgeKind.ALLIANCE, "social"),
                BoardEdge("e2", "a", "c", EdgeKind.TRAVEL, "physical"),
            ],
        )
        self.assertEqual(board.neighbors("a", layer="social"), ("b",))
        self.assertEqual(board.neighbors("a", kind=EdgeKind.TRAVEL), ("c",))
        self.assertEqual(board.neighbors("a", kind=EdgeKind.TRAVEL, layer="social"), ())

    def test_neighbours_of_an_unknown_node_raise(self):
        with self.assertRaises(BoardError):
            Board().neighbors("nope")

    def test_nodes_can_be_listed_by_layer(self):
        board = Board.from_records(
            [
                BoardNode("a", "A", layer="physical"),
                BoardNode("b", "B", layer="astral"),
                BoardNode("c", "C", layer="physical"),
            ]
        )
        self.assertEqual([node.identifier for node in board.nodes_in_layer("physical")], ["a", "c"])

    def test_pieces_can_be_listed_per_node(self):
        board = Board.from_records(
            [BoardNode("a", "A"), BoardNode("b", "B")],
            pieces=[BoardPiece("p1", "a"), BoardPiece("p2", "a"), BoardPiece("p3", "b")],
        )
        self.assertEqual([piece.identifier for piece in board.pieces_on("a")], ["p1", "p2"])

    def test_moving_a_piece_to_an_unknown_node_raises(self):
        board = Board.from_records([BoardNode("a", "A")], pieces=[BoardPiece("p1", "a")])
        with self.assertRaises(BoardError):
            board.move_piece("p1", "nope")
        board.move_piece("p1", "a")
        self.assertEqual(board.pieces["p1"].node_id, "a")

    def test_validate_repairs_nothing_and_catches_a_dangling_edge(self):
        """`from_dict` is the path that can produce a dangling edge, so `validate` is its guard."""
        payload = {
            "identifier": "b",
            "nodes": {"a": BoardNode("a", "A").to_dict()},
            "edges": {"e1": BoardEdge("e1", "a", "gone").to_dict()},
            "pieces": {},
        }
        board = Board.from_dict(payload)
        with self.assertRaises(BoardError):
            board.validate()

    def test_validate_catches_a_piece_off_the_board(self):
        payload = {
            "identifier": "b",
            "nodes": {"a": BoardNode("a", "A").to_dict()},
            "edges": {},
            "pieces": {"p1": BoardPiece("p1", "gone").to_dict()},
        }
        with self.assertRaises(BoardError):
            Board.from_dict(payload).validate()

    def test_board_round_trips(self):
        board = Board.from_records(
            [BoardNode("a", "A", "location", "physical", ("tag",)), BoardNode("b", "B")],
            [BoardEdge("e1", "a", "b", EdgeKind.OPPOSITION, "social", "notes")],
            [BoardPiece("p1", "b", "agent", "f1")],
        )
        self.assertEqual(Board.from_dict(json.loads(json.dumps(board.to_dict()))).to_dict(),
                         board.to_dict())
        Board.from_dict(board.to_dict()).validate()

    def test_the_board_carries_no_coordinates(self):
        """Topology is separate from cosmetic positions, so layout cannot corrupt the graph."""
        board = Board.from_records([BoardNode("a", "A")])
        self.assertNotIn("positions", board.to_dict())
        self.assertNotIn("x", board.nodes["a"].to_dict())

    def test_layout_holds_positions_beside_the_board(self):
        layout = Layout()
        layout.set("a", 1.5, -2.0)
        self.assertEqual(layout.get("a"), (1.5, -2.0))
        self.assertEqual(Layout.from_dict(json.loads(json.dumps(layout.to_dict()))).get("a"),
                         (1.5, -2.0))
        self.assertIsNone(layout.get("missing"))


# --------------------------------------------------------------------------------------------------
# tarot
# --------------------------------------------------------------------------------------------------
class TarotTests(unittest.TestCase):
    def test_the_five_interpreter_uses_are_declared(self):
        self.assertEqual(len(TAROT_USES), 5)
        self.assertEqual(set(TAROT_USES), {use.value for use in TarotUse})

    def test_a_tarot_card_needs_identity(self):
        with self.assertRaises(CardError):
            TarotCard(identifier="", display_name="x")
        with self.assertRaises(CardError):
            TarotCard(identifier="t1", display_name=" ")

    def test_a_tarot_card_carries_no_meaning_or_modifier(self):
        card = TarotCard("t1", "Illustrative arcana", symbols=("sun",))
        card.assert_placeholder()
        self.assertEqual(card.to_card().card_type, CardType.TAROT)

    def test_a_tarot_card_that_gains_a_mechanical_field_is_caught(self):
        """The placeholder check exists so an unapproved meaning cannot arrive unnoticed."""
        card = TarotCard("t1", "Illustrative arcana")
        card.modifier = 3  # type: ignore[attr-defined]
        with self.assertRaises(CardError):
            card.assert_placeholder()

    def test_one_deck_serves_several_interpreters(self):
        deck = tarot_deck("t", [TarotCard("t1", "One"), TarotCard("t2", "Two")])
        deck.shuffle(seed=1)
        narrative = draw_tarot(deck, TarotUse.NARRATIVE_OMEN, seed=2, scene_id="s1",
                               drawn_by="player", interpretation="an omen of delay")
        tactical = draw_tarot(deck, TarotUse.FACTION_SYMBOLISM, seed=3, scene_id="s2",
                              drawn_by="gm", alternatives=("or a warning",))
        self.assertNotEqual(narrative.card_id, tactical.card_id)
        self.assertIs(narrative.use, TarotUse.NARRATIVE_OMEN)
        self.assertIs(tactical.use, TarotUse.FACTION_SYMBOLISM)
        self.assertEqual(len(deck.history), 2)

    def test_a_draw_is_attributable(self):
        deck = tarot_deck("t", [TarotCard("t1", "One")])
        draw = draw_tarot(deck, TarotUse.PSI_INVESTIGATION, seed=9, scene_id="scene-7",
                          actor_id="actor-2", drawn_by="gm", context="what did the vision mean?",
                          alternatives=("a genuine signal", "noise"))
        self.assertEqual(draw.scene_id, "scene-7")
        self.assertEqual(draw.actor_id, "actor-2")
        self.assertEqual(draw.seed, 9)
        self.assertEqual(draw.alternatives, ("a genuine signal", "noise"))

    def test_drawing_tarot_from_a_non_tarot_deck_is_refused(self):
        deck = Deck.from_cards("events", [_card("e1", CardType.EVENT)])
        with self.assertRaises(CardError):
            draw_tarot(deck, TarotUse.GM_PROMPT, seed=1)

    def test_a_tarot_draw_round_trips(self):
        draw = TarotDraw(card_id="t1", use=TarotUse.CHARACTER_INTERPRETATION, seed=4,
                         alternatives=("a", "b"))
        self.assertEqual(TarotDraw.from_dict(json.loads(json.dumps(draw.to_dict()))), draw)

    def test_a_draw_needs_a_card(self):
        with self.assertRaises(CardError):
            TarotDraw(card_id="", use=TarotUse.GM_PROMPT)


# --------------------------------------------------------------------------------------------------
# the projection from WorldState
# --------------------------------------------------------------------------------------------------
class BridgeTests(unittest.TestCase):
    def _world(self) -> WorldState:
        return WorldState(
            leaders=[Leader("l1", "A leader")],
            factions=[Faction("f1", "A faction")],
            locations=[Location("loc1", "A place", 60.17, 24.94)],
            edges=[NetworkEdge("f1", "loc1", "communication")],
        )

    def test_the_projection_builds_layered_nodes(self):
        board = board_from_world(self._world())
        self.assertEqual(board.nodes["loc1"].layer, "physical")
        self.assertEqual(board.nodes["loc1"].kind, "location")
        self.assertEqual(board.nodes["f1"].layer, "social")
        self.assertEqual(board.nodes["f1"].kind, "faction")

    def test_the_source_layer_label_is_preserved_on_the_edge(self):
        board = board_from_world(self._world())
        edge = next(iter(board.edges.values()))
        self.assertEqual(edge.layer, "communication")
        self.assertEqual(edge.endpoints, ("f1", "loc1"))

    def test_an_edge_whose_endpoints_are_not_projected_is_skipped_not_invented(self):
        world = WorldState(
            factions=[Faction("f1", "A faction")],
            edges=[NetworkEdge("f1", "l1", "communication")],
        )
        self.assertEqual(board_from_world(world).edges, {})

    def test_the_projection_does_not_mutate_the_world_state(self):
        world = self._world()
        before = world.to_json()
        board_from_world(world)
        self.assertEqual(world.to_json(), before)

    def test_the_world_state_gains_no_board_field(self):
        """Joining the table to the shared container is the Gate D decision, so it must not drift in."""
        self.assertNotIn("board", {item.name for item in fields(WorldState)})
        self.assertNotIn("decks", {item.name for item in fields(WorldState)})

    def test_the_projection_is_a_valid_board(self):
        board_from_world(self._world()).validate()


# --------------------------------------------------------------------------------------------------
# snapshot
# --------------------------------------------------------------------------------------------------
class TableStateTests(unittest.TestCase):
    def _state(self) -> TableState:
        board = Board.from_records([BoardNode("a", "A")], [])
        deck = Deck.from_cards("d1", [_card("c1")])
        deck.shuffle(seed=1)
        state = TableState(board=board, decks={"d1": deck})
        state.rolls.record(roll(parse_notation("2d6"), seed=3, label="a check"))
        return state

    def test_the_payload_carries_exactly_the_declared_fields(self):
        state = TableState()
        self.assertEqual(set(state.to_dict()), {item.name for item in fields(TableState)})

    def test_an_empty_state_round_trips(self):
        self.assertEqual(TableState.from_json(TableState().to_json()), TableState())

    def test_a_populated_state_round_trips(self):
        state = self._state()
        self.assertEqual(TableState.from_json(state.to_json()).to_json(), state.to_json())

    def test_the_snapshot_is_byte_stable(self):
        state = self._state()
        self.assertEqual(state.to_json(), TableState.from_json(state.to_json()).to_json())
        self.assertEqual(list(json.loads(state.to_json())), sorted(json.loads(state.to_json())))

    def test_non_ascii_is_preserved(self):
        state = TableState(board=Board.from_records([BoardNode("a", "Helsingin Noösfääri")]))
        self.assertIn("Noösfääri", state.to_json())
        self.assertNotIn("\\u00f6", state.to_json())

    def test_the_schema_version_is_written(self):
        self.assertEqual(TableState().schema_version, TABLE_SCHEMA_VERSION)
        self.assertEqual(json.loads(TableState().to_json())["schema_version"], TABLE_SCHEMA_VERSION)

    def test_a_snapshot_missing_a_section_still_loads(self):
        minimal = json.dumps({"schema_version": TABLE_SCHEMA_VERSION})
        restored = TableState.from_json(minimal)
        self.assertEqual(restored.decks, {})
        self.assertEqual(len(restored.rolls), 0)

    def test_save_and_load_round_trip_on_disk(self):
        state = self._state()
        with tempfile.TemporaryDirectory() as folder:
            path = save_table(state, Path(folder) / "nested" / "table.json")
            self.assertTrue(path.exists())
            self.assertEqual(load_table(path).to_json(), state.to_json())

    def test_a_missing_snapshot_raises_rather_than_returning_an_empty_table(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError):
                load_table(Path(folder) / "absent.json")


# --------------------------------------------------------------------------------------------------
# packaging
# --------------------------------------------------------------------------------------------------
class TabletopPackagingTests(unittest.TestCase):
    def test_importing_the_primitives_needs_no_optional_adapter(self):
        """The table must load and be viewed with no Mesa, NetworkX, Ollama or Concordia present."""
        import importlib

        module = importlib.import_module("strategy_game.tabletop")
        self.assertTrue(hasattr(module, "TableState"))
        for name in ("mesa", "networkx", "ollama", "concordia"):
            self.assertFalse(
                name in sys.modules and getattr(sys.modules[name], "__file__", None) is None,
                f"{name} must not be required by the tabletop package",
            )

    def test_the_main_package_api_is_not_widened(self):
        """Issue #282 pins strategy_game.__all__ and a CI smoke step pins its view keys."""
        import strategy_game

        self.assertNotIn("TableState", strategy_game.__all__)
        self.assertNotIn("Board", strategy_game.__all__)


if __name__ == "__main__":
    unittest.main()
