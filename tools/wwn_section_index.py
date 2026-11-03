#!/usr/bin/env python3
"""Extract the section index of the WWN Deluxe book from its own running heads (#1101).

Issue #1101 asks for a rule-by-rule register "not just chapter headings", and it says the Deluxe PDF was
"not automatically available to repository agents" — so the Deluxe rows could previously only be guessed
at from chapter titles. This tool turns the purchased copy into citable sections: every printed page in the
book carries a running head like ``48• Injury, healing, and system strain`` (verso) or
``Skill checks •41`` (recto), which gives the section title *and* the printed page number on the same line.

The output is committed as `data/rules/wwn_sections.json`, because CI has no access to the PDF. Run with
the PDF to regenerate or to check:

    python3 tools/wwn_section_index.py --pdf ~/Lataukset/WorldsWithoutNumber_DeluxePDF_040221.pdf
    python3 tools/wwn_section_index.py --pdf ... --check     # exit 1 if the committed index is stale

Nothing here reproduces book text: it records titles, page numbers and chapter boundaries only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "rules" / "wwn_sections.json"

#: The book's chapter openings, from its own table of contents (printed pages).
CHAPTERS: tuple[tuple[int, str], ...] = (
    (1, "Tales of the Latter Earth"),
    (4, "Character Creation"),
    (38, "The Rules of the Game"),
    (60, "Magic and the Arcane Traditions"),
    (94, "The World of the Latter Earth"),
    (114, "Creating Your Campaign"),
    (222, "Creating Adventures"),
    (280, "Creatures of A Far Age"),
    (322, "Factions and Major Projects"),
    (344, "Arts of the Gyre"),
    (356, "Heroic Classes and Characters"),
    (358, "Legates"),
    (370, "Iterums and their Dwellers"),
    (376, "Additional GM Tools"),
    (394, "Index"),
)

#: Sections that are part of a chapter's apparatus rather than a rule or a setting description.
APPARATUS = {"index", "spell index", "kickstarter backers"}

RUNNING_HEAD = re.compile(r"^(?:(\d{1,3})\s*[•·]\s*(.+?)|(.+?)\s*[•·]\s*(\d{1,3}))\s*$")


def extracted_text(pdf: Path) -> list[str]:
    """The PDF as a list of page strings. Needs `pdftotext` (poppler), which CI does not require."""
    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext not found; install poppler-utils to regenerate the index")
    result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                            capture_output=True, text=True, check=True)
    return result.stdout.split("\f")


def parse_heads(pages: list[str]) -> dict[str, dict]:
    """Map section title -> the printed pages whose running head names it."""
    sections: dict[str, dict] = {}
    for index, page in enumerate(pages):
        printed = index - 2  # the PDF carries two cover/contents pages before printed page 1
        if printed < 1:
            continue
        for line in page.splitlines()[:5]:
            match = RUNNING_HEAD.match(line.strip())
            if not match:
                continue
            if match.group(1):
                number, title = int(match.group(1)), match.group(2)
            else:
                title, number = match.group(3), int(match.group(4))
            title = re.sub(r"\s+", " ", title).strip()
            if number != printed or len(title) < 4:
                continue
            key = title.lower()
            if key in APPARATUS:
                continue
            sections.setdefault(key, {"title": title, "pages": []})["pages"].append(printed)
    return sections


def chapter_of(page: int) -> str:
    current = CHAPTERS[0][1]
    for start, name in CHAPTERS:
        if page >= start:
            current = name
    return current


def build(pdf: Path) -> dict:
    pages = extracted_text(pdf)
    sections = parse_heads(pages)
    rows = []
    for key, data in sections.items():
        first = min(data["pages"])
        rows.append({
            "id": re.sub(r"[^a-z0-9]+", "-", key).strip("-"),
            "title": data["title"],
            "chapter": chapter_of(first),
            "first_page": first,
            "last_page": max(data["pages"]),
            "pages": sorted(data["pages"]),
        })
    rows.sort(key=lambda row: (row["first_page"], row["id"]))
    return {
        "format": "noopunk.rules.wwn_section_index",
        "version": 1,
        "issue": 1101,
        "source": {
            "title": "Worlds Without Number, Deluxe Edition",
            "author": "Kevin Crawford",
            "publisher": "Sine Nomine Publishing",
            "isbn": "978-1-950965-07-6",
            "date": "2021-04-02",
            "printed_pages": 399,
            "method": "printed running heads (verso 'NN• Title', recto 'Title •NN'), extracted with pdftotext -layout",
            "note": ("Titles and page numbers only. No book text is reproduced; the PDF itself is not in the "
                     "repository and is not redistributable."),
        },
        "chapters": [{"first_page": page, "title": name} for page, name in CHAPTERS],
        "sections": rows,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pdf", type=Path, default=os.environ.get("WWN_DELUXE_PDF", ""))
    parser.add_argument("--check", action="store_true", help="fail if the committed index is stale")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)

    if not args.pdf or not Path(args.pdf).is_file():
        print("wwn_section_index: pass --pdf or set WWN_DELUXE_PDF", file=sys.stderr)
        return 2
    data = build(Path(args.pdf))
    text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.is_file() else ""
        if current != text:
            print(f"wwn_section_index: {args.out.relative_to(ROOT)} is stale", file=sys.stderr)
            return 1
        print(f"wwn_section_index: up to date ({len(data['sections'])} sections)")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"wwn_section_index: {len(data['sections'])} sections -> {args.out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
