"""The shutdown gate must judge every headless entry point, not just the main slice (#883)."""

from __future__ import annotations

from tools.check_godot_shutdown import COMMANDS, check


def _problems(name: str, out: str, marker: str, baseline: int = 0) -> list[str]:
    return check(name, out, marker, baseline).problems


def test_every_command_declares_a_success_marker() -> None:
    for name, argv, marker in COMMANDS:
        assert name.strip()
        assert argv, f"{name} runs nothing"
        assert marker.strip(), f"{name} has no success marker"


def test_the_gate_covers_the_entry_points_ci_runs() -> None:
    names = [name for name, _, _ in COMMANDS]
    for required in ("slice", "rules", "playthrough", "ward", "interaction"):
        assert required in names, f"{required} is not gated"


def test_a_clean_run_passes() -> None:
    assert _problems("slice", "1375 checks, 0 failed\n", r"\d+ checks, 0 failed") == []


def test_a_missing_marker_fails_even_with_no_leaks() -> None:
    problems = _problems("ward", "nothing much happened\n", "WARD_READY")
    assert any("success marker" in problem for problem in problems)


def test_leaked_objects_fail() -> None:
    out = "WARD_READY\nWARNING: 3 ObjectDB instances were leaked at exit\n"
    assert any("leaked objects" in problem for problem in _problems("ward", out, "WARD_READY"))


def test_leaked_rids_fail() -> None:
    out = 'INTEGRATION_OK\nWARNING: 2 RIDs of type "CanvasItem" were leaked.\n'
    assert any("leaked RIDs" in problem
               for problem in _problems("interaction", out, "INTEGRATION_OK"))


def test_resources_still_in_use_are_reported_but_their_shutdown_line_is_allowed() -> None:
    out = ("INTEGRATION_OK\n"
           "ERROR: 1 resources still in use at exit\n"
           "ERROR: 5 resources still in use at exit\n")
    problems = _problems("interaction", out, "INTEGRATION_OK")
    assert not any("unexpected engine error" in problem for problem in problems)
    assert any("resources in use" in problem for problem in problems)


def test_any_other_engine_error_fails() -> None:
    out = "WARD_READY\nERROR: Cannot get path of node as it is not in a scene tree.\n"
    assert any("unexpected engine error" in problem for problem in _problems("ward", out, "WARD_READY"))


def test_script_and_parse_errors_always_fail() -> None:
    for line in ("SCRIPT ERROR: boom", "Parse Error: nope"):
        out = f"WARD_READY\n{line}\n"
        assert _problems("ward", out, "WARD_READY"), f"{line} was not flagged"


def test_expected_refusals_are_warnings_and_do_not_fail() -> None:
    out = ("1361 checks, 0 failed\n"
           "WARNING: NoopunkSceneFlow: unusable save data (refused)\n"
           "WARNING: InvestigationAdapter: no scene no_such_scene (refused)\n")
    assert _problems("slice", out, r"\d+ checks, 0 failed") == []


def test_a_failing_assertion_count_fails() -> None:
    out = "1361 checks, 2 failed\n"
    assert _problems("slice", out, r"\d+ checks, 0 failed"), "a failing suite passed the gate"
