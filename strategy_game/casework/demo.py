"""Headless demonstration of the packaged case (issue #502's Phase 1 vertical slice).

The demo plays *The Second Shadow* end to end with no UI: it walks the five scenes, spends the five
seats' actions, saves and reloads the case **mid-play**, assembles the clue chain, closes the case on
one of its three resolutions, and prints both the story it produced and the state that persisted.

It is the evidence that the slice is playable, not a second rules implementation: every number in the
output came from :mod:`strategy_game.rpg` and every persistent change came from
:func:`strategy_game.campaign.missions.apply_mission_outcome`.

    python -m strategy_game.casework
    python -m strategy_game.casework --route confront --approach force --seed 77
    python -m strategy_game.casework --json
"""
from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

from . import kallio
from .session import ActionResult, CaseSession, CaseworkError, load_session

__all__ = [
    "APPROACHES",
    "DEMO_SEED",
    "RESULT_LABELS",
    "ROUTES",
    "case_summary",
    "play",
    "render_text",
    "run_demo",
]

#: Per-route default seeds, chosen so each route demonstrates its **own** ending rather than falling
#: back to a referral. The script is deterministic at any seed (the case is fail-forward); these only
#: make the printed run show the ending the flag asks for.
DEMO_SEEDS = {"investigate": 461, "confront": 2, "refer": 461}
DEMO_SEED = DEMO_SEEDS["investigate"]

#: The three routes the demo can take, and the approach a confrontation uses.
ROUTES = ("investigate", "confront", "refer")
APPROACHES = ("pressure", "force")

RESULT_LABELS = {
    "investigate": "closed_by_evidence",
    "confront": "closed_by_confrontation",
    "refer": "closed_by_withdrawal",
}


def _entry(kind: str, text: str, **extra: Any) -> dict[str, Any]:
    return {"kind": kind, "text": text, **extra}


def _action(result: ActionResult) -> dict[str, Any]:
    """One action, as a reader needs it: who, what, the dice, and what it cost."""
    label = f"{result.seat_id}/{result.action_id}"
    if not result.ok:
        return _entry("action", f"refused {label}: {result.reason}", ok=False, seat=result.seat_id)
    parts: list[str] = []
    if result.skill:
        dice = "".join(f"{value:+d}" for value in result.dice)
        outcome = result.outcome.value if result.outcome else ""
        parts.append(f"{result.skill} {result.difficulty} [{dice}]={result.total} {outcome}".strip())
    if result.clues:
        parts.append(f"clue(s) {list(result.clues)}")
    if result.intel:
        parts.append(f"intel {list(result.intel)}")
    if result.aspect:
        parts.append(f"aspect {result.aspect!r}")
    if result.costs:
        parts.append("cost: " + ", ".join(result.costs))
    if result.scene_changed:
        parts.append(f"-> scene {result.scene_changed}")
    return _entry(
        "action",
        f"{label}: " + ("; ".join(parts) if parts else "done"),
        ok=True,
        seat=result.seat_id,
        action=result.action_id,
        outcome=None if result.outcome is None else result.outcome.value,
        clues=list(result.clues),
    )


def _scene_entry(session: CaseSession) -> dict[str, Any]:
    scene = session.scene_spec
    index = session.spec.scene_index(scene.id) + 1
    return _entry(
        "scene",
        f"[{index}/{len(session.spec.scenes)}] {scene.title} — {scene.location}",
        scene=scene.id,
        prose=scene.prose,
    )


def play(
    route: str = "investigate",
    *,
    seed: int | None = None,
    approach: str = "pressure",
    save_to: str | Path | None = None,
) -> tuple[CaseSession, list[dict[str, Any]], dict[str, Any]]:
    """Play the packaged case headless, saving and reloading once mid-case.

    Returns the live session, the structured log and a save/load confirmation. The mid-case reload is
    not decoration: it is the property the tests pin — a case saved between scenes resumes with the
    same subsequent rolls and produces the same ending as an uninterrupted run.
    """
    if route not in ROUTES:
        raise ValueError(f"route must be one of {ROUTES}, got {route!r}")
    if approach not in APPROACHES:
        raise ValueError(f"approach must be one of {APPROACHES}, got {approach!r}")
    seed = DEMO_SEEDS[route] if seed is None else int(seed)
    session = kallio.build_session(seed=seed)
    log: list[dict[str, Any]] = [_scene_entry(session)]
    target = (
        Path(save_to)
        if save_to is not None
        else Path(tempfile.gettempdir()) / "noopunk-case-kallio.json"
    )

    log.append(_action(session.act("harri_romppainen", "read_the_duty_log")))
    log.append(_action(session.act("pc_leader", "take_the_liaison_aside")))
    session.end_scene()
    log.append(_scene_entry(session))

    log.append(_action(session.act("laura_falk", "interview_nila")))
    log.append(_action(session.act("harri_romppainen", "scan_the_stack")))
    # A failure withholds the fragment, so the demo does what a table does: takes the *other* route
    # to the same fact while a seat is still free. Both routes failing is the partial chain.
    if "stack-manifest" not in session.clues:
        log.append(_action(session.act("pc_leader", "ask_the_clinic")))
    session.save(target)
    before = (session.scene_spec.id, len(session.clues), session.turn)
    session = load_session(target, kallio.CASE)
    after = (session.scene_spec.id, len(session.clues), session.turn)
    log.append(
        _entry(
            "note",
            f"saved mid-case to {target} and reloaded: scene {before[0]} -> {after[0]}, "
            f"{before[1]} -> {after[1]} clue(s), turn {before[2]} -> {after[2]}",
        )
    )

    log.append(_action(session.act("laura_univaara", "promise_protection")))
    session.end_scene()
    log.append(_scene_entry(session))
    log.append(_action(session.act("sebastian_virtanen", "read_the_stairwell")))
    log.append(_action(session.act("harri_romppainen", "pull_the_mesh_log")))
    log.append(_action(session.act("laura_falk", "search_the_landing")))
    # A free seat holds the hatch: the action is open to any seat (only ``suggested_actor`` is
    # presentation), and the suggested actor has already acted this scene.
    log.append(_action(session.act("pc_leader", "hold_the_hatch")))
    session.end_scene()
    log.append(_scene_entry(session))

    log.append(_action(session.act("laura_univaara", "supervise_the_reading")))
    log.append(_action(session.act("harri_romppainen", "check_the_thermal_record")))
    log.append(_action(session.act("laura_falk", "ask_her_why_she_stayed")))
    session.end_scene()
    log.append(_scene_entry(session))

    if route == "refer":
        log.append(
            _entry("note", "the party assembles nothing; the file goes upstairs as it stands")
        )
    else:
        log.append(_action(session.act("pc_leader", "assemble_the_chain")))
        log.append(_action(session.act("harri_romppainen", "pull_the_batch_signout")))
        log.append(_action(session.act("sebastian_virtanen", "read_his_file")))
        log.append(_action(session.act("laura_univaara", "brief_the_liaison_early")))
        log.append(_action(session.act("laura_falk", "get_to_the_bay_first")))

    # The case's one spendable aspect reaches the closing check, free, if the party earned it.
    free = next(
        (name for name, aspect in session.scene.aspects.items() if aspect.free_invocations > 0),
        None,
    )
    detail = "" if free is None else f" invoking {free!r} (free)"
    log.append(_entry("note", f"the closing check is rolled{detail}"))
    try:
        resolution = session.resolve(
            RESULT_LABELS[route],
            seat_id="pc_leader",
            approach=approach if route == "confront" else "",
            free_invoke=free,
        )
    except CaseworkError as refused:
        # The requested ending needs something the party did not get. The case still closes — on the
        # weaker record — which is what the demo shows rather than crashing on.
        log.append(_entry("note", f"{RESULT_LABELS[route]} is not available: {refused}"))
        resolution = session.resolve("closed_by_withdrawal", seat_id="pc_leader")
    log.append(
        _entry(
            "resolution",
            f"{resolution.label}: {resolution.outcome.value}"
            + (f" — {resolution.detail}" if resolution.detail else ""),
            resolution=resolution.resolution_id,
            requested=RESULT_LABELS[route],
            degraded=resolution.degraded,
            outcome=resolution.outcome.value,
        )
    )
    if resolution.degraded:
        log.append(
            _entry("note", "the attempt fell back to a referral: the case ends, on the weaker record")
        )
    for wound in resolution.wounds:
        log.append(_entry("wound", f"wound: {wound}"))

    session.save(target)
    reopened = load_session(target, kallio.CASE)
    confirmation = {
        "path": str(target),
        "finished_before_reload": session.finished,
        "finished_after_reload": reopened.finished,
        "same_clues": reopened.clues == session.clues,
        "same_evidence": reopened.report()["persisted"]["case_evidence"]
        == session.report()["persisted"]["case_evidence"],
        "campaign_notes": reopened.report()["persisted"]["campaign_notes"],
        "resolution_after_reload": reopened.report()["resolution"],
    }
    log.append(
        _entry(
            "note",
            f"closed case saved to {target} and reloaded: finished={confirmation['finished_after_reload']}, "
            f"evidence identical={confirmation['same_evidence']}, "
            f"campaign notes={confirmation['campaign_notes']}",
        )
    )
    return session, log, confirmation


def run_demo(
    route: str = "investigate",
    *,
    seed: int | None = None,
    approach: str = "pressure",
    save_to: str | Path | None = None,
) -> dict[str, Any]:
    """The demo as one JSON-able record: the log, the case report and the reload confirmation."""
    session, log, confirmation = play(route, seed=seed, approach=approach, save_to=save_to)
    report = session.report()
    return {
        "route": route,
        "approach": approach if route == "confront" else "",
        "seed": seed,
        "log": log,
        "case": case_summary(report),
        "persisted": report["persisted"],
        "reload": confirmation,
    }


def case_summary(report: dict[str, Any]) -> dict[str, Any]:
    """The reader-facing half of a session report, in the shape :func:`render_text` reads.

    Shared with the interactive play mode (:mod:`strategy_game.casework.play`) so that a played
    case and a headless run print the same ending from the same report — the report is the
    session's own, and nothing here computes anything.
    """
    return {
        "id": report["case_id"],
        "title": report["title"],
        "core_question": report["core_question"],
        "era_label": report["era_label"],
        "scene": report["scene"],
        "clues": report["clues"],
        "intel": report["intel"],
        "findings": report["findings"],
        "chain": report["chain"],
        "complications": report["complications"],
        "resolution": report["resolution"],
        "party": report["party"],
        "wounds": report["wounds"],
    }


def render_text(result: dict[str, Any]) -> str:
    """The demo's reading text. Every line is derived from the record, not from the prose."""
    case = result["case"]
    lines = [
        f"NoöPunk casework — {case['title']} ({case['id']})",
        f"{case['era_label']}",
        f"Question: {case['core_question']}",
        "Party: the faction leader (PC) and four agents",
        "",
    ]
    for entry in result["log"]:
        if entry["kind"] == "scene":
            lines.append("")
            lines.append(entry["text"])
            lines.append(_wrap(entry.get("prose", "")))
            continue
        if entry["kind"] == "resolution":
            lines.append("")
            lines.append(entry["text"])
            continue
        lines.append(f"  {entry['text']}")
    lines.append("")
    lines.append(
        f"Chain: {case['chain']['held']} of {case['chain']['of']} fragments — "
        + ", ".join(
            clue["id"]
            for clue in case["clues"]
            if clue["id"] in {"stack-manifest", "camera-gap", "impression-double"}
        )
    )
    for finding in case["findings"]:
        lines.append(
            f"Finding {finding['id']}" + (" (partial)" if finding["partial"] else "") + ":"
        )
        lines.append(_wrap(kallio.CASE.finding(finding["id"]).text))
    lines.append("")
    lines.append(f"Resolution: {case['resolution']}")
    if case["complications"]:
        lines.append(f"Complications carried: {', '.join(case['complications'])}")
    lines.append("")
    lines.append("Party state")
    for member in case["party"]:
        stress = sum(1 for box in member["physical_stress"] if box)
        mental = sum(1 for box in member["mental_stress"] if box)
        consequences = ", ".join(
            f"{item['name']} ({item['severity']})" for item in member["consequences"]
        )
        lines.append(
            f"  {member['seat']}: {member['name']} — fate {member['fate_points']}, "
            f"physical stress {stress}, mental stress {mental}"
            + (f", consequences: {consequences}" if consequences else "")
        )
    lines.append("")
    lines.append("Persisted in the campaign")
    persisted = result["persisted"]
    lines.append(f"  objectives: {persisted['objectives']}")
    lines.append(f"  intelligence_ids: {persisted['intelligence_ids']}")
    lines.append(f"  reputation_labels: {persisted['reputation_labels']}")
    lines.append(f"  resources: {persisted['resources']}")
    lines.append(f"  case evidence: {persisted['case_evidence']}")
    lines.append(f"  campaign notes: {persisted['campaign_notes']}")
    lines.append("")
    lines.append(f"Save file: {result['reload']['path']}")
    return "\n".join(lines)


def _wrap(text: str, width: int = 96) -> str:
    """Indent and wrap prose so the terminal report stays readable without a renderer."""
    import textwrap

    return "\n".join(
        "  " + line
        for paragraph in text.split("\n\n")
        for line in textwrap.wrap(" ".join(paragraph.split()), width=width)
    )
