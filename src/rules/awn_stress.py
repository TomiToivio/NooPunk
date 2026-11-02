"""AWN Stress, Breakdowns and Hardening — the Python owner of the #928 contract (#1083).

`data/rules/awn_stress.json` is the single source of the numbers. This module *reads* it and never
restates a value, and it never rolls dice: a diced amount arrives from the caller (`rolls={...}` or
`value=...`), because the CWN core owns the dice and a Stress overlay that rolled its own would be a
second resolution system.

The tracker is an **optional overlay**: nothing here changes a CWN attribute, check, save, hit point
total, System Strain pool or progression. `enabled=False` is the default and every method then
returns a no-op result, which is what lets a campaign ignore the module entirely.

Save format: `to_dict()` writes the same document `mods/noopunk/stress.gd` writes
(`noopunk.stress_tracker`, version 1) so the same save loads in either implementation. That is the
point of the port — one contract, one save, two front ends.

Why the port exists at all: #928 built this in GDScript, and the AWN inventory (#1045) recorded that
the rules library could not run an AWN scene without Godot. The rules are supposed to live in Python
and the engines are supposed to be adapters; this module moves the rule to where the architecture says
it belongs, and the Godot overlay becomes a consumer of the same contract.
"""
from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

CONTRACT_PATH = Path(__file__).resolve().parents[2] / "data/rules/awn_stress.json"

TRACKER_FORMAT = "noopunk.stress_tracker"
TRACKER_VERSION = 1
AUDIT_LIMIT = 200

_CACHE: dict[str, Any] = {}


class StressError(ValueError):
    """A rule was about to be broken: unknown event, a roll that was never supplied, bad save."""


def load_contract(path: str | Path | None = None) -> dict:
    """Read the contract, cached by resolved path."""
    resolved = Path(path or CONTRACT_PATH).resolve()
    key = str(resolved)
    if not resolved.is_file():
        raise StressError(f"the AWN stress contract is missing: {resolved}")
    if key not in _CACHE:
        data = json.loads(resolved.read_text(encoding="utf-8"))
        if data.get("format") != "noopunk.rules.awn_stress":
            raise StressError(f"{resolved} is not the AWN stress contract")
        _CACHE[key] = data
    return _CACHE[key]


def contract_path() -> Path:
    return CONTRACT_PATH


def _find(rows: Iterable[dict], identifier: str) -> dict:
    for row in rows:
        if str(row.get("id", "")) == identifier:
            return row
    return {}


def _ids(rows: Iterable[dict]) -> list[str]:
    return [str(row.get("id", "")) for row in rows]


def _amount(value: Any, options: dict, key: str) -> int:
    """Resolve a contract value that may be a number or a dice expression.

    The module never rolls: a dice value must arrive in ``options["rolls"][key]`` or as
    ``options["value"]``. That is the same rule the Godot overlay enforces, and it is what keeps the
    RNG in one place.
    """
    if isinstance(value, bool):
        raise StressError(f"{key}: a boolean is not a Stress amount")
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value or "").strip()
    if not text:
        return 0
    sign = 1
    body = text
    if body.startswith("-"):
        sign, body = -1, body[1:]
    rolls = options.get("rolls") or {}
    if key in rolls:
        return sign * int(rolls[key])
    if "value" in options:
        return sign * int(options["value"])
    raise StressError(f"a roll is required for {key} ({text}): this module does not roll dice")


def _base_amount(row: dict, options: dict, key: str) -> int:
    """A ranged entry ("one to three") takes the value the table picked, clamped into the range."""
    band = row.get("stress_range")
    if isinstance(band, list) and len(band) == 2 and "value" in options:
        low, high = int(band[0]), int(band[1])
        return max(low, min(high, int(options["value"])))
    return _amount(row.get("stress", 0), options, key)


class Stress:
    """One character's Stress tracker. Every method returns data; none of them touches a sheet."""

    def __init__(self, wisdom: int, *, enabled: bool | None = None, level: int = 1,
                 stress: int = 0, hardening_count: int = 0, scars: Iterable[str] = (),
                 addiction: bool = False, contract: dict | None = None) -> None:
        self.contract = contract or load_contract()
        contract_default = bool(self.contract["module"]["default_enabled"])
        self.enabled = contract_default if enabled is None else bool(enabled)
        self.wisdom = max(1, int(wisdom))
        self.level = max(1, int(level))
        self.stress = max(0, int(stress))
        self.hardening_count = max(0, int(hardening_count))
        self.scars = list(scars)
        self.active_breakdown = ""
        self.checks_made = 0
        self.awaiting_breakdown = False
        self._pending_save: dict = {"required": False, "kind": "mental", "penalty": 0}
        self.last_check: dict = {}
        self.day = 1
        self.recovered_today: dict[str, int] = {}
        self.scene: dict[str, Any] = {"raw": 0, "causes": []}
        self.addiction: dict[str, Any] = {"enabled": bool(addiction), "addictions": [],
                          "system_strain": 0, "missed_today": False,
                          "months_clean": 0, "weeks_clean": 0}
        self.audit: list[dict] = []
        self.seq = 0
        if not self.enabled:
            self._log("module", {"enabled": False})

    # ---- reading ---------------------------------------------------------
    @property
    def threshold(self) -> int:
        """The ceiling is the character's CWN WIS score, not a new attribute."""
        return self.wisdom

    @property
    def is_over(self) -> bool:
        return self.stress > self.threshold

    @property
    def over_by(self) -> int:
        return max(0, self.stress - self.threshold)

    def has_scar(self, identifier: str) -> bool:
        return identifier in self.scars

    def pending_save(self) -> dict:
        return dict(self._pending_save)

    def next_penalty(self) -> int:
        rules = self.contract["threshold"]
        return int(rules.get("first_penalty", -2)) + int(rules.get("penalty_step", -2)) * self.checks_made

    def active_conditions(self) -> list[dict]:
        rows: list[dict] = []
        if self.active_breakdown:
            row = _find(self.contract["breakdowns"]["options"], self.active_breakdown)
            rows.append({"kind": "breakdown", "id": self.active_breakdown,
                         "label": row.get("label", self.active_breakdown),
                         "effects": row.get("effects", {})})
        for identifier in self.scars:
            row = _find(self.contract["scars"]["options"], identifier)
            rows.append({"kind": "scar", "id": identifier, "label": row.get("label", identifier),
                         "effects": row.get("effects", {})})
        return rows

    def latest_causes(self) -> list[dict]:
        return list(self.scene.get("causes", []))

    # ---- the scene -------------------------------------------------------
    def begin_scene(self) -> dict:
        self.scene = {"raw": 0, "causes": []}
        self._log("scene", {"opened": True})
        return {"ok": True}

    def award(self, event_id: str, *, modifiers: Iterable[str] = (), rolls: dict | None = None,
              value: int | None = None, participated: bool = True) -> dict:
        """Record one stress-inducing event. The meter moves at ``end_scene``."""
        if not self.enabled:
            return {"ok": True, "enabled": False, "applied": 0, "pending": 0}
        row = _find(self.contract["gaining"]["events"], event_id)
        if not row:
            row = _find(self.contract.get("noopunk_events", {}).get("events", []), event_id)
        if not row:
            return {"ok": False, "reason": f"unknown stress event: {event_id}"}
        if not participated:
            # Mere presence is not participation. The contract says so; this is where it is enforced.
            return {"ok": True, "applied": 0, "pending": 0, "skipped": "not_a_participant"}
        if self.active_breakdown:
            self._log("suppressed", {"event": event_id, "reason": "breakdown"})
            return {"ok": True, "applied": 0, "pending": 0, "suppressed": "breakdown"}
        if self.has_scar("bloodthirsty") and event_id == "kill_human":
            self._log("suppressed", {"event": event_id, "reason": "bloodthirsty"})
            return {"ok": True, "applied": 0, "pending": 0, "suppressed": "bloodthirsty"}

        options = {"rolls": rolls or {}, **({"value": value} if value is not None else {})}
        raw = _base_amount(row, options, event_id)
        chosen = list(modifiers)
        modifier_rows: list[dict] = []
        for modifier in row.get("modifiers", []):
            identifier = str(modifier.get("id", ""))
            if identifier not in chosen:
                continue
            amount = _amount(modifier.get("stress", 0), options, identifier)
            raw += amount
            modifier_rows.append({"id": identifier, "value": amount})

        blunted = min(raw, self._addiction_count())
        raw = max(0, raw - blunted)
        self.scene["causes"].append({"event": event_id, "raw": raw, "modifiers": modifier_rows,
                                     "system": str(row.get("system", "awn"))})
        self.scene["raw"] = int(self.scene.get("raw", 0)) + raw
        projected = self._projected_gain()
        self._log("gain", {"event": event_id, "raw": raw, "projected": projected, "blunted": blunted})
        return {"ok": True, "event": event_id, "raw": raw, "modifiers": modifier_rows,
                "blunted": blunted, "pending": projected,
                "resisted": int(self.scene.get("raw", 0)) - projected}

    def end_scene(self) -> dict:
        if not self.enabled:
            return {"ok": True, "enabled": False}
        raw = int(self.scene.get("raw", 0))
        resistance = self._resistance_for_scene()
        resisted = min(raw, resistance)
        applied = raw - resisted
        self.stress = max(0, self.stress + applied)
        self.scene = {"raw": 0, "causes": []}
        result: dict[str, Any] = {"ok": True, "raw": raw, "resisted": resisted, "applied": applied,
                                  "stress": self.stress, "threshold": self.threshold,
                                  "save": self.pending_save()}
        if applied > 0 and self.is_over:
            result["save"] = self._arm_check()
        self._log("scene", {"closed": True, "applied": applied, "resisted": resisted,
                            "stress": self.stress})
        return result

    # ---- the check -------------------------------------------------------
    def resolve_save(self, success: bool) -> dict:
        """Hand the core's outcome back in. This module never rolls the save."""
        pending = self._pending_save
        if not pending.get("required", False):
            return {"ok": False, "reason": "no check is pending"}
        penalty = int(pending.get("penalty", -2))
        self.checks_made += 1
        self._pending_save = {"required": False, "kind": "mental", "penalty": 0}
        self.last_check = {"success": success, "penalty": penalty}
        self._log("save", {"success": success, "penalty": penalty})
        result: dict[str, Any] = {"ok": True, "success": success, "penalty": penalty,
                                  "checks_made": self.checks_made,
                                  "next_penalty": self.next_penalty(), "stress": self.stress}
        if success:
            return result
        self.awaiting_breakdown = True
        result.update({"awaiting_breakdown": True, "can_harden": True,
                       "breakdowns": _ids(self.contract["breakdowns"]["options"]),
                       "scars": self._available_scars()})
        return result

    def choose_breakdown(self, identifier: str) -> dict:
        if not self.awaiting_breakdown:
            return {"ok": False, "reason": "no breakdown is owed"}
        row = _find(self.contract["breakdowns"]["options"], identifier)
        if not row:
            return {"ok": False, "reason": f"unknown breakdown: {identifier}"}
        self.active_breakdown = identifier
        self.awaiting_breakdown = False
        self._log("breakdown", {"id": identifier})
        return {"ok": True, "breakdown": identifier, "effects": row.get("effects", {}),
                "ends_when": "stress_at_or_below_wisdom", "label": row.get("label", identifier)}

    def harden(self, scar_id: str) -> dict:
        if not self.awaiting_breakdown:
            return {"ok": False, "reason": "hardening is only available when a breakdown is owed"}
        row = _find(self.contract["scars"]["options"], scar_id)
        if not row:
            return {"ok": False, "reason": f"unknown psychic scar: {scar_id}"}
        if self.has_scar(scar_id):
            return {"ok": False, "reason": f"a psychic scar can only be taken once: {scar_id}"}
        self.scars.append(scar_id)
        self.hardening_count += 1
        self.stress = 0
        self.awaiting_breakdown = False
        self.active_breakdown = ""
        self.checks_made = 0
        self._pending_save = {"required": False, "kind": "mental", "penalty": 0}
        addiction_opened = False
        if scar_id == "addicted" and not self.addiction["enabled"]:
            self.addiction["enabled"] = True
            addiction_opened = True
        self._log("harden", {"scar": scar_id, "hardening_count": self.hardening_count})
        return {"ok": True, "hardening_count": self.hardening_count, "stress": 0,
                "scar": scar_id, "effects": row.get("effects", {}),
                "scene_resistance": self._resistance(), "addiction_opened": addiction_opened,
                "irreversible": True}

    # ---- recovery --------------------------------------------------------
    def new_day(self) -> dict:
        self.day += 1
        self.recovered_today = {}
        if self.addiction["enabled"]:
            self.addiction["missed_today"] = False
        self._log("day", {"day": self.day})
        return {"ok": True, "day": self.day}

    def can_recover(self, identifier: str) -> bool:
        row = _find(self.contract["recovery"]["events"], identifier)
        if not row:
            return False
        blocker = str(row.get("blocked_by_scar", ""))
        if blocker and self.has_scar(blocker):
            return False
        per_day = int(row.get("per_day", 0))
        return per_day <= 0 or self.recovered_today.get(identifier, 0) < per_day

    def recover(self, identifier: str, *, check_success: bool = False,
                failed_chance: bool = False, rolls: dict | None = None,
                value: int | None = None) -> dict:
        if not self.enabled:
            return {"ok": True, "enabled": False}
        row = _find(self.contract["recovery"]["events"], identifier)
        if not row:
            return {"ok": False, "reason": f"unknown recovery: {identifier}"}
        blocker = str(row.get("blocked_by_scar", ""))
        if blocker and self.has_scar(blocker):
            return {"ok": False, "reason": f"{blocker} cannot use this recovery: {identifier}"}
        per_day = int(row.get("per_day", 0))
        if per_day > 0 and self.recovered_today.get(identifier, 0) >= per_day:
            return {"ok": False, "reason": f"{identifier} is already used today"}
        if failed_chance and self.has_scar("bloodthirsty"):
            self._log("recover", {"id": identifier, "failed_chance": True})
            return {"ok": True, "recovered": 0, "failed_chance": True, "stress": self.stress}
        check = row.get("check", {})
        if check and not check_success:
            self.recovered_today[identifier] = self.recovered_today.get(identifier, 0) + 1
            helper = int((row.get("on_failure") or {}).get("helper_stress", 0))
            self._log("recover", {"id": identifier, "check": False, "helper_stress": helper})
            return {"ok": True, "recovered": 0, "check": False, "helper_stress": helper,
                    "stress": self.stress,
                    "note": "the helper carries the Stress; apply it to the helper's own tracker"}

        options = {"rolls": rolls or {}, **({"value": value} if value is not None else {})}
        amount = _amount(row.get("stress", 0), options, identifier)
        self.recovered_today[identifier] = self.recovered_today.get(identifier, 0) + 1
        before = self.stress
        after = max(0, before + amount)
        self.stress = after
        ended = False
        if after <= self.threshold:
            self.checks_made = 0
            self._pending_save = {"required": False, "kind": "mental", "penalty": 0}
            if self.active_breakdown:
                self.active_breakdown = ""
                ended = True
        self._log("recover", {"id": identifier, "recovered": before - after, "stress": after,
                              "ended_breakdown": ended})
        return {"ok": True, "recovered": before - after, "stress": after, "breakdown_ended": ended,
                "system_strain": int((row.get("cost") or {}).get("system_strain", 0)), "check": True}

    # ---- addiction (its own opt-in submodule) ----------------------------
    def addiction_enabled(self) -> bool:
        return bool(self.addiction.get("enabled", False))

    def enable_addiction(self, identifier: str = "") -> dict:
        if not self.enabled:
            return {"ok": False, "reason": "the stress module is off"}
        self.addiction["enabled"] = True
        if identifier and identifier not in self.addiction["addictions"]:
            self.addiction["addictions"].append(identifier)
        self._log("addiction", {"enabled": True, "id": identifier})
        return {"ok": True, "enabled": True, "addictions": list(self.addiction["addictions"])}

    def indulge(self, *, rolls: dict | None = None, value: int | None = None) -> dict:
        if not self.addiction_enabled():
            return {"ok": False, "reason": "the addiction submodule is off"}
        count = self._addiction_count()
        if count == 0:
            return {"ok": False, "reason": "no addiction to indulge"}
        options = {"rolls": rolls or {}, **({"value": value} if value is not None else {})}
        daily = self.contract["addiction"]["effects_while_indulged"]["daily_stress_removed"]
        amount = _amount(daily, options, "daily")
        removed = amount * count
        before = self.stress
        self.stress = max(0, before - removed)
        self.addiction["missed_today"] = False
        ended = False
        if self.active_breakdown and self.stress <= self.threshold:
            self.active_breakdown = ""
            self.checks_made = 0
            ended = True
        self._log("addiction", {"indulged": True, "removed": before - self.stress})
        return {"ok": True, "removed": before - self.stress, "stress": self.stress,
                "breakdown_ended": ended, "requires_strain_check": False}

    def miss_indulgence(self) -> dict:
        if not self.addiction_enabled() or self._addiction_count() == 0:
            return {"ok": False, "reason": "no active addiction"}
        row = self.contract["addiction"]["missed_day"]
        points = 0 if self.active_breakdown else int(row.get("stress", 1))
        self.stress = max(0, self.stress + points)
        self.addiction["missed_today"] = True
        self._log("addiction", {"missed": True, "stress": points})
        return {"ok": True, "stress": self.stress,
                "privation": bool(row.get("counts_as_privation", True)),
                "blocks_rest_recovery": bool(row.get("blocks_rest_recovery", True)),
                "gained": points}

    def rest_recovery_blocked(self) -> bool:
        return bool(self.addiction.get("missed_today", False))

    def monthly_check(self, success: bool) -> dict:
        if not self.addiction_enabled():
            return {"ok": False, "reason": "the addiction submodule is off"}
        if success:
            self.addiction["months_clean"] = int(self.addiction.get("months_clean", 0)) + 1
            self._log("addiction", {"month": True, "success": True})
            return {"ok": True, "success": True,
                    "system_strain": int(self.addiction.get("system_strain", 0))}
        self.addiction["system_strain"] = int(self.addiction.get("system_strain", 0)) + 1
        self._log("addiction", {"month": True, "success": False,
                                "system_strain": self.addiction["system_strain"]})
        return {"ok": True, "success": False, "gained_strain": 1,
                "system_strain": self.addiction["system_strain"],
                "death_window_days": int(self.contract["addiction"]["monthly"]
                                         .get("at_capacity_death_window_days", 30))}

    def break_addiction(self, identifier: str, success: bool) -> dict:
        if not self.addiction_enabled():
            return {"ok": False, "reason": "the addiction submodule is off"}
        if identifier not in self.addiction["addictions"]:
            return {"ok": False, "reason": f"not addicted to {identifier}"}
        if not success:
            self.addiction["weeks_clean"] = int(self.addiction.get("weeks_clean", 0)) + 1
            self._log("addiction", {"clean_attempt": identifier, "success": False})
            return {"ok": True, "success": False,
                    "weeks_clean": self.addiction["weeks_clean"]}
        self.addiction["addictions"].remove(identifier)
        self._log("addiction", {"clean_attempt": identifier, "success": True})
        return {"ok": True, "success": True, "addictions": list(self.addiction["addictions"])}

    # ---- persistence -----------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "format": TRACKER_FORMAT,
            "version": TRACKER_VERSION,
            "enabled": self.enabled,
            "wisdom": self.wisdom,
            "level": self.level,
            "stress": self.stress,
            "hardening_count": self.hardening_count,
            "scars": list(self.scars),
            "active_breakdown": self.active_breakdown,
            "checks_made": self.checks_made,
            "awaiting_breakdown": self.awaiting_breakdown,
            "pending_save": dict(self._pending_save),
            "last_check": dict(self.last_check),
            "day": self.day,
            "recovered_today": dict(self.recovered_today),
            "scene": {"raw": int(self.scene.get("raw", 0)),
                      "causes": [dict(c) for c in self.scene.get("causes", [])]},
            "addiction": {**{k: v for k, v in self.addiction.items() if k != "addictions"},
                          "addictions": list(self.addiction["addictions"])},
            "audit": [dict(e) for e in self.audit],
            "seq": self.seq,
        }

    @classmethod
    def from_dict(cls, data: dict, contract: dict | None = None) -> Stress:
        """Read a save written by either implementation. A foreign or pre-module save is disabled."""
        if not data or str(data.get("format", "")) != TRACKER_FORMAT:
            return cls(int(data.get("wisdom", 10)) if data else 10, enabled=False,
                       contract=contract)
        tracker = cls(int(data.get("wisdom", 10)),
                      enabled=bool(data.get("enabled", False)),
                      level=int(data.get("level", 1)),
                      stress=int(data.get("stress", 0)),
                      hardening_count=int(data.get("hardening_count", 0)),
                      scars=data.get("scars", []),
                      contract=contract)
        tracker.active_breakdown = str(data.get("active_breakdown", ""))
        tracker.checks_made = max(0, int(data.get("checks_made", 0)))
        tracker.awaiting_breakdown = bool(data.get("awaiting_breakdown", False))
        tracker._pending_save = dict(data.get("pending_save")
                                     or {"required": False, "kind": "mental", "penalty": 0})
        tracker.last_check = dict(data.get("last_check") or {})
        tracker.day = max(1, int(data.get("day", 1)))
        tracker.recovered_today = dict(data.get("recovered_today") or {})
        scene = data.get("scene") or {}
        tracker.scene = {"raw": int(scene.get("raw", 0)), "causes": list(scene.get("causes", []))}
        addiction = data.get("addiction") or {}
        tracker.addiction = {
            "enabled": bool(addiction.get("enabled", False)),
            "addictions": list(addiction.get("addictions", [])),
            "system_strain": int(addiction.get("system_strain", 0)),
            "missed_today": bool(addiction.get("missed_today", False)),
            "months_clean": int(addiction.get("months_clean", 0)),
            "weeks_clean": int(addiction.get("weeks_clean", 0)),
        }
        tracker.audit = [dict(e) for e in data.get("audit", [])]
        tracker.seq = int(data.get("seq", 0))
        return tracker

    # ---- internals -------------------------------------------------------
    def _addiction_count(self) -> int:
        if not self.addiction.get("enabled", False):
            return 0
        return len(self.addiction.get("addictions", []))

    def _resistance(self) -> int:
        return self.hardening_count * int(self.contract["hardening"].get("scene_resistance", 1))

    def _resistance_for_scene(self) -> int:
        resistance = self._resistance()
        if not self.has_scar("dependent"):
            return resistance
        exempt = sum(int(cause.get("raw", 0)) for cause in self.scene.get("causes", [])
                     if str(cause.get("event", "")) == "friend_mortal_wound")
        return max(0, resistance - exempt)

    def _projected_gain(self) -> int:
        raw = int(self.scene.get("raw", 0))
        return raw - min(raw, self._resistance_for_scene())

    def _arm_check(self) -> dict:
        penalty = self.next_penalty()
        self._pending_save = {"required": True, "kind": "mental", "penalty": penalty}
        self._log("check_owed", {"penalty": penalty, "checks_made": self.checks_made})
        return self.pending_save()

    def pending_safe(self) -> dict:
        return dict(self._pending_save)

    def _available_scars(self) -> list[str]:
        return [identifier for identifier in _ids(self.contract["scars"]["options"])
                if not self.has_scar(identifier)]

    def _log(self, kind: str, detail: dict) -> None:
        self.seq += 1
        entry = {"seq": self.seq, "kind": kind, "day": self.day, **detail}
        self.audit.append(entry)
        while len(self.audit) > AUDIT_LIMIT:
            self.audit.pop(0)


def new_tracker(wisdom: int, **options: Any) -> Stress:
    """The public constructor, named after the Godot function so a port is obvious."""
    return Stress(wisdom, **options)
