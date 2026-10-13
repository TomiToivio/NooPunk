"""NHI entity records for the NoöPunk codex (issue #348).

The issue asks for a data-driven catalogue of "beings, lineages, collective minds, manifestations and
engineered agents", organised into **Biologics, Noetics, Plasmoids and Constructs**, and it is explicit
that those four are *kinds of entity, NOT four political factions*: "A social memory complex is an
organizational/consciousness form, not necessarily a species. A Greys' synthetic drone might be a
Construct controlled by a biologic/Noetic operator."

Two modelling consequences follow, and both are in the types rather than in the prose:

* **Ontology and affiliation are independent axes.** :attr:`EntityRecord.ontology` is what the thing
  *is*; :attr:`EntityRecord.faction_relationships` is who it is bound to, if anyone. Nothing derives one
  from the other, which is what keeps "Orion-associated" from silently implying a morphology.
* **A primary category is revisable.** :attr:`EntityRecord.alternative_ontologies` carries rival
  hypotheses, because the issue asks to "allow primary category + alternative hypotheses + manifestation
  links" and to "avoid overdefining mysterious entities". An orb may be a device, an avatar, a
  misidentification or a phenomenon, and the record can say so.

:class:`EntityForm` keeps species, polity, organization, avatar, individual, vessel/technology and
mythonym apart, because the issue requires it: "Not everything gets a species card."

:class:`KnowledgeStatus` is the epistemic register the issue asks to distinguish, kept as **one field
with the issue's own six values** rather than a taxonomy of the author's invention. It deliberately
mixes provenance (what a claim *is*) with disclosure (whether the player may see it), because the issue
lists them together; :attr:`KnowledgeStatus.is_gm_only` and :attr:`KnowledgeStatus.is_player_visible`
make the disclosure half explicit so a UI can filter without guessing.

**No field here carries a capability, statistic or mechanical effect.** Those are reserved
(`AGENTS.md` §4, "NHI taxonomy or capabilities") and this module is where a later approved subsystem
would read its records from — not where it is decided.

Entity *content* is reviewed by the author, never by a test (#271). Only the behaviour of this code is
tested.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping


class CodexError(ValueError):
    """Raised for a malformed codex record."""


class EntityOntology(Enum):
    """The four kinds of entity the issue defines. Not political factions."""

    #: Embodied living entities. A physical appearance is not a definitive origin.
    BIOLOGIC = "biologic"
    #: Psychic / thought-form / astral / social-memory-complex manifestations.
    NOETIC = "noetic"
    #: Luminous / plasma-like or field-coherent phenomena; possible first-density elementals.
    PLASMOID = "plasmoid"
    #: Engineered physical or synthetic entities, vessels, androids, drones, thought-interface hardware.
    CONSTRUCT = "construct"


#: The declared value set, so callers can validate without constructing an enum member.
ENTITY_ONTOLOGIES: tuple[str, ...] = tuple(item.value for item in EntityOntology)


class EntityForm(Enum):
    """What kind of *thing* an entry is. Independent of ontology and of affiliation."""

    SPECIES = "species"
    POLITY = "polity"
    ORGANIZATION = "organization"
    AVATAR = "avatar"
    INDIVIDUAL = "individual"
    VESSEL_OR_TECHNOLOGY = "vessel_or_technology"
    #: A name that exists only as a myth or a label — a mythonym, not a taxon.
    MYTHONYM = "mythonym"


class KnowledgeStatus(Enum):
    """The epistemic register of an entry, using the six distinctions the issue names.

    :attr:`PLAYER_KNOWN` and :attr:`GM_TRUTH` are about *disclosure*; the others are about the claim's
    provenance. They are one field because the issue lists them as one set of things to keep apart, and
    the predicates below make the disclosure half explicit rather than implicit in the string.
    """

    #: Not yet classified. Deliberately the default, mirroring ``ProvenanceKind.UNKNOWN``: an
    #: unrecorded status stays visible rather than inheriting the confidence of its neighbours.
    UNKNOWN = "unknown"
    #: A reported claim — witness testimony, a sighting account, a document.
    REPORTED_CLAIM = "reported_claim"
    #: Source mythology: folklore, channeled material, religious iconography used as a creative source.
    SOURCE_MYTHOLOGY = "source_mythology"
    #: In-universe rumour within the setting.
    RUMOUR = "rumour"
    #: Known to the player.
    PLAYER_KNOWN = "player_known"
    #: GM-only truth: true in the fiction, not disclosed to the player.
    GM_TRUTH = "gm_truth"
    #: Approved NoöPunk canon.
    CANON = "canon"

    @property
    def is_gm_only(self) -> bool:
        """True when the entry must not be shown in a player-facing view."""
        return self is KnowledgeStatus.GM_TRUTH

    @property
    def is_player_visible(self) -> bool:
        return not self.is_gm_only


#: The declared value set, so callers can validate without constructing an enum member.
KNOWLEDGE_STATUSES: tuple[str, ...] = tuple(item.value for item in KnowledgeStatus)


def _strings(values: Iterable[Any], field_name: str) -> tuple[str, ...]:
    try:
        return tuple(str(value) for value in values)
    except TypeError as exc:
        raise CodexError(f"{field_name} must be an iterable of strings: {exc}") from exc


def _enum_value(enum_cls: type, value: Any, default: Any, field_name: str) -> Any:
    """Coerce a stored value to an enum member, raising when it is present but unrecognised.

    A missing value (``None``) takes ``default``. A *present* value that is not a member raises, so a
    typo cannot silently become a plausible default — the failure mode that would let a wrong
    classification enter the codex looking deliberate.
    """
    if value is None:
        return default
    allowed = enum_cls._value2member_map_
    text = str(value)
    if text in allowed:
        return allowed[text]
    raise CodexError(
        f"{field_name} = {text!r} is not one of {sorted(allowed)}; "
        "fix the data rather than letting a wrong value load as its default"
    )


@dataclass
class EntityRecord:
    """One codex entry.

    The field list is the one the issue specifies. Free-text fields are carried verbatim: the codex
    does not interpret a phenotype, a cognition or a source reference, and it never derives a
    capability from one.
    """

    identifier: str
    display_name: str
    #: Every other name the entry is known by. The issue expects "multiple human exonyms" and native
    #: names that may be unpronounceable.
    aliases: tuple[str, ...] = ()
    #: Primary classification. Revisable — see :attr:`alternative_ontologies`.
    ontology: EntityOntology = EntityOntology.BIOLOGIC
    #: Rival hypotheses about what the entry is. The point of the field is that the primary may be wrong.
    alternative_ontologies: tuple[EntityOntology, ...] = ()
    form: EntityForm = EntityForm.SPECIES
    phenotype: str = ""
    biology_or_substrate: str = ""
    cognition: str = ""
    individuality: str = ""
    #: How it communicates. Names from :class:`strategy_game.codex.translation.CommunicationMode` are
    #: the conventional set; the field stays free text so an entry is never forced into one.
    communication_modes: tuple[str, ...] = ()
    origin_claims: str = ""
    #: Affiliation is independent of ontology and of morphology, deliberately.
    faction_relationships: tuple[str, ...] = ()
    manifestations: tuple[str, ...] = ()
    related_entities: tuple[str, ...] = ()
    human_folklore_analogues: tuple[str, ...] = ()
    #: Citations. Real-world sources are recorded as text, per the issue's citation practice.
    source_references: tuple[str, ...] = ()
    knowledge_status: KnowledgeStatus = KnowledgeStatus.UNKNOWN
    #: Discovery stage label. Free text on purpose: no stage vocabulary is imposed here, so the entry
    #: carries whatever label the scenario uses (the issue's UCCC reveal order names three waves).
    reveal_stage: str = ""
    #: GM-only material. Never emitted by :meth:`player_view`.
    gm_secrets: str = ""
    art_direction: str = ""

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CodexError("an entity record needs a non-empty identifier")
        if not str(self.display_name).strip():
            raise CodexError(f"entity {self.identifier!r} needs a non-empty display name")
        if not isinstance(self.ontology, EntityOntology):
            raise CodexError(f"entity {self.identifier!r} needs an EntityOntology, got {self.ontology!r}")
        if not isinstance(self.form, EntityForm):
            raise CodexError(f"entity {self.identifier!r} needs an EntityForm, got {self.form!r}")
        if not isinstance(self.knowledge_status, KnowledgeStatus):
            raise CodexError(
                f"entity {self.identifier!r} needs a KnowledgeStatus, got {self.knowledge_status!r}"
            )
        if self.ontology in self.alternative_ontologies:
            raise CodexError(
                f"entity {self.identifier!r} lists its primary ontology {self.ontology.value!r} as an "
                "alternative hypothesis as well; alternatives must be the rival readings"
            )
        for name in ("aliases", "communication_modes", "faction_relationships", "manifestations",
                     "related_entities", "human_folklore_analogues", "source_references"):
            setattr(self, name, _strings(getattr(self, name), name))
        self.reveal_stage = str(self.reveal_stage)

    @property
    def hypotheses(self) -> tuple[EntityOntology, ...]:
        """The primary reading first, then the rivals. What an uncertain entry actually offers."""
        return (self.ontology,) + self.alternative_ontologies

    @property
    def is_contested(self) -> bool:
        return bool(self.alternative_ontologies)

    def knows(self, name: str) -> bool:
        """True if ``name`` is the display name or one of the aliases, case-insensitively."""
        needle = str(name).strip().casefold()
        return needle in {self.display_name.casefold(), *(a.casefold() for a in self.aliases)}

    # -- serialization ----------------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "identifier": self.identifier,
            "display_name": self.display_name,
            "aliases": list(self.aliases),
            "ontology": self.ontology.value,
            "alternative_ontologies": [item.value for item in self.alternative_ontologies],
            "form": self.form.value,
            "phenotype": self.phenotype,
            "biology_or_substrate": self.biology_or_substrate,
            "cognition": self.cognition,
            "individuality": self.individuality,
            "communication_modes": list(self.communication_modes),
            "origin_claims": self.origin_claims,
            "faction_relationships": list(self.faction_relationships),
            "manifestations": list(self.manifestations),
            "related_entities": list(self.related_entities),
            "human_folklore_analogues": list(self.human_folklore_analogues),
            "source_references": list(self.source_references),
            "knowledge_status": self.knowledge_status.value,
            "reveal_stage": self.reveal_stage,
            "gm_secrets": self.gm_secrets,
            "art_direction": self.art_direction,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> EntityRecord:
        """Rebuild from :meth:`to_dict` output.

        A **missing** key takes the default, so an older or newer record still loads. A key that is
        present but **unrecognised** raises instead of silently falling back: a typo'd ontology must not
        become ``BIOLOGIC``, because a wrong classification that looks deliberate is worse than a
        loading error.
        """
        raw_alternatives = data.get("alternative_ontologies") or ()
        return cls(
            identifier=str(data.get("identifier", "")),
            display_name=str(data.get("display_name", "")),
            aliases=tuple(data.get("aliases") or ()),
            ontology=_enum_value(
                EntityOntology, data.get("ontology"), EntityOntology.BIOLOGIC, "ontology"
            ),
            alternative_ontologies=tuple(
                _enum_value(EntityOntology, item, None, "alternative_ontologies")
                for item in raw_alternatives
            ),
            form=_enum_value(EntityForm, data.get("form"), EntityForm.SPECIES, "form"),
            phenotype=str(data.get("phenotype", "")),
            biology_or_substrate=str(data.get("biology_or_substrate", "")),
            cognition=str(data.get("cognition", "")),
            individuality=str(data.get("individuality", "")),
            communication_modes=tuple(data.get("communication_modes") or ()),
            origin_claims=str(data.get("origin_claims", "")),
            faction_relationships=tuple(data.get("faction_relationships") or ()),
            manifestations=tuple(data.get("manifestations") or ()),
            related_entities=tuple(data.get("related_entities") or ()),
            human_folklore_analogues=tuple(data.get("human_folklore_analogues") or ()),
            source_references=tuple(data.get("source_references") or ()),
            knowledge_status=_enum_value(
                KnowledgeStatus, data.get("knowledge_status"), KnowledgeStatus.UNKNOWN,
                "knowledge_status",
            ),
            reveal_stage=str(data.get("reveal_stage", "")),
            gm_secrets=str(data.get("gm_secrets", "")),
            art_direction=str(data.get("art_direction", "")),
        )
