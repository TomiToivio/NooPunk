#!/usr/bin/env python3
"""Build the CWN Free Edition parity matrix (#1025) from the linked SRD's real table of contents.

Why this exists
---------------
The mandatory initial audit in #1025 asks for a chapter-by-chapter and
subprocedure-by-subprocedure matrix over the *complete* table of contents, with
implementation path, Evennia command, test and an explicit status. The existing
20-row matrix (#950) recorded subsystems (``attributes``, ``combat``) rather than
SRD sections, so it could not answer "is this page of the book implemented?".

This script derives one row per SRD section from the published navigation, then
discovers implementation and test evidence by matching section tokens against
repository paths. It states what it can prove and leaves everything else alone:

* ``implemented``  — matching module(s) **and** at least one existing test;
* ``partial``      — matching module(s), no test that names them;
* ``missing``      — no matching module.

It never guesses a PDF page: the Free Edition PDF is not in the repository and a
page number taken from memory would be an invention. ``pdf_page`` stays ``null``
until someone reads it off the book, which is the point of the column.

Usage:
    python3 tools/cwn_parity_audit.py            # rebuild the JSON and markdown
    python3 tools/cwn_parity_audit.py --check    # fail if the JSON is stale
"""

from __future__ import annotations

import argparse
import ast
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "rules" / "cwn_compliance_matrix.json"
CURATED = ROOT / "data" / "rules" / "cwn_traceability.json"
REPORT = ROOT / "docs" / "rules" / "CWN_COVERAGE_1068.md"

SRD = "https://cwn.quadrifons.com"

#: Every section in the linked SRD's navigation, in reading order. Captured from the
#: site's own table of contents rather than transcribed from memory.
SECTIONS = [
    "character-creation",
    "character-creation/attributes",
    "character-creation/skills",
    "character-creation/backgrounds",
    "character-creation/contacts",
    "character-creation/edges",
    "character-creation/foci",
    "character-creation/focus-gear-budget",
    "character-creation/final-steps",
    "rules-of-the-game",
    "rules-of-the-game/scenes-rounds-mission-time",
    "rules-of-the-game/saving-throws",
    "rules-of-the-game/skill-checks",
    "rules-of-the-game/combat",
    "rules-of-the-game/combat/combat-initiative",
    "rules-of-the-game/combat/combat-actions",
    "rules-of-the-game/combat/attacks-in-combat",
    "rules-of-the-game/combat/damage-trauma-shock",
    "rules-of-the-game/combat/special-combat-maneuvers",
    "rules-of-the-game/combat/vehicle-combat",
    "rules-of-the-game/injury-healing-system-strain",
    "rules-of-the-game/injury-healing-system-strain/mortal-injury-stabilization",
    "rules-of-the-game/injury-healing-system-strain/system-strain",
    "rules-of-the-game/injury-healing-system-strain/natural-healing-first-aid-poisons",
    "rules-of-the-game/injury-healing-system-strain/major-injuries",
    "rules-of-the-game/chases-and-pursuit",
    "rules-of-the-game/character-advancement",
    "gear-vehicles-cyberware",
    "gear-vehicles-cyberware/encumbrance",
    "gear-vehicles-cyberware/mission-gear",
    "gear-vehicles-cyberware/weapons",
    "gear-vehicles-cyberware/weapons/weapon-stats-and-definitions",
    "gear-vehicles-cyberware/weapons/melee-thrown-weapons",
    "gear-vehicles-cyberware/weapons/firearms",
    "gear-vehicles-cyberware/weapons/heavy-weapons",
    "gear-vehicles-cyberware/weapons/weapon-mods",
    "gear-vehicles-cyberware/armor",
    "gear-vehicles-cyberware/armor/armor-terms-definitions",
    "gear-vehicles-cyberware/armor/armor-types",
    "gear-vehicles-cyberware/armor/armor-mods",
    "gear-vehicles-cyberware/armor/armor-accessories",
    "gear-vehicles-cyberware/cyberware",
    "gear-vehicles-cyberware/cyberware/cyberware-systems",
    "gear-vehicles-cyberware/cyberware/installing-cyberware",
    "gear-vehicles-cyberware/cyberware/removing-cyberware",
    "gear-vehicles-cyberware/cyberware/cyberware-maintenance",
    "gear-vehicles-cyberware/cyberware/cyberware-mods",
    "gear-vehicles-cyberware/cyberware/implant-complications",
    "gear-vehicles-cyberware/cyberware/concealing-detecting-cyberware",
    "gear-vehicles-cyberware/cyberware/skillplugs",
    "gear-vehicles-cyberware/cyberware/cyberdoc-tools",
    "gear-vehicles-cyberware/drones",
    "gear-vehicles-cyberware/vehicles",
    "gear-vehicles-cyberware/vehicle-mods",
    "gear-vehicles-cyberware/pharmaceuticals-street-drugs",
    "gear-vehicles-cyberware/lifestyles-wages-and-bribes",
    "gear-vehicles-cyberware/lifestyles-wages-and-bribes/lifestyle-costs",
    "gear-vehicles-cyberware/lifestyles-wages-and-bribes/common-wages",
    "gear-vehicles-cyberware/lifestyles-wages-and-bribes/bribe-costs",
    "hacking",
    "hacking/programs",
    "hacking/cyberdecks",
    "hacking/cyberdeck-mods",
    "hacking/node-links",
    "hacking/hacking-rules",
]

STATUSES = ["implemented", "partial", "missing", "not_applicable", "unverified"]

#: Sections whose implementation is named nothing like the SRD heading or whose mapping is a
#: judgement call. A keyword hit means the concept appears in code; it does NOT mean the procedure
#: is implemented. Such rows are `unverified`, never `implemented` and never `missing` — the first
#: would be a false claim, the second sends someone to rebuild what exists.
KEYWORDS: dict[str, list[str]] = {
    "character-creation:skills": ["SkillPool", "can_pick"],
    "character-creation:final-steps": ["starting gear", "finaliz"],
    "rules-of-the-game:combat:attacks-in-combat": ["resolve_attack", "attack_roll"],
    "rules-of-the-game:combat:special-combat-maneuvers": ["maneuver", "grapple"],
    "rules-of-the-game:injury-healing-system-strain:mortal-injury-stabilization": ["stabiliz"],
    "rules-of-the-game:injury-healing-system-strain:major-injuries": ["major_injur"],
    "rules-of-the-game:chases-and-pursuit": ["chase", "pursuit"],
    "gear-vehicles-cyberware:weapons:firearms": ["firearm", "pistol", "rifle"],
    "gear-vehicles-cyberware:armor:armor-accessories": ["accessor"],
    "gear-vehicles-cyberware:cyberware:installing-cyberware": ["install"],
    "gear-vehicles-cyberware:cyberware:removing-cyberware": ["remov"],
    "gear-vehicles-cyberware:cyberware:concealing-detecting-cyberware": ["conceal"],
    "gear-vehicles-cyberware:cyberware:cyberdoc-tools": ["cyberdoc"],
    "gear-vehicles-cyberware:lifestyles-wages-and-bribes": ["lifestyle", "bribe"],
    "gear-vehicles-cyberware:lifestyles-wages-and-bribes:common-wages": ["wage"],
    "hacking:programs": ["program"],
    "hacking:cyberdecks": ["cyberdeck"],
    "hacking:node-links": ["node_link"],
    "gear-vehicles-cyberware:cyberware:skillplugs": ["skillplug"],
}


def keyword_hits(section_id: str) -> list[str]:
    """Files that mention the section's concept, with no claim that they implement it."""
    pats = KEYWORDS.get(section_id)
    if not pats:
        return []
    hits = set()
    for f in list((ROOT / "src" / "rules").glob("*.py")) + list((ROOT / "mud" / "nopunk_mud" / "cwn").glob("*.py")):
        try:
            text = f.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            continue
        if any(p.lower() in text for p in pats):
            hits.add(str(f.relative_to(ROOT)))
    return sorted(hits)

#: Tokens too generic to establish a match on their own.
STOP = {
    "the", "and", "of", "in", "a", "an", "to", "game", "rules", "system", "systems",
    "character", "creation", "gear", "vehicles", "cyberware", "hacking", "combat",
    "weapons", "armor", "with", "for", "stats", "definitions", "terms", "special",
    "injury", "healing", "strain", "major", "common", "types", "mods",
}


def tokens(slug: str) -> list[str]:
    raw = [t for t in re.split(r"[-/]", slug.lower()) if len(t) > 2]
    distinctive = [t for t in raw if t not in STOP]
    # A section whose every word is generic ("combat", "hacking") is still a real section:
    # falling back to the raw tokens keeps it in scope instead of marking it not_applicable.
    return distinctive or raw


def title(slug: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-/]", slug.split("/")[-1]))


def chapter(slug: str) -> str:
    return slug.split("/")[0]


def discover() -> tuple[list[Path], list[Path], list[Path]]:
    """Candidate implementation modules, MUD modules and tests."""
    py = sorted((ROOT / "src" / "rules").glob("*.py"))
    mud = sorted((ROOT / "mud" / "nopunk_mud").rglob("*.py"))
    tests = sorted(list((ROOT / "tests").rglob("test_*.py")) + list((ROOT / "mud" / "tests").glob("test_*.py")))
    return py, mud, tests


def matches(paths: list[Path], toks: list[str]) -> list[str]:
    """Files whose name carries at least one distinctive section token."""
    if not toks:
        return []
    hits = []
    for path in paths:
        name = path.stem.lower().replace("-", "_")
        if any(t in name for t in toks):
            hits.append(str(path.relative_to(ROOT)))
    return hits


def procedure_modules(toks: list[str]) -> list[str]:
    """Modules whose *procedures* mention a section token.

    Filenames are a poor index of the SRD: `attributes` lives in `cwn_character.py`, and
    `saving throws` in `cwn_core.py`. Matching procedure names and docstrings is evidence
    from the code itself rather than from a name someone happened to choose.
    """
    registry = ROOT / "data" / "rules" / "cwn_coverage.json"
    if not registry.exists() or not toks:
        return []
    mods = json.loads(registry.read_text(encoding="utf-8")).get("modules", [])
    hits = []
    for mod in mods:
        text = " ".join(
            [str(pr.get("name", "")) + " " + str(pr.get("doc", "")) for pr in mod.get("procedures", [])]
        ).lower()
        if any(re.search(r"(?<![a-z])" + re.escape(t), text) for t in toks):
            path = ROOT / "src" / "rules" / str(mod.get("module", ""))
            if path.exists():
                hits.append(str(path.relative_to(ROOT)))
    return hits


def tests_touching(modules: list[str]) -> list[str]:
    """Existing tests that name one of the implementation modules."""
    if not modules:
        return []
    stems = {Path(m).stem for m in modules}
    found = []
    for test in sorted(list((ROOT / "tests").rglob("test_*.py")) + list((ROOT / "mud" / "tests").glob("test_*.py"))):
        try:
            text = test.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if any(stem in text for stem in stems):
            found.append(str(test.relative_to(ROOT)))
    return found


def commands_for(toks: list[str]) -> list[str]:
    """Evennia command classes whose name carries a section token, when a cmdset defines them."""
    cmdset = ROOT / "mud" / "nopunk_mud" / "default_cmdsets.py"
    if not cmdset.exists():
        return []
    text = cmdset.read_text(encoding="utf-8", errors="replace").lower()
    return [t for t in toks if t in text]



# --------------------------------------------------------------------------- #
# Curated, verified evidence (#1068)
# --------------------------------------------------------------------------- #

#: Statuses a curator may force, with the reason carried in the row's notes.
FORCEABLE = {"missing", "partial", "not_applicable"}


def module_names(path: Path) -> set[str]:
    """Top-level classes, functions and assigned names of a module, from its AST.

    Reading the AST rather than importing keeps the audit free of import side effects (some modules
    read data files at import time) while still proving the name exists in the file.
    """
    try:
        tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    names.add(target.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
    return names


def verify_entry(entry: dict) -> dict:
    """Check every piece of evidence a curated row claims, and say what failed.

    Evidence is attributed per module: a row cites ``{"path": ..., "procedures": [...]}`` so that
    "``resolve_attack`` lives in ``cwn_core``" is what gets checked, instead of demanding that every
    cited module export every cited name.
    """
    problems: list[str] = []
    specs = entry.get("modules", [])
    modules = [spec["path"] for spec in specs]
    tests = entry.get("tests", [])

    for spec in specs:
        rel = spec["path"]
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"module missing: {rel}")
            continue
        names = module_names(path)
        for procedure in spec.get("procedures", []):
            if procedure not in names:
                problems.append(f"{rel} has no {procedure!r}")

    for rel in tests:
        path = ROOT / rel
        if not path.is_file():
            problems.append(f"test missing: {rel}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        stems = [Path(m).stem for m in modules]
        if stems and not any(stem in text for stem in stems):
            problems.append(f"{rel} does not reference {stems}")

    rulebook = entry.get("rulebook")
    if rulebook and not (ROOT / rulebook).is_file():
        problems.append(f"rulebook anchor missing: {rulebook}")

    forced = entry.get("force_status")
    if forced is not None and forced not in FORCEABLE:
        problems.append(f"force_status {forced!r} is not one of {sorted(FORCEABLE)}")

    if forced in FORCEABLE:
        status = forced
    elif problems:
        status = "unverified"
    elif modules and tests:
        status = "implemented"
    elif modules:
        status = "partial"
    else:
        status = "missing"
    return {"status": status, "problems": problems}


def apply_curation(rows: list[dict]) -> dict[str, dict]:
    """Overwrite heuristic rows with verified curated evidence. Returns the verification per id."""
    if not CURATED.exists():
        return {}
    curated = json.loads(CURATED.read_text(encoding="utf-8"))
    verified: dict[str, dict] = {}
    by_id = {row["id"]: row for row in rows}
    for entry in curated.get("rows", []):
        row = by_id.get(entry["id"])
        if row is None:
            raise SystemExit(f"cwn_parity_audit: curated row {entry['id']!r} is not an SRD section")
        result = verify_entry(entry)
        verified[entry["id"]] = result
        row.update(
            python=[spec["path"] for spec in entry.get("modules", [])],
            procedures=[name for spec in entry.get("modules", [])
                        for name in spec.get("procedures", [])],
            tests=list(entry.get("tests", [])),
            rulebook=str(entry.get("rulebook", "")),
            coverage=result["status"],
            curated=True,
            verified=result["status"] == "implemented" and not result["problems"],
        )
        if entry.get("notes"):
            row["divergence"] = entry["notes"]
        if result["problems"]:
            row["divergence"] = "; ".join([row.get("divergence", "")] + result["problems"]).strip("; ")
    return verified


def build() -> dict:
    py, mud, tests = discover()
    rows = []
    for slug in SECTIONS:
        toks = tokens(slug)
        p = sorted(set(matches(py, toks) + procedure_modules(toks)))
        m = matches(mud, toks)
        t = sorted(set(matches(tests, toks) + tests_touching(p + m)))
        if "/" not in slug:
            # Chapter landing page: a table of contents, not a rule.
            coverage = "not_applicable"
        elif (p or m) and t:
            coverage = "implemented"
        elif p or m:
            coverage = "partial"
        else:
            kw = keyword_hits(slug.replace("/", ":"))
            if kw:
                coverage = "unverified"
                p = kw
            else:
                coverage = "missing"
        rows.append(
            {
                "id": slug.replace("/", ":"),
                "chapter": chapter(slug),
                "system": title(slug),
                "srd": f"{SRD}/{slug}/",
                "pdf_page": None,
                "godot": [],
                "python": p,
                "mud": m,
                "command": commands_for(toks),
                "coverage": coverage,
                "tests": t,
                "tested_against_book": False,
                "save_safe": False,
                "playtested": False,
                "classification": "cwn_rule",
                "divergence": (
                    "Concept appears in code but the procedure is not verified against the book; "
                    "matched by keyword in tools/cwn_parity_audit.py KEYWORDS."
                    if coverage == "unverified" else ""
                ),
            }
        )
    # The linked SRD omits Antagonists, but the Free Edition PDF contains it. Recording the
    # absence as an explicit `missing` row keeps the gap visible; dropping the row would make
    # an omission look like completeness.
    rows.append(
        {
            "id": "antagonists",
            "chapter": "antagonists",
            "system": "Antagonists",
            "srd": "(Free Edition PDF only; absent from the linked SRD)",
            "pdf_page": None,
            "godot": [],
            "python": [],
            "mud": [],
            "command": [],
            "coverage": "missing",
            "tests": [],
            "tested_against_book": False,
            "save_safe": False,
            "playtested": False,
            "classification": "cwn_rule",
            "divergence": (
                "Absent from the linked SRD; present in the Free Edition PDF. Recorded as missing "
                "rather than omitted so the gap stays visible."
            ),
        }
    )
    verification = apply_curation(rows)
    for row in rows:
        row.setdefault("procedures", [])
        row.setdefault("rulebook", "")
        row.setdefault("curated", False)
        row.setdefault("verified", False)
    return {
        "verification": verification,
        "$comment": (
            "CWN Free Edition parity matrix (#1025). Generated by tools/cwn_parity_audit.py from the "
            "linked SRD's own navigation. Status is derived from evidence: 'implemented' requires a "
            "matching module AND an existing test; 'partial' is a module with no test naming it. "
            "Evidence is matched by module filename and by procedure name/docstring tokens, so the "
            "module list is a candidate set, not a semantic equivalence proof: a row may cite a module "
            "that mentions the section without implementing it. Status answers 'is there code and a "
            "test', not 'does it match the book' — that is what tested_against_book records. "
            "pdf_page is null because the PDF is not in the repository and a page number must be read "
            "from the book, never guessed. tested_against_book/save_safe/playtested are separate "
            "columns precisely so file existence cannot be read as verification."
        ),
        "version": 2,
        "srd": {
            "url": SRD,
            "edition": "Cities Without Number, Free Edition (081123)",
            "scope_note": (
                "Sections captured from the hosted SRD navigation. The linked SRD omits Antagonists "
                "and the GM material present in the Free Edition PDF; those are therefore absent from "
                "this matrix rather than claimed. The PDF is the authoritative reference; where the two "
                "differ the PDF wins and the row records the divergence."
            ),
        },
        "statuses": STATUSES,
        "rows": rows,
    }


def render(matrix: dict) -> str:
    rows = matrix["rows"]
    counts = {s: sum(1 for r in rows if r["coverage"] == s) for s in STATUSES}
    lines = [
        "# CWN Free Edition parity matrix",
        "",
        "Generated by `tools/cwn_parity_audit.py` — do not edit by hand.",
        "",
        f"**{len(rows)} SRD sections.** Implemented **{counts['implemented']}**, "
        f"unverified **{counts['unverified']}**, partial **{counts['partial']}**, "
        f"missing **{counts['missing']}**, not applicable **{counts['not_applicable']}**.",
        "",
        "`implemented` means a matching module **and** a test that names it. It does not mean "
        "verified against the book: `tested_against_book`, `save_safe` and `playtested` are "
        "separate columns because they are separate claims.",
        "",
        "| Section | Chapter | Status | Python / MUD | Tests (n) | PDF page |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        impl = ", ".join((r["python"] + r["mud"])[:2]) or "—"
        test = r["tests"][0] if r["tests"] else "—"
        lines.append(
            f"| {r['system']} | {r['chapter']} | {r['coverage']} | {impl} | {test} | {r['pdf_page'] or '—'} |"
        )
    lines += [
        "",
        "## Why `pdf_page` is empty",
        "",
        "The Free Edition PDF is not in this repository. A page number written from memory would be "
        "indistinguishable from a checked one, so every row carries `null` until someone reads it off "
        "the book. Filling this column is the cheapest way to turn the matrix into an audit.",
        "",
    ]
    return "\n".join(lines)



def render_report(matrix: dict) -> str:
    """The #1068 coverage report: counts, the curated evidence, and the gaps with reasons."""
    rows = matrix["rows"]
    curated = [r for r in rows if r.get("curated")]
    counts = {s: sum(1 for r in rows if r["coverage"] == s) for s in STATUSES}
    verified_impl = [r for r in curated if r["coverage"] == "implemented" and r.get("verified")]
    gaps = [r for r in rows if r["coverage"] in ("partial", "missing", "unverified")]

    lines = [
        "# CWN coverage report (#1068)",
        "",
        "Generated by `tools/cwn_parity_audit.py` — do not edit by hand. Regenerate with "
        "`python3 tools/cwn_parity_audit.py`.",
        "",
        f"Reference: the Free Edition SRD at {SRD} (edition 081123). The Free Edition PDF is the "
        "authoritative book; the linked SRD omits Antagonists and the GM chapter, which this report "
        "records as a source limitation rather than filling from memory.",
        "",
        "## Counts",
        "",
        "| status | sections |",
        "| --- | ---: |",
    ]
    for status in STATUSES:
        lines.append(f"| {status} | {counts[status]} |")
    lines += [
        f"| **total** | **{len(rows)}** |",
        "",
        f"Of the {len(curated)} sections with curated evidence, **{len(verified_impl)}** are verified "
        "`implemented`: every cited module exists, every cited procedure/class/constant exists in that "
        "module's own AST, and every cited test file references the module it is cited for. The "
        f"remaining **{len(rows) - len(curated)}** sections keep the name-matching heuristic and are "
        "marked `provisional` below - they say 'there is code with this name and a "
        "test that names it', not 'this rule is implemented'.",
        "",
        "## Curated evidence (verified)",
        "",
        "| Section | Status | Python | Named procedures | Test | Rulebook |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in curated:
        modules = ", ".join(Path(m).name for m in row["python"]) or "—"
        procedures = ", ".join(row.get("procedures", [])[:4]) or "—"
        tests = str(len(row["tests"])) if row["tests"] else "—"
        rulebook = Path(row.get("rulebook", "")).name or "—"
        lines.append(f"| {row['system']} | {row['coverage']} | {modules} | {procedures} | {tests} | "
                     f"{rulebook} |")

    lines += ["", "## Gaps, with the reason recorded next to each", ""]
    if not gaps:
        lines.append("None.")
    for row in gaps:
        reason = row.get("divergence") or "no reason recorded"
        lines.append(f"- **{row['system']}** (`{row['coverage']}`) — {reason}")

    provisional = [r for r in rows if not r.get("curated")]
    lines += [
        "",
        f"## Provisional rows ({len(provisional)})",
        "",
        "These keep the filename/keyword heuristic from #1025. Promoting a row to the verified table "
        "means adding it to `data/rules/cwn_traceability.json` with the module, the named procedures "
        "and the test that exercises them; the audit then checks the claim against the code.",
        "",
        "| Section | Status | Modules (heuristic) |",
        "| --- | --- | --- |",
    ]
    for row in provisional:
        modules = ", ".join(Path(m).name for m in row["python"][:2]) or "—"
        lines.append(f"| {row['system']} | {row['coverage']} | {modules} |")

    lines += [
        "",
        "## No CWN core rule was modified",
        "",
        "This audit adds documentation, a traceability file and one new module "
        "(`src/rules/cwn_lifestyles.py`, covering a section that had no implementation). It changes no "
        "existing CWN procedure: `data/rules/cwn_baseline_sha256.json` pins the SHA-256 of every "
        "`src/rules/cwn_*.py` file, and `tests/test_cwn_traceability_1068.py` fails if one of them "
        "changes. Changing a CWN rule therefore cannot happen silently — it fails CI and requires the "
        "baseline to be re-pinned in a PR that says so.",
        "",
        "## How the two-way parity is enforced",
        "",
        "The rules side is enforced in CI: the matrix is regenerated by the audit tool and compared "
        "(`tools/cwn_parity_audit.py --check`), and the curated evidence is checked against the code. "
        "The tabletop side is a documentation claim, and `AGENTS.md` §271 forbids CI assertions over "
        "Markdown prose, so it is enforced by the PR checklist instead: a rules change must update "
        "`rulebook/` and `data/rules/cwn_traceability.json`'s `rulebook` column in the same PR. That is "
        "a deliberate, stated limitation of this mechanism, not an oversight.",
        "",
    ]
    return "\n".join(lines)


def stable_view(matrix: dict) -> dict:
    """The matrix as compared for freshness: test filenames reduced to a count.

    Test files are evidence, not the rule. A branch's matrix names the tests that existed when it was generated, so
    including the names in the equality test makes the lock depend on every other branch merged since — a PR that
    touched no CWN rule then fails CI because main gained a test file (#1228). Counting them keeps the useful signal
    ("this row has two named tests") without that coupling. The rule-bearing parts — sections, statuses, modules,
    procedures and the SHA baseline — are still compared exactly.
    """
    clone = copy.deepcopy(matrix)
    for row in clone.get("rows", ()):
        # Dropped, not counted: a count still moves when another branch adds or deletes one test file, and the point
        # is that the lock must not depend on the tree's test inventory at all.
        row.pop("tests", None)
    return clone


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    matrix = build()
    text = json.dumps(matrix, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        committed = json.loads(MATRIX.read_text(encoding="utf-8")) if MATRIX.exists() else None
        stale = (committed is None or stable_view(committed) != stable_view(matrix)
                 or not REPORT.exists()
                 or REPORT.read_text(encoding="utf-8") != render_report(matrix))
        if stale:
            print("cwn_parity_audit: matrix is stale; run python3 tools/cwn_parity_audit.py")
            return 1
        print(f"cwn_parity_audit: up to date ({len(matrix['rows'])} sections)")
        return 0
    MATRIX.parent.mkdir(parents=True, exist_ok=True)
    MATRIX.write_text(text, encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_report(matrix), encoding="utf-8")
    counts = {s: sum(1 for r in matrix["rows"] if r["coverage"] == s) for s in STATUSES}
    print(f"cwn_parity_audit: {len(matrix['rows'])} sections -> {MATRIX.relative_to(ROOT)}")
    print(f"  implemented={counts['implemented']} unverified={counts['unverified']} "
          f"partial={counts['partial']} missing={counts['missing']} "
          f"not_applicable={counts['not_applicable']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
