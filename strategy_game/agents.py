"""Agent/card ontology reader and validator (issue #303).

Issue #303 asks for a *"single common Agent/Card interface"* covering population segments, areas,
organisations, factions and leaders -- while fitting Luhmannian function systems and Castellsian
networks in **without anthropomorphizing them**.

What this module is
-------------------

A stdlib-only reader and validator for ``data/agent_ontology.json`` that enforces the distinction the
issue's own wording depends on:

* **Agents and interpretive contexts are disjoint sets.** An agent may be asked *"what do you do
  now?"*; a context may only be asked *"how does this read?"*. If a function system is ever declared
  as an agent, :meth:`AgentOntology.problems` reports it -- that is the single check that stops "the
  Law" from acquiring a turn.
* **A shared card shape is not a shared algorithm.** Every kind carries the common interface fields;
  none is given behaviour.
* **No numbers.** No numeric value appears in any kind or context, matching the no-quantity
  discipline that ``tests/test_political_layer.py`` already enforces for the political records.
* **No third spelling.** The unclassified signifier role keeps ``politics.py``'s ``unspecified`` and
  introduces no synonym, per ``V1_DISCOURSE_AND_NETWORK.md`` section 2.3.

What this module is not
-----------------------

Not an engine and not a simulation. It resolves no mechanic, approves no scale, and arbitrates
neither the ``politics.py`` / ``political.py`` fork nor the frontier's node-vs-edge question -- both
of which ``V1_DISCOURSE_AND_NETWORK.md`` section 2.2 routes to the author. ``RULEBOOK.md`` still says
NO RULES APPROVED.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import json

__all__ = [
    "ONTOLOGY_FORMAT",
    "DATA_PATH",
    "AGENT_KIND_IDS",
    "CONTEXT_IDS",
    "OntologyError",
    "Card",
    "AgentOntology",
    "ontology_from_dict",
    "load_agent_ontology",
]

#: Declared document type.
ONTOLOGY_FORMAT = "noopunk.strategy_game.agent_ontology"

DATA_PATH = Path(__file__).with_name("data") / "agent_ontology.json"

#: The four card kinds #303 names. Order is the issue's order: population, area, organisation, faction.
AGENT_KIND_IDS: tuple[str, ...] = ("population_segment", "location", "organization", "faction_leader")

#: The three interpretive contexts. These must never be agents.
CONTEXT_IDS: tuple[str, ...] = ("function_systems", "communication_networks", "discourse")

#: A synonym for the unclassified signifier role is banned (V1 section 2.3).
_BANNED_SPELLINGS = ("unrecorded", "unclassified")

#: Field-name fragments that would imply a scale this record has no authority to approve.
_SCALE_TOKENS = ("score", "rating", "points", "level", "strength", "percentage")


class OntologyError(ValueError):
    """Raised when a document cannot be read as an agent ontology."""


def _has_number(value: Any) -> bool:
    """True if a numeric value appears anywhere in the structure (bool is not a number here)."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, dict):
        return any(_has_number(v) for v in value.values())
    if isinstance(value, (list, tuple)):
        return any(_has_number(v) for v in value)
    return False


def _banned_spelling_values(value: Any) -> tuple[str, ...]:
    """Banned synonyms used as a *value* -- i.e. an enum role -- not merely named in prose.

    ``V1_DISCOURSE_AND_NETWORK.md`` section 2.3 bans a third spelling for the unclassified signifier
    role. Prose that *discusses* the ban necessarily mentions the words, so this checks string values
    for equality rather than scanning raw text.
    """
    found: list[str] = []
    if isinstance(value, str):
        if value.strip().lower() in _BANNED_SPELLINGS:
            found.append(value.strip().lower())
    elif isinstance(value, dict):
        for item in value.values():
            found.extend(_banned_spelling_values(item))
    elif isinstance(value, (list, tuple)):
        for item in value:
            found.extend(_banned_spelling_values(item))
    return tuple(found)


@dataclass
class Card:
    """One ontology entry, whether agent kind or interpretive context."""

    id: str
    label: str = ""
    is_agent: bool = False
    represents: str = ""
    what_it_is: str = ""
    why_not_an_agent: str = ""
    how_it_acts: str = ""
    not_: str = ""
    notes: str = ""
    aggregation_rule: str = ""
    double_counting_guard: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {**self.detail}
        data.update(
            id=self.id,
            label=self.label,
            is_agent=self.is_agent,
            represents=self.represents,
            what_it_is=self.what_it_is,
            why_not_an_agent=self.why_not_an_agent,
            how_it_acts=self.how_it_acts,
            not_=self.not_,
            notes=self.notes,
            aggregation_rule=self.aggregation_rule,
            double_counting_guard=self.double_counting_guard,
        )
        return {k: v for k, v in data.items() if v not in ("", None)}


@dataclass
class AgentOntology:
    """The read ontology: the two disjoint sets, the shared interface and the open choices."""

    format: str = ONTOLOGY_FORMAT
    status: str = ""
    sources: tuple[str, ...] = ()
    provenance: dict[str, Any] = field(default_factory=dict)
    terminology: dict[str, Any] = field(default_factory=dict)
    common_card_interface: dict[str, Any] = field(default_factory=dict)
    kinds: tuple[Card, ...] = ()
    contexts: tuple[Card, ...] = ()
    overlap_and_aggregation: dict[str, Any] = field(default_factory=dict)
    vocabulary_discipline: dict[str, Any] = field(default_factory=dict)
    pending_author_choices: tuple[str, ...] = ()
    raw: dict[str, Any] = field(default_factory=dict)

    # -- lookups -----------------------------------------------------------------
    def kind(self, kind_id: str) -> Card | None:
        return next((k for k in self.kinds if k.id == kind_id), None)

    def context(self, context_id: str) -> Card | None:
        return next((c for c in self.contexts if c.id == context_id), None)

    @property
    def kind_ids(self) -> tuple[str, ...]:
        return tuple(k.id for k in self.kinds)

    @property
    def context_ids(self) -> tuple[str, ...]:
        return tuple(c.id for c in self.contexts)

    @property
    def required_fields(self) -> tuple[str, ...]:
        return tuple(str(f) for f in self.common_card_interface.get("required_fields", []))

    @property
    def optional_fields(self) -> tuple[str, ...]:
        return tuple(str(f) for f in self.common_card_interface.get("optional_fields", []))

    def to_dict(self) -> dict[str, Any]:
        data = dict(self.raw)
        data["format"] = self.format
        data["agent_kinds"] = [k.to_dict() for k in self.kinds]
        data["interpretive_contexts"] = [c.to_dict() for c in self.contexts]
        return data

    # -- validation --------------------------------------------------------------
    def problems(self) -> tuple[str, ...]:
        """Ontology-internal defects. Reports; never raises."""
        issues: list[str] = []
        if self.format != ONTOLOGY_FORMAT:
            issues.append(f"format is {self.format!r}, expected {ONTOLOGY_FORMAT!r}")

        # 1. the two sets are disjoint -- the non-anthropomorphism rule
        both = set(self.kind_ids) & set(self.context_ids)
        if both:
            issues.append(f"declared as both agent and context: {sorted(both)}")

        # 2. a context is never an agent
        for ctx in self.contexts:
            if ctx.is_agent:
                issues.append(f"context {ctx.id!r} is marked is_agent")
        for kind in self.kinds:
            if not kind.is_agent:
                issues.append(f"agent kind {kind.id!r} is not marked is_agent")

        # 3. the four named kinds are present
        missing = [k for k in AGENT_KIND_IDS if k not in self.kind_ids]
        if missing:
            issues.append(f"missing agent kinds: {missing}")
        for ctx_id in CONTEXT_IDS:
            if ctx_id not in self.context_ids:
                issues.append(f"missing interpretive context: {ctx_id!r}")

        # 4. shared card shape, per kind
        for kind in self.kinds:
            for needed in ("represents", "aggregation_rule", "double_counting_guard"):
                if not getattr(kind, needed):
                    issues.append(f"{kind.id}: kind lacks {needed}")

        # 5. no numbers anywhere in the kinds or contexts
        for card in list(self.kinds) + list(self.contexts):
            if _has_number(card.detail):
                issues.append(f"{card.id}: a numeric value appears in the card")
            for key in card.detail:
                if any(tok in key.lower() for tok in _SCALE_TOKENS):
                    issues.append(f"{card.id}: scale-shaped field {key!r}")

        # 6. the common interface declares what a card carries
        for needed in ("kind", "identity", "provenance"):
            if needed not in self.required_fields:
                issues.append(f"common card interface does not require {needed!r}")
        for needed in ("relationships", "location_associations", "system_associations", "scenario_tags"):
            if needed not in self.optional_fields:
                issues.append(f"common card interface does not offer {needed!r}")

        # 7. no third spelling for the unclassified role, as a value
        for banned in _banned_spelling_values(self.raw):
            issues.append(f"banned synonym {banned!r} for the unclassified role appears as a value")

        # 8. overlap strategy is stated, not implied
        if not self.overlap_and_aggregation.get("rules"):
            issues.append("overlap_and_aggregation declares no rules")

        return tuple(issues)


def _card_from_dict(record: dict[str, Any]) -> Card:
    known = {
        "id", "label", "is_agent", "represents", "what_it_is", "why_not_an_agent", "how_it_acts",
        "not", "notes", "aggregation_rule", "double_counting_guard",
    }
    return Card(
        id=str(record.get("id", "")),
        label=str(record.get("label", "")),
        is_agent=bool(record.get("is_agent", False)),
        represents=str(record.get("represents", "")),
        what_it_is=str(record.get("what_it_is", "")),
        why_not_an_agent=str(record.get("why_not_an_agent", "")),
        how_it_acts=str(record.get("how_it_acts", "")),
        not_=str(record.get("not", "")),
        notes=str(record.get("notes", "")),
        aggregation_rule=str(record.get("aggregation_rule", "")),
        double_counting_guard=str(record.get("double_counting_guard", "")),
        detail={k: v for k, v in record.items() if k not in known},
    )


def ontology_from_dict(data: dict[str, Any]) -> AgentOntology:
    """Build an :class:`AgentOntology` from an already-parsed document."""
    if not isinstance(data, dict):
        raise OntologyError("ontology document must be an object")
    return AgentOntology(
        format=str(data.get("format", "")),
        status=str(data.get("status", "")),
        sources=tuple(str(s) for s in data.get("sources", []) or []),
        provenance=data.get("provenance", {}) or {},
        terminology=data.get("terminology", {}) or {},
        common_card_interface=data.get("common_card_interface", {}) or {},
        kinds=tuple(_card_from_dict(r) for r in data.get("agent_kinds", []) or []),
        contexts=tuple(_card_from_dict(r) for r in data.get("interpretive_contexts", []) or []),
        overlap_and_aggregation=data.get("overlap_and_aggregation", {}) or {},
        vocabulary_discipline=data.get("vocabulary_discipline", {}) or {},
        pending_author_choices=tuple(str(c) for c in data.get("pending_author_choices", []) or []),
        raw=data,
    )


def load_agent_ontology(path: Path | str | None = None) -> AgentOntology:
    """Read and validate the packaged ontology, refusing a foreign document type."""
    target = Path(path) if path is not None else DATA_PATH
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:  # pragma: no cover - packaging error
        raise OntologyError(f"ontology data not found at {target}") from exc
    except json.JSONDecodeError as exc:
        raise OntologyError(f"ontology data is not valid JSON: {exc}") from exc

    if data.get("format") != ONTOLOGY_FORMAT:
        raise OntologyError(f"{target} declares format {data.get('format')!r}, expected {ONTOLOGY_FORMAT!r}")
    return ontology_from_dict(data)
