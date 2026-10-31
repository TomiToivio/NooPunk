"""The linked-SRD compliance matrix must stay true to the repository (#950).

These tests do not restate the matrix; they check that it cannot lie. A row claiming a Godot module, a
test, or a Python symbol that does not exist fails here, and so does a page of the linked SRD that has
been quietly dropped.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _tool():
    spec = importlib.util.spec_from_file_location(
        "cwn_page_audit", ROOT / "tools/cwn_page_audit.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_matrix_is_consistent_with_the_repository():
    tool = _tool()
    matrix, pages = tool.load()
    found = tool.problems(matrix, pages)
    assert not found, "\n".join(found)


def test_every_page_of_the_linked_srd_is_accounted_for():
    tool = _tool()
    matrix, pages = tool.load()
    slugs = [row["srd"] for row in matrix["rows"]]
    assert len(slugs) == len(set(slugs)), "a page is listed more than once"
    assert sorted(slugs) == sorted(pages["pages"])
    assert len(slugs) == pages["count"]


def test_no_page_is_claimed_implemented_without_evidence():
    tool = _tool()
    matrix, _ = tool.load()
    for row in matrix["rows"]:
        if row["coverage"] == "implemented":
            assert row["tests"], f"{row['srd']}: implemented without a test"
            assert row["python"], f"{row['srd']}: implemented without a Python target"


def test_the_rendered_document_is_not_stale():
    """A hand-edited matrix is how a compliance claim starts drifting from the code."""
    tool = _tool()
    matrix, pages = tool.load()
    rendered = (ROOT / "docs/rules/CWN_SRD_PAGE_AUDIT_950.md").read_text(encoding="utf-8")
    assert rendered == tool.render(matrix, pages), (
        "docs/rules/CWN_SRD_PAGE_AUDIT_950.md is stale; "
        "run python3 tools/cwn_page_audit.py --render docs/rules/CWN_SRD_PAGE_AUDIT_950.md")
