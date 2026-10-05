class_name NooPunkCoreRules
extends RefCounted

## Godot adapter over data/rules/core.json.
## Canonical core: STAT + Skill + 1d10 vs DV (#111).

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

func skill_range() -> Array[int]:
    return [int(canon["skills"]["min"]), int(canon["skills"]["max"])]

func roll_d10(rng: RandomNumberGenerator) -> int:
    return rng.randi_range(1, 10)

func difficulty_target(name: String) -> int:
    for key in canon["difficulties"].keys():
        if str(canon["difficulties"][key]) == name:
            return int(key)
    push_error("Unknown authored difficulty: " + name)
    return -1

func resolve_check(
    rng: RandomNumberGenerator,
    stat: int,
    skill: int,
    target: int,
    die_override: Variant = null
) -> Dictionary:
    var sr := stat_range()
    var kr := skill_range()
    assert(stat >= sr[0] and stat <= sr[1], "STAT must be 1..10.")
    assert(skill >= kr[0] and skill <= kr[1], "Skill must be 1..10.")
    var die := roll_d10(rng) if die_override == null else int(die_override)
    assert(die >= 1 and die <= 10, "A 1d10 roll must be 1..10.")
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
