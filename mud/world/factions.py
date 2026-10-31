"""UNSA as the MUD's first playable faction (#946, milestone 4).

The MUD's authority rule says evennia/world state plus CWN mechanics decide what is
possible. So a faction is **inspectable state, not a strategy engine**: membership,
reputation and stocks, all readable with one command, all changed only by a logged
event. A "complex faction strategy game" is explicitly deferred by the issue, and the
cheapest way to keep it deferred is to give the faction no verbs of its own.

Pure Python — no Evennia import — so the state is testable and the same dict can be
persisted in ``db`` or exported to a simulation later.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

#: The stocks a collapse actually costs you first. Names, not mechanics.
STOCK_NAMES: tuple[str, ...] = ("food", "water", "power", "medicine")

#: Reputation is read off the sheet and spoken at the table; it never multiplies a roll.
REPUTATION_MIN = -3
REPUTATION_MAX = 3


@dataclass
class Faction:
    """One organisation's visible state. No member is ever added without a name."""

    name: str
    reputation: int = 0
    members: list[str] = field(default_factory=list)
    roles: dict[str, str] = field(default_factory=dict)
    stocks: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("a faction needs a name")
        self.stocks = {stock: int(self.stocks.get(stock, 0)) for stock in STOCK_NAMES}
        if not REPUTATION_MIN <= self.reputation <= REPUTATION_MAX:
            raise ValueError(f"reputation is {REPUTATION_MIN}..{REPUTATION_MAX}")

    def join(self, character: str, role: str = "analyst") -> bool:
        """Idempotent membership. The first member is not special; the author's is."""
        if not character.strip() or not role.strip():
            return False
        if character in self.members:
            return False
        self.members.append(character)
        self.roles[character] = role
        return True

    def leave(self, character: str) -> bool:
        if character not in self.members:
            return False
        self.members.remove(character)
        self.roles.pop(character, None)
        return True

    def adjust(self, stock: str, amount: int) -> int:
        """Move one stock by ``amount``; stocks never go below zero. Returns the new value."""
        if stock not in self.stocks:
            raise ValueError(f"unknown stock {stock!r}")
        self.stocks[stock] = max(0, self.stocks[stock] + int(amount))
        return self.stocks[stock]

    def reputation_with(self, delta: int) -> int:
        """The only way reputation moves, and it is a consequence somebody narrates."""
        self.reputation = max(REPUTATION_MIN, min(REPUTATION_MAX, self.reputation + int(delta)))
        return self.reputation

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "reputation": self.reputation,
            "members": list(self.members),
            "roles": dict(self.roles),
            "stocks": dict(self.stocks),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Faction":
        return cls(
            name=str(data["name"]),
            reputation=int(data.get("reputation", 0)),
            members=list(data.get("members", [])),
            roles=dict(data.get("roles", {})),
            stocks=dict(data.get("stocks", {})),
        )

    def to_text(self) -> str:
        stocks = ", ".join(f"{name} {value}" for name, value in self.stocks.items())
        people = ", ".join(self.members) or "nobody"
        return (
            f"|w{self.name}|n  reputation {self.reputation:+d}\n"
            f"Members: {people}\nStocks: {stocks}"
        )


def unsa() -> Faction:
    """The starting organisation: a structured institution that is still standing."""
    return Faction(
        name="UNSA",
        reputation=1,
        stocks={"food": 3, "water": 3, "power": 1, "medicine": 1},
    )
