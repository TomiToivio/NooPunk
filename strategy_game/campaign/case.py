"""The investigative Case record: the author's own case worksheet as data (#502 Phase 1).

The mission concept already exists in this repo as a **declaration**, and the
investigation concept exists as an **author worksheet**. This module reuses both and
invents neither:

* :class:`strategy_game.council.MissionDeclaration` (issue #323) is the declared move —
  leader, kind, target, which quantity it moves. It deliberately carries an
  **uninterpreted** ``outcome`` field, because nothing in that package resolves. A
  mission board is Phase 2 scope (#502) and stays unbuilt: no mission *list*, no
  mission *generation*, no clock.
* ``data/rules/unsa_case_template.json`` (the Helsinki/UNSA case worksheet) is the
  author's own field vocabulary for one case: ``case_id``/``hook``/``investigator``/
  ``partner``/``core_question``/``domain_leads``/``witnesses``/``evidence_ids``/
  ``contradictions``/``faction_interests``/``possible_player_choices``/
  ``consequences``/``resolution_notes``.

So a Phase 1 :class:`Case` is exactly that worksheet, as a record: the same field
names, a status the author declares, and no locked solution and no numeric progress
— the template's own ``rules.outcome`` line says "No mandatory fixed solution;
preserve player agency, uncertainty and consequence".

The two-layer skill distinction (#482) is honored structurally: participants are ids
that bind :class:`strategy_game.rpg.fate.Character` sheets held on the campaign, and
which layer a check belongs to stays a **check-time** decision the Fate layer already
owns (:class:`~strategy_game.rpg.skills.ActionContext`). Nothing here resolves,
rolls, or rates anything.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "CASE_TEMPLATE_FIELDS",
    "CASE_TEMPLATE_PATH",
    "Case",
    "case_from_dict",
    "resolve_case",
]

#: The packaged author worksheet this record mirrors. Read lazily, and only by tests
#: and tools — the game code never needs the file to construct a case.
CASE_TEMPLATE_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "rules" / "unsa_case_template.json"
)

#: The worksheet vocabulary, verbatim from the author's template. A field outside this
#: set is *retained* if the author supplies one (never dropped), but the schema names
#: exactly these as the case's declared fields.
CASE_TEMPLATE_FIELDS: tuple[str, ...] = (
    "case_id",
    "hook",
    "investigator",
    "partner",
    "controller",
    "forensic_ai_role",
    "core_question",
    "initial_scene",
    "domain_leads",
    "witnesses",
    "evidence_ids",
    "contradictions",
    "faction_interests",
    "possible_player_choices",
    "consequences",
    "resolution_notes",
)


class CaseError(ValueError):
    """A case operation the worksheet schema does not allow."""


@dataclass
class Case:
    """One investigation: the author's worksheet vocabulary as a record.

    ``core_question`` is required — a case without its question is not a case — and
    every list field is an **inventory**: free-text or id entries the author's
    scenario supplies. Nothing here generates leads, locks a solution, or counts
    progress, because the template's own rules forbid doing so.
    """

    case_id: str
    #: The core question. Required; the template names it first among non-id fields.
    core_question: str
    hook: str = ""
    #: Character ids of the participants (leader/agents), binding campaign sheets.
    investigator: str = ""
    partner: str = ""
    controller: str = ""
    forensic_ai_role: str = ""
    initial_scene: str = ""
    #: Per-domain leads keyed exactly as the worksheet's ``domain_leads``:
    #: physical / cybernetic / social / psychic_noospace. Open keys are retained.
    domain_leads: dict[str, list[str]] = field(default_factory=dict)
    witnesses: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)
    faction_interests: list[str] = field(default_factory=list)
    possible_player_choices: list[str] = field(default_factory=list)
    consequences: list[str] = field(default_factory=list)
    resolution_notes: list[str] = field(default_factory=list)
    #: Other authored fields, retained verbatim so nothing the author writes is lost.
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not str(self.case_id).strip():
            raise CaseError("a case needs a non-empty case_id")
        if not str(self.core_question).strip():
            raise CaseError(f"case {self.case_id!r}: the core_question is required")

    def to_dict(self) -> dict[str, Any]:
        """The worksheet vocabulary as plain JSON, plus retained detail."""
        payload: dict[str, Any] = dict(self.detail)
        payload.update(
            {
                "case_id": self.case_id,
                "core_question": self.core_question,
                "hook": self.hook,
                "investigator": self.investigator,
                "partner": self.partner,
                "controller": self.controller,
                "forensic_ai_role": self.forensic_ai_role,
                "initial_scene": self.initial_scene,
                "domain_leads": {k: list(v) for k, v in self.domain_leads.items()},
                "witnesses": list(self.witnesses),
                "evidence_ids": list(self.evidence_ids),
                "contradictions": list(self.contradictions),
                "faction_interests": list(self.faction_interests),
                "possible_player_choices": list(self.possible_player_choices),
                "consequences": list(self.consequences),
                "resolution_notes": list(self.resolution_notes),
            }
        )
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Case":
        if not isinstance(data, Mapping):
            raise CaseError(f"a case record must be a mapping, got {type(data).__name__}")
        known = frozenset(CASE_TEMPLATE_FIELDS) | {"detail"}
        return cls(
            case_id=str(data.get("case_id") or data.get("id") or ""),
            core_question=str(data.get("core_question") or ""),
            hook=str(data.get("hook") or ""),
            investigator=str(data.get("investigator") or ""),
            partner=str(data.get("partner") or ""),
            controller=str(data.get("controller") or ""),
            forensic_ai_role=str(data.get("forensic_ai_role") or ""),
            initial_scene=str(data.get("initial_scene") or ""),
            domain_leads={
                str(k): [str(x) for x in (v or [])]
                for k, v in dict(data.get("domain_leads") or {}).items()
            },
            witnesses=[str(x) for x in (data.get("witnesses") or [])],
            evidence_ids=[str(x) for x in (data.get("evidence_ids") or [])],
            contradictions=[str(x) for x in (data.get("contradictions") or [])],
            faction_interests=[str(x) for x in (data.get("faction_interests") or [])],
            possible_player_choices=[str(x) for x in (data.get("possible_player_choices") or [])],
            consequences=[str(x) for x in (data.get("consequences") or [])],
            resolution_notes=[str(x) for x in (data.get("resolution_notes") or [])],
            detail={key: value for key, value in data.items() if key not in known},
        )


def case_from_dict(data: Mapping[str, Any]) -> Case:
    """Build a case from :meth:`Case.to_dict` output (the loader seam the tests use)."""
    return Case.from_dict(data)


def resolve_case(case: Case, *, evidence_id: str, note: str = "") -> tuple[str, ...]:
    """Absorb one piece of evidence into the case's inventory (the thin Phase-1 loop).

    This is deliberately the *only* case-progress operation in Phase 1 — no progress
    score, no lead-unlock threshold and no auto-conclusion, because the worksheet's
    own ``rules.outcome`` line forbids a mandatory fixed solution and the resolution
    of *what the evidence means* stays a fiction/GM decision. Returns the evidence
    list before absorption so the caller's report can show the transition.
    """
    if not str(evidence_id).strip():
        raise CaseError("record an evidence id")
    if evidence_id not in case.evidence_ids:
        case.evidence_ids.append(evidence_id)
        if note:
            case.resolution_notes.append(note)
    return tuple(case.evidence_ids)