"""Deterministic NoöPunk faction operations atop swn_faction_turn.

Adaptation inspired by SWN Revised faction turns (printed pp. 211 onward).
All numbers are scenario-supplied; this does not reproduce SWN's asset tables.
Existing Faction.act() records intent; resolve_action() applies outcomes.
"""
from dataclasses import dataclass
from .swn_faction_turn import Faction, FactionTurnError


@dataclass(frozen=True)
class OperationResult:
    actor: str
    defender: str
    action: str
    success: bool
    die: int
    total: int
    difficulty: int
    damage: int = 0
    destroyed: bool = False


def resolve_action(actor: Faction, target: Faction, *,
                   action: str, acting_asset: str, target_asset: str,
                   die: int, bonus: int = 0, difficulty: int = 10,
                   damage: int = 1) -> OperationResult:
    """Resolve one pending strategic attack without silently taking extra turns.

    Resolution is deterministic and explicitly scenario-configured. To prevent
    accidental double spending or attacking across impossible locations,
    validate all inputs before mutating the defender or action record.
    """
    if actor.identifier == target.identifier:
        raise FactionTurnError("opposing factions must differ")
    if type(die) is not int or not 1 <= die <= 20:
        raise FactionTurnError("die must be an integer from 1 through 20")
    if type(bonus) is not int or type(difficulty) is not int:
        raise FactionTurnError("bonus and difficulty must be integers")
    if type(damage) is not int or damage < 0:
        raise FactionTurnError("damage must be nonnegative")
    if action != "attack":
        raise FactionTurnError("only attack resolution is currently supported")
    if acting_asset not in actor.assets or target_asset not in target.assets:
        raise FactionTurnError("unknown offensive or defensive asset")
    source = actor.assets[acting_asset]
    victim = target.assets[target_asset]
    if source.hp == 0 or victim.hp == 0:
        raise FactionTurnError("inactive asset cannot participate")
    if source.location != victim.location:
        raise FactionTurnError("assets must occupy the same strategic location")
    if not actor.history or actor.history[-1].get("turn") != actor.turn:
        raise FactionTurnError("no recorded operation for the current turn")
    pending = actor.history[-1]
    if (pending.get("action") != "attack"
            or pending.get("resolved") is not False
            or acting_asset not in pending.get("assets", ())
            or pending.get("target") != target.identifier):
        raise FactionTurnError("operation does not match the committed action")
    total = die + bonus
    success = die == 20 or (die != 1 and total >= difficulty)
    inflicted = min(victim.hp, damage) if success else 0
    if inflicted:
        victim.damage(inflicted)
    pending.update({"resolved": True, "die": die, "total": total,
                    "difficulty": difficulty, "success": success,
                    "target_asset": target_asset, "damage": inflicted})
    return OperationResult(actor.identifier, target.identifier, action,
                           success, die, total, difficulty, inflicted,
                           victim.hp == 0)


def relocate_asset(faction: Faction, *, asset_id: str, destination: str,
                   allowed_destinations: set[str]) -> None:
    """Resolve a previously committed move with explicit map authorization."""
    if not destination or destination not in allowed_destinations:
        raise FactionTurnError("destination has no authorized route")
    if asset_id not in faction.assets or faction.assets[asset_id].hp == 0:
        raise FactionTurnError("asset missing or inactive")
    if not faction.history or faction.history[-1].get("turn") != faction.turn:
        raise FactionTurnError("no pending movement")
    pending = faction.history[-1]
    if (pending.get("action") != "move" or pending.get("resolved") is not False
            or pending.get("target") != destination
            or asset_id not in pending.get("assets", ())):
        raise FactionTurnError("movement is not the committed turn action")
    old = faction.assets[asset_id].location
    faction.assets[asset_id].location = destination
    pending.update({"resolved": True, "from": old, "to": destination})
