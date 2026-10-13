"""Genre paradigms: the three technology domains and the six setting genres (issue #359).

Issue #359 introduces **Bionics** as a third technology of living, social and psychic worlds alongside
**Cybernetics** and **Psychotronics**, and adds six genre descriptors: Biopunk, Solarpunk, Nanopunk,
PSIpunk, UFOpunk and Xenopunk. This module carries that as data and enforces the three things in it
that are *rules of the record* rather than prose:

1. **The three domains are interacting, not mutually exclusive** — and the cybernetic/social row of the
   correspondence table is a game-design abstraction, never a claim that Luhmann's social communication
   is identical to computers. The Luhmannian distinction between biological, psychic and social systems
   stays a setting commitment, so no code here merges the domains into one tech tree.
2. **No genre spawns a game system.** The issue is explicit that the genres overlap without spawning
   separate systems, so :meth:`GenreParadigmsModel.systems_spawned_by_genres` must always be empty.
3. **A research tradition is never recorded as an achieved capability.** Rhine, Radin, Sheldrake and the
   Ganzfeld protocols are real investigative traditions; the setting's PSI paradigm is fiction. Every
   research-kind inspiration must therefore declare a :data:`CAPABILITY_STATUSES` value, and one that
   does not is reported as an unearned capability claim. That is the same never-upgrade rule the rest of
   this package applies to provenance.

Also recorded: **PSIpunk is a genre and not a new paradigm shift** (PSI and psychotronics already exist
as a paradigm), and **UFOpunk and Xenopunk are internal definitions** — the issue found no established
genre canon for those names, so they carry ``established_genre_canon: false`` rather than being asserted
as schools (with the prior, scattered uses it did find recorded separately in ``prior_uses``).

The issue's later sections are carried the same way, and the rules they share are the same rules:

4. **A lens is not a compulsory genre declaration.** The fourteen further lenses (Lunarpunk, Hopepunk,
   Cli-Fi, Silkpunk, Postcyberpunk, ...) are overlapping ways of reading the same six genres, so
   :meth:`GenreParadigmsModel.lenses_that_spawn_a_system` must also stay empty.
5. **No candidate paradigm is promoted.** The issue says a candidate becomes foundational only if it
   changes what society considers possible, creates distinctive factions and reshapes the loop —
   *"Otherwise use a genre lens, project, TAG or event."* So every candidate carries an explicit
   ``promotion`` status and the shipped record promotes none:
   :meth:`GenreParadigmsModel.promoted_paradigms` documents what would change if the author promotes one.
6. **A named event card or strategic project is a title, not an effect.** Every proposal must carry an
   empty ``effects``, so a card title cannot silently acquire a cost or an outcome:
   :meth:`GenreParadigmsModel.proposals_with_effects` reports any that does.
7. **A pressure axis is a pair of named positions**, never an ordered scale, so
   :meth:`GenreParadigmsModel.axes_that_are_not_pairs` must stay empty; whether any axis becomes a
   recorded tag set is the author's pending decision.

What this module is **not**: approved rules. `strategy_game/RULEBOOK.md` still says *NO RULES APPROVED*.
It defines no mechanic, no technology tree and no genre-specific subsystem. Standard library only.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .provenance import Provenance

__all__ = [
    "CAPABILITY_STATUSES",
    "CANDIDATE_KINDS",
    "DATA_PATH",
    "DOMAIN_IDS",
    "GENRE_FORMAT",
    "GENRE_IDS",
    "INSPIRATION_KINDS",
    "LENS_STATUSES",
    "PRIOR_USE_CLAIMS",
    "PROMOTION_STATUSES",
    "RESEARCH_KINDS",
    "CandidateParadigm",
    "FactionPressureAxis",
    "Genre",
    "GenreLens",
    "GenreParadigmsModel",
    "Inspiration",
    "PriorUse",
    "ProposedCard",
    "TechnologyDomain",
    "genre_paradigms_from_dict",
    "load_genre_paradigms",
]

#: The declared file format, so a caller cannot silently load a different document.
GENRE_FORMAT = "noopunk.strategy_game.genre_paradigms"

#: The packaged vocabulary.
DATA_PATH = Path(__file__).with_name("data") / "genre_paradigms.json"

#: The three technology domains the issue puts side by side.
DOMAIN_IDS: tuple[str, ...] = ("bionics", "psychotronics", "cybernetics")

#: The six genre descriptors.
GENRE_IDS: tuple[str, ...] = ("biopunk", "solarpunk", "nanopunk", "psipunk", "ufopunk", "xenopunk")

#: How an inspiration relates to reality.
INSPIRATION_KINDS: tuple[str, ...] = (
    "fiction",
    "real_research",
    "research_field",
    "research_tradition",
)

#: Kinds that describe real investigation rather than fiction, and therefore need a capability status.
RESEARCH_KINDS: tuple[str, ...] = ("real_research", "research_field", "research_tradition")

#: How firmly a real inspiration may be described. ``not_applicable`` belongs to fiction only.
CAPABILITY_STATUSES: tuple[str, ...] = (
    "early_research",
    "research_tradition",
    "visionary_proposal",
    "not_applicable",
)

#: What a further genre lens is: a way of reading the same six genres, never a seventh genre with rules.
LENS_STATUSES: tuple[str, ...] = (
    "primary_framing",
    "established_genre",
    "established_literary_movement",
    "established_mode",
    "self_defined_aesthetic",
    "retro_aesthetic",
    "emerging_aesthetic",
    "broad_tradition",
    "internal_descriptor",
)

#: A candidate paradigm is a technology or a social tendency, never a selected system.
CANDIDATE_KINDS: tuple[str, ...] = ("technology", "social")

#: How far a candidate has been taken. Only the author moves a candidate out of ``pending``.
PROMOTION_STATUSES: tuple[str, ...] = (
    "pending_author_decision",
    "promoted_foundational",
    "rejected_by_author",
    "merged_into_existing_domain",
)

#: What a prior use of a genre name establishes. ``false_match`` exists so a look-alike is recorded
#: rather than forgotten and later mistaken for support.
PRIOR_USE_CLAIMS: tuple[str, ...] = (
    "independent_attestation",
    "scattered_use",
    "false_match",
)


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
class TechnologyDomain:
    """One technology domain: what it spans, and that it is one of three that interact."""

    identifier: str
    label: str = ""
    domain: str = ""
    system_correspondence: str = ""
    paradigm_shift: bool = False
    scope: str = ""
    note: str = ""
    interacts_with: tuple[str, ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "domain": self.domain,
            "system_correspondence": self.system_correspondence,
            "paradigm_shift": self.paradigm_shift,
            "scope": self.scope,
            "note": self.note,
            "interacts_with": list(self.interacts_with),
        }
        payload.update(self.detail)
        return payload


@dataclass
class Genre:
    """One genre descriptor. A framing, never a rules subsystem."""

    identifier: str
    label: str = ""
    established_genre_canon: bool = False
    is_paradigm_shift: bool = False
    spawns_system: bool = False
    centres_on: tuple[str, ...] = ()
    definition: str = ""
    note: str = ""
    conflicts: tuple[str, ...] = ()
    overlaps: tuple[str, ...] = ()
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "established_genre_canon": self.established_genre_canon,
            "is_paradigm_shift": self.is_paradigm_shift,
            "spawns_system": self.spawns_system,
            "centres_on": list(self.centres_on),
            "definition": self.definition,
            "note": self.note,
            "conflicts": list(self.conflicts),
            "overlaps": list(self.overlaps),
        }
        payload.update(self.detail)
        return payload


@dataclass
class Inspiration:
    """An influence: fiction, or real work whose capability status must be declared."""

    identifier: str
    label: str = ""
    kind: str = "fiction"
    capability_status: str = ""
    genres: tuple[str, ...] = ()
    contributes: str = ""
    url: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def is_research(self) -> bool:
        return self.kind in RESEARCH_KINDS

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "kind": self.kind,
            "capability_status": self.capability_status,
            "genres": list(self.genres),
            "contributes": self.contributes,
            "url": self.url,
        }
        payload.update(self.detail)
        return payload


@dataclass
class GenreLens:
    """A further lens over the same six genres: Lunarpunk, Hopepunk, Cli-Fi, Silkpunk, and so on.

    The issue adds these "as overlapping lenses, not compulsory genre declarations", so a lens carries
    no rules, no prerequisite and no mechanic — and :meth:`GenreParadigmsModel.lenses_that_spawn_a_system`
    exists so a lens that acquired one would be reported rather than tolerated.
    """

    identifier: str
    label: str = ""
    status: str = ""
    spawns_system: bool = False
    adds: str = ""
    recommended_fiction: tuple[str, ...] = ()
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "status": self.status,
            "spawns_system": self.spawns_system,
            "adds": self.adds,
            "recommended_fiction": list(self.recommended_fiction),
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class CandidateParadigm:
    """A candidate transformation, recorded as a candidate and never as a foundational paradigm.

    ``attaches_to`` is the compact matrix the issue asks for: which of the three technology domains a
    candidate attaches to, which event cards it feeds, and which research it would unlock. The
    ``promotion`` field is the whole point of the type — it stays
    ``pending_author_decision`` until the author applies the issue's own design test.
    """

    identifier: str
    label: str = ""
    kind: str = "technology"
    priority: bool = False
    promotion: str = ""
    promotion_test: str = ""
    author_stated_use: str = ""
    attaches_to: tuple[str, ...] = ()
    research_unlocks: tuple[str, ...] = ()
    event_cards: tuple[str, ...] = ()
    fiction: tuple[str, ...] = ()
    game_facing_conflict: str = ""
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "kind": self.kind,
            "priority": self.priority,
            "promotion": self.promotion,
            "promotion_test": self.promotion_test,
            "author_stated_use": self.author_stated_use,
            "attaches_to": list(self.attaches_to),
            "research_unlocks": list(self.research_unlocks),
            "event_cards": list(self.event_cards),
            "fiction": list(self.fiction),
            "game_facing_conflict": self.game_facing_conflict,
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class FactionPressureAxis:
    """A pressure axis stated as two named poles. Not a scale, not a number, not a score."""

    identifier: str
    label: str = ""
    poles: tuple[str, ...] = ()
    recorded_as: str = ""
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "poles": list(self.poles),
            "recorded_as": self.recorded_as,
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class ProposedCard:
    """A named event-card idea or strategic project: a title with no effect.

    ``effects`` must stay empty. The issue supplies these as illustrations of what the paradigms could
    produce, and a title that came with a cost, an outcome or a threshold would be an unapproved
    mechanic arriving through a card name.
    """

    identifier: str
    label: str = ""
    genres: tuple[str, ...] = ()
    hook: str = ""
    alternatives: tuple[str, ...] = ()
    status: str = ""
    effects: tuple[Any, ...] = ()
    note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "genres": list(self.genres),
            "hook": self.hook,
            "alternatives": list(self.alternatives),
            "status": self.status,
            "effects": list(self.effects),
            "note": self.note,
        }
        payload.update(self.detail)
        return payload


@dataclass
class PriorUse:
    """One earlier use of a genre name, with the strength of the claim it supports."""

    identifier: str
    label: str = ""
    genre: str = ""
    claim: str = ""
    note: str = ""
    url: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.identifier,
            "label": self.label,
            "genre": self.genre,
            "claim": self.claim,
            "note": self.note,
            "url": self.url,
        }
        payload.update(self.detail)
        return payload


@dataclass
class GenreParadigmsModel:
    """The loaded vocabulary, and the three rules of the record it enforces."""

    technologies: dict[str, TechnologyDomain] = field(default_factory=dict)
    genres: dict[str, Genre] = field(default_factory=dict)
    inspirations: dict[str, Inspiration] = field(default_factory=dict)
    inspiration_order: tuple[str, ...] = ()
    genre_lenses: dict[str, GenreLens] = field(default_factory=dict)
    candidate_paradigms: dict[str, CandidateParadigm] = field(default_factory=dict)
    candidate_order: tuple[str, ...] = ()
    faction_pressure_axes: dict[str, FactionPressureAxis] = field(default_factory=dict)
    strategic_projects: dict[str, ProposedCard] = field(default_factory=dict)
    event_card_ideas: dict[str, ProposedCard] = field(default_factory=dict)
    prior_uses: dict[str, PriorUse] = field(default_factory=dict)
    prior_use_order: tuple[str, ...] = ()
    prior_use_reading: str = ""
    related_issues: tuple[dict[str, Any], ...] = ()
    system_distinction: dict[str, Any] = field(default_factory=dict)
    framing: dict[str, Any] = field(default_factory=dict)
    epistemic_rule: dict[str, Any] = field(default_factory=dict)
    open_questions: tuple[dict[str, Any], ...] = ()
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    detail: dict[str, Any] = field(default_factory=dict)

    # -- lookups ---------------------------------------------------------------------------

    def technology(self, domain_id: str) -> TechnologyDomain:
        return self.technologies[domain_id]

    def genre(self, genre_id: str) -> Genre:
        return self.genres[genre_id]

    def inspiration(self, inspiration_id: str) -> Inspiration:
        return self.inspirations[inspiration_id]

    def lens(self, lens_id: str) -> GenreLens:
        return self.genre_lenses[lens_id]

    def candidate(self, candidate_id: str) -> CandidateParadigm:
        return self.candidate_paradigms[candidate_id]

    def axis(self, axis_id: str) -> FactionPressureAxis:
        return self.faction_pressure_axes[axis_id]

    def project(self, project_id: str) -> ProposedCard:
        return self.strategic_projects[project_id]

    def event_card_idea(self, idea_id: str) -> ProposedCard:
        return self.event_card_ideas[idea_id]

    def candidates(self) -> tuple[CandidateParadigm, ...]:
        return tuple(self.candidate_paradigms[item] for item in self.candidate_order)

    def proposals(self) -> tuple[ProposedCard, ...]:
        """Strategic projects and event-card ideas together, projects first, in document order."""
        return tuple(self.strategic_projects.values()) + tuple(self.event_card_ideas.values())

    def inspirations_for_genre(self, genre_id: str) -> tuple[Inspiration, ...]:
        """Inspirations of one genre — an unknown genre raises rather than returning nothing."""
        if genre_id not in self.genres:
            raise KeyError(f"unknown genre: {genre_id!r}")
        return tuple(item for item in self.order() if genre_id in item.genres)

    def inspirations_for_kind(self, kind: str) -> tuple[Inspiration, ...]:
        return tuple(item for item in self.order() if item.kind == kind)

    def order(self) -> tuple[Inspiration, ...]:
        return tuple(self.inspirations[item] for item in self.inspiration_order)

    # -- the three rules of the record ------------------------------------------------------

    def systems_spawned_by_genres(self) -> tuple[str, ...]:
        """Rule 1: a genre is a descriptor, never a rules subsystem. This must stay empty."""
        return tuple(genre.identifier for genre in self.genres.values() if genre.spawns_system)

    def paradigm_shifts(self) -> tuple[str, ...]:
        """The technology domains that are paradigm shifts. Genres never are."""
        return tuple(
            technology.identifier for technology in self.technologies.values() if technology.paradigm_shift
        )

    def genre_paradigm_shifts(self) -> tuple[str, ...]:
        """Rule: PSIpunk is an explicit genre and NOT a new paradigm shift."""
        return tuple(genre.identifier for genre in self.genres.values() if genre.is_paradigm_shift)

    def unearned_capability_claims(self) -> tuple[str, ...]:
        """Rule 3: a real research tradition recorded without a capability status.

        An entry with a research ``kind`` and no ``capability_status`` would read as an achieved
        capability, which is exactly the upgrade the issue forbids. Fiction is exempt: its status is
        ``not_applicable`` by definition.
        """
        return tuple(
            item.identifier
            for item in self.order()
            if item.is_research and item.capability_status not in CAPABILITY_STATUSES
        )

    def domains_are_exclusive(self) -> bool:
        """Rule 2: the three domains interact. A record claiming exclusivity is a defect.

        A domain must name the *other* domains it interacts with, so the check subtracts the domain
        itself before deciding that an interaction is missing.
        """
        if self.system_distinction.get("domains_mutually_exclusive") is True:
            return True
        return any(
            (set(DOMAIN_IDS) - {technology.identifier}) - set(technology.interacts_with)
            for technology in self.technologies.values()
        )

    # -- the rules of the record, continued (the issue's later sections) ---------------------

    def lenses_that_spawn_a_system(self) -> tuple[str, ...]:
        """A further lens is a way of reading the six genres, never a seventh system."""
        return tuple(
            lens.identifier for lens in self.genre_lenses.values() if lens.spawns_system
        )

    def promoted_paradigms(self) -> tuple[str, ...]:
        """Candidates the record has promoted to a foundational paradigm. A promotion is the author's.

        The issue's own test gates promotion: a candidate must change what society considers possible,
        create distinctive factions and institutions, and materially reshape the shared strategy/RPG
        loop. This record applies no promotion, so the shipped answer is empty — and the method exists
        so a promotion cannot be recorded silently.
        """
        return tuple(
            candidate.identifier
            for candidate in self.candidates()
            if candidate.promotion == "promoted_foundational"
        )

    def candidates_without_a_promotion_status(self) -> tuple[str, ...]:
        """Every candidate must say where it stands, including *pending*."""
        return tuple(
            candidate.identifier
            for candidate in self.candidates()
            if candidate.promotion not in PROMOTION_STATUSES
        )

    def proposals_with_effects(self) -> tuple[str, ...]:
        """Rule 6: a named event card or strategic project carries no effect.

        The issue supplies these as titles and illustrations. A non-empty ``effects`` here would be a
        cost, an outcome or a threshold arriving through a card name — an unapproved mechanic.
        """
        return tuple(
            proposal.identifier for proposal in self.proposals() if proposal.effects
        )

    def axes_that_are_not_pairs(self) -> tuple[str, ...]:
        """Rule 7: a pressure axis is two named positions, never an ordered scale."""
        return tuple(
            axis.identifier for axis in self.faction_pressure_axes.values() if len(axis.poles) != 2
        )

    def prior_uses_claiming_established_canon(self) -> tuple[str, ...]:
        """A prior use may attest a name, appear scattered, or be a look-alike — never establish canon."""
        return tuple(
            use.identifier for use in self.prior_use_order_records() if use.claim not in PRIOR_USE_CLAIMS
        )

    def prior_use_order_records(self) -> tuple[PriorUse, ...]:
        return tuple(self.prior_uses[item] for item in self.prior_use_order)

    def genres_without_a_fiction_and_a_research_inspiration(self) -> tuple[str, ...]:
        """The issue asks for a fiction **and** a non-fiction catalogue per genre.

        A genre with only stories, or only researchers, is missing half of the issue's ask, so this
        reports it instead of leaving it to be noticed by hand.
        """
        missing: list[str] = []
        for genre_id in self.genres:
            items = self.inspirations_for_genre(genre_id)
            has_fiction = any(item.kind == "fiction" for item in items)
            has_research = any(item.is_research for item in items)
            if not (has_fiction and has_research):
                missing.append(genre_id)
        return tuple(missing)

    # -- reporting -------------------------------------------------------------------------

    def off_vocabulary(self) -> tuple[tuple[str, str, str], ...]:
        """``(record_id, field, value)`` for values outside the declared vocabularies, without raising."""
        out: list[tuple[str, str, str]] = []
        for genre_id, genre in self.genres.items():
            if genre_id not in GENRE_IDS:
                out.append((genre_id, "genre", genre_id))
            for technology_id in genre.centres_on:
                if technology_id not in DOMAIN_IDS:
                    out.append((genre_id, "centres_on", technology_id))
            for other in genre.overlaps:
                if other not in GENRE_IDS:
                    out.append((genre_id, "overlaps", other))
        for technology_id, technology in self.technologies.items():
            if technology_id not in DOMAIN_IDS:
                out.append((technology_id, "technology", technology_id))
            for other in technology.interacts_with:
                if other not in DOMAIN_IDS:
                    out.append((technology_id, "interacts_with", other))
        for item in self.order():
            if item.kind not in INSPIRATION_KINDS:
                out.append((item.identifier, "kind", item.kind))
            if item.capability_status and item.capability_status not in CAPABILITY_STATUSES:
                out.append((item.identifier, "capability_status", item.capability_status))
            for genre_id in item.genres:
                if genre_id not in GENRE_IDS:
                    out.append((item.identifier, "genres", genre_id))
        for lens_id, lens in self.genre_lenses.items():
            if lens.status not in LENS_STATUSES:
                out.append((lens_id, "lens_status", lens.status))
        for candidate in self.candidates():
            if candidate.kind not in CANDIDATE_KINDS:
                out.append((candidate.identifier, "candidate_kind", candidate.kind))
            if candidate.promotion not in PROMOTION_STATUSES:
                out.append((candidate.identifier, "promotion", candidate.promotion))
            for domain_id in candidate.attaches_to:
                if domain_id not in DOMAIN_IDS:
                    out.append((candidate.identifier, "attaches_to", domain_id))
            for idea_id in candidate.event_cards:
                if idea_id not in self.event_card_ideas:
                    out.append((candidate.identifier, "event_cards", idea_id))
        for proposal in self.proposals():
            for genre_id in proposal.genres:
                if genre_id not in GENRE_IDS:
                    out.append((proposal.identifier, "genres", genre_id))
        for use in self.prior_use_order_records():
            if use.genre not in GENRE_IDS:
                out.append((use.identifier, "genre", use.genre))
            if use.claim not in PRIOR_USE_CLAIMS:
                out.append((use.identifier, "claim", use.claim))
        return tuple(out)


def genre_paradigms_from_dict(data: dict[str, Any]) -> GenreParadigmsModel:
    """Build the model from the packaged document shape."""
    technologies: dict[str, TechnologyDomain] = {}
    for record in _records(data.get("technologies")):
        known = {
            "id", "label", "domain", "system_correspondence", "paradigm_shift", "scope", "note",
            "interacts_with",
        }
        technologies[str(record["id"])] = TechnologyDomain(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            domain=str(record.get("domain") or ""),
            system_correspondence=str(record.get("system_correspondence") or ""),
            paradigm_shift=bool(record.get("paradigm_shift")),
            scope=str(record.get("scope") or ""),
            note=str(record.get("note") or ""),
            interacts_with=_strings(record.get("interacts_with")),
            detail={k: v for k, v in record.items() if k not in known},
        )

    genres: dict[str, Genre] = {}
    for record in _records(data.get("genres")):
        known = {
            "id", "label", "established_genre_canon", "is_paradigm_shift", "spawns_system",
            "centres_on", "definition", "note", "conflicts", "overlaps",
        }
        genres[str(record["id"])] = Genre(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            established_genre_canon=bool(record.get("established_genre_canon")),
            is_paradigm_shift=bool(record.get("is_paradigm_shift")),
            spawns_system=bool(record.get("spawns_system")),
            centres_on=_strings(record.get("centres_on")),
            definition=str(record.get("definition") or ""),
            note=str(record.get("note") or ""),
            conflicts=_strings(record.get("conflicts")),
            overlaps=_strings(record.get("overlaps")),
            detail={k: v for k, v in record.items() if k not in known},
        )

    inspirations: dict[str, Inspiration] = {}
    order: list[str] = []
    for record in _records(data.get("inspirations")):
        inspiration_id = str(record["id"])
        if inspiration_id in inspirations:
            raise ValueError(f"duplicate inspiration id: {inspiration_id!r}")
        known = {"id", "label", "kind", "capability_status", "genres", "contributes", "url"}
        inspirations[inspiration_id] = Inspiration(
            identifier=inspiration_id,
            label=str(record.get("label") or ""),
            kind=str(record.get("kind") or "fiction"),
            capability_status=str(record.get("capability_status") or ""),
            genres=_strings(record.get("genres")),
            contributes=str(record.get("contributes") or ""),
            url=str(record.get("url") or ""),
            detail={k: v for k, v in record.items() if k not in known},
        )
        order.append(inspiration_id)

    lenses: dict[str, GenreLens] = {}
    for record in _records(data.get("genre_lenses")):
        known = {"id", "label", "status", "spawns_system", "adds", "recommended_fiction", "note"}
        lenses[str(record["id"])] = GenreLens(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            status=str(record.get("status") or ""),
            spawns_system=bool(record.get("spawns_system")),
            adds=str(record.get("adds") or ""),
            recommended_fiction=_strings(record.get("recommended_fiction")),
            note=str(record.get("note") or ""),
            detail={k: v for k, v in record.items() if k not in known},
        )

    candidates: dict[str, CandidateParadigm] = {}
    candidate_order: list[str] = []
    for record in _records(data.get("candidate_paradigms")):
        candidate_id = str(record["id"])
        if candidate_id in candidates:
            raise ValueError(f"duplicate candidate paradigm id: {candidate_id!r}")
        known = {
            "id", "label", "kind", "priority", "promotion", "promotion_test", "author_stated_use",
            "attaches_to", "research_unlocks", "event_cards", "fiction", "game_facing_conflict", "note",
        }
        candidates[candidate_id] = CandidateParadigm(
            identifier=candidate_id,
            label=str(record.get("label") or ""),
            kind=str(record.get("kind") or ""),
            priority=bool(record.get("priority")),
            promotion=str(record.get("promotion") or ""),
            promotion_test=str(record.get("promotion_test") or ""),
            author_stated_use=str(record.get("author_stated_use") or ""),
            attaches_to=_strings(record.get("attaches_to")),
            research_unlocks=_strings(record.get("research_unlocks")),
            event_cards=_strings(record.get("event_cards")),
            fiction=_strings(record.get("fiction")),
            game_facing_conflict=str(record.get("game_facing_conflict") or ""),
            note=str(record.get("note") or ""),
            detail={k: v for k, v in record.items() if k not in known},
        )
        candidate_order.append(candidate_id)

    axes: dict[str, FactionPressureAxis] = {}
    for record in _records(data.get("faction_pressure_axes")):
        known = {"id", "label", "poles", "recorded_as", "note"}
        axes[str(record["id"])] = FactionPressureAxis(
            identifier=str(record["id"]),
            label=str(record.get("label") or ""),
            poles=_strings(record.get("poles")),
            recorded_as=str(record.get("recorded_as") or ""),
            note=str(record.get("note") or ""),
            detail={k: v for k, v in record.items() if k not in known},
        )

    def proposals(key: str) -> dict[str, ProposedCard]:
        out: dict[str, ProposedCard] = {}
        for record in _records(data.get(key)):
            known = {"id", "label", "genres", "hook", "alternatives", "status", "effects", "note"}
            out[str(record["id"])] = ProposedCard(
                identifier=str(record["id"]),
                label=str(record.get("label") or ""),
                genres=_strings(record.get("genres")),
                hook=str(record.get("hook") or ""),
                alternatives=_strings(record.get("alternatives")),
                status=str(record.get("status") or ""),
                effects=tuple(record.get("effects") or ()),
                note=str(record.get("note") or ""),
                detail={k: v for k, v in record.items() if k not in known},
            )
        return out

    prior_uses: dict[str, PriorUse] = {}
    prior_use_order: list[str] = []
    prior_section = data.get("prior_uses") or {}
    if isinstance(prior_section, dict):
        prior_records = prior_section.get("entries") or ()
        prior_reading = str(prior_section.get("reading") or "")
    else:  # a bare list is accepted so the section shape can change without breaking a reader
        prior_records = prior_section
        prior_reading = ""
    for record in _records(prior_records):
        prior_id = str(record["id"])
        if prior_id in prior_uses:
            raise ValueError(f"duplicate prior-use id: {prior_id!r}")
        known = {"id", "label", "genre", "claim", "note", "url"}
        prior_uses[prior_id] = PriorUse(
            identifier=prior_id,
            label=str(record.get("label") or ""),
            genre=str(record.get("genre") or ""),
            claim=str(record.get("claim") or ""),
            note=str(record.get("note") or ""),
            url=str(record.get("url") or ""),
            detail={k: v for k, v in record.items() if k not in known},
        )
        prior_use_order.append(prior_id)

    return GenreParadigmsModel(
        technologies=technologies,
        genres=genres,
        inspirations=inspirations,
        inspiration_order=tuple(order),
        genre_lenses=lenses,
        candidate_paradigms=candidates,
        candidate_order=tuple(candidate_order),
        faction_pressure_axes=axes,
        strategic_projects=proposals("strategic_projects"),
        event_card_ideas=proposals("event_card_ideas"),
        prior_uses=prior_uses,
        prior_use_order=tuple(prior_use_order),
        prior_use_reading=prior_reading,
        related_issues=_records(data.get("related_issues")),
        system_distinction=dict(data.get("system_distinction") or {}),
        framing=dict(data.get("framing") or {}),
        epistemic_rule=dict(data.get("epistemic_rule") or {}),
        open_questions=_records(data.get("open_questions")),
        sources=_strings(data.get("sources")),
        provenance=Provenance.from_dict(data.get("provenance")),
        detail={
            key: value
            for key, value in data.items()
            if key
            not in {
                "format", "technologies", "genres", "inspirations", "system_distinction", "framing",
                "epistemic_rule", "open_questions", "sources", "provenance", "genre_lenses",
                "candidate_paradigms", "faction_pressure_axes", "strategic_projects",
                "event_card_ideas", "prior_uses", "related_issues",
            }
        },
    )


def load_genre_paradigms(path: Path | str | None = None) -> GenreParadigmsModel:
    """Load the packaged vocabulary, refusing a document that is not one."""
    target = Path(path) if path is not None else DATA_PATH
    with open(target, encoding="utf-8") as handle:
        data = json.load(handle)
    declared = data.get("format")
    if declared is not None and declared != GENRE_FORMAT:
        raise ValueError(f"not a NoöPunk genre-paradigm document: format={declared!r}")
    return genre_paradigms_from_dict(data)
