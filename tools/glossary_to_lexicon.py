#!/usr/bin/env python3
"""Generate the player lexicon from GLOSSARY.md (#1000).

`GLOSSARY.md` is the vocabulary source of truth. The game dictionary is **generated from it**, never edited
independently, so the two cannot drift. This tool parses the glossary, joins Tomi's headwords and definitions
to their classification, and writes ``data/world/lexicon.json``.

The glossary has two halves on purpose:

* the **definitions** stay in Tomi's prose, as bullet lines ``* Term - meaning``, untouched;
* the **classification** is a table keyed by term, giving category, provenance, register and spoiler tier.

Nothing is restated: the meaning lives in exactly one place, the metadata in another, and the join is checked.
That is what makes the parity test meaningful rather than decorative.

Usage:
    python3 tools/glossary_to_lexicon.py            # write the JSON
    python3 tools/glossary_to_lexicon.py --check    # fail if the JSON is stale or a term is unclassified

Exit codes: 0 = consistent, 1 = the glossary and the generated lexicon disagree.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLOSSARY = ROOT / "GLOSSARY.md"
OUTPUT = ROOT / "data/world/lexicon.json"

BULLET = re.compile(r"^\*\s+(?P<term>[^–\-]+?)\s+[-–]\s+(?P<meaning>.+?)\s*$")
ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$")

#: How a word relates to the world. The distinction is the point of the issue.
CATEGORIES = {
    "attested_modern": "real Stadin slangi in current use",
    "attested_older": "older Stadin slangi, still recognised",
    "real_borrowing": "a loanword in ordinary use",
    "noopunk_slang": "futuristic NoöPunk Helsinki slang",
    "universe": "NoöPunk universe terminology",
}
PROVENANCE = ("tomi", "documented", "agent_proposed")
SPOILER = ("public", "gated")


class GlossaryError(ValueError):
    """The glossary and its classification disagree."""


def fold(value: str) -> str:
    """Case- and diacritic-insensitive key, so `Dösä` and `dosa` are the same headword."""
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).strip()


def parse_glossary(text: str) -> tuple[list[tuple[str, str]], dict[str, dict[str, str]]]:
    """Return ``(headwords, classification)`` parsed from the glossary Markdown."""
    headwords: list[tuple[str, str]] = []
    classification: dict[str, dict[str, str]] = {}
    in_table = False

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and "classification" in stripped.lower():
            in_table = True
            continue
        if stripped.startswith("#") and in_table:
            in_table = False

        if in_table:
            match = ROW.match(stripped)
            if not match:
                continue
            cells = [cell.strip() for cell in match.group("cells").split("|")]
            if not cells or set(cells[0]) <= {"-", ":"}:
                continue  # the header separator
            if cells[0].lower() == "term":
                continue  # the header row
            if len(cells) < 5:
                raise GlossaryError(f"classification row needs 5 columns: {stripped}")
            term, category, provenance, register, spoiler = cells[:5]
            note = cells[5] if len(cells) > 5 else ""
            key = fold(term)
            if key in classification:
                raise GlossaryError(f"{term!r}: classified twice")
            classification[key] = {
                "term": term, "category": category, "provenance": provenance,
                "register": register, "spoiler": spoiler, "note": note,
            }
            continue

        match = BULLET.match(stripped)
        if match:
            headwords.append((match.group("term").strip(), match.group("meaning").strip()))

    return headwords, classification


def build(text: str) -> dict:
    """Join the headwords to their classification and validate the result."""
    headwords, classification = parse_glossary(text)
    if not headwords:
        raise GlossaryError("no headwords found; GLOSSARY.md must list `* Term - meaning` lines")

    seen: set[str] = set()
    terms = []
    for term, meaning in headwords:
        key = fold(term)
        if key in seen:
            raise GlossaryError(f"{term!r}: headword listed twice")
        seen.add(key)
        meta = classification.get(key)
        if meta is None:
            raise GlossaryError(
                f"{term!r}: no classification row. Every headword needs a category, provenance, "
                f"register and spoiler tier.")
        if meta["category"] not in CATEGORIES:
            raise GlossaryError(f"{term!r}: unknown category {meta['category']!r}")
        if meta["provenance"] not in PROVENANCE:
            raise GlossaryError(f"{term!r}: unknown provenance {meta['provenance']!r}")
        if meta["spoiler"] not in SPOILER:
            raise GlossaryError(f"{term!r}: unknown spoiler tier {meta['spoiler']!r}")
        if meta["spoiler"] == "gated" and not meta["note"]:
            raise GlossaryError(
                f"{term!r}: a gated term needs a note saying when it unlocks, "
                f"or the dictionary cannot explain why it is silent.")
        terms.append({
            "word": term,
            "meaning": meaning,
            "category": meta["category"],
            "provenance": meta["provenance"],
            "register": meta["register"],
            "spoiler": meta["spoiler"],
            "note": meta["note"],
        })

    unclassified = [meta["term"] for key, meta in classification.items() if key not in seen]
    if unclassified:
        raise GlossaryError(
            "classification names terms that are not headwords: " + ", ".join(sorted(unclassified)))

    return {
        "format": "nopunk-glossary-v1",
        "source": "GLOSSARY.md",
        "note": ("Generated from GLOSSARY.md by tools/glossary_to_lexicon.py; do not edit. "
                 "Definitions live in the glossary, classification in its table."),
        "terms": sorted(terms, key=lambda entry: fold(entry["word"])),
    }


def render(data: dict) -> str:
    """UTF-8 JSON, characters written as themselves rather than escaped."""
    return json.dumps(data, ensure_ascii=False, indent=1) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true",
                        help="verify the generated lexicon matches GLOSSARY.md instead of writing it")
    args = parser.parse_args(argv)

    try:
        data = build(GLOSSARY.read_text(encoding="utf-8"))
    except GlossaryError as exc:
        print(f"GLOSSARY.md: {exc}", file=sys.stderr)
        return 1

    text = render(data)
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if current != text:
            print(f"{OUTPUT.relative_to(ROOT)} is stale; run python3 tools/glossary_to_lexicon.py",
                  file=sys.stderr)
            return 1
        print(f"{OUTPUT.relative_to(ROOT)}: {len(data['terms'])} terms, consistent with GLOSSARY.md")
        return 0

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    gated = sum(1 for term in data["terms"] if term["spoiler"] == "gated")
    print(f"{OUTPUT.relative_to(ROOT)}: {len(data['terms'])} terms written, {gated} gated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
