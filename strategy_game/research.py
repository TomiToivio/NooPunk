"""Research, science and technology as the first instance of the strategic-project engine (#506).

Phase 1 of issue #506 asks for four small serializable records — a research project, a technology
node (the same record read as a *capability* the faction holds), a progress clock and a faction
capacity ledger — plus the one thing that turns a completed research programme into something the
RPG layer can use.

**Which layer the project check uses, and why.** Issue #506 says the lead researcher rolls a
**SCIENCE** skill check. In this crossover ``science`` is a **strategic agent skill**: it is one of
the seven proposed in ``data/strategic_skills.json``, whose ``status`` is ``PROPOSAL`` because issue
#482 approved the RPG foundation and the six *individual* skills (COG, INT, REF, SAV, SOM, WIL) and
deliberately did not approve a strategic roster. So the check is a
:attr:`~strategy_game.rpg.skills.ActionContext.FACTION_AGENT` check on the **strategic** ladder —
:attr:`strategy_game.rpg.fate.Character.strategic_skills` — resolved by
:func:`strategy_game.rpg.skills.check` with the proposal roster passed in. It is *not* an individual
scene check, and :data:`RESEARCH_LEAD_SKILL` is **not** promoted to an approved skill anywhere: with
no roster supplied the kernel refuses the check as pending author approval, which is the correct
behaviour and is covered by a test. The proposal's own ``mission_kinds`` for ``science`` are
``adopt_technology`` and ``investigate``, and the research kinds below use that vocabulary.

**Domain TAGs.** Issue #506 asks to "adapt to existing NoöPunk character sheet: SCIENCE plus
relevant domain TAGs such as Forensics, Parapsychology, Engineering". A domain TAG is a
``competence`` tag in issue #346's shared vocabulary, read through
:func:`strategy_game.rpg.skills.capabilities_of`. It is **reported**, never rated: the engine returns
which of the work's named domains the lead actually carries, and no tag moves the check or the
throughput, because ``rpg.skills.specialist_supplement`` already fixes that rule for the sheet ("it
grants no bonus, because a tag that moved a roll would be an unapproved mechanic"). Whether a matched
domain should ever modify the check is an author decision (row D28).

**Discovery, prototype and manufacture are three different grants.** :class:`TechNode` carries the
:class:`~strategy_game.projects.ProjectStage` its completion *produces*, and
:func:`complete_research` grants exactly that one capability. Understanding a recovered drive does
not hand the faction a factory: the next stage is a separate project whose prerequisite is the
capability this one granted. That is how the issue's non-conflation requirement is enforced by the
schema instead of by a rule somebody has to remember.
"""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, cast

from .projects import (
    FactionCapacity,
    Prerequisites,
    ProjectError,
    ProjectStage,
    StrategicProject,
    complete_project,
)
from .provenance import ProvenanceKind
from .rpg.fate import Character

if TYPE_CHECKING:  # no runtime cycle: campaign.state loads capability records lazily
    from .campaign.state import Campaign

__all__ = [
    "RESEARCH_LEAD_SKILL",
    "RESEARCH_PROJECT_KINDS",
    "RESEARCH_RESOURCE_KIND",
    "Capability",
    "FactionResearchCapacity",
    "ResearchCompletion",
    "ResearchProject",
    "ResearchYield",
    "RpgOption",
    "TechNode",
    "capability_from_dict",
    "complete_research",
    "prohibitions_for",
    "research_project_from_dict",
    "rpg_options",
]

#: The lead researcher's skill: the proposal's ``science`` id (``data/strategic_skills.json``,
#: ``status: PROPOSAL``). Nothing here approves it; the kernel refuses the check without the roster.
RESEARCH_LEAD_SKILL = "science"

#: The resource kind a research programme draws on by default. Issue #506's worked example commits
#: "3 research units"; the *kind* is data on the ledger, not a closed vocabulary.
RESEARCH_RESOURCE_KIND = "research"

#: Issue #506's seven kinds of research work, id -> the issue's own label. **Declared, not enforced**:
#: the issue says branches and kinds are "data-defined/modded", so :class:`ResearchProject.kind` stays
#: free text and this mapping exists so a caller can name the author's kinds without inventing ids.
RESEARCH_PROJECT_KINDS: Mapping[str, str] = {
    "archive_review": "Literature/archive review",
    "data_analysis": "Data analysis/intelligence synthesis",
    "basic_science": "Basic science / PSI experiments",
    "reverse_engineering": "Reverse engineering",
    "applied_engineering": "Applied engineering",
    "technology_transfer": "Technology transfer / industrialization",
    "biological_social_transformation": "Biological/social transformation",
}


@dataclass
class ResearchProject(StrategicProject):
    """A project whose success gate is the lead scientist's SCIENCE check (issue #506, criterion 1).

    The narrowing is deliberate and is the whole reason this type exists: a project that passes
    another lead skill is a perfectly good :class:`~strategy_game.projects.StrategicProject`, but it
    is not a *research project*, and calling it one would make the issue's first acceptance criterion
    unverifiable. Nothing else about the engine changes.
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.lead_skill != RESEARCH_LEAD_SKILL:
            raise ProjectError(
                f"a research project's lead check is the lead scientist's {RESEARCH_LEAD_SKILL.upper()} "
                f"check (issue #506); {self.lead_skill!r} is not it. A task with another lead skill is "
                "a StrategicProject, which the same engine already supports."
            )
        if self.lead_id and not self.domain_tags and not self.detail.get("domain_tags_waived"):
            raise ProjectError(
                f"research project {self.project_id!r} names no domain TAG. Issue #506 asks the check "
                "to adapt SCIENCE with the relevant domain (Forensics, Parapsychology, Engineering); "
                "declare the domains the work needs, or record why none applies."
            )


@dataclass(frozen=True)
class ResearchYield:
    """What a completed programme hands the **RPG layer** — issue #506 Phase 1's fourth criterion.

    Four optional ids, because the issue names three shapes of payoff ("a new RPG option, equipment
    or investigation clue") and the competence capability the lead and the faction gain is the
    fourth. All are ids into vocabularies that already exist: ``capability`` is a ``competence`` tag
    value (#346), ``equipment`` is a :attr:`~strategy_game.rpg.fate.Character.gear` entry, ``clue`` is
    an intel/evidence id, and ``option`` is a new choice the RPG can offer. Free text would let a
    narrator smuggle an effect through, so nothing here is free text.
    """

    capability: str = ""
    option: str = ""
    equipment: str = ""
    clue: str = ""

    def is_empty(self) -> bool:
        return not any((self.capability, self.option, self.equipment, self.clue))

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability": self.capability,
            "option": self.option,
            "equipment": self.equipment,
            "clue": self.clue,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any] | None) -> ResearchYield:
        if data is None:
            return cls()
        if not isinstance(data, Mapping):
            raise ProjectError(f"a research yield must be a mapping, got {type(data).__name__}")
        return cls(
            capability=str(data.get("capability") or ""),
            option=str(data.get("option") or ""),
            equipment=str(data.get("equipment") or ""),
            clue=str(data.get("clue") or ""),
        )


@dataclass(frozen=True)
class TechNode:
    """One capability: what a programme produces, and what producing it required (issue #506).

    Read as a record the faction *holds* it is the issue's "``Capability``" (see the alias below);
    read as a record the author *declares* it is a node of the branching graph Phase 3 will grow.
    ``branch`` and ``hybrid_of`` are free descriptive labels — the issue states that "branch identity
    is *descriptive*, not a rigid class: e.g. solar + bio, cyber + PSI" — so a hybrid path is a node
    that names both, and nothing derives a taxonomy from them.
    """

    node_id: str
    label: str
    #: The stage of understanding this node *is*. Not a tree level: a node at
    #: :attr:`~strategy_game.projects.ProjectStage.UNDERSTANDING` is a body of knowledge, and a node at
    #: :attr:`~strategy_game.projects.ProjectStage.MANUFACTURE` is an industrial fact.
    stage: ProjectStage
    requires: Prerequisites = field(default_factory=Prerequisites)
    branch: str = ""
    hybrid_of: tuple[str, ...] = ()
    #: Named ideological prohibitions, as belief labels the author's data attaches to this work.
    #: **Reported, never enforced here** (row D28): a faction that holds the belief is told the
    #: programme contradicts its own doctrine, and whether that stops the programme is a ruling.
    prohibited_by: tuple[str, ...] = ()
    yields: ResearchYield = ResearchYield()
    #: Other authored fields, retained verbatim so unknown material is never lost.
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not str(self.node_id).strip():
            raise ProjectError("a technology node needs a non-empty node_id")
        if not str(self.label).strip():
            raise ProjectError(f"technology node {self.node_id!r} needs a label")
        if not isinstance(self.stage, ProjectStage):
            try:
                object.__setattr__(self, "stage", ProjectStage(str(self.stage)))
            except ValueError as exc:
                raise ProjectError(
                    f"technology node {self.node_id!r}: stage {self.stage!r} is not one of "
                    f"({', '.join(s.value for s in ProjectStage)})"
                ) from exc
        if not isinstance(self.requires, Prerequisites):
            object.__setattr__(self, "requires", Prerequisites.from_dict(self.requires))
        if not isinstance(self.yields, ResearchYield):
            object.__setattr__(self, "yields", ResearchYield.from_dict(self.yields))
        if len(set(self.prohibited_by)) != len(self.prohibited_by):
            raise ProjectError(f"technology node {self.node_id!r}: prohibited_by repeats a label")

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = dict(self.detail)
        payload.update(
            {
                "node_id": self.node_id,
                "label": self.label,
                "stage": self.stage.value,
                "requires": self.requires.to_dict(),
                "branch": self.branch,
                "hybrid_of": list(self.hybrid_of),
                "prohibited_by": list(self.prohibited_by),
                "yields": self.yields.to_dict(),
            }
        )
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> TechNode:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a technology node record must be a mapping, got {type(data).__name__}")
        known = {
            "node_id", "label", "stage", "requires", "branch", "hybrid_of", "prohibited_by", "yields",
        }
        return cls(
            node_id=str(data.get("node_id") or ""),
            label=str(data.get("label") or ""),
            stage=data.get("stage"),  # type: ignore[arg-type]
            requires=Prerequisites.from_dict(data.get("requires")),
            branch=str(data.get("branch") or ""),
            hybrid_of=tuple(str(x) for x in (data.get("hybrid_of") or [])),
            prohibited_by=tuple(str(x) for x in (data.get("prohibited_by") or [])),
            yields=ResearchYield.from_dict(data.get("yields")),
            detail={key: value for key, value in data.items() if key not in known},
        )


#: The issue writes the record as "``TechNode``/``Capability``": the same five fields, named for what
#: the faction holds rather than for where it sits in a graph. One record, two readings — because a
#: second capability record would be a second thing for the two to disagree about.
Capability = TechNode

#: The issue's name for the throughput ledger (:class:`strategy_game.projects.FactionCapacity`).
#: One class: research is a resource *kind* on the same ledger, not a second ledger.
FactionResearchCapacity = FactionCapacity


def capability_from_dict(data: Mapping[str, Any]) -> TechNode:
    """Build a capability from :meth:`TechNode.to_dict` output (the campaign save/load seam)."""
    return TechNode.from_dict(data)


def research_project_from_dict(data: Mapping[str, Any]) -> ResearchProject:
    """Build a research project from :meth:`StrategicProject.to_dict` output.

    ``ResearchProject.from_dict`` narrows ``StrategicProject.from_dict`` by construction (its
    ``cls`` is the subclass), so a snapshot of a project whose lead skill is not SCIENCE is refused
    here rather than loading as a research project that the engine would never have advanced.
    """
    return cast(ResearchProject, ResearchProject.from_dict(data))


def prohibitions_for(
    campaign: Campaign, node: TechNode, *, faction_id: str | None = None
) -> tuple[str, ...]:
    """The node's declared prohibitions that the faction's **own members** actually hold.

    Beliefs are ``belief`` tags on the character sheets the campaign holds; the faction's doctrine is
    what its declared members believe, so a prohibition matching none of them is not a fact about
    this faction and is not reported. Reported rather than enforced, and with the matching labels
    named, so an author can see which doctrine the programme contradicts.
    """
    faction = campaign.faction(faction_id)
    held: set[str] = set()
    for member_id in (faction.leader_id, *faction.member_ids):
        sheet = campaign.sheets.get(member_id)
        if sheet is None:
            continue
        held.update(tag.value for tag in sheet.tags_of_kind("belief"))
    return tuple(sorted(set(node.prohibited_by) & held))


@dataclass(frozen=True)
class ResearchCompletion:
    """One resolved research programme: the capability granted and the RPG-facing payoff.

    ``applied`` is ``False`` on a replay of an already-resolved programme, which is what makes
    research completion **idempotent** in the save file as well as in memory.
    """

    project_id: str
    node_id: str
    turn: int
    applied: bool
    stage: ProjectStage
    capability_granted: bool = False
    option_id: str = ""
    equipment_id: str = ""
    clue_id: str = ""
    capability_id: str = ""
    resource_ids: tuple[str, ...] = ()
    prohibitions: tuple[str, ...] = ()
    note_index: int = -1

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "node_id": self.node_id,
            "turn": self.turn,
            "applied": self.applied,
            "stage": self.stage.value,
            "capability_granted": self.capability_granted,
            "option_id": self.option_id,
            "equipment_id": self.equipment_id,
            "clue_id": self.clue_id,
            "capability_id": self.capability_id,
            "resource_ids": list(self.resource_ids),
            "prohibitions": list(self.prohibitions),
            "note_index": self.note_index,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ResearchCompletion:
        if not isinstance(data, Mapping):
            raise ProjectError(f"a research completion must be a mapping, got {type(data).__name__}")
        try:
            stage = ProjectStage(str(data["stage"]))
        except (KeyError, ValueError) as exc:
            raise ProjectError(f"stage {data.get('stage')!r} is not a project stage") from exc
        return cls(
            project_id=str(data.get("project_id") or ""),
            node_id=str(data.get("node_id") or ""),
            turn=int(data.get("turn", 0)),
            applied=bool(data.get("applied", False)),
            stage=stage,
            capability_granted=bool(data.get("capability_granted", False)),
            option_id=str(data.get("option_id") or ""),
            equipment_id=str(data.get("equipment_id") or ""),
            clue_id=str(data.get("clue_id") or ""),
            capability_id=str(data.get("capability_id") or ""),
            resource_ids=tuple(str(x) for x in (data.get("resource_ids") or [])),
            prohibitions=tuple(str(x) for x in (data.get("prohibitions") or [])),
            note_index=int(data.get("note_index", -1)),
        )


def complete_research(
    campaign: Campaign,
    project_id: str,
    node: TechNode | None = None,
    *,
    turn: int,
    case_id: str | None = None,
) -> ResearchCompletion:
    """Resolve a filled research clock: grant the capability, the payoff and one audit note.

    The write order is the issue's, and each step is guarded so a replay changes nothing:

    1. the **generic** completion goes through :func:`strategy_game.projects.complete_project` — the
       one writer for a project completion — which grants the project's own resources and stamps its
       note;
    2. the **capability** the programme produced is recorded in ``Campaign.capabilities``. A
       capability cannot be granted before what it requires (``TechNode.requires.node_ids``), because
       that would be manufacture arriving before discovery;
    3. the **RPG-facing payoff** is written where the RPG layer already reads: the competence
       capability and the equipment onto the lead's sheet, the clue into the campaign's intelligence
       book and the named case's evidence inventory, and the option into this resolution's audit note
       and :func:`rpg_options`;
    4. **one** audit note of kind ``research_completion`` records which doctrine the work
       contradicted (:func:`prohibitions_for`), so the faction's own beliefs are visible at the
       moment the faction acts against them.
    """
    project = campaign.projects.get(project_id)
    if project is None:
        raise ProjectError(f"no project {project_id!r} on this campaign")
    if campaign.capabilities.get(project.node_id) is not None and node is None:
        node = campaign.capabilities[project.node_id]
    if node is None:
        raise ProjectError(
            f"research project {project_id!r} produces capability {project.node_id!r}; pass the "
            "declared node so the completion can name what it produced"
        )
    if project.node_id and node.node_id != project.node_id:
        raise ProjectError(
            f"project {project_id!r} produces {project.node_id!r}; the node passed is "
            f"{node.node_id!r}. A completion resolves the capability the project declared."
        )
    declared = campaign.tech_nodes.get(node.node_id)
    if declared is None:
        raise ProjectError(
            f"capability {node.node_id!r} is not declared in the campaign's tech_nodes; a completion "
            "grants a stage the world's own data declares, and inventing one here would be inventing "
            "a technology"
        )
    if declared != node:
        raise ProjectError(
            f"the node passed for {node.node_id!r} differs from the one tech_nodes declares; the "
            "declared node is the record"
        )
    ledger = campaign.capacities.get(project.faction_id)
    if ledger is None:
        raise ProjectError(
            f"faction {project.faction_id!r} has no capacity ledger; a project cannot draw on "
            "capacity the campaign does not track"
        )
    if not project.clock.is_complete:
        raise ProjectError(
            f"research project {project_id!r} is at {project.clock.filled}/{project.clock.work_required} "
            "segments; a completion resolves the difficulty-defined total work"
        )
    dangling = tuple(nid for nid in node.requires.node_ids if nid not in campaign.capabilities)
    if dangling:
        raise ProjectError(
            f"capability {node.node_id!r} requires {', '.join(dangling)}, which the campaign does not "
            "hold; a stage cannot be recorded before the stage it depends on"
        )
    lead = campaign.sheets.get(project.lead_id)
    if lead is None:
        raise ProjectError(
            f"project {project_id!r}: lead {project.lead_id!r} has no sheet on the campaign"
        )
    case = None
    if case_id is not None:
        case = campaign.cases.get(case_id)
        if case is None:
            raise ProjectError(f"case {case_id!r} is not on this campaign; a clue names its case")

    generic = complete_project(campaign, project_id, turn=turn)
    already = campaign.capabilities.get(node.node_id) is not None
    if already and project.detail.get("research_completion_note_index") is not None:
        _grant_capability_tag(lead, node.yields.capability)
        return ResearchCompletion(
            project_id=project_id,
            node_id=node.node_id,
            turn=turn,
            applied=False,
            stage=node.stage,
            capability_granted=False,
            option_id=node.yields.option,
            equipment_id=node.yields.equipment,
            clue_id=node.yields.clue,
            capability_id=node.yields.capability,
            resource_ids=(),
            prohibitions=prohibitions_for(campaign, node, faction_id=project.faction_id),
            note_index=int(project.detail["research_completion_note_index"]),
        )

    # Everything above is validation; nothing below may raise, so state is never half-written.
    if not already:
        campaign.capabilities[node.node_id] = node
    granted_capability = _grant_capability_tag(lead, node.yields.capability)
    if node.yields.equipment and node.yields.equipment not in lead.gear:
        lead.gear.append(node.yields.equipment)
    if node.yields.clue:
        if node.yields.clue not in campaign.intelligence_ids:
            campaign.intelligence_ids.append(node.yields.clue)
        if node.yields.clue not in campaign.faction(project.faction_id).intelligence_ids:
            campaign.faction(project.faction_id).intelligence_ids.append(node.yields.clue)
        if case is not None and node.yields.clue not in case.evidence_ids:
            case.evidence_ids.append(node.yields.clue)
    prohibitions = prohibitions_for(campaign, node, faction_id=project.faction_id)
    index = len(campaign.campaign_notes)
    campaign.campaign_notes.append(
        {
            "kind": "research_completion",
            "project_id": project_id,
            "faction_id": project.faction_id,
            "turn": turn,
            "node_id": node.node_id,
            "stage": node.stage.value,
            "branch": node.branch,
            "hybrid_of": list(node.hybrid_of),
            "option_id": node.yields.option,
            "equipment_id": node.yields.equipment,
            "clue_id": node.yields.clue,
            "capability_id": node.yields.capability,
            "prohibitions": list(prohibitions),
            "provenance": {
                "kind": ProvenanceKind.SIMULATED.value,
                "source": "strategy_game.research.complete_research",
                "note": (
                    "the capability this programme produced is one stage only (issue #506): "
                    f"{node.stage.value}, not the stages above or below it"
                ),
            },
            **({"generic_completion_note_index": generic.note_index} if generic.applied else {}),
        }
    )
    project.detail["research_completion_note_index"] = index
    return ResearchCompletion(
        project_id=project_id,
        node_id=node.node_id,
        turn=turn,
        applied=True,
        stage=node.stage,
        capability_granted=granted_capability,
        option_id=node.yields.option,
        equipment_id=node.yields.equipment,
        clue_id=node.yields.clue,
        capability_id=node.yields.capability,
        resource_ids=generic.resource_ids,
        prohibitions=prohibitions,
        note_index=index,
    )


def _grant_capability_tag(sheet: Character, capability: str) -> bool:
    """Add a ``competence`` capability to a sheet once; return whether it was added now.

    Uses the shared typed vocabulary (#346) rather than a second capability scheme, so a doctrine
    filed as a competence is still refused by name and a capability can never be read as a belief.
    """
    if not capability:
        return False
    from .characters import Tag

    if any(tag.value == capability for tag in sheet.tags_of_kind("competence")):
        return False
    sheet.tags = sheet.tags + (Tag("competence", capability),)
    return True


@dataclass(frozen=True)
class RpgOption:
    """One capability the faction holds, read as an option the RPG layer can offer (issue #506).

    Derived from ``Campaign.capabilities``, never stored twice: what the faction *knows* is the
    capability, and what a character may *do* with it is this view of the same record.
    """

    option_id: str
    node_id: str
    label: str
    stage: ProjectStage
    branch: str = ""
    hybrid_of: tuple[str, ...] = ()
    capability: str = ""
    equipment: str = ""
    clue: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "option_id": self.option_id,
            "node_id": self.node_id,
            "label": self.label,
            "stage": self.stage.value,
            "branch": self.branch,
            "hybrid_of": list(self.hybrid_of),
            "capability": self.capability,
            "equipment": self.equipment,
            "clue": self.clue,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> RpgOption:
        if not isinstance(data, Mapping):
            raise ProjectError(f"an RPG option must be a mapping, got {type(data).__name__}")
        try:
            stage = ProjectStage(str(data["stage"]))
        except (KeyError, ValueError) as exc:
            raise ProjectError(f"stage {data.get('stage')!r} is not a project stage") from exc
        return cls(
            option_id=str(data.get("option_id") or ""),
            node_id=str(data.get("node_id") or ""),
            label=str(data.get("label") or ""),
            stage=stage,
            branch=str(data.get("branch") or ""),
            hybrid_of=tuple(str(x) for x in (data.get("hybrid_of") or [])),
            capability=str(data.get("capability") or ""),
            equipment=str(data.get("equipment") or ""),
            clue=str(data.get("clue") or ""),
        )


def rpg_options(campaign: Campaign) -> tuple[RpgOption, ...]:
    """Every capability the faction holds, as an RPG-facing option, in node-id order.

    Research that changes later RPG decisions is Phase 1's fourth criterion; this is the read side of
    it. It derives and stores nothing, and returns the same tuple for the same campaign — which is
    what the save/load test pins.
    """
    options: list[RpgOption] = []
    for node_id in sorted(campaign.capabilities):
        node = campaign.capabilities[node_id]
        options.append(
            RpgOption(
                option_id=node.yields.option or node.node_id,
                node_id=node.node_id,
                label=node.label,
                stage=node.stage,
                branch=node.branch,
                hybrid_of=node.hybrid_of,
                capability=node.yields.capability,
                equipment=node.yields.equipment,
                clue=node.yields.clue,
            )
        )
    return tuple(options)
