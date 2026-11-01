"""Player-facing strings: Finnish-first, with English placeholders (#980, #981, #950).

The MUD's primary language is Finnish, and **Tomi writes the Finnish**. This module exists so that rule is
enforced by the data model rather than remembered by well-meaning agents:

* An agent never authors ``fi``. An entry marked :data:`ENGLISH_PLACEHOLDER` must carry **empty** Finnish,
  and the catalogue refuses to store it otherwise. Agent English is a working text waiting for Tomi.
* Every string carries a status, so a mixed build is visibly mixed instead of accidentally so. Finnish next
  to English is the intended first version, not a bug.
* Resolving a locale never rewrites the catalogue. Falling back to English for display must not overwrite
  the Finnish Tomi wrote - a fallback is a rendering decision, not a data change.
* Keys are stable and language-neutral, so renaming nothing in the data lets a save survive localization.
* Everything is UTF-8 clean: ``ä ö å š ž`` survive a round trip.

A later, proper English localization is a separate, edited deliverable. The English here is not it.
"""
from __future__ import annotations

import json
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field, replace
from pathlib import Path

#: Finnish authored by Tomi. The only status that may carry Finnish.
TOMI_FINNISH = "tomi_finnish"
#: Agent English awaiting Tomi's Finnish. Never carries Finnish.
ENGLISH_PLACEHOLDER = "english_placeholder"
#: An edited English localization, later. Not today's working text.
APPROVED_ENGLISH = "approved_english"

STATUSES = (TOMI_FINNISH, ENGLISH_PLACEHOLDER, APPROVED_ENGLISH)

KEY_PATTERN = re.compile(r"^[a-z0-9]+(?:[._-][a-z0-9]+)*$")


class StringError(ValueError):
    """A string breaks the language contract."""


@dataclass(frozen=True)
class StringEntry:
    """One player-facing line.

    ``key`` is the stable, language-neutral identity used by state machines and saves. ``en`` is always the
    working text an agent can write; ``fi`` is Tomi's, and empty until he writes it.
    """

    key: str
    en: str
    fi: str = ""
    status: str = ENGLISH_PLACEHOLDER
    notes: str = ""
    author: str = "agent"


@dataclass(frozen=True)
class Resolved:
    """The text to show, and why it is that text."""

    text: str
    locale: str
    status: str
    fell_back: bool
    source_status: str


@dataclass
class StringCatalogue:
    """A validated set of player-facing strings."""

    entries: dict[str, StringEntry] = field(default_factory=dict)

    # -- construction -------------------------------------------------------------------------
    def add(self, entry: StringEntry) -> StringEntry:
        """Store one entry after checking it against the language contract."""
        if not KEY_PATTERN.match(entry.key):
            raise StringError(f"{entry.key!r}: keys are lowercase, dotted or dashed, and language-neutral")
        if entry.key in self.entries:
            raise StringError(f"{entry.key!r}: already defined")
        if entry.status not in STATUSES:
            raise StringError(f"{entry.key!r}: unknown status {entry.status!r}")
        if entry.status == ENGLISH_PLACEHOLDER and entry.fi.strip():
            raise StringError(
                f"{entry.key!r}: an agent-authored string must not contain Finnish. "
                "Leave `fi` empty and let Tomi write it.")
        if entry.status == TOMI_FINNISH and not entry.fi.strip():
            raise StringError(f"{entry.key!r}: marked as Tomi's Finnish but has no Finnish")
        if not entry.en.strip():
            raise StringError(f"{entry.key!r}: needs English working text for Tomi to work from")
        self.entries[entry.key] = entry
        return entry

    def define(self, key: str, en: str, **kwargs: str) -> StringEntry:
        """Convenience for the common case: an agent writes English and nothing else."""
        return self.add(StringEntry(key=key, en=en, **kwargs))

    # -- lookup -------------------------------------------------------------------------------
    def entry(self, key: str) -> StringEntry:
        try:
            return self.entries[key]
        except KeyError:
            raise StringError(f"{key!r}: no such string") from None

    def resolve(self, key: str, locale: str = "fi") -> Resolved:
        """The text for a locale.

        Finnish is preferred; when Tomi has not written it yet the English working text is shown and the
        result says it fell back. The catalogue is not modified.
        """
        if locale not in ("fi", "en"):
            raise StringError(f"unsupported locale {locale!r}")
        entry = self.entry(key)
        if locale == "en":
            return Resolved(entry.en, "en", entry.status, False, entry.status)
        if entry.fi.strip():
            return Resolved(entry.fi, "fi", entry.status, False, entry.status)
        return Resolved(entry.en, "en", ENGLISH_PLACEHOLDER, True, entry.status)

    def finish(self, key: str, fi: str, *, status: str = TOMI_FINNISH) -> StringEntry:
        """Attach Tomi's Finnish to an existing string.

        This is the only path that may add Finnish, and it is meant to be used with text he supplied. An
        agent calling it with invented Finnish is breaking the rule the rest of this module enforces.
        """
        entry = self.entry(key)
        updated = replace(entry, fi=fi, status=status,
                          author="tomi" if status == TOMI_FINNISH else entry.author)
        self.entries[key] = updated
        self.add_check(updated)
        return updated

    def add_check(self, entry: StringEntry) -> None:
        if entry.status == ENGLISH_PLACEHOLDER and entry.fi.strip():
            raise StringError(f"{entry.key!r}: English placeholder cannot carry Finnish")
        if entry.status == TOMI_FINNISH and not entry.fi.strip():
            raise StringError(f"{entry.key!r}: Tomi's Finnish must actually be Finnish")

    # -- reporting ----------------------------------------------------------------------------
    def pending_finnish(self) -> list[str]:
        """Keys waiting for Tomi. This is the translation work queue."""
        return sorted(key for key, entry in self.entries.items()
                      if entry.status == ENGLISH_PLACEHOLDER and not entry.fi.strip())

    def coverage(self) -> dict[str, int | float]:
        total = len(self.entries)
        written = sum(1 for e in self.entries.values() if e.fi.strip())
        return {"total": total, "finnish_written": written,
                "awaiting_tomi": total - written,
                "percent_finnish": round(100 * written / total, 1) if total else 0.0}

    # -- persistence --------------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {"format": "nopunk-strings-v1",
                "entries": [e.__dict__ for e in sorted(self.entries.values(), key=lambda e: e.key)]}

    def to_json(self, *, indent: int = 1) -> str:
        """UTF-8 JSON with the characters written as themselves, not escaped."""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent) + "\n"

    @classmethod
    def from_dict(cls, data: Mapping) -> StringCatalogue:
        catalogue = cls()
        for raw in data.get("entries", []):
            fields = {k: v for k, v in raw.items() if k in
                      {"key", "en", "fi", "status", "notes", "author"}}
            catalogue.add(StringEntry(**fields))
        return catalogue

    @classmethod
    def load(cls, path: Path | str) -> StringCatalogue:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def save(self, path: Path | str) -> None:
        Path(path).write_text(self.to_json(), encoding="utf-8")


def build(entries: Iterable[StringEntry]) -> StringCatalogue:
    catalogue = StringCatalogue()
    for entry in entries:
        catalogue.add(entry)
    return catalogue
