"""CWN: lifestyle costs, common wages and bribe costs (SRD "Lifestyles, Wages and Bribes").

**One table, one home.** The numbers live in `data/rules/cwn/{lifestyles,common_wages,bribe_costs}.json`
— the same files the MUD adapter reads — and this module is the only procedure that turns them into
answers. Three parallel copies of this SRD section existed after a burst of parallel agent work on #1068:
an embedded table here, the JSON catalogues, and a separate reader in `mud/nopunk_mud/cwn/economy.py`.
They now share one source, and `tests/test_rule_duplication_merged.py` fails if a fourth copy appears.

The System Strain side of a lifestyle already lives in :mod:`cwn_core` (``LIFESTYLE_STRAIN``, which feeds
``strain_maximum``); this module reuses it and only maps the SRD's ``middle_class`` id onto the core's
``ordinary`` key rather than restating the modifiers.

Sources: https://cwn.quadrifons.com/gear-vehicles-cyberware/lifestyles-wages-and-bribes/
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final

from .cwn_core import LIFESTYLE_STRAIN, CwnError

__all__ = [
    "BRIBE_MULTIPLES",
    "COMMON_WAGES",
    "LIFESTYLE_ALIASES",
    "LIFESTYLE_COSTS",
    "LifestyleError",
    "bribe_cost",
    "bribe_needs_more_than_cash",
    "living_cost",
    "strain_modifier",
    "wage",
]

DATA = Path(__file__).resolve().parents[2] / "data" / "rules" / "cwn"

#: The SRD names the middle tier ``middle_class``; ``cwn_core.LIFESTYLE_STRAIN`` calls it ``ordinary``.
#: One tier, two vocabularies, mapped here so neither module restates the other's table.
LIFESTYLE_ALIASES: Final[dict[str, str]] = {"middle_class": "ordinary"}


class LifestyleError(CwnError):
    """Unknown lifestyle, worker or favour, or a table that cannot be read."""


def _load(name: str) -> dict:
    path = DATA / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:  # pragma: no cover - a missing data file is a broken checkout
        raise LifestyleError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise LifestyleError(f"{path} is not valid JSON: {exc}") from exc


_LIFESTYLE_LEVELS = _load("lifestyles.json")["levels"]

#: Cost per month, in credits, for each lifestyle the SRD lists.
LIFESTYLE_COSTS: Final[dict[str, int]] = {
    str(level["id"]): int(level["monthly_cost"]) for level in _LIFESTYLE_LEVELS}

#: The same rows' maximum-System-Strain modifiers, kept only to check the SRD against cwn_core.
_SRD_STRAIN: Final[dict[str, int]] = {
    str(level["id"]): int(level["max_strain_modifier"]) for level in _LIFESTYLE_LEVELS}

#: Average daily earnings by worker type.
COMMON_WAGES: Final[dict[str, int]] = {
    str(role): int(value) for role, value in _load("common_wages.json")["wages"].items()}

#: Favour -> (multiple of the target's daily wage, serious risk).
BRIBE_MULTIPLES: Final[dict[str, tuple[int, bool]]] = {
    str(row["id"]): (int(row["multiple"]), bool(row["serious"]))
    for row in _load("bribe_costs.json")["favours"]}


def _data_key(lifestyle: str) -> str:
    """Accept either vocabulary; the data files use the SRD's own ids."""
    if lifestyle == "ordinary":
        return "middle_class"
    return lifestyle


def _core_key(lifestyle: str) -> str:
    return LIFESTYLE_ALIASES.get(lifestyle, lifestyle)


def living_cost(lifestyle: str) -> int:
    """Monthly cost of a lifestyle, in credits."""
    key = _data_key(lifestyle)
    try:
        return LIFESTYLE_COSTS[key]
    except KeyError:
        raise LifestyleError(
            f"unknown lifestyle {lifestyle!r}; expected one of {sorted(LIFESTYLE_COSTS)}"
        ) from None


def strain_modifier(lifestyle: str) -> int:
    """The maximum-System-Strain modifier that applies while living that way."""
    key = _core_key(lifestyle)
    try:
        return LIFESTYLE_STRAIN[key]
    except KeyError:
        raise LifestyleError(
            f"unknown lifestyle {lifestyle!r}; expected one of {sorted(LIFESTYLE_COSTS)}"
        ) from None


def wage(worker: str) -> int:
    """Average daily earnings for a worker type, in credits."""
    try:
        return COMMON_WAGES[worker]
    except KeyError:
        raise LifestyleError(
            f"unknown worker type {worker!r}; expected one of {sorted(COMMON_WAGES)}"
        ) from None


def bribe_cost(favour: str, *, daily_wage: int) -> int:
    """What a favour costs, given the target's daily wage.

    The SRD expresses bribes as a multiple of the target's daily wage, "as it costs more to bribe a
    manager than a janitor". Like or dislike for the party can move the price; that is a GM decision
    and is deliberately not a parameter here.
    """
    try:
        multiple, _serious = BRIBE_MULTIPLES[favour]
    except KeyError:
        raise LifestyleError(
            f"unknown favour {favour!r}; expected one of {sorted(BRIBE_MULTIPLES)}"
        ) from None
    if daily_wage < 0:
        raise LifestyleError("a daily wage cannot be negative")
    return multiple * daily_wage


def bribe_needs_more_than_cash(favour: str) -> bool:
    """Whether the SRD marks this favour as a serious risk needing more than money."""
    try:
        return BRIBE_MULTIPLES[favour][1]
    except KeyError:
        raise LifestyleError(
            f"unknown favour {favour!r}; expected one of {sorted(BRIBE_MULTIPLES)}"
        ) from None
