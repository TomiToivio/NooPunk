# NoöPunk Design Principles

> **Status:** canonical design intent. These are project-level invariants, not loose
> inspirations. Preserve them unless the author explicitly instructs otherwise.

This is the **single canonical explanation** of NoöPunk's three core balances. Other
documents (`AGENTS.md`, `README.md`, `RULEBOOK.md`, the runtime architecture notes)
carry short references pointing here rather than restating the reasoning — if you need
to change what a balance *means*, change it here and nowhere else.

A balance is a deliberate tension held on purpose. If one pole starts winning, that is
a design decision that must be made explicitly, not something that happens by drift.

---

## 1. Gamism / Narrativism / Simulationism

NoöPunk aims for a deliberate balance across the three classic creative agendas. None of
them is the default that overwhelms the others.

Each pole has a canonical reference point. They are **design anchors for the three
poles, not systems to clone**:

| Pole | Canonical reference | What it contributes |
|---|---|---|
| **Gamism** | **CY_BORG** | challenge-oriented play; dangerous situations; meaningful player choices; resource pressure; emergent problem solving; fast playable rules rather than maximal mechanical complexity |
| **Simulationism** | **Cyberpunk 2020** | coherent world rules; material consequences; cybernetics and technology that actually matter mechanically; injuries, equipment, economy and social conditions; a believable causal relationship between world, character and mechanics |
| **Narrativism** | **The Sprawl** | fiction-forward consequences; story-generating mechanics; relationships, factions and corporations; failures and partial successes that change the situation; mechanics that push the narrative forward instead of returning bare pass/fail |

Short formulation:

> **CY_BORG for challenge. Cyberpunk 2020 for reality. The Sprawl for story.**

### What gamism does not mean

Gamism is **not** a mandate to make NoöPunk combat-focused or optimization-heavy.
Hacking, psionics, infiltration, investigation, social engineering and exploration are
all legitimate gamist challenge spaces.

### What simulationism does not mean

Simulation should make the setting feel internally consistent **without** turning every
subsystem into bookkeeping. Verisimilitude is the goal; accounting is not.

### What narrativism does not mean

Narrativism does not license inventing lore to make a better story. Setting canon still
follows author specification (see `AGENTS.md` §1).

---

## 2. Tabletop / Godot / Concordia balance

NoöPunk maintains a strong balance between its tabletop and computer implementations.
The implementation families are **Tabletop**, **Godot**, and **Concordia**.

The target principle:

> **Same world, same rules, same mechanics wherever possible.**

All three should use the same underlying:

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

The computer versions should be **implementations of the tabletop rules, not
reinterpretations of them**. Avoid separate tabletop and digital game systems unless it
is technically unavoidable.

### Shared vs. allowed to diverge

This distinction is deliberate and is not a loophole in the parity rule:

**Shared — must stay in parity**

- rules
- mechanics
- character model
- world model
- setting canon
- core systems
- balance

**May diverge — and probably should**

- scenarios
- missions
- maps
- encounters
- presentation
- UI
- pacing
- procedural generation
- implementation details required by the medium

A tabletop scenario, a Godot scenario and a Concordia simulation may differ from each
other freely. What they may **not** do is disagree about what a FIT check is.

Where duplicate rule implementations already exist, prefer extracting or defining a
shared specification so divergence becomes **easier to detect**. `data/rules/core.json`
plus `src/rules/` is the current instance of that pattern: one authored numeric canon,
consumed by every runtime.

---

## 3. Cyberpunk / Noösphere

NoöPunk is deliberately a balance between **Cyberpunk** and a
**Noösphere / urban-fantasy-like speculative layer**. Neither half should swallow the
other.

### Cyberpunk

The cyberpunk side grows from plausible near-future technological development, especially:

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

The premise is that present-day technological trajectories already point strongly toward
a cyberpunk future.

### Noösphere

The Noösphere is the setting's equivalent of the supernatural / urban-fantasy layer, but
it is based specifically on **three speculative paradigm shifts**:

1. **UFO / UAP Disclosure**
2. **Psionics**
3. **Panpsychism**

These progressively destabilize conventional assumptions about:

- mind
- matter
- consciousness
- intelligence
- reality
- humanity
- communication

**The Noösphere must not become generic fantasy magic.** Its strange phenomena retain
NoöPunk's science-fictional, philosophical and speculative character. It is a research,
technology and politics problem that happens to be stranger than expected — not
spellcasting.

---

## 4. Genre influences: comparative, not templates

These are documented carefully **without turning NoöPunk into a derivative clone**.

### Shadowrun

NoöPunk resembles Shadowrun **structurally**: it mixes cyberpunk with an urban-fantasy /
anomalous layer.

The difference is the source of that anomalous layer. Instead of traditional fantasy
races and magic, NoöPunk uses:

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

Eclipse Phase is an **important comparative influence**, especially where cyberpunk and
anomalous/posthuman themes meet. NoöPunk is not an Eclipse Phase homebrew, expansion, or
rules variant, and must not be presented as one.

### The relationship, stated once

Shadowrun and Eclipse Phase are the two nearest neighbours, and NoöPunk is deliberately
neither: it keeps cyberpunk as cyberpunk and replaces the urban-fantasy layer with the
Noösphere, NHI, psionics and consciousness-fundamental metaphysics.

---

## 5. How these balances change

A balance changes only when the author specifies a change. If an implementation appears
to require a departure from any balance here:

1. **do not silently redesign it**;
2. document the reason explicitly, in the issue or the document that forced the choice;
3. prefer a neutral placeholder or TODO over a quiet reinterpretation of the balance.

Examples, prototypes, test fixtures and genre convention are **not** authority to change
a balance. This mirrors the canon rule in `RULEBOOK.md` §18 and the author-intent rule in
`AGENTS.md` §1.
