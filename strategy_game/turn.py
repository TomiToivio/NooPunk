"""The connection between an approved RPG check and the ONE authoritative turn history.

Issue #347's checklist item: *"Connect RPG choice / character check and faction strategic action to
one authoritative state; expose turn outcome/dice provenance."*

What the one authoritative state is
-----------------------------------
The append-only, rule-neutral turn/event history the tabletop layer already keeps:
:class:`strategy_game.tabletop.history.HistoryLog` (issue #397). This module does **not** add a
second log; it is the *connection* to that one:

* an RPG character check is resolved through the **approved** Fate engine
  (:mod:`strategy_game.rpg.fate`, reached through its declared adapter
  :class:`strategy_game.rpg.boundary.LeaderRpgLayer`) and written into the history as a
  ``rule_outcome`` entry carrying its dice and the seed, so the turn outcome and its **dice
  provenance** are both inspectable and replayable;
* a **declaration** -- what a player, a GM or an optional model proposes -- is written as its own
  entry with its own provenance, and has no way to become an outcome.

Nothing an LLM or a narrative layer proposes may mutate authoritative state (``docs/design/VISION.md``
§5). Here that is structural, not promised: the only function that writes a rule outcome is
:func:`record_character_check`, and it calls the engine with a seed. Free text lives on a declaration
entry, is stored verbatim, and is never read. Because a recorded outcome is fully determined by its
dice, skill and difficulty, :func:`verify_outcome` re-derives that arithmetic relation, so an entry
that does not re-derive is *reported* rather than trusted -- the same "store the faces, replay without
the RNG" discipline ``tabletop.dice.RollLog`` uses. (A Fate 4dF face is -1, 0 or +1, so a Fate roll
cannot be a :class:`~strategy_game.tabletop.dice.RollResult`, whose faces are ``1..sides``; the
*pattern* is reused, the container is not, and no die is rolled here at all.)

The strategic-action half is PENDING
------------------------------------
#347's item pairs the RPG check with a *faction strategic action*. Faction strategy is **Gate C** and
the political simulation is **Gate B**, both unapproved
(``strategy_game/docs/RULE_SYSTEM_RESEARCH.md``), so no strategic mechanic is defined here. The
**seam** is fixed -- :class:`StrategicActionPort`, a signature-only protocol, plus
:data:`PENDING_STRATEGIC_ACTION` and :func:`strategic_action`, which refuses with the gate as its
reason. This is a container and a connection, not a rule: no action set, cost, cadence, threshold or
victory condition appears below, and ``difficulty`` / ``skill_name`` are the *check's* inputs,
established by the caller or GM exactly as the Fate rulebook requires -- never thresholds chosen here.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, NoReturn, Protocol

from .provenance import Provenance, ProvenanceKind
from .rpg.boundary import LeaderRpgLayer
from .rpg.fate import Action, Outcome
from .tabletop.history import HistoryEntry, HistoryLog

__all__ = [
    "TURN_SCHEMA_VERSION",
    "ENGINE",
    "DECLARATION_KIND",
    "OUTCOME_KIND",
    "DECLARATION_ORIGINS",
    "DICE_PROVENANCE_KEYS",
    "PENDING_STRATEGIC_ACTION",
    "MECHANICS_OWNER",
    "APPLIED",
    "TurnError",
    "StrategicActionPending",
    "TurnOutcome",
    "StrategicActionPort",
    "declaration_provenance",
    "record_declaration",
    "record_character_check",
    "outcome_entries",
    "turn_outcomes",
    "dice_log",
    "verify_outcome",
    "verify_history",
    "strategic_action",
]

#: Version of the outcome payload this connection writes into the history.
TURN_SCHEMA_VERSION = "turn-1"

#: The engine a rule outcome comes from. Named so provenance is checkable, not merely claimed.
ENGINE = "strategy_game.rpg.fate"

#: The history entry kind a resolved character check is written under.
OUTCOME_KIND = "rule_outcome"
#: The history entry kind a declared-but-unresolved check is written under.
DECLARATION_KIND = "player_declaration"

#: Who may declare a check. Recorded as provenance; never authoritative.
DECLARATION_ORIGINS: tuple[str, ...] = ("player", "gm", "llm")

#: The keys :meth:`TurnOutcome.dice_provenance` exposes. Declared so the payload cannot widen quietly.
DICE_PROVENANCE_KEYS: tuple[str, ...] = (
    "notation", "dice", "total", "shifts", "outcome", "seed", "engine",
    "turn", "character_id", "action", "skill", "difficulty", "provenance",
)

#: Why the faction strategic-action half of #347's item is not implemented. A gate, not a gap.
PENDING_STRATEGIC_ACTION: str = (
    "faction strategic action is unapproved: strategy rules are Gate C and the political simulation "
    "is Gate B (strategy_game/docs/RULE_SYSTEM_RESEARCH.md). Only the approved Fate RPG layer may "
    "write an outcome into the turn history today; no action set, cost, cadence or victory condition "
    "is defined here."
)

#: Who would own a strategic action's mechanics once the gate closes. Named so the seam is not read
#: as approval.
MECHANICS_OWNER: str = "gate-C (unapproved strategy rules)"

#: Whether any strategic mechanic is applied. Always ``False`` while the gate is open.
APPLIED: bool = False


class TurnError(ValueError):
    """Raised for a malformed declaration or an outcome that does not fit its own faces."""


class StrategicActionPending(RuntimeError):
    """Raised when a strategic action is attempted before its rules are approved."""


def declaration_provenance(origin: str) -> Provenance:
    """The provenance a declaration of this origin carries.

    A player's or a GM's declaration is authored; an optional model's is generated. The kinds come
    from :mod:`strategy_game.provenance`, so a proposal is never conflated with a rule outcome.
    """
    if origin not in DECLARATION_ORIGINS:
        raise TurnError(f"declaration origin {origin!r} is not one of {DECLARATION_ORIGINS}")
    kind = ProvenanceKind.GENERATED if origin == "llm" else ProvenanceKind.AUTHORED
    return Provenance(
        kind=kind,
        source=f"declaration:{origin}",
        note="declared intent - not authoritative; only a seeded resolution writes an outcome",
    )


@dataclass(frozen=True)
class TurnOutcome:
    """One resolved RPG character check as it entered the authoritative history.

    Every field comes from the approved engine's
    :class:`~strategy_game.rpg.fate.Resolution`; none is a rule chosen here. ``seed`` is recorded so
    the same check can be re-run and its faces compared. There is deliberately **no prose field**: a
    declaration is recorded separately by :func:`record_declaration`, so a narrative layer has no
    field on the authoritative outcome to write into.
    """

    turn: int
    character_id: str
    action: Action
    skill_name: str
    skill: int
    difficulty: int
    dice: tuple[int, ...]
    total: int
    shifts: int
    outcome: Outcome
    seed: int

    def __post_init__(self) -> None:
        if not str(self.character_id).strip():
            raise TurnError("an outcome names the character it resolved for")
        if len(self.dice) != 4:
            raise TurnError(f"a Fate check is four dice, got {len(self.dice)}")
        for face in self.dice:
            if face not in (-1, 0, 1):
                raise TurnError(f"a Fate die face is -1, 0 or +1, got {face}")

    def provenance(self) -> Provenance:
        """Where the record came from: the approved engine, seeded and replayable."""
        return Provenance(
            kind=ProvenanceKind.SIMULATED,
            source=ENGINE,
            note="committed by the approved Fate resolver from a seed",
        )

    def recompute(self) -> tuple[int, int]:
        """Re-derive ``(total, shifts)`` from the stored faces -- no RNG, no engine re-run.

        A recorded check makes no aspect invocation, so ``total = sum(dice) + skill``. Storing the
        faces is what lets the record be audited without reproducing the random stream.
        """
        total = sum(self.dice) + self.skill
        return total, total - self.difficulty

    def is_consistent(self) -> bool:
        """True when the stored totals re-derive from the stored faces."""
        return self.recompute() == (self.total, self.shifts)

    def dice_provenance(self) -> dict[str, Any]:
        """The turn outcome and its dice, exposed for the visible dice log #347 asks the UI to show."""
        return {
            "notation": "4dF",
            "dice": list(self.dice),
            "total": self.total,
            "shifts": self.shifts,
            "outcome": self.outcome.value,
            "seed": self.seed,
            "engine": ENGINE,
            "turn": self.turn,
            "character_id": self.character_id,
            "action": self.action.value,
            "skill": self.skill,
            "difficulty": self.difficulty,
            "provenance": self.provenance().to_dict(),
        }

    def to_dict(self) -> dict[str, Any]:
        """Plain-JSON record. This is what is stored on the history entry."""
        return {
            "schema_version": TURN_SCHEMA_VERSION,
            "turn": self.turn,
            "character_id": self.character_id,
            "action": self.action.value,
            "skill_name": self.skill_name,
            "skill": self.skill,
            "difficulty": self.difficulty,
            "dice": list(self.dice),
            "total": self.total,
            "shifts": self.shifts,
            "outcome": self.outcome.value,
            "seed": self.seed,
            "engine": ENGINE,
            "provenance": self.provenance().to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TurnOutcome":
        """Rebuild a record from :meth:`to_dict` output. Raises :class:`TurnError` if it does not fit."""
        if not isinstance(data, Mapping):
            raise TurnError(f"an outcome record must be a mapping, got {type(data).__name__}")
        try:
            return cls(
                turn=int(data.get("turn", 0)),
                character_id=str(data["character_id"]),
                action=Action(str(data["action"])),
                skill_name=str(data.get("skill_name", "")),
                skill=int(data.get("skill", 0)),
                difficulty=int(data.get("difficulty", 0)),
                dice=tuple(int(face) for face in (data.get("dice") or ())),
                total=int(data.get("total", 0)),
                shifts=int(data.get("shifts", 0)),
                outcome=Outcome(str(data["outcome"])),
                seed=int(data.get("seed", 0)),
            )
        except (KeyError, TypeError) as exc:
            raise TurnError(f"an outcome record is missing a field: {exc}") from exc


def record_declaration(
    history: HistoryLog,
    *,
    character_id: str,
    action: Action,
    skill_name: str,
    difficulty: int,
    turn: int = 0,
    statement: str = "",
    origin: str = "player",
) -> HistoryEntry:
    """Record *what someone declares*, separately from what resolves.

    ``statement`` is free text and is written verbatim; it is never read by anything in this module,
    so no amount of prose can move a result. The entry carries the declaration's provenance and
    writes **no** outcome.
    """
    if not str(character_id).strip():
        raise TurnError("a declaration names the character it is for")
    provenance = declaration_provenance(origin)
    return history.append(
        DECLARATION_KIND,
        f"{character_id} declares {action.value} {skill_name} ({origin})",
        actor_id=character_id,
        provenance=provenance.kind.value,
        details={
            "turn": turn,
            "character_id": character_id,
            "action": action.value,
            "skill_name": skill_name,
            "difficulty": difficulty,
            "statement": statement,
            "origin": origin,
            "provenance": provenance.to_dict(),
        },
    )


def record_character_check(
    layer: LeaderRpgLayer,
    history: HistoryLog,
    *,
    character_id: str,
    action: Action,
    skill_name: str,
    difficulty: int,
    seed: int,
    turn: int = 0,
) -> TurnOutcome:
    """Resolve one character check through the approved engine and write it into the history.

    This is the connection #347 asks for, and the **only** function here that produces a rule
    outcome: it calls :meth:`strategy_game.rpg.boundary.LeaderRpgLayer.resolve` with a seed and stores
    the engine's own dice, total, shifts and outcome. Free text is not an input at all -- the result
    depends on ``character_id``, ``action``, ``skill_name``, ``difficulty`` and ``seed`` alone, so no
    prose can move it. Record a proposal separately with :func:`record_declaration`.
    """
    resolution = layer.resolve(character_id, action, skill_name, difficulty, seed=seed)
    outcome = TurnOutcome(
        turn=turn,
        character_id=character_id,
        action=resolution.action,
        skill_name=skill_name,
        skill=resolution.skill,
        difficulty=resolution.difficulty,
        dice=tuple(resolution.dice),
        total=resolution.total,
        shifts=resolution.shifts,
        outcome=resolution.outcome,
        seed=seed,
    )
    history.append(
        OUTCOME_KIND,
        f"{character_id} {resolution.action.value} {skill_name} -> {resolution.outcome.value} "
        f"({len(resolution.dice)}dF, seed {seed})",
        actor_id=character_id,
        provenance=outcome.provenance().kind.value,
        details=outcome.to_dict(),
    )
    return outcome


def outcome_entries(history: HistoryLog) -> tuple[HistoryEntry, ...]:
    """Every ``rule_outcome`` entry in the history, in order."""
    return tuple(entry for entry in history.entries if entry.kind == OUTCOME_KIND)


def turn_outcomes(history: HistoryLog) -> tuple[TurnOutcome, ...]:
    """The turn outcomes recorded in the history, rebuilt from their own faces.

    Raises :class:`TurnError` for a ``rule_outcome`` entry that does not fit an outcome record, so a
    malformed entry is loud rather than silently skipped.
    """
    return tuple(TurnOutcome.from_dict(entry.details) for entry in outcome_entries(history))


def dice_log(history: HistoryLog) -> tuple[dict[str, Any], ...]:
    """Per-outcome dice provenance, for the visible dice log."""
    return tuple(outcome.dice_provenance() for outcome in turn_outcomes(history))


def verify_outcome(entry: HistoryEntry) -> tuple[str, ...]:
    """Readable problems with one outcome entry. Empty means it re-derives and carries engine provenance."""
    if entry.kind != OUTCOME_KIND:
        return (f"entry {entry.sequence} is a {entry.kind!r}, not a {OUTCOME_KIND!r}",)
    problems: list[str] = []
    if entry.provenance != ProvenanceKind.SIMULATED.value:
        problems.append(
            f"entry {entry.sequence}: an outcome must carry the engine's "
            f"{ProvenanceKind.SIMULATED.value!r} provenance, got {entry.provenance!r}"
        )
    try:
        outcome = TurnOutcome.from_dict(entry.details)
    except TurnError as exc:
        return (f"entry {entry.sequence} does not fit an outcome record: {exc}",)
    if not outcome.is_consistent():
        problems.append(
            f"entry {entry.sequence}: dice {list(outcome.dice)} + skill {outcome.skill} do not "
            f"re-derive total {outcome.total} / shifts {outcome.shifts}"
        )
    return tuple(problems)


def verify_history(history: HistoryLog) -> tuple[str, ...]:
    """Readable problems with every outcome entry in the history. Empty means the log re-derives."""
    return tuple(problem for entry in outcome_entries(history) for problem in verify_outcome(entry))


class StrategicActionPort(Protocol):
    """Signature only: the strategy layer's future route into the one authoritative turn history.

    An implementation would take a declared strategic action and return the outcome record it wrote --
    once the strategy rules exist. Fixing the signature now fixes *where* the mechanic will attach; it
    defines no mechanic, and its absence is not a broken game: the RPG half stands alone, exactly as
    :mod:`strategy_game.rpg.ports` argues for its own seam. Nothing here registers or loads one.
    """

    def strategic_outcome(self, request: object) -> object: ...


def strategic_action(*_args: Any, **_kwargs: Any) -> NoReturn:
    """The declared-but-unapproved half of #347's item. Refuses, with the gate as its reason.

    There is deliberately no implementation: an action set, a cost or a cadence defined here would be
    the strategy mechanic Gates B and C have not approved. :class:`StrategicActionPort` fixes where
    the mechanic will attach; this function is the guard that keeps it out until then.
    """
    raise StrategicActionPending(PENDING_STRATEGIC_ACTION)
