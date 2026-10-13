"""The founding story as a mechanical input: the founder and the patron as stateful edges (#346).

Issue #346's own creation flow makes the founder **step 2** and the corporate patron **step 4** of a
faction's story, and both arrive with strings attached: the founder brings legitimacy and access earned
*before* the paradigm shifts, and the patron brings means with a captured-agenda risk and, at the far
end of the step-4 ladder, an usurper. Before this module the faction draft held a single ``leader``
string and the patron had **no field at all** — and ``relationship`` and ``goal`` existed only as
*static card tags*, which is a label and not a condition: a label cannot diverge, be captured or be
severed.

So this module transcribes the two roles as **relationship edges** (:mod:`strategy_game.relationships`,
reused rather than paralleled) that carry their own goals, their own typed tags and a **mutable named
state**:

* the founder's edge (``founded_by``) runs ``ascendant / contested / discredited / superseded /
  departed``;
* the patron's edge (``patron_of``) runs ``aligned / divergent / conditional / withdrawing / captured /
  severed``.

Two things this module is careful about:

* **Belief is not capability.** A founder may hold a belief that is false in the fiction while being a
  competent researcher, so "wrong but rigorous" and "right but a fraud" stay two different games. The
  check is executable: a tag whose *declared* kind in ``data/faction_creation.json`` disagrees with the
  kind it is attached as is reported by name.
* **A patron's goal need not be the faction's.** Validation permits that divergence, because the
  divergence *is* the mechanic; a rule refusing it would be the defect, not the guard.

Not approved rules. ``strategy_game/RULEBOOK.md`` still says *NO RULES APPROVED*; no scale is approved
(``numeric_scale_approved`` stays false) and this module resolves nothing — it records names, checks
referential integrity, and leaves every magnitude, every consequence and every transition as an
explicitly recorded **pending author decision**. A container is not a rule.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .provenance import Provenance
from .quantities import QUANTITY_IDS, unknown_quantities
from .relationships import RelationshipEdge, RelationshipSet, edge_from_dict

__all__ = [
    "FOUNDER_STATES",
    "FOUNDING_STORY_FORMAT",
    "PATRON_STATES",
    "ROLE_IDS",
    "DATA_PATH",
    "FoundingRole",
    "FoundingStory",
    "FoundingStoryModel",
    "founding_story_from_dict",
    "load_founding_story",
]

#: The declared file format, so a caller cannot silently load a different document.
FOUNDING_STORY_FORMAT = "noopunk.strategy_game.founding_story"

#: The packaged vocabulary.
DATA_PATH = Path(__file__).with_name("data") / "founding_story.json"

#: The founder edge's named positions. The design comment's own list, kept in the order it gives so a
#: reviewer can check them off; the order carries no magnitude and no escalation.
FOUNDER_STATES: tuple[str, ...] = ("ascendant", "contested", "discredited", "superseded", "departed")

#: The patron edge's named positions. ``captured`` is the step-4 usurper as an edge state; ``severed``
#: is money-stops. Neither is scored.
PATRON_STATES: tuple[str, ...] = (
    "aligned",
    "divergent",
    "conditional",
    "withdrawing",
    "captured",
    "severed",
)

#: The two roles the issue's flow names.
ROLE_IDS: tuple[str, ...] = ("founder", "patron")

#: The edge kind each role uses, so a patron state can never be attached to a founder edge.
EDGE_KIND_BY_ROLE: dict[str, str] = {"founder": "founded_by", "patron": "patron_of"}

#: Keys that never reach a player view.
_WITHHELD_FIELDS = frozenset({"gm_notes"})


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
    return tuple(dict(item) for item in value if isinstance(item, dict))


@dataclass
class FoundingRole:
    """One of the two roles: what it gives, what it costs, what it touches, and what is still open."""

    identifier: str
    label: str = ""
    edge_kind: str = ""
    states: tuple[str, ...] = ()
    issue_step: int = 0
    archetype: str = ""
    gives: tuple[str, ...] = ()
    costs: tuple[str, ...] = ()
    cost_kind: str = ""
    quantities_touched: tuple[str, ...] = ()
    quantity_note: str = ""
    cannot_move: tuple[str, ...] = ()
    cannot_move_note: str = ""
    failure_modes: tuple[str, ...] = ()
    failure_note: str = ""
    #: What a state *does*: recorded as a container, never applied. ``declared`` is false on purpose.
    state_effects: dict[str, Any] = field(default_factory=dict)
    pending_author_decisions: tuple[dict[str, Any], ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "edge_kind": self.edge_kind,
            "issue_step": self.issue_step,
            "states": list(self.states),
            "archetype": self.archetype,
            "gives": list(self.gives),
            "costs": list(self.costs),
            "cost_kind": self.cost_kind,
            "quantities_touched": list(self.quantities_touched),
            "quantity_note": self.quantity_note,
            "cannot_move": list(self.cannot_move),
            "cannot_move_note": self.cannot_move_note,
            "failure_modes": list(self.failure_modes),
            "failure_note": self.failure_note,
            "state_effects": dict(self.state_effects),
            "pending_author_decisions": [dict(item) for item in self.pending_author_decisions],
        }
        payload.update(self.detail)
        return payload


@dataclass
class FoundingStory:
    """A faction's founding story as two edges: the founder (required) and the patron (optional).

    The founder edge is required because issue #346 makes step 2 a mechanical input rather than a
    name: a draft with no founder edge has no legitimacy source to put at risk.
    """

    faction_id: str
    founder_edge: RelationshipEdge | None = None
    patron_edge: RelationshipEdge | None = None
    note: str = ""

    def edges(self) -> tuple[RelationshipEdge, ...]:
        return tuple(edge for edge in (self.founder_edge, self.patron_edge) if edge is not None)

    def edge_set(self) -> RelationshipSet:
        return RelationshipSet(self.edges())

    def to_dict(self) -> dict[str, Any]:
        story: dict[str, Any] = {"faction_id": self.faction_id, "note": self.note}
        if self.founder_edge is not None:
            story["founder"] = self.founder_edge.to_dict()
        if self.patron_edge is not None:
            story["patron"] = self.patron_edge.to_dict()
        return story


@dataclass
class FoundingStoryModel:
    """The loaded roles, plus edge construction, validation and the pending-decision registry."""

    roles: dict[str, FoundingRole] = field(default_factory=dict)
    shared_edge: dict[str, Any] = field(default_factory=dict)
    belief_rule: dict[str, Any] = field(default_factory=dict)
    transitions: dict[str, Any] = field(default_factory=dict)
    ck3: dict[str, Any] = field(default_factory=dict)
    examples: tuple[dict[str, Any], ...] = ()
    pending_author_decisions: tuple[dict[str, Any], ...] = ()
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    detail: dict[str, Any] = field(default_factory=dict)

    # -- lookups ---------------------------------------------------------------------------

    def role(self, role_id: str) -> FoundingRole:
        return self.roles[role_id]

    def states(self, role_id: str) -> tuple[str, ...]:
        """The named positions a role's edge may carry. Never a range, never an ordering by size."""
        return self.roles[role_id].states

    def example(self, example_id: str) -> dict[str, Any]:
        for example in self.examples:
            if example.get("id") == example_id:
                return dict(example)
        raise KeyError(example_id)

    # -- edge construction -----------------------------------------------------------------

    def edge(
        self,
        role_id: str,
        *,
        identifier: str,
        holder_id: str,
        other_id: str,
        state: str = "",
        state_rationale: str = "",
        tags: Iterable[str] = (),
        goals: Iterable[str] = (),
        typed_tags: Iterable[Any] = (),
        observable: Iterable[str] = (),
        inferences: Iterable[str] = (),
        gm_notes: str = "",
    ) -> RelationshipEdge:
        """Build a founder or patron edge, carrying the role's own named-state vocabulary.

        An empty state with a ``state_rationale`` is accepted and is the honest shape when the author
        has not said what the founder's condition is yet; an empty state with no reason is *reported* by
        :meth:`validate` rather than silently tolerated.
        """
        role = self.roles[role_id]
        return RelationshipEdge(
            identifier=identifier,
            holder_id=holder_id,
            other_id=other_id,
            kind=role.edge_kind,
            role=role.identifier,
            state=state,
            state_vocabulary=role.states,
            state_rationale=state_rationale,
            tags=tuple(tags),
            typed_tags=tuple(typed_tags),
            goals=tuple(goals),
            observable=tuple(observable),
            inferences=tuple(inferences),
            gm_notes=gm_notes,
        )

    # -- validation ------------------------------------------------------------------------

    def validate(
        self,
        story: FoundingStory,
        *,
        known_endpoint_ids: Iterable[str] | None = None,
        faction_tag_ids: Iterable[str] = (),
        tag_vocabulary: Mapping[str, str] | None = None,
    ) -> tuple[str, ...]:
        """Readable problems with a founding story. Empty means well-formed.

        What is checked is **structure and reference**: a founder edge exists, each edge carries the
        right role and kind, a state is one of the role's named positions (or is empty *with a reason*),
        endpoints resolve, the declared quantities are really the six, and a typed tag's kind agrees with
        the vocabulary.

        What is deliberately **not** checked: whether the patron's goal is one the faction shares. The
        canon case is a patron whose goal diverges from the party's base, and that divergence is what
        produces the party's internal contradictions — so a story whose patron holds an unshared goal
        validates cleanly, and a rule refusing it would be the defect rather than the guard.

        ``faction_tag_ids`` is accepted so a caller *can* see the shared and unshared goals side by side;
        it is recorded in a note, never turned into a complaint.
        """
        problems: list[str] = []
        known = set(known_endpoint_ids) if known_endpoint_ids is not None else None
        if story.founder_edge is None:
            problems.append(
                "the founding story has no founder edge: issue #346's step 2 makes the founder a "
                "mechanical input (a legitimacy source that can be contested or discredited), not a name"
            )
        if story.patron_edge is not None:
            for field_name, endpoint in (
                ("patron holder", story.patron_edge.holder_id),
                ("patron other", story.patron_edge.other_id),
            ):
                if not endpoint:
                    problems.append(f"the {field_name} endpoint is empty")
            if not story.patron_edge.goals:
                problems.append(
                    "the patron edge carries no goal: step 4's whole point is that the patron's "
                    "backing arrives with their own aims attached, and a patron without a goal is a "
                    "resource rather than a person with agency"
                )
        for edge in story.edges():
            head = f"edge {edge.identifier}"
            role = self.roles.get(edge.role)
            if role is None:
                problems.append(
                    f"{head}: role {edge.role!r} is not one of the founding roles {ROLE_IDS}"
                )
            else:
                if edge.kind != role.edge_kind:
                    problems.append(
                        f"{head}: role {role.identifier!r} uses kind {role.edge_kind!r}, not "
                        f"{edge.kind!r}"
                    )
                if edge.state_vocabulary != role.states:
                    problems.append(
                        f"{head}: the state vocabulary is not the role's declared named positions "
                        f"{role.states}"
                    )
            if edge.holder_id == edge.other_id:
                # Unreachable in practice: RelationshipEdge refuses a self-tie at construction, which
                # is the right place for it. Kept as a note of where the rule lives.
                problems.append(f"{head}: a tie to itself is not a tie")
            for name in unknown_quantities(self._role_quantities(edge.role)):
                problems.append(f"{head}: {name!r} is not one of the six quantities")
        for role in self.roles.values():
            for name in unknown_quantities((*role.quantities_touched, *role.cannot_move)):
                problems.append(
                    f"role {role.identifier}: {name!r} is not one of the six quantities {QUANTITY_IDS}"
                )
        if "founder" in self.roles and tuple(self.roles["founder"].states) != FOUNDER_STATES:
            problems.append("the shipped founder role does not declare the design comment's states")
        problems.extend(
            story.edge_set().validate(
                known_endpoint_ids=known, tag_vocabulary=tag_vocabulary
            )
        )
        if faction_tag_ids and story.patron_edge is not None:
            shared = set(faction_tag_ids)
            unshared = tuple(goal for goal in story.patron_edge.goals if goal not in shared)
            if unshared:
                # Recorded, not complained about: divergence is the mechanic.
                story.note = (
                    f"the patron's own goals {list(unshared)} are not held by the faction; the "
                    "divergence is recorded and deliberately not treated as a problem"
                )
        return tuple(problems)

    def _role_quantities(self, role_id: str) -> tuple[str, ...]:
        role = self.roles.get(role_id)
        if role is None:
            return ()
        return (*role.quantities_touched, *role.cannot_move)

    # -- reporting -------------------------------------------------------------------------

    def unshared_goals(self, story: FoundingStory, faction_tag_ids: Iterable[str]) -> tuple[str, ...]:
        """The patron's goals the faction does not hold. Reported, never refused."""
        if story.patron_edge is None:
            return ()
        held = set(faction_tag_ids)
        return tuple(goal for goal in story.patron_edge.goals if goal not in held)

    def pending_decisions(self) -> tuple[dict[str, Any], ...]:
        """Every decision left to the author, with the reason it is open. Empty reasons are refused."""
        return (*self.pending_author_decisions, *(
            item for role in self.roles.values() for item in role.pending_author_decisions
        ))

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
        for role in self.roles.values():
            if role.identifier not in ROLE_IDS:
                out.append((role.identifier, "role", role.identifier))
            for state in role.states:
                if state.strip() != state or not state:
                    out.append((role.identifier, "state", state))
        return tuple(out)


def founding_story_from_dict(data: Mapping[str, Any]) -> FoundingStoryModel:
    """Build the model from the packaged document shape."""
    roles: dict[str, FoundingRole] = {}
    for record in _records(data.get("roles")):
        role = FoundingRole(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            edge_kind=str(record.get("edge_kind") or ""),
            states=_strings(record.get("states")),
            issue_step=int(record.get("issue_step") or 0),
            archetype=str(record.get("archetype") or ""),
            gives=_strings(record.get("gives")),
            costs=_strings(record.get("costs")),
            cost_kind=str(record.get("cost_kind") or ""),
            quantities_touched=_strings(record.get("quantities_touched")),
            quantity_note=str(record.get("quantity_note") or ""),
            cannot_move=_strings(record.get("cannot_move")),
            cannot_move_note=str(record.get("cannot_move_note") or ""),
            failure_modes=_strings(record.get("failure_modes")),
            failure_note=str(record.get("failure_note") or ""),
            state_effects=dict(record.get("state_effects") or {}),
            pending_author_decisions=_records(record.get("pending_author_decisions")),
            detail={
                key: value
                for key, value in record.items()
                if key
                not in {
                    "id", "label", "edge_kind", "states", "issue_step", "archetype", "gives", "costs",
                    "cost_kind", "quantities_touched", "quantity_note", "cannot_move",
                    "cannot_move_note", "failure_modes", "failure_note", "state_effects",
                    "pending_author_decisions",
                }
            },
        )
        roles[role.identifier] = role

    return FoundingStoryModel(
        roles=roles,
        shared_edge=dict(data.get("shared_edge") or {}),
        belief_rule=dict(data.get("belief_is_not_competence") or {}),
        transitions=dict(data.get("transitions") or {}),
        ck3=dict(data.get("ck3") or {}),
        examples=_records(data.get("examples")),
        pending_author_decisions=_records(data.get("pending_author_decisions")),
        sources=_strings(data.get("sources")),
        provenance=Provenance.from_dict(data.get("provenance")),
        detail={
            key: value
            for key, value in data.items()
            if key
            not in {
                "format", "status", "sources", "provenance", "shared_edge", "belief_is_not_competence",
                "roles", "transitions", "ck3", "examples", "pending_author_decisions",
            }
        },
    )


def load_founding_story(path: Path | str | None = None) -> FoundingStoryModel:
    """Load the packaged founding-story vocabulary, refusing a document that is not one."""
    target = Path(path) if path is not None else DATA_PATH
    with open(target, encoding="utf-8") as handle:
        data = json.load(handle)
    declared = data.get("format")
    if declared is not None and declared != FOUNDING_STORY_FORMAT:
        raise ValueError(f"not a NoöPunk founding-story document: format={declared!r}")
    return founding_story_from_dict(data)


def story_from_example(model: FoundingStoryModel, story_id: str) -> FoundingStory:
    """Build a :class:`FoundingStory` from a shipped example record.

    Convenience for callers and tests: the example's role, kind and state vocabulary are read from the
    role it names, so the shipped examples are exercised through exactly the same construction path a
    live faction would take.
    """
    record = model.example(story_id)
    role_id = str(record.get("role") or "")
    edge = edge_from_dict(record)
    role = model.roles[role_id]
    edge.role = role.identifier
    edge.kind = str(record.get("kind") or record.get("edge_kind") or role.edge_kind)
    edge.state_vocabulary = role.states
    faction_id = str(record.get("other_id") or "")
    if role_id == "founder":
        return FoundingStory(faction_id=faction_id, founder_edge=edge)
    return FoundingStory(faction_id=faction_id, patron_edge=edge)
