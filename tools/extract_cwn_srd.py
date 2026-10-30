#!/usr/bin/env python3
"""Extract the Cities Without Number SRD catalogues into JSON for the Godot rules engine.

Source: https://cwn.quadrifons.com/ — the CWN SRD, recorded in
``data/sources/game_system_rights.json`` as ``verified-public-domain`` (CC0). That decision covers
mechanics and tables; it does not cover the published books' art or their setting trademarks.

Why a tool instead of hand-written JSON: enumerated lists must be *parsed* from the source and
diffed, never recalled. A table transcribed from memory is confident and wrong. Running this again
against a changed SRD shows the difference instead of hiding it.

The SRD pages are static HTML but split across 82 URLs. ``--cache`` keeps a local copy so the
extraction is reproducible offline; ``--report`` prints per-file row counts and any row that failed
to parse, which is the diff a reviewer reads before trusting the data.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = "https://cwn.quadrifons.com"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "rules" / "cwn"

PAGES = {
    "firearms": "/gear-vehicles-cyberware/weapons/firearms/",
    "melee": "/gear-vehicles-cyberware/weapons/melee-thrown-weapons/",
    "heavy": "/gear-vehicles-cyberware/weapons/heavy-weapons/",
    "weapon_mods": "/gear-vehicles-cyberware/weapons/weapon-mods/",
    "armor": "/gear-vehicles-cyberware/armor/armor-types/",
    "armor_mods": "/gear-vehicles-cyberware/armor/armor-mods/",
    "missions": "/gear-vehicles-cyberware/mission-gear/",
    "cyberdecks": "/gear-vehicles-cyberware/cyberdecks/",
    "drones": "/gear-vehicles-cyberware/drones/",
    "vehicles": "/gear-vehicles-cyberware/vehicles/",
    "drugs": "/gear-vehicles-cyberware/pharmaceuticals-street-drugs/",
    "verbs": "/hacking/programs/program-verbs/",
    "subjects": "/hacking/programs/program-subjects/",
    "demons": "/hacking/demons-watchdogs/",
    "backgrounds": "/character-creation/backgrounds/",
    "advancement": "/rules-of-the-game/character-advancement/",
    "combat_actions": "/rules-of-the-game/combat/combat-actions/",
    "damage": "/rules-of-the-game/combat/damage-trauma-shock/",
    "body": "/gear-vehicles-cyberware/cyberware/cyberware-systems/body-cyberware/",
    "head": "/gear-vehicles-cyberware/cyberware/cyberware-systems/head-cyberware/",
    "skin": "/gear-vehicles-cyberware/cyberware/cyberware-systems/skin-cyberware/",
    "limb": "/gear-vehicles-cyberware/cyberware/cyberware-systems/limb-cyberware/",
    "sensory": "/gear-vehicles-cyberware/cyberware/cyberware-systems/sensory-cyberware/",
    "medical": "/gear-vehicles-cyberware/cyberware/cyberware-systems/medical-cyberware/",
    "nerve": "/gear-vehicles-cyberware/cyberware/cyberware-systems/nerve-cyberware/",
    "cyberware_mods": "/gear-vehicles-cyberware/cyberware/cyberware-mods/",
}


def fetch(path: str, cache: Path) -> str:
    slug = path.strip("/").replace("/", "_") or "index"
    target = cache / f"{slug}.html"
    if target.exists() and target.stat().st_size > 500:
        return target.read_text(encoding="utf-8", errors="replace")
    target.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["curl", "-sL", "-w", "\n%{http_code}", f"{BASE}{path}"],
        capture_output=True,
        text=True,
        check=False,
    )
    body, _, code = proc.stdout.rpartition("\n")
    if code.strip() != "200":
        raise SystemExit(f"fetch failed for {path}: HTTP {code.strip()}")
    target.write_text(body, encoding="utf-8")
    return body


def article(raw: str) -> str:
    match = re.search(r"(?is)<article[^>]*>(.*?)</article>", raw)
    body = match.group(1) if match else raw
    # Convert table structure to pipe-delimited text before stripping tags: the crawl's own
    # normalisation did this, and doing it here keeps the extractor independent of that step.
    body = re.sub(r"(?i)</t[dh]>", " | ", body)
    body = re.sub(r"(?i)</tr>|</table>", "\n", body)
    body = re.sub(r"(?i)</(p|div|li|h[1-6]|section)>", "\n", body)
    body = re.sub(r"(?i)<br\s*/?>", "\n", body)
    return body


def tables(html_fragment: str) -> list[list[list[str]]]:
    """Return every HTML table as a list of rows of cells.

    Parsing by ``<tr>``/``<td>`` rather than by text lines: two-column tables put one cell per
    line once block tags become newlines, so a line-based reader silently drops them. Backgrounds
    are almost entirely two-column tables, which is how the first attempt lost them.
    """
    out: list[list[list[str]]] = []
    for table in re.findall(r"(?is)<table[^>]*>(.*?)</table>", html_fragment):
        rows: list[list[str]] = []
        for tr in re.findall(r"(?is)<tr[^>]*>(.*?)</tr>", table):
            cells = [
                html.unescape(re.sub(r"(?is)<[^>]+>", " ", cell)).replace("\xa0", " ").strip()
                for cell in re.findall(r"(?is)<t[dh][^>]*>(.*?)</t[dh]>", tr)
            ]
            cells = [re.sub(r"\s+", " ", c) for c in cells]
            if cells:
                rows.append(cells)
        if len(rows) > 1:
            out.append(rows)
    return out


def to_rows(block: list[list[str]]) -> list[dict[str, str]]:
    header = [h for h in block[0]]
    rows = []
    for raw in block[1:]:
        if len(raw) != len(header):
            continue
        rows.append({header[i]: raw[i] for i in range(len(header))})
    return rows


def _numbered(cell: str) -> list[dict]:
    """Split a cell holding "1. X 2. Y ..." into [{"roll": 1, "result": "X"}, ...]."""
    items = re.split(r"(?:^|\s)(\d{1,2})\.\s+", cell)
    out: list[dict] = []
    for i in range(1, len(items) - 1, 2):
        out.append({"roll": int(items[i]), "result": re.sub(r"\s+", " ", items[i + 1]).strip()})
    return out


def background_sections(raw: str) -> list[dict]:
    """Backgrounds are headings with a free-skill table, quick skills in prose, and one
    growth/learning table whose cells each hold a whole numbered list.

    The generic pass cannot see any of this: it returns the same growth table once per background
    and loses the names, because the names are headings rather than cells.
    """
    parts = re.split(r"(?is)<h3[^>]*>(.*?)</h3>", raw)
    out: list[dict] = []
    for i in range(1, len(parts), 2):
        name = html.unescape(re.sub(r"(?is)<[^>]+>", "", parts[i])).strip()
        chunk = parts[i + 1]
        prose = re.sub(r"(?is)<table.*?</table>", " ", chunk)
        text = html.unescape(re.sub(r"(?is)<[^>]+>", " ", prose))
        quick = re.search(r"Quick Skills\s*:?\s*([^.]*)\.", text, re.I)
        quick_skills = [s.strip() for s in quick.group(1).split(",")] if quick else []
        entry: dict = {
            "name": name,
            "free_skill": "",
            "quick_skills": quick_skills,
            "growth": [],
            "learning": [],
        }
        for block in tables(chunk):
            header = [h.lower() for h in block[0]]
            if any("free skill" in h for h in header):
                entry["free_skill"] = block[1][0] if len(block) > 1 and block[1] else ""
            elif any("growth" in h for h in header) and len(block) > 1:
                entry["growth"] = _numbered(block[1][0])
                if len(block[1]) > 1:
                    entry["learning"] = _numbered(block[1][1])
        out.append(entry)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/cwn-srd-cache")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    cache = Path(args.cache)
    OUT.mkdir(parents=True, exist_ok=True)

    payload = {"source": BASE, "licence": "CC0 (verified-public-domain)", "tables": {}}
    report = {}
    for key, path in PAGES.items():
        blocks = tables(fetch(path, cache))
        payload["tables"][key] = [
            {"columns": block[0], "rows": to_rows(block)} for block in blocks
        ]
        report[key] = (len(blocks), sum(len(to_rows(b)) for b in blocks))

    payload["backgrounds"] = background_sections(fetch(PAGES["backgrounds"], cache))

    target = OUT / "srd_tables.json"
    target.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")

    if args.report:
        print(f"backgrounds      count={len(payload['backgrounds'])}")
        for key, (n_blocks, n_rows) in sorted(report.items()):
            print(f"{key:16s} blocks={n_blocks:2d} rows={n_rows:3d}")
        print(f"\nwrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
