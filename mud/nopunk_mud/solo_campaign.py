"""Deterministic, single-player UNSA prologue. No AI, Evennia or GM required.

Pure transition function: caller persists the resulting JSON-compatible state.
Scene content is original NoöPunk material, not copied from the CWN book.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict

@dataclass
class Campaign:
    stage: str = "briefing"
    clues: list[str] = field(default_factory=list)
    completed: list[str] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(stage=data.get("stage", "briefing"),
                   clues=list(data.get("clues", [])),
                   completed=list(data.get("completed", [])))

SCENES = {
    "briefing": "UNSA Helsinki: The dispatcher reports a missing university researcher. Start with 'accept'.",
    "investigation": "Investigate Kurvi and university records. Use 'interview', 'records' or 'report'.",
    "report": "UNSA headquarters awaits your report. Use 'submit' to close the case.",
    "complete": "Case closed. The official record is incomplete, but your investigation made a difference.",
}

def advance(campaign: Campaign, action: str, location: str) -> tuple[Campaign, str]:
    """Return a new state and feedback; rejected actions do not advance the story."""
    c = Campaign.from_dict(campaign.to_dict())
    action = action.lower().strip()
    if action == "status":
        return c, SCENES[c.stage] + " Clues: " + (", ".join(c.clues) or "none")
    if c.stage == "briefing" and action == "accept" and location == "UNSA safehouse":
        c.stage = "investigation"
        return c, "Assignment accepted: trace the researcher's last known movements."
    if c.stage == "investigation":
        if action == "interview" and location == "Kurvi":
            if "witness" not in c.clues:
                c.clues.append("witness")
            return c, "A witness remembers a university badge and an unmarked vehicle."
        if action == "records" and location == "University of Helsinki":
            if "records" not in c.clues:
                c.clues.append("records")
            return c, "Access logs place the researcher in the laboratory after closing."
        if action == "report" and location == "UNSA safehouse":
            if not c.clues:
                return c, "You have no evidence yet. Investigate before reporting."
            c.stage = "report"
            return c, "The dispatcher opens a confidential case file. Submit your findings."
    if c.stage == "report" and action == "submit" and location == "UNSA safehouse":
        c.stage = "complete"
        c.completed.append("Missing Researcher")
        return c, "Mission complete: Missing Researcher. Your evidence is filed."
    return c, "That action is unavailable here or at this stage. Use 'case status'."
