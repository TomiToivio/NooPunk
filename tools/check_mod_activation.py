#!/usr/bin/env python3
"""Report the mod activation contract (#1091, ADR_1054 §2) and fail when it is not met.

The contract itself is enforced by `src/rules/mod_boundary.py::validate_registry` — one validator, not
two, because a second copy of a rule is how the first one stops being true. This tool is the reporting
half: it prints what each mod declares, counts the mods that still have no printed procedure, and warns
when no test names a mod at all.

Exit codes: 0 when every mod satisfies the contract, 1 when one does not. A missing tabletop procedure
is not an error — a missing *statement* about it is.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "mods" / "registry.json"
TEST_GLOBS = ("tests/test_*.py", "mud/tests/test_*.py")

sys.path.insert(0, str(ROOT / "src"))
from rules.mod_boundary import BaselineViolation, validate_registry  # noqa: E402


def load(path: Path = REGISTRY) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_corpus() -> dict[str, str]:
    corpus: dict[str, str] = {}
    for pattern in TEST_GLOBS:
        for file in sorted(ROOT.glob(pattern)):
            corpus[str(file.relative_to(ROOT))] = file.read_text(encoding="utf-8", errors="ignore")
    return corpus


def referenced_by_tests(mod: dict, corpus: dict[str, str]) -> list[str]:
    needles = {Path(p).stem for p in mod.get("implementation", [])}
    needles.add(mod["name"])
    return sorted(rel for rel, text in corpus.items()
                  if any(n in text for n in needles if len(n) > 3))


def rows(data: dict, corpus: dict[str, str]) -> list[dict]:
    out = []
    for mod in data.get("mods", []):
        switch = mod.get("off_switch") or {}
        out.append({
            "name": mod["name"],
            "status": mod.get("status"),
            "hooks": len(mod.get("hooks") or ()),
            "state": len(mod.get("state") or ()),
            "off_switch": switch.get("kind"),
            "tabletop": bool(mod.get("tabletop_procedure")),
            "gap": mod.get("tabletop_gap"),
            "tests": len(referenced_by_tests(mod, corpus)),
        })
    return out


def render(table: list[dict]) -> str:
    lines = ["mod                          status        hooks state off-switch  tabletop tests",
             "-" * 82]
    for r in table:
        lines.append(f"{r['name']:<28} {r['status']:<13} {r['hooks']:>5} {r['state']:>5} "
                     f"{r['off_switch']:<11} {'yes' if r['tabletop'] else 'gap':>8} {r['tests']:>5}")
    implemented = sum(1 for r in table if r["status"] == "implemented")
    with_procedure = sum(1 for r in table if r["tabletop"])
    tested = sum(1 for r in table if r["tests"])
    lines += ["",
              f"{implemented}/{len(table)} implemented · {with_procedure}/{len(table)} have a printed "
              f"procedure · {tested}/{len(table)} are named by a test"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit non-zero on a contract violation")
    parser.add_argument("--json", action="store_true", help="machine-readable rows")
    args = parser.parse_args(argv)

    data = load()
    table = rows(data, test_corpus())

    try:
        validate_registry(data["mods"], root=ROOT)
    except BaselineViolation as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        if args.check:
            return 1
    else:
        for row in table:
            if row["status"] == "implemented" and not row["tests"]:
                print(f"WARN {row['name']}: no test names this mod", file=sys.stderr)
            if row["gap"]:
                print(f"GAP  {row['name']}: {row['gap']}", file=sys.stderr)

    print(json.dumps(table, indent=2) if args.json else render(table))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
