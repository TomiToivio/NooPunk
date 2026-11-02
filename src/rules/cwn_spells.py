"""CWN 6.1.3.5 — the spell list and overcasting (issue #1068).

The catalogue is data (`data/rules/cwn/spells.json`), transcribed from the CWN SRD with names, Effort commitment
and duration. Effect text is deliberately **not** reproduced here: it is the part a player reads in the book, and
a paraphrase would be a second rulebook nobody proof-reads.

Overcasting (6.1.3.3) is a procedure, not a catalogue, and is implemented exactly as written: declare it as an On
Turn action, the next spell this round costs no Effort, then roll and add Cast skill and the Constitution
modifier — **minus 2** if the spell would have required committing Effort for the day. If the resulting System
Strain would exceed the maximum, the mage falls unconscious for an hour and wakes with 1 hit point.
"""
from __future__ import annotations

import json
from pathlib import Path

from src.rules.wn_core import attribute_modifier

CATALOGUE = Path(__file__).resolve().parents[2] / "data/rules/cwn/spells.json"

COMMITMENTS = ("Day", "Scene", "Scene/Day", "None")


class SpellError(ValueError):
    """A rule was about to be broken."""


def load_spells(path: str | Path | None = None) -> list[dict]:
    data = json.loads(Path(path or CATALOGUE).read_text(encoding="utf-8"))
    spells = data["spells"]
    seen = set()
    for spell in spells:
        if spell["commitment"] not in COMMITMENTS:
            raise SpellError(f"{spell['name']}: unknown commitment {spell['commitment']!r}")
        if spell["name"] in seen:
            raise SpellError(f"duplicate spell {spell['name']!r}")
        seen.add(spell["name"])
    return spells


SPELLS = {s["name"]: s for s in load_spells()}


def spell(name: str) -> dict:
    try:
        return SPELLS[name]
    except KeyError:
        raise SpellError(f"unknown spell {name!r}") from None


def spells_committed(commitment: str) -> list[str]:
    return sorted(n for n, s in SPELLS.items() if s["commitment"] == commitment)


def overcast_roll(*, die: int, cast_skill: int, constitution: int, commits_for_day: bool) -> int:
    """The number looked up on the overcasting table."""
    if not 1 <= die <= 20:
        raise SpellError("overcasting rolls a d20")
    total = die + cast_skill + attribute_modifier(constitution)
    if commits_for_day:
        total -= 2
    return total


def overcast_outcome(total: int) -> dict:
    """The published table, verbatim in its bands."""
    if total <= 1:
        return {"band": "1-", "effect": "instant and unavoidable death", "strain": None}
    if total <= 4:
        return {"band": "2-4", "effect": "mortally wounded and at zero HP", "strain": None}
    if total <= 8:
        return {"band": "5-8", "effect": "unconscious for one minute", "strain": 4}
    if total <= 15:
        return {"band": "9-15", "effect": "stunned, cannot act next round", "strain": 2}
    if total <= 19:
        return {"band": "16-19", "effect": "lose next round's Main Action", "strain": 1}
    return {"band": "20+", "effect": "none beyond the strain", "strain": 1}


def overcast(*, die: int, cast_skill: int, constitution: int, commits_for_day: bool,
             current_strain: int, max_strain: int) -> dict:
    """Resolve an overcast attempt, including the unconsciousness rule (6.1.3.3)."""
    total = overcast_roll(die=die, cast_skill=cast_skill, constitution=constitution,
                          commits_for_day=commits_for_day)
    outcome = overcast_outcome(total)
    strain = outcome["strain"] or 0
    would_exceed = strain and (current_strain + strain > max_strain)
    outcome = dict(outcome)
    outcome["total"] = total
    outcome["new_strain"] = current_strain + strain
    outcome["unconscious_one_hour"] = bool(would_exceed)
    if would_exceed:
        outcome["note"] = "wakes with 1 hit point"
    return outcome
