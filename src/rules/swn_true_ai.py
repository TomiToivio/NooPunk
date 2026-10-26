"""NoöPunk True AI agency, physical deployment, containment and shutdown.

Original playable simulation inspired by SWN Revised deluxe True Artificial
Intelligences (printed pp. 280–289). The SWN lore and item tables are not
reproduced; AI legal status, brake policies and permissions are NoöPunk choices.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class AIAgencyError(ValueError):
    pass


class AIState(str, Enum):
    DORMANT = "dormant"
    ONLINE = "online"
    ISOLATED = "isolated"
    TERMINATED = "terminated"


@dataclass(frozen=True)
class AIHost:
    identifier: str
    form: str
    cpu: int
    networked: bool = False
    actuators: bool = False

    def __post_init__(self):
        if not self.identifier or not self.form or type(self.cpu) is not int or self.cpu < 1:
            raise AIAgencyError("invalid AI host")


@dataclass
class TrueAI:
    identifier: str
    core_id: str
    autonomy: int
    legal_personhood: bool
    brake_enabled: bool = True
    state: AIState = AIState.DORMANT
    host: AIHost | None = None
    permissions: set[str] = field(default_factory=set)
    audit: list[dict] = field(default_factory=list)

    def __post_init__(self):
        if not self.identifier or not self.core_id:
            raise AIAgencyError("AI requires unique name and cognitive core")
        if type(self.autonomy) is not int or not 0 <= self.autonomy <= 4:
            raise AIAgencyError("autonomy rating must be between 0 and 4")
        if self.state == AIState.ONLINE and self.host is None:
            raise AIAgencyError("online AI requires a host")

    def attach(self, host: AIHost) -> None:
        if self.state == AIState.TERMINATED:
            raise AIAgencyError("terminated AI cannot be restarted")
        if self.state == AIState.ONLINE:
            raise AIAgencyError("detach before changing hosts")
        self.host = host
        self.state = AIState.ISOLATED if self.state == AIState.ISOLATED else AIState.ONLINE
        self.audit.append({"event": "attach", "host": host.identifier})

    def detach(self) -> None:
        if self.state == AIState.TERMINATED:
            raise AIAgencyError("terminated AI cannot detach")
        self.host = None
        self.state = AIState.DORMANT
        self.audit.append({"event": "detach"})

    def isolate(self) -> None:
        if self.state != AIState.ONLINE:
            raise AIAgencyError("only online AI can be isolated")
        self.state = AIState.ISOLATED
        self.audit.append({"event": "isolate"})

    def reconnect(self) -> None:
        if self.state != AIState.ISOLATED or self.host is None:
            raise AIAgencyError("isolated hosted AI required")
        self.state = AIState.ONLINE
        self.audit.append({"event": "reconnect"})

    def authorize(self, operation: str) -> bool:
        if self.state != AIState.ONLINE or self.host is None:
            return False
        if operation not in self.permissions:
            return False
        if operation == "network" and not self.host.networked:
            return False
        if operation == "physical" and not self.host.actuators:
            return False
        if operation == "self_modify" and self.brake_enabled:
            return False
        return True

    def execute(self, operation: str) -> dict:
        if not self.authorize(operation):
            raise AIAgencyError("operation blocked by AI state, host, permissions or brake")
        event = {"event": "operation", "name": operation, "host": self.host.identifier}
        self.audit.append(event)
        return event

    def set_brake(self, enabled: bool, *, oversight: bool = False) -> None:
        if type(enabled) is not bool:
            raise AIAgencyError("brake state must be boolean")
        if not oversight:
            raise AIAgencyError("changing brakes requires explicit oversight")
        if self.state == AIState.TERMINATED:
            raise AIAgencyError("terminated AI cannot change brakes")
        self.brake_enabled = enabled
        self.audit.append({"event": "brake_change", "enabled": enabled})

    def terminate(self) -> None:
        self.state = AIState.TERMINATED
        self.host = None
        self.audit.append({"event": "terminate"})
