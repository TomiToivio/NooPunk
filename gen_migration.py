#!/usr/bin/env python3
"""Generate archive/rulebook-pre-narrative-2026-10/MIGRATION_MAP.md for #265.

Every top-level section of the ARCHIVED RULEBOOK.md is mapped to exactly one destination, so
nothing is silently discarded. The old numerical/tactical material is mapped to `historical` or
`advanced` -- never quietly reinstated as canon.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

ROOT = Path("/mnt/workspace/NooPunk")
ARCH = ROOT / "archive" / "rulebook-pre-narrative-2026-10"
SRC = ARCH / "RULEBOOK.md"
MARK = "# Extended canon and reference material"

#: Destination chapters of the new narrative-first rulebook, per #265's proposed list.
NEW = {
    1: "What is NoöPunk? Premise and narrative-first play",
    2: "The six attributes: FIT / REF / INT / SOC / PSY / CYB",
    3: "Character creation: Academy, background, skills, call-sign",
    4: "Playing scenes: dialogue, checks and consequences (formula awaiting decision)",
    5: "Social relationships, companions and NPC agency",
    6: "Psyche, beliefs, thoughts, dreams and personal change",
    7: "Investigation, evidence, decisions and clocks",
    8: "The three realities and access/embodiment constraints",
    9: "Simple conflict and consequences",
    10: "Running a UNSA case; first Helsinki/Ö-Mappi adventure",
    11: "Tabletop / Godot / Concordia parity and terminology",
    12: "Optional/deferred advanced-system roadmap and historical sources",
}
LORE = "lore/reference (kept, not rules)"
ADV = "advanced supplement (deferred)"
HIST = "historical archive only"

#: (regex on the section title, destination). Ordered; the first match wins.
RULES: list[tuple[str, str]] = [
    (r"(?i)^contents$", HIST),
    (r"(?i)introduction|what this document is|current project|project description|accessibility|premise",
     "new:1"),
    (r"(?i)^stats$|attributes|characters and identity|character generation|chargen|background|lifepath|call-?sign|academy|progress",
     "new:3"),
    (r"(?i)skill|specialist field", "new:3"),
    (r"(?i)action resolution|smallest playable rules kernel|pools and expendable|core architecture rule|rule-change|tie|partial|degree of success",
     "new:4"),
    (r"(?i)social|affect|faction|contact|reputation|motivation|npc|dialogue|relationship|companion",
     "new:5"),
    (r"(?i)psych|psyche|psi|noösphere interaction|noosphere interaction|noetic|dream|sleep|density|manifestation|crystal",
     "new:6"),
    (r"(?i)investigat|evidence|forensic|witness|hypothesis|unsa investigation", "new:7"),
    (r"(?i)mesh|hack|cyberspace|cybernetic|augmentation|software|gear|equipment|ai,|infomorph|interface|network|compute",
     "new:8"),
    (r"(?i)physical harm|wound|stress|combat|melee|fray|embodiment|morph|body|platform|conflict|ladder",
     "new:9"),
    (r"(?i)unsa: default campaign|running a|field catalog|scenario|campaign", "new:10"),
    (r"(?i)concordia|persistence|reproducib|adapter|godot|parity|deterministic", "new:11"),
    (r"(?i)provenance|licensing boundary|source hierarchy|reuse|attribution|rights", HIST),
    (r"(?i)change ledger|healthy rulebook|governing principle|immediate rulebook work|escape hatch",
     HIST),
    (r"(?i)lore|world|history|timeline|singularity|disclosure|confederation|orion|resleeving|xenopolitic|ontology|beings|nhi|cryptoterrestrial",
     LORE),
    (r"(?i)source|reading|influence|theoretical|glossary", LORE),
    (r"(?i)reverse-engineering|verification doctrine", ADV),
    (r"(?i)ep2|test-session|subset", HIST),
]


def sections() -> list[dict]:
    src = SRC.read_text(encoding="utf-8")
    mi = src.find(MARK)
    assert mi > 0, "the core/ledger marker is missing from the archived copy"
    out: list[dict] = []
    for tag, text in (("core", src[:mi]), ("ledger", src[mi:])):
        hs = list(re.finditer(r"(?m)^## (.+)$", text))
        for k, m in enumerate(hs):
            end = hs[k + 1].start() if k + 1 < len(hs) else len(text)
            out.append({
                "half": tag,
                "title": m.group(1).strip(),
                "size": end - m.start(),
            })
    return out


def destination(title: str) -> str:
    for pattern, dest in RULES:
        if re.search(pattern, title):
            return dest
    return "REVIEW"


def main() -> int:
    secs = sections()
    rows = [(s, destination(s["title"])) for s in secs]
    counts = Counter(d for _, d in rows)
    review = [s["title"] for s, d in rows if d == "REVIEW"]

    lines = [
        "# Migration and supersession map",
        "",
        f"Every top-level section of the **archived** `RULEBOOK.md` ({len(secs)} sections, "
        f"{sum(s['size'] for s in secs)} chars) mapped to exactly one destination. The archive "
        "copy is the mapping's source of truth, so this map stays valid after the cutover.",
        "",
        "**Destinations are not a claim that content moves unchanged.** A section mapped to a new "
        "chapter contributes its *subject*; the new chapter is newly written, narrative-first, and "
        "carries no old numerical rule as canon. Old tactical/numerical material is marked "
        "`advanced` or `historical` and is **never quietly reinstated**.",
        "",
        "| # | half | old section | destination |",
        "| ---: | --- | --- | --- |",
    ]
    for i, (s, d) in enumerate(rows, 1):
        title = s["title"].replace("|", "\\|")
        lines.append(f"| {i} | {s['half']} | {title} | {d} |")
    lines += ["", "## Counts by destination", ""]
    for dest, n in counts.most_common():
        lines.append(f"- **{dest}** — {n} section(s)")
    lines += [
        "",
        "## The twelve new chapters, for reference",
        "",
    ]
    for n, title in NEW.items():
        lines.append(f"{n}. {title}")
    lines += [
        "",
        "## Supersession, stated once",
        "",
        "The old numerical/tactical resolution (whatever engine it used) is **historical**. The "
        "new rulebook's resolution formula is **undecided** under #262 and is not inherited from "
        "any earlier proposal. Nothing in this map reinstates an old engine as canon.",
    ]
    (ARCH / "MIGRATION_MAP.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote MIGRATION_MAP.md: {len(secs)} sections")
    for dest, n in counts.most_common():
        print(f"   {n:>3}  {dest}")
    if review:
        print("\n!! UNMAPPED (need an explicit destination):")
        for t in review:
            print("   -", t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
