"""The casework session: one playable investigation on the approved rules kernel (#502).

The session composes what the repository already has and invents no rule:

============================  ==============================================================
five seats, one action each   :class:`strategy_game.rpg.roster.TurnLedger` over
                              :func:`~strategy_game.rpg.roster.default_seats` — one leader and
                              four agents (#461/#482). A scene is one turn: every character may
                              attempt one thing, and leaving the scene opens the next turn.
checks                        :func:`strategy_game.rpg.skills.check` in
                              :attr:`~strategy_game.rpg.skills.ActionContext.INDIVIDUAL` — the
                              approved Fate kernel, the six individual skills (#482), 4dF
scene aspects                 :class:`strategy_game.rpg.scene.Scene` — free invocations created by
                              a successful create-advantage action and spent by a later check
hits, stress, consequences    :func:`strategy_game.rpg.scene.apply_hit` — the one hit procedure
cyber reachability            :meth:`strategy_game.cyber.ConnectivityModel.resolve_access` — the
                              question asked **before** any skill roll (#344)
psi capability gate           :func:`strategy_game.rpg.skills.require_capability` — a named
                              ``competence`` TAG, refused before any dice (#482)
the one faction writer        :func:`strategy_game.campaign.missions.apply_mission_outcome` —
                              called **once**, at :meth:`CaseSession.resolve`
============================  ==============================================================

Fail-forward, stated exactly
----------------------------

The rulebook's own guidance is *"never make an essential clue depend on one successful check"* and
Fate's own failure text is *"in some overcome actions the GM may allow success at a serious cost"*.
So an action that yields a clue yields it on a tie and on a failure too **unless the case declares
otherwise**; the difference is the **price**, declared per action in the case file (a complication,
stress, or a named consequence). A tie costs the minor price, a failure the serious one. A
create-advantage action is the exception: it grants no clue on a failure, because the clue must never
have depended on it.

An action marked ``withhold_on_failure`` takes Fate's *other* reading of a failed overcome — *you do
not get it* — and withholds its fragment, charging the serious price instead. That is what lets a
chain end short. It is still fail-forward on three counts and each is measured: the price lands, the
case reaches every fragment by more than one action (so the other route is still on offer in the
same scene), and a short chain still assembles a **partial** finding with its gap named — or, below
the partial floor, closes on the weaker resolution with the gap on the record. Nothing dead-ends.

Aspects, stated exactly
-----------------------

A scene carries the **situation aspects its declaration names** from the first moment, and the ones
a create-advantage action earns join the same register. Any check may invoke one — a free invocation
if the aspect still has one, otherwise a Fate point from the character attempting the check — and the
+2 lands in the resolver's arithmetic. The closing check honours an invocation on **every** path,
passive and opposed: an opposed contest is one more check in the same scene, not a second resolver.

Combat is optional, one exchange, and losable
---------------------------------------------

A confrontation can be attempted with words (an opposed Savvy contest) or with force (an opposed
attack), and the case can always be closed without either. There is **one exchange**, not a combat
round: no initiative, no action economy, no turn order, no cover and no death rule — all of those are
author rows D34/D36 and remain open. A lost exchange writes a named mild consequence through
:func:`~strategy_game.rpg.scene.apply_hit` and **ends the case on the weaker resolution**, which is
what makes the fight dangerous rather than decorative.

What the session deliberately does not do
-----------------------------------------

* It does not rate, balance or aggregate outcomes. A resolution carries the ``Outcome`` of its own
  closing check, because that is an outcome the engine produced.
* It does not decide what a consequence *means* strategically (row D35). The injury lives on the
  sheet the campaign holds, and the faction-visible consequence is written as **named labels and id
  inventories** through the one writer — never as a magnitude.
* It does not narrate a death. ``taken out`` is recorded as the word Fate uses and nothing more.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Any

from ..campaign.missions import MissionOutcome, apply_mission_outcome
from ..campaign.state import Campaign, CampaignError, campaign_from_dict
from ..cyber import ConnectivityModel, load_connectivity
from ..rpg.fate import Action, Character, Outcome, resolve
from ..rpg.roster import RosterError, Seat, TurnLedger, default_seats
from ..rpg.scene import Hit, Scene, apply_hit
from ..rpg.skills import ActionContext, SkillLayerError, require_capability
from ..rpg.skills import check as skill_check
from .spec import (
    ActionSpec,
    CaseFile,
    CaseSpecError,
    Cost,
    CyberGate,
    ResolutionSpec,
)

__all__ = [
    "SESSION_SCHEMA_VERSION",
    "ActionResult",
    "CaseSession",
    "CaseworkError",
    "FindingResult",
    "ResolutionResult",
    "load_session",
]

#: Shape marker of a saved session. A foreign marker is refused rather than guessed into shape.
SESSION_SCHEMA_VERSION = "case-session-1"

#: The session's own dice seed when a caller supplies none. Recorded so a run can be replayed.
DEFAULT_SEED = 502

#: Fate's mild consequence slot. The one severity a single exchanged hit writes onto a sheet.
MILD_CONSEQUENCE = 2


class CaseworkError(ValueError):
    """A case operation the declaration or the campaign state does not allow."""


@dataclass(frozen=True)
class ActionResult:
    """What one attempted action produced. A refusal is a result, not an exception."""

    ok: bool
    scene_id: str
    action_id: str
    seat_id: str
    character_id: str = ""
    outcome: Outcome | None = None
    shifts: int = 0
    dice: tuple[int, ...] = ()
    total: int = 0
    difficulty: int = 0
    skill: str = ""
    clues: tuple[str, ...] = ()
    intel: tuple[str, ...] = ()
    aspect: str = ""
    costs: tuple[str, ...] = ()
    complications: tuple[str, ...] = ()
    consequence: str = ""
    taken_out: bool = False
    reason: str = ""
    scene_changed: str = ""
    #: Clues this action would have yielded but did not, because its failure withholds them.
    withheld: tuple[str, ...] = ()
    #: The aspect invoked on the check, and whether it was a free invocation or a Fate point.
    invoked: str = ""
    free_invocation: bool = False


@dataclass(frozen=True)
class FindingResult:
    """What assembling a clue chain produced. ``partial`` is a real, recorded shortfall."""

    ok: bool
    finding_id: str
    partial: bool = False
    already: bool = False
    missing: tuple[str, ...] = ()
    text: str = ""
    complication: str = ""
    reason: str = ""


@dataclass(frozen=True)
class ResolutionResult:
    """How the case ended, and what that wrote into the campaign's persistent state."""

    resolution_id: str
    label: str
    text: str
    outcome: Outcome
    detail: str = ""
    applied: MissionOutcome | None = None
    idempotent: bool = False
    degraded: bool = False
    wounds: tuple[str, ...] = ()
    #: Chain fragments the party never obtained. A short chain is a recorded gap, not a silence.
    gaps: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "resolution_id": self.resolution_id,
            "label": self.label,
            "text": self.text,
            "outcome": self.outcome.value,
            "detail": self.detail,
            "degraded": self.degraded,
            "wounds": list(self.wounds),
            "gaps": list(self.gaps),
            "applied": None if self.applied is None else self.applied.to_dict(),
        }


def _encode_rng_state(state: tuple[Any, ...]) -> list[Any]:
    """``Random.getstate()`` as JSON — the tuple of 625 ints becomes a list, nothing else changes."""
    return [int(state[0]), [int(value) for value in state[1]], state[2]]


def _decode_rng_state(payload: Any) -> tuple[Any, ...]:
    if not isinstance(payload, (list, tuple)) or len(payload) != 3:
        raise CaseworkError("a saved session's rng_state must be a three-part state record")
    return (int(payload[0]), tuple(int(value) for value in payload[1]), payload[2])


@dataclass
class CaseSession:
    """One case in progress: the scene, the five seats, the ledger, and what has been learned."""

    spec: CaseFile
    campaign: Campaign
    seed: int = DEFAULT_SEED
    rng: Random | None = None

    _connectivity: ConnectivityModel | None = field(default=None, init=False, repr=False)
    _scene: Scene = field(default_factory=Scene, init=False, repr=False)
    _scene_index: int = field(default=0, init=False, repr=False)
    _ledger: TurnLedger | None = field(default=None, init=False, repr=False)
    _dice: Random = field(default_factory=Random, init=False, repr=False)
    _used: set[str] = field(default_factory=set, init=False, repr=False)
    _clues: list[str] = field(default_factory=list, init=False, repr=False)
    _intel: list[str] = field(default_factory=list, init=False, repr=False)
    _findings: list[str] = field(default_factory=list, init=False, repr=False)
    _partial: set[str] = field(default_factory=set, init=False, repr=False)
    _complications: list[str] = field(default_factory=list, init=False, repr=False)
    _actors: list[str] = field(default_factory=list, init=False, repr=False)
    _events: list[dict[str, Any]] = field(default_factory=list, init=False, repr=False)
    _wounds: list[dict[str, Any]] = field(default_factory=list, init=False, repr=False)
    _applied: MissionOutcome | None = field(default=None, init=False, repr=False)
    _resolution_id: str = field(default="", init=False, repr=False)
    _seat_list: tuple[Seat, ...] = field(default=(), init=False, repr=False)

    # -- construction ----------------------------------------------------------

    def __post_init__(self) -> None:
        try:
            self.spec.validate()
        except CaseSpecError as exc:
            raise CaseworkError(str(exc)) from exc
        try:
            faction = self.campaign.faction()
        except CampaignError as exc:
            raise CaseworkError(str(exc)) from exc
        if not self.campaign.leader_id:
            raise CaseworkError("a case needs the faction-leader PC; the campaign declares no leader")
        agents = self.campaign.agent_views()
        try:
            seats = default_seats(self.campaign.leader_id, tuple(a.identifier for a in agents))
        except RosterError as exc:
            raise CaseworkError(str(exc)) from exc
        self._seat_list = seats
        if self.spec.id not in self.campaign.cases:
            raise CaseworkError(
                f"case {self.spec.id!r} is not on this campaign; add the campaign's Case record "
                "before play, because the outcome writer needs somewhere to record evidence"
            )
        problems = self.campaign.structural_problems()
        if problems:
            raise CaseworkError(
                "the campaign is not structurally sound, so a case cannot be played on it:\n  "
                + "\n  ".join(problems)
            )
        self._ledger = TurnLedger(seats)
        self._dice = self.rng if self.rng is not None else Random(self.seed)
        self._scene = self._scene_with_declared_aspects()
        self._connectivity = load_connectivity()
        if faction.leader_id != self.campaign.leader_id:  # pragma: no cover - structural_problems
            raise CaseworkError("the campaign leader is not the faction's own leader")

    # -- the party -------------------------------------------------------------

    @property
    def seats(self) -> tuple[Seat, ...]:
        return self._seat_list

    @property
    def ledger(self) -> TurnLedger:
        return self._ledger  # type: ignore[return-value]

    @property
    def scene(self) -> Scene:
        return self._scene

    @property
    def scene_spec(self):
        return self.spec.scenes[self._scene_index]

    @property
    def turn(self) -> int:
        return self.ledger.turn

    @property
    def clues(self) -> tuple[str, ...]:
        return tuple(self._clues)

    @property
    def intel(self) -> tuple[str, ...]:
        return tuple(self._intel)

    @property
    def findings(self) -> tuple[str, ...]:
        return tuple(self._findings)

    @property
    def complications(self) -> tuple[str, ...]:
        return tuple(self._complications)

    @property
    def events(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._events)

    @property
    def wounds(self) -> tuple[dict[str, Any], ...]:
        return tuple(self._wounds)

    @property
    def finished(self) -> bool:
        return self._applied is not None

    @property
    def applied(self) -> MissionOutcome | None:
        return self._applied

    @property
    def chain_progress(self) -> tuple[int, int]:
        return (sum(1 for clue in self.spec.chain if clue in self._clues), len(self.spec.chain))

    @property
    def chain_gaps(self) -> tuple[str, ...]:
        """The chain fragments the party does not hold, in the chain's own order.

        A fragment can be missing because the party never went where it was (a scene left, an
        action unavailable) or because the check that would have yielded it failed and the case
        withholds on failure. Either way the gap is named rather than left implicit: it is what the
        assembly reports, what the resolution record carries, and what a reader of the record needs
        to see before believing the finding.
        """
        return tuple(clue for clue in self.spec.chain if clue not in self._clues)

    def has(self, reference: str) -> bool:
        """Whether the party currently holds this clue or finding."""
        return reference in self._clues or reference in self._findings

    def seat_for(self, reference: str) -> Seat:
        """A seat by its own id or by the character id holding it, so a caller may name either."""
        for seat in self._seat_list:
            if seat.id == reference or seat.character_id == reference:
                return seat
        raise CaseworkError(
            f"no seat or character {reference!r} in this roster; seats are "
            f"{[(seat.id, seat.character_id) for seat in self._seat_list]}"
        )

    def sheet(self, seat_id: str) -> Character:
        seat = self.seat_for(seat_id)
        sheet = self.campaign.sheets.get(seat.character_id)
        if sheet is None:  # pragma: no cover - campaign construction refuses it first
            raise CaseworkError(f"seat {seat.id!r} holds {seat.character_id!r}, which has no sheet")
        return sheet

    def character(self, character_id: str) -> Character:
        sheet = self.campaign.sheets.get(character_id)
        if sheet is None:
            raise CaseworkError(f"no sheet for character {character_id!r} on this campaign")
        return sheet

    def seats_available(self) -> tuple[str, ...]:
        return self.ledger.seats_available

    def acted(self) -> dict[str, str]:
        return dict(self.ledger.acted)

    # -- what can be attempted -------------------------------------------------

    def actions(self) -> tuple[dict[str, Any], ...]:
        """The current scene's actions with an availability verdict and its reason.

        A refusal is computed here for the reader: already resolved, a missing prerequisite, a cyber
        path that does not exist, a psi capability the witness lacks. It is the same verdict
        :meth:`act` returns, so a UI never offers something the session will refuse.
        """
        out: list[dict[str, Any]] = []
        for action in self.scene_spec.actions:
            reason = self._unavailable(action)
            out.append(
                {
                    "id": action.id,
                    "label": action.label,
                    "text": action.text,
                    "available": not reason,
                    "reason": reason,
                    "suggested_actor": action.suggested_actor,
                    "skill": "" if action.check is None else action.check.skill,
                    "band": "" if action.check is None else action.check.band,
                }
            )
        return tuple(out)

    def _unavailable(self, action: ActionSpec) -> str:
        if action.id in self._used:
            return f"{action.id!r} is already resolved; a clue is read once per case"
        missing = tuple(item for item in action.requires if not self.has(item))
        if missing:
            return f"{action.id!r} requires {list(missing)} first"
        if action.psi is not None:
            witness = self.campaign.sheets.get(action.psi.witness_id)
            if witness is None:
                return f"the psi witness {action.psi.witness_id!r} is not on this campaign"
            try:
                require_capability(witness, action.psi.capability)
            except SkillLayerError as exc:
                return str(exc)
        if action.finding:
            reason = self._assembly_refusal(action.finding)
            if reason:
                return reason
        if action.cyber is not None:
            assessment = self._assess(action.cyber)
            if not assessment.possible:
                return (
                    f"no access path: {assessment.reason}. The reachability question is answered "
                    f"before any skill roll (#344)"
                )
        return ""

    def _assess(self, gate):
        assert self._connectivity is not None
        return self._connectivity.resolve_access(
            gate.target_class,
            gate.era,
            gate.path,
            local_presence=gate.local_presence,
            authorised=gate.authorised,
        )

    def probe_access(
        self,
        target_class: str,
        era: str,
        path: str,
        *,
        local_presence: bool = False,
        authorised: bool = False,
    ) -> dict[str, Any]:
        """Ask the connectivity model one reachability question, as a UI or a test would.

        This is issue #344's check, reported rather than rolled: *is the intrusion physically and
        logically possible, and along which access path?* It computes no difficulty and no odds.
        """
        return self._assess(
            CyberGate(
                target_class=target_class,
                era=era,
                path=path,
                local_presence=local_presence,
                authorised=authorised,
            )
        ).to_dict()

    # -- play ------------------------------------------------------------------

    def act(
        self,
        seat_id: str,
        action_id: str,
        *,
        free_invoke: str | None = None,
        invoke: str | None = None,
        reroll: bool = False,
    ) -> ActionResult:
        """Attempt one action with one character, spending that character's action for the scene.

        Refusals — unknown action, already resolved, missing prerequisite, the character already
        acted, a cyber path that does not exist, a psi capability the witness lacks — are returned
        with their reason and cost nothing. An **attempt** spends the action whether it succeeds or
        fails; that is the turn structure, not a new rule.

        Two ways to invoke an aspect on the check, which is Fate's one invoke rule:

        * ``free_invoke`` spends a **free invocation** a create-advantage action put on a scene
          aspect. It is refused, not silently downgraded, when the aspect has none left.
        * ``invoke`` spends a **Fate point** from the character attempting the check, on a scene
          aspect (declared situation aspects included) or on one of their own sheet aspects.

        Both add +2 through :func:`strategy_game.rpg.skills.check`, so an invocation lands in the
        same arithmetic as every other modifier; nothing here re-derives an outcome.
        """
        if self.finished:
            raise CaseworkError("the case is closed; a closed case does not take further actions")
        scene = self.scene_spec
        try:
            action = scene.action(action_id)
        except CaseSpecError as exc:
            raise CaseworkError(str(exc)) from exc
        if free_invoke is not None and invoke is not None:
            return self._refused(
                scene.id, action, seat_id, "one check carries at most one invocation"
            )
        if action_id in self._used:
            return self._refused(scene.id, action, seat_id, self._unavailable(action))
        missing = tuple(item for item in action.requires if not self.has(item))
        if missing:
            return self._refused(
                scene.id, action, seat_id, f"{action.id!r} requires {list(missing)} first"
            )
        seat = self.seat_for(seat_id)
        if seat.id in self.ledger.acted:
            return self._refused(scene.id, action, seat_id, self._ledger_refusal(seat.id))
        sheet = self.sheet(seat.id)
        named = free_invoke if free_invoke is not None else invoke
        if named is not None:
            refusal = self._invocation_refusal(named, sheet, free=free_invoke is not None)
            if refusal:
                return self._refused(scene.id, action, seat.id, refusal)
        reason = self._unavailable(action)
        if reason:
            return self._refused(scene.id, action, seat.id, reason)

        # Everything is validated; the action is spent from here on.
        try:
            self.ledger.declare(seat.id, statement=action.id)
        except RosterError as exc:  # pragma: no cover - guarded above
            return self._refused(scene.id, action, seat.id, str(exc))
        self._used.add(action.id)
        if seat.character_id not in self._actors:
            self._actors.append(seat.character_id)

        if action.finding:
            result = self.assemble(action.finding)
            if not result.ok:  # pragma: no cover - _unavailable validates the same condition
                return self._refused(scene.id, action, seat.id, result.reason)
            clues = self._grant_clues(action)
            intel = self._grant_intel(action)
            self._events.append(
                {
                    "kind": "case_action",
                    "scene": scene.id,
                    "action": action.id,
                    "seat": seat.id,
                    "character": seat.character_id,
                    "finding": action.finding,
                    "partial": result.partial,
                }
            )
            changed = self._advance_if_needed(action)
            return ActionResult(
                True,
                scene.id,
                action.id,
                seat.id,
                character_id=seat.character_id,
                clues=clues,
                intel=intel,
                scene_changed=changed,
                reason=result.reason,
            )

        if action.check is None:
            clues = self._grant_clues(action)
            intel = self._grant_intel(action)
            event = {
                "kind": "case_action",
                "scene": scene.id,
                "action": action.id,
                "seat": seat.id,
                "character": seat.character_id,
                "check": None,
                "clues": list(clues),
                "intel": list(intel),
            }
            self._events.append(event)
            changed = self._advance_if_needed(action)
            return ActionResult(
                True,
                scene.id,
                action.id,
                seat.id,
                character_id=seat.character_id,
                clues=clues,
                intel=intel,
                scene_changed=changed,
            )

        assert action.check is not None
        try:
            check = skill_check(
                sheet,
                ActionContext.INDIVIDUAL,
                action.check.action,
                action.check.skill,
                action.check.difficulty,
                rng=self._dice,
                scene=self._scene,
                invoked_aspect=named,
                free=free_invoke is not None,
                permitted=True,
                reroll=reroll,
            )
        except SkillLayerError as exc:  # pragma: no cover - the declaration validates the skill
            raise CaseworkError(f"action {action.id!r}: {exc}") from exc
        resolution = check.resolution
        style = resolution.outcome is Outcome.SUCCESS_WITH_STYLE
        success = resolution.outcome in (Outcome.SUCCESS, Outcome.SUCCESS_WITH_STYLE)

        clues: tuple[str, ...] = ()
        withheld: tuple[str, ...] = ()
        # Intel is the by-product of *taking* the action — the promise is made, the scan is
        # logged — so it is granted whatever the dice say. Clues are granted on every non-advantage
        # outcome, and the advantage action's own failure never withholds a clue because no clue
        # depends on it. An action the case marks ``withhold_on_failure`` is the other Fate reading:
        # a failed overcome does not get what it was after, and the declared failure price is what
        # it cost instead. Nothing else changes — the action is spent, the case goes on, the other
        # route to the same fragment is still on offer, and a short chain still assembles.
        intel = self._grant_intel(action)
        aspect = ""
        costs: list[str] = []
        consequence = ""
        taken_out = False
        if action.check.action is Action.CREATE_ADVANTAGE:
            if success:
                aspect = self._create_aspect(action.aspect, style=style)
            elif resolution.outcome is Outcome.TIE:
                costs.extend(self._apply_cost(sheet, action.on_tie, where=action.id))
            else:
                costs.extend(self._apply_cost(sheet, action.on_fail, where=action.id))
        else:
            # Overcome and attack: the clue is not hostage to the dice unless the case says so.
            if resolution.outcome is Outcome.FAILURE and action.withhold_on_failure and action.gives:
                withheld = tuple(clue for clue in action.gives if clue not in self._clues)
            else:
                clues = self._grant_clues(action)
            if resolution.outcome is Outcome.TIE:
                costs.extend(self._apply_cost(sheet, action.on_tie, where=action.id))
            elif resolution.outcome is Outcome.FAILURE:
                costs.extend(self._apply_cost(sheet, action.on_fail, where=action.id))
            if success and action.aspect:
                aspect = self._create_aspect(action.aspect, style=style)

        for cost_text in costs:
            if cost_text.startswith("consequence "):
                consequence = cost_text.split("consequence ", 1)[1].strip("'")
        # A hit that overflows the stress track is "taken out" whether or not it wrote a named
        # consequence; read the cost labels this action produced, not the earlier wound records.
        taken_out = any(label == "taken out" for label in costs) or any(
            w["character"] == seat.character_id and w.get("taken_out") for w in self._wounds
        )
        event = {
            "kind": "case_action",
            "scene": scene.id,
            "action": action.id,
            "seat": seat.id,
            "character": seat.character_id,
            "check": {
                "skill": action.check.skill,
                "difficulty": action.check.difficulty,
                "band": action.check.band,
                "dice": list(resolution.dice),
                "total": resolution.total,
                "shifts": resolution.shifts,
                "outcome": resolution.outcome.value,
                "invoked": named,
                "invoked_free": free_invoke is not None,
                "rerolled": bool(reroll),
            },
            "clues": list(clues),
            "withheld": list(withheld),
            "intel": list(intel),
            "aspect": aspect,
            "costs": list(costs),
            "consequence": consequence,
            "taken_out": taken_out,
        }
        self._events.append(event)
        changed = self._advance_if_needed(action)
        return ActionResult(
            True,
            scene.id,
            action.id,
            seat.id,
            character_id=seat.character_id,
            outcome=resolution.outcome,
            shifts=resolution.shifts,
            dice=tuple(resolution.dice),
            total=resolution.total,
            difficulty=action.check.difficulty,
            skill=action.check.skill,
            clues=clues,
            intel=intel,
            aspect=aspect,
            costs=tuple(costs),
            complications=tuple(self._complications),
            consequence=consequence,
            taken_out=taken_out,
            scene_changed=changed,
            withheld=withheld,
            invoked=named or "",
            free_invocation=free_invoke is not None,
        )

    def _refused(self, scene_id: str, action: ActionSpec, seat_id: str, reason: str) -> ActionResult:
        return ActionResult(False, scene_id, action.id, seat_id, reason=reason)

    def _invocation_refusal(self, name: str, sheet: Character, *, free: bool) -> str:
        """Why this invocation cannot be spent, or the empty string when it can.

        A **free** invocation must name a scene aspect that still has one: an aspect with none left
        is refused rather than quietly turned into a Fate-point spend, because that would charge the
        player for something the fiction already paid for. A **paid** invocation names a scene aspect
        (declared situation aspects included) or one of the character's own, and needs a Fate point.
        """
        in_scene = name in self._scene.aspects
        if free:
            if not in_scene:
                return (
                    f"{name!r} has no free invocation to spend: only a scene aspect a "
                    f"create-advantage action put there can carry one, and the scene holds "
                    f"{sorted(self._scene.aspects) or 'none'}"
                )
            if self._scene.aspects[name].free_invocations < 1:
                return (
                    f"{name!r} has no free invocations left this scene; invoke it with a Fate point "
                    f"instead (act(..., invoke={name!r}))"
                )
            return ""
        if not in_scene and name not in sheet.aspects:
            return (
                f"{name!r} is neither a scene aspect nor one of {sheet.name}'s aspects; the scene "
                f"declares {sorted(self._scene.aspects) or 'none'}"
            )
        if sheet.fate_points < 1:
            return (
                f"{sheet.name} has no Fate point left to invoke {name!r}; a free invocation costs "
                "nothing, a paid one costs a point of the character's own refresh"
            )
        return ""

    def _scene_with_declared_aspects(self, scene_id: str | None = None) -> Scene:
        """A fresh scene register holding the declaration's own situation aspects.

        A scene aspect is a fact the fiction establishes on arrival, so it is on the register from
        the first moment — with **no** free invocation, because a free invocation is what a
        create-advantage action earns and nothing else. That is the whole difference this makes: the
        party now walks into every scene with something it can invoke for +2 by spending Fate, and
        the aspects it creates sit beside them in the same register.
        """
        scene = Scene()
        wanted = self.spec.scene(scene_id) if scene_id else self.spec.scenes[self._scene_index]
        for name in wanted.aspects:
            scene.create_aspect(name, free_invocations=0)
        return scene

    def _ledger_refusal(self, seat_id: str) -> str:
        statement = self.ledger.acted.get(seat_id, "")
        return (
            f"{seat_id} has already acted this scene ({statement}). A character takes at most one "
            "action per turn (#461/#482); the next scene is a new ledger."
        )

    def _grant_clues(self, action: ActionSpec) -> tuple[str, ...]:
        added: list[str] = []
        for clue_id in action.gives:
            if clue_id not in self._clues:
                self._clues.append(clue_id)
                added.append(clue_id)
        return tuple(added)

    def _grant_intel(self, action: ActionSpec) -> tuple[str, ...]:
        added: list[str] = []
        for record in action.intel:
            if record not in self._intel:
                self._intel.append(record)
                added.append(record)
        return tuple(added)

    def _create_aspect(self, name: str, *, style: bool) -> str:
        if not name:
            return ""
        if name in self._scene.aspects:
            return name
        self._scene.create_aspect(name, free_invocations=2 if style else 1)
        return name

    def _apply_cost(self, sheet: Character, cost: Cost, *, where: str) -> list[str]:
        """Apply one declared cost through Fate's own stress/consequence procedure."""
        labels: list[str] = []
        for complication in cost.complications:
            if complication not in self._complications:
                self._complications.append(complication)
            labels.append(f"complication {complication!r}")
        if cost.consequence:
            occupied = any(
                item.severity == MILD_CONSEQUENCE and not item.recovered
                for item in sheet.consequences
            )
            if occupied:
                hit = apply_hit(sheet, max(1, cost.stress or 1), mental=cost.mental)
                labels.append("stress (the mild consequence slot was already taken)")
            else:
                hit = apply_hit(
                    sheet,
                    max(MILD_CONSEQUENCE, cost.stress),
                    mental=cost.mental,
                    consequence=(cost.consequence, MILD_CONSEQUENCE),
                )
                labels.append(f"consequence {cost.consequence!r}")
                self._wounds.append(
                    {
                        "character": sheet.id,
                        "name": cost.consequence,
                        "severity": MILD_CONSEQUENCE,
                        "source": where,
                        "stress_box": hit.stress_box,
                        "taken_out": hit.taken_out,
                    }
                )
        elif cost.stress:
            hit = apply_hit(sheet, cost.stress, mental=cost.mental)
            labels.append(
                f"{cost.stress} {'mental' if cost.mental else 'physical'} stress"
            )
        else:
            hit = None
        if hit is not None and hit.taken_out:
            labels.append("taken out")
        return labels

    def _advance_if_needed(self, action: ActionSpec) -> str:
        """Leave the scene when the action says so, or when no seat has an action left."""
        if action.next_scene:
            return self._enter(action.next_scene)
        if not self.ledger.seats_available:
            following = self.spec.next_scene_after(self.scene_spec.id)
            if following is not None:
                return self._enter(following.id)
        return ""

    def _enter(self, scene_id: str) -> str:
        self._scene_index = self.spec.scene_index(scene_id)
        self._scene = self._scene_with_declared_aspects(scene_id)
        self.ledger.next_turn()
        self._events.append(
            {"kind": "scene_change", "scene": scene_id, "turn": self.ledger.turn}
        )
        return scene_id

    def end_scene(self) -> str:
        """Leave the current scene early; every character's action refreshes in the next one."""
        if self.finished:
            raise CaseworkError("the case is closed")
        following = self.spec.next_scene_after(self.scene_spec.id)
        if following is None:
            raise CaseworkError(
                "this is the last scene; close the case with resolve(...) instead of leaving it"
            )
        return self._enter(following.id)

    # -- the clue chain --------------------------------------------------------

    def assemble(self, finding_id: str) -> FindingResult:
        """Assemble fragments into a conclusion. The deduction is never handed over by one clue.

        With every required fragment the finding is clean. Short of that, a finding with
        ``partial_min`` fragments can still be assembled and carries its declared complication —
        a weaker record, not a dead end. Below that, the refusal names exactly what is missing.
        """
        try:
            finding = self.spec.finding(finding_id)
        except CaseSpecError as exc:
            raise CaseworkError(str(exc)) from exc
        if finding_id in self._findings:
            return FindingResult(
                True, finding_id, already=True, text=finding.text,
                partial=finding_id in self._partial,
            )
        missing_all = [fragment for fragment in finding.requires_all if fragment not in self._clues]
        one_of_ok = not finding.requires_one_of or any(
            fragment in self._clues for fragment in finding.requires_one_of
        )
        if not missing_all and one_of_ok:
            self._findings.append(finding_id)
            self._events.append(
                {"kind": "finding", "finding": finding_id, "partial": False, "missing": []}
            )
            return FindingResult(True, finding_id, text=finding.text)

        held = sum(1 for fragment in finding.fragments if fragment in self._clues)
        if finding.partial_min and held >= finding.partial_min:
            self._findings.append(finding_id)
            self._partial.add(finding_id)
            if finding.partial_complication and finding.partial_complication not in self._complications:
                self._complications.append(finding.partial_complication)
            self._events.append(
                {
                    "kind": "finding",
                    "finding": finding_id,
                    "partial": True,
                    "missing": list(missing_all),
                }
            )
            return FindingResult(
                True,
                finding_id,
                partial=True,
                text=finding.text,
                complication=finding.partial_complication,
                reason=(
                    f"assembled from {held} of {len(finding.fragments)} fragments: "
                    f"{list(missing_all)} missing. The record says the chain is incomplete."
                ),
            )
        return FindingResult(
            False,
            finding_id,
            missing=tuple(missing_all),
            reason=self._assembly_refusal(finding_id),
        )

    def _finding_missing(self, finding_id: str) -> tuple[str, ...]:
        """The fragments this assembled finding had to do without — its recorded shortfall."""
        finding = self.spec.finding(finding_id)
        return tuple(
            fragment for fragment in finding.requires_all if fragment not in self._clues
        )

    def _assembly_refusal(self, finding_id: str) -> str:
        """Why this finding cannot be assembled yet, or the empty string when it can."""
        finding = self.spec.finding(finding_id)
        if finding_id in self._findings:
            return ""
        missing_all = [f for f in finding.requires_all if f not in self._clues]
        one_of_ok = not finding.requires_one_of or any(
            f in self._clues for f in finding.requires_one_of
        )
        if not missing_all and one_of_ok:
            return ""
        held = sum(1 for fragment in finding.fragments if fragment in self._clues)
        if finding.partial_min and held >= finding.partial_min:
            return ""
        return (
            f"{finding_id!r} cannot be assembled yet: {list(missing_all)} missing, and "
            f"{held} of {len(finding.fragments)} fragments held (partial needs "
            f"{finding.partial_min})."
        )

    # -- resolutions -----------------------------------------------------------

    def resolutions(self) -> tuple[dict[str, Any], ...]:
        """The endings this case offers, with availability and reason, in declaration order."""
        out: list[dict[str, Any]] = []
        for resolution in self.spec.resolutions:
            reason = self._resolution_unavailable(resolution)
            out.append(
                {
                    "id": resolution.id,
                    "label": resolution.label,
                    "available": not reason,
                    "reason": reason,
                    "skill": resolution.skill,
                    "band": resolution.band,
                    "opposed_by": resolution.opposed_by,
                }
            )
        return tuple(out)

    def _resolution_unavailable(self, resolution: ResolutionSpec) -> str:
        if self.finished:
            return "the case is already closed"
        if resolution.requires_finding and resolution.requires_finding not in self._findings:
            return (
                f"{resolution.id!r} needs the assembled finding "
                f"{resolution.requires_finding!r}; assemble the chain first"
            )
        missing = tuple(item for item in resolution.requires if item not in self._clues)
        if missing:
            return (
                f"{resolution.id!r} needs {list(missing)} in hand first; without them the party "
                "has nobody to confront"
            )
        if resolution.requires_fragments:
            held = sum(1 for clue in self.spec.chain if clue in self._clues)
            if held < resolution.requires_fragments:
                return (
                    f"{resolution.id!r} needs {resolution.requires_fragments} facts from the chain; "
                    f"the party holds {held}"
                )
        return ""

    def resolve(
        self,
        resolution_id: str,
        *,
        seat_id: str | None = None,
        approach: str = "",
        free_invoke: str | None = None,
        invoke: str | None = None,
    ) -> ResolutionResult:
        """Close the case and write the result into the campaign's persistent state, once.

        ``approach`` selects the confrontation's method: ``"pressure"`` (an opposed Savvy contest) or
        ``"force"`` (one opposed attack exchange). Any other resolution ignores it.

        ``free_invoke``/``invoke`` reach the closing check on **every** path, passive and opposed
        alike: the actor's roll goes through the same scene resolver either way, so a free invocation
        earned in the final scene is worth +2 to a contest exactly as it is to a passive overcome.
        Before this, both opposed paths silently dropped it, which made the case's one spendable
        aspect worth nothing at the one moment the case is decided by a single roll.

        Idempotent: the second call returns the record already applied and writes nothing.
        """
        if self._applied is not None:
            spec = self.spec.resolution(self._resolution_id)
            return ResolutionResult(
                spec.id, spec.label, spec.text, self._applied.outcome,
                applied=self._applied, idempotent=True, gaps=self.chain_gaps,
            )
        if self.finished:  # pragma: no cover - _applied is the only marker
            raise CaseworkError("the case is closed")
        if free_invoke is not None and invoke is not None:
            raise CaseworkError("one closing check carries at most one invocation")
        try:
            spec = self.spec.resolution(resolution_id)
        except CaseSpecError as exc:
            raise CaseworkError(str(exc)) from exc
        reason = self._resolution_unavailable(spec)
        if reason:
            raise CaseworkError(reason)

        leader_seat = next(seat for seat in self._seat_list if seat.character_id == self.campaign.leader_id)
        seat = self.seat_for(seat_id) if seat_id else leader_seat
        sheet = self.sheet(seat.id)
        named = free_invoke if free_invoke is not None else invoke
        if named is not None:
            refusal = self._invocation_refusal(named, sheet, free=free_invoke is not None)
            if refusal:
                raise CaseworkError(refusal)
        if seat.character_id not in self._actors:
            self._actors.append(seat.character_id)

        outcome, detail, degraded, wounds = self._closing_check(
            sheet, spec, approach=approach, free_invoke=free_invoke, invoke=invoke
        )

        ended = spec
        if degraded:
            ended = self.spec.resolution("closed_by_withdrawal")
            detail = f"{detail} The case falls back to a referral."

        gaps = self.chain_gaps
        if gaps:
            detail = (
                f"{detail} The chain is short {len(gaps)} of {len(self.spec.chain)} fragments: "
                f"{list(gaps)} never obtained, and the record says so."
            )
        if named:
            detail = f"{detail} Invoked {named!r} (+2, {'free' if free_invoke else 'a Fate point'})."

        findings = list(self._findings)
        intel = tuple(dict.fromkeys((*findings, *self._intel, *ended.intel)))
        reputation = list(ended.reputation)
        if outcome is Outcome.FAILURE and ended.on_fail_reputation:
            reputation = list(ended.on_fail_reputation)
        if any(item in self._partial for item in findings):
            reputation.append("case-chain-incomplete")
        report = MissionOutcome(
            mission_id=f"{self.spec.id}:{ended.id}",
            case_id=self.spec.id,
            outcome=outcome,
            leader_id=self.campaign.leader_id,
            agent_ids=tuple(
                character_id
                for character_id in self._actors
                if character_id != self.campaign.leader_id
            ),
            evidence_gained=tuple(self._clues),
            intel_gained=tuple(intel),
            resources_gained=ended.resources,
            reputation_labels_gained=tuple(dict.fromkeys(reputation)),
            objectives_completed=(ended.objective,),
            seed=None if self.rng is not None else self.seed,
        )
        self._applied = apply_mission_outcome(self.campaign, report)
        self._resolution_id = ended.id
        self._events.append(
            {
                "kind": "resolution",
                "resolution": ended.id,
                "requested": spec.id,
                "outcome": outcome.value,
                "degraded": degraded,
                "wounds": list(wounds),
                "invoked": named,
                "invoked_free": free_invoke is not None,
                "chain_gaps": list(gaps),
            }
        )
        return ResolutionResult(
            ended.id,
            ended.label,
            ended.text,
            outcome,
            detail=detail,
            applied=self._applied,
            degraded=degraded,
            wounds=tuple(wounds),
            gaps=gaps,
        )

    def _closing_check(
        self,
        sheet: Character,
        spec: ResolutionSpec,
        *,
        approach: str,
        free_invoke: str | None,
        invoke: str | None = None,
    ) -> tuple[Outcome, str, bool, list[str]]:
        """Roll the resolution's own closing check, including an optional opposed confrontation.

        Every path hands the actor's roll to :func:`strategy_game.rpg.skills.check` with the
        invocation attached, so an aspect is worth the same +2 whether the ending is a passive
        overcome or an opposed contest. The opposition (the suspect) invokes nothing: the case gives
        NPCs no Fate points, which would be a rules question, and an uninvoked defence is the
        honest floor for measuring how much the party's own aspects are worth.
        """
        force = spec.opposed_by and approach == "force"
        pressure = spec.opposed_by and approach == "pressure"
        if spec.opposed_by and approach not in ("force", "pressure"):
            raise CaseworkError(
                f"{spec.id!r} is a confrontation: choose approach='pressure' or approach='force'"
            )
        if force:
            return self._exchange(
                sheet, self.character(spec.opposed_by), spec,
                free_invoke=free_invoke, invoke=invoke,
            )
        if pressure:
            return self._contest(
                sheet, self.character(spec.opposed_by), spec,
                free_invoke=free_invoke, invoke=invoke,
            )
        try:
            result = skill_check(
                sheet,
                ActionContext.INDIVIDUAL,
                Action.OVERCOME,
                spec.skill,
                spec.difficulty,
                rng=self._dice,
                scene=self._scene,
                invoked_aspect=free_invoke or invoke,
                free=free_invoke is not None,
            ).resolution
        except SkillLayerError as exc:  # pragma: no cover - the declaration validates the skill
            raise CaseworkError(str(exc)) from exc
        wounds: list[str] = []
        degraded = False
        detail = (
            f"{spec.skill} {spec.band} ({spec.difficulty}): {result.total} vs {spec.difficulty}, "
            f"{result.outcome.value}"
        )
        if result.outcome is Outcome.FAILURE and spec.consequence:
            cost = Cost(stress=MILD_CONSEQUENCE, mental=spec.mental, consequence=spec.consequence)
            wounds = self._apply_cost(sheet, cost, where=spec.id)
            degraded = any("taken out" in label for label in wounds)
        elif result.outcome is Outcome.FAILURE and spec.opposed_by:
            degraded = True
        return result.outcome, detail, degraded, wounds

    def _contest(
        self,
        actor: Character,
        defender: Character,
        spec: ResolutionSpec,
        *,
        free_invoke: str | None = None,
        invoke: str | None = None,
    ) -> tuple[Outcome, str, bool, list[str]]:
        """An opposed social contest: both sides roll the approved kernel, highest total wins.

        The actor's roll goes through the scene resolver with its invocation, which is what makes a
        free invocation worth +2 here as well as on a passive check. The defender rolls the same
        kernel and does not invoke.
        """
        attack = self._actor_roll(
            actor, Action.OVERCOME, spec.skill, free_invoke=free_invoke, invoke=invoke
        )
        defence = resolve(
            Action.DEFEND, defender.skills.get(spec.skill, 0), attack.total, rng=self._dice
        )
        shifts = attack.total - defence.total
        outcome = (
            Outcome.FAILURE if shifts < 0
            else Outcome.TIE if shifts == 0
            else Outcome.SUCCESS_WITH_STYLE if shifts >= 3
            else Outcome.SUCCESS
        )
        detail = (
            f"opposed {spec.skill}: {actor.name} {attack.total} vs {defender.name} "
            f"{defence.total} — {outcome.value}"
        )
        if outcome is Outcome.TIE and spec.tie_is_not_total_failure:
            detail += " (a tie, and this case's tie option lets it stand)"
        return outcome, detail, self._degraded(outcome, spec), []

    def _exchange(
        self,
        actor: Character,
        defender: Character,
        spec: ResolutionSpec,
        *,
        free_invoke: str | None = None,
        invoke: str | None = None,
    ) -> tuple[Outcome, str, bool, list[str]]:
        """One attack exchange. The defender's defense is the attack's opposition, and a hit lands.

        There is no second exchange, no initiative and no turn order: those are open author rows
        (D34/D36). The consequence is named in the case data and applied by Fate's own hit procedure.

        Which skill the attack reads is the case's declaration: :attr:`ResolutionSpec.skill` by
        default, or :attr:`ResolutionSpec.force_attack_skill` when the case names one. Both are
        measurable options — this method does not choose between them.
        """
        skill = spec.force_attack_skill or spec.skill
        attack = self._actor_roll(
            actor, Action.ATTACK, skill, free_invoke=free_invoke, invoke=invoke
        )
        defence = resolve(
            Action.DEFEND, defender.skills.get("REF", 0), attack.total, rng=self._dice
        )
        shifts = attack.total - defence.total
        outcome = (
            Outcome.FAILURE if shifts < 0
            else Outcome.TIE if shifts == 0
            else Outcome.SUCCESS_WITH_STYLE if shifts >= 3
            else Outcome.SUCCESS
        )
        wounds: list[str] = []
        degraded = False
        if shifts > 0:
            hit = self._hit(defender, shifts, name=spec.consequence or "Cutter wound")
            detail = (
                f"opposed attack ({skill}): {actor.name} {attack.total} vs {defender.name} "
                f"{defence.total} — {shifts} shift(s), {defender.name} hit"
            )
            if hit.taken_out:
                detail += " and taken out"
            wounds = [f"{defender.name}: {hit_label(hit, spec.consequence)}"]
        elif shifts < 0:
            hit = self._hit(actor, -shifts, name=spec.consequence or "Cutter wound")
            detail = (
                f"opposed attack ({skill}): {actor.name} {attack.total} vs {defender.name} "
                f"{defence.total} — {-shifts} shift(s) against {actor.name}"
            )
            wounds = [f"{actor.name}: {hit_label(hit, spec.consequence)}"]
            degraded = True
        else:
            detail = (
                f"opposed attack ({skill}): {actor.name} {attack.total} vs {defender.name} "
                f"{defence.total} — a standoff, nobody lands a hit"
            )
            degraded = not spec.tie_is_not_total_failure
        return outcome, detail, degraded, wounds

    def _actor_roll(
        self,
        actor: Character,
        action: Action,
        skill: str,
        *,
        free_invoke: str | None,
        invoke: str | None,
    ):
        """The party's own half of an opposed check, through the scene resolver and its invocation."""
        try:
            return skill_check(
                actor,
                ActionContext.INDIVIDUAL,
                action,
                skill,
                0,
                rng=self._dice,
                scene=self._scene,
                invoked_aspect=free_invoke or invoke,
                free=free_invoke is not None,
            ).resolution
        except SkillLayerError as exc:  # pragma: no cover - the declaration validates the skill
            raise CaseworkError(str(exc)) from exc

    @staticmethod
    def _degraded(outcome: Outcome, spec: ResolutionSpec) -> bool:
        """Whether this closing outcome falls back to the weaker resolution.

        A tie and a failure both do, unless the case's tie option says otherwise: *what* a tie
        should cost is author row D32, so the option only decides whether a tie ends the attempt.
        """
        succeeded = outcome in (Outcome.SUCCESS, Outcome.SUCCESS_WITH_STYLE)
        stands_on_a_tie = outcome is Outcome.TIE and spec.tie_is_not_total_failure
        return not (succeeded or stands_on_a_tie)

    def _hit(self, target: Character, shifts: int, *, name: str) -> Hit:
        """One hit through the approved procedure; the mild slot is used if it is free."""
        occupied = any(
            item.severity == MILD_CONSEQUENCE and not item.recovered for item in target.consequences
        )
        consequence = None if occupied else (name, MILD_CONSEQUENCE)
        hit = apply_hit(target, max(1, shifts), consequence=consequence)
        if consequence is not None:
            self._wounds.append(
                {
                    "character": target.id,
                    "name": consequence[0],
                    "severity": MILD_CONSEQUENCE,
                    "source": "confrontation",
                    "stress_box": hit.stress_box,
                    "taken_out": hit.taken_out,
                }
            )
        return hit

    # -- reporting, saving, loading --------------------------------------------

    def report(self) -> dict[str, Any]:
        """The whole session as plain JSON — what a UI may read, and what persisted."""
        faction = self.campaign.faction()
        case = self.campaign.cases[self.spec.id]
        return {
            "schema_version": SESSION_SCHEMA_VERSION,
            "case_id": self.spec.id,
            "title": self.spec.title,
            "core_question": self.spec.core_question,
            "era": self.spec.era,
            "era_label": self.spec.era_label,
            "scene": {
                "id": self.scene_spec.id,
                "title": self.scene_spec.title,
                "location": self.scene_spec.location,
                "turn": self.turn,
            },
            "finished": self.finished,
            "resolution": self._resolution_id,
            "seed": None if self.rng is not None else self.seed,
            "clues": [
                {"id": clue, "label": self.spec.clue(clue).label} for clue in self._clues
            ],
            "intel": list(self._intel),
            "findings": [
                {
                    "id": finding,
                    "partial": finding in self._partial,
                    "missing": list(self._finding_missing(finding)),
                }
                for finding in self._findings
            ],
            "chain": {
                "held": self.chain_progress[0],
                "of": self.chain_progress[1],
                "missing": list(self.chain_gaps),
            },
            "complications": list(self._complications),
            "actors": list(self._actors),
            "party": [
                {
                    "seat": seat.id,
                    "character": seat.character_id,
                    "name": self.campaign.sheets[seat.character_id].name,
                    "acted": seat.id in self.ledger.acted,
                    "fate_points": self.campaign.sheets[seat.character_id].fate_points,
                    "physical_stress": list(
                        self.campaign.sheets[seat.character_id].physical_stress
                    ),
                    "mental_stress": list(self.campaign.sheets[seat.character_id].mental_stress),
                    "consequences": [
                        {"name": item.name, "severity": item.severity}
                        for item in self.campaign.sheets[seat.character_id].consequences
                    ],
                }
                for seat in self._seat_list
            ],
            "aspects": {
                name: aspect.free_invocations for name, aspect in self._scene.aspects.items()
            },
            "wounds": list(self._wounds),
            "persisted": {
                "objectives": list(faction.objectives),
                "intelligence_ids": list(faction.intelligence_ids),
                "reputation_labels": list(faction.reputation_labels),
                "resources": list(faction.resources),
                "case_evidence": list(case.evidence_ids),
                "campaign_notes": len(self.campaign.campaign_notes),
            },
            "events": list(self._events),
        }

    def to_dict(self) -> dict[str, Any]:
        """The session save payload: the party's state, the campaign's books, and the dice state."""
        return {
            "schema_version": SESSION_SCHEMA_VERSION,
            "case_id": self.spec.id,
            "campaign": self.campaign.to_dict(),
            "seed": None if self.rng is not None else self.seed,
            "rng_state": _encode_rng_state(self._dice.getstate()),
            "scene_index": self._scene_index,
            "turn": self.ledger.turn,
            "acted": dict(self.ledger.acted),
            "used_actions": sorted(self._used),
            "clues": list(self._clues),
            "intel": list(self._intel),
            "findings": list(self._findings),
            "partial_findings": sorted(self._partial),
            "complications": list(self._complications),
            "actors": list(self._actors),
            "events": list(self._events),
            "wounds": list(self._wounds),
            "aspects": {
                name: aspect.free_invocations for name, aspect in self._scene.aspects.items()
            },
            "resolution_id": self._resolution_id,
            "applied": None if self._applied is None else self._applied.to_dict(),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any], spec: CaseFile) -> CaseSession:
        """Rebuild a session from :meth:`to_dict`, refusing a foreign shape instead of guessing.

        The dice state is restored, so a case saved mid-scene resumes with the **same** subsequent
        rolls as an uninterrupted run. That is the property the determinism test pins.
        """
        if not isinstance(payload, Mapping):
            raise CaseworkError(f"a session save must be a mapping, got {type(payload).__name__}")
        if payload.get("schema_version") != SESSION_SCHEMA_VERSION:
            raise CaseworkError(
                f"unsupported session schema_version {payload.get('schema_version')!r}; expected "
                f"{SESSION_SCHEMA_VERSION!r}"
            )
        if payload.get("case_id") != spec.id:
            raise CaseworkError(
                f"the save is for case {payload.get('case_id')!r}, not {spec.id!r}"
            )
        seed = payload.get("seed")
        session = cls(
            spec=spec,
            campaign=campaign_from_dict(payload.get("campaign") or {}),
            seed=DEFAULT_SEED if seed is None else int(seed),
            rng=None,
        )
        session._dice.setstate(_decode_rng_state(payload.get("rng_state")))
        session._scene_index = int(payload.get("scene_index", 0))
        if not 0 <= session._scene_index < len(spec.scenes):
            raise CaseworkError("a saved session's scene_index is outside the case's scenes")
        session._ledger = TurnLedger(
            session._seat_list,
            turn=int(payload.get("turn", 0)),
            acted={str(k): str(v) for k, v in dict(payload.get("acted") or {}).items()},
        )
        session._used = {str(item) for item in (payload.get("used_actions") or [])}
        session._clues = [str(item) for item in (payload.get("clues") or [])]
        session._intel = [str(item) for item in (payload.get("intel") or [])]
        session._findings = [str(item) for item in (payload.get("findings") or [])]
        session._partial = {str(item) for item in (payload.get("partial_findings") or [])}
        session._complications = [str(item) for item in (payload.get("complications") or [])]
        session._actors = [str(item) for item in (payload.get("actors") or [])]
        session._events = [dict(item) for item in (payload.get("events") or [])]
        session._wounds = [dict(item) for item in (payload.get("wounds") or [])]
        session._scene = Scene()
        for name, free in dict(payload.get("aspects") or {}).items():
            session._scene.create_aspect(str(name), free_invocations=int(free))
        session._resolution_id = str(payload.get("resolution_id") or "")
        applied = payload.get("applied")
        session._applied = None if applied is None else MissionOutcome.from_dict(applied)
        if session._applied is not None:
            if not session._resolution_id:
                raise CaseworkError("a saved closed case names no resolution")
            spec.resolution(session._resolution_id)
        for clue in session._clues:
            spec.clue(clue)
        for finding in session._findings:
            spec.finding(finding)
        return session

    def save(self, path: str | Path) -> Path:
        """Write the session atomically: a partial save is not a save."""
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + ".tmp")
        temporary.write_text(
            json.dumps(self.to_dict(), indent=2, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
        temporary.replace(target)
        return target


def load_session(path: str | Path, spec: CaseFile) -> CaseSession:
    """Read a session written by :meth:`CaseSession.save` for the given case declaration."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise CaseworkError(f"{path!s} is not valid JSON: {exc}") from exc
    return CaseSession.from_dict(payload, spec)


def hit_label(hit: Hit, name: str) -> str:
    """A one-line description of where one hit went, for the demo and the record."""
    if hit.taken_out:
        return "taken out"
    parts: list[str] = []
    if hit.consequence is not None:
        parts.append(f"mild consequence {name!r}")
    if hit.stress_box is not None:
        parts.append(f"stress box {hit.stress_box}")
    return ", ".join(parts) or "hit absorbed"
