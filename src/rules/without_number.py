"""Initial Without Number-style RPG kernel for NoöPunk (#615).

This is the new target chassis for migration, not an automatic reinterpretation
of existing legacy save files or the strategy crossover. All algorithms here are
original code expressing common dice mechanics. No book text is reproduced.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import Mapping, Protocol

ATTRIBUTES = ("STR", "DEX", "CON", "INT", "WIS", "CHA")
SKILLS = (
    "Administer", "Connect", "Drive", "Exert", "Fix", "Heal", "Know",
    "Lead", "Notice", "Perform", "Pilot", "Program", "Punch", "Shoot",
    "Sneak", "Stab", "Survive", "Talk", "Trade", "Work",
)
ENVIRONMENTS = ("urban", "space", "noetic", "crisis")
UNTRAINED = -1
MAX_SKILL = 4


class Dice(Protocol):
    def randint(self, low: int, high: int) -> int: ...


def roll(sides: int, count: int = 1, rng: Dice | None = None) -> int:
    if sides < 2 or count < 1:
        raise ValueError("Invalid dice specification")
    source = rng if rng is not None else random
    return sum(source.randint(1, sides) for _ in range(count))


def modifier(score: int) -> int:
    """The six Without Number attribute score modifier bands."""
    if not 3 <= score <= 18:
        raise ValueError("Attribute score must be 3..18")
    if score == 18:
        return 2
    if score >= 14:
        return 1
    if score >= 8:
        return 0
    if score >= 4:
        return -1
    return -2


@dataclass
class Character:
    attributes: Mapping[str, int]
    skills: Mapping[str, int] = field(default_factory=dict)
    level: int = 1
    hit_points: int = 1
    effort_max: int = 0
    effort_committed: int = 0
    inventory: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if set(self.attributes) != set(ATTRIBUTES):
            raise ValueError("A character needs the six Without Number attributes")
        for score in self.attributes.values():
            modifier(score)
        if not 1 <= self.level:
            raise ValueError("Level must be positive")
        if self.hit_points < 0:
            raise ValueError("Hit points cannot be negative")
        if self.effort_max < 0 or not 0 <= self.effort_committed <= self.effort_max:
            raise ValueError("Invalid Effort pool")
        for name, level in self.skills.items():
            if name not in SKILLS or not UNTRAINED <= level <= MAX_SKILL:
                raise ValueError(f"Invalid skill rating: {name}={level}")

    def skill_level(self, name: str) -> int:
        if name not in SKILLS:
            raise KeyError(name)
        return self.skills.get(name, UNTRAINED)

    def commit_effort(self, amount: int = 1) -> None:
        if amount < 1 or self.effort_committed + amount > self.effort_max:
            raise ValueError("Not enough available Effort")
        self.effort_committed += amount

    def release_effort(self, amount: int = 1) -> None:
        if amount < 1 or amount > self.effort_committed:
            raise ValueError("Cannot release uncommitted Effort")
        self.effort_committed -= amount


@dataclass(frozen=True)
class Result:
    dice: int
    total: int
    target: int
    success: bool


def skill_check(character: Character, attribute: str, skill: str, target: int = 8,
                rng: Dice | None = None) -> Result:
    if attribute not in ATTRIBUTES:
        raise KeyError(attribute)
    rolled = roll(6, 2, rng)
    total = rolled + modifier(character.attributes[attribute]) + character.skill_level(skill)
    return Result(rolled, total, target, total >= target)


def attack_check(attack_bonus: int, armor_class: int, rng: Dice | None = None,
                 attribute_modifier: int = 0) -> Result:
    """d20 attacks vs ascending AC; caller owns weapon and target rules."""
    rolled = roll(20, rng=rng)
    total = rolled + attack_bonus + attribute_modifier
    return Result(rolled, total, armor_class, total >= armor_class)


def saving_throw(target: int, bonus: int = 0, rng: Dice | None = None) -> Result:
    rolled = roll(20, rng=rng)
    total = rolled + bonus
    return Result(rolled, total, target, total >= target)


def enter_environment(character: Character, environment: str) -> Character:
    """Switch the scene toolkit, never convert the character sheet."""
    if environment not in ENVIRONMENTS:
        raise ValueError(f"Unknown environment: {environment}")
    return character
