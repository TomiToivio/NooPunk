#!/usr/bin/env python3
"""Extract the SWN Revised faction asset catalogue from the book's own tables (#1105, P0-B).

The faction turn cannot be finished without the asset catalogue, and #1105 says so plainly: "existing turn
code is **not proof of a finished asset catalogue**". The catalogue is pure numbers — HP, cost, tech level,
type, the attack line and the counterattack line — which are mechanics, not prose, so they can be
re-expressed here. The book's ability *descriptions* are not reproduced.

The extraction reads the three one-page tables (Cunning p.219, Force p.221, Wealth p.223), joins rows that
wrap across lines, and records each row's printed page. Run with the authorised copy to regenerate or check:

    python3 tools/swn_faction_assets.py --pdf ~/Lataukset/StarsWithoutNumberRevised-DeluxeEdition-011418.pdf
    python3 tools/swn_faction_assets.py --pdf … --check
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
OUT = ROOT / "data" / "rules" / "swn_faction_assets.json"

#: Where each category's table is printed (the facing page carries the prose descriptions).
TABLE_PAGES = {"Cunning": 219, "Force": 221, "Wealth": 223}
PRINTED_OFFSET = 3          # printed page 1 is PDF page 5 (verified against the running heads)

ROW = re.compile(
    r"^(?P<name>[A-Za-z][A-Za-z'&]*(?: [A-Za-z'&]+)*?)\s{2,}(?P<hp>\d+|\*|-)\s{2,}(?P<cost>\d+|\*)\s{2,}"
    r"(?P<tl>\d+)\s{2,}(?P<kind>[A-Za-z ]+?)\s{2,}(?P<rest>.+?)\s{2,}(?P<notes>[ASP, \-]*)$")
LEVEL = re.compile(r"^\s*(Cunning|Force|Wealth)\s+(\d)\s*$")

#: "Cunning vs. Wealth, 1d4 damage" -> attacker attribute, defender attribute, damage die.
ATTACK = re.compile(r"(?P<att>[A-Za-z]+)\s+vs\.?\s+(?P<def>[A-Za-z]+)(?:,?\s+(?P<damage>(?:\d+d\d+[+\-]?\d*|\d+|special).*))?", re.I)


def book_pages(pdf: Path) -> list[str]:
    if shutil.which("pdftotext") is None:
        raise SystemExit("pdftotext not found; install poppler-utils to regenerate the catalogue")
    raw = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    return raw.split("\f")


def _attack(text: str) -> dict:
    match = ATTACK.search(text)
    if not match:
        return {"attribute": "", "defence": "", "damage": "", "special": text.strip()}
    damage = (match.group("damage") or "").strip()
    if damage.lower().startswith("special"):
        return {"attribute": match.group("att"), "defence": match.group("def"),
                "damage": "", "special": "special"}
    damage = re.sub(r"\s*dmg\b|\s*damage\b", "", damage).strip().rstrip(".* ").strip()
    return {"attribute": match.group("att"), "defence": match.group("def"), "damage": damage,
            "special": ""}


def parse_table(category: str, page: str, printed: int) -> list[dict]:
    assets: list[dict] = []
    level = 0
    pending: dict | None = None
    for line in page.splitlines():
        marker = LEVEL.match(line)
        if marker and marker.group(1) == category:
            level = int(marker.group(2))
            pending = None
            continue
        row = ROW.match(line.strip())
        if row and level:
            pending = {
                "name": re.sub(r"\s{2,}", " ", row.group("name")).strip(),
                "hp": None if row.group("hp") in ("*", "-") else int(row.group("hp")),
                "cost": None if row.group("cost") == "*" else int(row.group("cost")),
                "tech_level": int(row.group("tl")),
                "type": row.group("kind").strip(),
                "attack_text": row.group("rest").strip(),
                "notes": sorted({token.strip() for token in row.group("notes").split(",")
                                 if token.strip() and token.strip() != "-"}),
                "level": level,
                "page": printed,
            }
            assets.append(pending)
            continue
        # A row whose attack column was cut off by a page break ends in "vs" / "vs." with no damage or
        # "None" after it; only then does the next line continue the same asset. (A looser heuristic
        # captured the following prose column and turned "3d8" into "3d8 age every time they …".)
        if pending is not None and line.strip():
            tail = pending["attack_text"].rstrip().lower()
            if tail.endswith("vs") or tail.endswith("vs."):
                pending["attack_text"] += " " + line.strip()
    for asset in assets:
        raw = asset.pop("attack_text")
        # The two cells keep their column padding in the raw line; splitting on it *before* collapsing
        # whitespace is what separates "1d4 damage" from the counter column's "None".
        cells = [cell.strip() for cell in re.split(r"\s{2,}", raw) if cell.strip()]
        attack_cell = cells[0] if cells else "None"
        counter = cells[1] if len(cells) > 1 else "None"
        asset["attack"] = _attack(attack_cell)
        if not asset["attack"]["attribute"]:
            asset["attack"]["special"] = "none"
        asset["counter"] = ("none" if counter.lower().startswith("none")
                            else "special" if counter.lower().startswith("special")
                            else re.sub(r"\s*dmg\b|\s*damage\b", "", counter).strip(" ."))
        asset["id"] = re.sub(r"[^a-z0-9]+", "_", asset["name"].lower()).strip("_")
        asset["category"] = category
    return assets


def build(pdf: Path) -> dict:
    pages = book_pages(pdf)
    rows: list[dict] = []
    for category, printed in TABLE_PAGES.items():
        rows.extend(parse_table(category, pages[printed + PRINTED_OFFSET], printed))
    # "Base of Influence" is printed once per table and is one asset with no fixed cost.
    by_id: dict[str, dict] = {}
    for row in rows:
        existing = by_id.get(row["id"])
        if existing is None:
            by_id[row["id"]] = row
            continue
        existing["categories"] = sorted({existing["category"], row["category"]})
    for row in by_id.values():
        row.setdefault("categories", [row["category"]])
    ordered = sorted(by_id.values(), key=lambda row: (row["category"], row["level"], row["name"]))
    return {
        "format": "noopunk.rules.swn_faction_assets",
        "version": 1,
        "issue": 1105,
        "source": {
            "title": "Stars Without Number: Revised Edition — Deluxe Edition",
            "isbn": "978-1-936673-95-7",
            "pages": {category: page for category, page in TABLE_PAGES.items()},
            "note": ("Numbers only: hit points, cost, tech level, type, the attack and counterattack lines. "
                     "The book's ability descriptions and its lettered note legend (A/S/P) are NOT "
                     "reproduced; the codes are recorded so a reader can look them up."),
        },
        "assets": ordered,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pdf", type=Path, default=os.environ.get("SWN_DELUXE_PDF", ""))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args(argv)
    if not args.pdf or not Path(args.pdf).is_file():
        print("swn_faction_assets: pass --pdf or set SWN_DELUXE_PDF", file=sys.stderr)
        return 2
    data = build(Path(args.pdf))
    text = json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    if args.check:
        current = args.out.read_text(encoding="utf-8") if args.out.is_file() else ""
        if current != text:
            print(f"swn_faction_assets: {args.out.relative_to(ROOT)} is stale", file=sys.stderr)
            return 1
        print(f"swn_faction_assets: up to date ({len(data['assets'])} assets)")
        return 0
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    print(f"swn_faction_assets: {len(data['assets'])} assets -> {args.out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
