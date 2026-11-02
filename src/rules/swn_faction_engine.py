"""Deterministic multi-faction turn engine for the NoöPunk strategic layer (#1043).

Scope: the **procedure** of an SWN-style faction turn — who acts in what order, one action each, what
an action costs, what the audit log must show — kept faithful to the shape of SWN Revised's Factions
chapter (printed pp. 211+) while every *catalogue* value (asset costs, income, hit points) is supplied
by the scenario rather than hard-coded here. That division is deliberate and is the repository's
standing position on this system: ``data/sources/game_system_rights.json`` records SWN as having no
verified SRD, so inventing its tables would put unsourced numbers in the repo.

What this module therefore guarantees:

* a faction turn is a sequence of *legal, audited* actions, not a free-for-all;
* attribute ratings (Force / Cunning / Wealth) drive the turn order deterministically;
* a faction that has acted cannot act again until the round closes;
* income, hit points and costs arrive as scenario data, and the engine records which numbers it was
  given, so a table correction never requires a code change.

CWN remains untouched: this is an optional strategic layer. A campaign without a faction turn simply
never constructs an :class:`FactionEngine`.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum

from .swn_faction_turn import Asset, Faction, FactionTurnError

#: SWN rates every faction attribute 1..8; the band is checked, the meaning is the book's.
ATTRIBUTE_MIN, ATTRIBUTE_MAX = 1, 8

ATTRACTION_ORDER = ("force", "cunning", "wealth")


class FactionEngineError(ValueError):
    pass


class Attribute(str, Enum):
    FORCE = "force"
    CUNNING = "cunning"
    WEALTH = "wealth"


class GoalKind(str, Enum):
    """The three goal scales the chapter distinguishes, kept apart because they close differently."""

    MILITARY = "military"
    COMMERCIAL = "commercial"
    IDEOLOGICAL = "ideological"


@dataclass
class Goal:
    """A faction's current aim. Progress is game state; no table decides it."""

    kind: GoalKind
    target: str
    progress: int = 0
    needed: int = 1

    def __post_init__(self) -> None:
        if not self.target.strip():
            raise FactionEngineError("a goal needs a target")
        if type(self.needed) is not int or self.needed < 1:
            raise FactionEngineError("a goal needs a positive requirement")
        if not 0 <= self.progress <= self.needed:
            raise FactionEngineError("progress runs between zero and the requirement")

    @property
    def complete(self) -> bool:
        return self.progress >= self.needed

    def advance(self, amount: int = 1) -> bool:
        if type(amount) is not int or amount < 0:
            raise FactionEngineError("progress advances by a non-negative integer")
        self.progress = min(self.needed, self.progress + amount)
        return self.complete


@dataclass
class FactionProfile:
    """Everything the engine needs beyond :class:`~.swn_faction_turn.Faction`'s credits and assets."""

    faction: Faction
    force: int
    cunning: int
    wealth: int
    hp: int
    max_hp: int
    goal: Goal | None = None
    income: int = 0

    def __post_init__(self) -> None:
        for name in ATTRACTION_ORDER:
            value = getattr(self, name)
            if type(value) is not int or not ATTRIBUTE_MIN <= value <= ATTRIBUTE_MAX:
                raise FactionEngineError(f"{name} must be rated {ATTRIBUTE_MIN}..{ATTRIBUTE_MAX}")
        if type(self.hp) is not int or type(self.max_hp) is not int or not 0 <= self.hp <= self.max_hp:
            raise FactionEngineError("invalid faction hit points")
        if type(self.income) is not int or self.income < 0:
            raise FactionEngineError("income is a non-negative number of FacCreds")

    def attribute(self, which: Attribute) -> int:
        return getattr(self, which.value)

    def hurt(self, amount: int) -> int:
        if type(amount) is not int or amount < 0:
            raise FactionEngineError("damage cannot be negative")
        self.hp = max(0, self.hp - amount)
        return self.hp

    @property
    def defeated(self) -> bool:
        return self.hp == 0


class FactionEngine:
    """One world's strategic layer: registered factions, a deterministic order, an audited turn."""

    def __init__(self, *, order_tiebreak: str = "wealth") -> None:
        if order_tiebreak not in ATTRACTION_ORDER:
            raise FactionEngineError("the tiebreak must be one of the faction attributes")
        self.profiles: dict[str, FactionProfile] = {}
        self.order_tiebreak = Attribute(order_tiebreak)
        self.round = 1
        self.acted: set[str] = set()
        self.log: list[dict] = []

    # -- registration -----------------------------------------------------------------
    def register(self, profile: FactionProfile) -> FactionProfile:
        identifier = profile.faction.identifier
        if identifier in self.profiles:
            raise FactionEngineError(f"faction {identifier!r} is already registered")
        self.profiles[identifier] = profile
        self._record("faction.registered", identifier, hp=profile.hp, income=profile.income,
                     force=profile.force, cunning=profile.cunning, wealth=profile.wealth)
        return profile

    def profile(self, identifier: str) -> FactionProfile:
        if identifier not in self.profiles:
            raise FactionEngineError(f"unknown faction {identifier!r}")
        return self.profiles[identifier]

    # -- turn order --------------------------------------------------------------------
    def order(self) -> list[str]:
        """Highest attribute first, tie broken by the configured attribute, then by id.

        Deterministic on purpose: a seeded or shuffled order would make an audited turn impossible to
        replay, and the chapter's initiative is itself an attribute comparison.
        """
        def key(identifier: str) -> tuple:
            profile = self.profiles[identifier]
            best = max(profile.attribute(kind) for kind in map(Attribute, ATTRACTION_ORDER))
            return (-best, -profile.attribute(self.order_tiebreak), identifier)

        return [identifier for identifier in sorted(self.profiles, key=key) if not self.profiles[identifier].defeated]

    # -- actions -----------------------------------------------------------------------
    def action_available(self, identifier: str) -> bool:
        profile = self.profile(identifier)
        return not profile.defeated and identifier not in self.acted and profile.faction.actions_taken == 0

    def act(self, identifier: str, action: str, *, asset_ids: tuple[str, ...] = (),
            target: str = "") -> dict:
        """Record one strategic action, refusing everything the rules disallow."""
        profile = self.profile(identifier)
        if profile.defeated:
            raise FactionEngineError(f"{identifier} has no hit points left to act with")
        if identifier in self.acted:
            raise FactionEngineError(f"{identifier} has already acted this turn")
        if target and target != identifier and target not in self.profiles:
            raise FactionEngineError(f"unknown target faction {target!r}")
        if target == identifier:
            raise FactionEngineError("a faction cannot target itself")
        try:
            event = profile.faction.act(action, asset_ids, target)
        except FactionTurnError as exc:          # one error type reaches the caller
            raise FactionEngineError(str(exc)) from exc
        self.acted.add(identifier)
        self._record("faction.acted", identifier, action=action, assets=list(asset_ids),
                     target=target, credits=profile.faction.credits)
        return event

    def purchase(self, identifier: str, asset: Asset, *, cost: int) -> Asset:
        """Buy an asset. The cost is scenario data; the engine only enforces affordability and caps."""
        profile = self.profile(identifier)
        if identifier in self.acted:
            raise FactionEngineError("purchasing is this turn's action; the faction has already acted")
        try:
            profile.faction.add_asset(asset, cost)
        except FactionTurnError as exc:
            raise FactionEngineError(str(exc)) from exc
        self.acted.add(identifier)
        self._record("faction.purchased", identifier, asset=asset.identifier, cost=cost,
                     credits=profile.faction.credits)
        return asset

    def damage(self, identifier: str, amount: int) -> int:
        remaining = self.profile(identifier).hurt(amount)
        self._record("faction.damaged", identifier, amount=amount, hp=remaining)
        return remaining

    # -- round lifecycle ----------------------------------------------------------------
    def end_round(self) -> dict:
        """Close the turn: income lands, actions reset, the round number advances."""
        summary = {}
        for identifier, profile in self.profiles.items():
            if profile.defeated:
                summary[identifier] = {"income": 0, "credits": profile.faction.credits}
                continue
            profile.faction.next_turn(profile.income)
            summary[identifier] = {"income": profile.income, "credits": profile.faction.credits}
        self._record("round.closed", "engine", round=self.round, payouts=summary)
        self.round += 1
        self.acted.clear()
        for profile in self.profiles.values():
            profile.faction.actions_taken = 0
        return summary

    # -- audit --------------------------------------------------------------------------
    def _record(self, event: str, subject: str, **detail) -> None:
        self.log.append({"round": self.round, "event": event, "subject": subject, **detail})

    def audit(self) -> list[dict]:
        return list(self.log)

    def to_json(self) -> str:
        return json.dumps({"round": self.round, "acted": sorted(self.acted), "log": self.log,
                           "factions": {
                               identifier: {"force": profile.force, "cunning": profile.cunning,
                                            "wealth": profile.wealth, "hp": profile.hp,
                                            "max_hp": profile.max_hp, "income": profile.income,
                                            "credits": profile.faction.credits,
                                            "goal": None if profile.goal is None else
                                            {"kind": profile.goal.kind.value,
                                             "target": profile.goal.target,
                                             "progress": profile.goal.progress,
                                             "needed": profile.goal.needed}}
                               for identifier, profile in self.profiles.items()}},
                          indent=2)


__all__ = ["Asset", "Attribute", "Faction", "FactionEngine", "FactionEngineError", "FactionProfile",
           "FactionTurnError", "Goal", "GoalKind"]
