"""Audit a Romppainen case for the one failure a detective story cannot survive: a softlock (#1310).

A case is a finite graph: scenes are nodes, choices are edges, clues are the things you can only carry forward
if you happened to look. The player's failure mode is not death — it is arriving at the end without the evidence
that makes the ending mean anything, or being unable to reach the one clue that unlocks the only honest route.

This module answers the questions an author needs answered before playtesting:

* is every declared clue obtainable at all?
* is every **essential** clue obtainable on *every* path that reaches an ending — or is there a route that
  starves the player and still lets them finish?
* is every scene reachable, and does every ending have a way in?
* do the contradictions and deductions reference clues that exist?

It reads the same case format as `adventure.py` and adds nothing to it. `--check` exits non-zero on an error;
warnings do not fail a case, because an unreachable optional scene is untidy, not broken.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_CASE = Path(__file__).resolve().parents[1] / "Graphs" / "fixtures" / "romppainen_development_case.json"

REQUIRED_KEYS = ("id", "title", "start", "clues", "scenes")


@dataclass(frozen=True, slots=True)
class Finding:
    severity: str  # "error" or "warning"
    code: str
    message: str


def _choices(scene: dict) -> list[dict]:
    return [choice for choice in scene.get("choices", []) if isinstance(choice, dict)]


def reachable_scenes(case: dict) -> set[str]:
    """Every scene id the player can arrive at, ignoring clue gates."""
    scenes = case.get("scenes", {})
    start = case.get("start", "")
    seen: set[str] = set()
    frontier = [start] if start in scenes else []
    while frontier:
        current = frontier.pop()
        if current in seen:
            continue
        seen.add(current)
        for choice in _choices(scenes.get(current, {})):
            target = choice.get("to")
            if target in scenes and target not in seen:
                frontier.append(target)
    return seen


def endings(case: dict) -> set[str]:
    return {sid for sid, scene in case.get("scenes", {}).items() if scene.get("ending")}


def ending_reachable_without(case: dict, ending: str, clue: str, *, limit: int = 20000) -> bool:
    """Is there a route to ``ending`` that never picks up ``clue``?

    This is the softlock question, and it has to be answered path by path. A union of all clues carried into a
    scene answers the opposite question — "can this ever be known here" — and would let a shortcut pass.
    """
    scenes = case.get("scenes", {})
    start = case.get("start", "")
    if start not in scenes or ending not in scenes:
        return False
    seen: set[tuple[str, frozenset[str]]] = set()
    frontier: list[tuple[str, frozenset[str]]] = [(start, frozenset(scenes[start].get("adds", [])))]
    visited = 0
    while frontier:
        scene_id, carried = frontier.pop()
        visited += 1
        if visited > limit:  # pragma: no cover - a case this big is a design problem of its own
            return False
        state = (scene_id, carried)
        if state in seen:
            continue
        seen.add(state)
        if scene_id == ending and clue not in carried:
            return True
        for choice in _choices(scenes.get(scene_id, {})):
            target = choice.get("to")
            if target not in scenes:
                continue
            if not set(choice.get("requires", [])).issubset(carried):
                continue
            frontier.append((str(target), frozenset(carried | set(choice.get("adds", [])))))
    return False


def reachable_clues(case: dict) -> set[str]:
    """Every clue the player can pick up on some route (scene-level and choice-level)."""
    obtained: set[str] = set()
    for scene in case.get("scenes", {}).values():
        obtained.update(scene.get("adds", []))
        for choice in _choices(scene):
            obtained.update(choice.get("adds", []))
    return obtained


def audit(case: dict) -> list[Finding]:
    findings: list[Finding] = []
    for key in REQUIRED_KEYS:
        if key not in case:
            findings.append(Finding("error", "missing-key", f"case has no {key!r}"))
    if any(f.severity == "error" and f.code == "missing-key" for f in findings):
        return findings

    scenes: dict = case["scenes"]
    clues: dict = case["clues"]
    start = case["start"]
    if start not in scenes:
        findings.append(Finding("error", "bad-start", f"start scene {start!r} does not exist"))
        return findings

    reachable = reachable_scenes(case)
    for scene_id in sorted(set(scenes) - reachable):
        findings.append(Finding("warning", "unreachable-scene", f"scene {scene_id!r} cannot be reached"))

    for scene_id, scene in scenes.items():
        for index, choice in enumerate(_choices(scene)):
            target = choice.get("to")
            if target not in scenes:
                findings.append(
                    Finding("error", "dangling-choice",
                            f"{scene_id}: choice {index} points at unknown scene {target!r}")
                )
            for clue in choice.get("requires", []):
                if clue not in clues:
                    findings.append(
                        Finding("error", "unknown-requirement",
                                f"{scene_id}: choice {index} requires unknown clue {clue!r}")
                    )
        for clue in scene.get("adds", []):
            if clue not in clues:
                findings.append(Finding("error", "unknown-clue", f"{scene_id} adds unknown clue {clue!r}"))
        for index, choice in enumerate(_choices(scene)):
            for clue in choice.get("adds", []):
                if clue not in clues:
                    findings.append(
                        Finding("error", "unknown-clue",
                                f"{scene_id}: choice {index} adds unknown clue {clue!r}")
                    )

    obtainable = set()
    for scene in scenes.values():
        obtainable.update(scene.get("adds", []))
        for choice in _choices(scene):
            obtainable.update(choice.get("adds", []))
    for clue in sorted(set(clues) - obtainable):
        findings.append(Finding("error", "unobtainable-clue", f"clue {clue!r} is declared but never added"))

    ended = endings(case)
    if not ended:
        findings.append(Finding("error", "no-ending", "case has no scene marked ending:true"))
    for ending in sorted(ended - reachable):
        findings.append(Finding("error", "unreachable-ending", f"ending {ending!r} cannot be reached"))
    if len(ended) < 2:
        findings.append(
            Finding("warning", "single-ending",
                    "case offers one ending; the mandate asks for at least two meaningfully distinct outcomes")
        )

    essential = case.get("essential_clues", [])
    if essential:
        for ending in sorted(ended & reachable):
            for clue in essential:
                if clue not in clues:
                    findings.append(
                        Finding("error", "unknown-essential-clue",
                                f"essential_clues names unknown clue {clue!r}")
                    )
                    continue
                if ending_reachable_without(case, ending, clue):
                    findings.append(
                        Finding("error", "ending-without-essential-evidence",
                                f"ending {ending!r} can be reached without {clue!r}")
                    )
    else:
        findings.append(
            Finding("warning", "no-essential-clues",
                    "case declares no essential_clues, so the softlock audit cannot tell what must survive")
        )

    for index, contradiction in enumerate(case.get("contradictions", [])):
        for clue in contradiction.get("between", []):
            if clue not in clues:
                findings.append(
                    Finding("error", "bad-contradiction",
                            f"contradiction {index} names unknown clue {clue!r}")
                )
        if len(contradiction.get("between", [])) != 2:
            findings.append(
                Finding("error", "bad-contradiction",
                        f"contradiction {index} must name exactly two clues")
            )
    for index, deduction in enumerate(case.get("deductions", [])):
        for clue in deduction.get("requires", []):
            if clue not in clues:
                findings.append(
                    Finding("error", "bad-deduction",
                            f"deduction {index} requires unknown clue {clue!r}")
                )
        if not deduction.get("text"):
            findings.append(Finding("error", "bad-deduction", f"deduction {index} has no text"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit a Romppainen case for unreachable scenes and softlocks")
    parser.add_argument("--case", default=str(DEFAULT_CASE))
    parser.add_argument("--check", action="store_true", help="exit non-zero on any error")
    args = parser.parse_args(argv)

    try:
        case = json.loads(Path(args.case).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read {args.case}: {exc}", file=sys.stderr)
        return 2

    findings = audit(case)
    errors = [f for f in findings if f.severity == "error"]
    for finding in findings:
        print(f"{finding.severity.upper()}: {finding.code}: {finding.message}")
    print(
        f"{len(errors)} error(s), {len(findings) - len(errors)} warning(s) "
        f"in {case.get('id', 'unknown case')}"
    )
    return 1 if (args.check and errors) else 0


if __name__ == "__main__":
    raise SystemExit(main())
