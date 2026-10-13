#!/usr/bin/env python3
"""NoöPunk text-first card catalogue. Stdlib only; no combat mechanics."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "world" / "character_cards.json"
TYPES = {"canonical", "archetype", "nhi"}
ONTOLOGIES = {"Biologics", "Constructs", "Noetics", "Plasmoids"}
STATS = {"FIT", "REF", "INT", "SOC", "PSY", "CYB", "SCIENCE"}
ACTIONS = {"investigation", "influence", "recruitment", "espionage", "field_operations", "cyber", "psi", "combat"}

def load_cards(path=DATA):
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1 or not isinstance(doc.get("cards"), list):
        raise ValueError("Expected schema_version=1 and cards list")
    ids = set()
    for card in doc["cards"]:
        for key in ("id", "card_type", "name", "role", "summary", "factions", "tags", "attributes", "actions", "public"):
            if key not in card:
                raise ValueError(f"Missing {key}: {card.get('id','<unknown>')}")
        if card["id"] in ids:
            raise ValueError("Duplicate card ID: " + card["id"])
        ids.add(card["id"])
        if card["card_type"] not in TYPES:
            raise ValueError("Invalid card_type: " + card["id"])
        if not isinstance(card["factions"], list) or not isinstance(card["tags"], list):
            raise ValueError("Tags and factions must be arrays")
        if not set(card["attributes"]) <= STATS or not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in card["attributes"].values()):
            raise ValueError("Invalid attributes: " + card["id"])
        if not set(card["actions"]) <= ACTIONS:
            raise ValueError("Invalid actions: " + card["id"])
        if card["card_type"] == "nhi":
            nhi = card.get("nhi", {})
            if nhi.get("ontology") not in ONTOLOGIES or not isinstance(nhi.get("origin_hypotheses"), list) or nhi.get("certainty") not in {"unknown", "disputed", "provisional", "confirmed"}:
                raise ValueError("Invalid NHI taxonomy: " + card["id"])
        elif "nhi" in card:
            raise ValueError("NHI taxonomy on non-NHI card")
    return doc["cards"]

def view(card, reveal=False):
    front = f"[{card['card_type'].upper()}] {card['name']} | {card['role']}\n{card['summary']}\nTags: {', '.join(card['tags']) or 'none'} | Stats: {card['attributes']}"
    details = "\nFactions: " + (", ".join(card["factions"]) or "unaffiliated")
    if card.get("nhi"):
        n = card["nhi"]
        details += f"\nOntology: {n['ontology']} ({n['certainty']}) | Species: {n.get('species') or 'unknown'}"
        if reveal:
            details += "\nOrigin hypotheses: " + ", ".join(n["origin_hypotheses"])
    details += "\nActions: " + ", ".join(card["actions"])
    details += "\nPublic: " + json.dumps(card["public"], ensure_ascii=False)
    if reveal:
        details += "\nGM: " + json.dumps(card.get("gm_only", {}), ensure_ascii=False)
    return front + details

def instantiate(card, instance_id, name=None, faction=None):
    if card["card_type"] != "archetype":
        raise ValueError("Only archetypes can be instantiated; canonical characters must stay unique")
    if not instance_id.strip() or instance_id == card["id"]:
        raise ValueError("Supply a distinct instance ID")
    return {"instance_id": instance_id, "template_id": card["id"], "name": name or card["name"],
            "factions": [faction] if faction else list(card["factions"]),
            "attributes": dict(card["attributes"]), "tags": list(card["tags"]), "statuses": [],
            "relationships": [], "progression": {}, "loyalty": None}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--type", choices=sorted(TYPES))
    parser.add_argument("--tag")
    parser.add_argument("--faction")
    parser.add_argument("--id")
    parser.add_argument("--gm", action="store_true", help="Reveal GM-only material (spoilers)")
    parser.add_argument("--instantiate", metavar="INSTANCE_ID", help="Instantiate the --id archetype")
    parser.add_argument("--name")
    args = parser.parse_args()
    cards = load_cards()
    if args.validate:
        print(f"Validated {len(cards)} cards")
        return
    filtered = [c for c in cards if (not args.type or c["card_type"] == args.type)
                and (not args.tag or args.tag in c["tags"])
                and (not args.faction or args.faction in c["factions"])
                and (not args.id or args.id == c["id"])]
    if args.instantiate:
        if len(filtered) != 1:
            parser.error("--instantiate requires one matching --id archetype")
        print(json.dumps(instantiate(filtered[0], args.instantiate, args.name, args.faction), indent=2))
        return
    for c in filtered:
        print(view(c, args.gm) + "\n")

if __name__ == "__main__":
    main()
