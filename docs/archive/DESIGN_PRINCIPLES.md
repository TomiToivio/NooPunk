# NoöPunk Design Principles — the three balances

> **Status:** author-specified design invariants.
>
> This file is the **single canonical explanation** of NoöPunk's three design
> balances. Other documents should *reference* it in one or two lines rather than
> restate it, so there is one place to change and no competing source of truth.
>
> These are project-level invariants, not loose inspirations. Preserve them unless
> the author explicitly instructs otherwise. If an implementation genuinely needs a
> departure, document the reason explicitly instead of redesigning the balance
> silently.

The three balances are independent. A change to one does not authorize changing
another.

---

## 1. Gamism / Narrativism / Simulationism balance (issue #200)

**Author direction, 2026-10-10:** the three corners have **equal design weight**:
Simulationism ~33⅓%, Narrativism ~33⅓%, and Gamism ~33⅓%. These are
qualitative playtest goals, not fractional page counts or a second dice mechanic.
An apparent asymmetry in a particular scene (for example, tactical combat or
diplomacy) need not be forced into thirds. Overall play must support all three.

```text
                         SIMULATIONISM
                         Eclipse Phase
                             /\
                            /  \
                           /    \
                          / CORE \
                         / Fudge  \
                        /Psi-Punk  \
                       /Fate +     \
                      /Transhumanity\
                     /  's Fate     \
                    /_______________\
             NARRATIVISM             GAMISM
      Apocalypse World / The Veil    Cities Without Number /
                                    Stars Without Number
```

**One shared rules engine sits in the center of the triangle.** Its conceptual
foundations are a Fudge / Psi-Punk / Fate / Transhumanity's Fate synthesis.
The **separation between character Attributes and Skills is mandatory**.
The established six character Attributes (FIT, REF, INT, SOC, CYB, PSY) and
canonical Skill vocabulary remain in place. Equipment statistics such as
Interface, Network and Compute are device/session properties, not extra
character Attributes. The final dice model and scale conversion are a
separate, explicit migration and playtest decision under issue #200:
**do not silently replace the current d10 implementation.**

Each corner contributes a different kind of design:
- **Simulationism — Eclipse Phase:** causal coherence, equipment and
  resource differences, cybernetics, PSI, medicine, networks, transhuman
  consequences and persistent world state.
- **Narrativism — Apocalypse World / The Veil:** fictional positioning,
  meaningful choices, relationships, ideological and social conflicts,
  GM consequences, and developments that advance the story.
- **Gamism — Cities Without Number / Stars Without Number:** legible
  stakes, risk/reward, tactical choices, fast procedures, lightweight
  encounter and faction tools.

These are **inspirations and design principles, not source-code or rules-text
imports**. Fudge and Psi-Punk's designated open material is primarily
**OGL**, not automatically Creative Commons. Fate's official SRD has a
**CC BY** route. The cited Eclipse Phase and Transhumanity's Fate editions
are **CC BY-NC-SA** and cannot simply be reused in a commercially
reusable NoöPunk core. The Veil has a CC BY-SA text grant; permissions
for Apocalypse World and Without Number titles require edition/SRD
verification before any expression is copied. See
[`docs/licenses/ISSUE_200_CC_RELEASE_GATE.md`](../licenses/ISSUE_200_CC_RELEASE_GATE.md).

**Open-source acknowledgements:** NoöPunk should explicitly credit these
systems for their inspirations without claiming endorsement or using a
publisher's restricted marks. Distinguish original gameplay ideas from
verbatim licensed expressions and preserve their attribution and license
requirements. The desired NoöPunk release is fully Creative Commons,
with a compatible license chosen for the published rules/setting; code
licensing is evaluated separately.

**One game across media:** write tabletop rules first, then a deterministic
specification for Godot and Concordia/Ollama. LLMs can improvise dialogue,
NPC intent and narrative consequences but cannot secretly alter dice,
permission rules, equipment properties, action points or canonical state.

---
 
## 2. Tabletop / Godot / Concordia balance

NoöPunk is **one computer RPG/simulation** (#48 — see
[`NOOPUNK_AS_ONE_GAME.md`](NOOPUNK_AS_ONE_GAME.md)), not separate tabletop,
simulation and videogame products.

The tabletop / Godot / Concordia distinction below is therefore about **notation and
runtime sequence**, not about maintaining three products: the same rules are written
to read like tabletop rules, exercised by deterministic Python and Concordia agents,
and potentially presented by a future graphical frontend. Development is
deliberately sequential rather than parallel.

> **Tabletop first. Same world, same rules, same mechanics wherever possible.**

The **tabletop-style rules and worldbook are the canonical design source**. A system is written and stabilized in human-readable, playable form before substantive Concordia implementation begins.

The tabletop and computer versions should share the same underlying:

- attributes
- skills
- dice / probability model
- combat rules
- hacking rules
- psionics rules
- cybernetics rules
- character progression
- equipment logic
- world assumptions
- terminology
- core balance values

The computer versions are **implementations of the tabletop rules, not
reinterpretations of them**. Do not create separate tabletop and digital game
systems unless that is technically unavoidable.

The required conversion path is:

**tabletop rule → digital specification → Godot implementation → Concordia implementation**

If implementation reveals an ambiguity, resolve it in the tabletop source first. Existing digital scaffolds are preserved, but unfinished tabletop design must not be completed implicitly inside software.

### Shared

- rules
- mechanics
- character model
- world model
- setting canon
- core systems
- balance

### May diverge

- scenarios
- missions
- maps
- encounters
- presentation
- UI
- pacing
- procedural generation
- implementation details required by the medium

Scenario content and presentation are expected to differ between tabletop, Godot,
and Concordia. That divergence is intended, not a defect.

### Detecting divergence

Where duplicate rule implementations already exist, prefer extracting or defining
a shared specification so that divergence becomes easier to detect. The canonical
constants live in `data/rules/core.json`, generated from `src/rules/core.py`; the
Godot runtime reads that data instead of re-declaring a table, and a test fails the
build on drift.

---

## 3. Genre balance: Cyberpunk / Noösphere

NoöPunk is deliberately a balance between two halves. Neither may swallow the other.

### Cyberpunk

The cyberpunk side grows from plausible near-future technological development:

- AI
- AGI / advanced machine intelligence
- corporate power
- surveillance
- hacking
- cybernetics
- BCI
- transhumanism
- automation
- networked society
- technological inequality

The premise is that present-day technological trajectories already point strongly
toward a cyberpunk future.

### Noösphere

The Noösphere side is the setting's equivalent of a supernatural / urban-fantasy
layer, but it rests specifically on **three speculative paradigm shifts**:

1. **UFO / UAP Disclosure**
2. **Psionics**
3. **Panpsychism**

These progressively destabilize conventional assumptions about mind, matter,
consciousness, intelligence, reality, humanity, and communication.

The Noösphere must **not** become generic fantasy magic. Its strange phenomena
retain NoöPunk's science-fictional, philosophical, and speculative character.

---

## 4. Comparative influences

These are important comparisons. They are **not templates to copy**.

### Shadowrun

NoöPunk resembles Shadowrun *structurally*: both mix cyberpunk with an
urban-fantasy / anomalous layer.

The source of NoöPunk's anomalous layer is fundamentally different. Instead of
traditional fantasy races and magic, NoöPunk uses:

- UFO / UAP Disclosure
- psionics
- panpsychism
- the Noösphere

### Eclipse Phase

NoöPunk overlaps with Eclipse Phase through:

- transhumanism
- cyberpunk
- artificial intelligence
- altered / distributed identity
- psionics
- extraterrestrial or non-human intelligence themes

Use Eclipse Phase as an important comparative influence, especially where
cyberpunk and anomalous / posthuman themes meet.

Do not copy protected setting material, terminology, characters, factions,
mechanics, or text from either work, and do not silently import their assumptions.

---

## 5. Invariants for agents and contributors

1. Preserve the **Gamism / Narrativism / Simulationism balance**, with issue #51's current priority: **Narrativist experience + Simulationist world + Gamist friction**.
2. Use **Eclipse Phase** (Simulationism), **Apocalypse World / The Veil** (Narrativism), and **Cities Without Number / Stars Without Number** (Gamism) as the canonical reference poles, per the issue #200 triangle in §1; Fudge, Psi-Punk, Fate and Transhumanity's Fate supply the hybrid centre.
3. Preserve **rules/mechanics parity** between Tabletop, Godot, and Concordia wherever possible, with **Tabletop as the canonical first implementation**.
4. Allow scenarios and medium-specific presentation to diverge.
5. Preserve the **Cyberpunk / Noösphere balance**.
6. Treat **UFO Disclosure, Psionics, and Panpsychism** as the defining Noösphere paradigm shifts.
7. Treat **Shadowrun** and **Eclipse Phase** as comparative influences, not templates to copy.
8. Do not silently redesign these balances. If an implementation requires a departure, document the reason explicitly.
9. Treat NoöPunk as an **original rules system**. Existing games may be comparative references, but no game supplies default mechanics or a chassis.

`AGENTS.md` carries the same list as binding agent rules. `tests/test_design_principles.py`
enforces that this document, the agent rules, and the referring documents stay
consistent, so the invariants cannot be dropped by accident.

## 6. Where the theory lives

These balances say what NoöPunk is trying to be. They are not the theoretical
grounding of individual rules — that is recorded separately, per rule, in
[`THEORETICAL_SOURCES.md`](THEORETICAL_SOURCES.md).

`RULEBOOK.md` §18.2 states the requirement: **every canonical rule should have an
explicit theoretical source, model, or research tradition behind it.** The
registry carries one entry per grounded rule, and each entry separates what the
source actually argues from NoöPunk's interpretation, from NoöPunk's own
speculative or game-design extension, and from the concrete mechanical
consequence.

The first entry is the four-group character architecture in `RULEBOOK.md` §5
(Physical / Social / Psychic / Cybernetic), grounded in Luhmannian systems theory.
The paradigm shifts named in §3 above — in particular **Panpsychism** — are
setting metaphysics and belong to that speculative layer; naming one as a design
paradigm here does not make it an established result of physics or neuroscience.
