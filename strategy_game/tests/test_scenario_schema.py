"""Tests for the generic city-and-environs scenario schema (issue #324 deliverable C).

Executable-code tests only, per #271. The point of these is that the validator can *fail*: almost
every test below mutates a copy of the real scenario and demands that the specific problem is
reported, so a passing run means the shape was genuinely checked rather than assumed. The
second-city test is the one that proves the schema is reusable rather than Ukweli-shaped.
"""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from strategy_game.local_slice import DATA, PORTFOLIOS, Game
from strategy_game.scenario_schema import (
    SCHEMA_FORMAT,
    SCHEMA_VERSION,
    ScenarioSchemaError,
    build_local_game,
    load_scenario,
    load_schema,
    validate_scenario,
)

#: Every mutation below must be *detected*, or the guard is decoration.
MUTATIONS = [
    ("missing a required top-level field", lambda d: d.pop("setting"), "setting: required field missing"),
    ("a wrong top-level type", lambda d: d.__setitem__("year", "2027"), "year: expected int"),
    ("too few locations", lambda d: d.__setitem__("locations", d["locations"][:4]), "locations: needs at least 5 items"),
    ("a duplicate location id", lambda d: d["locations"][1].__setitem__("id", d["locations"][0]["id"]), "duplicate id"),
    ("an unknown record field", lambda d: d["locations"][0].__setitem__("colur", "red"), "unknown field 'colur'"),
    ("a wrong record type", lambda d: d["locations"][0].__setitem__("pressure", "high"), "'pressure' expected int"),
    ("a route with an unknown endpoint", lambda d: d["routes"][0].__setitem__(0, "atlantis"), "endpoint 'atlantis' is not a location id"),
    ("a route that does not pair", lambda d: d["routes"].append(["civic"]), "two-element list"),
    ("a leader in an unknown location", lambda d: d["leaders"][0].__setitem__("location", "atlantis"), "is not a location id"),
    ("a leader in an unknown faction", lambda d: d["leaders"][0].__setitem__("faction", "nobody"), "is not a party id"),
    ("a leader with an undeclared portfolio", lambda d: d["leaders"][0].__setitem__("portfolio", "propaganda"), "is not one of"),
    ("a party with three leaders", lambda d: d["parties"][0]["leader_ids"].pop(), "needs exactly 4 leader_ids"),
    ("a party citing an unknown leader", lambda d: d["parties"][0]["leader_ids"].__setitem__(0, "ghost"), "is not a leader"),
    ("a relationship to an unknown leader", lambda d: d["relationships"][0].__setitem__("b", "ghost"), "is not a leader id"),
    ("a relationship with identical endpoints", lambda d: d["relationships"][0].__setitem__("b", d["relationships"][0]["a"]), "two different endpoints"),
]


class SchemaContractTests(unittest.TestCase):
    def test_the_schema_file_declares_its_own_contract(self) -> None:
        schema = load_schema()
        self.assertEqual(schema["format"], SCHEMA_FORMAT)
        self.assertEqual(schema["version"], SCHEMA_VERSION)
        self.assertTrue(schema["reference_instance"].endswith("ukweli_local.json"))

    def test_the_declared_portfolios_match_the_engine(self) -> None:
        """The schema consumes the vocabulary instead of restating a second copy of it."""
        declared = tuple(load_schema()["vocabulary_is_consumed_not_restated"]["portfolios"])
        self.assertEqual(declared, tuple(PORTFOLIOS))

    def test_a_malformed_schema_contract_is_refused(self) -> None:
        for mutated in ({"format": "other"}, {"version": 99}):
            payload = json.loads(load_schema.__globals__["SCHEMA_PATH"].read_text(encoding="utf-8"))
            payload.update(mutated)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "schema.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(ScenarioSchemaError):
                    load_schema(path)


class RealScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_the_ukweli_configuration_conforms_to_the_schema(self) -> None:
        self.assertEqual(validate_scenario(self.data), ())

    def test_load_scenario_returns_the_data_and_no_problems(self) -> None:
        data, problems = load_scenario(DATA)
        self.assertEqual(problems, ())
        self.assertEqual(len(data["locations"]), 8)
        self.assertEqual(len(data["parties"]), 3)
        self.assertEqual(len(data["leaders"]), 12)

    def test_every_declared_mutation_is_detected(self) -> None:
        for description, mutate, expected in MUTATIONS:
            with self.subTest(description):
                candidate = copy.deepcopy(self.data)
                mutate(candidate)
                problems = validate_scenario(candidate)
                self.assertTrue(
                    any(expected in problem for problem in problems),
                    f"{description}: expected {expected!r} in {problems}",
                )

    def test_a_missing_scenario_file_is_reported(self) -> None:
        with self.assertRaises(ScenarioSchemaError):
            load_scenario(Path(tempfile.gettempdir()) / "definitely_not_a_scenario.json")


class ReusabilityTests(unittest.TestCase):
    """A second city must validate without touching code — that is what 'generic' has to mean."""

    def _second_city(self) -> dict:
        return {
            "format": "noopunk.strategy_game.example_second_city",
            "year": 2028,
            "setting": "A generic second city used only to prove the schema is not Ukweli-shaped",
            "locations": [
                {"id": "quay", "label": "Quay", "pressure": 1, "tags": ["trade"]},
                {"id": "market", "label": "Market", "pressure": 0, "tags": ["civic"]},
                {"id": "hill", "label": "Hill District", "tags": []},
                {"id": "works", "label": "Works", "tags": ["industry"]},
                {"id": "inlet", "label": "Inlet", "tags": ["water"]},
            ],
            "routes": [["quay", "market"], ["market", "hill"], ["works", "market"], ["inlet", "quay"]],
            "parties": [
                {"id": "harbour", "name": "Harbour League", "leader_ids": ["h1", "h2", "h3", "h4"]},
                {"id": "upland", "name": "Upland Assembly", "leader_ids": ["u1", "u2", "u3", "u4"]},
            ],
            "leaders": [
                {"id": "h1", "name": "Harbour Chair", "faction": "harbour", "location": "quay", "portfolio": "politics"},
                {"id": "h2", "name": "Harbour Organiser", "faction": "harbour", "location": "market", "portfolio": "networks"},
                {"id": "h3", "name": "Harbour Steward", "faction": "harbour", "location": "works", "portfolio": "operations"},
                {"id": "h4", "name": "Harbour Analyst", "faction": "harbour", "location": "inlet", "portfolio": "research"},
                {"id": "u1", "name": "Upland Chair", "faction": "upland", "location": "hill", "portfolio": "politics"},
                {"id": "u2", "name": "Upland Organiser", "faction": "upland", "location": "hill", "portfolio": "networks"},
                {"id": "u3", "name": "Upland Steward", "faction": "upland", "location": "works", "portfolio": "operations"},
                {"id": "u4", "name": "Upland Analyst", "faction": "upland", "location": "market", "portfolio": "research"},
            ],
            "relationships": [{"a": "h1", "b": "u1", "trust": -1, "tags": ["rivals"]}],
            "shocks": [{"title": "A generic shock", "legitimacy_delta": 0}],
        }

    def test_a_second_city_validates_without_code_changes(self) -> None:
        self.assertEqual(validate_scenario(self._second_city()), ())

    def test_the_engine_accepts_the_second_city_through_the_same_bridge(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "second_city.json"
            path.write_text(json.dumps(self._second_city()), encoding="utf-8")
            data, problems = load_scenario(path)
            self.assertEqual(problems, ())
            game = Game.from_scenario(path)
        self.assertEqual(len(game.parties), 2)
        self.assertEqual(len(game.leaders), 8)
        self.assertEqual(len(game.locations), 5)


class BridgeTests(unittest.TestCase):
    def test_build_local_game_validates_then_builds_the_ukweli_slice(self) -> None:
        game = build_local_game()
        self.assertEqual(len(game.parties), 3)
        self.assertEqual(len(game.leaders), 12)
        game.validate()  # the engine's own invariants still hold

    def test_the_bridge_refuses_a_scenario_that_fails_the_schema(self) -> None:
        broken = json.loads(DATA.read_text(encoding="utf-8"))
        broken["leaders"][0]["portfolio"] = "propaganda"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "broken.json"
            path.write_text(json.dumps(broken), encoding="utf-8")
            with self.assertRaises(ScenarioSchemaError):
                build_local_game(path)


if __name__ == "__main__":
    unittest.main()
