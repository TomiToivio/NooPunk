#!/usr/bin/env python3
"""Audit the module half of the Rules Constitution (#1006).

`docs/rules/RULES_CONSTITUTION.md` and `data/rules/rules_constitution.json` state *which sources* the
game runs on. `data/rules/overlay_registry.json` states which layers are backed by code.

This tool checks the third question, the one neither of those can answer: **is every rule module
classified, and does the baseline depend on a mod?** It reads `module_tiers` from the constitution:

* every file under `src/rules/` is classified **exactly once** — a new module cannot slip in
  unclassified, and a phantom entry cannot name a module that no longer exists;
* every tier is from the declared vocabulary;
* **no `cwn-core` module imports a `noopunk-mod` module** — "overlays sit on top, never inside" as a
  static check, which also catches an indirect import through an overlay.

`--markdown` renders `docs/rules/RULES_CONSTITUTION_TIERS.md` from the data, so document and registry
cannot drift.

The harder half — *vanilla still runs with every overlay blocked* — is proved by
`tests/test_rules_constitution_modules.py` in a subprocess whose import hook refuses each overlay.

    python3 tools/rules_constitution_audit.py            # audit, human-readable
    python3 tools/rules_constitution_audit.py --check    # exit 1 on any violation
    python3 tools/rules_constitution_audit.py --markdown > docs/rules/RULES_CONSTITUTION_TIERS.md

A data audit, not a CI prose gate: it asserts relationships (a file is classified, an import exists),
never wording.
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


def load() -> dict:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if "module_tiers" not in data:
        raise SystemExit(f"{REGISTRY}: no 'module_tiers' block — the module audit has nothing to read")
    return data


def tiers(data: dict) -> dict:
    return data["module_tiers"]


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
    block = tiers(data)
    violations: list[str] = []
    vocabulary = set(block["tier_vocabulary"])
    baseline_tier, overlay_tier = block["baseline"], block["overlay"]

    listed: dict[str, str] = {}
    for row in block["modules"]:
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

    overlay_stems = {Path(m).stem for m, t in listed.items() if t == overlay_tier}
    for module, tier in listed.items():
        if tier != baseline_tier:
            continue
        for name in _imports(ROOT / module):
            if name.split(".")[-1] in overlay_stems:
                violations.append(
                    f"{module}: a {baseline_tier} module imports the overlay {name!r} — "
                    "the baseline must not depend on a mod"
                )
    return violations


def counts(data: dict) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in tiers(data)["modules"]:
        out[row["tier"]] = out.get(row["tier"], 0) + 1
    return out


def markdown(data: dict) -> str:
    block = tiers(data)
    tally = counts(data)
    lines = [
        "# Rules Constitution — module tiers",
        "",
        "**Generated** by `python3 tools/rules_constitution_audit.py --markdown` from the",
        "`module_tiers` block of `data/rules/rules_constitution.json`. Do not edit by hand.",
        "",
        f"**Issue:** {data['issue']} · **Sources and precedence:** `docs/rules/RULES_CONSTITUTION.md`",
        "",
        "**Precedence:** " + " → ".join(f"`{s}`" for s in data["precedence"]),
        "",
        "**Minimum playable:** " + " + ".join(f"`{s}`" for s in data["minimum_playable"])
        + " — which in module terms is " + " + ".join(f"`{t}`" for t in block["vanilla_minimum"])
        + ". `tests/test_rules_constitution_modules.py` proves it by running the baseline with every",
        "`noopunk-mod` module refused by an import hook.",
        "",
        "| Tier | Modules |",
        "| --- | ---: |",
    ]
    for tier in block["tier_vocabulary"]:
        lines.append(f"| `{tier}` | {tally.get(tier, 0)} |")
    lines += ["", "## What each tier is", ""]
    for tier, note in block["tier_vocabulary"].items():
        lines.append(f"* **`{tier}`** — {note}")
    for tier in block["tier_vocabulary"]:
        rows = sorted(r["module"] for r in block["modules"] if r["tier"] == tier)
        if not rows:
            continue
        lines += ["", f"### `{tier}`", ""]
        lines += [f"* `{row}`" for row in rows]
    lines += ["", "**Maintenance rule.** A new module under `src/rules/` must be classified here in the",
              "same commit. An unclassified module is a rule nobody has agreed to.", ""]
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
    print(f"modules: {len(tiers(data)['modules'])}")
    for tier in tiers(data)["tier_vocabulary"]:
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
