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

:class:`EntityDescriptor` carries the **extended categories / descriptors** of `RULEBOOK.md` §43.4
(Process, Ecology, Assemblage, Collective, Geotic, Hybrid/Composite, Anomaly/Unclassified). They are
*descriptors*, not ontology values, because §43.4 itself says "some are better treated as cross-cutting
descriptors than as formal classes" — so they ride on top of :attr:`EntityRecord.ontology` instead of
replacing it. Transcribing them is not a taxonomy choice; whether any becomes a formal class (Process is
the one §43.4 names) is an author ruling, left PENDING.

:class:`ConsciousnessStatus` is the setting's posture on whether an entity is conscious, sharing the
vocabulary of the character-card layer (`strategy_game.characters.CONSCIOUSNESS_STATUSES`). It defaults
to ``unknown`` and is **never derived**: no method returns a boolean, and an in-world assertion
(``asserted_in_world``) requires a cited source, because the setting does not settle interiority
(`rulebook/6_PSYCHIC.md` §6.7.3). This is a posture, not a capability.

:attr:`EntityRecord.ontology` may be **absent** for a faction form — a ``polity`` or ``organization``
is not *a* body, and §43.4 forbids collapsing type into allegiance. Absence is recorded explicitly (a
``null`` with a stated :attr:`EntityRecord.ontology_absent_reason`), never left to look like a
substrate claim.

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


class EntityDescriptor(Enum):
    """The **extended categories / descriptors** of `RULEBOOK.md` §43.4.

    §43.4 lists these as "extended categories / descriptors; some are better treated as cross-cutting
    descriptors than as formal classes". They are transcribed from canon rather than invented, and they
    are carried as *descriptors* — a second, non-exclusive label on top of :class:`EntityOntology` —
    exactly because §43.4 declines to make most of them formal classes. §43.4's own worked example reads
    ``Noetic + Process + Collective + Distributed``, i.e. one primary type plus descriptors.

    Whether any of these (Process is the one §43.4 names as "the strongest candidate for an additional
    formal class") is later promoted to a fifth :class:`EntityOntology` value is an author ruling and is
    left **PENDING**; this enum makes the decision expressible without pre-empting it.
    """

    #: Intelligence primarily an ongoing process rather than a discrete organism.
    PROCESS = "process"
    #: The ecosystem is the relevant intelligent entity.
    ECOLOGY = "ecology"
    #: Intelligence emerging from heterogeneous interacting components.
    ASSEMBLAGE = "assemblage"
    #: Swarm, hive, civilisation-scale or distributed minds.
    COLLECTIVE = "collective"
    #: Consciousness/intelligence instantiated in apparently ordinary matter or planetary structures.
    GEOTIC = "geotic"
    #: A combination across substrate classes.
    HYBRID_OR_COMPOSITE = "hybrid_or_composite"
    #: A phenomenon whose ontology cannot be established reliably.
    ANOMALY_OR_UNCLASSIFIED = "anomaly_or_unclassified"


#: The declared value set, so callers can validate without constructing an enum member.
ENTITY_DESCRIPTORS: tuple[str, ...] = tuple(item.value for item in EntityDescriptor)


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


class ConsciousnessStatus(Enum):
    """The setting's posture on whether an entity is conscious — **never derived, never asserted**.

    The issue requires the model not to assert what the fiction cannot know, and `rulebook/6_PSYCHIC.md`
    §6.7.3 is explicit that no power, instrument or skill resolves whether an entity is conscious. So
    this is a *posture* with the same three values the character-card layer already uses
    (``strategy_game.characters.CONSCIOUSNESS_STATUSES``), keeping the two layers in one vocabulary:

    * :attr:`UNKNOWN` — the honest default. An unrecorded posture stays visibly unknown rather than
      inheriting the confidence of its neighbours, mirroring :attr:`KnowledgeStatus.UNKNOWN` and
      ``ProvenanceKind.UNKNOWN``.
    * :attr:`CONTESTED` — in-world readings disagree (the plasmoid case: physical existence is a
      different question from consciousness).
    * :attr:`ASSERTED_IN_WORLD` — someone *in the setting* claims it, which is why it needs a cited
      source; it is a claim, not the author's truth.

    **Nothing derives it.** No function returns a boolean and no property turns it into a truth value;
    the author's own truth, where it exists, belongs in :attr:`EntityRecord.gm_secrets`.
    """

    UNKNOWN = "unknown"
    CONTESTED = "contested"
    ASSERTED_IN_WORLD = "asserted_in_world"


#: The declared value set, so callers can validate without constructing an enum member.
CONSCIOUSNESS_STATUSES: tuple[str, ...] = tuple(item.value for item in ConsciousnessStatus)


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
    #: Primary classification. Revisable — see :attr:`alternative_ontologies`. **May be ``None``** for a
    #: faction form (a ``polity`` or ``organization`` is not *a* body); when absent,
    #: :attr:`ontology_absent_reason` must say why, so the absence reads as a stated fact rather than an
    #: unset default (the repo's own "a null with a reason rather than being filled in" convention).
    ontology: EntityOntology | None = EntityOntology.BIOLOGIC
    #: Required when :attr:`ontology` is absent. Empty otherwise.
    ontology_absent_reason: str = ""
    #: Rival hypotheses about what the entry is. The point of the field is that the primary may be wrong.
    alternative_ontologies: tuple[EntityOntology, ...] = ()
    #: The §43.4 **extended descriptors** carried on top of the primary ontology. Cross-cutting and
    #: non-exclusive: one entry may be, say, Noetic + Collective. Deliberately a separate axis from
    #: :attr:`ontology`, which stays the single primary reading.
    ontology_descriptors: tuple[EntityDescriptor, ...] = ()
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
    #: Whether *the entry itself* is asserted to be an entity at all — free text on purpose, mirroring
    #: :attr:`reveal_stage`. It exists so a record can say "phenomenon" or "not an entity" without
    #: forcing that claim into :class:`EntityForm` (the research record classifies black-eyed kids as a
    #: ``phenomenon`` and Black-eyed-kids/Cherubim as a ``manifestation``, neither of which is a form).
    #: No vocabulary is imposed: whether a phenomenon gets its own ``EntityForm`` value or a typed
    #: status field is an author ruling, left PENDING.
    entity_status: str = ""
    #: The setting's posture on whether this entity is conscious. Defaults to ``unknown`` and is never
    #: derived — see :class:`ConsciousnessStatus`.
    consciousness_status: ConsciousnessStatus = ConsciousnessStatus.UNKNOWN
    #: Load-bearing signifiers this entity expresses *non-equivalently* — the issue's pragmatics traps
    #: ("we", "gift", "weapon", "voluntary", "service", "harvest", "ownership", "individual"). Free text,
    #: like :attr:`communication_modes`; the conventional set is
    #: :data:`strategy_game.codex.translation.LOAD_BEARING_SIGNIFIERS`.
    referent_collisions: tuple[str, ...] = ()
    #: GM-only material. Never emitted by :meth:`player_view`.
    gm_secrets: str = ""
    art_direction: str = ""

    def __post_init__(self) -> None:
        if not str(self.identifier).strip():
            raise CodexError("an entity record needs a non-empty identifier")
        if not str(self.display_name).strip():
            raise CodexError(f"entity {self.identifier!r} needs a non-empty display name")
        if self.ontology is not None and not isinstance(self.ontology, EntityOntology):
            raise CodexError(
                f"entity {self.identifier!r} needs an EntityOntology or an explicit absence, "
                f"got {self.ontology!r}"
            )
        if not isinstance(self.form, EntityForm):
            raise CodexError(f"entity {self.identifier!r} needs an EntityForm, got {self.form!r}")
        if self.ontology is None:
            # Only a faction form may lack a substrate — a body always has one. And the absence must
            # be a stated fact, not a blank that a reader could mistake for a default.
            if self.form not in (EntityForm.POLITY, EntityForm.ORGANIZATION):
                raise CodexError(
                    f"entity {self.identifier!r}: ontology may be absent only for a polity or "
                    f"organization, not for form {self.form.value!r}; a body has a substrate"
                )
            if not str(self.ontology_absent_reason).strip():
                raise CodexError(
                    f"entity {self.identifier!r}: an absent ontology needs an "
                    "ontology_absent_reason, so the absence is a stated fact rather than a blank"
                )
        if not isinstance(self.knowledge_status, KnowledgeStatus):
            raise CodexError(
                f"entity {self.identifier!r} needs a KnowledgeStatus, got {self.knowledge_status!r}"
            )
        if not isinstance(self.consciousness_status, ConsciousnessStatus):
            raise CodexError(
                f"entity {self.identifier!r} needs a ConsciousnessStatus, got "
                f"{self.consciousness_status!r}"
            )
        if self.consciousness_status is ConsciousnessStatus.ASSERTED_IN_WORLD and not self.source_references:
            raise CodexError(
                f"entity {self.identifier!r}: claiming that a being is conscious needs a cited "
                "source; the setting does not settle interiority"
            )
        if self.ontology is not None and self.ontology in self.alternative_ontologies:
            raise CodexError(
                f"entity {self.identifier!r} lists its primary ontology {self.ontology.value!r} as an "
                "alternative hypothesis as well; alternatives must be the rival readings"
            )
        for name in ("aliases", "communication_modes", "faction_relationships", "manifestations",
                     "related_entities", "human_folklore_analogues", "source_references",
                     "referent_collisions"):
            setattr(self, name, _strings(getattr(self, name), name))
        descriptors = tuple(self.ontology_descriptors)
        for descriptor in descriptors:
            if not isinstance(descriptor, EntityDescriptor):
                raise CodexError(
                    f"entity {self.identifier!r} needs EntityDescriptor members, got {descriptor!r}"
                )
        if len(set(descriptors)) != len(descriptors):
            raise CodexError(
                f"entity {self.identifier!r} repeats an ontology descriptor; §43.4 descriptors are a set"
            )
        self.ontology_descriptors = descriptors
        self.reveal_stage = str(self.reveal_stage)
        self.entity_status = str(self.entity_status)
        self.ontology_absent_reason = str(self.ontology_absent_reason)

    @property
    def hypotheses(self) -> tuple[EntityOntology, ...]:
        """The primary reading first, then the rivals. What an uncertain entry actually offers.

        An entry with a recorded absent ontology (a polity) contributes no primary reading, only its
        rivals — the absence is the point, not a hidden default.
        """
        primary = () if self.ontology is None else (self.ontology,)
        return primary + self.alternative_ontologies

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
            "ontology": None if self.ontology is None else self.ontology.value,
            "ontology_absent_reason": self.ontology_absent_reason,
            "alternative_ontologies": [item.value for item in self.alternative_ontologies],
            "ontology_descriptors": [item.value for item in self.ontology_descriptors],
            "form": self.form.value,
            "phenotype": self.phenotype,
            "biology_or_substrate": self.biology_or_substrate,
            "cognition": self.cognition,
            "individuality": self.individuality,
            "communication_modes": list(self.communication_modes),
            "referent_collisions": list(self.referent_collisions),
            "origin_claims": self.origin_claims,
            "faction_relationships": list(self.faction_relationships),
            "manifestations": list(self.manifestations),
            "related_entities": list(self.related_entities),
            "human_folklore_analogues": list(self.human_folklore_analogues),
            "source_references": list(self.source_references),
            "knowledge_status": self.knowledge_status.value,
            "consciousness_status": self.consciousness_status.value,
            "reveal_stage": self.reveal_stage,
            "entity_status": self.entity_status,
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
        # A *present* null ontology means "absent with a reason" (a polity), which is different from a
        # *missing* key, which takes the historical default. Collapsing the two would re-introduce the
        # type/faction mix-up the field exists to prevent.
        if "ontology" in data and data.get("ontology") is None:
            ontology: EntityOntology | None = None
        else:
            ontology = _enum_value(
                EntityOntology, data.get("ontology"), EntityOntology.BIOLOGIC, "ontology"
            )
        return cls(
            identifier=str(data.get("identifier", "")),
            display_name=str(data.get("display_name", "")),
            aliases=tuple(data.get("aliases") or ()),
            ontology=ontology,
            ontology_absent_reason=str(data.get("ontology_absent_reason", "")),
            alternative_ontologies=tuple(
                _enum_value(EntityOntology, item, None, "alternative_ontologies")
                for item in raw_alternatives
            ),
            ontology_descriptors=tuple(
                _enum_value(EntityDescriptor, item, None, "ontology_descriptors")
                for item in (data.get("ontology_descriptors") or ())
            ),
            form=_enum_value(EntityForm, data.get("form"), EntityForm.SPECIES, "form"),
            phenotype=str(data.get("phenotype", "")),
            biology_or_substrate=str(data.get("biology_or_substrate", "")),
            cognition=str(data.get("cognition", "")),
            individuality=str(data.get("individuality", "")),
            communication_modes=tuple(data.get("communication_modes") or ()),
            referent_collisions=tuple(data.get("referent_collisions") or ()),
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
            consciousness_status=_enum_value(
                ConsciousnessStatus, data.get("consciousness_status"), ConsciousnessStatus.UNKNOWN,
                "consciousness_status",
            ),
            reveal_stage=str(data.get("reveal_stage", "")),
            entity_status=str(data.get("entity_status", "")),
            gm_secrets=str(data.get("gm_secrets", "")),
            art_direction=str(data.get("art_direction", "")),
        )
