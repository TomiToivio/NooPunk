#!/usr/bin/env python3
"""Extract the Cities Without Number SRD into the data contract the Godot game reads.

Source: https://cwn.quadrifons.com/ - the CWN System Reference Document, released CC0 1.0
(public domain dedication). Scope caveat: this is the SRD, not the commercial book; the site also
omits optional magic/spellcasting rules and the Antagonists & NPCs section.

Extraction is deterministic and mechanical: every <table> is captured with the page path and table
index it came from, so any value can be traced back to its source. Nothing is transcribed by hand,
and no value is invented - an absent table stays absent.

    python3 tools/cwn_srd_extract.py            # fetch and write data/rules/cwn/
    python3 tools/cwn_srd_extract.py --check    # verify the committed data matches the source
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = "https://cwn.quadrifons.com"
OUT = Path(__file__).resolve().parent.parent / "data" / "rules" / "cwn"

PAGES = [
    "/character-creation/", "/character-creation/attributes/", "/character-creation/skills/",
    "/character-creation/backgrounds/", "/character-creation/contacts/", "/character-creation/edges/",
    "/character-creation/foci/", "/character-creation/focus-gear-budget/", "/character-creation/final-steps/",
    "/rules-of-the-game/", "/rules-of-the-game/scenes-rounds-mission-time/", "/rules-of-the-game/saving-throws/",
    "/rules-of-the-game/skill-checks/", "/rules-of-the-game/combat/", "/rules-of-the-game/combat/combat-sequence",
    "/rules-of-the-game/combat/combat-initiative/", "/rules-of-the-game/combat/combat-actions/",
    "/rules-of-the-game/combat/attacks-in-combat/", "/rules-of-the-game/combat/damage-trauma-shock/",
    "/rules-of-the-game/combat/special-combat-maneuvers/", "/rules-of-the-game/combat/vehicle-combat/",
    "/rules-of-the-game/injury-healing-system-strain",
    "/rules-of-the-game/injury-healing-system-strain/mortal-injury-stabilization/",
    "/rules-of-the-game/injury-healing-system-strain/system-strain/",
    "/rules-of-the-game/injury-healing-system-strain/natural-healing-first-aid-poisons/",
    "/rules-of-the-game/injury-healing-system-strain/major-injuries/",
    "/rules-of-the-game/chases-and-pursuit/", "/rules-of-the-game/character-advancement/",
    "/rules-of-the-game/crafting-modifying-gear/", "/rules-of-the-game/crafting-modifying-gear/crafting-gear/",
    "/rules-of-the-game/crafting-modifying-gear/modifying-gear/",
    "/rules-of-the-game/crafting-modifying-gear/maintaining-mods/",
    "/rules-of-the-game/crafting-modifying-gear/factory-mods/", "/rules-of-the-game/encumbrance/",
    "/gear-vehicles-cyberware/", "/gear-vehicles-cyberware/mission-gear/",
    "/gear-vehicles-cyberware/lifestyles-wages-and-bribes/",
    "/gear-vehicles-cyberware/lifestyles-wages-and-bribes/lifestyle-costs/",
    "/gear-vehicles-cyberware/lifestyles-wages-and-bribes/common-wages/",
    "/gear-vehicles-cyberware/lifestyles-wages-and-bribes/bribe-costs/",
    "/gear-vehicles-cyberware/armor/", "/gear-vehicles-cyberware/armor/armor-terms-definitions/",
    "/gear-vehicles-cyberware/armor/armor-types/", "/gear-vehicles-cyberware/armor/armor-accessories/",
    "/gear-vehicles-cyberware/armor/armor-mods/", "/gear-vehicles-cyberware/weapons/",
    "/gear-vehicles-cyberware/weapons/weapon-stats-and-definitions/",
    "/gear-vehicles-cyberware/weapons/firearms/", "/gear-vehicles-cyberware/weapons/melee-thrown-weapons/",
    "/gear-vehicles-cyberware/weapons/heavy-weapons/", "/gear-vehicles-cyberware/weapons/weapon-mods/",
    "/gear-vehicles-cyberware/pharmaceuticals-street-drugs/", "/gear-vehicles-cyberware/cyberware/",
    "/gear-vehicles-cyberware/cyberware/installing-cyberware/",
    "/gear-vehicles-cyberware/cyberware/implant-complications/",
    "/gear-vehicles-cyberware/cyberware/cyberdoc-tools/",
    "/gear-vehicles-cyberware/cyberware/removing-cyberware/",
    "/gear-vehicles-cyberware/cyberware/concealing-detecting-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-maintenance/",
    "/gear-vehicles-cyberware/cyberware/skillplugs/", "/gear-vehicles-cyberware/cyberware/cyberware-mods/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/body-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/head-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/skin-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/limb-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/sensory-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/medical-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-systems/nerve-cyberware/",
    "/gear-vehicles-cyberware/cyberware/cyberware-alienation/",
    "/gear-vehicles-cyberware/cyberdecks/", "/gear-vehicles-cyberware/drones/",
    "/gear-vehicles-cyberware/vehicles/", "/hacking/", "/hacking/cyberspace-basics/",
    "/hacking/programs/acquiring-writing-programs/", "/hacking/hacking-mechanics/",
    "/hacking/programs/program-subjects/", "/hacking/cyberspace-actions/",
    "/hacking/programs/program-verbs/", "/hacking/programs/", "/hacking/demons-watchdogs/",
]


class _Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tables, self.cur, self.row, self.cell = [], None, None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.cur = []
        elif self.cur is not None and tag == "tr":
            self.row = []
        elif self.cur is not None and tag in ("td", "th"):
            self.cell = []

    def handle_endtag(self, tag):
        if self.cur is None:
            return
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if any(self.row):
                self.cur.append(self.row)
            self.row = None
        elif tag == "table":
            self.tables.append(self.cur)
            self.cur = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


class _Heads(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hs, self.cur = [], None

    def handle_starttag(self, tag, attrs):
        if tag in ("h2", "h3", "h4"):
            self.cur = []

    def handle_endtag(self, tag):
        if tag in ("h2", "h3", "h4") and self.cur is not None:
            value = " ".join("".join(self.cur).split())
            if value:
                self.hs.append(value)
            self.cur = None

    def handle_data(self, data):
        if self.cur is not None:
            self.cur.append(data)


def _keyify(headers, ncol):
    keys, seen = [], {}
    for i, h in enumerate(headers[:ncol]):
        k = re.sub(r"[^a-z0-9]+", "_", h.lower()).strip("_") or f"col{i}"
        seen[k] = seen.get(k, 0) + 1
        if seen[k] > 1:
            k = f"{k}_{seen[k]}"
        keys.append(k)
    while len(keys) < ncol:
        keys.append(f"col{len(keys)}")
    return keys


def fetch(path: str) -> str:
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "NooPunk-SRD-extract/1"})
    with urllib.request.urlopen(req, timeout=30) as fh:
        return fh.read().decode("utf-8", "replace")


def build() -> dict:
    tables, pages = [], {}
    for path in PAGES:
        html = fetch(path)
        tp = _Tables()
        tp.feed(html)
        hp = _Heads()
        hp.feed(html)
        page = path.strip("/") or "index"
        pages[page] = {"headings": hp.hs, "tables": len(tp.tables)}
        for i, table in enumerate(tp.tables):
            if not table:
                continue
            header, body = table[0], table[1:]
            ncol = max([len(header)] + [len(r) for r in body]) if body else len(header)
            looks_header = bool(body) and not all(
                re.fullmatch(r"[-\d.$–—+%x\d]*", (c or "x")) for c in header)
            if looks_header:
                keys, data = _keyify(header, ncol), body
            else:
                keys, data = [f"col{j}" for j in range(ncol)], [header] + body
            records = []
            for row in data:
                row = list(row) + [""] * (ncol - len(row))
                records.append({keys[j]: row[j] for j in range(ncol)})
            tables.append({"id": f"{page}[{i}]", "page": page, "index": i, "headers": header,
                           "columns": keys, "rows": records, "n": len(records)})
    return {
        "format": "cwn-srd-tables-v1",
        "source": {
            "title": "Cities Without Number System Reference Document",
            "author": "Kevin Crawford / Sine Nomine Publishing",
            "url": "https://cwn.quadrifons.com/",
            "licence": "CC0 1.0 Universal (public domain dedication)",
            "scope": ("The SRD. Not the commercial book. This site omits optional magic/spellcasting "
                      "rules and the Antagonists & NPCs section."),
            "attribution": ("None required. Courtesy credit recorded in "
                            "data/sources/game_system_rights.json"),
        },
        "generated": "deterministic extraction by tools/cwn_srd_extract.py; no hand transcription",
        "counts": {"pages": len(pages), "tables": len(tables),
                   "rows": sum(t["n"] for t in tables)},
        "pages": pages,
        "tables": tables,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="compare the committed data with a fresh extraction")
    args = ap.parse_args()
    doc = build()
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "srd_tables.json"
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        fresh = json.loads(text)
        committed = json.loads(current) if current else {}
        if fresh["counts"] != committed.get("counts") or fresh["tables"] != committed.get("tables"):
            print("MISMATCH: data/rules/cwn/srd_tables.json is stale", file=sys.stderr)
            return 1
        print(f"OK: {fresh['counts']['tables']} tables, {fresh['counts']['rows']} rows match")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target} ({doc['counts']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
