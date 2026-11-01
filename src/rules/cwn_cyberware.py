"""Cities Without Number: cyberware operations, skillplugs, mods and Alienation.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``). Section numbers are the SRD's own:

* **3.6.1** installation — surgery difficulty, equipment modifiers, recovery, donated work;
* **3.6.1.1** the d12 implant complication table and its "use 12 instead" fallback;
* **3.6.2** removal, including ungentle disassembly, salvage from a body and re-use grading;
* **3.6.3** concealing and detecting cyber (Medical / Touch / Sight);
* **3.6.4** maintenance — 5% of base cost monthly, hours equal to System Strain;
* **3.6.5** skillplugs — levels, jack types, the automatic-failure range and the scene lockout;
* **3.6.6** cyberware mods — Fix/Heal levels, percentage costs, one copy per system;
* **3.6.7** the cyberware systems catalogue (data, not prose: ``data/rules/cwn_cyberware.json``);
* **3.6.8** Alienation — optional rule, permanent gain, chrome syndromes, CIP and therapy.

## What this module owns, and what it deliberately delegates

The strain bands, the strain ceiling and :func:`resolve_implant_surgery` are owned by
``cwn_core``; this module *calls* them so there is exactly one copy of the installation table.
The Alienation arithmetic is owned here and nowhere else — a caller that needs "how much
Alienation is this system worth" must ask this module, never re-derive ``ceil(strain)``.

## Three details that are easy to get subtly wrong

1. The equipment/room table in 3.6.1 modifies the **surgeon's check**, not the difficulty
   number. :func:`surgery_check_modifier` therefore returns a roll bonus, and
   :func:`surgery_difficulty` is left as the book's flat target.
2. Failing by one or two points is **not** a failed surgery: the cyber is implanted and the
   user eats a complication roll (see ``cwn_core.resolve_implant_surgery``).
3. Alienation is an **optional** rule. The SRD's default cyber rules change nothing about a
   user's mind; :data:`ALIENATION_IS_OPTIONAL` says so where a caller can read it.

## Not modelled here

The per-system *effect* prose of 3.6.7 (e.g. what a Banshee Module's scream does) stays in
the SRD; this module exposes the mechanical row — cost, body type, concealment, permanent
System Strain — and lets the scenario layer reference the system by id.
"""
from __future__ import annotations

import json
import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .cwn_core import (
    CwnError,
    can_accept_implant,
    installation_terms,
    maintenance_overdue,
    resolve_implant_surgery,
)

__all__ = [
    "ALIENATION_IS_OPTIONAL",
    "COMPLICATIONS",
    "CONCEALMENT_LEVELS",
    "CYBERWARE_TABLES",
    "MODS",
    "SYNDROMES",
    "THERAPY_COST_PER_WEEK",
    "CyberSystem",
    "CyberwareError",
    "alienation_for_system",
    "auto_failure_faces",
    "can_accept_implant",
    "can_install_mod",
    "can_maintain",
    "complication",
    "complication_extra_strain",
    "concealment_rank",
    "detectable",
    "installation_attempt_penalty",
    "installation_cost",
    "installation_terms",
    "is_auto_failure",
    "is_psychotic",
    "load_systems",
    "maintenance_required",
    "max_alienation",
    "mod_cost",
    "mod_requirements",
    "monthly_upkeep",
    "permanent_alienation",
    "permanent_strain_total",
    "profile_adjusted",
    "removal_terms",
    "rescue_from_cip",
    "resolve_alienation_check",
    "resolve_brutal_removal",
    "resolve_implant_surgery",
    "resolve_removal",
    "resolve_reuse",
    "resolve_salvage",
    "resolve_skillplug_roll",
    "skillplug_cost",
    "skillplug_jack_allows",
    "surgery_check_modifier",
    "surgery_difficulty",
    "system",
    "therapy_week",
]


class CyberwareError(CwnError):
    """A constraint from the SRD's cyberware rules was about to be violated."""


#: SRD 3.6.8 opens with "In the default cyber rules, chrome does not cause dramatic psychological
#: changes in of itself". Alienation is an optional campaign rule, not part of the baseline.
ALIENATION_IS_OPTIONAL = True

#: SRD 3.6.7: the seven body categories a cyber system can belong to.
CYBERWARE_TABLES: tuple[str, ...] = ("body", "head", "skin", "limb", "sensory", "medical", "nerve")

CYBERWARE_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "cwn_cyberware.json"


# --------------------------------------------------------------------------- #
# 3.6.1 Installation: equipment modifiers, retries, donated work
# --------------------------------------------------------------------------- #
#: Theatre grade -> modifier on the surgeon's check. Grade 0 is the SRD's "only has a cyberdoc
#: kit" row, which is **-1**; the retired Godot kernel returned 0 for that row.
THEATRE_MODIFIERS: dict[int, int] = {0: -1, 1: 0, 2: 1, 3: 2}

#: Room quality -> modifier. Keys are the SRD's four rows.
ROOM_MODIFIERS: dict[str, int] = {
    "lacks_room": -1,
    "clean_room": 0,
    "sterile_operating_room": 1,
    "medical_clinic": 2,
}

#: SRD 3.6.1.2: "They grant a +1 skill check bonus when installing or removing cyberware made by
#: that manufacturer."
MANUFACTURERS_KIT_MODIFIER = 1

#: SRD 3.6.1: "+1 The cyber is new and unused".
NEW_CYBER_MODIFIER = 1

#: SRD 3.6.1: "Such additional attempts have a cumulative -1 penalty on all installation attempts
#: after the original".
RETRY_PENALTY = -1


def surgery_check_modifier(
    *,
    theatre_level: int = 1,
    room: str = "clean_room",
    new_cyber: bool = False,
    manufacturers_kit: bool = False,
) -> int:
    """The surgeon's modifier from equipment, room quality and the implant's provenance.

    ``theatre_level`` 0 means a cyberdoc kit and nothing else (SRD's -1 row). Failing to model
    the kit row is the difference between a street-doc operation and a clinic one.
    """
    if theatre_level not in THEATRE_MODIFIERS:
        raise CyberwareError(f"theatre level must be 0-3, got {theatre_level!r}")
    if room not in ROOM_MODIFIERS:
        raise CyberwareError(f"unknown room quality {room!r}; expected one of {sorted(ROOM_MODIFIERS)}")
    total = THEATRE_MODIFIERS[theatre_level] + ROOM_MODIFIERS[room]
    if new_cyber:
        total += NEW_CYBER_MODIFIER
    if manufacturers_kit:
        total += MANUFACTURERS_KIT_MODIFIER
    return total


def surgery_difficulty(strain: float) -> int:
    """The flat installation difficulty for a system of this permanent System Strain cost."""
    return int(installation_terms(strain)["difficulty"])


def installation_attempt_penalty(prior_attempts: int) -> int:
    """Cumulative -1 per attempt after the first (SRD 3.6.1, re-implantation paragraph)."""
    if prior_attempts < 0:
        raise CyberwareError("prior attempts cannot be negative")
    return RETRY_PENALTY * max(0, prior_attempts - 1)


def installation_cost(strain: float, *, surgeon_donates: bool = False) -> int:
    """SRD 3.6.1: "If the surgeon donates their work, the installation cost is halved"."""
    cost = int(installation_terms(strain)["cost"])
    return cost // 2 if surgeon_donates else cost


# --------------------------------------------------------------------------- #
# 3.6.1.1 The d12 implant complication table
# --------------------------------------------------------------------------- #
#: d12 rows. ``hook`` names the mechanical consequence the scenario layer must apply; this module
#: owns only what is arithmetic (the extra System Strain).
COMPLICATIONS: dict[int, dict[str, Any]] = {
    1: {"id": "unreliable", "name": "Unreliable",
        "hook": "first important daily use: roll 1d6, on a 1 the system is dead until maintained",
        "extra_strain": 0.0},
    2: {"id": "inefficient", "name": "Inefficient",
        "hook": "the ware costs an additional 0.5 System Strain", "extra_strain": 0.5},
    3: {"id": "loud", "name": "Loud",
        "hook": "audible five metres away while operating; stealth impossible", "extra_strain": 0.0},
    4: {"id": "fussy", "name": "Fussy",
        "hook": "the required maintenance interval is halved", "extra_strain": 0.0},
    5: {"id": "bad_connection", "name": "Bad Connection",
        "hook": "1 in 6 chance an activation fails and the action is wasted", "extra_strain": 0.0},
    6: {"id": "blatant", "name": "Blatant",
        "hook": "becomes obvious on sight even if it was Medical or Touch", "extra_strain": 0.0},
    7: {"id": "debilitating", "name": "Debilitating",
        "hook": "a relevant attribute's base score drops by 1d2 while implanted", "extra_strain": 0.0},
    8: {"id": "uncooperative", "name": "Uncooperative",
        "hook": "+1 System Strain if another implant shares its body category", "extra_strain": 1.0},
    9: {"id": "complicated", "name": "Complicated",
        "hook": "maintenance now needs Fix-1 or Heal-1", "extra_strain": 0.0},
    10: {"id": "exhausting", "name": "Exhausting",
         "hook": "24 hours of downtime after maintenance, else 2 System Strain", "extra_strain": 0.0},
    11: {"id": "power_hungry", "name": "Power Hungry",
         "hook": "half an hour a day on a grid or vehicle port, else inert", "extra_strain": 0.0},
    12: {"id": "petty_annoyance", "name": "Petty Annoyance",
         "hook": "a small quirk of fit with no functional problem", "extra_strain": 0.0},
}

#: SRD 3.6.1.1: "If the resulting complication somehow does not apply to the cyber, it counts as a
#: result of 12."
FALLBACK_COMPLICATION = 12


def complication(roll: int, *, applies: bool = True) -> dict[str, Any]:
    """The complication a d12 roll produces, with the SRD's substitute-12 rule applied.

    ``applies`` is whether the rolled complication can affect this particular implant (Loud on a
    passive system, Power Hungry on something with no draw). When it cannot, row 12 is used and
    ``substituted`` is set, so a caller can report the substitution instead of hiding it.
    """
    if not 1 <= roll <= 12:
        raise CyberwareError(f"the implant complication table is d12, got {roll!r}")
    used = roll if applies else FALLBACK_COMPLICATION
    row = COMPLICATIONS[used]
    return {
        "roll": roll,
        "used": used,
        "substituted": used != roll,
        "id": str(row["id"]),
        "name": str(row["name"]),
        "hook": str(row["hook"]),
        "extra_strain": float(row["extra_strain"]),
    }


def complication_extra_strain(roll: int, *, shares_category: bool = False) -> float:
    """The System Strain a complication adds, honouring Uncooperative's "only implant of its
    category" condition."""
    row = complication(roll)
    if row["id"] == "uncooperative" and not shares_category:
        return 0.0
    return float(row["extra_strain"])


# --------------------------------------------------------------------------- #
# 3.6.2 Removal, salvage and re-use
# --------------------------------------------------------------------------- #
def removal_terms(install_difficulty: int, *, gentle: bool = True) -> dict[str, Any]:
    """SRD 3.6.2: safe removal is an hour at the installation difficulty; a doc who does not care
    takes ten minutes and the subject "almost always dies"."""
    if install_difficulty <= 0:
        raise CyberwareError("installation difficulty must be positive")
    return {
        "difficulty": install_difficulty,
        "minutes": 60 if gentle else 10,
        "patient_survives": gentle,
        "check_required": gentle,
    }


def resolve_removal(check_total: int, difficulty: int) -> dict[str, Any]:
    """Gentle removal: the implant survives on a success; either way the patient is healthy and the
    permanent System Strain is gone."""
    return {
        "implant_intact": check_total >= difficulty,
        "patient_healthy": True,
        "system_strain_removed": True,
    }


def resolve_brutal_removal(*, minimally_invasive: bool) -> dict[str, Any]:
    """SRD 3.6.2: no roll, ten minutes, and the subject "almost always dies" — the exception is a
    minimally invasive system. Modelled as survival for a minimally invasive implant only."""
    return {
        "minutes": 10,
        "implant_intact": True,
        "patient_survives": minimally_invasive,
        "detail": "" if minimally_invasive
        else "the subject dies on the table; only minimally invasive systems are survivable",
    }


def resolve_salvage(check_total: int, hours_dead: float, difficulty: int = 10) -> dict[str, Any]:
    """SRD 3.6.2: salvaging from a corpse is an Int or Dex/Heal check against 10, and "subjects dead
    for more than 24 hours are unsalvageable"."""
    if hours_dead > 24:
        return {"recovered": False, "reason": "dead more than 24 hours — unsalvageable"}
    if hours_dead < 0:
        raise CyberwareError("hours dead cannot be negative")
    return {"recovered": check_total >= difficulty, "reason": ""}


def resolve_reuse(check_total: int, difficulty: int = 10) -> dict[str, Any]:
    """SRD 3.6.2: a second Heal check against 10 — success leaves the ware used but functional,
    failure makes it secondhand with an unavoidable implantation complication."""
    if check_total >= difficulty:
        return {"state": "used", "complication_required": False}
    return {"state": "secondhand", "complication_required": True}


# --------------------------------------------------------------------------- #
# 3.6.3 Concealing and detecting cyber
# --------------------------------------------------------------------------- #
#: Ordered least- to most-conspicuous. The catalogue's "Obvious" spelling is an alias of "sight".
CONCEALMENT_LEVELS: tuple[str, ...] = ("medical", "touch", "sight")

_CONCEALMENT_ALIASES = {
    "medical": "medical",
    "touch": "touch",
    "sight": "sight",
    "obvious": "sight",
}


def concealment_rank(level: str) -> int:
    """0 Medical, 1 Touch, 2 Sight. Unknown values raise rather than defaulting to the loudest."""
    key = str(level).strip().lower().replace("_", " ")
    if key not in _CONCEALMENT_ALIASES:
        raise CyberwareError(f"unknown concealment {level!r}; expected medical, touch or sight")
    return CONCEALMENT_LEVELS.index(_CONCEALMENT_ALIASES[key])


def detectable(level: str, method: str) -> bool:
    """Whether a given inspection method finds this grade of cyber.

    SRD 3.6.3: Medical work needs a cyber scanner or a medical examination; Touch work is
    "inobvious to mere visual examination" but a hand on the limb finds it; Sight work is visible
    and "even the most perfunctory patdown will detect it".
    """
    rank = concealment_rank(level)
    normalised = str(method).strip().lower()
    if normalised in {"visual", "sight", "look"}:
        return rank >= 2
    if normalised in {"touch", "patdown", "frisk"}:
        return rank >= 1
    if normalised in {"medical", "exam", "scanner", "cyber_scanner"}:
        return True
    raise CyberwareError(f"unknown inspection method {method!r}")


def profile_adjusted(level: str) -> str:
    """SRD 3.6.6 Profile Adjustment: lower the obviousness one step; no benefit at Medical."""
    return CONCEALMENT_LEVELS[max(0, concealment_rank(level) - 1)]


# --------------------------------------------------------------------------- #
# 3.6.4 Maintenance
# --------------------------------------------------------------------------- #
#: SRD 3.6.4: "maintenance and subscription expenses add up to 5% of the cyberware's base cost due
#: monthly, not including any cyberware mods or implant surgery expenses".
MONTHLY_UPKEEP_RATE = 0.05

#: SRD 3.6.4: "must be performed by someone with at least Fix-0 or Heal-0".
MAINTENANCE_MINIMUM_SKILL = 0


def monthly_upkeep(base_cost: int) -> int:
    """The monthly maintenance and subscription charge for a system of this base cost.

    The SRD gives 5% and no rounding instruction, so a half-dollar rounds **up** rather than to
    Python's banker's rounding: two callers must not disagree about a $12.50 charge.
    """
    if base_cost < 0:
        raise CyberwareError("a system's base cost cannot be negative")
    return math.floor(base_cost * MONTHLY_UPKEEP_RATE + 0.5)


def can_maintain(*, fix_level: int = -1, heal_level: int = -1) -> bool:
    """Fix-0 or Heal-0 (or better) suffices. Untrained is -1 in the Without Number scale."""
    return max(fix_level, heal_level) >= MAINTENANCE_MINIMUM_SKILL


def maintenance_required(months_since_upkeep: float) -> bool:
    """True once a month has passed: the SRD then has the GM pick or roll a complication."""
    return maintenance_overdue(months_since_upkeep)


# --------------------------------------------------------------------------- #
# 3.6.5 Skillplugs
# --------------------------------------------------------------------------- #
#: SRD 3.6.5 price table. Level-3 plugs are not purchasable: "normally only available through
#: special missions to obtain them", hence ``None`` rather than a price.
SKILLPLUG_COSTS: dict[int, int | None] = {0: 1_000, 1: 10_000, 2: 50_000, 3: None}

#: "X2 Physical-based skill".
PHYSICAL_SKILL_MULTIPLIER = 2

#: A Skillplug Jack I interfaces only with mental skills; Jack II is needed for physical ones.
#: The catalogue spells the two jacks ``skillplug_jack_i`` / ``skillplug_jack_ii``; both spellings
#: and plain ``1``/``2`` are accepted, because a table keyed by a printed name attracts variants.
JACK_PHYSICAL_SKILLS: dict[str, bool] = {
    "skillplug_jack_1": False,
    "skillplug_jack_2": True,
    "skillplug_jack_i": False,
    "skillplug_jack_ii": True,
}

#: Level-2 and level-3 plugs additionally require the Skillplug Wiring implant.
SKILLPLUG_WIRING_MIN_LEVEL = 2

#: "Whenever the user rolls a natural 2 on a skillplug-augmented skill check, or a natural 1 on a
#: skillplug-augmented attack roll, the check or roll is an automatic failure".
AUTO_FAILURE_SKILL_ROLL = 2
AUTO_FAILURE_ATTACK_ROLL = 1


def skillplug_cost(level: int, *, physical: bool = False) -> int:
    """Price of a skillplug, doubled for physical skills. Level 3 has no price: it is mission loot."""
    if level not in SKILLPLUG_COSTS:
        raise CyberwareError(f"skillplug level must be 0-3, got {level!r}")
    base = SKILLPLUG_COSTS[level]
    if base is None:
        raise CyberwareError("level-3 skillplugs are not for sale; they come from a mission")
    return base * PHYSICAL_SKILL_MULTIPLIER if physical else base


def skillplug_jack_allows(jack: str, *, physical: bool) -> bool:
    """Whether this plug jack can run a physical skillplug at all."""
    normalised = str(jack).strip().lower().replace(" ", "_").replace("-", "_")
    if normalised in {"1", "jack_1", "jack_i"}:
        normalised = "skillplug_jack_1"
    elif normalised in {"2", "jack_2", "jack_ii"}:
        normalised = "skillplug_jack_2"
    jack = normalised
    if jack not in JACK_PHYSICAL_SKILLS:
        raise CyberwareError(f"unknown plug jack {jack!r}; expected one of {sorted(JACK_PHYSICAL_SKILLS)}")
    return physical is False or JACK_PHYSICAL_SKILLS[jack]


def auto_failure_faces(*, attack: bool = False, plugs_running: int = 1) -> frozenset[int]:
    """The natural-roll faces that are automatic failures for a skillplug-augmented roll.

    Base is 2 on a skill check and 1 on an attack. "Each additional skillplug run after the first
    increases the automatic failure roll range by one point", so two plugs fail on 1-2 (attack) or
    2-3 (skill) and so on.
    """
    if plugs_running < 1:
        raise CyberwareError("at least one skillplug run must be active")
    start = AUTO_FAILURE_ATTACK_ROLL if attack else AUTO_FAILURE_SKILL_ROLL
    return frozenset(range(start, start + plugs_running))


def is_auto_failure(die: int, *, attack: bool = False, plugs_running: int = 1) -> bool:
    """Whether a natural roll on the d20 falls inside the automatic-failure range."""
    return die in auto_failure_faces(attack=attack, plugs_running=plugs_running)


def resolve_skillplug_roll(die: int, *, attack: bool = False, plugs_running: int = 1) -> dict[str, Any]:
    """The SRD's consequence bundle for one skillplug-augmented natural roll.

    An automatic failure is "an automatic failure that no reroll ability can save", and "the
    skillplug jack itself then locks up uselessly for the scene" — three separate facts that a
    single ``bool`` would lose.
    """
    if not 1 <= die <= 20:
        raise CyberwareError(f"natural rolls are d20, got {die!r}")
    failed = is_auto_failure(die, attack=attack, plugs_running=plugs_running)
    return {
        "natural": die,
        "auto_failure": failed,
        "no_reroll": failed,
        "jack_locked_for_scene": failed,
    }


# --------------------------------------------------------------------------- #
# 3.6.6 Cyberware mods
# --------------------------------------------------------------------------- #
#: SRD 3.6.6 table: required Fix/Heal skill levels, cost as a percentage of the host system, and
#: whether a special component is consumed. ``hook`` names the effect the scenario layer applies.
MODS: dict[str, dict[str, Any]] = {
    "biocapacitors": {"name": "Biocapacitors", "fix": 1, "heal": 2, "cost_percent": 30,
                      "components": 1, "hook": "the first System Strain the system would cost each day is ignored"},
    "durable_system": {"name": "Durable System", "fix": 1, "heal": 1, "cost_percent": 20,
                       "components": 0, "hook": "the next Major Injury to the limb is treated as a roll of 12; destroys this mod"},
    "firewalled": {"name": "Firewalled", "fix": 1, "heal": 1, "cost_percent": 20,
                   "components": 0, "hook": "-2 penalty on any skill check to hack the system"},
    "hardened_weave": {"name": "Hardened Weave", "fix": 2, "heal": 1, "cost_percent": 30,
                       "components": 0, "hook": "+2 AC from skin cyber; the system becomes obvious and Readied"},
    "low_maintenance": {"name": "Low Maintenance", "fix": 2, "heal": 2, "cost_percent": 10,
                        "components": 1, "hook": "no significant maintenance; illegal on systems with special upkeep"},
    "monoblade": {"name": "Monoblade", "fix": 2, "heal": 1, "cost_percent": 20,
                  "components": 0, "hook": "+1 Trauma Die, -2 base damage die and Shock"},
    "profile_adjustment": {"name": "Profile Adjustment", "fix": 1, "heal": 2, "cost_percent": 20,
                           "components": 0, "hook": "obviousness drops one step (Sight->Touch, Touch->Medical)"},
    "quick_detach": {"name": "Quick Detach", "fix": 2, "heal": 2, "cost_percent": 30,
                     "components": 0, "hook": "attach or detach the system with five minutes of work"},
    "tailored_interface": {"name": "Tailored Interface", "fix": 1, "heal": 3, "cost_percent": 30,
                           "components": 1, "hook": "-1 System Strain on a system costing 2 or more"},
    "targeting_processor": {"name": "Targeting Processor", "fix": 2, "heal": 1, "cost_percent": 30,
                            "components": 0, "hook": "+1 to hit with the cyber-weapon or a Gunlink-aimed gun"},
}

#: SRD 3.6.6: "a given cyberware mod can only be installed once on any given system".
MODS_PER_SYSTEM = 1


def _mod_row(mod: str) -> Mapping[str, Any]:
    key = str(mod).strip().lower().replace(" ", "_").replace("-", "_")
    if key not in MODS:
        raise CyberwareError(f"unknown cyberware mod {mod!r}; expected one of {sorted(MODS)}")
    return MODS[key]


def mod_cost(system_cost: int, mod: str) -> int:
    """SRD 3.6.6: "Cyberware mod costs are expressed as a percentage cost of the system"."""
    if system_cost < 0:
        raise CyberwareError("a system's base cost cannot be negative")
    return round(system_cost * float(_mod_row(mod)["cost_percent"]) / 100)


def mod_requirements(mod: str) -> dict[str, Any]:
    """The Fix and Heal levels the mod demands, and whether it consumes a special component."""
    row = _mod_row(mod)
    return {
        "name": str(row["name"]),
        "fix_level": int(row["fix"]),
        "heal_level": int(row["heal"]),
        "components": int(row["components"]),
        "hook": str(row["hook"]),
    }


def can_install_mod(mod: str, *, installed: Sequence[str] = (), system_strain: float | None = None) -> dict[str, Any]:
    """Whether a mod can go on this system.

    Two gates from the SRD: a mod is once per system, and Tailored Interface "only functions on cyber
    that inflicts 2+ points of permanent System Strain".
    """
    row = _mod_row(mod)
    key = str(mod).strip().lower().replace(" ", "_").replace("-", "_")
    if key in {str(existing).strip().lower().replace(" ", "_") for existing in installed}:
        return {"ok": False, "reason": f"{row['name']} is already installed on this system"}
    if key == "tailored_interface":
        if system_strain is None:
            raise CyberwareError("Tailored Interface needs the host system's System Strain")
        if system_strain < 2:
            return {"ok": False, "reason": "Tailored Interface needs a system costing 2+ System Strain"}
    return {"ok": True, "reason": ""}


# --------------------------------------------------------------------------- #
# 3.6.8 Alienation
# --------------------------------------------------------------------------- #
#: SRD 3.6.8.1: "if these points ever exceed the user's Wisdom score, they break down entirely".
ALIENATION_MAXIMUM_ATTRIBUTE = "Wisdom"

#: Nerve cyberware adds +2 Alienation per system on top of the rounded strain.
NERVE_ALIENATION_SURCHARGE = 2

#: SRD 3.6.8.1: therapy costs "about $2,000 a week" and drops the score by one point per week.
THERAPY_COST_PER_WEEK = 2_000

#: SRD 3.6.8.3: each syndrome raises the effective maximum by its listed amount; each may be taken
#: once. ``trigger`` names when the SRD forces an Alienation check.
SYNDROMES: dict[str, dict[str, Any]] = {
    "brutal": {"name": "Brutal", "bonus": 4,
               "trigger": "each round you attack someone with non-lethal intent",
               "effect": "cannot engage in non-lethal combat"},
    "candid": {"name": "Candid", "bonus": 3,
               "trigger": "trying to stay silent or avert the instinct for a scene",
               "effect": "instinctively answers questions with a sentence of truth"},
    "cold": {"name": "Cold", "bonus": 4,
             "trigger": "narrative — losing the capacity for affection",
             "effect": "unable to feel love or affection; lose your closest Contact"},
    "distant": {"name": "Distant", "bonus": 3,
                "trigger": "narrative — the social penalty is always on",
                "effect": "-1 to all social skill checks"},
    "exultant": {"name": "Exultant", "bonus": 3,
                 "trigger": "narrative — overconfidence",
                 "effect": "automatic unavoidable failure on a natural skill roll of 12"},
    "fearless": {"name": "Fearless", "bonus": 4,
                 "trigger": "narrative — dulled survival instinct",
                 "effect": "max HP -20% rounded down; NPC Morale 12"},
    "hypervigilant": {"name": "Hypervigilant", "bonus": 3,
                      "trigger": "narrative — insomnia",
                      "effect": "one permanent System Strain"},
    "murderous": {"name": "Murderous", "bonus": 6,
                  "trigger": "each day beyond a week without personally killing someone",
                  "effect": "must kill at least one person a week"},
    "ravenous": {"name": "Ravenous", "bonus": 4,
                 "trigger": "each time you resist an easy chance to indulge your sensory vice",
                 "effect": "pick a vice; pay $100 per permanent Alienation point per week"},
    "savage": {"name": "Savage", "bonus": 5,
               "trigger": "choosing to flee combat after taking hit point damage",
               "effect": "cannot run from a fight you have been hurt in"},
    "secretive": {"name": "Secretive", "bonus": 3,
                  "trigger": "each topic truthfully discussed in a scene",
                  "effect": "cannot fully answer questions outside common knowledge"},
    "stressed": {"name": "Stressed", "bonus": 5,
                 "trigger": "narrative — the hardware aggravates a weakened system",
                 "effect": "lowest attribute suffers a -1 modifier penalty, to a minimum of -3"},
}


def _syndrome_key(syndrome: str) -> str:
    return str(syndrome).strip().lower().replace(" ", "_").replace("-", "_")


def alienation_for_system(strain_cost: float, *, nerve: bool = False) -> int:
    """Alienation a system imposes: its System Strain **rounded up**, plus 2 if it is Nerve cyber.

    The rounding is the part that matters: "Eye or ear mods discounted by cybereyes or cyberears
    still round up to 1 Alienation each", so a 0.25-cost system is worth one point, not zero.
    """
    if strain_cost < 0:
        raise CyberwareError("System Strain cost cannot be negative")
    if strain_cost == 0:
        return 0
    points = math.ceil(strain_cost)
    if nerve:
        points += NERVE_ALIENATION_SURCHARGE
    return points


def permanent_alienation(systems: Iterable[Mapping[str, Any] | CyberSystem]) -> int:
    """The floor Alienation imposed by the cyber a character still carries.

    Each entry supplies ``strain``/``strain_cost`` and either ``nerve`` or a ``table`` equal to
    ``"nerve"``; the catalogue's :class:`CyberSystem` satisfies both spellings.
    """
    total = 0
    for system_row in systems:
        if isinstance(system_row, CyberSystem):
            total += alienation_for_system(system_row.strain, nerve=system_row.is_nerve)
            continue
        strain = float(system_row.get("strain", system_row.get("strain_cost", 0.0)))
        nerve = bool(system_row.get("nerve", str(system_row.get("table", "")).lower() == "nerve"))
        total += alienation_for_system(strain, nerve=nerve)
    return total


def max_alienation(wisdom: int, syndromes: Sequence[str] = ()) -> int:
    """Wisdom plus the bonuses of the chrome syndromes carried. A syndrome taken twice raises."""
    if not 3 <= wisdom <= 18:
        raise CyberwareError("Wisdom must be within the Without Number range 3-18")
    bonus = 0
    seen: set[str] = set()
    for syndrome in syndromes:
        key = _syndrome_key(syndrome)
        if key not in SYNDROMES:
            raise CyberwareError(f"unknown chrome syndrome {syndrome!r}")
        if key in seen:
            raise CyberwareError(f"the same chrome syndrome cannot be picked twice: {key}")
        seen.add(key)
        bonus += int(SYNDROMES[key]["bonus"])
    return wisdom + bonus


def gains_alienation_point(d20: int, current: int) -> bool:
    """SRD 3.6.8.1: "the user rolls 1d20; if the result is equal or less than their current
    Alienation, they gain one point". At 0 Alienation a check can never add a point."""
    if not 1 <= d20 <= 20:
        raise CyberwareError(f"an Alienation check is 1d20, got {d20!r}")
    if current < 0:
        raise CyberwareError("Alienation cannot be negative")
    return d20 <= current


def is_psychotic(total: int, wisdom: int, syndromes: Sequence[str] = ()) -> bool:
    """Strictly above the maximum: a character sitting exactly at their limit is still themselves."""
    return total > max_alienation(wisdom, syndromes)


def resolve_alienation_check(
    *,
    d20: int,
    current: int,
    wisdom: int,
    syndromes: Sequence[str] = (),
    mental_save: bool | None = None,
) -> dict[str, Any]:
    """One Alienation check, including the two different outcomes above the maximum.

    The SRD gives success and failure different results — "on success, they pick a new chrome
    syndrome, and on a failure they immediately suffer CIP" — so the return value names which. Pass
    ``mental_save=None`` when the save has not been rolled yet and the outcome is
    ``"needs_mental_save"``.
    """
    gained = gains_alienation_point(d20, current)
    total = current + (1 if gained else 0)
    maximum = max_alienation(wisdom, syndromes)
    if total <= maximum:
        return {"gained": gained, "total": total, "maximum": maximum, "outcome": "stable"}
    if mental_save is None:
        return {"gained": gained, "total": total, "maximum": maximum, "outcome": "needs_mental_save"}
    return {
        "gained": gained,
        "total": total,
        "maximum": maximum,
        "outcome": "pick_syndrome" if mental_save else "psychosis",
    }


def therapy_week(current: int, permanent_floor: int) -> int:
    """One week of cyberpsychological therapy: -1, never below the floor the remaining cyber sets."""
    if permanent_floor < 0:
        raise CyberwareError("the permanent Alienation floor cannot be negative")
    return max(permanent_floor, current - 1)


def rescue_from_cip(
    *,
    alienation: int,
    wisdom: int,
    syndromes: Sequence[str] = (),
    cyber_removed_except_medical: bool,
    mental_save_total: int,
    save_target: int,
    therapist_bonus: int = 0,
) -> dict[str, Any]:
    """SRD 3.6.8.2: the only way back from cyber-induced psychosis.

    All cyber must come out (bar medically necessary prostheses), therapy must bring Alienation
    below the victim's Wisdom, and then the victim makes a Mental save with a bonus equal to the
    therapist's best Heal or Talk skill. Success returns their reason; failure is permanent.
    """
    if not cyber_removed_except_medical:
        return {"eligible": False, "outcome": "ineligible",
                "reason": "all cyber must be removed except medically necessary prostheses"}
    maximum = max_alienation(wisdom, syndromes)
    if alienation >= maximum:
        return {"eligible": False, "outcome": "ineligible",
                "reason": "Alienation must first be brought below the victim's Wisdom"}
    total = mental_save_total + therapist_bonus
    if total >= save_target:
        return {"eligible": True, "outcome": "recovered", "total": total, "target": save_target}
    return {"eligible": True, "outcome": "permanently_compromised", "total": total, "target": save_target}


# --------------------------------------------------------------------------- #
# 3.6.7 The systems catalogue
# --------------------------------------------------------------------------- #
_TRANSLATION = str.maketrans({"\u2019": "'", "\u2018": "'", "\u02bc": "'", "\u2013": "-", "\u2014": "-"})


@dataclass(frozen=True)
class CyberSystem:
    """One row of the SRD's cyberware tables: price, body type, concealment, permanent strain."""

    id: str
    name: str
    table: str
    #: ``None`` for systems whose price is "as cyber" — the Cranial Jack and the Neural Buffer are
    #: bought as part of a cyberdeck or another implant, so the SRD prints no price.
    cost: int | None
    type: str
    concealment: str
    strain: float

    @property
    def is_nerve(self) -> bool:
        return self.table == "nerve"

    @property
    def alienation(self) -> int:
        return alienation_for_system(self.strain, nerve=self.is_nerve)


_CATALOGUE_CACHE: dict[Path, tuple[CyberSystem, ...]] = {}


def load_systems(path: Path | None = None) -> tuple[CyberSystem, ...]:
    """The mechanical rows of SRD 3.6.7, read from ``data/rules/cwn_cyberware.json`` (CC0)."""
    data_path = Path(path) if path is not None else CYBERWARE_PATH
    cached = _CATALOGUE_CACHE.get(data_path)
    if cached is not None:
        return cached
    payload = json.loads(data_path.read_text(encoding="utf-8"))
    rows = payload.get("tables")
    if not isinstance(rows, list) or not rows:
        raise CyberwareError(f"{data_path} carries no cyberware tables")
    systems = tuple(
        CyberSystem(
            id=str(row["id"]),
            name=str(row["name"]),
            table=str(row["table"]),
            cost=None if row.get("cost") is None else int(row["cost"]),
            type=str(row.get("type", row["table"])),
            concealment=str(row["concealment"]),
            strain=float(row["strain"]),
        )
        for row in rows
    )
    _CATALOGUE_CACHE[data_path] = systems
    return systems


def system(name: str, systems: Sequence[CyberSystem] | None = None) -> CyberSystem:
    """Look a system up by its printed name, normalising typographic punctuation first.

    ``Cybereyes`` vs ``Cybereyes`` with a curly apostrophe in an eye mod is the difference between a
    working lookup and ``unknown cyberware``, and the SRD's typesetting is not consistent about it.
    """
    catalogue = systems if systems is not None else load_systems()
    wanted = str(name).translate(_TRANSLATION).strip().lower()
    for row in catalogue:
        if row.name.translate(_TRANSLATION).strip().lower() == wanted or row.id == wanted:
            return row
    raise CyberwareError(f"unknown cyberware system {name!r}")


def permanent_strain_total(systems: Iterable[CyberSystem | Mapping[str, Any]]) -> float:
    """Total permanent System Strain the listed systems impose on their user."""
    total = 0.0
    for row in systems:
        strain = row.strain if isinstance(row, CyberSystem) else float(row.get("strain", 0.0))
        if strain < 0:
            raise CyberwareError("System Strain cost cannot be negative")
        total += strain
    return total
