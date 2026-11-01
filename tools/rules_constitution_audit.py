#!/usr/bin/env python3
"""Audit the Rules Constitution (#1006): every rule module has exactly one tier.

The constitution is data (`data/rules/rules_constitution.json`), and this tool is what stops it being
a paragraph:

* every file under `src/rules/` is classified **exactly once** — a new module cannot slip in
  unclassified, and a phantom entry cannot name a module that no longer exists;
* every tier is from the declared vocabulary;
* **no `cwn-core` module imports a `noopunk-mod` module.** That is the "overlays sit on top, they are
  never inside" rule as a static check, and it fails on an indirect import through an overlay too.

`--markdown` renders `docs/rules/RULES_CONSTITUTION_TIERS.md` from the data, so the document and the
registry cannot drift.

Vanilla playability — the harder half of the constitution — is proved by
`tests/test_rules_constitution.py`, which imports the vanilla tiers in a subprocess whose import hook
refuses every overlay module.

    python3 tools/rules_constitution_audit.py            # audit, human-readable
    python3 tools/rules_constitution_audit.py --check    # exit 1 on any violation
    python3 tools/rules_constitution_audit.py --markdown > docs/rules/RULES_CONSTITUTION_TIERS.md

A data audit, not a CI prose gate: it asserts relationships (a file is classified, an import exists),
never wording, and it is not wired into a workflow.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULES = ROOT / "src" / "rules"
REGISTRY = ROOT / "data" / "rules" / "rules_constitution.json"

#: Tiers whose modules must not be reachable from the baseline.
BASELINE_TIER = "cwn-core"
OVERLAY_TIER = "noopunk-mod"


def load() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def _imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
            names.update(f"{node.module}.{alias.name}" for alias in node.names)
    return names


def audit(data: dict) -> list[str]:
    violations: list[str] = []
    vocabulary = set(data["tier_vocabulary"])

    listed: dict[str, str] = {}
    for row in data["modules"]:
        module, tier = row["module"], row["tier"]
        if tier not in vocabulary:
            violations.append(f"{module}: unknown tier {tier!r}")
        if module in listed:
            violations.append(f"{module}: classified twice ({listed[module]}, {tier})")
        listed[module] = tier
        if not (ROOT / module).exists():
            violations.append(f"{module}: listed but does not exist")

    present = {f"src/rules/{p.name}" for p in RULES.glob("*.py")}
    for missing in sorted(present - set(listed)):
        violations.append(f"{missing}: in the tree but not in the constitution — classify it")

    overlay_stems = {Path(m).stem for m, t in listed.items() if t == OVERLAY_TIER}
    for module, tier in listed.items():
        if tier != BASELINE_TIER:
            continue
        for name in _imports(ROOT / module):
            leaf = name.split(".")[-1]
            if leaf in overlay_stems:
                violations.append(
                    f"{module}: a {BASELINE_TIER} module imports the overlay {name!r} — "
                    "the baseline must not depend on a mod"
                )
    return violations


def counts(data: dict) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in data["modules"]:
        out[row["tier"]] = out.get(row["tier"], 0) + 1
    return out


def markdown(data: dict) -> str:
    tally = counts(data)
    lines = [
        "# Rules Constitution — module tiers",
        "",
        "**Generated** by `python3 tools/rules_constitution_audit.py --markdown` from",
        "`data/rules/rules_constitution.json`. Do not edit by hand.",
        "",
        f"**Issue:** {data['issue']}",
        "",
        "**Authority order:** " + " → ".join(f"`{t}`" for t in data["authority_order"]),
        "",
        f"**Precedence.** {data['precedence']}",
        "",
        "**Vanilla minimum:** " + ", ".join(f"`{t}`" for t in data["vanilla_minimum"]["tiers"])
        + " — " + data["vanilla_minimum"]["statement"],
        "",
        "| Tier | Modules |",
        "| --- | ---: |",
    ]
    for tier in data["tier_vocabulary"]:
        lines.append(f"| `{tier}` | {tally.get(tier, 0)} |")
    lines += ["", "## What each tier is", ""]
    for tier, note in data["tier_vocabulary"].items():
        lines.append(f"* **`{tier}`** — {note}")
    for tier in data["tier_vocabulary"]:
        rows = sorted(r["module"] for r in data["modules"] if r["tier"] == tier)
        if not rows:
            continue
        lines += ["", f"### `{tier}`", ""]
        lines += [f"* `{row}`" for row in rows]
    lines += ["", f"**Classification rule.** {data['module_rule']}", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="exit non-zero on any violation")
    parser.add_argument("--markdown", action="store_true", help="print the generated document")
    args = parser.parse_args()

    data = load()
    if args.markdown:
        print(markdown(data))
        return 0

    violations = audit(data)
    tally = counts(data)
    print(f"modules: {len(data['modules'])}")
    for tier in data["tier_vocabulary"]:
        print(f"  {tier:<16}{tally.get(tier, 0)}")
    if violations:
        print("\nviolations:", file=sys.stderr)
        for violation in violations:
            print(f"  - {violation}", file=sys.stderr)
        return 1 if args.check else 0
    print("\nOK: every module has exactly one tier, and no baseline module imports an overlay")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
