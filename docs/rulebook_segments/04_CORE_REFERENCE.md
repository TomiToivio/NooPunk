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

## 9. Characters and identity

**Status: LEGACY EP2 → expected heavy NoöPunk conversion.**

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
| Firewall | **superseded in-world term; default campaign role is UNSA** — see below |
| TITANs | **deliberately undecided** — see below |

These are **working mappings**, not final terminology.

Two EP2 concepts are carried as **explicitly undecided** rather than mapped, because
the alternate timeline's divergence point falls inside them. Recording them as open is
the decision; a later contributor must not "helpfully" resolve them by inventing an
organisation, a history, or a mechanic.

**Firewall.** NoöPunk no longer uses **Firewall** as the in-world name of the
default player organization. The campaign function that once borrowed that Eclipse Phase
term is now fulfilled by the **United Nations Security Administration (UNSA)**, an overt UN agency
with classified operational networks. "Firewall" remains only a design/provenance reference
where comparison with Eclipse Phase is useful. The "Great Firewall" in §33.27 remains
China's internet-control system and is unrelated.

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

### 9.2 Six base STATs across the four-layer ontology

**Status: NOÖPUNK CORE — issue #131 supersedes issue #113.**

The character sheet is deliberately small. Six universal base STATs cover what every
character needs a rolled number for, organized by four ontological layers:

| Layer | STAT | Code |
| --- | --- | --- |
| Physical | Fitness | FIT |
| Physical | Reflexes | REF |
| Social | Intelligence | INT |
| Social | Social | SOC |
| Cybernetic | Cybernetics | CYB |
| Psychic | Psyche | PSY |

Operative ordinary-human STATS use the **1–10** scale established in #111. A layer that
does not meaningfully operate for an entity is **N/A** on human-readable sheets and
`null` in machine-readable data. **0 does not mean absence.**

Complexity belongs in the domain layers, not in more base attributes. **Intelligence** and
**Social** belong to the Social layer: language, symbolic reasoning, institutions,
discourse, and shared knowledge, with finer distinctions — reading another mind versus
projecting one's own — living in the Social Systems layer (§6). **Psyche** belongs to the
Psychic layer — consciousness, willpower, psychic resilience, PSI and Noetic capability —
with the PSI domains, awakening and energy centers living in the Psychic Systems layer
(§8). The two layers are deliberately distinct, and there is no generic Mental/Ego layer.

**Cybernetics (CYB)** measures direct functional coupling to machines, BCI, computation
and networks, not intelligence and not learned technique. A biological human without
meaningful direct cybernetic coupling may have the Cybernetic layer as N/A while still
using ordinary external computers through **INT** plus learned skills.

Processing, bandwidth, storage, hardening and similar hardware properties are statistics
of the decks, implants, devices and agents a character uses, **not character STATS**.
Cybernetic augmentation may later unlock the Cybernetic layer, provide narrow modifiers,
or produce an **effective** STAT above 10; keep the biological/base rating and the
augmentation separate so the 1–10 human scale stays legible.

The full definitions and entity examples are maintained in
[`rulebook/2_ATTRIBUTES.md`](rulebook/2_ATTRIBUTES.md).

### 9.3 Density, Polarization, and energy centers

**Density** is a consciousness-development **tier/state**, not a STAT and not IQ. NPCs may
be represented from 1D–7D where useful. PCs normally occupy 3D or 4D. A 3D PC may develop
toward 4D through a **six-segment Awakening Clock** advanced only by major Noetic,
developmental, catalyst, energy-center, or polarization events. Filling the clock makes a
character eligible for a story-significant 4D transition; it does not automatically grant
blanket numeric superiority.

**Polarization** is tracked separately from attributes on a Law-of-One-inspired
`-100 ... 0 ... +100` continuum:

- `+51` or higher = clearly Service-to-Others polarized;
- `-95` or lower = clearly Service-to-Self polarized;
- values between = mixed, developing, conflicted, or unpolarized.

Polarization changes through sustained meaningful action rather than chosen alignment.
High **SOC** can help perceive and enact StO possibilities but does not itself make a
character StO. High **PSY** can support disciplined self-directed control but does not
itself make a character StS.

The seven energy centers are **developmental states across the four-layer character
ontology**, not seven extra STATS. Use the states **Blocked / Active / Balanced /
Integrated**. Their strongest correspondences are:

- Red → Physical embodiment and survival;
- Orange → Psychic + Social selfhood and one-to-one relation;
- Yellow → Social groups, institutions, and role identity;
- Green → Social + Psychic compassion and reciprocity;
- Blue → Social communication and truthful expression;
- Indigo → Psychic intuition, disciplined consciousness, PSI, and Noetic work;
- Violet → whole-character integration / signature.

The **Cybernetic** layer is outside the chakra model, though technology may influence any
center. Do not invent an eighth cybernetic chakra or force one-to-one STAT mappings.

The detailed canonical design is in
[`rulebook/2_ATTRIBUTES.md`](rulebook/2_ATTRIBUTES.md).

### 9.4 Biological-human-first scope

The initial playable kernel prioritizes biological humans, optional cybernetics, the
four-layer attributes, PSI, Density, Polarization, Contacts/Factions/Motivations, and
UNSA agents.

Cortical-stack continuity, full resleeving, morph catalogs, forks/backups, and infomorph
edge cases remain deferred. Later transhuman mechanics must map onto this ontology rather
than replace it.


---

## 10. Action resolution

**Status: NOÖPUNK CORE — issue #111.**

NoöPunk's basic resolution engine is:

```text
STAT + Skill + 1d10 ≥ Difficulty Value
```

Both **STAT** and trained **Skill** ratings use a **1–10** scale. Their final names and lists are intentionally deferred. Stats and skills remain separate mechanical quantities.

### 10.1 Difficulty Values

| Difficulty | DV |
| --- | ---: |
| Simple | 9 |
| Everyday | 13 |
| Difficult | 15 |
| Professional | 17 |
| Heroic | 21 |
| Incredible | 24 |
| Legendary | 29 |

These are canonical starting values for playtesting. Do not silently change them.

### 10.2 Opposed checks

Both sides roll:

```text
STAT + Skill + 1d10
```

Higher total wins. **Ties are unresolved by the current core rules** and require a later explicit design decision.

### 10.3 Criticals and modifiers

Issue #111 deliberately does **not** define exploding 10s, fumbles on 1s, margin-based criticals, or a final situational-modifier procedure. Do not inherit those rules automatically from Cyberpunk RED, Cyberpunk 2020, Fate, PbtA, Eclipse Phase or any other game.

### 10.4 Probability pass

Representative success rates before future modifiers:

| Profile | DV 9 | DV 13 | DV 15 | DV 17 | DV 21 | DV 24 | DV 29 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Novice: STAT 4 + Skill 1 | 70% | 30% | 10% | 0% | 0% | 0% | 0% |
| Average trained: 5 + 3 | 100% | 60% | 40% | 20% | 0% | 0% | 0% |
| Professional: 6 + 5 | 100% | 90% | 70% | 50% | 10% | 0% | 0% |
| Expert: 7 + 7 | 100% | 100% | 100% | 80% | 40% | 10% | 0% |
| Elite: 8 + 9 | 100% | 100% | 100% | 100% | 70% | 40% | 0% |

The table is diagnostic, not permission to alter the authored DVs. Legendary DV 29 is intentionally beyond these representative ordinary profiles without future bonuses or exceptional rules.

## 11. Pools and expendable resources

**Status: LEGACY EP2 / EXPERIMENTAL FOR CONCORDIA.**

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

**Status: LEGACY EP2.**

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

**Status: LEGACY EP2, intentionally minimal.**

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

**Status: LEGACY EP2 → core NoöPunk subsystem.**

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

**Status: LEGACY EP2 → major NoöPunk reskin/replacement target.**

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

**Status: ADAPTED / INSPIRED / NOÖPUNK NATIVE METAPHYSICS; detailed mechanics still DEFERRED.**

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

