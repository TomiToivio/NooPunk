"""The reference console adapter: play a case with nothing but a terminal.

Two modes, one code path:

* interactive (``python scripts/noopunk_case.py``), reading commands from stdin;
* scripted (``--script beats.txt``), which is how the tests and the tabletop walkthrough drive the
  same session deterministically.

Every command prints one line per outcome and never hides a rule behind prose: a clue granted, a
refused move, a roll's dice and total. The console is a *reference* adapter -- if a rule needs
explaining, the sentence belongs in `docs/PORTABLE_CONSOLE_CASE.md`, not invented here.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rules.investigation import InvestigationError, Investigator, load_case_graph

from .session import CaseSession, SessionError, load_session

DEFAULT_CASE = "data/scenarios/lakkahaltia/case_graph.json"

HELP = """\
Commands
  look                     look around; declare a search for anything that needs one
  go <scene>               move through a discovered lead
  clues                    what you have found so far
  take <clue>              examine a clue you have not been handed yet
  support <clue>           read a clue as supporting your current theory
  contradict <clue>        read a clue as contradicting your current theory
  neutral <clue>           read a clue as not bearing on it
  theory <hypothesis>      state which hypothesis you are working on
  hypotheses               list the hypotheses this case allows
  risk <difficulty> [skill]  a CWN 2d6 check under pressure (difficulty 8, 10 or 12)
  goal <owner> <horizon> <text>   add a Goal tag (short|medium|long); faction:<name> for a faction
  goals                    the active goal tags, as they read on paper
  progress <goal> <kind> <event> [note]  progress|contribution|completed|failed|abandoned
  award <goal> <event>     pay the CWN XP for a recorded completion or contribution
  status                   scene, theory, evidence counts, turns
  conclude <hypothesis> [note]  record your answer; the case ends
  save [path] | load <path>     portable JSON state
  help | quit\
"""


def _clue_line(clue) -> str:
    return f"  [{clue.id}] {clue.fact}"


def _print_scene(session: CaseSession, out) -> None:
    scene = session.scene()
    print(f"\n== {scene.title} ({scene.id})", file=out)
    for clue_id in session.open_clues():
        print(_clue_line(session.clue(clue_id)), file=out)
    exits = session.exits()
    print(f"  leads: {', '.join(exits) if exits else 'none yet'}", file=out)


def build_session(args: argparse.Namespace) -> CaseSession:
    graph = load_case_graph(args.case)
    if args.load:
        return load_session(graph, args.load)
    try:
        ratings = {name: int(rank) for name, rank in
                   (skill.split("=", 1) for skill in args.skill)}
    except ValueError as exc:
        raise SessionError("--skill wants name=rank, e.g. --skill Notice=2") from exc
    if not ratings:
        # An investigator who holds no competency cannot leave any scene; the shortest competent
        # sheet that reaches the whole case is the one the walkthrough uses.
        ratings = {"Notice": 1, "Talk": 1, "Administer": 1, "Survive": 0, "Heal": 0,
                   "Know": 0, "Connect": 0}
    investigator = Investigator(name=args.name, ratings=ratings)
    return CaseSession.start(graph, investigator, seed=args.seed)


def run_command(session: CaseSession, line: str, *, save_path: str = "") -> tuple[bool, str]:
    """Execute one command. Returns ``(keep_going, output)``.

    Kept separate from printing so the tests can drive the same session without a terminal.
    """
    parts = line.strip().split()
    if not parts or parts[0].startswith("#"):
        return True, ""
    verb, args = parts[0].lower(), parts[1:]

    if verb in ("quit", "exit"):
        return False, "bye"
    if verb == "help":
        return True, HELP
    if verb == "look":
        result = session.look()
        return True, (f"\n== {result['title']} ({result['scene']})\n"
                      + "\n".join(_clue_line(clue) for clue in result["clues"]))
    if verb == "go":
        if not args:
            return True, "go needs a scene id"
        result = session.travel(args[0])
        return True, f"-> {result['title']} ({result['scene']})"
    if verb == "clues":
        if not session.discovered:
            return True, "nothing found yet"
        return True, "\n".join(_clue_line(session.clue(clue_id)) for clue_id in session.discovered)
    if verb == "take":
        if not args:
            return True, "take needs a clue id"
        clue = session.take(args[0])
        return True, _clue_line(clue)
    if verb in ("support", "contradict", "neutral"):
        if not args:
            return True, f"{verb} needs a clue id"
        if not session.theory_id:
            return True, "state a theory first: theory <hypothesis>"
        stance = {"support": "supports", "contradict": "contradicts", "neutral": "neutral"}[verb]
        result = session.attach(session.theory_id, args[0], stance)
        return True, f"{result['clue']} -> {result['stance']} {result['hypothesis']}"
    if verb == "theory":
        if not args:
            return True, "theory needs a hypothesis id"
        return True, f"working theory: {session.choose_theory(args[0])}"
    if verb == "hypotheses":
        return True, "\n".join(f"  [{h.id}] ({h.family}) {h.statement}" for h in session.graph.hypotheses)
    if verb == "risk":
        if not args:
            return True, "risk needs a difficulty"
        skill = args[1] if len(args) > 1 else ""
        result = session.risk(int(args[0]), skill)
        bonus = f" + {result['rank']} {skill}" if result["rank"] else ""
        verdict = "success" if result["success"] else "failure"
        return True, (f"2d6 {result['dice'][0]}+{result['dice'][1]}{bonus}"
                      f" = {result['total']} vs {result['difficulty']} -> {verdict}")
    if verb == "goal":
        # goal <owner> <horizon> <description...>; prefix the owner with faction: for a faction goal
        if len(args) < 3:
            return True, "goal needs an owner, a horizon (short|medium|long) and a description"
        try:
            result = session.add_goal(args[0], args[1], " ".join(args[2:]))
        except SessionError as exc:
            return True, f"refused: {exc}"
        return True, f"added {result['goal']} ({result['horizon']}) for {result['owner']}"
    if verb == "goals":
        view = session.goals_view()
        if not view["enabled"]:
            return True, "goals are switched off for this campaign"
        if not view["active"]:
            return True, "no active goals"
        lines = [f"  {row['paper']}" for row in view["active"]]
        if view["xp"]:
            lines.append("  xp: " + ", ".join(f"{owner} {xp}" for owner, xp in view["xp"].items()))
        return True, "\n".join(lines)
    if verb == "progress":
        # progress <goal-id> <progress|contribution|completed|failed|abandoned> <event> [note...]
        if len(args) < 3:
            return True, "progress needs a goal id, a kind and the event that evidences it"
        try:
            result = session.record_goal(args[0], args[1], args[2], " ".join(args[3:]))
        except SessionError as exc:
            return True, f"refused: {exc}"
        return True, f"{result['goal']} -> {result['kind']} ({result['status']})"
    if verb == "award":
        if len(args) < 2:
            return True, "award needs a goal id and the event that earned it"
        try:
            result = session.award_goal(args[0], args[1])
        except SessionError as exc:
            return True, f"refused: {exc}"
        return True, (f"awarded {result['xp']} XP to {result['goal']} "
                      f"(level {result['level']} by the CWN table)")
    if verb == "status":
        theory = session.theory_id or "(none)"
        readings = session.evidence.get(session.theory_id, {})
        return True, (f"scene {session.scene_id} | theory {theory} | clues {len(session.discovered)} | "
                      f"readings {len(readings)} | turns {session.turns} | seed {session.seed}")
    if verb == "conclude":
        if not args:
            return True, "conclude needs a hypothesis id"
        note = " ".join(args[1:])
        result = session.conclude(args[0], note)
        return True, (f"recorded: {result['hypothesis']} ({result['family']})\n"
                      f"  supports {result['supports']} · contradicts {result['contradicts']} · "
                      f"unread {result['unread']}\n"
                      f"  {result['verdict']}")
    if verb == "save":
        path = args[0] if args else (save_path or "noopunk-case-save.json")
        written = session.save(path)
        return True, f"saved {written}"
    if verb == "load":
        return True, "load is a start-up option: --load <path>"
    return True, f"unknown command {verb!r}; try help"


def run_opening_command(opening, line: str, *, save_path: str = "") -> tuple[bool, str]:
    """Drive the validated, built opening without making another command resolver.

    This narrow adapter is reusable by an Evennia command or a GUI command box.
    The Opening object alone validates available actions and mutates the session.
    """
    import json
    from .opening import OpeningError

    command = line.strip()
    if not command or command.startswith("#"):
        return True, ""
    verb = command.lower()
    if verb in ("quit", "exit"):
        return False, "bye"
    if verb in ("actions", "help"):
        return True, "Available: " + ", ".join(opening.actions()) + ", status, save [path], quit"
    if verb in ("status", "look"):
        view = opening.view()
        return True, (f"{view['scene']} | {view['location']['label']} | "
                      f"actions: {', '.join(view['actions']) or 'none'} | "
                      f"missing kit: {', '.join(view['equipment']['missing']) or 'none'}")
    if verb == "save" or verb.startswith("save "):
        target = command.split(None, 1)[1] if " " in command.strip() else (
            save_path or "noopunk-opening-save.json"
        )
        Path(target).write_text(
            json.dumps(opening.save(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return True, f"saved {target}"
    if verb.startswith("load"):
        return True, "load at startup: --opening --load <path>"
    try:
        return True, opening.act(verb)
    except OpeningError as exc:
        return True, f"refused: {exc}"


def run_opening(args: argparse.Namespace) -> int:
    """Resume a *built* officer. Never fabricate a background or Edge catalogue."""
    import json
    from .opening import Opening, OpeningError

    if not args.load:
        print("opening requires --load <validated opening save>; "
              "published Background/Edge catalogues are not yet available", file=sys.stderr)
        return 2
    try:
        opening = Opening.load(json.loads(Path(args.load).read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, OpeningError) as exc:
        print(f"cannot load opening: {exc}", file=sys.stderr)
        return 2
    print("NoöPunk · Tony German · built opening (mechanical preview)")
    print("Available: " + ", ".join(opening.actions()))
    if args.script:
        try:
            commands = Path(args.script).read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            print(f"cannot open script: {exc}", file=sys.stderr)
            return 2
    else:
        commands = None
    if commands is not None:
        for command in commands:
            keep_going, output = run_opening_command(opening, command, save_path=args.save)
            if output:
                print(output)
            if not keep_going:
                break
    else:
        while True:
            try:
                command = input("> ")
            except EOFError:
                print()
                break
            keep_going, output = run_opening_command(opening, command, save_path=args.save)
            if output:
                print(output)
            if not keep_going:
                break
    if args.save:
        Path(args.save).write_text(
            json.dumps(opening.save(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return 0


def run_first_day_command(session, line: str, *, save_path: str = "") -> tuple[bool, str]:
    """An alternate *mode* of the existing console, not a second game loop.

    The WorldSession remains authoritative for graph position, state and actor ID.
    """
    import json
    from .first_day import first_day_action, available_first_day_actions, FirstDayError

    command = line.strip().lower()
    if not command or command.startswith("#"):
        return True, ""
    if command in ("quit", "exit"):
        return False, "bye"
    if command in ("actions", "help"):
        return True, "Available: " + ", ".join(available_first_day_actions(session)) + (
            ", save [path], status, quit"
        )
    if command == "status":
        return True, (f"{session.scene_id} | {session.where('tony.german')} | "
                      f"equipment steps {sum(flag.startswith('first_day:inspect:') for flag in session.flags)}")
    if command == "save" or command.startswith("save "):
        target = command.split(" ", 1)[1].strip() if " " in command else (
            save_path or "noopunk-first-day-save.json"
        )
        Path(target).write_text(
            json.dumps(session.to_snapshot(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return True, f"saved {target}"
    if command.startswith("load"):
        return True, "load at startup: --first-day --load <path>"
    try:
        return True, first_day_action(session, command)
    except (FirstDayError, SessionError) as exc:
        return True, f"refused: {exc}"


def run_first_day(args: argparse.Namespace) -> int:
    """Use the canonical console's same scripted/interactive command loop."""
    import json
    from .first_day import create_first_day, available_first_day_actions
    from .world_session import WorldSession, WorldSessionError

    try:
        session = (WorldSession.from_snapshot(
            json.loads(Path(args.load).read_text(encoding="utf-8"))
        ) if args.load else create_first_day())
    except (OSError, ValueError, WorldSessionError) as exc:
        print(f"cannot start first day: {exc}", file=sys.stderr)
        return 2

    print("NoöPunk · Tony German · first day (mechanical preview; prose pending Tomi)")
    print("Available: " + ", ".join(available_first_day_actions(session)))
    if args.script:
        try:
            commands = Path(args.script).read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            print(f"cannot open script: {exc}", file=sys.stderr)
            return 2
        for command in commands:
            keep_going, output = run_first_day_command(session, command, save_path=args.save)
            if output:
                print(output)
            if not keep_going:
                break
        if args.save:
            import json
            Path(args.save).write_text(
                json.dumps(session.to_snapshot(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        return 0
    while True:
        try:
            command = input("> ")
        except EOFError:
            print()
            break
        keep_going, output = run_first_day_command(session, command, save_path=args.save)
        if output:
            print(output)
        if not keep_going:
            break
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Play a NoöPunk investigation case in a terminal")
    parser.add_argument("--opening", action="store_true",
                        help="resume a validated built-character opening (requires --load)")
    parser.add_argument("--first-day", action="store_true",
                        help="play Tony German's mechanical first-day preview")
    parser.add_argument("--case", default=DEFAULT_CASE, help="case graph JSON")
    parser.add_argument("--name", default="Etsivä Romppainen", help="investigator name")
    parser.add_argument("--skill", action="append", default=[],
                        help="skill=rank, repeatable; defaults to a competent starting sheet")
    parser.add_argument("--seed", type=int, default=7,
                        help="dice seed; the same seed and the same commands replay exactly")
    parser.add_argument("--load", default="", help="resume a saved session")
    parser.add_argument("--save", default="", help="path used by the plain `save` command")
    parser.add_argument("--script", default="", help="run commands from a file instead of stdin")
    args = parser.parse_args(argv)

    if args.opening and args.first_day:
        parser.error('--opening and --first-day are mutually exclusive')
    if args.opening:
        return run_opening(args)
    if args.first_day:
        return run_first_day(args)

    try:
        session = build_session(args)
    except (SessionError, InvestigationError, OSError) as exc:
        print(f"cannot start: {exc}", file=sys.stderr)
        return 2

    print(f"NoöPunk case console · {session.graph.case.id} · seed {session.seed}")
    _print_scene(session, sys.stdout)

    if args.script:
        script = Path(args.script).read_text(encoding="utf-8").splitlines()
        for line in script:
            keep_going, output = run_command(session, line, save_path=args.save)
            if output:
                print(output)
            if not keep_going:
                break
        if args.save:
            print(f"saved {session.save(args.save)}")
        return 0

    while True:
        try:
            line = input("> ")
        except EOFError:
            print()
            break
        keep_going, output = run_command(session, line, save_path=args.save)
        if output:
            print(output)
        if not keep_going:
            break
    return 0
