# NoöPunk dual-layer Fate rules (issue #482)

**Status:** RPG action resolution foundation approved; the final strategic skill roster, strategic missions and political outcomes remain proposals. This document complements [the existing RPG field manual](RULEBOOK.md), not the legacy Godot game.

## One person, two roles

**RPG scene (Citizen Sleeper / Disco Elysium):** a character acts *personally*. Choose one of the six broad Fate-rated skills derived from Eclipse Phase aptitudes: **COG** (reasoning), **INT** (intuition, awareness, creativity), **REF** (coordination and reaction), **SAV** (empathy/social adaptation), **SOM** (physical action and endurance), **WIL** (self-control and resolve). These are **skills**, not EP percentile aptitudes. The default sheet lists all six, with 0 for untrained. Specialist access still requires an explicit fictional reason, capability/TAG, permission and sometimes equipment. A personal conversation is SAV; thinking through evidence is COG. The character might physically infiltrate a building using REF; an ESP ability cannot be conjured merely by rolling WIL.

**Strategy board (Terra Invicta / Crusader Kings 3):** the same character acts *for a faction*. Select a separately rated **strategic skill** for a declared organizational mission. The character's personal COG must never stand in automatically for faction Science, nor SAV for faction Persuasion. Instead, the strategy skill represents trained and equipped organizational capacity. Both actions use the **same 4dF + rated skill versus opposition Fate resolution**. GM controls permissions/stakes and narrative consequences.

A strategic order is not automatically an RPG scene; zoom into scenes selectively when a mission needs conversation, investigation or confrontation. One leader plus four agents each have up to **one faction order per turn**. Scene actions within an encounter are not extra faction orders. No automatic strategic map effects or invented calendar cadence.

## Strategic skills: researched candidate roster, NOT approved

Terra Invicta Councilors defines Persuasion, Investigation, Espionage, Command, Administration, Science, Security, and Loyalty. For NoöPunk, **propose seven active strategic skills**: the first seven. Treat **Loyalty** as a relationship/aspect/trait rather than a rollable active mission skill. No Terra Invicta percentile rolls, 0–25 scale, recruiting economy or mission probabilities carry over.

| Proposed strategic skill | Consolidates examples from Transhumanity's Fate | Faction-agent mission example |
| --- | --- | --- |
| Persuasion | Rapport, Provoke, Deceive, Kinesics, reputation/contacts | negotiate support or shape elite cooperation |
| Investigation | Investigate, Notice, Cover, Kinesics | locate a covert cell through faction resources |
| Espionage | Infiltrate, Cover, Deceive, Infosec | run covert infiltration or intelligence operation |
| Command | Fight, Shoot, Athletics, Provoke | direct a security team or military operation |
| Administration | Cred, Hardware, Program, Pilot, network/rep resources | coordinate procurement or build organizational capacity |
| Science | Medicine, Program, Hardware, X-Risks, Xeno-Contact | direct a research/investigation program |
| Security | Survival, Fight, Shoot, Infosec | protect an asset or defend a field operation |

The crosswalk is **many-to-many by narrative purpose**, not a claim of an exact one-to-one rules equivalence. Transhumanity's Fate's *Somatics* and *Will* overlap the individual **SOM** and **WIL**; there are **no duplicate skills**. Fate-based cyber/PSI domain specialization remains capability-gated, without importing Eclipse Phase lore.

## Resolution and API

`strategy_game.rpg.dual_layer.DualLayerCharacter` owns a regular Fate `Character` (aspects, Fate points, stress, consequences and setting fields), a six-skill individual map, and a separately configured strategic-skill map. `act(Scale.RPG, ...)` or `act(Scale.STRATEGY, ...)` delegates to the *existing* Fate scene resolver, including invocations, rerolls, and tracked scene aspects. `CouncilTurn` validates five distinct characters and prevents a second strategic order for any one character.

The package does **not** compute strategic outcomes, enact faction effects, propagate ideology, determine travel, approve specific missions, or open cyber/PSI access by itself. The existing `boundary.py` remains the future state-adapter seam.

### Play examples

An investigator personally decodes a clue: RPG / COG / Overcome / opposition 2. The same investigator directing a multi-location evidence-gathering operation: Strategy / Investigation / Overcome / opposition chosen by GM. A gifted psyker personally performs controlled remote viewing only if a corresponding capability and narrative permission exist. An agent cannot submit a `netrunner`-gated strategic cyber mission without that capability. The actual mission repertoire is pending author approval.

## Deferred design decisions

- Final strategic skill list and exact crosswalk, skill budgets, growth, Fate refresh and stunt costs.
- Which strategic actions are generic and which require a TAG, implant, equipment or other capability.
- Turn duration, travel and mission resolution sequencing, resource effects and the LaclauGPT-inspired ideology/political layer.
- Richer simulationist systems from Eclipse Phase for cyber combat, physical combat and PSI.
- Fully Fate-consistent treatment of stunts, boost/discovery lifecycle, concessions, stress and recovery beyond the existing RPG MVP.

## Sources and reuse

**Mechanics only, not lore:** Fate Core and Transhumanity's Fate, with Eclipse Phase 2e attributes and optional simulationist inspiration. Councilor attributes from [Terra Invicta's reference](https://wiki.hoodedhorse.com/Terra_Invicta/Councilors). Fate Core System © Evil Hat Productions, CC BY 3.0. NoöPunk is unaffiliated with Evil Hat or Posthuman Studios. The code/documentation use original wording; do not transplant NC-SA text or artwork from EP/Transhumanity's Fate without a separate licensing decision. See [ATTRIBUTION.md](ATTRIBUTION.md).
