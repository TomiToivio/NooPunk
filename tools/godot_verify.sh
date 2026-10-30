#!/usr/bin/env bash
# Godot verification with an explicit error policy (issue #883).
#
#   tools/godot_verify.sh            # full run
#   GODOT=/path/to/godot tools/godot_verify.sh
#
# The problem this solves: the suite deliberately exercises negative paths - an unusable save, a
# dialogue choice that does not exist, a scene id that is not there - so it prints ERROR lines on
# purpose. Because those are indistinguishable from real failures in the raw log, everyone learns to
# skim past ERROR output, which is how a genuine engine error survives for weeks.
#
# This script classifies every diagnostic line into one of three buckets:
#
#   expected   - the negative-path diagnostics the tests are supposed to produce (allowlisted below)
#   noise      - known engine shutdown chatter (leaked RIDs/ObjectDB at exit, renderer dummy warnings)
#   unexpected - anything else. These fail the run.
#
# Allowlisting is deliberate and narrow: each pattern names who produces it and why it is expected. A
# new pattern requires a reason in this file, so silence has to be justified rather than discovered.

set -uo pipefail

GODOT="${GODOT:-godot}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

command -v "$GODOT" >/dev/null 2>&1 || { echo "godot binary not found (set GODOT=...)" >&2; exit 2; }

LOG="$(mktemp "${TMPDIR:-/tmp}/godot_verify.XXXXXX.log")"
trap 'rm -f "$LOG"' EXIT

# Diagnostics the suite produces on purpose, each tied to the test that provokes it.
EXPECTED='NoopunkSceneFlow: unusable save data|DialogueRunner: no choice|InvestigationAdapter: no scene|Unknown clue id|CwnWages: unknown role|CwnDrugs: unknown drug|CwnLifestyles: unknown lifestyle'

# Engine shutdown / renderer chatter that is not a rule or script failure.
NOISE='RID allocation|RIDs of type|ObjectDB instances were leaked|resources still in use at exit|at: clear \(core/io/resource|at: cleanup \(core/object|dummy renderer|DummyTexture|ShapedTextDataAdvanced|FontAdvanced|RichTextLabel4Item|CanvasItem.*leaked|Detected another project.godot|Godot Engine v[0-9]'

run() {
	local label="$1"; shift
	echo "== $label =="
	{ "$@" 2>&1 || true; } | tee -a "$LOG"
	echo
}

run "import" "$GODOT" --headless --path . --import
run "unit and procedure suite" "$GODOT" --headless --path . --script res://godot/tests/run_tests.gd
run "assembled playthrough" "$GODOT" --headless --path . res://godot/tests/playthrough.tscn --quit-after 300
run "integration playthrough" "$GODOT" --headless --path . --script res://godot/tests/integration_playthrough.gd

echo "================ classification ================"

UNEXPECTED="$(grep -E 'ERROR|SCRIPT ERROR|Parse Error' "$LOG" 2>/dev/null \
	| grep -vEi "$EXPECTED" | grep -vEi "$NOISE" || true)"

LEAKS="$(grep -Ei 'leaked|resources still in use' "$LOG" | grep -viE 'Godot Engine' || true)"
EXPECTED_HITS="$(grep -Ei "$EXPECTED" "$LOG" || true)"

if [ -n "$EXPECTED_HITS" ]; then
	echo "expected negative-path diagnostics: $(printf '%s\n' "$EXPECTED_HITS" | wc -l | tr -d ' ') line(s) (allowlisted)"
fi

if [ -n "$LEAKS" ]; then
	echo "shutdown leakage reported (counted, not hidden):"
	printf '%s\n' "$LEAKS" | sed 's/^/    /' | head -8
fi

if [ -n "$UNEXPECTED" ]; then
	echo
	echo "UNEXPECTED diagnostics:"
	printf '%s\n' "$UNEXPECTED" | sed 's/^/    /' | head -20
	echo
	echo "FAIL: unexpected Godot diagnostics. Either fix them, or add a narrowly-scoped, justified"
	echo "      entry to EXPECTED/NOISE in tools/godot_verify.sh."
	exit 1
fi

echo
echo "PASS: no unexpected Godot diagnostics."
echo "Note: shutdown leaks are reported above but do not fail this check yet - the known baseline is"
echo "not zero, so a hard gate would be permanently red. Issue #883 tracks reducing it; when the"
echo "baseline reaches zero this script should fail on any leak."
