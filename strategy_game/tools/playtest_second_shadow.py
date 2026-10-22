"""Playtest harness for *The Second Shadow* — measured evidence for issue #516.

This is **evidence, not a rule**. It drives the shipped case (``strategy_game.casework``) through
every route and approach it offers, over a seed range, and prints the tables a reader needs to judge
playability: pace, fail-forward price, ending distribution, check load, clue-chain behaviour and
determinism. It changes nothing: no difficulty, no skill, no outcome band, no resolution requirement
is read from anywhere but the case declaration, and nothing here writes to the campaign except
through the session's own one writer.

    python -m strategy_game.tools.playtest_second_shadow --seeds 300
    python -m strategy_game.tools.playtest_second_shadow --seeds 300 --json out.json

What is run
-----------

* **Route replays** — the four shipped demo paths, exactly as ``casework.demo.play`` plays them:
  ``investigate``, ``confront --approach pressure``, ``confront --approach force`` and ``refer``.
  (The demo's own names; the issue text's ``close``/``words`` are the same two things.)
* **Policies** — a *thorough* party (attempts every available action in every scene), a *minimal*
  party (only the actions a chosen ending needs, to measure the floor of check load), and a
  *random* party (uniform choice among available actions, to probe for dead ends). Each is played
  for every ending the case offers.
* **Skill-dependency probes** — a thorough party forbidden from one skill at a time, to measure
  which skills are actually load-bearing for which ending.
* **Forced-dice probes** — every check forced to fail, and every check forced to succeed, to test
  the fail-forward and assembled-not-handed-over properties at their extremes.
* **Determinism** — every run is played twice and the full case report plus the campaign payload are
  compared byte for byte; a subset is also saved mid-play and reloaded.

Every number this module prints is computed from the runs it executed. It decides nothing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import statistics
import tempfile
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Any

from strategy_game.casework import kallio, options
from strategy_game.casework.session import CaseSession, CaseworkError
from strategy_game.rpg.fate import Action

__all__ = [
    "APPROACHES",
    "ENDINGS",
    "POLICIES",
    "ROUTES",
    "Run",
    "main",
    "play_demo_route",
    "play_minimal",
    "play_random",
    "play_thorough",
    "probe",
    "summarise",
]

#: The three endings the case declares, as ``requested`` labels for the harness.
ENDINGS: tuple[str, ...] = ("evidence", "confront", "refer")

#: Ending label -> the resolution id the case uses for it.
RESOLUTION_FOR: dict[str, str] = {
    "evidence": "closed_by_evidence",
    "confront": "closed_by_confrontation",
    "refer": "closed_by_withdrawal",
}

#: The shipped demo routes, with the approach each uses (``""`` when the route has none).
ROUTES: tuple[tuple[str, str], ...] = (
    ("investigate", ""),
    ("confront", "pressure"),
    ("confront", "force"),
    ("refer", ""),
)

#: The approaches the confrontation declares.
APPROACHES: tuple[str, ...] = ("pressure", "force")

#: The action-policy names this harness can play.
POLICIES: tuple[str, ...] = ("thorough", "minimal", "random")

#: The six individual skills, so a dependency probe covers the whole sheet.
SKILLS: tuple[str, ...] = ("COG", "INT", "REF", "SAV", "SOM", "WIL")

#: A hard stop so a broken policy cannot spin. The case cannot need more than this.
ACTION_CAP = 40


# -- dice that do not roll ---------------------------------------------------------------------


class _Fixed(Random):
    """A die that always comes up with one face, for the forced extremes.

    ``Random.choice`` is the only randomness the kernel uses (``fate.roll_fate``), so overriding it
    is enough to force every check in a run without touching the engine.
    """

    def __init__(self, face: int) -> None:
        super().__init__(0)
        self._face = face

    def choice(self, seq):  # type: ignore[override]
        return self._face if self._face in seq else seq[0]


class _Queue(Random):
    """A die that plays a fixed script of faces, so one specific roll can be forced.

    The kernel rolls four dice per check and consumes them in order, so a queue long enough to
    carry the party through the case and then lose one exchange pins the *taken out* path exactly.
    """

    def __new__(cls, *args, **kwargs):  # type: ignore[no-untyped-def]
        # ``random.Random.__new__`` hands its arguments to the C constructor, which rejects a list.
        return super().__new__(cls)

    def __init__(self, faces: list[int]) -> None:
        super().__init__(0)
        self._faces = list(faces)

    def choice(self, seq):  # type: ignore[override]
        return self._faces.pop(0) if self._faces else seq[-1]


# -- the measured record ------------------------------------------------------------------------


@dataclass
class Run:
    """One playthrough, reduced to what the tables read."""

    policy: str
    requested: str
    seed: int
    applied: str = ""
    outcome: str = ""
    degraded: bool = False
    fell_back: bool = False
    checks: int = 0
    rolls: int = 0
    closing_skill: str = ""
    opposed: bool = False
    actions: int = 0
    refused: int = 0
    invocations: int = 0
    invocations_free: int = 0
    invocations_paid: int = 0
    closing_invocation: bool = False
    closing_invocation_free: bool = False
    withheld: tuple[str, ...] = ()
    chain_missing: tuple[str, ...] = ()
    scenes: tuple[str, ...] = ()
    turns: int = 0
    clues: tuple[str, ...] = ()
    chain_held: int = 0
    partial: bool = False
    finding: bool = False
    complications: tuple[str, ...] = ()
    wounds: tuple[dict[str, Any], ...] = ()
    taken_out: bool = False
    party_wounds: int = 0
    suspect_wounds: int = 0
    party_taken_out: bool = False
    acted_after_taken_out: int = 0
    stress: dict[str, int] = field(default_factory=dict)
    consequences: dict[str, list[str]] = field(default_factory=dict)
    skills: dict[str, int] = field(default_factory=dict)
    skill_outcomes: dict[str, dict[str, int]] = field(default_factory=dict)
    by_scene: dict[str, int] = field(default_factory=dict)
    by_action: dict[str, dict[str, Any]] = field(default_factory=dict)
    endings_available: tuple[str, ...] = ()
    blocked_states: int = 0
    fingerprint: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "policy": self.policy,
            "requested": self.requested,
            "seed": self.seed,
            "applied": self.applied,
            "outcome": self.outcome,
            "degraded": self.degraded,
            "fell_back": self.fell_back,
            "checks": self.checks,
            "rolls": self.rolls,
            "closing_skill": self.closing_skill,
            "opposed": self.opposed,
            "actions": self.actions,
            "refused": self.refused,
            "invocations": self.invocations,
            "invocations_free": self.invocations_free,
            "invocations_paid": self.invocations_paid,
            "closing_invocation": self.closing_invocation,
            "closing_invocation_free": self.closing_invocation_free,
            "withheld": list(self.withheld),
            "chain_missing": list(self.chain_missing),
            "scenes": list(self.scenes),
            "turns": self.turns,
            "clues": list(self.clues),
            "chain_held": self.chain_held,
            "partial": self.partial,
            "finding": self.finding,
            "complications": list(self.complications),
            "wounds": list(self.wounds),
            "taken_out": self.taken_out,
            "party_wounds": self.party_wounds,
            "suspect_wounds": self.suspect_wounds,
            "party_taken_out": self.party_taken_out,
            "acted_after_taken_out": self.acted_after_taken_out,
            "stress": dict(self.stress),
            "consequences": {k: list(v) for k, v in self.consequences.items()},
            "skills": dict(self.skills),
            "skill_outcomes": {k: dict(v) for k, v in self.skill_outcomes.items()},
            "by_scene": dict(self.by_scene),
            "by_action": {k: dict(v) for k, v in self.by_action.items()},
            "endings_available": list(self.endings_available),
            "blocked_states": self.blocked_states,
            "fingerprint": self.fingerprint,
        }


# -- small helpers ------------------------------------------------------------------------------


def _seat_for_action(session: CaseSession, action_id: str, *, best: bool = True) -> str:
    """The seat that takes this action.

    ``best`` models a party that puts its best available specialist on the check — the normal way a
    table plays, and the fair baseline for judging the case's difficulty. ``best=False`` models a
    party that simply uses the scene's suggested character and then takes whoever is free, which is
    how an inattentive table drifts into rolling a strong skill at a weak rating. ``suggested_actor``
    is presentation only; neither choice changes whether the action is legal.
    """
    action = session.scene_spec.action(action_id)
    free = tuple(session.ledger.seats_available)
    skill = "" if action.check is None else action.check.skill
    if best and skill:
        rated = [(session.sheet(seat_id).skills.get(skill, 0), seat_id) for seat_id in free]
        if rated:
            return max(rated, key=lambda item: item[0])[1]
    for reference in (action.suggested_actor, *free):
        if not reference:
            continue
        try:
            seat = session.seat_for(reference)
        except CaseworkError:
            continue
        if seat.id in free:
            return seat.id
    return ""


def _skill_of(session: CaseSession, action_id: str) -> str:
    """The skill an action's check reads, or ``""`` for an action with no check."""
    check = session.scene_spec.action(action_id).check
    return "" if check is None else check.skill


def _advantage_first(
    session: CaseSession, acts: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Order a scene's available actions the way a party that means to use an aspect takes them.

    Create-advantage actions first, then actions with a check, then the free ones (assembling a chain
    rolls no dice and can be done whenever). Declaration order is preserved inside each group, so the
    policy stays deterministic and the only thing it changes is *when* an aspect exists relative to
    the checks that could invoke it.
    """
    def rank(item: dict[str, Any]) -> tuple[int, int]:
        check = session.scene_spec.action(item["id"]).check
        if check is None:
            return (2, 0)
        return (0 if check.action is Action.CREATE_ADVANTAGE else 1, 0)

    return sorted(acts, key=rank)


def _blocked(session: CaseSession) -> bool:
    """A state the case cannot continue from: no action, no ending, and no scene to leave."""
    if session.finished:
        return False
    acts = [item for item in session.actions() if item["available"]]
    if acts and session.ledger.seats_available:
        return False
    if any(item["available"] for item in session.resolutions()):
        return False
    return session.spec.next_scene_after(session.scene_spec.id) is None


def _clue_chain(session: CaseSession) -> int:
    return sum(1 for clue in session.spec.chain if clue in session.clues)


def _record(
    session: CaseSession,
    *,
    policy: str,
    requested: str,
    seed: int,
    blocked: int,
    refused: int,
    events_offset: int = 0,
    closing_invocation: bool = False,
    closing_invocation_free: bool = False,
) -> Run:
    """Reduce a finished (or finished-as-far-as-it-goes) session to a :class:`Run`."""
    report = session.report()
    events = list(session.events)[events_offset:]
    skills: Counter[str] = Counter()
    skill_outcomes: dict[str, Counter[str]] = defaultdict(Counter)
    by_scene: Counter[str] = Counter()
    by_action: dict[str, dict[str, Any]] = {}
    scenes = [item["scene"] for item in events if item["kind"] == "scene_change"]
    for event in events:
        if event["kind"] != "case_action":
            continue
        check = event.get("check")
        if not check:
            continue
        skill = check["skill"]
        skills[skill] += 1
        skill_outcomes[skill][check["outcome"]] += 1
        by_scene[event["scene"]] += 1
        entry = by_action.setdefault(
            f"{event['scene']}/{event['action']}",
            {
                "outcome": Counter(),
                "costs": Counter(),
                "consequence": 0,
                "charged": 0,
                "checks": 0,
                "skill": skill,
                "band": check["band"],
                "difficulty": check["difficulty"],
            },
        )
        entry["checks"] += 1
        entry["outcome"][check["outcome"]] += 1
        entry["consequence"] += 1 if event.get("consequence") else 0
        entry["charged"] += 1 if event.get("costs") else 0
        for cost in event.get("costs") or ():
            entry["costs"][cost] += 1
    for entry in by_action.values():
        entry["outcome"] = dict(entry["outcome"])
        entry["costs"] = dict(entry["costs"])
    party = report["party"]
    party_ids = {member["character"] for member in party}
    # "Taken out" is recorded on the action's own event as well as on a consequence-bearing wound,
    # so read both: a stress overflow with no consequence slot free leaves no wound record at all.
    action_events = [event for event in events if event["kind"] == "case_action"]
    event_takeouts = [event for event in action_events if event.get("taken_out")]
    acted_after = 0
    for position, event in enumerate(action_events):
        if not event.get("taken_out"):
            continue
        if any(
            later["character"] == event["character"] for later in action_events[position + 1 :]
        ):
            acted_after += 1
    stress = {
        member["character"]: sum(1 for box in member["physical_stress"] if box)
        + sum(1 for box in member["mental_stress"] if box)
        for member in party
    }
    consequences = {
        member["character"]: [item["name"] for item in member["consequences"]]
        for member in party
    }
    findings = report["findings"]
    closing = next(
        (item for item in session.spec.resolutions if item.id == report["resolution"]), None
    )
    if closing is not None:
        skills[closing.skill] += 1
        skill_outcomes[closing.skill]["closing"] += 1
    run = Run(
        policy=policy,
        requested=requested,
        seed=seed,
        applied=report["resolution"],
        outcome=next(
            (
                item["outcome"]
                for item in reversed(events)
                if item["kind"] == "resolution"
            ),
            "",
        ),
        degraded=bool(
            next(
                (item["degraded"] for item in reversed(events) if item["kind"] == "resolution"),
                False,
            )
        ),
        checks=sum(skills.values()),
        rolls=sum(skills.values()) + (1 if closing is not None and closing.opposed_by else 0),
        closing_skill="" if closing is None else closing.skill,
        opposed=bool(closing is not None and closing.opposed_by),
        actions=sum(1 for event in events if event["kind"] == "case_action")
        + sum(1 for event in events if event["kind"] == "finding"),
        refused=refused,
        invocations=sum(
            1
            for event in events
            if event["kind"] == "case_action" and (event.get("check") or {}).get("invoked")
        ),
        invocations_free=sum(
            1
            for event in events
            if event["kind"] == "case_action"
            and (event.get("check") or {}).get("invoked")
            and (event.get("check") or {}).get("invoked_free")
        ),
        invocations_paid=sum(
            1
            for event in events
            if event["kind"] == "case_action"
            and (event.get("check") or {}).get("invoked")
            and not (event.get("check") or {}).get("invoked_free")
        ),
        closing_invocation=closing_invocation,
        closing_invocation_free=closing_invocation_free,
        withheld=tuple(clue for event in events for clue in (event.get("withheld") or ())),
        chain_missing=session.chain_gaps,
        scenes=tuple(scenes),
        turns=report["scene"]["turn"],
        clues=tuple(clue["id"] for clue in report["clues"]),
        chain_held=_clue_chain(session),
        partial=any(item["partial"] for item in findings),
        finding=bool(findings),
        complications=tuple(report["complications"]),
        wounds=tuple(report["wounds"]),
        taken_out=any(item.get("taken_out") for item in report["wounds"]) or bool(event_takeouts),
        party_wounds=sum(1 for item in report["wounds"] if item["character"] in party_ids),
        suspect_wounds=sum(
            1 for item in report["wounds"] if item["character"] not in party_ids
        ),
        party_taken_out=any(
            item.get("taken_out") and item["character"] in party_ids
            for item in report["wounds"]
        )
        or any(event["character"] in party_ids for event in event_takeouts),
        acted_after_taken_out=acted_after,
        stress=stress,
        consequences=consequences,
        skills=dict(skills),
        skill_outcomes={key: dict(value) for key, value in skill_outcomes.items()},
        by_scene=dict(by_scene),
        by_action=by_action,
        endings_available=tuple(
            item["id"] for item in session.resolutions() if item["available"]
        ),
        blocked_states=blocked,
    )
    run.fell_back = run.applied != RESOLUTION_FOR.get(requested, requested)
    run.fingerprint = _fingerprint(session)
    return run


def _fingerprint(session: CaseSession) -> str:
    """A digest of the whole persisted outcome: the case report and the campaign payload."""
    payload = {"report": session.report(), "campaign": session.campaign.to_dict()}
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# -- policies -----------------------------------------------------------------------------------


def _free_aspect(session: CaseSession) -> str | None:
    """The first scene aspect with a free invocation left, for a party that spends them."""
    for name, aspect in session.scene.aspects.items():
        if aspect.free_invocations > 0:
            return name
    return None


def _aspect_for(
    session: CaseSession, seat_id: str, *, spend_fate: bool, keep_one: bool = False
) -> tuple[str | None, bool]:
    """The aspect this check can invoke, and whether the invocation is free.

    A party spends what it already earned first: any scene aspect with a free invocation left. Only a
    party that is willing to pay Fate points reaches past that — to another scene aspect (a declared
    situation aspect included) or to one of the character's own sheet aspects. Returns ``(None,
    False)`` when nothing can be spent, which is the ``thorough-no-aspects`` policy's whole
    behaviour.

    ``keep_one`` leaves an aspect's **last** free invocation alone, which is how a table behaves when
    it expects one decisive roll later (the closing check). It is the difference between spending as
    you go and saving something for the moment the case is decided.
    """
    for name, aspect in session.scene.aspects.items():
        if aspect.free_invocations > (1 if keep_one else 0):
            return name, True
    if not spend_fate:
        return None, False
    try:
        sheet = session.sheet(seat_id)
    except CaseworkError:  # pragma: no cover - the seat came from the session
        return None, False
    if sheet.fate_points < 1:
        return None, False
    spare = [name for name, aspect in session.scene.aspects.items() if aspect.free_invocations == 0]
    for name in spare:
        return name, False
    if keep_one:
        return None, False
    for name in sheet.aspects:
        return name, False
    return None, False


def _close(
    session: CaseSession,
    requested: str,
    approach: str,
    *,
    free_invoke: str | None = None,
    invoke: str | None = None,
) -> tuple[bool, bool]:
    """Resolve the case, falling back to the referral when the requested ending is unavailable.

    This is the *harness's* rule for a scripted policy (the player asked for an ending the party has
    not earned); the case itself only ever refuses, so the fallback is recorded as ``fell_back``.
    Returns ``(invoked, free)`` — whether an aspect reached the closing check, and whether it cost a
    Fate point or nothing.
    """
    resolution = RESOLUTION_FOR[requested]
    available = {item["id"] for item in session.resolutions() if item["available"]}
    chosen = resolution if resolution in available else "closed_by_withdrawal"
    session.resolve(
        chosen,
        seat_id="pc_leader",
        approach=approach if chosen == RESOLUTION_FOR["confront"] else "",
        free_invoke=free_invoke,
        invoke=invoke,
    )
    return (free_invoke or invoke) is not None, free_invoke is not None


def play_thorough(
    seed: int,
    *,
    requested: str = "evidence",
    approach: str = "pressure",
    skip_skills: Iterable[str] = (),
    skip_scenes: Iterable[str] = (),
    use_aspects: bool = True,
    spend_fate: bool = False,
    advantage_first: bool = True,
    reserve_closing: bool = False,
    best_seats: bool = True,
    spec=None,
    rng: Random | None = None,
) -> Run:
    """Attempt every available action in every scene, then close on the requested ending.

    ``skip_skills`` forbids every action whose check reads one of those skills — the dependency
    probe. ``skip_scenes`` leaves a scene without playing it, which is how a party that never visits
    the caretaker ends up with two fragments instead of three. A scene is otherwise left only when
    nothing legal is left to attempt.

    ``use_aspects`` spends free invocations; ``spend_fate`` also spends Fate points on an aspect when
    no free invocation is left (that is the *paid* half of Fate's invoke rule). ``advantage_first``
    models a party that creates an advantage **before** the checks it intends to spend it on — the
    ordering a competent table uses, and the difference between an aspect economy that lands on an
    action check and one that is created after the last check of its scene.

    ``reserve_closing`` leaves each aspect's last free invocation unspent until the closing check —
    the party that saves something for the decisive roll rather than spending as it goes.

    ``spec`` plays a variant declaration (see :mod:`strategy_game.casework.options`); the default is
    the shipped case, byte for byte.
    """
    forced = set(skip_skills)
    skipped = set(skip_scenes)
    session = kallio.build_session(seed=seed, rng=rng, spec=spec)
    refused = 0
    blocked = 0
    guard = 0
    while not session.finished and guard < ACTION_CAP:
        guard += 1
        if _blocked(session):
            blocked += 1
            break
        if session.scene_spec.id in skipped:
            try:
                session.end_scene()
            except CaseworkError:
                break
            continue
        acts = [
            item
            for item in session.actions()
            if item["available"] and _skill_of(session, item["id"]) not in forced
        ]
        if acts and advantage_first:
            acts = _advantage_first(session, acts)
        if not acts or not session.ledger.seats_available:
            try:
                session.end_scene()
            except CaseworkError:
                break
            continue
        action_id = acts[0]["id"]
        seat = _seat_for_action(session, action_id, best=best_seats)
        if not seat:  # pragma: no cover - a free seat exists whenever availability allows an act
            blocked += 1
            break
        free, is_free = (
            _aspect_for(session, seat, spend_fate=spend_fate, keep_one=reserve_closing)
            if use_aspects
            else (None, False)
        )
        result = session.act(
            seat,
            action_id,
            free_invoke=free if is_free else None,
            invoke=None if is_free else free,
        )
        refused += 0 if result.ok else 1
        if not result.ok:  # pragma: no cover - availability was just queried
            break
    free, is_free = (
        _aspect_for(session, "pc_leader", spend_fate=spend_fate) if use_aspects else (None, False)
    )
    invoked, closing_free = _close(
        session,
        requested,
        approach,
        free_invoke=free if is_free else None,
        invoke=None if is_free else free,
    )
    return _record(
        session,
        policy="thorough" if not forced else f"thorough-without-{'+'.join(sorted(forced))}",
        requested=requested,
        seed=seed,
        blocked=blocked,
        refused=refused,
        closing_invocation=invoked,
        closing_invocation_free=closing_free,
    )


#: The actions a chosen ending needs, at the floor: one route to every fragment and nothing else.
MINIMAL_STEPS: dict[str, tuple[tuple[str, str], ...]] = {
    "evidence": (
        ("victim", "interview_nila"),
        ("victim", "scan_the_stack"),
        ("stairwell", "read_the_stairwell"),
        ("witness", "check_the_thermal_record"),
        ("resolution", "assemble_the_chain"),
    ),
    "confront": (
        ("victim", "interview_nila"),
        ("victim", "scan_the_stack"),
        ("stairwell", "read_the_stairwell"),
        ("witness", "check_the_thermal_record"),
        ("resolution", "assemble_the_chain"),
        ("resolution", "pull_the_batch_signout"),
    ),
    "refer": (),
}


def play_minimal(
    seed: int,
    *,
    requested: str = "evidence",
    approach: str = "pressure",
    force_loss: bool = False,
    spec=None,
    rng: Random | None = None,
) -> Run:
    """Take only the actions the requested ending needs, then close. Measures the check floor.

    ``force_loss`` swaps the dice for the closing exchange alone — four -1s for the attack and four
    +1s for the defence — so the one state the rules call *taken out* can be pinned exactly, however
    many dice the investigation consumed. That is the same technique the case's own test uses.
    """
    session = kallio.build_session(seed=seed, rng=rng, spec=spec)
    refused = 0
    blocked = 0
    for scene_id, action_id in MINIMAL_STEPS[requested]:
        while session.scene_spec.id != scene_id and not session.finished:
            try:
                session.end_scene()
            except CaseworkError:  # pragma: no cover - the step list is in scene order
                break
        if session.finished or session.scene_spec.id != scene_id:
            break
        seat = _seat_for_action(session, action_id)
        if not seat:  # pragma: no cover - five seats, at most four actions per scene
            blocked += 1
            break
        result = session.act(seat, action_id)
        refused += 0 if result.ok else 1
    if force_loss:
        session._dice = _Queue([-1] * 4 + [1] * 4)  # type: ignore[attr-defined]
    _close(session, requested, approach)
    return _record(
        session,
        policy="minimal",
        requested=requested,
        seed=seed,
        blocked=blocked,
        refused=refused,
    )


def play_random(
    seed: int,
    *,
    requested: str = "",
    approach: str = "",
    rng: Random | None = None,
    appetite: float = 0.8,
    abandon: float = 0.0,
) -> Run:
    """Play with a uniform random choice among the actions on offer, then end at random.

    ``requested``/``approach`` are ignored: this policy is the probe for *whether a party that plays
    arbitrarily still reaches an ending at all*, and which one. ``appetite`` is how often it takes
    another action rather than leaving the scene; ``abandon`` is how often it walks away from the
    case mid-scene and refers it, which is the only ending available that early.
    """
    chooser = Random(seed * 7919 + 13)
    session = kallio.build_session(seed=seed, rng=rng)
    refused = 0
    blocked = 0
    guard = 0
    while not session.finished and guard < ACTION_CAP:
        guard += 1
        if _blocked(session):
            blocked += 1
            break
        if chooser.random() < abandon:
            session.resolve("closed_by_withdrawal", seat_id="pc_leader")
            break
        acts = [item for item in session.actions() if item["available"]]
        if not acts or not session.ledger.seats_available or chooser.random() > appetite:
            try:
                session.end_scene()
            except CaseworkError:
                break
            continue
        action_id = chooser.choice([item["id"] for item in acts])
        seat = _seat_for_action(session, action_id)
        if not seat:  # pragma: no cover
            blocked += 1
            break
        result = session.act(seat, action_id)
        refused += 0 if result.ok else 1
    if session.finished:
        applied = session.report()["resolution"]
    else:
        available = [item for item in session.resolutions() if item["available"]]
        applied = chooser.choice([item["id"] for item in available])
        chosen_approach = (
            chooser.choice(list(APPROACHES)) if applied == RESOLUTION_FOR["confront"] else ""
        )
        session.resolve(applied, seat_id="pc_leader", approach=chosen_approach)
    requested_label = next(
        (label for label, resolution in RESOLUTION_FOR.items() if resolution == applied), ""
    )
    return _record(
        session,
        policy="random",
        requested=requested_label,
        seed=seed,
        blocked=blocked,
        refused=refused,
    )


def play_demo_route(seed: int, route: str, approach: str) -> Run:
    """Replay one shipped demo route exactly, through ``casework.demo.play``.

    The demo saves and reloads twice per run, so this measures the path a reader actually runs. The
    run's own log is part of the determinism check: two identical seeds must print the same
    transcript, not merely the same final state.
    """
    from strategy_game.casework import demo

    # A *stable* save path per (route, approach, seed), so two replays of the same seed print the
    # same transcript — the demo's log quotes its own save path, and a random temporary directory
    # would make an identical run look different.
    target = Path(tempfile.gettempdir()) / "noopunk-playtest" / (
        f"{route}-{approach or 'none'}-{seed}.json"
    )
    session, log, confirmation = demo.play(
        route,
        seed=seed,
        approach=approach or "pressure",
        save_to=target,
    )
    transcript = hashlib.sha256(
        json.dumps(log, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    requested = {
        "investigate": "evidence",
        "confront": "confront",
        "refer": "refer",
    }[route]
    run = _record(
        session,
        policy=f"demo:{route}" + (f":{approach}" if approach else ""),
        requested=requested,
        seed=seed,
        blocked=0,
        refused=0,
    )
    run.fingerprint = hashlib.sha256(
        (run.fingerprint + transcript).encode("utf-8")
    ).hexdigest()
    if not (confirmation["same_clues"] and confirmation["same_evidence"]):
        run.degraded = True  # surfaces a broken save/reload, not a rules outcome
    return run


# -- probes -------------------------------------------------------------------------------------


def option_matrix(seeds: int, *, start: int = 0) -> dict[str, Any]:
    """Measure each tuning **option** against the shipped setting, on the same seeds.

    Every group here is one question the case could answer two ways, run over the same seed block so
    the difference is the option and nothing else. Nothing in this function chooses: the shipped
    setting is the first row of every group, each alternative is built by
    :mod:`strategy_game.casework.options`, and the numbers are printed side by side.
    """
    seeds_iter = range(start, start + seeds)
    base = kallio.CASE
    always = options.with_chain_withholding(base, enabled=False)
    ref = options.with_force_attack_skill(base, "REF")
    tie_stands = options.with_tie_policy(base, not_total_failure=True)
    out: dict[str, list[tuple[str, list[Run]]]] = {}

    # (1) Does a failed check withhold its fragment?
    out["chain: does a failure withhold the fragment?"] = [
        ("yes — shipped (``withhold_on_failure``)", [
            play_thorough(seed, requested="evidence") for seed in seeds_iter
        ]),
        ("no — every check grants its clue, as before", [
            play_thorough(seed, requested="evidence", spec=always) for seed in seeds_iter
        ]),
    ]
    # The same question at the extreme the old evidence quoted: every check forced to fail.
    out["chain: every check forced to fail"] = [
        ("yes — shipped", [play_thorough(start, requested="evidence", rng=_Fixed(-1))]),
        (
            "no — as before",
            [play_thorough(start, requested="evidence", spec=always, rng=_Fixed(-1))],
        ),
    ]
    # (2) Which skill a force exchange attacks with.
    out["force: which skill attacks?"] = [
        ("the resolution's own — ``SAV`` (code, shipped)", [
            play_thorough(seed, requested="confront", approach="force") for seed in seeds_iter
        ]),
        ("``REF`` — the case document's \"REF opposed attack\"", [
            play_thorough(seed, requested="confront", approach="force", spec=ref)
            for seed in seeds_iter
        ]),
    ]
    # (3) Is a tie on a confrontation total failure?
    for approach in ("pressure", "force"):
        out[f"tie is total failure? ({approach})"] = [
            ("yes — shipped", [
                play_thorough(seed, requested="confront", approach=approach) for seed in seeds_iter
            ]),
            ("no — the attempt stands, priced by nothing here", [
                play_thorough(
                    seed, requested="confront", approach=approach, spec=tie_stands
                )
                for seed in seeds_iter
            ]),
        ]
    # (4) How much of the aspect economy the party spends.
    out["aspects: how much does the party spend?"] = [
        ("nothing (``thorough-no-aspects``)", [
            play_thorough(seed, requested="evidence", use_aspects=False) for seed in seeds_iter
        ]),
        ("free invocations, spent as they come", [
            play_thorough(seed, requested="evidence") for seed in seeds_iter
        ]),
        ("free invocations, one kept for the close", [
            play_thorough(seed, requested="evidence", reserve_closing=True) for seed in seeds_iter
        ]),
        ("free and paid (Fate points too)", [
            play_thorough(seed, requested="evidence", spend_fate=True) for seed in seeds_iter
        ]),
        ("free, created after the checks it would help", [
            play_thorough(seed, requested="evidence", advantage_first=False) for seed in seeds_iter
        ]),
    ]
    # The same question where it matters most: the one opposed roll that decides a detention.
    out["aspects: how much does the party spend? (confrontation)"] = [
        ("nothing", [
            play_thorough(seed, requested="confront", approach="pressure", use_aspects=False)
            for seed in seeds_iter
        ]),
        ("free, one kept for the close", [
            play_thorough(seed, requested="confront", approach="pressure", reserve_closing=True)
            for seed in seeds_iter
        ]),
    ]
    # (5) The floor of check load under the shipped chain setting.
    out["floor: the minimal party"] = [
        ("withholds on failure — shipped", [
            play_minimal(seed, requested="evidence") for seed in seeds_iter
        ]),
        ("always grants — as before", [
            play_minimal(seed, requested="evidence", spec=always) for seed in seeds_iter
        ]),
    ]
    return {
        group: [(label, [run.as_dict() for run in runs]) for label, runs in settings]
        for group, settings in out.items()
    }


def probe(seeds: int, *, start: int = 0) -> dict[str, Any]:
    """Everything the document's tables need, in one JSON-able record."""
    routes: dict[str, list[Run]] = {}
    for route, approach in ROUTES:
        label = route if not approach else f"{route}:{approach}"
        routes[label] = [play_demo_route(seed, route, approach) for seed in range(start, start + seeds)]

    policies: dict[str, list[Run]] = {}
    for requested in ENDINGS:
        approach = "pressure" if requested == "confront" else ""
        policies[f"thorough:{requested}"] = [
            play_thorough(seed, requested=requested, approach=approach or "pressure")
            for seed in range(start, start + seeds)
        ]
        policies[f"minimal:{requested}"] = [
            play_minimal(seed, requested=requested, approach=approach or "pressure")
            for seed in range(start, start + seeds)
        ]
    policies["random"] = [play_random(seed, abandon=0.05) for seed in range(start, start + seeds)]
    # The aspect economy: the same thorough party, once spending its free invocations and once
    # ignoring them. The difference is what "create an advantage" is actually worth in this case.
    for requested in ("evidence", "confront"):
        policies[f"thorough-no-aspects:{requested}"] = [
            play_thorough(
                seed,
                requested=requested,
                approach="pressure",
                use_aspects=False,
            )
            for seed in range(start, start + seeds)
        ]
        # The same party, but taking whoever is free rather than the best specialist: what seat
        # choice alone is worth in this case.
        policies[f"thorough-naive-seats:{requested}"] = [
            play_thorough(
                seed,
                requested=requested,
                approach="pressure",
                best_seats=False,
            )
            for seed in range(start, start + seeds)
        ]
        # The party that keeps one free invocation back for the decisive roll, and the party that
        # pays Fate points as well as spending what it earned. Together with the greedy `thorough`
        # family above these are the three ways a table actually spends an aspect economy.
        policies[f"thorough-reserve:{requested}"] = [
            play_thorough(
                seed, requested=requested, approach="pressure", reserve_closing=True
            )
            for seed in range(start, start + seeds)
        ]
    policies["thorough-paid:evidence"] = [
        play_thorough(seed, requested="evidence", spend_fate=True)
        for seed in range(start, start + seeds)
    ]
    # The ordering the old harness used: the create-advantage action is taken last in its scene, so
    # nothing is left to spend the aspect on. This is the control that shows the invocations above
    # are produced by the party's behaviour *and* the mechanics, not by the measurement.
    policies["thorough-advantage-last:evidence"] = [
        play_thorough(seed, requested="evidence", advantage_first=False)
        for seed in range(start, start + seeds)
    ]

    skills: dict[str, list[Run]] = {}
    for skill in SKILLS:
        skills[skill] = [
            play_thorough(seed, requested="evidence", skip_skills=(skill,))
            for seed in range(start, start + seeds)
        ]

    extremes: dict[str, Run] = {
        "every-check-fails": play_thorough(
            start, requested="evidence", rng=_Fixed(-1)
        ),
        "every-check-succeeds": play_thorough(
            start, requested="evidence", rng=_Fixed(1)
        ),
        "two-fragments": play_thorough(
            start, requested="evidence", skip_scenes=("witness",), rng=_Fixed(1)
        ),
        "one-fragment": play_thorough(
            start,
            requested="evidence",
            skip_scenes=("witness", "stairwell"),
            rng=_Fixed(1),
        ),
        # Two six-check passes, then a lost attack exchange: the leader is taken out and the case
        # falls back to the referral. This pins the one state the rules call "taken out".
        "forced-lost-fight": play_minimal(
            start,
            requested="confront",
            approach="force",
            force_loss=True,
            rng=_Fixed(1),
        ),
    }

    determinism = _determinism(seeds, start)
    return {
        "method": {
            "seeds_per_run": seeds,
            "seed_range": [start, start + seeds - 1],
            "routes": [f"{route}:{approach}" if approach else route for route, approach in ROUTES],
            "policies": list(policies),
            "skill_probes": list(skills),
            "case_id": kallio.CASE_ID,
            "case_options": options.describe(kallio.CASE),
            "action_count": sum(len(scene.actions) for scene in kallio.CASE.scenes),
            "check_count": sum(
                1
                for scene in kallio.CASE.scenes
                for action in scene.actions
                if action.check is not None
            ),
        },
        "routes": {key: [run.as_dict() for run in value] for key, value in routes.items()},
        "policies": {key: [run.as_dict() for run in value] for key, value in policies.items()},
        "options": option_matrix(seeds, start=start),
        "skills": {key: [run.as_dict() for run in value] for key, value in skills.items()},
        "extremes": {key: run.as_dict() for key, run in extremes.items()},
        "determinism": determinism,
    }


def _determinism(seeds: int, start: int) -> dict[str, Any]:
    """Replay every seed of every route twice and compare the persisted outcome byte for byte.

    The comparison is the case report **and** the campaign payload, serialised with sorted keys, so
    a difference anywhere — a clue, a stress box, a complication, a ledger note, an applied outcome —
    fails it. The demo route is compared on its printed transcript as well.
    """
    mismatched: list[str] = []
    reload_mismatched: list[str] = []
    compared = 0
    for route, approach in ROUTES:
        label = route if not approach else f"{route}:{approach}"
        for seed in range(start, start + seeds):
            first = play_demo_route(seed, route, approach)
            second = play_demo_route(seed, route, approach)
            compared += 1
            if first.fingerprint != second.fingerprint:
                mismatched.append(f"{label}/{seed}")
    for requested in ENDINGS:
        for seed in range(start, start + min(seeds, 40)):
            first = play_thorough(seed, requested=requested)
            second = play_thorough(seed, requested=requested)
            compared += 1
            if first.fingerprint != second.fingerprint:
                mismatched.append(f"thorough:{requested}/{seed}")
    # Save/reload mid-play must resume into the same run: one seed per route is enough to pin it,
    # because the property is the restored dice state, and 40 seeds check the restored ledger too.
    for seed in range(start, start + min(seeds, 40)):
        for requested in ENDINGS:
            if _reload_equivalent(seed, requested) is False:
                reload_mismatched.append(f"{requested}/{seed}")
    return {
        "runs_compared": compared,
        "mismatched": mismatched,
        "reload_compared": 3 * min(seeds, 40),
        "reload_mismatched": reload_mismatched,
    }


def _reload_equivalent(seed: int, requested: str) -> bool:
    """Play to a mid-case save, reload, finish, and compare with an uninterrupted run."""
    from strategy_game.casework.session import load_session

    def finish(session: CaseSession) -> str:
        while not session.finished:
            acts = [item for item in session.actions() if item["available"]]
            if not acts or not session.ledger.seats_available:
                try:
                    session.end_scene()
                except CaseworkError:
                    break
                continue
            action_id = acts[0]["id"]
            session.act(_seat_for_action(session, action_id), action_id)
        _close(session, requested, "pressure")
        return _fingerprint(session)

    straight = finish(kallio.build_session(seed=seed))
    with tempfile.TemporaryDirectory() as scratch:
        path = Path(scratch) / "mid.json"
        session = kallio.build_session(seed=seed)
        # Three actions in, then save: enough that clues, stress and the dice stream have diverged.
        for _ in range(3):
            acts = [item for item in session.actions() if item["available"]]
            if not acts:
                session.end_scene()
                continue
            action_id = acts[0]["id"]
            session.act(_seat_for_action(session, action_id), action_id)
        session.save(path)
        resumed = load_session(path, kallio.CASE)
        reloaded = finish(resumed)
    return straight == reloaded


# -- aggregation and tables ---------------------------------------------------------------------


def _pct(part: int, whole: int) -> str:
    return f"{100.0 * part / whole:.1f}%" if whole else "—"


def _mean(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.fmean(values) if values else 0.0


def _median(values: Iterable[float]) -> float:
    values = list(values)
    return statistics.median(values) if values else 0.0


def _span(values: Iterable[float]) -> str:
    values = sorted(values)
    if not values:
        return "—"
    low = values[int(0.1 * (len(values) - 1))]
    high = values[int(0.9 * (len(values) - 1))]
    return f"{low:g}–{high:g}"


def summarise(runs: Mapping[str, Iterable[Mapping[str, Any]]]) -> dict[str, Any]:
    """Aggregate one family of runs into the numbers the document reports."""
    out: dict[str, Any] = {}
    for label, group in runs.items():
        rows = list(group)
        if not rows:
            continue
        endings = Counter(row["applied"] for row in rows)
        requested = Counter(row["requested"] for row in rows)
        outcomes = Counter(row["outcome"] for row in rows)
        chain = Counter(row["chain_held"] for row in rows)
        available = Counter(len(row["endings_available"]) for row in rows)
        skills: Counter[str] = Counter()
        scenes: Counter[str] = Counter()
        for row in rows:
            skills.update(row["skills"])
            scenes.update(row["by_scene"])
        out[label] = {
            "n": len(rows),
            "requested": dict(requested),
            "endings": dict(endings),
            "outcomes": dict(outcomes),
            "degraded": sum(1 for row in rows if row["degraded"]),
            "checks": {
                "mean": round(_mean(row["checks"] for row in rows), 2),
                "median": _median(row["checks"] for row in rows),
                "p10_90": _span(row["checks"] for row in rows),
                "total": sum(row["checks"] for row in rows),
            },
            "actions": round(_mean(row["actions"] for row in rows), 2),
            "rolls": {
                "mean": round(_mean(row["rolls"] for row in rows), 2),
                "total": sum(row["rolls"] for row in rows),
            },
            "closing_skill": dict(Counter(row["closing_skill"] for row in rows)),
            "opposed": sum(1 for row in rows if row["opposed"]),
            "refused": sum(row["refused"] for row in rows),
            "invocations": {
                "mean": round(_mean(row["invocations"] for row in rows), 2),
                "runs_with_any": sum(1 for row in rows if row["invocations"]),
                "closing_offered": sum(1 for row in rows if row["closing_invocation"]),
                "free": sum(row["invocations_free"] for row in rows),
                "paid": sum(row["invocations_paid"] for row in rows),
                "closing_free": sum(1 for row in rows if row["closing_invocation_free"]),
            },
            "withheld": {
                "runs": sum(1 for row in rows if row["withheld"]),
                "total": sum(len(row["withheld"]) for row in rows),
                "by_clue": dict(
                    Counter(clue for row in rows for clue in row["withheld"]).most_common()
                ),
            },
            "blocked": sum(row["blocked_states"] for row in rows),
            "scenes": dict(Counter(len(row["scenes"]) + 1 for row in rows)),
            "scene_ids": dict(scenes),
            "chain": dict(sorted(chain.items())),
            "chain_missing": {
                "runs": sum(1 for row in rows if row["chain_missing"]),
                "by_clue": dict(
                    Counter(clue for row in rows for clue in row["chain_missing"]).most_common()
                ),
            },
            "partial": sum(1 for row in rows if row["partial"]),
            "finding": sum(1 for row in rows if row["finding"]),
            "complications": {
                "mean": round(_mean(len(row["complications"]) for row in rows), 2),
                "runs_with_any": sum(1 for row in rows if row["complications"]),
                "distinct": dict(
                    Counter(name for row in rows for name in row["complications"]).most_common()
                ),
            },
            "wounds": {
                "runs_with_any": sum(1 for row in rows if row["wounds"]),
                "taken_out_runs": sum(1 for row in rows if row["taken_out"]),
                "party_runs": sum(1 for row in rows if row["party_wounds"]),
                "party_wounds": sum(row["party_wounds"] for row in rows),
                "suspect_runs": sum(1 for row in rows if row["suspect_wounds"]),
                "party_taken_out": sum(1 for row in rows if row["party_taken_out"]),
                "distinct": dict(
                    Counter(
                        wound["name"] for row in rows for wound in row["wounds"]
                    ).most_common(8)
                ),
            },
            "stress": {
                "runs_with_any": sum(
                    1 for row in rows if any(value for value in row["stress"].values())
                ),
                "mean_boxes": round(
                    _mean(sum(row["stress"].values()) for row in rows), 2
                ),
            },
            "consequences": {
                "runs_with_any": sum(
                    1 for row in rows if any(name for name in row["consequences"].values())
                ),
                "by_character": {
                    member: sum(1 for row in rows if row["consequences"].get(member))
                    for member in sorted({key for row in rows for key in row["consequences"]})
                },
            },
            "skills": dict(skills),
            "endings_available": dict(sorted(available.items())),
        }
    return out


def _action_table(
    runs: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Per-action outcome and cost incidence across a family of runs."""
    table: dict[str, dict[str, Any]] = {}
    for row in runs:
        for key, entry in row["by_action"].items():
            slot = table.setdefault(
                key,
                {
                    "skill": entry["skill"],
                    "band": entry["band"],
                    "difficulty": entry["difficulty"],
                    "checks": 0,
                    "outcome": Counter(),
                    "consequence": 0,
                    "charged": 0,
                    "stressed": 0,
                    "complication": 0,
                    "tie_cost": 0,
                    "fail_cost": 0,
                },
            )
            slot["checks"] += 1
            slot["outcome"].update(entry["outcome"])
            slot["consequence"] += entry["consequence"]
            slot["charged"] += entry["charged"]
            for label, count in entry["costs"].items():
                if label.startswith("complication"):
                    slot["complication"] += count
                if "stress" in label:
                    slot["stressed"] += count
            slot["tie_cost"] += entry["outcome"].get("tie", 0)
            slot["fail_cost"] += entry["outcome"].get("failure", 0)
    return [{"action": key, **value} for key, value in table.items()]


def _md_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


def render_markdown(result: Mapping[str, Any]) -> str:
    """The measured tables, as markdown, so the document can quote the harness verbatim."""
    lines: list[str] = []
    method = result["method"]
    lines.append(
        f"Seeds per run: **{method['seeds_per_run']}** (seeds {method['seed_range'][0]}–"
        f"{method['seed_range'][1]}), case `{method['case_id']}`."
    )
    lines.append("")

    route_stats = summarise(result["routes"])
    lines.append("### Route replays (shipped demo paths)")
    lines.append("")
    rows = []
    for label, stats in route_stats.items():
        ending = ", ".join(f"{k} ({v})" for k, v in stats["endings"].items())
        rows.append(
            [
                f"`{label}`",
                stats["n"],
                ending,
                _pct(stats["degraded"], stats["n"]),
                stats["checks"]["mean"],
                stats["checks"]["p10_90"],
                stats["rolls"]["mean"],
                _pct(stats["chain"].get(3, 0), stats["n"]),
                _pct(stats["partial"], stats["n"]),
                stats["complications"]["mean"],
                _pct(stats["wounds"]["party_runs"], stats["n"]),
                _pct(stats["wounds"]["party_taken_out"], stats["n"]),
            ]
        )
    lines.append(
        _md_table(
            [
                "route",
                "runs",
                "ending",
                "degraded",
                "checks mean",
                "checks p10–p90",
                "rolls mean",
                "3/3 chain",
                "partial",
                "complications mean",
                "party wounded",
                "party taken out",
            ],
            rows,
        )
    )
    lines.append("")
    lines.append("Outcome of the closing check, per route:")
    lines.append("")
    rows = []
    for label, stats in route_stats.items():
        outcomes = stats["outcomes"]
        rows.append(
            [
                f"`{label}`",
                outcomes.get("failure", 0),
                outcomes.get("tie", 0),
                outcomes.get("success", 0),
                outcomes.get("success_with_style", 0),
            ]
        )
    lines.append(_md_table(["route", "failure", "tie", "success", "style"], rows))
    lines.append("")

    policy_stats = summarise(result["policies"])
    lines.append("### Policies (every ending, plus an arbitrary party)")
    lines.append("")
    rows = []
    for label, stats in policy_stats.items():
        ending = ", ".join(f"{k} ({v})" for k, v in stats["endings"].items())
        rows.append(
            [
                f"`{label}`",
                stats["n"],
                ending,
                _pct(stats["degraded"], stats["n"]),
                stats["checks"]["mean"],
                stats["checks"]["p10_90"],
                _pct(stats["chain"].get(3, 0), stats["n"]),
                _pct(stats["chain"].get(2, 0), stats["n"]),
                _pct(stats["chain"].get(1, 0) + stats["chain"].get(0, 0), stats["n"]),
                _pct(stats["partial"], stats["n"]),
                stats["blocked"],
                stats["refused"],
            ]
        )
    lines.append(
        _md_table(
            [
                "policy / requested",
                "runs",
                "ending",
                "degraded",
                "checks mean",
                "checks p10–p90",
                "3/3",
                "2/3",
                "≤1",
                "partial",
                "blocked",
                "refused",
            ],
            rows,
        )
    )
    lines.append("")
    lines.append("Scenes played before the ending:")
    lines.append("")
    rows = []
    for label, stats in policy_stats.items():
        scenes = ", ".join(f"{k}: {v}" for k, v in sorted(stats["scenes"].items()))
        rows.append([f"`{label}`", scenes])
    lines.append(_md_table(["policy / requested", "scenes per run"], rows))
    lines.append("")

    lines.append("### Lethality and cost")
    lines.append("")
    rows = []
    for label, stats in list(route_stats.items()) + list(policy_stats.items()):
        rows.append(
            [
                f"`{label}`",
                stats["n"],
                _pct(stats["wounds"]["party_runs"], stats["n"]),
                _pct(stats["wounds"]["suspect_runs"], stats["n"]),
                _pct(stats["wounds"]["party_taken_out"], stats["n"]),
                stats["stress"]["mean_boxes"],
                _pct(stats["stress"]["runs_with_any"], stats["n"]),
                stats["complications"]["mean"],
                _pct(stats["consequences"]["runs_with_any"], stats["n"]),
            ]
        )
    lines.append(
        _md_table(
            [
                "run family",
                "runs",
                "party wounded",
                "suspect wounded",
                "party taken out",
                "stress boxes mean",
                "any stress",
                "complications mean",
                "named consequence",
            ],
            rows,
        )
    )
    lines.append("")
    lines.append("Named consequences written, by character (runs with at least one):")
    lines.append("")
    rows = []
    for label, stats in list(route_stats.items()) + list(policy_stats.items()):
        values = ", ".join(
            f"{character} {count}"
            for character, count in sorted(stats["consequences"]["by_character"].items())
            if count
        )
        rows.append([f"`{label}`", values or "—"])
    lines.append(_md_table(["run family", "consequences (runs with at least one)"], rows))
    lines.append("")
    thorough = policy_stats.get("thorough:evidence")
    if thorough is not None:
        lines.append(
            f"Complications written by the thorough party (evidence ending, {thorough['n']} runs):"
        )
        lines.append("")
        rows = []
        for name, count in thorough["complications"]["distinct"].items():
            rows.append([f"`{name}`", count, _pct(count, thorough["n"])])
        lines.append(_md_table(["complication", "runs", "share of runs"], rows))
        lines.append("")

    lines.append("### Fail-forward price, per action (thorough party, all endings)")
    lines.append("")
    action_runs = [
        row
        for key in ("thorough:evidence", "thorough:confront", "thorough:refer")
        for row in result["policies"].get(key, ())
    ]
    rows = []
    for entry in _action_table(action_runs):
        checks = entry["checks"]
        outcome = entry["outcome"]
        rows.append(
            [
                f"`{entry['action']}`",
                f"{entry['skill']} {entry['band']} ({entry['difficulty']})",
                checks,
                _pct(outcome.get("success_with_style", 0), checks),
                _pct(outcome.get("success", 0), checks),
                _pct(outcome.get("tie", 0), checks),
                _pct(outcome.get("failure", 0), checks),
                _pct(entry["charged"], checks),
                _pct(entry["consequence"], checks),
            ]
        )
    lines.append(
        _md_table(
            [
                "action",
                "check",
                "rolls",
                "style",
                "success",
                "tie",
                "failure",
                "price charged",
                "named consequence",
            ],
            rows,
        )
    )
    lines.append("")

    lines.append("### Closing check, and the aspect economy")
    lines.append("")
    rows = []
    for label, stats in list(route_stats.items()) + list(policy_stats.items()):
        outcomes = stats["outcomes"]
        n = stats["n"]
        rows.append(
            [
                f"`{label}`",
                _pct(outcomes.get("failure", 0), n),
                _pct(outcomes.get("tie", 0), n),
                _pct(outcomes.get("success", 0), n),
                _pct(outcomes.get("success_with_style", 0), n),
                stats["invocations"]["runs_with_any"],
                stats["invocations"]["mean"],
                stats["invocations"]["free"],
                stats["invocations"]["paid"],
                stats["invocations"]["closing_offered"],
                stats["invocations"]["closing_free"],
            ]
        )
    lines.append(
        _md_table(
            [
                "run family",
                "closing failure",
                "closing tie",
                "closing success",
                "closing style",
                "runs invoking on an action",
                "invokes/run",
                "free",
                "paid",
                "runs offering one to the closing check",
                "…of which free",
            ],
            rows,
        )
    )
    lines.append("")
    lines.append("### The clue chain")
    lines.append("")
    rows = []
    for label, stats in list(route_stats.items()) + list(policy_stats.items()):
        n = stats["n"]
        rows.append(
            [
                f"`{label}`",
                _pct(stats["chain"].get(3, 0), n),
                _pct(stats["chain"].get(2, 0), n),
                _pct(stats["chain"].get(1, 0), n),
                _pct(stats["chain"].get(0, 0), n),
                _pct(stats["partial"], n),
                _pct(stats["chain_missing"]["runs"], n),
                ", ".join(
                    f"`{clue}` {count}"
                    for clue, count in stats["chain_missing"]["by_clue"].items()
                )
                or "—",
                ", ".join(
                    f"`{clue}` {count}" for clue, count in stats["withheld"]["by_clue"].items()
                )
                or "—",
            ]
        )
    lines.append(
        _md_table(
            [
                "run family",
                "3/3",
                "2/3",
                "1/3",
                "0/3",
                "partial finding",
                "runs with a recorded gap",
                "fragments missing (runs)",
                "fragments withheld by a failure",
            ],
            rows,
        )
    )
    lines.append("")

    lines.append("### Check load")
    rows = []
    for label, stats in policy_stats.items():
        total = sum(stats["skills"].values()) or 1
        rows.append(
            [
                f"`{label}`",
                ", ".join(
                    f"{skill} {count} ({_pct(count, total)})"
                    for skill, count in sorted(stats["skills"].items())
                ),
            ]
        )
    lines.append(_md_table(["policy / requested", "checks by skill"], rows))
    lines.append("")
    rows = []
    for label, stats in policy_stats.items():
        rows.append(
            [f"`{label}`", ", ".join(f"{k} {v}" for k, v in sorted(stats["scene_ids"].items()))]
        )
    lines.append(_md_table(["policy / requested", "checks by scene"], rows))
    lines.append("")

    lines.append("### Skill dependency (thorough party, evidence ending)")
    lines.append("")
    rows = []
    skill_stats = summarise(result["skills"])
    for label, stats in skill_stats.items():
        ending = ", ".join(f"{k} ({v})" for k, v in stats["endings"].items())
        rows.append(
            [
                f"without `{label}`",
                ending,
                _pct(stats["finding"] - stats["partial"], stats["n"]),
                _pct(stats["partial"], stats["n"]),
                _pct(stats["chain"].get(3, 0), stats["n"]),
                stats["checks"]["mean"],
                stats["blocked"],
            ]
        )
    lines.append(
        _md_table(
            ["probe", "ending", "clean finding", "partial finding", "3/3", "checks mean", "blocked"],
            rows,
        )
    )
    lines.append("")

    lines.append("### Forced extremes (one run each)")
    lines.append("")
    rows = []
    for label, run in result["extremes"].items():
        rows.append(
            [
                f"`{label}`",
                run["applied"],
                run["outcome"],
                run["chain_held"],
                run["partial"],
                run["checks"],
                len(run["complications"]),
                len(run["wounds"]),
                run["taken_out"],
                run["blocked_states"],
            ]
        )
    lines.append(
        _md_table(
            ["run", "ending", "closing outcome", "chain", "partial", "checks", "complications",
             "wounds", "taken out", "blocked"],
            rows,
        )
    )
    lines.append("")

    lines.append("### Options: each author question, measured both ways")
    lines.append("")
    lines.append(
        "Every block below runs the **same seeds** twice, once on the setting the shipped case "
        "declares and once on the alternative `strategy_game.casework.options` builds. The first row "
        "of each block is the shipped setting. No row is a recommendation."
    )
    lines.append("")
    for group, settings in result.get("options", {}).items():
        lines.append(f"**{group}**")
        lines.append("")
        rows = []
        for label, runs in settings:
            stats = summarise({label: runs})[label]
            n = stats["n"]
            rows.append(
                [
                    label,
                    n,
                    ", ".join(f"{k} ({v})" for k, v in sorted(stats["endings"].items())),
                    _pct(stats["chain"].get(3, 0), n),
                    _pct(stats["partial"], n),
                    _pct(stats["chain_missing"]["runs"], n),
                    stats["checks"]["mean"],
                    stats["complications"]["mean"],
                    _pct(stats["wounds"]["party_runs"], n),
                    stats["invocations"]["mean"],
                    _pct(stats["invocations"]["closing_offered"], n),
                ]
            )
        lines.append(
            _md_table(
                [
                    "setting",
                    "runs",
                    "ending",
                    "3/3",
                    "partial finding",
                    "a gap recorded",
                    "checks mean",
                    "complications mean",
                    "party wounded",
                    "invokes/run",
                    "closing invoke",
                ],
                rows,
            )
        )
        lines.append("")

    determinism = result["determinism"]
    lines.append("### Determinism")
    lines.append("")
    lines.append(
        f"- Route runs replayed twice and compared on report + campaign payload: "
        f"**{determinism['runs_compared']}** compared, **{len(determinism['mismatched'])}** "
        f"mismatched."
    )
    lines.append(
        f"- Mid-play save → reload → finish compared with an uninterrupted run: "
        f"**{determinism['reload_compared']}** compared, "
        f"**{len(determinism['reload_mismatched'])}** mismatched."
    )
    return "\n".join(lines)


# -- entry point --------------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m strategy_game.tools.playtest_second_shadow",
        description=(
            "Play *The Second Shadow* across every route and policy and print measured playtest "
            "tables (issue #516 evidence). This changes no rule."
        ),
    )
    parser.add_argument("--seeds", type=int, default=300, help="seeds per route and policy")
    parser.add_argument("--start", type=int, default=0, help="first seed (default 0)")
    parser.add_argument("--json", default=None, help="write the full measured record here")
    args = parser.parse_args(argv)

    result = probe(args.seeds, start=args.start)
    if args.json:
        Path(args.json).write_text(
            json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )
    print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
