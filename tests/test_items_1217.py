"""Carried items, issued kit and the device-grant bridge (#1217).

The gap: kit was string flags, `commit_device_grant` demanded `active_sources` nobody produced, and a
broken radio could either be ignored or dead-end the intro. These tests pin the state model, the
no-softlock rule, and the bridge into the PSI accounting that already exists.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from src.rules.psi_access import PsiAccessError, device_grant
from src.rules.swn_psionics import Duration, Psychic
from src.world.items import (
    FIRST_DAY_REQUIRED,
    ItemError,
    Kit,
    first_day_kit,
)


def kit(actor: str = "tony.german") -> Kit:
    book = Kit(actor)
    for item in first_day_kit():
        book.issue(item)
    return book


def ready(book: Kit) -> Kit:
    for item_id in ("police_radio", "phone", "computer", "gun", "body_camera"):
        book.activate(item_id)
    return book


class State(unittest.TestCase):
    def test_the_worn_uniform_starts_in_use_and_nothing_else_does(self) -> None:
        book = kit()
        self.assertTrue(book.get("uniform").active)
        self.assertFalse(book.get("police_radio").active)
        self.assertEqual(book.active_sources(), frozenset({"uniform"}))

    def test_the_same_item_cannot_be_issued_twice(self) -> None:
        book = kit()
        with self.assertRaises(ItemError):
            book.issue(first_day_kit()[0])

    def test_an_unknown_item_is_refused_by_id(self) -> None:
        with self.assertRaises(ItemError):
            kit().activate("grappling_hook")

    def test_two_actors_kits_are_independent(self) -> None:
        tony, laura = kit("tony.german"), kit("laura.wendt")
        tony.stow("police_radio")
        tony.mark_faulty("gun", "the slide is seized")
        self.assertFalse(tony.get("police_radio").carried)
        self.assertTrue(laura.get("police_radio").carried)
        self.assertEqual(laura.get("gun").fault, "")
        self.assertEqual(laura.actor, "laura.wendt")


class TheDiagnosticPuzzle(unittest.TestCase):
    def test_the_opening_is_not_ready_until_the_required_functions_are_live(self) -> None:
        book = kit()
        missing = book.missing()
        self.assertIn("uniform", book.coverage())          # worn immediately
        self.assertIn("dispatch.call", missing)            # nothing connected yet
        self.assertEqual(ready(kit()).missing(), ())

    def test_a_faulty_radio_does_not_softlock_the_opening(self) -> None:
        book = ready(kit())
        book.mark_faulty("police_radio", "the battery is dead")
        self.assertEqual(book.missing(), ())
        self.assertEqual(book.coverage()["dispatch.call"], ("phone",))

    def test_a_fault_stops_the_item_providing_anything(self) -> None:
        book = ready(kit())
        book.mark_faulty("gun", "the slide is seized")
        with self.assertRaises(ItemError):
            book.activate("gun")
        self.assertIn("weapon", book.missing())

    def test_a_stowed_item_provides_nothing(self) -> None:
        book = ready(kit())
        book.stow("body_camera")
        self.assertIn("recording", book.missing())

    def test_repair_returns_the_function_without_reactivating_it(self) -> None:
        book = ready(kit())
        book.mark_faulty("police_radio", "dead battery")
        book.repair("police_radio")
        self.assertNotIn("radio", book.coverage())
        book.activate("police_radio")
        self.assertIn("radio", book.coverage())

    def test_a_fault_needs_a_reason_the_player_can_act_on(self) -> None:
        with self.assertRaises(ItemError):
            ready(kit()).mark_faulty("police_radio", "  ")


class TheDeviceGrantBridge(unittest.TestCase):
    def test_grants_come_only_from_active_devices(self) -> None:
        book = kit()
        self.assertEqual(book.grants(), ())
        book.activate("romppainen_fujita_device")
        self.assertEqual(book.grants(), (("psychotronic link", "romppainen_fujita_device"),))

    def test_a_faulty_device_grants_nothing_and_is_not_an_active_source(self) -> None:
        book = kit()
        book.activate("romppainen_fujita_device")
        book.mark_faulty("romppainen_fujita_device", "the emitter is cracked")
        self.assertEqual(book.grants(), ())
        self.assertNotIn("romppainen_fujita_device", book.active_sources())

    def test_the_kit_supplies_the_active_sources_device_psi_requires(self) -> None:
        """`commit_device_grant(active_sources=...)` had no producer before this module."""
        book = kit()
        book.activate("romppainen_fujita_device")
        grant = device_grant("psychotronic link", source="romppainen_fujita_device")
        psychic = Psychic(wisdom=10, constitution=10)
        psychic.commit_device_grant(
            "device.link", grant,
            active_sources=set(book.active_sources()),
            amount=1, duration=Duration.SCENE,
        )
        self.assertEqual(psychic.free, psychic.capacity - 1)

    def test_a_stowed_device_cannot_back_a_commitment(self) -> None:
        book = kit()
        book.activate("romppainen_fujita_device")
        book.stow("romppainen_fujita_device")
        grant = device_grant("psychotronic link", source="romppainen_fujita_device")
        with self.assertRaises(PsiAccessError):
            Psychic(wisdom=10, constitution=10).commit_device_grant(
                "device.link", grant,
                active_sources=set(book.active_sources()),
                amount=1, duration=Duration.SCENE,
            )


class Wiring(unittest.TestCase):
    def test_the_first_day_adapter_and_the_kit_share_one_item_list(self) -> None:
        from src.console.first_day import KIT

        self.assertEqual(KIT, tuple(item.id for item in first_day_kit() if not item.worn))
        self.assertEqual(len(FIRST_DAY_REQUIRED), 5)

    def test_roundtrip_preserves_carried_active_and_fault_state(self) -> None:
        book = ready(kit())
        book.mark_faulty("forensic_scanner", "no reagent cartridges")
        restored = Kit.from_dict(book.to_dict())
        self.assertEqual(restored.to_dict(), book.to_dict())
        self.assertEqual(restored.get("forensic_scanner").fault, "no reagent cartridges")

    def test_an_unknown_item_in_a_save_is_refused(self) -> None:
        payload = kit().to_dict()
        payload["items"][0]["id"] = "grappling_hook"
        with self.assertRaises(ItemError):
            Kit.from_dict(payload)


if __name__ == "__main__":
    unittest.main()
