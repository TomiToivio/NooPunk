"""AWN Deluxe Mutant Edge character creation, based on printed pp. 16-25.

Mutation identities/effects must be registered from the owned rulebook, not invented.
NoöPunk's Europol-approved rookie is not assumed to be a Hybrid or a Psychic.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


class MutationError(ValueError):
    pass


@dataclass(frozen=True)
class Mutation:
    name: str
    kind: Literal["positive", "negative"]
    category: str
    source_page: int

    def __post_init__(self) -> None:
        if not self.name.strip() or not 16 <= self.source_page <= 25:
            raise MutationError("mutation needs a printed name and AWN p.16-25 reference")


@dataclass
class MutantBuild:
    actor_id: str
    europol_approved: bool
    stigma: str
    stigma_concealable: bool = False
    origin: str = "unknown"
    alien_hybrid: bool = False
    psychic: bool = False
    mutation_points: int = 2
    negatives: list[str] = field(default_factory=list)
    positives: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.actor_id or not self.europol_approved or not self.stigma:
            raise MutationError("rookie mutant requires actor ID, Europol approval, and an AWN Stigma")
        if self.alien_hybrid:
            raise MutationError("Europol rookie Mutant Edge does not establish Hybrid origin")
        if self.mutation_points != 2:
            raise MutationError("AWN Mutant Edge initially grants 2 Mutation Points (p.16)")
        if self.stigma_concealable:
            self.mutation_points -= 1

    def add_negative(self, mutation: Mutation) -> None:
        """Negative mutations are RANDOM and cannot repeat (AWN p.16)."""
        if mutation.kind != "negative" or mutation.name in self.negatives:
            raise MutationError("negative mutation must be a new published negative result")
        if len(self.negatives) >= 3:
            raise MutationError("no more than three negative mutations")
        self.negatives.append(mutation.name)
        self.mutation_points += 2

    def add_positive(self, mutation: Mutation, *,
                     method: Literal["pick", "random", "two_same_category"],
                     second: Mutation | None = None) -> None:
        """AWN p.16 costs: chosen = 3 MP, random = 1 MP, two same category = 3 MP."""
        costs = {"pick": 3, "random": 1, "two_same_category": 3}
        cost = costs[method]
        if self.mutation_points < cost:
            raise MutationError("insufficient Mutation Points")
        additions = [mutation]
        if method == "two_same_category":
            if second is None or second.category != mutation.category:
                raise MutationError("two category rolls require two mutations from the same category")
            additions.append(second)
        if any(m.kind != "positive" for m in additions):
            raise MutationError("positive purchase requires published positive mutations")
        names = [m.name for m in additions]
        if len(set(names)) != len(names) or any(n in self.positives for n in names):
            raise MutationError("duplicate mutation, reroll according to AWN p.16")
        self.positives.extend(names)
        self.mutation_points -= cost

    def take_mutation_acceleration(self) -> None:
        """AWN p.16: the separately selected Edge provides two further points."""
        self.mutation_points += 2
