"""Source-linked equipment index for NoöPunk's existing *descriptive* catalog.

This indexes authored markdown and does not invent cost, attack, cyberware,
or implant statistics. It works without network access and uses stdlib only.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ("rulebook/13_EQUIPMENT.md", "rulebook/9_FIELD_CATALOGS.md")
HEADER = re.compile(r"^#{2,4} (.+)$")
BOLD_CELL = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|\s*$")
BULLET = re.compile(r"^\s*- \*\*(.+?)\*\*\s*[—–-]\s*(.+)$")


@dataclass(frozen=True)
class CatalogEntry:
    name: str
    description: str
    source: str
    line: int
    section: str
    format: str


def collect_entries(root: Path = ROOT) -> list[CatalogEntry]:
    """Extract only explicitly authored items. Duplicates retain their citations."""
    entries = []
    for source in SOURCES:
        section = "(intro)"
        for lineno, line in enumerate((root / source).read_text(encoding="utf-8").splitlines(), 1):
            header = HEADER.match(line)
            if header:
                section = header.group(1)
                continue
            match = BOLD_CELL.match(line)
            fmt = "table" if match else "bullet"
            if match is None:
                match = BULLET.match(line)
            if match is None:
                continue
            name, description = (v.strip() for v in match.groups())
            if not name or not description:
                continue
            entries.append(CatalogEntry(name, description, source, lineno, section, fmt))
    return entries


def search_catalog(needle: str, entries: list[CatalogEntry] | None = None) -> list[CatalogEntry]:
    """Case-insensitive text search; every hit retains a source and line."""
    if not needle.strip():
        raise ValueError("search term must be nonempty")
    haystack = collect_entries() if entries is None else entries
    return [e for e in haystack if needle.casefold() in (e.name + " " + e.description + " " + e.section).casefold()]


def export_catalog(root: Path = ROOT) -> dict:
    return {"format": "noopunk.descriptive_equipment_index", "version": 1,
            "canonical_sources": list(SOURCES),
            "numeric_stats_finalized": False,
            "entries": [asdict(e) for e in collect_entries(root)]}


if __name__ == "__main__":
    print(json.dumps(export_catalog(), indent=2, ensure_ascii=False))
