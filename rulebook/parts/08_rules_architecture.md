# Reference: Rules Architecture and Governance

> Generated, verbatim segment of [RULEBOOK.md](../../RULEBOOK.md) (the extended-canon run). The rulebook file is canonical; this part and its section numbers are unchanged so that cross-references keep resolving. Regenerate with `python3 tools/split_rulebook.py --apply`.

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

> **NoöPunk: an independent 1–10 STAT + Skill + d10 RPG/social-simulation system set in 20XX, built for human play and deterministic Concordia/LLM-assisted simulation.**

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

Eclipse Phase is an important **influence and source library**, not NoöPunk's parent rules engine.

NoöPunk may selectively draw on Eclipse Phase for transhuman technology, morphs and embodiment, mesh/cyberspace ideas, reputation, posthuman identity, space habitats, existential risk and related concepts. Any directly adapted material must keep clear attribution, provenance and licensing.

Mechanically, however, NoöPunk does not inherit EP2 by default. Every subsystem must be judged on whether it serves NoöPunk's own play style and world. Existing EP2-derived Python modules are legacy/prototype material until deliberately ported, adapted or retired.

Canonical divergences include:

- **the Fall has not happened**;
- **Earth remains inhabited and politically central**;
- there have been multiple localized **Rogue AGI Disasters**, but no global extinction-level Fall;
- Eclipse Phase-level technologies exist, but distribution is highly uneven;
- most humans still inhabit their original biological bodies;
- roughly **25% of humanity has cortical stacks**;
- roughly half of those with cortical stacks have already resleeved at least once;
- roughly **50% of humanity has some cybernetic augmentation**, ranging from medically necessary replacements to mesh inserts and cognitive enhancements.

The setting may still use a pre-Fall, Earth-intact transhuman technology level as inspiration without making NoöPunk an Eclipse Phase conversion.

### 2.6 Core design identity

NoöPunk is simultaneously:

- a cyberpunk RPG;
- a Noösphere / consciousness RPG;
- a transhuman RPG;
- an NHI/UAP-contact setting;
- a political and ideological simulation;
- a social-science simulation;
- a Concordia multi-agent world;
- an **independent RPG system assembled from many influences rather than one parent game**.

Its central question is:

> **Who gets to define what humanity, intelligence, consciousness, progress, danger, and reality mean when several paradigm shifts happen at once?**

## 3. Rules provenance labels

Every substantial rules section should make its provenance clear without treating another RPG as the default chassis.

#### NOÖPUNK CORE

A canonical native rule of the independent NoöPunk system.

#### ADAPTED / INSPIRED

A NoöPunk rule that deliberately borrows a design idea from one or more external games but is implemented as NoöPunk's own rule.

#### LEGACY EP2

Existing Eclipse Phase-derived prototype material that is retained for provenance or transitional compatibility but is **not automatically active core canon**.

#### EXPERIMENTAL

A rule being tested and subject to removal.

#### DEFERRED

The subsystem is intentionally unresolved.

Licensing/source provenance remains mandatory for directly adapted material.

For compatibility with the older EP2 conversion matrix, the historical status vocabulary
`EP2 BASELINE`, `MODIFIED EP2`, `NOÖPUNK NATIVE`, `EXPERIMENTAL`, and `DEFERRED`
remains recognized as **legacy provenance metadata**. Those labels do not make EP2 the
current chassis.

## 4. Source hierarchy

When sources disagree, use this order:

1. **Explicit current author direction**
2. **RULEBOOK.md**
3. **Issue #111 and later issues that explicitly revise it**
4. **Implemented tests and shared machine-readable rules data**
5. **Earlier NoöPunk issues and design documents that do not conflict with the above**
6. **External RPGs as inspiration or source material, never as automatic default canon**
7. **Archived NoöPunk design documents**

Software is not allowed to silently override this document. If implementation and rulebook differ, record the discrepancy as porting debt and resolve it deliberately.

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

**Status: LEGACY EP2, to be simplified aggressively.**

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
