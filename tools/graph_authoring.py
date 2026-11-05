#!/usr/bin/env python3
"""Author-friendly YAML front door for the four graphs (#1178).

`src/rules/four_graphs.py` implements the model and does no file I/O; it speaks
`noopunk.four_graphs` snapshots. Authors should not hand-write that JSON, so this tool converts
YAML to the same snapshot and validates it through the same code path:

    python3 tools/graph_authoring.py --check data/graphs/example.yaml
    python3 tools/graph_authoring.py --json  data/graphs/example.yaml
    python3 tools/graph_authoring.py --example        # print a starter file to stdout

The YAML is *not* a second format: `--json` emits exactly `FourGraphs.to_json()`, so an author can
diff the YAML against the canonical snapshot at any time.

Astral is not accepted — that layer is deferred until scripted Astral Projection lands (#1178).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules.four_graphs import FourGraphs, GraphContractError

#: Block style on purpose. A flow mapping (`{label: Home, Sörnäinen}`) splits on the comma inside the
#: label, which is the first trap an author hits when naming places.
EXAMPLE = """\
# Author-edited NoöPunk four graphs (#1178).
# Physical and Cyber nodes are PLACES. Actors OCCUPY them; an actor is never a node.
# Astral is deferred until scripted Astral Projection lands.
format: noopunk.four_graphs
version: 1

physical:
  graph_type: physical
  version: 1
  nodes:
    - id: loc.sornainen.home
      label: "Home, Sörnäinen"
      kind: location
    - id: loc.ratakatu.hq
      label: "Europol HQ, Ratakatu"
      kind: location
  edges:
    - source: loc.sornainen.home
      target: loc.ratakatu.hq
      id: route.home_hq
      directed: true
  positions:
    act.rookie: loc.ratakatu.hq

cyber:
  graph_type: cyber
  version: 1
  nodes:
    - id: cyber.hq.camera
      label: Lobby camera
      kind: device
      physical_ref: loc.ratakatu.hq
      device_actions: [watch, record]
  edges: []
  positions: {}

social:
  graph_type: social
  version: 1
  nodes:
    - id: act.rookie
      kind: character
      label: Rookie
    - id: act.wendt
      kind: character
      label: Laura Wendt
  edges:
    - source: act.rookie
      target: act.wendt
      score: 3
      kind: relationship
      directed: false

story:
  graph_type: story
  version: 1
  nodes:
    - id: scene.intake
      kind: scene
      label: Intake
      scene_types: [Social]
    - id: scene.records
      kind: scene
      label: Records search
      scene_types: [Cyber, Investigation]
      references: [loc.ratakatu.hq, cyber.hq.camera]
  edges:
    - source: scene.intake
      target: scene.records
      kind: transition
      all_flags: [flag.badge_issued]

avatars: {}
"""


def load(path: Path) -> FourGraphs:
    """Parse YAML and validate it through the same path as a JSON snapshot."""
    import yaml  # local import: the rules layer must not depend on a parser

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        raise GraphContractError(f"{path}: {error}") from None
    if not isinstance(data, dict):
        raise GraphContractError(f"{path}: expected a mapping at the top level")
    for required in ("format", "version", "physical", "cyber", "social", "story"):
        if required not in data:
            raise GraphContractError(f"{path}: missing '{required}'")
    return FourGraphs.from_dict(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, help="YAML graph file")
    parser.add_argument("--check", action="store_true", help="exit 1 if the file does not validate")
    parser.add_argument("--json", action="store_true", help="print the canonical snapshot")
    parser.add_argument("--example", action="store_true", help="print a starter YAML file")
    args = parser.parse_args(argv)

    if args.example:
        print(EXAMPLE, end="")
        return 0
    if not args.path:
        parser.error("give a YAML path, or --example")

    try:
        graphs = load(args.path)
    except (GraphContractError, OSError) as error:
        print(f"INVALID: {error}", file=sys.stderr)
        return 1

    if args.check:
        print(
            f"ok: {args.path} — "
            f"{len(graphs.physical.nodes)} physical, {len(graphs.cyber.nodes)} cyber, "
            f"{len(graphs.social.nodes)} social, {len(graphs.story.nodes)} story nodes"
        )
        return 0
    if args.json:
        print(graphs.to_json())
        return 0

    print(f"valid: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
