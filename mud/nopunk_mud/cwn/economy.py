"""Daily wages, and what a hireling will and will not do.

From the Cities Without Number SRD (public domain), Common Wages: average daily earnings by worker type,
with the SRD's own caveat — a hireling is loyal within reason, not suicidal.

The table and the lookup are **not** implemented here: ``rules.cwn_lifestyles`` owns them, over
``data/rules/cwn/common_wages.json``. This module used to read that file itself, which made it the third
copy of one SRD section; it now delegates and keeps only what is genuinely MUD-side — the prose about
what a hireling will risk, and the budget arithmetic a MUD needs.
"""
from __future__ import annotations

try:  # imported as part of the repository (CWD or repo root on sys.path)
    from src.rules.cwn_lifestyles import COMMON_WAGES, LifestyleError, wage
except ModuleNotFoundError:  # pragma: no cover - installed package layout
    from rules.cwn_lifestyles import COMMON_WAGES, LifestyleError, wage

#: How far a hireling will go. Descriptive, not a morale score: CWN has its own reaction rolls.
RESOLVE: dict[str, str] = {
    "ordinary": "does the job; will not risk their life",
    "bodyguard": "defends the employer; only the best stay under overwhelming opposition",
    "ganger": "will commit extreme violence against rivals or the helpless; avoids a fair fight",
}

#: Short MUD names mapped onto the SRD wage table's own ids, so a MUD script can say "bodyguard".
ROLE_ALIASES: dict[str, str] = {
    "ordinary": "common_streetwalker",
    "bodyguard": "competent_street_bodyguard",
    "ganger": "low_level_ganger_or_street_thug",
}


class WageError(ValueError):
    """An unknown role, or a wage question the table cannot answer."""


def wages() -> dict[str, int]:
    return dict(COMMON_WAGES)


def daily_wage(role: str) -> int:
    try:
        return wage(ROLE_ALIASES.get(role, role))
    except LifestyleError as exc:
        raise WageError(str(exc)) from exc


def hire_cost(role: str, days: int) -> int:
    if days < 1:
        raise WageError("hire for at least one day")
    return daily_wage(role) * days


def affordable_hirelings(budget: int, role: str, days: int) -> int:
    if budget < 0:
        raise WageError("budget cannot be negative")
    cost = hire_cost(role, days)
    return budget // cost if cost else 0
