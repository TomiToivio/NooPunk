"""Regression tests for the conservative CWN subprocedure audit (#1025)."""
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "cwn_procedure_backlog_1025", ROOT / "tools" / "cwn_procedure_backlog_1025.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def test_inventory_is_provisional_and_has_unique_procedures():
    report = audit.build()
    assert len(report["procedures"]) >= 90
    assert len({row["id"] for row in report["procedures"]}) == len(report["procedures"])
    assert report["verified_complete"] == 0
    assert not audit.validate(report)
    assert all(row["status"] == "unverified" for row in report["procedures"])


def test_no_completion_claim_without_source_and_playtest_evidence():
    report = audit.build()
    row = report["procedures"][0]
    row["status"] = "complete"
    report["verified_complete"] = 1
    problems = audit.validate(report)
    assert any("unsupported complete claim" in problem for problem in problems)


def test_book_page_is_required_for_source_verified_claim():
    report = audit.build()
    report["procedures"][0]["source_verified"] = True
    assert any("lacks PDF page" in problem for problem in audit.validate(report))


def test_nonexistent_paths_are_rejected():
    report = audit.build()
    report["procedures"][0]["tests"] = ["tests/never-created-1025.py"]
    assert any("missing evidence file" in problem for problem in audit.validate(report))


def test_markdown_says_work_is_unverified():
    doc = audit.markdown(audit.build())
    assert "not a verified transcription" in doc
    assert "unverified" in doc
