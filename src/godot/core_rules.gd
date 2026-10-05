class_name NooPunkCoreRules
extends RefCounted

## Godot adapter over the shared independent NoöPunk rules.
## Canonical resolution: STAT + Skill + 1d10 vs Difficulty Value.

const CANON_PATH := "res://data/rules/core.json"

var canon: Dictionary

func _init() -> void:
    var file := FileAccess.open(CANON_PATH, FileAccess.READ)
    if file == null:
        push_error("Cannot open canonical NoöPunk rule data.")
        canon = {}
        return
    canon = JSON.parse_string(file.get_as_text())

func stat_range() -> Array[int]:
    return [int(canon["stats"]["min"]), int(canon["stats"]["max"])]

func skill_level_range() -> Array[int]:
    return [int(canon["skills"]["min"]), int(canon["skills"]["max"])]

func roll_d10(rng: RandomNumberGenerator) -> int:
    return rng.randi_range(1, 10)

func difficulty_names() -> Array[String]:
    var names: Array[String] = []
    for name in canon.get("difficulties", {}).values():
        names.append(str(name))
    return names

func difficulty_ladder() -> Array[int]:
    var ladder: Array[int] = []
    for key in canon.get("difficulties", {}).keys():
        ladder.append(int(key))
    ladder.sort()
    return ladder

func resolve_check(
    rng: RandomNumberGenerator,
    stat: int,
    skill: int,
    target: int,
    die_override: Variant = null
) -> Dictionary:
    var stat_bounds := stat_range()
    var skill_bounds := skill_level_range()
    assert(stat >= stat_bounds[0] and stat <= stat_bounds[1], "STAT must be 1..10.")
    assert(skill >= skill_bounds[0] and skill <= skill_bounds[1], "Skill must be 1..10.")

    var die := roll_d10(rng)
    if die_override != null:
        die = int(die_override)
        assert(die >= 1 and die <= 10, "A 1d10 check roll must be in 1..10.")

    var total := stat + skill + die
    return {
        "stat": stat,
        "skill": skill,
        "die": die,
        "target": target,
        "total": total,
        "success": total >= target
    }

func compare_opposed(left_total: int, right_total: int) -> Dictionary:
    if left_total > right_total:
        return {"winner": "left", "unresolved_tie": false}
    if right_total > left_total:
        return {"winner": "right", "unresolved_tie": false}
    return {"winner": null, "unresolved_tie": true}
