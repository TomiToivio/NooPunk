"""NoöPunk space vessel construction and encounters.

Original, deterministic SWN-inspired *adapter*, not the copyrighted SWN ship
catalogue. CWN remains authoritative for personal actions and combat.
Source: Stars Without Number Revised (2017), Starships, printed pp. 93–120.
"""
from __future__ import annotations
from dataclasses import dataclass, field


class StarshipError(ValueError):
    """Invalid ship or action; no game state should change."""


def _nonnegative(value: int, name: str) -> None:
    if type(value) is not int or value < 0:
        raise StarshipError(f"{name} must be a nonnegative integer")


@dataclass(frozen=True)
class Hull:
    identifier: str
    mass: int
    power: int
    hardpoints: int
    hit_points: int
    armor: int
    defense: int

    def __post_init__(self) -> None:
        if not self.identifier:
            raise StarshipError("hull requires an identifier")
        for name in ("mass", "power", "hardpoints", "hit_points", "armor", "defense"):
            _nonnegative(getattr(self, name), name)
        if self.hit_points == 0:
            raise StarshipError("hull must have positive hit points")


@dataclass(frozen=True)
class Fitting:
    identifier: str
    mass: int
    power: int
    hardpoints: int = 0

    def __post_init__(self) -> None:
        if not self.identifier:
            raise StarshipError("fitting requires an identifier")
        for name in ("mass", "power", "hardpoints"):
            _nonnegative(getattr(self, name), name)


@dataclass
class Vessel:
    name: str
    hull: Hull
    fittings: dict[str, Fitting] = field(default_factory=dict)
    hp: int | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise StarshipError("vessel requires a name")
        if self.hp is None:
            self.hp = self.hull.hit_points
        _nonnegative(self.hp, "hp")
        if self.hp > self.hull.hit_points:
            raise StarshipError("vessel hp exceeds hull capacity")
        if any(key != fitting.identifier for key, fitting in self.fittings.items()):
            raise StarshipError("fitting keys must match their identifiers")
        self._check_capacity(self.fittings)

    def _check_capacity(self, fittings: dict[str, Fitting]) -> None:
        for resource in ("mass", "power", "hardpoints"):
            used = sum(getattr(f, resource) for f in fittings.values())
            if used > getattr(self.hull, resource):
                raise StarshipError(f"ship has insufficient {resource}")

    def install(self, fitting: Fitting) -> None:
        if fitting.identifier in self.fittings:
            raise StarshipError("fitting is already installed")
        proposed = {**self.fittings, fitting.identifier: fitting}
        self._check_capacity(proposed)
        self.fittings = proposed

    def uninstall(self, identifier: str) -> Fitting:
        if identifier not in self.fittings:
            raise StarshipError("unknown fitting")
        return self.fittings.pop(identifier)

    @property
    def operational(self) -> bool:
        return self.hp > 0

    def snapshot(self) -> dict:
        return {"name": self.name, "hull": vars(self.hull).copy(),
                "fittings": {key: vars(f).copy() for key, f in self.fittings.items()},
                "hp": self.hp}

    @classmethod
    def from_snapshot(cls, data: dict) -> "Vessel":
        try:
            hull = Hull(**data["hull"])
            fittings = {key: Fitting(**value)
                        for key, value in data.get("fittings", {}).items()}
            return cls(data["name"], hull, fittings, data["hp"])
        except (KeyError, TypeError, AttributeError) as exc:
            raise StarshipError("invalid ship snapshot") from exc


@dataclass(frozen=True)
class ShipWeapon:
    identifier: str
    damage: int
    armor_piercing: int = 0

    def __post_init__(self) -> None:
        if not self.identifier:
            raise StarshipError("weapon requires an identifier")
        _nonnegative(self.damage, "damage")
        _nonnegative(self.armor_piercing, "armor_piercing")


@dataclass(frozen=True)
class AttackOutcome:
    hit: bool
    roll: int
    target: int
    damage: int
    remaining_hp: int


def resolve_attack(attacker: Vessel, defender: Vessel, weapon: ShipWeapon,
                   *, d20: int, attack_bonus: int = 0) -> AttackOutcome:
    """Explicit die input guarantees deterministic tests, save/replay and Godot parity.

    Values of defense/damage/armor are original scenario fixtures. This is not
    the SWN ship-combat action-economy or weapon catalogue.
    """
    if type(d20) is not int or not 1 <= d20 <= 20:
        raise StarshipError("d20 must be in 1..20")
    if type(attack_bonus) is not int:
        raise StarshipError("attack bonus must be an integer")
    if not attacker.operational or not defender.operational:
        raise StarshipError("both vessels must be operational")
    if weapon.identifier not in attacker.fittings:
        raise StarshipError("attack requires an installed weapon fitting")
    target = defender.hull.defense
    hit = d20 == 20 or (d20 != 1 and d20 + attack_bonus >= target)
    damage = max(0, weapon.damage - max(0, defender.hull.armor - weapon.armor_piercing)) if hit else 0
    defender.hp = max(0, defender.hp - damage)
    return AttackOutcome(hit, d20, target, damage, defender.hp)
