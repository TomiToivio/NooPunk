"""AWN regions as a two-level world model (#1045).

Source: *Ashes Without Number* printed pp. 136–151 (campaign creation, crises, regions), with the
NoöPunk-side design recorded in `docs/design/ISSUE_1045_AWN_INVENTORY_ASSESSMENT.md`. AWN has **no
verified open licence** in this repository, so nothing here reproduces book text: this module models
the *procedure NoöPunk adopted* (collapse is per location, transitions are dated events, recovery is
real) and leaves every AWN table to the caller.

Why the module exists at all: CWN is the character-scale engine and SWN owns faction turns. NoöPunk
canon is a *globally shared ontological apocalypse with uneven material collapse* — most of the world
still works, and only the worst-hit localities are an After-the-Fall setting. Without a region layer
that difference has nowhere to live, and every session either plays fully functional CWN or pretends
the whole world ended.

The five rules the model enforces, each with a test that would fail if it were dropped:

1. A region that is **functioning** on every material axis, with no anomaly, plays as ordinary CWN:
   `active_overlays()` returns nothing.
2. An **after_the_fall** region activates the AWN overlays this project marks P0 (travel and supplies,
   privation strain, encounter-site hazards). Those overlays are *additive*: they add strain and
   bookkeeping, they never change a CWN procedure.
3. A change requires a **dated event with a cause**. There is no clock: `transition()` refuses a
   transition that does not name the event that caused it.
4. **Recovery is real** and is the point: a region can climb back one rung at a time, and it can fall
   several rungs at once. Collapse is fast, repair is slow.
5. The **world layer** is an aggregate of region states, not a second simulation: crisis campaigns are
   runs of dated events, and the aggregate is derived, never authored.

CWN is untouched. Nothing here rolls dice, changes an attribute or resolves a check.
"""
from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from dataclasses import asdict, dataclass, field
from typing import Any

#: Material axes, best to worst. Index is severity, which is what the transition rule reads.
LADDER = ("functioning", "recovering", "emergency", "after_the_fall")

#: Governance additionally allows a contested administration, which is not a severity rung.
GOVERNANCE_VALUES = LADDER + ("contested",)

#: Anomaly intensity is a separate axis: a functioning city can still have a breached undercity.
ANOMALY_LADDER = ("none", "sporadic", "persistent", "breached")
SHOCK_LADDER = ("none", "local", "regional", "global")

MATERIAL_AXES = ("physical_infrastructure", "public_safety", "supplies", "communications")
TRANSITION_AXES = MATERIAL_AXES + ("governance", "anomaly", "ontological_shock")

#: Overlays a region turns on when it is no longer functioning. Names match the P0 rows of the AWN
#: inventory; each one is additive and none of them edits a CWN rule.
OVERLAYS = {
    "after_the_fall": ("travel_and_supplies", "privation_strain", "site_hazards"),
    "emergency": ("privation_strain",),
    "recovering": (),
    "functioning": (),
}


class RegionError(ValueError):
    """A rule was about to be broken: unknown axis value, undated transition, skipped recovery."""


def _valid_date(value: str) -> bool:
    """Lexical ordering is only safe for canonical ISO calendar dates."""
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


@dataclass(frozen=True)
class RegionState:
    """One region's dated condition. Frozen: a new condition is a new record, never an edit."""

    region: str
    date: str
    physical_infrastructure: str
    public_safety: str
    supplies: str
    communications: str
    governance: str = "functioning"
    anomaly: str = "none"
    ontological_shock: str = "none"

    def __post_init__(self) -> None:
        if not self.region:
            raise RegionError("a region state needs a region id")
        if not _valid_date(self.date):
            raise RegionError("region state date must be ISO YYYY-MM-DD")
        for axis in MATERIAL_AXES:
            value = getattr(self, axis)
            if value not in LADDER:
                raise RegionError(f"{axis} must be one of {LADDER}, not {value!r}")
        if self.governance not in GOVERNANCE_VALUES:
            raise RegionError(f"governance must be one of {GOVERNANCE_VALUES}, not {self.governance!r}")
        if self.anomaly not in ANOMALY_LADDER:
            raise RegionError(f"anomaly must be one of {ANOMALY_LADDER}, not {self.anomaly!r}")
        if self.ontological_shock not in SHOCK_LADDER:
            raise RegionError(
                f"ontological_shock must be one of {SHOCK_LADDER}, not {self.ontological_shock!r}")

    def axis(self, name: str) -> str:
        if name not in TRANSITION_AXES:
            raise RegionError(f"unknown axis {name!r}")
        return str(getattr(self, name))

    @property
    def is_functioning(self) -> bool:
        """Ordinary CWN play: every material axis works and nothing anomalous is loose."""
        return (all(self.axis(a) == "functioning" for a in MATERIAL_AXES)
                and self.governance == "functioning"
                and self.anomaly == "none")

    def active_overlays(self, *, awn_enabled: bool = True) -> tuple[str, ...]:
        """Optional AWN eligibility; disabled means no AWN effects, not erasure of history.

        This toggle scopes only AWN-specific effects. CWN remains authoritative and any
        independently enabled SWN/WWN rules keep their own activation contracts.
        """
        if not awn_enabled or self.is_functioning:
            return ()
        worst = max((self.axis(a) for a in MATERIAL_AXES), key=LADDER.index)
        overlays = set(OVERLAYS[worst])
        if self.anomaly != "none":
            overlays.add("anomaly_response")
        return tuple(sorted(overlays))


def _severity(value: str) -> int:
    """Index on the ladder; ``contested`` sits beside ``emergency`` for comparison purposes."""
    if value == "contested":
        return LADDER.index("emergency")
    return LADDER.index(value)


def transition_allowed(before: str, after: str) -> bool:
    """Collapse may skip rungs; recovery may not.

    A breach, a convoy lost or a quarantine can drop a region from functioning to after_the_fall in
    one event. Climbing back has to be earned one rung at a time — otherwise "recovery" is a single
    generous ruling that erases the campaign's cost.
    """
    if before == after:
        return False
    if before == "contested" or after == "contested":
        return True
    return _severity(after) > _severity(before) or _severity(before) - _severity(after) == 1


@dataclass(frozen=True)
class RegionEvent:
    """The dated cause of a change. No event, no transition."""

    date: str
    region: str
    axis: str | None
    to: str | None
    cause: str
    source: str = ""

    def __post_init__(self) -> None:
        if not _valid_date(self.date) or not self.region:
            raise RegionError("an event needs a region and ISO YYYY-MM-DD date")
        if not isinstance(self.cause, str) or not self.cause.strip():
            raise RegionError("an event needs a cause: 'the clock advanced' is not one")


@dataclass
class RegionLedger:
    """Append-only history of region states, and the world aggregate derived from it."""

    states: list[RegionState] = field(default_factory=list)
    events: list[RegionEvent] = field(default_factory=list)

    # ---- authoring -------------------------------------------------------
    def record(self, state: RegionState) -> None:
        """Append the opening state of a region, or a state reached with an event already recorded."""
        if self.state_at(state.region, state.date) is not None:
            raise RegionError(f"{state.region}: a state is already recorded for {state.date}")
        previous = self.latest(state.region)
        if previous is not None:
            if state.date < previous.date:
                raise RegionError(
                    f"{state.region}: {state.date} precedes {previous.date}; the ledger is dated")
            changed = any(getattr(state, axis) != getattr(previous, axis)
                          for axis in MATERIAL_AXES + ("governance", "anomaly", "ontological_shock"))
            recorded = [e for e in self.events
                        if e.region == state.region and e.date == state.date]
            if changed and not recorded:
                raise RegionError(
                    f"{state.region}: {state.date} changes the region without a recorded event")
        self.states.append(state)

    def transition(self, event: RegionEvent) -> RegionState:
        """Apply one dated, caused change and return the resulting state."""
        current = self.latest(event.region)
        if current is None:
            raise RegionError(f"{event.region}: no state recorded, so there is nothing to transition")
        if event.date < current.date:
            raise RegionError(f"{event.region}: {event.date} precedes {current.date}")
        if event.axis is None or event.to is None:
            raise RegionError("a transition must name the axis and its new value")
        if event.axis not in TRANSITION_AXES:
            raise RegionError(f"unknown transition axis {event.axis!r}")
        before = current.axis(event.axis)
        if event.axis == "governance":
            allowed_values: Iterable[str] = GOVERNANCE_VALUES
        elif event.axis in MATERIAL_AXES:
            allowed_values = LADDER
        else:
            allowed_values = ANOMALY_LADDER if event.axis == "anomaly" else SHOCK_LADDER
        if event.to not in tuple(allowed_values):
            raise RegionError(f"{event.axis} cannot be {event.to!r}")
        if event.axis in ("anomaly", "ontological_shock"):
            ladder = ANOMALY_LADDER if event.axis == "anomaly" else SHOCK_LADDER
            previous, following = ladder.index(before), ladder.index(event.to)
            permitted = following > previous or previous - following == 1
        else:
            permitted = transition_allowed(before, event.to)
        if not permitted:
            raise RegionError(
                f"{event.region}: {event.axis} cannot go from {before} to {event.to} in one event")
        fields = {axis: current.axis(axis)
                  for axis in MATERIAL_AXES + ("governance", "anomaly", "ontological_shock")}
        fields[event.axis] = event.to
        state = RegionState(region=event.region, date=event.date, **fields)
        self.events.append(event)
        self.states.append(state)
        return state

    # ---- reading ---------------------------------------------------------
    def latest(self, region: str) -> RegionState | None:
        rows = [s for s in self.states if s.region == region]
        return max(rows, key=lambda s: s.date) if rows else None

    def state_at(self, region: str, date: str) -> RegionState | None:
        rows = [s for s in self.states if s.region == region and s.date <= date]
        return max(rows, key=lambda s: s.date) if rows else None

    def regions(self) -> list[str]:
        return sorted({s.region for s in self.states})

    def world_at(self, date: str, *, awn_enabled: bool = True) -> dict[str, Any]:
        """The world layer: a derived aggregate, never a second authored state."""
        current: dict[str, RegionState] = {}
        for region in self.regions():
            state = self.state_at(region, date)
            if state is not None:
                current[region] = state
        counts: dict[str, int] = {value: 0 for value in LADDER}
        for state in current.values():
            worst = max((state.axis(a) for a in MATERIAL_AXES), key=LADDER.index)
            counts[worst] += 1
        return {
            "date": date,
            "regions": len(current),
            "by_worst_material_axis": counts,
            "functioning": sorted(r for r, s in current.items() if s.is_functioning),
            "overlays": {r: list(s.active_overlays(awn_enabled=awn_enabled)) for r, s in sorted(current.items())
                         if s.active_overlays(awn_enabled=awn_enabled)},
            "anomaly": {r: s.anomaly for r, s in sorted(current.items()) if s.anomaly != "none"},
            "treats_collapse_as_global": False,
        }

    # ---- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        return {"states": [asdict(s) for s in self.states],
                "events": [asdict(e) for e in self.events]}

    @classmethod
    def from_dict(cls, data: dict) -> RegionLedger:
        return cls(states=[RegionState(**row) for row in data.get("states", [])],
                   events=[RegionEvent(**row) for row in data.get("events", [])])
