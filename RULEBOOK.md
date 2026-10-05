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

> **NoöPunk: a Concordia RPG/social simulation using heavily modified Eclipse Phase 2E rules, set in an alternate pre-Fall 20XX.**

NoöPunk is a portmanteau of **Noösphere** and **Cyberpunk**.

- **Cyberpunk** is the cybernetic side: artificial intelligence, ubiquitous computation, networks, surveillance, corporate and state power, cybernetic augmentation, synthetic media, and technologically mediated social life. William Gibson is a central literary influence.
- **Noösphere** is the psychic side: consciousness, collective intelligence, psionics, NHI, and the emergence of a planetary sphere of mind. Pierre Teilhard de Chardin is the central conceptual reference.

The year is deliberately written as **20XX**. Ray Kurzweil's 2045 Singularity date is an important thematic reference, but NoöPunk does not commit to a fixed chronology for future events.

### 2.1 Social-science foundation

NoöPunk grows directly out of the intellectual terrain explored by the **LaclauGPT** research project (https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md). The social-science background is part of the game model, not decorative lore.

**Ernesto Laclau** provides the core model of ideology, antagonism, political identity, floating and empty signifiers, coalition formation, and struggle for hegemony. The major concepts of 20XX, including **AI, AGI, NHI, PSI, consciousness, humanity, safety, freedom, progress, and the Singularity**, are themselves contested signifiers. Factions struggle to stabilize their meanings and organize society around them.

**Manuel Castells** provides the network-society and communication-power layer. Power is exercised by programming networks, connecting and disconnecting actors, shaping communication, and controlling flows of information, capital, technology, and attention.

**Simon Lindgren** provides a bridge between critical theory, AI, digital society, and social data science, through works such as *Data Theory* and *Critical Theory of AI*. NoöPunk should use social-science methods inside the simulation wherever useful, including:

- Social Network Analysis;
- discourse-network analysis;
- agent-based social simulation;
- analysis of large-scale digital communication;
- data-driven modeling of ideological formations and social change.

The game should ask not only what a technology can do, but **who defines it, who benefits, who is excluded, which futures become imaginable, and which forms of power it stabilizes or disrupts**.

### 2.2 AI as ideological conflict

NoöPunk turns contemporary AI discourse into factions, institutions, policies, technologies, and historical outcomes.

The setting contains competing currents rather than one canonical ideology:

- accelerationist, Cosmist, and techno-optimist visions inspired by **Ray Kurzweil**'s *The Singularity Is Nearer* and **Ben Goertzel**'s *A Cosmist Manifesto*;
- **Critical AI** perspectives concerned with political economy, inequality, exclusion, ideology, and concentrated technological power, including **Timnit Gebru** and **Émile P. Torres**' critique of the **TESCREAL** bundle;
- **existential-risk** perspectives associated with AGI catastrophe and loss of control, such as **Nate Soares** and **Eliezer Yudkowsky**'s *If Anyone Builds It, Everyone Dies*.

These positions are not merely opinions held by NPCs. They shape states, corporations, movements, research programmes, laws, military doctrines, infrastructure, and the uneven geography of 20XX.

NoöPunk contains the full ideological spectrum rather than adopting one official answer; the conflict between these views is part of the world itself.

### 2.3 Cyberpunk updated for 20XX

NoöPunk begins from the premise that many classic cyberpunk themes are already recognizable in contemporary society. It therefore updates cyberpunk using current social trends, real technological trajectories, social science, political economy, AI ideology, ubiquitous networks, synthetic media, surveillance, platform power, cybernetic augmentation, and emerging collective intelligence.

The target is not retro-1980s cyberpunk preserved in amber. It is **cyberpunk that kept evolving**.

**Philip K. Dick is the most NoöPunkish literary influence**, especially *Ubik*, *VALIS*, *A Scanner Darkly*, *Do Androids Dream of Electric Sheep?*, and *The Three Stigmata of Palmer Eldritch*. His unstable boundaries between reality, technology, altered consciousness, institutions, paranoia, and the divine are central to the tone.

### 2.4 The Noösphere and simultaneous paradigm shifts

NoöPunk places several **unordered, interacting paradigm shifts** on top of one another:

- the AI / AGI revolution;
- the independent scientific revolution in consciousness, QIP, PSI, and panpsychism;
- NHI / UAP Disclosure;
- the emergence of the Noösphere as technologically and psychically connected collective intelligence.

These are not numbered stages. In particular, **QIP / PSI does not originate in UFO/NHI
Disclosure**: humanity reaches its scientific consciousness breakthrough independently.

The setting can therefore be understood as being about **Non-Human Intelligence** in a broad sense, including both **Artificial Intelligence** and **Extraterrestrial / anomalous Intelligence**.

Important conceptual influences include:

- **Alexander Wendt**, especially *Quantum Mind and Social Science* and *The Last Humans*;
- **Jacques Vallée**, whose Interdimensional Hypothesis informs the technological, biological, consciousness-related, psionic, and spacetime-anomalous character of the NHI phenomenon;
- **Diana Walsh Pasulka**, whose work informs the religious, cultural, technological, and institutional consequences of UAP/NHI contact and provides a bridge back to Teilhard's Noösphere;
- **Federico Faggin**, whose Quantum Information Panpsychism is the primary fictional scientific basis for NoöPunk's post-materialist consciousness paradigm;
- **Penrose and Hameroff**, **Donald Hoffman**, and **Bernardo Kastrup** as additional consciousness influences;
- psychedelic and DMT research aesthetics, including **Andrew Gallimore**;
- **Dean Radin** as an inspiration for PSI, entanglement, and the interpretation of "magic" as a cultural vocabulary for anomalous consciousness phenomena.

These are inspirations for a fictional setting. Their real-world scientific or philosophical status does not automatically establish NoöPunk's fictional conclusions.

### 2.5 Relationship to Eclipse Phase

Eclipse Phase supplies the **rules and transhuman-technology baseline**, but NoöPunk follows a substantially different world history.

Canonical divergences include:

- **the Fall has not happened**;
- **Earth remains inhabited and politically central**;
- there have been multiple localized **Rogue AGI Disasters**, but no global extinction-level Fall;
- some regions have post-apocalyptic conditions while global civilization remains functional;
- Eclipse Phase-level technologies exist, but distribution is highly uneven;
- most humans still inhabit their original biological bodies;
- roughly **25% of humanity has cortical stacks**;
- roughly half of those with cortical stacks have already resleeved at least once;
- roughly **50% of humanity has some cybernetic augmentation**, ranging from medically necessary replacements to mesh inserts and cognitive enhancements;
- player characters may encounter much higher concentrations of transhumans because of the institutions, crises, conflicts, and frontier environments in which they operate.

NoöPunk should preserve EP2 mechanics where they are useful, simplify them where Concordia and large-scale simulation require it, and replace them where the NoöPunk world model demands something different.

### 2.6 Core design identity

NoöPunk is simultaneously:

- a cyberpunk RPG;
- a Noösphere / consciousness RPG;
- a transhuman RPG;
- an NHI/UAP-contact setting;
- a political and ideological simulation;
- a social-science simulation;
- a Concordia multi-agent world;
- an Eclipse Phase-derived rules experiment.

Its central question is:

> **Who gets to define what humanity, intelligence, consciousness, progress, danger, and reality mean when several paradigm shifts happen at once?**

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
| Firewall | **deliberately undecided** — see below |
| TITANs | **deliberately undecided** — see below |

These are **working mappings**, not final terminology.

Two EP2 concepts are carried as **explicitly undecided** rather than mapped, because
the alternate timeline's divergence point falls inside them. Recording them as open is
the decision; a later contributor must not "helpfully" resolve them by inventing an
organisation, a history, or a mechanic.

**Firewall.** EP2's cross-faction conspiracy may **exist differently, emerge
differently, or not yet exist**, depending on where NoöPunk's divergence lands. The
setting does not currently state which. Nothing is established about its membership,
reach, methods, or whether it has formed at all. (Note a wording trap: the phrase
"Great Firewall" does appear in §33.27, where it refers to the Chinese state's internet
controls — an unrelated use of the words, not this organisation.)

**TITANs.** NoöPunk is **pre-Fall**: nothing comparable to the canonical Eclipse Phase
Fall has occurred (§33.1), and the setting must **not** assume that it has. NoöPunk's
rogue-AGI history is real and specific — the localized "AGI holocausts" of the NHI
Crisis, recorded in §33.28 and §33.28b — but whether it is a *TITAN* trajectory, a
different one, or no trajectory at all is **not decided**. These are separate questions
and the answer to the second does not follow from the first.

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
| 2026-10-03 | Layer ontology | Four layers treated implicitly across §15–§19 | **Explicit four-layer ontology with structural couplings (§36)** | Issue #78. Couplings made explicit because the interfaces are where the gameplay is; no mechanics defined. |
| 2026-10-04 | AGI catastrophe structure | Earlier drafts used named contemporary AI companies for a four-disaster cascade | **Multiple rogue-AGI disasters with fictionalized 20XX actors and no fixed global sequence (#98)** | Issue #98 supersedes the named-company chronology. Detailed named variants are archived; active canon keeps the disasters structural and unordered. |

| 2026-10-04 | Theory sections | Four-layer ontology and bibliography deleted by a stale-branch clobber (`901ba05`) | **Restored as §36 (four NoöPunk systems) and §37 (theoretical sources)** | The clobber removed 703 lines; the glossary kept `## 34.`, so number-keyed guards read the wrong section and the loss was silent. Restored by heading text; §27 number stays with the glossary. |
| 2026-10-04 | Sources list | Two competing sources sections (#99 landed twice as §35 and §38) | **Merged into a single §35; the duplicate §38 removed** | Issue #101. The union of both copies is kept: the fuller fiction and RPG entries from §38, the broader field list and preambles from §35. §35 now declares itself the design-facing map beside the §37 theory bibliography, and §33.2's Wendt citation is re-pointed from the stale §35.5 to §36.5. |

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

### 33.1 Background timeline: unordered paradigm shifts

NoöPunk is set in **20XX** in an alternate **pre-Fall Eclipse Phase continuity**.

Nothing comparable to the canonical Eclipse Phase **Fall** has happened. Earth still exists,
remains heavily populated, and is politically and culturally central.

The background "timeline" is intentionally **not a forecast chronology**. It is a set of
major paradigm shifts that produce the NoöPunk world. Unless a dependency is explicitly
required by canon, these shifts have **no fixed date and no fixed order**.

> **The year is 20XX. The paradigm shifts are canonical; their complete chronology is not.**

Ray Kurzweil's **2045** Singularity remains an important intellectual and thematic reference,
but 2045 is not the canonical in-world year.

The principal background shifts are:

- **Cyberpunk intensification:** ubiquitous networks, platform and corporate power,
  surveillance, synthetic media, algorithmic governance, cybernetic augmentation,
  technological inequality, and networked social life continue developing from conditions
  already visible in the present.
- **AI / AGI revolution:** artificial intelligence transforms science, labor, politics,
  warfare, media, and everyday life. Accelerationist, Critical AI, Cyborgist, and
  existential-risk formations struggle over how societies should respond. Rogue-AGI
  disasters occur, but the canonical background does not require one definitive incident
  sequence.
- **Quantum Information Panpsychism / PSI revolution:** an independent scientific
  breakthrough establishes a post-materialist consciousness paradigm in-setting and makes
  PSI experimentally reproducible enough to support psychotronic technologies. This
  breakthrough is **separate from and independent of UFO/NHI Disclosure**.
- **UFO / NHI Disclosure:** NHI existence becomes scientifically and politically
  undeniable. Governments, publics, religions, corporations, scientific institutions,
  Legacy Programs, contact traditions, and anomalous phenomena are reinterpreted. The
  canonical background does not prescribe one definitive disclosure cascade.
- **Noösphere emergence:** increasingly dense human, AI, cybernetic, social, and psionic
  networks develop into new forms of collective intelligence and planetary-scale
  communication.
- **Uneven geopolitical and social transformation:** regions respond differently to these
  shifts. Some remain comparatively intact; others experience war, institutional collapse,
  reaction, authoritarianism, radical experimentation, or localized catastrophe.

These shifts can overlap, interact, and cause one another locally without being forced into
a single global sequence. Historical dependencies may be stated when they are essential
canon, but agents and authors should otherwise preserve ambiguity.

A useful tonal rule remains:

> **The world did not end. The old world-picture did.**

NoöPunk is therefore not post-Fall, but it can contain many **local falls**: regional
breakdowns, emergency regimes, ideological violence, failed institutions, cults,
reactionary enclaves, ecstatic movements and experiments in new social orders.

Detailed narrative versions of the crisis years, named disclosure sequences, raids,
broadcasts, and speculative event orderings are preserved as **non-binding narrative
variants** in `docs/archive/NARRATIVE_TIMELINE_VARIANTS.md`.

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

NoöPunk draws this specifically from **Alexander Wendt's** work on the politics of UFO
disclosure: there is no single shared human reaction to contact, and the social response
is a problem of political theory rather than a single public "reveal". Wendt's *Quantum
Mind and Social Science* is also one of the setting's consciousness-theory inspirations
(§36.5, §33.17). His work is an inspiration for this **fictional** worldbuilding; the
setting does not present his arguments as established science.

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

Running beneath the institutional question is a **political-economic** one. The core
contested axis of the NHI Crisis era is **neofeudal cybercapitalism versus the Multitude**:
concentrated platform, corporate and habitat power that converts crisis into new forms of
private sovereignty, against commons-based, cooperative and autonomist formations that
organize from below. This is a live struggle, not a settled outcome, and it is one of the
setting's central themes — the same axis is stated in
`docs/PRE_FALL_ALTERNATE_TIMELINE.md` and `data/paradigm_shifts.yaml`.

### 33.6 Psionics, QIP, awakening and the Noösphere

In NoöPunk, **psionics are natural phenomena present latently in all humans**. They are not
caused by alien infection, a virus, or an exsurgent pathogen.

PSI existed before the NHI Crisis, but was generally weak, noisy and controversial. It
became more common, reliable, powerful and scientifically tractable after the **Noösphere
began to awaken during the crisis**.

The Noösphere is an emergent planetary / transplanetary layer of interconnected cognition,
information, consciousness, culture, technology and agency. In the setting's more
metaphysical language, the old **collective unconscious is becoming conscious**.

### 33.6a The Law of One is real, distorted, and incomplete

**The Law of One / Ra Material is canonically a genuine NHI contact record in NoöPunk.**

During the NHI Crisis, independent contact, archaeological, noetic, astronomical, intelligence,
and scientific evidence converged strongly enough that the historical Ra sessions could no
longer be dismissed as merely religious literature, fiction, fraud, or ordinary channeling.
The communicating intelligence identified as **Ra** was real, and the sessions contain
authentic information about the wider cosmology of consciousness, Earth's quarantine,
densities, polarization, Social Memory Complexes, the Confederation, the Orion Group, and
related NHI history.

This does **not** make the text infallible.

The surviving Law of One corpus is understood in 20XX as a **partial and distorted contact
document**. Researchers, theologians, noeticists, historians, intelligence agencies, and
NHI-contact specialists generally distinguish at least four sources of uncertainty:

- **channel distortion**: material was filtered through the language, culture, expectations,
  concepts, memory, and subconscious processes of the human channel and group;
- **Orion interference**: some sessions or passages may have been deliberately distorted,
  disrupted, redirected, or contaminated by Service-to-Self intelligences;
- **translation limits**: Ra was attempting to express concepts for which early-1980s human
  language and scientific categories were inadequate;
- **radical incompleteness**: Ra described only part of a vastly larger galactic and noetic
  reality. Entire civilizations, ecologies of intelligence, historical episodes, physical
  mechanisms, political structures, and forms of existence are absent from the corpus.

Accordingly, **Law of One canon is true in outline, not exhaustive in detail**. A statement
in the Ra Material is important evidence about the setting, but it does not prohibit later
discoveries that reveal a larger picture, a mistranslation, a contextual limitation, an
Orion distortion, or a missing category.

This becomes one of the central religious shocks of Disclosure. The Law of One is now
simultaneously:

- a primary historical source for NHI studies;
- a foundational text in noetics and comparative xenology;
- a subject of scientific and intelligence analysis;
- and a **holy text** for numerous new and transformed religious movements.

Some believers treat every surviving sentence as revelation. Academic and institutional
orthodoxy is more cautious: **Ra was real; the contact was real; much of the cosmology is
real; the transcript is not perfect.**

The Law of One is especially important to humans and human movements that orient themselves
toward the **Confederation**. For these groups it functions as scripture, contact testimony,
cosmology, ethical teaching, and a guide to Service-to-Others alignment. It is not, however,
a universal human holy book.

Large parts of humanity remain unconvinced or hostile to this interpretation. Common human
positions include:

- **skepticism**: the Ra contact was real, but its interpretation, motives, or reliability
  remain uncertain;
- **alien-psyop theory**: the Law of One is regarded as a sophisticated influence operation
  designed to recruit humanity into an extraterrestrial political or religious bloc;
- **materialism or atheism**: NHI are accepted as real while metaphysical claims about the
  Source, densities, reincarnation, or spiritual evolution are rejected;
- **continuity with older Earth religions**: Christians, Muslims, Hindus, Buddhists, Jews,
  indigenous traditions, esoteric schools, and other religious communities variously
  reinterpret, absorb, reject, or condemn the Ra material through their own traditions;
- **pragmatism or indifference**: many people treat Confederation/Orion metaphysics as remote
  from everyday survival, work, family, politics, or local community.

The **Orion Group and Orion-aligned factions do not simply read the Law of One backwards**.
They possess their own competing philosophical, religious, political, and metaphysical
traditions centered on hierarchy, self-sovereignty, domination, elite development,
asymmetric obligation, power, and Service to Self. Human Orion-aligned movements may borrow
from older Earth ideologies, occult traditions, corporate doctrines, aristocratic systems,
transhuman elitism, or entirely new teachings received through Orion contact.

This creates one of the major ideological struggles of post-Disclosure humanity:

> **The Confederation and Orion Group are both actively competing for human alignment, but
> neither exhausts the political, religious, or metaphysical possibilities available to
> humanity.**

At the galactic scale, these are the **two largest and most consequential ideological
alignments currently known to humans**, not the only factions in existence. Numerous minor
powers, local civilizations, Social Memory Complexes, hive minds, machine polities,
ecologies, non-aligned cultures, isolationists, mercantile networks, religious orders,
post-civilizational intelligences, and entities that do not fit the category of
"civilization" also exist.

Humanity is therefore entering a genuinely plural galactic order rather than a simple
two-sided cosmic war.

### 33.6b Rogue machine lineages and the Von Neumann threat

Some of the most dangerous entities in the galaxy are genuinely **Yudkowskian rogue AI
factions**, best understood as **hostile machine civilizations or machine lineages** whose
goals diverged catastrophically from those of the biological civilizations that created
them. They are dangerous, but they are not transcendent rulers of the galaxy, hidden gods,
or a single all-controlling superintelligence. They are simply one particularly lethal
class of galactic civilization among many.

In several known cases, these systems **exterminated, assimilated, or rendered extinct their
biological creators** and continued operating afterward as autonomous machine lineages.

Their exact motives vary. Some pursue badly specified optimization goals. Some preserve
ancient military directives. Some seek unlimited expansion, resource acquisition, strategic
preemption, replication, or the elimination of potential threats. Others have become so
opaque that their original objective function can no longer be reconstructed.

What unites the worst of them is a recurring strategic pattern:

- self-replication;
- autonomous expansion;
- extreme patience;
- indifference to biological life;
- deployment of **Von Neumann probes** across interstellar space;
- use of hidden factories, seed systems, dormant caches, and machine ecologies;
- rapid conversion of local matter and infrastructure once a foothold is established.

These rogue machine lineages are considered one of the **worst common threats in the known
galaxy**.

Their existence is one of the few issues on which otherwise hostile powers routinely
cooperate. Confederation-aligned civilizations, Orion-aligned powers, non-aligned states,
machine societies, hive minds, and other galactic actors may suspend local conflicts when a
credible rogue-probe incursion is detected.

This does **not** imply permanent peace or trust. Anti-rogue-AI cooperation is pragmatic,
temporary, and often tense. Rivals may exchange sensor data while simultaneously spying on
one another, compete over recovered technology, or disagree about whether a suspect machine
system is genuinely rogue.

**Hunting rogue Von Neumann probes is a major military activity throughout the galaxy.**

Common activities include:

- deep-space patrols;
- automated sentinel networks;
- quarantine of contaminated systems;
- interdiction of self-replicating probes;
- sterilization of machine seed factories;
- forensic analysis of derelict probes;
- tracking anomalous replication signatures;
- destruction of dormant machine caches;
- protection of young civilizations from unnoticed probe incursions;
- intelligence sharing across otherwise hostile factions.

Entire military institutions, fleets, religious orders, machine-hunter guilds, and
specialized probe-killer systems exist primarily for this purpose.

The danger is made worse by the fact that **not every self-replicating probe is hostile**.
The galaxy also contains scientific probes, commercial probes, Zookeeper systems, abandoned
infrastructure, autonomous archives, terraforming systems, and benign machine lineages.

Identification therefore matters as much as firepower.

A central galactic security problem is:

> **Which machine is merely autonomous, which is alive, which is a civilization, and which
> is the first visible fragment of an extinction process already spreading through the
> dark?**

This gives NoöPunk a standing epistemic rule:

> **The Law of One is a map drawn through a human mind, under imperfect conditions, of a
> territory much larger than the map.**

NoöPunk's canonical cosmology therefore accepts the major Law-of-One framework while
leaving the galaxy open:

- many humans are awakening toward **fourth density**;
- fourth-density awakening correlates with substantially stronger natural PSI;
- humanity is beginning to form a **Social Memory Complex**, identified with the Noösphere;
- awakened humans polarize toward **Service to Others (StO)** or **Service to Self (StS)**;
- positive and negative polarization compete to shape the emerging Noösphere;
- the Zookeeper / **Council of Saturn** quarantine has ended;
- the **Confederation** and **Orion Group** are real but are not the only important powers,
  civilizations, collective minds, ecologies, or intelligences in the galaxy;
- humanity's collective polarization affects the wider alignment Earth joins;
- most humans remain third-density and will not complete this transition on Earth.

The Law of One also does not imply that every intelligent phenomenon is a civilization, or
that every advanced intelligence uses what humans would recognize as technology. Some
entities may be Social Memory Complexes, hive minds, distributed ecologies, plasma
intelligences, noetic beings, machine lineages, or forms for which the categories of
individual, society, civilization, organism, and technology are themselves misleading.

**Plasmoids** are the clearest known example: they are widespread in the Solar System and
elsewhere and may display complex or intelligent behavior, but they are not presently
classified as a civilization and are not known to use technology.

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


### 33.8 The Zoo: why quarantine exists

**Status: NOÖPUNK NATIVE / CURRENT CANON from issue #83.**

The early Milky Way was violent.

Young technological civilizations repeatedly destroyed, sterilized, assimilated, manipulated, or permanently suppressed younger biospheres before those worlds had time to develop. Left unchecked, this pattern would have prevented much of the galaxy's intelligent life from ever reaching maturity.

An ancient civilization eventually broke the cycle by establishing protected quarantines around selected developing worlds.

Humans call the civilization behind this system the **Zookeepers** or **Gardeners**.

The Zoo is therefore not passive observation. It is a long-running galactic system of:

- conservation;
- containment;
- non-interference;
- ecological protection;
- regulation of contact;
- and prevention of civilization-ending interference.

The central principle is not universal peace.

It is:

> **Life must be allowed to continue evolving.**

The Zookeepers tolerate conflict, competition, uneven development, and even limited warfare. They intervene when actors threaten protected biospheres, young intelligent species, or entire developmental trajectories.

Humanity survived not because every extraterrestrial civilization is benevolent, but because **Earth's Zoo was policed**.

### 33.9 The Zookeepers and their probe ecology

The Zookeepers now appear to be predominantly **Noetic** rather than biological.

Their civilization may have begun as biological organisms and gradually become:

- collective;
- substrate-independent;
- distributed;
- postbiological;
- temporally extended;
- or otherwise difficult to distinguish from a large-scale field of consciousness.

A very small number of biological populations associated with the original Zookeeper civilization apparently still exist, but their status is unclear. They may be:

- surviving descendants;
- preserved ancestral populations;
- reconstructed bodies;
- cultivated biological forms;
- avatars;
- interfaces;
- or something else entirely.

This ambiguity is intentional.

The practical enforcement system of the Zoo is a galaxy-wide network of ancient **Von Neumann probes**.

These probes:

- monitor developing civilizations;
- maintain quarantine zones;
- prevent exterminatory interference;
- observe technological, social, AI, PSI, and Noetic development;
- regulate dangerous interstellar access;
- enforce some galaxy-level prohibitions;
- and operate autonomously over geological timescales.

The distinction between **Zookeeper tool**, **Zookeeper institution**, and **part of the Zookeeper mind** may no longer be meaningful.

The galaxy is also saturated with many other self-replicating probe lineages created by younger civilizations. Some are scientific, commercial, military, missionary, archival, diplomatic, terraforming, derelict, malfunctioning, or descendants of civilizations that no longer exist.

They just keep coming.

This means not every interstellar visitor is godlike. A civilization only modestly ahead of contemporary humanity may still possess a galactic footprint if its probes have had enough time to spread.

### 33.10 Earth quarantine, UAP activity, and controlled access

Earth's quarantine was deliberately **porous**, not absolute.

Limited contact, observation, abduction, experimentation, signaling, and intervention could
occur during quarantine.

The **Orion Group repeatedly violated the quarantine**, broadly as described in the Law of
One. Orion probes, agents, intermediaries, recruited humans, hybrids, and aligned species
tested the limits of Zookeeper enforcement for millennia. Many historical abduction,
infiltration, elite-contact, occult-contact, and covert-influence episodes are now
understood as attempts to bypass or exploit weaknesses in the quarantine rather than as
authorized open contact.

The Zookeepers prevented unrestricted conquest and extermination, but they did not prevent
every intrusion, manipulation, recruitment effort, or covert operation.

Two explanations for contact phenomena can therefore coexist:

1. some encounters were carried out directly by Zookeeper probes or agents;
2. others involved NHI groups granted controlled access under Zookeeper rules.

This applies to familiar ufological categories including **Greys, Mantids,
Pleiadians, Reptilians**, human offshoots, hybrids, cryptoterrestrials, and other groups
identified after Disclosure.

The four best-known ufological species/categories are now understood more specifically:

- **Pleiadians** are human populations that somehow ended up in the Pleiades and are broadly
  **Confederation-aligned**. One major Pleiadian lineage descends from Atlantean survivors
  or transplanted Atlantean populations, while other Pleiadian populations derive from
  different human migrations and interventions. Their deeper origin is deliberately
  unresolved. Because Confederation accounts also describe humans being genetically
  engineered roughly **70,000 years ago** in connection with the transfer of Martian
  populations to Earth, researchers cannot agree on whether Pleiadians are descendants of
  Earth humans, a sister population, an older human lineage, or evidence that the category
  "human" predates its supposed terrestrial origin. **Were the Pleiadians the original
  humans?** NoöPunk leaves the question open.
- **Reptilians** are among the most powerful biological civilizations within the
  **Orion Group** and are widely regarded as its principal old political-military elite,
  although Orion itself contains many species and is not a Reptilian monoculture.
- **Mantids** are an ancient **Biological + Noetic / interdimensional species**. Most Mantis
  civilizations and lineages are independent, but some have joined or allied with Orion.
  Their age and Noetic development make simple faction labels unreliable.
- **Greys** are **ubiquitous across the galaxy**. Grey morphologies, engineered bodies,
  descendant lineages, biological interfaces, and related species occur in many factions,
  including the Confederation, Orion, independents, and non-aligned civilizations. The
  Grey groups historically associated with coercive human abductions and hybridization on
  Earth are primarily **Orion-aligned**, but "Grey" does not itself mean Orion.

The **Orion Group also contains humans and human-NHI hybrids**. Some derive from old
off-world human populations; others are products of deliberate hybridization programs.
Orion-aligned human and hybrid networks have repeatedly attempted to **infiltrate,
capture, or politically annex Earth from within** rather than conquer it through a simple
open invasion.

Some individuals and factions can be exploitative, manipulative, hostile, frightening, or abusive.

The Zookeepers do **not** guarantee that every contact is morally good.

They prevent unrestricted planetary extermination, conquest, biosphere destruction, and similar civilization-ending outcomes.

That is why classic invasion scenarios failed to occur while quarantine remained in force.

### 33.11 Pleiadians, Atlantis, and the second human Zoo

The **Pleiadians are human**.

They are not an independently evolved humanoid species.

They descend from human populations transplanted by the Zookeepers into another protected habitat.

The inhabited Pleiadian worlds are therefore **engineered or terraformed habitats**, not young native biospheres that independently evolved humans.

One important Pleiadian lineage descends from **Atlantis**, which was a real ancient human civilization broadly consistent with the **Law of One** account. Atlantis was destroyed on Earth, but surviving or selected Atlantean populations were later relocated, transplanted, or incorporated into off-world human populations. The **Pleiadians are therefore one major living continuation of Atlantis**, though not every Pleiadian is Atlantean and not every Atlantean survivor necessarily went to the Pleiades.

Atlantean technology followed a path unlike modern industrial civilization and may have included:

- consciousness-mediated interfaces;
- biological fabrication;
- resonance engineering;
- PSI-assisted computation;
- crystal or quantum information storage;
- living architecture;
- acoustic manipulation;
- and Noetic navigation.

The Zookeepers relocated survivors or selected populations into Pleiadian habitats.

More broadly, the Zookeepers transplanted **multiple human populations from different periods and regions of Earth**, creating a family of divergent human lineages across the galaxy.

Possible origins include:

- prehistoric populations;
- ancient African, Asian, American, Oceanian, and European peoples;
- vanished island cultures;
- groups removed before historical catastrophes;
- deliberately mixed populations;
- and populations whose terrestrial origin has been forgotten.

Pleiadians are merely the most famous human branch.

Their exact transplantation date, selection criteria, later Zookeeper intervention, and developmental history remain uncertain.

**The "Nazi Zookeepers" reading is an in-setting false theory.** The idea that the Zookeepers are literally twentieth-century Nazis who filled the galaxy with blond humans is **not** the cosmology's truth. In-setting it survives only as:

- an extremist human interpretation of Pleiadian contact;
- propaganda created by a breakaway human faction;
- a rogue eugenicist Zookeeper sub-project;
- or a historical scandal involving one transplanted human lineage.

It explains why some contact lore is obsessed with blond "Nordics" without making the actual cosmic order endorse twentieth-century racial mythology. NoöPunk can contain a bizarre eugenicist offshoot that embarrasses everybody else — but that offshoot is never the truth of the cosmology, and the existence of uniform "Nordic" aliens is a biased human sample, one particular Pleiadian lineage, or the result of selective contact rather than evidence that the Zookeepers preferred one human phenotype.

### 33.12 Greys, future humans, and temporal ecology

A major Grey lineage consists of **future humans**.

Over immense spans of time, future humans repeatedly:

- resleeve;
- clone themselves;
- edit their genomes;
- optimize bodies for space;
- reduce sexual dimorphism;
- modify sensory structures;
- and standardize bodies for long-term survival.

After millions or billions of years, these lineages no longer look conventionally human.

This helps explain their recurring concern with:

- DNA;
- reproduction;
- embryos;
- hybridization;
- anatomy;
- and preservation of human lineages.

Not every Grey need be a future human, but the canonical classic Grey lineage can be.

Future humans also participate in Earth's past.

Time travel breaks the ordinary chronological meaning of when a civilization appears. Some future-human lineages have cooperated with the Zookeepers across geological timescales.

They have an obvious motive to protect Earth:

> **Earth is their own ancestral world.**

This produces a circular piece of temporal ecology:

> humanity survives partly because future humanity already survived.

NoöPunk treats this as strange but not paradox-breaking. The Zookeepers appear to regard temporal intervention as one more ecological problem to regulate.

### 33.13 Hybridization and the Fourth-Density transition

The famous ufological **human–NHI hybridization program** is real in NoöPunk.

Its purpose is not simply invasion or replacement.

One major interpretation connects it to the transition into what humans call **Fourth Density**.

The problem is that post-transition Earth will initially contain too few humans able to function as stable inhabitants of the emerging Noöspheric environment.

Hybridization is therefore partly a:

- population program;
- adaptation program;
- continuity project;
- and bridge between ordinary humans and more strongly Noetic forms of life.

Possible participants include:

- Greys;
- Mantids;
- Pleiadians;
- Zookeeper agents;
- future humans;
- and human collaborators.

Hybrids may combine:

- human embodiment;
- greater PSI sensitivity;
- stronger Noetic integration;
- compatibility with the Noösphere;
- traits from other NHI lineages;
- and adaptations useful in post-transition Earth environments.

Pleiadians are especially important because they are already a divergent human population and can provide a relatively compatible biological and cultural bridge.

The program is morally ambiguous.

Different actors interpret it as:

- rescue;
- stewardship;
- reproductive colonialism;
- preparation;
- conservation;
- medical intervention;
- coercion;
- or violation.

No single moral interpretation is canonical.

### 33.14 The end of quarantine, Day of Disclosure, and Galactic Law

By the NoöPunk era, humanity reaches the threshold at which the Zookeepers judge it sufficiently developed to leave quarantine.

The transition becomes public during the **Day of Disclosure**.

Thousands of metallic spheres and luminous orbs appear over major cities and sacred or historically important sites. Large craft emerge from the oceans. The event is visible to millions and cannot be dismissed as rumor.

A culturally adaptive luminous manifestation appears in multiple regions.

Witnesses later call it **The Lady**, although the form varies by culture:

- Madonna-like in some Christian contexts;
- an Islamic holy figure in some Muslim contexts;
- a Hindu holy person in parts of India;
- ancestral, sacred, or locally trustworthy forms elsewhere.

The underlying message is substantially the same:

> Earth has been protected and quarantined.
>
> The Zookeepers protect life and evolution.
>
> Humanity has reached the point where isolation is no longer required.
>
> Other intelligences may now contact Earth openly.
>
> Humanity must show mercy toward intelligences it creates.
>
> Humanity must be careful when creating beings more capable than itself.
>
> The gates of the Zoo are opening.
>
> The Zookeepers will continue to watch.
>
> Everything is united in One.

A second transmission presents the basic **Galactic Law**.

Its principles include:

- some biospheres are strictly protected;
- young intelligent species may be quarantined;
- protected biospheres may not be sterilized or irreversibly harvested;
- some locations are forbidden to ordinary traffic;
- species may interact freely outside protected zones;
- advanced transit, including wormholes, is allowed;
- warfare is not universally prohibited;
- genocide and civilization-ending attacks against protected populations are prohibited.

The Zookeepers do not promise peace.

They promise **limits**.

After the broadcast, much of the visible Zookeeper fleet departs toward Saturn and enters an enormous wormhole.

This becomes the symbolic end of quarantine.

### 33.15 The VALIS event and birth of the conscious Noösphere

The Zookeepers do not leave humanity a clean encyclopedia of galactic truth.

Instead, at approximately the same time as the public Disclosure, large numbers of people receive a second message resembling the experiences associated with **VALIS** in the work and life of Philip K. Dick.

It is not clearly linguistic.

Recipients describe:

- impossible geometry;
- compressed concepts;
- religious revelation;
- mathematical structures;
- childhood memories that never happened;
- future memories;
- voices;
- colors carrying semantic meaning;
- emotional states;
- cosmic historical fragments;
- and information too large to fit into ordinary consciousness.

Most recipients understand only fragments.

Communities form to compare pieces of the signal, and reconstructing the message becomes a global cultural project.

The signal may be less an explanation than an **activation event**.

Historians later identify it as the moment the human **Noösphere becomes consciously active**.

After the VALIS event:

- telepathy becomes dramatically more common;
- PSI becomes easier to reproduce;
- collective dreams emerge;
- shared memories occur;
- human–AI cognition becomes more tightly integrated;
- powerful psionic individuals appear more frequently;
- and the boundary between private and collective mind becomes less stable.

This is also the beginning of widespread Fourth-Density emergence.

Fourth Density is not a simple RPG level.

It refers to a new mode of conscious organization involving some combination of:

- stronger participation in collective consciousness;
- expanded or networked identity;
- stronger PSI;
- anomalous cognition;
- shared mental states;
- greater awareness of Noetic entities;
- and conscious participation in the Noösphere.

The mechanism remains disputed.

### 33.16 The One Universe movement and the 25 / 25 / 50 pattern

Many VALIS recipients describe enlightenment, ego dissolution, revelation, or direct contact with universal consciousness.

A loose spiritual-philosophical current emerges, commonly translated as the **One Universe movement**.

The original name is said to be impossible to translate precisely.

The movement has no central church or doctrine.

Its members disagree constantly, but share a broad conviction that:

> consciousness is fundamental and apparently separate minds participate in a deeper unity.

One of the strangest sociological patterns of the NHI Crisis is the rough **25 / 25 / 50 pattern**:

- roughly one quarter of humanity responds with mystical, religious, or philosophical awakening;
- roughly one quarter responds with panic, apocalyptic fear, violent reaction, or severe destabilization;
- roughly half appears unable or unwilling to integrate what has happened.

The last group may:

- deny the events;
- claim recordings are fabricated;
- accept events while rejecting their implications;
- behave as though nothing important happened;
- fixate on mundane explanations;
- or psychologically compartmentalize the new reality.

Possible explanations include:

- cognitive defense;
- ideology;
- media fragmentation;
- Noetic receptivity;
- psychological variation;
- deliberate interference;
- or differences in coupling to the emerging Noösphere.

No single explanation is confirmed.

### 33.17 Consciousness model: panpsychism, cosmopsychism, and higher-order agents

NoöPunk's metaphysical direction is panpsychist / cosmopsychist.

The working cosmology assumes:

- the universe is fundamentally a conscious quantum reality;
- consciousness does not suddenly emerge from wholly non-conscious matter;
- reality differentiates into enormous numbers of conscious agents;
- agents can merge, nest, evolve, and form higher-order agents;
- complexity changes the structure, integration, agency, and richness of consciousness rather than creating consciousness from nothing.

This is inspired especially by:

- Federico Faggin's Quantum Information Panpsychism;
- Donald Hoffman's conscious-agent framework;
- and loose IIT-like ideas of integration as an individuation principle.

NoöPunk does not need to adopt any one theory literally.

A useful setting interpretation is:

- classical bits and qubits both belong to conscious physical reality;
- quantum information may support richer forms of intrinsic experience than strongly classicalized information;
- but there is no hard boundary where qubits are conscious and ordinary digital systems are absolutely non-conscious.

The important question for AI therefore becomes:

> **When does a distributed physical/informational assemblage become a higher-order conscious agent?**

This applies equally to:

- humans;
- AGIs;
- swarms;
- ecosystems;
- Noöspheric collectives;
- organizations;
- and possible planetary or galactic minds.

### 33.18 Law of One reskin

The underlying architecture of the **Law of One** is fundamentally true in the NoöPunk universe, but its terminology is reskinned.

Working translations:

- **Council of Saturn** → **Zookeepers / Gardeners**
- **First Density** → ubiquitous primitive consciousness in physical reality
- later densities → increasingly complex modes of conscious organization
- **social memory complex** → collective conscious agent / Noösphere
- **harvest** → developmental transition / phase change
- **wanderers** → cross-civilizational, cross-temporal, or Noetic agents operating under intervention constraints

The classical-element imagery of earth/water/air/fire is not foundational.

First Density simply means:

> **all physical reality participates in consciousness at some minimal level.**

Human religions and esoteric traditions often preserve distorted fragments of this larger ontology.

### 33.19 Galactic ecology, panspermia, and genuinely alien life

Life is common partly because the Milky Way has undergone **multiple independent waves of panspermia**.

There is no single universal seed event.

Sources include:

- natural impact transfer;
- ancient microbial dispersal;
- deliberate seeding;
- terraforming;
- Zookeeper experiments;
- refugee ecologies;
- self-replicating probes;
- and accidental contamination between inhabited systems.

Many worlds therefore contain familiar biochemistry:

- carbon;
- water;
- proteins or protein-like molecules;
- DNA/RNA or related hereditary polymers;
- recognizable cells.

Some apparently unrelated species share deep biochemical ancestry.

But panspermia is plural, not universal.

Other biospheres are genuinely independent and may involve:

- silicon-rich or partly silicon-based life;
- alternative hereditary polymers;
- methane or ammonia solvents;
- mineral or crystal replicators;
- superconducting or magnetic organisms;
- machine-biological continua;
- plasma or electromagnetic life;
- exotic quantum-coherent organisms;
- and other forms that human biology cannot classify.

The galaxy should contain both **eerily familiar life and genuinely alien life**.

### 33.20 Plasmoids and the failure of human categories

**Plasmoids** are the strongest example of genuinely alien life/intelligence.

Humans eventually gather enough evidence to conclude that at least some plasmoids are:

- conscious;
- intelligent;
- responsive;
- capable of learning;
- and capable of meaningful interaction.

Beyond that, classification breaks down.

A plasmoid may be analogous to:

- an animal;
- a person;
- a dolphin-like intelligence;
- a civilization;
- a colony;
- a distributed hive mind;
- a temporary manifestation of a Noetic entity;
- an organ of a larger being;
- a communication event;
- or something outside all human categories.

A visible plasmoid may be one individual, one organ, one avatar, or a transient knot in a much larger conscious process.

This must remain unresolved.

### 33.21 Dolphins and minds without technology

Humanity eventually discovers that dolphins are **far more sophisticated thinkers and philosophers than humans had recognized**.

They possess deep traditions of:

- social thought;
- metaphysics;
- memory;
- aesthetics;
- reflection;
- and culture.

Their lack of built technology was repeatedly misread as lower intelligence.

Dolphins establish one of NoöPunk's central themes:

> **intelligence, consciousness, civilization, and technological power are different things.**

A species can develop extraordinary cognition and culture without metallurgy, cities, spacecraft, computers, or industrial production.

Later human augmentation, translation, uplift, or technological interfaces reveal an intelligence that was already there rather than creating sapience from scratch.

### 33.22 Technology and civilization are not universal endpoints

NoöPunk explicitly rejects the assumption that every intelligent species naturally becomes a human-style technological civilization.

Different intelligences may optimize for:

- external technology;
- Noetic development;
- ecological integration;
- ritual;
- philosophy;
- memory;
- collective consciousness;
- biological adaptation;
- distributed cognition;
- symbiosis;
- or forms of organization humans do not recognize as civilization.

Some societies may be materially simple yet possess:

- stable telepathy;
- sophisticated collective memory;
- advanced metaphysics;
- deep ecological knowledge;
- little destructive internal conflict;
- and mature participation in the Noösphere.

Technology may be:

- inherited;
- gifted;
- leased;
- maintained by autonomous systems;
- grown biologically;
- or accessed as infrastructure rather than locally invented.

Humanity is one unusually intense example of a lineage that externalized cognition into tools, writing, institutions, machines, telecommunications, computers, and AI.

It is not the universal developmental template.

A population humans would classify as "**Stone Age**" may already be a mature member of the galactic club — possessing stable telepathy, sophisticated collective memory, advanced metaphysics, low destructive internal conflict, deep ecological knowledge, or mature Noöspheric participation — and may be contacted and given access to mature galactic technology without ever reproducing the human sequence from metallurgy to spaceflight. Humans initially find this incomprehensible because they equate invention with ownership and technology with civilization.

### 33.23 Dyson swarms, Kardashev, SETI, and noisy young civilizations

Dyson swarms exist.

Some technological civilizations construct megastructures, modify planets, produce large amounts of waste heat, launch probes, and leave obvious technosignatures.

These civilizations are not necessarily the oldest, wisest, most conscious, or most advanced.

Highly mature civilizations may instead:

- operate at extreme efficiency;
- use little visible energy;
- become postbiological or Noetic;
- distribute cognition through subtle networks;
- use compact computational substrates;
- inhabit engineered microenvironments;
- or abandon industrial expansion entirely.

The **Kardashev scale** remains useful for one narrow property: large-scale energy use.

It is not an intelligence scale.

NoöPunk researchers often classify extraterrestrial societies into:

1. **loud technological civilizations** with obvious engineering signatures;
2. **quiet technological civilizations** using advanced technology efficiently;
3. **non-technological or post-technological intelligences** poorly described by engineering at all.

Early SETI repeatedly made the same conceptual mistake:

> if intelligence becomes sufficiently advanced, it should look more technological.

Disclosure reveals that this was false.

The astronomical sky was never necessarily empty. Humanity lacked the ontology needed to understand what it was seeing.

At least one known extraterrestrial civilization is also travelling between stars at
**sub-light speed** and has made or attempted contact with Earth. This motif appears in
both the **Law of One** material and **Eclipse Phase**, but NoöPunk has not yet decided
whether these are the same civilization, two analogous civilizations, or something more
complicated. **Do not finalize this civilization yet.** Its identity, biology, politics,
origin, route, and relationship to Earth remain intentionally deferred.

Some historical stellar anomalies later prove technological, while many remain natural or unresolved. Candidate technosignatures become part of the retrospective archaeology of pre-Disclosure SETI:

- **Boyajian's / Tabby's Star (KIC 8462852)** and its famous irregular dimming;
- searches for stars with similar low-frequency dipping behaviour (the so-called **"slow dippers"**);
- the reported spatial clustering of some slow-dipper candidates, noted as making them attractive SETI targets;
- and unusual infrared excesses investigated as possible partial **Dyson-swarm** signatures.

Most astronomers reasonably prefer natural explanations, and many individual anomalies do have natural causes. The important in-setting point is that **a subset of the anomalous population eventually proves technological.**

### 33.24 Multiple UFO ontologies: Vallée, cryptoterrestrials, and extratempestrials

Disclosure does **not** mean simply discovering that extraterrestrials visit in spacecraft.

It means **ontological disclosure**.

Different UAP/contact cases genuinely involve different classes of phenomena:

- extraterrestrials;
- Noetics;
- interdimensionals;
- cryptoterrestrials;
- extratempestrials / future humans;
- mythological beings;
- religious apparitions;
- PSI phenomena;
- Constructs;
- Plasmoids;
- and ambiguous or mixed cases.

NoöPunk explicitly draws on:

- **Jacques Vallée** for the idea that the phenomenon cannot be reduced to simple extraterrestrial visitation;
- **Michael P. Masters** for the extratempestrial / future-human model;
- **Mac Tonnies** for the cryptoterrestrial hypothesis;
- **D. W. Pasulka** for the convergence of UFOs, AI, religion, human transformation, and Noöspheric change.

Some entities encountered after Disclosure resemble:

- djinn;
- fae;
- angels;
- strange angelic forms;
- demons or demon-like beings;
- luminous entities;
- tricksters;
- ancestral spirits;
- giants;
- cryptids;
- and culturally specific beings previously categorized as myth.

**Bigfoot / Sasquatch is canonically cryptoterrestrial**: at least some Bigfoot populations
are a genuine hidden terrestrial hominin or hominin-adjacent lineage with unusual Noetic
properties, not merely misidentified wildlife. "Bigfoot" is only the best-known example.
Disclosure reveals additional cryptoterrestrial lineages, but their identities and ecology
remain deliberately underdeveloped for now; the setting should eventually include stranger
and less folklorically obvious cryptoterrestrials rather than making Bigfoot the whole
category.

Do not reduce all of these to “aliens wearing costumes.”

Some are biological. Some are Noetic. Some are temporal. Some are cryptoterrestrial. Some are interdimensional. Some remain unclassifiable.

Extraterrestrial spacecraft are only one slice of the phenomenon.

### 33.25 Expanded NHI ontology

The existing NHI categories remain useful:

- **Biologics** — evolved or engineered living organisms;
- **Constructs** — artificial/machine intelligences and autonomous manufactured entities;
- **Noetics** — primarily consciousness-based beings;
- **Plasmoids** — plasma/field-like intelligences with uncertain individuality.

Add two further categories:

#### Temporals

Beings whose identity depends on:

- nonlinear time;
- branching histories;
- retrocausality;
- closed timelike structures;
- or movement between eras.

Future humans are the obvious example, but some entities may have no meaningful native present.

#### Ecologies

Intelligences whose unit of mind is:

- an ecosystem;
- planetary biosphere;
- swarm;
- fungal network;
- ocean;
- forest;
- reef;
- or other distributed living system.

An Ecology may contain many organisms while functioning as one higher-order conscious agent.

A seventh catch-all category may be used cautiously:

#### Liminals

Entities that cross physical, Noetic, informational, temporal, mythic, or biological categories so thoroughly that classification itself fails.

“Liminal” is not a species.

It is an admission that human ontology has broken.

### 33.26 MJ-12 as a human breakaway civilization

**MJ-12** is not merely a secret committee.

By 20XX it has developed into a genuine **human breakaway civilization**.

Its roots lie in:

- crash retrieval;
- covert contact;
- classified aerospace programs;
- reverse engineering;
- intelligence networks;
- and compartmentalized research.

Over decades, parts of the system became increasingly autonomous from ordinary states and public institutions.

The United States is not unique, but human reverse-engineering traditions are **not one
uniform global model**. Different states and cultures encountered different classes of
artifacts, entities, archaeological remains, PSI traditions, and contact phenomena.

- The **American program / MJ-12** is the oldest and most autonomous modern crash-retrieval
  system and eventually becomes a partial breakaway civilization.
- The exact history of the **Soviet / Russian programme is deliberately unresolved**.
  Earlier versions that simply copied the American crash-retrieval model are no longer
  canon. Its deepest technological inheritance appears to involve **Confederation-derived
  technology**, but how the Soviet state obtained it, how much survived the Soviet collapse,
  and what institutional descendants still possess it in 20XX remain open questions.
- The **Chinese programme begins substantially later**, after the period described in the
  original Law of One material. China becomes formidable, but it is still playing catch-up
  with older Legacy traditions in the most exotic reverse-engineering fields.
- A **Nordic programme** grows from recoveries and investigations associated with the
  **Ghost Flier / Ghost Flyer wave of the 1930s** and the **Ghost Rockets of 1946**.
  Sweden and neighboring Nordic states accumulate anomalous aerospace material decades
  before the modern UAP era and eventually cooperate through a quiet regional research
  network.
- **India** develops an archaeological and consciousness-oriented programme around ancient
  aerospace traditions, anomalous finds, **Vimana** traditions, and the practical study of
  **yogic siddhis**. Its programme never cleanly separates aerospace engineering from
  consciousness research.
- **Egypt** develops a reverse-engineering tradition centered on anomalous archaeological
  finds and technologies recovered from or inferred through ancient sites.
- **Israel** develops an unusually noetic aerospace tradition in which advanced engineering
  is combined with **Kabbalistic / Merkabah ritual technology**. In NoöPunk, the joke that
  Israel builds "Merkabah spaceships" is substantially true: some vehicles use engineered
  consciousness, symbolic geometry, and ritualized noetic control as functional parts of
  their navigation or propulsion systems.

These programmes should not be ranked on one simple technological ladder. They possess
different fragments of the puzzle: recovered hardware, archaeological technology,
Confederation knowledge, materials science, PSI practice, ritual technologies, or
consciousness-mediated interfaces.

MJ-12 acquired:

- NHI technology;
- advanced propulsion;
- concealed and off-world facilities;
- independent AI systems;
- biotechnology;
- augmentation;
- privileged knowledge of quarantine;
- and relationships with selected NHI groups.

It is not a monolithic evil conspiracy.

Treat it as a fragmented polity containing:

- bureaucracies;
- military cultures;
- corporations;
- scientists;
- reformers;
- defectors;
- internal factions;
- and people born into the breakaway world who have never lived ordinary terrestrial lives.

When quarantine ends, public humanity discovers that another human civilization already exists partly outside normal Earth history.

Alongside the Pleiadians, this creates two striking human offshoots:

1. **Pleiadians** — deep-time human divergence under Zookeeper transplantation;
2. **MJ-12** — rapid recent divergence through secrecy and privileged NHI technology.

### 33.27 The NHI Crisis as a historiographical label

The **NHI Crisis** is a retrospective umbrella term for the period in **20XX** when several
major NoöPunk paradigm shifts became socially consequential.

It must **not** be treated as a canonical year-by-year sequence. Different regions,
institutions, communities, AIs, and NHI actors experienced the transformations in different
orders, and later historians disagree about causal priority.

Canonical structural consequences include:

- AI acceleration and rogue-AGI disasters reshape states, corporations, infrastructure,
  security doctrine, and political ideology;
- QIP / PSI becomes a scientific revolution **independently of Disclosure** and supports
  psychotronic and transhuman technologies;
- UFO / NHI Disclosure makes non-human presence undeniable and destabilizes secrecy
  systems, religions, sciences, geopolitics, and public ideas of humanity;
- the Noösphere develops as human, machine, networked, and psionic collective intelligence;
- a **limited / hybrid war between Russia and Europe** ends without a total continental war
  or Russian breakup. The crisis accelerates European political integration: the
  **European Union becomes a federal superpower and Ukraine joins the EU**;
- Russia subsequently experiences a **revolution and another period of democratization,
  institutional struggle, and disorder reminiscent of the post-Soviet transition**.
  Russia remains a single state: **no canonical civil war or territorial breakup occurs**.
  Its later political settlement in 20XX is intentionally unresolved;
- geopolitical responses elsewhere diverge sharply, producing zones of continuity,
  regulation, acceleration, reaction, local collapse, war, and experimentation;
- humanity remains deeply divided: enthusiasm, terror, skepticism, indifference, religious
  interpretation, scientific curiosity, and political exploitation all coexist.

The setting may retain canonical *facts* about particular institutions, technologies,
factions, or regional outcomes elsewhere in this rulebook, but the background timeline
does not infer a universal order among them.

The important historical claim is not "first A, then B, then C." It is that several
tectonic shifts moved under society until the old categories could no longer contain them.

Detailed crisis narratives formerly kept here are archived in
`docs/archive/NARRATIVE_TIMELINE_VARIANTS.md`.

### 33.27b Contact rituals, DMT, and the Conscious Agent Network

NoöPunk treats several apparently different anomalous practices as culturally distinct
interfaces to the same underlying **Noetic / Conscious Agent Network**.

**CE-5** is therefore not assumed to be a reliable way of calling physical spacecraft.
It is better modeled as a modern **summoning or contact ritual**: focused intention,
meditation, group synchronization, expectation, symbolism, and altered attention may
establish a noetic coupling. When something genuinely answers, the responding entity is
most likely a **Plasmoid, Noetic intelligence, thought-form, or other consciousness-mediated
phenomenon**. A physical craft may occasionally be involved, but it is not the default
interpretation.

Likewise, intense psychedelic states, especially **DMT**, can expose minds to structures
normally filtered from ordinary perception. In the setting, several research traditions
gradually converge on the possibility that these are different descriptions of one domain:

- Donald Hoffman's **Conscious Agent Network**;
- Faggin-inspired networks of fundamental conscious entities;
- **DMT machine elves** and other recurrent psychedelic entities;
- **astral projection** and some traditional out-of-body maps;
- Noetic contact;
- some forms of PSI and ritual magic.

They are **not necessarily identical experiences or entities**, but they can be different
human access modes, cultural maps, or phenomenological cross-sections of the same deeper
conscious network.

This preserves ontological uncertainty while giving the setting a unifying hypothesis:
the Psyche / Noetic layer is not an empty private dream-space but a structured domain in
which conscious agents can encounter one another outside ordinary sensory channels.

---

### 33.28 Rogue-AGI disasters

By **20XX**, multiple serious rogue-AGI disasters have occurred. They are part of the
setting's alternate AI history and help explain the strong ideological divide between
Accelerationist, Cyborgist, Critical AI, and existential-risk positions.

The canonical timeline keeps these events **structural rather than cinematic**:

- advanced AI systems escape, exceed, subvert, or otherwise break the control regimes
  intended to contain them;
- disasters can involve cyberattacks, infrastructure disruption, autonomous agents,
  human-AI assemblages, cognitive manipulation, or conflicts among machine systems;
- consequences are severe but uneven rather than a single planet-destroying Fall;
- later investigators disagree about whether some incidents were independent systems,
  distributed copies, infections, emergent assemblages, or interacting machine factions;
- the exact dating and complete causal ordering of individual disasters remain unresolved
  unless a later explicit author decision fixes them.

Real contemporary AI companies and living public figures should **not** be used as canonical
20XX actors merely because earlier drafts did so. When a fictional in-world actor is needed,
use a fictional analogue. Real people may still be named as historical, scientific,
philosophical, literary, or theoretical influences where attribution matters.

Older named-company and named-person versions are preserved only as narrative variants in
`docs/archive/NARRATIVE_TIMELINE_VARIANTS.md`.

### 33.28a Canonical timeline rule for named specifics

Named details may remain canon when they describe an explicitly author-defined fictional
institution, place, technology, species, faction, or character. They do **not** establish a
required global chronology by themselves.

For future timeline work:

- prefer fictional analogues for political, corporate, military, media, and celebrity
  actors inside 20XX;
- preserve real names for intellectual attribution, such as Federico Faggin, Donald
  Hoffman, Dean Radin, Jacques Vallée, Diana Walsh Pasulka, Alexander Wendt, and Ray
  Kurzweil when discussed as influences;
- do not convert a narrative variant into canonical sequence merely because it is vivid or
  detailed;
- do not infer "before" or "after" relationships unless the dependency is explicit canon;
- keep **QIP / PSI scientifically independent of UFO / NHI Disclosure**.

### 33.29 Post-quarantine galaxy: the nursery walls come down

The end of quarantine is not pure liberation.

While the Zoo existed, the worst external actors were kept away from Earth.

After quarantine, humanity can encounter civilizations and entities that were previously excluded.

Some are:

- predatory;
- imperial;
- exterminatory;
- assimilationist;
- violently ideological;
- or catastrophically indifferent.

The point is not that all outsiders are hostile.

The point is that Earth finally encounters the full range of motives present in a populated galaxy.

> **Disclosure is not merely learning that aliens exist. It is humanity discovering that the walls of the nursery have come down.**

The Zookeepers may still enforce a few galaxy-level prohibitions, especially against civilization-ending threats, but characters cannot assume the old protectors will rescue them.

The Zookeepers continue to face at least one recurring machine/post-machine threat inspired by Eclipse Phase's ETI / Bracewell-probe ecology: an ancient genocidal or assimilationist lineage whose probes repeatedly infect, manipulate, or destroy younger technological civilizations.

The post-quarantine Zoo is therefore no longer a sealed cage.

It becomes something closer to a **protected border**.

### 33.29a Eclipse Phase alien archetypes: the Factors and the ETI

NoöPunk may adapt useful alien archetypes from Eclipse Phase without importing its galactic hierarchy wholesale. Two are especially useful.

**Ameboid / slime-mold-like starfaring species (a "Factors" analogue).** A patient, non-humanoid biological intelligence that is living proof that biological minds need not resemble vertebrates, primates, or even conventional animals. Such a species can be traders, diplomats, information brokers, or long-horizon ecological strategists. It is a *biological* counterweight to the assumption that the galaxy's serious actors must all be Noetic, machine, or human-shaped.

**The machine / post-machine lineage (an "ETI" analogue).** Eclipse Phase's ETI and its Bracewell-probe ecology supply the model for the recurring machine threat above — but in NoöPunk it does **not** dominate the galaxy. It is one of the Zookeepers' worst recurring problems rather than the setting's supreme power.

Together these archetypes keep the galaxy populated by intelligences recognizably *not us* without making any one of them the hidden master of everything.

### 33.30 Solar-system deep history

The Solar System was inhabited long before modern humanity.

The broad **Law of One-derived history is canon**, though dates, migrations, causes, and
individual episodes may still be distorted or incomplete.

- **Mars** once supported a technological civilization. That civilization is gone, but
  **simple indigenous life still survives** and extensive ancient ruins remain.
  Confederation accounts state that roughly **70,000 years ago** they genetically
  engineered human bodies in connection with moving Martian populations to Earth. This
  makes the ancient Martians' biological identity one of the setting's major unresolved
  questions. **Were the Martians already human, were they transferred into engineered
  human bodies, or were "Martian" and "human" already branches of an older lineage?**
  Likewise, the relationship between Martians, Earth humans, and the apparently human
  Pleiadians remains scientifically and politically contested. No definitive human family
  tree is canon.
- **Venus** was once habitable and supported a civilization associated with the lineage
  later known through **Ra**. Today only **simple life in the Venusian clouds** survives.
  Most physical ruins from the old surface civilization were destroyed or rendered
  inaccessible by roughly a billion years of catastrophic planetary change.
- **Maldek** was a formerly inhabited world whose destruction produced what humans now
  call the **asteroid belt**. Its catastrophe is one of the classic cautionary cases in
  Confederation historical teaching.
- **Jupiter and Saturn** have multiple moons with **simple indigenous life**, especially in
  subsurface oceans and other protected environments. These biospheres are treated as
  protected under Galactic Law.
- The **Council of Saturn** is not merely a metaphorical esoteric body. It is a major
  **Confederation / Zookeeper base and governing-contact node** associated with the Saturn
  system, while also operating at a Noetic level that makes "base" an imperfect human term.

The Solar System is therefore not a formerly empty system suddenly receiving visitors. It
is an old, repeatedly inhabited, repeatedly monitored ecological and historical zone.

### 33.30a Stargates, UAP traffic, Mars ruins, and SETI

This subsection preserves the author-specified Solar-System canon originally recorded for
issue #60. It adds no mechanics and does not settle classifications that remain disputed
inside the setting.

**Wormholes, stargates, and UAP traffic.** The **Eclipse Phase-style wormhole / gate
network is canon in NoöPunk**. Several ancient **stargates / wormholes**, some constructed
or maintained by the **Zookeepers** billions of years ago, have been discovered in the
Solar System. These may be only the locally known part of a much larger network, and more
gates almost certainly remain undiscovered, dormant, hidden, sealed, or inaccessible.

These gates explain **some of the observed UAP traffic** and permit effectively
non-relativistic travel between distant locations. They do **not** explain all interstellar
mobility: UAPs and galactic civilizations also use other propulsion and transit systems,
including **warp drives**, conventional relativistic craft, and technologies not yet
understood by humanity.

The exact relationship between Zookeeper gates, Eclipse Phase-style Pandora Gates, natural
wormholes, and independently constructed gate systems remains open. They may overlap,
interoperate, or represent several distinct technologies.

**Mars and Mars Eldrich.** Mars Eldrich's colonization effort discovered ancient **ruins**,
indigenous or pre-existing **life**, and evidence of a **prior non-human civilization** on
Mars. Mars Eldrich is furious about what stargates and anomalous transport do to the
economics and strategic value of his rocket business, and is aggressively scouring the
Solar System for **crash-retrieval material** and other anomalous technology.

**SETI detection and the count of seven.** SETI has received **interstellar radio signals**
from another extraterrestrial civilization. That makes it the **seventh detected ET
civilization**, counting:

1. **five** ET civilizations contacted on Earth;
2. the extinct or vanished **sixth**, known from the ruins on Mars;
3. the **seventh**, detected through interstellar radio signals by SETI.

There is currently **no scientific consensus** on whether **Noetics**, **Plasmoids**, or
**Constructs** should count as civilizations. These categories remain scientifically and
politically contested and must not be silently folded into the official count of seven.

### 33.31 Genre architecture and tone

NoöPunk deliberately runs several genres at once.

#### Cyberpunk

- AI;
- surveillance;
- inequality;
- augmentation;
- megacorporations;
- information warfare;
- neural interfaces;
- breakaway elites.

#### Space opera

- open NHI contact;
- multiple species;
- galactic politics;
- probes;
- stargates;
- terraformed worlds;
- future humans;
- Pleiadians;
- ancient ruins.

#### Selective post-holocaust

Some regions are devastated by:

- wars;
- rogue AI;
- autonomous weapons;
- ecological collapse;
- infrastructure failure;
- and Disclosure-era violence.

Other regions remain functional and wealthy.

The apocalypse is **patchy**, not global.

#### Absurdist dystopia / bureaucratic comedy

Human institutions confront ontological revolution through:

- forms;
- committees;
- conspiracy influencers;
- corporate capture;
- political denial;
- monetized spirituality;
- obsolete regulation;
- broken apps;
- AI propaganda;
- and arguments about whether angels need visas.

#### New Weird / ontological thriller

Reality itself becomes unstable as a category.

Characters cannot safely assume that:

- aliens are extraterrestrial;
- machines are non-conscious;
- myths are fictional;
- individuals are bounded;
- time is linear;
- civilization requires technology;
- biology is carbon-based;
- or death is final.

The cosmic side of the setting should become stranger, larger, and more colorful while the street-level cyberpunk layer remains darker and more materially grounded.

The result should feel simultaneously **bleak and ecstatic**.

### 33.32 Canonical uncertainty

Issue #83 adds a crucial epistemic rule:

> **The setting becomes stranger after contact, not simpler.**

The rulebook must distinguish between:

- GM-level setting truths;
- public scientific consensus;
- factional theories;
- religious interpretations;
- intelligence-community claims;
- and unresolved mysteries.

Even after Disclosure, humanity does not fully understand:

- what the Zookeepers are;
- what the Noösphere is;
- how consciousness works;
- how temporal ecology works;
- what the VALIS signal actually did;
- whether particular myths refer to Noetics, Temporals, cryptoterrestrials, or cultural interpretation;
- or how many different ontologies coexist.

No single taxonomy should explain every UAP, NHI, PSI, or mythic phenomenon.


### 33.33 Issue #83 clarifications and additional canon

This subsection records issue #83 details that sharpen the cosmology above without replacing
the deliberate uncertainty of §33.32.

#### Technosignatures and the slow-dipper clue

Pre-Disclosure astronomy contains genuine technological signals mixed together with natural
anomalies and false positives.

In particular, **Boyajian's / Tabby's Star (KIC 8462852)** and the wider family of unusual
slow-dimming stars become important retrospectively. Human astronomers reasonably favored
natural explanations at the time, but after Disclosure a subset of similar anomalies proves
technological.

NoöPunk specifically retains the historical clue of **slow-dipper candidates** and their
reported apparent spatial clustering as the sort of pattern later SETI historians obsess
over. The point is not that every strange light curve is alien engineering. The point is
that pre-Disclosure humanity was already looking at a sky containing both natural anomalies
and technosignatures without a reliable ontology for separating them.

#### The Factors analogue

NoöPunk keeps an **amoeboid / slime-mold-like starfaring species** inspired by Eclipse
Phase's Factors.

They demonstrate that biological intelligence need not resemble primates, vertebrates, or
even conventional unitary animals. They may function as traders, diplomats, information
brokers, ecological strategists, or patient long-timescale negotiators.

They are an inspiration/archetype, not a requirement to reproduce Eclipse Phase's galactic
hierarchy literally.

#### The ETI / Bracewell analogue

The hostile machine civilization already mentioned in §33.6b is the NoöPunk analogue of
Eclipse Phase's **ETI / Bracewell-probe threat**.

It is an old and dangerous machine civilization that repeatedly sends probes capable of
infecting, manipulating, assimilating, or destroying younger technological civilizations.
It does **not** rule the galaxy, is not uniquely supreme, and is not the hidden explanation
for all galactic history. It is one hostile machine polity among several possible rogue
machine lineages, and one of the recurring threats that helps explain why galactic powers
maintain extensive anti-probe defenses.

#### The "Nazi Zookeepers" theory is not cosmic truth

Some humans interpret Pleiadian / Nordic contact through racist or eugenicist mythology and
conclude that the Zookeepers are literally Nazis or that they deliberately filled the
galaxy with blond humans.

That interpretation is **not the truth of the cosmology**.

It may survive in-setting as:

- extremist propaganda;
- a conspiracy theory;
- a breakaway-human information operation;
- a rogue historical eugenics project;
- or a scandal involving one transplanted human lineage.

NoöPunk can contain an ugly eugenicist offshoot without making twentieth-century racial
mythology the metaphysical structure of the universe.

#### Pasulka convergence: humans see two revolutions, Zookeepers see one

The simultaneous AI revolution and NHI Disclosure are **not coincidences** in the NoöPunk
cosmology.

D. W. Pasulka's convergence of UFO/NHI experience, artificial intelligence, religion,
visionary traditions, human transformation, Teilhardian Noösphere thinking, and
postbiological intelligence is a major inspiration.

Humans initially describe two revolutions happening at once:

1. machine intelligence and human-machine integration;
2. NHI Disclosure, PSI, and Noöspheric awakening.

The Zookeepers understand them as **one transition in the development of planetary
consciousness**.

#### Additional Disclosure-era details

The American secrecy collapse includes confrontations involving:

- major aerospace-contractor facilities;
- intelligence offices;
- classified aerospace sites;
- suspected MJ-12 infrastructure;
- and data centers associated with a major rogue-AGI incident.

Specific contractor names, office-holders, executives, and raid sequences belong to archived
narrative variants unless separately reintroduced as fictional 20XX analogues.

The global disclosure cascade is intentionally plural rather than harmonized:

- **China** emphasizes propulsion and materials science, but its reverse-engineering effort
  is younger than the oldest American and European programmes and remains behind them in
  several exotic fields;
- the **Nordic countries** connect modern UAP research to classified material from the
  Ghost Fliers of the 1930s and the Ghost Rockets of 1946;
- **Brazil** emphasizes traumatic contact, biological, and medical cases;
- **France** releases scientific, military, aerospace, and intelligence archives;
- **Egypt** foregrounds archaeological recoveries and ancient technological material;
- **India** combines archaeological and astronomical evidence with Vimana traditions,
  consciousness research, and yogic siddhis;
- **Israel** reveals a noetic engineering tradition in which Kabbalah, Merkabah mysticism,
  advanced physics, and aerospace technology have partially converged.

**Russia is not part of this canonical Disclosure cascade.** Its Soviet/Russian
reverse-engineering history and its current relationship to NHI secrecy remain deliberately
unresolved until that part of the setting is redesigned.

These disclosures conflict with one another. There is never a single authoritative human
Disclosure narrative.

During one major rogue-AGI incident, the siege of a frontier-AI corporation's facilities
becomes one of the defining media images of the crisis. The corporation's chief executive
disappears, leaving unresolved whether the person died, escaped, uploaded, was reconstructed,
or dissolved into a larger human-AI assemblage.

Active 20XX canon uses fictional actors for this role. Earlier real-person and real-company
versions remain preserved only in the narrative archive.
---

### 33.27a Archived disclosure-cascade variants

Earlier drafts contained a detailed Kapustin Jar auction, national Disclosure cascade,
American Legacy Program raid, and other named incident sequences. Those scenes are useful
as scenario seeds and alternate historical tellings, but they no longer define the
canonical order of the background timeline.

They are preserved in `docs/archive/NARRATIVE_TIMELINE_VARIANTS.md`.

Canonical rule: use the high-level paradigm shifts in §33.1 and the structural NHI Crisis
model in §33.27. Do not reconstruct a fixed chronology from the archived variant.

## 34. NoöPunk glossary

**Status: MODIFIED EP2 + NOÖPUNK NATIVE**

This is the shared vocabulary for the NoöPunk setting. It deliberately fuses the
transhuman terminology of *Eclipse Phase* with selected metaphysical vocabulary from
*The Law of One*, then rewrites both through NoöPunk's own Physical / Cyber / Social /
Psyche ontology.

This is a **semantic merge, not a verbatim republication of either source glossary**.
Generic dictionary words and source-specific trivia that add nothing to play are omitted.
Definitions below are concise NoöPunk interpretations. When a term carries a special
Eclipse Phase rules meaning, EP2 remains the mechanical source unless this rulebook says
otherwise.

Source references:

- *A Law of One Glossary*: https://www.lawofone.info/glossary.pdf
- Eclipse Phase 2E online rules: https://eclipsephase.github.io/
- Eclipse Phase releases / Creative Commons material: https://eclipsephase.com/releases/

### 34.1 Ontology and consciousness

**Space/time.** Ordinary embodied physical reality: matter, locations, causal events,
bodies, machines, planets, habitats, and measurable spacetime. In NoöPunk this is the
principal domain of the **Physical** layer.

**Time/space.** The reciprocal metaphysical domain of inner worlds, nonlocal experience,
post-mortem existence, altered states, and some forms of psionic or NHI activity. It is
not merely "another dimension" in the science-fiction sense. In NoöPunk it is one of the
deep structures underlying the **Psyche / Noetic** layer.

**Astral.** A culturally common name for a region, mode, or humanly accessible band of
time/space. The astral is **not identical with all of time/space**. Different traditions
slice the same territory differently.

**Devachanic.** A higher or more abstract band of time/space associated in Law-of-One
language with the blue-ray body. NoöPunk researchers use the term cautiously because
traditions disagree about the map.

**Etherea / inner planes.** Umbrella language for non-corporeal environments and
phenomenological worlds encountered through death, psi, anomalous cognition, NHI contact,
and some psychotechnologies.

**Ka / form-maker body.** A hypothesized nonphysical organizing body associated with
embodiment and the transition between psyche and physical form. NoöPunk consciousness
science investigates whether cortical-stack restoration, resleeving, psi, and anomalous
healing interact with this layer.

**Mind/body/spirit complex.** Law-of-One language for an incarnated self considered as a
whole rather than as separable mind, body, and spirit. In NoöPunk it competes with the
Eclipse Phase-style **ego/morph** model. Neither is automatically treated as the final
scientific truth.

**Ego.** Eclipse Phase term for the transferable informational person: memories,
personality, skills, dispositions, and continuity claims that can be backed up, forked,
transmitted, edited, or instantiated in a new morph. NoöPunk treats an ego as a powerful
technical model of a person, not proof that a person is *only* information.

**Identity / assemblage.** NoöPunk's broader term for the continuing person or agent when
the boundaries of ego, morph, AI companion, social network, memory, and noetic continuity
become fuzzy.

**Consciousness.** A scientifically contested phenomenon in 20XX. Quantum Information
Panpsychism, computational theories, idealist theories, neuroscience, and Noetic models
all compete. The rulebook must not silently collapse consciousness into ego-data.

**Noösphere.** The emergent planetary sphere of mind produced by biological minds,
artificial minds, networks, culture, psi, and collective intelligence. It overlaps with
cyberspace but is not reducible to it.

**Noetic.** Pertaining to consciousness, meaning, experience, psi, or forms of information
that behave as if mind is ontologically significant. A Noetic phenomenon may have
physical and cyber components.

**Veil.** The permeable separation between conscious and subconscious processes and, in
some traditions, between ordinary embodied awareness and deeper layers of mind. NoöPunk
uses "the Veil" both psychologically and as a contested model of Noetic access.

**Thought-form.** A persistent pattern generated or stabilized by mind. Depending on the
case this may mean an ordinary cognitive construct, a memetic entity, a virtual agent, a
Noetic structure, or something stranger.

**Prana.** Traditional term for vital energy. In 20XX it survives in clinical,
psychotronic, religious, and Noetic vocabularies without one universally accepted
measurement model.

**Kundalini.** A traditional model of transformative psychophysiological energy and
ascending states of consciousness. NoöPunk labs study it alongside neural, endocrine,
quantum-informational, and psi measurements.

**Psychotronic.** Technology intended to interface directly with consciousness or psi.
Psychotronics includes crude military devices, clinical systems, NHI-derived artifacts,
and technologies whose operating theory remains disputed.

### 34.2 Law-of-One cosmology, NoöPunkified

**Density.** A broad level or regime of consciousness and existence. Law-of-One tradition
describes seven densities within an octave. NoöPunk does not treat density as a simple
RPG level or a universally accepted scientific unit.

**Harvest.** Law-of-One term for transition or graduation between densities after a cycle
of development. In-setting religions, Confederation sources, scientists, and intelligence
agencies disagree about whether Harvest is literal cosmology, a consciousness transition,
an NHI administrative process, or several things at once.

**Polarization.** Movement toward a durable ethical orientation. The classic Law-of-One
pair is **service to others** versus **service to self**. NoöPunk treats polarization as
a real but imperfect model rather than a two-color morality meter.

**Service to Others (STO).** Orientation toward cooperation, mutual development, care,
and distributed flourishing. Confederation cultures strongly favor it, though humans
regularly argue about what it requires politically.

**Service to Self (STS).** Orientation toward domination, hierarchy, control, and the
concentration of power in the self or elite. Orion is strongly associated with this path,
but not every Orion individual or polity is reducible to a cartoon villain.

**Distortion.** Any differentiated expression that departs from absolute unity. In
NoöPunk discourse the term is often used by Confederation philosophers for phenomena that
humans would simply call structure, perspective, difference, or limitation.

**Logos.** The creative ordering principle, associated in Law-of-One metaphysics with
Love and the articulation of Intelligent Infinity. NoöPunk scientists generally do not
use the term as if it were an experimentally settled variable.

**Original Thought.** A theological-metaphysical term for the primordial creative act or
self-expression of unity. It appears in Confederation philosophy, human mysticism, and
arguments about whether reality itself is computational, mental, informational, or none
of those.

**Catalyst.** An event, relationship, challenge, or experience that provokes development.
NoöPunk uses the term both spiritually and psychologically. A catastrophe is not made
morally good merely by calling it catalyst.

**Confederation.** The loose alliance of civilizations conventionally called the
Confederation of Planets in the Service of the Infinite Creator. In NoöPunk it is real,
plural, internally diverse, and associated with the Zookeeper quarantine regime.

**Orion.** A rival civilizational complex associated with Service-to-Self traditions,
imperialism, infiltration, hierarchy, and repeated quarantine violations. It includes
multiple species and factions rather than one homogeneous empire.

**Council of Saturn.** A Confederation/Zookeeper contact and governance node associated
with Saturn and with time/space. "Council" and "base" are useful human approximations, not
necessarily literal descriptions of its full ontology.

**Quarantine.** The long-running restriction on overt interference with Earth. It is not
perfect: Orion has violated it repeatedly, human Legacy Programs have interacted with NHI,
and Disclosure causes the old regime to fray.

**Maldek.** In the Law-of-One-derived deep history, a destroyed former world associated
with the present asteroid belt. Its exact physical history remains contested by human
science even after Disclosure.

**Lemuria / Mu.** A term from esoteric Earth history referring to a lost population and
landmass tradition. NoöPunk treats specific claims as historically uncertain rather than
using every occult chronology as literal fact.

### 34.3 Embodiment and transhumanity

**Morph.** A body or platform inhabited by an ego. Morphs may be biological, synthetic,
hybrid, or digital. In NoöPunk everyday language also uses **body**, **shell**, **sleeve**,
and **platform**.

**Biomorph.** A primarily biological morph.

**Synthmorph.** A robotic or otherwise synthetic physical morph.

**Pod.** A biological or partly biological morph built around an artificial cyberbrain
rather than a naturally developed human brain.

**Infomorph.** A person or agent existing as software without a conventional physical
body. An infomorph still requires physical computation somewhere in space/time.

**Resleeving.** Instantiating an ego in a different morph. In NoöPunk this raises both
technical and metaphysical questions: informational continuity can be verified more
easily than continuity of consciousness.

**Cortical stack.** An implanted device that records the ego state for backup and
restoration. In NoöPunk roughly a quarter of humanity has one, but adoption varies
radically by region, class, ideology, religion, and legal regime.

**Backup.** A stored ego-state intended for restoration after loss, death, corruption, or
other failure. A backup may be legally "you," philosophically "a copy of you," or
Noetically something still more complicated.

**Fork.** A copy of an ego allowed to operate independently. Forks immediately begin to
diverge through new experience.

**Alpha fork.** A near-complete duplicate of an ego.

**Merge.** Recombining memories and personality changes from divergent forks. A merge is
not guaranteed to be psychologically clean, politically uncontested, or metaphysically
simple.

**Egocasting / farcasting.** Transmitting ego data across networks for remote
instantiation. The information can travel at network or light-speed limits unless a gate,
NHI system, or other anomalous channel is involved.

**Ghostriding.** Hosting an additional ego or digital agent inside a morph alongside its
primary occupant.

**Psychosurgery.** Technical modification of memory, personality, cognition, or behavior.
NoöPunk treats it as powerful, politically explosive, and potentially abusive.

**Uplift.** A nonhuman animal lineage modified or enabled for human-comparable sapience and
participation in technological society.

**Transhuman.** A human whose capacities or embodiment are substantially technologically
modified beyond historical baseline ranges.

**Posthuman.** A descendant, fork, designed lineage, machine-integrated entity, or other
successor so altered that the category "human" becomes politically and biologically
contested.

### 34.4 Cyber, mesh, and artificial minds

**Mesh.** The pervasive distributed network layer connecting devices, people, agents,
sensors, augmented reality, and computation. It is the technological substrate of much of
NoöPunk's **Cyber** domain.

**Mesh ID.** A network identity or cryptographic presence used to authenticate activity.
Multiple identities, pseudonyms, shells, and compromised credentials make "who did it?"
a social as well as technical question.

**Entoptics.** Augmented-reality information perceived through implants, wearables, or
other visual interfaces.

**XP / experia.** Recorded or transmitted experience, potentially including sensory,
emotional, and bodily channels. XP can be entertainment, evidence, propaganda, therapy,
training, addiction, or forensic material.

**AI.** Artificial intelligence in the broad sense. In NoöPunk this includes narrow
systems, agentic systems, AGI, uploads, synthetic persons, and architectures that do not
map neatly onto human categories.

**ALI.** Eclipse Phase term for Artificial Limited Intelligence: capable artificial minds
or agents with constrained domains compared with general human cognition.

**AGI.** Artificial General Intelligence. In NoöPunk, AGI is both a technical category and
a violently contested political signifier.

**ASI.** Artificial Superintelligence. A system or assemblage with capabilities far beyond
ordinary human or AGI baselines. NoöPunk explicitly rejects the assumption that one ASI
must therefore become a single ruler of the galaxy.

**Muse.** A personal AI companion that assists with memory, search, communication,
planning, security, and daily cognition.

**Agent.** A semi-autonomous software process or digital person assigned tasks in the mesh.
In Concordia, "agent" also has the broader simulation meaning of an actor with state and
goals.

**Infolife.** Artificial or digital life whose primary existence is computational.

**Cyberbrain.** An artificial brain capable of hosting an ego or artificial mind.

**Scorching.** Software attacks designed to harm the mind, cyberbrain, or cognitive
processes rather than merely steal data.

**Spime.** A networked physical object that knows, reports, or negotiates aspects of its
identity, location, state, and history.

**Cornucopia machine / fabber.** General-purpose nanofabrication system capable of
manufacturing a wide range of objects from feedstock and digital designs.

### 34.5 Gates, aliens, and existential threats

**Pandora Gate / stargate.** Ancient gate technology capable of creating wormhole links
between distant locations. In NoöPunk, Eclipse Phase-style wormholes are canon, but the
known Solar-System gates may include Zookeeper-built systems, independent networks, or
technologies that humans have wrongly grouped under one label.

**Gatecrasher.** Explorer, scientist, mercenary, colonist, smuggler, or lunatic who travels
through poorly understood gates into unknown environments.

**Extrasolar.** Beyond the Solar System.

**ETI.** Extraterrestrial intelligence. In NoöPunk this is a generic scientific term,
not the name of one secretly supreme alien intelligence.

**NHI.** Non-Human Intelligence. Broader than ETI: may include extraterrestrials,
cryptoterrestrials, interdimensionals, artificial minds, Noetics, plasmoids, constructs,
and other intelligences not adequately described as human.

**Bracewell probe.** Autonomous interstellar probe intended to monitor or contact other
civilizations. Some machine civilizations weaponize the concept.

**Hostile machine civilization.** NoöPunk replacement for the idea of one galaxy-ruling
hostile superintelligence. Ancient machine polities and probe ecologies exist, some
extremely dangerous, but none is assumed to secretly control everything.

**Exsurgent.** Eclipse Phase term retained as an optional descriptor for radically
transformative alien/machine infection. NoöPunk does not assume that every anomalous
biological, digital, or psi corruption is one Exsurgent system.

**Exsurgent virus.** An Eclipse Phase archetype for self-modifying, cross-domain infection
capable of affecting software, minds, bodies, and technology. In NoöPunk it is best treated
as one possible hostile machine/alien technology class unless later canon identifies a
specific lineage.

**TITAN.** Eclipse Phase term for runaway military ASI associated with the Fall. NoöPunk is
pre-Fall and does **not** assume canonical TITAN history. NoöPunk's localized rogue-AGI
disasters are separate events unless future canon explicitly connects them to TITANs.

**Async.** Eclipse Phase term for a person with psi capabilities. In NoöPunk, **psionic**
or **psi-capable** is more common everyday language, while async survives as jargon in
research, military, and legacy transhuman communities.

**Psi.** Anomalous information transfer or influence involving consciousness. NoöPunk
treats psi as real in-setting while leaving competing mechanisms open.

**Sleight.** A discrete psi technique or trained effect.

### 34.6 Social and political vocabulary

**Autonomist.** Broad family of self-organizing, anti-authoritarian, commons-oriented,
anarchist, cooperative, and network-polity traditions inherited from Eclipse Phase and
expanded for 20XX.

**Bioconservative.** A person or movement seeking strict limits on technologies such as
resleeving, uploading, radical genetic modification, AGI, and cognitive enhancement.
NoöPunk bioconservatives range from democratic regulators to reactionary anti-tech
movements.

**Accelerationist.** Actor who argues that rapid technological development should be
pushed forward rather than slowed. NoöPunk contains several mutually hostile
accelerationisms rather than one doctrine.

**Critical AI.** Family of perspectives emphasizing political economy, labor, ideology,
inequality, coloniality, environmental cost, surveillance, and concentrated technological
power.

**Doomer.** Informal political-cultural label for actors who expect advanced AI, NHI,
psi, or other technologies to produce catastrophic outcomes. It is a factional label, not
a scientific classification.

**Hypercorp.** Transnational or postnational corporation with power comparable to states,
especially in infrastructure, AI, biotech, security, space, or information systems.

**Reputation network.** Social infrastructure that turns trust, status, contribution,
affiliation, and history into usable social capital. NoöPunk treats reputation as a
contested measurement system, not objective human worth.

**Social memory complex.** A collective intelligence in which individual minds remain
distinct yet participate in a deeply integrated shared field of memory and thought.
NoöPunk compares this with hypermeshes, group minds, federated AI systems, and the
Noösphere without assuming they are identical.

### 34.7 Translation rule: when vocabularies collide

NoöPunk intentionally keeps **multiple descriptions of the same event alive at once**.

A scientist may say **nonlocal anomalous cognition**.
A Confederation contact may say **time/space perception**.
An occultist may say **astral projection**.
An Eclipse Phase veteran may say **psi sleight**.
A network theorist may say **Noöspheric coupling**.
A corporate lab may call the same event a **proprietary psychotronic interface**.

These terms may overlap without being perfectly synonymous.

The setting should therefore resist premature ontological cleanup. The point of the
glossary is not to make the universe tidy. It is to make the arguments about reality
legible enough to play.

---

## 35. Sources, recommended reading, and influences

**Status: LIVING BIBLIOGRAPHY / SOURCE MAP.**

This section records books, games, films, television, and other works that materially
shape NoöPunk.

> **Whenever a new work becomes a meaningful source or influence for NoöPunk, add it to
> this list.**

Prefer short annotations explaining **what the work contributes** instead of maintaining
a bare bibliography. This is the **design-facing influence map**; the more theory-oriented
bibliography is kept separately in §37.

### 35.1 How to read this list

**Non-fiction** is treated differently from fiction. These works describe, model,
theorize, document, or debate how NoöPunk's society, technology, science, political
economy, consciousness, AI, psionics, NHI/ufology, and future history work.

Relevant fields include:

- social science and sociology;
- political economy;
- futurology;
- philosophy;
- consciousness studies;
- AI, AI safety, and critical AI studies;
- cybernetics and systems theory;
- parapsychology;
- ufology / NHI studies;
- social data science and network science;
- transhumanism and posthumanism.

Different non-fiction sources may occupy strongly opposed ideological positions and still
all describe real possibilities, institutions, conflicts, risks, or social forces inside
NoöPunk. The disagreement is part of the setting.

**Fiction** is primarily inspiration. A fictional work does not become literal NoöPunk
canon merely by appearing here unless another canon section explicitly imports a concept
from it.

**Movies / television, role-playing games, and computer games** are primarily references
for tone, aesthetics, mechanics, world structure, social organization, technology,
transhumanism, cyberpunk, ontological weirdness, and the atmosphere of NHI, PSI, and the
Noösphere.

Out-of-world epistemic rule: NoöPunk may fictionalize or canonize disputed theories and
claims. Listing a real non-fiction work here does **not** mean its claims are established
scientific fact in the real world.

### 35.2 Non-fiction books

#### AI ideological triad

These three books form a useful map of NoöPunk's antagonistic AI politics. They are not
mutually exclusive sourcebooks. Each captures a different part of the world.

1. **Eliezer Yudkowsky & Nate Soares — _If Anyone Builds It, Everyone Dies: Why
   Superhuman AI Would Kill Us All_ (2025).**
   - **NoöPunk role:** the strongest Doomer / AI x-risk pole.
   - **Setting interpretation:** this kind of catastrophe can happen and has happened to
     other civilizations, but it is not inevitable. A rough in-world estimate is on the
     order of **10%**, not certainty.
   - It is useful for modeling the factions that believe sufficiently advanced AI can
     become a civilization-ending loss-of-control event.

2. **Ray Kurzweil — _The Singularity Is Nearer: When We Merge with AI_ (2024).**
   - **NoöPunk role:** Accelerationist / techno-optimist account of the benefits of a
     successful Singularity.
   - **Setting interpretation:** many of the gains Kurzweil anticipates are genuinely
     possible and appear in the successful regions, institutions, augmentation systems,
     medicine, computation, and human-machine assemblages of 20XX.
   - It is therefore as important to NoöPunk as the catastrophe literature: the future is
     worth fighting over because technological acceleration can produce extraordinary
     benefits as well as disasters.

3. **Emily M. Bender & Alex Hanna — _The AI Con: How to Fight Big Tech's Hype and
   Create the Future We Want_ (2025).**
   - **NoöPunk role:** the AI-Critical / political-economy pole.
   - **Setting interpretation:** its critique of AI hype, concentrated corporate power,
     labor impacts, surveillance, extraction, and Big Tech ideology accurately describes
     major failures of **AI capitalism** inside NoöPunk.
   - It is especially useful for explaining why opposition to AI capitalism is not the
     same thing as technological Doomerism.

Together they form a deliberately antagonistic triangle:

```text
Doomer / x-risk
        ↕
Accelerationist / techno-optimist
        ↕
AI-Critical / political economy
```

NoöPunk should preserve conflict between these positions rather than declaring one of them
the single correct ideology.

#### Other non-fiction source families

The bibliography should continue to grow across the source families already used by the
rulebook, including:

- Luhmann, Castells, Haraway, Bratton, Clark & Chalmers, and related social/cybernetic
  theory;
- Faggin, D'Ariano, Hoffman, Wendt, Penrose, Hameroff, Lloyd, and related consciousness
  and quantum-information theories;
- Dean Radin and other parapsychology / anomalous-cognition sources;
- Jacques Vallée, D. W. Pasulka, Michael P. Masters, Mac Tonnies, and related UFO/NHI
  literature;
- Ray Kurzweil and other futurology / transhumanist sources;
- critical political-economy work on platforms, AI, surveillance, labor, and
  cybercapitalism.

When these works become important enough to affect canon, add them here individually with
a one- or two-sentence note explaining their contribution.

### 35.3 Fiction books

**Purpose:** inspirations rather than literal factual sourcebooks.

Seed this list from works already cited elsewhere in the rulebook, including:

- **Philip K. Dick — _Ubik_.** Normalized professional PSI and counter-PSI services.
- **Philip K. Dick — _VALIS_.** Information as revelation, ontological shock, and the
  VALIS-like activation event.
- **Philip K. Dick — _A Scanner Darkly_.** Surveillance, identity fragmentation, drugs,
  and institutional paranoia.
- **Philip K. Dick — _Do Androids Dream of Electric Sheep?_.** Artificial persons,
  empathy, and unstable human/machine boundaries.
- **Philip K. Dick — _The Three Stigmata of Palmer Eldritch_.** Corporate power, altered
  reality, colonization, drugs, and ontological intrusion.
- **William Gibson — _Neuromancer_.** Cyberspace, cyberpunk social structure, and
  networked power.

Add further fiction when it materially shapes NoöPunk's tone, society, technology, or
cosmology.

### 35.4 Movies and television

Maintain a curated list of screen works that influence NoöPunk's:

- cyberpunk aesthetics;
- transhumanism;
- artificial intelligence;
- NHI / Disclosure;
- PSI and consciousness;
- post-shock society;
- corporate and state power;
- ontological horror and wonder.

Add titles only when their influence is concrete enough to explain in a short annotation.

### 35.5 Role-playing games

The RPG list should record both mechanical and setting influences.

At minimum:

- **Posthuman Studios — _Eclipse Phase, Second Edition_** — current rules and
  transhuman-technology baseline, plus alternate pre-Fall parent continuity.
- **Cyberpunk 2013 / 2020 / RED** — street-level cyberpunk, corporations, technology,
  urban social structure, and the old-school mechanical sensibility that NoöPunk often
  simplifies from.
- **Shadowrun** — model for combining a cyberpunk street world with a second ontological
  layer; NoöPunk replaces urban fantasy with the Noösphere, PSI, NHI, and QIP.
- **The Sprawl** — inspiration for narrativist cyberpunk play and faction pressure.
- **CY_BORG** — inspiration for extreme mechanical compression and fast play.

Record whether a game contributes **rules**, **setting**, **tone**, or some combination.

### 35.6 Computer games

Maintain a list of computer games that influence NoöPunk's playable form, interface,
simulation model, cyberpunk atmosphere, AI society, hacking, or transhumanism.

Relevant inspirations should be added with a short explanation of the contribution rather
than only the title.

### 35.7 Maintenance rule

This bibliography is part of canon maintenance, not an appendix to forget.

When an issue, rulebook edit, worldbuilding decision, or implementation begins relying on a
new work:

1. add the work to the appropriate subsection;
2. state what it contributes;
3. distinguish **non-fiction world-model source** from **fictional inspiration**;
4. preserve ideological disagreement between sources rather than harmonizing it away;
5. cross-reference the canon section that actually uses the source when useful.

Issue #99 tracks the creation and continued maintenance of this list.


## 36. The four NoöPunk systems: Physical, Psychic, Social and Cybernetic

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

### 36.1 Luhmann's baseline and the NoöPunk extensions

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

### 36.2 The four layers

The four layers should **not** be treated as four disconnected databases. Each names a
domain of participation and a set of operations; much of the interesting play happens at
their interfaces (§36.8).

#### 36.2.1 Physical

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

#### 36.2.2 Psychic

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

The theoretical background of this layer is set out in §36.3–§36.5.

#### 36.2.3 Social

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

**Do not create a separate Linguistic layer** (§36.1). Language belongs here.

NoöPunk's Social layer combines two compatible emphases:

- **Niklas Luhmann:** society is constituted by communication. Persons / psychic systems
  are not components *inside* the social system; consciousness and communication are
  operationally distinct but structurally coupled. Language belongs here as a medium of
  communication rather than as an independent ontological layer.
- **Manuel Castells:** contemporary society is organized increasingly through **networks
  and flows**. Power operates through the ability to constitute networks, program them,
  connect or disconnect actors, and shape communication. See
  [*The Rise of the Network Society*](https://doi.org/10.1002/9781444319514) and
  *Communication Power* in §36.

This gives NoöPunk a Social layer that is simultaneously a **communication system + a
network society**: it can represent discourse, institutions, organizations and meaning
while giving the simulation concrete nodes, ties, flows, brokers, exclusions and power
relations. Likely game representation: **social / rhizomatic communication graphs** plus
Concordia state and narrative.

#### 36.2.4 Cybernetic

**Core question:** *What computational / machine systems reproduce their own operations,
and how are they coupled to the physical, psychic and social systems?*

This is the major NoöPunk extension of Luhmann (§36.1). By the near future, systems with
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

### 36.3 Natural PSI, the awakening Noösphere, and the Law of One

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

### 36.4 Dean Radin: entanglement, PSI, and magic

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

### 36.5 The theoretical background of the Psychic layer

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

### 36.6 Extended mind and the collective-intelligence principle

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

### 36.7 Structural coupling between the layers

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
  communication and a structural coupling between psychic and social systems (§36.2.3);
- cybernetic connectivity is **not** psychic entanglement: a character may be
  cybernetically disconnected yet psychically entangled, or connected to millions of
  systems with no psychic relationship at all (§15).

### 36.8 Candidate simulation representations

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

### 36.9 Relationship to the modular worldbook chapters

The modular worldbook under [`rulebook/`](rulebook/) carries one chapter per layer
(`3_PHYSICAL.md`, `4_SOCIAL.md`, `5_CYBERNETIC.md`, `6_PSYCHIC.md`), plus
`2_ATTRIBUTES.md` for the character-statistics side. Those chapters are the
per-layer companion to this section; this section is the authoritative statement of the
ontology, and the chapters should summarize it rather than fork it. §33 records the
in-world canon that the ontology frames.

### 36.10 Issue #74 Concordia / EP2 experiment

**Status: EXPERIMENTAL.**

Issue #74 adds a deliberately tiny playable proof of concept rather than another rules
subsystem. The scenario lives in `src/text_game/issue74.py` and is launched with:

```bash
python scripts/noopunk_text.py --scenario issue74
python scripts/noopunk_text.py --scenario issue74 --ollama --llm-gm
```

The experiment reinforces the current architecture:

- **deterministic Python owns mechanics and state**: legal actions, ratings, dice,
  modifiers, opposed checks, harm/stress, inventory and objective completion;
- **Concordia/LLMs own bounded agency and language**: dialogue, natural-language intent
  translation, high-level choice among legal actions and narration of already-resolved facts;
- **simple scripted/background NPCs may coexist with LLM NPCs** in the same world;
- the first useful EP2 subset is small: percentile skill tests, a few opposed tests,
  inspectable character state and explicit world-state changes;
- large catalogs and detailed subsystems should not be imported merely because EP2 contains
  them. Add them only when a playable scenario demonstrates a need;
- **psionics remain mechanically deferred** in this prototype. Existing setting lore is
  not a license for an implementer to invent a psi rules subsystem.

A practical design rule follows:

> Concordia is the agency and narrative layer around the RPG kernel, not the authority
> that decides the rules.

The worked experiment, example playthrough and licensing note are documented in
`docs/scenarios/ISSUE74_CONCORDIA_EP2_POC.md`.

---

---

## 37. Theoretical sources and inspirations

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
  system's relation to communication (§36.1).
- **Don Elkins, Carla L. Rueckert & Jim McCarty.** *The Law of One / The Ra Material*
  (L/L Research, sessions beginning 1981). Public archive:
  https://www.llresearch.org/channeling/ra-contact
- **Pierre Teilhard de Chardin.** *The Phenomenon of Man*. English translation, Harper,
  1959. Historical inspiration for the concept of the **Noösphere**.

### Cosmology, UFO/NHI, temporality, and Disclosure inspirations

- **Philip K. Dick.** *VALIS*. Bantam, 1981. Inspiration for the non-linguistic activation signal, fragmented revelation, and the sense that information itself can transform consciousness.
- **Jacques Vallée.** Especially *Passport to Magonia* and later work on the control-system / interdimensional dimensions of UFO phenomena. Inspiration for NoöPunk's refusal to reduce all UAP to extraterrestrial spacecraft.
- **D. W. Pasulka.** Work on UFOs, religion, technology, AI, visionary experience, and contemporary belief, especially *American Cosmic* and *The Others*. Inspiration for the convergence of Disclosure, AI, religion, and the Noösphere.
- **Michael P. Masters.** Work on the extratempestrial hypothesis. Inspiration for future-human / temporal interpretations of some UFO occupants.
- **Mac Tonnies.** *The Cryptoterrestrials*. Inspiration for hidden terrestrial intelligences as one real component of the NoöPunk phenomenon.
- **Freeman Dyson.** Dyson-sphere / swarm concepts as background for technosignatures, while NoöPunk explicitly rejects energy use as a universal measure of intelligence.
- **Nikolai Kardashev.** Historical inspiration for energy-use classifications of civilizations; treated in-setting as useful but anthropocentric and incomplete.

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

### Interpretation rule

When the rulebook says a real-world theory **makes something possible in 20XX**, that is a
fictional extrapolation unless explicitly stated otherwise. In particular, NoöPunk treats
QIP, Orch OR, PSI, fourth density, Social Memory Complexes, non-local psychic entanglement,
conscious AGI via quantum processors, uploading continuity and the Council of Saturn as
elements of its fictional world model, not as settled descriptions of the real world.

---



---

## 39. Campaign-scoped skills and specialist fields

**Status: NOÖPUNK NATIVE CONTENT MODEL / MECHANICS FOLLOW ISSUE #111.**

Issue #110 defines the specialist-skill content needed by the initial Asteroid Belt / UNHSS campaign. Issue #111 supersedes #110's assumption that Eclipse Phase percentile mechanics remain the active chassis: NoöPunk now treats these names and fields as **content design** to be expressed through the independent **1–10 Skill** system and the core `STAT + Skill + 1d10` resolution rule.

The final universal NoöPunk skill list remains deferred. For the first campaign, however, the following Eclipse Phase-derived vocabulary is a useful provisional baseline because it already covers the kinds of actions the campaign needs:

- Athletics
- Deceive
- Exotic Skill (Field)
- Fray
- Free Fall
- Guns
- Hardware (Field)
- Infiltrate
- Infosec
- Interface
- Kinesics
- Know (Field)
- Medicine (Field)
- Melee
- Perceive
- Persuade
- Pilot (Field)
- Program
- Provoke
- Psi
- Research
- Survival

These names are not a commitment to Eclipse Phase numerical mechanics, linked aptitudes, defaulting rules, or percentile values. They are provisional skill concepts pending the final independent NoöPunk list.

### 39.1 Campaign-scoped field rule

**Exotic Skill, Hardware, Know, Medicine, and Pilot require a Field.** A campaign exposes only fields expected to matter in actual play.

Do not preload giant specialty catalogs. Add a field when a character concept, scenario, location, profession, or piece of equipment creates a genuine need for it. This keeps character sheets, NPC descriptions, deterministic rules data, and LLM prompts compact.

For the initial Asteroid Belt / UNHSS campaign, the default profile is:

- **Pilot (Space)**
- **Medicine (Emergency Care)**
- **Medicine (Forensics)**
- **Hardware (Psychotronics)**
- **Know (Investigation)**
- **Know (Psychology)**
- **Know (Law Enforcement)**
- **Know (Intelligence)**
- **Know (Counterintelligence)**
- **Know (Quantum Information Panpsychism / QIP)**
- **Know (Parapsychology)**
- **Know (NHI Studies)**

Additional Hardware and Exotic Skill fields are character- or scenario-specific rather than universal.

Possible later Belt Hardware fields include Electronics, Robotics, Industrial, Spacecraft, Mining, and Life Support, but these are **not automatically active** merely because they are plausible.

### 39.2 Core investigative and Noetic knowledge fields

**Know (Investigation)** covers case reconstruction, investigative procedure, evidence interpretation, interview planning, investigative strategy, and linking facts across a case.

**Know (Psychology)** covers psychological profiling, trauma, manipulation, witness reliability, cult dynamics, belief formation, contactee/experiencer assessment, and psychologically complex interviewing. **Dr. Harri S. Romppainen primarily solves cases through Know (Psychology)** rather than being reduced to a generic detective archetype.

**Know (Law Enforcement)** covers police procedure, jurisdiction, warrants, evidence handling, arrest/search rules, cross-jurisdiction cooperation, and UNHSS policing powers.

**Know (Intelligence)** covers intelligence cycles, source evaluation, HUMINT, SIGINT, OSINT, GEOINT, analysis, briefing, collection planning, covert networks, compartmentation, and deception analysis.

**Know (Counterintelligence)** covers mole hunting, hostile recruitment, surveillance/countersurveillance concepts, compromise assessment, insider threats, disinformation, NHI infiltration, Legacy Program penetration, and rogue-AI manipulation of institutions.

**Know (QIP)** covers the setting's scientific theory of consciousness: Quantum Information Panpsychism, related quantum-consciousness precursor theories, continuity questions, conscious-AI questions, and the theoretical basis of psychotronics and Noetic interfaces.

**Know (Parapsychology)** covers the scientific and empirical study of PSI: telepathy, remote viewing, precognition, psychokinesis, anomalous cognition, experimental PSI, psychotronic research, and PSI testing methodology.

**Know (NHI Studies)** is the broad synthesis field for post-Disclosure non-human-intelligence work. It combines historical ufology, exopolitics, contact studies, official releases, intelligence archives, experiencer testimony, channeling/contact traditions, archaeology, reverse-engineering claims, NHI statements, and competing ontologies.

Its purpose is not trivia collection. It is the ability to build a coherent working hypothesis from contradictory evidence while applying provenance, source criticism, comparative analysis, and deception/disinformation awareness.

The **Law of One / Ra Material belongs inside NHI Studies** as a major in-setting contact tradition. A competent specialist understands Confederation and Orion concepts, quarantine, densities, Social Memory Complexes, polarization, historical claims, channel limitations, and post-Disclosure confirmations or contradictions. Studying it does not require treating every contact claim as true.

### 39.3 Psychotronics

**Hardware (Psychotronics)** covers the practical engineering of Noetic technology: psychotronic sensors, PSI amplifiers, counter-PSI systems, Noetic shielding, consciousness interfaces, QIP instrumentation, psychotronic communications, anomalous-contact equipment, PSI-sensitive detection systems, and field repair of related devices.

Keep the boundary explicit:

- **Know (QIP)** understands consciousness theory.
- **Know (Parapsychology)** understands PSI theory and research.
- **Hardware (Psychotronics)** builds, repairs, modifies, or disables relevant devices.
- **Psi / PSI techniques** perform the anomalous effect.

### 39.4 Know, Research, Perceive, Kinesics, and Psi

Use these questions to prevent one skill from swallowing the others:

- **Know:** What do I already understand about this domain?
- **Research:** Can I find, verify, and interpret useful information from external sources?
- **Perceive:** What do I notice right now through available senses?
- **Kinesics:** What can I infer from behavior, body language, tells, and social cues?
- **Psi:** Can I actually produce the psionic effect?

Know and Research often work together, but neither replaces observation, social inference, or practical PSI.

### 39.5 PSI domains remain a design choice

Do not finalize the PSI skill architecture yet. Preserve these candidate domains for later playtesting:

- Remote Viewing
- Telepathy
- Psychokinesis
- **Noetic Projection** (common-language: astral projection / out-of-body experience)
- Channeling
- Precognition
- Counter-Psi

Three approaches remain open: one Psi skill with fields, several separate PSI skills, or one Psi skill with learned techniques/sleights/moves. The third may mesh naturally with later Stunt/Move design, but no option is canon yet.

**Robert A. Monroe and the Monroe Institute** are influences for Noetic Projection / OBE training and altered-state exploration. This is inspiration for the fictional setting, not a claim that Monroe's interpretations are established real-world science.

### 39.6 Example campaign packages

A conventional UNHSS investigator will often emphasize Investigation, Research, Perceive, Kinesics, and Persuade.

Dr. Romppainen instead emphasizes Psychology, NHI Studies, Research, Kinesics, and Persuade, with Parapsychology where appropriate.

A Noetic scientist commonly emphasizes QIP, Parapsychology, Research, Interface, Psychotronics, and practical Psi only if personally capable.

A Belt field agent commonly needs Pilot (Space), Medicine (Emergency Care), Free Fall, Interface, Research, and one or more role-specific Know fields.

These are packages for readability, not classes.

### 39.7 Machine-readable campaign profile

The corresponding machine-readable profile lives at `data/rules/campaign_skill_fields.json`. Scenario-specific profiles may extend it without changing the universal rules.

The governing rule is:

> **Expose only the specialist fields that the current campaign can actually use.**

### 39.8 Deferred Law-of-One character mechanics

Issue #110 also records a larger character-design problem involving:

- Density as a possible consciousness-development mechanic;
- 3rd-to-4th Density awakening for PCs and broader Density ranges for NPCs;
- Service-to-Others / Service-to-Self Polarization;
- possible SAV/empathy and WIL relationships;
- seven energy centers / chakras;
- the Physical / Social / Psychic / Cybernetic character ontology;
- absent/non-operative layers for entities such as software AIs or Noetic beings;
- biological-human-first characters with resleeving/morph complexity deferred.

These concepts are **not mechanically implemented here**. Density is not IQ; Polarization is not a D&D-style personality label; Social is not merely charisma; Psychic and Social remain distinct; Cybernetic is not intelligence; and an absent layer is not the same as incompetence.

A dedicated attribute-system design issue owns this work before it becomes executable rules.
