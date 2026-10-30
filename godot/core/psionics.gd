## #652: SWN-inspired psychic Effort with package authorization.
## Original NoöPunk scenario techniques. No source-book power descriptions.
class_name NoopunkPsionics
extends "res://godot/core/psychic_effort.gd"

const PACKAGES := ["swn_psychic", "swn_partial_psychic"]
const TECHNIQUES := {
    "surface_read": {"discipline": "Telepathy", "rank": 0},
    "empathic_trace": {"discipline": "Telepathy", "rank": 1},
    "premonition": {"discipline": "Precognition", "rank": 0},
}

var permissions: Array = []

const CATALOGUE_PATH := "res://data/rules/psionics_techniques.json"

var catalogue: Dictionary = {}

## `restricted_to` names the single discipline a Partial Psychic package grants. Empty is
## unrestricted, which is what the Psychic package is.
func _init(wis: int = 10, con: int = 10, skills: Dictionary = {}, packages: Array = [],
        restricted_to: String = "") -> void:
    super(wis, con, skills)
    permissions = packages.duplicate()
    restricted_discipline = restricted_to
    if FileAccess.file_exists(CATALOGUE_PATH):
        var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(CATALOGUE_PATH))
        if typeof(parsed) == TYPE_DICTIONARY:
            catalogue = parsed

func authorized() -> bool:
    for package in permissions:
        if package in PACKAGES:
            return true
    return false

func commit(key: String, discipline: String, rank: int = 0, duration: String = "scene", amount: int = 1) -> bool:
    if not authorized():
        return false
    # The package decides *which* disciplines may be studied; the rank gate then decides whether
    # this particular technique has been taught.
    if not can_learn_raw(discipline):
        return false
    return super.commit(key, discipline, rank, duration, amount)

## `can_learn` is inherited, but a package-restricted psychic whose restriction was not supplied
## defaults to the discipline they already rate highest — the one the sheet shows them training.
func can_learn_raw(discipline: String) -> bool:
    if restricted_discipline.is_empty() and "swn_partial_psychic" in permissions \
            and not ("swn_psychic" in permissions):
        restricted_discipline = _highest_ranked_discipline()
    return can_learn(discipline)

func _highest_ranked_discipline() -> String:
    var best := ""
    var best_rank := -1
    for name in ranks.keys():
        if String(name) in DISCIPLINES and int(ranks[name]) > best_rank:
            best = String(name)
            best_rank = int(ranks[name])
    return best

## A technique's catalogue entry, or the authorization map's fallback row. The catalogue is the one
## source of truth for rank, cost and duration; `TECHNIQUES` stays as the package-era fallback so an id
## that predates the catalogue still resolves.
func technique(technique_id: String) -> Dictionary:
    for entry in (catalogue.get("techniques", []) as Array):
        if String(entry.get("id", "")) == technique_id:
            return entry
    for discipline in (catalogue.get("discipline_cores", {}) as Dictionary).keys():
        var core: Dictionary = (catalogue["discipline_cores"] as Dictionary)[discipline]
        if String(core.get("id", "")) == technique_id:
            var resolved: Dictionary = core.duplicate()
            resolved["discipline"] = String(discipline)
            resolved["core"] = true
            return resolved
    if TECHNIQUES.has(technique_id):
        var fallback: Dictionary = TECHNIQUES[technique_id]
        return {"id": technique_id, "discipline": String(fallback["discipline"]),
            "min_skill": int(fallback["rank"]), "effort": "commit_scene"}
    return {}

## What using this technique does to the pool: ``none``, ``scene`` or ``day``.
func effort_duration(entry: Dictionary) -> String:
    return {"commit_scene": "scene", "commit_day": "day"}.get(String(entry.get("effort", "none")), "none")

## Uses a technique: package authorization, then the rank gate, then the Effort the catalogue names.
## A refusal spends nothing.
func use_technique(key: String, technique_id: String, duration: String = "") -> bool:
    var entry := technique(technique_id)
    if entry.is_empty():
        return false
    var resolved := duration
    if resolved.is_empty():
        resolved = effort_duration(entry)
    if resolved == "none":
        # A core technique costs no Effort: only authorization and rank gate it.
        return authorized() and int(ranks.get(String(entry["discipline"]), -1)) >= int(entry.get("min_skill", 0))
    return commit(key, String(entry["discipline"]), int(entry.get("min_skill", 0)), resolved)

## Biopsionics' core technique, scaled by rank. One home for the numbers the discipline's own
## chapter fixes: a rank-0 psychic stabilises, and higher ranks heal increasing dice and bonuses.
## Returns {"ok": false, "reason": ...} rather than a partial result, so a refusal spends nothing.
static func psychic_succor(rank: int, dice: Array, target_hp: int, target_max: int,
        strain: int, constitution: int, mortal: bool) -> Dictionary:
    if rank < 0 or rank > 4 or constitution < 3 or constitution > 18 \
            or target_max < 1 or target_hp < 0 or target_hp > target_max:
        return {"ok": false}
    var added_strain := 2 if mortal else 1
    if strain < 0 or strain + added_strain > constitution:
        return {"ok": false, "reason": "system_strain"}
    var die_count: int = [0, 1, 2, 2, 3][rank]
    var bonus: int = [0, 1, 2, 6, 8][rank]
    if dice.size() != die_count:
        return {"ok": false}
    var healed := bonus
    for die in dice:
        if typeof(die) != TYPE_INT or die < 1 or die > 6:
            return {"ok": false}
        healed += int(die)
    if rank == 0 and not mortal:
        return {"ok": false, "reason": "stabilization_only"}
    var new_hp: int = mini(target_max, healed if mortal else target_hp + healed)
    return {"ok": true, "hp": new_hp, "strain": strain + added_strain,
        "stabilized": mortal, "healed": healed}

## Teleportation's core technique range, by rank. A core technique improves with the skill; it is
## never bought.
## -1 is the book's "planetary / near-orbit" entry, not a distance.
const TELEPORT_METERS := [10.0, 100.0, 10000.0, 1000000.0, -1.0]

static func teleport_range_meters(rank: int) -> float:
    if rank < 0 or rank > 4:
        return 0.0
    return TELEPORT_METERS[rank]

## Activate a known technique by id: package, rank gate and the Effort the catalogue names.
func activate(technique_id: String, key: String, duration: String = "") -> bool:
    return use_technique(key, technique_id, duration)

## Release an active commitment early. Scene and day Effort cannot be refunded.
func release_active(key: String) -> bool:
    return release(key)

func snapshot() -> Dictionary:
    var state: Dictionary = super.snapshot()
    state["permissions"] = permissions.duplicate()
    return state

func restore(saved: Dictionary) -> bool:
    var packages: Array = saved.get("permissions", [])
    var permitted := false
    for package in packages:
        if package in PACKAGES:
            permitted = true
    if not permitted and not saved.get("commitments", {}).is_empty():
        return false
    if not super.restore(saved):
        return false
    permissions = packages.duplicate()
    return true
