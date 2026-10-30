## Executable parity regression for the two currently-live CWN Strain APIs.
## Remove one implementation only after its callers migrate.
extends RefCounted

const Primary := preload("res://godot/core/cwn_strain.gd")
const Compatibility := preload("res://src/godot/cwn/cwn_strain.gd")

func _check(label: String, passed: bool) -> Array:
	return [label, passed, "CWN Strain diverged" if not passed else ""]

func run() -> Array:
	var rows: Array = []
	var a := Primary.new(10, 2.0, 1.0)
	var b := Compatibility.new(10, 2.0, 1.0)
	rows.append(_check("strain initial state matches", a.to_dict() == b.to_dict()))
	rows.append(_check("cyberware install result matches", a.install_cyber(3.5) == b.install_cyber(3.5)))
	rows.append(_check("cyberware install accounting matches", a.to_dict() == b.to_dict()))
	rows.append(_check("overflow refusal matches", a.absorb(20.0) == b.absorb(20.0)))
	rows.append(_check("forced overflow result matches", a.absorb(20.0, true) == b.absorb(20.0, true)))
	rows.append(_check("forced overflow accounting matches", a.to_dict() == b.to_dict()))
	var snapshot: Dictionary = a.to_dict()
	var restored := Compatibility.from_dict(snapshot)
	rows.append(_check("compatibility snapshot retains unconsciousness", restored.to_dict() == snapshot))
	var c := Primary.new(10)
	c.from_dict(snapshot)
	rows.append(_check("primary snapshot retains unconsciousness", c.to_dict() == snapshot))
	rows.append(_check("negative install refused by primary", not a.install_cyber(-1.0)))
	a.remove_cyber(1.0)
	b.remove_cyber(1.0)
	rows.append(_check("permanent strain state matches", a.to_dict() == b.to_dict()))
	rows.append(_check("night rest result matches", a.rest_night() == b.rest_night()))
	rows.append(_check("night rest clears unconsciousness equally", a.to_dict() == b.to_dict()))
	return rows
