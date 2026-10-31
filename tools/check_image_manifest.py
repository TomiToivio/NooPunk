#!/usr/bin/env python3
"""Validate the image manifest (#908).

An art pipeline rots in a specific way: the manifest says one thing, the directory holds another, and by
the time a screen is wired the path is wrong and nobody remembers what the image was for. This checks the
things a machine can check, before any of that happens.

Rules enforced here:

* every entry has the required fields, with a non-empty provenance;
* ids are unique and snake_case;
* filenames are lowercase snake_case;
* the file lives in the directory its class names;
* declared dimensions match the actual pixels (for files that exist);
* a `sci_fi` motif carries a justification — early Helsinki is a lived-in 1970s city and the uncanny is an
  event, not a backdrop;
* an entry marked `approved` carries provenance that is not a placeholder.

Usage:
    python3 tools/check_image_manifest.py [--json]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "images" / "manifest.json"

#: Category -> the effect it has on how a screen may present the image. The category is also the
#: directory: one category, one home (#909's taxonomy, kept).
CATEGORY_KIND = {
    "characters/portraits": "portrait",
    "social_encounters": "encounter",
    "locations": "location",
    "events": "event",
    "placeholders": "placeholder",
}

REQUIRED = ("id", "category", "path", "subjects", "location", "aspect", "dimensions",
            "provenance", "approved")

SNAKE = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
ID = re.compile(r"^[a-z0-9]+(?:_[a-z0-9]+)*$")

#: Motifs that must be argued for, because they change what the setting looks like.
JUSTIFIED_MOTIFS = {"sci_fi"}


def _dimensions(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image
    except ImportError:  # pragma: no cover - dev convenience
        return None
    with Image.open(path) as image:
        return image.size


def validate(manifest: dict, root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()

    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        return ["manifest has no assets list"]

    for index, entry in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(entry, dict):
            problems.append(f"{label}: not an object")
            continue
        missing = [key for key in REQUIRED if key not in entry]
        if missing:
            problems.append(f"{label}: missing {', '.join(missing)}")
            continue

        asset_id = str(entry["id"])
        label = asset_id or label
        if not ID.match(asset_id):
            problems.append(f"{label}: id is not lowercase snake_case")
        if asset_id in seen:
            problems.append(f"{label}: duplicate id")
        seen.add(asset_id)

        if str(entry.get("provenance", "")).strip() == "":
            problems.append(f"{label}: empty provenance")

        category = str(entry["category"])
        if category not in CATEGORY_KIND:
            problems.append(f"{label}: unknown category {category!r}")
            continue
        rel = str(entry["path"])
        if not rel.startswith("res://images/"):
            problems.append(f"{label}: path must start with res://images/")
            continue
        relative = rel[len("res://images/"):]
        wanted = category + "/"
        if not relative.startswith(wanted):
            problems.append(f"{label}: category {category} belongs in {wanted}, path is {relative}")

        filename = Path(relative).name
        if Path(filename).suffix.lower() not in {".png", ".webp", ".jpg", ".jpeg"}:
            problems.append(f"{label}: unsupported image extension {Path(filename).suffix!r}")
        if not SNAKE.match(Path(filename).stem):
            problems.append(f"{label}: filename {filename!r} is not lowercase snake_case")

        absolute = root / "images" / relative
        if not absolute.exists():
            problems.append(f"{label}: file missing: {relative}")
        else:
            declared = entry.get("dimensions")
            actual = _dimensions(absolute)
            if actual is not None:
                if not isinstance(declared, list) or len(declared) != 2:
                    problems.append(f"{label}: dimensions must be [width, height]")
                elif [int(declared[0]), int(declared[1])] != [actual[0], actual[1]]:
                    problems.append(
                        f"{label}: declares {declared[0]}x{declared[1]}, file is {actual[0]}x{actual[1]}")

        if not isinstance(entry.get("subjects"), list):
            problems.append(f"{label}: subjects must be a list")

        motifs = entry.get("motifs", [])
        if not isinstance(motifs, list):
            problems.append(f"{label}: motifs must be a list")
        else:
            for motif in motifs:
                if motif in JUSTIFIED_MOTIFS and not str(entry.get("justification", "")).strip():
                    problems.append(
                        f"{label}: motif {motif!r} requires a justification — early Helsinki has no "
                        f"unexplained sci-fi backdrop")
                if motif in JUSTIFIED_MOTIFS and CATEGORY_KIND[category] != "event":
                    problems.append(
                        f"{label}: motif {motif!r} belongs to an events asset, not {category}")

        if bool(entry.get("approved")) and "placeholder" in str(entry.get("provenance", "")).lower():
            problems.append(f"{label}: a placeholder cannot be approved art")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--manifest", default=str(MANIFEST))
    args = parser.parse_args()

    path = Path(args.manifest)
    if not path.exists():
        print(f"missing manifest: {path}", file=sys.stderr)
        return 2
    manifest = json.loads(path.read_text())
    problems = validate(manifest, root=path.parent.parent)

    if args.json:
        print(json.dumps({"ok": not problems, "problems": problems}, indent=2))
    else:
        if problems:
            for problem in problems:
                print(f"FAIL {problem}")
            print(f"{len(problems)} problem(s)")
        else:
            print(f"image manifest OK — {len(manifest['assets'])} asset(s)")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
