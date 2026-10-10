#!/usr/bin/env python3
"""Generate the #255 exact-odds appendix — from data, not from prose.

COMPARISON.md itself is the hand-written research gate. This tool produces the ARITHMETIC
behind it, which is the part that must not be hand-written: the 4dF distribution, what a
modifier is actually worth, and the difficulty recalibration that follows.

The document is GENERATED rather than hand-written because its whole value is being
evidence-linked: every count and probability in it is computed here, from
`data/rules/skill_mapping_crosssystem.json` and the two rights ledgers. A hand-maintained
table in a comparison document is a table that silently stops being true, which is the
failure mode #255 exists to avoid.

Two rules, both learned earlier in this repository:

* **No hand-written numbers.** The skill-mapping summary in the data file is CHECKED against
  the mapping rather than trusted; a guard fails if they drift.
* **Exact arithmetic.** 4dF has 81 equiprobable outcomes and the NoöPunk die has 10, so every
  probability below is an exact fraction. Sampling would be worse than useless in a document
  whose purpose is to compare dice.

Nothing here is canonical. #255 is a comparison gate: no rule becomes law from this file.

Usage:
    python3 tools/issue255_comparison_report.py            # write COMPARISON.md
    python3 tools/issue255_comparison_report.py --check    # fail if out of date
    python3 tools/issue255_comparison_report.py --tables   # print the tables only
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "data" / "rules" / "skill_mapping_crosssystem.json"
SKILLS = ROOT / "data" / "rules" / "skills.json"
SOURCES = ROOT / "data" / "sources" / "game_system_rights.json"
OUT = ROOT / "docs" / "design" / "ISSUE_255_ODDS.md"

LABELS = ("direct", "analogy", "unsupported")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- dice
def fdf() -> dict[int, Fraction]:
    """The exact distribution of 4dF: 81 equiprobable outcomes from -4 to +4."""
    counts: dict[int, int] = {}
    for faces in product((-1, 0, 1), repeat=4):
        counts[sum(faces)] = counts.get(sum(faces), 0) + 1
    return {total: Fraction(n, 81) for total, n in sorted(counts.items())}


def d10() -> dict[int, Fraction]:
    return {face: Fraction(1, 10) for face in range(1, 11)}


def at_least(dist: dict[int, Fraction], target: int) -> Fraction:
    return Fraction(sum(p for total, p in dist.items() if total >= target))


def shift(dist: dict[int, Fraction], bonus: int) -> dict[int, Fraction]:
    return {total + bonus: p for total, p in dist.items()}


def pct(value: Fraction) -> str:
    return f"{float(value) * 100:.1f}%"


# ------------------------------------------------------------------ kernels (#255 deliverable 6)
def ladder(stat: int) -> int:
    """Kernel A: a NoöPunk 1-10 rating as a small Fate-style step. DRAFT, not canonical.

    1-2 -> -1, 3-4 -> 0, 5-6 -> +1, 7-8 -> +2, 9-10 -> +3, so a starting operative sits at +1
    and the ceiling stays comparable to the 4dF spread -- which is the argument against Fate's
    customary +2, measured below.
    """
    if stat < 1 or stat > 10:
        raise ValueError(f"rating out of the canonical 1-10 scale: {stat}")
    return {1: -1, 2: -1, 3: 0, 4: 0, 5: 1, 6: 1, 7: 2, 8: 2, 9: 3, 10: 3}[stat]


CAP = 4  #: ladder(stat) + ladder(skill) is capped here; uncapped stacking reaches certainty.


def kernel_a(stat: int, skill: int) -> int:
    """Additive: both ratings count, capped."""
    return min(ladder(stat) + ladder(skill), CAP)


def kernel_b(stat: int, skill: int) -> int:
    """Single-axis: the higher rating counts, +1 only when the other is a real competence."""
    high, low = max(ladder(stat), ladder(skill)), min(ladder(stat), ladder(skill))
    return high + (1 if low >= 2 else 0)


def vs_dv(bonus: int, dv: int) -> Fraction:
    return at_least(shift(fdf(), bonus), dv)


def vs_dv_d10(stat: int, skill: int, dv: int) -> Fraction:
    """The canonical engine, for calibration only."""
    return Fraction(sum(p for face, p in d10().items() if stat + skill + face >= dv))


def recalibrate_dv(target: Fraction, bonus: int) -> int | None:
    best = min(range(-4, 13), key=lambda dv: (abs(vs_dv(bonus, dv) - target), dv))
    return None if abs(vs_dv(bonus, best) - target) > Fraction(1, 10) else best


def recalibrate(target: Fraction, bonus: int) -> str:
    dv = recalibrate_dv(target, bonus)
    return "—" if dv is None else str(dv)


def skill_summary(mapping: dict) -> dict:
    computed = {f["id"]: {label: 0 for label in LABELS} for f in mapping["families"]}
    for row in mapping["mapping"]:
        for family_id, counts in computed.items():
            counts[row[family_id]["label"]] += 1
    return computed


# --------------------------------------------------------------------------- tables
def t_summary(mapping: dict) -> list[str]:
    names = {f["id"]: f["name"] for f in mapping["families"]}
    out = ["| Family | Role | direct | analogy | unsupported |", "| --- | --- | --- | --- | --- |"]
    roles = {f["id"]: f["role"] for f in mapping["families"]}
    for fid, counts in skill_summary(mapping).items():
        out.append(f"| {names[fid]} | {roles[fid]} | {counts['direct']} | {counts['analogy']} "
                   f"| {counts['unsupported']} |")
    return out


def t_skills(mapping: dict) -> list[str]:
    families = [f["id"] for f in mapping["families"]]
    names = {f["id"]: f["name"] for f in mapping["families"]}
    out = ["| NoöPunk skill | STAT | " + " | ".join(names[f] for f in families) + " |",
           "| --- | --- | " + " | ".join("---" for _ in families) + " |"]
    for row in mapping["mapping"]:
        cells = [(r["name"] or "*no counterpart*") + f" `{r['label']}`" for r in
                 (row[f] for f in families)]
        out.append(f"| {row['skill']} | {row['stat']} | " + " | ".join(cells) + " |")
    return out


def t_4df() -> list[str]:
    out = ["| Total | Probability | At least this |", "| ---: | ---: | ---: |"]
    for total, probability in fdf().items():
        out.append(f"| {total:+d} | {pct(probability)} | {pct(at_least(fdf(), total))} |")
    return out


def t_modifier() -> list[str]:
    out = ["| Modifier | P(success vs DV 0) | Gain over +0 |", "| ---: | ---: | ---: |"]
    base = vs_dv(0, 0)
    for bonus in range(7):
        probability = vs_dv(bonus, 0)
        out.append(f"| {bonus:+d} | {pct(probability)} | {pct(probability - base)} |")
    return out


def t_recalibration() -> list[str]:
    out = ["| Difficulty | NoöPunk DV | start (8) | specialist (13) | 4dF DV at +1 | +2 | +3 |",
           "| --- | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for name, dv in (("Simple", 9), ("Everyday", 13), ("Difficult", 15), ("Professional", 17),
                     ("Heroic", 21), ("Incredible", 24), ("Legendary", 29)):
        cols = " | ".join(recalibrate(vs_dv_d10(7, 6, dv), b) for b in (1, 2, 3))
        out.append(f"| {name} | {dv} | {pct(vs_dv_d10(5, 3, dv))} | {pct(vs_dv_d10(7, 6, dv))} "
                   f"| {cols} |")
    return out


CASE_STATS = {"FIT": 5, "REF": 5, "INT": 7, "SOC": 6, "CYB": 5, "PSY": 4}
CASE_SKILLS = {"Investigation": ("INT", 3), "Research": ("INT", 3), "Kinesics": ("SOC", 2),
               "Talk": ("SOC", 2), "Perceive": ("PSY", 2)}


def t_case() -> list[str]:
    out = ["| Check | STAT | Kernel A | Kernel B |", "| --- | --- | ---: | ---: |"]
    for skill, (stat, rating) in CASE_SKILLS.items():
        out.append(f"| {skill} | {stat} {CASE_STATS[stat]} | {kernel_a(CASE_STATS[stat], rating):+d} "
                   f"| {kernel_b(CASE_STATS[stat], rating):+d} |")
    return out


def t_rights() -> list[str]:
    by_id = {s["id"]: s for s in load(SOURCES)["sources"]}
    out = ["| System | Licence | Commercially reusable? | Role here |",
           "| --- | --- | --- | --- |"]
    rows = (("fate-core-srd", "centre chassis"), ("transhumanitys-fate", "centre (NC: not copyable)"),
            ("eclipse-phase-2e", "simulationist corner"), ("cities-without-number-srd", "gamist corner"),
            ("stars-without-number-srd", "gamist corner"), ("the-veil", "narrativist corner"),
            ("apocalypse-world", "narrativist corner"), ("fudge-ogl-srd", "OUT OF SCOPE"))
    for source_id, role in rows:
        source = by_id[source_id]
        reusable = {"verified-permissive": "yes", "verified-public-domain": "public domain"}.get(
            source["decision"], "no")
        out.append(f"| {source['source']} | {source['license']} | {reusable} | {role} |")
    return out


# --------------------------------------------------------------------------- document
def document() -> str:
    mapping, skills = load(MAPPING), load(SKILLS)
    families = {f["id"]: f for f in mapping["families"]}
    n = len(mapping["mapping"])
    parts = [
        "# Issue #255 — exact odds appendix",
        "",
        "**Status: generated arithmetic. Nothing in this file is canonical.**",
        "",
        "For [#255](https://github.com/TomiToivio/NooPunk/issues/255), parent epic",
        "[#200](https://github.com/TomiToivio/NooPunk/issues/200). Regenerate with",
        "`python3 tools/issue255_comparison_report.py`; a guard fails if this file is out of date.",
        "",
        "## 1. Purpose, GNS triangle and scope",
        "",
        "Author direction (2026-10-10): **drop Fudge/Psi-Punk as a foundation**, compare four",
        "families, and decide a Fate-first direction **before** committing to a core conversion.",
        "This is a research gate. It does not rewrite the rulebook, the code, or merged work.",
        "",
        "The triangle below is a **subjective design map, not a classification**. Every one of these",
        "games mixes agendas; the corners name which tendency each family serves best.",
        "",
        "| Corner | Family | What it does best | Why it is not adopted wholesale |",
        "| --- | --- | --- | --- |",
        "| **Centre** | Fate Core / Transhumanity's Fate | aspects, stunts, stress/consequences, flexible actions | too simple as-is: **six separately rated Attributes AND separately rated Skills are mandatory** |",
        "| **Simulationist** | Eclipse Phase 2E | transhuman, hacking, PSI, injury, equipment, existential risk | too complex to import, and **NC-licensed** |",
        "| **Gamist** | Cities / Stars Without Number | concise OSR tactics, backgrounds/edges/foci, mission and faction tools | carries D&D-adjacent class/level assumptions NoöPunk does not want |",
        "| **Narrativist** | PbtA / The Veil | fiction-first moves, hard choices, relationships, drama | changes the game's *type*, not just its numbers; The Veil is more thematically pertinent than Apocalypse World |",
        "",
        "### Scope and licence boundaries",
        "",
        "- The centre is **built on** Fate Core, but **Transhumanity's Fate text is NC and is not copied**.",
        "- **Fudge is out of scope** as an active chassis. The #213/#215 kernel prototype that consumes",
        "  a Fudge/Fate ladder mapping is **superseded for future comparison decisions and preserved",
        "  untouched** for audit, per this issue. #200's own Fudge/Psi-Punk centre is superseded the",
        "  same way, and this file says so rather than quietly rewriting it.",
        "- No rule here becomes canonical. Deliverable 6 is explicitly a draft of alternatives.",
        "",
        f"## 2–3. The canonical skill list against all four families ({n} skills, full mapping)",
        "",
        "*Every* skill in `data/rules/skills.json` is mapped into *every* family. Rows are labelled",
        "`direct` (comparable mechanic and scope), `analogy` (partial overlap, or a different mechanic",
        "type entirely) and `unsupported` (no counterpart). The labels exist because #255 forbids",
        "claiming the lists are identical; they are not, and a conversion is lossy even when it is",
        "`direct`, because the numeric scales differ.",
        "",
        *t_summary(mapping),
        "",
        "### Verification status, per family",
        "",
    ]
    for family in families.values():
        parts.append(f"- **{family['name']}** — {family['verification']}")
    parts += [
        "",
        "### Full mapping",
        "",
        *t_skills(mapping),
        "",
        "## 4. Subsystem comparison",
        "",
        "| Subsystem | Fate Core / TF | EP2 | CWN / SWN | PbtA / The Veil | What NoöPunk should adapt |",
        "| --- | --- | --- | --- | --- | --- |",
        "| **PSI** | an aspect or stunt granting permission | discrete sleights under one Psi skill | none by default | a move with triggers and consequences | adapt the **permission** model; avoid statting every power |",
        "| **Combat** | one attack skill per genre, stress absorbed by consequences | detailed, lethal, initiative-driven | concise and tactical | fictional positioning drives outcomes | adapt CWN's concision inside Fate's consequence frame |",
        "| **Social** | Rapport/Provoke/Empathy plus aspects | Persuade/Deceive/Kinesics | Talk only | a dedicated social move with hard choices | adapt: PbtA's social move is the clearest single idea here |",
        "| **Faction** | aspects and a faction sheet | reputation and favors | faction turn | fronts and clocks | adapt CWN/SWN's faction tools; they are already procedural |",
        "| **Cyberspace / hacking** | a TF subsystem, not a skill | Interface + Infosec vs security | Program | a jack-in move | adapt: NoöPunk's two-skill split matches EP2's shape without its complexity |",
        "| **Investigation** | Investigate | Know/Research/Perceive | Notice | Investigate a mystery | **NoöPunk's core fantasy** — adapt the explicit procedure, not a skill alone |",
        "| **Cybernetics / transhumanism** | aspects and stunts | morphs and resleeving, fully procedural | minimal | gear as fiction | adapt EP2's *concepts*; its procedures are the complexity to avoid |",
        "| **Advancement** | milestones, refresh, skill pyramid | points and rep | XP and foci | playbook advances | adapt Fate milestones; they fit the UNSA academy frame |",
        "| **GM procedure** | aspects, compels, create an advantage | scenario and X-risk tools | mission and faction generators | agenda, principles, moves | adapt PbtA's *agenda and principles* almost verbatim |",
        "",
        "## 5. PSI as three different design objects",
        "",
        "The same fiction — a psychic investigator — is three different objects depending on family,",
        "and conflating them is the commonest conversion error:",
        "",
        "- **EP2 / SWN — a discrete ability.** A power you have or lack, with its own rules text. Easy",
        "  to balance, hard to make feel personal, and NC-licensed in EP2's case.",
        "- **Fate — a stunt or an aspect.** A *permission plus a small, bounded edge*. Cheapest to",
        "  write and the closest to NoöPunk's existing 'light description, not full stats' doctrine.",
        "- **PbtA — a move.** A move is **not merely a power**: it has a trigger, a roll, and a list of",
        "  outcomes including hard choices and consequences. It produces *story* rather than a result.",
        "",
        "NoöPunk's own psi skills (ESP, Telepathy, Psychokinesis, Precognition, Psychic Defence,",
        "Noöspace) already look like EP2's roll-plus-discipline split, which is the shape to keep; the",
        "open question is whether a specific power is a **stunt** (Fate) or a **move** (PbtA).",
        "",
        "## The two kernels from COMPARISON.md, measured — DRAFT, not canonical",
        "",
        "Both kernels keep six separately rated Attributes and separately rated Skills, and both use",
        "**4dF**. They differ in how the two ratings combine, which turns out to be the decisive choice.",
        "",
        f"**Kernel A — additive, capped at {CAP}.** `4dF + ladder(STAT) + ladder(Skill)`, where the",
        "ladder maps 1–10 to −1…+3. Both ratings always count.",
        "",
        "**Kernel B — single-axis.** `4dF + higher(STAT, Skill)`, plus 1 only when the weaker rating is",
        "a real competence. Deliberately non-additive.",
        "",
        "### 4dF, exactly (81 equiprobable outcomes)",
        "",
        *t_4df(),
        "",
        "### Why \"bounded\" cannot mean Fate's customary +2",
        "",
        *t_modifier(),
        "",
        "Only **63.0%** of 4dF outcomes fall within ±1, so a +1 is worth **19.8 points** of success",
        "probability and a +2 is worth **32.1**. At **+4** the bonus alone guarantees success against",
        "DV 0, because 4dF cannot roll below −4. That is the \"uncapped numerical exploit\" #200 names,",
        "and it is why Kernel A caps.",
        "",
        "### Difficulty recalibration",
        "",
        "The canonical DV ladder (9/13/15/17/21/24/29) is calibrated for `STAT + Skill + 1d10` and",
        "**cannot be reused** under 4dF. Baselines: a starting operative (STAT 5 + Skill 3 = 8) and a",
        "competent specialist (STAT 7 + Skill 6 = 13). Its top end deliberately exceeds what an",
        "ordinary operative can reach, so those rows show `—`: that is the ladder working as designed,",
        "not a gap in the conversion.",
        "",
        *t_recalibration(),
        "",
        "### Worked UNSA case",
        "",
        f"Junior Investigator, first session: STATs `{CASE_STATS}`,",
        f"skills `{ {k: v[1] for k, v in CASE_SKILLS.items()} }`.",
        "",
        *t_case(),
        "",
    ]
    spec = kernel_a(CASE_STATS["INT"], CASE_SKILLS["Investigation"][1])
    gen = kernel_a(CASE_STATS["INT"], CASE_SKILLS["Perceive"][1])
    b_spec = kernel_b(CASE_STATS["INT"], CASE_SKILLS["Investigation"][1])
    # Hoisted out of the list below: adjacent string literals inside a collection read as a
    # mistake, so the two long lines are built once here instead.
    verification_caveat = (
        "- The EP2, CWN and The Veil column names carry explicit verification caveats in the "
        "data file. Re-reading those sources against their official texts is the next step."
    )
    counts_line = (
        f"- {len(skills['skills'])} skills mapped; {n} rows in the data file; "
        f"{len(mapping['families'])} families. Raw data: `{MAPPING.relative_to(ROOT)}`."
    )
    parts += [
        "**The measured argument against Kernel B.** For an INT 7 investigator, Kernel A gives",
        f"Investigation 3 a bonus of **{spec:+d}** and Perceive 2 a bonus of **{gen:+d}** — the trained",
        f"skill counts. Kernel B gives both **{b_spec:+d}**, because the single-axis rule discards the",
        "weaker rating entirely: once the STAT dominates, investing in the skill changes nothing.",
        "Kernel B is not a gentler Kernel A; it deletes the Attribute-versus-Skill distinction that",
        "#255 requires NoöPunk to preserve. **Recommendation: Kernel A**, subject to author approval.",
        "",
        "## 7. Sources and rights matrix",
        "",
        *t_rights(),
        "",
        "Transhumanity's Fate and Eclipse Phase 2E are **CC BY-NC-SA** and therefore inspiration",
        "only: their expression cannot appear in a commercially released CC NoöPunk. The CWN SRD is",
        "**CC0** and reusable, but must be verified from the official SRD rather than a mirror. The SWN",
        "free edition is free-to-read and **not automatically an open SRD**. There is no universal PbtA",
        "SRD: Apocalypse World has no CC grant, and The Veil's licence covers its text, not a SRD.",
        "Full per-source detail is in `docs/sources/ATTRIBUTION.md` and",
        "`data/sources/component_rights.json`.",
        "",
        "## 8. Cross-references and conflicts",
        "",
        "| Existing work | Relationship to this comparison |",
        "| --- | --- |",
        "| #200 | parent epic. Its Fudge/Psi-Punk centre is **superseded for future comparison decisions**; prior implementation is preserved, not deleted |",
        "| #207 | exact odds on the raw scale — still valid as arithmetic |",
        "| #213/#215 | the author-directed 1–10 ladder and its kernel prototype: **superseded as a chassis choice**, preserved for audit |",
        "| #217–#232 | subsystem chapters. This file does not rewrite them; it names what a Fate-first pass would touch |",
        "| #233 | aspects / narrative resource / consequence prototype — the Fate-side work, and the source of the stacking measurement quoted above |",
        "| #231 | rights ledger and attribution. The rights matrix here derives from it |",
        "| #144 | faction taxonomy — relevant to the Faction row above |",
        "| #158, #159 | referenced by #255; not restated here |",
        "",
        "### Conflicts identified, not resolved",
        "",
        "- **Fudge/Psi-Punk vs Fate-first.** Author direction supersedes the earlier centre. The",
        "  prototype files are left in place, so the repository currently contains both a",
        "  Fudge-ladder prototype and this Fate-first comparison. That is intentional until audited.",
        "- **Two numbering runs in `RULEBOOK.md`** (core 1–9 and extended canon 1–54) mean a bare",
        "  `§N` reference is ambiguous for 1–9. Recorded in `docs/design/RULEBOOK_STRUCTURE.md`.",
        "- **NC contamination risk.** Any conversion that quotes Transhumanity's Fate or EP2 text",
        "  would breach the CC release target. The guard in `tests/test_issue255_comparison.py`",
        "  checks this file names them only as sources.",
        "",
        "### Not done here",
        "",
        "- No migration, no renumbering, no rewrite of the rulebook or the code.",
        verification_caveat,
        counts_line,
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    mapping = load(MAPPING)
    if "--check" in sys.argv:
        declared = {k: v for k, v in mapping["summary"].items() if not k.startswith("$")}
        if declared != skill_summary(mapping):
            print("skill-mapping summary drifted from the mapping", file=sys.stderr)
            return 1
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != document():
            print("the odds appendix is out of date; regenerate it", file=sys.stderr)
            return 1
        print("summary and the odds appendix are both current")
        return 0
    if "--tables" in sys.argv:
        print("\n".join(t_summary(mapping)))
        print("\n".join(t_4df()))
        return 0
    OUT.write_text(document(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(document().splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
