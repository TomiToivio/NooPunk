# CWN ↔ AWN compatibility (#1109, Phase 0)

AWN models **places that have actually gone through the Crisis**; CWN models **functioning cyberpunk society**.
The same planet holds both, sometimes in the same country, and the rule that decides who resolves what is the
author's: **CWN for ordinary humans, AWN only where the region's state says so, and neither book's numbers
edited to fit the other.**

This matrix is the Phase 0 deliverable the tracker asks for: "shared mechanics delegate to CWN;
locale-triggered mechanics are optional; AWN-specific data contracts and rights documented" — verified
against AWN p.67 (*Mixing Sine Nomine Games Together*) and the CWN/SWN/WWN chapters that overlap.

Status vocabulary matches `data/rules/awn_traceability.json`:
`verified` · `verified_reuse` · `partial` · `documented` · `unverified` · `missing` · `not_applicable`.

| concern | AWN source | Where it is resolved | status | note |
|---|---|---|---|---|
| Attributes and modifiers | AWN p.5 | `src/rules/wn_core.py` → `attribute_modifier` | **verified_reuse** | The same Without Number band; pinned by `tests/test_wwn_shared_chassis.py`. |
| Skills and skill checks | AWN pp.5, 39 | `src/rules/wn_core.py` → `skill_check` | **verified_reuse** | 2d6 + skill + modifier, −1 untrained. One resolver. |
| Saves, HP, attack bonus | AWN pp.32, 38 | `src/rules/cwn_core.py` | **unverified** | CWN supplies them; AWN's printed values have not been compared row by row, and the register says so rather than claiming reuse. |
| Combat, rounds, actions, manoeuvres | AWN pp.40–47 | `src/rules/cwn_combat.py` | **unverified** | CWN resolves combat. AWN's optional lethality, vehicle combat, mounted combat and chases have no implementation at all. |
| Injury, healing, System Strain | AWN pp.52–53 | `src/rules/cwn_core.py`, `cwn_injury*` | **unverified** | One strain counter, CWN's. **AWN must never add a second Strain track**: the Stress track below is the post-apocalyptic resource, and it is not Strain. |
| Stress, breakdown, hardening | AWN pp.56–58 | `src/rules/awn_stress_tracker.py` over `data/rules/awn_stress.json` | **verified** | The AWN-specific track, reconciled with #928 and #1088; one tracker, one contract, seeded tests. |
| Addiction and recovery | AWN p.58 | same tracker | **partial** | Recovery and hardening steps exist; AWN's addiction procedure is not transcribed. |
| Travel, scouting, supplies, privation | AWN pp.59–63 | `src/rules/awn_survival.py` | **verified** | Terrain, hours, hexes/day, encounter checks, scouting, food/water, privation strain, starvation saves. Foraging takes a caller-supplied difficulty rather than inventing a table. |
| Advancement | AWN p.64 | `src/rules/cwn_core.py` | **unverified** | CWN advancement is authoritative; AWN's table is uncompared. |
| Equipment, tech levels, scrap, repair | AWN pp.70–103 | CWN gear for human-scale play | **missing** | AWN's tech-level/scrap/repair/build/modify procedures are unimplemented — the largest equipment gap and the natural next PR. CWN catalogues cover the CWN list only. |
| Enclave statistics and turns | AWN pp.104–135 | NoöPunk ledger (`awn_world.py`); AWN stats absent | **partial** | The ledger records enclaves, sites and crises as dated actors. AWN's Power/Cohesion/Features/Problems, Dominion/Interest and enclave-turn resolution are **not** implemented. #1083 owns that. |
| Region state and crisis pressure | AWN pp.136–151 | `src/rules/awn_region.py` | **verified** / **partial** | Regions, severity and legal transitions are implemented and tested; the printed crisis-building procedure is not transcribed. |
| Encounter sites | AWN pp.152–189 | `awn_world.py` (ledger only) | **partial** | Sites are dated entries; the tag/feature/occupant/hazard/loot procedures are unimplemented. |
| Creatures of the Wastes | AWN pp.202–229 | — | **missing** | No creature data model. CWN/SWN actors come first, per the tracker. |
| Cross-game mixing | AWN p.67 | this document | **documented** | The precedence below is the procedure; it is documentation, not code. |
| Albuquerque Death Zone | AWN pp.230–253 | — | **not_applicable** | Proprietary setting. NoöPunk uses its own regions; the mechanics it demonstrates are covered by the enclave and site rows. |
| Deluxe supplement (techno-wizards, Ash Sorcerer, Mentalist, power armour, hub settlements, mass combat) | AWN pp.254–293 | — | **missing** (deferred) | Deferred by the tracker until compared against WWN magic, SWN psionics, CWN armour and the enclave/faction scale. Deferral is recorded per row, not silently dropped. |

## Precedence when the systems are enabled together

1. **A character-scale action in a functioning region → CWN.** Attributes, skills, saves, combat, injury,
   gear and advancement come from CWN and are not re-derived by AWN.
2. **A character-scale action inside a collapsed region → CWN mechanics, AWN resources.** The dice do not
   change; what changes is that supplies, privation, Stress and tech scarcity apply. AWN never replaces the
   CWN action.
3. **A regional action → `awn_region` / `awn_world`.** Enclave turns, crises and sites are dated ledger
   events at their own scale. A field mission can *feed* them evidence; it cannot spend their resources.
4. **A strategic action → SWN factions** (its own turn and assets, untouched), or **WWN projects** for
   long-term works. AWN enclaves and SWN factions share identity, dates and events — never a turn loop.
   See `docs/rules/WWN_CWN_COMPATIBILITY.md` for the four-game view.
5. **Magic and psi keep their own pools.** WWN Effort, SWN psychic Effort and CWN System Strain are three
   resources; AWN Stress is a fourth. No two are ever added together or spent for one another.

## AWN off, AWN on

* With AWN disabled (`data/mods/registry.json`, `src/rules/mod_boundary.py`), nothing above changes the
  CWN game: `awn_stress_tracker.is_enabled()` is the switch for the Stress track, and a region's state is
  simply never consulted. Baseline CWN play must pass with every AWN module disabled, and the tests run
  that way by default.
* With AWN enabled, a region's severity is what activates the layer. Movement between a functioning and a
  collapsed region changes *which resources apply*, not which ruleset resolves the action.
* Recovery is as meaningful as collapse: `awn_region.transition_allowed()` permits both directions, because
  the tracker is explicit that the crisis is contingent and reversible.

## Rights

AWN has **no verified open-text licence** in `data/sources/game_system_rights.json`. Every procedure here is
independently written; the register cites printed pages only, and no AWN text, table, art or setting is
stored in the repository. The section index (`data/rules/awn_sections.json`) contains titles and page numbers,
which are facts about the book, not extracts from it.

## How to move a row out of `unverified`

1. Open the AWN page the register cites.
2. Write a test that takes the printed numbers *from the page* and asserts the shared resolver returns them
   — the shape of `tests/test_wwn_shared_chassis.py`.
3. If it fails, the resolver is wrong for AWN: add an AWN-native procedure **beside** the CWN one, cite the
   page, and leave CWN untouched.
4. Update `data/rules/awn_traceability.json`, then `python3 tools/awn_parity_audit.py`.
