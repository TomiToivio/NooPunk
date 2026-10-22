"""Lightweight tabletop-facing traits for Noöpunk RPG v0.1."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    name: str
    rank: int = 0

    def __post_init__(self) -> None:
        if self.rank < 0 or self.rank > 4:
            raise ValueError("Skill rank must be between +0 and +4")


@dataclass(frozen=True)
class Aspect:
    name: str
    description: str = ""
    invoke_bonus: int = 1


@dataclass(frozen=True)
class Stunt:
    name: str
    description: str
    action: str
    bonus: int = 2


@dataclass(frozen=True)
class Condition:
    name: str
    domain: str = "general"
    recovery: str = "fictional permission"


@dataclass(frozen=True)
class Consequence:
    name: str
    severity: int
    domain: str = "general"

    def __post_init__(self) -> None:
        if self.severity not in (2, 4, 6):
            raise ValueError("Consequence severity must be mild 2, moderate 4, or severe 6")


def advance_skill(character, skill: str, *, cost: int = 1, cap: int = 4) -> int:
    """Spend an advancement point to raise one skill, respecting the v0.1 cap."""
    if cost < 1:
        raise ValueError("Advancement cost must be positive")
    if character.advancement < cost:
        raise ValueError("Not enough advancement points")
    current = character.skill(skill)
    if current >= cap:
        raise ValueError(f"Skill is already at the +{cap} cap")
    character.skills[skill] = current + 1
    character.advancement -= cost
    return character.skills[skill]
