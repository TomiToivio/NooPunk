#!/usr/bin/env python3
"""Enumerate every public CWN/SWN/WN rule procedure the repository implements.

The Godot game must not re-implement the rules: `AGENTS.md` §13 says to consume a shared
specification rather than re-declare it in a second runtime, and `godot/core/rules_adapter.gd`
already reads a data kernel instead of hardcoding tables. This script produces the missing
piece for "all CWN rules in Godot": an exhaustive, machine-readable registry of the rule
procedures that already exist under ``src/rules``, so the adapter has something complete to
consume and so the gap to the SRD can be measured instead of guessed.

It parses with ``ast`` and never imports the modules, so it has no side effects and no
third-party dependencies.

Usage:
    python3 tools/cwn_coverage_manifest.py            # write data/rules/cwn_coverage.json
    python3 tools/cwn_coverage_manifest.py --check    # exit 1 if the file is stale
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "src" / "rules"
OUT = ROOT / "data" / "rules" / "cwn_coverage.json"
PREFIXES = ("cwn_", "swn_", "wn_")


def _signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    parts: list[str] = []
    positional = list(args.posonlyargs) + list(args.args)
    for i, arg in enumerate(positional):
        if arg.arg in ("self", "cls"):
            continue
        default_at = len(positional) - len(args.defaults)
        parts.append(arg.arg + ("=..." if i >= default_at else ""))
    if args.vararg:
        parts.append("*" + args.vararg.arg)
    elif args.kwonlyargs:
        parts.append("*")
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parts.append(arg.arg + ("=..." if default is not None else ""))
    if args.kwarg:
        parts.append("**" + args.kwarg.arg)
    return "(" + ", ".join(parts) + ")"


def _docline(node: ast.AST) -> str:
    doc = ast.get_docstring(node) or ""
    return doc.strip().splitlines()[0].strip() if doc.strip() else ""


def procedures_in(path: Path) -> list[dict[str, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    found: list[dict[str, str]] = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_"):
            found.append({"name": node.name, "signature": _signature(node), "doc": _docline(node)})
        elif isinstance(node, ast.ClassDef) and not node.name.startswith("_"):
            methods = [
                {"name": f"{node.name}.{sub.name}", "signature": _signature(sub), "doc": _docline(sub)}
                for sub in node.body
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef))
                and not sub.name.startswith("_")
            ]
            if methods:
                found.append({"name": node.name, "signature": "", "doc": _docline(node), "methods": methods})
    return found


def build() -> dict:
    modules = []
    total = 0
    for path in sorted(RULES.glob("*.py")):
        if not path.name.startswith(PREFIXES) or path.name == "__init__.py":
            continue
        procedures = procedures_in(path)
        count = sum(len(p.get("methods", [])) or 1 for p in procedures)
        total += count
        modules.append({"module": path.name, "procedures": procedures, "count": count})
    return {
        "schema": 1,
        "source": "src/rules",
        "note": "Registry of implemented rule procedures. Presence here is code coverage, not SRD parity.",
        "totals": {"modules": len(modules), "procedures": total},
        "modules": modules,
    }


def render(data: dict) -> str:
    return json.dumps(data, indent=2, sort_keys=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the committed registry is stale")
    args = parser.parse_args(argv)
    text = render(build())
    if args.check:
        if not OUT.exists():
            print(f"missing: {OUT.relative_to(ROOT)} (run tools/cwn_coverage_manifest.py)")
            return 1
        if OUT.read_text(encoding="utf-8") != text:
            print(f"stale: {OUT.relative_to(ROOT)} (run tools/cwn_coverage_manifest.py)")
            return 1
        print("cwn coverage registry is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    data = json.loads(text)
    print(f"wrote {OUT.relative_to(ROOT)}: {data['totals']['modules']} modules, {data['totals']['procedures']} procedures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
