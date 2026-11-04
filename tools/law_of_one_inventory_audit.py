#!/usr/bin/env python3
"""Law of One RPG inventory audit and renderer (#1124, Phase 1).

Phase 1 is an inventory. That means the deliverable is judged by *coverage*, not by code: every concept the
issue names must have a disposition, a citation and a decision about whether it needs a rule. A hand-written
document quietly drops rows; a generated one cannot, so this tool renders `docs/law_of_one/RULES_INVENTORY.md`
from `data/law_of_one/rules_inventory.json` and checks the coverage map against it.

Checks, all of which fail the build rather than warn:

* every row has an id, a priority from the fixed vocabulary, a group, at least one source reference, a
  faithful meaning, a non-goals note, and an explicit `rules_needed`;
* every row that needs rules states a minimal procedure and a state fragment — an "inventory item" that says
  it needs a mechanic without saying what the mechanic is, is not an inventory;
* every row that does not need rules says why in `non_goals`;
* every concept in `data/law_of_one/source_coverage.json` maps to at least one existing row, and every row is
  reachable from at least one concept (no orphans in either direction);
* the phase gate holds: no Law of One implementation module exists yet.

    python3 tools/law_of_one_inventory_audit.py            # render the inventory and the coverage map
    python3 tools/law_of_one_inventory_audit.py --check    # exit 1 if either document is stale or a check fails
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "law_of_one" / "rules_inventory.json"
COVERAGE = ROOT / "data" / "law_of_one" / "source_coverage.json"
CHECKS = ROOT / "data" / "law_of_one" / "passage_checks.json"
CHECKS = ROOT / "data" / "law_of_one" / "passage_checks.json"
DOC = ROOT / "docs" / "law_of_one" / "RULES_INVENTORY.md"
MAP = ROOT / "docs" / "law_of_one" / "COVERAGE_MAP.md"
CHECKS_DOC = ROOT / "docs" / "law_of_one" / "PASSAGE_CHECKS.md"
CHECKS_DOC = ROOT / "docs" / "law_of_one" / "PASSAGE_CHECKS.md"

PRIORITIES = ("core", "optional", "narrative_only", "out_of_scope")
GROUPS = ("essential_core", "fourth_density_activity", "optional_narrativist", "setting_principle")

#: Where a later phase's implementation would live. Phase 1 must leave these empty.
IMPLEMENTATION_PATHS = (ROOT / "src" / "law_of_one", ROOT / "law_of_one")


def load() -> tuple[dict, dict]:
    return (json.loads(INVENTORY.read_text(encoding="utf-8")),
            json.loads(COVERAGE.read_text(encoding="utf-8")))


def load_checks() -> dict:
    return json.loads(CHECKS.read_text(encoding="utf-8"))


def audit_checks(checks: dict, inventory: dict) -> list[str]:
    """Every check row must be honest about what it is, and every citation must be *somewhere* in the ledger."""
    problems: list[str] = []
    known = {row["id"] for row in inventory["rows"]}
    statuses = set(checks["statuses"])
    cited: set[str] = set()
    for check in checks["checks"]:
        ref = check.get("ref", "?")
        if check.get("status") not in statuses:
            problems.append(f"check {ref}: status {check.get('status')!r} is not one of {sorted(statuses)}")
        if not str(check.get("text", "")).strip():
            problems.append(f"check {ref}: no passage text recorded")
        if not str(check.get("supports_claim", "")).strip():
            problems.append(f"check {ref}: does not say what claim it is meant to support")
        for rid in check.get("used_by", []):
            if rid not in known:
                problems.append(f"check {ref}: unknown row {rid!r}")
            cited.add(rid)
    unchecked_rows = {row["id"] for row in inventory["rows"] if row["rules_needed"]} - cited
    if unchecked_rows:
        problems.append(f"rows that rely on no checked citation: {sorted(unchecked_rows)}")
    return problems


def render_checks(checks: dict) -> str:
    order = {"supports": 0, "partial": 1, "ambiguous": 2, "unchecked": 3}
    rows = sorted(checks["checks"], key=lambda c: (order.get(c["status"], 9), c["ref"]))
    lines = [
        "# Law of One RPG — passage checks (issue #1124, Phase 1)",
        "",
        "The updated issue asks for the cited passages to be checked directly, and for ambiguity to be",
        "annotated rather than smoothed over. This is that ledger. Generated from",
        "`data/law_of_one/passage_checks.json` by `tools/law_of_one_inventory_audit.py`.",
        "",
        "A citation is **not** verified because it is cited. Only `supports` means the passage was read and says",
        "what the inventory claims; `partial`, `ambiguous` and `unchecked` are recorded so that Phase 2 knows",
        "exactly what still needs reading.",
        "",
        "| ref | status | what the passage says | which claim it carries |",
        "|---|---|---|---|",
    ]
    for check in rows:
        text = str(check["text"]).replace("|", "/")
        if len(text) > 220:
            text = text[:217] + "..."
        lines.append(f"| {check['ref']} | `{check['status']}` | {text} | {str(check['supports_claim']).replace('|', '/')} |")
    counts: dict[str, int] = {}
    for check in checks["checks"]:
        counts[check["status"]] = counts.get(check["status"], 0) + 1
    lines += ["", "## Counts", ""]
    for status, meaning in checks["statuses"].items():
        lines.append(f"* **{status}** ({counts.get(status, 0)}) — {meaning}")
    lines += [
        "",
        "## What remains before the research can be called exhaustive",
        "",
        "The issue names three gaps; this ledger makes them concrete:",
        "",
        "* the **unchecked** and **ambiguous** rows above (`47.8`, `6.24`, `21.5`) must be read and either",
        "  confirmed or replaced;",
        "* the peripheral categories (Earth History, People, UFOs, Pyramids, Objects) are disposed of in the",
        "  coverage map but not read passage by passage;",
        "* the entity catalogue is a seed, not a concordance: the full named-entity scan across all sessions is",
        "  still open.",
        "",
    ]
    return "\n".join(lines)


def audit(inventory: dict, coverage: dict) -> list[str]:
    problems: list[str] = []
    rows = inventory["rows"]
    by_id: dict[str, dict] = {}
    for row in rows:
        rid = row.get("id", "?")
        if rid in by_id:
            problems.append(f"{rid}: duplicate id")
        by_id[rid] = row
        if row.get("priority") not in PRIORITIES:
            problems.append(f"{rid}: priority {row.get('priority')!r} is not one of {PRIORITIES}")
        if row.get("group") not in GROUPS:
            problems.append(f"{rid}: group {row.get('group')!r} is not one of {GROUPS}")
        if not row.get("source"):
            problems.append(f"{rid}: no source reference")
        if not str(row.get("faithful_meaning", "")).strip():
            problems.append(f"{rid}: no faithful meaning recorded")
        if not str(row.get("non_goals", "")).strip():
            problems.append(f"{rid}: no explicit non-goals")
        if type(row.get("rules_needed")) is not bool:
            problems.append(f"{rid}: rules_needed must be true or false, explicitly")
        elif row["rules_needed"]:
            if not str(row.get("minimal_procedure", "")).strip():
                problems.append(f"{rid}: needs rules but states no minimal procedure")
            if not str(row.get("state", "")).strip():
                problems.append(f"{rid}: needs rules but states no state fragment")
            if row["priority"] == "out_of_scope":
                problems.append(f"{rid}: out_of_scope but claims needed rules")
        else:
            if row["priority"] == "core":
                problems.append(f"{rid}: core priority with no rules")
            if not str(row.get("minimal_procedure", "")).strip():
                problems.append(f"{rid}: no treatment recorded for an unmechanised concept")

    mapped: set[str] = set()
    for concept in coverage["required"]:
        if not concept.get("rows"):
            problems.append(f"coverage {concept['id']}: no inventory row covers this concept")
        for rid in concept.get("rows", []):
            mapped.add(rid)
            if rid not in by_id:
                problems.append(f"coverage {concept['id']}: unknown row {rid!r}")

    orphans = sorted(set(by_id) - mapped)
    if orphans:
        problems.append(f"rows not reachable from any source concept: {orphans}")

    for path in IMPLEMENTATION_PATHS:
        if path.exists():
            problems.append(
                f"{path.relative_to(ROOT)} exists: Phase 1 is an inventory and the issue requires review "
                f"before implementation")

    return problems


def _cell(text: str) -> str:
    return str(text).replace("|", "/").replace("\n", " ").strip()



def load_checks() -> dict:
    return json.loads(CHECKS.read_text(encoding="utf-8"))


def audit_checks(checks: dict, inventory: dict) -> list[str]:
    """A citation is not verified because it is cited.

    Every check row must state a status, what the passage said and which claim it carries, and every row that
    needs rules must be reached by at least one check — otherwise "we cited something" would pass for "we read
    it".
    """
    problems: list[str] = []
    known = {row["id"] for row in inventory["rows"]}
    statuses = set(checks["statuses"])
    cited: set[str] = set()
    for check in checks["checks"]:
        ref = check.get("ref", "?")
        if check.get("status") not in statuses:
            problems.append(f"check {ref}: status {check.get('status')!r} is not one of {sorted(statuses)}")
        if not str(check.get("text", "")).strip():
            problems.append(f"check {ref}: no passage text recorded")
        if not str(check.get("supports_claim", "")).strip():
            problems.append(f"check {ref}: does not say which claim it supports")
        for rid in check.get("used_by", []):
            if rid not in known:
                problems.append(f"check {ref}: unknown row {rid!r}")
            cited.add(rid)
    uncovered = {row["id"] for row in inventory["rows"] if row["rules_needed"]} - cited
    if uncovered:
        problems.append(f"rows that rely on no checked citation: {sorted(uncovered)}")
    return problems


def render_checks(checks: dict) -> str:
    order = {"supports": 0, "partial": 1, "ambiguous": 2, "unchecked": 3}
    rows = sorted(checks["checks"], key=lambda c: (order.get(c["status"], 9), c["ref"]))
    lines = [
        "# Law of One RPG — passage checks (issue #1124, Phase 1)",
        "",
        "The updated issue asks for the cited passages to be checked directly, and for ambiguity to be annotated",
        "rather than smoothed over. This is that ledger. Generated from `data/law_of_one/passage_checks.json` by",
        "`tools/law_of_one_inventory_audit.py` — do not edit it by hand.",
        "",
        "A citation is **not** verified because it is cited. Only `supports` means the passage was read and says",
        "what the inventory claims; `partial`, `ambiguous` and `unchecked` are recorded so that Phase 2 knows",
        "exactly what still needs reading.",
        "",
        "| ref | status | what the passage says | which claim it carries |",
        "|---|---|---|---|",
    ]
    for check in rows:
        text = str(check["text"]).replace("|", "/")
        if len(text) > 220:
            text = text[:217] + "..."
        lines.append(f"| {check['ref']} | `{check['status']}` | {text} | "
                     f"{str(check['supports_claim']).replace('|', '/')} |")
    counts: dict[str, int] = {}
    for check in checks["checks"]:
        counts[check["status"]] = counts.get(check["status"], 0) + 1
    lines += ["", "## Counts", ""]
    for status, meaning in checks["statuses"].items():
        lines.append(f"* **{status}** ({counts.get(status, 0)}) — {meaning}")
    lines += [
        "",
        "## What remains before the research can be called exhaustive",
        "",
        "* the `unchecked` and `ambiguous` rows above must be read and either confirmed or replaced;",
        "* the peripheral categories (Earth History, People, UFOs, Pyramids, Objects) are disposed of in the",
        "  coverage map but not read passage by passage;",
        "* the entity catalogue is a seed, not a concordance: the full named-entity scan is still open.",
        "",
    ]
    return "\n".join(lines)


def render(inventory: dict, coverage: dict) -> str:
    rows = inventory["rows"]
    counts = {priority: sum(1 for row in rows if row["priority"] == priority) for priority in PRIORITIES}
    by_group = {group: [row for row in rows if row["group"] == group] for group in GROUPS}
    lines = [
        "# Law of One RPG — rules inventory (issue #1124, Phase 1)",
        "",
        "**Status: inventory only.** No rule below is implemented, and none may be until the inventory is",
        "reviewed. This file is generated from `data/law_of_one/rules_inventory.json` by",
        "`tools/law_of_one_inventory_audit.py`; edit the data, not the table.",
        "",
        "Every row separates **what the source says** (`Faithful meaning`) from **what the game would do**",
        "(`Minimal procedure`). The first is a claim about the Ra material and carries session citations; the",
        "second is ours, and is a proposal for playtest, not a claim that Ra wrote a rule.",
        "",
        f"**{len(rows)} concepts inventoried** — " + ", ".join(f"{k} **{v}**" for k, v in counts.items()) + ".",
        "",
        "| priority | meaning |",
        "|---|---|",
    ]
    for key, meaning in inventory["priorities"].items():
        lines.append(f"| `{key}` | {meaning} |")
    lines += ["", "## Conventions the inventory holds itself to", ""]
    for key, text in inventory["conventions"].items():
        lines.append(f"* **{key.replace('_', ' ')}** — {text}")
    lines += ["", "## Coverage map summary", "",
              "| source concept | rows |", "|---|---|"]
    for concept in coverage["required"]:
        lines.append(f"| {_cell(concept['title'])} ({concept['kind']}) | "
                     + ", ".join(f"`{rid}`" for rid in concept["rows"]) + " |")

    group_titles = {
        "essential_core": "1. Essential playable core",
        "fourth_density_activity": "2. Fourth-density activities",
        "optional_narrativist": "3. Optional narrativist tools",
        "setting_principle": "4. Setting principles and out-of-scope material",
    }
    for group in GROUPS:
        lines += ["", f"## {group_titles[group]}", ""]
        for row in by_group[group]:
            lines += [
                f"### `{row['id']}` — {row['concept']}",
                "",
                f"* **Priority:** `{row['priority']}` · **rules needed:** {'yes' if row['rules_needed'] else 'no'}"
                + (f" · **page:** {row['page']}" if row.get("page") else ""),
                f"* **Source:** {', '.join(row['source'])}",
                f"* **Faithful meaning (source claim):** {row['faithful_meaning']}",
                f"* **Minimal procedure / treatment (ours):** {row['minimal_procedure']}",
            ]
            if row.get("state"):
                lines.append(f"* **State fragment:** `{row['state']}`")
            if row.get("interactions"):
                lines.append(f"* **Interactions:** {row['interactions']}")
            lines.append(f"* **Non-goals:** {row['non_goals']}")
            if row.get("open_questions"):
                lines.append(f"* **Open question:** {row['open_questions']}")
            lines.append("")

    lines += [
        "## What this inventory deliberately does not do",
        "",
        "* It defines **no attributes, skills, hit points, combat, equipment, classes or XP**. Those belong to a",
        "  host game; this module is meant to attach to one, or to stand alone as a narrativist game.",
        "* It does not reskin anything, does not touch the NoöPunk rulebook, and does not merge rulebooks.",
        "* It does not turn cosmology into dice. Nine concepts are `narrative_only` and three are `out_of_scope`",
        "  precisely so that no one later mistakes a placeholder for a mechanic.",
        "",
        "## Phase gate",
        "",
        "Phase 2 (the standalone playable rulebook) may start only after this inventory is reviewed. The",
        "audit fails while any implementation module exists, which is how that gate is enforced rather than",
        "remembered.",
        "",
        f"_Generated from {len(rows)} rows; source: {inventory['source']['primary']['title']}._",
        "",
    ]
    return "\n".join(lines)


def render_map(coverage: dict, inventory: dict) -> str:
    by_id = {row["id"]: row for row in inventory["rows"]}
    lines = [
        "# Law of One RPG — source coverage map (issue #1124, Phase 1)",
        "",
        "Every source concept the issue requires, and the inventory rows that carry it. A concept mapped to",
        "several rows is normal: cosmology gets a narrative row, and anything playable gets a rules row beside",
        "it. Generated by `tools/law_of_one_inventory_audit.py`.",
        "",
        "| # | source concept | kind | rows (priority) |",
        "|---|---|---|---|",
    ]
    for index, concept in enumerate(coverage["required"], start=1):
        rows = ", ".join(f"`{rid}` ({by_id[rid]['priority']})" for rid in concept["rows"])
        lines.append(f"| {index} | [{_cell(concept['title'])}]({concept['url']}) | {concept['kind']} | {rows} |")
    kinds: dict[str, int] = {}
    for concept in coverage["required"]:
        kinds[concept["kind"]] = kinds.get(concept["kind"], 0) + 1
    lines += ["", "## Counts", ""]
    for kind, count in sorted(kinds.items()):
        lines.append(f"* **{kind}**: {count}")
    lines += [
        "",
        "## Named source pages that are not yet inventoried",
        "",
        "The categories index lists more pages than this phase covers. The following are deliberately outside",
        "the Phase 1 scope — each either duplicates a covered concept or is campaign material rather than a",
        "rule — and are recorded here so the gap is visible rather than silent:",
        "",
        "* Earth History, Earth Present, Solar System History, People, Places and objects (setting reference;",
        "  overlaps `entity-catalogue`)",
        "* Tarot (the archetypal deck itself; `archetypal-contemplation` uses it without importing it)",
        "* Sexual Energy Transfer (a distinct topic the issue does not request; would need its own consent-first",
        "  procedure before any implementation)",
        "* UFOs, Pyramids, Ra Contact, Books, Miscellanea, Not Answered (§setting and meta)",
        "* Science, The Original Thought, Before the Veil (cosmology already covered by the narrative rows)",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    inventory, coverage = load()
    checks = load_checks()
    problems = audit(inventory, coverage) + audit_checks(checks, inventory)
    doc = render(inventory, coverage)
    map_doc = render_map(coverage, inventory)
    checks_doc = render_checks(checks)

    if args.check:
        stale = []
        if not DOC.is_file() or DOC.read_text(encoding="utf-8") != doc:
            stale.append("RULES_INVENTORY.md")
        if not MAP.is_file() or MAP.read_text(encoding="utf-8") != map_doc:
            stale.append("COVERAGE_MAP.md")
        if not CHECKS_DOC.is_file() or CHECKS_DOC.read_text(encoding="utf-8") != checks_doc:
            stale.append("PASSAGE_CHECKS.md")
        if not CHECKS_DOC.is_file() or CHECKS_DOC.read_text(encoding="utf-8") != checks_doc:
            stale.append("PASSAGE_CHECKS.md")
        if stale:
            print(f"law_of_one_inventory_audit: stale document(s): {', '.join(stale)}", file=sys.stderr)
            return 1
        if problems:
            print(f"law_of_one_inventory_audit: {len(problems)} problem(s)", file=sys.stderr)
            for problem in problems:
                print(f"  {problem}", file=sys.stderr)
            return 1
        print(f"law_of_one_inventory_audit: up to date ({len(inventory['rows'])} concepts)")
        return 0

    DOC.parent.mkdir(parents=True, exist_ok=True)
    DOC.write_text(doc, encoding="utf-8")
    MAP.write_text(map_doc, encoding="utf-8")
    CHECKS_DOC.write_text(checks_doc, encoding="utf-8")
    CHECKS_DOC.write_text(checks_doc, encoding="utf-8")
    print(f"law_of_one_inventory_audit: {len(inventory['rows'])} concepts -> "
          f"{DOC.relative_to(ROOT)}, {MAP.relative_to(ROOT)}")
    if problems:
        print(f"  {len(problems)} problem(s)", file=sys.stderr)
        for problem in problems:
            print(f"    {problem}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
