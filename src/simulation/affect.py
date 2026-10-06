"""Unified NoöPunk Affect graph for issue #107."""
from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any

MIN_AFFECT = -10
MAX_AFFECT = 10
VALID_DOMAINS = frozenset({"faction_us","faction_frontier","motivation","reputation","contact"})

@dataclass(frozen=True, slots=True)
class AffectEdge:
    source: str
    source_type: str
    target: str
    target_type: str
    affect: str
    affect_score: int
    domain: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source or not self.target:
            raise ValueError("Affect edges require source and target")
        if not self.affect:
            raise ValueError("Affect edges require a semantic label")
        if not MIN_AFFECT <= self.affect_score <= MAX_AFFECT:
            raise ValueError("affect_score must be between -10 and +10")
        if self.domain not in VALID_DOMAINS:
            raise ValueError(f"Unknown Affect domain: {self.domain!r}")

    @property
    def key(self) -> tuple[str,str,str,str]:
        return (self.source,self.target,self.affect,self.domain)

    def to_dict(self) -> dict[str,Any]:
        return {"source":self.source,"source_type":self.source_type,"target":self.target,
                "target_type":self.target_type,"affect":self.affect,
                "affect_score":self.affect_score,"domain":self.domain,
                "metadata":dict(self.metadata)}

    @classmethod
    def from_dict(cls,data: Mapping[str,Any]) -> AffectEdge:
        return cls(source=str(data["source"]),source_type=str(data["source_type"]),
                   target=str(data["target"]),target_type=str(data["target_type"]),
                   affect=str(data["affect"]),affect_score=int(data["affect_score"]),
                   domain=str(data["domain"]),metadata=dict(data.get("metadata",{})))

@dataclass(slots=True)
class AffectGraph:
    edges: list[AffectEdge] = field(default_factory=list)

    def add(self, edge: AffectEdge, *, replace_exact: bool=True) -> None:
        if replace_exact:
            self.edges=[e for e in self.edges if e.key != edge.key]
        self.edges.append(edge)

    def remove(self, *, source:str, target:str, affect:str|None=None, domain:str|None=None) -> int:
        before=len(self.edges)
        self.edges=[e for e in self.edges if not (
            e.source==source and e.target==target and
            (affect is None or e.affect==affect) and
            (domain is None or e.domain==domain))]
        return before-len(self.edges)

    def between(self, source:str, target:str, *, domain:str|None=None) -> list[AffectEdge]:
        return [e for e in self.edges if e.source==source and e.target==target
                and (domain is None or e.domain==domain)]

    def effective_score(self, source:str, target:str, affect:str, *,
                        domain:str|None=None, fallback:int=0) -> int:
        matches=[e for e in self.between(source,target,domain=domain) if e.affect==affect]
        return matches[-1].affect_score if matches else fallback

    def to_dict(self) -> dict[str,Any]:
        return {"edges":[e.to_dict() for e in self.edges]}

    @classmethod
    def from_dict(cls,data: Mapping[str,Any]) -> AffectGraph:
        return cls([AffectEdge.from_dict(x) for x in data.get("edges",[])])

def inherit_faction_affects(*, character_id:str, faction_edges:Iterable[AffectEdge],
                            personal_edges:Iterable[AffectEdge]=()) -> list[AffectEdge]:
    """Starting condition: preserve distinct labels; mean matching labels; personal overrides."""
    buckets: dict[tuple[str,str,str],list[AffectEdge]]={}
    for edge in faction_edges:
        if edge.domain not in {"faction_us","faction_frontier"}:
            continue
        buckets.setdefault((edge.target,edge.target_type,edge.affect),[]).append(edge)
    inherited: dict[tuple[str,str,str],AffectEdge]={}
    for key,group in buckets.items():
        target,target_type,affect=key
        inherited[key]=AffectEdge(
            source=character_id,source_type="character",target=target,target_type=target_type,
            affect=affect,affect_score=int(sum(e.affect_score for e in group)/len(group)),
            domain="motivation",metadata={"origin":"faction_inheritance",
            "inherited_from":[e.source for e in group]})
    for edge in personal_edges:
        if edge.source != character_id:
            raise ValueError("Personal edge source must match character_id")
        inherited[(edge.target,edge.target_type,edge.affect)]=edge
    return list(inherited.values())
