"""The universal strategic-project engine: agent-lead check, faction throughput, work clock (#506).

Issue #506 asks for **one** incremental-action mechanic used by every faction strategy operation:

* **an agent-led skill check** decides whether the organisation can execute *productively this
  turn*. It is resolved through the **one** approved Fate kernel
  (:func:`strategy_game.rpg.skills.check`), in the faction-agent context, against the proposed
  strategic roster the caller passes in. There is deliberately **no second resolution path** here:
  a cross-layer skill name, an unknown name, a missing proposal roster and an ungranted capability
  are refused by that kernel **before any dice**, exactly as they are in a scene;
* **faction resources** decide *how much work a successful turn achieves*. The lead keeps a
  programme coordinated; the institution decides its scale. So the segments added on success are the
  faction's **committed throughput** for that project (:class:`FactionCapacity`), never the lead's
  rating, and never a number derived from the check's shifts;
* a **multi-turn progress clock** (:class:`ProjectClock`) holds the accumulated work until the
  author's difficulty-defined total is reached, and reports *why* a turn produced what it did
  (:class:`ProjectResult` / :class:`ProgressCause`).

``filled`` never decreases. A failed check adds **zero** and preserves every completed segment; a
turn the faction committed nothing to adds zero as well and says so, which is a different fact from
a failed check and is reported as a different cause. The opportunity cost of a stalled round is the
lead's action for the turn — already the structure ``strategy_game.rpg.roster.TurnLedger`` enforces
(one action per character per turn) — so this module invents no second price for failure.

What this module does **not** decide
------------------------------------

* No dice band, difficulty, work total, throughput figure or duration is *approved* here. The three
  numbers the engine needs are :data:`TUNING_CLOCK_BASE_SEGMENTS`,
  :data:`TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY`, :data:`TUNING_CLOCK_MAX_SEGMENTS` and
  :data:`TUNING_STYLE_BONUS_SEGMENTS`, and every one is named ``TUNING_`` so no reader mistakes a
  convention for canon. Issue #506 says the bands "should be aligned with existing rules and
  tested", so they are documented, tested and carried as two rows of ``docs/design/AUTHOR_DECISION_QUEUE.md``;
* discovery, prototype and manufacture are **not** one progress bar. :class:`ProjectStage` names
  which of issue #506's six stages a project's *completion* produces, and completing a project
  grants exactly that stage — a successor project is required for the next one;
* nothing here is per-faction bookkeeping beyond one ledger per faction id and one project per
  project id: no mission board, no assignment loop, no rival-faction simulation (Phase 2/3 scope).
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from random import Random
from typing import TYPE_CHECKING, Any

from .campaign.state import CampaignError
from .provenance import ProvenanceKind
from .rpg.fate import Action, Outcome
from .rpg.scene import Scene
from .rpg.skills import ActionContext, capabilities_of, check

if TYPE_CHECKING:  # no runtime cycle: campaign.state loads project records lazily
    from .campaign.state import Campaign

__all__ = [
    "PROJECT_RESULT_SCHEMA_VERSION",
    "STAGE_MEANINGS",
    "TUNING_CLOCK_BASE_SEGMENTS",
    "TUNING_CLOCK_MAX_SEGMENTS",
    "TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY",
    "TUNING_STYLE_BONUS_SEGMENTS",
    "Allocation",
    "FactionCapacity",
    "Prerequisites",
    "ProgressCause",
    "ProjectClock",
    "ProjectCompletion",
    "ProjectError",
    "ProjectResult",
    "ProjectStage",
    "StrategicProject",
    "advance_project",
    "capacity_from_dict",
    "clock_for_difficulty",
    "complete_project",
    "pause_project",
    "project_from_dict",
    "reassign_project",
    "resume_project",
    "unsatisfied_prerequisites",
]

#: Shape marker of the per-turn result *report* (the same discipline ``missions.py`` applies to a
#: mission report: a report that is stored names the schema that produced it).
PROJECT_RESULT_SCHEMA_VERSION = "project-result-1"

#: **TUNING PARAMETER — not canon.** The segments a clock starts from, and the segments each step of
#: the check's difficulty adds. Issue #506 states that difficulty legitimately influences both the
#: check target *and* the work required, and that this must not double-penalise until a major project
#: becomes impossible; these two numbers plus :data:`TUNING_CLOCK_MAX_SEGMENTS` are the smallest
#: convention that satisfies both, and they are awaiting an author ruling (row D27 of
#: ``docs/design/AUTHOR_DECISION_QUEUE.md``).
TUNING_CLOCK_BASE_SEGMENTS = 8
TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY = 2

#: **TUNING PARAMETER — not canon.** The ceiling :func:`clock_for_difficulty` will not exceed, so the
#: hardest project stays finite. 20 segments is five turns at a committed throughput of four.
TUNING_CLOCK_MAX_SEGMENTS = 20

#: **TUNING PARAMETER — not canon.** The extra segment a *success with style* adds on top of the
#: faction's committed throughput. It is deliberately smaller than the throughput the examples
#: commit (three), because issue #506 requires the lead's check to allow only "limited
#: quality/special-success effects" and never to replace institutional capacity.
TUNING_STYLE_BONUS_SEGMENTS = 1


class ProjectError(CampaignError):
    """A project, clock or capacity operation the Phase-1 schema does not allow."""


class ProjectStage(str, Enum):
    """Which of issue #506's stages a project's **completion** produces.

    The issue's own sentence is the vocabulary: "Distinguish known principles, scientific
    understanding, engineering prototypes, reproducible manufacture, deployment/infrastructure, and
    society-wide adoption." The six are an **ordered ladder of separate stages**, not six points on
    one progress bar: a project completes into exactly one of them, and reaching the next one is a
    separate project with its own prerequisites. That is how "without conflating discovery, prototype
    and manufacturing" is enforced structurally rather than by a rule the caller must remember.
    """

    PRINCIPLES = "known_principles"
    UNDERSTANDING = "scientific_understanding"
    PROTOTYPE = "engineering_prototype"
    MANUFACTURE = "reproducible_manufacture"
    DEPLOYMENT = "deployment_infrastructure"
    ADOPTION = "society_wide_adoption"


#: The issue's phrase for each stage, quoted so the vocabulary stays the author's rather than a
#: paraphrase this module invented.
STAGE_MEANINGS: Mapping[ProjectStage, str] = {
    ProjectStage.PRINCIPLES: "known principles",
    ProjectStage.UNDERSTANDING: "scientific understanding",
    ProjectStage.PROTOTYPE: "engineering prototypes",
    ProjectStage.MANUFACTURE: "reproducible manufacture",
    ProjectStage.DEPLOYMENT: "deployment/infrastructure",
    ProjectStage.ADOPTION: "society-wide adoption",
}


class ProgressCause(str, Enum):
    """Why a turn produced the number of segments it produced. The player-visible "why".

    A stalled turn is not one fact: a check that failed, a check that tied, a round the faction
    committed nothing to, and a project that is paused because it lost a prerequisite are four
    different situations, and an engine that collapsed them into "no progress" would make failure
    illegible — which issue #506 explicitly forbids.
    """

    ADVANCED = "advanced"
    COMPLETED = "completed"
    CHECK_FAILED = "check_failed"
    TIE = "tie"
    NO_CAPACITY = "no_capacity"
    PAUSED = "paused"
    ALREADY_COMPLETE = "already_complete"


@dataclass
class ProjectClock:
    """The project's work clock: ``filled`` of ``work_required`` segments.

    Work is counted in **segments** (issue #506: "Track tangible work units or filled clock
    segments"). :meth:`add` is the only mutator and it can only ever increase ``filled``, clamped at
    ``work_required``: no operation in this module reduces progress, and none can overfill the clock.
    """

    work_required: int
    filled: int = 0

    def __post_init__(self) -> None:
        if not isinstance(self.work_required, int) or self.work_required < 1:
            raise ProjectError("a clock needs at least one segment of work")
        if not isinstance(self.filled, int) or self.filled < 0:
            raise ProjectError("filled segments cannot be negative")
        if self.filled > self.work_required:
            raise ProjectError(
                f"a clock cannot be filled past its total ({self.filled} > {self.work_required}); "
                "a snapshot like that is corruption, not a state to clamp silently"
            )

    @property
    def remaining(self) -> int:
        return max(0, self.work_required - self.filled)

    @property
    def is_complete(self) -> bool:
        return self.filled >= self.work_required

    def add(self, work: int) -> int:
        """Add work and return the segments **actually** added.

        Returns less than ``work`` when the clock fills: the excess is not banked anywhere, because
        banking it would carry over capacity the faction did not commit. ``work`` of zero is legal
        and adds nothing.
        """
        if not isinstance(work, int) or work < 0:
            raise ProjectError("work added to a clock must be a nonnegative integer")
        added = min(work, self.remaining)
        self.filled += added
        return added

    def to_dict(self) -> dict[str, Any]:
        return {"work_required": self.work_required, "filled": self.filled}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ProjectClock:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a clock record must be a mapping, got {type(data).__name__}")
        return cls(
            work_required=int(data.get("work_required", 0)),
            filled=int(data.get("filled", 0)),
        )


def clock_for_difficulty(difficulty: int) -> ProjectClock:
    """The engine's convention for turning a check difficulty into a work total.

    ``difficulty`` drives both numbers — the check target the caller passes to
    :func:`advance_project` and this total — which is what issue #506 asks for. The ceiling keeps
    that from compounding into an impossible project, and the whole convention is a tuning
    parameter (module docstring) rather than an approved rule.
    """
    if not isinstance(difficulty, int) or difficulty < 0:
        raise ProjectError("difficulty must be a nonnegative integer")
    segments = TUNING_CLOCK_BASE_SEGMENTS + TUNING_CLOCK_SEGMENTS_PER_DIFFICULTY * difficulty
    return ProjectClock(min(segments, TUNING_CLOCK_MAX_SEGMENTS))


@dataclass(frozen=True)
class Prerequisites:
    """What must already be true before a project can produce work.

    Issue #506's list of prerequisites — "access to specimen/artefact/archive/data, lab or
    manufacturing facilities, personnel and security, diplomacy, particular expertise, or a
    resolved RPG mission" — is split into the two kinds the repository already has vocabulary for,
    and **no new inventory is created for either**:

    * ``resource_ids`` are ids the faction holds in ``CampaignFaction.resources``. A specimen, an
      archive, a lab and a personnel detail are all held-resource ids in that one book, so a
      mission-sourced artefact arrives here through
      :func:`strategy_game.campaign.missions.apply_mission_outcome` and nothing else;
    * ``node_ids`` are capability node ids the faction already holds in ``Campaign.capabilities`` —
      the previous stage of the same technology, which is what keeps discovery, prototype and
      manufacture from collapsing into one bar.

    "Particular expertise" is **not** here: an expertise requirement is
    :attr:`StrategicProject.required_capability`, the capability gate issue #482 already gives the
    kernel, so it is refused before any dice instead of being silently satisfied.
    """

    resource_ids: tuple[str, ...] = ()
    node_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name, values in (("resource_ids", self.resource_ids), ("node_ids", self.node_ids)):
            if len(set(values)) != len(values):
                raise ProjectError(f"prerequisites.{name} repeats an id: {sorted(values)}")
            for value in values:
                if not str(value).strip():
                    raise ProjectError(f"prerequisites.{name} carries an empty id")

    def is_empty(self) -> bool:
        return not self.resource_ids and not self.node_ids

    def to_dict(self) -> dict[str, Any]:
        return {"resource_ids": list(self.resource_ids), "node_ids": list(self.node_ids)}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> Prerequisites:
        if data is None:
            return cls()
        if not isinstance(data, Mapping):
            raise ProjectError(f"a prerequisites record must be a mapping, got {type(data).__name__}")
        return cls(
            resource_ids=tuple(str(x) for x in (data.get("resource_ids") or [])),
            node_ids=tuple(str(x) for x in (data.get("node_ids") or [])),
        )


@dataclass(frozen=True)
class Allocation:
    """One faction's commitment of ``units`` of one resource kind to one project, per turn."""

    project_id: str
    resource_kind: str
    units: int

    def __post_init__(self) -> None:
        if not str(self.project_id).strip():
            raise ProjectError("an allocation names its project")
        if not str(self.resource_kind).strip():
            raise ProjectError("an allocation names its resource kind")
        if not isinstance(self.units, int) or self.units < 0:
            raise ProjectError("an allocation is a nonnegative integer number of units")

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "resource_kind": self.resource_kind,
            "units": self.units,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Allocation:
        if not isinstance(data, Mapping):
            raise ProjectError(f"an allocation record must be a mapping, got {type(data).__name__}")
        return cls(
            project_id=str(data.get("project_id") or ""),
            resource_kind=str(data.get("resource_kind") or ""),
            units=int(data.get("units", 0)),
        )


@dataclass
class FactionCapacity:
    """One faction's throughput ledger: what it has, and what it has committed to which project.

    ``units`` is the faction's per-turn capacity **by resource kind** ("personnel, facilities,
    equipment, data, funding, time", in issue #506's words — the kinds are data, not a closed
    vocabulary this module invents). ``commitments`` is what is promised to each project, so a
    shortage is a fact the ledger can state (:meth:`free`) rather than a rule the caller must
    remember. Allocation is a *membership* change like every other book in the campaign: it can be
    made, replaced and released, and it moves no number outside this record.
    """

    faction_id: str
    units: dict[str, int] = field(default_factory=dict)
    commitments: list[Allocation] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not str(self.faction_id).strip():
            raise ProjectError("a capacity ledger names its faction")
        for kind, value in self.units.items():
            if not str(kind).strip() or not isinstance(value, int) or value < 0:
                raise ProjectError(f"capacity units for {kind!r} must be a nonnegative integer")
        allocations = [a for a in self.commitments]
        ids = [a.project_id for a in allocations]
        if len(set(ids)) != len(ids):
            raise ProjectError(f"a project is allocated capacity once; got {sorted(ids)}")
        for kind in {a.resource_kind for a in allocations}:
            committed = sum(a.units for a in allocations if a.resource_kind == kind)
            if committed > self.units.get(kind, 0):
                raise ProjectError(
                    f"faction {self.faction_id!r} commits {committed} units of {kind!r} but has "
                    f"{self.units.get(kind, 0)}; a ledger may not over-commit"
                )

    # -- reads ---------------------------------------------------------------

    def allocated(self, project_id: str) -> int:
        """The units committed to one project this turn (0 when it has none)."""
        for allocation in self.commitments:
            if allocation.project_id == project_id:
                return allocation.units
        return 0

    def committed(self, resource_kind: str) -> int:
        """Every unit of one kind committed to any project."""
        return sum(a.units for a in self.commitments if a.resource_kind == resource_kind)

    def free(self, resource_kind: str) -> int:
        """The units of one kind not yet committed. Zero or negative means a shortage."""
        return self.units.get(resource_kind, 0) - self.committed(resource_kind)

    # -- writes --------------------------------------------------------------

    def allocate(self, project_id: str, resource_kind: str, units: int) -> Allocation:
        """Commit units to a project, replacing that project's previous commitment.

        Refuses an over-commitment rather than silently trimming it: a faction that promises four
        units it does not have has a plan the ledger cannot keep, and saying so is the point.
        """
        replacement = Allocation(project_id, resource_kind, units)
        kept = [a for a in self.commitments if a.project_id != project_id]
        trial = FactionCapacity(self.faction_id, dict(self.units), kept + [replacement])
        self.commitments = trial.commitments
        return replacement

    def release(self, project_id: str) -> int:
        """Drop a project's commitment and return the units released."""
        released = self.allocated(project_id)
        self.commitments = [a for a in self.commitments if a.project_id != project_id]
        return released

    def to_dict(self) -> dict[str, Any]:
        return {
            "faction_id": self.faction_id,
            "units": {k: v for k, v in sorted(self.units.items())},
            "commitments": [a.to_dict() for a in sorted(self.commitments, key=lambda a: a.project_id)],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> FactionCapacity:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a capacity record must be a mapping, got {type(data).__name__}")
        return cls(
            faction_id=str(data.get("faction_id") or ""),
            units={str(k): int(v) for k, v in dict(data.get("units") or {}).items()},
            commitments=[
                Allocation.from_dict(item)
                for item in (data.get("commitments") or [])
                if isinstance(item, Mapping)
            ],
        )


@dataclass
class StrategicProject:
    """One faction operation on the shared engine: a lead, a check, a throughput and a clock.

    Research is the first instance of this record, not a special case of it. :class:`ResearchProject`
    in ``strategy_game.research`` narrows it to the lead scientist's SCIENCE check; a construction,
    organising, diplomatic, covert or security operation is the same record with another
    ``lead_skill`` and another ``resource_kind``, which is exactly the "at least one non-research
    task with another lead skill" issue #506 requires.
    """

    project_id: str
    faction_id: str
    title: str
    #: Free-text kind, drawn from the author's or the issue's own list (research kinds live in
    #: ``research.RESEARCH_PROJECT_KINDS``). Deliberately not an enum: issue #506 says branches and
    #: kinds are "data-defined/modded", so this is data.
    kind: str
    #: The lead agent: a character id with a sheet on the campaign.
    lead_id: str
    #: A **strategic** (faction-agent) skill id, resolved against the roster the caller passes in.
    lead_skill: str
    #: The check's target. The caller/GM sets it, exactly as the Fate rulebook requires.
    lead_difficulty: int
    clock: ProjectClock
    #: Which of the faction's resource kinds this project draws on.
    resource_kind: str
    #: The stage this project's **completion** produces, and only that one.
    stage: ProjectStage
    requires: Prerequisites = field(default_factory=Prerequisites)
    #: The capability node this project produces on completion. Empty for an operation that
    #: produces no capability (a construction, an organising task, a diplomatic campaign).
    node_id: str = ""
    #: "Particular expertise": the ``competence`` capability the lead must carry. Handed to the
    #: kernel's capability gate, so it is refused *before any dice* (issue #482).
    required_capability: str | None = None
    #: The domain TAGs the work names, e.g. Forensics, Parapsychology, Engineering (issue #506).
    #: Read from the lead's competences and **reported** as matched/missing in the result; a tag
    #: that moved a roll or the throughput would be an unapproved mechanic, so none does.
    domain_tags: tuple[str, ...] = ()
    #: Ideological prohibitions the author's data names for this work, as belief labels. Reported in
    #: the result with the faction's own matching beliefs; not enforced here (row D28).
    prohibited_by: tuple[str, ...] = ()
    #: Ids this project's completion adds to the faction's resource inventory. The generic effect of
    #: any operation: a research programme that cannot hand the faction a lab has done nothing.
    grants_resource_ids: tuple[str, ...] = ()
    paused: bool = False
    pause_reasons: list[str] = field(default_factory=list)
    #: The turn the clock filled. ``None`` until it does; the guard that makes completion idempotent.
    completed_on_turn: int | None = None
    #: Every turn this project ran, oldest first, as :meth:`ProjectResult.to_dict` payloads. A
    #: completed project's log is closed: no later call may append to it.
    history: list[dict[str, Any]] = field(default_factory=list)
    #: Other authored fields, retained verbatim so unknown material is never lost.
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name, value in (
            ("project_id", self.project_id),
            ("faction_id", self.faction_id),
            ("title", self.title),
            ("kind", self.kind),
            ("lead_skill", self.lead_skill),
            ("resource_kind", self.resource_kind),
        ):
            if not str(value).strip():
                raise ProjectError(f"a project needs a non-empty {name}")
        if not isinstance(self.lead_difficulty, int) or self.lead_difficulty < 0:
            raise ProjectError("a check target must be a nonnegative integer")
        if not isinstance(self.clock, ProjectClock):
            raise ProjectError("a project's clock must be a ProjectClock")
        if not isinstance(self.stage, ProjectStage):
            try:
                self.stage = ProjectStage(str(self.stage))
            except ValueError as exc:
                raise ProjectError(
                    f"stage {self.stage!r} is not one of the project stages "
                    f"({', '.join(s.value for s in ProjectStage)})"
                ) from exc
        if not isinstance(self.requires, Prerequisites):
            self.requires = Prerequisites.from_dict(self.requires)
        for name, values in (("domain_tags", self.domain_tags),
                             ("prohibited_by", self.prohibited_by),
                             ("grants_resource_ids", self.grants_resource_ids)):
            if len(set(values)) != len(values):
                raise ProjectError(f"{name} repeats an entry: {sorted(values)}")
        if self.paused and not self.pause_reasons:
            raise ProjectError(
                f"project {self.project_id!r} is paused; a pause states its reason, so a reader can "
                "tell a stalled programme from a stopped one"
            )
        if self.pause_reasons and not self.paused:
            raise ProjectError(
                f"project {self.project_id!r} carries pause reasons but is not paused; the flag and "
                "the reasons are one fact"
            )

    @property
    def is_complete(self) -> bool:
        return self.clock.is_complete

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = dict(self.detail)
        payload.update(
            {
                "project_id": self.project_id,
                "faction_id": self.faction_id,
                "title": self.title,
                "kind": self.kind,
                "lead_id": self.lead_id,
                "lead_skill": self.lead_skill,
                "lead_difficulty": self.lead_difficulty,
                "clock": self.clock.to_dict(),
                "resource_kind": self.resource_kind,
                "stage": self.stage.value,
                "requires": self.requires.to_dict(),
                "node_id": self.node_id,
                "required_capability": self.required_capability,
                "domain_tags": list(self.domain_tags),
                "prohibited_by": list(self.prohibited_by),
                "grants_resource_ids": list(self.grants_resource_ids),
                "paused": self.paused,
                "pause_reasons": list(self.pause_reasons),
                "completed_on_turn": self.completed_on_turn,
                "history": [dict(entry) for entry in self.history],
            }
        )
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> StrategicProject:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a project record must be a mapping, got {type(data).__name__}")
        known = {
            "project_id", "faction_id", "title", "kind", "lead_id", "lead_skill", "lead_difficulty",
            "clock", "resource_kind", "stage", "requires", "node_id", "required_capability",
            "domain_tags", "prohibited_by", "grants_resource_ids", "paused", "pause_reasons",
            "completed_on_turn", "history",
        }
        return cls(
            project_id=str(data.get("project_id") or ""),
            faction_id=str(data.get("faction_id") or ""),
            title=str(data.get("title") or ""),
            kind=str(data.get("kind") or ""),
            lead_id=str(data.get("lead_id") or ""),
            lead_skill=str(data.get("lead_skill") or ""),
            lead_difficulty=int(data.get("lead_difficulty", 0)),
            clock=ProjectClock.from_dict(data.get("clock") or {}),
            resource_kind=str(data.get("resource_kind") or ""),
            stage=data.get("stage"),  # type: ignore[arg-type]
            requires=Prerequisites.from_dict(data.get("requires")),
            node_id=str(data.get("node_id") or ""),
            required_capability=(
                str(data["required_capability"]) if data.get("required_capability") else None
            ),
            domain_tags=tuple(str(x) for x in (data.get("domain_tags") or [])),
            prohibited_by=tuple(str(x) for x in (data.get("prohibited_by") or [])),
            grants_resource_ids=tuple(str(x) for x in (data.get("grants_resource_ids") or [])),
            paused=bool(data.get("paused", False)),
            pause_reasons=[str(x) for x in (data.get("pause_reasons") or [])],
            completed_on_turn=(
                int(data["completed_on_turn"])
                if data.get("completed_on_turn") is not None
                else None
            ),
            history=[dict(entry) for entry in (data.get("history") or [])],
            detail={key: value for key, value in data.items() if key not in known},
        )


@dataclass(frozen=True)
class ProjectResult:
    """One turn of one project, as plain data: the report the player reads.

    ``outcome`` is the approved Fate ladder (``None`` when the turn rolled no dice at all, because
    the project was complete or paused). ``progress_added`` is the work actually banked — never more
    than the clock had room for — and ``cause`` says which of the engine's branches produced it.
    ``notes`` are the same facts in sentences, because issue #506 requires that a player can see why
    progress did or did not happen.
    """

    project_id: str
    turn: int
    cause: ProgressCause
    lead_id: str
    resource_kind: str
    progress_added: int
    filled: int
    work_required: int
    completed: bool
    #: The committed throughput the faction brought to this turn.
    throughput: int
    #: ``None`` when no check was rolled this turn (complete or paused).
    outcome: Outcome | None = None
    domain_tags_matched: tuple[str, ...] = ()
    domain_tags_missing: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    seed: int | None = None
    schema_version: str = PROJECT_RESULT_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if not str(self.project_id).strip():
            raise ProjectError("a result names its project")
        if not isinstance(self.cause, ProgressCause):
            raise ProjectError(f"cause must be a ProgressCause, got {type(self.cause).__name__}")
        if not isinstance(self.outcome, Outcome) and self.outcome is not None:
            raise ProjectError("a result's outcome is the approved Fate ladder, or None")
        if self.progress_added < 0:
            raise ProjectError("a turn cannot remove progress")
        if self.filled > self.work_required:
            raise ProjectError("a result cannot report a clock filled past its total")
        if self.progress_added and self.cause not in (ProgressCause.ADVANCED, ProgressCause.COMPLETED):
            raise ProjectError(
                f"cause {self.cause.value!r} reports progress; only an advanced or completed turn "
                "may carry work"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "project_id": self.project_id,
            "turn": self.turn,
            "cause": self.cause.value,
            "lead_id": self.lead_id,
            "resource_kind": self.resource_kind,
            "outcome": self.outcome.value if self.outcome is not None else None,
            "throughput": self.throughput,
            "progress_added": self.progress_added,
            "filled": self.filled,
            "work_required": self.work_required,
            "completed": self.completed,
            "domain_tags_matched": list(self.domain_tags_matched),
            "domain_tags_missing": list(self.domain_tags_missing),
            "notes": list(self.notes),
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ProjectResult:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a result record must be a mapping, got {type(data).__name__}")
        if data.get("schema_version") != PROJECT_RESULT_SCHEMA_VERSION:
            raise ProjectError(
                f"unsupported project-result schema_version {data.get('schema_version')!r}; "
                f"expected {PROJECT_RESULT_SCHEMA_VERSION!r}"
            )
        try:
            cause = ProgressCause(str(data["cause"]))
        except (KeyError, ValueError) as exc:
            raise ProjectError(f"cause {data.get('cause')!r} is not one of the engine's branches") from exc
        raw_outcome = data.get("outcome")
        try:
            outcome = Outcome(str(raw_outcome)) if raw_outcome is not None else None
        except ValueError as exc:
            raise ProjectError(
                f"outcome {raw_outcome!r} is not one of the approved Fate outcomes"
            ) from exc
        return cls(
            project_id=str(data.get("project_id") or ""),
            turn=int(data.get("turn", 0)),
            cause=cause,
            lead_id=str(data.get("lead_id") or ""),
            resource_kind=str(data.get("resource_kind") or ""),
            progress_added=int(data.get("progress_added", 0)),
            filled=int(data.get("filled", 0)),
            work_required=int(data.get("work_required", 0)),
            completed=bool(data.get("completed", False)),
            throughput=int(data.get("throughput", 0)),
            outcome=outcome,
            domain_tags_matched=tuple(str(x) for x in (data.get("domain_tags_matched") or [])),
            domain_tags_missing=tuple(str(x) for x in (data.get("domain_tags_missing") or [])),
            notes=tuple(str(x) for x in (data.get("notes") or [])),
            seed=int(data["seed"]) if data.get("seed") is not None else None,
        )


@dataclass(frozen=True)
class ProjectCompletion:
    """The one write a completed project makes to the campaign, and whether it happened now.

    ``applied`` is ``False`` on a replay: completion is **idempotent**, so re-applying a finished
    project grants nothing again and appends no second audit note.
    """

    project_id: str
    turn: int
    applied: bool
    resource_ids: tuple[str, ...] = ()
    note_index: int = -1

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "turn": self.turn,
            "applied": self.applied,
            "resource_ids": list(self.resource_ids),
            "note_index": self.note_index,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ProjectCompletion:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a completion record must be a mapping, got {type(data).__name__}")
        return cls(
            project_id=str(data.get("project_id") or ""),
            turn=int(data.get("turn", 0)),
            applied=bool(data.get("applied", False)),
            resource_ids=tuple(str(x) for x in (data.get("resource_ids") or [])),
            note_index=int(data.get("note_index", -1)),
        )


def project_from_dict(data: Mapping[str, Any]) -> StrategicProject:
    """Build a project from :meth:`StrategicProject.to_dict` output (the save/load seam)."""
    return StrategicProject.from_dict(data)


def capacity_from_dict(data: Mapping[str, Any]) -> FactionCapacity:
    """Build a capacity ledger from :meth:`FactionCapacity.to_dict` output."""
    return FactionCapacity.from_dict(data)


def unsatisfied_prerequisites(campaign: Campaign, project: StrategicProject) -> tuple[str, ...]:
    """The prerequisites of ``project`` the campaign does **not** satisfy, in a stable order.

    Reported rather than raised: an unsatisfied prerequisite can be a project that has not started
    (a defect) or one whose specimen was taken away mid-programme (an interruption), and the two are
    different situations the caller must be able to tell apart.
    """
    faction = campaign.faction(project.faction_id)
    missing = [rid for rid in project.requires.resource_ids if rid not in faction.resources]
    missing += [nid for nid in project.requires.node_ids if nid not in campaign.capabilities]
    return tuple(sorted(missing))


def _project(campaign: Campaign, project_id: str) -> StrategicProject:
    project = campaign.projects.get(project_id)
    if project is None:
        raise ProjectError(
            f"no project {project_id!r} on this campaign; declared: "
            f"{sorted(campaign.projects) or 'none'}"
        )
    return project


def _result(
    project: StrategicProject,
    *,
    turn: int,
    cause: ProgressCause,
    progress_added: int = 0,
    throughput: int = 0,
    outcome: Outcome | None = None,
    matched: tuple[str, ...] = (),
    missing_tags: tuple[str, ...] = (),
    notes: tuple[str, ...] = (),
    seed: int | None = None,
    record: bool = True,
) -> ProjectResult:
    """Build the turn's report, and append it to the project's log unless the project is closed."""
    result = ProjectResult(
        project_id=project.project_id,
        turn=turn,
        cause=cause,
        lead_id=project.lead_id,
        resource_kind=project.resource_kind,
        progress_added=progress_added,
        filled=project.clock.filled,
        work_required=project.clock.work_required,
        completed=project.clock.is_complete,
        throughput=throughput,
        outcome=outcome,
        domain_tags_matched=matched,
        domain_tags_missing=missing_tags,
        notes=notes,
        seed=seed,
    )
    if record:
        project.history.append(result.to_dict())
    return result


def advance_project(
    campaign: Campaign,
    project_id: str,
    *,
    rng: Random,
    turn: int,
    roster: Mapping[str, object] | None = None,
    scene: Scene | None = None,
    invoked_aspect: str | None = None,
    free: bool = False,
    reroll: bool = False,
) -> ProjectResult:
    """Advance one project by one faction turn: check, throughput, clock. The engine of #506.

    Order of operations, and why each step is where it is:

    1. **A completed project is closed.** It reports :attr:`ProgressCause.ALREADY_COMPLETE`, adds
       nothing and appends no log entry, so re-advancing a finished programme cannot repeat work or
       re-roll dice. (Tested by asserting the RNG's state is untouched.)
    2. **A paused project stays paused** and says why.
    3. **Prerequisites are read before dice.** A project that has never started and does not satisfy
       them is refused loudly (:class:`ProjectError`): an unfunded wish is not a programme. A project
       *already in progress* whose prerequisite was lost — the lab raided, the specimen reclaimed — is
       **paused** and reports the missing ids, which is issue #506's "project interruption".
    4. **The lead's check** goes through :func:`strategy_game.rpg.skills.check` in
       :attr:`~strategy_game.rpg.skills.ActionContext.FACTION_AGENT`, with the caller's proposed
       strategic roster, so a cross-layer skill name, an unknown name, a missing roster and an
       ungranted capability are all refused by the one kernel before any dice.
    5. **Success is gated, throughput is not.** Failure and a Fate *tie* add zero segments (a tie is
       "succeed at a minor cost" in Fate Core, and what that cost is is the author's call, so no
       segment is granted and the result says so). Success adds the faction's committed throughput,
       plus :data:`TUNING_STYLE_BONUS_SEGMENTS` on a success *with style*.
    6. **No capacity, no work.** A successful check with nothing committed advances nothing and
       reports :attr:`ProgressCause.NO_CAPACITY`: the lead cannot substitute for the institution.
    """
    project = _project(campaign, project_id)
    campaign.faction(project.faction_id)
    lead = campaign.sheets.get(project.lead_id)
    if lead is None:
        raise ProjectError(
            f"project {project.project_id!r}: lead {project.lead_id!r} has no sheet on the campaign; "
            "inventing one would be inventing a character"
        )
    ledger = campaign.capacities.get(project.faction_id)
    if ledger is None:
        raise ProjectError(
            f"faction {project.faction_id!r} has no capacity ledger on this campaign; a project "
            "cannot draw on capacity the campaign does not track"
        )

    matched = tuple(sorted(set(project.domain_tags) & set(capabilities_of(lead))))
    missing_tags = tuple(sorted(set(project.domain_tags) - set(matched)))

    if project.clock.is_complete:
        note = (
            f"{project.project_id} is already complete at "
            f"{project.clock.filled}/{project.clock.work_required} segments; a finished programme is "
            "closed, so nothing is repeated and no dice are rolled"
        )
        return _result(
            project, turn=turn, cause=ProgressCause.ALREADY_COMPLETE, record=False,
            matched=matched, missing_tags=missing_tags, notes=(note,),
        )

    if project.paused:
        note = f"{project.project_id} is paused: {'; '.join(project.pause_reasons)}"
        return _result(
            project, turn=turn, cause=ProgressCause.PAUSED,
            matched=matched, missing_tags=missing_tags, notes=(note,),
        )

    unsatisfied = unsatisfied_prerequisites(campaign, project)
    if unsatisfied:
        reason = (
            f"missing prerequisites: {', '.join(unsatisfied)}"
        )
        if project.clock.filled == 0:
            raise ProjectError(
                f"project {project.project_id!r} cannot start: {reason}. Issue #506 requires access "
                "to the specimen, artefact, archive, data or facility before the work exists at all; "
                "a resolved mission grants it through "
                "strategy_game.campaign.missions.apply_mission_outcome."
            )
        project.paused = True
        project.pause_reasons = [reason]
        note = (
            f"{project.project_id} is interrupted at "
            f"{project.clock.filled}/{project.clock.work_required} segments: {reason}. Completed "
            "segments are preserved; the project resumes when the prerequisite is back."
        )
        return _result(
            project, turn=turn, cause=ProgressCause.PAUSED,
            matched=matched, missing_tags=missing_tags, notes=(note,),
        )

    # -- the one check. Anything the layer refuses is refused before any dice. --------------
    check_result = check(
        lead,
        ActionContext.FACTION_AGENT,
        Action.OVERCOME,
        project.lead_skill,
        project.lead_difficulty,
        rng=rng,
        strategic_roster=roster,
        scene=scene,
        invoked_aspect=invoked_aspect,
        free=free,
        reroll=reroll,
        required_capability=project.required_capability,
    )
    resolution = check_result.resolution
    seed = _rng_seed(rng)
    throughput = ledger.allocated(project.project_id)

    if resolution.outcome is Outcome.FAILURE:
        note = (
            f"the {project.lead_skill} check failed ({resolution.total} against "
            f"{resolution.difficulty}): no progress this round, and every completed segment is "
            f"preserved at {project.clock.filled}/{project.clock.work_required}"
        )
        return _result(
            project, turn=turn, cause=ProgressCause.CHECK_FAILED, outcome=resolution.outcome,
            throughput=throughput, matched=matched, missing_tags=missing_tags, seed=seed,
            notes=(note,),
        )

    if resolution.outcome is Outcome.TIE:
        note = (
            f"the {project.lead_skill} check tied ({resolution.total} against "
            f"{resolution.difficulty}): a tie is 'succeed at a minor cost' in Fate Core, and no cost "
            "rule is approved, so the clock takes no segments and the cost stays a scene decision"
        )
        return _result(
            project, turn=turn, cause=ProgressCause.TIE, outcome=resolution.outcome,
            throughput=throughput, matched=matched, missing_tags=missing_tags, seed=seed,
            notes=(note,),
        )

    if throughput <= 0:
        note = (
            f"the check succeeded but the faction committed no {project.resource_kind} to "
            f"{project.project_id} this turn: individual competence keeps a programme on track, "
            "institutional resources decide its scale"
        )
        return _result(
            project, turn=turn, cause=ProgressCause.NO_CAPACITY, outcome=resolution.outcome,
            matched=matched, missing_tags=missing_tags, seed=seed, notes=(note,),
        )

    style_bonus = (
        TUNING_STYLE_BONUS_SEGMENTS
        if resolution.outcome is Outcome.SUCCESS_WITH_STYLE
        else 0
    )
    added = project.clock.add(throughput + style_bonus)
    style_note = f" (including the tuning style bonus of {style_bonus})" if style_bonus else ""
    completed = project.clock.is_complete
    cause = ProgressCause.COMPLETED if completed else ProgressCause.ADVANCED
    if completed and project.completed_on_turn is None:
        project.completed_on_turn = turn
    notes = [
        (
            f"the {project.lead_skill} check succeeded against {resolution.difficulty}; the faction "
            f"committed {throughput} {project.resource_kind}{style_note}, so the clock advanced by "
            f"{added} to {project.clock.filled}/{project.clock.work_required}"
        )
    ]
    if completed:
        notes.append(
            f"the clock is full: {project.project_id} has reached "
            f"{STAGE_MEANINGS[project.stage]!r} and nothing further is produced by repeating it"
        )
    return _result(
        project, turn=turn, cause=cause, outcome=resolution.outcome,
        progress_added=added, throughput=throughput,
        matched=matched, missing_tags=missing_tags, seed=seed, notes=tuple(notes),
    )


def pause_project(campaign: Campaign, project_id: str, reason: str) -> StrategicProject:
    """Stop a project until :func:`resume_project`. The reason is required and is shown to the player."""
    project = _project(campaign, project_id)
    text = str(reason).strip()
    if not text:
        raise ProjectError("a pause states its reason; a stoppage with no reason is not legible")
    project.paused = True
    project.pause_reasons = [text]
    return project


def resume_project(campaign: Campaign, project_id: str) -> StrategicProject:
    """Clear a pause. Unsatisfied prerequisites are re-read on the next advance, not here."""
    project = _project(campaign, project_id)
    project.paused = False
    project.pause_reasons = []
    return project


def reassign_project(campaign: Campaign, project_id: str, lead_id: str) -> StrategicProject:
    """Hand a project to another lead. Refuses a lead with no sheet, and keeps the clock."""
    project = _project(campaign, project_id)
    if lead_id not in campaign.sheets:
        raise ProjectError(
            f"project {project.project_id!r}: {lead_id!r} has no sheet on the campaign; a lead is a "
            "character, not a name"
        )
    if lead_id != project.lead_id:
        project.detail.setdefault("reassigned_from", []).append(project.lead_id)
        project.lead_id = lead_id
    return project


def complete_project(campaign: Campaign, project_id: str, *, turn: int) -> ProjectCompletion:
    """Resolve a filled clock: grant the project's resources and write one audit note.

    This is the **one** writer for a project's completion, and it is **idempotent**: the second call
    for the same project applies nothing and appends no second note, which is what makes a replayable
    campaign save safe. It refuses an unfilled clock, because reaching the difficulty-defined total
    work is the gate — not the caller's opinion that the programme is finished.
    """
    project = _project(campaign, project_id)
    if not project.clock.is_complete:
        raise ProjectError(
            f"project {project.project_id!r} is at {project.clock.filled}/"
            f"{project.clock.work_required} segments; a completion resolves the difficulty-defined "
            "total work, not an intention"
        )
    if project.completed_on_turn is None:
        project.completed_on_turn = turn
    faction = campaign.faction(project.faction_id)
    granted = tuple(rid for rid in project.grants_resource_ids if rid not in faction.resources)
    if project.detail.get("completion_note_index") is not None and not granted:
        return ProjectCompletion(
            project_id=project.project_id,
            turn=turn,
            applied=False,
            resource_ids=(),
            note_index=int(project.detail["completion_note_index"]),
        )
    for rid in granted:
        faction.resources.append(rid)
    index = len(campaign.campaign_notes)
    campaign.campaign_notes.append(
        {
            "kind": "project_completion",
            "schema_version": PROJECT_RESULT_SCHEMA_VERSION,
            "project_id": project.project_id,
            "faction_id": project.faction_id,
            "turn": turn,
            "stage": project.stage.value,
            "node_id": project.node_id,
            "resource_ids": list(granted),
            "provenance": {
                "kind": ProvenanceKind.SIMULATED.value,
                "source": "strategy_game.projects.complete_project",
                "note": "applied through the one project-completion interface (issue #506 Phase 1)",
            },
        }
    )
    project.detail["completion_note_index"] = index
    project.detail.setdefault("completion_turn", turn)
    return ProjectCompletion(
        project_id=project.project_id, turn=turn, applied=True,
        resource_ids=granted, note_index=index,
    )


def _rng_seed(rng: Random) -> int | None:
    """The seed a resolution can be replayed from, when the caller used a seeded generator.

    ``Random`` exposes its state rather than its seed, so this reports the seed only when the
    generator still carries one (``random.Random(seed)`` sets ``_seed``); otherwise it is ``None``,
    which is honest — an unseeded roll has no replay seed.
    """
    seed = getattr(rng, "_seed", None)
    return int(seed) if isinstance(seed, int) else None
