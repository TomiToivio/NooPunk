"""The mission-data schema: what is true on a tactical map, and nothing about how it looks (#515).

Issue #515's first milestone is *"choose renderer, grid/tile format and mission-data schema"*. The
renderer is the author's decision (queued as row D29); the **schema** is this module, and it is
deliberately renderer-independent so that decision cannot retroactively invalidate the prototype.

What a mission document says
----------------------------

A mission is one JSON object (:data:`MISSION_FORMAT`, :data:`MISSION_SCHEMA_VERSION`) carrying:

* ``grid`` — the map as ASCII rows of floor ``.`` / wall ``#`` / door ``+`` cells, plus any doors
  declared shut (see :mod:`strategy_game.tactical.grid`);
* ``deploy_cells`` — exactly four cells, bound to the faction's four agent seats **in seat order**;
* ``interactions`` — the mission's dialogue, clue and confrontation hooks: a cell, an optional Fate
  check (an approved ``rpg.fate.Action`` over one of the six individual skills), prerequisites, and
  the ids the interaction grants on success;
* ``objectives`` — the mission's goals, each completed by an interaction that names it.

What a mission document may not say
-----------------------------------

Nothing about presentation. There is **no sprite id, no tile id, no pixel coordinate, no colour, no
layer, no camera, no draw order and no animation** — and the loader refuses unknown keys rather than
retaining them, so a renderer cannot start using the mission file as its scene file. A renderer maps
``.``/``#``/``+`` to its own tiles and reads :meth:`MissionSession.report` for state; it contributes
no authority in return.

Nor does it say anything about **how the world works**: no damage, no movement cost, no line of
sight, no cover, no stealth, no initiative. The only mechanic a mission can name is a Fate check,
because that is the one resolution the repo has approved (issue #482), and the check is resolved by
the existing kernel (:mod:`strategy_game.rpg.skills`), never here.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from ..rpg.fate import Action
from ..rpg.roster import AGENT_SEAT_COUNT
from ..rpg.skills import ActionContext, SkillLayerError, validate_skill
from .grid import Cell, Grid, GridError

__all__ = [
    "MISSION_DATA_PATH",
    "MISSION_FORMAT",
    "MISSION_SCHEMA_VERSION",
    "Interaction",
    "InteractionKind",
    "MissionError",
    "MissionSpec",
    "Objective",
    "load_mission",
    "mission_from_dict",
]

#: Document type marker. A file that does not declare it is not a mission.
MISSION_FORMAT = "noopunk.tactical.mission"

#: Shape marker. Bump on an incompatible change; a loader refuses a foreign marker instead of
#: guessing, exactly as ``campaign.state.SCHEMA_VERSION`` does for saves.
MISSION_SCHEMA_VERSION = "tactical-mission-1"

#: The packaged example mission: a **non-canonical fixture** used by the spike's tests and demo.
MISSION_DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "tactical" / "spike_mission.json"

#: Top-level keys a mission document may carry. Anything else is a defect, not an extension point:
#: this is what keeps presentation fields out of the mission file.
_MISSION_KEYS = frozenset(
    {"format", "schema_version", "status", "mission_id", "case_id", "title", "note",
     "grid", "deploy_cells", "interactions", "objectives"}
)

#: Keys one interaction may carry.
_INTERACTION_KEYS = frozenset(
    {"id", "kind", "at", "label", "text", "action", "skill", "difficulty", "requires",
     "evidence", "intel", "objectives", "optional", "consequence"}
)

#: Keys one objective may carry.
_OBJECTIVE_KEYS = frozenset({"id", "label", "required"})


class MissionError(ValueError):
    """A mission document or operation the schema does not allow."""


class InteractionKind(str, Enum):
    """The three interaction kinds #515's adventure half needs, and no more.

    ``DIALOGUE`` costs no check — talking to a willing witness is not uncertain. ``CLUE`` and
    ``CONFRONTATION`` both resolve one Fate check through the approved kernel; the difference is
    social framing, and that a confrontation is the mission's **optional** hook: failing it wounds
    the character instead of merely leaving the clue unread.
    """

    DIALOGUE = "dialogue"
    CLUE = "clue"
    CONFRONTATION = "confrontation"


def _id_list(value: object, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, (list, tuple)):
        raise MissionError(f"{where} must be a list of ids")
    seen: list[str] = []
    for item in value:
        text = str(item).strip()
        if not text:
            raise MissionError(f"{where} carries an empty id")
        if text in seen:
            raise MissionError(f"{where}: duplicate id {text!r}")
        seen.append(text)
    return tuple(seen)


@dataclass(frozen=True)
class Objective:
    """One mission goal. ``label`` is what reaches the faction's ``objectives`` book on success.

    There is no progress counter and no partial credit: #515's adventure half is *"did the squad read
    the ledger"*, and a progress score would be a mechanic the author has not approved.
    """

    id: str
    label: str
    required: bool = True

    def __post_init__(self) -> None:
        if not str(self.id).strip():
            raise MissionError("an objective needs an id")
        if not str(self.label).strip():
            raise MissionError(f"objective {self.id!r} needs a label (it is written to faction state)")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "required": self.required}


@dataclass(frozen=True)
class Interaction:
    """One thing the squad can do at a cell: talk, read, or confront.

    A check-bearing interaction names the **approved** Fate action and one of the six **individual**
    skills, because a character standing on a map acts as a person, not as a faction agent (issue
    #482's two layers). The skill name is validated at load time, so a mission file cannot smuggle in
    a strategic skill, an invented attribute or an unknown action.
    """

    id: str
    kind: InteractionKind
    at: Cell
    label: str = ""
    #: Fixture prose. No rule reads it; it exists so a renderer has something to show.
    text: str = ""
    action: Action | None = None
    skill: str | None = None
    difficulty: int | None = None
    requires: tuple[str, ...] = ()
    evidence: tuple[str, ...] = ()
    intel: tuple[str, ...] = ()
    objectives: tuple[str, ...] = ()
    #: Confrontation only: the mission's optional hook cannot gate a required objective.
    optional: bool = False
    #: Confrontation only: the mild consequence a failed check writes onto the sheet.
    consequence: str = ""

    @property
    def has_check(self) -> bool:
        return self.action is not None

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "kind": self.kind.value,
            "at": self.at.to_pair(),
            "label": self.label,
        }
        if self.text:
            payload["text"] = self.text
        if self.action is not None:
            payload["action"] = self.action.value
        if self.skill is not None:
            payload["skill"] = self.skill
        if self.difficulty is not None:
            payload["difficulty"] = self.difficulty
        for name, values in (
            ("requires", self.requires),
            ("evidence", self.evidence),
            ("intel", self.intel),
            ("objectives", self.objectives),
        ):
            if values:
                payload[name] = list(values)
        if self.optional:
            payload["optional"] = True
        if self.consequence:
            payload["consequence"] = self.consequence
        return payload

    @classmethod
    def from_dict(cls, payload: object) -> Interaction:
        if not isinstance(payload, Mapping):
            raise MissionError(f"an interaction must be an object, got {type(payload).__name__}")
        unknown = sorted(set(payload) - _INTERACTION_KEYS)
        if unknown:
            raise MissionError(
                f"interaction {payload.get('id')!r} carries field(s) {unknown} the schema does not "
                "define; presentation fields do not belong in mission data"
            )
        try:
            kind = InteractionKind(str(payload.get("kind", "")))
        except ValueError as exc:
            raise MissionError(
                f"interaction {payload.get('id')!r} has kind {payload.get('kind')!r}; "
                f"expected one of {[k.value for k in InteractionKind]}"
            ) from exc
        at_raw = payload.get("at")
        try:
            at = Cell.from_pair(at_raw, what=f"interaction {payload.get('id')!r} cell")
        except GridError as exc:
            raise MissionError(str(exc)) from exc
        action: Action | None = None
        if payload.get("action") is not None:
            try:
                action = Action(str(payload["action"]))
            except ValueError as exc:
                raise MissionError(
                    f"interaction {payload.get('id')!r} names action {payload.get('action')!r}; "
                    f"expected one of {[a.value for a in Action]}"
                ) from exc
        difficulty = payload.get("difficulty")
        if difficulty is not None and (
            not isinstance(difficulty, int) or isinstance(difficulty, bool) or difficulty < 0
        ):
            raise MissionError(
                f"interaction {payload.get('id')!r} has difficulty {difficulty!r}; "
                "a Fate difficulty is a non-negative integer"
            )
        optional = bool(payload.get("optional", False))
        if optional and kind is not InteractionKind.CONFRONTATION:
            raise MissionError(
                f"interaction {payload.get('id')!r} is optional; only a confrontation is the "
                "mission's optional hook (#515), because an optional clue could silently leave a "
                "required objective uncompletable"
            )
        return cls(
            id=str(payload.get("id", "")).strip(),
            kind=kind,
            at=at,
            label=str(payload.get("label", "")),
            text=str(payload.get("text", "")),
            action=action,
            skill=str(payload["skill"]).strip() if payload.get("skill") is not None else None,
            difficulty=difficulty if isinstance(difficulty, int) else None,
            requires=_id_list(payload.get("requires"), f"interaction {payload.get('id')!r} requires"),
            evidence=_id_list(payload.get("evidence"), f"interaction {payload.get('id')!r} evidence"),
            intel=_id_list(payload.get("intel"), f"interaction {payload.get('id')!r} intel"),
            objectives=_id_list(
                payload.get("objectives"), f"interaction {payload.get('id')!r} objectives"
            ),
            optional=optional,
            consequence=str(payload.get("consequence", "")),
        )


@dataclass(frozen=True)
class MissionSpec:
    """One mission, as declared data: the map, the squad's deployment, its hooks and its goals."""

    mission_id: str
    case_id: str
    title: str
    grid: Grid
    deploy_cells: tuple[Cell, ...]
    interactions: tuple[Interaction, ...] = ()
    objectives: tuple[Objective, ...] = ()
    #: ``SPIKE_FIXTURE`` for the packaged example. Author scenario data would carry its own marker;
    #: this field exists so a fixture is never mistaken for canon.
    status: str = "SPIKE_FIXTURE"
    note: str = ""

    # -- lookups ---------------------------------------------------------------

    def interaction(self, interaction_id: str) -> Interaction:
        for item in self.interactions:
            if item.id == interaction_id:
                return item
        raise MissionError(
            f"no interaction {interaction_id!r} in mission {self.mission_id!r}; "
            f"interactions are {[i.id for i in self.interactions]}"
        )

    def objective(self, objective_id: str) -> Objective:
        for item in self.objectives:
            if item.id == objective_id:
                return item
        raise MissionError(f"no objective {objective_id!r} in mission {self.mission_id!r}")

    @property
    def required_objectives(self) -> tuple[Objective, ...]:
        return tuple(o for o in self.objectives if o.required)

    # -- validation ------------------------------------------------------------

    def problems(self) -> tuple[str, ...]:
        """Schema defects, reported rather than raised, in a stable order.

        This checks **shape and reachability only**: ids resolve, a check-bearing hook names an
        approved action and an individual skill, prerequisites are acyclic, objectives are
        completable, and every hook is reachable from every deployment cell. It checks no balance,
        difficulty or reward, because none is approved.
        """
        issues: list[str] = []
        if not self.mission_id.strip():
            issues.append("a mission needs a non-empty mission_id")
        if not self.case_id.strip():
            issues.append("a mission needs a non-empty case_id")
        if not self.status.strip():
            issues.append("a mission declares its status (SPIKE_FIXTURE for the packaged example)")
        if len(self.deploy_cells) != AGENT_SEAT_COUNT:
            issues.append(
                f"a mission deploys exactly {AGENT_SEAT_COUNT} agents (#461/#482); "
                f"{len(self.deploy_cells)} deployment cells declared"
            )
        if len(set(self.deploy_cells)) != len(self.deploy_cells):
            issues.append("two agents are deployed onto the same cell")
        for cell in self.deploy_cells:
            refusal = self.grid.refusal(cell)
            if refusal:
                issues.append(f"deployment cell cannot be stood on: {refusal}")
        if not self.objectives:
            issues.append("a mission needs at least one objective")
        if not self.required_objectives:
            issues.append("a mission needs at least one required objective")

        objective_ids = {o.id for o in self.objectives}
        if len(objective_ids) != len(self.objectives):
            issues.append("two objectives share an id")
        interaction_ids = {i.id for i in self.interactions}
        if len(interaction_ids) != len(self.interactions):
            issues.append("two interactions share an id")

        for item in self.interactions:
            where = f"interaction {item.id!r}"
            refusal = self.grid.refusal(item.at)
            if refusal:
                issues.append(f"{where}: its cell cannot be stood on: {refusal}")
                continue
            for deploy in self.deploy_cells:
                path = self.grid.path(deploy, item.at)
                if not path.ok:
                    issues.append(
                        f"{where} at {item.at} is unreachable from deployment cell {deploy}: "
                        f"{path.reason}"
                    )
                    break
            if item.kind is InteractionKind.DIALOGUE:
                if item.has_check or item.skill or item.difficulty is not None:
                    issues.append(
                        f"{where} is a dialogue: talking carries no Fate check, so it may not declare "
                        "an action, a skill or a difficulty"
                    )
                if item.consequence:
                    issues.append(f"{where} is a dialogue: only a confrontation can wound")
            else:
                if not item.has_check or item.skill is None or item.difficulty is None:
                    issues.append(
                        f"{where} is a {item.kind.value}: it needs an action, a skill and a "
                        "difficulty, because its outcome is uncertain"
                    )
                else:
                    try:
                        validate_skill(ActionContext.INDIVIDUAL, item.skill)
                    except SkillLayerError as exc:
                        issues.append(f"{where}: {exc}")
                if item.consequence and item.kind is not InteractionKind.CONFRONTATION:
                    issues.append(
                        f"{where}: only a confrontation declares a consequence; a failed clue "
                        "leaves the clue unread"
                    )
            for required in item.requires:
                if required == item.id:
                    issues.append(f"{where} requires itself")
                elif required not in interaction_ids:
                    issues.append(f"{where} requires unknown interaction {required!r}")
            for objective_id in item.objectives:
                if objective_id not in objective_ids:
                    issues.append(f"{where} completes unknown objective {objective_id!r}")

        completers = {oid for item in self.interactions for oid in item.objectives}
        for objective in self.objectives:
            if objective.id not in completers:
                issues.append(
                    f"objective {objective.id!r} is completed by no interaction; the squad could "
                    "never finish the mission"
                )
        for objective in self.required_objectives:
            if not any(
                objective.id in item.objectives and not item.optional for item in self.interactions
            ):
                issues.append(
                    f"required objective {objective.id!r} is only completed by an optional hook"
                )

        issues.extend(self._prerequisite_cycles())
        return tuple(issues)

    def _prerequisite_cycles(self) -> list[str]:
        """Prerequisites must form a DAG: a cycle is a mission no squad can open."""
        graph = {item.id: tuple(r for r in item.requires if r in {i.id for i in self.interactions})
                 for item in self.interactions}
        state: dict[str, int] = {}

        def visit(node: str, trail: tuple[str, ...]) -> list[str]:
            if state.get(node) == 2:
                return []
            if state.get(node) == 1:
                return [f"prerequisite cycle: {' -> '.join((*trail, node))}"]
            state[node] = 1
            for required in graph.get(node, ()):
                found = visit(required, (*trail, node))
                if found:
                    return found
            state[node] = 2
            return []

        for node in graph:
            found = visit(node, ())
            if found:
                return found
        return []

    # -- interchange -----------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "format": MISSION_FORMAT,
            "schema_version": MISSION_SCHEMA_VERSION,
            "status": self.status,
            "mission_id": self.mission_id,
            "case_id": self.case_id,
            "title": self.title,
            "grid": self.grid.to_dict(),
            "deploy_cells": [cell.to_pair() for cell in self.deploy_cells],
            "interactions": [item.to_dict() for item in self.interactions],
            "objectives": [objective.to_dict() for objective in self.objectives],
        }
        if self.note:
            payload["note"] = self.note
        return payload

    @classmethod
    def from_dict(cls, payload: object) -> MissionSpec:
        if not isinstance(payload, Mapping):
            raise MissionError(f"a mission must be an object, got {type(payload).__name__}")
        unknown = sorted(set(payload) - _MISSION_KEYS)
        if unknown:
            raise MissionError(
                f"mission document carries field(s) {unknown} the schema does not define; "
                "presentation fields (sprite, tile id, pixel size, layer, camera) do not belong in "
                "mission data"
            )
        if payload.get("format") != MISSION_FORMAT:
            raise MissionError(
                f"mission declares format {payload.get('format')!r}, expected {MISSION_FORMAT!r}"
            )
        if payload.get("schema_version") != MISSION_SCHEMA_VERSION:
            raise MissionError(
                f"unsupported mission schema_version {payload.get('schema_version')!r}; "
                f"expected {MISSION_SCHEMA_VERSION!r}"
            )
        try:
            grid = Grid.from_dict(payload.get("grid"))
        except GridError as exc:
            raise MissionError(f"grid: {exc}") from exc
        deploy_raw = payload.get("deploy_cells")
        if not isinstance(deploy_raw, (list, tuple)):
            raise MissionError("deploy_cells must be a list of [row, col] pairs")
        try:
            deploy = tuple(
                Cell.from_pair(pair, what="a deployment cell") for pair in deploy_raw
            )
        except GridError as exc:
            raise MissionError(str(exc)) from exc
        interactions_raw = payload.get("interactions")
        if not isinstance(interactions_raw, (list, tuple)) or not interactions_raw:
            raise MissionError("a mission needs a non-empty list of interactions")
        objectives_raw = payload.get("objectives")
        if not isinstance(objectives_raw, (list, tuple)) or not objectives_raw:
            raise MissionError("a mission needs a non-empty list of objectives")
        objectives: list[Objective] = []
        for record in objectives_raw:
            if not isinstance(record, Mapping):
                raise MissionError("an objective must be an object")
            unknown_fields = sorted(set(record) - _OBJECTIVE_KEYS)
            if unknown_fields:
                raise MissionError(
                    f"objective {record.get('id')!r} carries field(s) {unknown_fields} the schema "
                    "does not define"
                )
            objectives.append(
                Objective(
                    id=str(record.get("id", "")).strip(),
                    label=str(record.get("label", "")),
                    required=bool(record.get("required", True)),
                )
            )
        spec = cls(
            mission_id=str(payload.get("mission_id", "")).strip(),
            case_id=str(payload.get("case_id", "")).strip(),
            title=str(payload.get("title", "")),
            grid=grid,
            deploy_cells=deploy,
            interactions=tuple(Interaction.from_dict(record) for record in interactions_raw),
            objectives=tuple(objectives),
            status=str(payload.get("status", "")),
            note=str(payload.get("note", "")),
        )
        problems = spec.problems()
        if problems:
            raise MissionError(
                f"mission {spec.mission_id or '<unnamed>'} is not playable: " + "; ".join(problems)
            )
        return spec


def mission_from_dict(payload: object) -> MissionSpec:
    """Build a validated mission from an already-parsed document."""
    return MissionSpec.from_dict(payload)


def load_mission(path: str | Path | None = None) -> MissionSpec:
    """Read and validate a mission file, defaulting to the packaged spike fixture."""
    target = Path(path) if path is not None else MISSION_DATA_PATH
    try:
        payload = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:  # pragma: no cover - packaging error
        raise MissionError(f"mission data not found at {target}") from exc
    except json.JSONDecodeError as exc:
        raise MissionError(f"{target} is not valid JSON: {exc}") from exc
    try:
        return mission_from_dict(payload)
    except MissionError as exc:
        raise MissionError(f"{target}: {exc}") from exc
