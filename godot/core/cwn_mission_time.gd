## Cities Without Number — scenes, rounds and mission time.
##
## Transcribed from the SRD (CC0), ``rules-of-the-game/scenes-rounds-mission-time``.
##
## The three clocks the rules depend on:
##
## * **round** — about six seconds of combat
## * **scene** — one fight, chase or tense activity, "usually doesn't take more than ten or fifteen
##   minutes"; during mission time a scene refreshes after every fight or every ten minutes
## * **mission time** — minutes from minute zero, one per standard action, the clock that drives
##   patrol discovery and escalating security response
##
## Per-scene abilities in the rule system need one authority for "has the scene refreshed", so this
## object owns it rather than each ability counting for itself.
extends RefCounted
class_name CwnMissionTime

const ROUND_SECONDS := 6
const SCENE_MINUTES := 10
const STANDARD_ACTION_MINUTES := 1

var minute: int = 0
var scene: int = 0

var _scene_start_minute: int = 0


## Advance the mission clock and report what crossed during the jump.
##
## A long action may span several scenes; `scenes_elapsed` is how many of them the jump crossed, so a
## caller can expire per-scene abilities the right number of times.
func advance(minutes: int = STANDARD_ACTION_MINUTES) -> Dictionary:
	if minutes < 0:
		return {"ok": false, "reason": "mission time does not run backwards"}
	var before := scene
	minute += minutes
	scene = floori(float(minute) / float(SCENE_MINUTES))
	return {
		"ok": true,
		"minute": minute,
		"scene": scene,
		"scenes_elapsed": scene - before,
		"scene_refreshed": scene > before,
	}


## Spend a standard action (one minute) and report whether it started a new scene.
func spend_action(minutes: int = STANDARD_ACTION_MINUTES) -> Dictionary:
	return advance(minutes)


func minutes_into_scene() -> int:
	return minute - scene * SCENE_MINUTES


## How many combat rounds fit in one scene: six-second rounds against the ten-minute refresh.
static func rounds_in_a_scene() -> int:
	return (SCENE_MINUTES * 60) / ROUND_SECONDS


## Convert a number of rounds into mission minutes, for a fight that happened inside mission time.
static func rounds_to_minutes(rounds: int) -> float:
	return float(rounds * ROUND_SECONDS) / 60.0


## Rounds that fit in the given number of mission minutes, rounded down.
static func rounds_in_minutes(minutes: int) -> int:
	return (minutes * 60) / ROUND_SECONDS
