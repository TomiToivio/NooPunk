"""Faction creation: the five axes' position vocabulary, the typed tag system, and NHI diplomacy (#346).

Issue #346 asks for player-built ideological formations rather than only pregenerated parties, and it
fixes three separable things that this module carries as data:

* the **five ideological dimensions** the author names, expressed first as **named qualitative
  positions** (an ordered scale only after playtesting), with the standing warning that an ideology is
  not a personality, an intelligence, a moral grade, a psychic power or a predetermined loyalty;
* a **typed shared tag vocabulary** for faction and character cards, where the type of a tag — belief,
  competence, equipment, relationship, asset, goal — is what stops a `MATERIALIST` doctrine being read as
  a `REMOTE_VIEWER` capability, and one definition can serve different scopes (`REMOTE_VIEWING_TEAM` is
  a faction asset, `REMOTE_VIEWER` is a character competence);
* **NHI contact policy kept separate from named NHI diplomacy**: a general posture toward contact, and
  separate, mutable relations to each named polity. The issue's rule is explicit — *"avoid forcing
  'pro-NHI' to equal pro-Confederacy or pro-Orion"* — so nothing here derives either from the other.

What this module is **not**: approved rules. `strategy_game/RULEBOOK.md` still says *NO RULES
APPROVED*. It computes **no affinity, tension, recruitment or diplomatic score** — the issue allows
broad affinity cues as a later, author-approved gameplay aid and forbids unapproved numeric rules, so
this module's whole job is vocabulary, referential integrity and the player/GM split. It consumes
`data/global_factions.json` (which already declares the axes and the #329 paradigm positions) and
`docs/LEADER_COUNCIL_SYSTEM.md` (the court half) instead of restating them. Standard library only.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .provenance import Provenance

__all__ = [
    "CREATION_FORMAT",
    "DATA_PATH",
    "DIPLOMATIC_STATES",
    "POSITIONS",
    "TAG_KINDS",
    "TAG_SCOPES",
    "Axis",
    "DiplomaticState",
    "FactionCreationModel",
    "FactionDraft",
    "NhiPolity",
    "Position",
    "TagDefinition",
    "TagFamily",
    "creation_from_dict",
    "draft_from_dict",
    "load_faction_creation",
]

#: The declared file format, so a caller cannot silently load a different document.
CREATION_FORMAT = "noopunk.strategy_game.faction_creation"

#: The packaged vocabulary.
DATA_PATH = Path(__file__).with_name("data") / "faction_creation.json"

#: The named positions a faction may hold on an axis: descriptors first, numbers only after playtesting.
POSITIONS: tuple[str, ...] = (
    "strong_low_pole",
    "moderate_low_pole",
    "neutral",
    "moderate_high_pole",
    "strong_high_pole",
)

#: What a tag *is*. Issue #346: distinguish belief, competence, equipment, relationship, asset and goal
#: so that a doctrine is never read as a capability, and a capability never as equipment.
TAG_KINDS: tuple[str, ...] = ("belief", "competence", "equipment", "relationship", "asset", "goal")

#: The card types a tag may be attached to. Not every tag applies to every entity type.
TAG_SCOPES: tuple[str, ...] = ("faction", "character", "organization", "research", "government")

#: The relations a faction may hold toward a named NHI polity — mutable ties, not intrinsic ideology.
DIPLOMATIC_STATES: tuple[str, ...] = (
    "hostility",
    "contact",
    "trading",
    "alliance",
    "dependence",
    "resistance",
)

#: The field names a draft uses for the two separable NHI concepts the issue insists on separating.
POLICY_AXIS = "nhi"
RELATIONS_FIELD = "nhi_relations"

#: Draft keys that never reach a player view.
_WITHHELD_DRAFT_FIELDS = frozenset({"hidden_agenda"})


def _strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, (list, tuple)):
        return tuple(str(item) for item in value)
    return (str(value),)


def _records(value: Any) -> tuple[dict[str, Any], ...]:
    if value is None:
        return ()
    if isinstance(value, dict):
        return (dict(value),)
    if isinstance(value, (list, tuple)):
        return tuple(dict(item) if isinstance(item, dict) else {"value": item} for item in value)
    return ({"value": value},)


@dataclass
class Position:
    """One named position on an axis. ``rank`` orders the vocabulary; it is not a game quantity."""

    identifier: str
    label: str = ""
    rank: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.identifier, "label": self.label, "rank": self.rank}


@dataclass
class Axis:
    """One ideological dimension. Descriptive only: no weight, no threshold, no derived score."""

    identifier: str
    label: str = ""
    low_pole: str = ""
    high_pole: str = ""
    significance: str = ""
    declared_in: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "low_pole": self.low_pole,
            "high_pole": self.high_pole,
            "significance": self.significance,
            "declared_in": self.declared_in,
        }
        payload.update(self.detail)
        return payload


@dataclass
class TagDefinition:
    """One tag. Its ``kind`` is the whole point: doctrine and capability are different things."""

    identifier: str
    label: str = ""
    kind: str = "belief"
    family: str = ""
    applies_to: tuple[str, ...] = ()
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "kind": self.kind,
            "family": self.family,
            "applies_to": list(self.applies_to),
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class TagFamily:
    """A suggested family of tags. The issue marks these as examples, never a locked taxonomy."""

    identifier: str
    label: str = ""
    kind: str = "belief"
    suggested: bool = True
    note: str = ""
    tags: tuple[TagDefinition, ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "kind": self.kind,
            "suggested": self.suggested,
            "note": self.note,
            "tags": [tag.to_dict() for tag in self.tags],
        }
        payload.update(self.detail)
        return payload


@dataclass
class NhiPolity:
    """A named polity a faction can hold a relation toward."""

    identifier: str
    label: str = ""
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {"id": self.identifier, "label": self.label, "note": self.note}
        payload.update(self.detail)
        return payload


@dataclass
class DiplomaticState:
    """One mutable tie. Intentionally not derived from any axis position."""

    identifier: str
    label: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.identifier, "label": self.label}


@dataclass
class FactionDraft:
    """A faction being created: five positions, a handful of tags, and per-polity relations.

    ``hidden_agenda`` and unrevealed relations are GM-side; :meth:`FactionCreationModel.player_view`
    withholds them, so a starting UI cannot reveal classified author canon by accident.
    """

    identifier: str
    label: str = ""
    #: Axis id -> position id. Values are kept exactly as authored: coercing them to text would hide a
    #: number where a named position is required, which is the validation this model exists to do.
    positions: dict[str, Any] = field(default_factory=dict)
    tags: tuple[str, ...] = ()
    relations: dict[str, Any] = field(default_factory=dict)
    hidden_agenda: str = ""
    leader: str = ""
    revealed_polities: tuple[str, ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "positions": dict(self.positions),
            "tags": list(self.tags),
            RELATIONS_FIELD: dict(self.relations),
            "hidden_agenda": self.hidden_agenda,
            "leader": self.leader,
            "revealed_polities": list(self.revealed_polities),
        }
        payload.update(self.detail)
        return payload


def draft_from_dict(data: dict[str, Any]) -> FactionDraft:
    """Build a draft from a record. ``positions`` keys are axis ids; values are position ids."""
    if not isinstance(data, dict) or not data.get("id"):
        raise ValueError("a faction draft needs an 'id'")
    known = {
        "id", "label", "positions", "tags", RELATIONS_FIELD, "hidden_agenda", "leader",
        "revealed_polities",
    }
    return FactionDraft(
        identifier=str(data["id"]),
        label=str(data.get("label") or data["id"]),
        positions={str(k): v for k, v in (data.get("positions") or {}).items()},
        tags=_strings(data.get("tags")),
        relations={str(k): v for k, v in (data.get(RELATIONS_FIELD) or {}).items()},
        hidden_agenda=str(data.get("hidden_agenda") or ""),
        leader=str(data.get("leader") or ""),
        revealed_polities=_strings(data.get("revealed_polities")),
        detail={key: value for key, value in data.items() if key not in known},
    )


@dataclass
class FactionCreationModel:
    """The loaded vocabulary, plus referential validation and the player/GM split."""

    positions: dict[str, Position] = field(default_factory=dict)
    position_order: tuple[str, ...] = ()
    #: Whether the author has approved an ordered numeric scale. Named positions are the default.
    numeric_scale_approved: bool = False
    axes: dict[str, Axis] = field(default_factory=dict)
    families: dict[str, TagFamily] = field(default_factory=dict)
    tags: dict[str, TagDefinition] = field(default_factory=dict)
    polities: dict[str, NhiPolity] = field(default_factory=dict)
    states: dict[str, DiplomaticState] = field(default_factory=dict)
    flow: tuple[dict[str, Any], ...] = ()
    template: dict[str, Any] = field(default_factory=dict)
    comparative_examples: tuple[dict[str, Any], ...] = ()
    cross_axis_examples: tuple[dict[str, Any], ...] = ()
    separation_rule: dict[str, Any] = field(default_factory=dict)
    fog_of_war: dict[str, Any] = field(default_factory=dict)
    event_seed: dict[str, Any] = field(default_factory=dict)
    #: Issue #346 criterion 7's container: the field SLOTS a first-turn constraint would occupy.
    #: It carries names only — no value, no economy, no turn cadence.
    first_turn: dict[str, Any] = field(default_factory=dict)
    pending_author_decisions: tuple[dict[str, Any], ...] = ()
    cautions: tuple[dict[str, Any], ...] = ()
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    detail: dict[str, Any] = field(default_factory=dict)

    # -- lookups ---------------------------------------------------------------------------

    def axis(self, axis_id: str) -> Axis:
        return self.axes[axis_id]

    def family(self, family_id: str) -> TagFamily:
        return self.families[family_id]

    def tag(self, tag_id: str) -> TagDefinition:
        return self.tags[tag_id]

    def polity(self, polity_id: str) -> NhiPolity:
        return self.polities[polity_id]

    def tags_for(self, *, kind: str = "", scope: str = "") -> tuple[TagDefinition, ...]:
        """Tags of a kind, usable at a scope. Scope-filtering is what keeps an asset off a character."""
        out = []
        for tag in self.tags.values():
            if kind and tag.kind != kind:
                continue
            if scope and tag.applies_to and scope not in tag.applies_to:
                continue
            out.append(tag)
        return tuple(out)

    # -- validation ------------------------------------------------------------------------

    def validate_draft(self, draft: FactionDraft) -> tuple[str, ...]:
        """Referential problems with a draft, as readable strings. An empty tuple means well-formed.

        This checks *names*, never balance: the issue forbids unapproved numeric rules, so there is no
        affinity, tension or recruitment computation here to validate.
        """
        problems: list[str] = []
        for axis_id, value in draft.positions.items():
            if axis_id not in self.axes:
                problems.append(f"unknown axis {axis_id!r}")
                continue
            if value not in self.positions:
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    problems.append(
                        f"axis {axis_id!r} carries the number {value!r}: an ordered scale is not "
                        "approved, so a named position is required"
                    )
                else:
                    problems.append(f"unknown position {value!r} on axis {axis_id!r}")
        for tag_id in draft.tags:
            if tag_id not in self.tags:
                problems.append(f"unknown tag {tag_id!r}")
        for polity_id, state in draft.relations.items():
            if polity_id not in self.polities:
                problems.append(f"unknown NHI polity {polity_id!r}")
            if state not in self.states:
                problems.append(f"unknown diplomatic state {state!r} for {polity_id!r}")
        return tuple(problems)

    def validate_tag_scope(self, tag_id: str, scope: str) -> bool:
        """Whether a tag may be attached to a card of this type. No scope declared means every scope."""
        tag = self.tags[tag_id]
        return (not tag.applies_to) or scope in tag.applies_to

    # -- criterion 7's container: names only, never a value ---------------------------------

    def first_turn_fields(self) -> tuple[dict[str, Any], ...]:
        """The field slots a first-turn constraint would occupy, in the document's own order."""
        return _records(self.first_turn.get("candidate_sheet_fields"))

    def first_turn_problems(self) -> tuple[str, ...]:
        """Malformed first-turn container, refused by name. Empty means the container is well-formed.

        Issue #346's criterion 7 asks to *define* first-turn resource constraints, and the same issue
        marks its candidate sheet "not fixed". A starting economy is reserved to the author
        (``AGENTS.md`` §4) and ``strategy_game/RULEBOOK.md`` says no rules are approved, so this
        module must never invent a value. What it can refuse is a container that has stopped being a
        container: a field with no identifier, a repeated identifier, a field carrying anything but
        its name, or a container that does not say whether values are declared and why not.
        """
        problems: list[str] = []
        if not self.first_turn:
            problems.append(
                "no first-turn container is declared, so issue #346's criterion 7 has no slot to "
                "land in"
            )
            return tuple(problems)
        if not isinstance(self.first_turn.get("values_declared"), bool):
            problems.append(
                "the first-turn container does not state values_declared, so a reader cannot tell an "
                "approved sheet from an empty slot"
            )
        if not self.first_turn.get("values_declared") and not str(
            self.first_turn.get("reason") or ""
        ).strip():
            problems.append(
                "the first-turn container declares no values and gives no reason; an empty field is "
                "only honest with the reason it is empty"
            )
        seen: set[str] = set()
        for entry in self.first_turn_fields():
            identifier = str(entry.get("id") or "").strip()
            if not identifier:
                problems.append("a first-turn field has no identifier")
            elif identifier in seen:
                problems.append(f"first-turn field {identifier!r} appears more than once")
            seen.add(identifier)
            extra = sorted(key for key in entry if key not in {"id", "label", "note"})
            if extra:
                problems.append(
                    f"first-turn field {identifier!r} carries {extra}: the container names the fields "
                    "a constraint would occupy and holds no value, so a value here is an invented one"
                )
            for key, value in entry.items():
                if key in {"id", "label", "note"} and isinstance(value, (int, float)) and not isinstance(
                    value, bool
                ):
                    problems.append(
                        f"first-turn field {identifier!r}: {key} is the number {value!r}; every value "
                        "is the author's to approve"
                    )
        return tuple(problems)

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

    # -- the player / GM split -------------------------------------------------------------

    def player_view(self, draft: FactionDraft) -> dict[str, Any]:
        """A draft as a starting UI may show it: no hidden agenda, no unrevealed contact.

        The hidden agenda is withheld entirely rather than summarized, and a polity the faction does not
        know about yet is absent from the relations — the issue's fog-of-war rule.
        """
        payload = {
            key: value for key, value in draft.to_dict().items() if key not in _WITHHELD_DRAFT_FIELDS
        }
        payload[RELATIONS_FIELD] = {
            polity: state
            for polity, state in draft.relations.items()
            if polity in set(draft.revealed_polities)
        }
        payload["positions"] = dict(draft.positions)
        payload["tags"] = list(draft.tags)
        return payload

    # -- reporting -------------------------------------------------------------------------

    def referenced_tags(self) -> tuple[str, ...]:
        """Every tag id the shipped template and comparative examples point at, for integrity checks."""
        used: list[str] = []
        for source in (self.template, *self.comparative_examples):
            used.extend(_strings(source.get("tags")))
        return tuple(dict.fromkeys(used))

    def dangling_tag_references(self) -> tuple[str, ...]:
        """Referenced tag ids with no definition — reported, never silently dropped."""
        return tuple(tag for tag in self.referenced_tags() if tag not in self.tags)

    def off_vocabulary(self) -> tuple[tuple[str, str, str], ...]:
        """``(record_id, field, value)`` for values outside the declared vocabularies, without raising."""
        out: list[tuple[str, str, str]] = []
        for position in self.positions.values():
            if position.identifier not in POSITIONS:
                out.append((position.identifier, "position", position.identifier))
        for tag in self.tags.values():
            if tag.kind not in TAG_KINDS:
                out.append((tag.identifier, "kind", tag.kind))
            for scope in tag.applies_to:
                if scope not in TAG_SCOPES:
                    out.append((tag.identifier, "applies_to", scope))
        for state in self.states.values():
            if state.identifier not in DIPLOMATIC_STATES:
                out.append((state.identifier, "diplomatic_state", state.identifier))
        return tuple(out)


def creation_from_dict(data: dict[str, Any]) -> FactionCreationModel:
    """Build the model from the packaged document shape."""
    vocab = data.get("position_vocabulary") or {}
    positions: dict[str, Position] = {}
    order: list[str] = []
    for record in _records(vocab.get("positions")):
        position = Position(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            rank=int(record.get("rank", 0)),
        )
        positions[position.identifier] = position
        order.append(position.identifier)

    axes: dict[str, Axis] = {}
    for record in _records(data.get("axes")):
        known = {"id", "label", "low_pole", "high_pole", "significance", "declared_in"}
        axes[str(record["id"])] = Axis(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            low_pole=str(record.get("low_pole") or ""),
            high_pole=str(record.get("high_pole") or ""),
            significance=str(record.get("significance") or ""),
            declared_in=str(record.get("declared_in") or ""),
            detail={k: v for k, v in record.items() if k not in known},
        )

    families: dict[str, TagFamily] = {}
    tags: dict[str, TagDefinition] = {}
    for record in _records(data.get("tag_families")):
        family_id = str(record["id"])
        kind = str(record.get("kind") or "belief")
        members: list[TagDefinition] = []
        for item in _records(record.get("tags")):
            tag_id = str(item["id"])
            if tag_id in tags:
                raise ValueError(f"duplicate tag id: {tag_id!r}")
            tag = TagDefinition(
                identifier=tag_id,
                label=str(item.get("label") or ""),
                kind=str(item.get("kind") or kind),
                family=family_id,
                applies_to=_strings(item.get("applies_to")),
                note=str(item.get("note") or ""),
                detail={
                    k: v
                    for k, v in item.items()
                    if k not in {"id", "label", "kind", "applies_to", "note"}
                },
            )
            tags[tag_id] = tag
            members.append(tag)
        families[family_id] = TagFamily(
            identifier=family_id,
            label=str(record.get("label") or ""),
            kind=kind,
            suggested=bool(record.get("suggested", True)),
            note=str(record.get("note") or ""),
            tags=tuple(members),
            detail={
                k: v for k, v in record.items() if k not in {"id", "label", "kind", "suggested", "note", "tags"}
            },
        )

    polities = {
        str(r["id"]): NhiPolity(
            identifier=str(r["id"]), label=str(r.get("label") or ""), note=str(r.get("note") or "")
        )
        for r in _records(data.get("nhi_polities"))
    }
    states = {
        str(r["id"]): DiplomaticState(identifier=str(r["id"]), label=str(r.get("label") or ""))
        for r in _records(data.get("diplomatic_states"))
    }

    return FactionCreationModel(
        positions=positions,
        position_order=tuple(order),
        numeric_scale_approved=bool(vocab.get("numeric_scale_approved", False)),
        axes=axes,
        families=families,
        tags=tags,
        polities=polities,
        states=states,
        flow=_records(data.get("faction_creation_flow")),
        template=dict(data.get("template") or {}),
        comparative_examples=_records(data.get("comparative_examples")),
        cross_axis_examples=_records(data.get("cross_axis_examples")),
        separation_rule=dict(data.get("separation_rule") or {}),
        fog_of_war=dict(data.get("fog_of_war") or {}),
        event_seed=dict(data.get("event_seed") or {}),
        first_turn=dict(data.get("first_turn") or {}),
        pending_author_decisions=_records(data.get("pending_author_decisions")),
        cautions=_records(data.get("cautions")),
        sources=_strings(data.get("sources")),
        provenance=Provenance.from_dict(data.get("provenance")),
        detail={
            key: value
            for key, value in data.items()
            if key
            not in {
                "format", "position_vocabulary", "axes", "tag_families", "nhi_polities",
                "diplomatic_states", "faction_creation_flow", "template", "comparative_examples",
                "cross_axis_examples", "separation_rule", "fog_of_war", "event_seed", "cautions",
                "sources", "provenance", "first_turn", "pending_author_decisions",
            }
        },
    )


def load_faction_creation(path: Path | str | None = None) -> FactionCreationModel:
    """Load the packaged vocabulary, refusing a document that is not one."""
    target = Path(path) if path is not None else DATA_PATH
    with open(target, encoding="utf-8") as handle:
        data = json.load(handle)
    declared = data.get("format")
    if declared is not None and declared != CREATION_FORMAT:
        raise ValueError(f"not a NoöPunk faction-creation document: format={declared!r}")
    return creation_from_dict(data)
