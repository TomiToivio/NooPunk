"""CWN hacking beyond the catalogue: access, CPU, node links and program runs (#1068).

The catalogue (`data/rules/cwn/hacking_catalogue.json`) holds the Verbs and Subjects. This module holds
the procedure around them, from the Cities Without Number SRD (public domain), Hacking chapter:

* Access = Intelligence modifier + Program skill + the deck's bonus Access.
* A deck runs at most `cpu` programs; each running program occupies one slot until it self-terminates or
  is terminated.
* Getting from one node to another is a hop across a link. A guarded link needs the barrier defeated
  before the hop, which is what makes a network a map rather than a menu.
* Connecting wirelessly costs -2 on every cyberspace check; a VR crown instead of a cranial jack costs
  another -1.
* Every two failed checks against a network's Security count as one Alert the Network action.

Deterministic: dice are passed in, never rolled here.
"""
from __future__ import annotations

from dataclasses import dataclass, field

WIRELESS_PENALTY = -2
VR_CROWN_PENALTY = -1
FAILURES_PER_ALERT = 2


class HackingError(ValueError):
    """A state the rules do not allow: no CPU, no memory, unknown node, unaffordable Verb."""


@dataclass(frozen=True)
class Cyberdeck:
    """A deck's four stats. `cpu` and `memory` are slots; `shielding` absorbs Stun/Kill damage."""

    name: str
    bonus_access: int = 0
    memory: int = 0
    cpu: int = 0
    shielding: int = 0
    encumbrance: int = 1


@dataclass
class Cyberspace:
    """One network: its nodes, its links, and what the hacker has done to it."""

    security: int
    #: node -> neighbouring nodes. A link is the pair, so both directions must be listed.
    links: dict[str, set[str]] = field(default_factory=dict)
    #: frozenset({a, b}) -> barrier difficulty, when the link is guarded by a program subject.
    barriers: dict[frozenset[str], int] = field(default_factory=dict)
    failures: int = 0
    alerts: int = 0

    def add_node(self, name: str, *, neighbours: set[str] | None = None) -> None:
        self.links.setdefault(name, set())
        for other in neighbours or set():
            self.links[name].add(other)
            self.links.setdefault(other, set()).add(name)

    def neighbours(self, node: str) -> set[str]:
        if node not in self.links:
            raise HackingError(f"unknown node {node!r}")
        return set(self.links[node])

    def barrier(self, a: str, b: str) -> int | None:
        return self.barriers.get(frozenset({a, b}))

    def record_failure(self) -> int:
        """Count a failed check; return how many alerts that produced (0 or 1)."""
        self.failures += 1
        if self.failures % FAILURES_PER_ALERT == 0:
            self.alerts += 1
            return 1
        return 0


def access_score(intelligence_modifier: int, program_rank: int, deck: Cyberdeck) -> int:
    """The deck's total Access pool for one jack-in."""
    return intelligence_modifier + program_rank + deck.bonus_access


def connection_penalty(*, wireless: bool = False, vr_crown: bool = False) -> int:
    """Everything that makes a cyberspace check harder before the target's Security is even counted."""
    penalty = WIRELESS_PENALTY if wireless else 0
    if vr_crown:
        penalty += VR_CROWN_PENALTY
    return penalty


@dataclass(frozen=True)
class Program:
    verb: str
    subject: str
    cpu: int = 1
    access_cost: int = 1
    persistent: bool = False
    difficulty_modifier: int = 0


def run_program(
    *,
    program: Program,
    deck: Cyberdeck,
    running: int,
    access_available: int,
    security: int,
    total: int,
    network: Cyberspace | None = None,
) -> dict[str, object]:
    """Resolve one program run.

    `total` is the already-rolled Int/Program check (dice + skill + modifier + penalties), so the
    caller keeps the dice and this function stays deterministic.
    """
    if running >= deck.cpu:
        raise HackingError(f"{deck.name} has no free CPU ({running}/{deck.cpu} in use)")
    if access_available < program.access_cost:
        raise HackingError(
            f"{program.verb}/{program.subject} costs {program.access_cost} Access, {access_available} left"
        )
    difficulty = security + program.difficulty_modifier
    success = total >= difficulty
    result: dict[str, object] = {
        "success": success,
        "total": total,
        "difficulty": difficulty,
        "access_spent": program.access_cost,
        "cpu_held": program.cpu if (success and program.persistent) else 0,
        "alert": 0,
    }
    if not success and network is not None:
        result["alert"] = network.record_failure()
    return result


def move_node(
    network: Cyberspace,
    *,
    from_node: str,
    to_node: str,
    barrier_defeated: bool = False,
) -> dict[str, object]:
    """One hop along a link. A guarded link refuses the hop until its barrier is down."""
    if to_node not in network.neighbours(from_node):
        return {"moved": False, "reason": "no link between the nodes"}
    barrier = network.barrier(from_node, to_node)
    if barrier is not None and not barrier_defeated:
        return {"moved": False, "reason": "barrier", "difficulty": barrier}
    return {"moved": True, "node": to_node}


def can_jack_in(deck: Cyberdeck, *, running: int) -> bool:
    """Jacking in costs no CPU, but a deck with no free slot cannot run anything once there."""
    return running < deck.cpu


def memory_used(programs: list[Program], deck: Cyberdeck) -> int:
    used = len(programs)
    if used > deck.memory:
        raise HackingError(f"{used} utilities exceed {deck.name}'s {deck.memory} Memory")
    return used
