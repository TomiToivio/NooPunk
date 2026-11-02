#!/usr/bin/env python3
"""Duplication audit across the rules layers (#1053 priority 0, first box).

Both #1053 and #1054 name "the architecture audit of duplication" as their first unclosed item, and neither can
proceed cleanly without it: a rules engine cannot be extracted from engines while the same rule is implemented
several times with different behaviour.

This walks the rule-bearing trees, groups definitions by name, and — where it can — compares the bodies. The
distinction that matters is:

* **agreeing duplicates** are debt: four copies of `attribute_modifier` that all return the same thing will
  diverge the first time someone edits one;
* **diverging duplicates** are a bug already: the game gives different answers depending on which layer answered.

The report is generated so it cannot drift from the tree the way a hand-written inventory would.

Usage:
    python3 tools/duplication_audit.py --render docs/DUPLICATION_AUDIT_1053.md
    python3 tools/duplication_audit.py            # print a summary
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Trees that hold rules. `legacy/` is a frozen historical record and is deliberately excluded.
PY_TREES = ("src/rules", "mud/nopunk_mud", "mud/systems", "strategy_game")
GD_TREES = ("godot/core",)

#: Names that mean the same rule in each layer, so a match is not a coincidence of naming.
MIN_NAME_LEN = 8

#: Module-level names that are plumbing rather than rules: I/O, lifecycle, serialisation, entry points.
GENERIC_NAMES = frozenset({
    "main", "run", "setup", "reset", "update", "render", "save", "load", "serialize", "deserialize",
    "to_dict", "from_dict", "to_json", "from_json", "as_dict", "from_row", "to_frame", "to_csv", "to_jsonl",
    "get_state", "set_state", "load_state", "save_state", "parse_args", "build_parser", "build", "build_all",
    "register", "bootstrap", "initialise", "initialize", "shutdown", "start", "stop", "configure", "process",
    "validate", "normalise", "normalize", "summary", "describe", "report", "snapshot", "restore", "checkpoint",
    # scenario entry points and test helpers: they share names across slices without being the same rule
    "build_campaign", "run_demo", "declared_nodes", "roster_from_dict", "populated",
})


def _normalised(node: ast.AST) -> str:
    """A body fingerprint: docstrings dropped, names kept, whitespace and comments gone."""
    body = node.body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    dump = ast.dump(ast.Module(body=body, type_ignores=[]), annotate_fields=False)
    return hashlib.sha256(re.sub(r"\s+", "", dump).encode()).hexdigest()[:12]


def scan_python() -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = defaultdict(list)
    for tree in PY_TREES:
        for path in sorted((ROOT / tree).rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            try:
                module = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            # Module-level definitions only. A method called `to_dict` on two different classes is not a
            # duplicated rule, and counting it as one produced a number no reviewer should trust.
            for node in module.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name not in GENERIC_NAMES:
                    if len(node.name) < MIN_NAME_LEN or node.name.startswith("_"):
                        continue
                    found[node.name].append({
                        "file": str(path.relative_to(ROOT)),
                        "line": node.lineno,
                        "fingerprint": _normalised(node),
                    })
    return found


def scan_gdscript() -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = defaultdict(list)
    for tree in GD_TREES:
        for path in sorted((ROOT / tree).rglob("*.gd")):
            body = path.read_text(encoding="utf-8", errors="replace")
            for match in re.finditer(r"(?m)^\s*(?:static\s+)?func\s+(\w+)\s*\(", body):
                name = match.group(1)
                if len(name) >= MIN_NAME_LEN and not name.startswith("_"):
                    found[name].append({
                        "file": str(path.relative_to(ROOT)),
                        "line": body[:match.start()].count("\n") + 1,
                        "fingerprint": "",
                    })
    return found


def build() -> dict:
    python = scan_python()
    gdscript = scan_gdscript()

    duplicates = []
    for name, sites in sorted(python.items()):
        if len(sites) < 2:
            continue
        by_fingerprint = {site["fingerprint"] for site in sites}
        duplicates.append({
            "name": name,
            "sites": sites,
            "count": len(sites),
            "diverges": len(by_fingerprint) > 1,
        })

    # A rule implemented in Python and again in GDScript is the engine-coupling problem #1053 is about.
    cross = sorted(set(python) & set(gdscript))

    return {
        "python_duplicates": duplicates,
        "cross_language": [{"name": n, "python": python[n], "gdscript": gdscript[n]} for n in cross],
        "totals": {
            "duplicated_names": len(duplicates),
            "diverging": sum(1 for d in duplicates if d["diverges"]),
            "redundant_copies": sum(d["count"] - 1 for d in duplicates),
            "cross_language": len(cross),
        },
    }


def render(data: dict) -> str:
    t = data["totals"]
    lines = [
        "# Duplication audit (#1053 priority 0, #1054)",
        "",
        "**Generated by `tools/duplication_audit.py`; do not edit by hand.**",
        "",
        ("Both issues open with the same missing item: an audit of duplication across the rules layers. Extracting "
        "an engine-independent rules package is not possible while the same rule is implemented several times, "
        "because moving one copy leaves the others answering differently."),
        "",
        ("This is the **static** half of the audit: where the same rule is implemented more than once. It cannot "
        "tell you whether those copies *behave* the same, and it must not pretend to — a different body can "
        "compute the identical answer. That question is answered by the behavioural probe in "
        "`docs/RULES_PARITY_1053.md`, which calls every layer with the same character."),
        "",
        "| Finding | Meaning | What it needs |",
        "|---|---|---|",
        "| **Byte-identical copy** | same body in several homes | consolidation: debt, not yet a bug |",
        ("| **Differing implementation** | same rule, different code | behaviour unknown from source alone — "
        "run `tools/rules_parity_probe.py` |"),
        "",
        "| Measure | Count |",
        "|---|---:|",
        f"| Rule names defined in more than one file | **{t['duplicated_names']}** |",
        f"| …of those, **implemented differently** (behaviour unknown from source) | **{t['diverging']}** |",
        f"| Redundant copies to remove | **{t['redundant_copies']}** |",
        f"| Rules implemented in both Python and GDScript | **{t['cross_language']}** |",
        "",
        "## Rules written differently in more than one place",
        "",
    ]
    diverging = [d for d in data["python_duplicates"] if d["diverges"]]
    if not diverging:
        lines.append("None: every duplicated rule currently agrees with its copies.")
    else:
        lines += ["| Rule | Copies | Locations |", "|---|---:|---|"]
        for entry in diverging:
            sites = "<br>".join(f"`{s['file']}:{s['line']}`" for s in entry["sites"])
            lines.append(f"| `{entry['name']}` | {entry['count']} | {sites} |")
    lines += ["", "## Byte-identical copies — pure debt", ""]
    agreeing = [d for d in data["python_duplicates"] if not d["diverges"]]
    if not agreeing:
        lines.append("None.")
    else:
        lines += ["| Rule | Copies | Locations |", "|---|---:|---|"]
        for entry in agreeing:
            sites = "<br>".join(f"`{s['file']}:{s['line']}`" for s in entry["sites"])
            lines.append(f"| `{entry['name']}` | {entry['count']} | {sites} |")
    lines += ["", "## Rules implemented twice, in two languages", "",
              ("Python and GDScript both implementing a rule is the engine coupling #1053 is about: the Godot "
              "client is maintenance-only, yet it still holds rules the Python side must match by hand."), ""]
    if data["cross_language"]:
        lines += ["| Rule | Python | GDScript |", "|---|---|---|"]
        for entry in data["cross_language"]:
            py = "<br>".join(f"`{s['file']}`" for s in entry["python"])
            gd = "<br>".join(f"`{s['file']}`" for s in entry["gdscript"])
            lines.append(f"| `{entry['name']}` | {py} | {gd} |")
    else:
        lines.append("None.")
    lines += [
        "",
        "## How this was measured",
        "",
        "Definitions are collected with `ast` from `src/rules/`, `mud/nopunk_mud/`, `mud/systems/` and",
        "`strategy_game/`, and with a `func` regex from `godot/core/`. Functions are grouped by name; bodies are",
        "fingerprinted with docstrings removed so that a comment change is not mistaken for a behaviour change.",
        "`legacy/` is excluded because it is a frozen historical record that must not be modernised.",
        "",
        "A name match is evidence, not proof: two files may legitimately define `chase_modifier_table` in",
        "different layers. The fingerprint is what separates a real duplicate from a coincidence of naming, and",
        "the diverging table is the one to read first.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--render", metavar="PATH")
    parser.add_argument("--check", action="store_true", help="exit 1 if any duplicate diverges")
    args = parser.parse_args(argv)

    data = build()
    t = data["totals"]
    print(f"{t['duplicated_names']} duplicated rule names, {t['diverging']} diverging, "
          f"{t['redundant_copies']} redundant copies, {t['cross_language']} cross-language")

    if args.render:
        target = Path(args.render)
        text = render(data)
        if target.exists() and target.read_text(encoding="utf-8") == text:
            print(f"{target}: already up to date")
        else:
            target.write_text(text, encoding="utf-8")
            print(f"{target}: written")

    if args.check and t["diverging"]:
        print(f"{t['diverging']} duplicated rule(s) have diverged: see the audit", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
