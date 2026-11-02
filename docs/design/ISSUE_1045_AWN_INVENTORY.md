# Ashes Without Number: rule inventory and priority (source: #1045)

<!--
PROVENANCE: transcribed from the author's own issue text, unedited in substance.

STATUS: SOURCE MATERIAL, not an implementation order. Where the source says a rule must come from a book that
is not in this repository, the rule stays unimplemented here rather than guessed. Check the licensed book.
-->

# Purpose and canon
Build a **source-backed, prioritized Ashes Without Number (AWN) rules inventory** for eventual implementation in the NoöPunk **Evennia MUD**, without altering or replacing the permanently locked **Cities Without Number (CWN)** core. AWN is an optional cross-genre toolkit alongside SWN psionics/factions and WWN occult magic (see #1006, #1025, #1044). **This issue is planning/inventory, not a blanket mandate to implement AWN immediately.** Avoid redoing the existing AWN stress module issue #928; audit/reuse it.

## World-state distinction: two compatible post-apocalypses
1. **Current canon: globally shared ontological apocalypse, uneven material collapse.** Disclosure and the NHI Crisis destabilized everybody's understanding of reality, but most global infrastructure, states, cities, industry, law and commerce **still function**. Some worst-hit localities are effectively **AWN *After the Fall***: destroyed infrastructure, displacement, patchwork sovereignty, disrupted supply chains, contested UNSA/local authority, anomalous hazards, and surviving enclaves. Model collapse **per location**, not by converting the entire world into a wasteland.
2. **Possible future: a slow-burn *Crisis Campaign*.** The worst may be ahead. Cascading NHI/PSI/AI events, social conflict, fragile institutions and cascading scarcity can turn currently functioning areas into crisis zones during play. The transition must be optional, geographically differentiated, responsive to player/faction decisions, and not a predetermined global apocalypse.

Maintain the New Weird/science-fantasy and political themes: the crisis is not just nuclear waste and zombies; it is an **ontological** rupture with psychotronics, anomalous sites, interdimensional/NHI incursions and ideological responses. No generic Fallout reskin, no Tolkien-derived fantasy races.

## Primary source
**User-uploaded:** Kevin Crawford, *Ashes Without Number Deluxe* (2025, PDF filename `AshesWithoutNumber_Deluxe_061125(1).pdf`). Use the user's authorized copy when accessible; GitHub agents cannot assume chat attachments are locally mounted. Read and inventory the entire book rather than treating the below TOC-derived inventory as complete examination of each rule. Page numbers below refer to the **book's printed pages**, not PDF indices. Never upload the copyrighted deluxe PDF or reproduce substantial rulebook text in GitHub.

## Priority framework
- **P0:** highly usable in the existing partial-collapse campaign, without changing CWN.
- **P1:** essential for regional crisis zones and optional escalating Crisis Campaigns.
- **P2:** useful elective genre/NHI/PSI and long-term sandbox material.
- **P3:** defer unless a specific narrative/system need arises, or reject on incompatibility.
- For every item add: source page/section, current implementation status, CWN/SWN/WWN overlap, adaptation/reskin, feature flag/locale trigger, dependencies, integration and test acceptance criteria. Mark `already implemented` only after code/tests verification.

## P0: immediately relevant for NoöPunk's localized After the Fall
- [ ] **Stress / Breakdown / Hardening / Addiction and Recovery**, AWN pp. 56–58. Reconcile with **#928**; include trauma/ontological shock and social support; don't duplicate CWN core injury or overwrite existing mental-health mechanics. Stress is a game mechanic, not a mandatory clinical diagnosis.
- [ ] **Injury / healing / System Strain / Major Injuries / Disease / Radiation**, pp. 52–55: add crisis-zone hazards and persistent consequences *only where AWN extends CWN*; avoid duplicated strain/damage calculations.
- [ ] **Hunger, thirst and supplies; tracking, overland travel and scouting**, pp. 59–63: local scarcity, travel routes, evacuation, refugee relief, damaged transport, and search-and-rescue. Keep ordinary urban logistics normal outside affected areas.
- [ ] **Tech levels and scrap, damaging/repairing/building/modifying gear, identifying mysterious tech**, pp. 72–75, 102–103: salvaging broken cybernetics, emergency improvisation, reverse engineering anomalous psychotronic devices, restoring critical infrastructure; preserve CWN equipment/combat rules.
- [ ] **Enclaves and Settlements**, pp. 104–135: Power, Cohesion, **Features, Problems, Dominion, Interest**, action dice, enclave actions and turns, tags, PC effects. Model survivor communities, UNSA field bases, refugee settlements, quarantined districts, rogue municipalities and NHI/PSI cult enclaves. **Separate enclave/community scale from SWN faction scale** and WWN major projects; establish a documented mapping, not a replacement.
- [ ] **Encounter sites** pp. 152–189: site tags, history, features, occupants/leaders, hazards, salvage and loot. Reskin for anomalous contamination, boundary phenomena, abandoned laboratories, breach sites, evacuated metro tunnels, noetic/haunted spaces, and disputed quarantine zones.

## P1: Crisis Campaign progression and regional simulation
- [ ] **Campaign genres and structures**, pp. 136–145: assess *After the Fall* (primary regional mode), *Crisis Campaigns* pp. 142, *Exploration Campaigns* pp. 143, region creation pp. 144–145, and distinction from *Deadlands* and *Mutant Wasteland* genres (not global defaults).
- [ ] **Building Crises**, pp. 146–151: adapt crisis preparation/pressure and escalating complications to NHI/PSI/AI events; generate dynamic regional crisis phases and possible stabilization/recovery. Never automatically force apocalypse or predetermined player failure.
- [ ] **Crisis / Exploration / Social Adventures**, pp. 190–201: renewable Evennia single-player UNSA case hooks, civilian protection, investigations, humanitarian aid, supply relief, contested evacuation, faction choices, rewards/patrons.
- [ ] **Enclave turns & regional state evolution** (pp. 105–135): persist enclave conditions and supply shocks; how UNSA, municipal government and local groups interact under divergent emergency laws; player choices influence collapse/recovery; link to LaclauGPT ideology/faction simulation without hard-coded ideological morality.
- [ ] **Chases, pursuits, vehicle/mounted combat**, pp. 49–51; optional lethality and major injury pp. 48, 53: only AWN extensions useful to pursuits through broken infrastructure, convoys, drones, military operations, disrupted roads; don't replace CWN vehicle rules.
- [ ] **GM complications, reaction and morale**, pp. 66, 204–205: useful to GM-less single-player NPC/civilian/UNSA encounters, and later sandbox agents.

## P2: selectable character/setting capabilities and adversaries
- [ ] **Character Creation** pp. 4–35: backgrounds, skills, Edges, Foci, advancement, starting gear; use as regional NPC/background options where they add flavor; **do not replace CWN character generation, skills, Edges or core progression**.
- [ ] **Mutations / Stigmas / Positive and Negative Mutations**, pp. 16–25: optional NHI exposure, psychic mutation, anomalous biology and cultural stigma; make abilities and consequences separate from moral judgments about people and avoid default mutant races.
- [ ] **Equipment catalogs**, pp. 70–103: encumbrance, armor, mundane/high-tech weapons, heavy weapons, stims/pharmaceuticals, vehicles/fittings/mods, tools, survival gear; add only useful distinct items, respect existing CWN balance.
- [ ] **Creatures of the Wastes**, pp. 202–229: animals, cyborgs, humans, mutant animals/humanoids, robots, zombie infection options, nemesis traits, encounter judging and generators; transform selected entries into NoöPunk-specific anomalous creatures, constructs, PSI phenomena, synthetic intelligences. Zombies/Beastfolk **only optional** where setting demands them.
- [ ] **Evil Techno-wizards**, pp. 255–257 (Deluxe): occult technocrats, psychotronic predators, conspiracy generators, NHI cult operations; setting/narrative hooks.
- [ ] **Ash Sorcerer and disciplines**, pp. 258–263 (Deluxe): compare with WWN High Mage/Hermetic magick and SWN psionics; preserve the fiction's magick-as-PSI premise without creating duplicate free powers.
- [ ] **Mentalist and disciplines**, pp. 264–269 (Deluxe): compare with SWN psionics and Noösphere mod; integrate selectively only after gap analysis.
- [ ] **Modular Power Armor**, pp. 270–277 (Deluxe): optional heavy UNSA/military or NHI-response encounters; no need to supersede CWN armor/cyberware.

## P3: defer or adapt only when justified
- [ ] **Hub Settlement Rules**, pp. 278–285 (Deluxe): future survivor-hub management and longer-term sandbox.
- [ ] **Settlements and Mass Combat**, pp. 286–293 (Deluxe): large-scale crisis conflict, protect civilians, coordinate UNSA/national troops; compare with SWN faction and existing mass combat to avoid triple bookkeeping.
- [ ] **The Albuquerque Death Zone**, pp. 230–253: review as **design example only**, not NoöPunk canon; exclude its specific geography, Cowboy class, names and setting assumptions unless independently justified.
- [ ] Review all remaining AWN sections including **Mixing Sine Nomine Games Together** (p. 67 onward) for explicit cross-system conversion guidance, plus system quick reference pp. 36–47. Keep CWN first, add new capabilities modularly.

## Required two-level world model
Design a *region/locality* condition layer and *global/world* status layer. Example tags (NoöPunk-original, not AWN rules): `functioning`, `emergency`, `after_the_fall`, `contested`, `recovering`. Maintain explicit axes for **physical infrastructure, public safety, supplies, governance, communications, NHI/PSI anomaly intensity and ontological shock**. A region's collapse state activates suitable AWN overlays; a functioning city's ordinary play remains CWN. Define transitions, stabilizing interventions, recovery, migrations, resource flows and interregional political reactions. Preserve the reality that society survives even amid ontological upheaval.

## Deliverables / acceptance criteria
- [ ] A full **AWN rule inventory** in repository documentation, grouped by printed chapter/subsection, P0–P3 priorities, status and source-page links, with no silent omissions.
- [ ] **CWN → AWN compatibility matrix**; identify already shared mechanics versus unique post-apocalyptic rules, prevent duplicate Stress/System Strain/Edges/Foci and balance drift.
- [ ] **After the Fall localized-region design** with examples (an UNSA humanitarian mission in a ruined district vs ordinary Helsinki life), including switchable regional rules and recovery.
- [ ] **Crisis Campaign design** for slow, contingent escalation: crises and sites, triggers, consequences, stabilization, and player agency; test campaign state saves/loads in Evennia.
- [ ] Compare AWN **enclaves** to existing **SWN factions** and WWN **Major Projects**; document how the three scales interoperate.
- [ ] Review the **Deluxe-only** options separately, preserving user-supplied copyrighted rulebook access restrictions.
- [ ] Propose a phased issue/PR backlog. **Do not implement everything now**, and do not rewrite the locked CWN system.
- [ ] Respect current project language policy: human-authored Finnish stays; agents produce English.

## Cross-references
- CWN rules constitution: #1006; CWN parity: #1025
- AWN Stress existing work: #928
- WWN / Law of One / science-fantasy roadmap: #1044
- AWN publisher overview: https://5d-blog.com/ashes-without-number/
- This issue's uploaded source: `AshesWithoutNumber_Deluxe_061125(1).pdf` (2025 deluxe rulebook; **not automatically available in GitHub**).

