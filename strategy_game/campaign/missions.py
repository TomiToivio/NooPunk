"""Mission results update the same world state, via one tested interface (#502 Phase 1).

Phase 1 acceptance criterion 4 is: *"Mission results update faction/world state via
tested interfaces."* The mission **concept** already exists in this repo as the
council's declared move (``strategy_game.council.MissionDeclaration``, #323), whose
``outcome`` field is deliberately uninterpreted because nothing there resolves.
This module supplies the missing half for Phase 1 and nothing more:

* ``MissionOutcome`` records what a resolved mission **reports** — the outcome
  vocabulary is the **approved** ``strategy_game.rpg.fate.Outcome`` ladder
  (failure / tie / success / success_with_style), so no second result scale is
  invented here, and no success threshold is either (the difficulty is a check-time
  input; see ``rpg.turn.TurnOutcome``).
* ``apply_mission_outcome`` is the **one** function that writes a result onto
  faction world state — books move by membership, appending/removing ids and labels;
  no magnitude is computed anywhere. This satisfies Phase 1's "minimal faction state
  under the hood" for the slice where a leader-led mission over ``unsa_case_template``
  vocabulary cases resolves. There is deliberately **no other writer of these books**
  in this package, so the interface is testable as *the* interface.

* **Unapproved vocabulary is refused.** An unknown outcome name raises rather than
  entering state — the same refusal discipline ``rpg.skills.validate_skill`` applies
  to skill names, and the reason a caller cannot pass free text past the writer.

What is deliberately absent (Phase 2/3): no mission board or generation, no
assignment loop (``rpg.roster.TurnLedger`` already owns one-action-per-turn
structure), no mission clock, no resource costs, no combat, and no political or
hegemony effect. The outcome moves **inventories and labels only** — exactly what
Phase 1 can produce — and never a quantity, because none is approved.

The books a result may move (and only these)
--------------------------------------------
=============================== =============================================
faction book                      Phase-1 meaning (author's words in #502)
=============================== =============================================
``objectives``                  completed objective labels
``intelligence_ids``            intel records the mission surfaced
``resources``                   resource inventories gained or spent
``reputation_labels``           named reputation labels gained
=============================== =============================================
Everything else — support, legitimacy, seats, networks, discourse — is Phase 2/3
political simulation and is not touched.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from ..provenance import Provenance, ProvenanceKind
from ..rpg.fate import Outcome
from .case import Case
from .state import AGENT_CAPACITY, Campaign, CampaignError

__all__ = [
    "MISSION_REPORT_FIELDS",
    "MISSION_REPORT_SCHEMA_VERSION",
    "MissionError",
    "MissionOutcome",
    "apply_mission_outcome",
]

#: Version of the outcome payload shape, carried in the record and in the campaign's
#: ``campaign_notes`` audit trail so a later save always tells the reader which write
#: produced each note (the versioned-growth rule, applied at write time).
MISSION_REPORT_SCHEMA_VERSION = "mission-report-1"

#: The fields a mission report carries. Declared so the payload cannot widen quietly:
#: no narrative free-text field exists to smuggle a result through.
MISSION_REPORT_FIELDS: tuple[str, ...] = (
    "schema_version", "mission_id", "case_id", "outcome", "leader_id", "agent_ids",
    "evidence_gained", "intel_gained", "resources_gained", "resources_spent",
    "reputation_labels_gained", "objectives_completed", "seed",
)


class MissionError(CampaignError):
    """A mission-outcome operation the Phase-1 schema does not allow."""


def _ids(values: Any, field_name: str) -> tuple[str, ...]:
    seen: list[str] = []
    for item in values if isinstance(values, (list, tuple)) else ():
        text = str(item).strip()
        if not text:
            raise MissionError(f"{field_name} carries an empty id")
        if text in seen:
            raise MissionError(f"{field_name}: duplicate id {text!r}")
        seen.append(text)
    return tuple(seen)


@dataclass(frozen=True)
class MissionOutcome:
    """One resolved mission, as plain data — a *report*, not a mechanic.

    ``outcome`` is an :class:`~strategy_game.rpg.fate.Outcome`: the approved ladder,
    reused. Every ``*_gained`` field is an **inventory transition** (ids to add or
    remove), never a magnitude — there is no ``+2 reputation`` here because no
    numeric reputation scale exists. ``leader_id`` and ``agent_ids`` are the roster
    the mission was played through (the PC leader and its agents, #502);
    ``leader_id`` is required because the faction leader from day one is the PC.
    """

    mission_id: str
    case_id: str
    #: The approved Fate outcome this resolution landed on.
    outcome: Outcome
    leader_id: str
    #: Inventory transitions. Empty lists are honest "nothing changed" reports.
    evidence_gained: tuple[str, ...] = ()
    intel_gained: tuple[str, ...] = ()
    resources_gained: tuple[str, ...] = ()
    resources_spent: tuple[str, ...] = ()
    reputation_labels_gained: tuple[str, ...] = ()
    objectives_completed: tuple[str, ...] = ()
    #: The agents who took part, distinct from the leader; at most the approved four.
    #: (The roster *structure* is approved in #461/#482; capacity is checked here so
    #: the campaign books cannot silently widen it.)
    agent_ids: tuple[str, ...] = ()
    #: Seed of the Fate resolution, for replayability of the reported result. The
    #: roll itself lives in the Fate layer and in ``turn.py``'s outcome history; the
    #: outcome record only names it.
    seed: int | None = None

    def __post_init__(self) -> None:
        if not str(self.mission_id).strip():
            raise MissionError("an outcome names its mission")
        if not str(self.case_id).strip():
            raise MissionError("an outcome names the case it resolved")
        if not isinstance(self.outcome, Outcome):
            raise MissionError(
                "outcome must be a strategy_game.rpg.fate.Outcome (the approved ladder); "
                f"got {type(self.outcome).__name__}"
            )
        if not str(self.leader_id).strip():
            raise MissionError("a mission outcome names its leader (the PC faction leader)")
        if len({self.leader_id, *self.agent_ids}) != 1 + len(self.agent_ids):
            raise MissionError("the leader and the agents must be distinct people")
        if len(self.agent_ids) > AGENT_CAPACITY:
            raise MissionError(
                f"a mission is played through at most {AGENT_CAPACITY} agents (#461/#482), "
                f"got {len(self.agent_ids)}"
            )
        for name, values in (
            ("evidence_gained", self.evidence_gained),
            ("intel_gained", self.intel_gained),
            ("resources_gained", self.resources_gained),
            ("resources_spent", self.resources_spent),
            ("reputation_labels_gained", self.reputation_labels_gained),
            ("objectives_completed", self.objectives_completed),
        ):
            _ids(values, name)
        for gained, spent in zip(self.resources_gained, self.resources_spent):
            if gained == spent:
                raise MissionError(
                    f"resource {gained!r} is both gained and spent; split it into two reports"
                )

    # -- serialization -------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": MISSION_REPORT_SCHEMA_VERSION,
            "mission_id": self.mission_id,
            "case_id": self.case_id,
            "outcome": self.outcome.value,
            "leader_id": self.leader_id,
            "agent_ids": list(self.agent_ids),
            "evidence_gained": list(self.evidence_gained),
            "intel_gained": list(self.intel_gained),
            "resources_gained": list(self.resources_gained),
            "resources_spent": list(self.resources_spent),
            "reputation_labels_gained": list(self.reputation_labels_gained),
            "objectives_completed": list(self.objectives_completed),
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "MissionOutcome":
        if not isinstance(data, Mapping):
            raise MissionError(f"an outcome record must be a mapping, got {type(data).__name__}")
        if data.get("schema_version") != MISSION_REPORT_SCHEMA_VERSION:
            raise MissionError(
                f"unsupported mission-report schema_version {data.get('schema_version')!r}; "
                f"expected {MISSION_REPORT_SCHEMA_VERSION!r}"
            )
        try:
            outcome = Outcome(str(data["outcome"]))
        except KeyError as exc:
            raise MissionError("an outcome record names its 'outcome'") from exc
        except ValueError as exc:
            raise MissionError(
                f"outcome {data['outcome']!r} is not one of the approved Fate outcomes"
            ) from exc
        return cls(
            mission_id=str(data.get("mission_id") or ""),
            case_id=str(data.get("case_id") or ""),
            outcome=outcome,
            leader_id=str(data.get("leader_id") or ""),
            agent_ids=tuple(str(x) for x in (data.get("agent_ids") or [])),
            evidence_gained=tuple(str(x) for x in (data.get("evidence_gained") or [])),
            intel_gained=tuple(str(x) for x in (data.get("intel_gained") or [])),
            resources_gained=tuple(str(x) for x in (data.get("resources_gained") or [])),
            resources_spent=tuple(str(x) for x in (data.get("resources_spent") or [])),
            reputation_labels_gained=tuple(
                str(x) for x in (data.get("reputation_labels_gained") or [])
            ),
            objectives_completed=tuple(
                str(x) for x in (data.get("objectives_completed") or [])
            ),
            seed=int(data["seed"]) if data.get("seed") is not None else None,
        )

    def audit_entry(self) -> dict[str, Any]:
        """The provenance-stamped trail note :func:`apply_mission_outcome` writes to state."""
        return {
            "kind": "mission_outcome",
            "schema_version": MISSION_REPORT_SCHEMA_VERSION,
            **self.to_dict_no_schema(),
            "provenance": {
                "kind": ProvenanceKind.SIMULATED.value,
                "source": "strategy_game.campaign.missions.apply_mission_outcome",
                "note": "applied via the one tested campaign interface (issue #502 Phase 1)",
            },
        }

    def to_dict_no_schema(self) -> dict[str, Any]:
        payload = self.to_dict()
        payload.pop("schema_version")
        return payload


def apply_mission_outcome(campaign: Campaign, report: MissionOutcome) -> MissionOutcome:
    """Apply one mission outcome to faction world state and return the applied record.

    The **one tested interface** of Phase 1's criterion 4:

    * identity: the mission's case exists on the campaign; the named leader is the
      campaign's leader; the named agents are the faction's declared members. A
      record that does not fit refuses loudly, leaving state untouched (validate
      *all* transitions before writing anything);
    * the writes are the four Phase-1 books only — objectives, intelligence,
      resources, reputation labels — plus the case's evidence inventory; each is an
      id-level membership change, never arithmetic;
    * idempotent replay: every write is a set-membership update, so re-applying the
      same outcome cannot double-add (the property a replayable audit trail needs);
    * then appends the outcome to ``campaign_notes`` as an audit entry —
      provenance-stamped, verbatim, including the seed.

    Nothing is resolved here. The caller resolves through the approved Fate engine
    (``strategy_game.rpg``) and hands this function the outcome.
    """
    campaign.faction()  # raises CampaignError when the campaign has no playable faction
    case = campaign.cases.get(report.case_id)
    if case is None:
        raise MissionError(f"case {report.case_id!r} is not on this campaign")
    if report.leader_id != campaign.leader_id:
        raise MissionError(
            f"outcome leader {report.leader_id!r} is not the campaign's own leader "
            f"{campaign.leader_id!r}; the PC plays the leader's missions"
        )
    faction = campaign.faction()
    unknown_agents = tuple(
        a for a in report.agent_ids
        if a not in faction.member_ids or a == faction.leader_id
    )
    if unknown_agents:
        raise MissionError(
            f"agents {unknown_agents} are not declared member agents of faction "
            f"{faction.identifier!r}; roster ids bind real members only"
        )

    # All validation is done; nothing below may raise, so state is never half-written.
    faction.resources = [
        r for r in faction.resources if r not in set(report.resources_spent)
    ]
    for resource in report.resources_gained:
        if resource not in faction.resources:
            faction.resources.append(resource)
    for label in report.reputation_labels_gained:
        if label not in faction.reputation_labels:
            faction.reputation_labels.append(label)
    for goal in report.objectives_completed:
        if goal not in faction.objectives:
            faction.objectives.append(goal)
    for intel in report.intel_gained:
        if intel not in faction.intelligence_ids:
            faction.intelligence_ids.append(intel)
        if intel not in campaign.intelligence_ids:
            campaign.intelligence_ids.append(intel)
    for evidence in report.evidence_gained:
        if evidence not in case.evidence_ids:
            case.evidence_ids.append(evidence)

    campaign.campaign_notes.append(report.audit_entry())
    return report