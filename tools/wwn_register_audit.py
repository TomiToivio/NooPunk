#!/usr/bin/env python3
"""WWN rule register for #1101 — Phase 0.

#1101 asks for a **rule-by-rule register**, not a chapter list: edition, printed section, source rights,
applicability, Python module, test, tabletop procedure, status, dependency and risk. It also asks that the audit
come before any code.

This tool exists for one reason: a register that nobody checks decays into a wish list within a week. Every row
that claims to be implemented must name a module and a test that are actually in this repository, and every row
that depends on a source we may not use must be `blocked`. If the code moves, `--check` fails.

What it deliberately cannot do: verify that a procedure is *faithful* to the book. That needs a human comparing
the printed page, and pretending otherwise is how a coverage matrix starts lying.

Usage:
    python3 tools/wwn_register_audit.py --render docs/rules/WWN_COVERAGE_1101.md
    python3 tools/wwn_register_audit.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "data" / "rules" / "wwn_register.json"

#: Statuses that assert something exists here. Each must be backed by real files.
CLAIMS_CODE = {"implemented", "partial", "verified_reuse"}

#: Statuses permitted for a row whose source is not usable by repository agents.
BLOCKED_ALLOWED = {"blocked", "missing", "not_applicable"}

REQUIRED_FIELDS = ("id", "chapter", "subsystem", "edition", "source_ref", "rights",
                   "kind", "status", "python", "tests", "tabletop", "owner", "risk")


def load() -> dict:
    return json.loads(REGISTER.read_text(encoding="utf-8"))


def audit(register: dict) -> list[str]:
    """Every way this register could be lying, as a list of human-readable failures."""
    problems: list[str] = []

    # rights value -> may anything be built from it?
    usable_by_rights: dict[str, bool] = {}
    for source in register["sources"].values():
        rights = source.get("rights", "?")
        usable_by_rights[rights] = usable_by_rights.get(rights, False) or bool(source.get("usable"))

    seen: set[str] = set()
    for row in register["rows"]:
        rid = row.get("id", "?")
        for field in REQUIRED_FIELDS:
            if field not in row:
                problems.append(f"{rid}: missing required field {field!r}")
        if rid in seen:
            problems.append(f"{rid}: duplicate row id")
        seen.add(rid)

        if row.get("status") not in register["statuses"]:
            problems.append(f"{rid}: unknown status {row.get('status')!r}")

        # A row that claims code must cite files that exist, and must actually cite at least one.
        if row.get("status") in CLAIMS_CODE:
            cited = list(row.get("python", [])) + list(row.get("tests", []))
            if not row.get("python") or not row.get("tests"):
                problems.append(f"{rid}: status {row['status']!r} must cite both a module and a test")
            for relative in cited:
                if not (ROOT / relative).exists():
                    problems.append(f"{rid}: cites {relative!r}, which is not in the repository")

        # A source we may not use cannot produce a verified row. Rows carry a rights *value*, not a source key;
        # several documents share a grant, so usability is resolved per rights value.
        if row.get("rights") not in usable_by_rights:
            problems.append(f"{rid}: unknown rights value {row.get('rights')!r}")
        elif not usable_by_rights[row["rights"]] and row.get("status") not in BLOCKED_ALLOWED:
            problems.append(
                f"{rid}: source rights {row['rights']!r} is not usable, so status {row['status']!r} is not "
                f"allowed")

        # Deluxe rows specifically: the tracker forbids synthesising them.
        if row.get("edition") == "deluxe" and row.get("status") not in BLOCKED_ALLOWED:
            problems.append(f"{rid}: Deluxe row claims {row['status']!r}; Deluxe text is not available")

        if row.get("risk") not in {"low", "medium", "high"}:
            problems.append(f"{rid}: risk {row.get('risk')!r} is not low/medium/high")

    for key, source in register["sources"].items():
        if not source.get("rights"):
            problems.append(f"source {key!r}: missing rights")
        if not isinstance(source.get("usable"), bool):
            problems.append(f"source {key!r}: 'usable' must be explicitly true or false")

    for entry in register.get("compatibility", []):
        for field in ("topic", "cwn", "wwn", "swn", "awn", "precedence", "citation"):
            if not entry.get(field):
                problems.append(f"compatibility {entry.get('topic', '?')!r}: missing {field}")

    return problems


def counts(register: dict) -> dict[str, int]:
    out = {status: 0 for status in register["statuses"]}
    for row in register["rows"]:
        out[row["status"]] = out.get(row["status"], 0) + 1
    return out


def render(register: dict) -> str:
    c = counts(register)
    total = len(register["rows"])
    implemented = c.get("implemented", 0) + c.get("verified_reuse", 0)
    lines = [
        "# WWN rules register (#1101, Phase 0)",
        "",
        "**Generated by `tools/wwn_register_audit.py` from `data/rules/wwn_register.json` — do not edit by hand.**",
        "",
        ("#1101 requires a rule-by-rule register before any code, with edition, printed section, rights, "
        "applicability, implementation, test, tabletop procedure, status, dependency and risk. This is that "
        "register. It is an audit, not a completion certificate."),
        "",
        "## Status of the tracker",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Registered subsystems | **{total}** |",
        f"| Implemented or verified by reuse | **{implemented}** |",
        f"| Partial | **{c.get('partial', 0)}** |",
        f"| Missing | **{c.get('missing', 0)}** |",
        f"| Blocked (source unavailable) | **{c.get('blocked', 0)}** |",
        "",
        f"That is **{implemented} of {total}** rows with code and a test behind them. The tracker stays open.",
        "",
        "## Sources and what may be used",
        "",
        "| Source | Rights | Usable here | Why |",
        "|---|---|---|---|",
    ]
    for source in register["sources"].values():
        lines.append(f"| {source['document']} | `{source['rights']}` | "
                     f"{'yes' if source['usable'] else '**no**'} | {source['note']} |")

    lines += ["", "## The register", "",
              "| ID | Subsystem | Edition | Status | Python | Test | Owner | Risk |",
              "|---|---|---|---|---|---|---|---|"]
    for row in register["rows"]:
        python = "<br>".join(f"`{Path(p).name}`" for p in row["python"]) or "—"
        tests = "<br>".join(f"`{Path(t).name}`" for t in row["tests"]) or "—"
        lines.append(f"| {row['id']} | {row['subsystem']} | {row['edition']} | **{row['status']}** | "
                     f"{python} | {tests} | {row['owner']} | {row['risk']} |")

    lines += ["", "## What is actually done, and what only looks done", ""]
    for status in ("implemented", "verified_reuse", "partial", "blocked"):
        rows = [r for r in register["rows"] if r["status"] == status]
        if not rows:
            continue
        lines.append(f"**{status}** ({len(rows)})")
        lines.append("")
        for row in rows:
            note = f" — {row['notes']}" if row.get("notes") else ""
            lines.append(f"- **{row['id']} {row['subsystem']}** (`{row['source_ref']}`){note}")
        lines.append("")

    lines += ["## Cross-game compatibility (CWN ↔ WWN ↔ SWN ↔ AWN)", "",
              "| Topic | CWN | WWN | SWN | AWN | Precedence | Citation |",
              "|---|---|---|---|---|---|---|"]
    for entry in register.get("compatibility", []):
        lines.append(f"| {entry['topic']} | {entry['cwn']} | {entry['wwn']} | {entry['swn']} | "
                     f"{entry['awn']} | **{entry['precedence']}** | {entry['citation']} |")

    lines += ["", "## Phase 0 gaps, stated rather than smoothed over", ""]
    for gap in register.get("phase0_gaps", []):
        lines.append(f"- {gap}")
    lines += [
        "",
        "## What this register cannot tell you",
        "",
        ("It verifies that a claimed row names code and a test that exist. It cannot verify that the procedure is "
        "*faithful* to the printed book — that requires a human with the page open. A row marked `implemented` "
        "means \"there is code with a test here\", which is exactly what `docs/rules/CWN_IMMUTABLE_CORE_1068.md` "
        "warns is not the same claim as rules fidelity."),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--render", metavar="PATH")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    register = load()
    problems = audit(register)
    c = counts(register)
    print(f"wwn_register: {len(register['rows'])} rows — "
          f"implemented={c.get('implemented', 0)} reuse={c.get('verified_reuse', 0)} "
          f"partial={c.get('partial', 0)} missing={c.get('missing', 0)} blocked={c.get('blocked', 0)}")

    if problems:
        for problem in problems:
            print(f"  FAIL {problem}", file=sys.stderr)
        print(f"wwn_register: {len(problems)} problem(s)", file=sys.stderr)
        return 1

    if args.render:
        target = Path(args.render)
        text = render(register)
        if target.exists() and target.read_text(encoding="utf-8") == text:
            print(f"{target}: already up to date")
        else:
            target.write_text(text, encoding="utf-8")
            print(f"{target}: written")

    if args.check and args.render:
        target = Path(args.render)
        if not target.exists() or target.read_text(encoding="utf-8") != render(register):
            print("wwn_register: rendered document is stale", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
