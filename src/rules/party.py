"""Party roster: one persistent player character plus up to three companions (#806).

The design change behind this module is that the player is **not** Harri Romppainen. The player creates
a level-1 field agent; Romppainen is an experienced NPC who may join a mission. Party size varies from
solo to four, and the code must not assume a size.

Two rules are enforced here rather than left to the UI:

* **The player character is persistent.** Companions come and go; the PC's identity, progression and
  inventory survive every change of composition, so it cannot be swapped out by adding someone.
* **Size is a bound, not a target.** A mission may run solo; nothing in this module requires a party of
  four, and joining a fourth when the roster is full is refused rather than silently dropping someone.

Companion behaviour (AI versus direct control) is deliberately *not* decided here: it is a design
question for the scenario, and the roster only records who is present and whether they are the PC.
"""
from __future__ import annotations

from dataclasses import dataclass, field

MIN_PARTY_SIZE = 1
MAX_PARTY_SIZE = 4


class PartyError(ValueError):
    """A composition change the design forbids."""


@dataclass(frozen=True)
class PartyMember:
    """One character in the active party."""

    member_id: str
    name: str
    level: int
    #: True for the single player-created field agent.
    is_player_character: bool = False
    #: Free-form role tag: "field agent", "mentor", "specialist", ...
    role: str = ""
    #: Scenario-driven availability; a companion may be present without being controllable.
    controllable: bool = True


@dataclass
class Party:
    """The active roster. Exactly one player character, one to four members."""

    members: list[PartyMember] = field(default_factory=list)

    # -- construction ---------------------------------------------------------------------------
    def add_player_character(self, member: PartyMember) -> None:
        if not member.is_player_character:
            raise PartyError("add_player_character needs a member flagged as the player character")
        if any(existing.is_player_character for existing in self.members):
            raise PartyError("a party has exactly one player character")
        if len(self.members) >= MAX_PARTY_SIZE:
            raise PartyError(f"party is full ({MAX_PARTY_SIZE})")
        self.members.append(member)

    def add_companion(self, member: PartyMember) -> None:
        """Add a recruited ally or temporary quest companion."""
        if member.is_player_character:
            raise PartyError("use add_player_character for the player character")
        if any(existing.member_id == member.member_id for existing in self.members):
            raise PartyError(f"{member.member_id} is already in the party")
        if len(self.members) >= MAX_PARTY_SIZE:
            raise PartyError(
                f"party is full ({MAX_PARTY_SIZE}); remove someone before adding {member.member_id}"
            )
        self.members.append(member)

    def remove(self, member_id: str) -> PartyMember:
        """Remove a companion. The player character cannot be removed mid-campaign."""
        member = self.get(member_id)
        if member.is_player_character:
            raise PartyError("the player character is persistent and cannot leave the party")
        self.members.remove(member)
        return member

    # -- queries --------------------------------------------------------------------------------
    def get(self, member_id: str) -> PartyMember:
        for member in self.members:
            if member.member_id == member_id:
                return member
        raise PartyError(f"no such party member: {member_id}")

    @property
    def player_character(self) -> PartyMember | None:
        for member in self.members:
            if member.is_player_character:
                return member
        return None

    @property
    def size(self) -> int:
        return len(self.members)

    @property
    def companions(self) -> list[PartyMember]:
        return [member for member in self.members if not member.is_player_character]

    def controllable(self) -> list[PartyMember]:
        """Who the player may act as right now.

        A companion can be present and present in the fiction without being controllable; the UI asks
        this rather than assuming every member is selectable.
        """
        return [member for member in self.members if member.controllable or member.is_player_character]

    def is_valid(self) -> bool:
        return (
            MIN_PARTY_SIZE <= self.size <= MAX_PARTY_SIZE
            and sum(1 for member in self.members if member.is_player_character) == 1
        )

    def validate(self) -> None:
        """Fail closed on a composition the design does not allow."""
        if self.player_character is None:
            raise PartyError("a party needs exactly one player character")
        if not MIN_PARTY_SIZE <= self.size <= MAX_PARTY_SIZE:
            raise PartyError(f"party size {self.size} outside {MIN_PARTY_SIZE}-{MAX_PARTY_SIZE}")

    # -- persistence ----------------------------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "version": 1,
            "members": [
                {
                    "member_id": member.member_id,
                    "name": member.name,
                    "level": member.level,
                    "is_player_character": member.is_player_character,
                    "role": member.role,
                    "controllable": member.controllable,
                }
                for member in self.members
            ],
        }

    @classmethod
    def from_dict(cls, payload: dict) -> "Party":
        if int(payload.get("version", 0)) != 1:
            raise PartyError(f"unsupported party save version: {payload.get('version')!r}")
        party = cls()
        for row in payload.get("members", []):
            member = PartyMember(
                member_id=str(row["member_id"]),
                name=str(row["name"]),
                level=int(row["level"]),
                is_player_character=bool(row.get("is_player_character", False)),
                role=str(row.get("role", "")),
                controllable=bool(row.get("controllable", True)),
            )
            party.members.append(member)
        party.validate()
        return party
