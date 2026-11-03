#!/usr/bin/env python3
"""Extract the section index of the AWN Deluxe book from its own table of contents (#1109).

The AWN Deluxe copy has no titled running heads — only a page number — but it does have a **detailed**
two-level table of contents, which the other two books lack. So this tool parses the TOC and then verifies
every entry against the page it names: the title's words must appear on that page. An entry the book does
not back up is reported instead of trusted, which is the failure mode a hand-typed inventory always has.

Output: `data/rules/awn_sections.json` (titles and printed pages only; the PDF is not stored or
redistributed). CI has no access to the book, so the JSON is committed and `--check` re-verifies it when the
file is present.

    python3 tools/awn_section_index.py --pdf ~/Lataukset/AshesWithoutNumber_Deluxe_061125-1.pdf
    python3 tools/awn_section_index.py --pdf … --check
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
OUT = ROOT / "data" / "rules" / "awn_sections.json"

#: Top-level chapters, from the book's own contents page (printed pages).
CHAPTERS: tuple[tuple[int, str], ...] = (
    (1, "The Fires that Consume"),
    (4, "Character Creation"),
    (36, "The Rules of the Game"),
    (70, "Equipment"),
    (104, "Enclaves and Settlements"),
    (136, "Creating Your Campaign"),
    (152, "Building Encounter Sites"),
    (190, "Creating Adventures"),
    (202, "Creatures of the Wastes"),
    (230, "The Albuquerque Death Zone"),
    (254, "Supplementary Material (Deluxe)"),
    (270, "Modular Power Armor (Deluxe)"),
    (278, "Hub Settlement Rules (Deluxe)"),
    (286, "Settlements and Mass Combat (Deluxe)"),
    (294, "Index"),
)

#: Entries that are apparatus rather than content.
APPARATUS = {"index", "table of contents"}

#: The TOC prints dot leaders as a run of undecodable glyphs; the page number follows them.
TOC_ENTRY = re.compile(r"^(?P<title>[^\ufffd\x08]+?)[\ufffd\x08]+\s*(?P<page>\d{1,3})\s*$")


def pdf_pages(pdf: Path) -> list[str]:
    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext not found; install poppler-utils to regenerate the index")
    raw = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    return raw.split("\f")


def toc_text(pdf: Path) -> str:
    """The contents pages only. Both AWN and the WN books put them in the first few PDF pages."""
    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext not found; install poppler-utils to regenerate the index")
    return subprocess.run(["pdftotext", "-f", "3", "-l", "4", "-raw", str(pdf), "-"],
                          capture_output=True, text=True, check=True).stdout


def parse_toc(text: str) -> list[tuple[str, int]]:
    entries: list[tuple[str, int]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.lower().startswith("table of contents"):
            continue
        match = TOC_ENTRY.match(line)
        if not match:
            continue
        title = re.sub(r"\s{2,}", " ", match.group("title")).strip(" .")
        page = int(match.group("page"))
        if title and 1 <= page <= 320:
            entries.append((title, page))
    return entries


def _words(text: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if len(w) > 2]


def verify_entry(pages: list[str], title: str, printed: int) -> str:
    """Does the page the TOC names actually contain this title? Empty string means yes."""
    index = printed + 3          # printed page 1 is PDF page 5 (cover, blanks, contents)
    if index >= len(pages):
        return f"p.{printed} is beyond the end of the PDF"
    body = " ".join(_words(pages[index]))
    wanted = _words(title)
    missing = [word for word in wanted if word not in body]
    if wanted and len(missing) <= max(1, len(wanted) // 3):
        return ""
    return f"p.{printed} does not mention {', '.join(missing[:4]) or title!r}"


def chapter_of(page: int) -> str:
    current = CHAPTERS[0][1]
    for start, name in CHAPTERS:
        if page >= start:
            current = name
    return current


def build(pdf: Path) -> dict:
    pages = pdf_pages(pdf)
    entries = parse_toc(toc_text(pdf))
    rows, problems, seen = [], [], set()
    for title, printed in entries:
        key = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        if key in APPARATUS:
            continue
        if key in seen:
            problems.append(f"duplicate TOC entry: {title!r}")
            continue
        seen.add(key)
        check = verify_entry(pages, title, printed)
        if check:
            problems.append(check)
        rows.append({
            "id": key,
            "title": title,
            "chapter": chapter_of(printed),
            "first_page": printed,
        })
    rows.sort(key=lambda row: (row["first_page"], row["id"]))
    return {
        "format": "noopunk.rules.awn_section_index",
        "version": 1,
        "issue": 1109,
        "source": {
            "title": "Ashes Without Number, Deluxe Edition",
            "author": "Kevin Crawford",
            "publisher": "Sine Nomine Publishing",
            "date": "2025-06-12",
            "printed_pages": 295,
            "method": ("the book's own two-level table of contents (PDF pages 3-4), every entry verified "
                       "against the page it names"),
            "note": ("Titles and page numbers only. No book text is reproduced; the PDF is the author's "
                     "authorised copy, is not in the repository, and is not redistributable."),
        },
        "chapters": [{"first_page": page, "title": name} for page, name in CHAPTERS],
        "sections": rows,
        "unverified_entries": problems,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pdf", type=Path, default=os.environ.get("AWN_DELUXE_PDF", ""))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)

    if not args.pdf or not Path(args.pdf).is_file():
        print("awn_section_index: pass --pdf or set AWN_DELUXE_PDF", file=sys.stderr)
        return 2
    data = build(Path(args.pdf))
    text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.is_file() else ""
        if current != text:
            print(f"awn_section_index: {args.out.relative_to(ROOT)} is stale", file=sys.stderr)
            return 1
        print(f"awn_section_index: up to date ({len(data['sections'])} sections)")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"awn_section_index: {len(data['sections'])} sections -> {args.out.relative_to(ROOT)}")
    if data["unverified_entries"]:
        print(f"  {len(data['unverified_entries'])} TOC entr(ies) could not be found on their page:",
              file=sys.stderr)
        for problem in data["unverified_entries"][:10]:
            print(f"    {problem}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
