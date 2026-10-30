#!/usr/bin/env python3
"""Run the headless Godot checks and classify every warning and error (#883).

Godot prints engine-level problems (leaked RIDs, leaked ObjectDB instances, resources still in use,
script errors) and the games' own negative-path diagnostics onto the same stream. Before this gate, a
leak was just another line in a green log; now it fails the build, while the diagnostics that tests
*deliberately* provoke are named and allowed.

Usage:

    GODOT=/path/to/godot python tools/godot_verify.py            # run everything
    python tools/godot_verify.py --log slice=/tmp/slice.log      # classify existing logs

Exit code 0 only when every command reported passing assertions AND nothing unexpected appeared.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Diagnostics the suite provokes on purpose, with the test that provokes them. Anything not on this
#: list is unexpected and fails the gate — that is the whole point of writing the list down.
EXPECTED_DIAGNOSTICS: tuple[tuple[str, str], ...] = (
    (r"NoopunkSceneFlow: unusable save data",
     "test_scene_flow: a corrupt save must be refused, not half-loaded"),
    (r"DialogueRunner: no choice \d+ at node \w+",
     "test_dialogue: an out-of-range choice must be refused"),
    (r"InvestigationAdapter: no scene \w+",
     "test_investigation_adapter: an unknown scene fails closed"),
    (r"Unknown clue id: [\w-]+",
     "test_case_state: an unknown clue must be rejected, not counted"),
)

#: Engine-level trouble. Each of these means the run is not clean, whatever the assertions said.
FAIL_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"RIDs? of type .* (?:was|were) leaked", "renderer RID leak"),
    (r"\d+ RID allocations? of type .* (?:was|were) leaked", "renderer allocation leak"),
    (r"ObjectDB instances were leaked", "object leak"),
    (r"resources still in use at exit", "resource leak"),
    (r"SCRIPT ERROR", "script error"),
    (r"Parse Error", "script parse error"),
    (r"non-equal opposite anchors", "layout warning (anchors fight size)"),
    (r"Failed to load script", "script failed to load"),
)

#: Each command must print its own success marker; a silent green is not evidence.
CHECKS: tuple[tuple[str, tuple[str, ...], tuple[str, ...]], ...] = (
    ("slice", ("--script", "res://godot/tests/run_tests.gd"), (r"\d+ checks, 0 failed",)),
    ("rules", ("--script", "res://tools/run_godot_tests.gd"), (r"0 failure\(s\)",)),
    ("ward", ("res://scenes/lakkahaltia/ward.tscn", "--quit-after", "30"), (r"WARD_READY",)),
    ("interaction", ("--script", "res://tools/ward_integration.gd"), (r"INTEGRATION_OK",)),
)


@dataclass
class Report:
    unexpected: list[tuple[str, str, str]] = field(default_factory=list)
    expected: list[tuple[str, str]] = field(default_factory=list)
    missing: list[tuple[str, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.unexpected and not self.missing


def classify(name: str, log: str) -> Report:
    """Split one command's log into expected diagnostics, unexpected trouble, and missing markers."""
    report = Report()
    for line in log.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        for pattern, reason in EXPECTED_DIAGNOSTICS:
            if re.search(pattern, stripped):
                report.expected.append((name, reason))
                break
        else:
            for pattern, reason in FAIL_PATTERNS:
                if re.search(pattern, stripped):
                    report.unexpected.append((name, reason, stripped))
                    break
            else:
                # An `ERROR:` nobody wrote down is still an error: silence is how noise becomes normal.
                # Engine *warnings* are treated more leniently, because the dummy renderer emits its own.
                if stripped.startswith("ERROR:"):
                    report.unexpected.append((name, "unclassified error", stripped))
    return report


def check_markers(name: str, log: str) -> list[tuple[str, str]]:
    """Every command must show its own success marker."""
    wanted = next((markers for key, _, markers in CHECKS if key == name), ())
    return [(name, marker) for marker in wanted if not re.search(marker, log)]


def run(name: str, godot: str) -> str:
    args = next(cmd for key, cmd, _ in CHECKS if key == name)
    command = [godot, "--headless", "--path", str(ROOT), *args]
    completed = subprocess.run(command, capture_output=True, text=True, cwd=ROOT, check=False)
    return completed.stdout + completed.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", action="append", default=[], metavar="NAME=PATH",
                        help="classify an existing log instead of running Godot")
    parser.add_argument("--godot", default=os.environ.get("GODOT", "godot"))
    options = parser.parse_args(argv)

    logs: dict[str, str] = {}
    if options.log:
        for item in options.log:
            name, _, path = item.partition("=")
            logs[name] = Path(path).read_text(errors="replace")
    else:
        for name, _, _ in CHECKS:
            logs[name] = run(name, options.godot)

    report = Report()
    for name, log in logs.items():
        part = classify(name, log)
        report.unexpected += part.unexpected
        report.expected += part.expected
        report.missing += check_markers(name, log)

    for name, reason in report.expected:
        print(f"expected  {name}: {reason}")
    for name, reason, line in report.unexpected:
        print(f"UNEXPECTED {name}: {reason} — {line}")
    for name, marker in report.missing:
        print(f"MISSING   {name}: no success marker matching {marker}")

    print(f"godot_verify: {len(report.expected)} expected diagnostic(s), "
          f"{len(report.unexpected)} unexpected, {len(report.missing)} missing marker(s)")
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
