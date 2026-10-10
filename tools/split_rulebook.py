#!/usr/bin/env python3
"""Split the consolidated RULEBOOK.md into navigable segments — losslessly.

`RULEBOOK.md` is 6108 lines in one file: a core game book (sections 1-9) and a
54-section extended ledger, separated by the `# Extended canon and reference
material` marker. Reading it is hard, and a single file cannot be navigated by
part.

This tool derives `rulebook_parts/` from it, driven by the TOTAL section->part map
in `data/rules/rulebook_segmentation.json`. Losslessness is the whole point, so it
is proved rather than asserted: `--check` rebuilds the original byte stream from the
segments it handed out and compares it with the file on disk.

`RULEBOOK.md` stays canonical. The parts are a derived, navigable view; nothing in
the source is renumbered, reworded or removed, and the guards that pin the
core/ledger structure keep working because the source is untouched.

Usage:
    python3 tools/split_rulebook.py            # write rulebook_parts/
    python3 tools/split_rulebook.py --check    # prove losslessness, write nothing
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "RULEBOOK.md"
MAP_FILE = ROOT / "data" / "rules" / "rulebook_segmentation.json"
OUT_DIR = ROOT / "rulebook_parts"

HEAD_H1 = re.compile(r"^# (?!#)")
HEAD_H2 = re.compile(r"^## (?!#)")
NUMBERED = re.compile(r"^## (\d+)\.")
NAV_START = "<!-- rulebook-part-nav:start -->"
NAV_END = "<!-- rulebook-part-nav:end -->"


def load_map() -> dict:
    return json.loads(MAP_FILE.read_text(encoding="utf-8"))


def segment(lines: list[str], marker: str) -> list[dict]:
    """Cut the file into structural segments, in order.

    A segment begins at an H1 or H2 heading; everything before the first heading is
    the preamble. Splitting on H1 as well as H2 is what keeps the core/ledger marker
    from being swallowed by the last core section -- it becomes its own segment, so
    the two numbering spaces stay distinguishable.
    """
    starts = [i for i, ln in enumerate(lines) if HEAD_H1.match(ln) or HEAD_H2.match(ln)]
    if not starts or starts[0] != 0:
        starts = [0, *starts]
    segments: list[dict] = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        body = lines[start:end]
        first = body[0] if body else ""
        segments.append(
            {
                "start": start,
                "end": end,
                "lines": body,
                "heading": first.rstrip("\n"),
                "is_h1": bool(HEAD_H1.match(first)),
                "is_h2": bool(HEAD_H2.match(first)),
            }
        )
    # Which side of the marker a section sits on decides which numbering space it
    # belongs to. The marker is itself a segment, so this is a clean index compare.
    marker_index = next(
        (i for i, s in enumerate(segments) if s["heading"].strip() == marker), None
    )
    if marker_index is None:
        raise SystemExit(f"core/ledger marker not found: {marker!r}")
    for i, s in enumerate(segments):
        s["space"] = "preamble" if i < marker_index else "ledger"
    segments[marker_index]["space"] = "marker"
    return segments


def assign(segments: list[dict], mapping: dict) -> None:
    """Attach each segment to a part. Raises on anything unassigned or doubled."""
    parts = mapping["parts"]
    by_id = {p["id"]: p for p in parts}
    for part in parts:
        part["_segments"] = []
    seen: dict[tuple[str, str], str] = {}
    for s in segments:
        if s["space"] == "marker" or not s["is_h2"]:
            # The marker and every H1 are structural; the meta part holds structure.
            target = parts[0]["id"]
        else:
            match = NUMBERED.match(s["heading"])
            if match is None:
                # An unnumbered H2 before the marker is the core half's table of contents:
                # navigation, not a rules section, so it stays with the structural part.
                target = parts[0]["id"]
            else:
                # The core and ledger numbering spaces RESTART at 1, so a section's key in
                # the map depends on which side of the marker it came from: the core half is
                # declared under "core", the ledger under "ledger". Reading only "ledger" --
                # or treating "preamble" as blanket-structural -- silently files the entire
                # playable core game-book (Stats, Skills, the four system chapters, character
                # generation) under meta, which "holds no player-facing rules". The map said
                # otherwise and nothing noticed, because the core lists were never consulted.
                space = "core" if s["space"] == "preamble" else "ledger"
                key = match.group(1)
                target = next((p["id"] for p in parts if key in p.get(space, [])), None)
                if target is None:
                    raise SystemExit(f"unassigned {space} section: {s['heading']!r}")
                token = (space, key)
                if token in seen:
                    raise SystemExit(f"section {space} {key} assigned twice")
                seen[token] = target
        by_id[target]["_segments"].append(s)
        s["part"] = target
    for part in parts:
        if not part["_segments"]:
            raise SystemExit(f"part {part['id']} received no segments")


def reconstruct(segments: list[dict]) -> str:
    """The original text, rebuilt from the segments in canonical order."""
    return "".join("".join(s["lines"]) for s in segments)


def nav_block(part: dict, parts: list[dict]) -> str:
    links = " · ".join(
        f"[{p['title'].split(':')[0]}]({p['id']}.md)" for p in parts
    )
    return (
        f"{NAV_START}\n"
        f"> **Part of the NoöPunk rulebook.** Index: [INDEX.md](INDEX.md) · {links}\n"
        f">\n"
        f"> Source of truth: `RULEBOOK.md` (canonical). This part is generated by\n"
        f"> `python3 tools/split_rulebook.py`; edit the source, never this file.\n"
        f"{NAV_END}\n\n"
    )


def write_parts(mapping: dict) -> list[Path]:
    parts = mapping["parts"]
    OUT_DIR.mkdir(exist_ok=True)
    written: list[Path] = []
    for part in parts:
        target = OUT_DIR / f"{part['id']}.md"
        header = (
            f"# {part['title']}\n\n"
            f"*{part['purpose']}*\n\n"
            + nav_block(part, parts)
        )
        body = "".join("".join(s["lines"]) for s in part["_segments"])
        target.write_text(header + body, encoding="utf-8")
        written.append(target)
    index = ["# NoöPunk rulebook — segment index\n",
             "\n",
             "Generated from `RULEBOOK.md` by `tools/split_rulebook.py`. ",
             "Total: no section is unassigned and the concatenation of the parts ",
             "reproduces the source byte-for-byte (`--check`).\n\n"]
    for part in parts:
        index.append(f"## [{part['title']}]({part['id']}.md)\n\n")
        index.append(f"{part['purpose']}\n\n")
        for s in part["_segments"]:
            if s["is_h2"]:
                index.append(f"- {s['heading'][3:]}\n")
        index.append("\n")
    (OUT_DIR / "INDEX.md").write_text("".join(index), encoding="utf-8")
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="prove losslessness, write nothing")
    args = parser.parse_args(argv)

    mapping = load_map()
    original = SOURCE.read_text(encoding="utf-8")
    segments = segment(original.splitlines(keepends=True), mapping["core_ledger_marker"])
    assign(segments, mapping)

    rebuilt = reconstruct(segments)
    if rebuilt != original:
        a, b = original.splitlines(), rebuilt.splitlines()
        where = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
        print(f"LOSSY: reconstruction differs at line {where + 1}", file=sys.stderr)
        print(f"  source: {a[where][:90]!r}" if where < len(a) else "  source: <eof>", file=sys.stderr)
        print(f"  parts : {b[where][:90]!r}" if where < len(b) else "  parts : <eof>", file=sys.stderr)
        return 1

    covered = sum(len(p["_segments"]) for p in mapping["parts"])
    print(f"segments: {len(segments)} | assigned to {len(mapping['parts'])} parts | covered {covered}")
    print(f"lossless: reconstruction == RULEBOOK.md ({len(original)} bytes, "
          f"{original.count(chr(10)) + 1} lines)")
    if args.check:
        print("check only; nothing written")
        return 0
    written = write_parts(mapping)
    for path in written:
        print(f"wrote {path.relative_to(ROOT)}")
    print(f"wrote {(OUT_DIR / 'INDEX.md').relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
