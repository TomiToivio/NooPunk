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
as schools.

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
    "DATA_PATH",
    "DOMAIN_IDS",
    "GENRE_FORMAT",
    "GENRE_IDS",
    "INSPIRATION_KINDS",
    "RESEARCH_KINDS",
    "Genre",
    "GenreParadigmsModel",
    "Inspiration",
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
class GenreParadigmsModel:
    """The loaded vocabulary, and the three rules of the record it enforces."""

    technologies: dict[str, TechnologyDomain] = field(default_factory=dict)
    genres: dict[str, Genre] = field(default_factory=dict)
    inspirations: dict[str, Inspiration] = field(default_factory=dict)
    inspiration_order: tuple[str, ...] = ()
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

    return GenreParadigmsModel(
        technologies=technologies,
        genres=genres,
        inspirations=inspirations,
        inspiration_order=tuple(order),
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
                "epistemic_rule", "open_questions", "sources", "provenance",
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
