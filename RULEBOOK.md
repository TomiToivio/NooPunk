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

This is fictional setting metaphysics inspired by real scientific hypotheses and esoteric
sources. The real-world sources do not establish NoöPunk's fictional claims.

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
- **Don Elkins, Carla L. Rueckert & Jim McCarty.** *The Law of One / The Ra Material*
  (L/L Research, sessions beginning 1981). Public archive:
  https://www.llresearch.org/channeling/ra-contact
- **Pierre Teilhard de Chardin.** *The Phenomenon of Man*. English translation, Harper,
  1959. Historical inspiration for the concept of the **Noösphere**.

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

### Interpretation rule

When the rulebook says a real-world theory **makes something possible in 20XX**, that is a
fictional extrapolation unless explicitly stated otherwise. In particular, NoöPunk treats
QIP, Orch OR, PSI, fourth density, Social Memory Complexes, non-local psychic entanglement,
conscious AGI via quantum processors, uploading continuity and the Council of Saturn as
elements of its fictional world model, not as settled descriptions of the real world.

