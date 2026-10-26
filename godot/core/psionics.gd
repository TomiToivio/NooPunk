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

func _init(wis: int = 10, con: int = 10, skills: Dictionary = {}, packages: Array = []) -> void:
    super(wis, con, skills)
    permissions = packages.duplicate()

func authorized() -> bool:
    for package in permissions:
        if package in PACKAGES:
            return true
    return false

func commit(key: String, discipline: String, rank: int = 0, duration: String = "scene", amount: int = 1) -> bool:
    if not authorized():
        return false
    return super.commit(key, discipline, rank, duration, amount)

func use_technique(key: String, technique_id: String, duration: String = "scene") -> bool:
    if not TECHNIQUES.has(technique_id):
        return false
    var technique: Dictionary = TECHNIQUES[technique_id]
    return commit(key, String(technique["discipline"]), int(technique["rank"]), duration)

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
