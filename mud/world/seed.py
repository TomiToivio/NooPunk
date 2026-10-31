"""Idempotent starter world, deliberately independent of Godot."""
from evennia import create_object, search_object

def _room(key, desc, **attributes):
    existing = search_object(key, typeclass="typeclasses.rooms.ApocalypseRoom", exact=True)
    if existing:
        return existing[0]
    obj = create_object("typeclasses.rooms.ApocalypseRoom", key=key)
    obj.db.desc = desc
    for field, value in attributes.items():
        setattr(obj.db, field, value)
    return obj

def _exit(key, origin, destination):
    from evennia import DefaultExit
    if not any(obj.key == key and obj.destination == destination for obj in origin.exits):
        create_object(DefaultExit, key=key, location=origin, destination=destination)

def seed_helsinki():
    street = _room("Helsinginkatu", "Trams rumble past shuttered shops. No one agrees what happened last night.", scavengeable=True, food_cache=8)
    kurvi = _room("Kurvi", "A restless crowd trades conflicting news and scavenged batteries.", scavengeable=True, food_cache=4)
    unsa = _room("UNSA safehouse", "A former office now staffed by exhausted volunteers. A notice promises water and registration.", unsa_recruitment=True)
    _exit("east", street, kurvi)
    _exit("west", kurvi, street)
    _exit("north", street, unsa)
    _exit("south", unsa, street)
    if not search_object("UNSA dispatcher", exact=True):
        npc = create_object("evennia.DefaultCharacter", key="UNSA dispatcher", location=unsa)
        npc.db.npc_dialogue = "We need food, first aid, and people who can keep their heads. You can sign up here."
    return street
