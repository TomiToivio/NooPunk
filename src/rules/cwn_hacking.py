"""Cities Without Number: hacking — Access, security, connection and the alert clock.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``):

* ``hacking/cyberspace-basics/#access`` — what Access is and how a deck refreshes it;
* ``hacking/cyberspace-basics/#connecting-to-cyberspace`` — the cable, the wireless link and the VR
  crown, with their penalties;
* ``hacking/hacking-mechanics/#common-cyberspace-security-levels`` — the 7–12 ladder and its
  situation modifiers;
* ``hacking/hacking-mechanics/#hacking-a-device-or-server`` — the run-a-program procedure, and the
  rule that **every two failed checks count as one Alert the Network action**;
* ``hacking/hacking-mechanics/#hacking-cyberware-or-drones`` — ``7 + ceil(HD or level / 3)``, and 8
  for a drone with no operator.

## The two things this module refuses to flatten

**Access is a pool, not a bonus.** It is spent to run a Verb and refreshed by an hour of deck work,
once a day. A module that folded it into the roll would make the deck's Bonus Access meaningless and
delete the reason to prepare.

**Connection penalties are not circumstances.** The wireless link (−2) and the VR crown (−1) stack, so
a wireless-plus-crown hack is at −3. The skill-check bound of −2..+2 covers *circumstances*; routing
these through it would silently swallow a point. They are therefore passed as flat modifiers, the same
distinction :class:`rules.wn_core.Check` records in ``misc``.

## What this module deliberately does not model

Verbs, Subjects, programs, CPU slots, demons and watchdogs are catalogue content, not procedure: a Verb
is a row with a cost, an Access cost and a check modifier. :func:`hacking_check` takes that modifier as
an argument rather than shipping a table the author has not ruled on. The network's node graph is
scenario state, not a rules object.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .wn_core import attribute_modifier

#: SRD: the recorded security ladder. Anything between these values is a referee's call, not this file's.
SECURITY_LEVELS: dict[int, str] = {
    7: "private home network",
    8: "small business, minor gang or minor government office",
    9: "corp branch office, major gang or important government facility",
    10: "corp high-security network",
    12: "corp or government black site",
}

#: SRD: a wireless link applies -2 to all cyberspace skill checks, and cannot leave the entry node.
WIRELESS_PENALTY = -2
#: SRD: a VR crown instead of a cranial jack applies a further -1.
VR_CROWN_PENALTY = -1
#: SRD: "every two failed skill checks against network Security count as one triggering".
FAILURES_PER_ALERT = 2
#: SRD: the Alert the Network action must be taken twice, possibly rounds or nodes apart.
ALERT_ACTIONS_TO_ALERT = 2
#: SRD: a drone without a connected operator is difficulty 8.
UNOPERATED_DRONE_DIFFICULTY = 8
#: SRD: the referee's judgement of the network's tech quality, and what an informant buys.
#: Both are magnitudes the *caller* supplies; the ranges are declared here so the Godot kernel in
#: `godot/core/cwn_hacking.gd` clamps them identically instead of inventing its own bounds.
TECH_QUALITY_RANGE = (-2, 2)
INSIDE_INFORMATION_RANGE = (1, 3)


class HackError(ValueError):
    """A constraint from the SRD was about to be violated."""


def access_pool(*, intelligence_modifier: int, program_skill: int, deck_bonus: int = 0) -> int:
    """``INT modifier + Program + the deck's Bonus Access``. Never negative.

    The pool is refreshed by an hour of reprogramming, once a day — the caller owns the clock.
    """
    if program_skill < 0:
        raise HackError(f"Program skill cannot be negative, got {program_skill}")
    return max(0, int(intelligence_modifier) + int(program_skill) + int(deck_bonus))


def security_difficulty(
    security: int,
    *,
    alerted: bool = False,
    important_device: bool = False,
    tech_quality: int = 0,
    inside_info: int = 0,
) -> int:
    """The network's security level plus the SRD's situation modifiers.

    ``tech_quality`` is the referee's −2..+2; ``inside_info`` is the positive 1..3 an informant
    buys, which *lowers* the target. Both are clamped to their declared range, because a value
    outside it is a caller error that would otherwise silently move the difficulty.
    """
    if security not in SECURITY_LEVELS:
        raise HackError(f"{security} is not a recorded security level; expected {sorted(SECURITY_LEVELS)}")
    difficulty = int(security)
    difficulty += 1 if alerted else 0
    difficulty += 1 if important_device else 0
    difficulty += max(TECH_QUALITY_RANGE[0], min(TECH_QUALITY_RANGE[1], int(tech_quality)))
    if inside_info:
        difficulty -= max(INSIDE_INFORMATION_RANGE[0], min(INSIDE_INFORMATION_RANGE[1], int(inside_info)))
    return difficulty


def cyberware_difficulty(*, level_or_hit_dice: int, has_operator: bool = True) -> int:
    """``7 + ceil(HD or level / 3)``; a drone with no connected operator is difficulty 8."""
    if not has_operator:
        return UNOPERATED_DRONE_DIFFICULTY
    if level_or_hit_dice < 1:
        raise HackError(f"level or hit dice must be positive, got {level_or_hit_dice}")
    return 7 + (int(level_or_hit_dice) + 2) // 3


@dataclass(frozen=True)
class HackCheck:
    """One Int/Program check behind a Verb."""

    dice: tuple[int, int]
    attribute_modifier: int
    program_skill: int
    untrained: bool
    verb_modifier: int
    connection_penalty: int
    situational: int
    difficulty: int

    @property
    def total(self) -> int:
        return (sum(self.dice) + self.attribute_modifier + self.program_skill
                + self.verb_modifier + self.connection_penalty + self.situational
                - (1 if self.untrained else 0))

    @property
    def success(self) -> bool:
        return self.total >= self.difficulty


def hacking_check(
    *,
    intelligence_score: int,
    program_skill: int | None,
    difficulty: int,
    wireless: bool = False,
    vr_crown: bool = False,
    verb_modifier: int = 0,
    situational: int = 0,
    rng: Any = None,
    dice: tuple[int, int] | None = None,
) -> HackCheck:
    """Roll the check a run-program action needs, with the connection penalties kept flat."""
    if situational < -2 or situational > 2:
        # The kernel's bound is a rule, not a suggestion; clamp rather than raise, as it does.
        situational = max(-2, min(2, situational))
    source = rng
    if dice is None:
        if source is None:
            import random as _random
            source = _random.Random()
        faces = (source.randint(1, 6), source.randint(1, 6))
    else:
        faces = (int(dice[0]), int(dice[1]))
        if any(not 1 <= face <= 6 for face in faces):
            raise HackError(f"each die is 1..6, got {dice}")
    untrained = program_skill is None
    skill_level = 0 if untrained else int(program_skill)
    if skill_level < 0:
        raise HackError(f"Program skill cannot be negative, got {program_skill}")
    penalty = (WIRELESS_PENALTY if wireless else 0) + (VR_CROWN_PENALTY if vr_crown else 0)
    return HackCheck(
        dice=faces,
        attribute_modifier=attribute_modifier(intelligence_score),
        program_skill=skill_level,
        untrained=untrained,
        verb_modifier=int(verb_modifier),
        connection_penalty=penalty,
        situational=situational,
        difficulty=int(difficulty),
    )


@dataclass
class AlertClock:
    """The network's intruder clock: two failed checks per Alert action, two actions to alert."""

    failures: int = 0
    alert_actions: int = 0
    _pending: bool = field(default=False, repr=False)

    def record_failure(self) -> bool:
        """Record a failed check. True when this failure completes the network alert."""
        self.failures += 1
        if self.failures % FAILURES_PER_ALERT == 0:
            self.alert_actions += 1
        return self.alerted

    def record_alert_action(self) -> bool:
        """A demon or watchdog spent its Main action alerting. True when the network is alerted."""
        self.alert_actions += 1
        return self.alerted

    @property
    def alerted(self) -> bool:
        return self.alert_actions >= ALERT_ACTIONS_TO_ALERT


__all__ = [
    "ALERT_ACTIONS_TO_ALERT",
    "FAILURES_PER_ALERT",
    "INSIDE_INFORMATION_RANGE",
    "SECURITY_LEVELS",
    "TECH_QUALITY_RANGE",
    "UNOPERATED_DRONE_DIFFICULTY",
    "VR_CROWN_PENALTY",
    "WIRELESS_PENALTY",
    "AlertClock",
    "HackCheck",
    "HackError",
    "access_pool",
    "cyberware_difficulty",
    "hacking_check",
    "security_difficulty",
]
