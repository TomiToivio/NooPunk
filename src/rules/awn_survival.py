"""Ashes Without Number: the crisis-zone survival layer (travel, supplies, privation).

NoöPunk is not a uniform post-apocalypse — ``RULEBOOK.md`` §33.1 and §33.28 keep
Earth populated and politically central, with damage that is severe but *uneven*.
This module therefore models a **local crisis pocket**, not a world state: one
terrain, one day's supplies, one night's shelter, and the System Strain that a
shortage actually costs.

Transcribed procedure from **Ashes Without Number** (2025 free edition). AWN has
no verified open licence, so this is a re-expression of the mechanics in original
wording — no source sentence or table heading is reproduced
(``docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md``). The contract is
``data/rules/awn_survival.json``.

## It feeds CWN, it does not replace it

Privation produces **System Strain**, which ``src/rules/cwn_strain.py`` already
governs, and shortages block the natural healing ``src/rules/cwn_healing.py``
already computes. There is no parallel wound track, no separate hunger stat and
no new save category here.

## What is deliberately absent

The source's forage-difficulty-by-terrain table was **not transcribed**. Rather
than invent numbers for it, :func:`forage` takes the difficulty from the caller
and the gap is recorded in the contract (``foraging.difficulty_table_transcribed``).
"""

from __future__ import annotations

import json
import random
from collections.abc import Mapping
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

SURVIVAL_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "awn_survival.json"

TravelMode = Literal["walking", "vehicular"]
Privation = Literal[
    "first_day_without_food",
    "consecutive_day_without_food",
    "first_day_without_water",
    "consecutive_day_without_water",
    "night_without_adequate_shelter",
    "harsh_night_without_shelter",
]


class SurvivalError(ValueError):
    """A terrain, mode or privation the contract does not define."""


@lru_cache(maxsize=2)
def load_survival(path: str | Path | None = None) -> dict[str, Any]:
    return json.loads(Path(path or SURVIVAL_PATH).read_text(encoding="utf-8"))


def terrain(terrain_id: str) -> Mapping[str, Any]:
    for row in load_survival()["travel"]["terrain"]:
        if row["id"] == terrain_id:
            return row
    raise SurvivalError(f"unknown terrain: {terrain_id}")


def terrains() -> dict[str, Mapping[str, Any]]:
    return {row["id"]: row for row in load_survival()["travel"]["terrain"]}


# --------------------------------------------------------------------------- #
# Travel
# --------------------------------------------------------------------------- #


def travel_hours(terrain_id: str, *, mode: TravelMode = "walking", road: bool = False) -> float:
    """Hours to enter one hex. Vehicles cannot cross the worst terrain without a road.

    A road halves walking time to a minimum of one hour and gives vehicles a flat
    one hour. A forced march lengthens the *day*, not the hex — see
    :func:`travel_day_hours`.
    """
    rules = load_survival()["travel"]
    row = terrain(terrain_id)
    if mode == "walking":
        hours = float(row["walking_hours"])
        if road:
            hours = max(float(rules["road_minimum_hours"]), hours * float(rules["road_walking_multiplier"]))
    elif mode == "vehicular":
        raw = row["vehicular_hours"]
        if raw is None and not road:
            raise SurvivalError(f"{row['label']}: a ground vehicle needs a road to cross")
        hours = float(rules["road_vehicular_minimum_hours"]) if raw is None or road else float(raw)
    else:
        raise SurvivalError(f"unknown travel mode: {mode}")
    return hours


def travel_day_hours(*, forced_march: bool = False) -> float:
    rules = load_survival()["travel"]
    hours = float(rules["travel_hours_per_day"])
    if forced_march:
        hours += float(rules["forced_march_hours"])
    return hours


def hexes_per_day(terrain_id: str, *, mode: TravelMode = "walking", road: bool = False,
                  forced_march: bool = False) -> int:
    per_hex = travel_hours(terrain_id, mode=mode, road=road)
    return int(travel_day_hours(forced_march=forced_march) // per_hex)


def is_exposed(*, driving: bool = False, forced_march: bool = False) -> bool:
    """Driving, road marching in a hurry or a forced march all forfeit stealthy travel."""
    return driving or forced_march


def encounter_check(die: int) -> bool:
    """One d8 per travel day; an encounter on 1 or less. Exposed parties are found first."""
    rules = load_survival()["travel"]
    if not 1 <= int(die) <= int(rules["astray_die"]):
        raise SurvivalError("the encounter die is a d8")
    return int(die) <= int(rules["astray_encounter_on_or_below"])


def scouting_days(terrain_id: str) -> int:
    """How long it takes to turn a hex from crossed to Scouted."""
    return int(terrain(terrain_id)["scouting_days"])


def going_astray_difficulty(terrain_id: str, *, scouted: bool = False, road: bool = False) -> int | None:
    """No check on a scouted hex, a road, or terrain that offers no way to be lost."""
    if scouted or road:
        return None
    return terrain(terrain_id)["astray_difficulty"]


def goes_astray(*, check_total: int, terrain_id: str, scouted: bool = False, road: bool = False) -> bool:
    difficulty = going_astray_difficulty(terrain_id, scouted=scouted, road=road)
    if difficulty is None:
        return False
    return int(check_total) < int(difficulty)


# --------------------------------------------------------------------------- #
# Supplies and privation
# --------------------------------------------------------------------------- #


def food_encumbrance(days: int, *, travel_rations: bool = False) -> int:
    """One Encumbrance per person-day, or four per week of packed travel rations."""
    if days < 0:
        raise SurvivalError("days cannot be negative")
    if travel_rations:
        return -(-days // 7) * int(load_survival()["supplies"]["travel_rations_week_encumbrance"])
    return days * int(load_survival()["supplies"]["food_encumbrance_per_day"])


def privation_strain(kind: Privation) -> int:
    table = load_survival()["privation"]
    if kind not in table:
        raise SurvivalError(f"unknown privation: {kind}")
    return int(table[kind])


@dataclass(frozen=True)
class PrivationResult:
    current_strain: int
    maximum_strain: int
    gained: int

    @property
    def over_maximum(self) -> bool:
        return self.current_strain > self.maximum_strain

    @property
    def needs_physical_save(self) -> bool:
        return self.over_maximum

    @property
    def recovery_blocked(self) -> bool:
        return self.gained > 0 or bool(load_survival()["privation"]["blocks_recovery"])


def apply_privation(current_strain: int, maximum_strain: int, kind: Privation) -> PrivationResult:
    """Privation adds System Strain; crossing the maximum forces a Physical save.

    The save is *reported*, never rolled here: a caller with a seed rolls it, so
    the kernel stays deterministic. A success leaves the character helpless until
    rescued, which is a condition, not a number.
    """
    if maximum_strain <= 0:
        raise SurvivalError("maximum System Strain must be positive")
    return PrivationResult(
        current_strain=int(current_strain) + privation_strain(kind),
        maximum_strain=int(maximum_strain),
        gained=privation_strain(kind),
    )


def starvation_death_save_needed(result: PrivationResult) -> bool:
    return result.needs_physical_save


# --------------------------------------------------------------------------- #
# Foraging
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ForageResult:
    success: bool
    units: int
    check_total: int
    difficulty: int


def forage(
    check_total: int,
    difficulty: int,
    *,
    survive_levels: int = -1,
    rng: Any = None,
    die: int | None = None,
) -> ForageResult:
    """A successful WIS/Survive check yields ``1d6 + group Survive levels``, capped at 10.

    ``survive_levels=-1`` means nobody in the group has Survive at all, which
    subtracts one from the unit count with a floor of one.
    """
    rules = load_survival()["foraging"]
    if check_total < difficulty:
        return ForageResult(False, 0, int(check_total), int(difficulty))
    if die is None:
        roller = rng if rng is not None else random.Random()
        face = roller.randint(1, 6)
    else:
        face = int(die)
    if not 1 <= face <= 6:
        raise SurvivalError("the forage die is a d6")
    units = face
    if rules["add_survive_levels"]:
        units += survive_levels if survive_levels >= 0 else int(rules["untrained_penalty"])
    units = min(int(rules["maximum_units"]), units)
    if survive_levels < 0:
        units = max(int(rules["minimum_units"]), units)
    return ForageResult(True, units, int(check_total), int(difficulty))


__all__ = [
    "SURVIVAL_PATH",
    "ForageResult",
    "Privation",
    "PrivationResult",
    "SurvivalError",
    "TravelMode",
    "apply_privation",
    "encounter_check",
    "food_encumbrance",
    "forage",
    "goes_astray",
    "going_astray_difficulty",
    "hexes_per_day",
    "is_exposed",
    "load_survival",
    "privation_strain",
    "scouting_days",
    "starvation_death_save_needed",
    "terrain",
    "terrains",
    "travel_day_hours",
    "travel_hours",
]
