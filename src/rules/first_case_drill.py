"""Run the first NoöPunk case through every ported Without Number procedure.

"The first scenario must use all CWN rules and SWN psionics" is a claim that is
easy to write in a design doc and impossible to falsify. This module makes it
falsifiable: a declarative drill script (``data/scenarios/lakkahaltia/
chassis_drill.json``) names one beat per subsystem, and every beat calls the real
kernel — ``wn_core``, ``cwn_combat``, ``cwn_trauma``, ``cwn_hacking``,
``cwn_strain``, ``cwn_encumbrance``, ``cwn_advancement``, ``cwn_healing``,
``cwn_injury_procedure``, ``cwn_vehicles``, ``cwn_gear_mods``, ``swn_psionics``,
``awn_survival`` and ``wwn_projects``. Nothing is restated here.

## Why a seeded drill and not a narrative playthrough

The Godot slice is the player-facing path; this is the *coverage* path. It is
seeded, so the same seed produces the same log, and
``tests/test_first_case_drill.py`` can assert three things a prose claim cannot:
every required subsystem appears at least once, two runs with one seed agree
exactly, and no beat invents a number the contract does not carry.

## What it does not do

It does not write to canonical case records, it does not decide endings, and it
is not a second resolution engine — every outcome it reports comes out of a
kernel module the rest of the repo already uses.
"""

from __future__ import annotations

import json
import random
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, cast

from . import (
    awn_survival,
    cwn_advancement,
    cwn_combat,
    cwn_core,
    cwn_encumbrance,
    cwn_equipment,
    cwn_gear_mods,
    cwn_hacking,
    cwn_healing,
    cwn_injury_procedure,
    cwn_strain,
    cwn_trauma,
    cwn_vehicles,
    psionics,
    wn_core,
    wwn_projects,
)

DRILL_PATH = (Path(__file__).resolve().parents[2] / "data" / "scenarios" / "lakkahaltia"
              / "chassis_drill.json")


#: ``cwn_core`` takes the printed attribute names; the sheet carries the three-letter codes.
ATTRIBUTE_NAMES = {
    "Strength": "STR", "Dexterity": "DEX", "Constitution": "CON",
    "Intelligence": "INT", "Wisdom": "WIS", "Charisma": "CHA",
}


def _named_attributes(sheet: Mapping[str, Any]) -> dict[str, int]:
    return {name: int(sheet["attributes"][code]) for name, code in ATTRIBUTE_NAMES.items()}


class DrillError(ValueError):
    """The drill script asked for a beat or a reference the kernel cannot resolve."""


@dataclass(frozen=True)
class BeatResult:
    id: str
    where: str
    tags: tuple[str, ...]
    outcome: Mapping[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return {"id": self.id, "where": self.where, "tags": list(self.tags),
                "outcome": dict(self.outcome)}


@dataclass(frozen=True)
class DrillResult:
    seed: int
    beats: tuple[BeatResult, ...] = ()
    sheet: Mapping[str, Any] = field(default_factory=dict)

    @property
    def subsystems(self) -> frozenset[str]:
        found: set[str] = set()
        for beat in self.beats:
            found.update(beat.tags)
        return frozenset(found)

    def coverage_gaps(self, required: frozenset[str]) -> frozenset[str]:
        return required - self.subsystems

    def log(self) -> list[dict[str, Any]]:
        return [beat.as_dict() for beat in self.beats]


def load_drill(path: str | Path | None = None) -> dict[str, Any]:
    return json.loads(Path(path or DRILL_PATH).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
# Beat handlers. One per subsystem; each returns a plain dict for the log.
# --------------------------------------------------------------------------- #


def _skill(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    skills = sheet["skills"]
    skill = str(params["skill"])
    check = wn_core.skill_check(
        attribute_score=int(sheet["attributes"][str(params["attribute"])]),
        skill_level=skills.get(skill),
        difficulty=int(params["difficulty"]),
        rng=rng,
    )
    return {"total": check.total, "difficulty": check.difficulty, "success": check.success,
            "untrained": check.untrained, "dice": list(check.dice)}


def _ward_terminal(sheet: Mapping[str, Any], params: Mapping[str, Any],
                   rng: random.Random) -> dict:
    difficulty = cwn_hacking.security_difficulty(int(params["security"]))
    check = cwn_hacking.hacking_check(
        intelligence_score=int(sheet["attributes"]["INT"]),
        program_skill=sheet["skills"].get("Program"),
        difficulty=difficulty,
        wireless=bool(params.get("wireless")),
        vr_crown=bool(params.get("vr_crown")),
        verb_modifier=int(params.get("verb_modifier", 0)),
        rng=rng,
    )
    return {"access_pool": cwn_hacking.access_pool(
                intelligence_modifier=wn_core.attribute_modifier(int(sheet["attributes"]["INT"])),
                program_skill=int(sheet["skills"].get("Program") or 0)),
            "connection_penalty": check.connection_penalty,
            "total": check.total, "difficulty": check.difficulty, "success": check.success}


def _opposed(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    mine = _skill(sheet, params, rng)
    opponent = int(params["opponent_total"])
    return {"mine": mine["total"], "opponent": opponent,
            "won": mine["total"] > opponent, "success": mine["total"] >= int(params["difficulty"])}


def _psionics(sheet: Mapping[str, Any], params: Mapping[str, Any],
              rng: random.Random) -> dict:
    block = sheet["psionics"]
    psychic = psionics.Psychic(
        wisdom=int(sheet["attributes"]["WIS"]),
        constitution=int(sheet["attributes"]["CON"]),
        disciplines=dict(block["disciplines"]),
        permissions=set(block["packages"]),
    )
    technique = str(params["technique"])
    gated = psionics.may_use(block["disciplines"], technique)
    result: dict[str, Any] = {"capacity": psychic.capacity, "technique": technique,
                              "gated": gated, "committed": False}
    if not gated:
        return result
    psychic.use_technique(str(params["key"]), technique)
    result.update({"committed": True, "free_after": psychic.free,
                   "duration": psionics.effort_duration(technique)})
    psychic.end_scene()
    result["free_next_scene"] = psychic.free
    return result


def _attack_with_trauma(sheet: Mapping[str, Any], params: Mapping[str, Any],
                        rng: random.Random) -> dict:
    weapon_row = cwn_equipment.weapon(str(params["weapon"]))
    profile = cwn_equipment.damage_profile(weapon_row["id"])
    attacker = params["attacker"]
    roll = cwn_combat.attack_roll(
        attribute_score=int(attacker["attribute_score"]),
        skill_level=int(attacker["skill"]),
        attack_bonus=int(attacker["attack_bonus"]),
        armor_class=int(params["target_ranged_ac"]),
        rng=rng,
    )
    save = cwn_core.saving_throw("Physical", level=int(sheet["level"]),
                                 attributes=_named_attributes(sheet), rng=rng)
    return {"attack_total": roll.total, "armor_class": roll.armor_class, "hit": roll.hit,
            "target_physical_save": save.total, "save_target": save.target,
            "save_success": save.success,
            "weapon_damage": profile["damage_count"], "trauma_die": profile["trauma_die"],
            "trauma_rating": profile["trauma_rating"]}


def _chase(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    fleeing = params["fleeing"]
    fleeing_check = wn_core.skill_check(
        attribute_score=int(fleeing["attribute_score"]), skill_level=int(fleeing["skill"]),
        difficulty=0, rng=rng,
    )
    modifier = cwn_vehicles.vehicle_chase_modifier(**params["modifiers"])
    pursuer = params["pursuer"]
    pursuer_check = wn_core.skill_check(
        attribute_score=int(pursuer["attribute_score"]), skill_level=int(pursuer["skill"]),
        difficulty=0, situational=max(-2, min(2, modifier)), rng=rng,
    )
    hull = cwn_vehicles.fit_out(vehicle_id=sheet["vehicle"]["hull"], fittings=sheet["vehicle"]["fittings"], mods=sheet["vehicle"]["mods"])
    outcome = cwn_vehicles.resolve_chase(fleeing_check.total, [pursuer_check.total])
    return {"fleeing_pace": fleeing_check.total, "pursuer_total": pursuer_check.total,
            "modifier": modifier, "escaped": outcome.escaped,
            "hull_hit_points": hull.hit_points, "hull_armor": hull.armor,
            "moving_ac": cwn_vehicles.armor_class_in_combat(
                hull.base.ac, moving=True, driver_drive_skill=int(fleeing["skill"]))}


def _crash(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    hull = cwn_vehicles.fit_out(sheet["vehicle"]["hull"], fittings=sheet["vehicle"]["fittings"],
                                mods=sheet["vehicle"]["mods"])
    taken = cwn_vehicles.damage_to_vehicle(int(params["damage"]), trauma_multiplier=1,
                                           armor=hull.armor)
    physical = cwn_core.saving_throw("Physical", level=int(sheet["level"]),
                                     attributes=_named_attributes(sheet), rng=rng)
    luck = cwn_core.saving_throw("Luck", level=int(sheet["level"]),
                                 attributes=_named_attributes(sheet), rng=rng)
    crash = cwn_vehicles.crash_outcome(physical_save_made=physical.success,
                                       luck_save_made=luck.success)
    return {"damage_after_armor": taken, "destroyed": cwn_vehicles.is_destroyed(
                hull.hit_points - taken),
            "unscathed": crash.unscathed, "mortally_wounded": crash.mortally_wounded,
            "damage_fraction": crash.damage_fraction}


def _gunfire_with_mods(sheet: Mapping[str, Any], params: Mapping[str, Any],
                       rng: random.Random) -> dict:
    profile = cwn_equipment.damage_profile(str(params["weapon"]))
    weapon_mods = cwn_gear_mods.apply_weapon_mods(
        profile, params.get("weapon_mods") or [], connected=bool(params.get("connected")))
    armor_row = cwn_equipment.armor_piece(str(sheet["armor"]))
    armor_mods = cwn_gear_mods.apply_armor_mods(armor_row, sheet.get("armor_mods") or [])
    weapon = cwn_trauma.Weapon(
        damage_die=f"{profile['damage_count']}d{profile['damage_sides']}",
        trauma_rating=int(profile["trauma_rating"]),
        shock=cwn_trauma.Shock(value=int(profile["shock"]),
                               max_ac=int(profile["shock_ac"])) if profile["shock"] else None,
    )
    hit = cwn_trauma.resolve_hit(
        weapon,
        damage_roll=int(params["damage_roll"]) + weapon_mods.damage_bonus,
        attribute_modifier=wn_core.attribute_modifier(int(sheet["attributes"]["DEX"])),
        trauma_die_roll=int(params["trauma_die_roll"]),
        trauma_target=int(armor_mods.trauma_target_modifier) + 12,
        target_melee_ac=int(armor_mods.ac_melee),
        soak=armor_mods.damage_soak,
        current_hit_points=int(sheet["hit_points"]),
    )
    return {"mod_hit_bonus": weapon_mods.hit_bonus,
            "magazine_multiplier": weapon_mods.magazine_multiplier,
            "armor_soak": armor_mods.damage_soak,
            "total_damage": hit.total_damage, "soak_absorbed": hit.soak_absorbed,
            "damage_to_hit_points": hit.damage_to_hit_points,
            "traumatic": hit.traumatic, "major_injury_risk": hit.major_injury_risk}


def _zero_hp(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    outcome = cwn_injury_procedure.resolve_zero_hit_points(
        hit_points_after=int(sheet["hit_points"]) - int(params["damage_taken"]),
        traumatic_in_fight=bool(params["traumatic_in_fight"]),
        lethal=True,
        level=int(sheet["level"]),
        attributes=_named_attributes(sheet),
        save_die=rng.randint(1, 20),
        injury_roll=rng.randint(1, 12),
    )
    injury = outcome.injury
    detail: dict[str, Any] | None = None
    if injury is not None:
        detail = {"roll": injury.roll, "label": injury.label, "fatal": injury.fatal,
                  "coma": injury.coma, "needs_prosthetic": injury.needs_prosthetic}
    return {"mortally_wounded": outcome.mortally_wounded,
            "risked_major_injury": outcome.risked_major_injury,
            "save_success": None if outcome.save is None else outcome.save.success,
            "injury": detail}


def _stabilise(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    difficulty = cwn_healing.stabilize_difficulty(int(params["rounds_since_downed"]),
                                                  has_medkit=bool(params["has_medkit"]))
    check = wn_core.skill_check(
        attribute_score=int(sheet["attributes"]["INT"]),
        skill_level=sheet["skills"].get("Heal"),
        difficulty=difficulty, rng=rng,
    )
    patient = cwn_healing.Patient(hit_points=0, level_or_hit_dice=int(sheet["level"]),
                                  downed_round=1)
    result = {"difficulty": difficulty, "check_total": check.total, "success": check.success,
              "rounds_until_death": patient.rounds_until_death(int(params["rounds_since_downed"]) + 1)}
    if check.success:
        revived = cwn_healing.stabilized(patient)
        result.update({"hit_points_after": revived.hit_points, "frail": revived.frail})
    return result


def _strain(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    strain = cwn_strain.SystemStrain(constitution=int(sheet["attributes"]["CON"]),
                                     permanent=float(sheet["cyberware_strain"]))
    before = strain.available
    accepted = strain.absorb(float(params["implant_strain"]))
    shed = 0.0
    for _ in range(int(params["nights"])):
        shed += strain.rest_night()
    return {"maximum": strain.maximum, "accepted_implant": accepted,
            "available_before_rest": before, "shed_after_rest": shed,
            "total_after_rest": strain.total}


def _load(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    load = cwn_encumbrance.Load(stowed=float(params["stowed"]), readied=float(params["readied"]))
    strength = int(sheet["attributes"]["STR"])
    return {"tier": cwn_encumbrance.tier_for(strength, load),
            "stowed_capacity": cwn_encumbrance.stowed_capacity(strength),
            "readied_capacity": cwn_encumbrance.readied_capacity(strength),
            "move_metres": cwn_encumbrance.move_speed(strength, load),
            "can_haul": cwn_encumbrance.can_haul(strength, load)}


def _drone(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    from . import cwn_drones

    drone = cwn_drones.DRONES[str(sheet["drone"]).capitalize()]
    distance = float(params["distance_m"])
    return {"drone": drone.name, "ac": drone.armor_class, "hit_points": drone.hit_points,
            "portable": drone.portable, "mount_class": cwn_drones.mount_class(drone),
            "range_status": cwn_drones.range_status(distance),
            "control_penalty": cwn_drones.control_penalty(
                cast(Any, params["controller"]), cranial_jack=bool(params.get("cranial_jack"))),
            "capacity": cwn_drones.command_capacity(cast(Any, params["controller"]), drive_skill=1)}


def _rain_watch(sheet: Mapping[str, Any], params: Mapping[str, Any],
                rng: random.Random) -> dict:
    hours = awn_survival.travel_hours(str(params["terrain"]), mode=cast(Any, params["mode"]),
                                     road=bool(params["road"]))
    result = awn_survival.apply_privation(int(params["current_strain"]),
                                          cwn_strain.SystemStrain(
                                              constitution=int(sheet["attributes"]["CON"])).maximum,
                                          cast(Any, params["privation"]))
    forage = awn_survival.forage(
        check_total=rng.randint(2, 12) + wn_core.attribute_modifier(int(sheet["attributes"]["WIS"])),
        difficulty=int(params["forage_difficulty"]),
        survive_levels=int(params["survive_levels"]), rng=rng,
    )
    return {"hex_hours": hours, "hexes_per_day": awn_survival.hexes_per_day(
                str(params["terrain"]), mode=cast(Any, params["mode"]), road=bool(params["road"])),
            "strain_gained": result.gained, "strain_total": result.current_strain,
            "needs_physical_save": result.needs_physical_save,
            "recovery_blocked": result.recovery_blocked,
            "forage_success": forage.success, "forage_units": forage.units,
            "astray_difficulty": awn_survival.going_astray_difficulty(str(params["terrain"]))}


def _project(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    difficulty = wwn_projects.project_difficulty(
        cast(Any, params["probability"]), cast(Any, params["scope"]),
        cast(Any, params["opposition"]),
        disapproval=bool(params["disapproval"]),
    )
    state = wwn_projects.ProjectState(difficulty=difficulty)
    spent = state.advance(int(params["renown_spent"]))
    return {"difficulty": difficulty, "remaining": spent.remaining,
            "complete": spent.complete,
            "adventure_share": wwn_projects.adventure_share(difficulty, adventures_planned=3),
            "allied_share": wwn_projects.allied_faction_share(difficulty),
            "money_ladder_modelled": wwn_projects.money_purchase_is_modelled()}


def _advancement(sheet: Mapping[str, Any], params: Mapping[str, Any],
                 rng: random.Random) -> dict:
    level = cwn_advancement.level_for_xp(int(params["xp"]))
    return {"xp": int(params["xp"]), "level": level,
            "attack_bonus": cwn_advancement.attack_bonus(level),
            "save_target": cwn_advancement.save_target(level),
            "skill_point_cost_rank_1": cwn_advancement.skill_point_cost(1),
            "next_level_xp": cwn_advancement.xp_for_next_level(level)}


def _modding(sheet: Mapping[str, Any], params: Mapping[str, Any], rng: random.Random) -> dict:
    profile = cwn_equipment.damage_profile("light_pistol")
    weapon_mods = cwn_gear_mods.apply_weapon_mods(profile, params["weapon_mods"], connected=True)
    armor_row = cwn_equipment.armor_piece(str(sheet["armor"]))
    armor_mods = cwn_gear_mods.apply_armor_mods(armor_row, params["armor_mods"])
    score = cwn_gear_mods.maintenance_score(int(params["int_modifier"]),
                                            int(params["con_modifier"]),
                                            int(params["fix_skill"]))
    return {"weapon_hit_bonus": weapon_mods.hit_bonus,
            "weapon_magazine_multiplier": weapon_mods.magazine_multiplier,
            "armor_readied_bonus": armor_mods.readied_bonus,
            "armor_stowed_bonus": armor_mods.stowed_bonus,
            "armor_encumbrance": armor_mods.encumbrance,
            "maintenance_score": score,
            "install_weeks_customized": cwn_gear_mods.install_weeks(
                cwn_gear_mods.weapon_mod("customized"))}


HANDLERS: Mapping[str, Callable[[Mapping[str, Any], Mapping[str, Any], random.Random], dict]] = {
    "briefing_notice": _skill,
    "ward_terminal": _ward_terminal,
    "doctor_opposed": _opposed,
    "mirror_effort": _psionics,
    "stair_ambush": _attack_with_trauma,
    "roof_chase": _chase,
    "crash_landing": _crash,
    "gunfire_with_mods": _gunfire_with_mods,
    "zero_hp": _zero_hp,
    "stabilise": _stabilise,
    "strain_night": _strain,
    "kit_load": _load,
    "drone_recon": _drone,
    "rain_watch": _rain_watch,
    "referral_project": _project,
    "advancement": _advancement,
    "modding_kit": _modding,
}


def run_drill(path: str | Path | None = None, *, seed: int | None = None) -> DrillResult:
    """Execute every beat in order against one seed and return the log.

    Determinism is the point: the same seed reproduces the same log exactly, so a
    failing beat is a reproducible bug rather than a bad night's dice.
    """
    script = load_drill(path)
    run_seed = int(script["seed"] if seed is None else seed)
    rng = random.Random(run_seed)
    sheet = script["sheet"]
    results: list[BeatResult] = []
    for beat in script["beats"]:
        handler = HANDLERS.get(str(beat["id"]))
        if handler is None:
            raise DrillError(f"no handler for beat {beat['id']!r}")
        outcome = handler(sheet, beat.get("params") or {}, rng)
        results.append(BeatResult(id=str(beat["id"]), where=str(beat.get("where", "")),
                                  tags=tuple(beat.get("tags") or ()), outcome=outcome))
    return DrillResult(seed=run_seed, beats=tuple(results), sheet=sheet)


__all__ = [
    "DRILL_PATH",
    "HANDLERS",
    "BeatResult",
    "DrillError",
    "DrillResult",
    "load_drill",
    "run_drill",
]
