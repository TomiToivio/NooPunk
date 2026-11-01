"""Faction rank, scoped reputation and goals — the Phase 1 overlay of #1008.

Three rules shape this module, and each exists because the alternative is a game that lies to its player:

1. **Rank is authority, not skill.** It grants permission to lead a mission of N agents. It does not grant a
   bonus to a check, a free skill level, or an extra SWN faction action.
2. **Reputation is scoped and singular.** A scope is a network or a named person. When a reaction is rolled the
   caller must choose exactly one reputation; summing UNSA + SuomiNet + Hype + a supervisor is how a character
   becomes universally loved by doing nothing.
3. **Zero means unknown.** Not hostile, not friendly.

CWN remains untouched: `reaction()` adds the overlay modifier to the published 2d6 result, and nothing here
replaces a CWN procedure.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Iterable

#: Rank 0-4, and how many agents that rank may command in the field. None means "not a head-count limit":
#: local and global authority are governed by the chain of command, not by arithmetic.
RANK_SCOPE: dict[int, int | None] = {0: 1, 1: 2, 2: 4, 3: None, 4: None}
RANK_TITLES = {0: "Rookie agent", 1: "Experienced agent", 2: "Team leader",
               3: "Local manager", 4: "Global manager"}

REPUTATION_RANGE = (-4, 4)


class SocialError(ValueError):
    """A rule was about to be broken: out of range, ambiguous scope, or missing authority."""


@dataclass(frozen=True)
class Membership:
    organization: str
    rank: int = 0
    standing: int = 0          # internal record; deliberately separate from reputation
    promotions: tuple[str, ...] = ()

    def __post_init__(self):
        if self.rank not in RANK_SCOPE:
            raise SocialError(f"rank {self.rank} is outside 0..4")

    @property
    def title(self) -> str:
        return RANK_TITLES[self.rank]

    @property
    def max_agents(self) -> int | None:
        return RANK_SCOPE[self.rank]

    def may_command(self, agents: int) -> bool:
        """Authority to *propose and lead* a mission. Never a guarantee of success or of resources."""
        if agents < 1:
            raise SocialError("a mission needs at least one agent")
        limit = self.max_agents
        return True if limit is None else agents <= limit

    def promote(self, *, reason: str, authorized_by: str) -> "Membership":
        """Promotion is an audited event, not a number that moves on its own."""
        if self.rank >= 4:
            raise SocialError("rank 4 is the top of this track")
        if not reason or not authorized_by:
            raise SocialError("a promotion needs a reason and an authority")
        return Membership(self.organization, self.rank + 1, self.standing,
                          self.promotions + (f"{reason} ({authorized_by})",))


@dataclass(frozen=True)
class Reputation:
    """One value, one scope. `scope` is a network name or `npc:<id>`."""
    scope: str
    value: int
    visibility: str = "public"      # public | private | secret
    evidence: str = ""
    updated: str = ""

    def __post_init__(self):
        lo, hi = REPUTATION_RANGE
        if not lo <= self.value <= hi:
            raise SocialError(f"reputation {self.value} outside {lo}..{hi}")
        if self.visibility not in ("public", "private", "secret"):
            raise SocialError(f"unknown visibility {self.visibility!r}")
        if not self.scope:
            raise SocialError("reputation needs a scope")

    def known_to(self, viewer_scope: str, *, shares_secret: bool = False) -> bool:
        """Public is visible to everyone; private and secret are visible inside their own scope.

        `shares_secret` is for the case that matters in play: someone from outside the scope has been told.
        """
        if self.visibility == "public":
            return True
        if self.scope == viewer_scope:
            return True
        return bool(shares_secret)


def reaction_modifier(reputations: Iterable[Reputation], *, chosen_scope: str) -> int:
    """Exactly one reputation may apply, and the caller must say which.

    Summing scopes is the abuse this refuses: a character with +2 in four networks would otherwise reach +8 on
    a 2d6 roll, which is not a modifier any more, it is a different game.
    """
    candidates = [r for r in reputations if r.scope == chosen_scope]
    if not candidates:
        raise SocialError(f"no reputation recorded for scope {chosen_scope!r}")
    if len(candidates) > 1:
        raise SocialError(f"ambiguous scope {chosen_scope!r}: {len(candidates)} records")
    return candidates[0].value


def reaction(dice: tuple[int, int], charisma_modifier: int, reputation_value: int = 0,
             *, known: bool = True) -> dict:
    """CWN's 2d6 reaction, with the NoöPunk reputation overlay applied once.

    `known=False` means the NPC does not know the character's reputation, so the overlay does not apply. The
    modifier shapes *initial disposition* only; it is not mind control.
    """
    if len(dice) != 2 or not all(1 <= d <= 6 for d in dice):
        raise SocialError("reaction uses two d6")
    if not -3 <= charisma_modifier <= 4:
        raise SocialError("charisma modifier outside the CWN range")
    overlay = reputation_value if known else 0
    total = dice[0] + dice[1] + charisma_modifier + overlay
    if total <= 2:
        band = "as hostile as plausible"
    elif total <= 5:
        band = "hostile/unfriendly"
    elif total <= 8:
        band = "neutral"
    elif total <= 11:
        band = "unusually friendly/cooperative"
    else:
        band = "as friendly/helpful as plausible"
    return {"total": total, "band": band, "overlay_applied": overlay}


@dataclass
class Goal:
    """A descriptive tag with a state machine attached, not a stat bonus."""
    owner: str
    text: str
    kind: str = "personal"          # personal | faction
    status: str = "open"            # open | active | done | failed | abandoned
    priority: int = 3
    depends_on: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.owner or not self.text:
            raise SocialError("a goal needs an owner and a statement")
        if self.kind not in ("personal", "faction"):
            raise SocialError(f"unknown goal kind {self.kind!r}")
        if self.status not in ("open", "active", "done", "failed", "abandoned"):
            raise SocialError(f"unknown goal status {self.status!r}")


@dataclass
class SocialRecord:
    """What gets persisted: membership, reputation list, goals. Round-trips through JSON."""
    memberships: list[Membership] = field(default_factory=list)
    reputations: list[Reputation] = field(default_factory=list)
    goals: list[Goal] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"memberships": [asdict(m) for m in self.memberships],
                "reputations": [asdict(r) for r in self.reputations],
                "goals": [asdict(g) for g in self.goals]}

    @classmethod
    def from_dict(cls, data: dict) -> "SocialRecord":
        return cls(
            memberships=[Membership(m["organization"], m.get("rank", 0), m.get("standing", 0),
                                    tuple(m.get("promotions", ()))) for m in data.get("memberships", [])],
            reputations=[Reputation(r["scope"], r["value"], r.get("visibility", "public"),
                                    r.get("evidence", ""), r.get("updated", ""))
                         for r in data.get("reputations", [])],
            goals=[Goal(g["owner"], g["text"], g.get("kind", "personal"), g.get("status", "open"),
                        g.get("priority", 3), list(g.get("depends_on", [])))
                   for g in data.get("goals", [])])

    def membership(self, organization: str) -> Membership:
        for m in self.memberships:
            if m.organization == organization:
                return m
        raise SocialError(f"no membership in {organization!r}")

    def visible_reputations(self, viewer_scope: str, *, shares_secret: bool = False) -> list[Reputation]:
        return [r for r in self.reputations if r.known_to(viewer_scope, shares_secret=shares_secret)]
