"""WWN spell effects, batch 1 (High Magic level 1) — the resolver interface (#1085).

The catalogue (`data/rules/wwn_spells.json`) knows *which* spells exist and at what level. This module
adds what happens when one is cast, for the thirteen High Magic level-1 spells, as structured data
rather than prose:

* a damage formula resolves arithmetically (`1d8 per caster level` becomes a dice count and a total
  once the caller supplies the roll — this module never rolls);
* a save is returned as `{category, on_success, ...}` for the CWN core to resolve, never rolled here;
* anything the table must adjudicate comes back with `manual: true` and a one-line reason, so a caller
  cannot mistake "no structured effect" for "no effect".

Source: the WWN SRD (CC0). The rows paraphrase mechanics; no SRD sentence is reproduced. Spells whose
effects are not transcribed yet are refused by name rather than guessed — the remaining 39 High Magic,
15 Elementalist and 16 Necromancer entries are content work, tracked on #1085.
"""
from __future__ import annotations

import json
from pathlib import Path

EFFECTS_PATH = Path(__file__).resolve().parents[2] / "data/rules/wwn_spell_effects.json"

#: Effect kinds this batch uses. A caller should treat an unknown kind as `manual`.
KINDS = ("damage", "damage_or_destruction", "buff", "buff_or_debuff", "debuff", "control",
         "illusion", "information", "incapacitate")

_CACHE: dict[str, dict] = {}


class EffectError(ValueError):
    """A spell has no transcribed effect, or the call cannot be resolved without guessing."""


def load_effects(path: str | Path | None = None) -> dict[str, dict]:
    resolved = Path(path or EFFECTS_PATH).resolve()
    key = str(resolved)
    if not resolved.is_file():
        raise EffectError(f"the spell-effect catalogue is missing: {resolved}")
    if key not in _CACHE:
        data = json.loads(resolved.read_text(encoding="utf-8"))
        if data.get("format") != "noopunk.rules.wwn_spell_effects":
            raise EffectError(f"{resolved} is not a spell-effect catalogue")
        rows: dict[str, dict] = {}
        for row in data["effects"]:
            identifier = str(row.get("id", ""))
            if not identifier:
                raise EffectError("an effect row has no id")
            if identifier in rows:
                raise EffectError(f"duplicate effect {identifier}")
            if row.get("kind") not in KINDS:
                raise EffectError(f"{identifier}: unknown effect kind {row.get('kind')!r}")
            rows[identifier] = row
        _CACHE[key] = rows
    return _CACHE[key]


EFFECTS: dict[str, dict] = load_effects()


def effect(spell_id: str) -> dict:
    """The transcribed effect, or a refusal that names what is missing."""
    try:
        return EFFECTS[spell_id]
    except KeyError:
        raise EffectError(
            f"no transcribed effect for {spell_id!r}: only High Magic level 1 is in this batch "
            "(see issue #1085). Refusing rather than inventing an effect.") from None


def resolve(spell_id: str, *, caster_level: int, roll_total: int | None = None,
            save_made: bool | None = None) -> dict:
    """Resolve a spell into a structured, ready-to-apply result.

    ``roll_total`` is the caller's damage roll (the module does not own dice); ``save_made`` is the
    CWN core's save outcome. Both are optional at the point of resolution because a caller may be
    asking only *what would happen* — the returned payload then reports what it still needs.
    """
    if caster_level < 1:
        raise EffectError("caster level starts at 1")
    row = effect(spell_id)
    result: dict = {
        "spell": spell_id,
        "kind": row["kind"],
        "targets": row.get("targets", ""),
        "range": row.get("range", ""),
        "duration": row.get("duration", ""),
        "save": row.get("save"),
        "manual": bool(row.get("manual", False)),
        "note": row.get("note", ""),
    }
    if row.get("cost"):
        result["cost"] = dict(row["cost"])
    if "ignores" in row:
        result["ignores"] = list(row["ignores"])

    formula = row.get("damage")
    if formula:
        count = str(formula["die"]).partition("d")[0]
        dice = int(count or 1)
        per = str(formula.get("per", ""))
        multiplier = caster_level if per == "caster_level" else 1
        result["damage"] = {
            "die": formula["die"],
            "dice": dice * multiplier,
            "per": per,
            "applies_to": formula.get("applies_to", ""),
            "rolled_total": roll_total,
            "applied_total": _applied_total(roll_total, save_made, row.get("save")),
        }
        if roll_total is None:
            result["needs"] = "a damage roll (this module does not roll)"
    if row.get("save") and save_made is None:
        result.setdefault("needs", "the core's save outcome")
    return result


def _applied_total(roll_total: int | None, save_made: bool | None, save: dict | None) -> int | None:
    """Half on a made save when the row says half; the full total otherwise."""
    if roll_total is None:
        return None
    if save and save_made and save.get("on_success") == "half":
        return roll_total // 2
    if save and save_made and save.get("on_success") in ("negates the hit, per hit",):
        return 0
    return roll_total


def transcribed() -> list[str]:
    return sorted(EFFECTS)


def untranscribed(spells: list[str]) -> list[str]:
    """Which of the given spell ids still have no effect row — the batch boundary, stated plainly."""
    return sorted(set(spells) - set(EFFECTS))
