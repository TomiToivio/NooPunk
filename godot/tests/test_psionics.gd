## Psionics in the engine: the catalogue, the Effort pool, the training gate and torching.
##
## The mirror of `tests/test_swn_psionics.py`. Both runtimes read the same authored catalogue, so a
## technique that exists at the table exists in the game.
extends RefCounted

func run() -> Array:
	var rows: Array = []
	var psi := NoopunkPsionics.new()
	rows.append_array(_catalogue_rows(psi))
	rows.append_array(_effort_rows(psi))
	rows.append_array(_gate_rows(psi))
	rows.append_array(_torch_rows(psi))
	return rows

func _catalogue_rows(psi: NoopunkPsionics) -> Array:
	var rows: Array = []
	rows.append(_eq("six psionic disciplines", psi.disciplines().size(), 6))
	rows.append(_check("every discipline has a core technique", _core_count(psi) == 6))
	rows.append(_check("the catalogue holds at least eighteen techniques", psi.technique_count() >= 18))
	rows.append(_check("an unknown technique resolves to nothing", psi.technique("no_such_power").is_empty()))

	var legal := true
	for entry in (psi.catalogue.get("techniques", []) as Array):
		if not psi.disciplines().has(String(entry.get("discipline", ""))):
			legal = false
		if int(entry.get("min_skill", 0)) < 1 or int(entry.get("min_skill", 0)) > 4:
			legal = false
		if String(entry.get("effect", "")).strip_edges() == "":
			legal = false
	rows.append(_check("every technique names a discipline, a legal gate and an effect", legal))
	return rows

func _core_count(psi: NoopunkPsionics) -> int:
	var count := 0
	for discipline in psi.disciplines():
		if not psi.core_for(String(discipline)).is_empty():
			count += 1
	return count

func _effort_rows(psi: NoopunkPsionics) -> Array:
	var rows: Array = []
	var attributes := {"WIS": 14, "CON": 10}
	rows.append(_eq("max Effort is 1 + better modifier + best skill", psi.max_effort(attributes, {"Telepathy": 1}), 3))
	rows.append(_eq("without a psionic skill the term is zero", psi.max_effort(attributes, {}), 2))
	rows.append(_eq("an untrained discipline does not reduce the pool",
		psi.max_effort(attributes, {"Telepathy": -1}), 2))

	# The commitment lifecycle: named keys, no early refunds for scene/day, recovery on scene end.
	var pool := NoopunkPsionics.EffortPool.new(3)
	rows.append(_eq("active commitment accepted", pool.commit("contact", "active"), true))
	rows.append(_eq("scene commitment accepted", pool.commit("reading", "scene"), true))
	rows.append(_eq("day commitment accepted", pool.commit("vision", "day"), true))
	rows.append(_eq("zero Effort left", pool.available(), 0))
	rows.append(_eq("cannot commit beyond the pool", pool.commit("extra", "scene"), false))
	rows.append(_eq("cannot release a day commitment early", pool.release("vision"), false))
	rows.append(_eq("can release an active commitment", pool.release("contact"), true))
	rows.append(_eq("released Effort returns", pool.available(), 1))
	rows.append(_eq("duplicate key refused", pool.commit("reading", "scene"), false))
	pool.end_scene()
	rows.append(_eq("scene recovery leaves the day reserve", pool.available(), 2))
	pool.rest()
	rows.append(_eq("a night's rest returns everything", pool.available(), 3))

	# Persistence: a save must not silently reset the pool.
	pool.commit("oracle", "day")
	var saved := pool.snapshot()
	var restored := NoopunkPsionics.EffortPool.new()
	rows.append(_eq("an Effort snapshot restores", restored.restore(saved), true))
	rows.append(_eq("restored Effort matches", restored.available(), pool.available()))
	rows.append(_eq("a malformed snapshot is refused",
		NoopunkPsionics.EffortPool.new().restore({"maximum": 1, "reservations": {"bad": {"amount": 1, "duration": "hour"}}}), false))
	return rows

func _gate_rows(psi: NoopunkPsionics) -> Array:
	var rows: Array = []
	var core := psi.technique("surface_read")
	var learned := psi.technique("thread")
	rows.append(_eq("Surface Read is a Telepathy core", String(core.get("discipline", "")), "Telepathy"))
	rows.append(_eq("Thread needs Telepathy-1 or better", int(learned.get("min_skill", 0)), 1))

	var pool := NoopunkPsionics.EffortPool.new(3)
	var untrained: Dictionary = psi.use("thread", {"Telepathy": 0}, pool)
	rows.append(_check("an untaught technique is refused as a permission failure",
		not bool(untrained.get("ok", true)) and String(untrained.get("reason", "")).contains("never trained")))
	rows.append(_eq("a refused use commits nothing", pool.committed(), 0))

	var taught: Dictionary = psi.use("thread", {"Telepathy": 1}, pool)
	rows.append(_check("a trained character can use the technique", bool(taught.get("ok", false))))
	rows.append(_eq("using Thread commits one scene Effort", pool.committed_scene(), 1))
	psi.use("thread", {"Telepathy": 1}, pool)
	rows.append(_eq("the same power can be held twice", pool.reservations.size(), 2))

	var core_use: Dictionary = psi.use("surface_read", {"Telepathy": 0}, pool)
	rows.append(_check("a core technique commits nothing", bool(core_use.get("ok", false)) and String(core_use.get("committed", "")) == "none"))
	rows.append(_eq("effort cost maps to its duration", psi.effort_duration(psi.technique("command")), "day"))
	return rows

func _torch_rows(psi: NoopunkPsionics) -> Array:
	var rows: Array = []
	var attributes := {"WIS": 14, "CON": 10}
	var pool := NoopunkPsionics.EffortPool.new(1)
	pool.commit("scene")
	rows.append(_eq("a spent pool has nothing left", pool.available(), 0))
	pool.torched += 1
	rows.append(_eq("torching adds a point above the maximum", pool.available(), 1))

	var burned: Dictionary = psi.torch(1, attributes)
	rows.append(_eq("a 1 on the torching die costs Wisdom", String(burned.get("harm", "")), "lose_1_wisdom"))
	rows.append(_eq("and the attribute actually falls", int(attributes["WIS"]), 13))

	var harmless: Dictionary = psi.torch(6, attributes)
	rows.append(_check("a 6 does no harm", String(harmless.get("harm", "")) == "no_harm" and not bool(harmless.get("feral", true))))

	var fragile := {"WIS": 4, "CON": 10}
	psi.torch(1, fragile)
	var feral: Dictionary = psi.torch(1, fragile)
	rows.append(_check("a psychic below Wisdom 3 is feral", bool(feral.get("feral", false))))
	return rows

func _eq(label: String, actual: Variant, expected: Variant) -> Array:
	return [label, actual == expected, "expected %s, got %s" % [str(expected), str(actual)]]

func _check(label: String, ok: bool, detail: String = "") -> Array:
	return [label, ok, detail]
