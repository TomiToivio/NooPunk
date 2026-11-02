"""Headless deterministic investigation slice, independent of game engines.

This is an original, system-neutral narrative prototype, NOT a CWN rules
implementation. Published CWN/SWN/WWN/AWN rules remain authoritative.
"""
from dataclasses import dataclass, field, asdict
import json

STATE_VERSION = 1

@dataclass(frozen=True)
class Action:
    name: str

@dataclass
class GameState:
    version: int = STATE_VERSION
    location: str = "unsa_hq"
    clues: list[str] = field(default_factory=list)
    sidequest_done: bool = False
    finished: bool = False

@dataclass(frozen=True)
class Outcome:
    message: str
    events: tuple[str, ...] = ()

class Game:
    """Minimal playable UNSA case and optional sidequest; no random rules."""
    def __init__(self, state: GameState | None = None):
        self.state = state or GameState()
        if self.state.version != STATE_VERSION:
            raise ValueError("Unsupported campaign save version")

    def available_actions(self) -> tuple[str, ...]:
        if self.state.finished:
            return ("status",)
        at = self.state.location
        if at == "unsa_hq":
            return ("briefing", "go_hospital", "go_library", "status")
        if at == "hospital":
            return ("examine_room", "interview_witness", "go_hq", "conclude", "status")
        return ("catalogue_record", "go_hq", "status")

    def apply(self, action: Action) -> Outcome:
        name = action.name.strip().lower()
        if name not in self.available_actions():
            return Outcome("That action is not available here.")
        s = self.state
        if name == "status":
            return Outcome(f"Location: {s.location}; clues: {', '.join(s.clues) or 'none'}; sidequest: {'done' if s.sidequest_done else 'open'}; case: {'closed' if s.finished else 'open'}")
        if name == "briefing":
            return Outcome("Inspector Romppainen assigns you an anomaly report at the hospital. Find two independent clues and return your conclusion.")
        if name.startswith("go_"):
            s.location = {"go_hospital": "hospital", "go_library": "library", "go_hq": "unsa_hq"}[name]
            return Outcome(f"You arrive at {s.location}.", ("location_changed",))
        if name == "catalogue_record":
            s.sidequest_done = True
            return Outcome("Sidequest completed: the library catalogue identifies the missing ward's previous name.", ("sidequest_completed",))
        if name in ("examine_room", "interview_witness"):
            clue = {"examine_room": "anomalous_clock", "interview_witness": "witness_statement"}[name]
            if clue not in s.clues:
                s.clues.append(clue)
                return Outcome(f"Evidence recorded: {clue}.", ("clue_found",))
            return Outcome("You already documented that evidence.")
        if name == "conclude":
            if len(s.clues) < 2:
                return Outcome("Insufficient evidence. Find two independent clues before concluding.")
            s.finished = True
            return Outcome("Case solved. You submit a cautious anomaly report to UNSA. Campaign slice complete.", ("case_completed",))
        raise AssertionError("Unreachable action")

    def to_json(self) -> str:
        return json.dumps(asdict(self.state), sort_keys=True)

    @classmethod
    def from_json(cls, serialized: str) -> "Game":
        data = json.loads(serialized)
        if not isinstance(data, dict) or set(data) != {"version", "location", "clues", "sidequest_done", "finished"}:
            raise ValueError("Invalid campaign state")
        if data["version"] != STATE_VERSION or data["location"] not in ("unsa_hq", "hospital", "library") or not isinstance(data["clues"], list) or any(c not in ("anomalous_clock", "witness_statement") for c in data["clues"]) or len(data["clues"]) != len(set(data["clues"])) or type(data["sidequest_done"]) is not bool or type(data["finished"]) is not bool:
            raise ValueError("Invalid campaign state")
        return cls(GameState(**data))
