"""Issue #60: embodiment and inventory integration tests."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime.ep2_session import EP2Session
from eclipse_phase_homebrew import (
    EP2Character,
    EP2Embodiment,
    EP2GearItem,
    EP2Inventory,
    EP2PoolState,
)


class EmbodimentInventoryTests(unittest.TestCase):
    def test_inventory_stacks_matching_items(self) -> None:
        inventory = EP2Inventory()
        inventory.add(EP2GearItem("medkit", "Medkit", quantity=1, tags=("medical",)))
        inventory.add(EP2GearItem("medkit", "Medkit", quantity=2, tags=("medical",)))
        self.assertTrue(inventory.has("medkit", 3))
        self.assertEqual(inventory.items["medkit"].quantity, 3)

    def test_inventory_rejects_conflicting_stack_metadata(self) -> None:
        inventory = EP2Inventory()
        inventory.add(EP2GearItem("tool", "Toolkit", effects={"bonus": 10}))
        with self.assertRaises(ValueError):
            inventory.add(EP2GearItem("tool", "Toolkit", effects={"bonus": 20}))

    def test_inventory_remove_is_quantity_safe(self) -> None:
        inventory = EP2Inventory(
            items={"ammo": EP2GearItem("ammo", "Ammo", quantity=3)}
        )
        removed = inventory.remove("ammo", 2)
        self.assertEqual(removed.quantity, 2)
        self.assertEqual(inventory.items["ammo"].quantity, 1)
        with self.assertRaises(ValueError):
            inventory.remove("ammo", 2)

    def test_session_persists_initial_embodiment_and_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "world.sqlite"
            session = EP2Session(path)
            body = EP2Embodiment(
                "Baseline body", kind="biological", durability=35,
                wound_threshold=7, traits=("unaugmented",),
            )
            inventory = EP2Inventory()
            inventory.add(EP2GearItem("mesh-insert", "Mesh Insert", category="ware"))
            session.add_character(
                "player",
                EP2Character("Aino"),
                EP2PoolState(),
                embodiment=body,
                inventory=inventory,
            )
            session.close()

            resumed = EP2Session(path)
            state = resumed.character_state("player")
            self.assertEqual(state["embodiment"]["name"], "Baseline body")
            self.assertEqual(state["embodiment"]["traits"], ["unaugmented"])
            self.assertEqual(state["inventory"]["mesh-insert"]["name"], "Mesh Insert")
            resumed.close()

    def test_resleeve_is_persisted_as_event(self) -> None:
        session = EP2Session(":memory:")
        session.add_character("player", EP2Character("Aino"), EP2PoolState())
        event = session.set_embodiment(
            "player",
            EP2Embodiment("Synth shell", kind="synthetic", durability=45, wound_threshold=9),
        )
        self.assertEqual(event["action"], "set_embodiment")
        self.assertEqual(
            session.character_state("player")["embodiment"]["kind"], "synthetic"
        )
        self.assertEqual(session.memories()[-1]["action"], "set_embodiment")
        session.close()

    def test_gear_mutations_are_persistent_events(self) -> None:
        session = EP2Session(":memory:")
        session.add_character("player", EP2Character("Aino"), EP2PoolState())
        add_event = session.add_gear(
            "player",
            EP2GearItem("scanner", "Portable Scanner", category="tool", quantity=2),
        )
        remove_event = session.remove_gear("player", "scanner", 1)
        self.assertEqual(add_event["action"], "add_gear")
        self.assertEqual(remove_event["action"], "remove_gear")
        self.assertEqual(session.inventory("player").items["scanner"].quantity, 1)
        self.assertEqual(
            [event["action"] for event in session.memories()],
            ["add_gear", "remove_gear"],
        )
        session.close()

    def test_character_morph_label_bootstraps_embodiment(self) -> None:
        session = EP2Session(":memory:")
        session.add_character(
            "player",
            EP2Character("Aino", morph="splicer", durability=32, wound_threshold=6),
            EP2PoolState(),
        )
        body = session.character_state("player")["embodiment"]
        self.assertEqual(body["name"], "splicer")
        self.assertEqual(body["durability"], 32)
        session.close()


if __name__ == "__main__":
    unittest.main()
