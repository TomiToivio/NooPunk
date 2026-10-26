"""Original SWN-inspired faction turn for NoöPunk's strategy layer.

Turn scheduling, asset commitment and state validation are implemented;
specific SWN asset catalogs and combat tables remain reference-only.
"""
from dataclasses import dataclass, field


class FactionTurnError(ValueError):
    pass


@dataclass
class Asset:
    identifier: str
    faction: str
    location: str
    hp: int
    max_hp: int
    tags: tuple[str, ...] = ()

    def __post_init__(self):
        if not all((self.identifier, self.faction, self.location)):
            raise FactionTurnError("asset identity and position are required")
        if type(self.hp) is not int or type(self.max_hp) is not int or not 0 <= self.hp <= self.max_hp or self.max_hp < 1:
            raise FactionTurnError("invalid asset hit points")

    def damage(self, amount: int) -> int:
        if type(amount) is not int or amount < 0:
            raise FactionTurnError("damage cannot be negative")
        self.hp = max(0, self.hp - amount)
        return self.hp


@dataclass
class Faction:
    identifier: str
    credits: int
    assets: dict[str, Asset] = field(default_factory=dict)
    actions_taken: int = 0
    turn: int = 1
    history: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.identifier or type(self.credits) is not int or self.credits < 0:
            raise FactionTurnError("invalid faction")
        if self.actions_taken not in (0, 1):
            raise FactionTurnError("one faction action per turn")
        for key, asset in self.assets.items():
            if key != asset.identifier or asset.faction != self.identifier:
                raise FactionTurnError("faction assets have inconsistent ownership")

    def add_asset(self, asset: Asset, cost: int) -> None:
        if asset.faction != self.identifier or asset.identifier in self.assets:
            raise FactionTurnError("incorrect or duplicate asset")
        if type(cost) is not int or cost < 0 or cost > self.credits:
            raise FactionTurnError("insufficient faction credits")
        self.credits -= cost
        self.assets[asset.identifier] = asset

    def act(self, action: str, asset_ids: tuple[str, ...] = (), target: str = "") -> dict:
        if self.actions_taken:
            raise FactionTurnError("faction has already acted this turn")
        if action not in ("attack", "move", "purchase", "repair", "expand", "special"):
            raise FactionTurnError("unrecognized strategic action")
        if len(set(asset_ids)) != len(asset_ids) or any(key not in self.assets or self.assets[key].hp == 0 for key in asset_ids):
            raise FactionTurnError("invalid committed assets")
        event = {"turn": self.turn, "action": action, "assets": list(asset_ids),
                 "target": target, "resolved": False}
        self.history.append(event)
        self.actions_taken = 1
        return event

    def next_turn(self, income: int = 0) -> None:
        if type(income) is not int or income < 0:
            raise FactionTurnError("income must be non-negative")
        self.credits += income
        self.actions_taken = 0
        self.turn += 1
