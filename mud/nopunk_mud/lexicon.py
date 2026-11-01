"""Deterministic, spoiler-safe player lexicon for the single Finglish edition (#996, #1000).

The words are **not** kept here. `GLOSSARY.md` is the vocabulary source of truth, and
`tools/glossary_to_lexicon.py` generates `data/world/lexicon.json` from it. This module only reads that
generated file, so the game dictionary cannot drift away from the glossary: an entry the glossary does not
have does not exist, and a gated term stays silent until the story earns it.
"""
from __future__ import annotations

import json
import os
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

#: Overrides the generated-lexicon path. Useful for tests and for a packaged install.
ENV_PATH = "NOPUNK_LEXICON"
#: The generated artefact, relative to the repository root.
DEFAULT_PATH = Path("data") / "world" / "lexicon.json"

MISSING = "No public dictionary entry. Some terms may require investigation."


class LexiconError(RuntimeError):
    """The generated lexicon is absent or malformed."""


@dataclass(frozen=True)
class Term:
    """One headword, as the glossary defines it."""

    word: str
    meaning: str
    provenance: str
    register: str = "general"
    category: str = ""
    spoiler: str = "public"


def _fold(value: str) -> str:
    """Case- and diacritic-insensitive key, so `dosa` finds `dösä`."""
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).strip()


def _candidate_paths() -> list[Path]:
    override = os.environ.get(ENV_PATH)
    if override:
        return [Path(override)]
    here = Path(__file__).resolve()
    # repository layout: <root>/mud/nopunk_mud/lexicon.py
    return [here.parents[2] / DEFAULT_PATH, here.parents[1] / DEFAULT_PATH]


def _load() -> tuple[Term, ...]:
    for path in _candidate_paths():
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("format") != "nopunk-glossary-v1":
                raise LexiconError(f"{path}: unexpected lexicon format {data.get('format')!r}")
            return tuple(
                Term(
                    word=row["word"],
                    meaning=row["meaning"],
                    provenance=row.get("provenance", ""),
                    register=row.get("register", "general"),
                    category=row.get("category", ""),
                    spoiler=row.get("spoiler", "public"),
                )
                for row in data.get("terms", []))
    raise LexiconError(
        "generated lexicon not found; run python3 tools/glossary_to_lexicon.py "
        f"(looked in {', '.join(str(p) for p in _candidate_paths())})")


@lru_cache(maxsize=1)
def terms() -> tuple[Term, ...]:
    """Every headword the glossary defines, gated ones included."""
    return _load()


@lru_cache(maxsize=1)
def public_terms() -> tuple[Term, ...]:
    """The public subset. Gated terms are the story's, not the dictionary's."""
    return tuple(term for term in terms() if term.spoiler == "public")


#: Backwards-compatible view of the public vocabulary.
PUBLIC_TERMS = public_terms()


def _index() -> dict[str, Term]:
    return {_fold(term.word): term for term in public_terms()}


def lookup(query: str = "") -> str:
    """Explain a word in concise English, without progress or secret state.

    A gated word answers exactly as a word that does not exist, so the refusal cannot confirm that a secret is
    waiting to be unlocked.
    """
    query = query.strip()
    if not query:
        listing = ", ".join(term.word for term in public_terms())
        return f"Dictionary: {listing}\nUsage: dictionary <word or search>"

    needle = _fold(query)
    index = _index()
    exact = index.get(needle)
    matches = [exact] if exact else [
        term for term in public_terms()
        if needle in _fold(term.word) or needle in _fold(term.meaning)]
    if not matches:
        return MISSING
    return "\n".join(
        f"{term.word}: {term.meaning} [{term.provenance}; {term.register}]" for term in matches)
