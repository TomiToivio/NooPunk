"""Chases and pursuit, on foot and in vehicles (#1068).

From the Cities Without Number SRD (public domain), Chases and Pursuit:

* The fleeing side's pace is one skill check (Dex/Exert or Con/Exert), the best member rolling for the
  group; helpers can add up to +3.
* Pursuers roll once (foot) or per vehicle, modified by the situation table; meeting or beating the pace
  catches up, otherwise the quarry is away.
* Vehicle chases use Drive instead of Exert, and each pursuing vehicle is resolved separately.

Deterministic: totals are passed in.
"""
from __future__ import annotations

FOOT_PURSUIT_MODIFIERS: dict[str, int] = {
    "more_pursuers_than_pursued": -1,
    "no_head_start": 2,
    "one_round_head_start": 1,
    "under_a_minute_head_start": 0,
    "over_a_minute_head_start": -2,
    "half_hearted": -1,
    "enraged": 1,
}

VEHICLE_PURSUIT_MODIFIERS: dict[str, int] = {
    "cannot_see_pursued": -2,
    "pursuer_flying": 3,
    "pursued_flying": -3,
}

MAX_HELPER_BONUS = 3


class ChaseError(ValueError):
    """A chase the rules do not describe: unknown modifier, impossible head start."""


def helper_bonus(helpers: int) -> int:
    """Each successful hindrance adds +1, to a maximum of +3."""
    if helpers < 0:
        raise ChaseError("helpers cannot be negative")
    return min(helpers, MAX_HELPER_BONUS)


def foot_pace(*, best_total: int, successful_helpers: int = 0, botched_helpers: int = 0) -> int:
    return best_total + helper_bonus(successful_helpers) - botched_helpers


def foot_pursuit(
    *,
    pursuer_total: int,
    pace: int,
    situations: list[str] | None = None,
    terrain_advantage: int = 0,
) -> dict[str, object]:
    """One pursuit check. Terrain swings -2..+2 and is passed explicitly, not guessed."""
    if not -2 <= terrain_advantage <= 2:
        raise ChaseError("terrain advantage is -2..+2")
    total = pursuer_total + terrain_advantage
    for name in situations or []:
        if name not in FOOT_PURSUIT_MODIFIERS:
            raise ChaseError(f"unknown pursuit situation {name!r}")
        total += FOOT_PURSUIT_MODIFIERS[name]
    return {"caught": total >= pace, "total": total, "pace": pace}


def vehicle_pursuit(
    *,
    pursuer_total: int,
    pace: int,
    situations: list[str] | None = None,
) -> dict[str, object]:
    total = pursuer_total
    for name in situations or []:
        if name not in VEHICLE_PURSUIT_MODIFIERS:
            raise ChaseError(f"unknown vehicle situation {name!r}")
        total += VEHICLE_PURSUIT_MODIFIERS[name]
    return {"caught": total >= pace, "total": total, "pace": pace}


def resolve_vehicle_chase(*, pace: int, pursuers: dict[str, int]) -> dict[str, object]:
    """Each pursuing vehicle is resolved on its own; the ones that miss fall out of the chase."""
    caught = {name: total >= pace for name, total in pursuers.items()}
    return {
        "pace": pace,
        "caught": sorted(name for name, hit in caught.items() if hit),
        "lost": sorted(name for name, hit in caught.items() if not hit),
    }
