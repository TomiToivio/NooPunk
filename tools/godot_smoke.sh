#!/usr/bin/env bash
# Headless verification for the Godot slice (issue #631).
#
#   GODOT=/path/to/godot tools/godot_smoke.sh
#
# 1. imports the project and rebuilds the global class cache,
# 2. runs the gameplay-logic tests (tests/godot),
# 3. loads the ward scene headless and proves it built (WARD_READY marker),
#    failing on any SCRIPT ERROR.
#
# The dummy renderer prints mesh warnings for primitive meshes under --headless; they are
# renderer noise, not script failures, and are not treated as errors here.
set -uo pipefail

GODOT="${GODOT:-godot}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

if ! command -v "$GODOT" >/dev/null 2>&1; then
  echo "godot binary not found (set GODOT=/path/to/godot)" >&2
  exit 2
fi

echo "== import =="
"$GODOT" --headless --path . --editor --quit 2>&1 | tail -2 || exit 1

echo "== gameplay tests =="
"$GODOT" --headless --path . --script res://tools/run_godot_tests.gd || exit 1

echo "== ward scene smoke =="
output="$("$GODOT" --headless --path . res://scenes/lakkahaltia/ward.tscn --quit-after 30 2>&1)"
status=$?
if [ $status -ne 0 ]; then
  echo "$output" >&2
  exit $status
fi
if printf '%s' "$output" | grep -q "SCRIPT ERROR"; then
  echo "$output" >&2
  echo "scene loaded with script errors" >&2
  exit 1
fi
if ! printf '%s' "$output" | grep -q "WARD_READY"; then
  echo "$output" >&2
  echo "the ward scene did not report WARD_READY" >&2
  exit 1
fi
echo "ok: $(printf '%s' "$output" | grep -o 'WARD_READY.*' | head -1)"

echo "== interaction smoke =="
"$GODOT" --headless --path . --script res://tools/ward_integration.gd || exit 1
