"""The headless mission session: turns, movement, interactions and the mission's outcome (#515).

This is the spike's proof that a tactical mission layer can exist **before** a renderer is chosen.
It imports no drawing library, holds no pixel, and answers a UI in cells: *select one of four agents,
ask it to move somewhere, ask it to look at something*. In return it reports what happened, in the
same approved Fate vocabulary the rest of the crossover uses.

What is reused, and from where
------------------------------

============================  ==========================================================
turns (one action/character)  :class:`strategy_game.rpg.roster.TurnLedger`, over the four
                              **agent** seats of the approved one-leader/four-agent roster
                              (:func:`rpg.roster.default_seats`, #461/#482)
the squad                     :meth:`strategy_game.campaign.state.Campaign.agent_views` —
                              the faction's declared member agents, each with one
                              :class:`rpg.fate.Character` sheet held by identity
checks                        :func:`strategy_game.rpg.skills.check` in
                              :attr:`rpg.skills.ActionContext.INDIVIDUAL` — the approved
                              Fate kernel, six individual skills, 4dF
wounds                        :func:`strategy_game.rpg.scene.apply_hit` — stress boxes
                              and a mild consequence, exactly as a scene applies a hit
mission outcome               :class:`strategy_game.campaign.missions.MissionOutcome` and
                              :func:`~strategy_game.campaign.missions.apply_mission_outcome`,
                              the one tested writer of faction state
============================  ==========================================================

What is deliberately **not** invented
--------------------------------------

* **No movement cost.** One move is one action, whatever its length. Pricing a step (or a door, or
  difficult ground) is a rules decision nobody has made, so this session counts steps only to report
  them.
* **No occupancy rule beyond the destination.** A route may pass through another agent, but two agents
  may not end on one cell. That is the minimum needed to keep four tokens distinguishable on a map,
  and it is stated here as a spike convention, not as a rule.
* **No initiative, no combat round, no enemy, no line of sight, no cover, no stealth, no PSI, no
  hacking.** #515 lists them as later milestones. A mission here can talk, read and confront; it cannot
  fight a battle.
* **No new outcome scale.** The mission's outcome is the ``Outcome`` of the check that completed its
  last required objective — reported, not aggregated, because no aggregation rule exists. A mission
  with no decisive check has no mission-level outcome and says so instead of inventing one.
* **No consequence of a tie.** A tie grants nothing and wounds nobody; what "succeed at a minor cost"
  costs here is an author decision (#506's row D27 records the same open question for projects).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Any

from ..campaign.missions import MissionOutcome, apply_mission_outcome
from ..campaign.state import Campaign
from ..rpg import skills as rpg_skills
from ..rpg.fate import Character, Outcome, Resolution
from ..rpg.roster import (
    AGENT_SEAT_COUNT,
    RosterError,
    Seat,
    SeatKind,
    TurnLedger,
    default_seats,
)
from ..rpg.scene import apply_hit
from ..rpg.skills import ActionContext, SkillLayerError
from .grid import Cell, Grid
from .mission import Interaction, InteractionKind, MissionError, MissionSpec, Objective

__all__ = [
    "DEFAULT_SEED",
    "InteractionResult",
    "MissionSession",
    "MoveResult",
    "ObjectiveStatus",
]

#: Seed of the session's own dice when a caller supplies none. Recorded in the mission report so a
#: result can be replayed; a caller that injects an rng owns its own determinism.
DEFAULT_SEED = 515

#: Fate's mild consequence: the one severity a single failed check writes onto a sheet.
MILD_CONSEQUENCE = 2


@dataclass(frozen=True)
class MoveResult:
    """The answer to one click-to-move request.

    A refusal is a **result**, not an exception: a misclick on a wall is ordinary play, and the reason
    is written for the person who clicked. ``steps`` are the cells walked through, excluding the
    starting cell, so a renderer can animate them without asking the map again.
    """

    ok: bool
    seat_id: str
    destination: Cell | None = None
    steps: tuple[Cell, ...] = ()
    reason: str = ""


@dataclass(frozen=True)
class InteractionResult:
    """What one dialogue, clue or confrontation produced."""

    ok: bool
    interaction_id: str
    outcome: Outcome | None = None
    shifts: int = 0
    evidence: tuple[str, ...] = ()
    intel: tuple[str, ...] = ()
    objectives: tuple[str, ...] = ()
    #: The consequence written onto the sheet by a failed confrontation, if any.
    wound: str = ""
    reason: str = ""


@dataclass(frozen=True)
class ObjectiveStatus:
    id: str
    label: str
    required: bool
    done: bool


@dataclass
class MissionSession:
    """One mission in progress: the map, four agent seats, their positions and the ledger.

    The session never writes faction state during play. It **reports** — :meth:`report` — and writes
    once, through :func:`campaign.missions.apply_mission_outcome`, when :meth:`complete` is called.
    The one exception is a wound: :func:`rpg.scene.apply_hit` mutates the character's live sheet, which
    the campaign holds by identity, so a consequence taken mid-mission is already on the sheet that
    ``save_campaign`` writes.
    """

    spec: MissionSpec
    campaign: Campaign
    seed: int = DEFAULT_SEED
    rng: Random | None = None
    _position: dict[str, Cell] = field(default_factory=dict, init=False, repr=False)
    _selected: str | None = field(default=None, init=False)
    _completed: dict[str, Interaction] = field(default_factory=dict, init=False, repr=False)
    _checks: dict[str, Resolution] = field(default_factory=dict, init=False, repr=False)
    _decisive: tuple[str, Resolution] | None = field(default=None, init=False, repr=False)
    _evidence: list[str] = field(default_factory=list, init=False, repr=False)
    _intel: list[str] = field(default_factory=list, init=False, repr=False)
    _wounds: list[dict[str, Any]] = field(default_factory=list, init=False, repr=False)
    _applied: MissionOutcome | None = field(default=None, init=False, repr=False)
    seats: tuple[Seat, ...] = field(default=(), init=False)
    ledger: TurnLedger = field(init=False, repr=False)
    _dice: Random = field(default_factory=Random, init=False, repr=False)

    def __post_init__(self) -> None:
        faction = self.campaign.faction()
        agents = self.campaign.agent_views()
        if len(agents) != AGENT_SEAT_COUNT:
            raise MissionError(
                f"a mission is played by {AGENT_SEAT_COUNT} agents (#461/#482); faction "
                f"{faction.identifier!r} declares {len(agents)}. Deploying a different number is an "
                "author decision, not a default."
            )
        if self.spec.case_id not in self.campaign.cases:
            raise MissionError(
                f"mission {self.spec.mission_id!r} resolves case {self.spec.case_id!r}, which is not "
                "on this campaign; a mission without its case has nowhere to record evidence"
            )
        all_seats = default_seats(self.campaign.leader_id, tuple(a.identifier for a in agents))
        # The four **agent** seats, in the roster's own order; the leader chairs the faction and does
        # not deploy (the PC keeps the faction-leader role, #502/#515).
        self.seats = tuple(seat for seat in all_seats if seat.kind is SeatKind.AGENT)
        if len(self.seats) != AGENT_SEAT_COUNT:
            raise MissionError(
                f"a mission deploys the {AGENT_SEAT_COUNT} agent seats; the roster produced "
                f"{len(self.seats)}"
            )
        self.ledger = TurnLedger(self.seats)
        self._position = {
            seat.id: cell for seat, cell in zip(self.seats, self.spec.deploy_cells)
        }
        self._dice = self.rng if self.rng is not None else Random(self.seed)

    # -- roster and turn -------------------------------------------------------

    @property
    def seat_ids(self) -> tuple[str, ...]:
        return tuple(seat.id for seat in self.seats)

    @property
    def selected(self) -> str | None:
        return self._selected

    @property
    def turn(self) -> int:
        return self.ledger.turn

    @property
    def grid(self) -> Grid:
        return self.spec.grid

    def seat(self, seat_id: str) -> Seat:
        for seat in self.seats:
            if seat.id == seat_id:
                return seat
        raise MissionError(f"no agent seat {seat_id!r} in this mission; seats are {list(self.seat_ids)}")

    def sheet(self, seat_id: str) -> Character:
        seat = self.seat(seat_id)
        sheet = self.campaign.sheets.get(seat.character_id)
        if sheet is None:  # pragma: no cover - Campaign refuses a member without a sheet
            raise MissionError(f"seat {seat_id!r} holds {seat.character_id!r}, which has no sheet")
        return sheet

    def select(self, seat_id: str) -> Seat:
        """Make one agent the active one. Selection is UI state and costs no action."""
        seat = self.seat(seat_id)
        self._selected = seat.id
        return seat

    def position(self, seat_id: str) -> Cell:
        self.seat(seat_id)
        return self._position[seat_id]

    def position_of_character(self, character_id: str) -> Cell:
        for seat in self.seats:
            if seat.character_id == character_id:
                return self._position[seat.id]
        raise MissionError(f"character {character_id!r} is not deployed on this mission")

    def end_turn(self) -> int:
        """Close the turn and refresh every agent's action. The selection is kept."""
        return self.ledger.next_turn()

    def has_acted(self, seat_id: str) -> bool:
        return seat_id in self.ledger.acted

    # -- movement --------------------------------------------------------------

    def request_move(self, seat_id: str, target: Cell | tuple[int, int] | list[int]) -> MoveResult:
        """Resolve a click-to-move request through pathfinding.

        Refusals are returned, never raised, and each names its cause: the wrong agent is selected, the
        character has already acted this turn, the destination is occupied, the destination is a wall or
        a shut door or outside the grid, or no route exists. Only an unknown seat id raises, because
        that is a programming error rather than a click.
        """
        seat = self.seat(seat_id)
        if self._selected != seat.id:
            return MoveResult(
                False,
                seat.id,
                reason=(
                    f"{seat.id} is not the selected agent (selected: {self._selected or 'none'}); "
                    "select it before ordering a move — one agent acts at a time"
                ),
            )
        cell = target if isinstance(target, Cell) else Cell.from_pair(target, what="a move target")
        if not self.grid.in_bounds(cell):
            return MoveResult(
                False, seat.id, destination=cell,
                reason=f"the target {cell} is outside the {self.grid.width}x{self.grid.height} grid",
            )
        occupant = next(
            (other for other, where in self._position.items() if where == cell and other != seat.id),
            None,
        )
        if occupant is not None:
            return MoveResult(
                False, seat.id, destination=cell,
                reason=f"the target {cell} is occupied by {occupant}",
            )
        origin = self._position[seat.id]
        path = self.grid.path(origin, cell)
        if not path.ok:
            return MoveResult(False, seat.id, destination=cell, reason=path.reason)
        if not path.steps:
            return MoveResult(
                False, seat.id, destination=cell,
                reason=f"{seat.id} already stands at {cell}; a move needs a different destination",
            )
        refused = self._claim_action(seat, f"move to {cell}")
        if refused:
            return MoveResult(False, seat.id, destination=cell, reason=refused)
        self._position[seat.id] = cell
        return MoveResult(True, seat.id, destination=cell, steps=path.steps)

    def _claim_action(self, seat: Seat, statement: str) -> str:
        """Take this turn's action for the seat, returning the ledger's own refusal text if it may not.

        The refusal wording is the ledger's, deliberately: one implementation of "one action per
        character per turn" exists in this repository (#461/#482) and this session does not restate it.
        """
        try:
            self.ledger.declare(seat.id, statement=statement)
        except RosterError as exc:
            return str(exc)
        return ""

    # -- interactions ----------------------------------------------------------

    def interact(self, seat_id: str, interaction_id: str) -> InteractionResult:
        """Resolve one dialogue, clue or confrontation from the selected agent.

        Refusals (wrong agent, action already spent, out of reach, prerequisite unmet, hook already
        resolved) are returned with their reason. An attempted check **does** spend the action whether
        it succeeds or fails; that is the turn structure, not a new rule.
        """
        seat = self.seat(seat_id)
        if self._selected != seat.id:
            return InteractionResult(
                False, interaction_id,
                reason=(
                    f"{seat.id} is not the selected agent (selected: {self._selected or 'none'}); "
                    "select it before interacting"
                ),
            )
        interaction = self.spec.interaction(interaction_id)
        if interaction.id in self._completed:
            return InteractionResult(
                False, interaction.id,
                reason=f"{interaction.id!r} is already resolved; a clue is read once per mission",
            )
        missing = tuple(r for r in interaction.requires if r not in self._completed)
        if missing:
            return InteractionResult(
                False, interaction.id,
                reason=(
                    f"{interaction.id!r} requires {list(missing)} first; "
                    f"resolved so far: {sorted(self._completed) or 'nothing'}"
                ),
            )
        where = self._position[seat.id]
        distance = abs(where.row - interaction.at.row) + abs(where.col - interaction.at.col)
        if distance > 1:
            return InteractionResult(
                False, interaction.id,
                reason=(
                    f"{seat.id} stands at {where}; the {interaction.kind.value} at {interaction.at} is "
                    f"{distance} cells away — an interaction needs an adjacent cell (or the cell itself)"
                ),
            )
        refused = self._claim_action(seat, f"{interaction.kind.value} {interaction.id}")
        if refused:
            return InteractionResult(False, interaction.id, reason=refused)

        if not interaction.has_check:
            return self._resolve_success(
                seat,
                interaction,
                outcome=None,
                shifts=0,
                evidence=interaction.evidence,
                intel=interaction.intel,
                objectives=interaction.objectives,
            )

        assert interaction.action is not None and interaction.skill and interaction.difficulty is not None
        try:
            check = rpg_skills.check(
                self.sheet(seat.id),
                ActionContext.INDIVIDUAL,
                interaction.action,
                interaction.skill,
                interaction.difficulty,
                rng=self._dice,
            )
        except SkillLayerError as exc:  # pragma: no cover - the loader validates the skill
            raise MissionError(f"interaction {interaction.id!r}: {exc}") from exc
        resolution = check.resolution
        self._checks[interaction.id] = resolution
        if resolution.shifts > 0:
            return self._resolve_success(
                seat,
                interaction,
                outcome=resolution.outcome,
                shifts=resolution.shifts,
                evidence=interaction.evidence,
                intel=interaction.intel,
                objectives=interaction.objectives,
            )

        wound = ""
        if interaction.kind is InteractionKind.CONFRONTATION and interaction.consequence:
            wound = self._wound(seat, interaction, resolution.shifts)
        if resolution.shifts == 0:
            why = "the check tied (0 shifts): a tie grants nothing here and costs nothing"
        else:
            why = f"the check failed by {abs(resolution.shifts)} shift(s): nothing is granted"
        return InteractionResult(
            False, interaction.id, outcome=resolution.outcome, shifts=resolution.shifts,
            wound=wound, reason=why,
        )

    def _resolve_success(
        self,
        seat: Seat,
        interaction: Interaction,
        *,
        outcome: Outcome | None,
        shifts: int,
        evidence: tuple[str, ...],
        intel: tuple[str, ...],
        objectives: tuple[str, ...],
    ) -> InteractionResult:
        self._completed[interaction.id] = interaction
        for item in evidence:
            if item not in self._evidence:
                self._evidence.append(item)
        for item in intel:
            if item not in self._intel:
                self._intel.append(item)
        if outcome is not None:
            required_done = set(objectives) & {o.id for o in self.spec.required_objectives}
            if required_done:
                # The last check that closes a required objective is the mission's decisive one; the
                # mission outcome is its Outcome, reported rather than aggregated.
                self._decisive = (interaction.id, self._checks[interaction.id])
        return InteractionResult(
            True, interaction.id, outcome=outcome, shifts=shifts,
            evidence=evidence, intel=intel, objectives=objectives,
        )

    def _wound(self, seat: Seat, interaction: Interaction, shifts: int) -> str:
        """Apply one failed confrontation's hit through the approved scene helper.

        A mild consequence names the wound in the mission data; if that slot is already occupied the
        hit is taken on the stress track alone rather than fabricating a second consequence. Whether
        "taken out" ends a character's mission is not decided here — the fact is recorded, and what it
        means stays with Fate's own procedure and the GM.
        """
        sheet = self.sheet(seat.id)
        occupied = any(
            c.severity == MILD_CONSEQUENCE and not c.recovered for c in sheet.consequences
        )
        consequence = None if occupied else (interaction.consequence, MILD_CONSEQUENCE)
        hit = apply_hit(sheet, max(1, -shifts), consequence=consequence)
        self._wounds.append(
            {
                "seat": seat.id,
                "character": sheet.id,
                "interaction": interaction.id,
                "consequence": "" if consequence is None else consequence[0],
                "stress_box": hit.stress_box,
                "taken_out": hit.taken_out,
            }
        )
        return "" if consequence is None else consequence[0]

    # -- objectives and completion ---------------------------------------------

    def objectives(self) -> tuple[ObjectiveStatus, ...]:
        done = {oid for item in self._completed.values() for oid in item.objectives}
        return tuple(
            ObjectiveStatus(o.id, o.label, o.required, o.id in done) for o in self.spec.objectives
        )

    @property
    def mission_complete(self) -> bool:
        return all(status.done for status in self.objectives() if status.required)

    def outstanding_required_objectives(self) -> tuple[Objective, ...]:
        done = {status.id for status in self.objectives() if status.done}
        return tuple(o for o in self.spec.required_objectives if o.id not in done)

    def complete(self) -> MissionOutcome:
        """Finish the mission and write its outcome into the campaign's persistent state.

        Refuses while a required objective is open, and refuses a mission with no decisive check
        because the report's ``outcome`` must be one the engine actually produced. Idempotent: the
        second call returns the record already applied instead of writing twice.
        """
        if self._applied is not None:
            return self._applied
        outstanding = self.outstanding_required_objectives()
        if outstanding:
            raise MissionError(
                f"mission {self.spec.mission_id!r} is not complete; required objective(s) still open: "
                f"{[o.id for o in outstanding]}"
            )
        if self._decisive is None:
            raise MissionError(
                "no resolved check completed a required objective, so this mission has no "
                "mission-level Fate outcome to report; an aggregation rule would have to be approved "
                "first, and this spike does not invent one"
            )
        decisive = self._decisive[1]
        done = [status for status in self.objectives() if status.done]
        report = MissionOutcome(
            mission_id=self.spec.mission_id,
            case_id=self.spec.case_id,
            outcome=decisive.outcome,
            leader_id=self.campaign.leader_id,
            agent_ids=tuple(seat.character_id for seat in self.seats),
            evidence_gained=tuple(self._evidence),
            intel_gained=tuple(self._intel),
            objectives_completed=tuple(status.label for status in done),
            seed=None if self.rng is not None else self.seed,
        )
        self._applied = apply_mission_outcome(self.campaign, report)
        return self._applied

    # -- headless state report -------------------------------------------------

    def report(self) -> dict[str, Any]:
        """The mission's state as plain JSON — everything a renderer may read, and nothing visual.

        A renderer draws this: seats, cells, which hooks are resolved, which objectives are done. It
        cannot learn a sprite, a colour or a camera from here, because the mission layer has none.
        """
        return {
            "mission_id": self.spec.mission_id,
            "case_id": self.spec.case_id,
            "title": self.spec.title,
            "turn": self.turn,
            "selected": self._selected,
            "complete": self.mission_complete,
            "applied": self._applied is not None,
            "seed": None if self.rng is not None else self.seed,
            "grid": {"width": self.grid.width, "height": self.grid.height},
            "agents": [
                {
                    "seat": seat.id,
                    "character": seat.character_id,
                    "position": self._position[seat.id].to_pair(),
                    "acted": self.has_acted(seat.id),
                }
                for seat in self.seats
            ],
            "interactions": [
                {"id": item.id, "kind": item.kind.value, "at": item.at.to_pair(),
                 "resolved": item.id in self._completed, "optional": item.optional}
                for item in self.spec.interactions
            ],
            "objectives": [
                {"id": status.id, "label": status.label, "required": status.required,
                 "done": status.done}
                for status in self.objectives()
            ],
            "evidence": list(self._evidence),
            "intel": list(self._intel),
            "wounds": [dict(wound) for wound in self._wounds],
        }
