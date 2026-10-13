"""The codex: a lookup over entity records, with GM-only material structurally withheld.

The issue requires that the codex be a *Species/Entity Codex with discovery stages and conflicting human
research reports*, and that it "not spoil GM-only truths in player UI".

That last requirement is implemented as a filter over data rather than a convention in a template:

* :meth:`Codex.player_records` returns only the entries whose
  :attr:`~strategy_game.codex.entities.KnowledgeStatus` is player-visible;
* :meth:`Codex.player_view` returns an entry's payload with :attr:`EntityRecord.gm_secrets` removed;
* :meth:`Codex.player_payload` is the whole codex as a player would receive it.

A test asserts that a GM-only secret string appears nowhere in :meth:`Codex.player_payload`, so "the
player UI does not spoil it" is a property of the code, not a promise about a renderer.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from .entities import (
    CodexError,
    EntityDescriptor,
    EntityForm,
    EntityOntology,
    EntityRecord,
    KnowledgeStatus,
)


@dataclass
class Codex:
    """Entity records by identifier, with alias lookup and a player-facing projection."""

    entries: dict[str, EntityRecord] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.entries)

    def add(self, record: EntityRecord) -> EntityRecord:
        if record.identifier in self.entries:
            raise CodexError(f"the codex already holds an entry identified {record.identifier!r}")
        self.entries[record.identifier] = record
        return record

    def extend(self, records: Iterable[EntityRecord]) -> None:
        for record in records:
            self.add(record)

    # -- lookup ------------------------------------------------------------------------------------

    def get(self, key: str) -> EntityRecord:
        """Look up by identifier, display name or alias. Raises when nothing matches."""
        needle = str(key).strip().casefold()
        if key in self.entries:
            return self.entries[key]
        for record in self.entries.values():
            if record.knows(needle):
                return record
        raise CodexError(f"the codex has no entry matching {key!r}")

    def find(self, key: str) -> EntityRecord | None:
        try:
            return self.get(key)
        except CodexError:
            return None

    def by_ontology(self, ontology: EntityOntology) -> tuple[EntityRecord, ...]:
        return tuple(item for item in self.entries.values() if item.ontology is ontology)

    def by_form(self, form: EntityForm) -> tuple[EntityRecord, ...]:
        return tuple(item for item in self.entries.values() if item.form is form)

    def by_descriptor(self, descriptor: EntityDescriptor) -> tuple[EntityRecord, ...]:
        """Entries carrying a `RULEBOOK.md` §43.4 extended descriptor.

        Descriptors are a separate, non-exclusive axis from ``ontology`` (``EntityOntology``): an entry
        can be, say, Noetic *and* Collective, so this filters on the descriptor list rather than on the
        primary type.
        """
        return tuple(item for item in self.entries.values()
                     if descriptor in item.ontology_descriptors)

    def by_reveal_stage(self, stage: str) -> tuple[EntityRecord, ...]:
        needle = str(stage).strip().casefold()
        return tuple(item for item in self.entries.values()
                     if item.reveal_stage.strip().casefold() == needle)

    def by_knowledge_status(self, status: KnowledgeStatus) -> tuple[EntityRecord, ...]:
        return tuple(item for item in self.entries.values() if item.knowledge_status is status)

    def contested(self) -> tuple[EntityRecord, ...]:
        """Entries carrying rival hypotheses — the ones the issue wants left underdetermined."""
        return tuple(item for item in self.entries.values() if item.is_contested)

    def related(self, identifier: str) -> tuple[EntityRecord, ...]:
        """Entries this one names, that the codex actually holds. Unheld names are not invented."""
        record = self.get(identifier)
        found: list[EntityRecord] = []
        for name in record.related_entities:
            match = self.find(name)
            if match is not None and match.identifier != record.identifier:
                found.append(match)
        return tuple(found)

    # -- player-facing projection ------------------------------------------------------------------

    def player_records(self) -> tuple[EntityRecord, ...]:
        return tuple(item for item in self.entries.values() if item.knowledge_status.is_player_visible)

    def player_view(self, key: str) -> dict[str, Any]:
        """One entry as a player may see it: ``gm_secrets`` removed, everything else intact."""
        payload = self.get(key).to_dict()
        payload.pop("gm_secrets", None)
        return payload

    def player_payload(self) -> dict[str, Any]:
        """The whole codex stripped of GM-only entries and of every GM secret."""
        return {
            "entries": [self.player_view(item.identifier) for item in self.player_records()],
        }

    # -- serialization -----------------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {"entries": {key: self.entries[key].to_dict() for key in sorted(self.entries)}}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Codex:
        codex = cls()
        for key, payload in (data.get("entries") or {}).items():
            codex.entries[str(key)] = EntityRecord.from_dict(payload)
        return codex

    @classmethod
    def from_json(cls, text: str) -> Codex:
        return cls.from_dict(json.loads(text))

    @classmethod
    def from_path(cls, path: str | Path) -> Codex:
        """Load the codex data file. A missing file raises rather than yielding an empty codex."""
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, indent=2)


#: The codex data file shipped with the package.
CODEX_PATH = Path(__file__).resolve().parents[1] / "data" / "codex.json"


def load_codex(path: str | Path | None = None) -> Codex:
    """Load the shipped codex, or one from ``path``."""
    return Codex.from_path(CODEX_PATH if path is None else path)


__all__ = ["CODEX_PATH", "Codex", "load_codex"]
