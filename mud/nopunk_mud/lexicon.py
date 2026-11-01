"""Deterministic, spoiler-safe player lexicon for the single Finglish edition."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Term:
    word: str
    meaning: str
    provenance: str
    register: str = "general"

# Public terms only. Classified revelations belong in progress-gated dossiers, never here.
PUBLIC_TERMS = (
    Term("Stadi", "Helsinki.", "attested slang", "Helsinki"),
    Term("spora", "Tram.", "attested slang", "Helsinki"),
    Term("dösä", "Bus.", "attested slang", "Helsinki"),
    Term("steissi", "Railway station.", "attested slang", "Helsinki"),
    Term("kundi", "Guy or young man.", "attested slang", "Helsinki"),
    Term("hima", "Home.", "attested slang", "Helsinki"),
    Term("duuni", "Work or job.", "attested slang", "Helsinki"),
    Term("fyrkka", "Money.", "attested slang", "Helsinki"),
    Term("Wallah!", "Emphatic oath or assertion; meaning depends on context.", "Tomi-provided contemporary expression", "urban"),
    Term("Mä vannon!", "I swear!", "Tomi-provided Finnish expression", "urban"),
    Term("Suomi Perkele Saatana!", "An emphatic exclamation invoking Finland and Finnish swearing.", "Tomi-provided expression", "exclamation"),
    Term("UNSA", "The organization employing the player character.", "established game term", "institutional"),
    Term("BCI", "Brain-computer interface.", "technical term", "technical"),
)
_INDEX = {term.word.casefold(): term for term in PUBLIC_TERMS}

def lookup(query: str = "") -> str:
    """Find public terms, including substring search, without progress or secret state."""
    query = query.strip().casefold()
    if not query:
        return "Dictionary: " + ", ".join(term.word for term in PUBLIC_TERMS) + "\nUsage: dictionary <word or search>"
    exact = _INDEX.get(query)
    matches = [exact] if exact else [term for term in PUBLIC_TERMS if query in term.word.casefold() or query in term.meaning.casefold()]
    if not matches:
        return "No public dictionary entry. Some terms may require investigation."
    return "\n".join(f"{term.word}: {term.meaning} [{term.provenance}; {term.register}]" for term in matches)
