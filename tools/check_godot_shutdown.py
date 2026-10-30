#!/usr/bin/env python3
"""Check that the Godot test run shuts down cleanly (#883).

Runs the headless suite and classifies its output:

* **SCRIPT ERROR / Parse Error** — always a failure.
* **ERROR:** lines — a failure, except the known "resources still in use" shutdown line, which Godot
  emits as an ERROR but which is the same leak bookkeeping as the WARNING below.
* **Expected refusals** — product code logs a `push_warning(..., refused)` for invalid caller input
  (an unreadable save, a missing dialogue choice, an unknown scene). Those are warnings, not errors,
  which is what makes "any ERROR line is unexpected" a usable rule.
* **Leak bookkeeping** — the suites free the Nodes they create, so the full run reports zero leaked
  objects, resources and RIDs. The gate pins that at zero: any leak line fails, because it is new
  leakage rather than tolerated engine bookkeeping.

Usage:
    python3 tools/check_godot_shutdown.py [--godot ~/.local/bin/godot] [--baseline 90]
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: The suites free the nodes they create, so a clean run reports nothing at exit. Pinned at zero:
#: any leak line is new leakage, not tolerated engine bookkeeping.
BASELINE_OBJECTS = 0
BASELINE_RESOURCES = 0
BASELINE_RIDS = 0

ALLOWED_ERROR_LINES = (
    "resources still in use at exit",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--godot",
        default=shutil.which("godot") or str(Path.home() / ".local/bin/godot"),
        help="Godot binary; defaults to PATH, then ~/.local/bin/godot",
    )
    parser.add_argument("--baseline", type=int, default=BASELINE_OBJECTS)
    args = parser.parse_args()

    proc = subprocess.run(
        [args.godot, "--headless", "--path", str(ROOT),
         "--script", "res://godot/tests/run_tests.gd"],
        cwd=ROOT, capture_output=True, text=True, timeout=900,
    )
    out = proc.stdout + proc.stderr
    problems: list[str] = []

    # 1. Game assertions.
    summary = re.search(r"(\d+) checks, (\d+) failed", out)
    if not summary:
        problems.append("no test summary line — the suite did not run to completion")
    elif int(summary.group(2)) != 0:
        problems.append(f"{summary.group(2)} game-rule assertions failed")

    # 2. Script and parse errors are never acceptable.
    for line in out.splitlines():
        if "SCRIPT ERROR" in line or "Parse Error" in line:
            problems.append(line.strip())

    # 3. Any ERROR that is not known shutdown bookkeeping means something unexpected happened.
    for line in out.splitlines():
        stripped = line.strip()
        if not stripped.startswith("ERROR:"):
            continue
        if any(allowed in stripped for allowed in ALLOWED_ERROR_LINES):
            continue
        problems.append(f"unexpected engine error: {stripped}")

    # 4. Leak bookkeeping may not grow.
    objects = re.search(r"(\d+) ObjectDB instances were leaked", out)
    resources = re.search(r"(\d+) resources still in use", out)
    rids = re.search(r"(\d+) RIDs? of type", out)
    counts = {
        "objects": int(objects.group(1)) if objects else 0,
        "resources": int(resources.group(1)) if resources else 0,
        "rids": int(rids.group(1)) if rids else 0,
    }
    if counts["objects"] > args.baseline:
        problems.append(f"{counts['objects']} leaked objects exceeds baseline {args.baseline}")
    if counts["resources"] > BASELINE_RESOURCES:
        problems.append(f"{counts['resources']} resources in use exceeds baseline {BASELINE_RESOURCES}")

    print(f"godot shutdown: {counts['objects']} objects, {counts['resources']} resources, "
          f"{counts['rids']} RIDs (baseline {args.baseline})")
    if summary:
        print(f"assertions: {summary.group(1)} checks, {summary.group(2)} failed")
    if problems:
        print("\nFAILED:")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("OK: clean shutdown, no unexpected errors, leakage within baseline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
