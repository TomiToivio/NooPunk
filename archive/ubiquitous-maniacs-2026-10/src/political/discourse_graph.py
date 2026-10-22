"""Pydantic models for LaclauGPT discourse analysis and network society graphs.

This module defines three layers of graph models:
1. Social Network Ontology (basic Nodes and Edges)
2. Network Society Ontology (Castells)
3. Discourse Analysis Ontology (Laclau)

These models complement the unified KnowledgeBaseEntity and RDFTriple models
in knowledge_base.py, providing domain-specific graph extraction schemas for
the LLM postprocessing step.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List


# ---------------------------------------------------------------------------
# Layer 1: Social Network Ontology (basic Nodes and Edges)
# ---------------------------------------------------------------------------

class SocialNode(BaseModel):
    """A basic social network node using spaCy NER types."""
    id: str
    label: Literal[
        "PERSON", "NORP", "FAC", "ORG", "GPE", "LOC", "PRODUCT", "EVENT",
        "WORK_OF_ART", "LAW", "LANGUAGE", "DATE", "TIME", "PERCENT", "MONEY",
        "QUANTITY", "ORDINAL", "CARDINAL", "CONCEPT", "ACTOR", "NODE",
    ]
    name: str
    subtype: Optional[str] = None
    description: Optional[str] = None


class SocialEdge(BaseModel):
    """A basic social network edge."""
    source: str
    target: str
    relation: Literal[
        "supports", "opposes", "mentions",
        "has_negative_sentiment_towards", "has_positive_sentiment_towards",
        "has_neutral_sentiment_towards",
        "member_of", "located_in", "authored_by", "participated_in",
        "owner_of", "regulates", "jurisdiction", "knows", "developed", "edge",
    ]
    description: Optional[str] = None
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: Optional[str] = None


class SocialGraphExtraction(BaseModel):
    """Extraction schema for social network analysis."""
    nodes: List[SocialNode]
    edges: List[SocialEdge]


# ---------------------------------------------------------------------------
# Layer 2: Network Society Ontology (Manuel Castells)
# ---------------------------------------------------------------------------

class CastellsNode(BaseModel):
    """A node in the Network Society ontology based on Castells."""
    id: str
    label: Literal[
        "Network",
        "Node",
        "Hub",
        "SpaceOfFlows",
        "SpaceOfPlaces",
        "ProgrammingPower",
        "SwitchingPower",
        "Counterpower",
        "MassSelfCommunication",
        "IdentityProject",
        "LegitimizingIdentity",
        "ResistanceIdentity",
        "ProjectIdentity",
        "SocialMovement",
        # Also allow spaCy NER types for mixed extraction
        "PERSON", "NORP", "ORG", "GPE", "LOC", "FAC", "PRODUCT", "EVENT",
        "WORK_OF_ART", "LAW", "CONCEPT",
    ]
    name: str
    description: Optional[str] = None
    world_systems_position: Optional[Literal["core", "semiperiphery", "periphery"]] = None


class CastellsEdge(BaseModel):
    """An edge in the Network Society ontology based on Castells."""
    source: str
    target: str
    relation: Literal[
        "connects",          # Node is connected to a network
        "switches",          # Hub switches between networks
        "programs",          # Actor/Org sets the rules/protocols
        "dominates",         # SpaceOfFlows dominates SpaceOfPlaces
        "resists",           # Counterpower resists dominant network
        "organizes",         # MassSelfCommunication organizes movements
        "constructs",        # Identity project constructs a movement
        "excludes",          # Network excludes certain identities
        "flows_through",     # Resource flows through a network
        # Also allow social network relations
        "supports", "opposes", "mentions", "located_in", "owner_of", "developed",
    ]
    description: Optional[str] = None
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: Optional[str] = None


class CastellsGraphExtraction(BaseModel):
    """Extraction schema for Network Society analysis (Castells)."""
    nodes: List[CastellsNode]
    edges: List[CastellsEdge]


# ---------------------------------------------------------------------------
# Layer 3: Discourse Analysis Ontology (Ernesto Laclau)
# ---------------------------------------------------------------------------

class LaclauNode(BaseModel):
    """A node in the Discourse Analysis ontology based on Laclau."""
    id: str
    label: Literal[
        "Signifier",
        "NodalPoint",
        "Demand",
        "Identity",
        "ChainOfEquivalence",
        "ChainOfDifference",
        "Antagonism",
        "Hegemony",
        "Dislocation",
        "Articulation",
        "Imaginary",
        # Also allow spaCy NER types for mixed extraction
        "PERSON", "NORP", "ORG", "GPE", "CONCEPT", "EVENT",
    ]
    name: str
    subtype: Optional[str] = None
    description: Optional[str] = None
    is_empty_signifier: Optional[bool] = None
    ideological_stance: Optional[Literal[
        "acceleration", "deceleration",
        "liberal", "authoritarian",
        "left", "right", "center",
    ]] = None


class LaclauEdge(BaseModel):
    """An edge in the Discourse Analysis ontology based on Laclau."""
    source: str
    target: str
    relation: Literal[
        "AUTHORED",
        "PROMOTES",
        "USES_SIGNIFIER",
        "EXPRESSES_DEMAND",
        "CONSTRUCTS_IDENTITY",
        "CONSTRUCTS_AS_ENEMY",
        "HAS_NODAL_POINT",
        "PART_OF_CHAIN",
        "UNIFIED_BY",
        "OPPOSES",
        "ARTICULATED_WITH",
        "CONTESTED_BY",
        "HEGEMONIZES",
        "DISLOCATED_BY",
        "RESPONDS_TO",
    ]
    logic: Optional[Literal[
        "equivalence",
        "difference",
        "antagonism",
        "hegemony",
        "dislocation",
        "contestation",
    ]] = None
    weight: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: Optional[str] = None


class LaclauGraphExtraction(BaseModel):
    """Extraction schema for Discourse Analysis (Laclau)."""
    nodes: List[LaclauNode]
    edges: List[LaclauEdge]


# ---------------------------------------------------------------------------
# Combined extraction result for all three layers
# ---------------------------------------------------------------------------

class CombinedGraphExtraction(BaseModel):
    """Combined extraction result across all three graph layers."""
    social: SocialGraphExtraction
    castells: CastellsGraphExtraction
    laclau: LaclauGraphExtraction