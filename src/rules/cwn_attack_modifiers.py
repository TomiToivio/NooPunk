"""Cities Without Number: attack-roll modifiers.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``), ``rules-of-the-game/combat/attacks-in-combat/``.

The SRD's attack roll is ``1d20 + attack bonus + attribute modifier + combat skill``, with ``-2`` when
the attacker lacks even level-0 in the skill. :func:`src.rules.cwn_combat.attack_roll` implements that
arithmetic and takes an ``other_modifier``; this module is where that modifier comes from.

Two circumstances in the SRD's table are **not penalties but impossibilities** — a two-handed gun
cannot be fired while in melee, and a target whose position is unknown cannot be shot at. Folding those
into a number would let a caller "shoot anyway at −4", so they raise instead.

The table is data, keyed by stable ids, so a scenario can name the circumstance in a log line without
duplicating the number.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

#: SRD attack-roll modifier table. Negative numbers are penalties.
#: Read from `data/rules/wn_core.json` (``combat.attack_modifiers.table``) rather than transcribed.
#: The two copies were byte-identical when this was found, which is the most dangerous kind of duplicate:
#: nothing fails until somebody corrects one of them. `tests/test_rule_duplication_merged.py` holds them equal.
ATTACK_MODIFIER_TABLE: dict[str, int] = {
    str(circumstance): int(modifier)
    for circumstance, modifier in json.loads(
        (Path(__file__).resolve().parents[2] / "data" / "rules" / "wn_core.json").read_text(
            encoding="utf-8"))["combat"]["attack_modifiers"]["table"].items()
}

#: Circumstances the SRD marks ``N/A``: no attack is possible, so there is no modifier to apply.
IMPOSSIBLE_CIRCUMSTANCES: dict[str, str] = {
    "two_handed_gun_in_melee": "a two-handed gun cannot be fired while in melee",
    "target_unseen_position_unknown": "the target's position is unknown, so it cannot be attacked",
}

#: How a ranged weapon is held, for the in-melee rule.
RANGED_HANDEDNESS = ("one_handed", "two_handed", "thrown")


class AttackImpossibleError(ValueError):
    """The SRD says this attack cannot be made at all."""


def attack_modifier(*circumstances: str) -> int:
    """Sum the SRD modifiers for the named circumstances.

    Raises :class:`AttackImpossibleError` for an ``N/A`` circumstance and ``KeyError`` for an
    unknown id, so a typo cannot silently become a zero modifier.
    """
    return sum(_modifier_for(circumstance) for circumstance in circumstances)


def attack_modifier_for(circumstances: Iterable[str]) -> int:
    """Iterable form of :func:`attack_modifier`."""
    return attack_modifier(*circumstances)


def _modifier_for(circumstance: str) -> int:
    if circumstance in IMPOSSIBLE_CIRCUMSTANCES:
        raise AttackImpossibleError(IMPOSSIBLE_CIRCUMSTANCES[circumstance])
    if circumstance not in ATTACK_MODIFIER_TABLE:
        raise KeyError(f"unknown attack circumstance {circumstance!r}")
    return ATTACK_MODIFIER_TABLE[circumstance]


def in_melee_penalty(handedness: str) -> int:
    """The penalty for firing while an enemy is in melee range.

    One-handed guns and thrown weapons take ``-4``; two-handed guns cannot be fired at all.
    """
    if handedness not in RANGED_HANDEDNESS:
        raise ValueError(f"handedness must be one of {RANGED_HANDEDNESS}, got {handedness!r}")
    if handedness == "two_handed":
        raise AttackImpossibleError(IMPOSSIBLE_CIRCUMSTANCES["two_handed_gun_in_melee"])
    return ATTACK_MODIFIER_TABLE[
        "thrown_while_in_melee" if handedness == "thrown" else "one_handed_gun_in_melee"
    ]
