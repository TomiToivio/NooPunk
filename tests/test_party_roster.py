"""Party roster rules (#806): one persistent PC, 1-4 members, companions join and leave.

These pin the constraints the design states, not a UI: solo play must be legal, four is a bound rather
than a target, and the player character cannot be swapped out when a companion arrives.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules.party import MAX_PARTY_SIZE, MIN_PARTY_SIZE, Party, PartyError, PartyMember  # noqa: E402


def pc(level: int = 1) -> PartyMember:
    return PartyMember(member_id="pc", name="Field Agent", level=level, is_player_character=True, role="field agent")


def companion(member_id: str, level: int = 5, controllable: bool = True) -> PartyMember:
    return PartyMember(member_id=member_id, name=member_id.title(), level=level, role="mentor", controllable=controllable)


class CompositionTest(unittest.TestCase):
    def test_solo_play_is_legal(self):
        party = Party()
        party.add_player_character(pc())
        party.validate()
        self.assertEqual(party.size, 1)

    def test_party_of_four_is_legal(self):
        party = Party()
        party.add_player_character(pc())
        for name in ("romppainen", "ally", "specialist"):
            party.add_companion(companion(name))
        party.validate()
        self.assertEqual(party.size, 4)

    def test_a_fifth_member_is_refused_not_silently_dropped(self):
        party = Party()
        party.add_player_character(pc())
        for name in ("a", "b", "c"):
            party.add_companion(companion(name))
        with self.assertRaises(PartyError):
            party.add_companion(companion("d"))
        self.assertEqual(party.size, MAX_PARTY_SIZE)

    def test_two_player_characters_are_refused(self):
        party = Party()
        party.add_player_character(pc())
        with self.assertRaises(PartyError):
            party.add_player_character(pc())

    def test_companion_cannot_be_added_through_the_pc_slot(self):
        party = Party()
        with self.assertRaises(PartyError):
            party.add_player_character(companion("romppainen"))

    def test_duplicate_companion_is_refused(self):
        party = Party()
        party.add_player_character(pc())
        party.add_companion(companion("romppainen"))
        with self.assertRaises(PartyError):
            party.add_companion(companion("romppainen"))


class PersistenceTest(unittest.TestCase):
    def test_the_player_character_cannot_leave(self):
        party = Party()
        party.add_player_character(pc())
        with self.assertRaises(PartyError):
            party.remove("pc")

    def test_companions_leave_and_the_pc_survives(self):
        party = Party()
        party.add_player_character(pc(level=3))
        party.add_companion(companion("romppainen", level=9))
        party.remove("romppainen")
        self.assertEqual(party.size, 1)
        self.assertEqual(party.player_character.level, 3)
        party.validate()

    def test_romppainen_is_an_experienced_companion_not_the_avatar(self):
        party = Party()
        party.add_player_character(pc())
        party.add_companion(companion("romppainen", level=9))
        self.assertFalse(party.get("romppainen").is_player_character)
        self.assertGreater(party.get("romppainen").level, party.player_character.level)

    def test_round_trip_through_save(self):
        party = Party()
        party.add_player_character(pc(level=2))
        party.add_companion(companion("romppainen", level=9, controllable=False))
        restored = Party.from_dict(party.to_dict())
        self.assertEqual(restored.size, 2)
        self.assertEqual(restored.player_character.level, 2)
        self.assertFalse(restored.get("romppainen").controllable)

    def test_unknown_save_version_is_refused(self):
        with self.assertRaises(PartyError):
            Party.from_dict({"version": 99, "members": []})

    def test_a_save_without_a_player_character_is_refused(self):
        payload = {"version": 1, "members": [{"member_id": "x", "name": "X", "level": 1}]}
        with self.assertRaises(PartyError):
            Party.from_dict(payload)


class ControlTest(unittest.TestCase):
    def test_a_present_but_uncontrollable_companion_is_not_selectable(self):
        party = Party()
        party.add_player_character(pc())
        party.add_companion(companion("romppainen", controllable=False))
        self.assertEqual([m.member_id for m in party.controllable()], ["pc"])

    def test_a_quest_companion_becomes_selectable_when_the_scenario_allows(self):
        party = Party()
        party.add_player_character(pc())
        party.add_companion(companion("romppainen", controllable=True))
        self.assertEqual({m.member_id for m in party.controllable()}, {"pc", "romppainen"})

    def test_bounds_are_the_published_ones(self):
        self.assertEqual((MIN_PARTY_SIZE, MAX_PARTY_SIZE), (1, 4))


if __name__ == "__main__":
    unittest.main()
