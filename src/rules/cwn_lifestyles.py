"""CWN: lifestyle costs, common wages and bribe costs (SRD 3.8).

The System Strain side of a lifestyle already lives in :mod:`cwn_core` (``LIFESTYLE_STRAIN``), because
it modifies ``strain_maximum``. This module adds the money side and **reuses** that table instead of
keeping a second copy that could drift from it:

* ``LIFESTYLE_COSTS``  — cost per month for each lifestyle (SRD "Lifestyle Costs");
* ``COMMON_WAGES``     — average daily earnings per worker type (SRD "Common Wages");
* ``BRIBE_MULTIPLES``  — bribe price as a multiple of the target's daily wage (SRD "Bribe Costs").

Values are the Free Edition SRD's own numbers. Nothing here invents a rule: where the SRD gives a
range or a "GM's discretion" clause, that is recorded in the note rather than turned into a formula.

Sources: https://cwn.quadrifons.com/gear-vehicles-cyberware/lifestyles-wages-and-bribes/
"""

from __future__ import annotations

from typing import Final

from .cwn_core import LIFESTYLE_STRAIN, CwnError

__all__ = [
    "BRIBE_MULTIPLES",
    "COMMON_WAGES",
    "LIFESTYLE_COSTS",
    "LifestyleError",
    "bribe_cost",
    "living_cost",
    "strain_modifier",
    "wage",
]


class LifestyleError(CwnError):
    """Unknown lifestyle, worker or favour."""


#: Cost per month, in credits, for each lifestyle the SRD lists. The keys are the same as
#: ``cwn_core.LIFESTYLE_STRAIN``; a test asserts the two tables stay key-compatible.
LIFESTYLE_COSTS: Final[dict[str, int]] = {
    "squatter": 0,
    "slum": 300,
    "ordinary": 1_000,
    "fine": 5_000,
    "luxury": 20_000,
}

#: Average daily earnings, in credits. Hireling loyalty is prose in the SRD, not a number; it is not
#: modelled here.
COMMON_WAGES: Final[dict[str, int]] = {
    "unskilled_labourer": 10,
    "low_level_ganger": 15,
    "streetwalker": 20,
    "street_stall_merchant": 25,
    "entry_level_corp_worker": 30,
    "low_level_corp_lifer": 40,
    "street_tech_or_cyberdoc": 50,
    "street_bodyguard": 50,
    "street_cop_or_skilled_corp_worker": 100,
    "professional_companion": 200,
    "corp_hacker": 200,
    "corp_middle_manager": 250,
    "corp_cyberdoc": 250,
    "elite_bodyguard": 500,
    "gang_boss": 750,
    "corp_branch_manager": 1_000,
    "high_ranking_corp_exec": 5_000,
    "oligarchic_elite": 10_000,
}

#: Bribe price as a multiple of the target's daily wage. ``serious`` marks the favours the SRD flags
#: with an asterisk: many NPCs will want more than cash before agreeing.
BRIBE_MULTIPLES: Final[dict[str, tuple[int, bool]]] = {
    "look_the_other_way_minor": (2, False),
    "pass_out_information": (2, False),
    "small_favour_within_authority": (5, False),
    "blind_eye_when_it_might_trouble": (14, True),
    "blind_eye_when_it_will_trouble": (60, True),
    "favour_with_minor_backlash": (30, True),
    "favour_that_might_get_them_punished": (90, True),
    "favour_that_might_get_them_fired": (180, True),
}


def living_cost(lifestyle: str) -> int:
    """Monthly cost of a lifestyle, in credits."""
    try:
        return LIFESTYLE_COSTS[lifestyle]
    except KeyError:
        raise LifestyleError(
            f"unknown lifestyle {lifestyle!r}; expected one of {sorted(LIFESTYLE_COSTS)}"
        ) from None


def strain_modifier(lifestyle: str) -> int:
    """The maximum-System-Strain modifier that applies while living that way."""
    try:
        return LIFESTYLE_STRAIN[lifestyle]
    except KeyError:
        raise LifestyleError(
            f"unknown lifestyle {lifestyle!r}; expected one of {sorted(LIFESTYLE_STRAIN)}"
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
