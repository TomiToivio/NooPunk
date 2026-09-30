#!/usr/bin/env python3
"""Smoke-check the NoöPunk Concordia scaffold.

By default this validates only the NoöPunk runtime objects and does not contact
Ollama. Pass --build-concordia-config to also import Concordia and translate the
placeholder session into its current prefab configuration.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from concordia_runtime import GameMasterSpec, LLMAgentSpec, SessionSpec
from concordia_runtime.session import build_concordia_config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--build-concordia-config",
        action="store_true",
        help="Also import Concordia and build its prefab Config.",
    )
    args = parser.parse_args()

    spec = SessionSpec(
        gm=GameMasterSpec(name="placeholder_gm"),
        llm_agents=(LLMAgentSpec(name="placeholder_actor"),),
        premise="placeholder_premise",
        max_steps=1,
    )

    print("NoöPunk Concordia session scaffold: OK")
    print(f"GM: {spec.gm.name}")
    print(f"LLM agents: {len(spec.llm_agents)}")
    print("Human player: optional / not attached")

    if args.build_concordia_config:
        config = build_concordia_config(spec)
        print(f"Concordia prefab config: OK ({type(config).__name__})")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
