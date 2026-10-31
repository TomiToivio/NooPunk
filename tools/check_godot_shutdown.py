#!/usr/bin/env python3
"""Check that every headless Godot entry point shuts down cleanly (#883).

Runs each command CI relies on and classifies its output:

* **SCRIPT ERROR / Parse Error** — always a failure.
* **ERROR:** lines — a failure, except the known "resources still in use" shutdown line, which Godot
  emits as an ERROR but which is the same leak bookkeeping as the warnings below.
* **Expected refusals** — product code logs a `push_warning(..., refused)` for invalid caller input
  (an unreadable save, a missing dialogue choice, an unknown scene). Those are warnings, not errors,
  which is what makes "any ERROR line is unexpected" a usable rule.
* **Leak bookkeeping** — the suites free the Nodes they create, so a clean run reports zero leaked
  objects, resources and RIDs. The gate pins that at zero: any leak line fails, because it is new
  leakage rather than tolerated engine bookkeeping.
* **Success markers** — each command must print its own summary. A run that dies early prints no
  leak lines at all, and would otherwise look clean.

Usage:
    python3 tools/check_godot_shutdown.py [--godot ~/.local/bin/godot] [--baseline 90]
    python3 tools/check_godot_shutdown.py --only slice rules
    python3 tools/check_godot_shutdown.py --only slice --log /tmp/noopunk-slice.log
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
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

#: Every entry point the Godot CI job runs. Extending this list is how a new scene or suite gets the
#: same shutdown scrutiny as the main slice; before #883 only the first one was checked.
COMMANDS: tuple[tuple[str, tuple[str, ...], str], ...] = (
    ("slice", ("--script", "res://godot/tests/run_tests.gd"), r"\d+ checks, 0 failed"),
    ("rules", ("--script", "res://tools/run_godot_tests.gd"), r"0 failure\(s\)"),
    ("playthrough", ("res://godot/tests/playthrough.tscn", "--quit-after", "300"),
     r"\d+ checks, 0 failed"),
    ("ward", ("res://scenes/lakkahaltia/ward.tscn", "--quit-after", "30"), r"WARD_READY"),
    ("interaction", ("--script", "res://tools/ward_integration.gd"), r"INTEGRATION_OK"),
)


@dataclass
class Result:
    name: str
    counts: dict[str, int] = field(default_factory=lambda: {"objects": 0, "resources": 0, "rids": 0})
    summary: str = ""
    problems: list[str] = field(default_factory=list)


def check(name: str, out: str, marker: str, baseline: int) -> Result:
    result = Result(name)

    summary = re.search(marker, out)
    if not summary:
        result.problems.append(f"no success marker matching {marker!r} — the command did not finish")
    else:
        result.summary = summary.group(0)

    for line in out.splitlines():
        stripped = line.strip()
        if "SCRIPT ERROR" in stripped or "Parse Error" in stripped:
            result.problems.append(stripped)
        elif stripped.startswith("ERROR:") and not any(
                allowed in stripped for allowed in ALLOWED_ERROR_LINES):
            result.problems.append(f"unexpected engine error: {stripped}")

    objects = re.search(r"(\d+) ObjectDB instances were leaked", out)
    resources = re.search(r"(\d+) resources still in use", out)
    rids = re.search(r"(\d+) RIDs? of type", out)
    result.counts = {
        "objects": int(objects.group(1)) if objects else 0,
        "resources": int(resources.group(1)) if resources else 0,
        "rids": int(rids.group(1)) if rids else 0,
    }
    if result.counts["objects"] > baseline:
        result.problems.append(f"{result.counts['objects']} leaked objects exceeds baseline {baseline}")
    if result.counts["resources"] > BASELINE_RESOURCES:
        result.problems.append(
            f"{result.counts['resources']} resources in use exceeds baseline {BASELINE_RESOURCES}")
    if result.counts["rids"] > BASELINE_RIDS:
        result.problems.append(f"{result.counts['rids']} leaked RIDs exceeds baseline {BASELINE_RIDS}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--godot",
        default=shutil.which("godot") or str(Path.home() / ".local/bin/godot"),
        help="Godot binary; defaults to PATH, then ~/.local/bin/godot",
    )
    parser.add_argument("--baseline", type=int, default=BASELINE_OBJECTS)
    parser.add_argument("--only", nargs="+", metavar="NAME",
                       help="run just these commands (slice, rules, playthrough, ward, interaction)")
    parser.add_argument("--log", type=Path,
                       help="read an already-captured Godot log instead of running the command again")
    args = parser.parse_args()

    wanted = [entry for entry in COMMANDS if not args.only or entry[0] in args.only]
    if not wanted:
        print(f"no such command; choose from {[entry[0] for entry in COMMANDS]}")
        return 2

    if args.log is not None and len(wanted) != 1:
        print("--log needs exactly one command: pass --only NAME")
        return 2

    results: list[Result] = []
    for name, argv, marker in wanted:
        if args.log is not None:
            out = args.log.read_text(encoding="utf-8", errors="replace")
        else:
            proc = subprocess.run([args.godot, "--headless", "--path", str(ROOT), *argv],
                                  cwd=ROOT, capture_output=True, text=True, timeout=900)
            out = proc.stdout + proc.stderr
        results.append(check(name, out, marker, args.baseline))

    failures = 0
    for result in results:
        print(f"{result.name}: {result.counts['objects']} objects, {result.counts['resources']} "
              f"resources, {result.counts['rids']} RIDs ({result.summary or 'no summary'})")
        for problem in result.problems:
            print(f"  - {problem}")
        failures += 1 if result.problems else 0

    if failures:
        print(f"\nFAILED: {failures} of {len(results)} command(s) not clean")
        return 1
    print(f"OK: clean shutdown, no unexpected errors, leakage within baseline "
          f"({len(results)} command(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
