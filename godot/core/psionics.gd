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

func _init(wis: int = 10, con: int = 10, skills: Dictionary = {}, packages: Array = []) -> void:
    super(wis, con, skills)
    permissions = packages.duplicate()
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
    return super.commit(key, discipline, rank, duration, amount)

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
