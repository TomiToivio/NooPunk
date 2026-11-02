#!/usr/bin/env python3
"""The machine-readable half of the mod activation contract (#1080, ADR_1054).

`docs/architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md` says a mod declares its activation, its conflict
handling, its state home, its tests and its tabletop equivalent. Until now that sentence was prose: no
mod said any of it in a form a machine could read, so "each mod ships its own tests" and "the mod may
not claim to be playable without a printed procedure" were claims nobody checked.

This tool reads `data/mods/registry.json` and reports, per mod:

* whether every declared `implementation` path exists (a broken path is an error);
* whether a declared `tabletop_procedure` exists (a broken path is an error);
* whether a mod without one carries a `tabletop_gap` (a silent omission is an error);
* whether any test under `tests/` or `mud/tests/` names the module at all (a warning, not an error:
  some mods are exercised through the engine rather than by name, and a warning that fires wrongly is
  how a check gets deleted).

`--check` exits non-zero only for the structural errors. The gap report is the point of the exercise:
it turns "we should document tabletop procedures" into a count.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from src.rules.mod_boundary import BaselineViolation, validate_registry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data" / "mods" / "registry.json"
TEST_GLOBS = ("tests/test_*.py", "mud/tests/test_*.py")


def load(path: Path = REGISTRY) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_corpus() -> dict[str, str]:
    corpus: dict[str, str] = {}
    for pattern in TEST_GLOBS:
        for file in ROOT.glob(pattern):
            corpus[str(file.relative_to(ROOT))] = file.read_text(encoding="utf-8", errors="ignore")
    return corpus


def referenced_by_tests(mod: dict, corpus: dict[str, str]) -> list[str]:
    """A mod counts as tested when a test names one of its files or its id."""
    needles = {Path(p).stem for p in mod.get("implementation", [])}
    needles.add(mod["name"])
    hits = []
    for rel, text in corpus.items():
        if any(needle in text for needle in needles if len(needle) > 3):
            hits.append(rel)
    return sorted(hits)


def audit(data: dict, corpus: dict[str, str]) -> tuple[list[str], list[str], list[dict]]:
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[dict] = []

    if data.get("schema") != 3:
        errors.append("registry schema must be 3: hooks/state/dependencies/off_switch are mandatory")
    try:
        validate_registry(data.get("mods", []), root=str(ROOT))
    except (BaselineViolation, TypeError, ValueError) as exc:
        errors.append(str(exc))

    for mod in data.get("mods", []):
        name = mod.get("name", "<unnamed>")
        if "implementation" not in mod:
            errors.append(f"{name}: no implementation paths declared")
            paths = []
        else:
            paths = list(mod["implementation"])

        for rel in paths:
            if not (ROOT / rel).exists():
                errors.append(f"{name}: implementation path does not exist: {rel}")

        procedure = mod.get("tabletop_procedure")
        if procedure:
            if not (ROOT / procedure).exists():
                errors.append(f"{name}: tabletop procedure does not exist: {procedure}")
        elif not mod.get("tabletop_gap"):
            errors.append(f"{name}: no tabletop procedure and no recorded gap")

        tests = referenced_by_tests(mod, corpus)
        if not tests:
            warnings.append(f"{name}: no test names this mod")
        if not paths:
            warnings.append(f"{name}: documented but not implemented")

        rows.append({"name": name, "paths": len(paths), "tabletop": bool(procedure),
                     "tests": len(tests), "implemented": bool(paths)})
    return errors, warnings, rows


def render(rows: list[dict]) -> str:
    lines = ["mod                          impl  tabletop  tests", "-" * 52]
    for row in rows:
        lines.append(f"{row['name']:<28} {row['paths']:>4}  {'yes' if row['tabletop'] else 'no ':>8}"
                     f"  {row['tests']:>5}")
    with_procedure = sum(1 for r in rows if r["tabletop"])
    implemented = sum(1 for r in rows if r["implemented"])
    tested = sum(1 for r in rows if r["tests"])
    lines.append("")
    lines.append(f"{implemented}/{len(rows)} mods implemented · {with_procedure}/{len(rows)} have a printed "
                 f"procedure · {tested}/{len(rows)} are named by a test")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit non-zero on structural errors")
    parser.add_argument("--json", action="store_true", help="machine-readable rows")
    args = parser.parse_args(argv)

    errors, warnings, rows = audit(load(), test_corpus())
    print(render(rows) if not args.json else json.dumps(rows, indent=2))
    for warning in warnings:
        print(f"WARN {warning}", file=sys.stderr)
    for error in errors:
        print(f"FAIL {error}", file=sys.stderr)
    if args.check and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
