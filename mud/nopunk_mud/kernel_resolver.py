"""The CWN kernel, wired to the solo arc's injection point (#966).

`solo_arc` takes a resolver as a callable; the tests in `tests/test_solo_arc.py` inject `_always` and `_never`
because they are testing the story, not the dice. This module is the resolver a real game injects: it calls
`cwn_core` — the published arithmetic — and nothing else.

It also carries the two resolutions a scene can ask for beyond a skill check: **combat** and **hacking**. Both
use the same kernel and both return plain data, so a scene can record what happened without importing rules.

Difficulty names are the arc's vocabulary; the numbers are the published bands.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable

from nopunk_mud import cwn_core

#: The arc says "routine"; the kernel wants 8.
DIFFICULTY_NAMES: dict[str, int] = {
    "easy": 6,
    "routine": 8,
    "hard": 10,
    "very_hard": 12,
    "heroic": 14,
}


class ResolverError(ValueError):
    """A resolution the kernel refuses, named so a scene can record it rather than crash."""


def difficulty_number(name: str) -> int:
    key = str(name).strip().lower()
    if key not in DIFFICULTY_NAMES:
        raise ResolverError(f"unknown difficulty {name!r}; expected one of {tuple(DIFFICULTY_NAMES)}")
    return DIFFICULTY_NAMES[key]


#: Which attribute a NoöPunk-side skill leans on. The arc names skills, not attributes.
SKILL_ATTRIBUTES: dict[str, str] = {
    "Notice": "INT",
    "Investigate": "INT",
    "Administer": "INT",
    "Program": "INT",
    "Talk": "CHA",
    "Connect": "CHA",
    "Exert": "STR",
    "Sneak": "DEX",
    "Shoot": "DEX",
}


@dataclass(frozen=True)
class Resolver:
    """A character's competence, ready to inject into `solo_arc.advance`."""

    attributes: dict[str, int]
    skills: dict[str, int]
    rng: random.Random

    @classmethod
    def for_recruit(cls, seed: int = 7) -> "Resolver":
        return cls(
            attributes={"STR": 10, "DEX": 12, "CON": 11, "INT": 13, "WIS": 10, "CHA": 9},
            skills={"Notice": 1, "Administer": 1, "Talk": 0, "Shoot": 0},
            rng=random.Random(seed),
        )

    # ---- the callable the arc expects -------------------------------------------------------

    def __call__(self, skill: str, difficulty: str, dice: tuple[int, ...] = ()) -> bool:
        """Resolve a skill check with published numbers. `dice` is honoured when supplied."""
        return self.check(skill, difficulty, dice=dice).success

    def check(self, skill: str, difficulty: str, *, dice: Iterable[int] = ()) -> cwn_core.Check:
        pair: tuple[int, int] | None = None
        if dice:
            faces = [int(face) for face in dice]
            if len(faces) != 2:
                raise ResolverError(f"a skill check rolls 2d6, got {len(faces)} dice")
            pair = (faces[0], faces[1])
        attribute = SKILL_ATTRIBUTES.get(skill, "INT")
        score = self.attributes.get(attribute)
        if score is None:
            raise ResolverError(f"no {attribute} score on this sheet")
        return cwn_core.skill_check(
            rank=int(self.skills.get(skill, -1)),
            attribute_score=score,
            difficulty=difficulty_number(difficulty),
            dice=pair,
            rng=None if pair else self.rng,
        )


# ---- combat --------------------------------------------------------------------------------------

def attack(resolver: Resolver, *, armor_class: int, attack_bonus: int = 0,
           skill: str = "Shoot", die: int | None = None) -> dict:
    """One attack against an AC. Returns what happened; the caller decides what it means."""
    face = int(die) if die is not None else resolver.rng.randint(1, 20)
    result = cwn_core.attack_roll(
        attack_bonus=attack_bonus,
        attribute_score=resolver.attributes.get("DEX", 10),
        combat_rank=int(resolver.skills.get(skill, -1)),
        armor_class=armor_class,
        die=face,
    )
    return {"hit": bool(result.hit), "die": int(result.die), "total": int(result.total),
            "armor_class": int(result.armor_class)}


def strike(resolver: Resolver, *, weapon_die: int, roll: int | None = None) -> int:
    """Damage from one weapon die plus the Dexterity modifier, never below zero."""
    face = int(roll) if roll is not None else resolver.rng.randint(1, weapon_die)
    return int(cwn_core.damage(weapon_die, [face], resolver.attributes.get("DEX", 10))["damage"])


# ---- hacking -------------------------------------------------------------------------------------

#: A node-link intrusion reduced to what a scripted scene needs: a check against security, and a trace clock.
HACK_DIFFICULTIES: dict[str, str] = {
    "consumer": "easy",
    "corporate": "routine",
    "government": "hard",
    "military": "very_hard",
}


def hack(resolver: Resolver, *, security: str, trace_limit: int = 3,
         dice: Iterable[int] = ()) -> dict:
    """Attempt one access. Returns success, the roll, and how much trace budget was spent."""
    if security not in HACK_DIFFICULTIES:
        raise ResolverError(f"unknown security {security!r}; expected one of {tuple(HACK_DIFFICULTIES)}")
    if trace_limit < 1:
        raise ResolverError("a trace limit below 1 leaves no room to act")
    check = resolver.check("Program", HACK_DIFFICULTIES[security], dice=dice)
    return {
        "success": check.success,
        "total": check.total,
        "difficulty": check.difficulty,
        "trace_spent": 1,
        "trace_remaining": max(0, trace_limit - 1),
        # A failed intrusion costs trace too: the attempt is visible even when it does not work.
        "alarm": not check.success,
    }
