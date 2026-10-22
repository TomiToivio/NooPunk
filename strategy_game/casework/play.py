"""Interactive terminal play for the packaged case (issue #502's vertical slice).

``python -m strategy_game.casework --play`` sits a human down in front of *The Second Shadow*: the
five scenes, the five seats, the clue chain and the three endings, one command at a time.

This module is a **front end, not an engine**. It owns no rule and computes no number:

* what may be attempted, and whether it may be attempted, comes from
  :meth:`strategy_game.casework.session.CaseSession.actions` and
  :meth:`~strategy_game.casework.session.CaseSession.resolutions` — the session's own verdicts, so the
  CLI cannot offer something ``act`` would refuse;
* the party, the clues, the chain, the complications, the wounds and the campaign books come from
  :meth:`~strategy_game.casework.session.CaseSession.report`;
* every transition is :meth:`~strategy_game.casework.session.CaseSession.act`,
  :meth:`~strategy_game.casework.session.CaseSession.end_scene` and
  :meth:`~strategy_game.casework.session.CaseSession.resolve`;
* saving is :meth:`~strategy_game.casework.session.CaseSession.save` and resuming is
  :func:`strategy_game.casework.session.load_session`, dice state included.

The declaration (:mod:`.spec`) supplies what the *reader* needs and the engine never has to: the
scene's prose, an action's label and outcome text, the Fate band an action is rolled against (the
case's own :data:`~.spec.DIFFICULTY_BANDS`), the clue labels, and the declared tie/failure prices.

The player is the **faction leader** (#502): they hold the leader's own seat, assign any of the four
agents to any action, choose the method when a closing decision is a confrontation, and take the
closing decision itself. Nothing is locked to a character — that is the session's rule, not this
CLI's — so assignment is a choice about who is where, never a gate.

Determinism
-----------
``--seed`` fixes the dice exactly as it does headless. With no ``--seed`` the session uses its own
default seed (:data:`~.session.DEFAULT_SEED`), and either way the save carries
``Random.getstate()``, so an interrupted morning resumes into the rolls it would have had.

    python -m strategy_game.casework --play
    python -m strategy_game.casework --play --seed 77 --save /tmp/kallio-save.json
    python -m strategy_game.casework --play --save /tmp/kallio-save.json   # resumes that morning
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..rpg.skills import individual_skill
from . import kallio
from .demo import APPROACHES, _action, _scene_entry, _wrap, case_summary, render_text
from .session import (
    DEFAULT_SEED,
    ActionResult,
    CaseSession,
    CaseworkError,
    load_session,
)
from .spec import ActionSpec, CaseSpecError, Cost, ResolutionSpec

__all__ = ["COMMANDS", "DEFAULT_SAVE", "PlayOutcome", "play", "render_menu", "render_scene"]

#: Where a played morning is kept when the player names no file. The same file resumes it.
DEFAULT_SAVE = "noopunk-case-save.json"

#: Every command the prompt accepts, in the order the menu prints them.
COMMANDS: tuple[tuple[str, str], ...] = (
    ("act <seat> <action>", "send one character into one of the scene's actions"),
    ("party", "the five seats, their fate points, stress and consequences"),
    ("status", "the scene, the clues in hand and the chain's progress"),
    ("next", "leave the scene early; every seat refreshes in the next one"),
    ("resolve <ending> [pressure|force] [seat]", "take the closing decision"),
    ("approach [pressure|force]", "set the method you will use if you confront him"),
    ("save", "write the case to the save file"),
    ("quit", "save and leave"),
)

#: Read one line from the player; :func:`input` in a terminal, a script in a test.
Read = Callable[[str], str]
#: Write one line to the player; :func:`print` in a terminal, a list in a test.
Write = Callable[[str], None]


@dataclass
class PlayOutcome:
    """What one interactive sitting produced: the session, the record, and why it stopped."""

    session: CaseSession | None = None
    log: list[dict[str, Any]] = field(default_factory=list)
    record: dict[str, Any] | None = None
    transcript: list[str] = field(default_factory=list)
    exit_reason: str = ""
    save_path: Path | None = None


# -- small readers over the session's own view ---------------------------------


def _name(session: CaseSession, reference: str) -> str:
    """A seat's character name, as the campaign's sheet writes it ("You" for the leader).

    ``reference`` may be a seat id or a character id; both name the same person.
    """
    try:
        seat_id = session.seat_for(reference).id
    except CaseworkError:  # pragma: no cover - callers pass a seat they just resolved
        return reference
    for member in session.report()["party"]:
        if member["seat"] == seat_id:
            return str(member["name"])
    return seat_id


def _skill_label(skill: str) -> str:
    return individual_skill(skill).name


def _check_text(action: ActionSpec) -> str:
    """An action's check as a player reads it: the skill, the Fate band and the band's number."""
    if action.check is None:
        return "no dice — the deduction is the action itself"
    return f"{_skill_label(action.check.skill)} {action.check.band} ({action.check.difficulty})"


def _cost_text(cost: Cost) -> str:
    """One declared price, in the case file's own vocabulary."""
    parts: list[str] = []
    if cost.complications:
        parts.append("complication " + ", ".join(f"'{item}'" for item in cost.complications))
    if cost.stress:
        parts.append(f"{cost.stress} {'mental' if cost.mental else 'physical'} stress")
    if cost.consequence:
        parts.append(f"consequence '{cost.consequence}'")
    return "; ".join(parts) or "nothing"


def _clue_label(session: CaseSession, clue_id: str) -> str:
    try:
        return session.spec.clue(clue_id).label
    except CaseSpecError:  # pragma: no cover - the declaration validates its clue ids
        return clue_id


def _yield_text(session: CaseSession, action: ActionSpec) -> str:
    """What an action gives the party, by the declaration's own labels."""
    parts: list[str] = []
    if action.gives:
        parts.append(
            "clue " + ", ".join(f"'{_clue_label(session, clue)}'" for clue in action.gives)
        )
    if action.aspect:
        parts.append(f"aspect '{action.aspect}'")
    if action.finding:
        parts.append(f"conclusion '{session.spec.finding(action.finding).label}'")
    return "; ".join(parts) or "nothing the case records"


def _party_block(session: CaseSession) -> str:
    """The five seats as the campaign holds them — stress and consequences included."""
    lines = ["", "The party"]
    for member in session.report()["party"]:
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
    return "\n".join(lines)


def _status_block(session: CaseSession) -> str:
    """What the case knows so far, read off the session's report."""
    report = session.report()
    held = ", ".join(f"'{_clue_label(session, clue)}'" for clue in session.clues) or "nothing yet"
    lines = [
        "",
        f"Scene: {session.scene_spec.title} (turn {session.turn})",
        f"Clues in hand: {held}",
        f"Chain: {report['chain']['held']} of {report['chain']['of']} fragments",
    ]
    if report["findings"]:
        lines.append(
            "Assembled: "
            + ", ".join(
                f"{session.spec.finding(item['id']).label}"
                + (" (partial)" if item["partial"] else "")
                for item in report["findings"]
            )
        )
    if session.complications:
        lines.append("Complications carried: " + ", ".join(session.complications))
    return "\n".join(lines)


def render_scene(session: CaseSession) -> str:
    """The scene as the player meets it: number, title, place, and the case's own prose."""
    scene = session.scene_spec
    index = session.spec.scene_index(scene.id) + 1
    lines = [
        "",
        f"[{index}/{len(session.spec.scenes)}] {scene.title} — {scene.location}",
        _wrap(scene.prose),
        "",
    ]
    ready = [seat.id for seat in session.seats if seat.id in session.seats_available()]
    lines.append(
        "  Ready: "
        + (", ".join(_name(session, seat) for seat in ready) or "nobody — the turn is spent")
    )
    spent = session.acted()
    if spent:
        lines.append(
            "  Already acted: "
            + ", ".join(
                f"{_name(session, seat)} ({statement})" for seat, statement in spent.items()
            )
        )
    return "\n".join(lines)


def render_menu(session: CaseSession) -> str:
    """The scene's actions, exactly as the session reports their availability.

    Every line is read off :meth:`CaseSession.actions` and the declaration: the action's own label,
    the check the session will roll, the clue the declaration says it yields, and the price the
    declaration puts on a tie and on a failure. A locked action keeps its line and carries the
    session's reason, so the player is never offered something ``act`` would refuse.
    """
    specs = {action.id: action for action in session.scene_spec.actions}
    lines = ["", "  What can be attempted:"]
    for number, entry in enumerate(session.actions(), start=1):
        action = specs[entry["id"]]
        lines.append(f"   {number}) {action.label}")
        if not entry["available"]:
            lines.append(f"      locked — {entry['reason']}")
            continue
        detail = _check_text(action)
        actor = entry["suggested_actor"] or session.campaign.leader_id
        try:
            sheet = session.sheet(actor)
        except CaseworkError:  # pragma: no cover - suggested actors are on the campaign
            sheet = None
        if sheet is not None and action.check is not None:
            rated = sheet.skills.get(action.check.skill, 0)
            detail += f" · {_name(session, session.seat_for(actor).id)}: {rated}"
        lines.append(f"      {detail} · yields {_yield_text(session, action)}")
        prices: list[str] = []
        if not action.on_tie.empty:
            prices.append(f"tie: {_cost_text(action.on_tie)}")
        if not action.on_fail.empty:
            prices.append(f"fail: {_cost_text(action.on_fail)}")
        if prices:
            lines.append("      price — " + " · ".join(prices))
    return "\n".join(lines)


def render_endings(session: CaseSession) -> str:
    """The ways out the case offers, with the session's verdict on each."""
    lines = ["", "  Endings:"]
    for number, entry in enumerate(session.resolutions(), start=1):
        spec = session.spec.resolution(entry["id"])
        if not entry["available"]:
            lines.append(f"   {number}) {spec.label} — not yet: {entry['reason']}")
            continue
        method = (
            f"; opposed by {session.character(spec.opposed_by).name} (pressure or force)"
            if spec.opposed_by
            else ""
        )
        needs: list[str] = []
        if spec.requires_finding:
            needs.append(
                f"the assembled finding '{session.spec.finding(spec.requires_finding).label}'"
            )
        if spec.requires:
            needs.append(
                "in hand: "
                + ", ".join(f"'{_clue_label(session, clue)}'" for clue in spec.requires)
            )
        if spec.requires_fragments:
            needs.append(f"{spec.requires_fragments} chain fragments")
        lines.append(
            f"   {number}) {spec.label} — {_skill_label(spec.skill)} {spec.band} "
            f"({spec.difficulty}){method}"
        )
        lines.append(
            "      needs " + ("; ".join(needs) if needs else "nothing the case requires")
            + f" · writes: {spec.objective}"
        )
    return "\n".join(lines)


def _commands_block() -> str:
    return "\n".join(
        ["", "  Commands:"]
        + [f"   {usage:43s}{description}" for usage, description in COMMANDS]
    )


def render_outcome(
    session: CaseSession, action: ActionSpec, seat_id: str, result: ActionResult
) -> str:
    """What the attempt produced: the case's own outcome prose, then the dice and the price."""
    lines = ["", f"{_name(session, seat_id)} — {action.label}", _wrap(action.text)]
    if action.check is not None:
        dice = "".join(f"{value:+d}" for value in result.dice)
        outcome = result.outcome.value if result.outcome else ""
        lines.append(
            f"  {_skill_label(action.check.skill)} {action.check.band} "
            f"({action.check.difficulty}): [{dice}] = {result.total} · {outcome}"
        )
    else:
        lines.append("  no dice — the deduction is the action.")
    gained: list[str] = []
    if result.clues:
        gained.append(
            "clue "
            + ", ".join(f"'{_clue_label(session, clue)}'" for clue in result.clues)
        )
    if result.intel:
        gained.append("intel " + ", ".join(result.intel))
    if result.aspect:
        free = session.scene.aspects[result.aspect].free_invocations
        gained.append(f"aspect '{result.aspect}' ({free} free invocation(s))")
    if gained:
        lines.append("  gained: " + "; ".join(gained))
    if result.costs:
        lines.append("  cost: " + "; ".join(result.costs))
    if result.taken_out:
        lines.append("  taken out — the word the sheet carries, and the case goes on")
    if action.finding and result.reason:
        lines.append("  " + result.reason)
    return "\n".join(lines)


# -- command tokens ------------------------------------------------------------


def _seat_token(session: CaseSession, token: str):
    """A seat by seat id, character id, party number, ``pc``/``leader``, or a unique name fragment.

    The seats' own ids are ``leader``/``agent_1``..; players type ``harri`` or ``laura_univaara``,
    so a fragment that matches exactly one seat or character is accepted and an ambiguous one names
    its candidates instead of guessing.
    """
    known = {seat.id for seat in session.seats} | {seat.character_id for seat in session.seats}
    if token in known:
        return session.seat_for(token)
    if token.lower() in ("pc", "leader", "you"):
        return session.seat_for(session.campaign.leader_id)
    if token.isdigit():
        index = int(token)
        if 1 <= index <= len(session.seats):
            return session.seats[index - 1]
    needle = token.lower()
    matches = [
        seat
        for seat in session.seats
        if needle in seat.character_id.lower() or needle in _name(session, seat.id).lower()
    ]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise CaseworkError(
            f"{token!r} matches {', '.join(seat.character_id for seat in matches)}; "
            "say which one"
        )
    raise CaseworkError(
        f"no seat {token!r}; the seats are "
        + ", ".join(f"{index}={seat.character_id}" for index, seat in enumerate(session.seats, 1))
    )


def _action_token(session: CaseSession, token: str) -> ActionSpec:
    actions = session.scene_spec.actions
    if token.isdigit():
        index = int(token)
        if 1 <= index <= len(actions):
            return actions[index - 1]
        raise CaseworkError(f"this scene lists no action {index}; it offers 1..{len(actions)}")
    return session.scene_spec.action(token)


def _ending_token(session: CaseSession, token: str) -> ResolutionSpec:
    resolutions = session.spec.resolutions
    if token.isdigit():
        index = int(token)
        if 1 <= index <= len(resolutions):
            return resolutions[index - 1]
        raise CaseworkError(f"this case has no ending {index}; it offers 1..{len(resolutions)}")
    return session.spec.resolution(token)


def _resolution_entry(result) -> dict[str, Any]:
    """The log entry for a closing decision, in the shape the headless report writes."""
    return {
        "kind": "resolution",
        "text": f"{result.label}: {result.outcome.value}"
        + (f" — {result.detail}" if result.detail else ""),
        "resolution": result.resolution_id,
        "requested": result.resolution_id,
        "degraded": result.degraded,
        "outcome": result.outcome.value,
    }


# -- the loop ------------------------------------------------------------------


def play(
    *,
    seed: int | None = None,
    save_to: str | Path | None = None,
    resume: bool = True,
    read: Read = input,
    write: Write = print,
) -> PlayOutcome:
    """Play the packaged case from a terminal, or from a script that stands in for one.

    ``read`` and ``write`` are the only I/O; everything else is the session. The case is saved after
    every action and on the way out, so an interrupted morning resumes at the decision it stopped on.
    """
    transcript: list[str] = []

    def out(text: str = "") -> None:
        transcript.append(text)
        write(text)

    target = Path(save_to) if save_to is not None else Path(DEFAULT_SAVE)
    seed_used = DEFAULT_SEED if seed is None else int(seed)
    resumed = bool(resume and target.exists())

    if resumed:
        try:
            session = load_session(target, kallio.CASE)
        except CaseworkError as exc:
            out(f"case refused: {exc}")
            out("(delete the save file or pass --new to start a fresh morning)")
            return PlayOutcome(transcript=transcript, exit_reason="refused", save_path=target)
        out(f"NoöPunk casework — {kallio.CASE.title} ({kallio.CASE.id})")
        out(
            f"Resumed from {target}: {session.scene_spec.title}, turn {session.turn}, "
            f"{session.report()['chain']['held']} of {session.report()['chain']['of']} fragments."
        )
    else:
        session = kallio.build_session(seed=seed_used)
        out(f"NoöPunk casework — {kallio.CASE.title} ({kallio.CASE.id})")
        out(f"{kallio.CASE.era_label}")
        out(f"Question: {kallio.CASE.core_question}")
        out("You are the faction leader; four agents hold the morning with you.")
        out(f"Dice seed {seed_used}. Save file: {target}.")

    outcome = PlayOutcome(session=session, save_path=target, transcript=transcript)
    log = outcome.log
    approach = "pressure"
    shown = ""

    def show_scene() -> None:
        nonlocal shown
        out(render_scene(session))
        log.append(_scene_entry(session))
        shown = session.scene_spec.id

    def save() -> Path:
        return session.save(target)

    def leave(reason: str, note: str = "") -> PlayOutcome:
        path = save()
        if note:
            out("")
            out(note)
        out(f"[saved to {path}]")
        outcome.exit_reason = reason
        return outcome

    def ask(prompt: str) -> str | None:
        try:
            return read(prompt)
        except EOFError:
            return None

    def finish(approach_used: str) -> PlayOutcome:
        """Print what was decided and what persisted, then confirm the save reopens closed.

        The record keeps the whole morning's log. What is printed here is the headless report's
        closing half — the resolution, the chain, the finding, the party's state, the campaign's
        books and the save path — because the scenes were already narrated as they were played.
        """
        path = save()
        reopened = load_session(path, kallio.CASE)
        report = session.report()
        record = {
            "route": "interactive",
            "approach": approach_used,
            "seed": None if resumed else seed_used,
            "log": log,
            "case": case_summary(report),
            "persisted": report["persisted"],
            "reload": {
                "path": str(path),
                "finished_after_reload": reopened.finished,
                "same_evidence": reopened.report()["persisted"]["case_evidence"]
                == report["persisted"]["case_evidence"],
                "campaign_notes": reopened.report()["persisted"]["campaign_notes"],
                "resolution_after_reload": reopened.report()["resolution"],
            },
        }
        outcome.record = record
        closing = [entry for entry in log if entry["kind"] in ("resolution", "wound")]
        text = render_text({**record, "log": closing})
        # The trimmed log leaves the report's own spacing doubled where the scenes used to be.
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")
        out("")
        out(text)
        outcome.exit_reason = "ended"
        return outcome

    if session.finished:
        log.append(_scene_entry(session))
        return finish("")

    show_scene()
    out(render_menu(session))
    out(render_endings(session))
    out(_commands_block())

    while True:
        raw = ask("> ")
        if raw is None:
            return leave("eof", "End of input — the case is saved where you left it.")
        line = raw.strip()
        if not line:
            continue
        parts = line.split()
        verb, rest = parts[0].lower(), parts[1:]

        if verb in ("quit", "exit", "q"):
            return leave("quit", "The morning waits. The case is saved where you left it.")

        if verb in ("help", "?", "commands"):
            out(_commands_block())
            continue

        if verb in ("party", "p"):
            out(_party_block(session))
            continue

        if verb in ("status", "s"):
            out(_status_block(session))
            continue

        if verb == "save":
            out(f"[saved to {save()}]")
            continue

        if verb == "approach":
            if rest and rest[0].lower() in APPROACHES:
                approach = rest[0].lower()
                out(f"The confrontation will be taken with {approach}.")
            else:
                out(f"approach takes one of {', '.join(APPROACHES)}; it is {approach} now.")
            continue

        if verb in ("next", "leave", "continue"):
            try:
                session.end_scene()
            except CaseworkError as exc:
                out(f"The case refuses: {exc}")
                continue
            save()
            show_scene()
            out(render_menu(session))
            out(render_endings(session))
            continue

        if verb in ("act", "a"):
            if len(rest) != 2:
                out("act needs a seat and an action: act <seat> <action>")
                out("  e.g. act pc 2   ·   act harri_romppainen read_the_duty_log")
                continue
            try:
                seat = _seat_token(session, rest[0])
                action = _action_token(session, rest[1])
            except (CaseworkError, CaseSpecError) as exc:
                out(f"Not available: {exc}")
                continue
            verdict = next(item for item in session.actions() if item["id"] == action.id)
            if not verdict["available"]:
                out(f"The case refuses that: {verdict['reason']}")
                continue
            result = session.act(seat.id, action.id)
            if not result.ok:
                out(f"{_name(session, seat.id)} cannot do that: {result.reason}")
                continue
            log.append(_action(result))
            out(render_outcome(session, action, seat.id, result))
            save()
            if result.scene_changed or session.scene_spec.id != shown:
                show_scene()
                out(render_menu(session))
                out(render_endings(session))
            elif not session.seats_available():
                out("")
                out("  The turn is spent and this is the last scene: take the closing decision.")
                out(render_endings(session))
            continue

        if verb in ("resolve", "close", "end"):
            if not rest:
                out("resolve needs an ending: resolve <ending> [pressure|force] [seat]")
                out(render_endings(session))
                continue
            try:
                spec = _ending_token(session, rest[0])
            except (CaseworkError, CaseSpecError) as exc:
                out(f"Not available: {exc}")
                continue
            verdict = next(item for item in session.resolutions() if item["id"] == spec.id)
            if not verdict["available"]:
                out(f"The case cannot close that way yet: {verdict['reason']}")
                continue
            seat_id = None
            approach_given = False
            for token in rest[1:]:
                if token.lower() in APPROACHES:
                    approach = token.lower()
                    approach_given = True
                    continue
                try:
                    seat_id = _seat_token(session, token).id
                except CaseworkError as exc:
                    out(f"Not available: {exc}")
            if spec.opposed_by and not approach_given:
                answer = ask(
                    "How do you take him — pressure (words) or force (one exchange)? [pressure] "
                )
                if answer is None:
                    return leave("eof", "End of input — the case is saved where you left it.")
                chosen = answer.strip().lower() or "pressure"
                if chosen not in APPROACHES:
                    out(f"approach takes one of {', '.join(APPROACHES)}; using pressure.")
                    chosen = "pressure"
                approach = chosen
            try:
                result = session.resolve(
                    spec.id,
                    seat_id=seat_id,
                    approach=approach if spec.opposed_by else "",
                )
            except CaseworkError as exc:
                out(f"The case refuses: {exc}")
                continue
            log.append(_resolution_entry(result))
            out("")
            out(f"{_name(session, seat_id or session.campaign.leader_id)} — {result.label}")
            out(_wrap(result.text))
            if result.detail:
                out(f"  {result.detail}")
            if result.degraded:
                out("  The attempt falls back to a referral: the case ends, on the weaker record.")
            for wound in result.wounds:
                log.append({"kind": "wound", "text": f"wound: {wound}"})
                out(f"  wound: {wound}")
            return finish(approach if spec.opposed_by else "")

        out(f"Not a command: {line!r}. Type help.")
