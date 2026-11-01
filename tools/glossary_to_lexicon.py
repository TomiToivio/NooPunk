#!/usr/bin/env python3
"""Generate the player lexicon from GLOSSARY.md (#1000).

`GLOSSARY.md` is the vocabulary source of truth; the game dictionary is **generated** from it, never edited
independently, so the two cannot drift.

The glossary forbids an agent from assigning a category or an etymology, so this tool does not try. It reads
what the glossary actually states:

* every `* Term - meaning` line becomes an entry;
* a trailing `[gated]` marker means the dictionary must stay silent until the story unlocks the term;
* nothing else is invented. Categories are not written here because the glossary says they are Tomi's to give.

The generated JSON therefore carries `classification: "unknown"` for every term until Tomi fills it in, which
is the honest state rather than a plausible-looking guess.

Usage:
    python3 tools/glossary_to_lexicon.py            # write the JSON
    python3 tools/glossary_to_lexicon.py --check    # fail if the JSON is stale

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
GATED = re.compile(r"\s*\[gated\]\s*$", re.IGNORECASE)


class GlossaryError(ValueError):
    """The glossary cannot be turned into a lexicon."""


def fold(value: str) -> str:
    """Case- and diacritic-insensitive key, so `Dösä` and `dosa` are the same headword."""
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch)).strip()


def build(text: str) -> dict:
    """Read the glossary's headwords into lexicon entries."""
    terms: list[dict] = []
    seen: set[str] = set()

    for line in text.splitlines():
        match = BULLET.match(line.strip())
        if not match:
            continue
        term = match.group("term").strip()
        meaning = match.group("meaning").strip()
        gated = bool(GATED.search(meaning))
        if gated:
            meaning = GATED.sub("", meaning).strip()
        if not meaning:
            raise GlossaryError(f"{term!r}: a headword needs a definition")
        key = fold(term)
        if key in seen:
            raise GlossaryError(f"{term!r}: headword listed twice")
        seen.add(key)
        terms.append({
            "word": term,
            "meaning": meaning,
            "classification": "unknown",   # the glossary leaves this to Tomi
            "provenance": "tomi",
            "register": "",
            "spoiler": "gated" if gated else "public",
            "note": "",
        })

    if not terms:
        raise GlossaryError("no headwords found; GLOSSARY.md must list `* Term - meaning` lines")

    return {
        "format": "nopunk-glossary-v1",
        "source": "GLOSSARY.md",
        "note": ("Generated from GLOSSARY.md by tools/glossary_to_lexicon.py; do not edit. "
                 "Classification is 'unknown' until Tomi assigns one - an agent must not guess a category, "
                 "an etymology or an attestation."),
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
