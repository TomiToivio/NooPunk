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

## 1. Gamism / Narrativism / Simulationism balance

NoöPunk aims for a deliberate balance between three creative agendas. None of them
is the default that may overwhelm the others.

The canonical reference points are three tabletop RPGs, one per pole:

- **Gamism: CY_BORG**
- **Simulationism: Cyberpunk 2020**
- **Narrativism: The Sprawl**

> **CY_BORG for challenge. Cyberpunk 2020 for reality. The Sprawl for story.**

### Gamism — CY_BORG

CY_BORG is the main reference for:

- challenge-oriented play
- dangerous situations
- meaningful player choices
- resource pressure
- emergent problem solving
- fast, playable rules rather than maximal mechanical complexity

Gamism does **not** mean NoöPunk becomes combat-focused or optimization-heavy.
Hacking, psionics, infiltration, investigation, social engineering, and exploration
can all function as gamist challenge spaces.

### Simulationism — Cyberpunk 2020

Cyberpunk 2020 is the main reference for:

- coherent world rules
- material consequences
- cybernetics and technology that actually matter mechanically
- injuries, equipment, economy, and social conditions
- a believable causal relationship between world, character, and mechanics

Simulation should make the setting feel internally consistent without turning every
subsystem into unnecessary bookkeeping.

### Narrativism — The Sprawl

The Sprawl is the main reference for:

- fiction-forward consequences
- story-generating mechanics
- relationships, factions, and corporations
- failures and partial successes that change the situation
- mechanics that push the narrative forward rather than merely returning pass/fail

### On the references

NoöPunk is not a clone of these systems. They are **design anchors for the three
poles**. Use them to check that no pole has quietly swallowed the others.

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

1. Preserve the **Gamism / Narrativism / Simulationism balance**.
2. Use **CY_BORG**, **Cyberpunk 2020**, and **The Sprawl** as the canonical reference poles.
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
