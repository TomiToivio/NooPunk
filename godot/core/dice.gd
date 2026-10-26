## Deterministic dice for the NoöPunk Godot slice (#631).
##
## A seeded RandomNumberGenerator, wrapped so that every roll in the game can be replayed from a
## single number. Tests depend on this: the same seed and the same sequence of calls must produce the
## same results on every platform, so nothing here uses global randomness.
class_name NoopunkDice
extends RefCounted

var _rng := RandomNumberGenerator.new()
var seed_value: int = 1
## How many dice this stream has produced. Saved with the case so that a reload resumes the stream
## instead of replaying it from the first roll (which would let a player reroll a bad check by saving).
var rolls_made: int = 0

func _init(initial_seed: int = 1) -> void:
	seed_value = initial_seed
	_rng.seed = initial_seed

func roll(sides: int) -> int:
	if sides < 2:
		push_error("NoopunkDice.roll: a die needs at least two sides, got %d" % sides)
		return 1
	rolls_made += 1
	return _rng.randi_range(1, sides)

## Rolls `count` dice and returns them in order, so a caller can show the actual faces.
func pool(count: int, sides: int) -> Array:
	var faces: Array = []
	for i in count:
		faces.append(roll(sides))
	return faces

## Resets the stream to its first roll.
func reseed(new_seed: int) -> void:
	seed_value = new_seed
	_rng.seed = new_seed
	rolls_made = 0

## The save record for the stream: the seed and how far it has been consumed.
func snapshot() -> Dictionary:
	return { "seed": seed_value, "rolls": rolls_made }

## Rebuilds the stream at the position it had when the case was saved.
##
## `RandomNumberGenerator` exposes no state, so the position is reproduced by making the same number
## of draws. `randi_range` consumes one value per call whatever its bounds, so the replay only has to
## call it the same number of times.
func restore(initial_seed: int, rolls: int) -> void:
	seed_value = initial_seed
	_rng.seed = initial_seed
	rolls_made = 0
	for _i in maxi(0, rolls):
		_rng.randi_range(1, 6)
	rolls_made = maxi(0, rolls)
