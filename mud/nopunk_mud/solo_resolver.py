"""CWN-backed resolver for the phase-1 engine-independent solo arc (#966).

No Evennia import. Difficulty and skill mappings are explicit so scenario prose
cannot silently invent a new dice system.
"""
from __future__ import annotations

import random
from collections.abc import Callable, Mapping

from . import cwn_core

DIFFICULTY = {"routine": 8, "standard": 10, "hard": 12, "extreme": 14}
SKILL = {"notice": "notice", "program": "program", "shoot": "shoot",
         "fight": "fight", "connect": "connect", "talk": "talk"}


def make_resolver(
    attributes: Mapping[str, int],
    ranks: Mapping[str, int],
    *,
    skill_attributes: Mapping[str, str] | None = None,
    rng: random.Random | None = None,
) -> Callable[[str, str, tuple[int, ...]], bool]:
    """Bind a CWN sheet to the arc's (skill, difficulty, dice) callback.

    Production resolves with a Random source, while tests may pass exactly
    two explicit d6 faces. Unknown skill/difficulty/attribute fails closed.
    """
    association = dict(skill_attributes or {})
    source = rng or random.Random()

    def resolve(skill: str, difficulty: str, dice: tuple[int, ...] = ()) -> bool:
        name = SKILL.get(skill.lower())
        if name is None:
            raise ValueError(f"unsupported CWN skill: {skill}")
        target = DIFFICULTY.get(difficulty.lower())
        if target is None:
            raise ValueError(f"unsupported CWN difficulty: {difficulty}")
        attribute = association.get(name, "WIS" if name == "notice" else "INT").upper()
        if attribute not in cwn_core.ATTRIBUTES:
            raise ValueError(f"unsupported CWN attribute: {attribute}")
        if attribute not in attributes:
            raise ValueError(f"missing CWN attribute: {attribute}")
        if dice and (len(dice) != 2 or any(type(d) is not int or not 1 <= d <= 6 for d in dice)):
            raise ValueError("skill check dice must be two d6 faces")
        return cwn_core.skill_check(
            rank=int(ranks.get(name, -1)),
            attribute_score=int(attributes[attribute]),
            difficulty=target,
            dice=(dice[0], dice[1]) if dice else None,
            rng=source,
        ).success

    return resolve
