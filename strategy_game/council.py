"""The council, portfolio, mission and relationship layer of the strategy game (#323).

Issue #323 asks for four leader characters per faction, at most one leader-led active mission each per
turn, one persistent management portfolio per leader, and relationships that change strategy state
rather than only dialogue. The written specification is ``docs/LEADER_COUNCIL_SYSTEM.md`` (stage A,
landed); this module implements its **structure** and nothing else.

Two layers, and the difference between them is the whole discipline of this file:

* :meth:`CouncilModel.structural_problems` carries the checks **the issue itself states as acceptance
  criteria** — a mission with no leader is invalid, one leader cannot lead two missions in a turn, a
  faction cannot declare more moves than it has leader-turns, a mission has to name which of the six
  quantities it is trying to move, and the four posts are distinct. These are refusals, because the
  issue makes them requirements.
* :meth:`CouncilModel.consequence_reports` carries everything whose *effect* is still unauthored — the
  DRAFT status table's no-mission rows, the magnitude of a portfolio's passive, the effect of a council
  refusal, the price of a declared resource. These are **reports, never refusals**, because refusing on
  a DRAFT rule would be implementing an unapproved rule. A report names the row or the field it comes
  from so a reviewer can check it against the specification.

Nothing in this module resolves anything. No mission is rolled, no outcome is written, no quantity is
moved, no magnitude is computed, no turn advances, and no win condition exists: gate A (leader RPG) and
gate C (strategy) in ``docs/RULE_SYSTEM_RESEARCH.md`` are open, and ``AGENTS.md`` §4 reserves
resolution, thresholds and cadence to the author. ``MissionDeclaration.outcome`` is an uninterpreted
field that nothing here sets.

Why the council is an argument rather than decoration, structurally: ``docs/design/NOOPUNK_GLOBAL.md``
§7 says the six quantities are non-identical, and the four-move cap says a faction cannot pursue all of
its priorities in a turn. :meth:`CouncilModel.unpursued_quantities` therefore always leaves something
out, and :meth:`CouncilModel.shared_interest_report` shows whether the four offices even disagree. That
is set membership over names — no weight, no score, no priority ordering is computed anywhere.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .provenance import Provenance
from .quantities import QUANTITY_IDS, unknown_quantities
from .relationships import RelationshipEdge, RelationshipSet

__all__ = [
    "CHANNEL_APPLIES",
    "COUNCIL_FORMAT",
    "DATA_PATH",
    "LEADER_STATUSES",
    "PORTFOLIO_IDS",
    "Council",
    "CouncilError",
    "CouncilLeader",
    "CouncilModel",
    "MissionCost",
    "MissionDeclaration",
    "PassiveEffect",
    "Portfolio",
    "StatusRow",
    "StrategicChannel",
    "council_from_dict",
    "load_council",
]

#: The declared file format, so a caller cannot silently load a different document.
COUNCIL_FORMAT = "noopunk.strategy_game.council"

#: The packaged vocabulary.
DATA_PATH = Path(__file__).with_name("data") / "council.json"

#: The four offices ``docs/LEADER_COUNCIL_SYSTEM.md`` §2 names. DRAFT names: the ids are that
#: document's, transcribed, and no office is approved.
PORTFOLIO_IDS: tuple[str, ...] = (
    "politics_diplomacy",
    "organisation_networks",
    "operations_resources",
    "research_intelligence",
)

#: The statuses §4 lists. What each one *does* is DRAFT and is reported, not enforced.
LEADER_STATUSES: tuple[str, ...] = (
    "busy",
    "injured",
    "unavailable",
    "compromised",
    "exhausted",
    "absent",
)

#: How a strategic channel attaches to a tie: by its tags, or to every tie there is.
CHANNEL_APPLIES: tuple[str, ...] = ("tag_conditional", "every_tie")


class CouncilError(ValueError):
    """Raised for a malformed council record."""


def _strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def _records(value: Any) -> tuple[dict[str, Any], ...]:
    if value is None:
        return ()
    if isinstance(value, dict):
        return (dict(value),)
    return tuple(dict(item) for item in value if isinstance(item, Mapping))


@dataclass
class PassiveEffect:
    """What an office's passive touches. The **quantity** is named; the size is not approved."""

    quantity: str = ""
    magnitude_declared: bool = False
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "quantity": self.quantity,
            "magnitude_declared": self.magnitude_declared,
            "reason": self.reason,
        }


@dataclass
class Portfolio:
    """One office: what it decides, which quantities it serves, and what its holder argues for."""

    identifier: str
    label: str = ""
    decides: str = ""
    serves: tuple[str, ...] = ()
    primary: str = ""
    standing_position: str = ""
    argues_for: str = ""
    quantity_note: str = ""
    passive: PassiveEffect = field(default_factory=PassiveEffect)
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "decides": self.decides,
            "serves": list(self.serves),
            "primary": self.primary,
            "standing_position": self.standing_position,
            "argues_for": self.argues_for,
            "quantity_note": self.quantity_note,
            "passive": self.passive.to_dict(),
        }
        payload.update(self.detail)
        return payload


@dataclass
class MissionCost:
    """One declared cost of a mission: a name and a note, never a price."""

    identifier: str
    label: str = ""
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.identifier, "label": self.label, "note": self.note}


@dataclass
class StatusRow:
    """One row of §4's DRAFT status table, kept so a consequence can cite it."""

    status: str
    mission: str = ""
    portfolio: str = ""
    note: str = ""

    def allows_a_mission(self) -> bool:
        """Whether the row's own DRAFT wording permits a mission. Not a rule: cited, not applied."""
        return self.mission.strip().lower().startswith("yes")


@dataclass
class StrategicChannel:
    """One declared way a personal tie reaches the strategic layer."""

    identifier: str
    label: str = ""
    applies: str = "every_tie"
    opened_by: tuple[str, ...] = ()
    closed_by: tuple[str, ...] = ()
    carries: tuple[str, ...] = ()
    note: str = ""
    enforced: bool = False
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier,
            "label": self.label,
            "applies": self.applies,
            "opened_by": list(self.opened_by),
            "closed_by": list(self.closed_by),
            "carries": list(self.carries),
            "note": self.note,
            "enforced": self.enforced,
            "reason": self.reason,
        }


@dataclass
class CouncilLeader:
    """A named leader with one office and a declared status. No attribute is named anywhere."""

    identifier: str
    name: str = ""
    portfolio: str = ""
    status: str = ""
    location_id: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "name": self.name,
            "portfolio": self.portfolio,
            "status": self.status,
            "location_id": self.location_id,
        }
        payload.update(self.detail)
        return payload


@dataclass
class MissionDeclaration:
    """One declared active move. A declaration is not an outcome: nothing here resolves or writes one."""

    identifier: str
    leader_id: str = ""
    kind: str = ""
    target_id: str = ""
    location_id: str = ""
    #: WHICH of the six quantities the move tries to move. The field that stops it being a generic roll.
    quantity: str = ""
    authorised_by: str = ""
    allocated_resource_ids: tuple[str, ...] = ()
    patron_edge_id: str = ""
    refusals: tuple[str, ...] = ()
    #: Uninterpreted. Nothing in this package produces an outcome, so it stays empty.
    outcome: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "leader_id": self.leader_id,
            "kind": self.kind,
            "target_id": self.target_id,
            "location_id": self.location_id,
            "quantity": self.quantity,
            "authorised_by": self.authorised_by,
            "allocated_resource_ids": list(self.allocated_resource_ids),
            "patron_edge_id": self.patron_edge_id,
            "refusals": list(self.refusals),
            "outcome": self.outcome,
        }
        payload.update(self.detail)
        return payload


@dataclass
class Council:
    """A faction's four offices and the turn's declared moves."""

    identifier: str
    principal_id: str = ""
    leaders: tuple[CouncilLeader, ...] = ()
    missions: tuple[MissionDeclaration, ...] = ()
    note: str = ""

    def leader(self, identifier: str) -> CouncilLeader | None:
        for leader in self.leaders:
            if leader.identifier == identifier:
                return leader
        return None

    def portfolio_of(self, leader_id: str) -> str:
        leader = self.leader(leader_id)
        return leader.portfolio if leader is not None else ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier,
            "principal_id": self.principal_id,
            "leaders": [leader.to_dict() for leader in self.leaders],
            "missions": [mission.to_dict() for mission in self.missions],
            "note": self.note,
        }


def council_from_dict(data: Mapping[str, Any]) -> Council:
    """Build a council from a record. ``leaders`` and ``missions`` are lists of mappings."""
    if not isinstance(data, Mapping) or not data.get("id"):
        raise CouncilError("a council needs an 'id'")
    known_leader_keys = {"id", "name", "portfolio", "status", "location_id"}
    known_mission_keys = {
        "id", "leader_id", "kind", "target_id", "location_id", "quantity", "authorised_by",
        "allocated_resource_ids", "patron_edge_id", "refusals", "outcome",
    }
    leaders = tuple(
        CouncilLeader(
            identifier=str(item["id"]),
            name=str(item.get("name") or ""),
            portfolio=str(item.get("portfolio") or ""),
            status=str(item.get("status") or ""),
            location_id=str(item.get("location_id") or ""),
            detail={k: v for k, v in item.items() if k not in known_leader_keys},
        )
        for item in _records(data.get("leaders"))
        if item.get("id")
    )
    missions = tuple(
        MissionDeclaration(
            identifier=str(item["id"]),
            leader_id=str(item.get("leader_id") or ""),
            kind=str(item.get("kind") or ""),
            target_id=str(item.get("target_id") or ""),
            location_id=str(item.get("location_id") or ""),
            quantity=str(item.get("quantity") or ""),
            authorised_by=str(item.get("authorised_by") or ""),
            allocated_resource_ids=_strings(item.get("allocated_resource_ids")),
            patron_edge_id=str(item.get("patron_edge_id") or ""),
            refusals=_strings(item.get("refusals")),
            outcome=str(item.get("outcome") or ""),
            detail={k: v for k, v in item.items() if k not in known_mission_keys},
        )
        for item in _records(data.get("missions"))
        if item.get("id")
    )
    return Council(
        identifier=str(data["id"]),
        principal_id=str(data.get("principal_id") or ""),
        leaders=leaders,
        missions=missions,
        note=str(data.get("note") or ""),
    )


@dataclass
class CouncilModel:
    """The loaded council vocabulary, plus the two validators and the structural reports."""

    portfolios: dict[str, Portfolio] = field(default_factory=dict)
    portfolio_order: tuple[str, ...] = ()
    council_size: int = 0
    council_size_record: dict[str, Any] = field(default_factory=dict)
    central_rule: dict[str, Any] = field(default_factory=dict)
    mission: dict[str, Any] = field(default_factory=dict)
    costs: tuple[MissionCost, ...] = ()
    status_rows: tuple[StatusRow, ...] = ()
    status_record: dict[str, Any] = field(default_factory=dict)
    channels: tuple[StrategicChannel, ...] = ()
    disagreement: dict[str, Any] = field(default_factory=dict)
    worked_example: dict[str, Any] = field(default_factory=dict)
    cautions: tuple[dict[str, Any], ...] = ()
    pending_author_decisions: tuple[dict[str, Any], ...] = ()
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    detail: dict[str, Any] = field(default_factory=dict)

    # -- lookups ---------------------------------------------------------------------------

    def portfolio(self, identifier: str) -> Portfolio:
        return self.portfolios[identifier]

    def channel(self, identifier: str) -> StrategicChannel:
        return next(item for item in self.channels if item.identifier == identifier)

    def cost(self, identifier: str) -> MissionCost:
        return next(item for item in self.costs if item.identifier == identifier)

    def status_row(self, status: str) -> StatusRow | None:
        for row in self.status_rows:
            if row.status == status:
                return row
        return None

    def worked_example_council(self) -> Council:
        """The shipped illustrative turn as a :class:`Council`, so the example is exercised as data."""
        record = dict(self.worked_example)
        return council_from_dict(
            {
                "id": str(record.get("id") or "worked_example"),
                "principal_id": str(record.get("principal_id") or ""),
                "leaders": record.get("leaders") or [],
                "missions": record.get("missions") or [],
                "note": str(record.get("note") or ""),
            }
        )

    # -- structural validation: what the issue itself requires -----------------------------

    def structural_problems(
        self,
        council: Council,
        *,
        edges: RelationshipSet | None = None,
    ) -> tuple[str, ...]:
        """The issue's own requirements, refused by name. An empty tuple means the declaration is legal.

        These are the checks issue #323 states as acceptance criteria, and only those: a mission names
        exactly one leader, one leader leads at most one move per turn, the faction declares no more
        moves than it has leader-turns, a move names one of the six quantities, the four posts are
        distinct, and a mission that draws on a patron names an edge that exists.
        """
        problems: list[str] = []
        if len(self.portfolios) != len(PORTFOLIO_IDS):
            problems.append(
                f"the vocabulary declares {len(self.portfolios)} offices; issue #323's council is four"
            )
        # A repeated identifier is not an additional character/action slot. A mission
        # lookup would otherwise silently resolve to the first matching record.
        seen_leader_ids: set[str] = set()
        held: dict[str, str] = {}
        for leader in council.leaders:
            if not leader.identifier.strip():
                problems.append("council leader has no identifier")
            elif leader.identifier in seen_leader_ids:
                problems.append(
                    f"leader identifier {leader.identifier!r} appears more than once in the roster"
                )
            seen_leader_ids.add(leader.identifier)
            if leader.status and leader.status not in LEADER_STATUSES:
                problems.append(
                    f"leader {leader.identifier}: status {leader.status!r} is not one of "
                    f"{LEADER_STATUSES}"
                )
            if not leader.portfolio:
                continue
            if leader.portfolio not in self.portfolios:
                problems.append(
                    f"leader {leader.identifier}: portfolio {leader.portfolio!r} is not one of the "
                    f"four offices {PORTFOLIO_IDS}"
                )
                continue
            if leader.portfolio in held:
                problems.append(
                    f"portfolio {leader.portfolio!r} is held by both {held[leader.portfolio]!r} and "
                    f"{leader.identifier!r}; a leader holds at most one portfolio and the four posts "
                    "are distinct"
                )
            held[leader.portfolio] = leader.identifier

        per_leader: dict[str, int] = {}
        seen_mission_ids: set[str] = set()
        for mission in council.missions:
            head = f"mission {mission.identifier}"
            if not mission.identifier.strip():
                problems.append("mission has no identifier")
            elif mission.identifier in seen_mission_ids:
                problems.append(f"{head}: identifier appears more than once in this turn")
            seen_mission_ids.add(mission.identifier)
            if not mission.location_id.strip():
                problems.append(f"{head}: no location; each active mission must name a location")
            if not mission.leader_id.strip():
                problems.append(
                    f"{head}: no leader. Issue #323's central rule is that every active faction move "
                    "has exactly one named leader responsible for carrying it out, so a leaderless "
                    "mission is invalid rather than merely weaker"
                )
            else:
                if council.leader(mission.leader_id) is None:
                    problems.append(
                        f"{head}: leader {mission.leader_id!r} is not in this faction's roster"
                    )
                per_leader[mission.leader_id] = per_leader.get(mission.leader_id, 0) + 1
            if not mission.quantity.strip():
                problems.append(
                    f"{head}: names no quantity. A move must state WHICH of the six quantities it "
                    "tries to move, which is what stops it being a generic success roll"
                )
            elif mission.quantity not in QUANTITY_IDS:
                problems.append(
                    f"{head}: quantity {mission.quantity!r} is not one of the six {QUANTITY_IDS}"
                )
            if not mission.target_id.strip():
                problems.append(f"{head}: no target; a mission needs a valid target to be legal")
            if not mission.authorised_by.strip():
                problems.append(
                    f"{head}: nobody authorised it. A mission is assigned by the faction leader, so "
                    "an unauthorised declaration is not a declaration"
                )
            if mission.patron_edge_id and edges is not None:
                known = {edge.identifier for edge in edges if edge.role == "patron"}
                if mission.patron_edge_id not in known:
                    problems.append(
                        f"{head}: patron edge {mission.patron_edge_id!r} is not a patron edge in the "
                        "relationship set; issue #346 step 4 makes patron resources a negotiated "
                        "access, so the edge has to exist"
                    )
        for leader_id, count in sorted(per_leader.items()):
            if count > 1:
                problems.append(
                    f"leader {leader_id!r} leads {count} missions; at most one active mission per "
                    "leader per turn"
                )
        if len(council.missions) > self.council_size:
            problems.append(
                f"{len(council.missions)} missions declared against {self.council_size} leader-turns: "
                "members and resources amplify a leader-led mission and never add one"
            )
        return tuple(problems)

    # -- reports: what the author has not ruled on -----------------------------------------

    def consequence_reports(
        self,
        council: Council,
        *,
        edges: RelationshipSet | None = None,
    ) -> tuple[str, ...]:
        """Everything whose *effect* is unauthored, reported with its source. Never a refusal.

        Refusing on one of these would be implementing a DRAFT rule: the status table is marked DRAFT
        with three TODOs, a portfolio's passive magnitude is unapproved, the effect of a refusal is
        decision D6, and a declared resource has no price.
        """
        reports: list[str] = []
        if len(council.leaders) != self.council_size:
            reports.append(
                f"the roster holds {len(council.leaders)} leaders against {self.council_size} slots. "
                "Issue #323 says a faction has four leaders; issue #346 says the four-slot limit "
                "counts characters ASSIGNED to field actions rather than all managers. Reported, not "
                "refused: the two wordings are the author's to reconcile."
            )
        unstaffed = tuple(pid for pid in PORTFOLIO_IDS if pid not in {
            leader.portfolio for leader in council.leaders
        })
        if unstaffed:
            reports.append(
                f"{len(unstaffed)} office(s) unstaffed: {list(unstaffed)}. An empty portfolio grants "
                "no bonus and no penalty, but nobody holds that interest at the table."
            )
        for mission in council.missions:
            head = f"mission {mission.identifier}"
            leader = council.leader(mission.leader_id)
            row = self.status_row(leader.status) if leader is not None else None
            if row is not None and not row.allows_a_mission():
                reports.append(
                    f"{head}: its leader's status is {row.status!r}, which the DRAFT status table in "
                    "docs/LEADER_COUNCIL_SYSTEM.md section 4 marks as no mission. Recovery timing, "
                    "the compromised reduction and exposure risk are TODO: requires author "
                    "specification, so this is reported rather than refused."
                )
            if mission.refusals:
                reports.append(
                    f"{head}: contested by {list(mission.refusals)}. A portfolio holder may contest a "
                    "mission that cuts against their office's quantity; whether that refusal is a "
                    "status or an authored choice is decision D6 in "
                    "docs/LEADER_MICRO_RULES_PROPOSAL.md, unauthored. The slot is described, the rule "
                    "is not made."
                )
            if mission.allocated_resource_ids:
                reports.append(
                    f"{head}: draws on {list(mission.allocated_resource_ids)}. Named, not priced: what "
                    "a resource contributes to a mission is a rule."
                )
            if mission.patron_edge_id:
                reports.append(
                    f"{head}: draws on patron edge {mission.patron_edge_id!r}, which is a dependence "
                    "debt rather than a free resource. Issue #346 step 4: patron resources are not "
                    "automatically faction property."
                )
            if council.principal_id and mission.authorised_by and mission.authorised_by != council.principal_id:
                reports.append(
                    f"{head}: authorised by {mission.authorised_by!r} rather than the principal "
                    f"{council.principal_id!r}. Whether the council may authorise without the "
                    "principal is not decided here."
                )
            if edges is not None:
                tie = edges.between(mission.leader_id, mission.target_id)
                if not tie:
                    reports.append(
                        f"{head}: target {mission.target_id!r} has no authored tie to its leader. "
                        "This is UNMODELLED, not a neutral-zero relationship: the record is sparse, so "
                        "nothing may be read from the absence."
                    )
                else:
                    for channel in self.channels_for(tie[0]):
                        reports.append(
                            f"{head}: the tie to {mission.target_id!r} opens the declared channel "
                            f"{channel.identifier!r} ({channel.label}). Declared only: "
                            "enforced=false, so nothing is granted."
                        )
            if mission.outcome:
                reports.append(
                    f"{head}: carries an outcome {mission.outcome!r}. Nothing in this package writes "
                    "one; gate A and gate C are open."
                )
            if mission.quantity and mission.quantity in QUANTITY_IDS:
                attempted, others = self.failure_shape(mission.quantity)
                if others:
                    reports.append(
                        f"{head}: if it fails, quantity {attempted!r} does not move and a different "
                        f"quantity ({list(others)}) moves the wrong way. A failure that moved nothing "
                        "would be the empty turn the playtest checklist rules out; WHICH quantity "
                        "moves wrong is a rule and is declared false."
                    )
        for portfolio in self.portfolios.values():
            if not portfolio.passive.magnitude_declared:
                reports.append(
                    f"office {portfolio.identifier}: its passive touches "
                    f"{portfolio.passive.quantity!r} and its magnitude is unapproved. "
                    f"{portfolio.passive.reason}"
                )
        return tuple(reports)

    # -- reporting: the two structural readings --------------------------------------------

    def shared_interest_report(self, council: Council | None = None) -> dict[str, Any]:
        """Which quantities more than one office serves as its primary, and which none serves.

        Set membership over names. No weight, no priority and no score is computed: the point is only
        whether the four offices *can* disagree, which the six-quantity rule requires them to be able
        to do.
        """
        primaries = [portfolio.primary for portfolio in self.portfolios.values() if portfolio.primary]
        counts: dict[str, int] = {}
        for name in primaries:
            counts[name] = counts.get(name, 0) + 1
        shared = {name: count for name, count in counts.items() if count > 1}
        served = {name for portfolio in self.portfolios.values() for name in portfolio.serves}
        served_primaries = {name for name in primaries if name in QUANTITY_IDS}
        return {
            "primaries": sorted(primaries),
            "distinct_primaries": sorted(set(primaries)),
            "shared_primaries": shared,
            "unclaimed_quantities": [name for name in QUANTITY_IDS if name not in served],
            "all_four_serve_one_quantity": len(set(primaries)) == 1 and len(primaries) == len(
                self.portfolios
            ),
            "unpursued_quantities": self.unpursued_quantities(council) if council is not None else list(
                QUANTITY_IDS
            ),
            "served_by_any_office": sorted(served),
            "served_primary_quantities": sorted(served_primaries),
        }

    def unpursued_quantities(self, council: Council) -> tuple[str, ...]:
        """The six minus the quantities this turn's declared missions name, in §7's order.

        With four leader-turns against six non-identical quantities, this is never empty — which is
        what the council is arguing about. It is a list of names, not a count of points.
        """
        named = {mission.quantity for mission in council.missions}
        return tuple(name for name in QUANTITY_IDS if name not in named)

    def unclaimed_quantities(self, council: Council | None = None) -> tuple[str, ...]:
        """Quantities no office's declared interests touch at all."""
        served = {name for portfolio in self.portfolios.values() for name in portfolio.serves}
        return tuple(name for name in QUANTITY_IDS if name not in served)

    def failure_shape(self, attempted: str) -> tuple[str, tuple[str, ...]]:
        """The declared failure shape for an attempted quantity: what does *not* move, and what does.

        Read from the declared ``mission.failure_is_not_nothing`` container. Nothing here applies it.
        """
        record = (self.mission.get("failure_is_not_nothing") or {}).get("examples") or []
        for example in record:
            if example.get("attempted") == attempted:
                return str(attempted), _strings(example.get("moves_wrong_way"))
        return str(attempted), ()

    # -- the relationship channel -----------------------------------------------------------

    def channels_for(self, edge: RelationshipEdge) -> tuple[StrategicChannel, ...]:
        """The declared channels this edge reaches, by its tags.

        A ``tag_conditional`` channel opens on the tags it declares and closes on the ones it names as
        closing — so a ``mentor`` tie reaches the channel that gates legality and cost and a
        ``suspicious`` one reaches it from the other side. An ``every_tie`` channel holds for having a
        tie at all. ``enforced`` is false on every channel, so this lookup grants nothing.
        """
        out = []
        for channel in self.channels:
            if channel.applies == "every_tie":
                out.append(channel)
                continue
            if set(edge.tags) & (set(channel.opened_by) | set(channel.closed_by)):
                out.append(channel)
        return tuple(out)

    def strategic_consequences(
        self, mission: MissionDeclaration, edges: RelationshipSet
    ) -> dict[str, Any]:
        """What the relationship record has to say about a declared mission. Nothing is computed but a lookup.

        Returns the target's authored tie (or nothing, and says so as *unmodelled* rather than zero), the
        channels that tie opens, and — for a mission that draws on a patron — the stance the patron's own
        goal takes toward the mission's quantity.
        """
        tie = edges.between(mission.leader_id, mission.target_id)
        payload: dict[str, Any] = {
            "mission": mission.identifier,
            "quantity": mission.quantity,
            "target_modelled": bool(tie),
            "edge_ids": [edge.identifier for edge in tie],
            "channels": [channel.identifier for channel in self.channels_for(tie[0])] if tie else [],
            "enforced": False,
            "note": (
                "the tie is read, and nothing is applied: no modifier, no threshold and no outcome "
                "exists here. An empty edge list means the tie is UNMODELLED, not zero."
            ),
        }
        if mission.patron_edge_id:
            patron = next((edge for edge in edges if edge.identifier == mission.patron_edge_id), None)
            payload["patron_goal_diverges"] = bool(
                patron is not None and mission.quantity not in ("",) and patron.state == "divergent"
            )
            payload["patron_state"] = patron.state if patron is not None else ""
        return payload

    # -- rival parity -----------------------------------------------------------------------

    def validate_all(self, councils: Iterable[Council], **kwargs: Any) -> dict[str, tuple[str, ...]]:
        """Validate every faction's council with the same function and the same cap.

        Rival and player factions are not special-cased anywhere in this module: an AI faction cannot
        bank an unused mission, gain a free action from its members, or hold a fifth office.
        """
        return {council.identifier: self.structural_problems(council, **kwargs) for council in councils}

    # -- registries ------------------------------------------------------------------------

    def pending_decisions(self) -> tuple[dict[str, Any], ...]:
        """Every decision left to the author, with the reason it is open."""
        return tuple(self.pending_author_decisions)

    def unreasoned_decisions(self) -> tuple[str, ...]:
        """Pending decisions whose ``why_not_decided`` is empty — a container pretending to be an answer."""
        return tuple(
            str(item.get("id") or "?")
            for item in self.pending_decisions()
            if not str(item.get("why_not_decided") or "").strip()
        )

    def off_vocabulary(self) -> tuple[tuple[str, str, str], ...]:
        """``(record_id, field, value)`` for values outside the declared vocabularies, without raising."""
        out: list[tuple[str, str, str]] = []
        for portfolio in self.portfolios.values():
            if portfolio.identifier not in PORTFOLIO_IDS:
                out.append((portfolio.identifier, "portfolio", portfolio.identifier))
            out.extend(
                (portfolio.identifier, "serves", name)
                for name in unknown_quantities(portfolio.serves)
            )
            if portfolio.primary and portfolio.primary not in QUANTITY_IDS:
                out.append((portfolio.identifier, "primary", portfolio.primary))
            if portfolio.passive.quantity and portfolio.passive.quantity not in QUANTITY_IDS:
                out.append((portfolio.identifier, "passive.quantity", portfolio.passive.quantity))
        for row in self.status_rows:
            if row.status not in LEADER_STATUSES:
                out.append((row.status, "status", row.status))
        for channel in self.channels:
            if channel.applies not in CHANNEL_APPLIES:
                out.append((channel.identifier, "applies", channel.applies))
            out.extend(
                (channel.identifier, "carries", name)
                for name in unknown_quantities(channel.carries)
            )
        return tuple(out)


def council_model_from_dict(data: Mapping[str, Any]) -> CouncilModel:
    """Build the model from the packaged document shape."""
    portfolios: dict[str, Portfolio] = {}
    order: list[str] = []
    for record in _records(data.get("portfolios")):
        passive = record.get("passive") or {}
        portfolio = Portfolio(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            decides=str(record.get("decides") or ""),
            serves=_strings(record.get("serves")),
            primary=str(record.get("primary") or ""),
            standing_position=str(record.get("standing_position") or ""),
            argues_for=str(record.get("argues_for") or ""),
            quantity_note=str(record.get("quantity_note") or ""),
            passive=PassiveEffect(
                quantity=str(passive.get("quantity") or ""),
                magnitude_declared=bool(passive.get("magnitude_declared", False)),
                reason=str(passive.get("reason") or ""),
            ),
            detail={
                key: value
                for key, value in record.items()
                if key not in {
                    "id", "label", "decides", "serves", "primary", "standing_position", "argues_for",
                    "quantity_note", "passive",
                }
            },
        )
        portfolios[portfolio.identifier] = portfolio
        order.append(portfolio.identifier)

    mission = dict(data.get("mission") or {})
    costs = tuple(
        MissionCost(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            note=str(record.get("note") or ""),
        )
        for record in _records(mission.get("costs"))
    )
    status_record = dict(data.get("status_consequences") or {})
    rows = tuple(
        StatusRow(
            status=str(record.get("status") or ""),
            mission=str(record.get("mission") or ""),
            portfolio=str(record.get("portfolio") or ""),
            note=str(record.get("note") or ""),
        )
        for record in _records(status_record.get("rows"))
    )
    channels = tuple(
        StrategicChannel(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            applies=str(record.get("applies") or "every_tie"),
            opened_by=_strings(record.get("opened_by")),
            closed_by=_strings(record.get("closed_by")),
            carries=_strings(record.get("carries")),
            note=str(record.get("note") or ""),
            enforced=bool(record.get("enforced", False)),
            reason=str(record.get("reason") or ""),
        )
        for record in _records(data.get("strategic_channels"))
    )
    size_record = dict(data.get("council_size") or {})
    return CouncilModel(
        portfolios=portfolios,
        portfolio_order=tuple(order),
        council_size=int(size_record.get("value") or 0),
        council_size_record=size_record,
        central_rule=dict(data.get("central_rule") or {}),
        mission=mission,
        costs=costs,
        status_rows=rows,
        status_record=status_record,
        channels=channels,
        disagreement=dict(data.get("structural_disagreement") or {}),
        worked_example=dict(data.get("worked_example") or {}),
        cautions=_records(data.get("cautions")),
        pending_author_decisions=_records(data.get("pending_author_decisions")),
        sources=_strings(data.get("sources")),
        provenance=Provenance.from_dict(data.get("provenance")),
        detail={
            key: value
            for key, value in data.items()
            if key
            not in {
                "format", "status", "sources", "provenance", "consumes", "council_size",
                "central_rule", "portfolios", "structural_disagreement", "mission",
                "status_consequences", "strategic_channels", "worked_example", "cautions",
                "pending_author_decisions",
            }
        },
    )


def load_council(path: Path | str | None = None) -> CouncilModel:
    """Load the packaged council vocabulary, refusing a document that is not one."""
    target = Path(path) if path is not None else DATA_PATH
    with open(target, encoding="utf-8") as handle:
        data = json.load(handle)
    declared = data.get("format")
    if declared is not None and declared != COUNCIL_FORMAT:
        raise ValueError(f"not a NoöPunk council document: format={declared!r}")
    return council_model_from_dict(data)
