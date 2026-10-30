# Issue #749: Godot turn-based RPG MVP delivery ledger

**Status:** implementation blueprint and audited starting point, not a completed MVP. Parent: [#749](https://github.com/TomiToivio/NooPunk/issues/749). Game: legacy NoöPunk RPG only, **not** `strategy_game/`.

## Authority and constraints

1. `AGENTS.md` 2026-10-26 override and `rulebook/WITHOUT_NUMBER_BASELINE.md` govern mechanics: CWN operator, optional SWN Revised Psychic/Partial Psychic package. Never add psychic ranks to Romppainen by default.
2. Keep the existing Lakkahaltia case playable. Treat the new home/HQ/mission flow as an additional route, not a replacement. Preserve source-specific Main/Move/On Turn/Instant action costs.
3. `docs/archive/DESIGN_PRINCIPLES.md`: meaningful simulation, narrative agency and tactical choices. `docs/GODOT.md` and `docs/CWN_SRD_GODOT_IMPLEMENTATION.md` describe existing playable and rules slices.
4. **Only test executable behavior.** No automated lore, scenario-text or rulebook-wording gates.
5. Rights: `docs/licenses/ISSUE_569_CWN_SWN_LICENCE_AUDIT.md`. CWN SRD permissions are not blanket permission for the paid book; the freely available SWN edition is not an SRD. Do not bundle copied SWN technique descriptions, commercial tables, or protected artwork. Get review for redistribution of any source-dependent catalogue.

## Repository starting point (audited 2026-10-30)

| Layer | Existing entrypoint | Current gap for #749 |
| --- | --- | --- |
| Main project | `project.godot`; `scenes/main.tscn` | Existing title opens Lakkahaltia, not a new multi-location start |
| Playable investigation | `scenes/lakkahaltia/ward.tscn`, `src/godot/case_state.gd`, `data/scenarios/lakkahaltia/` | Ward-based case only; no home/HQ/mission travel loop |
| Alternative/older Godot scaffold | `godot/scenes/hospital.tscn`, `godot/core/game_state.gd` | Must audit overlapping state/autoload contracts before reuse |
| Godot rules | `src/godot/wn_rules.gd`, `src/godot/cwn_rules.gd`, `src/godot/cwn_progression.gd` | No verified end-to-end tactical and hacking interface |
| Python rules | `src/rules/cwn_*.py`, `src/rules/swn_psionics.py` | Many covered procedures in Python; Godot parity must be shown procedure-by-procedure |
| CWN hacking | `src/rules/cwn_hacking.py` | Existing rules core must be audited against CWN source and ported/exposed through Godot; reachability precheck is **not** full hacking |
| PSI | `src/rules/swn_psionics.py` and `docs/rules/SWN_PSIONICS_ADAPTATION.md` | Effort lifecycle exists; complete techniques, packages and advancement are not verified |
| Rights/source audit | `docs/licenses/ISSUE_569_CWN_SWN_LICENCE_AUDIT.md` | Needs per-content release decision before shipping commercial-only material |

**Source-of-truth note:** earlier `docs/design/ISSUE_728_GODOT_IMPLEMENTATION_PLAN.md` proposes a generic two-action hacking turn. Do **not** implement that illustrative proposal unless it is verified against vanilla CWN. The 2026-10-26 baseline and #749 override older design sketches.

## State and engine boundaries

A single versioned `CampaignState` contract should serialize `current_location`, character sheet (CWN attributes/skills/level/HP/saves/AC/strain), inventory, mission flags, journal/clues, dialogue choices, encounter actor states, network nodes/permissions/alert/access/CPU and RNG state or committed roll results. Avoid merging unrelated legacy save schemas. Use explicit version and reject incompatible saves with a helpful message.

Data (location graph, dialogue, encounter placements, evidence, network topology) must be separate from canonical rule procedures. Three Godot views operate on one campaign state:

- **Exploration/narrative:** Home → UNSA HQ → mission → debrief; dialogue and clues, travel triggers, inventory/journal.
- **Tactical:** turn order, tile movement, cover, combat actions, NPC turns and objective results; adapter resolves actual CWN actions.
- **Cyberspace:** node/edge drawing and valid CWN network transitions/program calls, not an arcade replacement. Explicitly show Access, CPU, program cost, risk, defenses and alert.

No scene script should independently compute dice results, substitute old stats, make invented PSI techniques, or grant equipment stats absent from verified source data. A digital-only pixel-art camera or menu is not a new tabletop rule.

## Source coverage gates (not claims of completion)

| Source | Coverage unit | Existing implementation | Required evidence to mark MVP-ready |
| --- | --- | --- | --- |
| CWN: Character Creation/Advancement | legal level-1 operator, Edges/Foci, starting skills, level/XP | `cwn_character.py`, `cwn_edges_foci.py`, `cwn_advancement.py`, `cwn_progression.gd` | one reproducible Romppainen creation choice sheet, source chapter reference, save roundtrip |
| CWN: Rules of the Game | 2d6 checks, d20 saves, attack rolls, assistance | `wn_rules.gd`, `cwn_rules.gd`, `cwn_core.py` | golden seeded action cases, visible modifiers, no duplicate rerolls |
| CWN: Combat | initiative, action types, movement, cover, melee/ranged, shock, trauma | Python `cwn_combat*.py`, `cwn_trauma.py` | legal turn selection, enemy response, no skipped resource accounting |
| CWN: Damage/Injury/Healing | HP, trauma, stabilization, system strain | Python `cwn_healing.py`, `cwn_injury_procedure.py` | source-checked transitions and save/reload mid-combat |
| CWN: Gear/Cyberware | two ACs, load, ammo/reload, cyberware | `data/rules/cwn_equipment.json`, Python equipment/strain | source-licensed stat-line provenance and inventory effects |
| CWN: Hacking/Cyberdecks | connectivity, Jack In, program legality, Access/CPU, alert/defense | Python `cwn_hacking.py`; Godot precheck only per documentation | complete end-to-end legal attack on a small graph; costs and consequences persist |
| CWN: NPC/Mission | one encounter, objective, reaction and payout | case infrastructure | optional violence and peaceful completion produce distinct, reproducible outcomes |
| SWN Revised: Psionics | legal class option, six disciplines, Effort, techniques and advancement | `swn_psionics.py` resource layer | source-verified test psychic (not Romppainen), legal technique execution; track unported techniques |
| CWN other chapters | crafting, vehicles, drones, long-form economy | various Python modules | explicitly **later**, never label as finished |
| SWN PSI other techniques | complete discipline catalogue and upgrades | partial | explicitly **later** until individually verified and licensed |

Use source chapter and ideally section/page, implementation link, executable test link, and one of `verified`, `partial`, `unimplemented`, `blocked-by-source-rights`. Do not mark any whole book as complete based on a handful of tests.

## Delivery order / PR gates

### Gate 1: shared campaign save, transitions and content skeleton
- Add a **new** campaign start at Romppainen's home without deleting or silently replacing the Lakkahaltia entry point.
- Home, UNSA HQ and mission are small scene/data records with a working transition and return/debrief.
- Persist location, flags, clue journal and explicit character data. Pending character creation choices must appear as choices, never secretly invented canon.
- Automated behavior tests for transitions, restart/save/load and duplicate event prevention.
- **Demo:** start at home, speak/read clue, go HQ, accept mission, return and see resolution.

### Gate 2: rule-faithful character/gear and tactical encounter
- Port/adapt complete legal CWN operator sheet and basic gear with source references.
- Add one optional tactical encounter with initiative, movement, Main/Move/etc., weapon/ammo/AC, cover, damage, trauma/medical consequences and enemy state.
- Implement deterministic seeded tests for allowed/forbidden actions, death/incapacitation, and noncombat bypass.
- **Demo:** encounter can be solved peacefully or tactically, and saved halfway through.

### Gate 3: full CWN hacking interaction
- Audit `cwn_hacking.py` against book/SRD per verb and resource before exposing it.
- Create separate node/edge view, but keep access, CPU, programs and alarms in the canonical adapter.
- Test disconnected/air-gapped network, wireless penalty, insufficient resources, defensive reaction, alert escalation, save/load.
- **Demo:** terminal objective succeeds or fails through source-legal CWN actions; consequences visible back in physical scene.

### Gate 4: SWN PSI optional test, refinement and verification
- Use a separately and legally created SWN psychic fixture; Romppainen remains non-psychic unless selected through valid source procedures.
- Validate Effort commitment/recovery, discipline and prerequisite gates, legal initial technique execution, advancement boundaries. Keep unavailable techniques explicitly unavailable.
- Apply original or correctly licensed simple pixel art and provenance; review controls and visual contrast.
- Execute headless suite, manual Godot windowed Ubuntu playtest, update `docs/GODOT.md`, completion matrix and source/licensing ledger.
- **Demo:** home → HQ → mission with investigation + optional tactical + hacking → debrief, save/load throughout.

## Review policy and release conditions

- Never break existing Lakkahaltia tests or conflate the NoöPunk RPG with the strategy game.
- Do not close #749 after only architecture or scene-navigation work. Close only when the whole vertical slice is playable and its implemented-source coverage is honestly described.
- Document missing source-specific rules explicitly; no silent approximations to vanilla CWN/SWN.
- Verify manual windowed play before claiming visual quality. The repo reports past headless verification but not proof of current Linux windowed play.
