# Reference: Characters, Identity, AI, NPCs and Beings

> Generated, verbatim segment of [RULEBOOK.md](../../RULEBOOK.md) (the extended-canon run). The rulebook file is canonical; this part and its section numbers are unchanged so that cross-references keep resolving. Regenerate with `python3 tools/split_rulebook.py --apply`.

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

## 19. AI, AGI, infomorphs, and non-human agents

**Status: ADAPTED / INSPIRED / NOÖPUNK NATIVE DIRECTION.**

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

#### Full agents

Important characters may use Concordia + LLM cognition, memory, goals, conversation, and the full relevant character state.

#### Lightweight agents

Background characters may use deterministic logic, state machines, Mesa-style agents, or extremely limited behavior.

Lightweight agents should not become socially omniscient merely because the game can call an LLM.

Promote an NPC to a full agent only when the simulation or story benefits from it.

---

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
