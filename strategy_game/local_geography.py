"""The Ukweli local geography as structure: the city, the islands, and the exclusion island (#324).

Issue #324 asks for **one modern city, several islands and 6-8 simple locations**, with one island in
the set marked restricted, and it leaves a set of naming and geography questions for the author. This
module is the **structural** half of that: it reads the live playable board
(``data/ukweli_local.json``) and the declared geography record (``data/ukweli_geography.json``) and
answers four questions **by reading, never by assuming**:

* which islands the record declares, which of them are playable, and which is the restricted /
  exclusion one - together with a **reason** where a declared island is not on the board, so the gap is
  recorded rather than hidden;
* what the state's official name is, and which register the everyday and informal forms occupy;
* what the Eldrich Island / Freedom Colony relation is - **reported as OPEN with its options**, never
  resolved, because issue #326 says the relation is undefined;
* which author decisions are still outstanding, recorded empty **with a reason**.

What this module is not
-----------------------

Not a rule and not a map engine. It computes no cost, no route, no travel time, no support, no
control and no victory; it declares no number, threshold, magnitude or scale
(``numeric_scale_approved`` stays false) and it resolves nothing. A **container is not a rule**: the
three options for the island relation are recorded as named strings so a later pass can act on the
author's ruling instead of re-deriving the question. ``strategy_game/RULEBOOK.md`` still says
**NO RULES APPROVED**, and this layer touches no engine behaviour.

Two separations the code keeps honest:

* **A declaration is not a board marker.** The record declares the island set; the board *may* carry
  ``island`` / ``access`` markers. Where a board marker exists it must **agree** with the declaration,
  and where it does not the declaration stands - a missing marker is *unrecorded*, never silently read
  as "not an island".
* **An absent island is accounted for.** A declared island that is not on the playable board must carry
  an ``absent_reason``, so "declared canon but not playable" is never mistaken for a node that was
  simply forgotten.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

__all__ = [
    "ACCESS_CLASSES",
    "BOARD_PATH",
    "DATA_PATH",
    "GEOGRAPHY_FORMAT",
    "GEOGRAPHY_VERSION",
    "NODE_BUDGET",
    "BoardPlace",
    "DeclaredIsland",
    "GeographyError",
    "LocalGeography",
    "NameRegister",
    "OpenRelation",
    "PendingDecision",
    "geography_from_dict",
    "load_local_geography",
]

#: Declared document type. A differently-typed file is not this record.
GEOGRAPHY_FORMAT = "noopunk.strategy_game.ukweli_geography"

#: Bumped when the record's shape changes incompatibly.
GEOGRAPHY_VERSION = 1

#: The packaged record, next to the other strategy-game data.
DATA_PATH = Path(__file__).with_name("data") / "ukweli_geography.json"

#: The live playable board this record cross-checks rather than restates.
BOARD_PATH = Path(__file__).with_name("data") / "ukweli_local.json"

#: The access classes a place may carry. ``open`` is ordinary play; ``restricted`` and ``prohibited``
#: are the two degrees of closure issue #325 names for the exclusion island.
ACCESS_CLASSES: tuple[str, ...] = ("open", "restricted", "prohibited")

#: The node envelope both issues state (``#322``: 5-8 districts; ``#325``: 6-8 location nodes).
NODE_BUDGET: tuple[int, int] = (5, 8)

#: Field-name fragments that would be a statistic. None may appear anywhere in the record.
_NUMERIC_FORBIDDEN: tuple[str, ...] = (
    "score",
    "strength",
    "rating",
    "threshold",
    "weight",
    "probability",
    "magnitude",
    "victory_points",
)


class GeographyError(ValueError):
    """Raised when the geography record cannot be read as this record."""


def _strings(value: Any) -> tuple[str, ...]:
    """Coerce a JSON list of scalars into a tuple of strings; never raise on shape."""
    if isinstance(value, str):
        return (value,) if value.strip() else ()
    if not isinstance(value, (list, tuple)):
        return ()
    return tuple(str(item) for item in value)


def _all_keys(value: Any) -> set[str]:
    """Every mapping key anywhere in a payload. Used only to look for a numeric-shaped name."""
    found: set[str] = set()
    if isinstance(value, Mapping):
        for key, item in value.items():
            found.add(str(key))
            found |= _all_keys(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            found |= _all_keys(item)
    return found


@dataclass(frozen=True)
class BoardPlace:
    """One node of the live playable board, as declared.

    ``island`` is ``None`` when the board declares no island marker for the node, and ``access`` is
    empty for the same reason: an unrecorded marker is *unknown*, never assumed to be ``open`` or to
    mean "not an island".
    """

    identifier: str
    label: str
    tags: tuple[str, ...] = ()
    island: bool | None = None
    access: str = ""

    @property
    def is_exclusion(self) -> bool:
        """True when the *board* marks the node closed. Absence is not a claim either way."""
        return self.access in ("restricted", "prohibited")


@dataclass(frozen=True)
class DeclaredIsland:
    """One island the record declares, and whether it is playable."""

    identifier: str
    label: str
    access: str
    on_playable_board: bool
    absent_reason: str = ""
    rationale: str = ""
    sources: tuple[str, ...] = ()

    @property
    def is_exclusion(self) -> bool:
        return self.access in ("restricted", "prohibited")


@dataclass(frozen=True)
class OpenRelation:
    """A relation the sources leave undefined, carried as named options + a resolution flag.

    ``resolved`` is ``True`` only once an author ruling is cited in ``ruling_source``. A relation that
    claims to be resolved without a cited ruling is a defect, which :meth:`LocalGeography.problems`
    reports rather than accepts.
    """

    identifier: str
    label: str
    resolved: bool = False
    ruling_source: str = ""
    options: tuple[str, ...] = ()
    note: str = ""
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier,
            "label": self.label,
            "resolved": self.resolved,
            "ruling_source": self.ruling_source,
            "options": list(self.options),
            "note": self.note,
            "sources": list(self.sources),
        }


@dataclass(frozen=True)
class NameRegister:
    """The state's naming registers: the official name, its source, and the informal forms."""

    official: str
    official_source: str
    everyday: tuple[str, ...] = ()
    informal: str = ""
    register_mapping_recorded: bool = False
    residual_pending: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PendingDecision:
    """An author decision, recorded empty with a reason and the container standing in for it."""

    identifier: str
    question: str
    why_not_decided: str = ""
    container_instead: str = ""
    sources: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier,
            "question": self.question,
            "why_not_decided": self.why_not_decided,
            "container_instead": self.container_instead,
            "sources": list(self.sources),
        }


@dataclass
class LocalGeography:
    """The read record: the board, the island set, the naming registers and the open questions."""

    format: str = GEOGRAPHY_FORMAT
    version: int = GEOGRAPHY_VERSION
    status: str = ""
    numeric_scale_approved: bool = False
    sources: tuple[str, ...] = ()
    places: tuple[BoardPlace, ...] = ()
    islands: tuple[DeclaredIsland, ...] = ()
    island_count_declared: int = 0
    island_count_on_board: int = 0
    island_envelope: tuple[int, int] = (0, 0)
    relations: tuple[OpenRelation, ...] = ()
    name_register: NameRegister | None = None
    party_labels: tuple[dict[str, Any], ...] = ()
    pending_decisions: tuple[PendingDecision, ...] = ()
    node_budget: tuple[int, int] = NODE_BUDGET
    detail: dict[str, Any] = field(default_factory=dict)

    # -- readings ------------------------------------------------------------
    def on_board(self, identifier: str) -> bool:
        """True when the identifier is a node of the live board."""
        return any(place.identifier == identifier for place in self.places)

    @property
    def board_ids(self) -> tuple[str, ...]:
        return tuple(place.identifier for place in self.places)

    @property
    def board_islands(self) -> tuple[DeclaredIsland, ...]:
        """The declared islands that are playable today. A reading, not a claim about the fiction."""
        return tuple(island for island in self.islands if island.on_playable_board)

    @property
    def off_board_islands(self) -> tuple[DeclaredIsland, ...]:
        """The declared islands that are canon but not playable. Each carries an absent_reason."""
        return tuple(island for island in self.islands if not island.on_playable_board)

    @property
    def board_exclusions(self) -> tuple[BoardPlace, ...]:
        """Board nodes the board itself marks closed. None is not the same as "no closed node"."""
        return tuple(place for place in self.places if place.is_exclusion)

    @property
    def exclusion_islands(self) -> tuple[DeclaredIsland, ...]:
        return tuple(island for island in self.islands if island.is_exclusion)

    def place(self, identifier: str) -> BoardPlace | None:
        return next((p for p in self.places if p.identifier == identifier), None)

    def declared_island(self, identifier: str) -> DeclaredIsland | None:
        return next((i for i in self.islands if i.identifier == identifier), None)

    def relation(self, identifier: str) -> OpenRelation | None:
        return next((r for r in self.relations if r.identifier == identifier), None)

    def unresolved_relations(self) -> tuple[OpenRelation, ...]:
        return tuple(relation for relation in self.relations if not relation.resolved)

    def unresolved_party_labels(self) -> tuple[dict[str, Any], ...]:
        return tuple(label for label in self.party_labels if not label.get("resolved", False))

    # -- validation ----------------------------------------------------------
    def problems(self) -> tuple[str, ...]:
        """Return the structural problems found; empty means the record is consistent.

        Every check here is a *shape, reference or agreement* check. None of them reads, applies or
        invents a rule, and none of them decides an author question.
        """
        problems: list[str] = []
        if self.format != GEOGRAPHY_FORMAT:
            problems.append(f"format is {self.format!r}, expected {GEOGRAPHY_FORMAT!r}")
        if self.version != GEOGRAPHY_VERSION:
            problems.append(f"version is {self.version!r}, expected {GEOGRAPHY_VERSION!r}")
        if self.numeric_scale_approved:
            problems.append(
                "numeric_scale_approved is true: no ordered or numeric scale is approved anywhere in "
                "this project, so the flag may not be raised by an unauthorised record"
            )

        low, high = self.node_budget
        count = len(self.places)
        if not low <= count <= high:
            problems.append(
                f"the board has {count} location nodes; the stated envelope is {low}-{high}"
            )
        seen: set[str] = set()
        for place in self.places:
            if place.identifier in seen:
                problems.append(f"duplicate board location id {place.identifier!r}")
            seen.add(place.identifier)
            if place.access and place.access not in ACCESS_CLASSES:
                problems.append(
                    f"{place.identifier}: access marker {place.access!r} not in {ACCESS_CLASSES}"
                )

        if not self.islands:
            problems.append("no island is declared; #324 requires 'multiple islands'")
        for island in self.islands:
            if island.access not in ACCESS_CLASSES:
                problems.append(f"{island.identifier}: access {island.access!r} not in {ACCESS_CLASSES}")
            if island.on_playable_board and island.identifier not in seen:
                problems.append(
                    f"{island.identifier}: declared as on the playable board but absent from the board"
                )
            if not island.on_playable_board and not island.absent_reason.strip():
                problems.append(
                    f"{island.identifier}: declared off the playable board without a reason; an absent "
                    "island must be accounted for"
                )

        exclusions = self.exclusion_islands
        if len(exclusions) != 1:
            problems.append(
                f"expected exactly one restricted / exclusion island, found {len(exclusions)}"
            )

        # A board marker must agree with the declaration. A missing marker is unrecorded, not a claim.
        for place in self.places:
            declared = self.declared_island(place.identifier)
            if place.island is True and declared is None:
                problems.append(
                    f"{place.identifier}: the board marks this node as an island but no island is "
                    "declared for it"
                )
            if place.island is False and declared is not None:
                problems.append(
                    f"{place.identifier}: the board denies island status for a declared island"
                )
            if place.access and declared is not None and place.access != declared.access:
                problems.append(
                    f"{place.identifier}: the board declares access {place.access!r} but the record "
                    f"declares {declared.access!r}"
                )
            if place.access and declared is None:
                problems.append(
                    f"{place.identifier}: the board marks this node {place.access!r} but no island is "
                    "declared for it"
                )

        if self.name_register is None:
            problems.append("the state's naming registers are not declared")
        else:
            if not self.name_register.official.strip():
                problems.append("the official name of the state is empty")
            if not self.name_register.official_source.strip():
                problems.append(
                    "the official name is asserted without a cited source: a name is canon and is "
                    "never invented"
                )

        for relation in self.relations:
            if relation.resolved and not relation.ruling_source.strip():
                problems.append(
                    f"{relation.identifier}: marked resolved without a cited author ruling"
                )
            if not relation.resolved and not relation.options:
                problems.append(
                    f"{relation.identifier}: unresolved and declares no options, so nothing is "
                    "offered for the author's ruling"
                )

        for decision in self.pending_decisions:
            if not decision.why_not_decided.strip():
                problems.append(
                    f"{decision.identifier}: an open decision must say WHY it is open"
                )

        for key in _all_keys(self.to_dict()):
            if any(bad in str(key) for bad in _NUMERIC_FORBIDDEN):
                problems.append(f"numeric-looking field {key!r} found in the record")

        return tuple(problems)

    # -- serialization -------------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "format": self.format,
            "version": self.version,
            "status": self.status,
            "numeric_scale_approved": self.numeric_scale_approved,
            "sources": list(self.sources),
            "board": {"node_budget": list(self.node_budget)},
            "places": [
                {
                    "id": place.identifier,
                    "label": place.label,
                    "tags": list(place.tags),
                    "island": place.island,
                }
                for place in self.places
            ],
            "islands": [
                {
                    "id": island.identifier,
                    "label": island.label,
                    "access": island.access,
                    "on_playable_board": island.on_playable_board,
                    "absent_reason": island.absent_reason,
                }
                for island in self.islands
            ],
            "island_count": {
                "declared": self.island_count_declared,
                "on_playable_board": self.island_count_on_board,
                "issue_envelope": list(self.island_envelope),
            },
            "relations": [relation.to_dict() for relation in self.relations],
            "party_labels": [dict(label) for label in self.party_labels],
            "pending_author_decisions": [d.to_dict() for d in self.pending_decisions],
        }
        if self.name_register is not None:
            payload["state_names"] = {
                "official": self.name_register.official,
                "official_source": self.name_register.official_source,
                "everyday_register": list(self.name_register.everyday),
                "informal_register": self.name_register.informal,
                "register_mapping_recorded": self.name_register.register_mapping_recorded,
                "residual_pending": dict(self.name_register.residual_pending),
            }
        payload.update(self.detail)
        return payload


def _place_from_board(record: Mapping[str, Any]) -> BoardPlace:
    island_raw = record.get("island")
    return BoardPlace(
        identifier=str(record.get("id", "")),
        label=str(record.get("label", "")),
        tags=_strings(record.get("tags")),
        island=(None if island_raw is None else bool(island_raw)),
        access=str(record.get("access", "") or ""),
    )


def _island_from_dict(record: Mapping[str, Any]) -> DeclaredIsland:
    return DeclaredIsland(
        identifier=str(record.get("id", "")),
        label=str(record.get("label", "")),
        access=str(record.get("access", "")),
        on_playable_board=bool(record.get("on_playable_board", False)),
        absent_reason=str(record.get("absent_reason", "")),
        rationale=str(record.get("rationale", "")),
        sources=_strings(record.get("sources")),
    )


def _relation_from_dict(record: Mapping[str, Any]) -> OpenRelation:
    return OpenRelation(
        identifier=str(record.get("id", "")),
        label=str(record.get("label", "")),
        resolved=bool(record.get("resolved", False)),
        ruling_source=str(record.get("ruling_source", "")),
        options=_strings(record.get("options")),
        note=str(record.get("note", "")),
        sources=_strings(record.get("sources")),
    )


def _decision_from_dict(record: Mapping[str, Any]) -> PendingDecision:
    return PendingDecision(
        identifier=str(record.get("id", "")),
        question=str(record.get("question", "")),
        why_not_decided=str(record.get("why_not_decided", "")),
        container_instead=str(record.get("container_instead", "")),
        sources=_strings(record.get("sources")),
    )


def geography_from_dict(
    data: Mapping[str, Any], board: Mapping[str, Any] | None = None
) -> LocalGeography:
    """Build a :class:`LocalGeography` from an already-parsed record (and optionally a board)."""
    if not isinstance(data, Mapping):
        raise GeographyError("the geography record must be a JSON object")
    board_places: tuple[BoardPlace, ...] = ()
    if isinstance(board, Mapping):
        board_places = tuple(
            _place_from_board(item)
            for item in (board.get("locations") or [])
            if isinstance(item, Mapping) and item.get("id")
        )
    names = data.get("state_names")
    count = data.get("island_count") or {}
    budget = (data.get("board") or {}).get("node_budget") or list(NODE_BUDGET)
    islands = tuple(
        _island_from_dict(item) for item in (data.get("islands") or []) if isinstance(item, Mapping)
    )
    on_board_ids = {place.identifier for place in board_places}
    return LocalGeography(
        format=str(data.get("format", "")),
        version=int(data.get("version", 0) or 0),
        status=str(data.get("status", "")),
        numeric_scale_approved=bool(data.get("numeric_scale_approved", False)),
        sources=_strings(data.get("sources")),
        places=board_places,
        islands=islands,
        island_count_declared=int(count.get("declared", len(islands)) or 0),
        island_count_on_board=int(
            count.get("on_playable_board", sum(1 for i in islands if i.identifier in on_board_ids)) or 0
        ),
        island_envelope=tuple(int(x) for x in (count.get("issue_envelope") or [0, 0])),  # type: ignore[arg-type]
        relations=tuple(
            _relation_from_dict(item) for item in (data.get("relations") or []) if isinstance(item, Mapping)
        ),
        name_register=(
            NameRegister(
                official=str(names.get("official", "")),
                official_source=str(names.get("official_source", "")),
                everyday=_strings(names.get("everyday_register")),
                informal=str(names.get("informal_register", "")),
                register_mapping_recorded=bool(names.get("register_mapping_recorded", False)),
                residual_pending=dict(names.get("residual_pending") or {}),
            )
            if isinstance(names, Mapping)
            else None
        ),
        party_labels=tuple(
            dict(item) for item in (data.get("party_labels") or []) if isinstance(item, Mapping)
        ),
        pending_decisions=tuple(
            _decision_from_dict(item)
            for item in (data.get("pending_author_decisions") or [])
            if isinstance(item, Mapping)
        ),
        node_budget=(int(budget[0]), int(budget[1])),
    )


def load_local_geography(
    path: Path | str | None = None, board_path: Path | str | None = None
) -> LocalGeography:
    """Read the packaged record and the live board, and check the record's declared format."""
    target = Path(path) if path is not None else DATA_PATH
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise GeographyError(f"geography record not found: {target}") from exc
    except json.JSONDecodeError as exc:
        raise GeographyError(f"{target} is not valid JSON: {exc}") from exc

    declared = str(data.get("format", ""))
    if declared != GEOGRAPHY_FORMAT:
        raise GeographyError(f"unexpected format {declared!r}; expected {GEOGRAPHY_FORMAT!r}")

    source = Path(board_path) if board_path is not None else BOARD_PATH
    try:
        board = json.loads(source.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise GeographyError(f"the playable board could not be read at {source}: {exc}") from exc
    return geography_from_dict(data, board)
