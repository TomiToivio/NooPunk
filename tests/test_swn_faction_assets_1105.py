"""The SWN faction asset catalogue, checked against the book's own tables (#1105, P0-B).

#1105 states the gap this file guards: "the turn module explicitly says SWN asset catalogues and combat
tables remain reference-only", and "existing turn code is **not proof of a finished asset catalogue**".
So the tests here do three things:

* **prove the catalogue is the book's**, by spot-checking printed rows (hit points, cost, tech level, type,
  attack line, counterattack line) that a transcription error would move;
* **prove the attack exchange follows the printed procedure** — 1d10 + rating each side, higher wins, a tie
  means *both* succeed, and the damage and counterattack dice are the ones the table prints;
* **prove the purchase rules are the book's** — catalogue price, one asset per turn, and the Base of Influence
  only through Expand Influence.

Values are cited by printed page; the book's prose and its A/S/P note legend are not reproduced.
"""

from __future__ import annotations

import json
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rules import swn_faction_assets as assets  # noqa: E402
from rules.swn_faction_turn import Faction, FactionTurnError  # noqa: E402

RATINGS = {"Cunning": 3, "Force": 2, "Wealth": 1}


class CatalogueTests(unittest.TestCase):
    def test_the_catalogue_has_the_books_assets(self) -> None:
        """24 Cunning + 22 Force + 22 Wealth, with the Base of Influence printed once."""
        self.assertEqual(assets.catalogue_size(), 68)
        for category, expected in (("Cunning", 24), ("Force", 22), ("Wealth", 22)):
            self.assertEqual(len(assets.by_category(category)), expected, category)

    def test_every_asset_is_printed_somewhere(self) -> None:
        for entry in assets.ASSETS.values():
            self.assertIn(entry["category"], assets.CATEGORIES)
            self.assertIn(entry["page"], (219, 221, 223), entry["name"])
            self.assertGreaterEqual(entry["level"], 1)
            self.assertLessEqual(entry["level"], 8)
            self.assertTrue(entry["type"].strip(), entry["name"])

    def test_printed_rows_match_the_book(self) -> None:
        """Spot checks across the three tables; each value is on the printed page named beside it."""
        smugglers = assets.asset("smugglers")                       # p.219, Cunning 1
        self.assertEqual((smugglers["hp"], smugglers["cost"], smugglers["tech_level"]),
                         (4, 2, 4))
        self.assertEqual(smugglers["type"], "Starship")
        self.assertEqual(smugglers["attack"], {"attribute": "Cunning", "defence": "Wealth",
                                               "damage": "1d4", "special": ""})

        party_machine = assets.asset("party_machine")               # p.219, Cunning 4
        self.assertEqual((party_machine["hp"], party_machine["cost"]), (10, 8))
        self.assertEqual(party_machine["counter"], "1d6")

        pretech_infantry = assets.asset("pretech_infantry")         # p.221, Force 6
        self.assertEqual((pretech_infantry["hp"], pretech_infantry["cost"]), (16, 20))
        self.assertEqual(pretech_infantry["attack"]["damage"], "2d8")
        self.assertEqual(pretech_infantry["counter"], "2d8+2")

        capital_fleet = assets.asset("capital_fleet")               # p.221, Force 8
        self.assertEqual((capital_fleet["hp"], capital_fleet["cost"]), (30, 40))
        self.assertEqual(capital_fleet["attack"]["damage"], "3d10+4")

        monopoly = assets.asset("monopoly")                          # p.223, Wealth 4
        self.assertEqual((monopoly["hp"], monopoly["cost"]), (12, 8))
        self.assertEqual(monopoly["attack"]["defence"], "Wealth")

    def test_the_table_of_influence_is_not_a_purchasable_asset(self) -> None:
        base = assets.asset("base_of_influence")
        self.assertIsNone(base["hp"])
        self.assertIsNone(base["cost"])
        stealth = assets.asset("stealth")
        self.assertIsNone(stealth["hp"], "p.219 prints '-': it cannot be attacked")

    def test_every_attack_line_is_parseable_or_declared_special(self) -> None:
        for entry in assets.ASSETS.values():
            attack = entry["attack"]
            if not attack["attribute"]:
                self.assertEqual(attack["special"], "none", entry["name"])
                continue
            self.assertIn(attack["attribute"], assets.CATEGORIES, entry["name"])
            self.assertIn(attack["defence"], assets.CATEGORIES, entry["name"])
            if attack["damage"]:
                assets.damage_roll(attack["damage"], rng=random.Random(1))   # raises if malformed
            else:
                self.assertEqual(attack["special"], "special", entry["name"])

    def test_note_letters_are_kept_but_not_interpreted(self) -> None:
        """The legend is in the book; keeping the letters lets a reader find it without us guessing."""
        notes = {code for entry in assets.ASSETS.values() for code in entry["notes"]}
        self.assertLessEqual(notes, {"A", "S", "P"})
        self.assertIn("A", notes)


class AttackExchangeTests(unittest.TestCase):
    def test_the_higher_total_wins_and_takes_the_printed_damage(self) -> None:
        result = assets.attack_exchange("smugglers", "false_front",
                                        attacker_ratings={"Cunning": 5, "Force": 0, "Wealth": 0},
                                        defender_ratings={"Cunning": 0, "Force": 0, "Wealth": 0},
                                        rng=random.Random(4))
        self.assertTrue(result["attacker_hits"])
        self.assertGreaterEqual(result["damage_to_defender"], 1)
        self.assertLessEqual(result["damage_to_defender"], 4, "1d4 damage")

    def test_a_tie_means_both_succeed(self) -> None:
        """SWN p.214: "A tie on the roll results in both Attack and Counterattack succeeding." """
        # Equal ratings and one fixed die each: the same seed gives the same 1d10 to both sides.
        class SameDie(random.Random):
            def randint(self, a: int, b: int) -> int:
                return 5

        # security_personnel attacks "Force vs. Force": equal Force ratings plus equal dice is a tie.
        result = assets.attack_exchange("security_personnel", "hitmen",
                                        attacker_ratings={"Cunning": 0, "Force": 2, "Wealth": 0},
                                        defender_ratings={"Cunning": 0, "Force": 2, "Wealth": 0},
                                        rng=SameDie())
        self.assertTrue(result["tie"])
        self.assertTrue(result["attacker_hits"])
        self.assertTrue(result["defender_counterattacks"])

    def test_the_defender_counters_with_its_own_die(self) -> None:
        class DefenderWins(random.Random):
            calls = 0

            def randint(self, a: int, b: int) -> int:
                self.calls += 1
                return 1 if self.calls == 1 else 10

        result = assets.attack_exchange("security_personnel", "party_machine",
                                        attacker_ratings={"Cunning": 0, "Force": 0, "Wealth": 0},
                                        defender_ratings={"Cunning": 5, "Force": 0, "Wealth": 0},
                                        rng=DefenderWins())
        # security_personnel attacks with Force and party_machine defends with Cunning
        self.assertFalse(result["attacker_hits"])
        self.assertTrue(result["defender_counterattacks"])
        self.assertGreaterEqual(result["damage_to_attacker"], 1, "party_machine's counter is 1d6")

    def test_an_asset_without_an_attack_cannot_attack(self) -> None:
        with self.assertRaises(assets.FactionAssetError):
            assets.attack_exchange("false_front", "smugglers",
                                   attacker_ratings=RATINGS, defender_ratings=RATINGS,
                                   rng=random.Random(1))

    def test_a_missing_rating_is_named_rather_than_assumed(self) -> None:
        with self.assertRaises(assets.FactionAssetError) as caught:
            assets.attack_exchange("smugglers", "false_front",
                                   attacker_ratings={"Force": 1}, defender_ratings={"Wealth": 1},
                                   rng=random.Random(1))
        self.assertIn("Cunning", str(caught.exception))

    def test_damage_expression_parsing(self) -> None:
        self.assertEqual(assets.damage_roll("1d3+1", rng=random.Random(0)) >= 1, True)
        with self.assertRaises(assets.FactionAssetError):
            assets.damage_roll("a lot", rng=random.Random(0))
        # A negative modifier can floor at 0 rather than healing the target.
        for seed in range(20):
            self.assertGreaterEqual(assets.damage_roll("1d4-1", rng=random.Random(seed)), 0)


class PurchaseTests(unittest.TestCase):
    def test_buying_charges_the_catalogue_cost_and_takes_the_printed_hp(self) -> None:
        faction = Faction(identifier="unsa", credits=10)
        bought = assets.purchase(faction, "smugglers", identifier="smugglers_1", location="terra")
        self.assertEqual(faction.credits, 8)
        self.assertEqual((bought.hp, bought.max_hp), (4, 4))
        self.assertIn("smugglers_1", faction.assets)

    def test_insufficient_credits_is_refused(self) -> None:
        faction = Faction(identifier="unsa", credits=1)
        with self.assertRaises(FactionTurnError):
            assets.purchase(faction, "smugglers", identifier="s1", location="terra")
        self.assertEqual(faction.credits, 1)

    def test_the_base_of_influence_is_bought_by_expanding_influence(self) -> None:
        faction = Faction(identifier="unsa", credits=50)
        with self.assertRaises(assets.FactionAssetError) as caught:
            assets.purchase(faction, "base_of_influence", identifier="b1", location="terra")
        self.assertIn("Expand Influence", str(caught.exception))

    def test_an_asset_with_no_hit_points_cannot_be_fielded(self) -> None:
        with self.assertRaises(assets.FactionAssetError):
            assets.to_turn_asset("stealth", identifier="st1", faction="unsa", location="terra")

    def test_one_purchase_per_turn(self) -> None:
        faction = Faction(identifier="unsa", credits=20, actions_taken=1)
        with self.assertRaises(FactionTurnError):
            assets.purchase(faction, "informers", identifier="i1", location="terra")


class CatalogueFileTests(unittest.TestCase):
    def test_the_committed_file_matches_the_runtime_view(self) -> None:
        raw = json.loads((ROOT / "data/rules/swn_faction_assets.json").read_text(encoding="utf-8"))
        self.assertEqual(assets.catalogue_size(), len(raw["assets"]))
        self.assertEqual({entry["id"] for entry in raw["assets"]}, set(assets.ASSETS))

    def test_the_source_records_what_it_does_not_reproduce(self) -> None:
        raw = json.loads((ROOT / "data/rules/swn_faction_assets.json").read_text(encoding="utf-8"))
        note = raw["source"]["note"].lower()
        self.assertIn("not", note)
        self.assertIn("legend", note)


if __name__ == "__main__":
    unittest.main()
