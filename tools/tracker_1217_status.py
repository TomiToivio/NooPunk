"""Derive the #1217 tracker status from the tree, and fail when the evidence disappears (#1217 line 19).

The tracker is a checklist written before the code existed, so its boxes drift: an item ticked by hand can point at a
file that was later renamed, and an item left unticked can describe work that has been done for a week. This tool makes
the status a *derived* artefact: each row names the files that prove it, the tool checks they exist, and the rendered
page is compared byte-for-byte in CI terms by `--check`.

Usage:
    python3 tools/tracker_1217_status.py            # regenerate docs/design/TRACKER_1217_STATUS.md
    python3 tools/tracker_1217_status.py --check    # exit 1 if the page is stale or evidence is missing
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "design" / "TRACKER_1217_STATUS.md"

#: `(tracker line, status, evidence, note)`.
#:
#: statuses: DONE (code + tests), PARTIAL (code, gap named), BLOCKED (an author decision is required), DEFERRED (by the
#: issue's own instruction), OUT (not this issue).
ROWS: tuple[tuple[str, str, tuple[str, ...], str], ...] = (
    (
        "Opening: audit creation, background, edges, foci, tags, inventory",
        "DONE",
        ("src/rules/cwn_character.py", "src/rules/cwn_edges_foci.py", "src/rules/cwn_foci.py",
         "src/rules/cwn_backgrounds.py", "src/rules/scene_tags.py", "src/world/items.py",
         "docs/design/TRACKER_1217_AUDIT.md"),
        "the audit page records what exists and what each module owns; no parallel engine was added",
    ),
    (
        "Opening: deterministic lifepath builder for Tony German",
        "PARTIAL",
        ("src/rules/europol_lifepath.py", "tests/test_europol_lifepath_1217.py",
         "docs/rules/EUROPOL_LIFEPATH_1217.md"),
        "builder core done: fixed facts, three routes, delegated budgets, 26 legality tests. The player-facing flow "
        "still needs a verified CWN Edge catalogue to offer, and the tag offer lists are an authoring decision",
    ),
    (
        "Opening: scripted first day (nightmare to Ratakatu 12)",
        "DONE",
        ("src/console/first_day.py", "src/console/world_session.py"),
        "every authored step exists as a session transition; no forced roll to reach work",
    ),
    (
        "Opening: first approved investigation on the graphs",
        "BLOCKED",
        ("docs/scenarios/CAMPAIGN_ROADMAP_1120.md", "docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md"),
        "no case has been author-approved yet; #1120 delivers a complete case awaiting that decision",
    ),
    (
        "Opening: runtime adapters, one canonical actor id and sheet",
        "PARTIAL",
        ("src/world/actor_registry.py", "src/console/first_day.py", "src/world/graphs.py"),
        "console and graphs share `tony.german`; the Evennia side does not yet reference the authored actor, so parity "
        "is unproven rather than done",
    ),
    (
        "Opening: kit as a legible diagnostic puzzle, failure cannot softlock",
        "DONE",
        ("src/world/items.py", "src/console/first_day.py"),
        "issue/fault/activate states, FIRST_DAY_REQUIRED, and a fault path that still reaches the office",
    ),
    (
        "Opening: companion interaction once D71 is resolved",
        "BLOCKED",
        (),
        "D71 is an open author decision; implementing a companion now would invent its personality and refusal rules",
    ),
    (
        "Opening: deterministic offline regression tests",
        "PARTIAL",
        ("tests/test_clock_scheduler_1230.py", "tests/test_europol_lifepath_1217.py"),
        "first-day, lifepath legality, save/resume and graph tests exist; branch coverage of every authored choice and "
        "cross-platform parity are not yet covered",
    ),
    (
        "Rules: AWN Mutation Edge for PCs, independent of ancestry and PSI",
        "PARTIAL",
        ("src/rules/awn_mutant.py", "src/rules/psi_edges.py"),
        "build rules are enforced (Europol approval, no automatic Hybrid, independence). The mutation tables are not "
        "registered: they are printed content, and transcribing them is an author/licence decision",
    ),
    (
        "Rules: AWN Mentalist selectable, no SWN discipline smuggled in",
        "DONE",
        ("src/rules/awn_mentalist.py", "src/rules/psi_access.py", "src/rules/rookie_build.py",
         "tests/test_psychic_training_1217.py"),
        "arts, Effort accounting and the Mentalist/Spellcaster bar are enforced; the Edge is a PC option",
    ),
    (
        "Rules: SWN Psychic Training Focus",
        "DONE",
        ("src/rules/psychic_training.py", "tests/test_psychic_training_1217.py",
         "docs/rules/PSYCHIC_TRAINING_FOCUS_1217.md"),
        "implemented from the author's quotation in #1178; prose not reproduced; the retroactive formula is a reading "
        "awaiting confirmation",
    ),
    (
        "Rules: device-granted PSI",
        "DONE",
        ("src/rules/psi_edges.py", "src/rules/psi_access.py", "src/rules/swn_psionics.py",
         "docs/design/ISSUE_1196_DEVICE_PSI.md"),
        "a grant lives and dies with the device, reserves Effort only when the equipment says so, and never becomes a "
        "selectable discipline",
    ),
    (
        "Rules: AWN environmental and social procedures",
        "PARTIAL",
        ("src/rules/awn_survival.py", "src/rules/awn_stress_tracker.py", "src/rules/awn_region.py",
         "src/rules/cwn_pharmaceuticals.py", "src/rules/cwn_combat.py"),
        "survival, stress, region and pharmaceuticals exist; radiation, vehicle combat and chases have no dedicated "
        "module yet — they are CWN/AWN procedures that must be verified against the book before any code",
    ),
    (
        "Rules: verify tags, clues and investigation overlays",
        "DONE",
        ("src/rules/investigation.py", "src/rules/scene_tags.py", "tests/test_scene_tags_20261105.py",
         "tests/test_investigation_access_and_inquiry.py", "tests/test_goals_1119.py"),
        "four tag types, one clue model and the investigation procedures are implemented and tested",
    ),
    (
        "Rules: Astral graph",
        "DEFERRED",
        (),
        "deferred by #1178 and #1230 until an authored scene needs navigable astral locations",
    ),
    (
        "Data: Greater Helsinki jurisdictions and zones",
        "BLOCKED",
        ("src/world/helsinki.py", "data/world/helsinki_locations.json"),
        "the canonical places load; the four jurisdiction levels, economic and diplomatic zones and protection regions "
        "are setting data awaiting author approval (#1121)",
    ),
    (
        "Data: recurring clues, provenance, restrained social reactions",
        "PARTIAL",
        ("src/rules/investigation.py", "docs/scenarios/CASE_01_THE_TUESDAY_COMPLAINT.md"),
        "clue provenance exists; the 50/25/25 reaction envelope is documented but not encoded, because it is a table "
        "the author has not approved",
    ),
    (
        "Data: Galactic Machine War and Nordic history as discoverable material",
        "BLOCKED",
        ("docs/proposals/CATASTROPHIC_NORMALITY_AND_NORDIC_1946_MEMO_DRAFT.md",),
        "material exists as a design memo; turning it into discoverable files before a case needs them is exactly what "
        "the issue forbids — it waits for an author-approved case that needs the material",
    ),
    (
        "Review: persistence, canon vs event log, reproducible tests, docs",
        "PARTIAL",
        ("src/simulation/events.py", "src/simulation/scheduler.py", "docs/DUPLICATION_AUDIT.md",
         "docs/DOCUMENT_REGISTER.md"),
        "event log, clock/queue persistence and the document register exist; a full audit of every save path is still "
        "outstanding",
    ),
)

STATUS_ORDER = ("DONE", "PARTIAL", "BLOCKED", "DEFERRED")


def missing_evidence() -> list[tuple[str, str]]:
    """Every (item, path) whose file does not exist. A row is not evidence until its evidence is there."""
    absent: list[tuple[str, str]] = []
    for item, _status, evidence, _note in ROWS:
        for path in evidence:
            if not (ROOT / path).is_file():
                absent.append((item, path))
    return absent


def render() -> str:
    counts = {status: sum(1 for _r in ROWS if _r[1] == status) for status in STATUS_ORDER}
    lines = [
        "# Tracker #1217 — derived status",
        "",
        "> **Generated.** `python3 tools/tracker_1217_status.py` rewrites this page; `--check` fails when it is stale or "
        "when a row's evidence file has disappeared. Every status below is a claim about files that exist right now, not "
        "about a commit message.",
        "",
        f"**Totals:** {counts['DONE']} done · {counts['PARTIAL']} partial · {counts['BLOCKED']} blocked · "
        f"{counts['DEFERRED']} deferred.",
        "",
        "| # | tracker item | status | evidence | note |",
        "|---|---|---|---|---|",
    ]
    for index, (item, status, evidence, note) in enumerate(ROWS, start=1):
        links = "<br>".join(f"`{path}`" for path in evidence) or "—"
        lines.append(f"| {index} | {item} | **{status}** | {links} | {note} |")
    lines += [
        "",
        "## What \"blocked\" means here",
        "",
        "A blocked row needs a decision that is not an agent's to make: an approved case, an approved data table, a "
        "resolved author question (D71), or a licence decision about transcribing printed tables. Blocked is not "
        "unstarted — it is *started to the edge of the decision* and then stopped on purpose.",
        "",
        "## What \"partial\" means here",
        "",
        "The mechanism exists and is tested; a named piece of scope does not. The note says which piece, so the row can "
        "be finished without re-reading the issue.",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    absent = missing_evidence()
    if absent:
        for item, path in absent:
            print(f"missing evidence for {item!r}: {path}", file=sys.stderr)
        return 1

    text = render()
    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.is_file() else ""
        if current != text:
            print("docs/design/TRACKER_1217_STATUS.md is stale; run python3 tools/tracker_1217_status.py",
                  file=sys.stderr)
            return 1
        print("tracker status: up to date")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    done = sum(1 for row in ROWS if row[1] == "DONE")
    print(f"wrote {OUT.relative_to(ROOT)} — {len(ROWS)} rows, {done} done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
