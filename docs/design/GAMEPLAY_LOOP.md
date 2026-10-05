# NoöPunk gameplay loop

Status: design direction from issue #107. Tabletop/text specification first.

NoöPunk's initial playable form is a text-forward social RPG structurally inspired by Citizen Sleeper, Citizen Sleeper 2, old-school interactive fiction, a single-player MUD, Eclipse Phase and The Expanse. These are interaction references, not permission to copy protected characters, quests, prose, setting or assets.

## Core loop

location hub -> inspect places/tasks/people -> choose action or conversation -> resolve consequences -> update character, Affect graph and world state -> advance clocks/missions where applicable -> travel/form party/enter mission -> return to persistent world.

The social graph persists across hubs.

## Locations and rooms

The player is always in a Location such as a city, orbital, asteroid colony, station, ship, habitat, district or base. A Location contains connected Rooms / Places / Nodes. The character can move, inspect, work, rest, shop, investigate, meet NPCs, communicate with Contacts, receive messages, start missions, form a party, and travel to mission locations. Exact economy, work, rest and travel procedures remain separate design questions.

## Interaction modes

Exploration/location mode covers movement, inspection, work, rest, shopping and investigation. Social mode covers dialogue, negotiation, Contacts, Reputation and faction interaction. Mission mode takes a selected party into a bounded objective location. Combat, Cyberspace and Psionics are further interaction modes using the same persistent world model and their own rules when those are defined.

These are interfaces around shared state, not separate games.

## Communication channels

Face-to-face speech, text/chat, voice/video, Mesh communication and PSI/telepathic communication are channels over the same social-interaction architecture. Channel-specific access, surveillance, latency, range, authentication or PSI requirements may later modify an interaction without creating another relationship system.

## Parties and missions

A character may form a crew from PCs and eligible Contacts. Mission locations read the same character sheets, Affect graph, inventory and world state as hub play.

## First vertical slice: the Asteroid Belt

Prefer a small Belt colony, station, ship route or cluster of asteroid habitats. Use a few connected hubs, a small recurring cast, faction pressure, tasks, Contacts and crew missions. Stations naturally support text/MUD navigation; travel creates chapter boundaries; labor, reputation, hacking, physical danger, transhuman technology and gradual NHI/noetic material can coexist without simulating the whole Solar System.

This is a scope rule, not a demand to reproduce Citizen Sleeper or The Expanse.

## Implementation boundary

Build the tabletop/text specification first. Godot and Concordia should later consume the same domain state. LLMs may provide dialogue/narration around supplied state, while deterministic code owns dice, scores, graph mutation, clocks and other numeric mechanics once specified.
