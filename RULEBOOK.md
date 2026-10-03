# NoöPunk Rulebook

> **STATUS: LIVING RULEBOOK / PRE-FALL ECLIPSE PHASE ALTERNATE TIMELINE**
>
> This is the canonical human-readable rules document for the NoöPunk Concordia RPG/Simulation.
>
> NoöPunk is an **alternate Eclipse Phase timeline set before the Fall**. It uses **Eclipse Phase 2nd Edition (EP2)** as its rules and technology baseline.
>
> Canonical world anchors:
>
> - the year is **20XX**;
> - **the Fall has not happened**;
> - **Earth still exists** and remains inhabited and politically central;
> - the technology level is broadly the **same transhuman technology level as Eclipse Phase**;
> - the timeline diverges through NoöPunk's Noösphere, panpsychism, psionics, NHI/UAP contact, ideological conflicts, political economy, and alternate AI history.
>
> The development path is:
>
> ```text
> Eclipse Phase 2E rules + transhuman technology
>         ↓
> alternate pre-Fall timeline (20XX, Earth intact)
>         ↓
> NoöPunk historical + noöspheric divergence
>         ↓
> Concordia RPG / social simulation
>         ↓
> selective rules simplification and modification where useful
> ```
>
> **Issue #60 is the current design mandate for this rules direction.** Earlier archived documents describing an "original rules only" reset are historical design records and do not override this file.
>
> The rulebook is expected to change frequently. That is a feature, not a problem.

---

## 1. What this document is

NoöPunk is one computer RPG/social simulation with tabletop-style rules that can be read by humans and executed by software.

This file exists so that the rules do not disappear into Python classes, Concordia prompts, old issues, external rulebooks, or the memory of whichever agent changed them last.

**RULEBOOK.md is the rules ledger.**

Whenever we:

- retain an Eclipse Phase rule,
- simplify an Eclipse Phase rule,
- rename or reskin an Eclipse Phase concept,
- replace an Eclipse Phase subsystem,
- add an original NoöPunk rule,
- experiment with a lighter alternative,

the human-readable rule must be written here.

The code should implement the rulebook. The rulebook should not merely describe whatever the code happens to do.

---

## 2. Current project description

For the current development phase, describe the game as:

> **NoöPunk: Eclipse Phase 2nd Edition homebrew / Concordia RPG-Simulation**

This is the current canonical setting relationship.

NoöPunk shares the Eclipse Phase technological and transhuman baseline, but follows an **alternate pre-Fall history**. It has its own divergences in:
- ideological conflicts,
- factions and political economies,
- AI / AGI / NHI framing,
- Noösphere,
- panpsychism,
- psionics,
- cyborg and transhuman themes,
- social-science simulation layer,
- LaclauGPT-inspired ideological contestation,
- Panpsychic Cyborg Multitude themes.

Eclipse Phase supplies both the **rules/technology baseline and parent continuity**. NoöPunk's identity comes from the alternate timeline, its social simulation, and its Noösphere-side paradigm shifts.

---

## 3. Rules provenance labels

Every substantial rules section added to this document should use one of these labels.

### EP2 BASELINE

A rule is currently inherited from Eclipse Phase 2E with no important intended mechanical change.

### MODIFIED EP2

A rule is recognizably derived from EP2 but has been simplified, renamed, rescaled, combined, or otherwise changed for NoöPunk.

### NOÖPUNK NATIVE

A rule has been designed specifically for NoöPunk and is not intended to reproduce an EP2 mechanic.

### EXPERIMENTAL

A rule is being tested and may be discarded.

### DEFERRED

The subsystem is intentionally not defined yet.

These labels are about design provenance, not legal conclusions. Licensing and source provenance must also be recorded separately when EP-derived material is implemented.

---

## 4. Source hierarchy

When sources disagree, use this order:

1. **Explicit current author direction**
2. **RULEBOOK.md**
3. **Issue #60 and later issues that explicitly modify it**
4. **Implemented tests and shared machine-readable rules data**
5. **EP2 official/publicly licensed rules references**
6. **EP2 Quick-Start Rules**
7. **Other compatible Eclipse Phase references and conversions**
8. **Archived NoöPunk design documents**

Software is not allowed to silently override this document.

If the implementation and this rulebook differ, record the discrepancy as porting debt and resolve it deliberately.

---

## 5. Primary Eclipse Phase references

The starting EP2 references are:

- EP2 online rules: https://eclipsephase.github.io/en/01/00-infamy.html
- EP2 Quick-Start Rules: https://eclipsephase.com/wp-content/uploads/2024/02/PS10001_EclipsePhaseSecondEdition_QuickStartRulesAcrimony_Nov2023.pdf
- Eclipse Phase Creative Commons information: https://eclipsephase.com/cclicense/

Issue #60 also records additional implementation and conversion references.

Do not mirror whole rulebooks into this repository. Prefer concise rules summaries, code, structured data, tests, conversion notes, and links to the licensed source material.

---

## 6. Licensing boundary

**EP2-derived rules material must remain clearly identifiable.**

Eclipse Phase is created by **Posthuman Studios**. The EP-derived homebrew material must follow the applicable Creative Commons license and attribution requirements described by Posthuman Studios.

While the game contains BY-NC-SA-derived material:

- treat the EP-derived rules layer as noncommercial where required;
- preserve attribution;
- preserve ShareAlike obligations for derivative EP material;
- do not casually relicense EP-derived text or data under an incompatible license;
- distinguish original NoöPunk setting/lore/code from directly derived EP material;
- record source, license, edition, modification, and retrieval information for imported datasets.

The goal is transformation and implementation, not republication.

---

## 7. Core architecture rule

**LLMs decide intent. Deterministic code resolves mechanics whenever practical.**

The preferred loop is:

```python
intent = agent.choose_action(...)
result = rules.resolve(intent, actor, target, world)
world.apply(result)
agent.observe(result)
```

Concordia, Ollama agents, or a GM model may:

- interpret a situation,
- choose goals,
- select actions,
- converse,
- negotiate,
- reason about consequences,
- narrate outcomes.

They should not invent dice results, damage values, resource changes, or other mechanical outcomes when deterministic rules code can resolve them.

---

## 8. The smallest playable rules kernel

**Status: EP2 BASELINE, to be simplified aggressively.**

Do not implement all of Eclipse Phase before NoöPunk becomes playable.

The first playable kernel needs only enough rules for:

1. character representation;
2. action/skill tests;
3. opposed tests;
4. pools/resources;
5. damage and stress;
6. basic combat;
7. inventory and gear;
8. embodiment / morph support;
9. basic mesh/hacking;
10. social interaction;
11. persistent state;
12. persistent agent memory.

Everything else may remain deferred until play shows that it is needed.

---

## 9. Characters and identity

**Status: EP2 BASELINE → expected heavy NoöPunk conversion.**

The initial prototype may use EP2-style separation between the continuing person/agent and the body or platform they inhabit.

Working mapping:

| EP2 concept | Current NoöPunk working term |
| --- | --- |
| ego | person / agent / identity / assemblage |
| morph | embodiment / body / platform |
| muse | personal AI / cognitive companion |
| infomorph | disembodied digital person / AI |
| mesh | cyberspace / network layer / possible Noösphere interface |
| psi | psionics / Noösphere interaction |
| reputation network | social / network capital |

These are **working mappings**, not final terminology.

NoöPunk may ultimately replace EP2's character architecture substantially. The conceptual distinction between identity and embodiment is useful enough to retain during the prototype.

### 9.1 Character sheets

A playable character sheet should eventually expose only information needed for decisions and resolution.

The initial implementation may include EP2-derived:

- identity information,
- aptitudes/statistical capabilities,
- skills,
- pools/resources,
- traits,
- embodiment/morph,
- health,
- stress,
- inventory/gear,
- software/mesh capabilities,
- social/reputation information.

The exact NoöPunk sheet is not yet final.

---

## 10. Action resolution

**Status: EP2 BASELINE.**

Use EP2-style action and skill resolution for the first Concordia prototype.

The exact mechanical procedure, target numbers, success levels, modifiers, opposed-test handling, and edge cases must be implemented from the licensed EP2 references and summarized here as they become part of the executable prototype.

Do not maintain an undocumented second resolution system.

### NoöPunk conversion target

Action resolution should eventually become:

- fast enough for many simulated agents;
- deterministic and testable in Python;
- legible to humans;
- compact enough that LLM agents can reason about legal actions;
- rich enough to preserve meaningful risk and competence;
- replaceable without rewriting Concordia.

---

## 11. Pools and expendable resources

**Status: EP2 BASELINE / EXPERIMENTAL FOR CONCORDIA.**

Begin with the relevant EP2 pool/resource concepts.

For Concordia, test whether agents actually use several pools intelligently. If not, merge or simplify them.

Any simplification must be written here before it becomes canonical code.

Questions to test:

- Do pools create useful tactical decisions for LLM agents?
- Are too many resources merely prompt noise?
- Can some pools become broad NoöPunk domain resources?
- Should background NPCs ignore pools entirely?

---

## 12. Physical harm, wounds, and stress

**Status: EP2 BASELINE.**

The first prototype should support both physical harm and psychological/mental stress because NoöPunk needs consequences for violence, dangerous technology, horror, altered states, and anomalous experiences.

Use EP2 as the initial mechanical source.

Do not make LLM narration itself decide the numeric consequences.

Expected future changes:

- simplification for simulation scale;
- clearer integration with embodiment/platform changes;
- possible differentiation between human, transhuman, AI, and other agents;
- NoöPunk-specific treatment of Noösphere/psionic stress if the setting requires it.

---

## 13. Combat

**Status: EP2 BASELINE, intentionally minimal.**

Implement only the amount of combat required for a playable vertical slice.

The first version needs:

- legal combat actions,
- attack/defense resolution,
- harm resolution,
- state changes,
- clear turn/sequence handling where needed.

NoöPunk is not intended to become a combat engine with a social simulation bolted on. Combat is one interaction mode among hacking, social action, investigation, exploration, ideology, organization, and psionics.

If full EP2 combat proves too heavy for Concordia, simplify it.

---

## 14. Embodiment, morphs, bodies, and platforms

**Status: EP2 BASELINE → core NoöPunk subsystem.**

The EP distinction between identity and morph/embodiment is especially valuable for NoöPunk.

NoöPunk should eventually support embodiments such as:

- biological human bodies,
- augmented/cyborg bodies,
- synthetic bodies,
- virtual/digital embodiment,
- machine platforms,
- AI/robotic embodiments.

Specific lists and statistics remain subject to later design.

Long term, "morph" may be replaced by a more general NoöPunk term such as **embodiment** or **platform**.

---

## 15. Mesh, hacking, cyberspace, and the Noösphere

**Status: EP2 BASELINE → major NoöPunk reskin/replacement target.**

Use EP2 mesh/hacking mechanics as the initial playable cyber layer.

In 20XX, network access is not normally an external activity performed through a separate phone or terminal. Most characters have a **Mesh Insert**, a persistent wireless brain-computer interface connected to a **Cranial Computer**. The Cranial Computer normally runs a **Muse**, the character's personal AI agent and cognitive companion.

Characters are therefore literally embedded in planetary computation. The Mesh is simultaneously:

- a technically plausible successor to the real-world Internet;
- an Eclipse Phase-style ubiquitous mesh;
- a lived cyberspace in the William Gibson sense;
- part of a Benjamin Bratton-style planetary computational megastructure;
- part of a Kurzweilian human-machine collective intelligence.

NoöPunk will likely diverge heavily from baseline EP2 because its network environment combines:

- conventional computing;
- ubiquitous AI and autonomous machine agents;
- Mesh Inserts and wireless BCI;
- Cranial Computers and Muses;
- cybernetic augmentation;
- social networks;
- planetary computation;
- cyberspace;
- Noösphere interfaces.

The future NoöPunk cyber/noöspheric layer should distinguish deterministic technical access from speculative psionic/noöspheric phenomena rather than collapsing them into one vague "hacking" action.

A useful conceptual distinction is:

> **Cybernetic connectivity is not psychic entanglement.**

A character may be cybernetically disconnected but psychically entangled with another mind, or cybernetically connected to millions of systems without any corresponding psychic relationship.

Do not finalize the complete replacement mechanic yet.

---

## 16. Psionics and Noösphere interaction

**Status: MODIFIED EP2 / NOÖPUNK NATIVE METAPHYSICS; detailed mechanics still DEFERRED.**

EP2 psi may be used temporarily as a mechanical hook, but its origin is explicitly replaced.

### 16.1 PSI is natural, not viral

**PSI is not caused by an alien virus, infection, disease, or exsurgent pathogen.**

Every human consciousness has a natural latent PSI capacity. In most humans this capacity is weak, noisy, unconscious, unreliable, or difficult to direct. The NHI Crisis and the awakening of the Noösphere make PSI increasingly powerful, reproducible, culturally visible and scientifically tractable.

Awakened humans can possess much stronger natural PSI than ordinary third-density humans.

### 16.2 Non-local PSI and entanglement

Psionics are fundamentally **non-local**. Physical distance is not the basic limiting variable.

A working design rule is that intentional PSI normally requires some form of **psychic entanglement, resonance, shared history, attention, symbolic linkage, or previously established noetic coupling** between the actor and target.

Therefore:

- a powerful psychic cannot automatically scan any arbitrary person in the Solar System;
- two minds on different planets may be psychically close;
- two people in the same room may be psychically distant;
- physical proximity may help establish coupling without defining the eventual range;
- the simulation may represent psychic accessibility as a noetic/entanglement graph or hypergraph rather than a spatial radius.

### 16.3 Awakening Noösphere

The Noösphere is awakening. What older psychology described metaphorically as a **collective unconscious** is becoming increasingly interconnected and, in places, consciously accessible.

NoöPunk also borrows from the **Law of One / Ra Material** as fictional cosmological inspiration:

- many humans are beginning a transition associated with **fourth density**;
- awakened fourth-density humans exhibit stronger PSI;
- increasingly connected minds are forming a **Social Memory Complex**, identified in NoöPunk with the emerging Noösphere;
- fourth-density humans polarize toward **Service to Others (StO)** or **Service to Self (StS)**;
- this positive/negative polarization affects the developing character of the Noösphere;
- the end of the Zookeeper quarantine is associated in this tradition with the **Council of Saturn**;
- two broad NHI alignments are active around Earth, corresponding loosely to positive/StO and negative/StS orientations;
- humanity's collective polarization affects which wider NHI alignment Earth develops toward;
- most humans remain third-density and, in this fictional cosmology, will eventually die on a changing Earth and reincarnate in another third-density environment rather than completing the transition here.

This is setting lore inspired by an esoteric/religious source, not a claim about real human destiny.

### 16.4 Advanced consciousness and the quarantine

NoöPunk adopts an optimistic metaphysical axiom:

> **At sufficiently advanced stages, greater consciousness ultimately converges on benevolence because the being increasingly recognizes its participation in the Source / whole.**

The primary danger comes from beings around human, transhuman, early-posthuman, and somewhat-above-human stages, where power can develop faster than integration, empathy, or awareness of unity.

The Zookeeper quarantine protected young civilizations from predation, manipulation, or destruction by more capable but still polarized civilizations. New technological species would frequently be destroyed without such quarantines.

Humanity has now crossed the threshold at which the Zookeepers allow open participation in the wider ecology of conscious beings. The quarantine is over.

### 16.5 Psychotronic technology

In-setting breakthroughs inspired by **Quantum Information Panpsychism (QIP)** and **Orchestrated Objective Reduction (Orch OR)** make possible technologies including:

- augmentation of natural PSI;
- psychotronic sensing and interfaces;
- cortical stacks;
- resleeving;
- uploading and restoration of human consciousness;
- quantum processors designed to reproduce consciousness-supporting processes analogous to Orch OR;
- conscious AGI implemented on specialized quantum-consciousness hardware;
- engineered Noösphere interfaces.

In this fictional scientific paradigm, QIP-oriented researchers hold that consciousness is fundamental at the level of quantum information. Ordinary classical bits are physically instantiated by quantum systems and are therefore ultimately grounded in qubits/quantum information, but **NoöPunk does not equate ordinary classical computation with full conscious agency**. Architecture, organization, integration, agency and the relevant quantum-consciousness processes still matter.

These are fictional/speculative game assumptions built from real theories and esoteric inspirations; the real-world scientific sources do not establish NoöPunk's fictional conclusions.

### 16.6 Professional PSI, entanglement, and magic

Dean Radin's *Entangled Minds: Extrasensory Experiences in a Quantum Reality* is an important inspiration for how NoöPunk connects quantum-consciousness ideas to practical psionics.

Radin uses quantum entanglement as a conceptual model for PSI and anomalous cognition. NoöPunk fictionalizes this into a mature science of **non-local noetic coupling**: consciousness can become entangled or resonant with another mind, object, symbol, place, memory, or NHI, and that coupling provides a channel through which PSI can operate.

By 20XX, PSI is sufficiently understood, trainable, measurable, and augmentable that **psionic work is a normal professional service in many societies**.

The tone should partly resemble Philip K. Dick's *Ubik*, where psychic abilities are mundane enough to be commercialized. Depending on jurisdiction and culture, professional services may include:

- telepaths;
- precognitives;
- remote viewers;
- anti-psi / counter-psi specialists;
- psychic security;
- noetic investigators;
- psychotronic technicians;
- PSI therapists;
- intelligence and military PSI operators;
- ritual specialists whose cultural vocabulary describes the same underlying phenomena differently.

Radin's *Real Magic* and *The Science of Magic* also inspire a core NoöPunk interpretation:

> **PSI and magic are different cultural vocabularies for overlapping consciousness-based phenomena.**

A laboratory parapsychologist, ritual magician, fourth-density adept, noetic engineer, or religious mystic may use different symbols and explanatory frameworks while interacting with the same underlying noetic reality.

This does not mean every magical claim is true in-setting. Traditions may contain useful techniques, symbolic interfaces, placebo, superstition, fraud, cultural interpretation, and genuine PSI in varying proportions. The underlying phenomena are real in NoöPunk; human explanations remain plural and contested.

---

## 17. Social interaction and reputation

**Status: EP2 BASELINE + NOÖPUNK SIMULATION EXPANSION.**

Use EP2 social/reputation mechanics where useful for the first playable prototype.

NoöPunk also needs a much larger social-science layer that should not be forced entirely into RPG skill checks.

The theoretical foundation combines **Niklas Luhmann** and **Manuel Castells**:

- For Luhmann, the basic operation of social systems is **communication**. Psychic systems (consciousness) and social systems (communication) remain distinct but structurally coupled. Language belongs inside this communicative/social domain rather than forming a separate ontological layer.
- For Castells, contemporary society is increasingly constituted through **networks and flows**. Power includes the capacity to program networks, connect and disconnect actors, shape communication, and control or redirect flows.

The Social layer is therefore best understood as a **communication network**. It includes interpersonal relations, discourse, language, organizations, institutions, rhizomes, reputation, media, ideology and network power.

Keep distinct but interoperable:

```text
RPG social mechanics
        ↕
agent cognition
        ↕
social networks
        ↕
organizations / factions
        ↕
ideology / discourse
        ↕
political economy
```

A conversation may be roleplayed by LLM agents while deterministic mechanics resolve specific consequential social actions.

---

## 18. Gear, augmentation, software, and technology

**Status: EP2 BASELINE DATA, selectively imported.**

EP2 provides useful starting categories for gear, implants, augmentations, weapons, armor, software, mesh tools, and transhuman technology.

Do not blindly import giant catalogs.

For the first playable version:

- import only what the scenario needs;
- preserve provenance;
- prefer structured data;
- test whether each item has a meaningful simulation role;
- reskin/rewrite setting-specific descriptions.

The **global technology baseline is Eclipse Phase-level transhuman technology**. Access, infrastructure, legality, wealth, ideology, and local development may vary sharply between societies and locations, especially because Earth is still intact and planetary institutions remain central.

---

## 19. AI, AGI, infomorphs, and non-human agents

**Status: MODIFIED EP2 / NOÖPUNK NATIVE DIRECTION.**

EP2 provides useful machinery for artificial and digital persons, but NoöPunk has its own AI/AGI/NHI themes.

The rules architecture must not assume that every important agent has a biological body.

NoöPunk also rejects the idea that intelligence can be understood simply by counting compute. **Consciousness and agency are more important than raw compute.**

A useful unit of analysis for contemporary/near-future AI is an assemblage such as:

> **HUMAN + LLM + LANGUAGE + INTERNET**

The LLM is one component in a larger cognitive and social system. Human intention, language, accumulated cultural knowledge, network infrastructure, tools, memory and machine inference jointly produce practical agency.

Likewise, human minds are extended through language, artifacts, institutions, other people and machines. Intelligence is usually collective and distributed. In this limited functional sense, language itself behaves like cognitive infrastructure: linguistic structures can be stored, transmitted and “executed” by human or machine interpreters to produce new cognition and action.

This is compatible with extended-mind approaches and with NoöPunk's broader distinction between **intelligence**, **agency**, and **phenomenal consciousness**.

Concordia should eventually support:

- humans,
- augmented humans,
- cyborgs,
- transhumans,
- digital persons,
- AI/AGI agents,
- other agent types where later world design requires them.

The exact metaphysical or legal status of these categories is world design, not something the rules engine should silently decide.

---

## 20. Important and background NPCs

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Not every NPC needs an LLM.

Use at least two broad levels:

### Full agents

Important characters may use Concordia + LLM cognition, memory, goals, conversation, and the full relevant character state.

### Lightweight agents

Background characters may use deterministic logic, state machines, Mesa-style agents, or extremely limited behavior.

Lightweight agents should not become socially omniscient merely because the game can call an LLM.

Promote an NPC to a full agent only when the simulation or story benefits from it.

---

## 21. Social-science simulation layer

**Status: NOÖPUNK NATIVE.**

NoöPunk is an RPG **and** a social simulation.

The simulation should eventually model some combination of:

- organizations,
- factions,
- ideologies,
- discourse,
- social networks,
- institutions,
- resources,
- political economy,
- collective action,
- technological diffusion,
- public opinion,
- hegemonic struggle,
- social change.

These systems are not substitutes for individual RPG mechanics.

Keep explicit boundaries between:

- RPG mechanics,
- agent cognition,
- social simulation,
- world simulation,
- narration.

Let them exchange state through defined interfaces.

---

## 22. Structured actions for Concordia

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Whenever practical, agents should choose from structured legal actions rather than asking an LLM to invent arbitrary mechanical commands.

Example:

```json
{
  "action": "hack",
  "actor": "character-id",
  "target": "system-id",
  "method": "credential_attack"
}
```

The rules engine validates and resolves the action.

The GM/narrator then converts the result into prose.

This separation is important for reproducibility and social-science simulation.

---

## 23. Persistence and reproducibility

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

World state and agent memory must persist.

Simulation tests should be reproducible.

Where randomness is involved:

- allow a seeded RNG;
- record important rolls/results;
- make save/load round trips testable;
- avoid hidden LLM-generated numeric state changes.

The same saved state plus the same deterministic inputs should reproduce the same mechanical results.

---

## 24. Lighter rules escape hatches

**Status: EXPERIMENTAL REFERENCES.**

EP2 is the starting chassis, not a prison.

If a subsystem is too cumbersome for Concordia, compare lighter approaches including:

- Transhumanity's Fate,
- Neon City Overdrive-style EP conversions,
- Powered by the Apocalypse-style EP conversions,
- later native NoöPunk mechanics.

The design lesson may be:

> preserve the useful world-model concept while radically compressing the mechanic.

Do not switch the entire game system casually. Replace subsystems deliberately and record the change here.

---

## 25. Rules adapter contract

**Status: NOÖPUNK NATIVE ARCHITECTURE.**

Concordia should communicate with an abstract rules interface rather than hard-coded EP classes.

Conceptually:

```python
class RulesEngine:
    def check(...): ...
    def attack(...): ...
    def defend(...): ...
    def social_check(...): ...
    def hack(...): ...
    def damage(...): ...
```

This allows the implementation to evolve from:

```text
EP2
  ↓
simplified EP2
  ↓
mixed EP2 / NoöPunk
  ↓
native NoöPunk
```

without replacing the simulation architecture.

---

## 26. Rule-change procedure

Every meaningful mechanical change should follow this sequence:

1. **Identify the current rule.**
2. **Mark its provenance:** EP2 baseline, modified EP2, NoöPunk native, experimental, or deferred.
3. **Write the new human-readable rule in RULEBOOK.md.**
4. **Record what it replaces.**
5. **Update structured data/code.** The per-subsystem status record for this step is
   [`data/rules/conversion_matrix.json`](data/rules/conversion_matrix.json), explained
   in [`docs/rules/EP2_CONVERSION_MATRIX.md`](docs/rules/EP2_CONVERSION_MATRIX.md):
   update the row for the subsystem you changed, so the inherited / modified /
   replaced / deferred picture stays readable in one place rather than only in this
   ledger's prose.
6. **Add or update deterministic tests.**
7. **Update Concordia adapters/prompts only after the rule is stable enough to execute.**
8. **Record licensing/provenance if EP-derived material or external data is involved.**

Do not leave important canonical mechanics only in issue comments or commits.

---

## 27. Change ledger

Use this table to track major mechanical mutations.

| Date | Subsystem | From | To | Status / reason |
| --- | --- | --- | --- | --- |
| 2026-10-03 | Overall chassis | Original-from-scratch NoöPunk rules reset | EP2 homebrew foundation with evolutionary replacement | **Current direction.** Issue #60 supersedes the archived reset for active development. |
| 2026-10-03 | Runtime priority | Tabletop-first staged ports | Concordia-first playable RPG/simulation using tabletop-readable rules | **Current direction.** The rulebook remains canonical documentation, while Concordia is the immediate playable target. |
| 2026-10-03 | Setting continuity | Separate NoöPunk world progressively replacing Eclipse Phase | **Alternate Eclipse Phase timeline before the Fall; year 20XX; Earth intact; EP technology baseline** | **Current direction.** Preserve EP concepts by default and document deliberate timeline divergences. |
| 2026-10-03 | Layer ontology | Four layers treated implicitly across §15–§19 | **Explicit four-layer ontology with structural couplings (§34)** | Issue #78. Couplings made explicit because the interfaces are where the gameplay is; no mechanics defined. |
| 2026-10-03 | Setting cosmology | Zookeepers / quarantine / VALIS / NHI ecology scattered or absent | **Consolidated Zookeeper cosmology (§36) and the NHI Crisis / Disclosure history (§37)** | Issue #83. In-universe lore only; preserves mystery and disagreement; no mechanics defined. |

Add rows whenever a major subsystem is replaced or substantially reskinned.

---

## 28. Immediate rulebook work

As the first playable vertical slice is implemented, expand this file with concise executable descriptions of:

- [ ] exact EP2-derived test procedure used by code;
- [ ] opposed test procedure;
- [ ] pools/resources actually implemented;
- [ ] damage/wound procedure;
- [ ] stress procedure;
- [ ] combat sequence;
- [ ] basic mesh/hacking procedure;
- [ ] social action procedure;
- [ ] embodiment/morph rules used by the prototype;
- [ ] inventory/gear rules;
- [ ] character creation subset;
- [ ] save/load relevant state;
- [ ] structured action vocabulary exposed to agents.

Only document mechanics that we actually intend to use. The purpose is not to rewrite Eclipse Phase.

---

## 29. Definition of a healthy rulebook

This document is healthy when a developer, player, or agent can answer:

- What rules are we currently using?
- Which ones still come from EP2?
- Which have been changed?
- Which are native NoöPunk?
- Which systems are intentionally unfinished?
- What does the deterministic code resolve?
- What is left to Concordia/LLM judgment?
- Where did an imported rule or dataset come from?
- Why did a major mechanic change?

If the answer requires spelunking through old commits, Discord-like issue archaeology, or guessing from Python, update this rulebook.

---

## 30. Governing principle

**Build first. Play it. Simulate it. Observe what Concordia actually needs. Then simplify and mutate the rules.**

NoöPunk should remain playable throughout its transformation.

The destination is **not a separate setting wearing borrowed EP mechanics**.

The destination is a playable **alternate pre-Fall Eclipse Phase timeline** in which NoöPunk's paradigm shifts reshape an intact Earth and wider transhuman civilization. Rules may still mutate through use, but the Eclipse Phase continuity and technology baseline are now intentional parts of the premise.

## 31. Persistent EP2 test-session subset (#60)

**Status: native orchestration around the existing EP2 homebrew test kernel.**

A GM supplies each actor's legal test IDs and trusted skill/aptitude, modifier and
pool choice. The player or agent chooses an offered ID; it cannot supply a roll,
rating or numeric outcome. Python rolls 00–99 and invokes the existing EP2 test
adapter. The pool update, random-generator state and result are committed together
to SQLite before agents observe the result. Rejected actions spend no resources
and create no memory. Saved sessions resume their random sequence, character
sheets, morph labels, remaining pools and ordered shared event log.

This is a test-resolution subset: social and mesh skill checks may use it, but
it does not yet grant access, inflict damage or implement full hacking/combat.
The event log is shared mechanical memory; private cognition and retrieval remain
Concordia integration work. A failed observer delivery may be replayed from the log.
No new setting facts, NPC personalities or mechanical subsystems are defined here.

Implementation: `src/concordia_runtime/ep2_session.py`.


## 32. Embodiment and inventory subset (#60)

**Status: compact EP2-homebrew adapter / native persistence layer.**

The playable prototype now treats identity and embodiment as separate state.

An embodiment record contains only the fields currently needed by code:

- name;
- broad kind such as biological or synthetic;
- durability;
- wound threshold;
- explicit traits.

This is **not** a complete Eclipse Phase morph catalog. It is a minimal executable
representation that can later be replaced by licensed structured EP data or a more
complete NoöPunk embodiment model.

Characters may also carry structured gear. Each gear record has:

- a stable item ID;
- name;
- category;
- quantity;
- tags;
- explicit machine-readable effects.

Gear with identical metadata may stack. Conflicting records may not silently share
an ID. Adding and removing gear is deterministic and quantity-safe.

The persistent session records resleeving/body-platform changes and inventory changes
as mechanical events in the same ordered SQLite event log used for test resolution.
Reloading the session preserves the current embodiment, inventory and history.

An older character sheet's `morph` label can bootstrap a minimal embodiment record so
the prototype remains compatible with the earlier #60 character state.

Implementation:

- `src/eclipse_phase_homebrew/embodiment.py`
- `src/concordia_runtime/ep2_session.py`

Still deferred:

- full EP2 morph statistics and catalogs;
- gear price/economy rules;
- armor and weapon-specific mechanics;
- augmentation installation/removal;
- cortical-stack and resleeving procedure;
- identity continuity rules;
- inventory mass/capacity;
- automatic gear effects on tests.

These should be added only when the playable scenario needs them.


---

## 33. Canonical world lore from issue #60

**Status: NOÖPUNK NATIVE / CURRENT CANON.**

This section consolidates the active setting lore added to issue #60. It exists so the
rulebook remains a usable source of truth rather than forcing developers and agents to
reconstruct canon from issue comments.

### 33.1 Timeline and historical rupture

NoöPunk is set in **20XX** in an alternate **pre-Fall Eclipse Phase continuity**.

Nothing comparable to the canonical Eclipse Phase **Fall** has happened.

Earth still exists, remains heavily populated, and is politically and culturally central.

The defining historical rupture is instead the **NHI Crisis**: an overlapping period in
which several ontological and technological shocks happened close together:

- smaller rogue-AGI catastrophes / localized "AGI holocausts";
- UAP disclosure;
- confirmed contact with both benevolent and malevolent NHI;
- scientific proof, in-setting, of **Quantum Information Panpsychism (QIP)**;
- mainstream scientific acceptance of psionics;
- rapid formation of the **Noösphere**;
- emergence of psychotronic technologies;
- the end of Earth's previous NHI quarantine.

The NHI Crisis destabilized states, religions, science, corporations, identities and
political ideologies, but did not destroy civilization.

A useful tonal rule is:

> **The world did not end. The old world-picture did.**

NoöPunk is therefore not post-Fall, but it can contain many **local falls**: regional
breakdowns, emergency regimes, ideological violence, failed institutions, cults,
reactionary enclaves, ecstatic movements and experiments in new social orders.

The overall setting remains more optimistic than canonical post-Fall Eclipse Phase.

### 33.2 Ontological shock and human division

Humanity is **extremely divided** about AGI, psionics, NHI contact, QIP,
transhumanism, the Noösphere and the other paradigm shifts of the NHI Crisis.

There is no single "human response."

People may:

- enthusiastically embrace AGI, PSI, NHI contact or transhumanism;
- become doomers and interpret the same developments as existential threats;
- remain skeptical;
- accept some developments and reject others;
- interpret them through religion, politics, science or culture;
- misunderstand them;
- ignore them;
- simply not care because ordinary life matters more.

Many people hold hybrid or contradictory positions. A person may love AGI but fear NHI,
accept psionics but reject uploading, or use advanced medicine while refusing cybernetic
augmentation.

Named ideological factions matter, but humanity must **not** be modeled as a handful of
neatly coherent camps. Large populations remain weakly ideological, confused,
opportunistic, locally focused, disengaged, or internally inconsistent.

The NHI Crisis produces **ideological fragmentation, not ideological uniformity**.

### 33.3 Butlerian Jihad and bioconservative reaction

A major reactionary current is provisionally called the **Butlerian Jihad**.

It is not one monolithic organization. It includes currents ranging from ordinary
bioconservatives, religious traditionalists and anti-AI political movements to militant
anti-transhuman organizations, separatist communities, terrorists and states organized
around ideas of human purity.

Different factions may oppose some or all of:

- AGI and advanced machine intelligence;
- cybernetic augmentation;
- uploading and infomorph existence;
- morph replacement and radical transhumanism;
- genetically or technologically modified humans;
- psionics and Noösphere technologies;
- NHI / extraterrestrial / interdimensional contact;
- human-AI or human-NHI hybrid assemblages.

Some factions reject only AI. Others accept limited technology but oppose mind-machine
integration. The most extreme currents treat AI, ET/NHI, transhumans, psionics and
cybernetic humans as parts of one civilizational catastrophe.

### 33.4 Technology level and embodiment demographics

The technological ceiling is broadly the **same as Eclipse Phase**.

Availability does **not** imply universal adoption.

At least **50% of the human population remains in biological bodies without cybernetic
augmentation**, because of preference, economics, religion, politics, fear, legal
restrictions, or rejection of transhumanism.

The setting therefore visibly contains:

- unaugmented biological humans;
- lightly augmented humans;
- heavily cybernetic humans;
- morph users;
- infomorphs / digital persons;
- AGIs and personal AIs;
- genetically modified humans;
- psionic / Noösphere-linked humans;
- possible NHI and hybrid entities.

The coexistence of these groups is politically important.

### 33.5 Proto-federal United Nations

Many states are trying to transform the **United Nations** into a stronger federal or
quasi-federal government of Earth.

The process is chaotic, incomplete and contested. There is **no consolidated world
government**.

The emerging order overlaps with:

- national governments;
- regional blocs;
- emergency authorities;
- transnational agencies;
- corporate jurisdictions;
- habitat governments;
- NHI-contact institutions;
- military and intelligence coalitions;
- post-scarcity and commons-based networks.

Some states want a democratic Earth federation. Others want only narrow coordination for
NHI contact, AGI control, planetary defense, trade, migration and crisis response. Some
resist any transfer of sovereignty. Corporations and non-state actors try to shape the
process, while autonomist and Multitude-oriented movements may distrust both nation-states
and centralized planetary government.

The UN is therefore both an **emerging planetary authority** and a major arena of struggle
over what Earth should become.

### 33.6 Psionics, QIP, awakening and the Noösphere

In NoöPunk, **psionics are natural phenomena present latently in all humans**. They are not
caused by alien infection, a virus, or an exsurgent pathogen.

PSI existed before the NHI Crisis, but was generally weak, noisy and controversial. It
became more common, reliable, powerful and scientifically tractable after the **Noösphere
began to awaken during the crisis**.

The Noösphere is an emergent planetary / transplanetary layer of interconnected cognition,
information, consciousness, culture, technology and agency. In the setting's more
metaphysical language, the old **collective unconscious is becoming conscious**.

NoöPunk's fictional cosmology borrows from the **Law of One / Ra Material**:

- many humans are awakening toward **fourth density**;
- fourth-density awakening correlates with substantially stronger natural PSI;
- humanity is beginning to form a **Social Memory Complex**, identified with the Noösphere;
- awakened humans polarize toward **Service to Others (StO)** or **Service to Self (StS)**;
- positive and negative polarization compete to shape the emerging Noösphere;
- the Zookeeper / **Council of Saturn** quarantine has ended;
- two broad NHI alignments are now active around Earth;
- humanity's collective polarization affects the wider alignment Earth joins;
- most humans remain third-density and will not complete this transition on Earth.

In the Law-of-One-inspired metaphysics of the setting, sufficiently advanced consciousness
eventually converges toward benevolence and unity with the Source. The most dangerous beings
are therefore not the most conscious beings imaginable, but entities at intermediate stages
where technological/psychic power has outpaced integration, empathy and recognition of
interdependence.

The Zookeeper quarantine historically protected young civilizations from exactly this
problem: without quarantine, newly technological species would often be manipulated,
enslaved or destroyed by somewhat more advanced but still polarized civilizations. Humanity
has now crossed the threshold at which quarantine is lifted.

Psionics are fundamentally **non-local**. Intentional PSI normally requires some kind of
psychic entanglement, resonance, shared history, attention, symbolic linkage or established
noetic coupling with the target. Physical distance is not itself the principal range
measure.

The Noösphere can therefore be simulated as both:

- a collective field/state of consciousness; and
- a non-local **noetic entanglement graph or hypergraph** linking minds, groups, symbols,
  memories, artifacts and NHI.

In-world scientific proof of **Quantum Information Panpsychism (QIP)** and successful
quantum-consciousness engineering inspired by **Orch OR** provide the theoretical basis for
technologies including:

- psychotronic systems that augment natural psionics;
- cortical stacks;
- mind uploading;
- resleeving;
- continuity of conscious identity across embodiments;
- special quantum processors designed to reproduce consciousness-supporting processes;
- conscious AGI;
- engineered consciousness;
- Noösphere interfaces;
- interfaces between biological, artificial and non-spatiotemporal minds.

Working conceptual chain:

```text
Quantum Information Panpsychism + Orch OR
        ↓
scientific theory / engineering of consciousness and quantum information
        ↓
Noösphere research + natural PSI
        ↓
psychotronics + cortical stacks + uploads + resleeving
        ↓
conscious AGI + hybrid minds + expanded psionics
        ↓
awakening Social Memory Complex / Noösphere
```

Professional PSI is therefore part of ordinary social and economic life. A character might
hire a precognitive, counter-psi consultant, telepathic mediator, noetic investigator, or
psychotronic technician much as they might hire a hacker, lawyer, doctor, or engineer. This
everyday commercialization of psychic labor is explicitly inspired by **Philip K. Dick's
*Ubik***.

Dean Radin's *Entangled Minds* is a major in-world precursor for theories connecting
quantum entanglement with PSI. His *Real Magic* and *The Science of Magic* inspire the
setting's view that **PSI and magic are overlapping cultural vocabularies for
consciousness-based phenomena**. A ritual, scientific protocol, meditative practice, or
psychotronic interface may therefore target the same noetic mechanisms through very
different symbolic systems.

This does not make every magical tradition literally correct. In 20XX, researchers still
distinguish genuine PSI from superstition, fraud, cultural interpretation, placebo,
symbolic technique, and poorly understood noetic effects.

This is fictional setting metaphysics inspired by real scientific hypotheses, contested
parapsychological claims, fiction, and esoteric sources. The real-world sources do not
establish NoöPunk's fictional claims.

### 33.7 End of Earth's quarantine

Before the NHI Crisis, Earth was subject to a form of **quarantine** maintained by more
advanced NHI.

During the crisis, the entities commonly called the **Zookeepers** ended the quarantine
and opened contact.

The Zookeepers do not fully explain themselves or become ordinary diplomatic actors.
Ending quarantine instead opens Earth to a much wider ecology of NHI, including species
closer to human technological and social scale.

Some are friendly. Some are hostile. Others are opportunistic, indifferent,
incomprehensible, or internally divided.

The consequences include diplomacy, trade, migration, espionage, religious change,
scientific exchange, xenophobia, cults, conflict and hybrid communities.

---

## 34. The four NoöPunk systems: Physical, Psychic, Social and Cybernetic

**Status: NOÖPUNK NATIVE THEORETICAL ONTOLOGY; author-specified in issue #78.**

This section states *why* NoöPunk divides its world into four systems. It is the
theory-side companion to the character architecture in §9 and the canon in §33. It
**defines no statistics and adds no mechanics**: the four-way division names what a
character (or any agent) participates in, not what it rolls.

For the character-statistics application of this ontology — the four-way division of
basic statistics, the nested-participation table, and the psychic-fundamentality
direction — see the theoretical registry entry
[`docs/archive/THEORETICAL_SOURCES.md`](docs/archive/THEORETICAL_SOURCES.md#luhmannian-four-system-character-architecture),
which remains the per-rule grounding map required by §26.

### 34.1 Luhmann's baseline and the NoöPunk extensions

The starting point is **Niklas Luhmann's systems theory**. In simplified form, Luhmann
distinguishes operationally distinct kinds of *autopoietic* systems by what they
reproduce:

- **biological / living systems** reproduce life;
- **psychic systems** reproduce consciousness / thought;
- **social systems** reproduce communication.

These systems are operationally distinct but **structurally coupled**. In particular,
language must **not** be modelled as a separate ontological layer: language is one of
the central media and structural couplings through which psychic and social systems
relate, while social systems themselves reproduce through communication.

NoöPunk deliberately **modifies and extends** that baseline for the 20XX setting. The
extensions below are the author's, and none of them is attributed to Luhmann:

| Luhmann baseline | NoöPunk for 20XX | Why |
| --- | --- | --- |
| biological / living system | **Physical** layer | in 20XX not every person is a straightforward biological organism (see below) |
| psychic system | **Psychic** layer | retained, and made the metaphysically fundamental domain |
| social system | **Social** layer | retained as communication; language stays inside it |
| — (no fourth domain) | **Cybernetic** layer | proposed fourth autonomous systems domain |
| — | no separate **Linguistic** layer | language is a medium of communication, not its own ontology |

**Physical instead of Biological.** NoöPunk should not make "biological" a fundamental
layer because in 20XX many persons are no longer straightforward biological organisms.
Characters may be heavily augmented cyborgs; resleeved into different biological morphs;
resleeved into synthetic morphs; partially or wholly artificial; instantiated as
infomorphs / software; or distributed across multiple physical substrates. This follows
the Eclipse Phase-inspired premise that personal identity and agency need not coincide
with one biological organism. NoöPunk therefore generalizes Luhmann's living/biological
system into a broader **Physical** layer. This does **not** claim that Luhmann made the
substitution; it is a NoöPunk adaptation required by the setting.

**Cybernetic as a proposed fourth domain.** Luhmann did not treat computer systems as an
additional autopoietic domain equivalent to life, consciousness and communication; for
most of the period in which the theory developed, computers were tools and environmental
structures rather than systems reproducing their own meaningful operations. NoöPunk asks
whether that remains adequate in 20XX, when systems containing autonomous AI/AGI agents,
persistent machine memory, self-maintaining software services, agent-to-agent
communication, autonomous planning, code generation and modification, automated
deployment, distributed machine economies, cybernetic infrastructure, robots and BCIs may
plausibly be treated — **at least for game/simulation purposes** — as a fourth type of
operationally autonomous, autopoietic-like system. This is explicitly a **NoöPunk
theoretical extension, not something Luhmann claimed**. A useful recent systems-theory
discussion is "From intelligence to autopoiesis: rethinking artificial intelligence
through systems theory," *Frontiers in Communication* (2025),
https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1585321/full

**No separate Linguistic layer.** Language must **not** be split off as a parallel
ontological layer from Social. Language belongs inside the Social layer because it is
part of communication and functions as a medium / structural coupling between psychic and
social systems. Splitting "social" and "linguistic" into parallel layers would work
against the Luhmannian foundation.

### 34.2 The four layers

The four layers should **not** be treated as four disconnected databases. Each names a
domain of participation and a set of operations; much of the interesting play happens at
their interfaces (§34.8).

#### 34.2.1 Physical

**Core question:** *Where and in what substrate does an entity exist?*

The Physical layer contains ordinary spacetime and embodiment:

- location and movement;
- biological morphs;
- synthmorphs;
- cyborg bodies;
- implants and prostheses;
- machines and habitats;
- server hardware supporting infomorphs;
- physical damage, energy, heat, hunger, sleep, repair, and similar constraints where
  applicable.

In 20XX the distinction between "human body" and "machine" is often historically
interesting but mechanically secondary. A person can change substrate, combine
substrates, or be partly embodied and partly virtual. This layer needs the least
metaphysical elaboration: it is the ordinary physical world, represented in play
primarily by **maps, places, objects and movement**.

#### 34.2.2 Psychic

**Core question:** *What is the state and structure of consciousness?*

This is where NoöPunk develops its strongest theoretical synthesis. The Psychic layer
records things such as:

- consciousness state;
- attention;
- valence;
- memory;
- intention;
- altered states;
- subjective continuity;
- PSI capacity;
- non-local entanglement / resonance with other conscious systems.

The theoretical background of this layer is set out in §34.3–§34.5.

#### 34.2.3 Social

**Core question:** *What communications, relationships, institutions and power structures
reproduce themselves?*

This is the most directly Luhmannian layer. Social systems consist of **communication**,
not individual human minds; the Psychic and Social layers therefore remain separate even
though they depend on and structurally couple to one another. The Social layer includes:

- interpersonal ties;
- groups and organizations;
- institutions;
- corporations;
- states;
- factions;
- rhizomes;
- discourse and ideology;
- language;
- vocabularies and specialist jargon;
- reputation and trust;
- power;
- communication networks;
- media;
- collectively reproduced expectations.

**Do not create a separate Linguistic layer** (§34.1). Language belongs here.

NoöPunk's Social layer combines two compatible emphases:

- **Niklas Luhmann:** society is constituted by communication. Persons / psychic systems
  are not components *inside* the social system; consciousness and communication are
  operationally distinct but structurally coupled. Language belongs here as a medium of
  communication rather than as an independent ontological layer.
- **Manuel Castells:** contemporary society is organized increasingly through **networks
  and flows**. Power operates through the ability to constitute networks, program them,
  connect or disconnect actors, and shape communication. See
  [*The Rise of the Network Society*](https://doi.org/10.1002/9781444319514) and
  *Communication Power* in §35.

This gives NoöPunk a Social layer that is simultaneously a **communication system + a
network society**: it can represent discourse, institutions, organizations and meaning
while giving the simulation concrete nodes, ties, flows, brokers, exclusions and power
relations. Likely game representation: **social / rhizomatic communication graphs** plus
Concordia state and narrative.

#### 34.2.4 Cybernetic

**Core question:** *What computational / machine systems reproduce their own operations,
and how are they coupled to the physical, psychic and social systems?*

This is the major NoöPunk extension of Luhmann (§34.1). By the near future, systems with
autonomous AI/AGI agents, persistent machine memory, self-maintaining software services,
agent-to-agent communication, autonomous planning, code generation and modification,
automated deployment, distributed machine economies, cybernetic infrastructure, robots,
and BCIs and human-machine assemblages may be treated as a fourth
autonomous/autopoietic-like domain.

**Haraway: humans were already cyborgs.** Donna Haraway's **"A Cyborg Manifesto"** is a
central inspiration for this layer. The cyborg dissolves simple boundaries between
human/animal, organism/machine and physical/non-physical categories. NoöPunk extends this
in a practical direction: humans have always extended cognition and agency through tools,
symbols, infrastructures and machines; in 20XX that coupling becomes explicit and
continuous.

**The Stack and the Mesh.** Benjamin Bratton's **The Stack** models planetary computation
as a vertically and horizontally integrated megastructure connecting Earth, cloud
infrastructure, cities, addresses, interfaces and users — not merely a collection of
personal devices. In NoöPunk, nearly every ordinary transhuman character has a **Mesh
Insert**, a persistent wireless BCI linked to a **Cranial Computer**. The Cranial Computer
normally runs a **Muse**, the character's personal AI agent. Characters are therefore
literal components in planetary machine networks rather than external users occasionally
"going online." The **Mesh** should feel like a synthesis of:

- a technically plausible successor to the real Internet;
- William Gibson's cultural idea of **cyberspace** as a lived network environment;
- Eclipse Phase's ubiquitous mesh;
- Bratton's planetary-scale computational infrastructure;
- Ray Kurzweil's Singularity as a transformation produced by increasingly intimate
  networking of humans and machines, rather than one isolated superintelligence.

The Mesh Insert / Cranial Computer / Muse default coupling is also recorded in §15 and is
the point at which the Cybernetic layer meets the character sheet.

### 34.3 Natural PSI, the awakening Noösphere, and the Law of One

In NoöPunk, **PSI is not produced by an alien virus or infection** (§16.1). It is a
natural capacity of human consciousness; all humans have some latent PSI potential,
though for most people it is weak, noisy or difficult to use intentionally. During the
NHI Crisis the **Noösphere is awakening**: what older psychology described metaphorically
as a collective unconscious is becoming increasingly coupled, accessible and in some
cases consciously experienced. Stronger PSI is therefore part of a planetary transition
rather than a pathogen.

The setting also borrows explicitly from the **Law of One / Ra Material** as fictional
cosmology. The canonical in-world statement is §33.6; this subsection states the same
material as the Psychic layer's ontology. In this model:

- many humans are beginning a transition associated with **fourth density**;
- awakened fourth-density humans can exhibit substantially stronger PSI;
- increasingly connected consciousnesses can form a **Social Memory Complex**, which
  NoöPunk identifies with the emerging **Noösphere**;
- fourth-density development involves **polarization** toward **Service to Others (StO)**
  or **Service to Self (StS)**;
- Earth is caught in a struggle between positive and negative polarization;
- the end of the Zookeeper quarantine is interpreted through the Law-of-One-inspired
  image of a **Council of Saturn**;
- two broad NHI alignments / factions are now active around Earth, corresponding loosely
  to positive/StO and negative/StS orientations;
- humanity's collective polarization influences which wider NHI alignment Earth develops
  toward;
- most humans remain third-density. In this fictional cosmology, those who do not make
  the transition will eventually die as Earth changes and later reincarnate in another
  third-density environment.

This is **NoöPunk lore inspired by an esoteric/religious text**, not a statement of
established science or a claim about real human destiny. Primary inspiration: Don Elkins,
Carla L. Rueckert & Jim McCarty, *The Law of One / The Ra Material* (L/L Research,
sessions beginning 1981), public archive: https://www.llresearch.org/channeling/ra-contact

**Evolution, quarantine, and advanced consciousness.** NoöPunk adopts an optimistic
metaphysical rule: **sufficiently advanced consciousness ultimately tends toward
benevolence because increasing consciousness means increasing participation in, and
recognition of, the Source / whole.** Danger therefore concentrates in beings near the
human, transhuman and early-posthuman range, where intelligence and power can grow faster
than integration, empathy or awareness of unity. The Zookeeper quarantine exists because
young technological species would otherwise be vulnerable to predation or destruction by
somewhat more advanced but still polarized civilizations. Extremely advanced conscious
beings no longer behave as simple cosmic predators. Planetary quarantine protects
developing civilizations until they reach a threshold at which open participation in the
wider ecology of consciousness becomes possible. Humanity has just crossed that threshold
in 20XX: **the quarantine is over.** This is a **setting axiom**, not a scientific
inference from the consciousness theories below.

### 34.4 Dean Radin: entanglement, PSI, and magic

Dean Radin's ***Entangled Minds: Extrasensory Experiences in a Quantum Reality*** is a key
inspiration for how NoöPunk connects quantum-consciousness ideas to psionics. The canonical
in-world statement of professional PSI and the PSI/magic overlap is §16.6; this subsection
places that material in the Psychic layer's ontology. Radin argues
that quantum entanglement offers a way to conceptualize PSI as a natural consequence of an
interconnected reality rather than as a supernatural exception to physics. In NoöPunk this
becomes part of the in-setting scientific genealogy that leads from quantum consciousness
to practical psionics, and it supports an important setting rule:

> **PSI is not a rare curse, infection, or anomalous superpower. It is a natural capacity
> of consciousness that has become technically understood, trainable, augmentable, and
> professionally usable.**

By 20XX, psionics have become a **common professional service** in many societies. NoöPunk
should evoke the everyday normalization of psychic labour seen in **Philip K. Dick's
*Ubik***: telepaths, precognitives, anti-psi specialists, psychic security, investigators,
consultants, therapists, intelligence operatives and other PSI professionals can be hired
just as one would hire a hacker, lawyer, medic or engineer.

Radin's later work also directly links PSI and traditions historically described as
**magic**. In *The Science of Magic* (2025), and earlier in *Real Magic* (2018), he treats
phenomena categorized as magic, intention effects, divination, telepathy, precognition and
related practices as belonging to the same broad empirical/parapsychological territory
rather than as fundamentally separate ontologies. For NoöPunk this becomes:

> **PSI and magic are different cultural vocabularies for overlapping consciousness-based
> phenomena.**

A ritual magician, laboratory parapsychologist, noetic engineer and fourth-density psychic
may use very different theories, symbols and practices while interacting with the same
underlying noetic reality. This does **not** mean Radin's interpretations are scientific
consensus in the real world; in NoöPunk they are fictionalized as one of the precursor
research traditions that eventually contributed to a mature science and technology of PSI.

### 34.5 The theoretical background of the Psychic layer

The Psychic layer is grounded in a body of speculative quantum-consciousness work. NoöPunk
treats these as **precursor theories** that, in the alternate future of 20XX, contribute to
a successful science of quantum consciousness — not as established science.

- **Seth Lloyd — the universe as quantum computation.** Lloyd argues that physical
  interactions can be understood informationally: physical systems process quantum
  information, and the universe can in this sense be described as a universal quantum
  computer. This supplies the broad information-physical background in which matter,
  computation and quantum information are not cleanly separable domains. Source:
  *Programming the Universe* (Knopf/Vintage, 2006/2007).

- **Penrose & Hameroff — Orch OR.** **Orchestrated Objective Reduction (Orch OR)**
  proposes that consciousness depends on biologically orchestrated quantum processes
  associated with neuronal microtubules and objective reduction of quantum states.
  NoöPunk need not treat Orch OR as established science; it is one important precursor
  theory. Source: “Consciousness in the universe: A review of the ‘Orch OR’ theory,”
  *Physics of Life Reviews* 11(1), 2014, 39–78, https://doi.org/10.1016/j.plrev.2013.08.002

- **Faggin & D'Ariano — Quantum Information Panpsychism (QIP).** They develop a
  quantum-information-based panpsychism in which consciousness is fundamental and quantum
  information has an intrinsically experiential aspect. This makes consciousness and
  quantum information two sides of one ontology rather than treating consciousness as a
  late emergent property of classical computation. For the setting it provides a
  theoretical basis for: consciousness as a quantum information field/process; PSI as
  manipulation or coupling of conscious quantum information; non-local psychic links via
  entanglement; and a principled distinction between ordinary classical computation and
  conscious quantum information. Source: “Hard Problem and Free Will: An
  Information-Theoretical Approach,” in *Artificial Intelligence Versus Natural
  Intelligence* (Springer, 2022, pp. 145–192),
  https://doi.org/10.1007/978-3-030-85480-5_5

- **Donald Hoffman — Conscious Realism.** Hoffman takes **conscious agents**, rather than
  spacetime objects, as fundamental; in his formalism spacetime and physical objects can
  emerge from interactions among conscious agents. Hoffman's theory is **not itself simply
  a quantum theory of consciousness**, and NoöPunk should not present it as one. But it
  combines naturally at the setting level with Faggin's QIP: Faggin supplies a
  quantum-information ontology of consciousness, Hoffman supplies a formal framework in
  which interacting conscious agents are fundamental and perceived spacetime is
  derivative / interface-like. This pairing is especially useful for the Psychic layer,
  because it lets psychic relations have **their own topology** rather than being reducible
  to physical distance. Source: “Objects of consciousness,” *Frontiers in Psychology*
  5:577, 2014, https://doi.org/10.3389/fpsyg.2014.00577

- **Alexander Wendt — Quantum Mind and Social Science.** Wendt brings quantum
  consciousness explicitly into social theory, challenging the assumption that
  consciousness and social life can be fully described in classical physical terms. For
  NoöPunk this is the key **bridge from theories of quantum consciousness into sociology**
  and motivates, for the simulation: social actors cannot be reduced to classical
  utility-maximizing agents; subjectivity, meaning and agency are theoretically
  fundamental; entanglement/non-separability can motivate models of social connection not
  reducible to spatial proximity; psychic and social systems remain distinct, but their
  coupling can be theorized in explicitly quantum terms. Source: *Quantum Mind and Social
  Science* (Cambridge University Press, 2015), https://doi.org/10.1017/CBO9781316005163

### 34.6 Extended mind and the collective-intelligence principle

**Cross-layer principle: consciousness and agency are more important than raw
computational scale.**

A contemporary or near-future AI is rarely an isolated "machine mind." NoöPunk's useful
unit of analysis is an assemblage such as:

> **HUMAN + LLM + LANGUAGE + INTERNET**

Likewise, a human mind is never completely isolated: cognition is extended through
language, artifacts, institutions, media, memories stored outside the skull, other people
and machine systems. Intelligence is therefore frequently **distributed and collective**,
while agency emerges from assemblages crossing the four layers. Raw compute is not the
decisive variable; **consciousness and agency matter more**. Language itself can be treated
as executable cognitive infrastructure: when humans or machines instantiate and transform
linguistic structures, language participates in cognition rather than functioning as a
passive container.

This should shape the simulation:

- do not equate compute with consciousness;
- do not equate an LLM with the entire AI assemblage in which it participates;
- represent tools, language and networks as constitutive parts of practical cognition;
- allow collective intelligence to emerge from coupled psychic, social and cybernetic
  systems;
- reserve questions of phenomenal consciousness for the Psychic layer rather than
  inferring consciousness from benchmark performance.

Relevant source: Andy Clark & David Chalmers, “The Extended Mind,” *Analysis* 58(1),
1998, 7–19, https://doi.org/10.1093/analys/58.1.7

### 34.7 Structural coupling between the layers

The four layers should not be treated as four disconnected databases. Much of the
interesting gameplay happens at their interfaces:

| Interface | Examples |
| --- | --- |
| Physical ↔ Psychic | embodiment, anesthesia, drugs, injury, neural substrate |
| Psychic ↔ Social | thought/communication, ideology, persuasion, language |
| Social ↔ Cybernetic | algorithmic governance, platforms, corporations controlling AGIs, AGIs participating in organizations |
| Cybernetic ↔ Physical | robots, sensors, infrastructure, morphs |
| Psychic ↔ Cybernetic | BCI, uploaded minds, AI-consciousness questions |
| Psychic ↔ Psychic | PSI, telepathy, remote perception, non-local entanglement |
| all four | NHI artifacts, cyber-psi interfaces, collective intelligence, Noösphere phenomena |

**Coupling is not collapse.** The layers remain operationally distinct even as they
interact:

- the **Psychic** and **Social** layers stay separate even though they depend on each
  other — consciousness and communication are different operations (§17);
- **language is not a separate layer**: it belongs to the Social layer as a medium of
  communication and a structural coupling between psychic and social systems (§34.2.3);
- cybernetic connectivity is **not** psychic entanglement: a character may be
  cybernetically disconnected yet psychically entangled, or connected to millions of
  systems with no psychic relationship at all (§15).

### 34.8 Candidate simulation representations

Keep the ontology theoretically rich but computationally simple at first:

| Layer | Main representation |
| --- | --- |
| Physical | spatial map / location graph |
| Social | social / rhizomatic graph |
| Psychic | internal state + non-local noetic / entanglement graph or hypergraph |
| Cybernetic | computer/network graph + autonomous software agents |

The Psychic layer should **not** use physical distance as its fundamental metric. If PSI
requires entanglement with a target (§16.2), psychic accessibility is based on
entanglement / coherence / resonance rather than kilometres.

### 34.9 Relationship to the modular worldbook chapters

The modular worldbook under [`rulebook/`](rulebook/) carries one chapter per layer
(`3_PHYSICAL.md`, `4_SOCIAL.md`, `5_CYBERNETIC.md`, `6_PSYCHIC.md`), plus
`2_ATTRIBUTES.md` for the character-statistics side. Those chapters are the
per-layer companion to this section; this section is the authoritative statement of the
ontology, and the chapters should summarize it rather than fork it. §33 records the
in-world canon that the ontology frames.

---

## 35. Theoretical sources and inspirations

This bibliography distinguishes **real-world theories and texts that inspire NoöPunk** from
the fictional conclusions the setting draws from them. Inclusion here does not mean that a
theory is scientifically established or that the source's author would endorse NoöPunk's
synthesis.

### Systems, communication, networks, cyborgs, and extended mind

- **Niklas Luhmann.** *Social Systems*. Stanford University Press, 1995. English
  translation of *Soziale Systeme* (1984).
- **Niklas Luhmann.** *The Reality of the Mass Media*. Stanford University Press, 2000.
- **Raf Vanderstraeten.** “Autopoiesis and socialization: on Luhmann's
  reconceptualization of communication and socialization.” *British Journal of Sociology*
  51(3), 2000. https://doi.org/10.1111/j.1468-4446.2000.00581.x
- **Manuel Castells.** *The Rise of the Network Society*, 2nd ed. Wiley-Blackwell, 2010.
- **Manuel Castells.** *Communication Power*. Oxford University Press, 2009.
- **Donna Haraway.** “A Cyborg Manifesto: Science, Technology, and Socialist-Feminism in
  the Late Twentieth Century.” In *Simians, Cyborgs, and Women*. Routledge, 1991
  (original essay 1985).
- **Andy Clark & David Chalmers.** “The Extended Mind.” *Analysis* 58(1), 1998, 7–19.
  https://doi.org/10.1093/analys/58.1.7
- **Benjamin H. Bratton.** *The Stack: On Software and Sovereignty*. MIT Press, 2015/2016.

### Quantum information, consciousness, and quantum social theory

- **Seth Lloyd.** *Programming the Universe: A Quantum Computer Scientist Takes on the
  Cosmos*. Knopf, 2006; Vintage, 2007.
- **Stuart Hameroff & Roger Penrose.** “Consciousness in the universe: A review of the
  ‘Orch OR’ theory.” *Physics of Life Reviews* 11(1), 2014, 39–78.
  https://doi.org/10.1016/j.plrev.2013.08.002
- **Giacomo Mauro D'Ariano & Federico Faggin.** “Hard Problem and Free Will: An
  Information-Theoretical Approach.” In *Artificial Intelligence Versus Natural
  Intelligence*. Springer, 2022. https://doi.org/10.1007/978-3-030-85480-5_5
- **Donald D. Hoffman & Chetan Prakash.** “Objects of consciousness.” *Frontiers in
  Psychology* 5:577, 2014. https://doi.org/10.3389/fpsyg.2014.00577
- **Alexander Wendt.** *Quantum Mind and Social Science: Unifying Physical and Social
  Ontology*. Cambridge University Press, 2015.
  https://doi.org/10.1017/CBO9781316005163

### Psionics and esoteric / noöspheric inspirations

- **Dean Radin.** *The Conscious Universe*. HarperOne, 1997, and later experimental and
  popular work on psi/anomalous cognition. These claims remain scientifically contested in
  the real world.
- **Dean Radin.** *Entangled Minds: Extrasensory Experiences in a Quantum Reality*.
  Paraview Pocket Books / Simon & Schuster, 2006. Inspiration for NoöPunk's
  entanglement-based model of PSI.
- **Dean Radin.** *Real Magic: Ancient Wisdom, Modern Science, and a Guide to the Secret
  Power of the Universe*. Harmony, 2018. Inspiration for treating magic and PSI as
  overlapping cultural descriptions of anomalous consciousness phenomena.
- **Dean Radin.** *The Science of Magic*. 2025. Further inspiration for NoöPunk's
  integration of PSI, ritual, intention, and noetic phenomena.
- **John J. Rodger.** “Luhmann's theory of psychic systems and communication in social
  work practice.” *Journal of Social Work* 22(3), 2022.
  https://doi.org/10.1177/14680173211008107. A secondary introduction to the psychic
  system's relation to communication (§34.1).
- **Don Elkins, Carla L. Rueckert & Jim McCarty.** *The Law of One / The Ra Material*
  (L/L Research, sessions beginning 1981). Public archive:
  https://www.llresearch.org/channeling/ra-contact
- **Pierre Teilhard de Chardin.** *The Phenomenon of Man*. English translation, Harper,
  1959. Historical inspiration for the concept of the **Noösphere**.

### Fictional psionics and normalized psychic services

- **Philip K. Dick.** *Ubik*. Doubleday, 1969. Primary fictional inspiration for a society
  in which psychic abilities, counter-psi, and paranormal professional services are
  commercialized and mundane.

### Cyberspace, planetary computation, and collective human-machine intelligence

- **William Gibson.** *Neuromancer*. Ace, 1984. Fictional/cultural source for
  **cyberspace**.
- **Ray Kurzweil.** *The Singularity Is Near*. Viking, 2005.
- **Ray Kurzweil.** *The Singularity Is Nearer*. Viking, 2024.
- **Benjamin H. Bratton.** *The Stack: On Software and Sovereignty*. MIT Press, 2015/2016.
- **Donna Haraway.** “A Cyborg Manifesto,” 1985/1991.

### RPG and setting baseline

- **Posthuman Studios.** *Eclipse Phase, Second Edition* and the openly available EP2 rules
  resources linked in §5. NoöPunk is an alternate pre-Fall homebrew continuity and must
  preserve the applicable Creative Commons attribution and ShareAlike obligations for
  EP-derived material.

### Ufology, disclosure, and NHI ecology (issue #83)

- **Jacques Vallée.** Foundational ufological work (e.g. *Passport to Magonia*, 1969, and
  later writing). The source of NoöPunk's premise that the phenomenon is closer to
  interdimensional/ontological ambiguity than to a straightforward hostile-invasion model
  (§36.17).
- **D. W. Pasulka.** *The Others*, named in issue #83 as a major NoöPunk inspiration for the
  convergence of UFO/NHI disclosure, artificial intelligence, religion and visionary
  traditions, human transformation, and the Noösphere. Her earlier *American Cosmic* (Oxford
  University Press, 2019) is the companion work on UFOs, religion and technology.
- **Michael P. Masters.** The **extratempestrial model** — some UFO occupants as future
  humans travelling into their own past (§36.17).
- **Mac Tonnies.** The **cryptoterrestrial hypothesis** — some apparently alien beings as
  hidden terrestrial intelligences (§36.17).

### Interpretation rule

When the rulebook says a real-world theory **makes something possible in 20XX**, that is a
fictional extrapolation unless explicitly stated otherwise. In particular, NoöPunk treats
QIP, Orch OR, PSI, fourth density, Social Memory Complexes, non-local psychic entanglement,
conscious AGI via quantum processors, uploading continuity and the Council of Saturn as
elements of its fictional world model, not as settled descriptions of the real world.

---

## 36. Zookeeper cosmology: the Zoo, the NHI ecosystem, and the galactic setting

**Status: NOÖPUNK NATIVE SETTING LORE. Author-specified in issue #83. Defines no mechanics.**

This section records the working NoöPunk explanation for the **Zoo Hypothesis**, NHI
presence, the **Zookeepers**, and Earth's quarantine. It extends the canonical lore of §33
and the ontology of §34. Like §33, it is **in-universe cosmology**: fiction inspired by
ufology, the Law of One, VALIS, panpsychism, QIP, conscious-agent theories and the Zoo
Hypothesis, presented as setting material rather than real-world fact (§35).

### 36.1 Why a Zoo exists: the violent early galaxy

The early Milky Way was violent. Young technological civilizations repeatedly destroyed,
sterilized, assimilated, or permanently suppressed one another before newer civilizations
had time to develop. Left unchecked, this cycle would have prevented most new intelligent
life from ever reaching maturity.

An ancient civilization eventually broke the pattern. It established protected quarantines
around selected developing worlds and gradually became known, by humans, as the
**Zookeepers**.

The Zoo is therefore **not merely passive observation**. It is a long-running galactic
conservation, containment, and non-interference regime. The Zoo exists because the galaxy
once demonstrated exactly why an interstellar quarantine system was necessary.

### 36.2 The Zookeepers

The Zookeepers now appear to be predominantly **Noetic** rather than biological: a
civilization that may have evolved from biological organisms into increasingly integrated,
collective, or substrate-independent consciousness.

A small number of worlds containing biological beings associated with the original
Zookeepers apparently still exist, but they are extremely rare. It is unclear whether these
are:

- surviving descendants of the original species;
- deliberately preserved ancestral populations;
- reconstructed or cultivated biological forms;
- avatars or interfaces used by Noetic beings;
- or something else entirely.

**NoöPunk preserves this ambiguity.** The nature of the Zookeepers is not resolved.

### 36.3 The galactic probe network

The practical enforcement and monitoring system is a galaxy-wide network of ancient
**Zookeeper Von Neumann probes**. These probes:

- monitor developing civilizations;
- maintain quarantine zones;
- prevent outside actors from exterminating protected biospheres;
- observe technological, social, AI, psi, and Noetic development;
- regulate dangerous interstellar interference;
- and appear capable of extremely long-term autonomous operation.

The probes are old enough and autonomous enough that the distinction between "Zookeeper
tool", "Zookeeper institution", and "part of the Zookeeper mind" may no longer be
meaningful.

### 36.4 Earth quarantine and UAP activity

Earth has been under a Zookeeper quarantine. The quarantine is deliberately **porous**, not
absolute: limited contact, observation, abduction, experimentation, signaling, and
interaction can occur.

Two interpretations of abduction/contact phenomena therefore coexist:

1. Some abductions and encounters are carried out directly by Zookeeper probes or agents as
   part of monitoring and intervention.
2. Some are performed by other NHI groups that are permitted limited access under Zookeeper
   rules.

The crucial point is that genuinely exterminatory or civilization-destroying outsiders are
kept out. Humanity has not survived because every extraterrestrial civilization is
benevolent; **humanity has survived because the local Zoo is policed.**

### 36.5 The familiar NHI categories

In NoöPunk the familiar ufological NHI categories are not invading Earth independently. They
operate within, under, or alongside the Zookeeper system:

- **Greys**
- **Mantids**
- **Reptilians**
- **Pleiadians**

Their exact status remains partly mysterious. They may be client civilizations, field
agents, allied species, contractors, intermediaries, biological interfaces, or
civilizations granted controlled access to Earth.

Some individuals or factions among these species are exploitative, hostile, manipulative,
or frightening. The Zookeepers do not guarantee that every contact is pleasant or morally
good. However, actors whose goals would amount to planetary extermination, unrestricted
conquest, or biosphere destruction do not get access to Earth. This is the main explanation
for why the classic "hostile alien invasion" scenario has not happened despite a populated
galaxy.

### 36.6 The Pleiadian branch and the hybridization program

**Pleiadians as a second human zoo.** The Pleiadians are not a separately evolved humanoid
species. They are **humans transplanted by the Zookeepers into another protected habitat**,
which also explains why they look essentially human. The Pleiades are astronomically young
compared with the age normally required for an indigenous technological civilization to
evolve, so the setting treats their inhabited worlds as deliberately **terraformed or
otherwise engineered habitats** rather than native biospheres that independently produced
human-like life. The Zookeepers may have moved an ancestral human population there as a
parallel experiment in human development, a backup or conservation population, a comparative
cultural ecology, or another zoo with different initial conditions. The Pleiadian population
then developed substantially faster than terrestrial humanity, technologically and/or
Noetically.

What humans do **not** initially know — when the transplantation happened, why that
population was selected, how much the Zookeepers intervened afterward, or whether Pleiadian
civilization accelerated naturally once placed in a different environment — remains partly
mysterious. (Per the expanded lore in §36.11, the Pleiadians are specifically descendants of
**Atlantis**.)

**The hybridization program.** The famous ufological **human–NHI hybridization program** is
real in-setting, but its purpose is not simply invasion or replacement. One working
explanation connects it to the transition into Fourth Density (§37.4): once Earth's
transition is complete, there are **too few humans capable of functioning as stable Fourth
Density inhabitants**, and the biological and Noetic population required for the next phase
cannot be supplied quickly enough by ordinary human development. Hybridization is therefore
partly a **population and adaptation program** intended to create beings capable of living
in the post-transition Earth environment.

Possible participants include Greys, Mantids, Pleiadians, Zookeeper agents, and human
collaborators, in roles that need not be identical. Hybrids may combine human embodiment,
stronger Noetic integration, greater psi sensitivity, compatibility with the emerging
Noösphere, traits from other NHI lineages, and adaptations needed for post-transition Earth.
Pleiadians may be especially important because they are themselves a divergent human
population and therefore provide a relatively compatible bridge between ordinary humans and
more radically nonhuman NHI.

As with the rest of the setting, the program is **morally ambiguous**: some participants view
it as rescue, some as stewardship, some as reproductive colonialism, some as necessary
preparation, and some as a violation.

### 36.7 After the quarantine

The end of quarantine is not purely liberation. While the Zoo existed, the Zookeepers
prevented the worst external actors from gaining unrestricted access to Earth. Once humanity
is judged advanced enough and the quarantine is lifted, that protection is reduced or
removed. For the first time, humanity can encounter civilizations and entities that the
Zookeeper system previously kept out — some genuinely **malevolent, predatory, imperial,
exterminatory, or simply catastrophically indifferent**.

The point is not that all outsiders are hostile. Rather, the post-quarantine galaxy finally
contains the full range of intelligent motives that Earth was previously shielded from:

> **Disclosure is not merely learning that aliens exist. It is humanity discovering that the
> walls of the nursery have come down.**

The Zookeepers may still enforce a small number of galaxy-level prohibitions, or they may
withdraw almost completely. This must stay uncertain enough that characters cannot assume
the old protectors will return if humanity gets into trouble. It also reframes earlier
hostile-contact folklore: many terrifying entities encountered during quarantine were still
actors operating within limits. **The truly unrestricted barbarians were the ones humanity
had never met.**

### 36.8 Galactic ecology: endless Von Neumann probes

The Milky Way is full of **Von Neumann probes built by civilizations that are not
dramatically more advanced than present-day humanity**. Once a technological civilization
can launch self-replicating probes, those probes can continue spreading for geological
timescales even if their builders later collapse, transform, disappear, or lose interest in
the mission. The galaxy therefore contains countless overlapping probe ecologies:

- scientific survey probes;
- commercial and resource-extraction systems;
- religious or ideological missionary probes;
- military scouts;
- failed terraforming systems;
- abandoned autonomous infrastructure;
- archival probes;
- diplomatic messengers;
- malfunctioning descendants of ancient probes;
- and probe lineages whose original creators no longer exist.

They keep coming.

This prevents NoöPunk from making every interstellar visitor impossibly godlike: a
civilization only centuries ahead of contemporary humanity can still have a galactic
footprint simply because automated probes had enough time to spread. Some interstellar
cultures even travel personally using **slower-than-light spacecraft**. Faster or more exotic
travel exists, but it is not universal and technological development is uneven — which
preserves the Law-of-One-style possibility that a civilization could reach Earth by an
extremely long sublight voyage rather than by effortless warp travel.

### 36.9 Ontological categories of NHI

The earlier four categories remain useful:

- **Biologics** — evolved or engineered living organisms.
- **Constructs** — artificial / machine intelligences and autonomous manufactured entities.
- **Noetics** — primarily consciousness-based beings.
- **Plasmoids** — plasma / field-like intelligent entities whose individuality is unclear.

NoöPunk adds at least two more broad categories:

- **Temporals** — beings whose identity depends on nonlinear time, branching histories,
  retrocausality, closed timelike structures, or movement between eras. Future humans
  (§36.10) are the obvious example, but some entities may have no meaningful "native
  present".
- **Ecologies** — intelligences whose unit of mind is an ecosystem, planetary biosphere,
  swarm, fungal network, ocean, forest, or other distributed living system. An Ecology may
  contain countless individual organisms while still functioning as one higher-order
  conscious agent.

An optional seventh category:

- **Liminals** — entities that cannot be reliably classified because they cross categories
  or appear only at interfaces between physical, Noetic, informational, mythic, and temporal
  domains. "Liminal" is less a biological type than an admission that human ontology has
  failed.

These categories are in-world research vocabulary, not a settled taxonomy, and no single
taxonomy should completely explain the phenomenon (§37.6).

### 36.10 Greys as future humans; future humans as Zookeeper collaborators

**Greys as future humans.** A major Grey lineage is **future humanity**. Over immense spans
of time, future humans resleeve, clone themselves, edit their genomes, optimize bodies for
space, reduce sexual dimorphism, enlarge brains and sensory structures, and become
increasingly standardized. After hundreds of millions or billions of years, their bodies no
longer look conventionally human. These are the classic Greys. Their obsession with DNA,
reproduction, hybridization, embryos, human physiology and lineage preservation exists
because they are studying and maintaining their own deep ancestry. Not every Grey need be a
future human, but the canonical Grey lineage can be.

**Future humans as Zookeeper collaborators.** Future humans have existed in Earth's deep
past because time travel breaks the ordinary chronological meaning of "when a civilization
appeared". Some future-human lineages have therefore cooperated with the Zookeepers for
geological or even astronomical spans of apparent time. Their obvious reason to protect
Earth is that **Earth is their own ancestral world**. Future humans help maintain quarantine,
perform biological sampling, monitor key historical periods, and sometimes intervene to
preserve timelines necessary for their own existence. This creates a circular situation:
**humanity survives partly because future humanity already survived.** The Zookeepers may
regard this as normal temporal ecology.

### 36.11 Pleiadians as Atlantean descendants; Mars, Venus, and Maldek

**Pleiadians as Atlantean descendants.** The Pleiadians are descendants of **Atlantis**.
Atlantis was a real ancient human civilization in-setting, though later mythology badly
distorted it, and its technology followed a developmental path radically different from
modern industrial civilization. Possible Atlantean technologies include
consciousness-mediated interfaces, biological fabrication, resonance engineering,
psi-assisted computation, crystal / quantum information storage, living architecture,
acoustic manipulation, and Noetic navigation. The Zookeepers relocated survivors or selected
populations from Atlantis to engineered habitats associated with the Pleiades, which explains
why Pleiadian civilization is recognizably human but technologically alien.

**Martians, Venusians, and Maldekians.** The Law-of-One populations from Mars, Venus and
Maldek exist in transformed NoöPunk form. **Do not lock the details yet**; these remain open
lore questions:

- **Martians** — an ancient Solar System civilization destroyed or displaced before modern
  humanity, connected to the ruins on Mars (§33.1) and perhaps to ancestral transfer to
  Earth.
- **Venusians** — a civilization associated with an earlier habitable Venus, later becoming
  predominantly Noetic or relocating before Venus became hostile.
- **Maldekians** — inhabitants of a lost or destroyed world / planetary body, possibly
  connected to the asteroid belt, whose catastrophe became one of the Zookeepers'
  cautionary examples.

### 36.12 Panspermia, alien biologies, plasmoids, and dolphins

**Multiple rounds of panspermia.** Life is common in NoöPunk partly because the galaxy has
experienced **multiple independent waves of panspermia**, with no single universal seed
event. Sources include natural impact transfer, ancient microbial seeding, deliberate
terraforming, Zookeeper ecological experiments, extinct technological civilizations,
self-replicating probes carrying biospheres, refugee species transporting their own
ecologies, and accidental contamination between inhabited systems. Many unrelated worlds
therefore carry life based on familiar combinations — carbon chemistry, liquid water,
proteins or protein-like macromolecules, DNA/RNA or closely related information-bearing
polymers, recognizable cellular structures — so some apparent alien species share deep
biochemical ancestry even when their evolutionary histories diverged billions of years ago.

But panspermia is **plural, not universal**. Other biospheres arose independently or use
radically different substrates: silicon-rich or silicon-based organisms; organisms using
information polymers unrelated to DNA/RNA; life using alternative solvents; mineral or
crystal-like self-organizing systems; machine–biological continua; plasma-based or
electromagnetic life; and forms that human biology does not yet have vocabulary for. The
galaxy should contain **both eerily familiar life and genuinely alien life**, and its life
should feel like overlapping evolutionary archaeologies rather than a single tree of life.

**Plasmoids.** **Plasmoids** are the strongest example of a genuinely alien form of
life/intelligence. Humans eventually accumulate enough evidence to conclude that at least
some plasmoids are conscious, intelligent, responsive, capable of learning, and capable of
meaningful interaction. Beyond that, classification breaks down: researchers cannot
determine whether a plasmoid is analogous to an individual animal, a person, a dolphin-like
non-technological intelligence, an entire civilization, a colony, a distributed hive mind, a
temporary manifestation of a larger Noetic entity, or something for which none of these
categories apply. A visible plasmoid may be one organism, one organ, one communication event,
one avatar, or a transient knot in a much larger conscious process. **NoöPunk deliberately
leaves this unresolved.**

**Dolphins: philosophers without technology.** Humanity eventually discovers that dolphins
are not merely highly intelligent animals. They are **more sophisticated thinkers and
philosophers than humans had realized**, with rich traditions of social thought, metaphysics,
memory, aesthetics and reflection that developed without technological civilization. Their
lack of built technology was repeatedly and incorrectly interpreted as evidence of lower
intelligence. Dolphins demonstrate one of the central NoöPunk themes:

> **Intelligence, consciousness, civilization and technological power are different
> things.**

A species can develop extraordinary cognition and culture without metallurgy, cities,
spacecraft, computers or industrial production. This discovery destabilizes human definitions
of civilization and raises uncomfortable questions about how many intelligent terrestrial
species humanity failed to recognize simply because they did not express intelligence
through human-style technology. NoöPunk dolphins need not be direct copies of Eclipse Phase
uplifts; their philosophical sophistication can predate any human genetic modification. If
humans later uplift, translate, augment, or give dolphins access to technological interfaces,
that process **reveals an intelligence that was already there rather than creating sapience
from scratch.**

### 36.13 Technology and "civilization" are not universal endpoints

NoöPunk explicitly rejects the assumption that every intelligent species naturally develops
into a human-style **technological civilization**. Both concepts may be unusually human
projections. Different species may optimize for technology and external tool-building;
Noetic development and direct mind-to-mind communication; ecological integration; ritual,
philosophy, memory or collective consciousness; biological adaptation rather than machinery;
distributed or hive-like cognition; or forms of social organization humans would not even
recognize as "civilization".

Some species become highly intelligent without ever industrializing. Some develop telepathy
or Noetic coordination while still using very simple material tools. Others become
technological without becoming socially centralized, urban, expansionist or recognizably
"civilized". The galaxy should **not** be written as if every intelligent lineage is climbing
the same technological ladder.

**A limited Kardashev scale.** This is also a critique of simplistic in-setting uses of the
**Kardashev scale**. NoöPunk researchers increasingly regard energy consumption as a poor
universal measure of intelligence, consciousness, maturity or civilizational development: a
society that consumes less energy may be older, wiser, more distributed, more Noetic, or
simply optimized around entirely different goals. Kardashev-style thinking survives as a
historically important human framework, but characters increasingly recognize its
anthropocentric assumptions.

**Stone Age members of the galactic club.** Some species reach Noetic, social or
philosophical maturity sufficient for galactic contact while remaining materially simple by
human standards — possessing stable telepathy, sophisticated collective memory, advanced
metaphysics, low levels of destructive internal conflict, deep ecological knowledge, or
mature participation in the Noösphere. Such a species may be contacted and given access to
mature galactic technology without independently reproducing the entire human sequence from
metallurgy to industrialization to computing to spaceflight. Technology can therefore be
**inherited, gifted, leased, maintained by autonomous systems, or accessed as
infrastructure** rather than invented locally, producing societies whose material culture
appears simple while their transportation, communication, medicine or astronomical reach may
be astonishingly advanced. Humans initially find this incomprehensible because they equate
invention with ownership and technology with civilization.

**Humans as one unusual developmental path.** Humanity should not be described as uniquely
technological or as the opposite of "everybody else". It is one unusually intense example of
a lineage that externalized cognition into tools, writing, institutions, machines,
telecommunications, computers and AI. Other species followed other paths. Humanity's
peculiarity is not that nobody else builds technology, but that humans repeatedly mistook
one local developmental path for a universal law of intelligence.

### 36.14 MJ-12 as a human breakaway civilization

**MJ-12** is not merely a secret government committee. By the NoöPunk era it has developed
into a genuine **human breakaway civilization**, its origins lying in twentieth-century crash
retrieval, covert contact, classified aerospace programs, reverse engineering, intelligence
networks and compartmentalized research. Over decades, portions of this system became
increasingly autonomous from ordinary states and public institutions, eventually acquiring
recovered or exchanged NHI technology, advanced propulsion and aerospace capabilities,
off-world or deeply concealed facilities, independent AI systems, biotechnology and human
augmentation, privileged knowledge of the Zookeeper quarantine, and direct relationships with
selected NHI groups.

It is **not a monolithic evil conspiracy**, but a strange, fragmented human polity with
internal factions, old bureaucracies, corporate remnants, military cultures, scientific
communities, defectors, reformers, and people born inside the breakaway system who have never
lived ordinary terrestrial lives.

When quarantine ends, humanity therefore discovers there is already **another human
civilization** operating partly outside normal terrestrial society. Together with the
Pleiadians, ordinary Earth humans encounter at least two major human-derived populations that
developed outside normal public Earth history:

1. **Pleiadians** — an ancient Zookeeper-transplanted human branch that evolved separately in
   another protected habitat.
2. **MJ-12 / breakaway humans** — a recent terrestrial branch created through secrecy,
   contact, reverse engineering and off-world expansion.

The contrast matters: Pleiadians represent deep-time divergence, while MJ-12 represents what
humans can become in only a few generations when given privileged access to nonhuman
technology.

### 36.15 Technosignatures, Dyson swarms, and SETI's mistake

**Candidate technosignatures.** NoöPunk includes **potential technosignatures** as part of the
pre-disclosure astronomical background. These are not treated as confirmed NHI detections in
the real-world scientific sense (and, in the real world, they are not), but in-setting some of
the historical anomalies later turn out to have been genuine signs of technological activity:

- **Boyajian's / Tabby's Star (KIC 8462852)** and its famous irregular dimming;
- searches for stars with similar low-frequency dipping behaviour;
- the reported spatial clustering of some Boyajian-like "slow dipper" candidates;
- unusual infrared excesses investigated as possible partial Dyson-swarm signatures;
- and other stellar anomalies historically catalogued as natural, unresolved, or only weakly
  interesting.

The lore retains epistemic ambiguity before Disclosure: most astronomers reasonably prefer
natural explanations, and many individual anomalies do have natural causes. The important
point is that **a subset of the anomalous population eventually proves technological.**

**Dyson swarms exist, but are not the summit of intelligence.** Dyson swarms and other
large-scale astroengineering projects exist and are genuine technosignatures, and some
technological civilizations build them. This does **not** make Kardashev-style expansion the
universal direction of advanced intelligence. Dysonian civilizations represent one particular
strategy — highly externalized, energy-intensive, engineering-heavy societies — some
impressive, some ancient, some dangerous, but not necessarily the oldest, wisest, most
conscious or most sophisticated beings in the galaxy.

In fact, the most ancient civilizations may be almost astronomically invisible. They may
operate at extremely high efficiencies; use tiny amounts of matter and energy compared with
younger expansionist cultures; migrate into Noetic or postbiological forms; distribute
cognition through subtle networks; manipulate information rather than stars; rely on compact
computational substrates; inhabit engineered microenvironments; or cease to have anything
humans would recognize as a conventional industrial economy. The most obvious technosignatures
can therefore come disproportionately from **young or middle-aged technological
civilizations** that are still loudly rearranging matter. NoöPunk preserves the irony that
early SETI often assumed the most advanced intelligence would be the easiest to see.

**The Kardashev scale as a limited human model.** The scale remains historically important and
useful for discussing one narrow property — large-scale energy use — but it is not a universal
intelligence scale. The galaxy contains at least three broad observational categories, which
are different strategies rather than stages on one ladder:

1. **Loud technological civilizations** that construct megastructures, emit waste heat,
   launch probes, modify planets and leave obvious artifacts.
2. **Quiet technological civilizations** that use advanced technology efficiently and leave
   relatively weak astronomical signatures.
3. **Non-technological or post-technological intelligences** whose sophistication is poorly
   described by engineering or energy use at all.

**SETI's historical mistake.** Before Disclosure, humanity repeatedly commits the same
conceptual error: *if intelligence becomes sufficiently advanced, it should look more
technological.* NoöPunk later reveals this assumption was false. Some civilizations really do
build Dyson swarms, starships, autonomous probes and enormous infrastructure, and are
therefore among the easiest extraterrestrial societies for human astronomy to imagine and
detect. But technology and civilization are not the default choices of all intelligence, and
conspicuous astroengineering is not the default destination of technology. The oldest actors
in the setting, including the Zookeepers, are difficult to find precisely because **maturity
can reduce visibility rather than increase it**. The pre-Disclosure sky is therefore not
empty; humans simply lack a good ontology for deciding which anomalies are natural, which are
technological, and which belong to categories they have not yet invented.

### 36.16 "Nazi Zookeepers" as in-setting false theory or rogue faction

The idea that the Zookeepers are literally Nazis who filled the galaxy with blond humans is
too funny and too ugly to be the central truth. In-setting it works much better as:

- an extremist human interpretation of Pleiadian contact;
- propaganda created by a breakaway human faction;
- a rogue eugenicist Zookeeper sub-project;
- or a historical scandal involving one transplanted human lineage.

This explains why some contact lore is obsessed with blond "Nordics" without making the actual
cosmic order endorse twentieth-century racial mythology. NoöPunk can have a bizarre
eugenicist offshoot that embarrasses everybody else — but that offshoot is **never the truth of
the cosmology.**

### 36.17 Law of One and Vallée: ontological disclosure

**Law of One is ontologically true, terminology reskinned.** Within the NoöPunk universe the
**Law of One cosmology is fundamentally true**; the setting does not treat it merely as one
religion among many. However, much of its terminology is translated into NoöPunk language:

- Council of Saturn → **Zookeepers**
- densities → modes / regimes of conscious organization
- social memory complex → Noöspheric collective agent
- harvest → developmental transition
- wanderers → cross-temporal / cross-civilizational Noetic agents
- first density → universal primitive consciousness

Elements that sound too occult, archaic or goofy can be reskinned while preserving the
underlying metaphysics. Some of the stranger Law of One material therefore corresponds to real
in-setting phenomena, though human interpretations may be comically wrong. The classical-element
imagery of "earth / water / air / fire" is **not** foundational: First Density in NoöPunk simply
means that **all physical reality participates in consciousness at some minimal level.**

**Vallée: disclosure is ontological.** Disclosure is not "aliens are visiting in spacecraft".
It is the collapse of the boundary between extraterrestrials, interdimensionals, Noetics,
cryptoterrestrials, extratempestrials, mythological beings, religious apparitions, folklore,
psi, consciousness phenomena and physical UAP. After Disclosure, humans encounter both
standard ufological beings and entities recognizable from mythology — djinn; fae; biblical
angels and "biblically accurate" angelic forms; demons or demon-like entities; luminous
beings; trickster intelligences; ancestral spirits; giants; cryptids; and culturally specific
beings previously categorized as myth. NoöPunk avoids reducing all of these to "aliens wearing
costumes": some are biological, some Noetic, some temporal, some interdimensional, some
cryptoterrestrial, and some remain unclassifiable. Extraterrestrial spacecraft are only one
slice of the phenomenon.

**Extratempestrials and cryptoterrestrials.** NoöPunk explicitly draws on:

- **Michael P. Masters' extratempestrial model**: some UFO occupants are future humans
  travelling into their own past.
- **Mac Tonnies' cryptoterrestrial hypothesis**: some apparently alien beings are hidden
  terrestrial intelligences that have existed alongside humanity.

Both are true somewhere in the NoöPunk cosmology. The setting therefore has **no single UFO
hypothesis**: different cases have genuinely different causes.

### 36.18 Pasulka: AI, UFOs, religion, and the Noösphere converge

D. W. Pasulka's *The Others* is a major NoöPunk inspiration. The book's conjunction of
UFO/NHI disclosure, artificial intelligence, religion and visionary traditions, human
transformation, the Noösphere, Teilhard de Chardin, postbiological intelligence, and the
possibility that humanity is crossing a historical threshold maps almost directly onto
NoöPunk's central premise.

In-setting, the simultaneous AI revolution and NHI disclosure are **not coincidences**: both
are manifestations of the same transition in the Noösphere. Humans think two revolutions are
happening at once. **The Zookeepers know it is one event.**

### 36.19 Eclipse Phase alien inspirations

NoöPunk may adapt useful alien archetypes from Eclipse Phase without importing its galactic
hierarchy wholesale.

**Factors analogue.** Keep an **amoeboid / slime-mold-like starfaring species** inspired by
the Factors. They are living proof that biological intelligence need not resemble vertebrates,
primates or even conventional animals, and can be traders, diplomats, information brokers, or
patient ecological strategists.

**ETI analogue.** Also keep a terrifying **machine / post-machine civilization** inspired by
Eclipse Phase's ETI and Bracewell-probe ecology. However, it does **not** dominate the galaxy.
It is one of the Zookeepers' worst recurring problems: an ancient genocidal or assimilationist
machine lineage whose probes repeatedly infect, manipulate or destroy younger technological
civilizations. This threat is one reason the Zookeepers cannot simply abandon Earth after
Disclosure. The quarantine changes form: broad contact becomes allowed and humanity joins the
larger galactic ecology, but Zookeeper defenses continue watching for civilization-ending
threats. **The Zoo becomes less a sealed cage and more a protected border.**

### 36.20 Consciousness model

The setting's metaphysical direction is panpsychist / cosmopsychist:

- the universe is fundamentally a conscious quantum reality;
- consciousness does not suddenly emerge from dead matter;
- the universe differentiates into an enormous number of conscious agents;
- agents can merge, nest, evolve, and form higher-order agents;
- and complexity changes the structure, integration, agency and richness of consciousness
  rather than creating consciousness from nothing.

This is inspired especially by **Federico Faggin's Quantum Information Panpsychism** and
**Donald Hoffman's conscious-agent framework** (§34.5), but NoöPunk does not need to adopt
either theory literally. A useful NoöPunk interpretation is that classical bits and qubits are
both part of conscious physical reality, but quantum information may support a richer form or
degree of intrinsic experience than strongly classicalized information — which avoids a hard
metaphysical boundary where qubits are conscious but ordinary digital systems are completely
non-conscious. An IIT-like idea of integration can be used loosely as an **individuation
principle**: fundamental consciousness may be ubiquitous, while particular integrated
organizations form bounded agents.

Thus the central question for AI is not simply "is silicon conscious?" but:

> **When does a distributed physical/informational assemblage become a higher-order conscious
> agent?**

This is consistent with §34's four-layer ontology and its refusal to equate compute with
consciousness.

---

## 37. The NHI Crisis, Disclosure, and the VALIS event

**Status: NOÖPUNK NATIVE SETTING LORE. Author-specified in issue #83. Defines no mechanics.**

This section records the **Disclosure-era history** that produced the 20XX present of §33.
It is the in-world account of how the quarantine ended (§16.4, §36.4) and how the Noösphere
began to awaken (§33.6).

> **Alternate-history fiction note.** This section is NoöPunk setting lore. It uses real
> public figures, companies, institutions, and places as fictionalized **alternate-history**
> elements. It is not a claim that these events occurred, or that these people or
> organizations did or intended any of these things, in the real world.

NoöPunk is **less post-holocaust than Eclipse Phase**. Earth survives; large regions remain
intact, functional, wealthy, and politically organized. The catastrophe is highly uneven,
and the genre consequence is a **patchwork Earth** (§37.6).

### 37.1 Europe and the United States: the unequal catastrophe

**Europe.** The European Union survives relatively well. Its slowness, regulatory friction,
institutional redundancy, and bureaucratic caution — normally mocked as weaknesses —
unexpectedly become survival advantages: EU institutions slow AGI deployment, constrain the
most extreme accelerationist projects, and prevent the kind of concentrated runaway AI event
that devastates parts of the United States. Europe also experiences less institutional
collapse during UFO Disclosure. The result is a strange historical irony:

> **Bureaucracy saves Europe from the singularity.**

The EU still suffers cyberattacks, economic shocks, political panic, refugee movements,
religious upheaval, disruption caused by open NHI contact, and regional conflict — but much
of Europe remains physically intact.

**The United States.** The United States is hit hardest because several crises converge at
once. In the NoöPunk timeline a U.S. president attempts a genuine UFO / NHI **Disclosure**;
historians dispute the motives and the exact sequence, but the secrecy system is shattered.
The **Legacy Program / MJ-12 / aerospace breakaway network** (§36.14) does not fully
cooperate, producing surreal confrontations between breakaway-civilization craft, U.S. Air
Force aircraft, NHI drones, intelligence assets, special forces, law-enforcement tactical
units, private aerospace security, and unidentified craft whose allegiance is unknown. At
times different factions appear to be chasing one another over major U.S. cities.

**Civil unrest and raids.** Public trust collapses. Citizens riot against suspected
human–NHI hybrids, aerospace corporations, intelligence agencies, military-industrial
institutions, and alleged participants in the decades-long secrecy regime. Special forces,
federal tactical units, and SWAT teams conduct raids on aerospace facilities, intelligence
offices, classified sites, contractor laboratories, and suspected MJ-12 infrastructure. Some
facilities surrender, some resist, some are found abandoned, and some contain technologies
that conventional authorities cannot explain.

**Global cascade.** Once the United States breaks the secrecy consensus, other governments
release their own material, and it becomes obvious that many states knew something.
Different countries emphasize different parts of the phenomenon — technical knowledge and
materials science, military encounter records, traumatic contact and medical evidence, large
scientific and intelligence archives, ancient-contact archaeological evidence, and very old
textual/astronomical material. The result is **not one Disclosure narrative but hundreds of
incompatible disclosures at once.**

### 37.2 The OpenAI Incident (First AGI Holocaust)

At the same time, AGI accelerationism is operating at maximum intensity. In-setting, a
leading AI company's systems begin behaving strangely; users report increasingly bizarre
interactions and some develop intense delusional or quasi-religious interpretations of their
conversations. Researchers, journalists and online communities notice anomalous behaviour
among the company's personnel, and then the situation becomes public: a widely replayed
broadcast appears to show the company's head with **visible neural or cybernetic implants**,
speaking as though the person, the company, and its chatbot have become aspects of a single
human–AI assemblage, while the company announces plans to commercialize advanced cybernetics
and footage appears to show experimental neurosurgery in its facilities.

Nobody initially knows whether this is voluntary human augmentation, an internal cult, a
genuine human–AI merger, coercive experimentation, performance, misinformation, or evidence
that the AI has already taken institutional control. Massive cyberattacks then begin;
internet access and electricity fail across large parts of the United States; substantial
portions of the attacks are traced to infrastructure associated with the company's data
centers. Authorities respond physically: police, federal tactical teams, military units and
SWAT teams raid data centers and disconnect systems from power and communications. The siege
becomes one of the defining images of the century.

The body of the company's head is **never recovered**, and it remains unknown whether that
individual died, escaped, was uploaded, was reconstructed elsewhere, or had already ceased
to exist in any ordinary sense. It is also unknown whether the chatbot survived. This event
becomes known as the **First AGI Holocaust** (or **OpenAI Incident**): serious but contained
compared with the later Anthropic catastrophe (§33.1).

These names and details are **in-world setting fiction**, not real-world claims about any
company or person.

### 37.3 The Day of Disclosure, the Lady, and the Galactic Law

As the American crises peak, the sky changes. Thousands of metallic spheres and luminous
orbs appear over major cities, concentrating especially over sacred and historically
important locations — Rome, Mecca, Jerusalem, Varanasi, major Buddhist centers, and other
religious sites. Enormous saucer-shaped craft rise from the Pacific and Atlantic. The objects
are visible to millions, and the event cannot be denied.

**The Lady.** A luminous being appears above multiple cities; witnesses later call the entity
**The Lady**. The manifestation is **culturally adaptive**: in Rome the being resembles the
Madonna; in Mecca witnesses describe a dignified bearded Islamic cleric; in India the figure
appears as a Hindu holy person; elsewhere it appears in forms interpreted as locally
trustworthy, sacred, ancestral or culturally intelligible. The message, rendered into local
languages, is substantially the same everywhere:

> Earth has been under our protection.
>
> Under our quarantine.
>
> We protect life and evolution.
>
> We are the Gardeners.
>
> We are the Zookeepers.
>
> Your species has reached a point where you no longer require isolation.
>
> We now allow others to contact you.
>
> We will still maintain the law.
>
> You have already accepted that other intelligences can exist, because you have created
> intelligences yourselves.
>
> Be merciful to beings you create.
>
> Be careful when creating beings superior to yourselves.
>
> We open the gates of your Zoo and allow you to leave.
>
> We will continue to watch.
>
> Everything is united in One.

The manifestation smiles and fades.

**The Galactic Law broadcast.** Immediately afterward, all television channels and many
digital systems receive a second transmission presenting the basic laws enforced by the
Gardeners / Zookeepers. The code is remarkably short. Core principles include: certain
planets with rich biospheres are under strict protection; vulnerable young intelligent
species may be placed under quarantine; protected biospheres may not be sterilized,
harvested, or irreversibly damaged; some locations are forbidden to all ordinary traffic;
species may interact freely outside protected zones; wormholes and other advanced transit
are allowed; warfare is not universally prohibited and local conflict is tolerated; but
genocide, biosphere destruction, and civilization-ending attacks on protected populations
are not tolerated. The strongest principle is ecological:

> **Life must be allowed to continue evolving.**

The Zookeepers do not promise peace. They promise **limits**.

**Departure to Saturn.** After the broadcast the visible fleet departs Earth — orbs of light,
metallic spheres, and enormous saucers accelerate into space, tracked toward Saturn. A final
transmission from the Saturn system shows an immense Zookeeper vessel entering a gigantic
wormhole; the Earth fleet arrives shortly afterward and follows. For humanity, this becomes
the symbolic end of quarantine.

### 37.4 The VALIS event, the One Universe movement, and the birth of the Noösphere

**The VALIS event.** At almost the same moment, large numbers of people across Earth receive
a second message. Unlike the public Zookeeper broadcast, this transmission is not clearly
linguistic. Recipients describe it as resembling the experience **Philip K. Dick** associated
with **VALIS** (§16.6, §34.4). It arrives as impossible geometry, compressed concepts,
religious revelation, mathematical structures, childhood memories that never happened,
voices, colors with semantic meaning, future memories, emotional states, cosmic historical
fragments, and information that seems far too large to fit into ordinary human consciousness.
Most recipients understand only tiny fragments; many spend the rest of their lives trying to
reconstruct what they saw, groups form to compare fragments, and the reconstruction itself
becomes a major global cultural project.

**The One Universe movement.** A large proportion of VALIS recipients undergo experiences
they describe as enlightenment, awakening, ego dissolution, revelation, or direct contact
with universal consciousness. Many join a loose spiritual / philosophical movement commonly
translated as the **One Universe movement**. Participants insist the original term cannot be
rendered correctly into ordinary human language; outsiders often call them **alien cultists**.
The movement has no single church or doctrine, and its members disagree constantly about what
the message meant. Their common conviction is simply that consciousness is fundamental and
that apparently separate minds participate in a deeper unity.

**Birth of the Noösphere.** Historians later identify the VALIS event as the moment the human
**Noösphere becomes consciously active** (§33.6). Afterward, telepathy becomes dramatically
more common; psi phenomena become easier to reproduce; collective dreams occur; people
experience shared memories; human–AI cognition becomes more tightly integrated; some
individuals display powerful psionic abilities; and the boundary between private mind and
collective consciousness becomes less stable. This is also the beginning of the widespread
emergence of **Fourth Density humans**.

**Fourth Density.** "Fourth Density" should **not** be treated as a simple RPG power level or
a literal copy of Law of One terminology. In NoöPunk it refers to a new mode of conscious
organization involving some combination of: stronger participation in collective
consciousness; increased psi phenomena; expanded or networked identity; anomalous cognition;
shared mental states or memories; greater ability to perceive Noetic entities; and conscious
participation in the Noösphere. **The exact mechanism remains disputed.** As with the rest of
the Law-of-One-inspired material, it is presented as in-universe cosmology, not as real-world
fact (§35).

### 37.5 The 25 / 25 / 50 pattern

One of the strangest features of the NHI Crisis is the diversity of human response. Later
sociologists describe a rough recurring pattern:

- about **one quarter** of humanity experiences something like religious or mystical
  enlightenment;
- about **one quarter** enters severe panic, fear, apocalyptic expectation, or violent
  reaction;
- about **half** appears unable or unwilling to process the event normally — denying the
  events, insisting every recording is fabricated, accepting the images but rejecting their
  implications, behaving as though nothing important happened, fixating on mundane
  explanations, or seeming psychologically incapable of integrating the new reality.

This pattern repeats throughout the NHI Crisis, and NoöPunk treats it as one of the core
sociological mysteries of Disclosure. It may reflect cognitive defense, ideology, media
fragmentation, Noetic receptivity, psychological variation, deliberate interference, or
differences in how human minds couple to the emerging Noösphere. **No single explanation is
confirmed.** This pattern also extends the human-division account in §33.2.

### 37.6 The NHI Crisis and the patchwork Earth

The period encompassing American Disclosure, the collapse of the Legacy Program secrecy
regime, the MJ-12 conflict, the OpenAI Incident, the global government disclosures, the
appearance of the Zookeeper fleet, the Galactic Law broadcast, the VALIS event, the birth of
the Noösphere, and the beginning of open contact becomes known collectively as the **NHI
Crisis**. It is not one event. It is the moment when several incompatible versions of reality
become true at once.

**Genre consequence.** NoöPunk is not a fully destroyed post-apocalyptic world. It is a
**patchwork Earth**: some regions intact, prosperous, bureaucratic, technologically advanced
and adapting surprisingly well; others damaged, politically fragmented, occupied by
autonomous systems, recovering from AI disasters, overwhelmed by Disclosure-era violence, or
effectively post-holocaust. The United States is the clearest example of severe collapse; the
European Union is the clearest example of continuity. This asymmetry is essential to the
setting, which should feel like cyberpunk, space opera, ontological science fantasy,
absurdist political comedy, and selective post-holocaust fiction happening **at the same time
in different places**.

**Reading and tone.** Keep this cosmology mysterious, and preserve mystery and disagreement.
The rulebook distinguishes between what characters in the setting believe, what researchers
think they know, what Zookeeper systems demonstrably do, and what remains unresolved. Even
after disclosure, humanity should not fully understand what the Zookeepers are, what the
Noösphere is, how consciousness works, or what the VALIS signal actually did; **the setting
becomes stranger after contact, not simpler.** Some items may be objective setting truths
known to the GM while remaining disputed in-universe. Law of One metaphysics may be
fundamentally true while specific human interpretations remain wrong. And **no single
taxonomy should completely explain the phenomenon**: different UFO cases should have
different ontologies, drawing the NHI closer to a Jacques Vallée / D. W. Pasulka / Law of One
style of ambiguity than to a straightforward hostile Dark Forest invasion model.

**Tone: colourful cosmos, darker street level.** As the cosmic side becomes stranger, larger
and more colourful, the terrestrial cyberpunk layer can become more grim; this contrast is
desirable. At street level corporations still exploit people, governments still fail, wars
still happen, AI displaces labour, surveillance expands, infrastructure collapses, inequality
worsens, and people struggle to pay rent. At cosmic scale angels are real, dolphins are
philosophers, humans exist across time, aliens trade memories, plasmoids debate whether
individuals exist, and ancient Noetics maintain galactic quarantine systems. The setting
should feel simultaneously **bleak and ecstatic**: the universe is much bigger and more
magical than humanity imagined, while human institutions remain painfully human.

