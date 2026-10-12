"""The authored global faction roster as data (issues #328 and #329). No rules live here.

This module loads `data/global_factions.json`: the seven global paradigm factions the author
specified, condensed from his own text and nothing else. It is a **container and a reader**, not a
mechanic — it has no positions, thresholds, scores, transitions, actions or win conditions, and
`strategy_game/RULEBOOK.md` still says *no rules approved*.

Why a loader at all: the two issues state the same roster with different names, so a machine-
readable reconciliation lets the later V1 layers consume one list instead of two. Unknown fields are
**retained** rather than dropped, so a future author field survives until code catches up.

Provenance discipline (`docs/INTEGRATION_BOUNDARIES.md`): the roster is author-set setting canon, so
it defaults to :attr:`ProvenanceKind.AUTHORED` when the file says so and to `UNKNOWN` when it does
not — never silently promoted to evidence. A faction's stated PSI/NHI posture is that faction's
in-world *belief*, which is why the roster's evidence model keeps belief, testimony, allegation and
fact apart.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .provenance import Provenance

__all__ = [
    "ENTITY_KINDS",
    "PARADIGM_STANCES",
    "ROSTER_FORMAT",
    "FactionRoster",
    "GlobalFaction",
    "faction_from_dict",
    "load_roster",
    "roster_from_dict",
]

#: The declared file format, so a caller cannot silently load a different document.
ROSTER_FORMAT = "noopunk.strategy_game.global_factions"

#: The entity kinds #329 section 4.2 distinguishes. A faction's kind is structural, not a belief.
ENTITY_KINDS: tuple[str, ...] = (
    "human_ideological_formation",
    "nhi_aligned_formation",
    "latent_public",
)

#: The paradigm positions #329 section 4.1 keeps separate from the two conventional axes.
PARADIGM_STANCES: tuple[str, ...] = (
    "agi",
    "psi",
    "nhi",
    "confederacy_accession",
    "sovereignty_agency_consent",
)

#: Fields the loader lifts into typed attributes; everything else is retained in ``detail``.
_KNOWN_FACTION_FIELDS = frozenset(
    {"id", "label", "kind", "subtitle", "axis_defaults", "stances", "core_signifiers", "sources"}
)

#: The packaged roster document.
DATA_PATH = Path(__file__).with_name("data") / "global_factions.json"


@dataclass
class GlobalFaction:
    """One authored faction. Descriptive fields only — no quantity, no position, no mechanic."""

    identifier: str
    label: str
    kind: str
    subtitle: str = ""
    axis_defaults: dict[str, Any] = field(default_factory=dict)
    stances: dict[str, str] = field(default_factory=dict)
    signifiers: tuple[str, ...] = ()
    sources: tuple[str, ...] = ()
    provenance: Provenance = field(default_factory=Provenance)
    #: Every other authored field, retained verbatim so unknown material is never lost.
    detail: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Plain-JSON form: the retained detail with the typed fields written back over it."""
        payload = dict(self.detail)
        payload.update(
            {
                "id": self.identifier,
                "label": self.label,
                "kind": self.kind,
                "subtitle": self.subtitle,
                "axis_defaults": dict(self.axis_defaults),
                "stances": dict(self.stances),
                "core_signifiers": list(self.signifiers),
                "sources": list(self.sources),
            }
        )
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any], *, provenance: Provenance | None = None,
                  where: str = "faction") -> "GlobalFaction":
        if not isinstance(payload, dict):
            raise ValueError(f"{where} must be an object, got {type(payload).__name__}")
        for required in ("id", "label", "kind"):
            if required not in payload:
                raise ValueError(f"{where} is missing required field {required!r}")
        return cls(
            identifier=str(payload["id"]),
            label=str(payload["label"]),
            kind=str(payload["kind"]),
            subtitle=str(payload.get("subtitle", "")),
            axis_defaults=dict(payload.get("axis_defaults") or {}),
            stances=dict(payload.get("stances") or {}),
            signifiers=tuple(payload.get("core_signifiers") or ()),
            sources=tuple(payload.get("sources") or ()),
            provenance=provenance if provenance is not None else Provenance(),
            detail={k: v for k, v in payload.items() if k not in _KNOWN_FACTION_FIELDS},
        )


@dataclass
class FactionRoster:
    """The loaded roster. Read-only helpers only; nothing here decides an outcome."""

    format: str
    version: str
    status: str
    provenance: Provenance
    entity_kinds: tuple[str, ...]
    factions: tuple[GlobalFaction, ...]
    open_question_ids: tuple[str, ...] = ()
    #: The whole authored document, retained so nothing the author wrote is dropped.
    detail: dict[str, Any] = field(default_factory=dict)

    def by_id(self, identifier: str) -> GlobalFaction | None:
        """The faction with this id, or ``None``. Reads only."""
        for faction in self.factions:
            if faction.identifier == identifier:
                return faction
        return None

    def of_kind(self, kind: str) -> tuple[GlobalFaction, ...]:
        """Every faction of the given entity kind, in file order. Reads only."""
        return tuple(faction for faction in self.factions if faction.kind == kind)


def _kind_ids(payload: Any) -> tuple[str, ...]:
    """The declared kind ids, accepting either plain strings or ``{"id": ...}`` objects."""
    ids: list[str] = []
    for item in payload or ():
        entry = item.get("id") if isinstance(item, dict) else item
        if entry:
            ids.append(str(entry))
    return tuple(ids)


def faction_from_dict(payload: dict[str, Any], *, provenance: Provenance | None = None,
                      index: int = 0) -> GlobalFaction:
    """Build one faction, naming its position in the file when something is wrong."""
    return GlobalFaction.from_dict(payload, provenance=provenance, where=f"factions[{index}]")


def roster_from_dict(payload: dict[str, Any]) -> FactionRoster:
    """Build a roster from an already-parsed document, validating its declared format."""
    if not isinstance(payload, dict):
        raise ValueError(f"roster must be an object, got {type(payload).__name__}")
    declared = payload.get("format")
    if declared != ROSTER_FORMAT:
        raise ValueError(f"unexpected roster format {declared!r}; expected {ROSTER_FORMAT!r}")
    provenance = Provenance.from_dict(payload.get("provenance"))
    factions = tuple(
        faction_from_dict(item, provenance=provenance, index=index)
        for index, item in enumerate(payload.get("factions") or ())
    )
    questions = tuple(
        str(question.get("id"))
        for question in payload.get("open_questions") or ()
        if isinstance(question, dict) and question.get("id")
    )
    return FactionRoster(
        format=str(declared),
        version=str(payload.get("version", "")),
        status=str(payload.get("status", "")),
        provenance=provenance,
        entity_kinds=_kind_ids(payload.get("entity_kinds")),
        factions=factions,
        open_question_ids=questions,
        detail=dict(payload),
    )


def load_roster(path: str | Path | None = None) -> FactionRoster:
    """Load the roster document, defaulting to the one packaged with this module."""
    source = Path(path) if path is not None else DATA_PATH
    return roster_from_dict(json.loads(source.read_text(encoding="utf-8")))
