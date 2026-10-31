"""The image manifest is a contract, so something has to check it (#908).

`images/manifest.json` says which artwork the game may show, where it lives, what it depicts and whether
it is approved. A JSON file nobody validates drifts the first time someone adds an asset by hand: a
category that does not exist, a portrait cropped to 16:9, a hash from a file that was re-exported, or —
the rule this issue cares most about — science-fiction scenery in an early-Helsinki scene that nobody
asked for.

This module is the checker. It is stdlib-only on purpose: it runs in CI, in `unittest`, and on a fresh
clone with no image libraries installed, and it reads PNG/WebP headers itself rather than trusting the
author's note about dimensions.

Nothing here needs Godot. `godot/ui/image_library.gd` reads the same manifest at runtime and refuses the
same assets, so the two cannot disagree about what is approved.
"""
from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path
from typing import Any, Iterable, Mapping

__all__ = [
    "CATEGORY_ASPECTS",
    "CATEGORIES",
    "PROJECT_ROOT",
    "MANIFEST",
    "approved_assets",
    "image_size",
    "load",
    "resolve",
    "validate",
]

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = PROJECT_ROOT / "images" / "manifest.json"

#: The four asset classes, and the aspect ratios each may use. #908 fixes the compositions: a portrait is
#: 3:4 or 2:3 so a face is not cropped by a wide frame, locations are 16:9, encounters and events are the
#: two wide shapes. (width, height) pairs, reduced.
CATEGORY_ASPECTS: dict[str, tuple[tuple[int, int], ...]] = {
    "characters/portraits": ((3, 4), (2, 3)),
    "social_encounters": ((4, 3), (16, 9)),
    "locations": ((16, 9),),
    "events": ((4, 3), (16, 9)),
}
CATEGORIES: tuple[str, ...] = tuple(CATEGORY_ASPECTS)
SUFFIXES = {".png", ".webp"}
SCHEMA_VERSION = 1
MANIFEST_ROOT = "res://images/"

#: Aspect tolerance: an export may be a pixel off after rescaling, and that is not a defect.
ASPECT_TOLERANCE = 0.02


def load(path: Path = MANIFEST) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _slug(asset_id: str) -> bool:
    return bool(asset_id) and asset_id == asset_id.lower() and all(
        part and part.isalnum() for part in asset_id.split("_")) and "__" not in asset_id


def _aspect_ok(width: int, height: int, category: str) -> bool:
    if width <= 0 or height <= 0:
        return False
    ratio = width / height
    return any(abs(ratio - (w / h)) <= ASPECT_TOLERANCE for w, h in CATEGORY_ASPECTS[category])


def image_size(data: bytes) -> tuple[int, int] | None:
    """Read (width, height) from a PNG or WebP header without decoding the image."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP" and len(data) >= 30:
        chunk = data[12:16]
        if chunk == b"VP8X":  # extended: 24-bit canvas size, minus one
            width = int.from_bytes(data[24:27], "little") + 1
            height = int.from_bytes(data[27:30], "little") + 1
            return width, height
        if chunk == b"VP8L":  # lossless: 14 bits each, biased by one
            bits = int.from_bytes(data[21:25], "little")
            return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
        if chunk == b"VP8 ":  # lossy: 14-bit size after the 3-byte start code
            start = data.find(b"\x9d\x01\x2a", 20)
            if start != -1:
                width, height = struct.unpack("<HH", data[start + 3:start + 7])
                return width & 0x3FFF, height & 0x3FFF
    return None


def _file_problems(asset: Mapping[str, Any], project_root: Path) -> list[str]:
    """An approved asset is only approved if the bytes are there and match their record."""
    asset_id = str(asset.get("id", ""))
    relative = str(asset.get("path", "")).removeprefix(MANIFEST_ROOT)
    path = project_root / MANIFEST_ROOT.removeprefix("res://") / relative
    if not path.is_file():
        return [f"{asset_id}: approved asset has no file at {asset.get('path')}"]
    data = path.read_bytes()
    problems: list[str] = []
    digest = hashlib.sha256(data).hexdigest()
    if str(asset.get("sha256", "")).lower() != digest:
        problems.append(f"{asset_id}: sha256 does not match the committed file")
    measured = image_size(data)
    declared = asset.get("dimensions") or {}
    if measured is None:
        problems.append(f"{asset_id}: not a readable PNG/WebP")
    else:
        width, height = measured
        if (int(declared.get("width", 0)), int(declared.get("height", 0))) != (width, height):
            problems.append(
                f"{asset_id}: dimensions say {declared}, file is {width}x{height}")
        if not _aspect_ok(width, height, str(asset.get("category", ""))):
            problems.append(
                f"{asset_id}: {width}x{height} is not an allowed composition for "
                f"{asset.get('category')} ({CATEGORY_ASPECTS.get(str(asset.get('category')), ())})")
    return problems


def validate(manifest: Mapping[str, Any], project_root: Path = PROJECT_ROOT) -> list[str]:
    """Return every problem found. An empty list means the manifest is a truthful contract."""
    problems: list[str] = []
    if int(manifest.get("schema_version", 0)) != SCHEMA_VERSION:
        problems.append(f"schema_version must be {SCHEMA_VERSION}")
    if str(manifest.get("root")) != MANIFEST_ROOT:
        problems.append(f"root must be {MANIFEST_ROOT}")
    declared_categories = tuple(manifest.get("categories") or ())
    if declared_categories != CATEGORIES:
        problems.append(f"categories must be {CATEGORIES}, found {declared_categories}")

    seen: set[str] = set()
    for asset in manifest.get("assets") or []:
        asset_id = str(asset.get("id", ""))
        category = str(asset.get("category", ""))
        if not _slug(asset_id):
            problems.append(f"{asset_id!r}: id must be lowercase snake_case")
        if asset_id in seen:
            problems.append(f"{asset_id}: duplicate id")
        seen.add(asset_id)
        if category not in CATEGORY_ASPECTS:
            problems.append(f"{asset_id}: unknown category {category!r}")
            continue
        expected_prefix = f"{MANIFEST_ROOT}{category}/"
        if not str(asset.get("path", "")).startswith(expected_prefix):
            problems.append(f"{asset_id}: path must live under {expected_prefix}")
        if Path(str(asset.get("path", ""))).suffix.lower() not in SUFFIXES:
            problems.append(f"{asset_id}: path must end in {sorted(SUFFIXES)}")
        for field in ("licence", "provenance"):
            if not str(asset.get(field, "")).strip():
                problems.append(f"{asset_id}: {field} is required")
        # #908: background science fiction is opt-in. A motif must be justified in the same record, so an
        # unattended generation pass cannot quietly add a skyline to a Helsinki street.
        motifs = asset.get("sci_fi_motifs") or []
        if motifs and not str(asset.get("sci_fi_justification", "")).strip():
            problems.append(f"{asset_id}: sci_fi_motifs {motifs} need sci_fi_justification")
        if asset.get("approved") is not True:
            problems.append(f"{asset_id}: listed in assets but not approved")
            continue
        problems.extend(_file_problems(asset, project_root))

    for entry in manifest.get("pending") or []:
        asset_id = str(entry.get("id", ""))
        if not _slug(asset_id):
            problems.append(f"pending {asset_id!r}: id must be lowercase snake_case")
        if asset_id in seen:
            problems.append(f"{asset_id}: duplicate id across assets and pending")
        seen.add(asset_id)
        category = str(entry.get("category", ""))
        if category not in CATEGORY_ASPECTS:
            problems.append(f"pending {asset_id}: unknown category {category!r}")
        target = str(entry.get("target_path", ""))
        if not target.startswith(f"{MANIFEST_ROOT}{category}/"):
            problems.append(f"pending {asset_id}: target_path must live under {MANIFEST_ROOT}{category}/")
        if not str(entry.get("status", "")).strip():
            problems.append(f"pending {asset_id}: status is required")
        # The sci-fi rule binds the *direction* too: an unrequested skyline is easiest to slip in while
        # writing a brief, before any pixels exist.
        motifs = entry.get("sci_fi_motifs") or []
        if motifs and not str(entry.get("sci_fi_justification", "")).strip():
            problems.append(f"pending {asset_id}: sci_fi_motifs {motifs} need sci_fi_justification")
        # A file that exists is no longer pending. Promoting it is the act that makes it showable, and
        # `resolve()` will not return it until someone does.
        if (project_root / MANIFEST_ROOT.removeprefix("res://") /
                target.removeprefix(MANIFEST_ROOT)).is_file():
            problems.append(
                f"pending {asset_id}: the binary exists at {target} — promote it to assets with its "
                f"sha256, dimensions and licence")
    return problems


def approved_assets(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    """The assets the game may actually load: approved, and nothing else."""
    return {str(a.get("id", "")): dict(a) for a in manifest.get("assets") or []
            if a.get("approved") is True}


def resolve(manifest: Mapping[str, Any], asset_id: str,
            project_root: Path = PROJECT_ROOT) -> Path | None:
    """Path to an approved asset whose bytes are present, or ``None``. Never guesses."""
    asset = approved_assets(manifest).get(asset_id)
    if asset is None or _file_problems(asset, project_root):
        return None
    return project_root / MANIFEST_ROOT.removeprefix("res://") / str(
        asset["path"]).removeprefix(MANIFEST_ROOT)


def describe(manifest: Mapping[str, Any]) -> Iterable[str]:
    """Human-readable inventory, for an operator wondering what is actually usable."""
    for asset_id, asset in sorted(approved_assets(manifest).items()):
        yield f"{asset_id}\t{asset.get('category')}\t{asset.get('path')}"
    for entry in manifest.get("pending") or []:
        yield f"{entry.get('id')}\tPENDING\t{entry.get('status')}"
