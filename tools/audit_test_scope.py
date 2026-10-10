#!/usr/bin/env python3
"""Classify NoöPunk test methods: executable-code tests vs documentation tests (issue #271).

Project policy: automated tests are for **executable game/software code only**. A test that
freezes rulebook/lore/design *text* is a documentation test and must go; a test of a rules
*implementation* is a code test and stays. The two are routinely mixed inside one file, so the
unit of classification here is the **test method**, not the file.

Heuristic, stated so it can be argued with:

* a method is a **documentation test** if its body asserts on the content of a ``.md`` artefact
  (a ``.md`` string literal, or a name bound to one in the module, e.g. ``CHAPTER``);
* otherwise it is a **code test** if the module imports anything from ``src``/``src.rules``/
  ``src.*`` (or a runtime module), or calls a name bound to such an import;
* otherwise it is **unknown** and reported for a human to read — never silently deleted.

Usage:
    python3 tools/audit_test_scope.py            # human-readable report
    python3 tools/audit_test_scope.py --json     # machine-readable, for CI or review
"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def module_bindings(tree: ast.Module) -> dict[str, object]:
    """Names bound to a ``.md`` path vs names bound to imported code."""
    md_names: set[str] = set()
    code_names: set[str] = set()
    imports_code = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("src") or mod in {"concordia_runtime"}:
                imports_code = True
                for a in node.names:
                    code_names.add(a.asname or a.name)
        elif isinstance(node, ast.Call):
            # sys.path.insert(0, str(ROOT / "src")) followed by a plain import is the repo's
            # dominant test style; without this the classifier calls half the suite "unknown".
            fn = node.func
            if isinstance(fn, ast.Attribute) and fn.attr == "insert":
                parts = [a.value for a in ast.walk(node) if isinstance(a, ast.Constant)
                         and isinstance(a.value, str)]
                if any(p.endswith("src") or p == "src" for p in parts):
                    imports_code = True
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.startswith("src") or a.name == "concordia_runtime":
                    imports_code = True
                    code_names.add(a.asname or a.name.split(".")[0])
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if not isinstance(tgt, ast.Name):
                    continue
                value = node.value
                if isinstance(value, ast.Constant) and isinstance(value.value, str) \
                        and value.value.endswith(".md"):
                    md_names.add(tgt.id)
                elif isinstance(value, ast.BinOp):  # e.g. ROOT / "docs" / "x.md"
                    parts = [n.value for n in ast.walk(value)
                             if isinstance(n, ast.Constant) and isinstance(n.value, str)]
                    if any(p.endswith(".md") for p in parts):
                        md_names.add(tgt.id)
    return {"md_names": md_names, "code_names": code_names, "imports_code": imports_code}


def classify_method(fn: ast.FunctionDef, bindings: dict) -> tuple[str, str]:
    body_src = ast.dump(fn)
    # 1) documentation: asserts on a .md artefact's content
    for name in bindings["md_names"]:
        if f"'{name}'" in body_src or f'"{name}"' in body_src or f"Name(id='{name}'" in body_src:
            return "documentation", f"asserts on the contents of a .md bound to {name}"
    for node in ast.walk(fn):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and ".md" in node.value:
            return "documentation", "references a .md path directly"
    # 2) code: exercises imported behaviour
    if bindings["imports_code"]:
        for name in bindings["code_names"]:
            if f"Name(id='{name}'" in body_src:
                return "code", f"exercises imported code ({name})"
        return "code", "module imports executable code and this test asserts on its behaviour"
    return "unknown", "no .md assertion and no code import found — read it before deciding"


def audit() -> dict:
    report: list[dict] = []
    for path in sorted(TESTS.glob("test_*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:  # pragma: no cover
            report.append({"file": path.name, "error": f"unparseable: {exc}"})
            continue
        bindings = module_bindings(tree)
        methods = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                kind, why = classify_method(node, bindings)
                methods.append({"name": node.name, "kind": kind, "why": why})
        doc = [m for m in methods if m["kind"] == "documentation"]
        code = [m for m in methods if m["kind"] == "code"]
        unknown = [m for m in methods if m["kind"] == "unknown"]
        verdict = (
            "documentation-only" if methods and not code and not unknown
            else "mixed" if doc and code
            else "code-only" if methods and not doc
            else "read-me"
        )
        report.append({
            "file": path.name,
            "verdict": verdict,
            "imports_code": bindings["imports_code"],
            "total": len(methods),
            "documentation": len(doc),
            "code": len(code),
            "unknown": len(unknown),
            "documentation_methods": [m["name"] for m in doc],
            "unknown_methods": [m["name"] for m in unknown],
        })
    return {"tests_dir": "tests", "files": report}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    data = audit()
    if args.json:
        print(json.dumps(data, indent=2))
        return 0
    total = doc = code = unknown = 0
    print(f"{'file':52s}{'verdict':20s}{'tot':>5}{'doc':>5}{'code':>6}{'?':>4}")
    for f in data["files"]:
        if "error" in f:
            print(f"{f['file']:52s}ERROR: {f['error']}")
            continue
        total += f["total"]; doc += f["documentation"]
        code += f["code"]; unknown += f["unknown"]
        print(f"{f['file']:52s}{f['verdict']:20s}{f['total']:>5}"
              f"{f['documentation']:>5}{f['code']:>6}{f['unknown']:>4}")
    print(f"{'TOTAL':52s}{'':20s}{total:>5}{doc:>5}{code:>6}{unknown:>4}")
    print()
    print("documentation-only files (candidates for removal):")
    for f in data["files"]:
        if f.get("verdict") == "documentation-only":
            print(f"  - {f['file']} ({f['documentation']} doc tests)")
    print("mixed files (remove the doc methods, keep the code ones):")
    for f in data["files"]:
        if f.get("verdict") == "mixed":
            print(f"  - {f['file']} ({f['documentation']} doc / {f['code']} code)")
    if unknown:
        print("files with unclassified methods (READ before deciding):")
        for f in data["files"]:
            if f.get("unknown"):
                print(f"  - {f['file']}: {f['unknown_methods'][:4]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
