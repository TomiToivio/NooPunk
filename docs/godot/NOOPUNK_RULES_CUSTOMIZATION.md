# NoöPunk as a customized CWN/SWN core (#809)

**Status:** direction and first integration. CWN/SWN is the mechanical floor, not the ceiling: the
author wants substantially more customization than the original "faithful port" plan assumed. Old
tested behaviour is preserved until an explicit NoöPunk replacement exists, and there is **one
canonical Godot implementation per customized mechanic** (AGENTS.md §16).

## What NoöPunk keeps from the floor

Kept as-is, because they carry the game and the tabletop can be played with them today:

| layer | kept from | where it lives |
| --- | --- | --- |
| attributes 3–18, modifiers capped ±2 | CWN | `godot/core/cwn_character.gd` |
| saves, skill ranks 0–4, difficulty numbers | CWN | `rules_adapter.gd`, `cwn_character.gd` |
| attack vs AC, Shock, Trauma, damage floor | CWN | `combat.gd`, `cwn_combat_rules.gd` |
| System Strain, Major Injury, healing, Frailty | CWN | `cwn_strain.gd`, `cwn_injury.gd`, `cwn_healing.gd` |
| Effort, commitments, Torching, discipline ranks | SWN | `psychic_effort.gd`, `psionics.gd`, `swn_progression.gd` |
| hacking: Alert clock, verbs, target ranks | CWN | `cwn_hacking.gd`, `hacking.gd` |

## What NoöPunk replaces or wraps

These are customization surfaces. Nothing here may silently drift into a second copy of the floor:

1. **The protagonist.** Not a borrowed NPC. A created **level-1 field agent** of *Suojelupoliisi*,
   *Europol* or *UNSA* (`godot/core/field_agent.gd`), producing a sheet in the shape the session,
   combat, hacking and scene code already consume.
2. **The party.** 1–4 members, all sizes legal, no fixed-size assumption anywhere
   (`godot/core/party.gd`). Romppainen is a **senior recruitable companion** (`data/npcs/romppainen.json`),
   AI-run by default, loanable to the player for a quest, never the avatar.
3. **Check ownership.** Whose sheet answers a check is the *selected* member's — the PC unless a
   companion is selected. `control` only says who is driving.
4. **Backgrounds, edges, foci and skills.** The NoöPunk-native list is authored in the tabletop layer
   first and only then wired into `field_agent.gd`. Until it exists, the agent gets the CWN defaults
   (Investigate/Notice/Shoot at rank 0) and a sidearm.
5. **Psionics.** The six SWN disciplines are kept as the mechanical skeleton; the *technique
   catalogue* is NoöPunk-authored (`data/rules/psionics_techniques.json`, `is_canonical: false`) and
   deliberately not the SWN power list.
6. **Lore, agencies, missions, tone.** Entirely ours; no upstream table constrains them.

## Open decisions this layer must not pre-empt

- **Level-1 hit points.** `godot/core/cwn_character.gd::hit_points(level, con, rolls)` adds a
  `6 + CON` base on top of the rolls; `src/godot/cwn/cwn_character.gd::max_hit_points(roll, con_mod, htk)`
  is a single-level roll. They cannot both be the tabletop rule. `field_agent.gd` computes
  `1d6 + CON` itself and says so, rather than importing either convention into new content. **Needs
  an author ruling**; that ruling then fixes the kernel.
- **Remaining `src/godot/` overlaps** (`cwn:catalogue`, `cwn:character`, `cwn:combat`) stay as
  documented compatibility paths until a NoöPunk design requires the change — per #809, migrating
  them is not to be done blind in the name of upstream parity.
- **Scenario fixtures** (`ward`, `prototype`, `hospital`) remain tested compatibility scenarios until
  story and asset parity permits consolidation.

## Save and migration policy

- `GameState` saves are versioned. The party is additive: a save without a party block loads with its
  single sheet as the protagonist and no companions rather than being rejected.
- A save whose roster is internally inconsistent (no protagonist, protagonist not level 1, more than
  four members, a selected member who is not present) is **refused**, not half-applied.
- Older campaigns are never rewritten in place: the version bump is read at load, and only the
  in-memory shape is upgraded.

## What is done in this increment

- `godot/core/field_agent.gd` — the level-1 law enforcer, session-shaped sheet, three agencies.
- `godot/core/party.gd` — protagonist, 1–4 roster, selection, join/leave, versioned round-trip.
- `Session` — the current party-aware encounter implementation reads actor IDs from the roster,
  or the character record for legacy single-character scenarios, without hardcoding Romppainen.
- `data/npcs/romppainen.json` — the senior companion descriptor.
- `godot/tests/test_field_agent.gd` — 52 rows: creation legality, session shape, roster seating,
  every party size, selection ownership, join/leave, round-trip, refusals.

## What remains (still owned by #809)

- The NoöPunk background/edge/focus list and its tabletop rules text.
- Wiring the created PC into the hospital start flow, the character editor and the scene dialogues.
- Party support in movement, hacking, investigation and inventory UI (combat already supports
  roster actors through `CwnParty`).
- Migrating mission data that still names Romppainen as the protagonist.
- Static validator and CI updates, then desktop playtests.
