"""CWN 6.2.8 — spirit powers catalogue (issue #1068).

Transcribed from the CWN SRD: name, cost in spirit points, and the effect as the book states it. Cost feeds the
summoning cost in `cwn_summoning.effort_cost`, where the number of powers is what the summoner pays for.
"""
from __future__ import annotations

import json
from pathlib import Path

CATALOGUE = Path(__file__).resolve().parents[2] / "data/rules/cwn/spirit_powers.json"


class SpiritPowerError(ValueError):
    """A rule was about to be broken."""


def load_powers(path: str | Path | None = None) -> list[dict]:
    data = json.loads(Path(path or CATALOGUE).read_text(encoding="utf-8"))
    powers = data["powers"]
    seen = set()
    for power in powers:
        if power["cost"] < 0:
            raise SpiritPowerError(f"{power['name']}: negative cost")
        if power["name"] in seen:
            raise SpiritPowerError(f"duplicate power {power['name']!r}")
        seen.add(power["name"])
    return powers


POWERS = {p["name"]: p for p in load_powers()}


def power(name: str) -> dict:
    try:
        return POWERS[name]
    except KeyError:
        raise SpiritPowerError(f"unknown spirit power {name!r}") from None


def total_cost(names: list[str]) -> int:
    """Sum of the listed powers' costs — the figure that becomes the summoning Effort cost."""
    return sum(power(n)["cost"] for n in names)


def max_power_level_requirement(names: list[str]) -> int:
    """Powers whose cost is high enough to require a minimum character level (book notes per power)."""
    return max((power(n)["cost"] for n in names), default=0)
