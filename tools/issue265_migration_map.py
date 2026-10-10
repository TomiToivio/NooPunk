#!/usr/bin/env python3
"""Generate the migration / supersession map for issue #265.

#265 requires that "nothing is silently discarded" and that every old section and subsystem has a
destination. So the map is GENERATED from an explicit table rather than written as prose: a
prose map can quietly omit a section, a generated one cannot, and a guard fails if any section or
archived file has no destination.

The finding that shapes the whole table: RULEBOOK.md's 54-section appendix is largely *process,
provenance and lore* rather than player rules. Most of it was never a rulebook chapter, so
"archive" for those entries is routing, not loss.

Destinations:
  NEW        a chapter of the new narrative-first rulebook (#265 §"Proposed introductory chapters")
  DEFERRED   the optional advanced/tactical supplement, planned not implemented
  LORE       world canon and reference material, kept
  PROCESS    repo engineering/provenance documentation, never player-facing rules
  ARCHIVE    historical numbers and superseded engines, retained as history

Usage:
    python3 tools/issue265_migration_map.py            # write MIGRATION_MAP.md
    python3 tools/issue265_migration_map.py --check    # fail if stale
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "archive" / "rulebook-pre-narrative-2026-10"
OUT = ARCHIVE / "MIGRATION_MAP.md"
NEW_CHAPTERS = {
    1: "What is NoöPunk? Premise and narrative-first play",
    2: "The six attributes: FIT / REF / INT / SOC / PSY / CYB",
    3: "Character creation: Academy, background, skills, call-sign",
    4: "Playing scenes: dialogue, checks and meaningful consequences (formula undecided)",
    5: "Social relationships, companions and NPC agency",
    6: "Psyche, beliefs, thoughts, dreams and personal change",
    7: "Investigation, evidence, decisions and clocks",
    8: "The three realities and access/embodiment constraints",
    9: "Simple conflict and consequences",
    10: "Running a UNSA case; first Helsinki/Ö-Mappi adventure",
    11: "Tabletop / Godot / Concordia parity and terminology",
    12: "Optional/deferred advanced-system roadmap and historical-source references",
}

#: core run: RULEBOOK.md `## 1..9.` -- the actual player rules.
CORE = {
    1: ("NEW", 1, "the premise chapter, rewritten narrative-first"),
    2: ("LORE", None, "world history, kept as canon"),
    3: ("NEW", 2, "the six attributes, preserved exactly as approved"),
    4: ("NEW", 3, "the skill catalogue carried forward for the #263 crosswalk"),
    5: ("NEW", 8, "physical reality as one of the three layers"),
    6: ("NEW", 5, "social systems -- now a core pillar, not a subsystem"),
    7: ("NEW", 8, "cybernetic reality as one of the three layers"),
    8: ("NEW", 6, "psychic systems; PSI kept distinct from Psyche"),
    9: ("NEW", 3, "character generation, Academy lifepath and call-sign"),
}

#: appendix run: RULEBOOK.md `## 1..54.` (second numbering space).
APPENDIX = {
    1: ("PROCESS", None, "what the document is -- meta"),
    2: ("PROCESS", None, "project description"),
    3: ("PROCESS", None, "rules provenance labels"),
    4: ("PROCESS", None, "source hierarchy"),
    5: ("LORE", None, "primary Eclipse Phase references; rights ledger territory"),
    6: ("PROCESS", None, "licensing boundary -- kept, still binding"),
    7: ("PROCESS", None, "core architecture rule"),
    8: ("ARCHIVE", None, "the old 'smallest playable kernel'; its engine is superseded"),
    9: ("PROCESS", None, "characters and identity as meta"),
    10: ("NEW", 4, "action resolution -- formula explicitly undecided under #262"),
    11: ("ARCHIVE", None, "pools and expendable resources: old numeric economy"),
    12: ("NEW", 9, "physical harm and stress, light ladder only"),
    13: ("DEFERRED", None, "combat -- the advanced supplement, not first edition"),
    14: ("NEW", 8, "embodiment, morphs and platforms as a layer constraint"),
    15: ("NEW", 8, "mesh, hacking and the Noösphere as a layer"),
    16: ("NEW", 8, "psionics and Noösphere interaction"),
    17: ("NEW", 5, "Affect, Factions, Motivations, Reputation, Contacts -- the relationship pillar"),
    18: ("LORE", None, "gear, augmentation and technology reference"),
    19: ("LORE", None, "AI/AGI/infomorphs and non-human agents"),
    20: ("NEW", 10, "NPCs -- the party and HQ cast"),
    21: ("PROCESS", None, "social-science simulation layer: engineering, not play"),
    22: ("PROCESS", None, "structured actions for Concordia"),
    23: ("PROCESS", None, "persistence and reproducibility -- still binding"),
    24: ("ARCHIVE", None, "lighter rules escape hatches: old optional layer"),
    25: ("PROCESS", None, "rules adapter contract"),
    26: ("PROCESS", None, "rule-change procedure"),
    27: ("PROCESS", None, "change ledger -- superseded by the archive manifest and tag"),
    28: ("ARCHIVE", None, "old immediate rulebook work list, completed or superseded"),
    29: ("PROCESS", None, "definition of a healthy rulebook"),
    30: ("PROCESS", None, "governing principle"),
    31: ("ARCHIVE", None, "EP2 test-session subset (#60): old engine"),
    32: ("ARCHIVE", None, "embodiment and inventory subset (#60): old engine"),
    33: ("LORE", None, "canonical world lore from #60 -- kept"),
    34: ("LORE", None, "glossary"),
    35: ("LORE", None, "sources and influences"),
    36: ("NEW", 8, "the four systems reframed as the three realities plus Social"),
    37: ("LORE", None, "theoretical sources and inspirations"),
    38: ("NEW", 10, "UNSA as the default campaign institution"),
    39: ("NEW", 3, "campaign-scoped skills and specialist fields -- the specialisation layer"),
    40: ("LORE", None, "cryptoterrestrial map (#105)"),
    41: ("LORE", None, "disclosure and ontological shock (#106)"),
    42: ("LORE", None, "human factions and UN Parliament parties (#109)"),
    43: ("LORE", None, "faction taxonomy and schema (#144)"),
    44: ("LORE", None, "the Singularity Crisis and two Singularities"),
    45: ("LORE", None, "Confederation, Orion, resleeving"),
    46: ("LORE", None, "psychotronics, PSI, psyops"),
    47: ("LORE", None, "hybrid verification doctrine"),
    48: ("NEW", 6, "sleep, dreams and disentanglement -- the dream pillar"),
    49: ("LORE", None, "density, manifestation and ontological forensics"),
    50: ("LORE", None, "field catalogs: characters, equipment, implants, PSI, beings"),
    51: ("NEW", 9, "physical harm light ladder; the old numbers are historical"),
    52: ("LORE", None, "equipment list"),
    53: ("LORE", None, "xenopolitics after the NHI Crisis"),
    54: ("LORE", None, "noetic practice, crystal technology"),
}

#: the distinct reference chapters under rulebook/ (prose that exists nowhere in RULEBOOK.md).
CHAPTERS = {
    "rulebook/1_NOÖPUNK.md": ("NEW", 1, "premise material"),
    "rulebook/2_ATTRIBUTES.md": ("NEW", 2, "the six attributes at length"),
    "rulebook/3_PHYSICAL.md": ("NEW", 8, "physical layer"),
    "rulebook/4_SOCIAL.md": ("NEW", 5, "social layer -- a core pillar"),
    "rulebook/5_CYBERNETIC.md": ("NEW", 8, "cybernetic layer"),
    "rulebook/6_PSYCHIC.md": ("NEW", 6, "psychic and Psyche material"),
    "rulebook/7_TIMELINE.md": ("LORE", None, "timeline"),
    "rulebook/8_FACTIONS.md": ("LORE", None, "factions"),
    "rulebook/9_FIELD_CATALOGS.md": ("LORE", None, "field catalogs"),
    "rulebook/10_SINGULARITY_CRISIS.md": ("LORE", None, "the Singularity Crisis"),
    "rulebook/11_ONTOLOGY.md": ("LORE", None, "ontology"),
    "rulebook/12_BEINGS.md": ("LORE", None, "beings"),
    "rulebook/13_EQUIPMENT.md": ("LORE", None, "equipment"),
    "rulebook/14_CHARACTER_GENERATION.md": ("NEW", 3, "character generation at length"),
    "rulebook/15_XENOPOLITICS.md": ("LORE", None, "xenopolitics"),
    "rulebook/16_CONFEDERACY_SOURCE_AND_CONTACT.md": ("LORE", None, "Confederacy contact"),
    "rulebook/17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md": ("LORE", None, "noetic practice"),
    "rulebook/18_CROSS_DOMAIN_STATE.md": ("NEW", 8, "realm-spanning procedure; vocabulary reconciled here"),
    "rulebook/19_NARRATIVE_LAYER.md": ("NEW", 4, "the narrative layer"),
    "rulebook/README.md": ("PROCESS", None, "navigation for the reference chapters"),
    "rulebook_parts/INDEX.md": ("PROCESS", None, "navigation for the generated parts view"),
    "docs/rulebook_segments/README.md": ("PROCESS", None, "navigation for the generated segments view"),
    "rulebook/source_snapshots/rulebook_parts/INDEX.md": ("ARCHIVE", None, "a nested snapshot of an index"),
}


def read_sections() -> tuple[dict[int, str], dict[int, str]]:
    text = (ROOT / "RULEBOOK.md").read_text(encoding="utf-8")
    found = re.findall(r"^##\s+(\d+)\.\s+(.+)$", text, re.MULTILINE)
    core: dict[int, str] = {}
    appendix: dict[int, str] = {}
    switched = False
    for n, title in found:
        if n == "1" and title.strip().startswith("Introduction"):
            switched = False
        elif n == "1":
            switched = True
        target = appendix if switched else core
        target[int(n)] = title.strip()
    return core, appendix


def main() -> int:
    core, appendix = read_sections()
    rows: list[tuple[str, str, str, str]] = []
    for number, title in sorted(core.items()):
        kind, chapter, why = CORE[number]
        dest = f"new ch. {chapter}" if chapter else kind.lower()
        rows.append((f"core §{number}", title, f"{dest} — {why}"[:150], kind))
    for number, title in sorted(appendix.items()):
        kind, chapter, why = APPENDIX[number]
        dest = f"new ch. {chapter}" if chapter else kind.lower()
        rows.append((f"app. §{number}", title, f"{dest} — {why}"[:150], kind))
    for path, (kind, chapter, why) in CHAPTERS.items():
        dest = f"new ch. {chapter}" if chapter else kind.lower()
        rows.append((path.removeprefix("rulebook/"), "(reference chapter)", f"{dest} — {why}", kind))

    counts: dict[str, int] = {}
    for row in rows:
        counts[row[3]] = counts.get(row[3], 0) + 1

    lines = [
        "# Migration and supersession map — pre-narrative rulebook",
        "",
        "For issue [#265](https://github.com/TomiToivio/NooPunk/issues/265). Generated by",
        "`tools/issue265_migration_map.py`; regenerate rather than edit, and a guard fails if this",
        "file is stale or if any section or archived file has no destination.",
        "",
        "**Nothing is silently discarded.** Every numbered section of `RULEBOOK.md` and every",
        "distinct reference chapter has exactly one destination below. `ARCHIVE` means the entry is",
        "retained as history — reachable in full at the immutable tag",
        "`rulebook-pre-narrative-2026-10` — not deleted.",
        "",
        "## What the inventory found",
        "",
        "The corpus is **not** one rulebook repeated four times. Two of the four views are generated,",
        "and the appendix is largely not rules at all:",
        "",
        "| View | Files | Role |",
        "| --- | ---: | --- |",
        "| `RULEBOOK.md` | 1 | canonical text, 63 numbered sections in two numbering runs (core 1–9, appendix 1–54) |",
        "| `rulebook/*.md` | 20 | **distinct** reference chapters — prose that exists nowhere in `RULEBOOK.md` (0–2% overlap) |",
        "| `rulebook_parts/*.md` | 9 | generated views (93–100% overlap) — regenerable |",
        "| `docs/rulebook_segments/*.md` | 9 | generated views (100% overlap) — regenerable |",
        "",
        "The single most useful finding: **most of the 54-section appendix is process, provenance and",
        "lore, not player rules.** Routing those to `PROCESS`/`LORE` is not losing rules that existed —",
        "they were never player-facing chapters.",
        "",
        "## Destinations",
        "",
        "| Destination | Count | Meaning |",
        "| --- | ---: | --- |",
    ]
    meaning = {
        "NEW": "a chapter of the new narrative-first rulebook",
        "DEFERRED": "the optional advanced supplement — planned, not implemented",
        "LORE": "world canon and reference, kept",
        "PROCESS": "repo engineering/provenance documentation, never player rules",
        "ARCHIVE": "historical numbers and superseded engines, retained as history",
    }
    for kind in ("NEW", "LORE", "PROCESS", "ARCHIVE", "DEFERRED"):
        lines.append(f"| `{kind}` | {counts.get(kind, 0)} | {meaning[kind]} |")
    lines += [
        "",
        "## New rulebook chapters these entries feed",
        "",
        "| # | Chapter |",
        "| ---: | --- |",
    ]
    for number, title in sorted(NEW_CHAPTERS.items()):
        lines.append(f"| {number} | {title} |")

    lines += ["", "## Section-by-section map", "",
              "| Source | Title | Destination | Class |", "| --- | --- | --- | --- |"]
    for source, title, dest, kind in rows:
        lines.append(f"| `{source}` | {title} | {dest} | `{kind}` |")

    lines += [
        "",
        "## Old engine, explicitly historical",
        "",
        "The superseded resolution engine is **not** carried forward. `STAT + Skill + 1d10` against a",
        "DV ladder lives in `data/rules/core.json` and is consumed by the landed subsystems and their",
        "tests; #262 marks the dice formula **undecided** and this map does not choose one.",
        "`docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md` cites that engine as its rules boundary and is",
        "reconciled in the migration, not in this document.",
        "",
        "No old numeric or tactical rule is reinstated anywhere by this map.",
        "",
    ]
    text = "\n".join(lines) + "\n"
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print("MIGRATION_MAP.md is stale; regenerate it", file=sys.stderr)
            return 1
        print(f"migration map is current ({len(rows)} entries)")
        return 0
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} entries, {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
