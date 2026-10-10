#!/usr/bin/env python3
"""Remove documentation tests identified by tools/audit_test_scope.py (issue #271).

Removes test methods whose bodies assert on the content of a ``.md`` artefact, and deletes
files that consist of nothing else. Code tests are untouched. Every edit is validated by
re-parsing the module, and the caller must run the suite afterwards.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/mnt/workspace/NooPunk")
TESTS = ROOT / "tests"


def line_span(fn: ast.FunctionDef) -> tuple[int, int]:
    start = min([d.lineno for d in fn.decorator_list] + [fn.lineno])
    end = fn.end_lineno or fn.lineno
    return start, end


def main() -> int:
    data = json.loads(subprocess.run(
        ["python3", "tools/audit_test_scope.py", "--json"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout)

    removed_total = 0
    for entry in data["files"]:
        path = TESTS / entry["file"]
        doc = entry.get("documentation_methods") or []
        if not doc:
            continue
        if entry["verdict"] == "documentation-only":
            path.unlink()
            removed_total += len(doc)
            print(f"DELETED  {entry['file']} ({len(doc)} documentation tests, no code tests)")
            continue

        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        want = set(doc)
        spans = [line_span(n) for n in ast.walk(tree)
                 if isinstance(n, ast.FunctionDef) and n.name in want]
        # A name may occur in two classes, so the audit's name SET can be smaller than the
        # number of matching definitions; both belong to the same removal.
        assert len(spans) >= len(want), f"{entry['file']}: found {len(spans)} of {len(want)}"

        # A class whose every method is being removed would be left with an empty body, which is
        # a SyntaxError -- so drop the class whole instead of leaving a headless block.
        class_spans: list[tuple[int, int]] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
            if methods and all(m.name in want for m in methods) and all(
                    m.name.startswith("test_") for m in methods):
                class_spans.append(line_span(node))
        covered = set()
        for a, b in class_spans:
            covered.update(range(a, b + 1))
        spans = [s for s in spans if not any(s[0] in covered for s in [s])]
        lines = source.splitlines(keepends=True)
        drop: set[int] = set()
        for start, end in spans + class_spans:
            drop.update(range(start - 1, end))
        kept = [ln for i, ln in enumerate(lines) if i not in drop]
        new = "".join(kept)
        ast.parse(new)  # must still be valid Python
        path.write_text(new, encoding="utf-8")
        removed_total += len(spans)
        print(f"REMOVED  {entry['file']}: {len(spans)} documentation tests "
              f"({entry['total'] - len(spans)} code tests kept)")

    print(f"\ntotal documentation tests removed: {removed_total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
