"""Daily wages, and what a hireling will and will not do (#1068).

From the Cities Without Number SRD (public domain), Common Wages: average daily earnings by worker type,
with the SRD's own caveat — a hireling is loyal within reason, not suicidal.
"""
from __future__ import annotations

import json
from pathlib import Path

WAGES_PATH = Path(__file__).resolve().parents[3] / "data" / "rules" / "cwn" / "common_wages.json"

#: How far a hireling will go. Descriptive, not a morale score: CWN has its own reaction rolls.
RESOLVE: dict[str, str] = {
    "ordinary": "does the job; will not risk their life",
    "bodyguard": "defends the employer; only the best stay under overwhelming opposition",
    "ganger": "will commit extreme violence against rivals or the helpless; avoids a fair fight",
}


class WageError(ValueError):
    """An unknown role, or a wage question the table cannot answer."""


def wages() -> dict[str, int]:
    return dict(json.loads(WAGES_PATH.read_text(encoding="utf-8"))["wages"])


def daily_wage(role: str) -> int:
    table = wages()
    if role not in table:
        raise WageError(f"no wage for {role!r}; known roles: {len(table)}")
    return table[role]


def hire_cost(role: str, days: int) -> int:
    if days < 1:
        raise WageError("hire for at least one day")
    return daily_wage(role) * days


def affordable_hirelings(budget: int, role: str, days: int) -> int:
    if budget < 0:
        raise WageError("budget cannot be negative")
    cost = hire_cost(role, days)
    return budget // cost if cost else 0
