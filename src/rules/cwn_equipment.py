"""Cities Without Number equipment: the SRD's weapon and armour tables, as data.

Transcribed from the **Cities Without Number SRD** (CC0; rights entry in
``data/sources/game_system_rights.json``):

* ``gear-vehicles-cyberware/weapons/firearms/``;
* ``gear-vehicles-cyberware/weapons/heavy-weapons/``;
* ``gear-vehicles-cyberware/weapons/melee-thrown-weapons/``;
* ``gear-vehicles-cyberware/armor/armor-types/``.

## Why the tables are data and not code

A weapon is a row: damage, range, cost, magazine, Shock, Trauma die and rating. Hard-coding rows into
the kernel would mean every scenario stat line re-typing them, and the first case already did exactly
that — a Light Pistol was ``1d6``, ``1d8`` Trauma and ``x2`` in three separate places. The catalogue is
the one row per weapon; :func:`damage_profile` decomposes it into the shape the combat kernel and the
Godot adapter take.

## Notation is preserved, not interpreted

The SRD marks damage with ``!``, ``#``, ``^`` and ``¶`` and defines them in footnotes. This module keeps
the marker in the string, and :func:`parse_damage` ignores it: the flags describe firing modes and
requirements, not the dice. A caller that needs a flag reads ``damage`` raw.

## What this module does not model

Weapon and armour *mods*, accessories, drones and vehicles are separate SRD chapters with their own
tables; they are not folded in here. House weapons belong in scenario data, never in the SRD catalogue.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

EQUIPMENT_PATH = Path(__file__).resolve().parents[2] / "data" / "rules" / "cwn_equipment.json"

_DAMAGE = re.compile(r"^\s*(\d+)d(\d+)\s*(?:([+-])\s*(\d+))?\s*[!#^¶*]*\s*$")


class EquipmentError(ValueError):
    """An equipment row was asked for that the SRD catalogue does not have."""


@lru_cache(maxsize=4)
def load_equipment(path: str | Path | None = None) -> dict[str, Any]:
    """Load the catalogue once and return it with ``weapons``/``armor`` keyed by id."""
    raw = json.loads(Path(path or EQUIPMENT_PATH).read_text(encoding="utf-8"))
    weapons: dict[str, dict] = {}
    for row in raw.get("weapons", []):
        key = str(row["id"])
        if key in weapons:
            raise EquipmentError(f"duplicate weapon id in the catalogue: {key}")
        weapons[key] = row
    armor: dict[str, dict] = {}
    for row in raw.get("armor", []):
        key = str(row["id"])
        if key in armor:
            raise EquipmentError(f"duplicate armor id in the catalogue: {key}")
        armor[key] = row
    return {"weapons": weapons, "armor": armor, "meta": {k: v for k, v in raw.items()
                                                        if k.startswith("_") or k in {"format", "version"}}}


def weapons() -> dict[str, dict]:
    return load_equipment()["weapons"]


def armor() -> dict[str, dict]:
    return load_equipment()["armor"]


def weapon(weapon_id: str) -> dict:
    try:
        return weapons()[weapon_id]
    except KeyError as exc:
        raise EquipmentError(f"unknown weapon: {weapon_id}") from exc


def armor_piece(armor_id: str) -> dict:
    try:
        return armor()[armor_id]
    except KeyError as exc:
        raise EquipmentError(f"unknown armor: {armor_id}") from exc


def find_weapon(name: str) -> dict:
    """Look a weapon up by its printed name, case- and space-insensitively.

    Scenario stat lines carry names ("Unarmed", "Light pistol"); the catalogue carries ids.
    """
    wanted = name.strip().lower()
    for row in weapons().values():
        printed = row["name"].strip().lower()
        # "Unarmed" is how a stat line prints the SRD's "Unarmed Attack".
        printed = printed.removesuffix(" attack")
        if wanted in {printed, row["id"], row["id"].replace("_", " ")}:
            return row
    raise EquipmentError(f"unknown weapon name: {name}")


def _sides(die: str) -> int:
    """``1d8`` → ``8``; a bare number is already the sides. The SRD's TD column is always one die."""
    match = re.fullmatch(r"\s*(?:\d+)\s*[dD]\s*(\d+)\s*", die)
    if match:
        return int(match.group(1))
    return int(die) if die.strip().isdigit() else 0


def parse_damage(damage: str) -> tuple[int, int, int]:
    """``1d10+2`` → ``(1, 10, 2)``. Firing-mode markers are irrelevant to the dice."""
    match = _DAMAGE.match(damage)
    if not match:
        raise EquipmentError(f"not a damage expression: {damage!r}")
    count, sides, sign, bonus = match.groups()
    return int(count), int(sides), (int(bonus) if sign == "+" else -int(bonus)) if bonus else 0


def damage_profile(weapon_id: str) -> dict:
    """The row decomposed into the shape the combat kernel and the Godot adapter take."""
    row = weapon(weapon_id)
    count, sides, bonus = parse_damage(str(row["damage"]))
    shock = row.get("shock") or {}
    trauma_die = _sides(str(row.get("trauma_die") or "0"))
    rating = str(row.get("trauma_rating") or "x1").lstrip("xX")
    attributes = row.get("attribute") or []
    return {
        "id": row["id"],
        "label": row["name"],
        "damage_count": count,
        "damage_sides": sides,
        "damage_bonus": bonus,
        # A melee row may list two attributes ("Str/Dex"); the first is the damage-adding one.
        "attribute": attributes[0] if attributes else "DEX",
        "shock": int(shock.get("damage", 0)),
        "shock_ac": int(shock.get("max_ac", -1)),
        "trauma_die": trauma_die,
        "trauma_rating": int(rating) if rating.isdigit() else 1,
    }


__all__ = [
    "EQUIPMENT_PATH",
    "EquipmentError",
    "armor",
    "armor_piece",
    "damage_profile",
    "find_weapon",
    "load_equipment",
    "parse_damage",
    "weapon",
    "weapons",
]
