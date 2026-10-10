#!/usr/bin/env python3
"""Generate docs/sources/ATTRIBUTION.md from the two rights ledgers (issue #231).

The attribution document is generated rather than hand-written for one reason: a licence
obligation that lives only in prose is a licence obligation that rots. CC BY 3.0 and CC BY-SA
both require attribution as a CONDITION of the grant, so the sources that owe it are derived
from data/sources/game_system_rights.json, and a guard fails if any of them is missing from
the generated text.

Usage:
    python3 tools/issue231_attribution.py            # write docs/sources/ATTRIBUTION.md
    python3 tools/issue231_attribution.py --check    # fail if the file is out of date
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "sources" / "game_system_rights.json"
COMPONENTS = ROOT / "data" / "sources" / "component_rights.json"
OUT = ROOT / "docs" / "sources" / "ATTRIBUTION.md"

#: Decisions whose licence REQUIRES attribution as a condition of the grant.
ATTRIBUTION_OBLIGATIONS = {
    "verified-permissive": True,       # CC BY / CC BY-SA: attribution is a condition
    "verified-nc-sharealike": None,    # NOT shippable: nothing is owed while it is unused
    "verified-public-domain": False,   # CC0: no obligation, credited as courtesy
    "blocked-unverified": None,        # unknown grant: not shippable, nothing owed yet
    "no-cc-grant-established": None,   # no grant: not shippable
    "proprietary-out-of-scope": None,  # not shippable
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def notice(source: dict) -> str:
    """The attribution string, or the source name when the ledger has no grant to quote."""
    return (source.get("attribution") or "").strip() or f"{source['source']} — terms not established"


def owing(sources: dict) -> list[dict]:
    return [s for s in sources["sources"]
            if ATTRIBUTION_OBLIGATIONS.get(s["decision"]) is True]


def courtesy(sources: dict) -> list[dict]:
    return [s for s in sources["sources"]
            if ATTRIBUTION_OBLIGATIONS.get(s["decision"]) is False]


def render() -> str:
    sources, components = load(SOURCES), load(COMPONENTS)
    target = components["target_license"]
    lines = [
        "# Attribution and notices",
        "",
        "**Status: generated. Do not edit by hand.**",
        "",
        "Parent epic [#200](https://github.com/TomiToivio/NooPunk/issues/200); work package",
        "[#231](https://github.com/TomiToivio/NooPunk/issues/231). Regenerate with",
        "`python3 tools/issue231_attribution.py`; a guard fails if this file is out of date.",
        "",
        "## Licence of this work",
        "",
        f"**Not yet chosen.** {target['$comment']}",
        "",
        "| Component class | Candidate |",
        "| --- | --- |",
        f"| Rulebook and original setting | {target['recommended']} (recommended) |",
        f"| Source code | {target['code_license']} |",
        "",
        "Until the choice lands, nothing in the repository may be redistributed as if licensed.",
        "",
        "## Required attributions",
        "",
        "These grants are conditional on attribution, so the notices below are obligations rather",
        "than courtesies. They are derived from `data/sources/game_system_rights.json`.",
        "",
        "| Work | Licence | Notice |",
        "| --- | --- | --- |",
    ]
    for source in owing(sources):
        lines.append(f"| {source['source']} | {source['license']} | {notice(source)} |")
    lines += [
        "",
        "## Courtesies",
        "",
        "Public-domain or licence-free material, credited because it deserves to be.",
        "",
        "| Work | Licence | Notice |",
        "| --- | --- | --- |",
    ]
    for source in courtesy(sources):
        lines.append(f"| {source['source']} | {source['license']} | {notice(source)} |")
    lines += [
        "",
        "## Shipped components",
        "",
        "What this repository ships, and what each part owes.",
        "",
        "| Component | Kind | Licence | Attribution | Third-party inputs |",
        "| --- | --- | --- | --- | --- |",
    ]
    for component in components["components"]:
        inputs = ", ".join(component["third_party_inputs"]) or "—"
        lines.append(
            f"| `{component['id']}` | {component['kind']} | {component['license']} | "
            f"{'yes' if component['attribution_required'] else 'no'} | {inputs} |"
        )
    lines += [
        "",
        "## Not shippable as inputs",
        "",
        f"{components['not_shipped']['why']}",
        "",
        "`" + "`, `".join(components["not_shipped"]["excluded_sources"]) + "`",
        "",
        "## Open items",
        "",
    ]
    lines += [f"- {item}" for item in components["open_items"]]
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("ATTRIBUTION.md is out of date; run without --check", file=sys.stderr)
            return 1
        print("ATTRIBUTION.md is current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
