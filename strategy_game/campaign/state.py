"""The one campaign world state the roadmap's three phases will share (#502).

Phase 1 asks for minimal faction state "under the hood" — leader, members,
objectives, relationships, intelligence, resources, reputation — plus save/load, and
states the architecture rule this module follows: **one world model, three views**,
with "small data schemas and versioned save files that grow progressively". So the
members are ids that annotate records held elsewhere, and every extension point is an
empty declared blank, not an invented mechanic (AGENTS.md §1).

Why this is a new module instead of one of the existing state containers
------------------------------------------------------------------------

Each existing candidate was audited and left as it is:

* :class:`strategy_game.core.WorldState` is the scaffold's *declared-data board*
  (locations, edges, events); its ``Faction`` carries a leader and assets but no
  member roster, objectives or persistable campaign books. Extending *it* would also
  change the payload its pinned entrypoint contract derives from, so this package
  subclasses ``core.Faction`` (same field vocabulary, verifiable identity) instead of
  forking or widening the board container.
* :mod:`src.simulation.world_state` is the #40 event-log reducer state — the
  empirical LaclauGPT side, not a playable campaign.
* :class:`strategy_game.local_slice.Game` is the #322 numeric playtest slice with its
  own Leader/Party/Mission records and turn simulation.
* :class:`src.text_game.model.World` is the #51 text prototype's rooms/items/actors.

What is reused verbatim, and from where
---------------------------------------

* the sheet: :class:`strategy_game.rpg.fate.Character` — issue #482's approved
  two-layer model (one sheet, six individual skills plus the strategic ladder) —
  held **by identity** on :attr:`Campaign.sheets`, never copied;
* the member structure: the one-leader-plus-four-agent seat structure approved in
  #461/#482 (:data:`AGENT_CAPACITY` is :data:`strategy_game.rpg.roster.AGENT_SEAT_COUNT`
  itself — asserted by ``assertIs`` in the tests, not a copied number);
* the faction base: :class:`strategy_game.core.Faction` (``identifier``, ``name``,
  ``leader_id``, ``asset_ids``). ``asset_ids`` keeps its existing meaning (Asset
  records owned by the faction); the Phase 1 member roster is the new
  ``member_ids`` book rather than a second meaning for the base field;
* ties: :class:`strategy_game.relationships.RelationshipEdge` (issue #346) reused
  verbatim through its own ``edge_from_dict`` loader — no second tie record here;
* reputation: a *named label* list, not a number — the quantities module (#323/#338)
  keeps political quantities apart and no numeric reputation scale is approved.

The PC premise (#502): the player character **is the faction leader from the
start**. :attr:`Campaign.faction_id` names the player's faction and
:attr:`Campaign.leader_id` names its leader — a distinct :class:`Leader` type, not a
rookie field agent who earns strategy access. A campaign cannot be constructed with
one of the two and not the other.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Mapping

from ..core import Faction
from ..provenance import Provenance
from ..rpg.fate import Character, Consequence
from ..rpg.roster import AGENT_SEAT_COUNT
from ..relationships import RelationshipEdge, edge_from_dict

if TYPE_CHECKING:  # no runtime cycle: the project and research records are loaded lazily below
    from ..projects import FactionCapacity, StrategicProject
    from ..research import TechNode

if TYPE_CHECKING:  # no runtime cycle: Case lives in .case and state never imports it at runtime
    from .case import Case

__all__ = [
    "SCHEMA_VERSION",
    "AGENT_CAPACITY",
    "CampaignError",
    "Agent",
    "Campaign",
    "CampaignFaction",
    "Leader",
    "campaign_from_dict",
    "load_campaign",
    "save_campaign",
]

#: Save-file shape marker. Bump on an **incompatible** change; ``campaign_from_dict`` refuses a
#: snapshot with a different marker instead of guessing a migration (roadmap rule 1: versioned saves
#: that **grow** — later phases extend the payload; they do not reinterpret it). Growth that is
#: *compatible* keeps the marker: the strategic-project books added here (#506 Phase 1) are new
#: optional fields with empty defaults, so a snapshot written before them still loads and every field
#: it did carry is read back unchanged — nothing is reinterpreted and nothing is guessed. A change
#: that instead gave an existing field a new meaning, or made an old snapshot unreadable, is the case
#: this marker exists for.
SCHEMA_VERSION = "campaign-save-1"

#: The member capacity of a playable faction: one leader and four agents (#461/#482).
#: The *structure* is approved; who sits in the seats is author content.
AGENT_CAPACITY = AGENT_SEAT_COUNT


class CampaignError(ValueError):
    """A campaign-record or save-file operation the schema does not allow."""


def _text(value: Any, where: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise CampaignError(f"{where} must be a non-empty identifier")


@dataclass(frozen=True)
class Leader:
    """The faction-leader PC: a named identity record binding one character id (issue #502).

    The PC **is the faction leader from the start**; this distinct type exists so a
    leader is never modelled as a field agent who gets promoted later. The full sheet
    stays on :attr:`Campaign.sheets` — this view adds no attributes of its own and
    cannot drift from the sheet it names. The seat vocabulary is #461/#482's: the
    leader chairs the faction and the four :class:`Agent` members carry its work.
    """

    identifier: str
    name: str
    faction_id: str

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CampaignError("a leader needs a non-empty identifier")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.identifier, "name": self.name, "faction_id": self.faction_id}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Leader":
        if not isinstance(data, Mapping):
            raise CampaignError(f"a leader record must be a mapping, got {type(data).__name__}")
        return cls(
            identifier=_text(data.get("id"), "a leader record's id"),
            name=str(data.get("name", "")),
            faction_id=_text(data.get("faction_id"), "a leader record's faction_id"),
        )


@dataclass(frozen=True)
class Agent:
    """One of the faction's member agents: a named identity record over a sheet (#461/#482).

    The party around the leader are agents (Phase 1's PC premise); this is the member
    record, distinct from :class:`Leader` — an agent does not chair the faction and is
    never the PC. Sheets live once on :attr:`Campaign.sheets`, so leader and agent
    records are identities, not duplicated character models.
    """

    identifier: str
    name: str
    faction_id: str

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CampaignError("an agent needs a non-empty identifier")

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.identifier, "name": self.name, "faction_id": self.faction_id}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Agent":
        if not isinstance(data, Mapping):
            raise CampaignError(f"an agent record must be a mapping, got {type(data).__name__}")
        return cls(
            identifier=_text(data.get("id"), "an agent record's id"),
            name=str(data.get("name", "")),
            faction_id=_text(data.get("faction_id"), "an agent record's faction_id"),
        )


@dataclass
class CampaignFaction(Faction):
    """The playable faction: the scaffold's :class:`~strategy_game.core.Faction` plus Phase 1's books.

    ``identifier``, ``name``, ``leader_id`` and ``asset_ids`` come from the base
    record unchanged — ``asset_ids`` keeps its original meaning (Asset records owned
    by the faction), so the member roster is a genuinely new ``member_ids`` field
    rather than a second use of an existing one. Two collections would exist for one
    concept otherwise.

    Every book below is an **inventory or a declared blank**: there is deliberately no
    numeric rating anywhere (the scaffold stores unspecified quantities never —
    storing a number *is* inventing a mechanic, per ``src.simulation.world_state``'s
    and the quantities layer's rule), and no transition threshold, because none is
    approved.
    """

    #: The faction's members (the leader plus at most four agents, #461/#482).
    member_ids: list[str] = field(default_factory=list)
    #: Free-text objectives the author's scenario supplies. Not mission ids — the
    #: mission board is Phase 2 and stays unbuilt.
    objectives: list[str] = field(default_factory=list)
    #: Sparse intel record ids the faction holds. What an intel record *is* stays with
    #: the evidence layer; a numeric "intelligence stat" is deliberately absent.
    intelligence_ids: list[str] = field(default_factory=list)
    #: Free-text reputation labels, e.g. ``"known_in_helsinki"``. A numeric track
    #: would invent an unapproved mechanic.
    reputation_labels: list[str] = field(default_factory=list)
    #: The faction's resource inventory ids. Contents are author data; these are the
    #: books Phase 1 asks for ("minimal faction state ... intelligence, resources").
    resources: list[str] = field(default_factory=list)
    #: Provenance of the faction's authored state, so an evidence-backed label is
    #: never silently confused with an authored one (INTEGRATION_BOUNDARIES.md).
    provenance: Provenance = field(default_factory=Provenance)
    #: Every other authored field, retained verbatim so unknown material is never
    #: lost — the same retention discipline ``factions.GlobalFaction`` follows.
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        members = [m for m in self.member_ids]
        if len(set(members)) != len(members):
            raise CampaignError(f"faction {self.identifier!r}: duplicate member id")
        if len([m for m in members if m != self.leader_id]) > AGENT_CAPACITY:
            raise CampaignError(
                f"faction {self.identifier!r} declares more than {AGENT_CAPACITY} agent members "
                f"(#461/#482); a larger roster is an author decision"
            )
        if len(set(self.resources)) != len(self.resources):
            raise CampaignError(f"faction {self.identifier!r}: duplicate resource id")
        if not isinstance(self.provenance, Provenance):
            self.provenance = Provenance.from_dict(self.provenance)

    def to_dict(self) -> dict[str, Any]:
        """The base record's fields plus this layer's books, plain JSON throughout."""
        payload: dict[str, Any] = dict(self.detail)
        payload.update(
            {
                "id": self.identifier,
                "name": self.name,
                "leader_id": self.leader_id,
                "asset_ids": list(self.asset_ids),
                "member_ids": list(self.member_ids),
                "objectives": list(self.objectives),
                "intelligence_ids": list(self.intelligence_ids),
                "reputation_labels": list(self.reputation_labels),
                "resources": list(self.resources),
                "provenance": self.provenance.to_dict(),
            }
        )
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CampaignFaction":
        if not isinstance(data, Mapping):
            raise CampaignError(f"a faction record must be a mapping, got {type(data).__name__}")
        known = {
            "id", "identifier", "name", "leader_id", "asset_ids", "member_ids",
            "objectives", "intelligence_ids", "reputation_labels", "resources", "provenance",
        }
        payload = dict(data)
        return cls(
            identifier=str(payload.get("id") or payload.get("identifier") or ""),
            name=str(payload.get("name") or ""),
            leader_id=str(payload.get("leader_id") or "") or None,
            asset_ids=[str(x) for x in (payload.get("asset_ids") or [])],
            member_ids=[str(x) for x in (payload.get("member_ids") or [])],
            objectives=[str(x) for x in (payload.get("objectives") or [])],
            intelligence_ids=[str(x) for x in (payload.get("intelligence_ids") or [])],
            reputation_labels=[str(x) for x in (payload.get("reputation_labels") or [])],
            resources=[str(x) for x in (payload.get("resources") or [])],
            provenance=Provenance.from_dict(payload.get("provenance")),
            detail={key: value for key, value in payload.items() if key not in known},
        )


@dataclass
class Campaign:
    """One shared world model (#502 rule 1): sheets, factions, cases, ties — one each.

    There is deliberately **one** of each collection at package level. Cases, sheets,
    ties and factions are all keyed by id and shared; nothing in this package nests a
    second case store or a faction private roster store beside them.
    """

    #: The player's faction — the PC premise: the player character **is** its leader.
    faction_id: str = ""
    #: The leader's character id. Distinct from the agent members; from day one.
    leader_id: str = ""
    sheets: dict[str, Character] = field(default_factory=dict)
    factions: dict[str, CampaignFaction] = field(default_factory=dict)
    cases: dict[str, "Case"] = field(default_factory=dict)
    ties: dict[str, RelationshipEdge] = field(default_factory=dict)
    #: Campaign-wide intel record ids the shared world has picked up; a faction's own
    #: list names what it has. Declared blank: what a record is is the case layer's.
    intelligence_ids: list[str] = field(default_factory=list)
    #: Campaign-scoped authored notes. Nothing reads them; provenance keeps them honest.
    campaign_notes: list[dict[str, Any]] = field(default_factory=list)
    #: The strategic projects declared on this campaign, by project id (issue #506 Phase 1). Research
    #: is the first kind of project on the one engine; a construction, organising or diplomatic task
    #: is the same record. The books live **here**, on the one world model, rather than in a second
    #: state file — the roadmap's rule 1 ("one world model, three views").
    projects: dict[str, StrategicProject] = field(default_factory=dict)
    #: The capability nodes the author's data declares for this world, by node id: the branching
    #: technology graph Phase 3 grows. Declared, not held.
    tech_nodes: dict[str, TechNode] = field(default_factory=dict)
    #: The capabilities the faction **holds**, by node id — one stage at a time, each granted by a
    #: completed project. This is what a research programme produces and what the RPG reads as a new
    #: option (``research.rpg_options``).
    capabilities: dict[str, TechNode] = field(default_factory=dict)
    #: One resource-throughput ledger per faction id (``projects.FactionCapacity``): what each faction
    #: can do per turn, and what it has committed to which project.
    capacities: dict[str, FactionCapacity] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if bool(self.faction_id) != bool(self.leader_id):
            raise CampaignError(
                "the PC premise binds the leader and the faction together (#502): the player "
                "character is the faction leader from the start, so one cannot be set alone"
            )
        if self.faction_id and self.faction_id not in self.factions:
            raise CampaignError(
                f"campaign faction {self.faction_id!r} is not among the factions; "
                "an unknown faction id is a defect, not a default"
            )
        if self.leader_id and self.leader_id not in self.sheets:
            raise CampaignError(
                f"campaign leader {self.leader_id!r} has no sheet on the campaign; "
                "inventing one would be inventing a character"
            )
        for faction_id, ledger in self.capacities.items():
            if ledger.faction_id != faction_id:
                raise CampaignError(
                    f"capacity ledger {faction_id!r} names faction {ledger.faction_id!r}; a ledger is "
                    "keyed by the faction it belongs to"
                )
            if faction_id not in self.factions:
                raise CampaignError(
                    f"capacity ledger {faction_id!r} belongs to no faction on this campaign; "
                    "an unknown faction id is a defect, not a default"
                )
        for project_id, project in self.projects.items():
            if project.project_id != project_id:
                raise CampaignError(
                    f"project record {project_id!r} names itself {project.project_id!r}; a project is "
                    "keyed by its own id"
                )
            if project.faction_id not in self.factions:
                raise CampaignError(
                    f"project {project_id!r} belongs to faction {project.faction_id!r}, which is not "
                    "on this campaign"
                )
        for node_id, node in self.capabilities.items():
            declared = self.tech_nodes.get(node_id)
            if declared is None:
                raise CampaignError(
                    f"capability {node_id!r} is held but not declared in tech_nodes; a held stage "
                    "must be one the world's data declares"
                )
            if declared != node:
                raise CampaignError(
                    f"capability {node_id!r} differs from the node tech_nodes declares; the held "
                    "stage and the declared node are one record"
                )
    # -- roster ---------------------------------------------------------------

    def attach_sheet(self, sheet: Character) -> None:
        """Bind a character sheet to the campaign **by identity**."""
        if not isinstance(sheet, Character):
            raise CampaignError("campaign sheets are strategy_game.rpg.fate.Character records")
        existing = self.sheets.get(sheet.id)
        if existing is not None and existing is not sheet:
            raise CampaignError(f"character {sheet.id!r} already has a different sheet")
        self.sheets[sheet.id] = sheet

    def agent_views(self, faction_id: str | None = None) -> tuple[Agent, ...]:
        """Agent identity views for the faction's declared members, in ``member_ids`` order.

        Raises for a member without a bound sheet rather than inventing a name; a
        declared roster shorter than four is a declared blank — see
        :meth:`roster_report`, which reports it instead of padding it.
        """
        faction = self.faction(faction_id)
        missing = [m for m in faction.member_ids if m not in self.sheets]
        if missing:
            raise CampaignError(
                f"faction {faction.identifier!r}: member(s) {missing} have no sheet on the "
                "campaign; inventing one would be inventing a character"
            )
        return tuple(
            Agent(identifier=m, name=self.sheets[m].name, faction_id=faction.identifier)
            for m in faction.member_ids
            if m != faction.leader_id
        )

    def leader_view(self, faction_id: str | None = None) -> Leader:
        """The faction's leader as a :class:`Leader` record."""
        faction = self.faction(faction_id)
        if not faction.leader_id:
            raise CampaignError(f"faction {faction.identifier!r} declares no leader")
        sheet = self.sheets.get(faction.leader_id)
        if sheet is None:
            raise CampaignError(
                f"leader {faction.leader_id!r} has no sheet on the campaign; "
                "inventing one would be inventing a character"
            )
        return Leader(identifier=sheet.id, name=sheet.name, faction_id=faction.identifier)

    def faction(self, faction_id: str | None = None) -> "CampaignFaction":
        target = faction_id or self.faction_id
        if not target or target not in self.factions:
            raise CampaignError(f"no faction {target!r} on this campaign")
        return self.factions[target]

    def roster_report(self, faction_id: str | None = None) -> dict[str, Any]:
        """The leader plus the member roster **and the declared blanks**, so a short
        roster is visible rather than padded."""
        faction = self.faction(faction_id)
        members = [m for m in faction.member_ids if m != faction.leader_id]
        return {
            "leader_id": faction.leader_id or "",
            "member_ids": list(members),
            "agent_capacity": AGENT_CAPACITY,
            "unfilled_seats": max(0, AGENT_CAPACITY - len(members)),
        }

    # -- validation / persistence ------------------------------------------------

    def structural_problems(self) -> tuple[str, ...]:
        """Referential problems, reported rather than raised, in a stable order.

        Validation checks **structure** — ids resolve, seats stay within the approved
        roster structure, ties end at known records. It checks no balance, cost,
        threshold or cadence, because none is approved.
        """
        problems: list[str] = []
        faction = self.factions.get(self.faction_id)
        if faction is not None:
            if faction.leader_id != self.leader_id:
                problems.append(
                    f"campaign leader {self.leader_id!r} is not the faction's own "
                    f"leader_id {faction.leader_id!r}"
                )
        for identifier, faction in self.factions.items():
            member_count = sum(1 for m in faction.member_ids if m != faction.leader_id)
            if member_count > AGENT_CAPACITY:
                problems.append(
                    f"faction {identifier!r} declares {member_count} agent members; "
                    f"the approved maximum is {AGENT_CAPACITY} (#461/#482)"
                )
            for endpoint in (faction.leader_id, *faction.member_ids):
                if endpoint and endpoint not in self.sheets:
                    problems.append(f"faction {identifier!r}: member {endpoint!r} has no sheet")
        for cid, case in self.cases.items():
            for endpoint in (case.investigator, case.partner):
                if endpoint and endpoint not in self.sheets:
                    problems.append(f"case {cid!r}: participant {endpoint!r} has no sheet")
        for tie_id, tie in self.ties.items():
            for endpoint in (tie.holder_id, tie.other_id):
                if endpoint not in self.sheets and endpoint not in self.factions:
                    problems.append(f"tie {tie_id}: endpoint {endpoint!r} is not a known record")
        for project_id, project in self.projects.items():
            if project.lead_id and project.lead_id not in self.sheets:
                problems.append(f"project {project_id!r}: lead {project.lead_id!r} has no sheet")
            ledger = self.capacities.get(project.faction_id)
            if ledger is None:
                problems.append(
                    f"project {project_id!r}: faction {project.faction_id!r} has no capacity ledger "
                    "to draw on"
                )
            elif project.resource_kind not in ledger.units:
                problems.append(
                    f"project {project_id!r}: the faction's ledger declares no {project.resource_kind!r} "
                    "capacity"
                )
        for node_id, node in self.capabilities.items():
            for required in node.requires.node_ids:
                if required not in self.capabilities:
                    problems.append(
                        f"capability {node_id!r} requires node {required!r}, which the campaign does "
                        "not hold"
                    )
        for node_id, node in self.tech_nodes.items():
            for required in node.requires.node_ids:
                if required not in self.tech_nodes:
                    problems.append(
                        f"tech node {node_id!r} requires node {required!r}, which is not declared"
                    )
        return tuple(problems)

    def to_dict(self) -> dict[str, Any]:
        """The JSON save payload. This is the file format; nothing else is stored.

        Deliberately exposes only declared data: no score, no threshold, no cadence,
        no derived quantity of any kind.
        """
        return {
            "schema_version": SCHEMA_VERSION,
            "faction_id": self.faction_id,
            "leader_id": self.leader_id,
            "sheets": {cid: _sheet_dict(sheet) for cid, sheet in sorted(self.sheets.items())},
            "factions": {fid: f.to_dict() for fid, f in sorted(self.factions.items())},
            "cases": {cid: case.to_dict() for cid, case in sorted(self.cases.items())},
            "ties": {tid: tie.to_dict() for tid, tie in sorted(self.ties.items())},
            "intelligence_ids": sorted(self.intelligence_ids),
            "campaign_notes": [dict(note) for note in self.campaign_notes],
            "projects": {pid: p.to_dict() for pid, p in sorted(self.projects.items())},
            "tech_nodes": {nid: n.to_dict() for nid, n in sorted(self.tech_nodes.items())},
            "capabilities": {nid: n.to_dict() for nid, n in sorted(self.capabilities.items())},
            "capacities": {fid: c.to_dict() for fid, c in sorted(self.capacities.items())},
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, allow_nan=False)


def campaign_from_dict(report: Mapping[str, Any]) -> Campaign:
    """Build a campaign from :meth:`Campaign.to_dict` output.

    A snapshot with a foreign ``schema_version`` is refused rather than guessed into
    shape: same-marker saves round trip exactly, and growth across phases means new
    optional fields behind a bumped marker, never reinterpretation.
    """
    if not isinstance(report, Mapping):
        raise CampaignError(f"a campaign save must be a mapping, got {type(report).__name__}")
    if report.get("schema_version") != SCHEMA_VERSION:
        raise CampaignError(
            f"unsupported campaign save schema_version {report.get('schema_version')!r}; "
            f"expected {SCHEMA_VERSION!r}"
        )
    from ..projects import capacity_from_dict, project_from_dict
    from ..research import capability_from_dict
    from .case import case_from_dict  # local to keep .state importable without .case

    sheets = {
        cid: _sheet_from_dict(payload)
        for cid, payload in dict(report.get("sheets") or {}).items()
    }
    factions = {
        fid: CampaignFaction.from_dict(payload)
        for fid, payload in dict(report.get("factions") or {}).items()
    }
    cases = {
        cid: case_from_dict(payload) for cid, payload in dict(report.get("cases") or {}).items()
    }
    ties = {tid: edge_from_dict(payload) for tid, payload in dict(report.get("ties") or {}).items()}
    return Campaign(
        faction_id=str(report.get("faction_id") or ""),
        leader_id=str(report.get("leader_id") or ""),
        sheets=sheets,
        factions=factions,
        cases=cases,
        ties=ties,
        intelligence_ids=[str(x) for x in (report.get("intelligence_ids") or [])],
        campaign_notes=[dict(note) for note in (report.get("campaign_notes") or [])],
        projects={
            pid: project_from_dict(payload)
            for pid, payload in dict(report.get("projects") or {}).items()
        },
        tech_nodes={
            nid: capability_from_dict(payload)
            for nid, payload in dict(report.get("tech_nodes") or {}).items()
        },
        capabilities={
            nid: capability_from_dict(payload)
            for nid, payload in dict(report.get("capabilities") or {}).items()
        },
        capacities={
            fid: capacity_from_dict(payload)
            for fid, payload in dict(report.get("capacities") or {}).items()
        },
    )


# -- sheet serialization ----------------------------------------------------------

def _sheet_dict(sheet: Character) -> dict[str, Any]:
    """The approved sheet's plain-JSON form, reused rather than re-declared.

    ``rpg.boundary.LeaderRpgLayer.sheet()`` is the display projection the strategy
    layer already reads for a subset of these fields; the save persists the **full**
    sheet, so the tests pin this payload against the record's own declared fields.
    """
    return {
        "id": sheet.id,
        "name": sheet.name,
        "aspects": list(sheet.aspects),
        "tags": [tag.to_dict() for tag in sheet.tags],
        "skills": dict(sheet.skills),
        "strategic_skills": dict(sheet.strategic_skills),
        "stunts": list(sheet.stunts),
        "gear": list(sheet.gear),
        "fate_points": sheet.fate_points,
        "refresh": sheet.refresh,
        "physical_stress": list(sheet.physical_stress),
        "mental_stress": list(sheet.mental_stress),
        "consequences": [
            {"name": c.name, "severity": c.severity, "recovered": c.recovered}
            for c in sheet.consequences
        ],
        "body": sheet.body,
        "cortical_stack": sheet.cortical_stack,
        "resleeved": sheet.resleeved,
        "natural_psi": sheet.natural_psi,
        "psi_abilities": list(sheet.psi_abilities),
        "statuses": list(sheet.statuses),
    }


def _sheet_from_dict(payload: Mapping[str, Any]) -> Character:
    from ..characters import Tag

    return Character(
        id=str(payload["id"]),
        name=str(payload.get("name", "")),
        aspects=[str(x) for x in (payload.get("aspects") or [])],
        skills={str(k): int(v) for k, v in dict(payload.get("skills") or {}).items()},
        strategic_skills={
            str(k): int(v) for k, v in dict(payload.get("strategic_skills") or {}).items()
        },
        stunts=[str(x) for x in (payload.get("stunts") or [])],
        fate_points=int(payload.get("fate_points", 3)),
        refresh=int(payload.get("refresh", 3)),
        physical_stress=[bool(x) for x in (payload.get("physical_stress") or [])],
        mental_stress=[bool(x) for x in (payload.get("mental_stress") or [])],
        consequences=[
            Consequence(name=str(c.get("name", "")), severity=int(c.get("severity", 0)),
                        recovered=bool(c.get("recovered", False)))
            for c in (payload.get("consequences") or [])
            if isinstance(c, Mapping)
        ],
        gear=[str(x) for x in (payload.get("gear") or [])],
        body=str(payload.get("body", "original_biological")),
        cortical_stack=bool(payload.get("cortical_stack", False)),
        resleeved=bool(payload.get("resleeved", False)),
        natural_psi=bool(payload.get("natural_psi", False)),
        psi_abilities=[str(x) for x in (payload.get("psi_abilities") or [])],
        statuses=[str(x) for x in (payload.get("statuses") or [])],
        tags=tuple(
            Tag(str(item.get("kind", "")), str(item.get("value", "")))
            for item in (payload.get("tags") or [])
            if isinstance(item, Mapping)
        ),
    )


# -- file save/load -----------------------------------------------------------------

def save_campaign(campaign: Campaign, path: str | Path) -> None:
    """Write the campaign snapshot. The format is :meth:`Campaign.to_dict`."""
    Path(path).write_text(campaign.to_json(), encoding="utf-8")


def load_campaign(path: str | Path) -> Campaign:
    """Read a snapshot written by :func:`save_campaign`.

    ``campaign_from_dict`` refuses a foreign ``schema_version``, so a snapshot from a
    different shape never loads as this one's data.
    """
    text = Path(path).read_text(encoding="utf-8")
    return campaign_from_dict(json.loads(text))