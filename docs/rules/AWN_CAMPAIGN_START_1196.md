# AWN Deluxe: campaign-start rules and compatibility (#1196)

**Source:** user's authorised *Ashes Without Number Deluxe* PDF (2025 printing). Printed page numbers below, not PDF viewer page numbers. This is an integration inventory, not reproduced proprietary tables.

## Character creation

- **Mutant** is available to the Europol-approved rookie at generation (AWN pp.16–25). It is not evidence of Grey DNA, Hybrid ancestry, alien infiltration or SWN Psychic status. The character can be a non-Hybrid human mutant. Origin, mutation and psychic capacity are independent.
- The published Mutant procedure starts with **2 Mutation Points** (MP); concealable Stigma costs 1; at most 3 randomly generated negative mutations grant 2 MP each; a chosen positive costs 3 MP, a random positive 1 MP, or two same-category random results 3 MP. The separately selected Mutation Acceleration Edge grants 2 more MP. The printed effects and roll tables remain lookup material (no invented entry text). Implemented by `src/rules/awn_mutant.py`.
- **Mentalist** is selectable at first level (AWN Deluxe pp.264–269). Its initial grant is Mentalism-0 and two lesser arts. Effort maximum is 1 + Mentalism + highest Wisdom/Charisma modifier; scene/day commitments are different. Its arts are **not SWN disciplines**. The player cannot stack it with SWN full/partial Psychic, CWN Mage/Spellcaster/Summoner, and cannot implant Nerve-type CWN cyberware. Implemented as a first-level model by `src/rules/awn_mentalist.py`. The published art descriptions remain in the book; this repository does not offer a public effects catalogue.
- SWN Psychic is still an alternative starting route; if used, PC discipline choices remain Telepathy/Telekinesis only. The fictional claim that Magick is PSI does not unify their mechanics.

## Campaign-start overlay inventory

| Requested rules | Printed pages | What is implemented / reused | Remaining integration |
| --- | --- | --- | --- |
| Radiation | 55 | `awn_campaign_start.radiation_exposure`: Physical saves, 1d4 Strain or 1d6 CON damage, excess Strain conversion, fatal CON<3 flag, optional mutation event | Exposure interval scheduling, treatment/recovery, mutations from natural rolls |
| Addiction and Recovery | 58 | `Addiction` tracks abstinence weeks, weekly successful Physical/Mental recovery save; caller may apply caregiver Heal | Daily penalties, indulgence costs, stress/strain coupling, UI |
| Stress | 56–58 | **Existing** `awn_stress_tracker.py` is the authoritative runtime (plus existing tests); imported by `stress_engine()` | No competing implementation; connect to character and scene state |
| Vehicle Combat | 49 | Main-action driver control and Luck crash/halt, moving unsecured weapon penalty | Existing CWN attack/armor/damage resolver and vehicle entity should be wired; other AWN vehicle-specific effects need parity checks |
| Chases and Pursuit | 51 | Foot escape vs pursuit, vehicle speed/maneuver/pursuit comparison; seeded rolls are external | Integrate with existing `cwn_vehicles.py` / scene controllers, pursuit modifiers and obstacle consequences |
| Pharmaceuticals / Stims | 86–87 | Conventional application vs Main-action stim; Heal skill gate | Reuse `cwn_pharmaceuticals.py` for CWN goods; AWN drug effect catalogue, addiction/toxin/disease interactions remain to be wired |
| Enclaves and Settlements | 104–110 | Power (1–5), Action Die, Cohesion, Dominion, Trouble, one internal action / Power external action slots as properties; seedable checks | AWN Features/Problems and action resolution including Interest, Enact Change and contests are incomplete. Bridge to existing `awn_world.WorldLedger`, without a second universe of enclave identities |

## Source precedence

CWN **always** owns character-scale attacks, rolls and sheets, SWN remains owner of faction turns and SWN psychic progression, AWN contributes *optional* region-specific systems. Enclave mechanics and the strategic faction system must not share a turn loop. Enclave stats are separate from CWN action decisions.

None of the above changes the scripted status of Astral Projection, the permitted player SWN disciplines, or the requirement for one canonical actor record. No automatic mutation-to-Hybrid inference.

## Coverage assessment

The existing generated `docs/rules/AWN_SECTION_COVERAGE_1109.md` records **133** AWN sections. Its prior baseline was verified 4, verified reuse 3, partial 6, unverified 13, missing 84 and not applicable 22. This PR updates a subset; **it does not claim full AWN implementation**. Do not manually edit the generated coverage report: regenerate `data/rules/awn_traceability.json` via the existing audit workflow after follow-up integrations and tests.

### Immediate follow-ups

1. Connect generation-time Mutant/Mentalist choices to the actual playable character builder; map art and mutation names from the printed rulebook using a private/licensed lookup. The public modules validate and track but do not expose all published effects.
2. Finish AWN enclave turns (Interest, Features/Problems, contests, Enact Change) in coordination with existing `awn_world` ledger.
3. Connect the overlay functions to Action scenes and existing CWN vehicle/drug resolution. Validate full integration tests and the generated AWN coverage audit.
4. Keep #1196 open until remaining rulebook-dependent and runtime tasks are completed. Astral Graph still waits for a concrete authored navigable projection scene.
