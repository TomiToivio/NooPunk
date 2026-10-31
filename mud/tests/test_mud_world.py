"""The world, the two accounts and the survival loop (#946, milestones 2-4).

Evennia's own fixtures give two accounts and two puppeted characters, which is the
cheapest honest way to assert "two concurrent players" without a network: the state they
share is the database, and the database is what a restart reloads.
"""
from __future__ import annotations

from evennia.utils import create
from evennia.utils.test_resources import EvenniaCommandTest

from commands.noopunk import CmdFaction, CmdScavenge, CmdSheet
from world import helsinki
from world.factions import unsa


class WorldBuildTests(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.rooms = helsinki.build()

    def test_the_neighbourhood_is_the_authored_map(self) -> None:
        self.assertEqual(len(self.rooms), len(helsinki.ROOMS))
        self.assertIn(helsinki.START, self.rooms)
        self.assertEqual(self.rooms[helsinki.START].db.powered, False)

    def test_building_twice_does_not_double_the_world(self) -> None:
        """A restart runs the builder again. Nothing may be created twice."""
        from evennia.objects.models import ObjectDB

        before = ObjectDB.objects.count()
        helsinki.build()
        self.assertEqual(ObjectDB.objects.count(), before)

    def test_every_exit_lands_in_a_real_room(self) -> None:
        for spec in helsinki.ROOMS:
            room = self.rooms[spec["key"]]
            self.assertEqual(len(room.exits), len(spec["exits"]), spec["key"])
            for exit_obj in room.exits:
                self.assertIsNotNone(exit_obj.destination, exit_obj.key)

    def test_the_map_is_walkable_from_the_start_to_the_safehouse(self) -> None:
        """A graph walk over the authored data, so a broken exit is found without a session."""
        seen, frontier = {helsinki.START}, [helsinki.START]
        while frontier:
            key = frontier.pop()
            spec = next(s for s in helsinki.ROOMS if s["key"] == key)
            for target in spec["exits"].values():
                if target not in seen:
                    seen.add(target)
                    frontier.append(target)
        self.assertIn("UNSA safehouse", seen)
        self.assertEqual(len(seen), len(helsinki.ROOMS), "a room is unreachable from the start")


class SheetCommandTests(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.char1.db.cwn = None
        self.char1.at_object_creation()

    def test_the_sheet_command_reports_six_attributes(self) -> None:
        text = self.call(CmdSheet(), "", caller=self.char1)
        for attribute in ("Strength", "Dexterity", "Constitution",
                          "Intelligence", "Wisdom", "Charisma"):
            self.assertIn(attribute, text)


class ScavengeTests(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.char1.db.cwn = None
        self.char1.at_object_creation()
        self.char1.location = helsinki.build()[helsinki.START]
        self.char1.db.supplies = 0
        self.char1.location.db.scarcity = 0

    def test_exactly_one_consequence_lands_per_attempt(self) -> None:
        """Whatever the dice do, the loop is one check, one consequence — never two."""
        for _ in range(6):
            before = self.char1.db.supplies
            scarcity = self.char1.location.db.scarcity
            self.call(CmdScavenge(), "", caller=self.char1)
            gained = self.char1.db.supplies - before
            worsened = self.char1.location.db.scarcity - scarcity
            self.assertEqual(gained + worsened, 1)
            self.assertIn(gained, (0, 1))

    def test_supplies_cannot_go_negative_and_only_the_check_grants_them(self) -> None:
        self.char1.db.supplies = 0
        self.call(CmdScavenge(), "nonsense", caller=self.char1)
        self.assertEqual(self.char1.db.supplies, 0)


class FactionTests(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        self.char1.db.cwn = None
        self.char1.at_object_creation()

    def test_unsa_is_the_starting_faction_and_is_inspectable(self) -> None:
        text = self.call(CmdFaction(), "", caller=self.char1)
        self.assertIn("UNSA", text)
        self.assertIn("food", text)

    def test_joining_twice_adds_one_member(self) -> None:
        self.call(CmdFaction(), "join Dana", caller=self.char1)
        self.call(CmdFaction(), "join Dana", caller=self.char1)
        self.assertEqual(self.char1.faction.members.count("Dana"), 1)

    def test_handing_over_stock_moves_it_and_never_creates_it(self) -> None:
        self.char1.db.supplies = 1
        faction = unsa()
        before = faction.stocks["food"]
        self.char1.save_faction(faction)
        self.call(CmdFaction(), "give food 5", caller=self.char1)
        self.assertEqual(self.char1.faction.stocks["food"], before)
        self.call(CmdFaction(), "give food", caller=self.char1)
        self.assertEqual(self.char1.faction.stocks["food"], before + 1)
        self.assertEqual(self.char1.db.supplies, 0)


class MultiplayerTests(EvenniaCommandTest):
    def setUp(self):
        super().setUp()
        room = helsinki.build()[helsinki.START]
        for character in (self.char1, self.char2):
            character.db.cwn = None
            character.at_object_creation()
            character.location = room

    def test_two_accounts_share_one_room_and_one_world(self) -> None:
        self.assertEqual(self.char1.location, self.char2.location)
        self.assertNotEqual(self.char1.account, self.char2.account)
        self.char1.execute_cmd("say the lift is out")
        self.assertEqual(self.char1.location, self.char2.location)

    def test_state_written_by_one_is_read_by_the_other(self) -> None:
        self.char1.location.db.scarcity = 3
        self.assertEqual(self.char2.location.db.scarcity, 3)

    def test_faction_state_is_per_character_data_not_global_mutable(self) -> None:
        self.char1.faction.join("Dana")
        faction = self.char1.faction
        self.char1.save_faction(faction)
        self.assertNotIn("Dana", self.char2.faction.members)
