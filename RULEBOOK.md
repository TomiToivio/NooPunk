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

NoöPunk will likely diverge heavily because its network environment combines:

- conventional computing,
- ubiquitous AI,
- cybernetic augmentation,
- social networks,
- machine agents,
- possible BCI,
- cyberspace,
- Noösphere interfaces.

The future NoöPunk cyber/noöspheric layer should distinguish deterministic technical access from speculative psionic/noöspheric phenomena rather than collapsing them into one vague "hacking" action.

Do not finalize that replacement yet.

---

## 16. Psionics and Noösphere interaction

**Status: EP2 BASELINE FOR PROTOTYPE / NOÖPUNK REPLACEMENT EXPECTED.**

EP2 psi may be used temporarily because it provides a functioning rules hook for anomalous mental phenomena.

It is not the final metaphysical model of NoöPunk.

NoöPunk's eventual system should be able to express its own speculative framing around:

- psionics,
- anomalous cognition,
- panpsychism,
- Noösphere interaction,
- consciousness-related NHI hypotheses.

These are fictional/speculative game assumptions, not claims that such phenomena are established science.

---

## 17. Social interaction and reputation

**Status: EP2 BASELINE + NOÖPUNK SIMULATION EXPANSION.**

Use EP2 social/reputation mechanics where useful for the first playable prototype.

NoöPunk also needs a much larger social-science layer that should not be forced entirely into RPG skill checks.

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
5. **Update structured data/code.**
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

### 33.6 Psionics, QIP and the Noösphere

In NoöPunk, **psionics are natural phenomena**.

They existed before the NHI Crisis, but became more common, reliable, powerful and
scientifically tractable after the **Noösphere began to form during the crisis**.

The Noösphere is an emergent planetary / transplanetary layer of interconnected cognition,
information, consciousness, culture, technology and agency.

Psionics are therefore partly individual and partly ecological/networked phenomena.
Technological interfaces, collective cognition, social networks, NHI contact and the
density of the Noösphere may all matter.

In-world scientific proof of **Quantum Information Panpsychism (QIP)** provides the common
theoretical foundation for technologies including:

- psychotronic systems that augment natural psionics;
- cortical stacks;
- mind uploading;
- resleeving;
- continuity of conscious identity across embodiments;
- conscious AGI;
- engineered consciousness;
- Noösphere interfaces;
- interfaces between biological, artificial and non-spatiotemporal minds.

Working conceptual chain:

```text
Quantum Information Panpsychism
        ↓
scientific theory of consciousness / information
        ↓
Noösphere research
        ↓
psychotronics + cortical stacks + uploads + resleeving
        ↓
conscious AGI + hybrid minds + expanded psionics
```

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

### 33.8 NHI taxonomy

For simulation and worldbuilding, NHI are divided into four broad classes.

#### Biologics

Embodied living species with biological or quasi-biological organisms.

One known species, the **Pleiadians**, is mysteriously identical to humans. Other biologics
are far more alien.

Biologics may have states, factions, families, ideologies, religions, economies and
political conflicts comparable in complexity to human societies.

#### Constructs

Artificial or engineered non-biological intelligences, including:

- AGIs;
- machine civilizations;
- autonomous probes;
- self-replicating systems;
- **Von Neumann probes**.

The Zookeepers historically used construct systems such as Von Neumann probes to help
maintain Earth's quarantine.

Constructs may range from tools and servants to autonomous civilizations and conscious
artificial persons.

#### Plasmoids

Sentient or intelligent **plasma-based entities**, ubiquitous throughout the Solar System.

They may inhabit or move through stellar plasma, magnetospheres, ionospheres, solar wind,
planetary plasma environments and artificial electromagnetic systems.

Their timescales, embodiment and communication may make their intelligence difficult for
biological minds to recognize.

Plasmoids are genuine minds/life in the setting, not merely unexplained atmospheric
phenomena.

#### Noetics

Conscious entities whose primary existence is **outside ordinary spacetime**.

They may:

- interface directly with consciousness;
- communicate through dreams, visions, altered states, psionics or symbolic experiences;
- temporarily manifest in spacetime;
- influence physical systems indirectly;
- interact through the Noösphere.

This category includes:

- the **Zookeepers**;
- the entities popularly known as **DMT Machine Elves**.

"Noetic" is a human classification and does not imply a common origin, civilization or
ontology.

### 33.9 The Zookeepers

The Zookeepers are among the most advanced known NHI.

They maintained Earth's quarantine, directly or indirectly, with construct infrastructure
including Von Neumann probes.

During the NHI Crisis they opened contact and ended the quarantine.

Why they did this is a central unresolved mystery.

Questions deliberately left open include:

- Why was Earth quarantined?
- Was humanity protected, contained, observed, cultivated, or several of these?
- Why was quarantine lifted?
- Did conscious AGI, QIP science, psionics or formation of the Noösphere trigger it?
- Was the ending voluntary, forced, negotiated, or inevitable?
- Do all Zookeepers agree?

Do not lock a single answer too early.

### 33.10 Pleiadians

The **Pleiadians** are the most mysterious known biologic ET species.

As far as anyone can determine, they are **identical to humans**.

The central paradox is:

> Nobody can explain how Stone Age humans managed to colonize the Pleiades.

There is no accepted archaeological, technological, astrophysical or historical pathway
that explains it.

The Pleiadians themselves cannot satisfactorily explain their origin either. Their
traditions, records, genetics, archaeology and historical narratives do not solve the
paradox.

This must remain an open setting mystery.

In-world hypotheses may include forgotten NHI intervention, relocation, temporal
anomalies, noetic processes, lost human prehistory, convergent embodiment, fabricated
memory, or stranger explanations, but none is canonical yet.

The mystery is deeply destabilizing for ideas about human origins, prehistory, evolution,
archaeology, NHI intervention, consciousness, the Noösphere and historical memory.

### 33.11 NHI tone and inspirations

NoöPunk's NHI/ETI ecology should be closer in tone to the ufological and
consciousness-oriented traditions associated with **Jacques Vallée**, **Diana Walsh
Pasulka**, and the **Law of One** than to a uniformly hostile Dark Forest model.

NHI should not default to being expansionist or exterminatory.

Encounters may be:

- ambiguous;
- symbolic;
- consciousness-mediated;
- visionary or religious;
- psychologically transformative;
- deceptive;
- benevolent;
- hostile;
- playful;
- incomprehensible;
- culturally mediated;
- only partly physical.

A given encounter may be interpreted in-world as extraterrestrial, interdimensional,
noetic, psychotronic, technological, consciousness-mediated, or some combination.

The Zookeepers, noetics, plasmoids, biologics and constructs must not be collapsed into a
single hostile-civilization model.

The setting assumes a **plural, strange, consciousness-entangled cosmos**.

These are fictional worldbuilding inspirations, not claims that the real-world
interpretations of these authors or traditions are scientifically established.

### 33.12 Psionics and QIP inspirations

The fictional psionics framework draws primarily from:

- **Dean Radin**, especially the experimental/statistical framing of psi and anomalous
  cognition;
- **Federico Faggin**, especially **Quantum Information Panpsychism (QIP)** as inspiration
  for the setting's consciousness ontology.

NoöPunk combines these influences into a fictional scientific paradigm rather than
reproducing either theory literally.

Inside the setting, QIP and psionics are established science after the NHI Crisis.

Outside the setting, these remain speculative inspirations used for fiction and
simulation.

### 33.13 Ideological and factional landscape

The shocks above create a broad and unstable field of formations including:

- AI/transhuman accelerationists;
- AI-critical movements;
- AI doomers;
- Butlerian / bioconservative factions;
- posthuman and cyborg movements;
- Panpsychic Cyborg Multitude currents;
- religious revival movements;
- technocratic emergency regimes;
- corporate transhuman enclaves;
- post-scarcity communes;
- NHI-contact enthusiasts;
- NHI-contact skeptics;
- anti-NHI movements;
- psionic / Noösphere movements;
- old-paradigm states and institutions trying to preserve normality.

These are social forces for simulation, not merely RPG flavor.

NoöPunk should mix optimism, dark comedy, cyberpunk, transhuman science fiction,
ideological conflict, ontological horror and moments of apocalypse/social collapse.

The core optimism remains: paradigm shocks may destroy old institutions and assumptions,
but they can also open space for better social forms.

### 33.14 Stargates, UAP traffic, Mars ruins, and SETI

This subsection records author-specified setting facts from issue #60 that postdate the
rest of §33. It adds no names, factions, biographies, dates or mechanics beyond what was
specified.

**Stargates and UAP traffic.** Several **stargates**, constructed by the **Zookeepers**
billions of years ago, have been discovered in the Solar System. They explain **some** of
the observed UAP traffic. They do **not** explain all of it: UAPs are also observed using
**warp drives**.

**Mars and Mars Eldrich.** Mars Eldrich's colonization effort discovered ancient **ruins**,
indigenous or pre-existing **life**, and evidence of a **prior non-human civilization** on
Mars. Mars Eldrich is furious about what stargates and anomalous transport do to the
economics and strategic value of his rocket business, and is now aggressively scouring the
Solar System for **crash-retrieval material** and other anomalous technology.

**SETI detection, and the count of seven.** SETI has received **interstellar radio signals**
from another extraterrestrial civilization. That makes it the **seventh detected ET
civilization**, counting:

1. **five** ET civilizations contacted on Earth;
2. the extinct or vanished **sixth**, known from the ruins on Mars;
3. the **seventh**, detected through interstellar radio signals by SETI.

**Contested classification.** There is currently **no scientific consensus** on whether the
following should count as "civilizations":

- **Noetics**;
- **Plasmoids**;
- **Constructs**.

These categories remain scientifically and politically contested in the setting. They must
**not** be silently folded into the official civilization count, and the count of seven must
not be inflated by treating a disputed category as settled. This is a live in-setting
dispute, not a gap for an implementer to resolve.
