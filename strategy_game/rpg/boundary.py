"""The RPG layer's adapter boundary to the faction strategy and political simulation.

Issue #389's criterion: *"Provide a clean future adapter boundary to separate faction
strategy/simulation, without inventing that layer's mechanics."*

So this module does exactly two things:

* it fills the reserved ``strategy_game.ports.LeaderRPG`` seam with
  :meth:`LeaderRpgLayer.describe`, the same way the text renderer fills ``MapProvider`` — the port
  already existed, and filling it is an adapter decision, not a rule decision;
* it exposes character sheets and deterministic check resolution to a future strategy layer, while
  declaring **in code** what this layer is not (see :data:`NOT_THIS_LAYER`).

Nothing here reads or writes :class:`strategy_game.core.WorldState`: ``describe`` accepts the state
because the port's signature requires it, and deliberately joins nothing to it. No turn cadence, no
faction action, no economy, no victory condition and no political transition is defined — those are
Gate A/B/C work and stay unapproved.
"""
from __future__ import annotations

from random import Random
from typing import Any, Mapping, Sequence

from ..core import WorldState
from .fate import Action, Character, Resolution, skill_check

#: Version of this boundary's payload shape.
BOUNDARY_SCHEMA_VERSION = "rpg-boundary-1"

#: What this layer is not. Declared so a test can assert the separation instead of trusting prose.
NOT_THIS_LAYER: tuple[str, ...] = (
    "turn cadence",
    "faction action",
    "resource economy",
    "victory condition",
    "political transition",
    "discourse or network simulation",
)

#: Keys the boundary payload may expose. Nothing strategic: no score, no resource, no turn.
PAYLOAD_KEYS: tuple[str, ...] = (
    "schema_version",
    "characters",
    "excluded",
    "note",
)

SHEET_KEYS: tuple[str, ...] = (
    "id",
    "name",
    "aspects",
    "tags",
    "skills",
    "stunts",
    "gear",
    "fate_points",
    "stress",
    "consequences",
    "body",
    "cortical_stack",
    "resleeved",
    "natural_psi",
    "psi_abilities",
    "statuses",
)


class BoundaryError(ValueError):
    """Raised for an invalid boundary operation."""


class LeaderRpgLayer:
    """The RPG layer as a *future* strategy layer may see it: sheets and checks, never factions.

    Characters are held here; no faction, faction action or strategic resource appears, because
    those belong to a layer that is not approved yet.
    """

    def __init__(self, characters: Sequence[Character] | None = None) -> None:
        self.characters: dict[str, Character] = {}
        for character in characters or ():
            if not isinstance(character, Character):
                raise BoundaryError("the layer holds Character records only")
            if character.id in self.characters:
                raise BoundaryError(f"duplicate character id {character.id!r}")
            self.characters[character.id] = character

    # -- what a strategy layer may ask for ---------------------------------
    def sheet(self, character_id: str) -> dict[str, Any]:
        """One character as plain data. Display only: nothing here is a modifier or a score."""
        try:
            character = self.characters[character_id]
        except KeyError as exc:
            raise BoundaryError(f"no character {character_id!r} in this layer") from exc
        return {
            "id": character.id,
            "name": character.name,
            "aspects": list(character.aspects),
            "tags": [tag.to_dict() for tag in character.tags],
            "skills": dict(character.skills),
            "stunts": list(character.stunts),
            "gear": list(character.gear),
            "fate_points": character.fate_points,
            "stress": {
                "physical": list(character.physical_stress),
                "mental": list(character.mental_stress),
            },
            "consequences": [
                {"name": c.name, "severity": c.severity, "recovered": c.recovered}
                for c in character.consequences
            ],
            "body": character.body,
            "cortical_stack": character.cortical_stack,
            "resleeved": character.resleeved,
            "natural_psi": character.natural_psi,
            "psi_abilities": list(character.psi_abilities),
            "statuses": list(character.statuses),
        }

    def resolve(
        self,
        character_id: str,
        action: Action,
        skill_name: str,
        difficulty: int,
        *,
        seed: int,
        invoked_aspect: str | None = None,
    ) -> Resolution:
        """A deterministic character-scale check. The same engine handles cyber, PSI and dialogue.

        A seed is required rather than optional: a strategy layer replaying a turn must be able to
        reproduce the roll from the record, which is why the result carries its dice.
        """
        if character_id not in self.characters:
            raise BoundaryError(f"no character {character_id!r} in this layer")
        return skill_check(
            self.characters[character_id], action, skill_name, difficulty,
            rng=Random(seed), invoked_aspect=invoked_aspect,
        )

    def describe(self, state: WorldState | None = None) -> dict[str, Any]:
        """The reserved ``LeaderRPG`` port: a projection, with no join to the world state.

        ``state`` is accepted because the port's signature requires it and is **not read**: joining
        the table to ``WorldState`` is the Gate D decision, and this boundary performs none.
        """
        return {
            "schema_version": BOUNDARY_SCHEMA_VERSION,
            "characters": [self.sheet(identifier) for identifier in sorted(self.characters)],
            "excluded": list(NOT_THIS_LAYER),
            "note": (
                "RPG-scale sheets and checks only. Faction strategy, political simulation, turn "
                "cadence and victory are a different, unapproved layer; the world state is "
                "deliberately not joined here."
            ),
        }
