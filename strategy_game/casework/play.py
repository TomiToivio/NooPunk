"""Play the packaged case by hand: ``python -m strategy_game.casework.play``.

The headless demo (:mod:`strategy_game.casework.demo`) plays *one* fixed route through the
packaged case, so the five-scene case is reachable but not *playable*: a person at the table
cannot take an action, see why an action is refused, or decide when to end a scene.

This module is that missing surface. It drives the same :class:`~strategy_game.casework.session.CaseSession`
the demo drives, with the same refusal semantics, the same engine and the same save file — it
adds a human at the keyboard, and no rule of its own.

Three commands do the work:

* ``act <seat> <action>`` — attempt one action with one character. A refusal is reported with its
  reason and costs nothing, exactly as :meth:`CaseSession.act` returns it.
* ``end`` — end the current scene and move to the next.
* ``resolve <investigate|confront|refer>`` — close the case and write it into the campaign.

Everything else is display: the scene, who may act, what is available and what is refused and why.
The availability verdict shown is the session's own (:meth:`CaseSession.actions`), so the CLI
never offers something the session will refuse.

This is the **authored scenario content** of the packaged case and it is *not canon*: the frame
(2045, the Quarantine in force, the old Internet behind the Blackwall) is canon, the case, its
people and its events are not.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Callable

from .kallio import CASE, build_session
from .session import CaseSession, load_session
from .spec import CaseSpecError, band_difficulty

#: How the case may be closed. The ids are the session's own resolution ids.
RESOLUTIONS = ("closed_by_evidence", "closed_by_confrontation", "closed_by_withdrawal")

#: What each resolution id means in the player's own terms, so the choice is legible.
RESOLUTION_HELP = {
    "closed_by_evidence": "close it on the assembled evidence",
    "closed_by_confrontation": "close it by confronting the second figure (words or force)",
    "closed_by_withdrawal": "close it by referral: the file goes upstairs as it stands",
}

#: The approaches the confrontation resolution accepts.
APPROACHES = ("pressure", "force")


def _rule(char: str = "─") -> str:
    return char * 72


def _scene_header(session: CaseSession) -> str:
    spec = session.scene_spec
    index = session.spec.scene_index(spec.id) + 1
    total = len(session.spec.scenes)
    return f"[{index}/{total}] {spec.title} — {spec.location}"


def _print_scene(session: CaseSession) -> None:
    spec = session.scene_spec
    print(_rule())
    print(_scene_header(session))
    print(_rule())
    for line in spec.prose.splitlines():
        print(line)
    print()


def _print_party(session: CaseSession) -> None:
    print("Party (the seat id is what `act` takes):")
    for seat in session.seats:
        sheet = session.sheet(seat.id)
        acted = seat.id in session.ledger.acted
        mark = "acted" if acted else "ready"
        print(f"  {seat.id:12} {sheet.name:26} {mark}")
    print()


def _print_actions(session: CaseSession) -> None:
    actions = session.actions()
    if not actions:
        print("No actions in this scene.")
        print()
        return
    print("Actions:")
    for action in actions:
        if action["available"]:
            who = action.get("suggested_actor") or "anyone"
            # The band is a Fate difficulty word; the number behind it is what a check is
            # resolved against, so show both.
            band = action.get("band") or ""
            skill = action.get("skill") or ""
            if band:
                try:
                    difficulty = band_difficulty(band)
                    where = f"{skill} {band}({difficulty})" if skill else f"{band}({difficulty})"
                except CaseSpecError:
                    where = skill or band
            else:
                where = skill or "no check"
            print(f"  {action['id']:28} [{where:16}] (suggested: {who}) — {action['label']}")
        else:
            print(f"  {action['id']:28} refused: {action['reason']}")
    print()


def _print_state(session: CaseSession) -> None:
    clues = session.clues
    intel = session.intel
    findings = session.findings
    print(f"Turn {session.turn} | clues {len(clues)} | intel {len(intel)} | findings {len(findings)}")
    if clues:
        print(f"  clues:    {', '.join(clues)}")
    if intel:
        print(f"  intel:    {', '.join(intel)}")
    if findings:
        print(f"  findings: {', '.join(findings)}")
    complications = session.complications
    if complications:
        print(f"  costs:    {', '.join(complications)}")
    wounds = session.wounds
    if wounds:
        print(f"  wounds:   {len(wounds)}")
    print()


def _print_result(result, session: CaseSession) -> None:
    if not result.ok:
        print(f"  refused: {result.reason}")
        print()
        return
    parts: list[str] = []
    if result.skill:
        dice = "".join(f"{value:+d}" for value in result.dice)
        outcome = result.outcome.value if result.outcome else ""
        parts.append(f"{result.skill} vs {result.difficulty} [{dice}] = {result.total} → {outcome}")
    if result.clues:
        parts.append(f"clue(s) {', '.join(result.clues)}")
    if result.intel:
        parts.append(f"intel {', '.join(result.intel)}")
    if result.aspect:
        parts.append(f"aspect {result.aspect!r}")
    if result.costs:
        parts.append(f"cost: {', '.join(result.costs)}")
    if result.complications:
        parts.append(f"complication: {', '.join(result.complications)}")
    if result.consequence:
        parts.append(f"consequence: {result.consequence}")
    if result.taken_out:
        parts.append("taken out")
    print(f"  {result.seat_id}/{result.action_id}: " + ("; ".join(parts) if parts else "done"))
    print()


def _print_resolution(resolution) -> None:
    print(_rule())
    print(f"{resolution.label}: {resolution.outcome.value}")
    if resolution.detail:
        print(resolution.detail)
    if resolution.degraded:
        print("  (the attempt fell back to a referral: the case ends on the weaker record)")
    for wound in resolution.wounds:
        print(f"  wound: {wound}")
    print(_rule())


def _print_help() -> None:
    print("Commands:")
    print("  act <seat> <action>        attempt one action with one character")
    print("  end                        end the current scene")
    print("  resolve <id> [approach]    close the case (see the ids below)")
    print("  state                      show clues, intel, findings and costs")
    print("  save [path]                write the save file now")
    print("  help                       this list")
    print("  quit                       leave without resolving")
    print()
    print("Resolutions:")
    for name in RESOLUTIONS:
        print(f"  {name:24} {RESOLUTION_HELP[name]}")
    print(f"  (the confrontation takes an approach: {', '.join(APPROACHES)})")
    print()


def _run(
    session: CaseSession,
    save_path: Path | None,
    reader: Callable[[str], str],
) -> int:
    """The read-eval loop. Returns the process exit status.

    ``reader`` is how the next line of input arrives. It is a parameter rather than a direct
    ``input()`` call so the loop can be driven by a test without patching the interpreter's
    builtins, and so a future renderer can supply its own reader.
    """
    print(_rule())
    print("NoöPunk / The Second Shadow — an interactive case")
    print("Authored scenario content. Not canon.")
    print(_rule())
    _print_scene(session)
    _print_party(session)
    _print_actions(session)
    _print_state(session)
    _print_help()

    while True:
        try:
            raw = reader("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Left without resolving. Nothing was decided; the save file holds the case as far as it got.")
            return 0
        if not raw:
            continue
        parts = raw.split()
        command = parts[0].lower()

        if command in {"help", "?"}:
            _print_help()
            continue
        if command in {"quit", "exit", "q"}:
            print("Left without resolving.")
            return 0
        if command == "state":
            _print_state(session)
            continue
        if command == "save":
            target = save_path or (Path.cwd() / "noopunk-case-kallio.json")
            written = session.save(target)
            print(f"Saved to {written}")
            continue
        if command == "end":
            if session.finished:
                print("  the case is already closed")
                continue
            try:
                following = session.end_scene()
            except ValueError as exc:
                print(f"  refused: {exc}")
                continue
            if following is None or session.finished:
                print("  the case is closed")
                _print_state(session)
                continue
            print()
            _print_scene(session)
            _print_party(session)
            _print_actions(session)
            _print_state(session)
            continue
        if command == "act":
            if len(parts) < 3:
                print("  usage: act <seat> <action>")
                continue
            seat_id, action_id = parts[1], parts[2]
            try:
                result = session.act(seat_id, action_id)
            except ValueError as exc:
                print(f"  refused: {exc}")
                continue
            _print_result(result, session)
            if result.scene_changed:
                print(f"  -> the scene changed: {result.scene_changed}")
                print()
                _print_scene(session)
                _print_party(session)
                _print_actions(session)
            _print_state(session)
            continue
        if command == "resolve":
            if len(parts) < 2:
                print("  usage: resolve <id> [approach]")
                _print_help()
                continue
            resolution_id = parts[1]
            if resolution_id not in RESOLUTIONS:
                print(f"  unknown resolution {resolution_id!r}; see `help`")
                continue
            approach = parts[2] if len(parts) > 2 else ""
            if resolution_id == "closed_by_confrontation" and approach not in APPROACHES:
                print(f"  the confrontation needs an approach: {', '.join(APPROACHES)}")
                continue
            try:
                resolution = session.resolve(resolution_id, seat_id="pc_leader", approach=approach)
            except ValueError as exc:
                # The session refuses a resolution it is not ready for (an unassembled finding,
                # a missing approach). A refusal is an answer, not a crash.
                print(f"  refused: {exc}")
                continue
            _print_resolution(resolution)
            _print_state(session)
            if save_path is not None:
                written = session.save(save_path)
                print(f"Saved to {written}")
            print("The case is closed. The saved event ledger can feed later strategic adapters.")
            return 0
        print(f"  unknown command {command!r}; `help` lists them")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m strategy_game.casework.play",
        description=(
            "Play the packaged case by hand (issue #502's RPG-first vertical slice). The same "
            "session, the same engine and the same refusals as the headless demo, with a human "
            "at the keyboard."
        ),
    )
    parser.add_argument(
        "--save",
        default=None,
        help="where to write the save file (default: ./noopunk-case-kallio.json)",
    )
    parser.add_argument(
        "--load",
        default=None,
        help="resume a saved session instead of starting the case",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=502,
        help="dice seed for the session (default: 502, the case's own)",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="print the first scene and the available actions, then leave (no input)",
    )
    args = parser.parse_args(argv)

    save_path = Path(args.save) if args.save else Path.cwd() / "noopunk-case-kallio.json"

    try:
        if args.load:
            session = load_session(args.load, CASE)
            print(f"Resumed {args.load}.")
        else:
            session = build_session(seed=args.seed)
    except (OSError, ValueError) as exc:
        print(f"could not open the case: {exc}", file=sys.stderr)
        return 2

    if args.non_interactive:
        print("Authored scenario content. Not canon.")
        _print_scene(session)
        _print_party(session)
        _print_actions(session)
        _print_state(session)
        return 0

    return _run(session, save_path, input)


if __name__ == "__main__":
    raise SystemExit(main())
