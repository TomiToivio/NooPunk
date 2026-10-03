"""Embodiment and inventory primitives for the #60 playable slice.

This is intentionally a compact NoöPunk/EP2-homebrew adapter layer. It preserves the
identity-versus-body distinction without importing a full Eclipse Phase morph catalog.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True, slots=True)
class EP2Embodiment:
    """Minimal body/platform record used by the prototype."""

    name: str
    kind: str = "biological"
    durability: int = 30
    wound_threshold: int = 6
    traits: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Embodiment name must not be empty.")
        if not self.kind.strip():
            raise ValueError("Embodiment kind must not be empty.")
        if self.durability <= 0 or self.wound_threshold <= 0:
            raise ValueError("Embodiment durability and wound threshold must be positive.")


@dataclass(frozen=True, slots=True)
class EP2GearItem:
    """Small structured gear entry; effects remain explicit rather than prose-driven."""

    item_id: str
    name: str
    category: str = "general"
    quantity: int = 1
    tags: tuple[str, ...] = ()
    effects: Mapping[str, int | str | bool] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.item_id.strip() or not self.name.strip():
            raise ValueError("Gear requires nonempty item_id and name.")
        if self.quantity < 1:
            raise ValueError("Gear quantity must be at least one.")


@dataclass(slots=True)
class EP2Inventory:
    """Deterministic inventory with stack-safe add/remove operations."""

    items: dict[str, EP2GearItem] = field(default_factory=dict)

    def add(self, item: EP2GearItem) -> None:
        existing = self.items.get(item.item_id)
        if existing is None:
            self.items[item.item_id] = item
            return
        if (
            existing.name != item.name
            or existing.category != item.category
            or tuple(existing.tags) != tuple(item.tags)
            or dict(existing.effects) != dict(item.effects)
        ):
            raise ValueError("Cannot stack gear records with conflicting metadata.")
        self.items[item.item_id] = EP2GearItem(
            item_id=existing.item_id,
            name=existing.name,
            category=existing.category,
            quantity=existing.quantity + item.quantity,
            tags=existing.tags,
            effects=existing.effects,
        )

    def remove(self, item_id: str, quantity: int = 1) -> EP2GearItem:
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError("Removal quantity must be at least one.")
        existing = self.items.get(item_id)
        if existing is None or existing.quantity < quantity:
            raise ValueError("Not enough gear to remove.")
        removed = EP2GearItem(
            item_id=existing.item_id,
            name=existing.name,
            category=existing.category,
            quantity=quantity,
            tags=existing.tags,
            effects=existing.effects,
        )
        remaining = existing.quantity - quantity
        if remaining:
            self.items[item_id] = EP2GearItem(
                item_id=existing.item_id,
                name=existing.name,
                category=existing.category,
                quantity=remaining,
                tags=existing.tags,
                effects=existing.effects,
            )
        else:
            del self.items[item_id]
        return removed

    def has(self, item_id: str, quantity: int = 1) -> bool:
        if quantity < 1:
            raise ValueError("Quantity must be at least one.")
        existing = self.items.get(item_id)
        return existing is not None and existing.quantity >= quantity
