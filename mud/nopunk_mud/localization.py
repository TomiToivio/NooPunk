"""Locale-aware MUD strings with a one-way Finnish rule (#980/#981).

The MUD is Finnish-first. Tomi authors Finnish; agents author English placeholders. This module
enforces the part code can enforce:

* a Finnish string may only be set with author ``tomi``;
* an English fallback can never overwrite Finnish;
* rendering falls back visibly (``[EN] ...``) instead of passing English off as Finnish;
* keys are language-neutral and UTF-8 safe.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, replace
from pathlib import Path

FI_AUTHOR = "tomi"
FALLBACK_MARKER = "[EN] "


class LocalizationError(ValueError):
    """A string or author would break the language policy."""


@dataclass(frozen=True)
class Entry:
    key: str
    en: str = ""
    fi: str = ""
    author_en: str = "agent"
    author_fi: str = ""
    status: str = "english_placeholder"  # english_placeholder | tomi_finnish | approved_english

    def json(self) -> dict:
        return {"en": self.en, "fi": self.fi, "author_en": self.author_en,
                "author_fi": self.author_fi, "status": self.status}


@dataclass(frozen=True)
class Rendered:
    key: str
    text: str
    locale: str
    fallback: bool


class Localization:
    """A bundle of keyed strings. No method lets an agent set Finnish."""

    def __init__(self, entries: dict[str, Entry] | None = None) -> None:
        self._entries: dict[str, Entry] = dict(entries or {})

    def __contains__(self, key: str) -> bool:
        return key in self._entries

    def add_english(self, key: str, text: str, *, author: str = "agent") -> Entry:
        """Add or replace an English placeholder. Finnish already present is untouched."""
        if not key or not key.strip():
            raise LocalizationError("a string needs a stable key")
        existing = self._entries.get(key)
        if existing is None:
            entry = Entry(key=key, en=text, author_en=author)
        else:
            entry = replace(existing, en=text, author_en=author,
                            status="english_placeholder" if not existing.fi else existing.status)
        self._entries[key] = entry
        return entry

    def set_finnish(self, key: str, text: str, *, author: str) -> Entry:
        """Set Tomi-authored Finnish. Any other author is refused, not silently accepted."""
        if author.strip().lower() != FI_AUTHOR:
            raise LocalizationError("only Tomi may author Finnish strings")
        entry = self._entries.get(key)
        if entry is None:
            entry = Entry(key=key, fi=text, author_fi=author, status="tomi_finnish")
        else:
            entry = replace(entry, fi=text, author_fi=author, status="tomi_finnish")
        self._entries[key] = entry
        return entry

    def render(self, key: str, locale: str = "fi") -> Rendered:
        entry = self._entries.get(key)
        if entry is None:
            raise LocalizationError(f"unknown string key {key!r}")
        if locale == "fi" and entry.fi:
            return Rendered(key, entry.fi, "fi", False)
        if not entry.en:
            raise LocalizationError(f"string {key!r} has no English fallback yet")
        text = FALLBACK_MARKER + entry.en if locale == "fi" else entry.en
        return Rendered(key, text, "en", locale == "fi")

    def to_json(self) -> str:
        return json.dumps({key: entry.json() for key, entry in sorted(self._entries.items())},
                          ensure_ascii=False, indent=2, sort_keys=True)

    @classmethod
    def from_json(cls, text: str) -> "Localization":
        raw = json.loads(text)
        entries = {key: Entry(key=key, **value) for key, value in raw.items()}
        for entry in entries.values():
            if entry.fi and entry.author_fi.strip().lower() != FI_AUTHOR:
                raise LocalizationError(f"{entry.key}: Finnish text is not authored by Tomi")
        return cls(entries)


def load(path: Path) -> Localization:
    return Localization.from_json(path.read_text(encoding="utf-8"))
