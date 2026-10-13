"""Declaration-only PSI operation seam for NoöPunk Global (issue #345).

A psychic operation is an agent-led mission, not a free action from a passive asset.
This boundary records proposals and uncertain observations. It neither rolls dice
nor authenticates anomalous claims, and invents no PSI skill or power statistics.
It is independent of the approved Fate-based character RPG resolver.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


class PsiOperationError(ValueError):
    """Invalid operation declaration or report."""


@dataclass(frozen=True)
class PsiOperation:
    identifier: str
    agent_id: str
    target_id: str
    location_id: str
    approach: str
    asset_ids: tuple[str, ...] = ()
    purpose: str = ""

    def __post_init__(self) -> None:
        for name in ("identifier", "agent_id", "target_id", "location_id", "approach"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise PsiOperationError(f"{name} must be a nonempty string")
        if not isinstance(self.asset_ids, tuple) or any(
            not isinstance(asset, str) or not asset.strip() for asset in self.asset_ids
        ):
            raise PsiOperationError("asset_ids must be a tuple of nonempty identifiers")
        if len(set(self.asset_ids)) != len(self.asset_ids):
            raise PsiOperationError("asset_ids cannot contain duplicates")
        if not isinstance(self.purpose, str):
            raise PsiOperationError("purpose must be a string")

    def to_dict(self) -> dict[str, object]:
        return {
            "id": self.identifier,
            "agent_id": self.agent_id,
            "target_id": self.target_id,
            "location_id": self.location_id,
            "approach": self.approach,
            "asset_ids": list(self.asset_ids),
            "purpose": self.purpose,
        }


@dataclass(frozen=True)
class PsiFinding:
    """Unverified testimony or observation, never an automatic world-state fact."""

    operation_id: str
    observation: str
    verification: str = "unverified"
    evidence_refs: tuple[str, ...] = ()
    alternative_explanations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.operation_id.strip() or not self.observation.strip():
            raise PsiOperationError("finding requires operation_id and observation")
        if self.verification not in ("unverified", "inconclusive", "corroborated", "contradicted"):
            raise PsiOperationError("unknown verification status")
        for values in (self.evidence_refs, self.alternative_explanations):
            if not isinstance(values, tuple) or any(not isinstance(x, str) or not x.strip() for x in values):
                raise PsiOperationError("evidence and alternatives must be tuples of nonempty strings")
        if self.verification == "corroborated" and not self.evidence_refs:
            raise PsiOperationError("corroborated findings need independent evidence references")

    def to_dict(self) -> dict[str, object]:
        return {
            "operation_id": self.operation_id,
            "observation": self.observation,
            "verification": self.verification,
            "evidence_refs": list(self.evidence_refs),
            "alternative_explanations": list(self.alternative_explanations),
        }


@dataclass
class PsiOperationLedger:
    """A small record boundary. No effects on politics, targets or other layers."""

    operations: dict[str, PsiOperation] = field(default_factory=dict)
    findings: dict[str, list[PsiFinding]] = field(default_factory=dict)

    def declare(self, operation: PsiOperation, *, agents: Mapping[str, object], assets: Mapping[str, object]) -> None:
        if operation.identifier in self.operations:
            raise PsiOperationError("operation identifier already exists")
        if operation.agent_id not in agents:
            raise PsiOperationError("a known named agent must lead the operation")
        if any(asset_id not in assets for asset_id in operation.asset_ids):
            raise PsiOperationError("operation refers to an unknown asset")
        self.operations[operation.identifier] = operation

    def report(self, finding: PsiFinding) -> None:
        if finding.operation_id not in self.operations:
            raise PsiOperationError("finding refers to an unknown operation")
        self.findings.setdefault(finding.operation_id, []).append(finding)

    def to_dict(self) -> dict[str, object]:
        return {
            "operations": [self.operations[key].to_dict() for key in sorted(self.operations)],
            "findings": {key: [finding.to_dict() for finding in values]
                         for key, values in sorted(self.findings.items())},
        }
