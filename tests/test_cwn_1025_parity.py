"""Integrity of the CWN Free Edition parity matrix (#1025), not a test of rule prose."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "rules" / "cwn_free_edition_parity_1025.json"
STATUSES = {"complete", "partial", "missing", "not_applicable"}


def rows():
    return json.loads(DATA.read_text(encoding="utf-8"))["rows"]


def test_matrix_is_nonempty_unique_and_in_toc_order():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    entries = data["rows"]
    assert data["issue"] == 1025
    assert len(entries) >= 70
    sections = [row["section"] for row in entries]
    assert len(sections) == len(set(sections))
    pages = [row["page"] for row in entries]
    assert pages == sorted(pages)


def test_statuses_are_declared_and_missing_rows_explain_the_gap():
    for row in rows():
        assert row["status"] in STATUSES, row["section"]
        if row["status"] in {"missing", "partial"}:
            assert row["note"].strip(), row["section"]


def test_complete_rows_have_python_and_an_executable_test():
    for row in rows():
        if row["status"] != "complete":
            continue
        assert row["python"].strip(), row["section"]
        assert row["tests"].strip(), row["section"]
        for path in (part.strip() for part in row["tests"].split(";")):
            assert (ROOT / path).exists(), (row["section"], path)


def test_all_referenced_repository_paths_exist():
    for row in rows():
        for field in ("python", "mud", "tests"):
            for path in (part.strip() for part in row[field].split(";")):
                if not path or not path.startswith(("src/", "mud/", "tests/", "data/", "docs/")):
                    continue
                assert (ROOT / path).exists(), (row["section"], field, path)


def test_rendered_matrix_matches_the_source_counts():
    sys_path = ROOT / "tools" / "render_cwn_1025_matrix.py"
    assert sys_path.exists()
    rendered = (ROOT / "docs" / "rules" / "CWN_FREE_EDITION_PARITY_1025.md").read_text(encoding="utf-8")
    assert f"**Rows:** {len(rows())}" in rendered
    for row in rows():
        assert row["section"] in rendered
