"""NoöPunk faction authority, scoped reputation and goal overlay (#1008).

This module does not modify CWN character rules or SWN faction turns.
It is deterministic and serializable; only authorized callers may mutate its ledger.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone

NETWORKS = ("UNSA", "SipuliVerkko", "SuomiNet", "Internet", "MarsNet Hype")
RANKS = ("Rookie agent", "Experienced agent", "Team leader",
         "Local manager", "Global manager")
SCOPES = ("network", "faction", "community", "npc")
VISIBILITIES = ("public", "private", "secret")
GOAL_STATES = ("active", "complete", "failed", "abandoned")


def _range(value: int, low: int, high: int) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"expected integer from {low} to {high}")
    return value


@dataclass
class Membership:
    faction: str
    rank: int = 0
    active: bool = True
    suspended: bool = False
    history: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.faction:
            raise ValueError("faction is required")
        _range(self.rank, 0, 4)

    def can_lead(self, agents: int, *, local: bool = False, global_: bool = False) -> bool:
        if not self.active or self.suspended or type(agents) is not int or agents < 1:
            return False
        if global_:
            return self.rank == 4
        if local:
            return self.rank >= 3
        return agents <= (1, 2, 4, 4, 4)[self.rank]


@dataclass
class Reputation:
    scope: str
    target: str
    score: int = 0
    visibility: str = "public"
    evidence: list[str] = field(default_factory=list)
    changed_at: str | None = None

    def __post_init__(self):
        if self.scope not in SCOPES or not self.target:
            raise ValueError("invalid reputation scope or target")
        if self.visibility not in VISIBILITIES:
            raise ValueError("invalid visibility")
        _range(self.score, -4, 4)


@dataclass
class Goal:
    id: str
    description: str
    owner: str
    target: str = ""
    status: str = "active"
    priority: int = 0
    dependencies: list[str] = field(default_factory=list)
    progress: int = 0

    def __post_init__(self):
        if not self.id or not self.description or not self.owner:
            raise ValueError("goal requires id, description and owner")
        if self.status not in GOAL_STATES:
            raise ValueError("invalid goal status")
        _range(self.progress, 0, 100)


@dataclass
class FactionOverlay:
    memberships: dict[str, Membership] = field(default_factory=dict)
    reputations: dict[str, Reputation] = field(default_factory=dict)
    goals: dict[str, Goal] = field(default_factory=dict)
    audit: list[dict] = field(default_factory=list)

    @classmethod
    def rookie(cls) -> "FactionOverlay":
        return cls(memberships={"UNSA": Membership("UNSA")})

    @staticmethod
    def key(scope: str, target: str) -> str:
        if scope not in SCOPES or not target or ":" in scope:
            raise ValueError("invalid scope/target")
        return f"{scope}:{target}"

    def set_reputation(self, scope: str, target: str, score: int, *,
                       visibility: str = "public", evidence: str = "",
                       actor: str = "system") -> None:
        key = self.key(scope, target)
        old = self.reputations.get(key)
        if old and old.visibility == "secret" and actor != "admin":
            raise PermissionError("secret reputation requires administrator")
        if not evidence.strip():
            raise ValueError("reputation change needs evidence")
        entry = Reputation(scope, target, score, visibility,
                           (old.evidence if old else []) + [evidence],
                           datetime.now(timezone.utc).isoformat())
        self.reputations[key] = entry
        self.audit.append({"action": "reputation", "key": key, "old": old.score if old else 0,
                           "new": score, "actor": actor, "evidence": evidence})

    def visible_reputations(self, *, include_private: bool = False,
                            admin: bool = False) -> dict[str, Reputation]:
        return {key: value for key, value in self.reputations.items()
                if admin or value.visibility == "public"
                or (include_private and value.visibility == "private")}

    def reaction_modifier(self, known_targets: list[tuple[str, str]], *,
                          max_magnitude: int = 2) -> int:
        """Use the first *known, relevant* scope only. Never sum networks.

        Returns an optional NoöPunk modifier for an external canonical CWN roll.
        The caller establishes what an NPC actually knows; no automatic omniscience.
        """
        _range(max_magnitude, 0, 4)
        for scope, target in known_targets:
            reputation = self.reputations.get(self.key(scope, target))
            if reputation is not None:
                return max(-max_magnitude, min(max_magnitude, reputation.score))
        return 0

    def promote(self, faction: str, rank: int, *, authorized: bool,
                evidence: str, actor: str) -> None:
        if not authorized or not evidence.strip() or not actor.strip():
            raise PermissionError("promotion requires authorization and recorded evidence")
        member = self.memberships[faction]
        _range(rank, 0, 4)
        if not member.active or member.suspended or rank != member.rank + 1:
            raise ValueError("promotion requires active member and exactly one higher rank")
        member.history.append({"from": member.rank, "to": rank, "actor": actor,
                               "evidence": evidence})
        member.rank = rank
        self.audit.append({"action": "promotion", "faction": faction, "rank": rank})

    def add_goal(self, goal: Goal) -> None:
        if goal.id in self.goals:
            raise ValueError("goal already exists")
        if goal.id in goal.dependencies:
            raise ValueError("self-dependency")
        self.goals[goal.id] = goal
        self.audit.append({"action": "goal_added", "id": goal.id})

    def snapshot(self) -> dict:
        return {"version": 1, "memberships": {k: asdict(v) for k, v in self.memberships.items()},
                "reputations": {k: asdict(v) for k, v in self.reputations.items()},
                "goals": {k: asdict(v) for k, v in self.goals.items()},
                "audit": list(self.audit)}

    @classmethod
    def from_snapshot(cls, data: dict) -> "FactionOverlay":
        if data.get("version") != 1:
            raise ValueError("unsupported overlay snapshot")
        result = cls(
            {k: Membership(**v) for k, v in data.get("memberships", {}).items()},
            {k: Reputation(**v) for k, v in data.get("reputations", {}).items()},
            {k: Goal(**v) for k, v in data.get("goals", {}).items()},
            list(data.get("audit", [])))
        if any(k != result.key(v.scope, v.target) for k, v in result.reputations.items()):
            raise ValueError("reputation key mismatch")
        return result
