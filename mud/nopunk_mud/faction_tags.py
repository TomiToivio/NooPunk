"""Issue #1008: additive faction authority, scoped reputation and goals.

Pure Python state handlers. Evennia persists the returned dictionaries in Attributes.
No CWN skill, roll, SWN faction turn or advancement rule is replaced.
"""
from __future__ import annotations

from copy import deepcopy

RANKS = ("Rookie agent", "Experienced agent", "Team leader", "Local manager", "Global manager")
NETWORKS = {
    "UNSA": "International UNSA institutional network",
    "SipuliVerkko": "Finnish criminal darknet",
    "SuomiNet": "Finnish public safe network",
    "Internet": "Isolated hostile legacy AI network; access is dangerous",
    "MarsNet Hype": "Solar-system-wide Mars Eldrich social network",
}
SCOPES = {"network", "faction", "local", "person"}
VISIBILITIES = {"public", "member", "private", "secret"}
GOAL_STATES = {"active", "completed", "failed", "abandoned"}
AUTHORITY = ("individual", "partner", "team", "local", "global")
REWARDS = (
    {"equipment": "standard issue", "training": "academy", "salary": "rookie"},
    {"equipment": "field issue", "training": "field", "salary": "experienced"},
    {"equipment": "team requisition", "training": "leadership", "salary": "team leader"},
    {"equipment": "local requisition", "training": "management", "salary": "local manager"},
    {"equipment": "strategic requisition", "training": "strategy", "salary": "global manager"},
)


def initial_state() -> dict:
    return {
        "memberships": {"UNSA": {"rank": 0, "active": True, "history": []}},
        "reputations": {},
        "goals": {},
        "traits": [],
        "audit": [],
    }


def normalize(raw: dict | None) -> dict:
    state = initial_state() if raw is None else deepcopy(raw)
    if not isinstance(state, dict):
        raise ValueError("Invalid faction state")
    for key, default in initial_state().items():
        state.setdefault(key, deepcopy(default))
    return state


def _log(state, action, detail):
    state["audit"].append({"action": action, "detail": detail})


def rank(state: dict, faction="UNSA") -> int | None:
    membership = state["memberships"].get(faction)
    return membership["rank"] if membership and membership["active"] else None


def can_command(state: dict, kind: str, *, available_agents: int = 1, authorized: bool = True, faction="UNSA") -> bool:
    """Rank permits a request, never generates staff or an SWN faction action."""
    if kind not in AUTHORITY or not authorized or available_agents < 1:
        return False
    level = rank(state, faction)
    if level is None or level < AUTHORITY.index(kind):
        return False
    if kind == "partner":
        return available_agents >= 2
    if kind == "team":
        return available_agents >= 4
    return True


def promote(state: dict, faction: str, next_rank: int, *, approved: bool, xp_award: int = 0) -> dict:
    """Game/admin-approved promotion; XP award is a *request* for CWN progression."""
    current = rank(state, faction)
    if not approved or current is None or not isinstance(next_rank, int) or next_rank != current + 1 or next_rank > 4:
        raise ValueError("Promotion requires an authorized single-rank increase")
    if not isinstance(xp_award, int) or xp_award < 0:
        raise ValueError("Invalid XP award")
    state["memberships"][faction]["rank"] = next_rank
    state["memberships"][faction]["history"].append({"from": current, "to": next_rank, "xp_award_pending": xp_award})
    _log(state, "promote", {"faction": faction, "rank": next_rank, "xp_award_pending": xp_award})
    return dict(REWARDS[next_rank], xp_award_pending=xp_award)


def set_reputation(state: dict, scope: str, subject: str, value: int, *,
                   known: bool = True, visibility: str = "public", evidence: str = "", actor: str = "system"):
    if scope not in SCOPES or not subject.strip() or visibility not in VISIBILITIES:
        raise ValueError("Invalid reputation scope, subject or visibility")
    if type(value) is not int or not -4 <= value <= 4:
        raise ValueError("Reputation must be an integer from -4 to +4")
    key = f"{scope}:{subject}"
    state["reputations"][key] = {"scope": scope, "subject": subject, "value": value,
                                 "known": bool(known), "visibility": visibility, "evidence": evidence}
    _log(state, "reputation", {"key": key, "value": value, "actor": actor})


def visible_reputations(state: dict, *, viewer: str = "public"):
    allowed = {"public"} if viewer == "public" else {"public", "member"} if viewer == "member" else VISIBILITIES
    return {k: v for k, v in state["reputations"].items() if v["visibility"] in allowed}


def reputation_modifier(state: dict, scope: str, subject: str, *, npc_knows: bool) -> int:
    """Exactly one explicitly selected relevant tag, never stacked."""
    entry = state["reputations"].get(f"{scope}:{subject}")
    return entry["value"] if npc_knows and entry and entry["known"] else 0


def reaction(total_2d6: int, charisma_modifier: int = 0, reputation: int = 0):
    """Additive reputation overlay on an externally supplied CWN 2d6 roll.

    The calling CWN adapter must supply its actual applicable Charisma modifier
    once; do not call this on an already Charisma-adjusted total.
    """
    if not 2 <= total_2d6 <= 12 or not -4 <= reputation <= 4:
        raise ValueError("Invalid reaction input")
    score = total_2d6 + charisma_modifier + reputation
    category = ("hostile/violent" if score <= 2 else
                "hostile/unfriendly" if score <= 5 else
                "neutral" if score <= 8 else
                "friendly/cooperative" if score <= 11 else "very helpful")
    return score, category


def set_goal(state: dict, goal_id: str, description: str, *, owner: str = "PC",
             status: str = "active", priority: int = 1, visibility: str = "private"):
    if not goal_id or not description.strip() or status not in GOAL_STATES or visibility not in VISIBILITIES or not 0 <= priority <= 4:
        raise ValueError("Invalid goal")
    state["goals"][goal_id] = {"description": description, "owner": owner, "status": status,
                               "priority": priority, "visibility": visibility}
    _log(state, "goal", {"id": goal_id, "status": status})


def visible_goals(state: dict, *, viewer: str = "owner"):
    allowed = {"public"} if viewer == "public" else {"public", "member"} if viewer == "member" else VISIBILITIES
    return {k: v for k, v in state["goals"].items() if v["visibility"] in allowed}
