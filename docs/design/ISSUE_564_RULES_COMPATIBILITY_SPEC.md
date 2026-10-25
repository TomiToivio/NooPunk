# Issue #564 — rules compatibility specification

**Status: `proposal_pending_author_review`. Nothing in this document is approved, and no mechanic
here may be implemented until Gate A opens.**

`strategy_game/docs/RULE_SYSTEM_RESEARCH.md` §"Gates" still reads: *"Until all relevant gates, no
gameplay mechanics are implemented."* This file is the epic's step 2 — the *specification* — written
that way on purpose. Every number is marked `OPEN`, and no rule is stated as settled.

It is also deliberately **kernel-agnostic**. The epic's blocking question (queue **D40**) is whether
the dice layer stays on Fate `4dF` or becomes the Without Number `2d6`. Most of what follows does
not depend on that answer, so it is specified as *procedures riding on a resolve interface*, and the
kernel is a parameter (§4). That way the answer to D40 chooses one line in §4 instead of rewriting
the file.

**Division of labour with `ISSUE_571_COMBAT_INJURY_TRAUMA.md`:** combat, Shock, Trauma, mortal
injury, stabilisation and healing are **#571's**, which has already read the CWN SRD and measured both
live models. This file does not restate them; where it touches them it defers.

---

## 1. What this specification covers

| Area | Here | Elsewhere |
| --- | --- | --- |
| The resolve interface (one call, any kernel) | **§4** | — |
| **Effort** — the committed-resource model for PSI and BCI | **§3.1** | queue D36 |
| **Foci** ↔ the approved stunt structure | **§3.2** | `strategy_game/RULEBOOK.md` §16 (catalogue unapproved) |
| **Four saves** as named checks | **§3.3** | — |
| **Edges** as the classless advancement answer | **§3.4** | queue D23 (advancement unapproved) |
| Access prerequisites for hacking | **§3.5** | `ISSUE_222_CYBERSPACE_SCOPE.md` |
| Morale and reaction | **§3.6** | — |
| Shock, Trauma, injury, healing | cross-reference only | **`ISSUE_571_COMBAT_INJURY_TRAUMA.md`** |
| Attributes, skills, character creation | not reopened | queue D22/D23/D30, #482 |
| Chassis / kernel choice | parameterised | queue **D40**, D29, D31 |

**Deliberately out of scope:** classes, levels, XP thresholds, world/sector generation, starships,
and psionics-as-discipline-tree. §5 lists why each is excluded rather than merely omitted.

---

## 2. The design rule this specification obeys

The Without Number family is **one engine with per-book extensions** (CWN, SWN, AWN, WWN). Its
portable parts are *procedures*: how a committed resource behaves, how a save is called, how a
specialism is packaged, how lethality is adjudicated. Its **non**-portable parts are its *dice
convention*, its *attribute set*, and its *setting furniture*.

**Licensing is a hard precondition, not a footnote.** `data/sources/game_system_rights.json` records
CWN as `verified-public-domain` (CC0) and **SWN as `blocked-unverified`** — no SWN SRD was located, so
**nothing from SWN may be adapted until the ledger changes**. WWN and AWN are **not yet in the
ledger**. Consequently every procedure below is sourced from **CWN**, and the WWN/AWN material is
*candidate* material pending entries. Where CWN and SWN share a procedure (saves, morale), CWN is the
source of record — nothing is lost by the block.

So the rule is: **import procedures, never the convention.** A procedure may be adopted only if it
can be stated without naming a die. If it cannot, it is a kernel question and belongs in §4/D40.

---

## 3. Procedures proposed for adoption

Each block gives: what it is in the source, why NoöPunk wants it, the NoöPunk shape proposed, what
stays open, and what it would touch.

### 3.1 Effort — the committed-resource model (WWN; also SWN psionics)

**In the source.** A small pool of points. Using a lasting ability *commits* Effort for as long as
the effect lasts; other abilities *commit for the scene*; a character can overspend at a cost
(`OPEN`: the source prices this as taking damage or being unable to act). Effort is not spent and
forgotten — it is **tied up**, which is the distinctive part.

**Why NoöPunk wants it.** The epic asks for "cybernetic cognition/BCI" and "PSI/psychotronics" as
explicit systems, and the setting's whole position is that *the mind pays for the mind's work*. The
sheet today has physical and mental stress, and queue **D36** offers three weak options: no cyber
track at all (cyber conflict has no attrition), a separate `Interface` track (a third track every
character carries for a subsystem only some use), or a track per device (bookkeeping nobody
maintains).

**Effort is a fourth option and the best one**, because it is:
- **one pool, not one per subsystem** — PSI and BCI draw on the same scarce resource, which is
  itself a setting claim ("a mind can hold only so much");
- **committed, not depleted** — a running psychic effect or an active BCI link *occupies* capacity
  rather than subtracting a number, so the cost is legible at the table without arithmetic;
- **already-shaped like the approved consequence ladder** — both express "this is still with you".

**Proposed NoöPunk shape (proposal, not rule).**

| Element | Proposal | Status |
| --- | --- | --- |
| The pool | A single **Effort** pool, size `OPEN` | a number the author sets; it must not be derived from a STAT without approval |
| Committed vs free | An *ongoing* PSI effect or an *active* BCI link holds Effort until ended; an *instant* effect releases it | core of the proposal |
| Overspend | Allowed, with a **consequence**, not a hit-point subtraction | `OPEN`: which consequence, and whether it is chosen or assigned |
| What it does *not* do | It never grants a bonus to a check by itself | holds the existing rule that equipment and cybernetics are **named permissions, not statistics** (`strategy_game/RULEBOOK.md` §16) |
| Interplay with stress | Effort is **not** a third stress track; a *failed* PSI or intrusion still lands on mental stress | keeps the sheet at two tracks, which is D36's stated concern |

**This replaces D36's three options with a fourth and should be answered in D36, not here.** Note
that D36 also asks about a *cyberware capacity limit*; Effort answers the **PSI/BCI** half and only
partially the implant half, since an implant is a permanent permission rather than a committed
effect. Two separate questions, one row.

### 3.2 Foci ↔ the approved stunt structure (WWN)

**In the source.** A Focus is a **two-tier** package: a first-level benefit and a second-level
benefit, sometimes requiring a prerequisite. It is the family's answer to feats, and it is flatter
than a level-based tree.

**Why NoöPunk wants it.** `strategy_game/RULEBOOK.md` §16 states that **stunts are approved** but
**"the full stunt catalogue" is not**. A catalogue has to be written eventually, and Foci supply a
*shape* for it: two tiers, explicit prerequisite, no tree.

**Proposed NoöPunk shape.** A stunt may declare an **upgrade tier**, taken later, with the same
prerequisite discipline. Nothing else changes: a stunt is still a permission priced in refresh, and
no stunt grants a flat bonus by name alone — the standing rule.

**Open.** Whether the catalogue is authored as Foci-shaped tiers at all, or kept as a flat list with
free upgrades. This is a catalogue-shape decision, not a mechanic, and it is the author's.

### 3.3 Four saves as named checks (CWN — CC0-verified)

**In the source.** Four fixed saves — Physical, Evasion, Mental, Luck — rolled when the fiction calls
for a reflex, a resistance, a dodge or a matter of chance.

**Why NoöPunk wants it.** A named save is faster to call at the table than "roll this skill", and it
gives the GM a consistent vocabulary that does not depend on remembering the skill list.

**Proposed NoöPunk shape.** Four **named saves** expressed as *a check against a fixed trait*,
mapped onto existing traits — not as a new dice convention. Under any kernel this is
`resolve(<the trait the save names>, <difficulty>)`; it adds vocabulary, not arithmetic.

**Open.** Which trait each save names under each kernel, and whether `Luck` survives at all — a
luck save is a strong tonal claim in a game about structural power and discourse, and it may be the
one save the setting should refuse rather than adopt.

### 3.4 Edges as the classless advancement answer (CWN; AWN)

**In the source.** One class, differentiated by **Edges** — small packages chosen at creation and
occasionally later. There is no multi-classing because there is nothing to multi-class.

**Why NoöPunk wants it.** The epic forbids classes and levels, `#197` recorded Geeks/Jocks/Freaks as
*slang, explicitly not classes*, and queue **D23** records advancement as unapproved with two
incompatible models on the table (Fate milestone/refresh vs CWN XP/level).

**Edges resolve that tension**: they are the family's own answer to "differentiate without classes",
so adopting them is not inventing a structure — it is importing a classless one.

**Proposed NoöPunk shape.** Differentiation lives in **Edges + aspects + stunts**, and advancement
is *milestone-shaped* (an Edge or a stunt tier at a milestone rather than an XP threshold), which is
closer to the approved Fate side than to XP. `OPEN`: how many Edges at creation, how often they
arrive, and whether they are chosen or tied to the Lifepath (#144).

**This is D23's answer, if the author wants it**, and it should be recorded there.

### 3.5 Access prerequisites for hacking (CWN)

**In the source.** Hacking is gated by *access first*: you need physical or credentialed reach before
a check is possible. The check governs what you do once inside, not whether you can reach it.

**Why NoöPunk wants it.** This is the epic's own requirement — *"crisis-era network constraints
(including disconnected devices and physical ingress)"* — and `ISSUE_222_CYBERSPACE_SCOPE.md`
already scopes cyberspace this way. The import is the **prerequisite structure**, not the dice.

**Proposed NoöPunk shape.** A hack declares its **access** (physical, credentialed, or none), and
the access tier sets what a successful check can achieve. No access, no check — the scene becomes a
physical or social one instead. This is a *procedure*, so it survives any kernel unchanged.

### 3.6 Morale and reaction (CWN — CC0-verified)

**In the source.** Reaction rolls when meeting unknown parties, and morale rolls when a fight turns
bad — both give NPCs a reason to stop.

**Why NoöPunk wants it.** The epic asks to *retain investigative, dialogue-first play*. A game whose
NPCs never disengage is a combat game with talking in front of it; morale is what makes a fight
losable *without* being fatal, which is also what #571's lethality work needs.

**Proposed NoöPunk shape.** One reaction call at first contact and one morale call at a stated
trigger, expressed as ordinary checks against the NPC's own traits. `OPEN`: the triggers, and
whether a named NPC is ever subject to either (a canon character should probably not be, since
canon behaviour is authored).

---

## 4. The resolve interface — how the kernel stays swappable

Every procedure above needs exactly one thing from the dice layer: **an outcome from a trait and a
difficulty.** Nothing in §3 needs to know *which* die was rolled.

```
resolve(trait_value, difficulty, modifiers) -> outcome
outcome ∈ {failure, tie_or_cost, success, success_with_style}
```

- The **four outcomes** are the approved Fate band (`#389`). A WN kernel would have to map its own
  four-ish bands onto these, or replace them — which is a D40 sub-decision, not a §3 change.
- **"Succeed at a cost" sits on the tie**, per queue D32's recommendation. Every procedure above is
  written to tolerate that: Effort overspend is a cost, a failed hack is a cost, a failed morale
  call is a cost.
- **Opposed vs fixed difficulty** is a property of the kernel, not of these procedures.

Consequently, the three candidate parameterisations are:

| | Kernel | What §3 costs | What else must change |
| --- | --- | --- | --- |
| **K1** | Fate `4dF + skill` (approved, implemented) | nothing — procedures ride it unchanged | nothing |
| **K2** | WN `2d6 + attribute modifier + skill` | nothing — procedures ride it unchanged | the Fate kernel's tests retire; `strategy_game/RULEBOOK.md` baseline rewritten; D31 option D invoked |
| **K3** | legacy `STAT + Skill + 1d10` | nothing — but this kernel is the **legacy** game's | would mean unifying both games, i.e. D29 option (b) |

**The point of the table:** the choice in D40 does not change §3 at all. It changes the dice, the
sheets and the tests. That is the strongest argument for specifying procedures first.

---

## 5. What is excluded, and why

| Excluded | Why |
| --- | --- |
| CWN/SWN attribute set (STR/DEX/CON/INT/WIS/CHA) | Deletes `SOC`, `PSY` and `CYB`, the three attributes that carry this setting's meanings. The issue's own wording already drifted to `CHA` — see the matrix §3.1. |
| Classes and levels | Forbidden by the epic; `#197` recorded the slang as explicitly *not* classes. Edges (§3.4) are the classless substitute. |
| XP thresholds | Incompatible with milestone advancement; D23 owns the question. |
| SWN/WWN world and sector generation | Would **manufacture canon**, which `AGENTS.md` §1 forbids an agent to do. The world is authored. |
| Starships and space operations | The epic says not to turn an Earth-based game into a space campaign. |
| Psionics as a discipline tree / virus | NoöPunk's PSI is panpsychic and ontological (canon: *QIP vs virus*). The family's psionics are the wrong model; §3.1 borrows only the **Effort** mechanic, not the psionic framework. |
| Faction turn (SWN/WWN) | Belongs to the strategy layer, whose Gate C is open, and `rpg/boundary.py` refuses the join to `WorldState` on purpose. |

---

## 6. Compatibility and migration strategy

Stated per kernel so the cost of D40 is visible before the decision.

**Nothing here is executed. It is a plan for the author's chosen option.**

### K1 — stay on `4dF` (lowest cost)

- `strategy_game/` keeps its kernel, sheet and tests. §3's procedures attach as **optional
  modules**; a character without Effort or Edges is still a valid character.
- Legacy `RULEBOOK.md` untouched; its `1d10` kernel is a different game's and stays.
- Migration: none. New material is additive.

### K2 — move to `2d6` (highest cost)

- The Fate kernel and everything pinned to it becomes **legacy**: `rpg/fate.py`, the four outcomes,
  Fate points and refresh, and their tests.
- `strategy_game/RULEBOOK.md`'s baseline line is rewritten, and §2–§7's approved sections need
  restatement in the WN convention — including the *sheet*, which is built on six Fate-rated skills.
- Migration: a **versioned sheet schema plus an adapter**, as the epic's step 4 requires. Old and new
  sheets must be distinguishable in the data, never silently reinterpreted.
- The epic's "do not land a destructive rewrite in one PR" applies with full force here.

### K3 — two kernels plus an appendix

- Both kernels stay; §3's procedures are specified once and bound twice in the appendix.
- Migration: none for either game; the cost is a third document and the risk that the procedures
  drift apart in the two bindings.

---

## 7. Open questions this file creates, in one place

| # | Question | Owner |
| --- | --- | --- |
| 1 | Kernel: K1, K2 or K3? | **D40** |
| 2 | Is "3d6" attribute generation, or a third kernel? | **D40** (secondary) |
| 3 | Effort pool size, and what overspend costs | D36 (now with a fourth option) |
| 4 | Does a cyberware *implant* have a capacity limit at all? | D36 (second half, separate) |
| 5 | Is the stunt catalogue Foci-shaped (two tiers) or flat? | new; author |
| 6 | Does `Luck` survive as a save? | new; author |
| 7 | How many Edges, how often, chosen or Lifepath-bound? | **D23** |
| 8 | Are named canon NPCs subject to morale/reaction? | new; author |
| 9 | Which access tiers exist, and what each unlocks? | #222 owner |

---

## 8. What this file does not do

- It does not approve a mechanic, a number, or a kernel. Gates A–D stay open.
- It does not edit either rulebook, `rpg/fate.py`, or any schema.
- It does not restate combat, injury, Shock, Trauma or healing — those are `ISSUE_571`'s.
- It does not claim any of §3 is adopted. Each block is a proposal awaiting review, and the open
  numbers are marked `OPEN` rather than filled with a plausible value.
