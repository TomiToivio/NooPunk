#!/usr/bin/env python3
"""Rule registers for the Without Number trackers (#1101 WWN, #1105 SWN).

Both trackers ask for the same artefact with the same purpose: replace a chapter-level table with a
**rule-by-rule register** — edition, printed page, rights, applicability, implementation, test, tabletop
procedure, status — and keep it honest as the code moves.

This is the shared implementation. `tools/wwn_register_audit.py` and `tools/swn_register_audit.py` are thin
wrappers that point it at their register. They are wrappers and not copies on purpose: this repository has
already paid for two coverage generators that drifted apart, and a second identical validator would be the same
mistake with a different filename.

What makes a register auditable rather than decorative:

* a row claiming code must cite a module **and** a test that exist on disk;
* a row cannot lean on a source that cannot be used;
* an edition listed in `blocked_editions` may not claim to be done;
* where the register asks for it, a row must state how far its implementation has been checked against the
  published text — because "there is code with this name" and "this matches the book" are different claims.

What it cannot do: verify fidelity. That needs a human with the page open, and pretending otherwise is how a
coverage matrix starts lying.

Usage:
    python3 tools/rules_register_audit.py --register data/rules/swn_register.json \
        --render docs/rules/SWN_COVERAGE_1105.md
    python3 tools/rules_register_audit.py --register ... --render ... --check
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Statuses that assert something exists here. Each must be backed by real files.
CLAIMS_CODE = {"implemented", "partial", "verified_reuse"}

#: Statuses permitted for a row whose source is not usable by repository agents.
BLOCKED_ALLOWED = {"blocked", "missing", "not_applicable"}

#: A row must say where in the book it comes from, in whichever form its tracker uses.
SOURCE_FIELDS = ("source_ref", "printed_page")

REQUIRED_FIELDS = ("id", "chapter", "subsystem", "edition", "rights", "status",
                   "python", "tests", "tabletop", "owner")


def load(register_path: Path | str) -> dict:
    path = Path(register_path)
    if not path.is_absolute():
        path = ROOT / path
    return json.loads(path.read_text(encoding="utf-8"))


def audit(register: dict) -> list[str]:
    """Every way this register could be lying, as a list of human-readable failures."""
    problems: list[str] = []

    # rights value -> may anything be built from it?
    usable_by_rights: dict[str, bool] = {}
    text_available_by_rights: dict[str, bool] = {}
    for source in register["sources"].values():
        rights = source.get("rights", "?")
        usable_by_rights[rights] = usable_by_rights.get(rights, False) or bool(source.get("usable"))
        text_available_by_rights[rights] = (text_available_by_rights.get(rights, False)
                                           or bool(source.get("text_available", False)))

    blocked_editions = set(register.get("blocked_editions", []))
    requires_fidelity = bool(register.get("requires_fidelity"))
    fidelities = register.get("fidelities", {})

    seen: set[str] = set()
    for row in register["rows"]:
        rid = row.get("id", "?")
        for field in REQUIRED_FIELDS:
            if field not in row:
                problems.append(f"{rid}: missing required field {field!r}")
        if rid in seen:
            problems.append(f"{rid}: duplicate row id")
        seen.add(rid)

        if not any(row.get(field) for field in SOURCE_FIELDS):
            problems.append(f"{rid}: cites no book location (expected one of {SOURCE_FIELDS})")

        if row.get("status") not in register["statuses"]:
            problems.append(f"{rid}: unknown status {row.get('status')!r}")

        # A row that claims code must cite files that exist, and must actually cite at least one of each.
        if row.get("status") in CLAIMS_CODE:
            if not row.get("python") or not row.get("tests"):
                problems.append(f"{rid}: status {row['status']!r} must cite both a module and a test")
            for relative in list(row.get("python", [])) + list(row.get("tests", [])):
                if not (ROOT / relative).exists():
                    problems.append(f"{rid}: cites {relative!r}, which is not in the repository")

        # A source we may not use cannot produce a verified row.
        if row.get("rights") not in usable_by_rights:
            problems.append(f"{rid}: unknown rights value {row.get('rights')!r}")
        elif not usable_by_rights[row["rights"]] and row.get("status") not in BLOCKED_ALLOWED:
            problems.append(
                f"{rid}: source rights {row['rights']!r} is not usable, so status {row['status']!r} is not "
                f"allowed")

        # Editions whose text is unavailable cannot produce a done row.
        if row.get("edition") in blocked_editions and row.get("status") not in BLOCKED_ALLOWED:
            problems.append(f"{rid}: edition {row['edition']!r} is blocked, so status {row['status']!r} is not "
                            f"allowed")

        if requires_fidelity:
            fidelity = row.get("fidelity")
            if fidelity not in fidelities:
                problems.append(f"{rid}: fidelity {fidelity!r} is not one of {sorted(fidelities)}")
            elif fidelity == "verified" and not text_available_by_rights.get(row.get("rights"), False):
                problems.append(
                    f"{rid}: claims verified fidelity, but no readable copy of its source is available")

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


def fidelity_counts(register: dict) -> dict[str, int]:
    out = {fidelity: 0 for fidelity in register.get("fidelities", {})}
    for row in register["rows"]:
        if row.get("fidelity") in out:
            out[row["fidelity"]] += 1
    return out


def render(register: dict) -> str:
    c = counts(register)
    total = len(register["rows"])
    done = c.get("implemented", 0) + c.get("verified_reuse", 0)
    title = register.get("title", "Rules register")
    lines = [
        f"# {title}",
        "",
        "**Generated by `tools/rules_register_audit.py` from the register JSON — do not edit by hand.**",
        "",
        register.get("intro", ""),
        "",
        "## Status",
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Registered subsystems | **{total}** |",
    ]
    for status in register["statuses"]:
        lines.append(f"| {status} | **{c.get(status, 0)}** |")
    lines.append(f"| **rows with code and a test** | **{done}** |")

    if register.get("requires_fidelity"):
        fc = fidelity_counts(register)
        lines += ["", "### How far the code has been checked against the book", "",
                  ("A row can be implemented and still unverified. These two columns are separate claims and this "
                  "register keeps them separate."), "",
                  "| Fidelity | Rows |", "|---|---:|"]
        for fidelity in register.get("fidelities", {}):
            lines.append(f"| {fidelity} | **{fc.get(fidelity, 0)}** |")
        lines.append("")
        for fidelity, meaning in register.get("fidelities", {}).items():
            lines.append(f"- **{fidelity}** — {meaning}")

    lines += ["", "## Sources and what may be used", "",
              "| Source | Rights | Usable here | Why |", "|---|---|---|---|"]
    for source in register["sources"].values():
        lines.append(f"| {source.get('document', '?')} | `{source.get('rights')}` | "
                     f"{'yes' if source.get('usable') else '**no**'} | {source.get('note', '')} |")

    faithful = register.get("requires_fidelity")
    header = "| ID | Subsystem | Page | Status |" + (" Fidelity |" if faithful else "") + " Python | Test | Owner |"
    rule = "|---|---|---|---|" + ("---|" if faithful else "") + "---|---|---|"
    lines += ["", "## The register", "", header, rule]
    for row in register["rows"]:
        python = "<br>".join(f"`{Path(p).name}`" for p in row["python"]) or "—"
        tests = "<br>".join(f"`{Path(t).name}`" for t in row["tests"]) or "—"
        page = row.get("printed_page") or row.get("source_ref") or "—"
        mid = f" {row['fidelity']} |" if faithful else ""
        lines.append(f"| {row['id']} | {row['subsystem']} | {page} | **{row['status']}** |{mid} "
                     f"{python} | {tests} | {row['owner']} |")

    lines += ["", "## What is actually done, and what only looks done", ""]
    for status in ("implemented", "verified_reuse", "partial", "blocked", "not_applicable"):
        rows = [r for r in register["rows"] if r["status"] == status]
        if not rows:
            continue
        lines.append(f"**{status}** ({len(rows)})")
        lines.append("")
        for row in rows:
            note = f" — {row['notes']}" if row.get("notes") else ""
            lines.append(f"- **{row['id']} {row['subsystem']}**{note}")
        lines.append("")

    lines += ["## Cross-game compatibility (CWN ↔ WWN ↔ SWN ↔ AWN)", "",
              "| Topic | CWN | WWN | SWN | AWN | Precedence | Citation |",
              "|---|---|---|---|---|---|---|"]
    for entry in register.get("compatibility", []):
        lines.append(f"| {entry['topic']} | {entry['cwn']} | {entry['wwn']} | {entry['swn']} | "
                     f"{entry['awn']} | **{entry['precedence']}** | {entry['citation']} |")

    lines += ["", "## Gaps, stated rather than smoothed over", ""]
    for gap in register.get("gaps", []):
        lines.append(f"- {gap}")
    lines += [
        "",
        "## What this register cannot tell you",
        "",
        ("It verifies that a claimed row names code and a test that exist, that no row leans on a source it may "
        "not use, and — where the tracker asks — how far the implementation has been checked against the printed "
        "text. It cannot verify fidelity itself. That needs a human with the page open."),
        "",
    ]
    return "\n".join(lines)


def run(argv: list[str] | None, default_register: str | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--register", default=default_register,
                        help="path to the register JSON")
    parser.add_argument("--render", metavar="PATH")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)

    if not args.register:
        print("rules_register_audit: --register is required", file=sys.stderr)
        return 2

    register = load(args.register)
    problems = audit(register)
    c = counts(register)
    summary = " ".join(f"{k}={c.get(k, 0)}" for k in register["statuses"] if c.get(k))
    print(f"{Path(args.register).name}: {len(register['rows'])} rows — {summary}")
    if register.get("requires_fidelity"):
        fc = fidelity_counts(register)
        print("  fidelity: " + " ".join(f"{k}={v}" for k, v in fc.items()))

    if problems:
        for problem in problems:
            print(f"  FAIL {problem}", file=sys.stderr)
        print(f"rules_register_audit: {len(problems)} problem(s)", file=sys.stderr)
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
            print("rules_register_audit: rendered document is stale", file=sys.stderr)
            return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    return run(argv)


if __name__ == "__main__":
    raise SystemExit(main())
