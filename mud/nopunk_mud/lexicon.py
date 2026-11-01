"""Deterministic, spoiler-safe player lexicon generated from the canonical GLOSSARY.md (#1000)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

GLOSSARY_PATH = Path(__file__).resolve().parents[2] / "GLOSSARY.md"
PUBLIC = "public"


@dataclass(frozen=True)
class Term:
    word: str
    meaning: str
    category: str
    provenance: str
    register: str = "general"
    variants: str = ""
    notes: str = ""
    spoiler: str = PUBLIC


def parse_glossary(path: Path = GLOSSARY_PATH) -> tuple[Term, ...]:
    """Read the canonical Markdown table. The file is the authority; no second list exists."""
    rows: list[Term] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-", " "}:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 8 or cells[0] in {"Term", "---"}:
            continue
        rows.append(Term(*cells))
    if not rows:
        raise ValueError(f"no glossary entries parsed from {path}")
    return tuple(rows)


PUBLIC_TERMS = tuple(term for term in parse_glossary() if term.spoiler == PUBLIC)
_INDEX = {term.word.casefold(): term for term in PUBLIC_TERMS}


def lookup(query: str = "") -> str:
    """Find public terms, including substring search, without progress or secret state."""
    query = query.strip().casefold()
    if not query:
        return "Dictionary: " + ", ".join(term.word for term in PUBLIC_TERMS) + "\nUsage: dictionary <word or search>"
    exact = _INDEX.get(query)
    matches = [exact] if exact else [
        term for term in PUBLIC_TERMS
        if query in term.word.casefold() or query in term.meaning.casefold()]
    if not matches:
        return "No public dictionary entry. Some terms may require investigation."
    return "\n".join(
        f"{term.word}: {term.meaning} [{term.category}; {term.provenance}; {term.register}]"
        for term in matches)
