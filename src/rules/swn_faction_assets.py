"""SWN faction asset catalogue and combat resolution (#1105, P0-B).

The faction turn has existed for a while; the **catalogue** never did, and #1105 names that gap exactly: "the
turn module explicitly says SWN **asset catalogues and combat tables remain reference-only**" and "existing
turn code is **not proof of a finished asset catalogue**". This module is that catalogue, plus the one
procedure the tables need to be usable: the attack/counterattack exchange.

Where the numbers come from: the book's three asset tables (Cunning p.219, Force p.221, Wealth p.223), read by
`tools/swn_faction_assets.py` and committed as `data/rules/swn_faction_assets.json`. Hit points, cost, tech
level, type, attack attribute/defence/damage and the counterattack die are mechanics, so they are recorded.
The book's ability prose and its lettered note legend are **not** reproduced: each asset keeps its note
letters (`A`, `S`, `P`) so a reader can look them up in the book.

What this module deliberately does not do: it does not implement the ~60 individual special abilities. Each
is a sentence of rules text tied to a specific asset, and half of them change what an action is allowed to
be (Informers attacking a faction rather than an asset, Lobbyists withdrawing a permission, Boltholes
spoiling a kill). Faking them with a generic "special: see book" would be worse than leaving them out; the
tabletop sheet tells the GM to read the asset's entry before using it.

Sources: *Stars Without Number: Revised Edition — Deluxe Edition* (Kevin Crawford), pp.211–223.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Mapping

from .swn_faction_turn import Asset, Faction, FactionTurnError

__all__ = [
    "ASSETS",
    "CATEGORIES",
    "FactionAssetError",
    "asset",
    "attack_exchange",
    "by_category",
    "catalogue_size",
    "damage_roll",
    "purchase",
    "to_turn_asset",
]

DATA = Path(__file__).resolve().parents[2] / "data" / "rules" / "swn_faction_assets.json"

CATEGORIES: Final[tuple[str, ...]] = ("Cunning", "Force", "Wealth")


class FactionAssetError(ValueError):
    """An asset that is not in the catalogue, or a use the book does not allow."""


def _load() -> dict[str, dict[str, Any]]:
    raw = json.loads(DATA.read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in raw["assets"]}


#: id -> catalogue entry. Loaded once; the file is committed and checked by tests.
ASSETS: Final[dict[str, dict[str, Any]]] = _load()


def catalogue_size() -> int:
    return len(ASSETS)


def asset(asset_id: str) -> dict[str, Any]:
    try:
        return ASSETS[asset_id]
    except KeyError:
        raise FactionAssetError(f"no such faction asset: {asset_id!r}") from None


def by_category(category: str, *, level: int | None = None) -> list[dict[str, Any]]:
    if category not in CATEGORIES:
        raise FactionAssetError(f"unknown asset category {category!r}; expected one of {CATEGORIES}")
    rows = [entry for entry in ASSETS.values() if entry["category"] == category]
    if level is not None:
        rows = [entry for entry in rows if entry["level"] == level]
    return sorted(rows, key=lambda entry: (entry["level"], entry["name"]))


def _dice(spec: str) -> tuple[int, int, int]:
    """``"2d8+2"`` -> (2, 8, 2). Raises rather than guessing."""
    text = spec.strip().lower().replace(" ", "")
    if not text:
        raise FactionAssetError("no damage die")
    count, _, rest = text.partition("d")
    if not count.isdigit() or not rest:
        raise FactionAssetError(f"{spec!r} is not a die expression")
    bonus = 0
    for sign in ("+", "-"):
        if sign in rest:
            faces, _, tail = rest.partition(sign)
            if not faces.isdigit() or not tail.isdigit():
                raise FactionAssetError(f"{spec!r} is not a die expression")
            bonus = int(tail) * (1 if sign == "+" else -1)
            rest = faces
            break
    if not rest.isdigit():
        raise FactionAssetError(f"{spec!r} is not a die expression")
    return int(count), int(rest), bonus


def damage_roll(spec: str, *, rng: random.Random | None = None) -> int:
    """Roll a damage expression such as ``2d6+2``. Minimum 0, as a damage roll cannot heal."""
    count, faces, bonus = _dice(spec)
    rng = rng or random.Random()
    total = sum(rng.randint(1, faces) for _ in range(count)) + bonus
    return max(0, total)


def attack_exchange(attacker_id: str, defender_id: str, *,
                    attacker_ratings: Mapping[str, int], defender_ratings: Mapping[str, int],
                    rng: random.Random | None = None) -> dict[str, Any]:
    """One attacking asset against one defending asset (SWN p.214).

    Both sides roll 1d10 and add the attribute their attack line names — the attacker's attack attribute
    rating, the defender's *defence* attribute rating. Higher total wins. **A tie means both succeed**: both
    attack and counterattack land. The attacker's damage die is rolled on a win or a tie; the defender's
    counterattack die only when the defending asset has one and the attack did not simply miss.
    """
    attacker = asset(attacker_id)
    defender = asset(defender_id)
    attack = attacker["attack"]
    if not attack["attribute"]:
        raise FactionAssetError(f"{attacker['name']} has no attack and cannot attack")
    rng = rng or random.Random()
    # Which rating each side adds is printed on the attacker's own attack line: "Cunning vs. Wealth"
    # means the attacker adds Cunning and the defender adds Wealth.
    try:
        attacker_rating = int(attacker_ratings[attack["attribute"]])
        defender_rating = int(defender_ratings[attack["defence"]])
    except KeyError as exc:
        raise FactionAssetError(
            f"{attacker['name']}: no rating for {exc.args[0]!r}; pass all three Cunning/Force/Wealth "
            f"ratings for both factions") from None
    attacker_total = rng.randint(1, 10) + attacker_rating
    defender_total = rng.randint(1, 10) + defender_rating
    attacker_hits = attacker_total >= defender_total      # a tie: both succeed
    defender_hits = defender_total >= attacker_total

    dealt = 0
    if attacker_hits:
        if attack["damage"]:
            dealt = damage_roll(attack["damage"], rng=rng)
        elif attack["special"] != "special":
            raise FactionAssetError(f"{attacker['name']} has an attack with no damage die")
    returned = 0
    counter = defender["counter"]
    if defender_hits and isinstance(counter, str) and counter not in ("none", "special"):
        returned = damage_roll(counter, rng=rng)
    return {
        "attacker": attacker_id, "defender": defender_id,
        "attacker_total": attacker_total, "defender_total": defender_total,
        "attacker_hits": attacker_hits, "defender_counterattacks": defender_hits,
        "damage_to_defender": dealt, "damage_to_attacker": returned,
        "tie": attacker_total == defender_total,
        "special": attack["special"] or "",
    }


def to_turn_asset(asset_id: str, *, identifier: str, faction: str, location: str) -> Asset:
    """Build the turn module's `Asset` from the catalogue, so the sheet and the engine agree on HP."""
    entry = asset(asset_id)
    hp = entry["hp"]
    if hp is None:
        raise FactionAssetError(f"{entry['name']} has no printed hit points; it is not a fieldable asset")
    return Asset(identifier=identifier, faction=faction, location=location, hp=int(hp), max_hp=int(hp))


def purchase(faction: Faction, asset_id: str, *, identifier: str, location: str) -> Asset:
    """Buy one asset for a faction, charging the catalogue cost (SWN p.214, "Buy Asset").

    Refuses the Base of Influence, which the book allows only through the Expand Influence action, and
    refuses a second purchase in the same turn.
    """
    entry = asset(asset_id)
    if entry["cost"] is None:
        raise FactionAssetError(
            f"{entry['name']} is bought through the Expand Influence action, not by purchase")
    if faction.actions_taken >= 1:
        raise FactionTurnError("a faction may buy only one asset per turn, and it has acted")
    built = to_turn_asset(asset_id, identifier=identifier, faction=faction.identifier, location=location)
    faction.add_asset(built, int(entry["cost"]))
    return built
