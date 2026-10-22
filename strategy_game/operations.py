"""Phase 2 of #506: concurrent projects, personnel, capacity investments, sabotage, the loop.

Phase 1 gave the strategy layer **one** incremental-action engine
(``strategy_game.projects``): an agent-lead check gates the turn, the faction's committed
throughput decides how much work it produces, and a progress clock accumulates it. Phase 2 asks
for the *organisation* around that engine — issue #506's own list:

    "Concurrent projects, personnel assignments, lab/facility upgrades, capacity bottlenecks,
    recruitment and opposition sabotage."
    "Research outcomes open missions; missions generate research inputs."

What this module adds, and what each addition refuses to invent
---------------------------------------------------------------

* **Concurrent projects** (:func:`run_faction_turn`). Several projects run in one faction turn,
  each with its own lead, allocation and clock. The one-action-per-character rule is
  :class:`strategy_game.rpg.roster.TurnLedger`'s, reused — not restated. A lead that already
  acted this turn cannot drive a second project, and the report says which and why instead of
  quietly skipping it.
* **Real capacity accounting** (:func:`plan_allocations`). Two projects drawing on the same
  resource kind cannot both be handed their request when the faction does not have it:
  :class:`~strategy_game.projects.FactionCapacity` already *refuses* an over-commitment, so the
  planner hands out what exists in a declared priority order and reports each project's
  **shortfall**, and the faction-wide unmet units per kind. Nothing is trimmed in silence.
* **Personnel assignment** (:func:`assign_support`, :func:`project_personnel`). A project needs a
  lead and may name supporting personnel. Both are character ids on the campaign's one roster —
  there is no second roster here — and availability is read from the sheet
  (:func:`personnel_availability`) and from the turn ledger.
* **Facility and capacity upgrades, and recruitment** (:func:`apply_investment`). One explicit,
  bounded, costed action: it charges declared resource ids and raises one resource kind by
  :data:`TUNING_CAPACITY_INVESTMENT_UNITS`, with a ceiling of
  :data:`TUNING_CAPACITY_INVESTMENT_CEILING_SEATS` units per kind. Not a multiplier, and not an
  unbounded ladder.
* **Bottleneck remedies** (:func:`remedies_for`). A shortage is not a dead end: the report names
  the concrete choices — recruit, upgrade a facility, reassign the lead, pause, release capacity a
  finished programme is still holding — each with the number it would move.
* **Opposition sabotage** (:func:`resolve_sabotage`). One check by the saboteur through the one
  Fate kernel, then a **legible** consequence the project records. The engine's Phase-1 invariant
  that ``filled`` never decreases is *kept*: a set-back raises the clock's **total** work
  (:data:`TUNING_SABOTAGE_SETBACK_SEGMENTS`), so completed segments stay completed and the
  programme has further to go. Nothing here can delete progress, and a completed project cannot be
  re-opened.
* **The loop** (:func:`available_missions`, :func:`project_inputs`). A completed programme that
  names an option in its yield opens a mission the RPG layer may run; a mission resolved through
  :func:`strategy_game.campaign.missions.apply_mission_outcome` hands the faction the resource ids
  a project requires. Both directions are **read-only projections**; the one writer of a mission
  result stays the mission applier.

What stays the author's
-----------------------

* **Row D27** (the dice band and the work scale) is untouched: every Phase-1 ``TUNING_`` constant
  is imported and used as it stands, and no new canonical number is added. The three numbers this
  module needs are named ``TUNING_``, **derived from quantities that already exist**, and carried
  on the decision queue as row **D39** — see the design record
  ``strategy_game/docs/STRATEGIC_OPERATIONS_PHASE2.md`` §6.
* **Row D28** (what a domain TAG or an ideological prohibition should *do*) is untouched: nothing
  in this module reads a domain TAG or a prohibition.
* **Phase 3** is not here: no branching technology DAG, no faction divergence, no trade or
  espionage. ``campaign.tech_nodes`` remains the declared seam it was in Phase 1.
* No tactical or graphical UI: the demo is headless text (the renderer question is rows D13/D38).
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from random import Random
from typing import TYPE_CHECKING, Any

from .campaign.state import AGENT_CAPACITY, Campaign, CampaignError
from .projects import (
    TUNING_STYLE_BONUS_SEGMENTS,
    FactionCapacity,
    ProjectError,
    ProjectResult,
    ProjectStage,
    StrategicProject,
    advance_project,
    pause_project,
    unsatisfied_prerequisites,
)
from .provenance import ProvenanceKind
from .rpg.fate import Action, Outcome
from .rpg.roster import RosterError, Seat, TurnLedger
from .rpg.skills import ActionContext, check

if TYPE_CHECKING:  # pragma: no cover - typing only
    from .campaign.missions import MissionOutcome

__all__ = [
    "ALLOCATION_SCHEMA_VERSION",
    "PERSONNEL_RESOURCE_KIND",
    "SABOTAGE_LEAD_SKILL",
    "SABOTAGE_REPORT_SCHEMA_VERSION",
    "TUNING_CAPACITY_INVESTMENT_CEILING_SEATS",
    "TUNING_CAPACITY_INVESTMENT_UNITS",
    "TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME",
    "TUNING_SABOTAGE_SETBACK_SEGMENTS",
    "AllocationPlan",
    "AvailabilityState",
    "CapacityInvestment",
    "FactionTurnReport",
    "InvestmentKind",
    "InvestmentResult",
    "MissionOption",
    "OperationError",
    "PersonnelAvailability",
    "PersonnelReport",
    "ProjectInput",
    "ProjectTurn",
    "ProjectTurnKind",
    "Remedy",
    "RemedyKind",
    "SabotageAttempt",
    "SabotageConsequenceKind",
    "SabotageReport",
    "Shortfall",
    "apply_investment",
    "assign_support",
    "available_missions",
    "capacity_investment_from_dict",
    "invested_units",
    "personnel_availability",
    "plan_allocations",
    "project_inputs",
    "project_personnel",
    "remedies_for",
    "resolve_sabotage",
    "run_faction_turn",
    "sabotage_from_dict",
]

#: Shape markers for the two reports this module can store. A stored report names the schema that
#: produced it — the same discipline ``missions.MISSION_REPORT_SCHEMA_VERSION`` applies.
SABOTAGE_REPORT_SCHEMA_VERSION = "sabotage-report-1"
ALLOCATION_SCHEMA_VERSION = "allocation-plan-1"

#: **TUNING PARAMETER — not canon** (row D39). The capacity units one investment adds. Derived
#: from Phase 1 rather than chosen: issue #506's worked examples commit **three** units a turn, so
#: one investment is a third of a turn's throughput — deliberately small enough that an upgrade
#: never dwarfs institutional commitment, which is the thing that decides a project's scale.
TUNING_CAPACITY_INVESTMENT_UNITS = 1

#: **TUNING PARAMETER — not canon** (row D39). The ceiling on capacity **added by investment**, per
#: resource kind: the approved roster size, one leader and four agents
#: (:data:`strategy_game.campaign.state.AGENT_CAPACITY`). The faction's own seats are therefore the
#: bound on how far it can grow by its own action, and a bigger organisation is an author decision
#: about the roster rather than a number this module picked.
TUNING_CAPACITY_INVESTMENT_CEILING_SEATS = AGENT_CAPACITY

#: **TUNING PARAMETER — not canon** (row D39). The segments a successful sabotage adds to a
#: project's **total work**. Derived from :data:`strategy_game.projects.TUNING_STYLE_BONUS_SEGMENTS`
#: — the smallest amount by which the engine already moves a clock — so a set-back is of the same
#: order as a good turn's bonus and never more than a turn's work.
TUNING_SABOTAGE_SETBACK_SEGMENTS = TUNING_STYLE_BONUS_SEGMENTS

#: **TUNING PARAMETER — not canon** (row D39). How many consequences from the attempt's declared
#: menu a sabotage lands: one on a success, two on a success with style. It reuses the **approved**
#: Fate ladder — no new band is defined here — and only says how much a step of that ladder buys.
TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME: Mapping[Outcome, int] = {
    Outcome.FAILURE: 0,
    Outcome.TIE: 0,
    Outcome.SUCCESS: 1,
    Outcome.SUCCESS_WITH_STYLE: 2,
}


class OperationError(CampaignError):
    """A Phase-2 organisation operation the schema does not allow."""


def _project(campaign: Campaign, project_id: str) -> StrategicProject:
    project = campaign.projects.get(project_id)
    if project is None:
        raise OperationError(
            f"no project {project_id!r} on this campaign; declared: "
            f"{sorted(campaign.projects) or 'none'}"
        )
    return project


# -- personnel ----------------------------------------------------------------------------------


class AvailabilityState(str, Enum):
    """Why a character can or cannot take strategic duty this turn.

    Each state is a different fact and is reported as one, because *"the lead is unavailable"*
    collapses five situations the player must be able to tell apart: a person who is fine, a person
    who has already spent the turn, a person Fate has taken out, a person carrying an unrecovered
    consequence, and a character the campaign does not hold a sheet for.
    """

    AVAILABLE = "available"
    ACTED = "acted"
    TAKEN_OUT = "taken_out"
    CONSEQUENCED = "consequenced"
    NO_SHEET = "no_sheet"


@dataclass(frozen=True)
class PersonnelAvailability:
    """One character's fitness for strategic duty this turn, with the reasons in words."""

    character_id: str
    state: AvailabilityState
    reasons: tuple[str, ...] = ()

    @property
    def available(self) -> bool:
        return self.state is AvailabilityState.AVAILABLE

    def to_dict(self) -> dict[str, Any]:
        return {
            "character_id": self.character_id,
            "state": self.state.value,
            "available": self.available,
            "reasons": list(self.reasons),
        }


def _acted_this_turn(ledger: TurnLedger, character_id: str) -> str:
    """The seat statement under which ``character_id`` already acted this turn, or ``""``."""
    for seat_id, statement in ledger.acted.items():
        if ledger.seat(seat_id).character_id == character_id:
            return statement or seat_id
    return ""


def _seat_for(ledger: TurnLedger, character_id: str) -> Seat | None:
    for seat in ledger.seats:
        if seat.character_id == character_id:
            return seat
    return None


def personnel_availability(
    campaign: Campaign, character_id: str, *, ledger: TurnLedger | None = None
) -> PersonnelAvailability:
    """Read one character's fitness for strategic duty from the sheet and the turn ledger.

    Only facts the repository already owns are read: Fate's own "taken out" condition (every stress
    box of a track ticked), an unrecovered :class:`~strategy_game.rpg.fate.Consequence` — a
    consequence is by definition an injury that persists until it is recovered — and the turn
    ledger's record of who has already acted. Nothing here rates anybody, and no severity threshold
    is invented: that choice is row **D39**'s, and a *severity-based* reading would be a new number.
    """
    sheet = campaign.sheets.get(character_id)
    if sheet is None:
        return PersonnelAvailability(
            character_id,
            AvailabilityState.NO_SHEET,
            (f"{character_id!r} has no sheet on this campaign; inventing one would be inventing a character",),
        )
    if ledger is not None:
        statement = _acted_this_turn(ledger, character_id)
        if statement:
            message = (
                f"{sheet.name} has already acted this turn ({statement}); one character takes "
                "at most one action per turn (#461/#482)"
            )
            return PersonnelAvailability(character_id, AvailabilityState.ACTED, (message,))
    for track_name, track in (("physical", sheet.physical_stress), ("mental", sheet.mental_stress)):
        if track and all(track):
            return PersonnelAvailability(
                character_id,
                AvailabilityState.TAKEN_OUT,
                (f"{sheet.name} is taken out: every {track_name} stress box is ticked",),
            )
    open_consequences = [c for c in sheet.consequences if not c.recovered]
    if open_consequences:
        labels = ", ".join(sorted(f"{c.name!r} (severity {c.severity})" for c in open_consequences))
        return PersonnelAvailability(
            character_id,
            AvailabilityState.CONSEQUENCED,
            (f"{sheet.name} carries an unrecovered consequence: {labels}",),
        )
    return PersonnelAvailability(character_id, AvailabilityState.AVAILABLE)


@dataclass(frozen=True)
class PersonnelReport:
    """A project's people: its lead, its supporting personnel, and whether the lead can act."""

    project_id: str
    lead: PersonnelAvailability
    support: tuple[PersonnelAvailability, ...] = ()

    @property
    def ready(self) -> bool:
        return self.lead.available

    @property
    def support_available(self) -> tuple[str, ...]:
        return tuple(item.character_id for item in self.support if item.available)

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "lead": self.lead.to_dict(),
            "support": [item.to_dict() for item in self.support],
            "ready": self.ready,
            "support_available": list(self.support_available),
        }


def project_personnel(
    campaign: Campaign, project_id: str, *, ledger: TurnLedger | None = None
) -> PersonnelReport:
    """The project's lead and supporting personnel, each with its availability."""
    project = _project(campaign, project_id)
    return PersonnelReport(
        project_id=project_id,
        lead=personnel_availability(campaign, project.lead_id, ledger=ledger),
        support=tuple(
            personnel_availability(campaign, cid, ledger=ledger) for cid in project.support_ids
        ),
    )


def assign_support(campaign: Campaign, project_id: str, support_ids: Sequence[str]) -> StrategicProject:
    """Name the supporting personnel on a project. Ids are character ids on the one roster.

    A supporter must have a sheet (a name is not a person), must not be the lead (the lead is
    already the lead), and must not repeat. Support is **assignment, not a bonus**: no supporter
    moves the check or the throughput, because a supporter who did would be an unapproved mechanic
    (row D39 states the open question). What support buys today is what the turn report can say:
    who is on the programme, who can still act, and who could take it over when the lead cannot
    (:func:`remedies_for`).
    """
    project = _project(campaign, project_id)
    ids = tuple(str(value).strip() for value in support_ids)
    if any(not value for value in ids):
        raise OperationError("a supporting person needs a non-empty character id")
    if len(set(ids)) != len(ids):
        raise OperationError(f"project {project_id!r}: supporting personnel repeat an id: {sorted(ids)}")
    if project.lead_id in ids:
        raise OperationError(
            f"project {project_id!r}: {project.lead_id!r} is already the lead; a person is not their "
            "own support"
        )
    missing = [cid for cid in ids if cid not in campaign.sheets]
    if missing:
        raise OperationError(
            f"project {project_id!r}: supporting personnel {missing} have no sheet on the campaign; "
            "inventing one would be inventing a character"
        )
    project.support_ids = ids
    return project


# -- capacity investments: facilities, equipment, recruitment ------------------------------------


class InvestmentKind(str, Enum):
    """The two ways a faction raises its own capacity — both explicit, both costed.

    The split is not decoration: a **facility** investment raises a material resource kind (a lab,
    a workshop, an archive terminal) and a **recruitment** raises the ``personnel`` kind. Keeping
    them apart means a caller cannot silently buy research throughput by hiring, or hire by buying a
    machine, and the audit trail says which happened.
    """

    FACILITY = "facility"
    RECRUITMENT = "recruitment"


#: The resource kind a recruitment raises. Data, not a closed vocabulary: a campaign that calls its
#: staff something else passes that kind and this constant is only the default name for people.
PERSONNEL_RESOURCE_KIND = "personnel"


@dataclass(frozen=True)
class CapacityInvestment:
    """One bounded, explicit, costed raise of one faction's capacity in one resource kind.

    ``cost_resource_ids`` is what the investment **charges**: ids the faction must hold and that are
    removed when the investment applies. That is the same id-level inventory transition
    :func:`strategy_game.campaign.missions.apply_mission_outcome` already performs, so a cost is a
    real, visible loss of a held thing rather than an invented currency.
    """

    investment_id: str
    faction_id: str
    kind: InvestmentKind
    resource_kind: str
    units: int = TUNING_CAPACITY_INVESTMENT_UNITS
    cost_resource_ids: tuple[str, ...] = ()
    label: str = ""

    def __post_init__(self) -> None:
        if not str(self.investment_id).strip():
            raise OperationError("an investment names itself")
        if not str(self.faction_id).strip():
            raise OperationError("an investment names the faction that pays for it")
        if not isinstance(self.kind, InvestmentKind):
            try:
                object.__setattr__(self, "kind", InvestmentKind(str(self.kind)))
            except ValueError as exc:
                raise OperationError(
                    f"investment kind {self.kind!r} is not one of "
                    f"({', '.join(k.value for k in InvestmentKind)})"
                ) from exc
        if not str(self.resource_kind).strip():
            raise OperationError("an investment names the resource kind it raises")
        if not isinstance(self.units, int) or self.units < 1:
            raise OperationError("an investment adds at least one unit")
        if self.units > TUNING_CAPACITY_INVESTMENT_UNITS:
            raise OperationError(
                f"an investment adds at most {TUNING_CAPACITY_INVESTMENT_UNITS} unit(s) "
                f"(tuning parameter); {self.units} is a bigger step than the engine offers"
            )
        if not self.cost_resource_ids:
            raise OperationError(
                "an investment declares what it costs; capacity that appears from nowhere is a "
                "multiplier, and issue #506 asks for a bounded action with a cost"
            )
        if len(set(self.cost_resource_ids)) != len(self.cost_resource_ids):
            raise OperationError(f"investment {self.investment_id!r}: cost repeats an id")
        if self.kind is InvestmentKind.RECRUITMENT and self.resource_kind != PERSONNEL_RESOURCE_KIND:
            raise OperationError(
                f"a recruitment raises {PERSONNEL_RESOURCE_KIND!r} capacity; "
                f"{self.resource_kind!r} is raised by a facility investment"
            )
        if self.kind is InvestmentKind.FACILITY and self.resource_kind == PERSONNEL_RESOURCE_KIND:
            raise OperationError(
                f"a facility does not add {PERSONNEL_RESOURCE_KIND!r} capacity; recruit people with "
                "InvestmentKind.RECRUITMENT"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "investment_id": self.investment_id,
            "faction_id": self.faction_id,
            "kind": self.kind.value,
            "resource_kind": self.resource_kind,
            "units": self.units,
            "cost_resource_ids": list(self.cost_resource_ids),
            "label": self.label,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CapacityInvestment:
        if not isinstance(data, Mapping):
            raise OperationError(
                f"an investment record must be a mapping, got {type(data).__name__}"
            )
        return cls(
            investment_id=str(data.get("investment_id") or ""),
            faction_id=str(data.get("faction_id") or ""),
            kind=data.get("kind"),  # type: ignore[arg-type]
            resource_kind=str(data.get("resource_kind") or ""),
            units=int(data.get("units", TUNING_CAPACITY_INVESTMENT_UNITS)),
            cost_resource_ids=tuple(str(x) for x in (data.get("cost_resource_ids") or [])),
            label=str(data.get("label") or ""),
        )


def capacity_investment_from_dict(data: Mapping[str, Any]) -> CapacityInvestment:
    """Build an investment from :meth:`CapacityInvestment.to_dict` output (the save/load seam)."""
    return CapacityInvestment.from_dict(data)


@dataclass(frozen=True)
class InvestmentResult:
    """What one investment changed, and whether it changed anything this time.

    ``applied`` is ``False`` on a replay: an investment applies **once**, so calling it again
    charges nothing and adds nothing, which is what makes a replayable save safe.
    """

    investment_id: str
    faction_id: str
    resource_kind: str
    units: int
    applied: bool
    capacity_before: int
    capacity_after: int
    charged_resource_ids: tuple[str, ...] = ()
    note_index: int = -1

    def to_dict(self) -> dict[str, Any]:
        return {
            "investment_id": self.investment_id,
            "faction_id": self.faction_id,
            "resource_kind": self.resource_kind,
            "units": self.units,
            "applied": self.applied,
            "capacity_before": self.capacity_before,
            "capacity_after": self.capacity_after,
            "charged_resource_ids": list(self.charged_resource_ids),
            "note_index": self.note_index,
        }


def invested_units(campaign: Campaign, faction_id: str, resource_kind: str) -> int:
    """Every capacity unit this faction has already added to ``resource_kind`` by investment."""
    return sum(
        item.units
        for item in campaign.capacity_investments.values()
        if item.faction_id == faction_id and item.resource_kind == resource_kind
    )


def apply_investment(
    campaign: Campaign, investment: CapacityInvestment, *, turn: int
) -> InvestmentResult:
    """Charge the cost and raise the capacity — bounded, once, and with one audit note.

    Order of operations, and why:

    1. **the faction and its ledger must exist.** Capacity the campaign does not track is capacity
       no project can draw on;
    2. **a replay applies nothing.** The investment id is the key, so a save-replayed turn cannot
       charge twice;
    3. **the ceiling is checked before the purchase.** Capacity added by investment is bounded by
       :data:`TUNING_CAPACITY_INVESTMENT_CEILING_SEATS` units per kind, and a faction that has spent
       its ceiling is refused **with the numbers**, rather than quietly capped;
    4. **the cost must be held.** Every cost id is read from the faction's inventory *before*
       anything is written, so a purchase that cannot be paid for leaves state untouched;
    5. **the raise is validated as a ledger.** The new units are committed through a fresh
       :class:`~strategy_game.projects.FactionCapacity`, so the "commitments never exceed units"
       invariant is re-checked rather than assumed.
    """
    faction = campaign.faction(investment.faction_id)
    ledger = campaign.capacities.get(investment.faction_id)
    if ledger is None:
        raise OperationError(
            f"faction {investment.faction_id!r} has no capacity ledger; an investment raises "
            "capacity the campaign must already track"
        )
    existing = campaign.capacity_investments.get(investment.investment_id)
    if existing is not None:
        if existing != investment:
            raise OperationError(
                f"investment {investment.investment_id!r} is already applied with different terms; "
                "one id names one investment"
            )
        return InvestmentResult(
            investment_id=investment.investment_id,
            faction_id=investment.faction_id,
            resource_kind=investment.resource_kind,
            units=0,
            applied=False,
            capacity_before=ledger.units.get(investment.resource_kind, 0),
            capacity_after=ledger.units.get(investment.resource_kind, 0),
            charged_resource_ids=(),
            note_index=int(faction.detail.get("capacity_investment_note_index", -1)),
        )
    already = invested_units(campaign, investment.faction_id, investment.resource_kind)
    if already + investment.units > TUNING_CAPACITY_INVESTMENT_CEILING_SEATS:
        raise OperationError(
            f"faction {investment.faction_id!r} has already added {already} "
            f"{investment.resource_kind!r} unit(s) by investment and may add at most "
            f"{TUNING_CAPACITY_INVESTMENT_CEILING_SEATS} (tuning parameter, derived from the "
            f"approved roster size of {AGENT_CAPACITY} agent seats); another "
            f"{investment.units} would exceed the ceiling"
        )
    unheld = [rid for rid in investment.cost_resource_ids if rid not in faction.resources]
    if unheld:
        raise OperationError(
            f"investment {investment.investment_id!r} costs {', '.join(unheld)}, which faction "
            f"{investment.faction_id!r} does not hold; nothing is charged and nothing is raised"
        )

    # Everything above is validation; nothing below may raise, so state is never half-written.
    before = ledger.units.get(investment.resource_kind, 0)
    trial = FactionCapacity(
        ledger.faction_id,
        {**ledger.units, investment.resource_kind: before + investment.units},
        list(ledger.commitments),
    )
    ledger.units = trial.units
    faction.resources = [rid for rid in faction.resources if rid not in set(investment.cost_resource_ids)]
    campaign.capacity_investments[investment.investment_id] = investment
    faction.detail.setdefault("capacity_investments", []).append(investment.investment_id)
    index = len(campaign.campaign_notes)
    campaign.campaign_notes.append(
        {
            "kind": "capacity_investment",
            "investment_id": investment.investment_id,
            "faction_id": investment.faction_id,
            "turn": turn,
            "investment_kind": investment.kind.value,
            "resource_kind": investment.resource_kind,
            "units": investment.units,
            "capacity_before": before,
            "capacity_after": before + investment.units,
            "charged_resource_ids": list(investment.cost_resource_ids),
            "label": investment.label,
            "provenance": {
                "kind": ProvenanceKind.SIMULATED.value,
                "source": "strategy_game.operations.apply_investment",
                "note": (
                    "a bounded capacity raise with a charged cost (issue #506 Phase 2); the "
                    "magnitude and ceiling are tuning parameters pending row D39"
                ),
            },
        }
    )
    faction.detail["capacity_investment_note_index"] = index
    return InvestmentResult(
        investment_id=investment.investment_id,
        faction_id=investment.faction_id,
        resource_kind=investment.resource_kind,
        units=investment.units,
        applied=True,
        capacity_before=before,
        capacity_after=before + investment.units,
        charged_resource_ids=investment.cost_resource_ids,
        note_index=index,
    )


# -- bottlenecks: what a shortage lets the faction do --------------------------------------------


class RemedyKind(str, Enum):
    """The explicit choices a faction has when a project is short of what it draws on.

    Issue #506 Phase 2 names them: *"capacity bottlenecks, recruitment"* — and requires that the
    faction can *act* on a shortage. Each remedy is a different act with a different consequence,
    so the report lists them instead of collapsing them into "you need more capacity".
    """

    RECRUIT = "recruit"
    UPGRADE_FACILITY = "upgrade_facility"
    REASSIGN_LEAD = "reassign_lead"
    PAUSE = "pause"
    RELEASE_STRANDED = "release_stranded"


@dataclass(frozen=True)
class Remedy:
    """One choice, with the consequence it would have — the numbers in it are the real ones."""

    kind: RemedyKind
    label: str
    effect: str

    def to_dict(self) -> dict[str, Any]:
        return {"kind": self.kind.value, "label": self.label, "effect": self.effect}


def remedies_for(
    campaign: Campaign,
    project_id: str,
    *,
    shortfall_units: int | None = None,
    ledger: TurnLedger | None = None,
) -> tuple[Remedy, ...]:
    """The remedies that would actually help *this* project, each with its visible consequence.

    Reported rather than applied: every one of these is a decision with a cost — an investment
    charges held resources, a reassignment moves a project to another person, a pause stops the
    clock — so none of them happens behind the player's back.
    """
    project = _project(campaign, project_id)
    capacity = campaign.capacities.get(project.faction_id)
    short = shortfall_units
    short_text = f"{short} unit(s)" if short else "the shortfall"
    remedies: list[Remedy] = []

    if project.resource_kind == PERSONNEL_RESOURCE_KIND:
        remedies.append(
            Remedy(
                RemedyKind.RECRUIT,
                "Recruit staff",
                f"raises {PERSONNEL_RESOURCE_KIND!r} capacity by "
                f"{TUNING_CAPACITY_INVESTMENT_UNITS} unit(s) for its declared cost, up to "
                f"{TUNING_CAPACITY_INVESTMENT_CEILING_SEATS} invested unit(s) per resource kind "
                f"(ceiling); it adds staff capacity, not a seat — the roster stays one leader and "
                f"{AGENT_CAPACITY} agents",
            )
        )
    else:
        remedies.append(
            Remedy(
                RemedyKind.UPGRADE_FACILITY,
                f"Upgrade {project.resource_kind!r} capacity",
                f"raises {project.resource_kind!r} capacity by "
                f"{TUNING_CAPACITY_INVESTMENT_UNITS} unit(s) for its declared cost, up to "
                f"{TUNING_CAPACITY_INVESTMENT_CEILING_SEATS} invested unit(s) per resource kind "
                f"(ceiling), and covers {short_text} of the shortfall from the next turn on",
            )
        )
    if ledger is not None:
        candidates = [
            seat
            for seat in ledger.seats
            if seat.character_id != project.lead_id
            and personnel_availability(campaign, seat.character_id, ledger=ledger).available
        ]
        if candidates:
            remedies.append(
                Remedy(
                    RemedyKind.REASSIGN_LEAD,
                    "Reassign the lead",
                    "hands the project to one of "
                    + ", ".join(sorted(seat.character_id for seat in candidates))
                    + "; the clock and every completed segment move with it, and the new lead "
                    "spends its action next turn",
                )
            )
    remedies.append(
        Remedy(
            RemedyKind.PAUSE,
            "Pause the project",
            f"stops the clock at {project.clock.filled}/{project.clock.work_required} segments, "
            "preserves every completed segment and releases the capacity committed to it for other "
            "projects",
        )
    )
    if capacity is not None:
        stranded = [
            other
            for other in campaign.projects.values()
            if other.faction_id == project.faction_id
            and other.project_id != project.project_id
            and other.clock.is_complete
            and capacity.allocated(other.project_id) > 0
        ]
        if stranded:
            remedies.append(
                Remedy(
                    RemedyKind.RELEASE_STRANDED,
                    "Release capacity a finished programme is still holding",
                    "; ".join(
                        f"{other.project_id!r} is complete and still holds "
                        f"{capacity.allocated(other.project_id)} unit(s) of "
                        f"{other.resource_kind!r}"
                        for other in sorted(stranded, key=lambda p: p.project_id)
                    )
                    + f", which would cover {short_text} of this project's shortfall",
                )
            )
    return tuple(remedies)


# -- concurrent projects and their per-turn capacity accounting ---------------------------------


@dataclass(frozen=True)
class Shortfall:
    """One project's unmet request, and what the faction could do about it."""

    project_id: str
    resource_kind: str
    requested: int
    granted: int
    shortfall: int
    free_after: int
    remedies: tuple[Remedy, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "resource_kind": self.resource_kind,
            "requested": self.requested,
            "granted": self.granted,
            "shortfall": self.shortfall,
            "free_after": self.free_after,
            "remedies": [remedy.to_dict() for remedy in self.remedies],
        }


@dataclass(frozen=True)
class AllocationPlan:
    """The turn's capacity decision: what each project asked for, got, and went without.

    ``grants`` is in the priority order the caller declared — that order *is* the decision, so the
    plan records it instead of leaving it implicit. ``unmet`` is the faction-wide shortfall per
    resource kind: the number that says "this organisation cannot do everything it wants".
    """

    faction_id: str
    grants: tuple[tuple[str, int], ...]
    shortfalls: tuple[Shortfall, ...] = ()
    unmet: tuple[tuple[str, int], ...] = ()
    stranded: tuple[tuple[str, int], ...] = ()
    released: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    schema_version: str = ALLOCATION_SCHEMA_VERSION

    def granted(self, project_id: str) -> int:
        for pid, units in self.grants:
            if pid == project_id:
                return units
        return 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "faction_id": self.faction_id,
            "grants": [{"project_id": pid, "units": units} for pid, units in self.grants],
            "shortfalls": [item.to_dict() for item in self.shortfalls],
            "unmet": [{"resource_kind": kind, "units": units} for kind, units in self.unmet],
            "stranded": [{"project_id": pid, "units": units} for pid, units in self.stranded],
            "released": list(self.released),
            "notes": list(self.notes),
        }


def _demand_pairs(demands: Mapping[str, int] | Sequence[tuple[str, int]]) -> tuple[tuple[str, int], ...]:
    if isinstance(demands, Mapping):
        return tuple((str(pid), int(units)) for pid, units in demands.items())
    pairs: list[tuple[str, int]] = []
    for item in demands:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            raise OperationError(
                "a demand is a (project_id, units) pair; got "
                f"{item!r}"
            )
        pairs.append((str(item[0]), int(item[1])))
    return tuple(pairs)


def plan_allocations(
    campaign: Campaign,
    faction_id: str,
    demands: Mapping[str, int] | Sequence[tuple[str, int]],
) -> AllocationPlan:
    """Hand out one turn's capacity among concurrent projects, in the caller's priority order.

    This is the whole point of Phase 2's capacity accounting: a faction running four programmes
    still has one pool per resource kind, and :class:`~strategy_game.projects.FactionCapacity`
    **refuses** to promise more than it holds. So the planner

    1. **releases** the demands' previous commitments, so re-planning is a decision about this turn
       rather than an accumulation on top of last turn's;
    2. **grants in order**, each project receiving ``min(request, what is left)`` — the first
       project in the order is the faction's stated priority, and the ledger never over-commits;
    3. **reports every shortfall**, the remedies that would change it, and the faction-wide unmet
       units per kind, so a shortage is a visible fact rather than a silent zero;
    4. **reports stranded capacity**: units still committed to a programme whose clock is full. That
       is the most common real bottleneck, and it is a faction's own decision — releasing it is the
       fifth remedy.
    """
    faction = campaign.faction(faction_id)
    ledger = campaign.capacities.get(faction_id)
    if ledger is None:
        raise OperationError(
            f"faction {faction.identifier!r} has no capacity ledger; there is no capacity to plan"
        )
    pairs = _demand_pairs(demands)
    seen: list[str] = []
    for pid, units in pairs:
        project = campaign.projects.get(pid)
        if project is None:
            raise OperationError(
                f"no project {pid!r} on this campaign; declared: "
                f"{sorted(campaign.projects) or 'none'}"
            )
        if project.faction_id != faction_id:
            raise OperationError(
                f"project {pid!r} belongs to faction {project.faction_id!r}, not "
                f"{faction_id!r}; one faction plans its own capacity"
            )
        if units < 0:
            raise OperationError(f"project {pid!r}: a demand is a nonnegative number of units")
        if pid in seen:
            raise OperationError(f"project {pid!r} appears twice in one plan")
        seen.append(pid)

    released = tuple(pid for pid in seen if ledger.allocated(pid) > 0)
    for pid in released:
        ledger.release(pid)

    grants: list[tuple[str, int]] = []
    pending: list[tuple[str, str, int, int]] = []
    for pid, units in pairs:
        project = campaign.projects[pid]
        kind = project.resource_kind
        free = max(0, ledger.free(kind))
        grant = min(units, free)
        if grant:
            ledger.allocate(pid, kind, grant)
            grants.append((pid, grant))
        if grant < units:
            pending.append((pid, kind, units, grant))

    shortfalls: list[Shortfall] = []
    notes: list[str] = []
    for pid, kind, requested, granted in pending:
        short = requested - granted
        free_after = ledger.free(kind)
        remedies = remedies_for(campaign, pid, shortfall_units=short, ledger=None)
        shortfalls.append(
            Shortfall(
                project_id=pid,
                resource_kind=kind,
                requested=requested,
                granted=granted,
                shortfall=short,
                free_after=free_after,
                remedies=remedies,
            )
        )
        notes.append(
            f"{pid} asked for {requested} {kind} unit(s) and got {granted}: {short} unit(s) short "
            f"because the faction's {kind!r} capacity is fully committed. "
            + (
                f"The project still runs — at {granted} unit(s) of throughput, which is what the "
                "institution can actually give it."
                if granted
                else "It is allocated nothing this turn, so a successful check would report "
                "NO_CAPACITY: the lead cannot substitute for the institution."
            )
        )

    totals: dict[str, int] = {}
    for _pid, kind, requested, granted in pending:
        totals[kind] = totals.get(kind, 0) + (requested - granted)
    unmet = tuple(sorted(totals.items()))

    stranded: list[tuple[str, int]] = []
    for pid, project in sorted(campaign.projects.items()):
        if project.faction_id != faction_id or pid in seen:
            continue
        if project.clock.is_complete and ledger.allocated(pid) > 0:
            stranded.append((pid, ledger.allocated(pid)))
    for pid, units in stranded:
        notes.append(
            f"{pid} is complete and still holds {units} unit(s) of "
            f"{campaign.projects[pid].resource_kind!r}; releasing them is a decision the faction can "
            "take at any time (FactionCapacity.release)"
        )
    for kind in sorted(ledger.units):
        notes.append(
            f"{kind}: {ledger.units.get(kind, 0)} unit(s), {ledger.committed(kind)} committed, "
            f"{ledger.free(kind)} free"
        )
    return AllocationPlan(
        faction_id=faction_id,
        grants=tuple(grants),
        shortfalls=tuple(shortfalls),
        unmet=unmet,
        stranded=tuple(stranded),
        released=released,
        notes=tuple(notes),
    )


class ProjectTurnKind(str, Enum):
    """What happened to one project in one faction turn — the legible per-project outcome.

    ``ADVANCED``-style causes live on :class:`~strategy_game.projects.ProgressCause`, which says what
    the *clock* did. This enum says what the *organisation* did: whether the project got its lead's
    action at all, and if not, which of the seven reasons stopped it.
    """

    RAN = "ran"
    CLOSED = "closed"
    PAUSED = "paused"
    BLOCKED = "blocked"
    BUSY = "busy"
    UNAVAILABLE = "unavailable"
    UNSEATED = "unseated"
    NO_SHEET = "no_sheet"
    ERROR = "error"


@dataclass(frozen=True)
class ProjectTurn:
    """One project's place in one faction turn."""

    project_id: str
    turn: int
    kind: ProjectTurnKind
    action_taken: bool
    result: ProjectResult | None = None
    reason: str = ""
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "turn": self.turn,
            "kind": self.kind.value,
            "action_taken": self.action_taken,
            "reason": self.reason,
            "error": self.error,
            "progress_added": self.result.progress_added if self.result is not None else 0,
            "cause": self.result.cause.value if self.result is not None else None,
            "filled": self.result.filled if self.result is not None else None,
            "work_required": self.result.work_required if self.result is not None else None,
            "notes": list(self.result.notes) if self.result is not None else [],
        }


@dataclass(frozen=True)
class FactionTurnReport:
    """One faction turn across every project it tried to run."""

    faction_id: str
    turn: int
    turns: tuple[ProjectTurn, ...]
    allocations: AllocationPlan | None = None
    actions_used: int = 0
    actions_free: int = 0
    errors: tuple[tuple[str, str], ...] = ()
    notes: tuple[str, ...] = ()

    def turn_for(self, project_id: str) -> ProjectTurn:
        for item in self.turns:
            if item.project_id == project_id:
                return item
        raise OperationError(
            f"project {project_id!r} is not in this turn's report; it ran "
            f"{[item.project_id for item in self.turns]}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "faction_id": self.faction_id,
            "turn": self.turn,
            "turns": [item.to_dict() for item in self.turns],
            "allocations": self.allocations.to_dict() if self.allocations is not None else None,
            "actions_used": self.actions_used,
            "actions_free": self.actions_free,
            "errors": [{"project_id": pid, "error": text} for pid, text in self.errors],
            "notes": list(self.notes),
        }


def run_faction_turn(
    campaign: Campaign,
    *,
    turn: int,
    ledger: TurnLedger,
    rng: Random,
    roster: Mapping[str, object] | None = None,
    faction_id: str | None = None,
    order: Sequence[str] | None = None,
    demands: Mapping[str, int] | Sequence[tuple[str, int]] | None = None,
    scene: Any = None,
    invoked_aspect: str | None = None,
    free: bool = False,
    reroll: bool = False,
) -> FactionTurnReport:
    """Run every project the faction attempts this turn, on one ledger and one capacity pool.

    This is Phase 2's "concurrent projects" in one function, and the order of checks is the
    argument for it:

    1. **the ledger and the turn number must agree.** A report that says turn 4 while the ledger is
       on turn 7 is a lie about when something happened;
    2. **capacity is planned first** when ``demands`` is given, so no project is handed throughput
       the faction does not have (:func:`plan_allocations`);
    3. per project, in the caller's ``order`` (the priority): a **closed** project is skipped, a
       **paused** one stays paused, a lead with **no sheet** or **no seat** is reported rather than
       guessed at, a lead who **already acted** is reported as busy, a lead Fate has **taken out**
       or who carries an unrecovered consequence is reported as unavailable, and a project that has
       never started and does not satisfy its **prerequisites** is blocked — and none of those six
       spends the lead's action;
    4. only then is the lead's action declared on
       :class:`~strategy_game.rpg.roster.TurnLedger` and the project advanced through
       :func:`strategy_game.projects.advance_project`, the one Phase-1 engine. Failure, tie, zero
       capacity and a mid-flight interruption keep the Phase-1 meanings;
    5. a :class:`~strategy_game.projects.ProjectError` from one project is **recorded, not
       swallowed and not fatal**: the other projects still run and the error is in the report.
    """
    faction = campaign.faction(faction_id)
    if ledger.turn != turn:
        raise OperationError(
            f"the turn ledger is on turn {ledger.turn} but the report says {turn}; a turn is "
            "resolved once, on the ledger that counts it"
        )

    project_ids = (
        tuple(str(pid) for pid in order)
        if order is not None
        else tuple(pid for pid, project in sorted(campaign.projects.items())
                   if project.faction_id == faction.identifier)
    )
    for pid in project_ids:
        project = campaign.projects.get(pid)
        if project is None:
            raise OperationError(f"no project {pid!r} on this campaign")
        if project.faction_id != faction.identifier:
            raise OperationError(
                f"project {pid!r} belongs to faction {project.faction_id!r}, not "
                f"{faction.identifier!r}"
            )

    allocations = (
        plan_allocations(campaign, faction.identifier, demands) if demands is not None else None
    )

    turns: list[ProjectTurn] = []
    errors: list[tuple[str, str]] = []
    notes: list[str] = []
    for pid in project_ids:
        project = campaign.projects[pid]
        if project.clock.is_complete:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.CLOSED, action_taken=False,
                    reason=(
                        f"{pid} is closed at {project.clock.filled}/{project.clock.work_required} "
                        "segments; a finished programme takes no action and no capacity"
                    ),
                )
            )
            continue
        if project.paused:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.PAUSED, action_taken=False,
                    reason=f"{pid} is paused: {'; '.join(project.pause_reasons)}",
                )
            )
            continue
        availability = personnel_availability(campaign, project.lead_id, ledger=ledger)
        if availability.state is AvailabilityState.NO_SHEET:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.NO_SHEET, action_taken=False,
                    reason=availability.reasons[0],
                )
            )
            continue
        seat = _seat_for(ledger, project.lead_id)
        if seat is None:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.UNSEATED, action_taken=False,
                    reason=(
                        f"lead {project.lead_id!r} holds no seat in this turn's roster; a project is "
                        "driven by a seated character, and inventing a seat would be inventing a "
                        "roster"
                    ),
                )
            )
            continue
        if availability.state is AvailabilityState.ACTED:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.BUSY, action_taken=False,
                    reason=availability.reasons[0],
                )
            )
            continue
        if not availability.available:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.UNAVAILABLE, action_taken=False,
                    reason=availability.reasons[0],
                )
            )
            continue
        unsatisfied = unsatisfied_prerequisites(campaign, project)
        if unsatisfied and project.clock.filled == 0:
            turns.append(
                ProjectTurn(
                    pid, turn, ProjectTurnKind.BLOCKED, action_taken=False,
                    reason=(
                        f"{pid} cannot start: missing prerequisites {', '.join(unsatisfied)}. Issue "
                        "#506 requires access to the specimen, artefact, archive, data or facility "
                        "before the work exists at all; a resolved mission grants it through "
                        "strategy_game.campaign.missions.apply_mission_outcome."
                    ),
                )
            )
            continue
        try:
            ledger.declare(seat.id, statement=pid)
        except RosterError as exc:  # pragma: no cover - the ACTED check above runs first
            turns.append(
                ProjectTurn(pid, turn, ProjectTurnKind.BUSY, action_taken=False, reason=str(exc))
            )
            continue
        try:
            result = advance_project(
                campaign,
                pid,
                rng=rng,
                turn=turn,
                roster=roster,
                scene=scene,
                invoked_aspect=invoked_aspect,
                free=free,
                reroll=reroll,
            )
        except ProjectError as exc:
            errors.append((pid, str(exc)))
            turns.append(
                ProjectTurn(pid, turn, ProjectTurnKind.ERROR, action_taken=True, error=str(exc))
            )
            continue
        turns.append(ProjectTurn(pid, turn, ProjectTurnKind.RAN, action_taken=True, result=result))
        notes.extend(result.notes)

    used = sum(1 for item in turns if item.action_taken)
    if used:
        notes.append(
            f"{used} character action(s) spent on {faction.identifier!r}'s programmes this turn; "
            f"{len(ledger.seats) - len(ledger.acted)} seat(s) still free"
        )
    skipped = [item for item in turns if not item.action_taken and item.kind is not ProjectTurnKind.CLOSED]
    for item in skipped:
        notes.append(item.reason)
    return FactionTurnReport(
        faction_id=faction.identifier,
        turn=turn,
        turns=tuple(turns),
        allocations=allocations,
        actions_used=used,
        actions_free=len(ledger.seats) - len(ledger.acted),
        errors=tuple(errors),
        notes=tuple(notes),
    )


# -- opposition sabotage -------------------------------------------------------------------------

#: The sabotaging agent's skill: the proposal roster's covert id (``data/strategic_skills.json``,
#: ``status: PROPOSAL``). Nothing here approves it; the kernel refuses the check without the roster,
#: exactly as it does for :data:`strategy_game.research.RESEARCH_LEAD_SKILL`.
SABOTAGE_LEAD_SKILL = "security"


class SabotageConsequenceKind(str, Enum):
    """What a successful disruption does to the project — three legible, different harms.

    None of them is "you lose the work you have done", because issue #506's Phase-1 rules forbid
    erasing completed progress (``ProjectClock.filled`` never decreases). The set-back is therefore a
    **longer road**, not a shorter one: the clock's total work grows and every completed segment
    stays completed.
    """

    #: The programme must do more work than it thought: ``work_required`` grows by
    #: :data:`TUNING_SABOTAGE_SETBACK_SEGMENTS`; ``filled`` is untouched.
    SETBACK = "setback"
    #: The programme is interrupted and must be resumed: a pause with a stated reason, progress kept.
    COMPLICATION = "complication"
    #: The faction loses the capacity it had committed to this project: the units return to the pool
    #: and the shortage becomes visible in the next plan.
    ALLOCATION_LOSS = "allocation_loss"


@dataclass(frozen=True)
class SabotageAttempt:
    """One declared attempt by another party to disrupt one project.

    ``difficulty`` is the **guard**: the target's preparedness, set by the caller/GM exactly as
    :attr:`strategy_game.projects.StrategicProject.lead_difficulty` is set. ``consequences`` is the
    menu this attempt can land, worst-first as the caller declares it; how many of them land is the
    approved Fate ladder's business (:data:`TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME`), never a new
    dice band.
    """

    attempt_id: str
    project_id: str
    saboteur_id: str
    difficulty: int
    lead_skill: str = SABOTAGE_LEAD_SKILL
    consequences: tuple[SabotageConsequenceKind, ...] = (SabotageConsequenceKind.SETBACK,)

    def __post_init__(self) -> None:
        for name, value in (
            ("attempt_id", self.attempt_id),
            ("project_id", self.project_id),
            ("saboteur_id", self.saboteur_id),
            ("lead_skill", self.lead_skill),
        ):
            if not str(value).strip():
                raise OperationError(f"a sabotage attempt needs a non-empty {name}")
        if not isinstance(self.difficulty, int) or self.difficulty < 0:
            raise OperationError("a sabotage attempt's guard is a nonnegative integer")
        if not self.consequences:
            raise OperationError(
                "a sabotage attempt declares the consequences it can land; an attempt with an "
                "empty menu cannot report what it did"
            )
        resolved: list[SabotageConsequenceKind] = []
        for item in self.consequences:
            if isinstance(item, SabotageConsequenceKind):
                resolved.append(item)
                continue
            try:
                resolved.append(SabotageConsequenceKind(str(item)))
            except ValueError as exc:
                raise OperationError(
                    f"sabotage consequence {item!r} is not one of "
                    f"({', '.join(k.value for k in SabotageConsequenceKind)})"
                ) from exc
        if len(set(resolved)) != len(resolved):
            raise OperationError(
                f"attempt {self.attempt_id!r} declares the same consequence twice; each kind lands "
                "at most once per attempt"
            )
        object.__setattr__(self, "consequences", tuple(resolved))

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "project_id": self.project_id,
            "saboteur_id": self.saboteur_id,
            "difficulty": self.difficulty,
            "lead_skill": self.lead_skill,
            "consequences": [kind.value for kind in self.consequences],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SabotageAttempt:
        if not isinstance(data, Mapping):
            raise OperationError(f"a sabotage attempt must be a mapping, got {type(data).__name__}")
        return cls(
            attempt_id=str(data.get("attempt_id") or ""),
            project_id=str(data.get("project_id") or ""),
            saboteur_id=str(data.get("saboteur_id") or ""),
            difficulty=int(data.get("difficulty", 0)),
            lead_skill=str(data.get("lead_skill") or SABOTAGE_LEAD_SKILL),
            consequences=tuple(data.get("consequences") or (SabotageConsequenceKind.SETBACK,)),
        )


@dataclass(frozen=True)
class SabotageReport:
    """What the attempt did, as the project records it — including the proof it deleted nothing.

    The invariants are enforced here rather than trusted: ``filled_after == filled_before`` always,
    and ``work_required`` never shrinks. A report that violated them could not be constructed, so no
    caller can hand the log a sabotage that quietly ate a completed segment.
    """

    attempt_id: str
    project_id: str
    faction_id: str
    turn: int
    saboteur_id: str
    outcome: Outcome | None
    applied: tuple[SabotageConsequenceKind, ...] = ()
    filled_before: int = 0
    filled_after: int = 0
    work_required_before: int = 0
    work_required_after: int = 0
    released_units: int = 0
    paused: bool = False
    notes: tuple[str, ...] = ()
    seed: int | None = None
    schema_version: str = SABOTAGE_REPORT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not str(self.attempt_id).strip():
            raise OperationError("a sabotage report names its attempt")
        if self.filled_after != self.filled_before:
            raise OperationError(
                f"sabotage report {self.attempt_id!r} moves the clock from {self.filled_before} to "
                f"{self.filled_after} filled segments; a set-back may lengthen the road but issue "
                "#506's Phase-1 rules forbid deleting completed progress"
            )
        if self.work_required_after < self.work_required_before:
            raise OperationError(
                f"sabotage report {self.attempt_id!r} shortens the work required "
                f"({self.work_required_before} -> {self.work_required_after}); sabotage that reduces "
                "the work would be help, not harm"
            )
        if self.outcome is not None and not isinstance(self.outcome, Outcome):
            raise OperationError("a sabotage report's outcome is the approved Fate ladder, or None")

    @property
    def progress_preserved(self) -> bool:
        return self.filled_after == self.filled_before

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "attempt_id": self.attempt_id,
            "project_id": self.project_id,
            "faction_id": self.faction_id,
            "turn": self.turn,
            "saboteur_id": self.saboteur_id,
            "outcome": self.outcome.value if self.outcome is not None else None,
            "applied": [kind.value for kind in self.applied],
            "filled_before": self.filled_before,
            "filled_after": self.filled_after,
            "work_required_before": self.work_required_before,
            "work_required_after": self.work_required_after,
            "progress_preserved": self.progress_preserved,
            "released_units": self.released_units,
            "paused": self.paused,
            "notes": list(self.notes),
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> SabotageReport:
        if not isinstance(data, Mapping):
            raise OperationError(f"a sabotage report must be a mapping, got {type(data).__name__}")
        if data.get("schema_version") != SABOTAGE_REPORT_SCHEMA_VERSION:
            raise OperationError(
                f"unsupported sabotage-report schema_version {data.get('schema_version')!r}; "
                f"expected {SABOTAGE_REPORT_SCHEMA_VERSION!r}"
            )
        raw_outcome = data.get("outcome")
        try:
            outcome = Outcome(str(raw_outcome)) if raw_outcome is not None else None
        except ValueError as exc:
            raise OperationError(
                f"outcome {raw_outcome!r} is not one of the approved Fate outcomes"
            ) from exc
        applied: list[SabotageConsequenceKind] = []
        for item in data.get("applied") or ():
            try:
                applied.append(SabotageConsequenceKind(str(item)))
            except ValueError as exc:
                raise OperationError(f"applied consequence {item!r} is not one of the kinds") from exc
        return cls(
            attempt_id=str(data.get("attempt_id") or ""),
            project_id=str(data.get("project_id") or ""),
            faction_id=str(data.get("faction_id") or ""),
            turn=int(data.get("turn", 0)),
            saboteur_id=str(data.get("saboteur_id") or ""),
            outcome=outcome,
            applied=tuple(applied),
            filled_before=int(data.get("filled_before", 0)),
            filled_after=int(data.get("filled_after", 0)),
            work_required_before=int(data.get("work_required_before", 0)),
            work_required_after=int(data.get("work_required_after", 0)),
            released_units=int(data.get("released_units", 0)),
            paused=bool(data.get("paused", False)),
            notes=tuple(str(x) for x in (data.get("notes") or [])),
            seed=int(data["seed"]) if data.get("seed") is not None else None,
        )


def sabotage_from_dict(data: Mapping[str, Any]) -> SabotageReport:
    """Build a sabotage report from :meth:`SabotageReport.to_dict` output (the save/load seam)."""
    return SabotageReport.from_dict(data)


def resolve_sabotage(
    campaign: Campaign,
    attempt: SabotageAttempt,
    *,
    rng: Random,
    turn: int,
    roster: Mapping[str, object] | None = None,
) -> SabotageReport:
    """Resolve one disruption attempt and record a consequence the project cannot hide.

    The sequence is the one issue #506's engine already uses for every other check:

    1. **the target must be open.** A completed programme is closed (Phase 1's idempotent
       completion), so an attempt on it is refused rather than pretending to damage a record that no
       longer accumulates work;
    2. **the saboteur is a character, not a name.** A missing sheet is refused *before any dice* —
       the RNG is untouched — exactly as an unknown lead is;
    3. **one check, on the one kernel**, in the faction-agent context with the caller's proposal
       roster. The *approved* Fate ladder decides whether the disruption lands, and the ladder's own
       steps decide how many consequences of the attempt's declared menu land
       (:data:`TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME`). No new band is defined;
    4. **the consequence is legible and recorded**: the project's clock total grows, or it is paused
       with the reason, or its committed capacity is released — and the report states before/after
       for the clock, the units released and the pause. **``filled`` is never touched**;
    5. **one audit note**, and the attempt id is the key in ``Campaign.sabotages``, so a replayed
       turn applies nothing twice.
    """
    project = _project(campaign, attempt.project_id)
    faction = campaign.faction(project.faction_id)
    if project.clock.is_complete:
        raise OperationError(
            f"project {project.project_id!r} is complete at "
            f"{project.clock.filled}/{project.clock.work_required}; a closed programme accumulates "
            "no work, so there is nothing for sabotage to lengthen and no progress to preserve"
        )
    saboteur = campaign.sheets.get(attempt.saboteur_id)
    if saboteur is None:
        raise OperationError(
            f"attempt {attempt.attempt_id!r}: saboteur {attempt.saboteur_id!r} has no sheet on the "
            "campaign; inventing one would be inventing a character"
        )
    if attempt.saboteur_id == project.lead_id:
        raise OperationError(
            f"attempt {attempt.attempt_id!r}: {attempt.saboteur_id!r} is the project's own lead; a "
            "lead sabotaging its own programme is a different act from an outside disruption and "
            "this engine does not model it"
        )
    stored = campaign.sabotages.get(attempt.attempt_id)
    if stored is not None:
        return SabotageReport(
            attempt_id=stored.attempt_id,
            project_id=stored.project_id,
            faction_id=stored.faction_id,
            turn=stored.turn,
            saboteur_id=stored.saboteur_id,
            outcome=stored.outcome,
            applied=(),
            filled_before=stored.filled_before,
            filled_after=stored.filled_after,
            work_required_before=stored.work_required_before,
            work_required_after=stored.work_required_after,
            released_units=0,
            paused=stored.paused,
            notes=(
                (
                    f"attempt {attempt.attempt_id!r} was already resolved on turn {stored.turn}; a "
                    "replay applies nothing a second time"
                ),
                *stored.notes,
            ),
            seed=stored.seed,
        )

    check_result = check(
        saboteur,
        ActionContext.FACTION_AGENT,
        Action.OVERCOME,
        attempt.lead_skill,
        attempt.difficulty,
        rng=rng,
        strategic_roster=roster,
    )
    resolution = check_result.resolution
    seed = int(rng._seed) if isinstance(getattr(rng, "_seed", None), int) else None
    count = TUNING_SABOTAGE_CONSEQUENCES_BY_OUTCOME.get(resolution.outcome, 0)
    landed = tuple(attempt.consequences[:count])

    filled_before = project.clock.filled
    work_before = project.clock.work_required
    released = 0
    paused = False
    notes: list[str] = []
    if not landed:
        notes.append(
            f"the disruption failed ({resolution.outcome.value}, {resolution.total} against a guard "
            f"of {resolution.difficulty}): {project.project_id} is untouched at "
            f"{filled_before}/{work_before} segments and keeps its {faction.identifier!r} capacity"
        )
    for kind in landed:
        if kind is SabotageConsequenceKind.SETBACK:
            project.clock.work_required += TUNING_SABOTAGE_SETBACK_SEGMENTS
            notes.append(
                f"set-back: {project.project_id} needs {TUNING_SABOTAGE_SETBACK_SEGMENTS} further "
                f"segment(s) of work ({work_before} -> {project.clock.work_required}); the "
                f"{filled_before} segment(s) already completed are untouched"
            )
        elif kind is SabotageConsequenceKind.COMPLICATION:
            reason = (
                f"sabotage {attempt.attempt_id!r} on turn {turn}: the programme is interrupted and "
                f"keeps its {filled_before} completed segment(s)"
            )
            if project.paused:
                project.pause_reasons.append(reason)
            else:
                pause_project(campaign, project.project_id, reason)
            paused = True
            notes.append(
                f"complication: {project.project_id} is paused ({reason}) and resumes through "
                "projects.resume_project"
            )
        else:  # ALLOCATION_LOSS
            ledger = campaign.capacities.get(faction.identifier)
            released = ledger.release(project.project_id) if ledger is not None else 0
            notes.append(
                f"allocation loss: {released} unit(s) of {project.resource_kind!r} committed to "
                f"{project.project_id} returned to {faction.identifier!r}; the next capacity plan "
                "will show the shortage"
            )

    report = SabotageReport(
        attempt_id=attempt.attempt_id,
        project_id=project.project_id,
        faction_id=faction.identifier,
        turn=turn,
        saboteur_id=attempt.saboteur_id,
        outcome=resolution.outcome,
        applied=landed,
        filled_before=filled_before,
        filled_after=project.clock.filled,
        work_required_before=work_before,
        work_required_after=project.clock.work_required,
        released_units=released,
        paused=paused,
        notes=tuple(notes),
        seed=seed,
    )
    campaign.sabotages[attempt.attempt_id] = report
    project.detail.setdefault("sabotage_attempts", []).append(attempt.attempt_id)
    campaign.campaign_notes.append(
        {
            "kind": "sabotage",
            **report.to_dict(),
            "provenance": {
                "kind": ProvenanceKind.SIMULATED.value,
                "source": "strategy_game.operations.resolve_sabotage",
                "note": (
                    "a disruption records a longer road, an interruption or a lost allocation; it "
                    "never deletes completed progress (issue #506 Phase 1)"
                ),
            },
        }
    )
    return report


# -- the loop: research opens missions, missions feed research ------------------------------------


@dataclass(frozen=True)
class MissionOption:
    """A mission the RPG layer may now run because the faction holds a capability.

    Derived from ``Campaign.capabilities`` and stored nowhere else: what the faction *knows* is the
    capability, and the mission it opens is the option the author's node names in its yield. A node
    that names no option changes what a character can do inside a scene rather than opening a
    mission, and inventing a mission id for it here would be inventing content.
    """

    mission_id: str
    node_id: str
    label: str
    stage: ProjectStage
    branch: str = ""
    equipment: str = ""
    clue: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "mission_id": self.mission_id,
            "node_id": self.node_id,
            "label": self.label,
            "stage": self.stage.value,
            "branch": self.branch,
            "equipment": self.equipment,
            "clue": self.clue,
        }


def available_missions(campaign: Campaign) -> tuple[MissionOption, ...]:
    """Every mission the faction's held capabilities open, in node-id order.

    The research→mission half of the loop, and the reason ``ResearchYield.option`` exists: a
    completed programme hands the RPG layer a choice it did not have. Nothing is written here.
    """
    missions: list[MissionOption] = []
    for node_id in sorted(campaign.capabilities):
        node = campaign.capabilities[node_id]
        if not node.yields.option:
            continue
        missions.append(
            MissionOption(
                mission_id=node.yields.option,
                node_id=node.node_id,
                label=node.label,
                stage=node.stage,
                branch=node.branch,
                equipment=node.yields.equipment,
                clue=node.yields.clue,
            )
        )
    return tuple(missions)


@dataclass(frozen=True)
class ProjectInput:
    """What one resolved mission did for one project — the mission→research half of the loop."""

    project_id: str
    ready: bool
    satisfied_by_report: tuple[str, ...] = ()
    missing: tuple[str, ...] = ()
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "ready": self.ready,
            "satisfied_by_report": list(self.satisfied_by_report),
            "missing": list(self.missing),
            "note": self.note,
        }


def project_inputs(
    campaign: Campaign,
    report: MissionOutcome,
    *,
    faction_id: str | None = None,
) -> tuple[ProjectInput, ...]:
    """Which of the faction's projects a resolved mission has just made possible.

    Read **after** :func:`strategy_game.campaign.missions.apply_mission_outcome`, and read-only: the
    ids the mission reported are checked against the faction's inventory and each project's
    ``requires.resource_ids``, so the answer is about world state and not about the report's prose.
    A report that was never applied therefore shows as *not ready*, which is the honest answer.
    """
    faction = campaign.faction(faction_id)
    gained = {
        *report.resources_gained,
        *report.intel_gained,
        *report.evidence_gained,
    }
    held = set(faction.resources)
    inputs: list[ProjectInput] = []
    for pid, project in sorted(campaign.projects.items()):
        if project.faction_id != faction.identifier or project.clock.is_complete:
            continue
        # An id counts only if the faction now *holds* it: a report that was never applied names
        # ids the world does not have, and claiming otherwise would make this a reading of prose.
        satisfied = tuple(sorted(gained & set(project.requires.resource_ids) & held))
        missing = unsatisfied_prerequisites(campaign, project)
        if not missing and satisfied:
            note = (
                f"{pid} is startable now: the mission supplied {', '.join(satisfied)} and the "
                "project's prerequisites are all held"
            )
        elif not missing:
            note = f"{pid} needed nothing from this mission; it was already startable"
        elif satisfied:
            note = (
                f"{pid} still misses {', '.join(missing)}; the mission supplied "
                f"{', '.join(satisfied)} but not everything it needs"
            )
        else:
            note = (
                f"{pid} still misses {', '.join(missing)}; the mission added nothing it holds, "
                "because a reported id is not a held one until the mission outcome is applied"
            )
        inputs.append(
            ProjectInput(
                project_id=pid,
                ready=not missing,
                satisfied_by_report=satisfied,
                missing=missing,
                note=note,
            )
        )
    return tuple(inputs)

