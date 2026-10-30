#!/usr/bin/env python3
"""Fail when one CWN rule is implemented in more than one Godot module.

Two parallel agent sessions built the same rules in `godot/core/` and `src/godot/`, each with its
own tests, and nothing failed — the repository simply grew two answers to every question. This guard
makes the rule in `docs/godot/UNIFIED_IMPLEMENTATION.md` executable instead of aspirational.

It compares *domains*, not filenames: `cwn_combat_rules.gd` and `cwn_combat.gd` are the same domain,
as are `psionics.gd` and `swn_psionics.gd`. A domain implemented in two trees fails the check unless
it is listed in `ALLOWED` — the migration backlog. That list may only shrink: adding to it re-opens
exactly the drift this exists to stop.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Rules trees that must not both implement a domain. Application and campaign modules
#: (`campaign_state`, `title`, `case_state`, scenes, UI) are not rules and are exempt.
TREES = {
    "rules": ROOT / "godot" / "core",
    "rules_alt": ROOT / "src" / "godot" / "cwn",
    "app_alt": ROOT / "src" / "godot",
}

#: Campaign, presentation and state files are not rules; they are allowed to live beside the
#: application without being a second implementation of a rule.
EXEMPT = {
    "campaign_state", "campaign_screen", "title", "case_state", "lakkahaltia_case",
    "network_map", "core", "cwn_progression", "cwn_attack_context", "cwn_combat_effects",
    "cwn_combat_round", "cwn_rules", "wn",
}

#: Known duplicates, oldest first. Each row names the domain and the file that is being merged away.
#: Delete a row when its migration step in UNIFIED_IMPLEMENTATION.md lands.
ALLOWED = {
    "cwn:catalogue",  # godot/core/cwn_catalogue.gd  <- src/godot/cwn/cwn_catalogue.gd
    "cwn:character",  # godot/core/cwn_character.gd  <- src/godot/cwn/cwn_character.gd
    "cwn:combat",     # godot/core/cwn_combat_rules.gd <- src/godot/cwn/cwn_combat.gd
    # "strain" retired in #791: src/godot/cwn/cwn_strain.gd was merged into godot/core/cwn_strain.gd
    # and deleted. The guard now fails if the domain reappears, which is the intent.
    # "healing" retired in #791: src/godot/cwn/cwn_healing.gd merged into godot/core/cwn_healing.gd
    # (rounds_until_death, remove_frailty and first_aid came with it) and deleted.
    # "psionics" retired in #791: src/godot/swn_psionics.gd was merged into godot/core/psionics.gd
    # (its two core-technique statics came with it) and deleted.
}

#: A domain is the file stem with the system prefix and a trailing "_rules" removed, so
#: `cwn_combat_rules` and `cwn_combat` collide on purpose.
#: The system prefix is part of the domain: `cwn_progression` (character advancement) and
#: `swn_progression` (psychic training) are not the same rule, and the guard must not report them as
#: a duplicate pair. The same prefix on both sides still collides, which is the case it exists for.
PREFIX = re.compile(r"^(cwn|swn|noopunk|wn)_")
SYSTEM = re.compile(r"^(cwn|swn|noopunk|wn)")
SUFFIX = re.compile(r"_(rules|procedures)$")


def domain_of(path: Path) -> str:
    """`<system>:<rule>` — the system prefix stays, because CWN and SWN are different rules."""
    stem = path.stem.lower()
    system = SYSTEM.match(stem)
    prefix = system.group(1) if system else "noopunk"
    stem = PREFIX.sub("", stem)
    stem = SUFFIX.sub("", stem)
    return f"{prefix}:{stem}"


def scan() -> dict[str, list[str]]:
    found: dict[str, list[str]] = defaultdict(list)
    for label, directory in TREES.items():
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.gd")):
            domain = domain_of(path)
            if domain in EXEMPT:
                continue
            found[domain].append(f"{label}:{path.relative_to(ROOT).as_posix()}")
    return {domain: files for domain, files in found.items() if len({f.split(':')[0] for f in files}) > 1}


def main() -> int:
    duplicated = scan()
    new = sorted(set(duplicated) - ALLOWED)

    if duplicated:
        print("rule domains implemented in more than one tree:")
        for domain in sorted(duplicated):
            mark = "new" if domain in new else "known"
            print(f"  [{mark}] {domain}")
            for f in duplicated[domain]:
                print(f"        {f}")

    if new:
        print(
            "\nFAIL: new duplicate rule implementation(s): "
            + ", ".join(new)
            + "\nAdd the rule to the single tree named in docs/godot/UNIFIED_IMPLEMENTATION.md,"
            " or delete the duplicate. Do not add to ALLOWED.",
            file=sys.stderr,
        )
        return 1

    stale = sorted(ALLOWED - set(duplicated))
    if stale:
        print("\nNOTE: these allowlist rows are now migrated and should be deleted: " + ", ".join(stale))
    print(f"\nOK: {len(duplicated)} known duplicate domain(s), no new ones.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
