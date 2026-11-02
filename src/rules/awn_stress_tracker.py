"""AWN Stress tracker in plain Python (#1083), reading the same contract as the Godot mod.

`data/rules/awn_stress.json` is the single source of the numbers. `mods/noopunk/stress.gd` loads it; this module
loads it too, so a scene can run without Godot and neither implementation can drift into owning its own copy of a
threshold. **No numeric rule value is written in this file** — if you find a literal here, it is a bug.

What the contract says, and what this file therefore refuses to do:

* The ceiling is the character's **CWN WIS score**, not a new attribute. Equality is safe: the check fires when
  Stress rises **above** WIS.
* The **save belongs to CWN core**. This module never rolls: the caller resolves the Mental save and passes the
  outcome in.
* A successful save does not reduce Stress.
* Hardening is a **player choice**, clears Stress to zero, grants a psychic scar and is irreversible.

Licence: AWN has no verified open licence in this repository, so the contract is a *procedure* in NooPunk wording.
This module adds no new wording, only arithmetic over the values that already exist.
"""
from __future__ import annotations

import json
from pathlib import Path

CONTRACT_PATH = Path(__file__).resolve().parents[2] / "data/rules/awn_stress.json"


class StressError(ValueError):
    """A rule was about to be broken."""


def load_contract(path: str | Path | None = None) -> dict:
    contract = json.loads(Path(path or CONTRACT_PATH).read_text(encoding="utf-8"))
    for key in ("threshold", "gaining", "recovery", "hardening"):
        if key not in contract:
            raise StressError(f"contract is missing {key!r}")
    return contract


CONTRACT = load_contract()


def event_ids() -> list[str]:
    return [e["id"] for e in CONTRACT["gaining"]["events"]]


def recovery_ids() -> list[str]:
    return [e["id"] for e in CONTRACT["recovery"]["events"]]


def event(event_id: str) -> dict:
    for row in CONTRACT["gaining"]["events"]:
        if row["id"] == event_id:
            return row
    raise StressError(f"unknown stress event {event_id!r}")


def recovery(event_id: str) -> dict:
    for row in CONTRACT["recovery"]["events"]:
        if row["id"] == event_id:
            return row
    raise StressError(f"unknown recovery {event_id!r}")


def new_tracker(wisdom: int, *, enabled: bool = True, stress: int = 0,
                hardening_count: int = 0, scars: list[str] | None = None) -> dict:
    """The same shape the GDScript builds, so a save can move between the two."""
    if wisdom < 1:
        raise StressError("WIS must be at least 1")
    return {
        "enabled": bool(enabled),
        "wisdom": int(wisdom),
        "stress": max(0, int(stress)),
        "hardening_count": max(0, int(hardening_count)),
        "scars": list(scars or []),
        "awaiting_breakdown": False,
        "pending_save": {"required": False, "kind": CONTRACT["threshold"]["save"], "penalty": 0},
        "recovered_today": {},
        "day": 1,
        "audit": [],
    }


def is_enabled(tracker: dict) -> bool:
    return bool(tracker.get("enabled", False))


def stress(tracker: dict) -> int:
    return int(tracker.get("stress", 0))


def threshold(tracker: dict) -> int:
    """CWN WIS, per the contract — never a new attribute."""
    return int(tracker.get("wisdom", 1))


def over_by(tracker: dict) -> int:
    return max(0, stress(tracker) - threshold(tracker))


def is_over(tracker: dict) -> bool:
    """Equality is safe: the contract crosses when Stress is *above* WIS."""
    return stress(tracker) > threshold(tracker)


def penalty(tracker: dict) -> int:
    """first_penalty for the first point over, then penalty_step per further point, uncapped, reset when safe."""
    if not is_over(tracker):
        return 0
    rule = CONTRACT["threshold"]
    steps = over_by(tracker) - 1
    return int(rule["first_penalty"]) + steps * int(rule["penalty_step"])


def apply_event(tracker: dict, event_id: str, *, amount: int | None = None) -> dict:
    """Gain Stress. The save is *flagged*, not rolled — CWN core owns the die."""
    row = event(event_id)
    delta = row["stress"] if amount is None else amount
    before = stress(tracker)
    tracker["stress"] = max(0, before + int(delta))
    tracker["audit"].append({"op": "gain", "event": event_id, "delta": int(delta),
                             "from": before, "to": tracker["stress"]})
    crossed = (not before > threshold(tracker)) and is_over(tracker) and int(delta) > 0
    if crossed:
        tracker["awaiting_breakdown"] = True
        tracker["pending_save"] = {"required": True,
                                   "kind": CONTRACT["threshold"]["save"],
                                   "penalty": penalty(tracker)}
    return tracker


def recover(tracker: dict, recovery_id: str) -> dict:
    """Apply a recovery row, honouring its per-day limit and its cost."""
    row = recovery(recovery_id)
    used = tracker["recovered_today"].get(recovery_id, 0)
    limit = row.get("per_day")
    if limit is not None and used >= limit:
        raise StressError(f"{recovery_id} already used {used} time(s) today")
    before = stress(tracker)
    tracker["stress"] = max(0, before + int(row.get("stress", 0)))
    tracker["recovered_today"][recovery_id] = used + 1
    tracker["audit"].append({"op": "recover", "event": recovery_id,
                             "delta": int(row.get("stress", 0)), "from": before,
                             "to": tracker["stress"], "cost": row.get("cost", {})})
    if not is_over(tracker):
        tracker["awaiting_breakdown"] = False
        tracker["pending_save"] = {"required": False,
                                   "kind": CONTRACT["threshold"]["save"], "penalty": 0}
    return tracker


def harden(tracker: dict, scar: str) -> dict:
    """Player choice: clears Stress to zero, grants a psychic scar, irreversible."""
    if not scar:
        raise StressError("hardening grants a psychic scar and needs its id")
    rule = CONTRACT["hardening"]
    if not rule.get("player_choice", False):
        raise StressError("the contract does not allow choosing Hardening")
    tracker["stress"] = int(rule.get("clears_stress_to", 0))
    tracker["hardening_count"] = int(tracker.get("hardening_count", 0)) + 1
    tracker["scars"].append(scar)
    tracker["awaiting_breakdown"] = False
    tracker["pending_save"] = {"required": False,
                               "kind": CONTRACT["threshold"]["save"], "penalty": 0}
    tracker["audit"].append({"op": "harden", "scar": scar,
                             "hardening_count": tracker["hardening_count"]})
    return tracker


def next_day(tracker: dict) -> dict:
    """Reset the per-day recovery ledger; Stress itself does not move on its own."""
    tracker["day"] = int(tracker.get("day", 1)) + 1
    tracker["recovered_today"] = {}
    return tracker
