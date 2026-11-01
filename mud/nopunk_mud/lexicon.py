"""The in-game lexicon: an aid to understanding, not a translation (#996).

NoöPunk ships in one canonical language — NoöPunk Finglish — and will not be localized. That makes the
vocabulary load-bearing: a player meets words they cannot look up anywhere else and has to be able to ask
the game what they mean. This module is that answer.

Three rules shape it:

* **A gloss, never a translation.** Entries explain a term in English in a line or two. They do not carry
  translated scenes, and they are not a parallel language edition.
* **Provenance is stated, not implied.** A term is either *attested* contemporary/historical usage (which
  requires a source), an *author neologism* by Tomi, or *proposed*. Speculation must never be presented as
  etymology, so an `attested` entry without a source is refused outright.
* **Spoilers stay shut.** Public entries are always readable; `dossier` entries need progress to unlock.
  The dictionary must never leak the Noösphere/NHI revelations a scene is still holding back.

Determinism matters because the lexicon is content, not a service: identical input yields identical output,
search ordering is stable, and nothing here calls out to a model.
"""
from __future__ import annotations

import json
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path

#: A term from real, checkable usage — contemporary slang or historical Stadin slangi.
ATTESTED = "attested"
#: A term Tomi coined for NoöPunk.
AUTHOR_NEOLOGISM = "author_neologism"
#: A proposed expression, not yet adopted into canon.
PROPOSED = "proposed"

PROVENANCE = (ATTESTED, AUTHOR_NEOLOGISM, PROPOSED)

#: Readable from the start.
PUBLIC = "public"
#: Unlocked by game progress; never shown early.
DOSSIER = "dossier"

TIERS = (PUBLIC, DOSSIER)


class LexiconError(ValueError):
    """An entry breaks the lexicon contract."""


@dataclass(frozen=True)
class Entry:
    """One vocabulary item.

    ``gloss`` is a short English explanation, not a translated line of dialogue. ``source`` is required for
    attested usage and ignored otherwise.
    """

    term: str
    gloss: str
    register: str = "street"
    provenance: str = ATTESTED
    tier: str = PUBLIC
    source: str = ""
    notes: str = ""

    def label(self) -> str:
        """How the provenance reads to a player, without overclaiming."""
        return {
            ATTESTED: "attested usage",
            AUTHOR_NEOLOGISM: "NoöPunk coinage",
            PROPOSED: "provisional term",
        }[self.provenance]


def _fold(value: str) -> str:
    """Case- and diacritic-insensitive form, so `dösä` is findable as `dosa`."""
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def _validate(entry: Entry) -> None:
    if not entry.term.strip():
        raise LexiconError("an entry needs a term")
    if not entry.gloss.strip():
        raise LexiconError(f"{entry.term!r}: an entry needs an English gloss")
    if entry.provenance not in PROVENANCE:
        raise LexiconError(f"{entry.term!r}: unknown provenance {entry.provenance!r}")
    if entry.tier not in TIERS:
        raise LexiconError(f"{entry.term!r}: unknown tier {entry.tier!r}")
    if entry.provenance == ATTESTED and not entry.source.strip():
        raise LexiconError(
            f"{entry.term!r}: attested usage needs a source. A term with no evidence is "
            f"{PROPOSED!r}, and must not be presented as established usage.")


@dataclass
class Lexicon:
    """A validated, read-only vocabulary."""

    entries: dict[str, Entry] = field(default_factory=dict)

    # -- construction -------------------------------------------------------------------------
    def add(self, entry: Entry) -> Entry:
        _validate(entry)
        key = _fold(entry.term)
        if key in self.entries:
            raise LexiconError(f"{entry.term!r}: already defined")
        self.entries[key] = entry
        return entry

    @classmethod
    def from_dict(cls, data: Mapping) -> Lexicon:
        lexicon = cls()
        for raw in data.get("entries", []):
            fields = {k: v for k, v in raw.items()
                      if k in {"term", "gloss", "register", "provenance", "tier", "source", "notes"}}
            lexicon.add(Entry(**fields))
        return lexicon

    @classmethod
    def load(cls, path: Path | str) -> Lexicon:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    # -- lookup -------------------------------------------------------------------------------
    def lookup(self, term: str, *, unlocked: Iterable[str] = ()) -> Entry:
        """The entry for a term, if the player is allowed to see it."""
        entry = self.entries.get(_fold(term))
        if entry is None:
            raise LexiconError(f"{term!r}: not in the lexicon")
        if entry.tier == DOSSIER and _fold(entry.term) not in {_fold(u) for u in unlocked}:
            # Deliberately indistinguishable from "unknown": a refusal that names the term would confirm it.
            raise LexiconError(f"{term!r}: not in the lexicon")
        return entry

    def search(self, query: str, *, unlocked: Iterable[str] = (), limit: int = 20) -> list[Entry]:
        """Stable, deterministic search over terms and glosses."""
        needle = _fold(query.strip())
        if not needle:
            return []
        allowed = {_fold(t) for t in unlocked}
        hits = []
        for key in sorted(self.entries):
            entry = self.entries[key]
            if entry.tier == DOSSIER and key not in allowed:
                continue
            if needle in _fold(entry.term) or needle in _fold(entry.gloss):
                hits.append(entry)
        return hits[:max(0, limit)]

    def render(self, term: str, *, unlocked: Iterable[str] = ()) -> str:
        """A player-facing entry: term, gloss, provenance, and the rest of the line."""
        entry = self.lookup(term, unlocked=unlocked)
        line = f"{entry.term} ({entry.register}) — {entry.gloss}"
        return f"{line}\n  {entry.label()}"

    @property
    def public_terms(self) -> list[str]:
        return sorted(e.term for e in self.entries.values() if e.tier == PUBLIC)

    @property
    def locked_terms(self) -> list[str]:
        """Dossier terms. Exposed for tooling only — never render this to a player."""
        return sorted(e.term for e in self.entries.values() if e.tier == DOSSIER)

    def index(self) -> list[tuple[str, str]]:
        """``(term, register)`` for the browseable index, public only, in stable order."""
        return sorted((e.term, e.register) for e in self.entries.values() if e.tier == PUBLIC)


def build(entries: Sequence[Entry]) -> Lexicon:
    lexicon = Lexicon()
    for entry in entries:
        lexicon.add(entry)
    return lexicon
