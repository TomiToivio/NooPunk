"""Guards against the failure mode this repository keeps producing: two agents, one feature, two files.

Nothing here checks style. Each test asserts that a feature has **one** home, and fails when a second one appears —
because a duplicate does not announce itself, it arrives as a reasonable-looking parallel implementation and is
discovered three weeks later when the two disagree.

If a test here fails, the answer is almost never "register the new path". It is to decide which implementation is
canonical, delete the other, and record the decision in `docs/DUPLICATION_AUDIT.md`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Directories that hold gameplay code. Tests, docs and data are excluded on purpose.
CODE_ROOTS = ("src/rules", "src/console", "mud/nopunk_mud", "portable_noopunk")


def _py_files():
    for root in CODE_ROOTS:
        base = ROOT / root
        if base.is_dir():
            yield from sorted(p for p in base.rglob("*.py") if "__pycache__" not in p.parts)


def test_only_one_console_entry_point_exists():
    """One playable text front end. A second one silently forks the rules it calls."""
    candidates = [p for p in _py_files()
                  if re.search(r"class\s+(Console|CaseSession)\b", p.read_text(encoding="utf-8", errors="ignore"))]
    names = sorted(str(p.relative_to(ROOT)) for p in candidates)
    assert len(candidates) <= 1, f"more than one console/session implementation: {names}"


def test_only_one_campaign_model_is_live():
    """`solo_campaign.py` is a deprecated shim; anything new must use `campaign/engine.py`."""
    engines = [p for p in _py_files()
               if "campaign" in p.name.lower() or "campaign" in str(p.parent).lower()]
    live = [p for p in engines if "solo_campaign" not in p.name]
    assert live, "the live campaign engine has disappeared"
    solo = ROOT / "mud/nopunk_mud/solo_campaign.py"
    if solo.is_file():
        assert "DEPRECATED" in solo.read_text(encoding="utf-8"), (
            "solo_campaign.py must stay marked deprecated or be deleted")


def test_the_coverage_matrix_has_one_live_file():
    """Several audits have been written. Exactly one is kept current; the rest must say they are not.

    The earlier version of this test only counted documents containing the word "canonical", which a
    document could satisfy by accident and which said nothing about *which* one was live. Two generated
    reports from the same tool, and six older hand-maintained matrices disagreeing with both, all passed it.

    The rule now: `docs/rules/CWN_COVERAGE_1068.md` is the live report, it is byte-for-byte the generator's
    output, and every other `*COVERAGE*` document carries the superseded banner.
    """
    import sys

    sys.path.insert(0, str(ROOT / "tools"))
    from cwn_parity_audit import build, render_report

    live = ROOT / "docs/rules/CWN_COVERAGE_1068.md"
    assert live.is_file(), "the generated coverage report is missing"
    assert live.read_text(encoding="utf-8") == render_report(build()), (
        "docs/rules/CWN_COVERAGE_1068.md is stale; run python3 tools/cwn_parity_audit.py")

    def is_cwn_status_doc(path: Path) -> bool:
        """CWN rule coverage/parity only: engine coverage (Godot) and SWN are different subjects."""
        name = path.name.upper()
        return (path.suffix == ".md" and "CWN" in name
                and ("COVERAGE" in name or "PARITY" in name) and "GODOT" not in name)

    undocumented = []
    for path in sorted(p for p in (ROOT / "docs").rglob("*.md") if is_cwn_status_doc(p)):
        if path == live:
            continue
        head = path.read_text(encoding="utf-8", errors="ignore")[:600]
        if "Superseded" not in head:
            undocumented.append(path.name)
    assert not undocumented, (
        f"these documents still present themselves as coverage of CWN: {undocumented}. Either add the "
        f"'> **Superseded:**' banner pointing at docs/rules/CWN_COVERAGE_1068.md, or delete the file.")


#: Collisions that are **known and explained**. Each one is a different subsystem that happens to share a
#: filename, or a deliberately kept second implementation with a migration plan. Adding an entry here is a
#: decision that must also be recorded in `docs/DUPLICATION_AUDIT.md`.
KNOWN_COLLISIONS = {
    "cwn_core": "src/rules is canonical (ADR 1054); mud/nopunk_mud/cwn_core.py is a second kernel used only by "
                "the parity probes in tools/. Merge deferred: the MUD's campaign engine imports it. Audit entry.",
    "social": "Different subsystems: src/rules/social.py is the provisional #220 social procedures "
              "(IS_CANONICAL = False); mud/nopunk_mud/social.py is the #1008 rank/reputation overlay. "
              "Rename one before either grows.",
    "session": "Different layers: src/console/session.py is the portable case session; mud/nopunk_mud/session.py "
               "is the Evennia adapter over CampaignEngine. Not duplicates; the names are the problem.",
}


def test_a_rule_module_does_not_exist_twice_under_two_roots():
    """The same rule in `src/rules` and again under `mud/` is the classic drift.

    A new collision fails this test. A known one passes only because it is written down above, with a reason —
    an allowlist that nobody has to justify is how the duplicates win.
    """
    names: dict[str, list[str]] = {}
    for path in _py_files():
        stem = path.stem
        if stem.startswith("test_") or stem == "__init__":
            continue
        names.setdefault(stem, []).append(str(path.relative_to(ROOT)))
    duplicates = {k: v for k, v in names.items() if len(v) > 1}
    unexplained = {k: v for k, v in duplicates.items() if k not in KNOWN_COLLISIONS}
    assert not unexplained, (
        f"new duplicate module names: {unexplained}. Decide which is canonical, delete the other, or add a "
        f"justified entry to KNOWN_COLLISIONS and docs/DUPLICATION_AUDIT.md.")


def test_every_known_collision_has_a_written_reason():
    for name, reason in KNOWN_COLLISIONS.items():
        assert len(reason) > 60, f"{name}: the reason is too short to be a decision"
    audit = ROOT / "docs/DUPLICATION_AUDIT.md"
    assert audit.is_file(), "KNOWN_COLLISIONS must be mirrored in docs/DUPLICATION_AUDIT.md"
    text = audit.read_text(encoding="utf-8")
    for name in KNOWN_COLLISIONS:
        assert name in text, f"{name} is in the allowlist but not in the audit"
