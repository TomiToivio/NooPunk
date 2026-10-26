"""NoöPunk transhuman identity continuity and embodiment.

Original mechanics inspired by SWN Revised deluxe Transhuman Campaigns,
printed pp. 248–265. This is NOT a transcription of copyrighted shell and
Face tables. Rules are deliberately explicit about mind continuity.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class ContinuityError(ValueError):
    pass


class DuplicationPolicy(str, Enum):
    SOFT = "soft"  # one active mind per continuity lineage
    HARD = "hard"  # independent simultaneous forks


@dataclass(frozen=True)
class Shell:
    identifier: str
    type: str
    physical: bool = True
    capacity: int = 1
    strain: int = 0

    def __post_init__(self):
        if not self.identifier or not self.type:
            raise ContinuityError("shell requires identity and type")
        if type(self.capacity) is not int or self.capacity < 1:
            raise ContinuityError("shell capacity must be positive")
        if type(self.strain) is not int or self.strain < 0:
            raise ContinuityError("shell strain must be nonnegative")


@dataclass(frozen=True)
class Imprint:
    identifier: str
    lineage: str
    revision: int
    memory_marker: str

    def __post_init__(self):
        if not self.identifier or not self.lineage or not self.memory_marker:
            raise ContinuityError("imprint requires identifiers and a memory marker")
        if type(self.revision) is not int or self.revision < 0:
            raise ContinuityError("revision must be nonnegative")


@dataclass
class Mind:
    identifier: str
    lineage: str
    imprint: Imprint
    shell: Shell | None = None
    active: bool = False

    def __post_init__(self):
        if not self.identifier or self.lineage != self.imprint.lineage:
            raise ContinuityError("mind and imprint lineage mismatch")
        if self.active and self.shell is None:
            raise ContinuityError("active mind requires a shell")


@dataclass
class ContinuityRegistry:
    """Track separate agents rather than overwriting identity on copying.

    Backups are inert Imprints. Activation is subject to the selected policy;
    creating a backup never silently kills, merges or replaces its origin.
    """
    policy: DuplicationPolicy
    minds: dict[str, Mind] = field(default_factory=dict)
    backups: dict[str, Imprint] = field(default_factory=dict)
    events: list[dict] = field(default_factory=list)

    def _check_shell(self, shell: Shell, exclude: str = "") -> None:
        if any(m.active and m.shell is not None and m.shell.identifier == shell.identifier
               and m.identifier != exclude for m in self.minds.values()):
            raise ContinuityError("shell already occupied")

    def register(self, mind: Mind) -> None:
        if mind.identifier in self.minds:
            raise ContinuityError("mind identifier already registered")
        if mind.active:
            self._check_shell(mind.shell)
            if self.policy == DuplicationPolicy.SOFT and any(
                m.active and m.lineage == mind.lineage for m in self.minds.values()
            ):
                raise ContinuityError("soft policy prohibits simultaneous lineage instances")
        self.minds[mind.identifier] = mind
        self.events.append({"event": "register", "mind": mind.identifier})

    def backup(self, mind_id: str, backup_id: str) -> Imprint:
        if mind_id not in self.minds or not backup_id or backup_id in self.backups:
            raise ContinuityError("unknown mind or duplicate backup")
        mind = self.minds[mind_id]
        imprint = Imprint(backup_id, mind.lineage, mind.imprint.revision, mind.imprint.memory_marker)
        self.backups[backup_id] = imprint
        self.events.append({"event": "backup", "mind": mind_id, "imprint": backup_id})
        return imprint

    def deactivate(self, mind_id: str) -> None:
        if mind_id not in self.minds:
            raise ContinuityError("unknown mind")
        self.minds[mind_id].active = False
        self.events.append({"event": "deactivate", "mind": mind_id})

    def resleeve(self, mind_id: str, shell: Shell) -> None:
        mind = self.minds.get(mind_id)
        if mind is None or not mind.active:
            raise ContinuityError("resleeving requires an active mind")
        self._check_shell(shell, exclude=mind_id)
        mind.shell = shell
        self.events.append({"event": "resleeve", "mind": mind_id, "shell": shell.identifier})

    def instantiate(self, backup_id: str, mind_id: str, shell: Shell) -> Mind:
        if backup_id not in self.backups or not mind_id or mind_id in self.minds:
            raise ContinuityError("backup missing or mind identifier reused")
        imprint = self.backups[backup_id]
        self._check_shell(shell)
        if self.policy == DuplicationPolicy.SOFT and any(
            m.active and m.lineage == imprint.lineage for m in self.minds.values()
        ):
            raise ContinuityError("soft continuity requires prior instance to be inactive")
        mind = Mind(mind_id, imprint.lineage, imprint, shell, True)
        self.minds[mind_id] = mind
        self.events.append({"event": "instantiate", "mind": mind_id,
                            "source": backup_id, "shell": shell.identifier})
        return mind

    def active_lineage(self, lineage: str) -> list[str]:
        return sorted(m.identifier for m in self.minds.values()
                      if m.active and m.lineage == lineage)
