"""The shutdown-noise classifier (#883) must fail on leaks and tolerate only named diagnostics."""

from __future__ import annotations

from tools.godot_verify import FAIL_PATTERNS, classify, check_markers


def _lines(report) -> list[str]:
    return [f"{name}:{reason}" for name, reason, _ in report.unexpected]


def test_a_clean_log_has_nothing_unexpected() -> None:
    log = "PASS every rule\n1375 checks, 0 failed\n"
    report = classify("slice", log)
    assert report.unexpected == []
    assert report.expected == []


def test_leaked_rids_fail_the_gate() -> None:
    log = 'WARNING: 43 RIDs of type "CanvasItem" were leaked.\n'
    assert "slice:renderer RID leak" in _lines(classify("slice", log))


def test_leaked_objects_and_resources_fail_the_gate() -> None:
    log = (
        "WARNING: 209 ObjectDB instances were leaked at exit\n"
        "ERROR: 7 resources still in use at exit\n"
    )
    reasons = _lines(classify("slice", log))
    assert "slice:object leak" in reasons
    assert "slice:resource leak" in reasons


def test_script_errors_fail_the_gate() -> None:
    assert "slice:script error" in _lines(classify("slice", "SCRIPT ERROR: boom"))
    assert "slice:script parse error" in _lines(classify("slice", "Parse Error: nope"))


def test_layout_anchor_warning_fails_the_gate() -> None:
    log = "WARNING: Nodes with non-equal opposite anchors will have their size overridden after _ready()."
    assert "slice:layout warning (anchors fight size)" in _lines(classify("slice", log))


def test_expected_negative_path_diagnostics_are_allowed() -> None:
    log = (
        "ERROR: NoopunkSceneFlow: unusable save data\n"
        "ERROR: DialogueRunner: no choice 99 at node doctor_end\n"
        "ERROR: InvestigationAdapter: no scene no_such_scene\n"
        "WARNING: Unknown clue id: no-such-clue\n"
    )
    report = classify("slice", log)
    assert report.unexpected == []
    assert len(report.expected) == 4


def test_an_unknown_error_is_not_swallowed() -> None:
    log = "ERROR: SomethingNobodyExpected: the sky fell\n"
    assert _lines(classify("slice", log)), "an unlisted error must fail the gate"


def test_success_markers_are_required() -> None:
    assert check_markers("slice", "1375 checks, 0 failed") == []
    assert check_markers("slice", "1375 checks, 3 failed") != []
    assert check_markers("ward", "WARD_READY npcs=3") == []
    assert check_markers("ward", "nothing happened") != []


def test_every_fail_pattern_is_a_non_empty_regex() -> None:
    for pattern, reason in FAIL_PATTERNS:
        assert pattern.strip()
        assert reason.strip()
