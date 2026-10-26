"""Worlds Without Number: Major Projects — the campaign-scale goal procedure.

A major project is the answer to "the party wants to change the world and no
single act will do it". Its cost is measured in **Renown**, and its difficulty is
a product of three judgements — plausibility, scope, and the greatest active
opposition — plus a doubling when the affected population is against the change.

Transcribed procedure from **Worlds Without Number** (CC0). Numbers live in
``data/rules/wwn_projects.json``; this module is arithmetic over that contract.

## Why this is not the SWN faction turn

``src/rules/swn_faction_turn.py`` models what *organisations* do with assets.
This models what the *party* wants and what it costs in standing. The baseline
keeps them separate on purpose (``rulebook/WITHOUT_NUMBER_BASELINE.md`` §6): a
faction that helps a project supplies a share of Renown, it does not spend
faction Treasure, and a project that damages a faction's Asset does so in the
fiction rather than by double-counting a second currency.

## The one thing this module refuses to do

The source prices purchased Renown on an escalating money ladder. That table was
not transcribed, so :func:`money_purchase_is_modelled` returns ``False`` and no
function invents a price. A caller that wants cash-for-progress must supply the
referee's own ladder; silently guessing would be an unauthored rule.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

PROJECTS_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "wwn_projects.json"

Probability = Literal["plausible", "improbable", "impossible"]
Scope = Literal["village", "city", "region", "kingdom", "known_world"]
Opposition = Literal["none", "minor_figures", "local_leaders", "major_noble_or_famed_beast",
                     "king_or_legendary_power"]


class ProjectError(ValueError):
    """A project was described with a key the contract does not define."""


@lru_cache(maxsize=2)
def load_projects(path: str | Path | None = None) -> dict[str, Any]:
    return json.loads(Path(path or PROJECTS_PATH).read_text(encoding="utf-8"))


def money_purchase_is_modelled() -> bool:
    """``False``: the source's money-per-Renown ladder was not transcribed."""
    return False


def project_difficulty(
    probability: Probability,
    scope: Scope,
    opposition: Opposition = "none",
    *,
    disapproval: bool = False,
    permanent: bool = False,
) -> int:
    """Renown needed to make the change happen.

    ``permanent`` is the source's clause for a magical working fixed forever, which
    multiplies the working's own cost fourfold. It is offered because NoöPunk has
    noetic workings; it is not applied to ordinary institutional change.
    """
    rules = load_projects()
    try:
        base = int(rules["probability"][probability])
        multiplier = int(rules["scope"][scope])
        opposed = int(rules["opposition"][opposition])
    except KeyError as exc:
        raise ProjectError(f"unknown project key: {exc.args[0]}") from exc
    difficulty = base * multiplier * opposed
    if disapproval:
        difficulty *= int(rules["disapproval_multiplier"])
    if permanent:
        difficulty *= int(rules["renown"]["permanent_working_multiplier"])
    return difficulty


def renown_after_adventures(adventures: int, *, starting: int = 0) -> int:
    """One point per adventure, plus whatever the character already had."""
    if adventures < 0 or starting < 0:
        raise ProjectError("adventure and Renown counts cannot be negative")
    return starting + adventures * int(load_projects()["renown"]["per_adventure"])


def adventure_share(difficulty: int, *, adventures_planned: int) -> int:
    """The share of a goal one relevant adventure is worth, rounded up."""
    if difficulty < 0:
        raise ProjectError("difficulty cannot be negative")
    if adventures_planned < 1:
        raise ProjectError("a goal must be worth at least one adventure")
    return math.ceil(difficulty / adventures_planned)


def allied_faction_share(difficulty: int) -> int:
    """An allied institution can supply a quarter of the Renown as an action."""
    if difficulty < 0:
        raise ProjectError("difficulty cannot be negative")
    share = float(load_projects()["decreasing_difficulty"]["allied_faction_share"])
    return math.ceil(difficulty * share)


@dataclass(frozen=True)
class ProjectState:
    difficulty: int
    renown_spent: int = 0

    @property
    def remaining(self) -> int:
        return max(0, self.difficulty - self.renown_spent)

    @property
    def complete(self) -> bool:
        return self.remaining == 0

    def advance(self, renown: int) -> ProjectState:
        if renown < 0:
            raise ProjectError("Renown spent cannot be negative")
        return ProjectState(self.difficulty, self.renown_spent + renown)

    def reduce_difficulty(self, amount: int) -> ProjectState:
        """Quelling an opponent or changing the situation lowers what is still owed."""
        if amount < 0:
            raise ProjectError("a difficulty reduction cannot be negative")
        return ProjectState(max(0, self.difficulty - amount), self.renown_spent)


__all__ = [
    "PROJECTS_PATH",
    "Opposition",
    "Probability",
    "ProjectError",
    "ProjectState",
    "Scope",
    "adventure_share",
    "allied_faction_share",
    "load_projects",
    "money_purchase_is_modelled",
    "project_difficulty",
    "renown_after_adventures",
]
