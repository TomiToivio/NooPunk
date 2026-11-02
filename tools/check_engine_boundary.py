#!/usr/bin/env python3
"""Enforce the engine boundary: the rules and campaign layers must not import an engine (#1053/#1054).

#1054 declares that no front-end may be the source of truth for a rule, and #1053 makes that checkable.
Prose cannot hold that line — a stray ``import evennia`` in a helper turns the domain into an Evennia
package and the console slice dies. So this tool reads the two domain trees with ``ast`` (never
importing them) and fails on any import of a front-end, UI, database or model-serving framework.

The adapter layer is *expected* to import engines and is not scanned; that is the whole point of the
boundary.

    python3 tools/check_engine_boundary.py          # human-readable report
    python3 tools/check_engine_boundary.py --check   # exit 1 on any violation
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: Trees that must stay engine-free. `mud/nopunk_mud` is the application layer even though it lives
#: under `mud/`: it holds the campaign engine, world state and console, all of which run without Evennia.
DOMAIN_TREES = ("src/rules", "mud/nopunk_mud")

#: Packages that would couple a rule to a runtime, a UI, a database or a model provider. A rule module
#: may use the standard library and other rule modules, nothing else from the outside world.
FORBIDDEN = frozenset({
    "evennia", "twisted",           # MUD engine
    "pygame", "pyglet", "arcade",   # graphical front-ends
    "mesa", "gymnasium",            # agent simulation frameworks
    "streamlit", "dash", "flask", "fastapi", "django", "starlette",  # web/UI
    "sqlalchemy", "pymongo", "psycopg2", "redis",   # storage
    "openai", "anthropic", "ollama", "transformers", "torch",       # model/LLM providers
})


def _imported_roots(tree: ast.AST) -> set[str]:
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    return roots


def scan(root: Path = ROOT) -> list[dict]:
    violations: list[dict] = []
    for tree_name in DOMAIN_TREES:
        for path in sorted((root / tree_name).rglob("*.py")):
            try:
                module = ast.parse(path.read_text(encoding="utf-8"))
            except SyntaxError as exc:  # a broken file is a different failure; surface it plainly
                violations.append({"file": str(path.relative_to(root)), "import": "<syntax error>",
                                   "line": exc.lineno or 0})
                continue
            for node in ast.walk(module):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                    names = [node.module.split(".")[0]]
                for name in names:
                    if name in FORBIDDEN:
                        violations.append({"file": str(path.relative_to(root)), "import": name,
                                           "line": getattr(node, "lineno", 0)})
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="exit 1 on any violation")
    args = parser.parse_args(argv)

    violations = scan()
    if args.check:
        if violations:
            for item in violations:
                print(f"{item['file']}:{item['line']}: imports {item['import']}")
            print(f"\n{len(violations)} engine import(s) in the domain layer — move the code to an adapter.")
            return 1
        print("engine boundary intact: no front-end, storage or model import in the domain layer")
        return 0

    scanned = sum(len(list((ROOT / tree).rglob("*.py"))) for tree in DOMAIN_TREES)
    print(f"scanned {scanned} modules under {', '.join(DOMAIN_TREES)}")
    print(f"forbidden packages: {', '.join(sorted(FORBIDDEN))}")
    print(f"violations: {len(violations)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
