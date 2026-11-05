"""Scene procedures for the five live scene types (#1164, #1184).

A scene is an **interface shape**, not a second rules engine. Each procedure here answers the same
three questions and then hands the uncertainty to a module that already owns it:

* what may the player do in this scene?
* what does the scene *require* to be true before it can end?
* which existing module resolves the check?

| Scene | Resolved by | Produces |
| --- | --- | --- |
| Social | ``rules.social.resolve_social`` | a social tag (a fact, never a number) |
| Investigation | ``rules.investigation.discover`` | clue tags, one per clue actually found |
| Exploration | ``world.graphs.PhysicalGraph`` | visited places and what was found there |
| Cyber | ``rules.cwn_hacking.hacking_check`` + ``AlertClock`` | a device action outcome and network alert state |
| Action | ``world.graphs.PhysicalGraph`` + ``rules.physical_combat`` | a phase, an arrest, or a recorded use of force |

**Astral is not implemented.** It is postponed by author decision, and asking for it raises
``PostponedScene`` rather than silently returning an empty result — an unimplemented scene type must
be loud, or someone will ship a scene that resolves to nothing.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

# The repository imports its own packages two ways: from the repository root as ``src.world``
# (pytest's rootdir is on the path) and with ``src/`` itself on the path as ``world`` (the
# ``sys.path.insert`` style the older tests use). Supporting both here costs four lines and saves
# every caller from knowing which one it is.
try:  # pragma: no cover - the second branch is exercised by the other import style
    from src.rules.cwn_hacking import AlertClock, HackError, hacking_check
    from src.rules.investigation import Case, InvestigationError, Investigator, discover
    from src.rules.social import UNMOVED, SocialError, resolve_social
    from src.world.graphs import CyberGraph, GraphError, PhysicalGraph
    from src.world.narrative_tags import (
        ClueTag,
        Polarity,
        SocialTag,
        TagBook,
    )
except ModuleNotFoundError:  # pragma: no cover
    from rules.cwn_hacking import AlertClock, HackError, hacking_check
    from rules.investigation import Case, InvestigationError, Investigator, discover
    from rules.social import UNMOVED, SocialError, resolve_social
    from world.graphs import CyberGraph, GraphError, PhysicalGraph
    from world.narrative_tags import (
        ClueTag,
        Polarity,
        SocialTag,
        TagBook,
    )

#: What a scene may be. Astral is deliberately absent.
SCENE_TYPES: tuple[str, ...] = ("Social", "Investigation", "Exploration", "Action", "Cyber")

#: Named, not implemented. Kept visible so a caller can explain the omission to a player.
POSTPONED_SCENE_TYPES: tuple[str, ...] = ("Astral",)


class SceneError(ValueError):
    """A scene was asked to do something its type does not do."""


class PostponedScene(SceneError):
    """The scene type exists in the design and is deliberately not implemented yet."""


def _text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SceneError(f"{label} must be a nonempty string")
    return value.strip()


@dataclass(frozen=True, slots=True)
class SceneFrame:
    """The stable identity of a scene: who is in it, where, and what makes it end.

    ``exit_fact`` is the fact that must be established for the scene to close. It is a sentence, not
    a check: "the warrant number is in hand", "the suspect is in custody", "the device is ours".
    """

    id: str
    title: str
    scene_type: str
    participants: tuple[str, ...] = ()
    place: str = ""
    stakes: str = ""
    exit_fact: str = ""

    def __post_init__(self) -> None:
        _text(self.id, "scene id")
        _text(self.title, "scene title")
        if self.scene_type in POSTPONED_SCENE_TYPES:
            raise PostponedScene(
                f"{self.scene_type} scenes are postponed by author decision; "
                "they are not an empty implementation"
            )
        if self.scene_type not in SCENE_TYPES:
            raise SceneError(
                f"unknown scene type {self.scene_type!r}; known: {', '.join(SCENE_TYPES)}"
            )
        if any(not str(p).strip() for p in self.participants):
            raise SceneError("participants must be nonempty ids")


@dataclass(frozen=True, slots=True)
class SceneResult:
    """What a scene produced. ``facts`` are sentences the table can write down."""

    scene_id: str
    scene_type: str
    passed: bool
    facts: tuple[str, ...] = ()
    tags_added: tuple[Any, ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.scene_type not in SCENE_TYPES:
            raise SceneError(f"unknown scene type {self.scene_type!r}")


# --------------------------------------------------------------------------- #
# Social
# --------------------------------------------------------------------------- #

def run_social_scene(
    frame: SceneFrame,
    book: TagBook,
    *,
    holder: str,
    target: str,
    approach: str,
    actor_total: int,
    resistance_total: int,
    method: str,
    witnessed: bool = False,
    tag_id: str = "",
) -> SceneResult:
    """A conversation that is trying to change someone's mind.

    The one rule this procedure adds is the one that makes social tags matter: **without a lever
    there is no check**. A social scene with no social tag and no clue in hand is not a hard
    conversation, it is a conversation that does not move — so the procedure refuses to roll rather
    than letting a good die beat an empty hand.

    The check itself is CWN's, resolved by ``rules.social``. Coercion always leaves a Grievance, and
    this procedure records it as an unfavourable tag instead of inventing a penalty.
    """
    if frame.scene_type != "Social":
        raise SceneError("this procedure runs Social scenes")
    _text(holder, "holder")
    _text(target, "target")
    if holder == target:
        raise SceneError("a social scene needs two different parties")

    if not book.has_leverage(actor=target, subject=holder):
        return SceneResult(
            scene_id=frame.id,
            scene_type=frame.scene_type,
            passed=False,
            notes=(
                (
                    f"no lever on {holder}: nothing in the tag book bears on this ask, "
                    "so the conversation does not move and no check is made"
                ),
            ),
        )

    try:
        outcome = resolve_social(actor_total, resistance_total, method=method, witnessed=witnessed)
    except SocialError as exc:  # pragma: no cover - defensive, resolve_social validates its own input
        raise SceneError(str(exc)) from exc

    passed = outcome.consequence != UNMOVED
    polarity = Polarity.UNFAVOURABLE if outcome.coercive else Polarity.FAVOURABLE
    fact = outcome.consequence if passed else "unmoved by the approach"
    if outcome.grievance:
        fact = f"{fact}; grievance recorded"

    tag = SocialTag(
        id=tag_id or f"social.{frame.id}.{holder}",
        holder=holder,
        target=target,
        fact=fact,
        polarity=polarity,
        source=frame.id,
    )
    return SceneResult(
        scene_id=frame.id,
        scene_type=frame.scene_type,
        passed=passed,
        facts=(f"{holder}: {fact}",),
        tags_added=(tag,),
        notes=(
            f"method {method!r}; consequence {outcome.consequence!r}"
            + ("; coercive" if outcome.coercive else ""),
        ),
    )


# --------------------------------------------------------------------------- #
# Investigation
# --------------------------------------------------------------------------- #

def run_investigation_scene(
    frame: SceneFrame,
    case: Case,
    investigator: Investigator,
    *,
    alternative_method: bool = False,
    access: Iterable[str] = (),
    inquiry: Iterable[str] = (),
    route: str = "observed",
    reliability: str = "witness",
) -> SceneResult:
    """A scene where the point is to find something out.

    Competency buys the clue; there is no roll to fail. What this procedure adds is the record: a
    ``ClueTag`` per clue actually found, carrying the route it came by and its rung on the evidence
    ladder, so "how do you know that?" has an answer later.
    """
    if frame.scene_type != "Investigation":
        raise SceneError("this procedure runs Investigation scenes")
    try:
        discovery = discover(
            case,
            frame.id,
            investigator,
            alternative_method=alternative_method,
            access=access,
            inquiry=inquiry,
        )
    except InvestigationError as exc:
        raise SceneError(str(exc)) from exc

    tags = tuple(
        ClueTag(
            id=f"clue.{frame.id}.{clue.id}",
            clue_id=clue.id,
            holder=investigator.name,
            fact=clue.fact,
            route=route,
            reliability=reliability,
            scene_ref=frame.id,
        )
        for clue in discovery.clues
    )
    facts = tuple(clue.fact for clue in discovery.clues)
    notes = [f"granted by {discovery.granted_by}"]
    if discovery.withheld_ids:
        notes.append("withheld: " + ", ".join(discovery.withheld_ids))
    if not discovery.can_leave:
        notes.append("the scene cannot be left on this investigator's competencies alone")
    return SceneResult(
        scene_id=frame.id,
        scene_type=frame.scene_type,
        passed=discovery.can_leave,
        facts=facts,
        tags_added=tags,
        notes=tuple(notes),
    )


# --------------------------------------------------------------------------- #
# Exploration
# --------------------------------------------------------------------------- #

def run_exploration_scene(
    frame: SceneFrame,
    graph: PhysicalGraph,
    actor: str,
    moves: Iterable[str] = (),
    *,
    discoveries: Mapping[str, str] | None = None,
) -> SceneResult:
    """A scene about going somewhere and seeing what is there.

    Movement is the graph's, not a new subsystem: every move is checked with ``can_move`` and applied
    with ``move``, so a locked door or a missing route fails here exactly as it fails everywhere else.
    """
    if frame.scene_type != "Exploration":
        raise SceneError("this procedure runs Exploration scenes")
    _text(actor, "actor")
    found = dict(discoveries or {})
    visited: list[str] = []
    facts: list[str] = []
    try:
        for destination in moves:
            if not graph.can_move(actor, destination):
                return SceneResult(
                    scene_id=frame.id,
                    scene_type=frame.scene_type,
                    passed=False,
                    facts=tuple(facts),
                    notes=(f"route to {destination!r} is not passable from here",),
                )
            graph.move(actor, destination)
            visited.append(destination)
            if destination in found:
                facts.append(found[destination])
    except GraphError as exc:
        raise SceneError(str(exc)) from exc

    return SceneResult(
        scene_id=frame.id,
        scene_type=frame.scene_type,
        passed=True,
        facts=tuple(facts),
        notes=(("visited: " + ", ".join(visited)) if visited else "no moves made",),
    )


# --------------------------------------------------------------------------- #
# Cyber
# --------------------------------------------------------------------------- #

def run_cyber_scene(
    frame: SceneFrame,
    graph: CyberGraph,
    avatar: str,
    device: str,
    *,
    intelligence_score: int,
    program_skill: int | None,
    difficulty: int,
    wireless: bool = False,
    vr_crown: bool = False,
    verb_modifier: int = 0,
    situational: int = 0,
    dice: tuple[int, int] | None = None,
    clock: AlertClock | None = None,
) -> SceneResult:
    """A hacking scene.

    CWN's hacking check resolves the action; the network's alert clock keeps the cost of failure.
    This procedure adds nothing numeric. Note what it does *not* do: a successful run program does
    not hand over the files — the data still has to be collected, which is the next scene.
    """
    if frame.scene_type != "Cyber":
        raise SceneError("this procedure runs Cyber scenes")
    _text(device, "device")
    if device not in graph.nodes:
        raise SceneError(f"device {device!r} is not on the cyber graph")
    try:
        check = hacking_check(
            intelligence_score=intelligence_score,
            program_skill=program_skill,
            difficulty=difficulty,
            wireless=wireless,
            vr_crown=vr_crown,
            verb_modifier=verb_modifier,
            situational=situational,
            dice=dice,
        )
    except HackError as exc:
        raise SceneError(str(exc)) from exc

    alert = clock if clock is not None else AlertClock()
    if not check.success:
        alert.record_failure()
    return SceneResult(
        scene_id=frame.id,
        scene_type=frame.scene_type,
        passed=check.success,
        facts=(f"run program against {device}: {'success' if check.success else 'failure'}",),
        notes=(
            f"total {check.total} against difficulty {difficulty}",
            f"alert failures {alert.failures}, alert actions {alert.alert_actions}",
            "network alerted" if alert.alerted else "network not yet alerted",
        ),
    )


# --------------------------------------------------------------------------- #
# Action
# --------------------------------------------------------------------------- #

#: The four phases an Action scene passes through. They are phases of a police problem, not a
#: tactical round structure: most scenes end in ``contact`` or ``aftermath`` without force at all.
ACTION_PHASES: tuple[str, ...] = ("approach", "contact", "force", "aftermath")

ACTION_VERBS: Mapping[str, tuple[str, ...]] = {
    "approach": ("close", "observe", "call_backup", "make_contact", "withdraw"),
    "contact": ("order", "negotiate", "contain", "pursue", "escalate", "arrest",
                "withdraw"),
    "force": ("restrain", "brawl", "draw_firearm", "fire", "arrest", "break_off"),
    "aftermath": ("arrest", "first_aid", "report", "release"),
}


@dataclass
class ActionScene:
    """An arrest, a pursuit, a door, a standoff — the scene the old rules called Combat.

    This is a **phase machine**, because the thing that makes a Finnish police action scene different
    is that most of it is talking, waiting and walking, and force is the short exception. It enforces
    three things no amount of prose does:

    * **force needs a recorded reason.** ``escalate`` refuses without one.
    * **a firearm needs recorded grounds.** ``draw_firearm`` refuses without them — the Europol
      burden-of-proof rule from ``docs/rules/PSI_ACCESS_1178.md`` §5, applied to the ordinary case.
    * **an arrest needs a lawful basis and the suspect in hand.** ``arrest`` refuses otherwise.

    The violence itself is CWN's: ``rules.physical_combat`` owns margins, wounds and armour, and this
    class never rolls for them.
    """

    frame: SceneFrame
    graph: PhysicalGraph
    actor: str
    target: str = ""
    phase: str = "approach"
    force_reason: str = ""
    force_grounds: str = ""
    firearm_drawn: bool = False
    log: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.frame.scene_type != "Action":
            raise SceneError("this procedure runs Action scenes")
        _text(self.actor, "actor")
        if self.phase not in ACTION_PHASES:
            raise SceneError(f"unknown action phase {self.phase!r}")

    # -- reading -----------------------------------------------------------------------------
    def allowed_verbs(self) -> tuple[str, ...]:
        verbs = list(ACTION_VERBS[self.phase])
        if self.phase == "force" and not self.firearm_drawn:
            verbs.remove("fire")
        return tuple(verbs)

    def can(self, verb: str) -> bool:
        return verb in self.allowed_verbs()

    # -- acting ------------------------------------------------------------------------------
    def apply(self, verb: str, **kwargs: Any) -> str:
        """Apply one verb and return a one-line fact for the table log."""
        if not self.can(verb):
            raise SceneError(f"{verb!r} is not legal in phase {self.phase!r}")

        if verb == "close":
            destination = _text(kwargs.get("destination", ""), "destination")
            if not self.graph.can_move(self.actor, destination):
                raise SceneError(f"no passable route to {destination!r}")
            self.graph.move(self.actor, destination)
            note = f"moved to {destination}"
        elif verb == "pursue":
            note = self._pursue()
        elif verb == "escalate":
            reason = _text(kwargs.get("reason", ""), "reason")
            self.force_reason = reason
            self.phase = "force"
            note = f"force authorised: {reason}"
        elif verb == "draw_firearm":
            grounds = _text(kwargs.get("grounds", ""), "grounds")
            self.force_grounds = grounds
            self.firearm_drawn = True
            note = f"firearm drawn, grounds recorded: {grounds}"
        elif verb == "fire":
            note = "firearm discharge — resolved by rules.physical_combat; report follows"
        elif verb == "restrain":
            note = "subject restrained — CWN grapple/combat resolves whether it holds"
        elif verb == "brawl":
            note = "brawl — resolved by rules.physical_combat"
        elif verb == "break_off":
            self.phase = "aftermath"
            note = "withdrew from force; scene moves to aftermath"
        elif verb == "arrest":
            note = self._arrest(kwargs)
        elif verb == "contain":
            note = "perimeter held; the subject is confined to this part of the graph"
        elif verb == "order":
            note = "order given — compliance is a social exchange, not an automatic effect"
        elif verb == "negotiate":
            self.phase = "contact" if self.phase == "approach" else self.phase
            note = "negotiation opened — run the social scene for the actual exchange"
        elif verb == "make_contact":
            self.phase = "contact"
            note = "contact made — orders, negotiation, containment or pursuit are now in reach"
        elif verb == "call_backup":
            note = "backup requested"
        elif verb == "observe":
            note = "observed"
        elif verb == "withdraw":
            self.phase = "aftermath"
            note = "withdrew"
        elif verb == "first_aid":
            note = "first aid — CWN healing rules resolve it"
        elif verb == "report":
            note = "reported"
        elif verb == "release":
            note = "released"
        else:  # pragma: no cover - allowed_verbs is the single source of truth
            raise SceneError(f"unhandled verb {verb!r}")

        self.log.append(f"{self.phase}: {note}")
        return note

    # -- internals ---------------------------------------------------------------------------
    def _pursue(self) -> str:
        if not self.target:
            raise SceneError("a pursuit needs a target")
        if self.target not in self.graph.occupants:
            raise SceneError(f"target {self.target!r} is not on the physical graph")
        here = self.graph.occupants.get(self.actor)
        theirs = self.graph.occupants[self.target]
        if here == theirs:
            return "caught up — the subject is in reach"
        route = self._step_towards(here, theirs)
        if route is None:
            raise SceneError("no passable route toward the subject")
        self.graph.move(self.actor, route)
        return f"pursuit step to {route}"

    def _step_towards(self, start: str | None, goal: str) -> str | None:
        """One breadth-first step toward the subject. A pursuit is a path problem, not a chase mini-game."""
        if start is None:
            return None
        seen = {start}
        queue: list[tuple[str, str | None]] = [(start, None)]
        while queue:
            node, first = queue.pop(0)
            if node == goal:
                return first
            for neighbour in self.graph.adjacent(node):
                if neighbour in seen:
                    continue
                seen.add(neighbour)
                queue.append((neighbour, first or neighbour))
        return None

    def _arrest(self, kwargs: Mapping[str, Any]) -> str:
        basis = _text(kwargs.get("lawful_basis", ""), "lawful_basis")
        if not self.target:
            raise SceneError("an arrest needs a subject")
        if not self.graph.co_located(self.actor, self.target):
            raise SceneError("the subject is not in reach; arrest follows containment or pursuit")
        self.phase = "aftermath"
        return f"arrested on the basis of {basis}"
