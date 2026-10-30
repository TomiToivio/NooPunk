## Cities Without Number — Contacts (SRD §1.4).
##
## Two levels, and the distinction is not flavour:
##
## * an **acquaintance** will do honest business, perform their professional skill, and take on favors
##   that do not put them at risk or significant expense;
## * a **friend** will also take on favors with considerable risk or significant expense.
##
## Neither will go on a mission with the party, and a contact may be called on **once per session** —
## those two rules are what stop a Contact from becoming a free henchman, so they are properties of the
## model rather than a note in a rulebook.
extends RefCounted
class_name CwnContacts

const LEVELS := {
	"acquaintance": {"risk": false, "significant_expense": false},
	"friend": {"risk": true, "significant_expense": true},
}

##: A new PC starts with either two acquaintances or one friend.
const STARTING_CHOICES := {
	"two_acquaintances": ["acquaintance", "acquaintance"],
	"one_friend": ["friend"],
}

const CALLS_PER_SESSION := 1


## The starting roster for a creation choice.
static func starting_set(choice: String) -> Dictionary:
	if not STARTING_CHOICES.has(choice):
		return {"ok": false, "reason": "choice must be two_acquaintances or one_friend"}
	var levels: Array = STARTING_CHOICES[choice]
	var contacts: Array = []
	for level in levels:
		contacts.append({"level": level})
	return {"ok": true, "contacts": contacts}


## A contact needs a name, a profession and a history — the SRD's four creation steps without the
## optional physical description.
static func validate(contact: Dictionary) -> Dictionary:
	var missing: Array = []
	for field in ["name", "profession", "history"]:
		if String(contact.get(field, "")).strip_edges().is_empty():
			missing.append(field)
	if not LEVELS.has(String(contact.get("level", ""))):
		missing.append("level")
	return {"ok": missing.is_empty(), "missing": missing}


## Whether a request is within the relationship: risk and significant expense are what separate a
## friend from an acquaintance.
static func can_ask(level: String, risk: bool = false, significant_expense: bool = false) -> Dictionary:
	if not LEVELS.has(level):
		return {"ok": false, "reason": "unknown contact level: %s" % level}
	var limits: Dictionary = LEVELS[level]
	var allowed := true
	var refusal := ""
	if risk and not bool(limits["risk"]):
		allowed = false
		refusal = "an acquaintance will not take on real risk"
	elif significant_expense and not bool(limits["significant_expense"]):
		allowed = false
		refusal = "an acquaintance will not take on significant expense"
	return {"ok": true, "allowed": allowed, "refusal": refusal}


## Contacts never join a mission.
static func can_join_mission() -> bool:
	return false


## One call per contact per session.
static func calls_per_session() -> int:
	return CALLS_PER_SESSION


## Losing trust downgrades: friend → acquaintance → gone.
static func downgrade(level: String) -> String:
	match level:
		"friend":
			return "acquaintance"
		"acquaintance":
			return "none"
		_:
			return "none"


## Earning trust upgrades: acquaintance → friend; a friend stays a friend.
static func upgrade(level: String) -> String:
	match level:
		"acquaintance":
			return "friend"
		"friend":
			return "friend"
		_:
			return "acquaintance"
