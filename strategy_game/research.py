"""Issue #506: opt-in faction research clocks using the existing Fate kernel.

This is a deliberately small RPG-first vertical slice. It does not approve the
other strategic skill roster, invent a resource economy, or change legacy rules.
SCIENCE is the skill explicitly requested by the author in #506.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from random import Random
from typing import Any, Mapping

from .rpg.fate import Action, Character, Outcome, Resolution, resolve


class ResearchError(ValueError):
    """Invalid research declaration or unavailable prerequisite."""


@dataclass(frozen=True)
class TechNode:
    identifier: str
    name: str
    branches: tuple[str, ...]
    prerequisites: tuple[str, ...] = ()
    required_evidence: tuple[str, ...] = ()
    forbidden_policies: tuple[str, ...] = ()
    stage: str = "understanding"
    unlocks: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.identifier or not self.name or not self.branches:
            raise ResearchError("technology requires an id, name, and at least one branch")
        if self.identifier in self.prerequisites:
            raise ResearchError("technology cannot depend on itself")
        if self.stage not in {"understanding", "prototype", "manufacture", "deployment"}:
            raise ResearchError("unknown technology stage")

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier, "name": self.name,
            "branches": list(self.branches), "prerequisites": list(self.prerequisites),
            "required_evidence": list(self.required_evidence),
            "forbidden_policies": list(self.forbidden_policies),
            "stage": self.stage, "unlocks": list(self.unlocks),
        }

    @classmethod
    def from_dict(cls, record: Mapping[str, Any]) -> "TechNode":
        return cls(
            identifier=str(record["identifier"]), name=str(record["name"]),
            branches=tuple(record["branches"]),
            prerequisites=tuple(record.get("prerequisites", ())),
            required_evidence=tuple(record.get("required_evidence", ())),
            forbidden_policies=tuple(record.get("forbidden_policies", ())),
            stage=str(record.get("stage", "understanding")),
            unlocks=tuple(record.get("unlocks", ())),
        )


def validate_catalog(nodes: Mapping[str, TechNode]) -> None:
    """Reject dangling or cyclic prerequisites; branches may otherwise overlap."""
    for key, node in nodes.items():
        if key != node.identifier:
            raise ResearchError("technology key disagrees with node id")
        if any(prerequisite not in nodes for prerequisite in node.prerequisites):
            raise ResearchError(f"unknown prerequisite for {key}")
    visited: set[str] = set()
    active: set[str] = set()

    def visit(key: str) -> None:
        if key in active:
            raise ResearchError("cyclic technology prerequisites")
        if key in visited:
            return
        active.add(key)
        for prerequisite in nodes[key].prerequisites:
            visit(prerequisite)
        active.remove(key)
        visited.add(key)

    for key in nodes:
        visit(key)


@dataclass
class ResearchProject:
    identifier: str
    node_id: str
    leader_id: str
    difficulty: int
    work_required: int
    progress: int = 0
    allocated_capacity: int = 0
    paused: bool = False
    completed: bool = False

    def __post_init__(self) -> None:
        if not self.identifier or not self.node_id or not self.leader_id:
            raise ResearchError("project, node and lead ids are required")
        if not isinstance(self.difficulty, int):
            raise ResearchError("difficulty must be an integer Fate target")
        for name in ("work_required", "progress", "allocated_capacity"):
            value = getattr(self, name)
            if type(value) is not int or value < 0:
                raise ResearchError(f"{name} must be a nonnegative integer")
        if self.work_required == 0 or self.progress > self.work_required:
            raise ResearchError("project requires positive work and bounded progress")
        if self.completed != (self.progress == self.work_required):
            raise ResearchError("completed flag must equal clock completion")

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier, "node_id": self.node_id,
            "leader_id": self.leader_id, "difficulty": self.difficulty,
            "work_required": self.work_required, "progress": self.progress,
            "allocated_capacity": self.allocated_capacity, "paused": self.paused,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ResearchProject":
        return cls(**dict(data))


@dataclass
class ResearchState:
    nodes: dict[str, TechNode]
    projects: dict[str, ResearchProject] = field(default_factory=dict)
    known: set[str] = field(default_factory=set)
    evidence: set[str] = field(default_factory=set)
    policies: set[str] = field(default_factory=set)
    unlocked_rpg_options: set[str] = field(default_factory=set)
    history: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        validate_catalog(self.nodes)
        if not self.known.issubset(self.nodes):
            raise ResearchError("known technologies must exist in catalog")
        for key, project in self.projects.items():
            if key != project.identifier or project.node_id not in self.nodes:
                raise ResearchError("project reference is invalid")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "research-save-1",
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "projects": {k: v.to_dict() for k, v in self.projects.items()},
            "known": sorted(self.known), "evidence": sorted(self.evidence),
            "policies": sorted(self.policies),
            "unlocked_rpg_options": sorted(self.unlocked_rpg_options),
            "history": list(self.history),
        }

    @classmethod
    def from_dict(cls, record: Mapping[str, Any]) -> "ResearchState":
        if record.get("schema_version") != "research-save-1":
            raise ResearchError("unsupported research save schema")
        return cls(
            nodes={k: TechNode.from_dict(v) for k, v in record["nodes"].items()},
            projects={k: ResearchProject.from_dict(v) for k, v in record["projects"].items()},
            known=set(record.get("known", ())), evidence=set(record.get("evidence", ())),
            policies=set(record.get("policies", ())),
            unlocked_rpg_options=set(record.get("unlocked_rpg_options", ())),
            history=list(record.get("history", ())),
        )

    def eligible(self, project: ResearchProject) -> bool:
        node = self.nodes[project.node_id]
        return (
            set(node.prerequisites).issubset(self.known)
            and set(node.required_evidence).issubset(self.evidence)
            and not set(node.forbidden_policies).intersection(self.policies)
        )

    def add_evidence(self, identifier: str) -> None:
        """A mission may unlock research by supplying a concrete evidence id."""
        if not identifier:
            raise ResearchError("evidence id is required")
        self.evidence.add(identifier)


@dataclass(frozen=True)
class ResearchTurn:
    outcome: str
    gained: int
    progress: int
    work_required: int
    check: Resolution | None = None


def advance_research(
    state: ResearchState, project_id: str, lead: Character, *, rng: Random,
) -> ResearchTurn:
    """Resolve one turn: Fate SCIENCE gate, then allocated faction work units.

    Fate ties do not count as successful work for this project-clock rule.
    Failed/stalled turns preserve prior progress; no hidden resource currency is spent.
    """
    project = state.projects[project_id]
    if project.completed:
        return ResearchTurn("already_completed", 0, project.progress, project.work_required)
    if project.paused:
        return ResearchTurn("paused", 0, project.progress, project.work_required)
    if lead.id != project.leader_id:
        raise ResearchError("assigned lead does not match project")
    if "SCIENCE" not in lead.strategic_skills:
        raise ResearchError("lead has no explicit SCIENCE strategic skill rating")
    if not state.eligible(project):
        return ResearchTurn("blocked", 0, project.progress, project.work_required)
    if project.allocated_capacity == 0:
        return ResearchTurn("unfunded", 0, project.progress, project.work_required)
    check = resolve(
        Action.OVERCOME, lead.strategic_skills["SCIENCE"],
        project.difficulty, rng=rng,
    )
    if check.outcome not in (Outcome.SUCCESS, Outcome.SUCCESS_WITH_STYLE):
        result = ResearchTurn("stalled", 0, project.progress, project.work_required, check)
    else:
        gained = min(project.allocated_capacity, project.work_required - project.progress)
        project.progress += gained
        project.completed = project.progress == project.work_required
        if project.completed:
            state.known.add(project.node_id)
            state.unlocked_rpg_options.update(state.nodes[project.node_id].unlocks)
        result = ResearchTurn(
            "completed" if project.completed else "advanced",
            gained, project.progress, project.work_required, check,
        )
    state.history.append({
        "project_id": project_id, "lead_id": lead.id, "outcome": result.outcome,
        "gained": result.gained, "progress": result.progress,
        "dice": list(check.dice), "total": check.total,
    })
    return result


def demo_research(seed: int = 17) -> dict[str, Any]:
    """A non-canonical example: mission evidence enables an NHI research clock."""
    artifact = TechNode(
        "nhi_drive_principles", "Recovered drive principles",
        ("alien-derived", "quantumpunk"), required_evidence=("crash_fragment",),
        unlocks=("inspect_drive_field",),
    )
    state = ResearchState(
        nodes={artifact.identifier: artifact},
        projects={"drive": ResearchProject("drive", artifact.identifier, "agent", 1, 12, allocated_capacity=3)},
    )
    lead = Character("agent", "Research lead", ["Methodical"], strategic_skills={"SCIENCE": 3})
    state.add_evidence("crash_fragment")
    rng = Random(seed)
    outcomes = []
    for _ in range(8):
        outcomes.append(advance_research(state, "drive", lead, rng=rng).outcome)
        if state.projects["drive"].completed:
            break
    return {"outcomes": outcomes, "state": state.to_dict()}
