## Deterministic dice for the NoöPunk Godot slice (#631).
##
## A seeded RandomNumberGenerator, wrapped so that every roll in the game can be replayed from a
## single number. Tests depend on this: the same seed and the same sequence of calls must produce the
## same results on every platform, so nothing here uses global randomness.
class_name NoopunkDice
extends RefCounted

var _rng := RandomNumberGenerator.new()
var seed_value: int = 1

func _init(initial_seed: int = 1) -> void:
	seed_value = initial_seed
	_rng.seed = initial_seed

func roll(sides: int) -> int:
	if sides < 2:
		push_error("NoopunkDice.roll: a die needs at least two sides, got %d" % sides)
		return 1
	return _rng.randi_range(1, sides)

## Rolls `count` dice and returns them in order, so a caller can show the actual faces.
func pool(count: int, sides: int) -> Array:
	var faces: Array = []
	for i in count:
		faces.append(roll(sides))
	return faces

## Resets the stream. Used by save/load so that a reloaded game continues the same sequence.
func reseed(new_seed: int) -> void:
	seed_value = new_seed
	_rng.seed = new_seed
