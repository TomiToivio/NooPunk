# Phase 1 supplement: Law of One × Without Number compatibility

**Issue:** #1124. **Status:** research and design comparison only, **not approved rules or an implementation**. This is a supplement to the canonical [generated Phase 1 inventory](RULES_INVENTORY.md), not a competing inventory. The inventory source of truth is `data/law_of_one/rules_inventory.json`; do not hand-edit its generated markdown. Compare against [Without Number baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md), [CWN implementation audit](../rules/CWN_COVERAGE_1068.md), and [engine architecture](../architecture/ADR_1054_ENGINE_AGNOSTIC_CORE.md). Keep the **Law of One RPG rulebook separate** from NoöPunk's `RULEBOOK.md`, and do not change the published CWN core. No reskin now.

## Decision framework

- **Existing:** the specialist WN source actually defines an applicable *mechanical procedure*. This does **not** mean it implements the Law of One philosophy or is necessarily complete in NoöPunk code.
- **Partial/analogue:** WN covers the action or consequence but not its noetic meaning, eligibility or group state.
- **Missing:** a Law of One-specific lightweight extension is necessary.
- **OSR addition:** concrete effect with cost, timing, duration, target, limit and published action/saves/damage where applicable.
- **Narrativist addition:** tags, catalyst reflection, story permissions, shared progress and scripted events without new skill or attack checks.
- **Narrative only:** no mechanical requirement.
- **Never combine the strongest mechanics from SWN, WWN and AWN to bypass their separate class, resource or progression prerequisites.**

## 1. Coverage of Law of One concepts by source rules

| Law of One domain | CWN | SWN Revised | WWN | AWN | Gap & proposed treatment |
|---|---|---|---|---|---|
| Physical body, injury, resistance | **Existing:** HP, combat, Shock, Trauma, saves, healing, System Strain | — | — | **Existing:** survival hazards | **OSR:** optional Red-ray mitigation power; apply after CWN damage rules, never replace HP/Trauma |
| Ordinary actions and social skills | **Existing:** attribute/skill checks, Talk, Lead, Know, Notice, Heal, etc. | — | — | crisis social encounters | **Tags:** permissions and consequences, not new skills |
| Psychic energy expenditure | — | **Existing:** psychic Effort, scene/day commitments, overexertion | **Existing:** Arts Effort, distinct spell resources | Possible Mentalist option (deluxe; verify source) | **OSR:** Chakra pools inspired by *commitment*, but do not overwrite imported Effort |
| Empathy, telepathy, mind contact | CWN social context only | **Existing:** Telepathy and Metapsionics techniques | — | Mentalist candidate | **OSR:** gate imported effects by their published packages; **tags:** StO purpose/consent |
| Telekinesis / psychic protection | Saves and ordinary consequences | **Existing:** Telekinesis, Metapsionics | — | Mentalist candidate | Prefer SWN native effects; only add Law of One attunement where a missing effect is demonstrated |
| Psychic healing | **Existing:** injuries and System Strain | **Existing:** Biopsionics | **Partial:** Healer Arts | Medical/crisis conditions | **Tags:** consent, green-ray harmony, service catalyst; **no duplicate healing roll** |
| Adept practice, White Magic, rituals | — | Psychic discipline is not all magic | **Partial/Existing:** spellcasting, Arts, Workings | — | **OSR:** Law of One intention/attunement prerequisites for new effects; **tags:** symbolic ritual and ethical outcome |
| Archetypical Mind and contemplation | — | — | Magic is not equivalent | — | **Tags:** optional archetypal prompts, no class |
| Meditation and balancing | Rest rules don't model spirituality | Effort recovery is mechanical analogue | Effort recovery analogue | Recovery analogue | **Tags/procedure:** reflection, ray block/strain changes; do not let it freely refill published Effort |
| Chakra centers, red through indigo | No analogue | Effort is **resource analogue** | Effort is analogue | — | **OSR:** six independent pools and named attunements; **tags:** blocked/imbalanced. Violet is holistic register, not a pool |
| Mind/body/spirit complex | Ordinary body statistics only | Psychic abilities partial | Spirit/magic analogues | — | **Tags:** integrated metaphysical profile, not three replacement attributes |
| Prana/vital/intelligent energy | System Strain is **not** prana | Effort is **not automatically** prana | Magical Effort **not automatically** prana | — | Choose **one cost per activation**: Chakra for native mod effect, published Effort for imported power |
| Polarization (StO) | No ethical track | No equivalent | No equivalent | No equivalent | **Narrative score:** 0–10 proposal, at 0 positive-path PC → NPC with advance warnings; failures ≠ evil |
| Fourth-density Awareness | No equivalent | Psychic advancement is about technique, not density | — | — | **Narrative score:** 0–10 proposal, experience/integration and perception permissions |
| Catalyst, integration, distortions | Mission XP/ordinary outcomes are not equivalent | — | — | — | **Tags/procedure:** stakes → free choice → consequences → reflection → rare score/tag change |
| Free Will / service ethics | Roleplay baseline only | — | — | — | **Narrative procedure:** respecting agency and consent, no morality saving throws |
| Astral Projection | No core analogue | Teleportation is **not** astral projection | Otherworld exploration and magical movement **partial** | Exploration procedures | **OSR-lite:** required attunement, body anchor, projected state, accessible region, return; **tags** for consequences |
| Time/Space, inner planes | No core analogue | Space travel ≠ Time/Space | **Partial:** site/wilderness exploration | **Partial:** exploration | **Tags/scene rules:** realm, conditions, boundaries, temporal correspondence. No duplicate travel engine |
| Ectoplasm / astral manifestation | Combat remains normal on physical layer | — | Partial supernatural effects | — | **OSR permission:** bounded physical interaction tied to astral state and named cost |
| Higher Self, Veil, Wanderers | Background analogues | **Do not enable SWN Precognition** for this mod | — | — | **Scripted tags:** memory, dream, past-life clue, guidance; precognition never player-activated |
| SMC telepathic connection | No collective consciousness | **Partial:** Telepathy | — | — | **Narrative:** individual connection score, consent, shared knowledge/memories |
| SMC development | Party organization not SMC | **SWN Faction** models political assets, **not** collective mind | **WWN Major Projects** support material ventures | **AWN Enclaves** support settlements | **Narrative:** shared SMC sheet, 4-stage progression and rupture/reconciliation; three scales remain distinct |
| Harvest / demography | — | Faction activities only | Major Projects only | Crisis and enclave transitions | **World-state tags:** quarantine ended, new births, demographic phase-out, reincarnation setting, migration, SMC emergence |
| Confederation, Orion, immigrant populations | NPCs only | **Existing:** faction/sector/space operations | — | — | **World data and NPCs:** faction ≠ species ≠ density ≠ SMC; no new player races |
| Density and visibility | No density track | No density track | — | — | **Tags:** fixed fourth-density human PC, ordinarily physically visible. Previous Quarantine stealth via equipment/secrecy; astral nonmanifestation is separate |

**Important qualification:** “Existing” identifies the relevant published-source procedure, **not guaranteed current Python parity**. The repo's canonical audit identifies verified, partial, missing and provisional WN work. Check each invoked API and source edition before implementing the mod. In particular, SWN psychic packages and AWN deluxe Mentalist should be evaluated **as alternatives, never as stackable free upgrades**.

## 2. Recommended hybrid design

### A. Evolution: narrativist only
- **Polarization** (0–10, suggested initial 5; at zero leaves positive-path PC control); no rolls to determine ethical intention.
- **Awareness** (0–10, initial 1) gates noetic comprehension and attunement opportunities, not generic skill bonuses.
- **SMC Connection** (0–10, initial 0) measures the individual's connection to a *named* collective. Keep a separate shared collective progress sheet.
- **Catalyst and Distortions** are transparent tags/reflection beats; do not grind XP or award automatic numerical rewards per deed.

### B. Chakras: the one substantial additional tactical resource
Six spendable pools: red, orange, yellow, green, blue, indigo. **Violet is not spent.**
- Each records **capacity**, **available**, **committed**, and an independent **blockage condition**.
- **Open** = full functioning; **Strained** = some energy unavailable; **Depleted** = zero usable energy, **not automatically Blocked**; **Blocked** = a distinct unresolved metaphysical condition.
- **Spend** energy for a one-off effect; **Commit** energy to maintain an effect for its specified duration. Recovery follows explicit mod timing. Overextending is a separate high-risk permission, never automatic.
- **Attunement** is required to use a new extraordinary effect. Chakra abundance alone does not grant all powers.
- **Red:** resilience / physical embodiment; **Orange:** selfhood / individual interaction; **Yellow:** group roles and social power; **Green:** compassion / empathic support; **Blue:** truthful communication; **Indigo:** adept practice / astral access.
- **No bonus for the entire Chakra score**. Limit special-case bonus to an ability's explicitly written effect.

### C. Mandatory power-format contract (OSR compatibility)
Each Law of One-native ability needs: **Name | center and attunement prerequisite | range/target | action timing (CWN turn action type) | point spend/commit | duration | eligible action/check/save | exact effect | stacking and recovery | source reference | tabletop example and test**. Delegated published abilities preserve **all** their SWN/WWN requirements, resource costs and advancement. Neither Chakra resources nor new access tags waive those requirements.

**Illustrative draft powers (NOT approved balance):**
- **Red: Physical Resilience.** After ordinary CWN damage mitigation, spend 1 Red to prevent **up to 1 HP damage** from one hit; proposed cap 1 per hit until tested. Do *not* also erase Trauma/Shock/major injury unless ability explicitly says so. Declare at an allowed reaction/Instant timing.
- **Green: Empathic Resonance.** Law of One-native minor emotional perception could spend 1 Green; if instead mapped to a published SWN Telepathy technique, use the source Psychic eligibility, effect and **Effort**, not Green cost as well.
- **Indigo: Astral Projection.** Proposed 2 Indigo **committed** while projected; physical anchor, destination constraints, return conditions, optional astral interference tags. No astral combat, omniscient scouting, free teleportation or selectable precognition.

**Critical accounting invariant:** for each activation **use Chakra cost OR native imported Effort, not both by default**. A future full conversion of a specific *whole* psychic/magic package to Chakra accounting needs its own explicit conversion matrix, advancement parity audit and approval. No ‘pay less in either currency’ exploit.

### D. Astral, Higher Self and SMC: lightweight narrative states
- Astral scenes record `embodied/projected/manifesting`, realm `space_time/time_space`, named inner plane, anchor and exit restrictions. Realm ≠ density ≠ geometry; fourth-density PC does not become invisible innately.
- Higher Self / Veil / Wanderer can supply rare authored memories, dreams and relationships; **precognition stays scripted**.
- The collective sheet stores members, consent boundaries, shared memories, emerging purpose, unresolved distortions and stage **0–4**. Progress is earned by consented events and reflection rather than an SWN faction action. A collective may affect an SWN faction, but they are not the same record.
- Harvest is a **decades-to-centuries world-state transition**, not an instant “beam up the souls” encounter. New earthly generations are fourth density by campaign choice; third-density survivors remain visible/embodied and progressively depart through ordinary mortality. No free density invisibility for PCs.

## 3. Adapter architecture

The standalone Law of One rulebook remains separate. A future engine-independent Python package owns **consciousness scores, Chakra pools, catalyst records, astral transitions and SMC state**. Its optional `standalone` adapter uses a very small narrativist uncertainty procedure, while WN adapters delegate conventional outcomes:

1. **CWN adapter:** attributes, skill checks, saves, combat, HP, Trauma, System Strain and action timings stay canonical and unchanged.
2. **SWN adapter:** published Psychic package, eligible techniques, Effort, faction and starship procedures. **Precognition is not offered as a Law of One PC ability**.
3. **WWN adapter:** optionally published magic/Arts/Workings; do not combine overlapping psychic/magic effects for double benefits.
4. **AWN adapter:** hazards, scarcity, Enclave/survival and optionally deluxe Mentalist *instead of* SWN Psychic, not in addition.

The adapter must never reach inside the WN rule implementation to patch source constants. Use published inputs/outputs, and trace chosen source/edition and requirements in both rulebook and Python tests.

**Plausible first playable integration slice:** (1) one Red defensive mitigation, (2) one Green empathic permission or mapped native SWN telepathic technique, (3) one Indigo projection, (4) Catalyst/Polarization/Awareness, (5) a group SMC sheet. Test tabletop examples and automated golden cases for resource use, conversion exploits, blocked/depleted distinction, session transitions, and negative-path handoff.

## 4. Integration decision checklist / gaps

- [ ] Audit exact SWN psychic discipline and Effort API; reconcile techniques and optional AWN deluxe Mentalist with published licensing and source access.
- [ ] Audit WWN High Mage/Healer/Workings interfaces. **Avoid claiming magical Workings are already implemented if the repo has no verified code**.
- [ ] Confirm CWN HP damage mitigation order, Instant timing and Trauma interaction before approving Red Resilience.
- [ ] Decide Chakra pool capacity scaling and recovery timing; test six pools against SWN and WWN resource-accounting overhead.
- [ ] Decide if an imported Psychic/mage class requires source-specific acquisition cost and whether the Law of One add-on is available without an imported class (separate new abilities only).
- [ ] Verify source passages on Chakra meanings, Time/Space and astral bodies before codifying abilities.
- [ ] Keep **all source mechanics unchanged**, host rulebook untouched, and Law of One RPG rulebook separate.
- [ ] Update the **structured Phase 1 inventory source** after accepting specific decisions, then regenerate the inventory. Do not edit generated `docs/law_of_one/RULES_INVENTORY.md` by hand.

**Design outcome:** *CWN for ordinary action and damage, SWN for psychic effects, WWN for rituals and Workings, AWN for crisis civilization, and a small Law of One layer for positive polarization, chakras, astral experience and shared consciousness.* The compatibility matrix is an aid to selecting existing procedures, not a request to rewrite, import or reproduce published book text.
