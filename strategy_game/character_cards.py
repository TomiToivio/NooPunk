"""Data-only character cards for the separate NoöPunk strategy game.

No character statistics, dice or combat rules are assumed.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

KINDS = frozenset({"canonical", "archetype", "nhi"})
CATEGORIES = frozenset({"Biologics", "Constructs", "Noetics", "Plasmoids"})
VISIBILITIES = frozenset({"public", "discovered", "gm"})
EVIDENCE = frozenset({"observed", "reported", "disputed", "unknown"})


@dataclass
class CharacterCard:
    id: str
    kind: str
    name: str
    summary: str
    tags: list[str] = field(default_factory=list)
    factions: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)
    category: str | None = None
    species: str | None = None
    origin_hypothesis: str | None = None
    evidence_status: str = "unknown"
    visibility: str = "public"
    portrait: str | None = None
    lore: str = ""
    abilities: list[str] = field(default_factory=list)
    relationships: list[str] = field(default_factory=list)
    state: dict[str, Any] = field(default_factory=dict)
    secrets: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "CharacterCard":
        valid = set(cls.__dataclass_fields__)
        extra = set(data) - valid
        if extra:
            raise ValueError(f"unknown character card keys: {sorted(extra)}")
        card = cls(**data)
        card.validate()
        return card

    def validate(self) -> None:
        if not self.id or not self.name.strip():
            raise ValueError("card id and name are required")
        if self.kind not in KINDS:
            raise ValueError(f"unknown card kind: {self.kind}")
        if self.visibility not in VISIBILITIES or self.evidence_status not in EVIDENCE:
            raise ValueError("invalid visibility or evidence status")
        if self.category is not None and self.category not in CATEGORIES:
            raise ValueError("invalid ontological category")
        if self.kind == "nhi" and self.category is None:
            raise ValueError("NHI cards require an ontological category")
        if self.kind != "nhi" and self.category is not None:
            raise ValueError("category is reserved for NHI cards")
        for key in ("tags", "factions", "roles", "abilities", "relationships"):
            values = getattr(self, key)
            if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
                raise ValueError(f"{key} must be a list of strings")
        if not isinstance(self.state, dict) or not isinstance(self.secrets, dict):
            raise ValueError("state and secrets must be objects")

    def visible_to(self, knowledge: str = "public") -> dict[str, Any]:
        """A public card never leaks GM secrets into normal player views."""
        if knowledge not in VISIBILITIES:
            raise ValueError("invalid knowledge level")
        access = {"public": 0, "discovered": 1, "gm": 2}
        if access[knowledge] < access[self.visibility]:
            return {"id": self.id, "hidden": True}
        return {
            "id": self.id, "kind": self.kind, "name": self.name,
            "summary": self.summary, "tags": list(self.tags),
            "factions": list(self.factions), "roles": list(self.roles),
            "category": self.category, "species": self.species,
            "origin_hypothesis": self.origin_hypothesis,
            "evidence_status": self.evidence_status,
            "portrait": self.portrait, "lore": self.lore,
            "abilities": list(self.abilities),
            "relationships": list(self.relationships),
            "state": dict(self.state),
            **({"secrets": dict(self.secrets)} if knowledge == "gm" else {}),
        }


def load_cards(data: list[dict[str, Any]]) -> dict[str, CharacterCard]:
    result: dict[str, CharacterCard] = {}
    for row in data:
        card = CharacterCard.from_dict(row)
        if card.id in result:
            raise ValueError(f"duplicate character id: {card.id}")
        result[card.id] = card
    return result


def instantiate(template: CharacterCard, instance_id: str, name: str | None = None) -> CharacterCard:
    """Spawn a mutable instance, never duplicate a unique canonical character."""
    if template.kind == "canonical":
        raise ValueError("canonical characters must not be cloned")
    if not instance_id or instance_id == template.id:
        raise ValueError("instance requires a new id")
    from dataclasses import replace
    return replace(template, id=instance_id, name=name or template.name,
                   tags=list(template.tags), factions=list(template.factions),
                   roles=list(template.roles), abilities=list(template.abilities),
                   relationships=list(template.relationships),
                   state=dict(template.state), secrets=dict(template.secrets))
