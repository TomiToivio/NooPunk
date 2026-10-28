# #712: OSR chassis, investigative/narrative overlays and attributes (research only)

Status: **comparative design research**, not canon. Baseline: `rulebook/WITHOUT_NUMBER_BASELINE.md`, `data/rules/without_number.json`, `src/rules/wn_core.py`. See #704, merged #711, #716, `docs/design/ISSUE_704_GUMSHOE_INVESTIGATION.md`. The existing `src/rules/investigation.py` already handles guaranteed competent clue acquisition; this report does not redefine it.

## Comparison and application

| Source | Problem it solves | Proposed bounded use | Incompatibility / risk |
| --- | --- | --- | --- |
| CWN + SWN | OSR skill checks, lethal action, equipment, encumbrance, faction procedures, psionic Effort | Keep 3–18 scores/modifiers, 2d6 skills, d20 attacks/saves; SWN PSI as specialist subsystem | Replacing dice invalidates probability, progression and NPC balance |
| GUMSHOE SRD | Investigative competence and core clues | Already adapted: access + competency yields clue, consequential action uses CWN | No point pools; free information must not become free access |
| PbtA | Mixed outcomes, hard choices, threats/clocks, GM agenda | Preselect consequences and external clocks without importing move rolls | CWN failure is not automatically PbtA 6−; avoid double outcomes |
| Fate Core | Aspects, compels, situational truths | Tags to guide referee rulings and player-authored dilemmas | Fate point economy and +2 invokes do not map to CWN unchanged |
| The Veil | Identity, emotional and cybernetic mediation | Scene questions about emotion, embodiment and perceived reality | Emotion-based stats would replace OSR checks, not merely enhance them |
| Call/Trail of Cthulhu | Unsettling encounters, Stability and information | Independently track optional insight vs distress; allow recovery | Psychological distress must never validate a paranormal hypothesis |
| Eclipse Phase | Forks, continuity, transhuman identity | Source of questions for AI, BCI, distributed selfhood | Many stress/identity subsystems duplicate CWN conditions |

## Attribute choices (not approved)

**A: retain STR/DEX/CON/INT/WIS/CHA.** All scores, saves, skills, generated characters and stat blocks remain exactly as published. Give NoöPunk examples: STR carrying a patient; DEX avoiding a drone; CON resisting exposure; INT decoding BCI logs; WIS noticing contradictions; CHA establishing rapport. Cheapest, least distinctive.

**B: six display aliases.** STR = Body Power; DEX = Coordination; CON = Resilience; INT = Reason; WIS = Awareness; CHA = Presence. Preserve exact canonical identifiers in JSON, save formulae, imports, NPC contracts, scripts and old save files. Test that presentation round-trips to same codes. Recommended **reversible trial**, subject to #716 author approval.

**C1: mental-heavy six.** FIT (STR + CON conceptually), REF (DEX), INT (reason), AWA (perception and intuition), PSY (integration, will), SOC (empathy and influence). 2 physical / 4 mental. Combining STR/CON removes a dimension that distinguishes athletic power from endurance, complicates physical saves, HP/Strain and load. PSY is a general attribute, **not** an automatic psionic discipline. CYB stays gear/interfaces; SCIENCE stays a skill.

**C2: seven-stat variant.** FIT, REF, RES, INT, AWA, PSY, SOC: 3 physical / 4 mental. RES retains endurance, permitting constitution-derived HP and physical resilience, at cost of extra generation points and a new numeric economy. The 3–18 modifier bands could remain individually, but changing one ability distribution changes advantage frequency and skill/attack probabilities. If cybernetic proficiency is desired, use existing Program/Fix, cyberware and System Strain rather than a universal CYB score.

**Legacy alternative:** FIT/REF/INT/SOC/PSY/CYB is thematically strong but CYB double-counts equipment and denies nonaugmented or disembodied entities an obvious default; removing WIS/AWA risks collapsing observation into PSI. The historical Physical/Social/Psychic/Cybernetic *domains* are better tags for encounters than four universal scores.

## Migration/compatibility matrix

| Contract | A | B | C1 or C2 |
| --- | --- | --- | --- |
| 3–18 modifier table and 2d6 skills | identical | identical | can preserve table but must reassign every skill's governing attributes |
| Physical / Evasion / Mental saves | identical | identical | physical STR/CON, evasion DEX/INT, mental WIS/CHA must be remapped and recalibrated |
| HP, healing, System Strain, encumbrance | identical | identical | RES/CON removal and FIT fusion require new formulas |
| Initiative, attacks, equipment | identical | identical | REF mapping plus regression tests for hit probability |
| Characters, NPCs, scenario checks and data/rules JSON | identical | display labels only | **versioned migration**, all six-code references and exports updated |
| SWN psychic skills and Effort | identical | identical | remain trained techniques; PSY must not grant free powers |
| AI/no-body/noetic agents | scenario-specific exceptions | same | explicit N/A and interface rules needed, never invented physical stats |

**Worked checks** (illustrative, not simulation): under A/B, a Program-0 investigator using INT 14 (+1) rolls CWN 2d6+1 vs difficulty 8 to access a secured ward console; discovery of the subsequently accessible terminal timestamp is automatic. With an untrained Program skill (-1), 2d6+1-1 vs 8 governs the **risky intrusion**, never whether a properly obtained core timestamp exists. A psychiatrist with Heal-0 and authorized chart access obtains the amendment fact without dice. A telepath can only invoke an actually learned SWN technique with its Effort, not substitute a PSY roll. A human cyborg pays normal Strain for installed hardware, whereas a pure AI's physical saves and cyberware interface need explicit species/chassis rules. A noetic entity is not assumed to have human musculature. An institutional actor uses faction procedures, not a personal STR check.

**Balance risks:** C1 increases emphasis on mental scores while losing CON as a distinct balancing lever; C2 adds a seventh allocation target; either shifts starting modifier distributions unless generation budgets and sample characters are recalculated. Run 10k seeded synthetic character generations and exact 2d6 distributions *before* approving mechanical changes; compare skill success at targets 6/8/10/12 and physical/evasion/mental save outcomes by archetype. Do not describe those unrun tests as evidence.

## Noösphere, insight and Stability

Treat physical, cyberspace and noetic channels as **evidence provenance**, not automatic truth categories. Optional independent tracks: Insight = familiarity with anomalous models, Stability = current functioning/stress; either can move without the other, and either can recover independently. No track establishes ontology, moral worth or a psychiatric diagnosis. Cybernetic BCI access, psychotronic devices and natural SWN PSI have distinct prerequisites.

## Four test scenes

1. **Romppainen:** an authorized psychiatric interview gives a core testimony; a pressured attempt to retrieve protected case files uses a CWN check; mundane and anomalous hypotheses both remain open.
2. **BCI/PSI:** an interface produces a timestamp while a trained psychic reports an image; record provenance separately, charge Effort for the SWN technique, test contradictions without announcing an external entity.
3. **Hacker/researcher/cyborg:** Program handles system entry, Know handles scientific interpretation, cyberware sets affordances and Strain, not a CYB attribute.
4. **Pure AI/noetic entity/faction:** require substrate and interface rules for action; faction-scale bargaining follows faction actions, not a human personal-stat migration.

## Licences and next work

CWN SRD availability is not a grant to copy commercial CWN/SWN/WWN/AWN text wholesale. GUMSHOE SRD v3 is CC BY 3.0 with attribution (see `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`); Fate Core uses CC BY 3.0 / OGL pathways depending on text; PbtA is a family of designs and each specific game's terms differ. The Veil and other commercial text require separate clearance. Mechanics ideas can be independently re-expressed but trademarks, prose and protected expression need audit (#569). Source entry points: https://cwn.quadrifons.com/ ; https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/ ; https://fate-srd.com/ ; https://www.apocalypse-world.com/ ; https://www.drivethrurpg.com/ (check actual editions/licences before reproducing anything).

**Recommendation:** keep A as the active baseline, trial B *only after explicit author choice* in #716, reserve C1/C2 for a separate versioned migration issue. PbtA consequences, Fate tags and The Veil identity questions may enrich scenes while preserving the OSR probability engine. This document makes no canonical or code changes.
