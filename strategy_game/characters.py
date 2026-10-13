"""Character cards: reusable, data-driven game pieces — content and schema, never mechanics.

Issue #356 asks for three card families (canonical named characters, generic faction/civilian
archetypes, generic NHI exemplars), a shared schema, a template -> instance lifecycle,
visibility that can carry secrets without spoiling them, and filtering. This module is that
layer, and nothing more: **no statistic is derived, no roll is compared, no effect is applied,
no action is resolved.** Gates A-D in ``docs/RULE_SYSTEM_RESEARCH.md`` are open, and
``AGENTS.md`` §4 reserves resolution, thresholds and cadence to the author.

Design rules this module follows rather than restates:

* **Reuse the card primitive.** :class:`strategy_game.tabletop.cards.Card` already carries
  identity, a generic type (including ``CardType.CHARACTER``), tags, ``art_ref`` for placeholder
  art, structured-but-uninterpreted ``prerequisites``/``effects`` and a provenance record.
  :func:`to_card` projects a character onto it instead of adding a second card type.
* **Do not invent the NHI taxonomy.** ``data/codex.json`` already declares ``ontology`` =
  ``biologic`` / ``construct`` / ``noetic`` / ``plasmoid``, ``knowledge_status`` and
  ``alternative_ontologies``. :class:`NhiCategory` and :class:`ClaimStatus` mirror those value
  sets, and :func:`classification_from_codex_entry` *derives* a classification from a codex
  entry — so category, contested status and certainty are never a card author's assertion.
* **Do not invent the tag vocabulary.** ``TAG_KINDS`` mirrors issue #346's shared tag kinds
  (``data/faction_creation.json``); :func:`tag_vocabulary_matches` checks the two agree.
* **Unknown stays visible.** A card with no recorded origin keeps ``ProvenanceKind.UNKNOWN``,
  per :mod:`strategy_game.provenance`.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Mapping

from .provenance import Provenance, ProvenanceKind
from .tabletop.cards import Card, CardRole, CardType, CardVisibility

#: Data-file contract, checked by :func:`load_character_cards`.
CHARACTER_CARDS_FORMAT = "noopunk.strategy_game.character_cards"
#: Bumped when the entry shape changes incompatibly.
CHARACTER_CARDS_VERSION = 1


class CharacterError(ValueError):
    """Raised for a malformed character card or roster."""


class CharacterFamily(Enum):
    """The three families the issue names. A content category, not a mechanic."""

    CANONICAL = "canonical"
    ARCHETYPE = "archetype"
    NHI = "nhi"


CHARACTER_FAMILIES: tuple[str, ...] = tuple(family.value for family in CharacterFamily)


class NhiCategory(Enum):
    """The setting's four NHI categories, mirroring the codex ``ontology`` field.

    A category is *not* a species: a Grey, a mantid or an orb is not a whole category, and a
    card carries the category and the species reference separately.
    """

    BIOLOGIC = "biologic"
    CONSTRUCT = "construct"
    NOETIC = "noetic"
    PLASMOID = "plasmoid"


NHI_CATEGORIES: tuple[str, ...] = tuple(category.value for category in NhiCategory)


class ClaimStatus(Enum):
    """How well-established a claim about a card is, mirroring the codex ``knowledge_status``.

    The last three are *uncertain* claims: they stay readable precisely because the setting is
    about living with uncertainty. :data:`REDACTED_CLAIM_STATUSES` is what a renderer hides until
    asked, so card metadata cannot spoil a reveal.
    """

    CANON = "canon"
    PLAYER_KNOWN = "player_known"
    REPORTED_CLAIM = "reported_claim"
    RUMOUR = "rumour"
    SOURCE_MYTHOLOGY = "source_mythology"
    GM_TRUTH = "gm_truth"


CLAIM_STATUSES: tuple[str, ...] = tuple(status.value for status in ClaimStatus)

#: Claims a renderer redacts unless the caller explicitly asks for secrets.
REDACTED_CLAIM_STATUSES: tuple[ClaimStatus, ...] = (ClaimStatus.GM_TRUTH,)

#: The shared tag kinds declared by issue #346 (``data/faction_creation.json``).
TAG_KINDS: tuple[str, ...] = ("belief", "competence", "equipment", "relationship", "asset", "goal")

#: The action *labels* issue #356 lists for cards. Names only: nothing here resolves one.
DECLARED_ACTION_KINDS: tuple[str, ...] = (
    "investigation",
    "influence",
    "recruitment",
    "espionage",
    "field_operations",
    "cyber",
    "psi",
    "combat",
)

_DEFAULT_DATA = Path(__file__).with_name("data") / "character_cards.json"
_CODEX_DATA = Path(__file__).with_name("data") / "codex.json"
_FACTION_CREATION_DATA = Path(__file__).with_name("data") / "faction_creation.json"


def slug(text: str) -> str:
    """A stable, filesystem- and id-safe token for a label."""
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


@dataclass(frozen=True)
class Tag:
    """One typed tag. ``kind`` is what makes it self-describing; nothing interprets it."""

    kind: str
    value: str

    def __post_init__(self) -> None:
        if self.kind not in TAG_KINDS:
            raise CharacterError(f"unknown tag kind {self.kind!r}; expected one of {TAG_KINDS}")
        if not self.value.strip():
            raise CharacterError("a tag needs a non-empty value")

    def to_dict(self) -> dict[str, str]:
        return {"kind": self.kind, "value": self.value}


@dataclass(frozen=True)
class Relationship:
    """A tie to another card. The kind is a label; no rule reads it."""

    other_id: str
    kind: str
    visibility: CardVisibility = CardVisibility.PUBLIC

    def __post_init__(self) -> None:
        if not self.other_id.strip():
            raise CharacterError("a relationship needs an other_id")
        if not self.kind.strip():
            raise CharacterError("a relationship needs a kind label")


@dataclass(frozen=True)
class NhiClassification:
    """Category, species, hypotheses, allegiance and certainty — kept apart on purpose.

    ``contested`` is true when the codex entry lists an ``alternative_ontologies`` reading, so a
    disputed classification stays disputed instead of being flattened by the card.
    """

    category: NhiCategory
    species_ref: str
    origin_hypotheses: tuple[str, ...] = ()
    allegiances: tuple[str, ...] = ()
    claim_status: ClaimStatus = ClaimStatus.RUMOUR
    contested: bool = False
    reveal_stage: str = ""

    def __post_init__(self) -> None:
        if not self.species_ref.strip():
            raise CharacterError("an NHI classification needs a species_ref (codex identifier)")

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category.value,
            "species_ref": self.species_ref,
            "origin_hypotheses": list(self.origin_hypotheses),
            "allegiances": list(self.allegiances),
            "claim_status": self.claim_status.value,
            "contested": self.contested,
            "reveal_stage": self.reveal_stage,
        }


def classification_from_codex_entry(entry: Mapping[str, Any]) -> NhiClassification:
    """Derive a classification from a codex entry.

    Everything here comes from the entry: ``ontology`` gives the category,
    ``alternative_ontologies`` decides ``contested``, ``knowledge_status`` gives the claim
    status, ``faction_relationships`` the allegiances and ``origin_claims`` the hypotheses. A
    card therefore cannot upgrade a rumour into canon by asserting it.
    """
    ontology = str(entry.get("ontology", "")).strip()
    if ontology not in NHI_CATEGORIES:
        raise CharacterError(
            f"codex entry ontology {ontology!r} is not one of the four categories {NHI_CATEGORIES}"
        )
    status = str(entry.get("knowledge_status", "")).strip()
    if status not in CLAIM_STATUSES:
        raise CharacterError(f"codex knowledge_status {status!r} is not a known claim status")
    return NhiClassification(
        category=NhiCategory(ontology),
        species_ref=str(entry.get("identifier", "")).strip(),
        origin_hypotheses=_strings(entry.get("origin_claims")),
        allegiances=_strings(entry.get("faction_relationships")),
        claim_status=ClaimStatus(status),
        contested=bool(entry.get("alternative_ontologies")),
        reveal_stage=str(entry.get("reveal_stage", "")).strip(),
    )


@dataclass
class CharacterCard:
    """One character card. Content data: the schema has no numeric stat and no resolution."""

    identifier: str
    family: CharacterFamily
    display_name: str
    role: str = ""
    summary: str = ""
    faction_ids: tuple[str, ...] = ()
    tags: tuple[Tag, ...] = ()
    declared_actions: tuple[str, ...] = ()
    statuses: tuple[str, ...] = ()
    relationships: tuple[Relationship, ...] = ()
    visibility: CardVisibility = CardVisibility.PUBLIC
    claim_status: ClaimStatus | None = None
    nhi: NhiClassification | None = None
    #: Reference to artwork kept outside the card, so placeholder art can exist from day one.
    art_ref: str = ""
    #: Set on an instance made from a template; templates themselves leave it empty.
    template_id: str | None = None
    #: Declared progression fields (injury, loyalty, allegiance). Uninterpreted, like the rest.
    state: dict[str, str] = field(default_factory=dict)
    #: Where the card's content came from. Defaults to UNKNOWN on purpose.
    provenance: Provenance = field(default_factory=Provenance)
    #: Citations for authored content: issue numbers, repo documents, codex identifiers.
    sources: tuple[str, ...] = ()
    #: Author-facing note. Redacted by :func:`render_front` and by detail renders by default.
    gm_notes: str = ""

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CharacterError("a card needs an identifier")
        if slug(self.identifier) != self.identifier:
            raise CharacterError(f"identifier {self.identifier!r} must be a stable slug")
        if not str(self.display_name).strip():
            raise CharacterError(f"card {self.identifier} needs a display_name")
        for action in self.declared_actions:
            if action not in DECLARED_ACTION_KINDS:
                raise CharacterError(
                    f"card {self.identifier}: declared action {action!r} is not one of "
                    f"{DECLARED_ACTION_KINDS}"
                )
        if self.family is CharacterFamily.CANONICAL:
            if self.template_id:
                raise CharacterError("a canonical character is not an instance of a template")
            if not self.sources:
                raise CharacterError(
                    f"canonical card {self.identifier} must cite its sources: canon is never "
                    "invented"
                )
        if self.family is CharacterFamily.ARCHETYPE and self.nhi is not None:
            raise CharacterError("an archetype is not an NHI classification; use the nhi family")
        if self.family is CharacterFamily.NHI and self.nhi is None:
            raise CharacterError(
                f"NHI card {self.identifier} must carry a classification; category, species, "
                "hypotheses and certainty belong on the card"
            )

    # -- serialization ------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "identifier": self.identifier,
            "family": self.family.value,
            "display_name": self.display_name,
            "role": self.role,
            "summary": self.summary,
            "faction_ids": list(self.faction_ids),
            "tags": [tag.to_dict() for tag in self.tags],
            "declared_actions": list(self.declared_actions),
            "statuses": list(self.statuses),
            "relationships": [
                {"other_id": rel.other_id, "kind": rel.kind, "visibility": rel.visibility.value}
                for rel in self.relationships
            ],
            "visibility": self.visibility.value,
            "art_ref": self.art_ref,
            "state": dict(self.state),
            "sources": list(self.sources),
            "gm_notes": self.gm_notes,
            "provenance": self.provenance.to_dict(),
        }
        if self.claim_status is not None:
            data["claim_status"] = self.claim_status.value
        if self.nhi is not None:
            data["nhi"] = self.nhi.to_dict()
        if self.template_id is not None:
            data["template_id"] = self.template_id
        return data

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CharacterCard:
        if not isinstance(data, Mapping):
            raise CharacterError(f"a card must be a mapping, got {type(data).__name__}")
        family_value = str(data.get("family", "")).strip()
        if family_value not in CHARACTER_FAMILIES:
            raise CharacterError(f"unknown family {family_value!r}; expected {CHARACTER_FAMILIES}")
        visibility = str(data.get("visibility", CardVisibility.PUBLIC.value)).strip()
        province = data.get("provenance")
        nhi_raw = data.get("nhi")
        claim_raw = data.get("claim_status")
        return cls(
            identifier=str(data.get("identifier", "")).strip(),
            family=CharacterFamily(family_value),
            display_name=str(data.get("display_name", "")).strip(),
            role=str(data.get("role", "")).strip(),
            summary=str(data.get("summary", "")).strip(),
            faction_ids=_strings(data.get("faction_ids")),
            tags=tuple(
                Tag(str(item.get("kind", "")).strip(), str(item.get("value", "")).strip())
                for item in (data.get("tags") or [])
            ),
            declared_actions=_strings(data.get("declared_actions")),
            statuses=_strings(data.get("statuses")),
            relationships=tuple(
                Relationship(
                    other_id=str(item.get("other_id", "")).strip(),
                    kind=str(item.get("kind", "")).strip(),
                    visibility=CardVisibility(str(item.get("visibility", CardVisibility.PUBLIC.value))),
                )
                for item in (data.get("relationships") or [])
            ),
            visibility=CardVisibility(visibility),
            claim_status=ClaimStatus(str(claim_raw)) if claim_raw else None,
            nhi=NhiClassification(
                category=NhiCategory(str(nhi_raw.get("category", "")).strip()),
                species_ref=str(nhi_raw.get("species_ref", "")).strip(),
                origin_hypotheses=_strings(nhi_raw.get("origin_hypotheses")),
                allegiances=_strings(nhi_raw.get("allegiances")),
                claim_status=ClaimStatus(str(nhi_raw.get("claim_status", ClaimStatus.RUMOUR.value))),
                contested=bool(nhi_raw.get("contested")),
                reveal_stage=str(nhi_raw.get("reveal_stage", "")).strip(),
            )
            if isinstance(nhi_raw, Mapping)
            else None,
            art_ref=str(data.get("art_ref", "")).strip(),
            template_id=(str(data["template_id"]).strip() or None) if data.get("template_id") else None,
            state={str(k): str(v) for k, v in (data.get("state") or {}).items()},
            provenance=Provenance.from_dict(province) if isinstance(province, Mapping) else Provenance(),
            sources=_strings(data.get("sources")),
            gm_notes=str(data.get("gm_notes", "")),
        )


def to_card(card: CharacterCard) -> Card:
    """Project a character onto the existing tabletop :class:`Card`.

    The projection reuses the shared primitive — ``CardType.CHARACTER`` already exists and needs
    no sibling class. ``prerequisites`` and ``effects`` stay empty on purpose: a character card
    declares *labels*, and turning one into a mechanism is gated work.
    """
    return Card(
        identifier=card.identifier,
        card_type=CardType.CHARACTER,
        title=card.display_name,
        role=CardRole.PERSISTENT_RECORD,
        text=card.summary,
        art_ref=card.art_ref,
        tags=tuple(f"{tag.kind}:{tag.value}" for tag in card.tags),
        owner_id=card.faction_ids[0] if card.faction_ids else None,
        visibility=card.visibility,
        provenance=card.provenance,
    )


class CharacterRoster:
    """A loaded, validated set of cards with filtering, instantiation and rendering."""

    def __init__(
        self,
        cards: Iterable[CharacterCard],
        *,
        version: int = CHARACTER_CARDS_VERSION,
        sources: Iterable[str] = (),
        visibility_policy: Mapping[str, Any] | None = None,
    ) -> None:
        self.cards: dict[str, CharacterCard] = {}
        for card in cards:
            if card.identifier in self.cards:
                raise CharacterError(f"duplicate card identifier {card.identifier!r}")
            self.cards[card.identifier] = card
        self.version = version
        self.sources = tuple(sources)
        self.visibility_policy = dict(visibility_policy or {})

    def __len__(self) -> int:
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards.values())

    def get(self, identifier: str) -> CharacterCard:
        try:
            return self.cards[identifier]
        except KeyError as exc:
            raise CharacterError(f"no card {identifier!r} in the roster") from exc

    def filter(
        self,
        *,
        family: CharacterFamily | str | None = None,
        faction: str | None = None,
        tag: str | None = None,
        category: NhiCategory | str | None = None,
        role: str | None = None,
        text: str = "",
    ) -> tuple[CharacterCard, ...]:
        """Filter by family, affiliation, tag value, NHI category, role or free text."""
        want_family = CharacterFamily(family) if isinstance(family, str) and family else family
        want_category = NhiCategory(category) if isinstance(category, str) and category else category
        needle = text.strip().lower()
        out = []
        for card in self.cards.values():
            if want_family is not None and card.family is not want_family:
                continue
            if faction is not None and faction not in card.faction_ids:
                continue
            if tag is not None and not any(
                tag.lower() in (t.value.lower(), t.kind.lower()) for t in card.tags
            ):
                continue
            if want_category is not None and (card.nhi is None or card.nhi.category is not want_category):
                continue
            if role is not None and role.lower() not in card.role.lower():
                continue
            if needle and needle not in f"{card.display_name} {card.summary} {card.role}".lower():
                continue
            out.append(card)
        return tuple(out)

    def instantiate(
        self,
        template_id: str,
        *,
        display_name: str = "",
        identifier: str | None = None,
        faction_ids: Iterable[str] = (),
        statuses: Iterable[str] = (),
        state: Mapping[str, str] | None = None,
    ) -> CharacterCard:
        """Make an individual from a generic template.

        Only archetypes are instanced: a canonical character is a unique persistent identity, so
        duplicating one is refused rather than silently allowed.
        """
        template = self.get(template_id)
        if template.family is CharacterFamily.CANONICAL:
            raise CharacterError(
                f"{template_id!r} is a canonical character, not a template; canonical identities "
                "are not duplicated"
            )
        name = display_name.strip() or template.display_name
        raw_id = identifier.strip() if identifier else f"{template.identifier}_{slug(name)}"
        # Normalise before the uniqueness check: slug() collapses separators, so checking the raw
        # form would let a duplicate slip past and silently replace an existing card.
        new_id = slug(raw_id)
        if new_id in self.cards:
            raise CharacterError(f"identifier {new_id!r} already exists; instances are not duplicated")
        instance = CharacterCard(
            identifier=new_id,
            family=template.family,
            display_name=name,
            role=template.role,
            summary=template.summary,
            faction_ids=tuple(faction_ids) or template.faction_ids,
            tags=template.tags,
            declared_actions=template.declared_actions,
            statuses=tuple(statuses) or template.statuses,
            relationships=template.relationships,
            visibility=template.visibility,
            claim_status=template.claim_status,
            nhi=template.nhi,
            art_ref=template.art_ref,
            template_id=template.identifier,
            state=dict(state or {}),
            provenance=Provenance(kind=ProvenanceKind.GENERATED, note=f"instance of {template.identifier}"),
            sources=template.sources,
        )
        self.cards[instance.identifier] = instance
        return instance

    def validate(
        self,
        *,
        codex: Mapping[str, Mapping[str, Any]] | None = None,
        known_faction_ids: Iterable[str] | None = None,
    ) -> tuple[str, ...]:
        """Return the problems found, empty when the roster is consistent.

        With ``codex`` supplied, every NHI classification is checked against the real codex entry:
        the category must equal the entry's ``ontology`` and the claim status its
        ``knowledge_status``. With ``known_faction_ids`` supplied, affiliations must resolve.
        """
        problems: list[str] = []
        for card in self.cards.values():
            if card.nhi is not None and codex is not None:
                entry = codex.get(card.nhi.species_ref)
                if entry is None:
                    problems.append(f"{card.identifier}: NHI species_ref {card.nhi.species_ref!r} not in the codex")
                else:
                    derived = classification_from_codex_entry(entry)
                    if derived.category is not card.nhi.category:
                        problems.append(
                            f"{card.identifier}: category {card.nhi.category.value!r} contradicts codex "
                            f"ontology {derived.category.value!r}"
                        )
                    if derived.claim_status is not card.nhi.claim_status:
                        problems.append(
                            f"{card.identifier}: claim {card.nhi.claim_status.value!r} contradicts codex "
                            f"knowledge_status {derived.claim_status.value!r}"
                        )
                    if derived.contested != card.nhi.contested:
                        problems.append(
                            f"{card.identifier}: contested={card.nhi.contested} contradicts codex "
                            f"alternative_ontologies={list(entry.get('alternative_ontologies') or [])}"
                        )
                    if tuple(card.nhi.origin_hypotheses) != derived.origin_hypotheses:
                        problems.append(
                            f"{card.identifier}: origin hypotheses must quote the codex origin_claims "
                            "verbatim; a paraphrase or a truncation is a card inventing canon"
                        )
                    if tuple(card.nhi.allegiances) != derived.allegiances:
                        problems.append(
                            f"{card.identifier}: allegiances must quote the codex faction_relationships "
                            "verbatim"
                        )
            if known_faction_ids is not None:
                known = set(known_faction_ids)
                for faction_id in card.faction_ids:
                    if faction_id not in known:
                        problems.append(f"{card.identifier}: faction {faction_id!r} is not a known faction id")
        return tuple(problems)


def load_character_cards(path: Path | str | None = None) -> CharacterRoster:
    """Load the card data file and check its declared format and version."""
    source = Path(path) if path is not None else _DEFAULT_DATA
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CharacterError(f"character card data file not found: {source}") from exc
    except json.JSONDecodeError as exc:
        raise CharacterError(f"{source} is not valid JSON: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise CharacterError("the character card data file must contain a JSON object")
    declared_format = str(payload.get("format", "")).strip()
    if declared_format != CHARACTER_CARDS_FORMAT:
        raise CharacterError(f"unexpected format {declared_format!r}; expected {CHARACTER_CARDS_FORMAT!r}")
    version = payload.get("version")
    if version != CHARACTER_CARDS_VERSION:
        raise CharacterError(f"unexpected version {version!r}; expected {CHARACTER_CARDS_VERSION}")
    entries = [CharacterCard.from_dict(item) for item in (payload.get("entries") or [])]
    return CharacterRoster(
        entries,
        version=version,
        sources=_strings(payload.get("sources")),
        visibility_policy=payload.get("visibility_policy"),
    )


def codex_entry_map(path: Path | str | None = None) -> dict[str, dict[str, Any]]:
    """The codex entries by identifier, read from the same file the codex module loads."""
    source = Path(path) if path is not None else _CODEX_DATA
    payload = json.loads(source.read_text(encoding="utf-8"))
    entries = payload.get("entries") or {}
    return {str(key): dict(value) for key, value in entries.items() if isinstance(value, Mapping)}


def tag_vocabulary_matches(path: Path | str | None = None) -> bool:
    """True when :data:`TAG_KINDS` agrees with issue #346's declared tag kinds."""
    source = Path(path) if path is not None else _FACTION_CREATION_DATA
    payload = json.loads(source.read_text(encoding="utf-8"))
    declared = tuple(str(item.get("id", "")).strip() for item in (payload.get("tag_kinds") or []))
    return declared == TAG_KINDS


def render_front(card: CharacterCard) -> str:
    """The compact face: what a player reads at a glance. Never prints secrets."""
    lines = [f"{card.display_name} — {card.role or card.family.value}"]
    if card.faction_ids:
        lines.append("factions: " + ", ".join(card.faction_ids))
    if card.nhi is not None:
        contested = " (contested)" if card.nhi.contested else ""
        lines.append(f"category: {card.nhi.category.value}{contested} | claim: {card.nhi.claim_status.value}")
    if card.tags:
        lines.append("tags: " + ", ".join(f"{tag.kind}:{tag.value}" for tag in card.tags))
    if card.art_ref:
        lines.append(f"art: {card.art_ref}")
    return "\n".join(lines)


def render_detail(
    card: CharacterCard,
    *,
    reveal_secrets: bool = False,
    codex: Mapping[str, Mapping[str, Any]] | None = None,
    roster: CharacterRoster | None = None,
) -> str:
    """The expandable back: lore, relationships, certainty and the GM's note.

    A redacted claim status is withheld unless ``reveal_secrets`` is set, so a card's own
    metadata cannot spoil a reveal. With a codex mapping, the referenced entry expands the lore.
    """
    lines = [render_front(card), "", card.summary or "(no summary)"]
    if card.declared_actions:
        lines.append("may be used for: " + ", ".join(card.declared_actions))
    if card.statuses:
        lines.append("statuses: " + ", ".join(card.statuses))
    if card.state:
        lines.append("state: " + ", ".join(f"{k}={v}" for k, v in sorted(card.state.items())))
    if card.relationships:
        lines.append(
            "relationships: "
            + ", ".join(f"{rel.kind} -> {rel.other_id}" for rel in card.relationships)
        )
    if card.nhi is not None:
        nhi = card.nhi
        lines.append(
            f"NHI: category={nhi.category.value} species={nhi.species_ref} "
            f"certainty={nhi.claim_status.value} contested={nhi.contested} stage={nhi.reveal_stage or '-'}"
        )
        if nhi.origin_hypotheses:
            lines.append("origin hypotheses: " + ", ".join(nhi.origin_hypotheses))
        if nhi.allegiances:
            lines.append("allegiances: " + ", ".join(nhi.allegiances))
        if codex is not None:
            entry = codex.get(nhi.species_ref)
            if entry is not None:
                biology = str(entry.get("biology_or_substrate", "")).strip()
                if biology:
                    lines.append(f"lore: {biology}")
                if entry.get("art_direction"):
                    lines.append(f"art direction: {entry['art_direction']}")
    if card.sources:
        lines.append("sources: " + "; ".join(card.sources))
    if card.template_id:
        lines.append(f"instance of: {card.template_id}")
    if roster is not None and card.template_id:
        template = roster.get(card.template_id)
        lines.append(f"template: {template.display_name}")
    redacted = card.claim_status in REDACTED_CLAIM_STATUSES or (
        card.nhi is not None and card.nhi.claim_status in REDACTED_CLAIM_STATUSES
    )
    if card.gm_notes and (reveal_secrets or not redacted):
        lines.append(f"GM notes: {card.gm_notes}")
    elif card.gm_notes:
        lines.append("GM notes: [redacted — pass reveal_secrets=True]")
    return "\n".join(lines)
