"""The crossover's five seats and the one-action-per-character turn (#461, #482).

The faction side of the crossover is **one leader and four agents**: five characters on five seats,
each of whom may take **at most one action per turn**. This module holds that structure and its
ledger. It holds nothing else:

* no mission list, no mission effect, no difficulty, no cost, no clock and no resource;
* no numeric world effect, and no statement about which quantity anything moves.

Issue #482 authorises the *structure* and leaves the strategic mission roster and the faction
simulation mechanics to their own approvals. Issue #461's Fork 1 states the same five seats while
noting that the canonical council roster (`council.json::council_size`, `founder_authority`) remains
an open author decision: four leader-slots that generate a four-move cap, and whether the founder is
one of the seats or a fifth authority over them. **This module does not settle either.** It
implements the seat structure the crossover is played with and reports the two cases it does not
decide, so no reader mistakes the roster for a ruling.

Why the seats live here rather than in the strategy layer
-------------------------------------------------------

A seat is *a character*, and the sheet already lives in this package; the strategy layer owns what a
mission is worth, which nothing here states. So this module imports the Fate kernel and the skill
layer, and no strategy engine module at all -- the same boundary ``rpg/boundary.py`` declares.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .fate import Character
from .skills import ActionContext

__all__ = [
    "AGENT_SEAT_COUNT",
    "AgentSeat",
    "RosterError",
    "Seat",
    "SeatKind",
    "TurnLedger",
    "default_seats",
]


#: Issue #461/#482: one leader plus four agents.
AGENT_SEAT_COUNT = 4


class RosterError(ValueError):
    """A roster, seat or turn-ledger operation the structure does not allow."""


class SeatKind(str, Enum):
    """What a seat is for. A leader chairs the faction; an agent carries its missions."""

    LEADER = "leader"
    AGENT = "agent"


@dataclass(frozen=True)
class Seat:
    """One of the five seats, held by one character.

    The seat is structural: it names the kind and the character, and asserts nothing about which
    portfolio, quantity or office the character holds -- those are the strategy layer's vocabulary
    and are awaiting their own approval.
    """

    id: str
    kind: SeatKind
    character_id: str

    @property
    def context(self) -> ActionContext:
        """The skill layer a check from this seat uses.

        Always :attr:`ActionContext.FACTION_AGENT`: a seat acts for the faction, which is exactly what
        distinguishes a strategic mission from the same character's personal scene. The character's
        *individual* checks stay available in scenes and read the six individual skills.
        """
        return ActionContext.FACTION_AGENT


class AgentSeat(Enum):
    """The five seat ids, so a caller never writes a seat name as a bare string."""

    LEADER = "leader"
    AGENT_1 = "agent_1"
    AGENT_2 = "agent_2"
    AGENT_3 = "agent_3"
    AGENT_4 = "agent_4"


def default_seats(leader_id: str, agent_ids: tuple[str, ...]) -> tuple[Seat, ...]:
    """Build the five seats for one faction, refusing a roster that is not one leader and four agents."""
    ids = tuple(str(value).strip() for value in agent_ids)
    if len(ids) != AGENT_SEAT_COUNT:
        raise RosterError(
            f"a faction has exactly {AGENT_SEAT_COUNT} agent seats; got {len(ids)}. Issue #461 states "
            "the one-leader/four-agent structure, so a different count is an author decision."
        )
    if not str(leader_id).strip():
        raise RosterError("a leader seat needs a character id")
    if any(not character_id for character_id in ids):
        raise RosterError("every agent seat needs a non-empty character id")
    if len(set(ids)) != len(ids) or str(leader_id).strip() in ids:
        raise RosterError("a character holds one seat: the leader and the four agents must be distinct")
    seats = [Seat(AgentSeat.LEADER.value, SeatKind.LEADER, str(leader_id).strip())]
    seats += [
        Seat(member.value, SeatKind.AGENT, character_id)
        for member, character_id in zip(
            (AgentSeat.AGENT_1, AgentSeat.AGENT_2, AgentSeat.AGENT_3, AgentSeat.AGENT_4), ids
        )
    ]
    return tuple(seats)


@dataclass
class TurnLedger:
    """Who has acted this turn. At most one action per character per turn.

    The limit is per **character**, not per seat, because that is how issue #482 states it ("up to one
    action per character per turn"); a character holding two seats would still act once. A refused
    declaration does **not** consume the action here -- refusal happens before dice in the strategy
    layer (``council.py::structural_problems``), and whether a refused order costs the turn is that
    layer's open decision, so this ledger records only what it can decide.
    """

    seats: tuple[Seat, ...]
    turn: int = 0
    acted: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.seats:
            raise RosterError("a turn ledger needs the seats it is played on")
        if len({seat.id for seat in self.seats}) != len(self.seats):
            raise RosterError("two seats share an id")

    @property
    def character_ids(self) -> tuple[str, ...]:
        return tuple(seat.character_id for seat in self.seats)

    @property
    def seats_available(self) -> tuple[str, ...]:
        return tuple(seat.id for seat in self.seats if seat.id not in self.acted)

    def seat(self, seat_id: str) -> Seat:
        for seat in self.seats:
            if seat.id == seat_id:
                return seat
        raise RosterError(f"no seat {seat_id!r} in this roster; seats are {[s.id for s in self.seats]}")

    def declare(self, seat_id: str, *, statement: str = "") -> str:
        """Take this turn's action for a seat, or refuse because the character already acted.

        Returns the acting character's id, which is what a record needs; ``statement`` is free text
        that nothing reads, so no amount of prose can move a result.
        """
        seat = self.seat(seat_id)
        already = self.acted.get(seat.id)
        if already is not None:
            raise RosterError(
                f"{seat.id} has already acted this turn ({already}). A character takes at most one "
                "action per turn (#461/#482); the next turn is a new ledger."
            )
        for holder, previous_seat in self.acted.items():
            if self.seat(holder).character_id == seat.character_id:
                raise RosterError(
                    f"{seat.character_id!r} already acted this turn on seat {holder} "
                    f"({previous_seat}): the limit is one action per character, not per seat."
                )
        self.acted[seat.id] = statement or seat.kind.value
        return seat.character_id

    def next_turn(self) -> int:
        """Close the turn and open the next one. The seats and characters are unchanged."""
        self.turn += 1
        self.acted.clear()
        return self.turn

    def characters_without_a_sheet(self, sheets: dict[str, Character]) -> tuple[str, ...]:
        """Character ids on a seat that have no sheet in the supplied mapping.

        Reported rather than refused: a seat may legitimately be held by a character whose sheet is
        not loaded in this process, and inventing one would be inventing a character.
        """
        return tuple(sorted({cid for cid in self.character_ids if cid not in sheets}))
