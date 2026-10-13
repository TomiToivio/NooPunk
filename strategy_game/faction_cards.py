"""Faction cards: the four card types the faction game uses — schema and content, never mechanics.

Issue #346's acceptance criterion 4 asks to *specify the four card types: character, organization,
research and government influence, with minimal effects and interactions*. Before this layer only the
**character** family had a record (``strategy_game/characters.py`` + ``data/character_cards.json``,
issue #356); organization, research and government cards had no layer at all.

This module is that record layer and nothing more, and it keeps the character layer's discipline:

* :class:`FactionCard` is **content data**: no statistic is derived, no effect is applied, no action
  is resolved. Gates A–D in ``docs/RULE_SYSTEM_RESEARCH.md`` are open and ``AGENTS.md`` §4 reserves
  resolution, thresholds and effects to the author.
* the four types are **consumed, not restated**: the scope vocabulary is issue #346's ``TAG_SCOPES``
  (``faction_creation.py``) and the tag-kind vocabulary is ``characters.TAG_KINDS``. The character
  card stays in ``characters.py`` and is *referenced*, never duplicated here.
* the issue's *"minimal effects and interactions"* clause arrives as **declared** data with
  ``enforced: false``: the declared chain (a character leads an organization; an organization
  produces research; research improves advocacy or operations; agents use capabilities to gain
  government influence; government influence funds or restricts organizations and research) is
  transcribed so the container is legible, and the *effect* — what an interaction actually changes —
  is an explicit :data:`PENDING` author decision rather than an invented rule. **A container is not a
  rule**, so this layer does not claim to satisfy the "effects" half of criterion 4; it names the
  half that is structure and leaves the other one open.
* a card never carries a resolved effect or a numeric field: the projection onto the shared
  :class:`strategy_game.tabletop.cards.Card` leaves ``prerequisites`` and ``effects`` empty on
  purpose, exactly as :func:`strategy_game.characters.to_card` does.

The one gap the shared primitive shows is recorded rather than papered over: ``CardType`` has members
for ``character``, ``organization`` and ``research`` but **none** for ``government``, so a government
card is declared here and its projection onto the primitive is recorded as a dependency
(:data:`UNPROJECTABLE`) instead of extending the board layer's enum, which belongs to a sibling unit.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .characters import TAG_KINDS, Relationship as CardRelationship, Tag, slug
from .faction_creation import FactionCreationModel, load_faction_creation
from .provenance import Provenance, ProvenanceKind
from .tabletop.cards import Card, CardRole, CardType, CardVisibility

__all__ = [
    "CARD_TYPE_IDS",
    "CONTROL_STATES",
    "EFFECTS_ENFORCED",
    "FACTION_CARDS_FORMAT",
    "FACTION_CARDS_VERSION",
    "PROJECTABLE_TO_PRIMITIVE",
    "UNPROJECTABLE",
    "CardTypeSpec",
    "DeclaredInteraction",
    "FactionCard",
    "FactionCardError",
    "FactionCardModel",
    "faction_cards_from_dict",
    "load_faction_cards",
    "to_card",
]

#: The declared file format, so a caller cannot silently load a different document.
FACTION_CARDS_FORMAT = "noopunk.strategy_game.faction_cards"
#: Bumped when the entry shape changes incompatibly.
FACTION_CARDS_VERSION = 1

#: The four card types issue #346's criterion 4 names. Transcribed, not invented.
CARD_TYPE_IDS: tuple[str, ...] = ("character", "organization", "research", "government")

#: How a faction's tie to an organization or a jurisdiction may be described. Named positions,
#: transcribed from the issue's own wording: an organization "may be owned, allied, infiltrated or
#: patron-controlled"; a government relation is "collaboration, not political ownership"; influence
#: is "captured and contested" rather than an entire government being automatically owned.
CONTROL_STATES: tuple[str, ...] = (
    "owned",
    "allied",
    "infiltrated",
    "patron_controlled",
    "cooperating",
    "autonomous",
    "contested",
)

#: A faction card resolves no effect, ever. Present as a constant so a caller can read the fact.
EFFECTS_ENFORCED = False

#: The card types the shared tabletop primitive already has a member for, so a card projects cleanly.
PROJECTABLE_TO_PRIMITIVE: Mapping[str, CardType] = {
    "character": CardType.CHARACTER,
    "organization": CardType.ORGANIZATION,
    "research": CardType.RESEARCH,
}
#: The shared primitive declares no ``government`` member. Extending the enum would touch the board
#: layer's file, which belongs to a sibling unit, so the gap is recorded as a dependency here.
UNPROJECTABLE: tuple[str, ...] = ("government",)

#: Content keys that would mean a mechanic had crept into the data. Read by the shipped-data check
#: and mirrored in the module's own refusal below.
FORBIDDEN_CARD_KEYS: tuple[str, ...] = (
    "stat",
    "stats",
    "attributes",
    "skill",
    "skill_value",
    "target_number",
    "modifier",
    "difficulty",
    "dice",
    "threshold",
    "cost",
    "upkeep",
    "effects",
    "effect",
    "prerequisites",
)

_DEFAULT_DATA = Path(__file__).with_name("data") / "faction_cards.json"

#: Where the effects half of criterion 4 is left, with the reason. Read by the tests and by a caller.
PENDING: tuple[str, ...] = (
    "the_effect_of_each_declared_interaction",
    "whether_a_government_card_gains_a_shared_primitive_member",
)


class FactionCardError(ValueError):
    """Raised for a malformed faction card, specification or roster."""


def _strings(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    return tuple(str(item).strip() for item in value if str(item).strip())


def _records(value: Any) -> tuple[dict[str, Any], ...]:
    if value is None:
        return ()
    if isinstance(value, Mapping):
        return (dict(value),)
    return tuple(dict(item) for item in value if isinstance(item, Mapping))


@dataclass
class CardTypeSpec:
    """One of the four card types: what it represents, its tag scope, and what it may not carry.

    ``declared_function`` is the issue's own *illustrative mechanical function* column, carried
    verbatim and marked unenforced: it is what a reviewer asked to see, and it is **not** an effect
    this layer applies.
    """

    identifier: str
    label: str = ""
    represents: str = ""
    tag_scope: str = ""
    declared_function: str = ""
    declared_function_enforced: bool = False
    card_role: str = CardRole.PERSISTENT_RECORD.value
    control_states_apply: bool = False
    control_note: str = ""
    may_carry: tuple[str, ...] = ()
    may_not_carry: tuple[str, ...] = ()
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "represents": self.represents,
            "tag_scope": self.tag_scope,
            "declared_function": self.declared_function,
            "declared_function_enforced": self.declared_function_enforced,
            "card_role": self.card_role,
            "control_states_apply": self.control_states_apply,
            "control_note": self.control_note,
            "may_carry": list(self.may_carry),
            "may_not_carry": list(self.may_not_carry),
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class DeclaredInteraction:
    """One declared link between card types. A design claim, never an applied effect."""

    identifier: str
    label: str = ""
    source: str = ""
    target: str = ""
    via: str = ""
    enforced: bool = False
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier,
            "label": self.label,
            "source": self.source,
            "target": self.target,
            "via": self.via,
            "enforced": self.enforced,
            "reason": self.reason,
        }


@dataclass
class FactionCard:
    """One faction card. Content data: the schema has no numeric field and no resolved effect."""

    identifier: str
    card_type: str
    title: str
    summary: str = ""
    tags: tuple[Tag, ...] = ()
    #: Faction or organization that holds the card. A reference, or empty with a reason.
    owner_id: str = ""
    #: A named control state from :data:`CONTROL_STATES`, or empty with ``control_rationale``.
    control: str = ""
    control_rationale: str = ""
    #: Declared links to other card ids. Read as names, never followed as a rule.
    produces: tuple[str, ...] = ()
    consumes: tuple[str, ...] = ()
    relationships: tuple[CardRelationship, ...] = ()
    #: What happened — evidence-shaped, and kept apart from the field below.
    observable: tuple[str, ...] = ()
    #: What someone concludes from it. Attribution, and the thing a player may hold wrongly.
    inferences: tuple[str, ...] = ()
    visibility: CardVisibility = CardVisibility.PUBLIC
    #: Uninterpreted declared state (injury, availability, condition). Names, never magnitudes.
    state: dict[str, str] = field(default_factory=dict)
    provenance: Provenance = field(default_factory=Provenance)
    #: Citations for authored content. Required for an ``AUTHORED`` card.
    sources: tuple[str, ...] = ()
    gm_notes: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise FactionCardError("a card needs an identifier")
        if slug(self.identifier) != self.identifier:
            raise FactionCardError(f"identifier {self.identifier!r} must be a stable slug")
        if not str(self.title).strip():
            raise FactionCardError(f"card {self.identifier} needs a title")
        if self.card_type not in CARD_TYPE_IDS:
            raise FactionCardError(
                f"card {self.identifier}: card_type {self.card_type!r} is not one of the four "
                f"{CARD_TYPE_IDS}; a fifth card type is the author's to add"
            )
        for tag in self.tags:
            if tag.kind not in TAG_KINDS:
                raise FactionCardError(
                    f"card {self.identifier}: tag kind {tag.kind!r} is not one of {TAG_KINDS}"
                )
        if self.control and self.control not in CONTROL_STATES:
            raise FactionCardError(
                f"card {self.identifier}: control {self.control!r} is not one of {CONTROL_STATES}; a "
                "named position is required"
            )
        for key in self.state:
            if key in FORBIDDEN_CARD_KEYS:
                raise FactionCardError(
                    f"card {self.identifier}: state key {key!r} is a mechanic; declared state is a "
                    "name, and no magnitude or effect is approved"
                )
        if self.provenance.kind is ProvenanceKind.AUTHORED and not self.sources:
            raise FactionCardError(
                f"authored card {self.identifier} must cite its sources: canon is never invented"
            )

    # -- serialization ----------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.identifier,
            "card_type": self.card_type,
            "title": self.title,
            "summary": self.summary,
            "tags": [tag.to_dict() for tag in self.tags],
            "owner_id": self.owner_id,
            "control": self.control,
            "control_rationale": self.control_rationale,
            "produces": list(self.produces),
            "consumes": list(self.consumes),
            "relationships": [
                {"other_id": rel.other_id, "kind": rel.kind, "visibility": rel.visibility.value}
                for rel in self.relationships
            ],
            "observable": list(self.observable),
            "inferences": list(self.inferences),
            "visibility": self.visibility.value,
            "state": dict(self.state),
            "provenance": self.provenance.to_dict(),
            "sources": list(self.sources),
            "gm_notes": self.gm_notes,
        }
        payload.update(self.detail)
        return payload


def _card_from_dict(data: Mapping[str, Any]) -> FactionCard:
    """Build a card from a record. A forbidden mechanic key is refused by name, never carried."""
    if not isinstance(data, Mapping) or not data.get("id"):
        raise FactionCardError("a faction card needs an 'id'")
    for key in FORBIDDEN_CARD_KEYS:
        if key in data:
            raise FactionCardError(
                f"card {data.get('id')!r}: key {key!r} is a mechanic. A faction card carries names, "
                "tags and declared links; an effect or a statistic is unauthored"
            )
    known = {
        "id", "card_type", "title", "summary", "tags", "owner_id", "control", "control_rationale",
        "produces", "consumes", "relationships", "observable", "inferences", "visibility", "state",
        "provenance", "sources", "gm_notes",
    }
    return FactionCard(
        identifier=str(data["id"]),
        card_type=str(data.get("card_type") or ""),
        title=str(data.get("title") or ""),
        summary=str(data.get("summary") or ""),
        tags=tuple(
            Tag(str(item.get("kind", "")).strip(), str(item.get("value", "")).strip())
            for item in (data.get("tags") or [])
            if isinstance(item, Mapping)
        ),
        owner_id=str(data.get("owner_id") or ""),
        control=str(data.get("control") or ""),
        control_rationale=str(data.get("control_rationale") or ""),
        produces=_strings(data.get("produces")),
        consumes=_strings(data.get("consumes")),
        relationships=tuple(
            CardRelationship(
                other_id=str(item.get("other_id", "")).strip(),
                kind=str(item.get("kind", "")).strip(),
                visibility=CardVisibility(str(item.get("visibility", CardVisibility.PUBLIC.value))),
            )
            for item in (data.get("relationships") or [])
            if isinstance(item, Mapping)
        ),
        observable=_strings(data.get("observable")),
        inferences=_strings(data.get("inferences")),
        visibility=CardVisibility(str(data.get("visibility") or CardVisibility.PUBLIC.value)),
        state={str(k): str(v) for k, v in (data.get("state") or {}).items()},
        provenance=Provenance.from_dict(data.get("provenance")),
        sources=_strings(data.get("sources")),
        gm_notes=str(data.get("gm_notes") or ""),
        detail={key: value for key, value in data.items() if key not in known},
    )


@dataclass
class FactionCardModel:
    """The loaded card vocabulary: the four type specifications, the declared interactions, a roster.

    ``roster`` holds cards keyed by identifier. ``pending_author_decisions`` records what is open,
    each with the reason it is open — the same idiom as the council and founding-story layers.
    """

    specs: dict[str, CardTypeSpec] = field(default_factory=dict)
    spec_order: tuple[str, ...] = ()
    roster: dict[str, FactionCard] = field(default_factory=dict)
    control_states: tuple[str, ...] = ()
    interactions: tuple[DeclaredInteraction, ...] = ()
    pending_author_decisions: tuple[dict[str, Any], ...] = ()
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    visibility_policy: dict[str, Any] = field(default_factory=dict)
    detail: dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.roster)

    def __iter__(self):
        return iter(self.roster.values())

    # -- lookups ---------------------------------------------------------------------------

    def spec(self, card_type: str) -> CardTypeSpec:
        return self.specs[card_type]

    def get(self, identifier: str) -> FactionCard:
        try:
            return self.roster[identifier]
        except KeyError as exc:
            raise FactionCardError(f"no faction card {identifier!r} in the roster") from exc

    def by_type(self, card_type: str) -> tuple[FactionCard, ...]:
        return tuple(card for card in self.roster.values() if card.card_type == card_type)

    def interactions_from(self, card_type: str) -> tuple[DeclaredInteraction, ...]:
        return tuple(item for item in self.interactions if item.source == card_type)

    # -- validation ------------------------------------------------------------------------

    def validate(
        self,
        *,
        tag_model: FactionCreationModel | None = None,
        known_owner_ids: Iterable[str] | None = None,
    ) -> tuple[str, ...]:
        """Readable problems with the roster, empty when it is consistent.

        Checked: every card's type is one of the four; a named control state is declared; a card
        whose provenance is ``AUTHORED`` cites its sources; a tag attached at a scope the tag's own
        definition does not allow is refused (issue #346's scope rule, consumed from
        ``faction_creation.py`` rather than re-declared); ``produces``/``consumes`` and
        ``owner_id`` resolve when the caller supplies the known sets; and the declared interaction
        chain names only the four types.

        Nothing here judges balance, magnitude or consequence: there is no such quantity to judge.
        """
        problems: list[str] = []
        for card in self.roster.values():
            head = f"card {card.identifier}"
            if card.card_type not in CARD_TYPE_IDS:
                problems.append(
                    f"{head}: card_type {card.card_type!r} is not one of the four {CARD_TYPE_IDS}"
                )
            if card.control and card.control not in CONTROL_STATES:
                problems.append(
                    f"{head}: control {card.control!r} is not one of {CONTROL_STATES}"
                )
            if not card.control and not card.control_rationale.strip():
                problems.append(
                    f"{head}: no control state and no reason. An empty field needs a reason; leaving "
                    "it blank and silent is how an invented value gets in later"
                )
            if card.provenance.kind is ProvenanceKind.AUTHORED and not card.sources:
                problems.append(f"{head}: an authored card must cite its sources")
            if tag_model is not None:
                spec = self.specs.get(card.card_type)
                scope = spec.tag_scope if spec is not None else ""
                for tag in card.tags:
                    if tag.value in tag_model.tags and scope and not tag_model.validate_tag_scope(
                        tag.value, scope
                    ):
                        problems.append(
                            f"{head}: tag {tag.value!r} is not declared for scope {scope!r}; one "
                            "definition serves different scopes and they are not interchangeable"
                        )
            if card.owner_id and known_owner_ids is not None and card.owner_id not in set(
                known_owner_ids
            ):
                problems.append(f"{head}: owner {card.owner_id!r} is not a known faction id")
            for linked in (*card.produces, *card.consumes):
                if linked not in self.roster:
                    problems.append(
                        f"{head}: link {linked!r} does not resolve to a card in this roster; a "
                        "declared link is a name and must name something"
                    )
        for spec in self.specs.values():
            if spec.identifier not in CARD_TYPE_IDS:
                problems.append(
                    f"card type {spec.identifier!r} is not one of the four {CARD_TYPE_IDS}"
                )
            if spec.tag_scope and spec.tag_scope not in {*CARD_TYPE_IDS, "faction"}:
                problems.append(
                    f"card type {spec.identifier!r}: tag scope {spec.tag_scope!r} is off vocabulary"
                )
        for interaction in self.interactions:
            for endpoint in (interaction.source, interaction.target):
                if endpoint not in self.specs:
                    problems.append(
                        f"interaction {interaction.identifier!r}: endpoint {endpoint!r} is not a "
                        "declared card type"
                    )
            if not interaction.reason.strip():
                problems.append(
                    f"interaction {interaction.identifier!r}: no reason recorded for why it is "
                    "declared and not enforced"
                )
        return tuple(problems)

    # -- the player / GM split -------------------------------------------------------------

    def player_view(self, card: FactionCard, *, reveal_secrets: bool = False) -> dict[str, Any]:
        """A card as a starting UI may show it.

        The GM note is withheld by the **code** rather than by renderer discipline, mirroring
        ``characters.render_detail``. ``observable`` and ``inferences`` stay two separate lists:
        what happened and what someone concludes from it are different things.
        """
        payload = card.to_dict()
        payload["gm_notes"] = (
            card.gm_notes if reveal_secrets else "[redacted — pass reveal_secrets=True]"
        )
        return payload

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


def faction_cards_from_dict(data: Mapping[str, Any]) -> FactionCardModel:
    """Build the model from the packaged document shape."""
    specs: dict[str, CardTypeSpec] = {}
    order: list[str] = []
    for record in _records(data.get("card_types")):
        known = {
            "id", "label", "represents", "tag_scope", "declared_function",
            "declared_function_enforced", "card_role", "control_states_apply", "control_note",
            "may_carry", "may_not_carry", "note",
        }
        spec = CardTypeSpec(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            represents=str(record.get("represents") or ""),
            tag_scope=str(record.get("tag_scope") or ""),
            declared_function=str(record.get("declared_function") or ""),
            declared_function_enforced=bool(record.get("declared_function_enforced", False)),
            card_role=str(record.get("card_role") or CardRole.PERSISTENT_RECORD.value),
            control_states_apply=bool(record.get("control_states_apply", False)),
            control_note=str(record.get("control_note") or ""),
            may_carry=_strings(record.get("may_carry")),
            may_not_carry=_strings(record.get("may_not_carry")),
            note=str(record.get("note") or ""),
            detail={key: value for key, value in record.items() if key not in known},
        )
        specs[spec.identifier] = spec
        order.append(spec.identifier)

    roster = {card.identifier: card for card in (
        _card_from_dict(item) for item in _records(data.get("cards"))
    )}
    if len(roster) != len(_records(data.get("cards"))):
        raise FactionCardError("duplicate card identifier in the faction-card roster")

    interactions = tuple(
        DeclaredInteraction(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            source=str(record.get("source") or ""),
            target=str(record.get("target") or ""),
            via=str(record.get("via") or ""),
            enforced=bool(record.get("enforced", False)),
            reason=str(record.get("reason") or ""),
        )
        for record in _records(data.get("declared_interactions"))
    )

    return FactionCardModel(
        specs=specs,
        spec_order=tuple(order),
        roster=roster,
        control_states=_strings(data.get("control_states")),
        interactions=interactions,
        pending_author_decisions=_records(data.get("pending_author_decisions")),
        sources=_strings(data.get("sources")),
        provenance=Provenance.from_dict(data.get("provenance")),
        visibility_policy=dict(data.get("visibility_policy") or {}),
        detail={
            key: value
            for key, value in data.items()
            if key
            not in {
                "format", "version", "status", "sources", "provenance", "card_types",
                "control_states", "declared_interactions", "cards", "pending_author_decisions",
                "visibility_policy",
            }
        },
    )


def load_faction_cards(path: Path | str | None = None) -> FactionCardModel:
    """Load the packaged card vocabulary, checking its declared format and version."""
    source = Path(path) if path is not None else _DEFAULT_DATA
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise FactionCardError(f"faction-card data file not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise FactionCardError(f"{source} is not valid JSON: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise FactionCardError("the faction-card data file must contain a JSON object")
    declared = str(payload.get("format", "")).strip()
    if declared != FACTION_CARDS_FORMAT:
        raise FactionCardError(f"unexpected format {declared!r}; expected {FACTION_CARDS_FORMAT!r}")
    version = payload.get("version")
    if version != FACTION_CARDS_VERSION:
        raise FactionCardError(f"unexpected version {version!r}; expected {FACTION_CARDS_VERSION}")
    return faction_cards_from_dict(payload)


def to_card(card: FactionCard) -> Card:
    """Project a faction card onto the existing tabletop :class:`Card`.

    ``prerequisites`` and ``effects`` stay empty on purpose: a faction card declares *labels* and
    *links*, and turning one into a mechanism is gated work. A ``government`` card has no member on
    the primitive yet, so the projection refuses it by name rather than inventing a mapping — see
    :data:`UNPROJECTABLE`.
    """
    primitive_type = PROJECTABLE_TO_PRIMITIVE.get(card.card_type)
    if primitive_type is None:
        raise FactionCardError(
            f"card {card.identifier}: card type {card.card_type!r} has no member on the shared "
            f"Card primitive ({UNPROJECTABLE}); adding one would touch the board layer's file, so "
            "the gap is recorded as a dependency instead of guessed at"
        )
    return Card(
        identifier=card.identifier,
        card_type=primitive_type,
        title=card.title,
        role=CardRole.PERSISTENT_RECORD,
        text=card.summary,
        tags=tuple(f"{tag.kind}:{tag.value}" for tag in card.tags),
        owner_id=card.owner_id or None,
        visibility=card.visibility,
        provenance=card.provenance,
    )


def render_front(card: FactionCard) -> str:
    """The compact face: type, title, control and tags. Never prints the GM note."""
    lines = [f"{card.title} — {card.card_type}"]
    if card.owner_id:
        lines.append(f"held by: {card.owner_id}")
    if card.control:
        lines.append(f"control: {card.control}")
    if card.tags:
        lines.append("tags: " + ", ".join(f"{tag.kind}:{tag.value}" for tag in card.tags))
    return "\n".join(lines)


def tag_model() -> FactionCreationModel:
    """Issue #346's tag/scope vocabulary, so a card's tags can be scope-checked against one source."""
    return load_faction_creation()
