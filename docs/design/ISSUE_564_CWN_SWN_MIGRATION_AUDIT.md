# Issue #564: Cities Without Number / Stars Without Number migration audit

**Status:** exploratory migration record, **not** a rules override or authorization to replace running game code.  
**Decision gate:** the author must reconcile issue #564 with the later/other active canon before any dice or character-schema migration.

## Source of truth and incompatible existing tracks

This repository contains **two games sharing one world** (AGENTS.md §0):

1. **Legacy NoöPunk RPG**: root `RULEBOOK.md` and `rulebook/`. Root `RULEBOOK.md` presently says **independent 1–10 STAT + 1–10 Skill + 1d10 against Difficulty**, with **FIT/REF/INT/SOC/CYB/PSY**. See design decisions #111, #131 and #159; code lies under `src/rules/`, `src/text_game/`, and later-media ports. Root `RULEBOOK.md` is the canonical human-readable rules ledger for this game.
2. **Crossover strategy/RPG**: `strategy_game/RULEBOOK.md`, `strategy_game/rpg/RULEBOOK.md` and `strategy_game/rpg/fate.py`. Approved individual RPG rules use Fate's 4dF, aspects and stress and six differently named individual skills (COG/INT/REF/SAV/SOM/WIL; #389 and #482). Faction political simulation remains a separate layer, with mechanics mostly unapproved. Legacy rules must not be imported automatically.

**Conflict:** #564 refers to preserving a 3d6 core, 3d6 human character generation, a -3..+3 modifier scale, and FIT/REF/INT/CHA/CYB/PSY. Those are not uniformly the current canonical rules. Earlier CWN-policy issue #19 and skill proposal #22 also are not carte blanche to override newer game-specific decisions. `AGENTS.md` and `docs/archive/DESIGN_PRINCIPLES.md` explicitly prohibit inventing or silently replacing mechanics. Therefore **do not swap to 2d6/3d6, revert SOC to CHA, impose CWN trained skills 0–4 on legacy 1–10 skills, or replace the crossover's 4dF without explicit reconciliation**.

## Sources and reuse boundary

- *Cities Without Number* (2023), Kevin Crawford, uploaded deluxe edition, used **for comparative reading only**: character creation (printed pp. 4–26), core game rules (28–46), hardware (48–89), hacking (90–105), mission creation (132–179), and GM procedures.
- *Stars Without Number Revised* (2017), Kevin Crawford, uploaded deluxe edition, used **for comparative reading only**: character creation (pp. 3 onward), psionics (29–44), systems (45–60), equipment (61–92), factions (211–230), and optional deluxe subjects such as transhuman campaigns and true AIs.
- Public CWN SRD: https://cwn.quadrifons.com/ . Only content actually present in an explicitly reusable source under its actual license can be adapted as text/code, with required notices. **Possession of the deluxe PDFs grants no blanket right to redistribute their prose, tables, illustrations or setting.** Verify SWN's specific rights separately. This audit contains original summaries and decision proposals, not copied game text.
- Project policy: #19, #22, #200, #389, #482, #564; `AGENTS.md`; `docs/archive/DESIGN_PRINCIPLES.md`; root `RULEBOOK.md`; `strategy_game/RULEBOOK.md`.

## Subsystem crosswalk

**Classification** is a *recommended review action*, not an implemented rule change. **Status** means migration state, not completeness of existing NoöPunk features. Source references are chapter-level comparisons to the uploaded deluxe books.

| Subsystem | CWN/SWN reference | Action | NoöPunk boundary / rationale | Migration status |
|---|---|---|---|---|
| Character attributes | CWN/SWN Character Creation | REPLACE | Preserve six existing legacy STATs including SOC, and crossover's separate six-skill Fate definition until reconciled; do not adopt STR/DEX/CON/WIS or alter existing scale | Blocked: author decision |
| Attributes rolled at creation | Both Character Creation | DEFER | #564 describes 3d6 generation; root rulebook currently records a different active 1–10 scale. Distinguish *generation dice* from *task dice* | Blocked: author decision |
| Skills and specialties | Both Character Creation/Skills; #22 | MODIFY | Compare CWN 0–4 trained/untrained structure with root legacy 1–10 and crossover six-skill Fate vocabulary; never conflate | Blocked: author decision |
| Core skill checks and difficulty | CWN Rules / SWN Systems | REPLACE | No automatic 2d6 import. Legacy currently uses d10; crossover uses 4dF. #564's 3d6 claim needs adjudication | Blocked: author decision |
| Saving throws / resistance | CWN Rules / SWN Systems | DEFER | Specify relationship to existing STAT+Skill tests and Fate defense before adding an extra save layer | Not migrated |
| Character backgrounds/lifepaths | Both Character Creation | MODIFY | Retain existing UNSA training/lifepath; adapt only procedures explicitly approved | Not migrated |
| Classes, edges and foci | Both Character Creation | DEFER | A class/level/feature economy would alter existing models; review separately | Not migrated |
| Advancement / experience | CWN Advancement / SWN Character Creation | DEFER | Avoid importing XP thresholds, skill caps, levels or class bonuses by default | Not migrated |
| Scene turns / initiative / action economy | CWN Rules / SWN Systems | MODIFY | Preserve separate personal-scene and faction-turn boundaries; one faction leader + four agents does not imply CWN combat action rules | Not migrated |
| Combat and harm | CWN Combat/Injury / SWN Systems | MODIFY | Aim for quick, dangerous confrontation, but migrate only after probability and wounds have a canonical tabletop model | Not migrated |
| Armor, weapons and gear | CWN Tools / SWN Equipment | MODIFY | No copyrighted gear tables; map existing named items to approved original mechanical properties | Not migrated |
| Medicine, recovery, strain | CWN Injury/Healing / SWN Systems | MODIFY | Compare strain and recovery concepts with existing NoöPunk harm ladder; don't introduce unapproved numeric thresholds | Not migrated |
| Augmentation/cyberware | CWN Cyberware / SWN Equipment | MODIFY | CYB remains NoöPunk-specific; capability gates, devices and human augmentation are not reducible to generic item bonuses | Not migrated |
| Network access and intrusion | CWN Hacking | REPLACE | Preserve physical/remote access prerequisites, BCI/device properties and post-AGI Blackwall/Slownet context; no automatic global omnipresent network | Not migrated |
| Drones, vehicles and chases | CWN Tools/Vehicle Combat / SWN Equipment | MODIFY | Compare tactical procedures, preserving device/session model | Not migrated |
| PSI and psychotronics | SWN Psionics | REPLACE | SWN psychic classes and power lists are **not NoöPunk canon**; NoöPunk natural PSI and psychotronic/BCI alternatives remain distinct | Not migrated |
| AI/ASI, uploaded people, NHI | SWN optional deluxe AI/transhuman chapters | REPLACE | Compare abstract capabilities only; do not use protected SWN AI societies, alien setting or unique lore | Not migrated |
| Contacts, clues, investigative scenes | CWN Contacts/Missions | MODIFY | Adapt light investigative scaffolding; preserve dialogue-first resolution and evidence/provenance | Not migrated |
| Missions, complications, heat | CWN Creating/Running Missions | MODIFY | Mission structure offers useful sandbox scaffolding, but consequences must reflect NoöPunk institutions and politics | Not migrated |
| Faction and social-network turns | SWN Factions / CWN Schemes | MODIFY | Adapt strategic *workflow*, not SWN numbers; leave Laclau/Castells/Luhmann power transitions author-approved | Not migrated |
| Geographic/world procedures | SWN Sector Creation / CWN Creating the City | OMIT | Do not transplant CWN corporate-city setting or SWN interstellar-sector premise into Earth-first pre-crisis campaign | Not migrated |
| NPC threats, reactions and morale | CWN Faces on the Street / SWN GM Resources | MODIFY | Light sandbox encounter prompts may help, but no protected stat blocks or setting NPC imports | Not migrated |
| Existing scenario payloads | No direct source | REPLACE | Legacy Helsinki/UNSA and Ubiquitous Maniacs must explicitly select a rules profile rather than silently mixing engines | Needs inventory |
| Godot/Concordia adapters | No direct source | DEFER | Stabilize the tabletop rules and versioned data contract before updating ports | Not migrated |

## Safe implementation architecture (proposal, not approved mechanics)

1. Keep both current playable routes functional. Avoid invasive mutation of `src/rules` or `strategy_game/rpg` while resolution/character definitions disagree.
2. Define a future **versioned rules-profile contract** with distinct identifiers for legacy d10, crossover Fate 4dF and any later CWN/SWN-derived system. A character/scenario must name its profile; an incompatible profile should fail explicitly, never quietly convert rolls or bonuses.
3. Every migrated subsystem needs: a tabletop specification and worked example; license/source record; deterministic Python behavior tests **only for implemented code**; and one reproducible scenario check. Never add prose/canon CI tests (AGENTS.md).
4. Port the smallest playable slice in order: character/sheet → investigation/social check → access-gated intrusion → PSI permissions → dangerous confrontation → save/load → scenario smoke test. Only then consider media adapters.
5. Retain a readable compatibility/legacy route and original creative canon; deletions require inventory and demonstrated replacements.

## Required author decisions before code migration

- **D1:** Which game(s) does #564 convert? Legacy only, crossover only, or separately coordinated conversion of both? Existing `AGENTS.md` says these are distinct and legacy must not be rewritten without separate approval. #564's broad request may authorize a new direction, but does not settle cross-game schema equivalence.
- **D2:** Which dice core wins for each game: legacy 1d10, crossover 4dF, #564's mentioned 3d6, or an explicitly playtested new variant? Keep current engines untouched pending decision.
- **D3:** Confirm current canonical six STATs **FIT/REF/INT/SOC/CYB/PSY** versus the issue's historical **CHA** variant, and whether crossover's six Fate skills stay independent.
- **D4:** Is #22's CWN trained-skill 0–4 scale to apply to a new profile, or supersede the current 1–10 legacy skills? Clarify unskilled -1 / BLOCKED.
- **D5:** Choose the actual SWN-derived mechanics intended for adaptation; SWN factions and sandbox procedures are good candidates, but their numeric rules, PSI class mechanics and space-sector defaults are not implied.
- **D6:** Determine original licensing/distribution for NoöPunk and verify exact source text grants for every imported excerpt. Deluxe PDFs remain reference only.

## Deliverables and verification queue

- [x] Record current competing rules tracks and how #564 conflicts with author-approved canon.
- [x] Comparative chapter-level CWN/SWN crosswalk and licensing boundary.
- [ ] Author approves D1–D6 and a single normative tabletop profile for the first migration.
- [ ] Write and playtest original quickstart, example character, and end-to-end investigation/combat/hacking/PSI session using that profile.
- [ ] Implement tested, profile-versioned engine; add executable behavior tests (never prose tests).
- [ ] Migrate legacy Helsinki/UNSA and Ubiquitous Maniacs scenarios with deterministic no-LLM playthroughs.
- [ ] Check CI, Godot and Concordia integration, and compatible source licensing before final merge.
- [ ] Close #564 only after functional acceptance criteria pass.

## Progress is not completion

This audit **does not implement a new dice system, change active character sheets, port campaigns, or establish the legality of directly redistributing deluxe material**. Those would require the explicit outstanding decisions and working tests. Issue #564 remains open.

## Four-book extension: Worlds and Ashes Without Number (2026-10-25)

The #564 review now covers **CWN + SWN + WWN + AWN**, not just CWN/SWN. Original tabletop work has begun at [`docs/rules/ISSUE_564_FOUR_BOOK_TABLETOP_PROCEDURES.md`](../rules/ISSUE_564_FOUR_BOOK_TABLETOP_PROCEDURES.md): a crisis-linked investigation mission workflow, optional regional disruption/recovery module, institution/major-project turn, and example scenario. These are **playtest drafts**, not numeric changes or tested digital engine implementations.

| Added comparison | Printed book chapters | Decision for NoöPunk | Status |
|---|---|---|---|
| WWN exploration, site mysteries | Creating Your Campaign (114); Creating Adventures (222) | **MODIFY:** adapt question/location/evidence scaffolding for NoöPunk investigations and Noösphere anomalies; no Latter Earth content | Draft tabletop procedure |
| WWN factions and major projects | Factions and Major Projects (322) | **MODIFY:** projects as qualitative institutional change tracking; no second asset economy | Draft tabletop procedure |
| WWN fantasy magic / heroic classes | Magic and the Arcane Traditions (60); Heroic Classes (356) | **OMIT:** PSI is not spellcasting and NoöPunk does not gain classes by default | Explicit exclusion |
| AWN regional crisis and survival | Rules (36), Overland Travel (60), Hunger/Thirst/Supplies (62) | **MODIFY:** optional access, supplies and travel constraints in real *localized* disruptions, using existing core rules | Draft tabletop procedure |
| AWN settlements and enclave management | Enclaves and Settlements (104) | **DEFER:** compare with SWN factions and WWN projects; choose one compatible institution model before numeric implementation | Qualitative draft only |
| AWN crisis/expedition/social adventures | Crisis Campaigns (142); Exploration Campaigns (143); Social Adventures (196) | **MODIFY:** consequences, recoveries and local social dilemmas, without total-collapse assumption | Draft mission worksheet |
| AWN injury, disease, radiation, stress | Injury (52), Disease (54), Radiation (55), Stress (56) | **DEFER:** compare with NoöPunk's harm and health rules without importing numeric tracks | Not implemented |
| AWN scrap, repair, high-tech | Equipment (70), Tech Levels/Scrap (72), Repair (73) | **DEFER:** condition-based logistics first, later equipment and resource audit | Not implemented |
| AWN zombies, mutations, setting | Character Creation/Mutations (16), Creatures (202), Albuquerque Death Zone (230) | **OMIT** as defaults; any rare encounter is a separately authored scenario decision | Explicit exclusion |

**Licensing:** the WWN deluxe (2021) and AWN free (2025) PDFs are **reference copies, not open-content grants**. No copyrighted prose/tables or publisher-specific setting was incorporated. This also applies to the CWN/SWN deluxe editions. Four-book mechanical inspiration alone does not confer copyright permission.

**Acceptance update:** the issue now additionally requires a four-book subsystem map and coherent WWN exploration + AWN crisis/enclave fit with NoöPunk's two distinct games. Numeric engine conversion, scenario migration, reproducible gameplay and CI remain uncompleted.
