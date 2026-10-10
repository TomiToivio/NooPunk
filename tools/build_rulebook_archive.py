#!/usr/bin/env python3
"""Build the pre-narrative rulebook archive for issue #265.

Produces, deterministically and re-runnably:

  archive/rulebook-pre-narrative-2026-10/MANIFEST.md     human-readable inventory
  archive/rulebook-pre-narrative-2026-10/manifest.json   machine-readable inventory
  archive/rulebook-pre-narrative-2026-10/MIGRATION_MAP.md  section-by-section supersession map

Design rules:
  * #243 already made a lossless inventory + exact snapshot of the root RULEBOOK.md and
    rulebook_parts/. This tool **extends** that; it does not duplicate or undo it. Where a
    source is already snapshotted by #243 the manifest says so and points at it.
  * Nothing is deleted and nothing is silently discarded: every legacy unit gets a
    destination. A unit whose destination is genuinely unclear is marked REVIEW, not guessed.
  * Hashes are content hashes plus git blob shas, so a reader can prove retrievability.

Usage: python3 tools/build_rulebook_archive.py [--check]
  --check  verify the on-disk archive matches what the generator would write (guard mode)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "archive" / "rulebook-pre-narrative-2026-10"
TAG = "rulebook-pre-narrative-2026-10"

# --------------------------------------------------------------------------------------
# The twelve proposed introductory chapters of the new narrative-first rulebook (#265).
# --------------------------------------------------------------------------------------
# The new entry point is part of the *new* book, not the legacy corpus: never inventoried as legacy.
EXCLUDE = {"00_START_HERE.md"}

NEW_CHAPTERS = {
    "01": "What is NoöPunk? Premise and narrative-first play",
    "02": "The six attributes: FIT / REF / INT / SOC / PSY / CYB",
    "03": "Character creation: Academy, background, skills, call-sign",
    "04": "Playing scenes: dialogue, checks and meaningful consequences",
    "05": "Social relationships, companions and NPC agency",
    "06": "Psyche, beliefs, thoughts, dreams and personal change",
    "07": "Investigation, evidence, decisions and clocks",
    "08": "The three realities and access/embodiment constraints",
    "09": "Simple conflict and consequences",
    "10": "Running a UNSA case; first Helsinki/Ö-Mappi adventure",
    "11": "Tabletop / Godot / Concordia parity and terminology",
    "12": "Optional/deferred advanced-system roadmap and historical-source references",
}

# Legacy file sets that are *generated derivatives* of another source: they carry no
# independent content, so they are preserved but not individually reconciled.
DERIVATIVE_SETS = {
    "rulebook/parts": "generated verbatim segments of RULEBOOK.md (tools/split_rulebook.py); guard-enforced",
    "docs/rulebook_segments": "generated per-book segments of RULEBOOK.md (#232 split work)",
}

# Exact-title overrides, checked before the keyword rules. Use where a keyword rule would
# land the unit in a defensible but *less* correct place.
OVERRIDES: dict[str, tuple[str, str | None, str]] = {
    "36. The four NoöPunk systems: Physical, Psychic, Social and Cybernetic":
        ("NEW-CORE", "08", "the systems overview becomes the three-realties + Social-dimension chapter"),
    "5. Physical Systems": ("NEW-CORE", "09", "lightweight conflict; no grid in the first edition"),
    "19. AI, AGI, infomorphs, and non-human agents":
        ("LORE", None, "AI/NHI canon retained as lore"),
    "33. Canonical world lore from issue #60": ("LORE", None, "world canon retained as lore/reference"),
    "38. UNSA: default campaign institution": ("LORE", None, "institution canon retained; the *case* is chapter 10"),
}

# Ordered keyword rules. First match wins. (pattern, destination, chapter, note)
KEYWORD_RULES: list[tuple[str, str, str | None, str]] = [
    # --- historical / self-description (checked early: these are old process text) ------
    (r"subset|test-session", "HISTORICAL", None, "old test-session subset; kept as history"),
    (r"what this document is|current project description|change ledger|rule-change|rule change|healthy rulebook|governing principle|immediate rulebook work",
     "HISTORICAL", None, "process/self-description of the old book; kept as history"),
    (r"provenance|source hierarchy|licensing boundary|eclipse phase", "HISTORICAL", None, "licensing/provenance record; retained for attribution"),
    (r"core architecture|kernel|scale migration", "HISTORICAL", None, "old numeric kernel; explicitly historical, not reinstated"),
    # --- new core ---------------------------------------------------------------------
    (r"introduction to noöpunk|what is noöpunk|premise", "NEW-CORE", "01", "the opening premise, rewritten narrative-first"),
    (r"\bstats\b|\battributes\b|\baptitudes\b", "NEW-CORE", "02", "six attributes carried forward as independent axes"),
    (r"skills", "NEW-CORE", "03", "canonical 40-skill catalogue retained pending the #263 crosswalk"),
    (r"character generation|character creation|lifepath|characters and identity",
     "NEW-CORE", "03", "Academy newcomer, flexible background, player-chosen call-sign"),
    (r"social|affect|motivation|reputation|npcs?\b", "NEW-CORE", "05", "relationships are a core pillar; reuse #220/#144 affect graph"),
    (r"psychic|psionic|\bpsi\b|psyche|dream|sleep", "NEW-CORE", "06", "Psyche is distinct from PSI; both retained"),
    (r"narrative layer|aspect|gm move", "NEW-CORE", "04", "aspects/consequences/GM moves feed the scene chapter"),
    (r"investigat|evidence|forensic|case template", "NEW-CORE", "07", "evidence/hypothesis separation, no one-roll softlocks"),
    (r"action resolution|smallest playable|pools and expendable|escape hatch|adapter contract|resolution",
     "NEW-CORE", "04", "formula UNDECIDED under #262; legacy engines are reference only"),
    (r"mesh|hacking|cyberspace|noösphere|noosphere|cybernetic", "NEW-CORE", "08", "Cyber layer; #222 four modes retained"),
    (r"cross[-_]domain|realm|embodiment|morph|body|bodies|platform|astral|projection",
     "NEW-CORE", "08", "Physical/Cyber/Astral access and embodiment limits"),
    (r"physical systems|\bcombat\b|physical harm|wound|damage", "NEW-CORE", "09", "lightweight abstract conflict; no grid in the first edition"),
    (r"persistence|reproducib|structured actions for concordia|parity|godot",
     "NEW-CORE", "11", "deterministic event record shared by tabletop/Godot/Concordia"),
    # --- lore / reference -------------------------------------------------------------
    (r"sources|recommended reading|influences|theoretical source|bibliograph", "LORE", None, "provenance and bibliography retained"),
    (r"equipment|gear|augmentation|implant|technology|field catalog", "LORE", None, "equipment catalogues retained as reference"),
    (r"glossary|timeline|history|ontology|beings|xenopolitic|confederacy|orion|singul|nh\w|cryptoterrestrial|\bcontact\b|disclosure|world lore|doctrine|verification|unsa|academy|institution|faction|political part|parliament|infomorph|non-human",
     "LORE", None, "world canon retained as lore/reference"),
]

# Per-chapter overrides for files whose H1 does not carry a classifiable keyword.
CHAPTER_OVERRIDES: dict[str, tuple[str, str | None, str]] = {
    "1_NOÖPUNK.md": ("NEW-CORE", "01", "the premise chapter of the new book"),
    "3_PHYSICAL.md": ("NEW-CORE", "09", "lightweight conflict; no grid in the first edition"),
}

DESTINATIONS = {
    "NEW-CORE": "New narrative-first chapter (see chapter number)",
    "DEFERRED": "Deferred advanced supplement (later edition)",
    "LORE": "Lore / reference material (retained, not a rule)",
    "HISTORICAL": "Historical archive only (never quietly reinstated)",
    "REVIEW": "Needs author review — destination not safely inferable",
}


def git_blob_sha(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path)], cwd=REPO, capture_output=True, text=True, check=False
    ).stdout.strip()


def digest(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def classify(title: str) -> tuple[str, str | None, str]:
    if title in OVERRIDES:
        return OVERRIDES[title]
    t = title.lower()
    for pattern, dest, chapter, note in KEYWORD_RULES:
        if re.search(pattern, t):
            return dest, chapter, note
    return "REVIEW", None, "no keyword rule matched; author decides the destination"


def legacy_sources() -> list[Path]:
    """Every distinct legacy source, in a stable order."""
    out: list[Path] = []
    out.append(REPO / "RULEBOOK.md")
    for p in sorted((REPO / "rulebook").glob("[0-9]*.md")):
        if p.name not in EXCLUDE:
            out.append(p)  # chapters + 00_INDEX (legacy only)
    for d in ("rulebook/parts", "rulebook_parts", "docs/rulebook_segments"):
        for p in sorted((REPO / d).glob("*.md")):
            out.append(p)
    for p in sorted((REPO / "docs" / "archive").glob("RULEBOOK*.md")):
        out.append(p)
    for p in sorted((REPO / "docs" / "archive").glob("*RULEBOOK*.md")):
        if p not in out:
            out.append(p)
    for j in ("data/rules/rulebook_segmentation.json", "data/rules/rulebook_split_manifest.json",
              "data/rules/fudge_scale_migration.json", "docs/rulebook_consolidation/inventory.json"):
        q = REPO / j
        if q.exists():
            out.append(q)
    return [p for p in out if p.exists()]


def rulebook_sections() -> list[tuple[str, int]]:
    """(heading, line) for every '## ' section of RULEBOOK.md, excluding 'Contents'."""
    secs: list[tuple[str, int]] = []
    for i, line in enumerate((REPO / "RULEBOOK.md").read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## ") and line.strip() != "## Contents":
            secs.append((line[3:].strip(), i))
    return secs


def build() -> dict[str, str]:
    srcs = legacy_sources()
    rows = []
    for p in srcs:
        sha, size = digest(p)
        rel = str(p.relative_to(REPO))
        if rel == "RULEBOOK.md":
            where = "rulebook/source_snapshots/root/RULEBOOK.md"
        elif rel.startswith("rulebook_parts/"):
            where = "rulebook/source_snapshots/" + rel
        else:
            where = "in place (not deleted)"
        rows.append({
            "source": rel,
            "bytes": size,
            "sha256": sha,
            "git_blob_sha": git_blob_sha(p),
            "preserved_at": where,
        })

    # ---- manifest -------------------------------------------------------------------
    m = [f"# Archive manifest — `{TAG}`", "",
         "Complete inventory of the pre-narrative NoöPunk rulebook corpus, with content hashes so",
         "retrievability is provable rather than claimed. Generated by `tools/build_rulebook_archive.py`.", "",
         f"- **Immutable tag:** `{TAG}` — an annotated tag marking the **pre-narrative baseline**",
         "  (published before this archive; it covers the full legacy corpus). This archive directory is",
         "  the discoverable inventory and migration map for that baseline.",
         "- **Nothing was deleted**, so the baseline remains readable in the tree at every path listed below.",
         "- **#243 relationship:** #243 produced a *lossless inventory and exact snapshot* of the root",
         "  `RULEBOOK.md` and `rulebook_parts/` (`docs/rulebook_consolidation/inventory.json`,",
         "  `rulebook/source_snapshots/`), and explicitly did **not** reconcile. This archive extends that",
         "  inventory to the remaining corpus and adds the migration map. #243's work is reused, not undone.",
         "- **Nothing is deleted.** Every file below is still present at its original path.", "",
         "## Distinct sources", "",
         "| Source | Bytes | sha256 (first 16) | Preserved at |", "| --- | --- | --- | --- |"]
    for r in rows:
        m.append(f"| `{r['source']}` | {r['bytes']:,} | `{r['sha256'][:16]}` | {r['preserved_at']} |")
    m += ["", "## Generated derivatives (preserved, no independent content)", "",
          "| Set | Nature |", "| --- | --- |"]
    for k, v in DERIVATIVE_SETS.items():
        m.append(f"| `{k}/` | {v} |")
    m += ["", "## Verification", "", "```sh",
          "python3 tools/build_rulebook_archive.py --check   # hashes must match on-disk",
          "git show " + TAG + "                            # the immutable annotated tag", "```", ""]

    manifest = "\n".join(m)

    man_json = {
        "format": "noopunk.rulebook.archive",
        "version": 1,
        "issue": 265,
        "tag": TAG,
        "extends": {"issue": 243, "inventory": "docs/rulebook_consolidation/inventory.json",
                    "snapshots": "rulebook/source_snapshots/"},
        "hash_type": "sha256+git_blob_sha1",
        "deleted_anything": False,
        "files": rows,
        "generated_derivatives": DERIVATIVE_SETS,
    }

    # ---- migration map --------------------------------------------------------------
    secs = rulebook_sections()
    mm = [f"# Migration and supersession map — `{TAG}`", "",
          "Every legacy unit below maps to exactly one destination. **Nothing is silently discarded.**",
          "`REVIEW` means the destination is not safely inferable and the author decides — it is not a",
          "guess and not a silent drop. Old numerical/tactical rules are marked `HISTORICAL`: retained",
          "and readable, **never quietly reinstated** as canon.", "",
          "## Destinations", ""]
    for k, v in DESTINATIONS.items():
        mm.append(f"- **{k}** — {v}")
    mm += ["", "## New narrative-first chapters (target of `NEW-CORE`)", "",
           "| Chapter | Title |", "| --- | --- |"]
    for num, title in NEW_CHAPTERS.items():
        mm.append(f"| {num} | {title} |")

    mm += ["", f"## A. `RULEBOOK.md` sections ({len(secs)} units)", "",
           "| Line | Legacy section | Destination | Chapter | Note |", "| --- | --- | --- | --- | --- |"]
    for title, line in secs:
        dest, chap, note = classify(title)
        mm.append(f"| {line} | {title} | **{dest}** | {chap or '—'} | {note} |")

    chapters = sorted(p for p in (REPO / "rulebook").glob("[0-9]*.md") if p.name not in EXCLUDE)
    mm += ["", f"## B. `rulebook/` chapters ({len(chapters)} units)", "",
           "| Legacy chapter | Destination | Chapter | Note |", "| --- | --- | --- | --- |"]
    for p in chapters:
        title = p.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip() if p.stat().st_size else p.name
        if p.name == "00_INDEX.md":
            dest, chap, note = "HISTORICAL", None, "generated table of contents for the old split; superseded by the new entry point"
        elif p.name in CHAPTER_OVERRIDES:
            dest, chap, note = CHAPTER_OVERRIDES[p.name]
        else:
            dest, chap, note = classify(title + " " + p.name)
        mm.append(f"| `{p.name}` | **{dest}** | {chap or '—'} | {note} |")

    mm += ["", "## C. Distinct legacy source sets", "",
           "| Set | Count | Destination | Note |", "| --- | --- | --- | --- |",
           f"| `rulebook_parts/` | {len(list((REPO / 'rulebook_parts').glob('*.md')))} | **HISTORICAL** | earlier modular draft; snapshotted by #243 |",
           f"| `rulebook/parts/` | {len(list((REPO / 'rulebook' / 'parts').glob('*.md')))} | **HISTORICAL** | generated segments of `RULEBOOK.md` |",
           f"| `docs/rulebook_segments/` | {len(list((REPO / 'docs' / 'rulebook_segments').glob('*.md')))} | **HISTORICAL** | generated per-book segments (#232) |",
           f"| `docs/archive/` | {len(list((REPO / 'docs' / 'archive').glob('*.md')))} | **HISTORICAL** | pre-existing archive; untouched |",
           "", "## D. Machine-readable definitions", "",
           "| File | Destination | Note |", "| --- | --- | --- |",
           "| `data/rules/rulebook_segmentation.json` | **HISTORICAL** | describes the old split |",
           "| `data/rules/rulebook_split_manifest.json` | **HISTORICAL** | describes the old split |",
           "| `data/rules/fudge_scale_migration.json` | **HISTORICAL** | old scale migration; reference only |",
           "| `data/rules/skills.json` | **NEW-CORE** (03) | **retained unchanged** — pending the #263 crosswalk |",
           "| `data/rules/core.json` | **REVIEW** | live kernel; its fate is #262's dice decision, not this issue |",
           "", "## E. Not superseded", "",
           "Character/world canon, the licensing and attribution record, and every test remain in force.",
           "This map supersedes *presentation and structure*, not the setting.", ""]

    migration = "\n".join(mm)

    readme = f"""# `{TAG}` — pre-narrative rulebook archive

This directory is the discoverable entry point to the **complete pre-narrative NoöPunk rulebook
corpus**. It documents the immutable annotated tag **`{TAG}`**, which marks the pre-narrative
baseline (published before this archive, covering the full legacy corpus).

- **[MANIFEST.md](MANIFEST.md)** — every distinct legacy source with byte size and sha256, and where
  its preserved copy lives. Nothing was deleted; every file is still at its original path.
- **[MIGRATION_MAP.md](MIGRATION_MAP.md)** — section-by-section: each legacy unit's destination (new
  chapter, deferred supplement, lore/reference, or historical archive), plus anything awaiting author
  review.
- **[manifest.json](manifest.json)** — the machine-readable inventory, inspectable directly
  (its former documentation test was removed under issue #271, per the code-only testing policy).

## Retrieval

```sh
git show {TAG}                 # the pre-narrative baseline
python3 tools/build_rulebook_archive.py --check   # prove the hashes still match
```

## Relationship to #243

Issue #243 made a *lossless inventory and exact snapshot* of the root `RULEBOOK.md` and
`rulebook_parts/`, and deliberately did **not** reconcile them
(`docs/rulebook_consolidation/inventory.json`, `rulebook/source_snapshots/`). This archive **extends**
that work to the rest of the corpus and adds the migration map. It does not duplicate or undo #243.

## Scope

Preservation and mapping only. It changes no rule, deletes nothing, and approves no dice formula.
"""
    return {"MANIFEST.md": manifest, "manifest.json": json.dumps(man_json, indent=2, sort_keys=False) + "\n",
            "MIGRATION_MAP.md": migration, "README.md": readme}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    files = build()
    if args.check:
        bad = []
        for name, content in files.items():
            p = ARCHIVE / name
            if not p.exists() or p.read_text(encoding="utf-8") != content:
                bad.append(name)
        if bad:
            print("archive out of date: " + ", ".join(bad))
            return 1
        print(f"archive OK ({len(files)} files)")
        return 0
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (ARCHIVE / name).write_text(content, encoding="utf-8")
        print(f"wrote archive/rulebook-pre-narrative-2026-10/{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
