# NoöPunk Gameplay Loop

> Canonical interaction-design companion to RULEBOOK.md §§17, 42 and issues #107/#108.

NoöPunk's first vertical slice should be small enough to simulate deeply. The preferred
starting frame is an **Asteroid Belt station / habitat campaign** built around UNHSS /
Firewall field work.

## Core loop

```text
hub location
→ choose room / district / channel
→ inspect available tasks and clocks
→ encounter NPCs / factions
→ act using Physical, Social, Cybernetic or Psychic mode
→ update world state + Affect graph
→ mission / consequence / new clock
→ travel, recover, or return to hub
```

A station is a MUD-like social map rather than a menu pasted over a static world.
Locations contain people, institutions, access constraints, communication channels,
opportunities, dangers and ongoing processes.

## Tasks and clocks

Tasks represent immediate opportunities. Clocks represent processes that continue when
the player does something else: investigations, political crises, repairs, relationships,
faction pressure, NHI activity, deadlines and travel.

The exact clock mechanics are deferred. This document defines the architecture, not a
numerical clock subsystem.

## Contacts and social graph

Meaningful NPC encounters may create Contact edges. Contacts, reputation, faction
relations and motivations all use the same directional Affect graph.

Unknown is not neutral. Ambivalent edges are allowed. Relationship change must follow
fictional events rather than fixed universal increments.

## Missions and parties

UNHSS missions can leave the hub for ships, habitats, asteroid sites, corporations,
Noetic environments or other stations. Citizen Sleeper 2-style crew/party structure is
an interaction reference, not a content template.

## Four interaction modes

- **Physical:** movement, danger, combat, rescue, material intervention.
- **Social:** communication, investigation, persuasion, institutions, ideology.
- **Cybernetic:** networks, AI, software, devices, information infrastructure.
- **Psychic:** PSI, Noetic contact, altered states and consciousness-mediated action.

They share one character sheet, one world state and one core d10 resolution engine.
They are not separate minigames by default.

## Scope rule

Build the first hub richly before simulating the whole Solar System. New habitats and
regions are added when missions and play require them.
