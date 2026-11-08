"""Static soundness audit for a detective case (#1310).

`tests/test_detective_adventure_1310.py` walks one path by hand. This answers the question that
actually matters for P5 — *can this case be finished at all, and can any clue be locked away?* — for
every scene and every ending, without playing it.

The model is exact rather than approximate because clue acquisition is **monotone**: a clue, once
added, is never removed, so a fixed point over "which scenes are reachable with the clues I can
already have" is the full set of reachable scenes. A gate whose clues are unobtainable therefore
shows up as an unreachable scene, which is precisely the softlock.

Run:

    python3 NooPunk-Simulator/Code/case_audit.py                       # the shipped development case
    python3 NooPunk-Simulator/Code/case_audit.py --case path/case.json

Exit codes: 0 sound, 1 findings printed, 2 the case could not be read.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

#: `Code/` is a directory of standalone scripts, not a package (the path contains a hyphen), so the
#: runner is imported as a sibling module rather than through the filesystem dance a package needs.
_CODE_DIR = Path(__file__).resolve().parent
if str(_CODE_DIR) not in sys.path:
    sys.path.insert(0, str(_CODE_DIR))

import adventure

__all__ = ["audit", "main", "reachable"]


def reachable(case):
    """Every scene that can be entered and every clue that can be collected, as a fixed point."""
    scenes = {case["start"]}
    clues = set()
    grown = True
    while grown:
        grown = False
        for scene_id in sorted(scenes):
            for choice in case["scenes"][scene_id]["choices"]:
                if not set(choice.get("requires", [])).issubset(clues):
                    continue
                if choice["to"] not in scenes:
                    scenes.add(choice["to"])
                    grown = True
                for clue in choice.get("adds", []):
                    if clue not in clues:
                        clues.add(clue)
                        grown = True
    return scenes, clues


def ending_reachable_without(case, ending, clue, limit=20000):
    """Is there a route to ``ending`` that never picks up ``clue``?

    This is the softlock question, and it has to be answered path by path. The reachability fixed point above
    answers the opposite question — "can this clue ever be collected" — and would let a shortcut pass: a case
    where *some* route collects the evidence and *another* route skips it looks sound to a union, and strands
    the player in a story they cannot honestly finish.
    """
    scenes = case.get("scenes", {})
    start = case.get("start", "")
    if start not in scenes or ending not in scenes:
        return False
    seen = set()
    frontier = [(start, frozenset(scenes[start].get("adds", [])))]
    visited = 0
    while frontier:
        scene_id, carried = frontier.pop()
        visited += 1
        if visited > limit:  # pragma: no cover - a case this large is its own design problem
            return False
        state = (scene_id, carried)
        if state in seen:
            continue
        seen.add(state)
        if scene_id == ending and clue not in carried:
            return True
        for choice in scenes[scene_id].get("choices", []):
            target = choice.get("to")
            if target not in scenes:
                continue
            if not set(choice.get("requires", [])).issubset(carried):
                continue
            frontier.append((target, frozenset(carried | set(choice.get("adds", [])))))
    return False


def audit(case):
    """Findings that would strand a player. An empty list means the case is finishable as written."""
    findings = []
    scenes, clues = reachable(case)
    endings = [scene_id for scene_id, scene in case["scenes"].items() if scene.get("ending")]

    if not endings:
        findings.append("case has no ending: it cannot be finished")

    for scene_id, scene in case["scenes"].items():
        if scene_id not in scenes:
            findings.append(
                f"scene {scene_id!r} is unreachable: no satisfiable path leads to it "
                "(a gate whose clues cannot be collected is a softlock)"
            )
        if not scene.get("ending") and not scene.get("choices"):
            findings.append(f"scene {scene_id!r} is neither an ending nor offers a choice")

    for scene_id in endings:
        if scene_id not in scenes:
            findings.append(f"ending {scene_id!r} can never be reached")
    if endings and not any(scene_id in scenes for scene_id in endings):
        findings.append("no ending is reachable: the investigation cannot be closed")

    for clue in case.get("clues", {}):
        if clue not in clues:
            findings.append(f"clue {clue!r} can never be collected")

    for hypothesis_id, hypothesis in zip(adventure.hypothesis_ids(case),
                                         case.get("hypotheses", [])):
        if not set(hypothesis.get("requires", [])).issubset(clues):
            findings.append(
                f"hypothesis {hypothesis_id!r} can never become available: its evidence is unobtainable"
            )

    for index, contradiction in enumerate(case.get("contradictions", [])):
        contradiction_id = str(contradiction.get("id") or "c" + str(index + 1))
        if not set(contradiction.get("between", [])).issubset(clues):
            findings.append(
                f"contradiction {contradiction_id!r} can never surface: its evidence is unobtainable"
            )

    for clue in case.get("essential_clues", []):
        if clue not in case.get("clues", {}):
            findings.append(f"essential_clues names unknown clue {clue!r}")
            continue
        for ending in endings:
            if ending not in scenes:
                continue
            if ending_reachable_without(case, ending, clue):
                findings.append(
                    f"ending {ending!r} can be reached without essential clue {clue!r}: "
                    "that route ends the case with the player unable to justify it"
                )

    return findings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Static soundness audit for a detective case (#1310)")
    parser.add_argument("--case", type=Path, default=adventure.DEFAULT_CASE, help="case JSON to audit")
    arguments = parser.parse_args(argv)
    try:
        case = adventure.load_case(arguments.case)
    except (OSError, ValueError, TypeError) as error:
        print(f"case-audit: cannot read {arguments.case}: {error}", file=sys.stderr)
        return 2

    findings = audit(case)
    scenes, clues = reachable(case)
    endings = sum(1 for scene in case["scenes"].values() if scene.get("ending"))
    if findings:
        print(f"case-audit: {len(findings)} finding(s) in {arguments.case}:", file=sys.stderr)
        for finding in findings:
            print("  " + finding, file=sys.stderr)
        return 1
    print(f"case-audit: sound — {len(scenes)}/{len(case['scenes'])} scenes reachable, "
          f"{len(clues)}/{len(case.get('clues', {}))} clues obtainable, {endings} ending(s), "
          f"no softlock")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
