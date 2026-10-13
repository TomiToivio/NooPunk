"""The one sparse, *stateful* relationship edge — shared by the council (#323) and the founding story (#346).

``strategy_game/characters.py`` already carries a :class:`~strategy_game.characters.Relationship`, and
it is the right record for what it does: a **static card tag** — ``other_id``, ``kind``,
``visibility`` — such as the canon ``patron_of -> ulp`` on ``sir_mars_eldrich``. A label with no
condition attached cannot do what two landed issues now ask for:

* issue #323 asks relationships to *modify* recruitment, negotiation, cooperation, internal cohesion,
  intelligence sharing, defection and rivals' responses — i.e. a tie has to be **read** by the mission
  layer; and
* issue #346 asks for a founder and a patron whose edges **diverge, capture or are severed** — i.e. a
  tie has to **change**.

So this module adds the missing record, and deliberately **the only one**: the #346 design comment's
own instruction is that the founder and patron edges "reuse that record, not a parallel one". The
static card tag is consumed, never replaced — :meth:`RelationshipSet.from_card_relationships` builds a
stateful edge out of a card's declared tie so the two never drift apart silently.

What this module is **not**: approved rules. ``strategy_game/RULEBOOK.md`` still says *NO RULES
APPROVED*. Nothing here rolls, resolves, compares or applies:

* no affinity, opinion score, modifier, difficulty or threshold is computed, ever;
* ``state`` is a **named position** drawn from a vocabulary the *caller* declares — the council layer
  declares none for a plain tie and the founding-story layer declares the founder's and the patron's —
  so a number in that field is refused with a reason rather than accepted;
* an edge that would need a value the author has not given carries an **empty field with a reason**
  (``state_rationale``), because an empty field with a reason is a question and an invented number is a
  rule;
* a **sparse** set is not a dense one: two records with no authored edge between them are *unmodelled*,
  not a neutral-zero edge in a complete graph (``docs/LEADER_COUNCIL_SYSTEM.md`` §5).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

from .characters import Relationship as CardRelationship, Tag
from .tabletop.cards import CardVisibility

__all__ = [
    "EDGE_KINDS",
    "RELATIONSHIP_TAGS",
    "RelationshipEdge",
    "RelationshipError",
    "RelationshipSet",
    "edge_from_dict",
    "slug",
]

#: Endpoint kinds are **not** asserted here: an endpoint is a named record (a person, a faction, an
#: organisation, a body), and the roster and the codex decide which. Whether the founder is one of the
#: four leaders or a fifth authority over them — and whether a patron sits on the council — are
#: *open* author questions (#346 step 4 names ally / council member / rival power centre / usurper and
#: fixes none as the default), so this module refuses to hard-code an endpoint taxonomy.

#: The edge kinds this vocabulary knows. The first two are the founding-story roles (#346 step 2 and
#: step 4); the rest are the interpersonal ties the two issues name. An off-vocabulary kind is
#: *reported*, never silently coerced, because a kind is a claim about what a tie is.
EDGE_KINDS: tuple[str, ...] = (
    "founded_by",
    "patron_of",
    "allied_with",
    "rival_of",
    "mentor_of",
    "indebted_to",
    "suspicious_of",
    "former_ally_of",
    "family_of",
    "contested_by",
)

#: The evocative tags ``docs/LEADER_COUNCIL_SYSTEM.md`` §5 lists, verbatim. The document marks the list
#: **open and extensible**, so an unknown tag is reported rather than refused — and no tag carries an
#: effect, because no effect is approved.
RELATIONSHIP_TAGS: tuple[str, ...] = (
    "friend",
    "rival",
    "family",
    "mentor",
    "indebted",
    "suspicious",
    "former_ally",
)


class RelationshipError(ValueError):
    """Raised for a malformed edge. Deliberately the only thing this module raises on its own."""


def slug(text: str) -> str:
    """A stable, id-safe token. Mirrors :func:`strategy_game.characters.slug`."""
    out = [ch.lower() if ch.isalnum() else "_" for ch in str(text).strip()]
    collapsed = "".join(out)
    while "__" in collapsed:
        collapsed = collapsed.replace("__", "_")
    return collapsed.strip("_")


def _strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    return tuple(str(item).strip() for item in value if str(item).strip())


@dataclass
class RelationshipEdge:
    """A sparse, pairwise, **stateful** tie between two named records.

    The record is mutable on purpose — that is the whole gap it closes. :meth:`reassign_state` changes
    the edge's condition and logs the previous one; **which** transitions are legitimate is a rule the
    author has not given, so no transition is judged here.
    """

    identifier: str
    #: The end from which the tie is held. Direction is authored, not asserted: the canon
    #: ``sir_mars_eldrich -> ulp`` edge reads founder-side, and this record keeps that direction.
    holder_id: str
    #: The other end.
    other_id: str
    kind: str = ""
    #: ``""`` for a plain interpersonal tie; ``founder`` or ``patron`` for a founding-story edge.
    role: str = ""
    #: A **named position**, never a number. Empty only with a reason in :attr:`state_rationale`.
    state: str = ""
    #: The named positions this edge's state may be drawn from — declared by the caller (the
    #: founding-story roles declare theirs). Empty means the author has declared none for this tie,
    #: which is a fact worth reporting rather than papering over.
    state_vocabulary: tuple[str, ...] = ()
    #: Why :attr:`state` is empty, when it is. An empty field with a reason is a question.
    state_rationale: str = ""
    #: Qualitative tags from the open list above.
    tags: tuple[str, ...] = ()
    #: Typed tags — belief / competence / equipment / relationship / asset / goal — using issue #346's
    #: vocabulary through :class:`strategy_game.characters.Tag`. The kind is the point: a doctrine is
    #: never read as a capability.
    typed_tags: tuple[Tag, ...] = ()
    #: The edge's **own** goals (goal ids or authored goal text). A patron's goal need not be the
    #: faction's, and that divergence is the mechanic rather than a footnote.
    goals: tuple[str, ...] = ()
    #: Optional obligation text (``docs/LEADER_COUNCIL_SYSTEM.md`` §7).
    obligation: str = ""
    visibility: CardVisibility = CardVisibility.PUBLIC
    #: What happened — evidence-shaped, and kept apart from the field below.
    observable: tuple[str, ...] = ()
    #: What someone concludes from it. Attribution, and the thing a player may hold wrongly.
    inferences: tuple[str, ...] = ()
    #: Prior states, oldest first, written by :meth:`reassign_state`.
    state_history: tuple[str, ...] = ()
    #: Author-facing note. Withheld by :meth:`player_view` unless secrets are asked for.
    gm_notes: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise RelationshipError("an edge needs an identifier")
        if slug(self.identifier) != self.identifier:
            raise RelationshipError(f"edge identifier {self.identifier!r} must be a stable slug")
        if not str(self.holder_id).strip() or not str(self.other_id).strip():
            raise RelationshipError(f"edge {self.identifier}: both endpoints must be named")
        if self.holder_id == self.other_id:
            raise RelationshipError(
                f"edge {self.identifier}: a tie to oneself is not a tie; the record is sparse and "
                "pairwise"
            )

    # -- mutability -------------------------------------------------------------------------

    @property
    def is_severed(self) -> bool:
        """Whether the edge carries the ``severed`` named position.

        Nothing is deleted: whether a severed edge is dropped, kept as history or replaced by another
        patron is an **open author decision** (#346's own question list), so this property reads the
        state and removes nothing.
        """
        return self.state == "severed"

    def reassign_state(self, state: str, *, reason: str = "") -> str:
        """Move the edge to another **named position** and return the previous one.

        Raises when the edge has no declared vocabulary, or when ``state`` is not one of its declared
        positions — a state outside the vocabulary would be this module inventing a rule. The
        *legitimacy* of a transition (may ``divergent`` become ``captured``?) is not judged: the
        design comment's own framing is that money-stops and capture are state transitions rather than
        die rolls, and which transitions are permitted is the author's.
        """
        if not self.state_vocabulary:
            raise RelationshipError(
                f"edge {self.identifier} declares no state vocabulary, so a state cannot be checked; "
                "the author has declared no named positions for this tie"
            )
        if state not in self.state_vocabulary:
            raise RelationshipError(
                f"edge {self.identifier}: {state!r} is not one of {self.state_vocabulary}; a named "
                "position is required"
            )
        previous = self.state
        self.state_history = (*self.state_history, previous)
        self.state = state
        if reason:
            self.detail["last_state_reason"] = reason
        return previous

    # -- serialization ----------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.identifier,
            "holder_id": self.holder_id,
            "other_id": self.other_id,
            "kind": self.kind,
            "role": self.role,
            "state": self.state,
            "state_vocabulary": list(self.state_vocabulary),
            "state_rationale": self.state_rationale,
            "tags": list(self.tags),
            "typed_tags": [tag.to_dict() for tag in self.typed_tags],
            "goals": list(self.goals),
            "obligation": self.obligation,
            "visibility": self.visibility.value,
            "observable": list(self.observable),
            "inferences": list(self.inferences),
            "state_history": list(self.state_history),
            "gm_notes": self.gm_notes,
        }
        payload.update(self.detail)
        return payload


def edge_from_dict(data: Mapping[str, Any]) -> RelationshipEdge:
    """Build an edge from a record. ``typed_tags`` entries are ``{"kind": ..., "value": ...}``."""
    if not isinstance(data, Mapping) or not data.get("id"):
        raise RelationshipError("an edge needs an 'id'")
    known = {
        "id", "holder_id", "other_id", "kind", "role", "state", "state_vocabulary",
        "state_rationale", "tags", "typed_tags", "goals", "obligation", "visibility", "observable",
        "inferences", "state_history", "gm_notes",
    }
    return RelationshipEdge(
        identifier=str(data["id"]),
        holder_id=str(data.get("holder_id") or ""),
        other_id=str(data.get("other_id") or ""),
        kind=str(data.get("kind") or ""),
        role=str(data.get("role") or ""),
        state=str(data.get("state") or ""),
        state_vocabulary=_strings(data.get("state_vocabulary")),
        state_rationale=str(data.get("state_rationale") or ""),
        tags=_strings(data.get("tags")),
        typed_tags=tuple(
            Tag(str(item.get("kind", "")).strip(), str(item.get("value", "")).strip())
            for item in (data.get("typed_tags") or [])
            if isinstance(item, Mapping)
        ),
        goals=_strings(data.get("goals")),
        obligation=str(data.get("obligation") or ""),
        visibility=CardVisibility(str(data.get("visibility") or CardVisibility.PUBLIC.value)),
        observable=_strings(data.get("observable")),
        inferences=_strings(data.get("inferences")),
        state_history=_strings(data.get("state_history")),
        gm_notes=str(data.get("gm_notes") or ""),
        detail={key: value for key, value in data.items() if key not in known},
    )


class RelationshipSet:
    """A sparse collection of stateful edges, with referential validation and a player view."""

    def __init__(self, edges: Iterable[RelationshipEdge] = ()) -> None:
        self.edges: dict[str, RelationshipEdge] = {}
        for edge in edges:
            if edge.identifier in self.edges:
                raise RelationshipError(f"duplicate edge identifier {edge.identifier!r}")
            self.edges[edge.identifier] = edge

    def __len__(self) -> int:
        return len(self.edges)

    def __iter__(self):
        return iter(self.edges.values())

    def get(self, identifier: str) -> RelationshipEdge:
        try:
            return self.edges[identifier]
        except KeyError as exc:
            raise RelationshipError(f"no edge {identifier!r} in the set") from exc

    def between(self, first: str, second: str, *, kind: str = "") -> tuple[RelationshipEdge, ...]:
        """The authored edges joining two records, in either direction.

        An empty tuple means **unmodelled**, not zero: the record is sparse, so two people with no
        authored tie are simply not represented (``LEADER_COUNCIL_SYSTEM.md`` §5). Callers must not
        read this as "no effect of magnitude zero" — that would be the dense graph the spec forbids.
        """
        out = []
        for edge in self.edges.values():
            if {edge.holder_id, edge.other_id} != {first, second}:
                continue
            if kind and edge.kind != kind:
                continue
            out.append(edge)
        return tuple(out)

    def with_role(self, role: str) -> tuple[RelationshipEdge, ...]:
        """Every edge carrying this role — ``founder`` or ``patron``, or ``""`` for a plain tie."""
        return tuple(edge for edge in self.edges.values() if edge.role == role)

    def of(self, identifier: str) -> tuple[RelationshipEdge, ...]:
        """Every edge touching this record."""
        return tuple(
            edge for edge in self.edges.values() if identifier in (edge.holder_id, edge.other_id)
        )

    # -- validation -------------------------------------------------------------------------

    def validate(
        self,
        *,
        known_endpoint_ids: Iterable[str] | None = None,
        tag_vocabulary: Mapping[str, str] | None = None,
    ) -> tuple[str, ...]:
        """Readable referential problems with the set. Empty means well-formed.

        ``tag_vocabulary`` maps a tag id to its declared **kind** (issue #346's
        ``data/faction_creation.json`` supplies exactly that). Supplying it is what turns "belief is
        not capability" from a slogan into a check: an id the vocabulary files under ``belief`` may not
        be attached as a ``competence``, and vice versa. Free-text tag values are the norm in this
        repository's card data, so a value the vocabulary does not define is not a problem.

        Nothing here judges balance, magnitude or consequence: there is no such quantity to judge.
        """
        problems: list[str] = []
        known = set(known_endpoint_ids) if known_endpoint_ids is not None else None
        for edge in self.edges.values():
            head = f"edge {edge.identifier}"
            if edge.kind and edge.kind not in EDGE_KINDS:
                problems.append(f"{head}: kind {edge.kind!r} is not one of {EDGE_KINDS}")
            for tag in edge.tags:
                if tag not in RELATIONSHIP_TAGS:
                    problems.append(
                        f"{head}: tag {tag!r} is not one of the declared tags {RELATIONSHIP_TAGS}; "
                        "the list is open, so this is reported rather than refused"
                    )
            if not edge.state:
                if not edge.state_rationale.strip():
                    problems.append(
                        f"{head}: the state is empty with no reason. An empty field needs a reason; "
                        "leaving it blank and silent is how an invented rule gets in later"
                    )
            elif not edge.state_vocabulary:
                problems.append(
                    f"{head}: state {edge.state!r} has no declared vocabulary to check it against; "
                    "the author has declared no named positions for this tie"
                )
            elif edge.state not in edge.state_vocabulary:
                if isinstance(edge.state, (int, float)) and not isinstance(edge.state, bool):
                    problems.append(
                        f"{head}: state {edge.state!r} is a number; a named position from "
                        f"{edge.state_vocabulary} is required"
                    )
                else:
                    problems.append(
                        f"{head}: state {edge.state!r} is not one of {edge.state_vocabulary}; a named "
                        "position is required"
                    )
            if not (edge.typed_tags or edge.goals or edge.tags):
                problems.append(
                    f"{head}: no tag and no goal. A tie that carries nothing cannot be read by "
                    "anything, which is the static card tag this record replaces"
                )
            for tag in edge.typed_tags:
                declared = (tag_vocabulary or {}).get(tag.value)
                if declared is not None and declared != tag.kind:
                    problems.append(
                        f"{head}: tag {tag.value!r} is declared as a {declared} in the vocabulary but "
                        f"attached here as a {tag.kind}; belief is not capability"
                    )
            if known is not None:
                for endpoint in (edge.holder_id, edge.other_id):
                    if endpoint not in known:
                        problems.append(f"{head}: endpoint {endpoint!r} is not a known record id")
        return tuple(problems)

    # -- the player / GM split ---------------------------------------------------------------

    def player_view(self, edge: RelationshipEdge, *, reveal_secrets: bool = False) -> dict[str, Any]:
        """An edge as a starting UI may show it.

        The GM note is withheld by the **code** rather than by renderer discipline, mirroring
        ``characters.render_detail``. ``observable`` and ``inferences`` stay two separate lists: the
        canon patron tie is a public fact, and the reading "that the party is his instrument" is an
        inference a player may hold wrongly — collapsing them would assert the inference.
        """
        payload = edge.to_dict()
        payload["observable"] = list(edge.observable)
        payload["inferences"] = list(edge.inferences)
        payload["gm_notes"] = edge.gm_notes if reveal_secrets else "[redacted — pass reveal_secrets=True]"
        return payload

    # -- consuming the static card tag -------------------------------------------------------

    @staticmethod
    def from_card_relationships(
        card_identifier: str,
        relationships: Iterable[CardRelationship],
        *,
        role: str = "",
        state: str = "",
        state_vocabulary: Iterable[str] = (),
        state_rationale: str = "",
    ) -> tuple[RelationshipEdge, ...]:
        """Upgrade a card's static ties into stateful edges, keeping the card's own direction.

        ``characters.Relationship`` stays the record on the card; this reads it so the stateful layers
        consume the same ids instead of declaring a rival pair of edges. Direction is preserved: a
        card that declares ``patron_of -> ulp`` produces an edge from the card to ``ulp``.
        """
        out = []
        for index, relationship in enumerate(relationships):
            out.append(
                RelationshipEdge(
                    identifier=slug(f"{card_identifier}_{relationship.kind}_{relationship.other_id}")
                    if relationship.kind
                    else slug(f"{card_identifier}_tie_{index}"),
                    holder_id=card_identifier,
                    other_id=relationship.other_id,
                    kind=relationship.kind,
                    role=role,
                    state=state,
                    state_vocabulary=tuple(state_vocabulary),
                    state_rationale=state_rationale,
                    visibility=relationship.visibility,
                )
            )
        return tuple(out)
