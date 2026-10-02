class_name NooPunkCoreRules
extends RefCounted

## Godot adapter over the shared NoöPunk canon.
##
## The authored numeric values live in `res://data/rules/core.json`, the same file
## the Python runtime reads, so Godot cannot drift from canon by re-declaring
## tables. RULEBOOK.md is the source of truth above both (AGENTS.md §13: a rules
## difference between runtimes is a defect).
##
## The skill-check engine is 2d6 + skill level + attribute modifier against
## 6/8/10/12/14+ (RULEBOOK §4). The earlier 3d6 skill-check engine and its
## 3/6/9/12/15/18 ladder are withdrawn. Attribute *generation* is still 3d6 per
## attribute (§5.2) — that is the generation roll, not the check engine.

const CANON_PATH := "res://data/rules/core.json"

var canon: Dictionary

func _init() -> void:
    var file := FileAccess.open(CANON_PATH, FileAccess.READ)
    if file == null:
        push_error("Cannot open canonical NoöPunk rule data.")
        canon = {}
        return
    canon = JSON.parse_string(file.get_as_text())

func attribute_ids() -> Array[String]:
    var ids: Array[String] = []
    for item in canon.get("attributes", []):
        ids.append(str(item["id"]))
    return ids

func empty_attributes(value: int = 0) -> Dictionary:
    var attributes := {}
    for attribute_id in attribute_ids():
        attributes[attribute_id] = value
    return attributes

func human_modifier(raw_3d6: int) -> int:
    ## Map a 3d6 attribute *generation* roll to its modifier (RULEBOOK §5.2).
    if raw_3d6 < 3 or raw_3d6 > 18:
        push_error("Human attribute generation requires a 3d6 total in 3..18.")
        return 0
    return int(canon["human_3d6_generation"]["modifier_table"][str(raw_3d6)])

func roll_3d6(rng: RandomNumberGenerator) -> int:
    return rng.randi_range(1, 6) + rng.randi_range(1, 6) + rng.randi_range(1, 6)

func roll_2d6(rng: RandomNumberGenerator) -> int:
    ## The skill-check dice. The LLM/runtime never substitutes its own roll.
    return rng.randi_range(1, 6) + rng.randi_range(1, 6)

func check_dice_count() -> int:
    return int(canon["skill_check"]["dice_count"])

func check_dice_sides() -> int:
    return int(canon["skill_check"]["dice_sides"])

func min_check_roll() -> int:
    return check_dice_count()

func max_check_roll() -> int:
    return check_dice_count() * check_dice_sides()

func skill_level_range() -> Array[int]:
    return [int(canon["skill_levels"]["min"]), int(canon["skill_levels"]["max"])]

func generate_human_attributes(rng: RandomNumberGenerator) -> Dictionary:
    var raw := {}
    var modifiers := {}
    for attribute_id in attribute_ids():
        var rolled := roll_3d6(rng)
        raw[attribute_id] = rolled
        modifiers[attribute_id] = human_modifier(rolled)
    return {"raw_rolls": raw, "modifiers": modifiers}

func difficulty_names() -> Array[String]:
    var names: Array[String] = []
    for name in canon.get("difficulties", {}).keys():
        names.append(str(name))
    return names

func difficulty_target(name: String) -> int:
    return int(canon["difficulties"][name])

func difficulty_ladder() -> Array[int]:
    var ladder: Array[int] = []
    for name in difficulty_names():
        ladder.append(difficulty_target(name))
    ladder.sort()
    return ladder

func resolve_check(
    rng: RandomNumberGenerator,
    attribute_modifier: int,
    target: int,
    extra_modifiers: Array[int] = [],
    has_skill: bool = true,
    trained_only: bool = false,
    skill_level: int = 0,
    dice_total_override: Variant = null,
    aid_bonus: int = 0
) -> Dictionary:
    ## Resolve one skill check: 2d6 + skill level + attribute modifier vs difficulty.
    ##
    ## `dice_total_override` exists for deterministic callers (replay, tests), never
    ## for LLM output. A blocked trained-only attempt rolls no dice and returns
    ## success = null, so "blocked" cannot be mistaken for "failed" (RULEBOOK §4.2).
    if trained_only and not has_skill:
        return {
            "attempted": false,
            "success": null,
            "total": null,
            "dice_total": null,
            "blocked_reason": "trained_only_without_skill"
        }

    var level := 0
    if has_skill:
        var bounds := skill_level_range()
        level = skill_level
        if level < bounds[0] or level > bounds[1]:
            push_error("Skill level must be %d..%d; unskilled is has_skill=false, not level 0." % [bounds[0], bounds[1]])
            return {"attempted": false, "success": null, "total": null, "dice_total": null, "blocked_reason": "invalid_skill_level"}

    var unskilled_modifier := 0
    if not has_skill:
        unskilled_modifier = int(canon["unskilled_penalty"])

    var dice_total := roll_2d6(rng)
    if dice_total_override != null:
        dice_total = int(dice_total_override)
        assert(dice_total >= min_check_roll() and dice_total <= max_check_roll(),
            "A 2d6 check roll must be in %d..%d." % [min_check_roll(), max_check_roll()])

    var extras_total := 0
    for modifier in extra_modifiers:
        extras_total += modifier
    var capped_aid := min(aid_bonus, int(canon["aiding"]["cap"]))
    var total := dice_total + level + attribute_modifier + extras_total + unskilled_modifier + capped_aid

    return {
        "attempted": true,
        "dice_total": dice_total,
        "attribute_modifier": attribute_modifier,
        "skill_level": level,
        "extra_modifiers": extra_modifiers.duplicate(),
        "unskilled_modifier": unskilled_modifier,
        "aid_bonus": capped_aid,
        "target": target,
        "total": total,
        "success": total >= target
    }

func compare_opposed(
    left_total: int,
    right_total: int,
    left_is_player_character: bool = false,
    right_is_player_character: bool = false
) -> Dictionary:
    ## RULEBOOK §4.1: higher total wins; on a tie a player character wins.
    ## A tie with no player character involved is deliberately left unresolved —
    ## the rulebook defines the PC tie and declines to define a general one.
    if left_total > right_total:
        return {"winner": "left", "unresolved_tie": false, "decided_by": "higher_total"}
    if right_total > left_total:
        return {"winner": "right", "unresolved_tie": false, "decided_by": "higher_total"}
    if left_is_player_character and not right_is_player_character:
        return {"winner": "left", "unresolved_tie": false, "decided_by": "player_character_tie"}
    if right_is_player_character and not left_is_player_character:
        return {"winner": "right", "unresolved_tie": false, "decided_by": "player_character_tie"}
    return {"winner": null, "unresolved_tie": true, "decided_by": "unresolved_tie"}
