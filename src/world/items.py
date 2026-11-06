"""Carried items, issued kit and the device-grant bridge (#1217).

The audit on #1217 found the gap this fills: `data/rules/cwn_equipment.json` lists weapons and armour,
the first-day adapter tracked its kit as bare string flags, and the device-PSI path
(`swn_psionics.Psychic.commit_device_grant`) required `active_sources` that **nothing produced**. So
equipment could be "inspected" without existing, and a psychotronic implant could grant an effect while
the question "is the device actually on you and working?" had no answer.

This module is deliberately small and not a second equipment engine:

* it records **what is carried and whether it is active**, not what anything costs — CWN's equipment
  rules stay the authority for cost, damage and encumbrance;
* `active_sources()` is the input `commit_device_grant` already asks for;
* `coverage()` makes the opening's diagnostic puzzle honest: a function is available if **some** active,
  unfaulted item provides it, which is what stops a broken radio from softlocking the first day.
"""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "FIRST_DAY_REQUIRED",
    "FUNCTIONS",
    "ITEM_KINDS",
    "CarriedItem",
    "Item",
    "ItemError",
    "Kit",
    "first_day_kit",
]

ITEM_KINDS: tuple[str, ...] = ("uniform", "weapon", "armour", "tool", "device", "consumable")

#: Functions a scene may require. They are interface capabilities, not skills.
FUNCTIONS: tuple[str, ...] = (
    "uniform",
    "dispatch.call",
    "radio",
    "phone",
    "records",
    "forensics",
    "weapon",
    "weapon.melee",
    "psi.interface",
    "recording",
)

#: What the opening needs before Tony can report for duty: get dressed, call Dispatch. Deliberately
#: function-based and deliberately short — *any* item that provides a function satisfies it, so a dead
#: radio, a seized sidearm or a broken scanner costs a decision, never the intro (#1217: "equipment
#: failure must not softlock the intro"). Kit is still inspected and connected; it just is not a
#: prerequisite for being able to report.
FIRST_DAY_REQUIRED: tuple[str, ...] = (
    "uniform",
    "dispatch.call",
)


class ItemError(ValueError):
    """An item was carried, activated or granted in a way its state does not allow."""


@dataclass(frozen=True)
class Item:
    """A definition. State lives on `CarriedItem`; a definition never mutates."""

    id: str
    label: str
    kind: str
    functions: tuple[str, ...] = ()
    grants: tuple[str, ...] = ()
    worn: bool = False

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ItemError("an item needs an id")
        if not self.label.strip():
            raise ItemError(f"{self.id!r} needs a label")
        if self.kind not in ITEM_KINDS:
            raise ItemError(f"unknown item kind {self.kind!r}; expected {ITEM_KINDS}")
        unknown = [function for function in self.functions if function not in FUNCTIONS]
        if unknown:
            raise ItemError(f"{self.id!r} claims unknown functions {unknown}")
        object.__setattr__(self, "functions", tuple(self.functions))
        object.__setattr__(self, "grants", tuple(self.grants))


@dataclass
class CarriedItem:
    """One actor's instance of an item: carried, maybe active, maybe faulty."""

    item: Item
    carried: bool = True
    active: bool = False
    fault: str = ""

    @property
    def usable(self) -> bool:
        return self.carried and not self.fault

    @property
    def providing(self) -> tuple[str, ...]:
        return self.item.functions if self.usable and self.active else ()


@dataclass
class Kit:
    """The items one actor carries. Actor-scoped so two people cannot share one radio."""

    actor: str
    items: dict[str, CarriedItem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.actor.strip():
            raise ItemError("a kit belongs to an actor")

    # -- issuing ---------------------------------------------------------- #
    def issue(self, item: Item) -> CarriedItem:
        if item.id in self.items:
            raise ItemError(f"{item.id!r} is already carried by {self.actor!r}")
        # Worn kit is already in use; everything else must be switched on at the interface.
        carried = CarriedItem(item=item, active=item.worn)
        self.items[item.id] = carried
        return carried

    def get(self, item_id: str) -> CarriedItem:
        try:
            return self.items[item_id]
        except KeyError:
            raise ItemError(f"{self.actor!r} does not carry {item_id!r}") from None

    def stow(self, item_id: str) -> CarriedItem:
        carried = self.get(item_id)
        carried.carried = False
        carried.active = False
        return carried

    def take(self, item_id: str) -> CarriedItem:
        carried = self.get(item_id)
        carried.carried = True
        return carried

    # -- the diagnostic puzzle -------------------------------------------- #
    def activate(self, item_id: str) -> CarriedItem:
        carried = self.get(item_id)
        if not carried.usable:
            raise ItemError(f"{item_id!r} cannot be activated{': ' + carried.fault if carried.fault else ''}")
        carried.active = True
        return carried

    def deactivate(self, item_id: str) -> CarriedItem:
        carried = self.get(item_id)
        carried.active = False
        return carried

    def mark_faulty(self, item_id: str, reason: str) -> CarriedItem:
        """Break a device. It stops providing functions and stops granting effects."""
        if not reason.strip():
            raise ItemError("a fault needs a reason the player can act on")
        carried = self.get(item_id)
        carried.fault = reason.strip()
        carried.active = False
        return carried

    def repair(self, item_id: str) -> CarriedItem:
        carried = self.get(item_id)
        carried.fault = ""
        return carried

    # -- what the rest of the system reads -------------------------------- #
    def active_sources(self) -> frozenset[str]:
        """Exactly the argument `commit_device_grant(active_sources=...)` expects."""
        return frozenset(
            carried.item.id for carried in self.items.values() if carried.active and carried.usable
        )

    def coverage(self) -> dict[str, tuple[str, ...]]:
        """function -> item ids that currently provide it (active and unfaulted)."""
        found: dict[str, list[str]] = {}
        for carried in sorted(self.items.values(), key=lambda entry: entry.item.id):
            for function in carried.providing:
                found.setdefault(function, []).append(carried.item.id)
        return {function: tuple(ids) for function, ids in found.items()}

    def missing(self, required: Iterable[str] = FIRST_DAY_REQUIRED) -> tuple[str, ...]:
        covered = set(self.coverage())
        return tuple(function for function in required if function not in covered)

    def grants(self) -> tuple[tuple[str, str], ...]:
        """(ability, source) pairs from active, unfaulted items — never selectable options."""
        pairs: list[tuple[str, str]] = []
        for carried in sorted(self.items.values(), key=lambda entry: entry.item.id):
            if carried.active and carried.usable:
                pairs.extend((ability, carried.item.id) for ability in carried.item.grants)
        return tuple(pairs)

    # -- serialization ---------------------------------------------------- #
    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "noopunk.kit",
            "version": 1,
            "actor": self.actor,
            "items": [
                {
                    "id": carried.item.id,
                    "carried": carried.carried,
                    "active": carried.active,
                    "fault": carried.fault,
                }
                for carried in sorted(self.items.values(), key=lambda entry: entry.item.id)
            ],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> Kit:
        definitions = {item.id: item for item in first_day_kit()}
        kit = cls(actor=str(payload["actor"]))
        for raw in payload.get("items", ()):
            item_id = str(raw["id"])
            if item_id not in definitions:
                raise ItemError(f"no item definition for {item_id!r}")
            kit.issue(definitions[item_id])
            carried = kit.items[item_id]
            carried.carried = bool(raw.get("carried", True))
            carried.active = bool(raw.get("active", False))
            carried.fault = str(raw.get("fault", ""))
        return kit


def first_day_kit() -> tuple[Item, ...]:
    """The kit Tony is issued. One source of truth: `first_day.py` derives its id list from here."""
    return (
        Item("uniform", "Academy graduation uniform", "uniform",
             functions=("uniform",), worn=True),
        Item("police_radio", "Europol police radio", "device",
             functions=("dispatch.call", "radio")),
        Item("phone", "Europol phone", "device", functions=("dispatch.call", "phone")),
        Item("computer", "Field computer", "tool", functions=("records",)),
        Item("forensic_scanner", "Forensic scanner", "tool", functions=("forensics",)),
        Item("gun", "Service sidearm", "weapon", functions=("weapon",)),
        Item("sword", "Ceremonial sword", "weapon", functions=("weapon", "weapon.melee")),
        Item("romppainen_fujita_device", "Romppainen–Fujita device", "device",
             functions=("psi.interface",), grants=("psychotronic link",)),
        Item("body_camera", "Body camera", "device", functions=("recording",)),
    )
