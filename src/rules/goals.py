"""The NoöPunk **Goal** tag (#1119): one tag, one lifecycle, CWN still authoritative.

A goal is a line on a character or faction sheet, not a new engine:

    Goal: <description> | owner: <character/faction> | horizon: short / medium / long | status: <note>

Why this is not in `rules/tags.py` or `rules/noopunk_tags.py`: those modules implement the **retired**
NoöPunk prototype chassis (`STAT + Skill + 1d10`, a 1-10 attribute scale) that the #1068 audit replaced
with CWN. Attaching a campaign objective to the retired resolver would give the repository a second
answer to "what is a tag". This module therefore stores goals **beside** a CWN character, changes no
attribute, roll, save or hit point, and hands experience to `cwn_advancement`, which owns the XP table.

The rules, as the issue states them:

* **Three horizons.** ``short`` completes in a scene or a case, ``medium`` takes several scenarios,
  ``long`` is a direction of action that may never close.
* **A goal never rolls.** Resolution uses unmodified CWN.
* **Completion retires the tag** (short/medium); a long goal stays active and records distinct
  contributions.
* **XP is CWN's XP.** One qualifying contribution is *typically* one point, awarded through
  `cwn_advancement.level_for_xp`; there is no second currency and no second level table.
* **Anti-farming.** A given event may pay its owner **once**, even when it advances several goals. The
  ledger keys on ``(owner, event)``, not on the goal.
* **Factions never receive character XP.** They earn permissions, assets or standing, recorded as text.
* **Failure and abandonment pay nothing**, and deleting a tag is not a reward.
* **Disabling the tag erases nothing**: the history stays in the save; only the active list empties.

Deliberately absent, per the issue: personality, mental state, reputation, bionics, psychotronics, a
generic tag engine, a rules DSL, goal dice, or a universal reward optimiser. Those are later issues,
each with its own playable example.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

from src.rules import cwn_advancement

FORMAT = "noopunk.rules.goals"
VERSION = 1

HORIZONS = ("short", "medium", "long")
OWNER_KINDS = ("character", "faction")
STATUSES = ("active", "completed", "failed", "abandoned")

#: What can be recorded against a goal. ``progress`` is bookkeeping; only ``completed`` (short/medium)
#: and ``contribution`` (long) can carry a reward, which is what stops "we did something" from paying.
PROGRESS_KINDS = ("progress", "contribution", "completed", "failed", "abandoned")

#: The issue's "typically 1 XP" made operational: an award is at least one point and never a jackpot.
#: The upper bound is a guard against typos, not a balance ruling; a campaign that wants a larger one
#: makes that choice in its own reward procedure.
MIN_AWARD = 1
MAX_AWARD = 3


class GoalError(ValueError):
    """A rule was about to be broken."""


@dataclass(frozen=True)
class Goal:
    """One tag. Frozen: a status change is a recorded event, not an edit of the past."""

    id: str
    owner: str
    owner_kind: str
    description: str
    horizon: str
    status: str = "active"
    created: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise GoalError("a goal needs an id")
        if not self.owner.strip():
            raise GoalError("a goal needs an owner")
        if self.owner_kind not in OWNER_KINDS:
            raise GoalError(f"owner_kind must be one of {OWNER_KINDS}, not {self.owner_kind!r}")
        if self.horizon not in HORIZONS:
            raise GoalError(f"horizon must be one of {HORIZONS}, not {self.horizon!r}")
        if self.status not in STATUSES:
            raise GoalError(f"status must be one of {STATUSES}, not {self.status!r}")
        if not self.description.strip():
            raise GoalError("a goal needs a description a player can read on paper")

    @property
    def is_active(self) -> bool:
        return self.status == "active"


@dataclass(frozen=True)
class Progress:
    """One dated thing that happened to a goal: the evidence, not an opinion."""

    goal: str
    kind: str
    event: str
    date: str = ""
    note: str = ""

    def __post_init__(self) -> None:
        if self.kind not in PROGRESS_KINDS:
            raise GoalError(f"progress kind must be one of {PROGRESS_KINDS}, not {self.kind!r}")
        if not self.event.strip():
            raise GoalError("progress needs the event that evidences it; that is the anti-farming key")


@dataclass(frozen=True)
class Award:
    """A reward that was actually paid, with the CWN level it implies."""

    goal: str
    event: str
    xp: int
    level: int
    date: str = ""
    perk: str = ""


@dataclass
class GoalLog:
    """Every goal, its history and the XP paid out. One log per campaign."""

    enabled: bool = True
    goals: list[Goal] = field(default_factory=list)
    progress: list[Progress] = field(default_factory=list)
    awards: list[Award] = field(default_factory=list)
    perks: list[dict] = field(default_factory=list)

    # ---- authoring -------------------------------------------------------
    def add(self, goal: Goal) -> Goal:
        if any(existing.id == goal.id for existing in self.goals):
            raise GoalError(f"goal {goal.id!r} already exists; ids are permanent")
        self.goals.append(goal)
        return goal

    def goal(self, goal_id: str) -> Goal:
        for existing in self.goals:
            if existing.id == goal_id:
                return existing
        raise GoalError(f"unknown goal {goal_id!r}")

    def active(self, owner: str | None = None) -> list[Goal]:
        """The tags still on the sheet. Empty while the mod is off, without deleting anything."""
        if not self.enabled:
            return []
        return [g for g in self.goals
                if g.is_active and (owner is None or g.owner == owner)]

    def retired(self) -> list[Goal]:
        return [g for g in self.goals if not g.is_active]

    # ---- the lifecycle ---------------------------------------------------
    def record(self, goal_id: str, kind: str, event: str, *, date: str = "",
               note: str = "") -> Goal:
        """Record one progress event and apply the status change it implies.

        ``completed``/``failed``/``abandoned`` retire the tag. ``contribution`` is reserved for long
        horizons, because that is the one place the issue lets a *contribution* pay while the goal
        stays open; a short goal earns by completing, not by trying.
        """
        goal = self.goal(goal_id)
        if not goal.is_active:
            raise GoalError(f"goal {goal_id!r} is {goal.status}; record history, not a new status")
        entry = Progress(goal=goal_id, kind=kind, event=event, date=date, note=note)
        if kind == "contribution" and goal.horizon != "long":
            raise GoalError(
                "only a long-horizon goal can record a contribution: a short or medium goal earns by "
                "completing, or every attempt becomes a payday")
        self.progress.append(entry)
        if kind in ("completed", "failed", "abandoned"):
            retired = Goal(**{**asdict(goal), "status": kind})
            self.goals[self.goals.index(goal)] = retired
            return retired
        return goal

    # ---- rewards ---------------------------------------------------------
    def award_xp(self, goal_id: str, event: str, *, xp: int = MIN_AWARD, date: str = "",
                 track: str = "fast") -> Award:
        """Pay CWN experience for a recorded completion or contribution.

        Refusals, each of which is a way a tag would otherwise become a second economy:

        * a **faction** owner — a faction is not a CWN character;
        * an event that is not recorded against this goal as ``completed`` or ``contribution``;
        * an event the **owner has already been paid for**, on this goal or any other;
        * an award outside 1..3 points, which is a typo guard, not a balance ruling.
        """
        goal = self.goal(goal_id)
        if goal.owner_kind == "faction":
            raise GoalError(
                f"{goal.owner} is a faction: faction rewards are assets, access or standing, not "
                "character experience — record them with award_perk()")
        supporting = [p for p in self.progress if p.goal == goal_id and p.event == event]
        if not supporting:
            raise GoalError(f"no recorded progress for {event!r} on {goal_id!r}: award the evidence, not the mood")
        if supporting[-1].kind not in ("completed", "contribution"):
            raise GoalError(
                f"{event!r} is recorded as {supporting[-1].kind!r}; only a completed goal or a "
                "long-horizon contribution can be rewarded")
        if not MIN_AWARD <= int(xp) <= MAX_AWARD:
            raise GoalError(f"an award is {MIN_AWARD}..{MAX_AWARD} XP, got {xp}")
        if any(a.event == event and self.goal(a.goal).owner == goal.owner for a in self.awards):
            raise GoalError(
                f"{goal.owner} has already been paid for {event!r}: one event pays once, however many "
                "goals it advanced")
        total = self.xp_for(goal.owner) + int(xp)
        award = Award(goal=goal_id, event=event, xp=int(xp),
                      level=cwn_advancement.level_for_xp(total, track=track), date=date)
        self.awards.append(award)
        return award

    def award_perk(self, goal_id: str, text: str, event: str, *, date: str = "") -> dict:
        """Record a fictional, social or material consequence. The tag never grants a mechanic."""
        goal = self.goal(goal_id)
        if not text.strip():
            raise GoalError("a perk needs the consequence written down, or it did not happen")
        row = {"goal": goal.id, "owner": goal.owner, "event": event, "text": text.strip(), "date": date}
        if any(p["goal"] == goal.id and p["event"] == event and p["text"] == row["text"]
               for p in self.perks):
            raise GoalError("that perk is already recorded for this event")
        self.perks.append(row)
        return row

    def xp_for(self, owner: str) -> int:
        return sum(a.xp for a in self.awards if self.goal(a.goal).owner == owner)

    def level_for(self, owner: str, *, track: str = "fast") -> int:
        """The CWN level the awarded XP implies — the existing table, not a second one."""
        return cwn_advancement.level_for_xp(self.xp_for(owner), track=track)

    def perks_for(self, owner: str) -> list[dict]:
        return [p for p in self.perks if p["owner"] == owner]

    # ---- paper -----------------------------------------------------------
    def paper(self, goal_id: str) -> str:
        """The sheet line, exactly as the issue writes it."""
        goal = self.goal(goal_id)
        note = goal.status
        if goal.is_active:
            latest = [p for p in self.progress if p.goal == goal_id]
            note = latest[-1].note or latest[-1].kind if latest else "in progress"
        return (f"Goal: {goal.description} | owner: {goal.owner} | horizon: {goal.horizon} "
                f"| status: {note}")

    # ---- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "format": FORMAT,
            "version": VERSION,
            "enabled": self.enabled,
            "goals": [asdict(g) for g in self.goals],
            "progress": [asdict(p) for p in self.progress],
            "awards": [asdict(a) for a in self.awards],
            "perks": [dict(p) for p in self.perks],
        }

    @classmethod
    def from_dict(cls, data: dict | None) -> GoalLog:
        """Read a save. An absent log is an empty log: older saves simply have no goals."""
        if not data:
            return cls()
        if data.get("format") != FORMAT:
            raise GoalError(f"{data.get('format')!r} is not a goal log")
        return cls(
            enabled=bool(data.get("enabled", True)),
            goals=[Goal(**row) for row in data.get("goals", [])],
            progress=[Progress(**row) for row in data.get("progress", [])],
            awards=[Award(**row) for row in data.get("awards", [])],
            perks=[dict(row) for row in data.get("perks", [])],
        )


# --------------------------------------------------------------------------- #
# Module-level hooks — the surface the mod contract declares and a scenario calls
# --------------------------------------------------------------------------- #


def add_goal(log: GoalLog, goal: Goal) -> Goal:
    """Attach one tag to a character or faction sheet."""
    return log.add(goal)


def record_progress(log: GoalLog, goal_id: str, kind: str, event: str, *, date: str = "",
                    note: str = "") -> Goal:
    """Record the evidence that something happened, and the status change it implies."""
    return log.record(goal_id, kind, event, date=date, note=note)


def award_xp(log: GoalLog, goal_id: str, event: str, *, xp: int = MIN_AWARD, date: str = "",
             track: str = "fast") -> Award:
    """Pay CWN experience for a recorded completion or long-horizon contribution."""
    return log.award_xp(goal_id, event, xp=xp, date=date, track=track)


def paper_line(log: GoalLog, goal_id: str) -> str:
    """The line the player writes on the sheet."""
    return log.paper(goal_id)
