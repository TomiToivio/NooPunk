#!/usr/bin/env python3
"""Generate the pre-narrative rulebook archive manifest for issue #265.

#265 requires the complete old corpus to stay retrievable, with a *tested* inventory, and warns
against mistaking a partial duplicate for the whole thing. So this tool does three jobs:

1. Classifies every rulebook-shaped file as `canonical`, `derived` or `distinct`, by measuring
   how much of its prose already exists in RULEBOOK.md. This is the part that matters: four
   things in the tree look like "the rulebook", and two of them are generated views.
2. Emits `archive/rulebook-pre-narrative-2026-10/MANIFEST.json` with a sha256 for every file, the
   commit it was taken from and its classification.
3. Is re-runnable: the guard regenerates and compares, so the manifest cannot silently go stale.

Retrieval is by immutable annotated tag, not by copying 2.3 MB of text into the archive. The
manifest is what makes the tag verifiable, file by file.

Usage:
    python3 tools/issue265_archive_manifest.py            # write MANIFEST.json
    python3 tools/issue265_archive_manifest.py --check    # fail if stale
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "rulebook-pre-narrative-2026-10"
MANIFEST = ARCHIVE / "MANIFEST.json"
TAG = "rulebook-pre-narrative-2026-10"
SUBSTANTIVE = 40  #: minimum line length to count as prose rather than markdown furniture


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def corpus() -> list[pathlib.Path]:
    """Every rulebook-shaped file: the canonical text and all derived/distinct views."""
    files = [ROOT / "RULEBOOK.md"]
    for pattern in ("rulebook/**/*.md", "rulebook_parts/**/*.md", "docs/rulebook_segments/**/*.md"):
        files += sorted(p for p in ROOT.glob(pattern) if p.is_file())
    return sorted(set(files))


def substantive_lines(path: pathlib.Path) -> list[str]:
    return [s for s in (ln.strip() for ln in path.read_text(encoding="utf-8").splitlines())
            if len(s) >= SUBSTANTIVE]


def classify(path: pathlib.Path, canonical_lines: set[str]) -> tuple[str, float, int]:
    """`canonical` for RULEBOOK.md itself; otherwise by prose overlap with it."""
    if path.name == "RULEBOOK.md":
        return "canonical", 1.0, len(canonical_lines)
    lines = substantive_lines(path)
    if not lines:
        return "distinct", 0.0, 0
    share = sum(1 for ln in lines if ln in canonical_lines) / len(lines)
    if share >= 0.85:
        kind = "derived"          # a generated view of RULEBOOK.md; regenerable, not new content
    elif share <= 0.15:
        kind = "distinct"         # prose that exists nowhere in RULEBOOK.md; must be preserved
    else:
        kind = "partial"          # index/generated with some shared headings
    return kind, round(share, 3), len(lines)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.strip()


def build() -> dict:
    canonical_lines = set(substantive_lines(ROOT / "RULEBOOK.md"))
    entries: list[dict[str, Any]] = []
    for path in corpus():
        kind, share, lines = classify(path, canonical_lines)
        entries.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "classification": kind,
            "prose_overlap_with_canonical": share,
            "substantive_lines": lines,
        })
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry["classification"]] = counts.get(entry["classification"], 0) + 1
    return {
        "$comment": ("Archive manifest for the pre-narrative rulebook corpus. Retrieval is by the "
                     "annotated tag below; this manifest makes that tag verifiable file by file. "
                     "`derived` entries are generated views whose content already exists in "
                     "RULEBOOK.md; `distinct` entries carry prose that exists nowhere else and "
                     "must survive the migration."),
        "issue": 265,
        "archive": "archive/rulebook-pre-narrative-2026-10",
        "tag": TAG,
        "source_commit": git("rev-parse", "HEAD"),
        "source_date": git("show", "-s", "--format=%cI", "HEAD"),
        "totals": {
            "files": len(entries),
            "bytes": sum(e["bytes"] for e in entries),
            "by_classification": counts,
        },
        "files": entries,
    }


def main() -> int:
    manifest = build()
    if "--check" in sys.argv:
        if not MANIFEST.exists():
            print(f"{MANIFEST.relative_to(ROOT)} is missing", file=sys.stderr)
            return 1
        on_disk = json.loads(MANIFEST.read_text(encoding="utf-8"))
        # the commit is expected to move; the file list and hashes are not
        for key in ("files", "totals", "tag", "archive"):
            if on_disk.get(key) != manifest.get(key):
                print(f"manifest is stale in `{key}`; regenerate it", file=sys.stderr)
                return 1
        print("archive manifest is current")
        return 0
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    totals = manifest["totals"]
    print(f"wrote {MANIFEST.relative_to(ROOT)}: {totals['files']} files, "
          f"{totals['bytes'] / 1024:.0f} KB, {totals['by_classification']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
