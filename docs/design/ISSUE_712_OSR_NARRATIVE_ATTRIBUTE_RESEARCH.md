# #712: OSR chassis, narrative overlays and mental-heavy attributes

**Status:** comparative research only. No rules, saves, data formats or character sheets change. **Authority:** `rulebook/WITHOUT_NUMBER_BASELINE.md`, `data/rules/without_number.json`; investigation is separately implemented in `src/rules/investigation.py` (#704, PR #711). The earlier #710 record provisionally retains A; #716 explicitly reserves the author decision.

## Subsystem fit and limits

| Source | Useful problem-specific idea | Proposed boundary / risk |
|---|---|---|
| CWN / SWN | 3–18 attributes, 2d6 skills, d20 combat/saves; SWN psychic skill and Effort; faction turn | **Keep** as resolution authority; PSI training is not an attribute |
| GUMSHOE SRD | Core observations follow competent, plausible inquiry; actions and optional benefits may cost | #704 already covers this; avoid point spends and a second investigative ability list |
| PbtA | Consequence prompts, progress clocks, escalating GM responses | Clock records established consequences, not a second 2d6 move engine |
| Fate | Situation aspects and meaningful choices/compels | A descriptive tag need not give a Fate point or reroll |
| The Veil | Emotional condition, identity and perception of mediated reality | Emotion should affect fictional positioning, not replace attributes or diagnose truth |
| Trail/Call of Cthulhu | Exposure, shock, uncertainty and recovery | Never equate psychiatric distress with proof of paranormal events or moral failure |
| Eclipse Phase | Forks, identity continuity, memory provenance | Treat as inspiration; do not import large resource economies |

**Source checks:** [GUMSHOE SRD v3](https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/) (CC BY 3.0); [Fate licensing](https://fate-srd.com/official-licensing-fate) (official CC BY SRDs); [CWN SRD introduction](https://www.drivethrurpg.com/) (verify which actual text is included before reuse). Other named games require title-specific permissions review. An idea may inspire original procedures without copying expression. Keep attributions and source provenance; do not suggest endorsement.

## Attribute candidates

| Model | Scores and mapping | Advantages | Main costs |
|---|---|---|---|
| A: canonical six | STR DEX CON INT WIS CHA | Zero migration; unchanged saves and derived quantities | Fantasy-coded player-facing vocabulary |
| B: display aliases | Body Power=STR, Coordination=DEX, Resilience=CON, Reason=INT, Awareness=WIS, Presence=CHA | Same probability and save behavior, clearer near-present tone | Requires one authoritative label mapping, mixed vocabulary risk |
| C6: mental-heavy | FIT=(STR+CON role), REF=DEX, INT=INT, AWA=WIS/perception, PSY=will/integration, SOC=CHA | 2 physical / 4 mental roles; suited to investigation | No independent resilience; new mental save pair, derived HP/load/Strain changes; STR vs CON characters collapse |
| C7: resilience retained | FIT, REF, RES, INT, AWA, PSY, SOC | 3 physical / 4 mental; avoids FIT swallowing durability | Seven scores, changed generation and probability coverage; mental saves need explicit rules |
| Legacy alternative | FIT REF INT SOC PSY CYB | Specific cyberpunk vocabulary | CYB falsely makes equipment into innate power; duplicates System Strain, PSI skill/Effort |

**Recommendation for later author decision:** B is the least disruptive expressive change; A is the current authority until #716 records a new author decision. C6/C7 are genuine rules redesigns, not mere aliases. **SCIENCE stays a Know/specialist skill, cyberware stays equipment, and PSY is not the SWN psychic skill or Effort.**

### Compatibility audit before any C migration

- **Character generation:** decide how six 3–18 scores are produced and what happens to old saves. Never derive new 3–18 scores by adding two old scores without a specified distribution.
- **Saves:** current Physical STR/CON, Evasion DEX/INT, Mental WIS/CHA. C6 could propose Physical FIT/REF, Evasion REF/INT, Mental PSY/SOC, but double-weights REF and loses a resilience axis. C7 could instead propose Physical FIT/RES, Evasion REF/INT, Mental PSY/SOC while AWA has no direct save: deliberately audit the asymmetry.
- **Derived stats:** audit hit points, encumbrance, initiative, System Strain, trauma, equipment prerequisites, psychic effort, NPC lines, progression and AI/nonembodied entities. Do not assume new names retain modifier distributions or source-rule semantics.
- **Computational tests:** assert every saved/check attribute is valid, save-pair membership, all six source score probabilities, zero unhandled NPCs, old-character load behavior, and round-trip schema migration if a C variant is ever selected.

### Worked adjudications, unchanged 2d6 chassis

At 2d6+skill+modifier against difficulty 8, a trained rank-0 investigator with modifier +1 succeeds on a die total >=7: 21 of 36 outcomes (58.3%). With +0 the same test succeeds on >=8: 15 of 36 (41.7%). **These are for consequential actions, not core-clue discovery.**

1. Romppainen with access and Notice 0 sees the ward's amended roster automatically; a risky effort to photograph it before security intervenes uses 2d6 + Notice/appropriate attribute. Source and interpretation remain separate.
2. A hacker with Program 1 can read an authorized exposed terminal clue; an intrusion against a protected network follows CWN hacking, not an extra "cyber attribute" check.
3. A qualified researcher uses Know to interpret a result, a cyborg uses the same skill while cyberware and Strain remain equipment/derived effects, and a pure AI needs a specific embodied/virtual interface policy rather than forced CON.
4. A natural psychic must possess SWN training/techniques and commit Effort; a BCI user has a technological channel, not automatic telepathy. A noetic entity needs capabilities and interaction permissions specified by scenario.
5. A faction's ideological action belongs to the faction turn, not a leader's solitary SOC roll. See #719.

## Two independent tracking axes worth prototyping, not canon

**Insight** records *how many discriminating observations the party can compare* (0–3, with an evidence reference for each increase). **Stability** records immediate capacity to function and access care/resources (0–3, recoverable); high Insight does not establish any interpretation, and low Stability does not validate one. Avoid moral grading and clinical labels. Neither is an ability score or a source of psychic power. Compare a zero-track version first.

## Future decision and playtest gates

1. #716: author selects A/B/C; if C, exact names, saving throws and rebuild-versus-migrate policy first.
2. #717: run real people through the same Lakkahaltia graph twice, with and without optional outcome bands. Count clues per scene, discovery/action/consequence rolls, actual optional benefit payments, hypotheses preserved, gate discriminators and GM bookkeeping minutes. **No synthetic table result counts as a playtest.**
3. #718: keep one graph contract and verify access, scene reachability, discovery and save/load across the runtimes.
4. Only after those decisions, propose bounded trials of Insight/Stability, descriptive aspects and progress clocks, compared against a CWN-only control. Do not canonise by writing this memo.
