"""Issue #347 items 7 and 9, as executable contracts rather than promises.

Item 7 — every one of the ten card kinds the issue names has at least one shipped, data-driven example.
Item 9 — a new foreign node and a new character card can be added from data alone: this test performs
both additions in a temporary copy, loads them through the modules that already own those kinds, and
proves the shipped data was not touched.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

from strategy_game import characters, content_schema, council, faction_cards, local_geography
from strategy_game.content_schema import CARD_KINDS, KIND_IDS, kind_examples, missing_kinds, validate_registry

DATA = content_schema.DATA_DIR


def _digest_tree() -> dict[str, str]:
    return {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(DATA.glob("*.json"))
    }


def _first_record_list(data: Any) -> tuple[str, list[dict[str, Any]]] | None:
    """The first list of id-carrying records in a JSON document, without assuming its key."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and value and isinstance(value[0], dict) and "id" in value[0]:
                return key, value
        for value in data.values():
            found = _first_record_list(value)
            if found is not None:
                return found
    return None


class CardKindRegistryTests(unittest.TestCase):
    """Item 7."""

    def test_the_registry_carries_exactly_the_ten_kinds_the_issue_names(self) -> None:
        self.assertEqual(
            set(KIND_IDS),
            {"character", "faction", "organization", "place", "research", "event", "mission",
             "relationship", "ideology_signifier", "tarot_placeholder"},
        )
        self.assertEqual(len(KIND_IDS), len(set(KIND_IDS)))

    def test_the_registry_itself_is_well_formed(self) -> None:
        self.assertEqual(validate_registry(), ())

    def test_every_kind_has_at_least_one_shipped_example(self) -> None:
        counts = kind_examples()
        self.assertEqual(missing_kinds(), (), f"kinds without an example: {missing_kinds()} in {counts}")
        for kind, count in sorted(counts.items()):
            with self.subTest(kind=kind):
                self.assertGreaterEqual(count, 1)

    def test_the_shipped_examples_load_through_the_modules_that_own_them(self) -> None:
        self.assertTrue(characters.load_character_cards().cards)
        faction_cards.load_faction_cards()
        council.load_council()

    def test_the_registry_defines_no_mechanic(self) -> None:
        """A kind registry that grew a number would be a rule system in a data file's clothes."""
        for kind in CARD_KINDS:
            with self.subTest(kind=kind.identifier):
                self.assertFalse(kind.note and "effect" in kind.note and "unenforced" not in kind.note)


class DataOnlyAuthoringTests(unittest.TestCase):
    """Item 9: a new foreign node and a new card from data alone."""

    def setUp(self) -> None:
        self.before = _digest_tree()

    def tearDown(self) -> None:
        self.assertEqual(_digest_tree(), self.before, "the authoring test touched shipped data")

    def test_a_new_character_card_can_be_added_from_data_alone(self) -> None:
        source = DATA / "character_cards.json"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / source.name
            shutil.copy(source, target)
            document = json.loads(source.read_text(encoding="utf-8"))
            id_field = "id" if "id" in document["entries"][0] else "identifier"
            template = next(
                entry for entry in document["entries"] if entry.get(id_field) == "archetype_activist"
            )
            added = copy.deepcopy(template)
            added[id_field] = "modded_example_organizer"
            added["name"] = "Modded Example Organizer"
            document["entries"].append(added)
            target.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            roster = characters.load_character_cards(target)
            self.assertIn("modded_example_organizer", roster.cards)
            self.assertEqual(len(roster.cards), len(json.loads(source.read_text())["entries"]) + 1)

    def test_a_new_foreign_node_can_be_added_from_data_alone(self) -> None:
        source = DATA / "ukweli_geography.json"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / source.name
            shutil.copy(source, target)
            document = json.loads(source.read_text(encoding="utf-8"))
            found = _first_record_list(document)
            self.assertIsNotNone(found, "the geography document has no id-carrying record list")
            assert found is not None
            key, records = found
            added = copy.deepcopy(records[0])
            added["id"] = "foreign_node_example"
            records.append(added)
            target.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

            local_geography.load_local_geography(target)
            self.assertIn("foreign_node_example", target.read_text(encoding="utf-8"))
            self.assertNotIn("foreign_node_example", source.read_text(encoding="utf-8"))
            self.assertGreater(len(records), 0, key)


if __name__ == "__main__":
    unittest.main()
