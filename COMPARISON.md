# COMPARISON.md — Fate-first comparison gate for the NoöPunk core

**Status: RESEARCH / GATE. Nothing in this document is canonical.** Issue
[#255](https://github.com/TomiToivio/NooPunk/issues/255) requires a comparison before any core
rules conversion is chosen. No rule change, no code change and no migration follows from this
document until the comparison is reviewed and the author records decisions.

**Author direction (2026-10-10): drop Fudge / Psi-Punk as a foundation.** This document therefore
carries no Fudge or Psi-Punk column. See §0 for what that supersedes.

---

## 0. Supersession, recorded rather than assumed

Issue **#200** placed a *Fudge / Psi-Punk / Fate / Transhumanity's Fate* hybrid at the centre of the
design triangle. **#255 supersedes that centre for all future comparison decisions**: the starting
chassis is now **Fate Core / Transhumanity's Fate**, and Fudge and Psi-Punk are **out of scope as
active sources**.

This is a direction change, not an erasure:

- `docs/design/ISSUE_200_*`, the resolution lab, the kernel prototype, the cross-system converter
  and every test they carry **remain in the tree and keep passing**. Nothing is deleted.
- Where this document compares dice history (§6), it says plainly that the Fudge-style 4dF lineage
  came through #200 and is now evaluated as *one option among others*, not as the inherited centre.
- OGL-only expression from Fudge or Psi-Punk must not enter the CC release regardless of this
  document's conclusions — that is a licensing constraint, not a design preference (§7).

---

## 1. Goals, design triangle, trade-offs and scope

### 1.1 The triangle as a design *map*, not a rating

GNS is a **subjective heuristic**. Every game below mixes agendas; the corners say what each family
is *best used for* in NoöPunk, not what it "is".

```
                    SIMULATIONISM
                     Eclipse Phase 2E
                          /\
                         /  \
                        /    \
                       / CORE \
                      /  Fate  \
                     /  Core /  \
                    / Transhumanity's
                   /      Fate      \
                  /__________________\
   NARRATIVISM                        GAMISM
   PbtA / The Veil                    Cities Without Number
                                       Stars Without Number
```

- **Centre — Fate Core / Transhumanity's Fate (preferred starting chassis).** Aspects, stunts,
  stress/consequences, flexible actions. **Too simple as-is**: NoöPunk requires **six independently
  rated Attributes AND separately rated Skills**, which Fate does not supply.
- **Simulationist corner — Eclipse Phase 2E.** Rich transhuman, hacking, PSI, injury, equipment and
  existential-risk procedures; **too complex to import wholesale**.
- **Gamist corner — CWN / SWN.** Concise playable OSR tactics, backgrounds/edges or foci, skills,
  mission/faction tools. **Avoid D&D/class/level assumptions.**
- **Narrativist corner — PbtA / The Veil.** Fiction-first moves, hard choices, relationships,
  consequences. **The Veil is more thematically pertinent than Apocalypse World** (postmodern
  cyberpunk, a digital overlay over the senses) and is the PbtA reference used here.

### 1.2 Non-negotiable requirements carried from the author direction

1. Six independently rated Attributes: **FIT / REF / INT / SOC / PSY / CYB**.
2. **Attributes distinct from Skills** (Fate's unified approach does not satisfy this alone).
3. **Preserve the existing NoöPunk skill list** exactly — `data/rules/skills.json`, 40 skills.
4. No silent rule switch and no arbitrary 1:1 mapping (§3).
5. No Fudge in the recommended active sources.
6. No NC or OGL-only **expression** in the commercial CC target.

### 1.3 Scope boundary

**In scope:** comparison, conversion tables, probability analysis, a source/rights matrix and two
*proposals*.
**Out of scope:** changing `data/rules/*`, editing `RULEBOOK.md` or `rulebook/*`, implementing any
kernel, closing #217 or #232.

---

**No rule becomes canonical without the author's recorded approval.**

## 2. Side-by-side conversion tables

**Family key:** **F** = Fate Core / Transhumanity's Fate · **E** = Eclipse Phase 2E ·
**C** = Cities Without Number / Stars Without Number · **P** = PbtA / The Veil.
**Row labels:** **D** = direct correspondence · **A** = conceptual analogy · **U** = no counterpart.

### 2.1 Attributes and stat analogues

| NoöPunk | F | E | C | P |
| --- | --- | --- | --- | --- |
| FIT (Fitness) | A — *Physique* covers force/endurance, not general fitness | **D** — *Somatics* (2e: Fitness/BOD) | A — *Exert* (skill) + hit points | U — approaches (Forceful/…) are not attributes |
| REF (Reflexes) | A — *Athletics* + *Notice* split | **D** — *Reflexes* | A — initiative, no attribute | U |
| INT (Intelligence) | A — *Lore* + *Investigate*, knowledge-as-skill | **D** — *Cognition* | A — *Know* (skill) | U |
| SOC (Social) | A — *Rapport* / *Contacts* / *Provoke* split three ways | **D** — *Savvy* (2e: CHA/SAV) | A — *Talk* / *Lead* / *Connect* split | A — moves like *Read a Person* |
| PSY (Psyche) | A — *Will*; TF adds psi via stunts/aspects | **D** — *Willpower* + *Psi* | A — *Survive* (skill); SWN psi is a separate subsystem | A — *Resist* / psychic moves |
| CYB (Cybernetics) | U — no cyber attribute; TF handles it as gear/stunts | A — 2e has no single cyber attribute; implants are gear | A — cyber is gear; CWN adds a *Hacking* skill | U — gear tags |
| **Attribute + Skill as a check** | **U** — Fate resolves on a single rated skill + 4dF | **D** — aptitude + skill + d10 | A — skill + 2d6 / + level | U — 2d6 + stat, but stats are the playbook's |

**Lossy points, stated:** the NoöPunk attribute set is *six independent axes including a dedicated
CYB and PSY*. EP2 is the only family with a genuinely comparable attribute array; Fate and PbtA
require **new attributes to be added**, and CWN/SWN require attributes to be introduced at all.

### 2.2 The canonical 40-skill list across all four families

This is the full mapping the issue requires. "No counterpart" is marked **U** rather than
hand-waved; where a family covers the ground with a *different kind* of object (a Fate skill, a PbtA
move, an SWN skill) that is stated.

| # | NoöPunk skill (STAT) | F | E | C | P |
| --- | --- | --- | --- | --- | --- |
| 1 | Administrate (INT) | U | U | **D** — *Administer* | U |
| 2 | Athletics (FIT) | **D** — *Athletics* | **D** — *Athletics* | A — *Exert* | A — *Act Under Pressure* |
| 3 | Connect (SOC) | **D** — *Contacts* | A — *Persuade* / networking | **D** — *Connect* | A — *Streetwise*-type moves |
| 4 | Counterintelligence (INT) | A — *Deceive* inverted | A — *Infiltrate* / Kinesics | A — *Sneak* + *Notice* | A — *Read a Person* |
| 5 | Deceive (SOC) | **D** — *Deceive* | **D** — *Deceive* | A — *Talk* | A — *Manipulate* |
| 6 | ESP (PSY) | A — psi stunt | **D** — psi sleights | A — psychic powers (separate subsystem) | A — psychic move |
| 7 | Exotic Skill (any) | A — any skill with a stunt | A — *Exotic Skill* concept | A — foci/edges grant odd competencies | A — playbook move |
| 8 | First Aid (INT) | A — *Medicine* | **D** — *Medicine* (trauma care) | A — *Heal* | U |
| 9 | Forensics (INT) | A — *Investigate* | A — *Research* / *Perceive* | A — *Know* + *Notice* | A — *Investigate*-type move |
| 10 | Fray (REF) | A — *Athletics* defence | **D** — *Fray* | A — AC/armour + *Exert* | A — *Defy Danger* |
| 11 | Free Fall (REF) | U | **D** — *Free Fall* | U | U |
| 12 | Guns (REF) | **D** — *Shoot* | **D** — *Guns* | **D** — *Shoot* | A — *Open Fire*-type move |
| 13 | Hardware (INT) | A — *Crafts* | **D** — *Hardware* | A — *Fix* | U |
| 14 | Infosec (INT) | U | **D** — *Infosec*-family (see #17 caution) | A — *Program* | A — hacking move |
| 15 | Intelligence Analysis (INT) | A — *Investigate* | **D** — *Research* + *Know* | A — *Know* + *Administer* | A — *Assess* move |
| 16 | Interface (CYB) | U | **D** — *Interface* | A — *Program* | A — hacking move |
| 17 | Investigation (INT) | **D** — *Investigate* | A — *Research* + *Perceive* + *Know* | A — *Notice* + *Know* | **D**-ish — the core *investigate* loop |
| 18 | Kinesics (SOC) | A — *Empathy* | **D** — *Kinesics* | A — *Notice* | A — *Read a Person* |
| 19 | Know (INT) | A — *Lore* | **D** — *Know* | **D** — *Know* | A — *Spout Lore* |
| 20 | Lead (SOC) | A — *Rapport* + command | A — *Persuade* (leadership) | **D** — *Lead* | A — *Command*-type move |
| 21 | Medicine (INT) | A — *Medicine* stunt | **D** — *Medicine* | A — *Heal* | U |
| 22 | Melee (REF) | **D** — *Fight* | **D** — *Melee* | **D** — *Stab* | A — *Hack and Slash* |
| 23 | Noöspace (PSY) | A — TF psi stunt | A — psi + mesh interaction | U | A — psychic/astral move |
| 24 | Perceive (REF) | **D** — *Notice* | **D** — *Perceive* | **D** — *Notice* | A — *Read a Sitch* |
| 25 | Perform (SOC) | A — *Rapport* / *Provoke* | A — *Persuade* performance | **D** — *Perform* | A — *Manipulate* |
| 26 | Pilot (REF) | **D** — *Drive* | **D** — *Pilot* | **D** — *Pilot* | U |
| 27 | Precognition (PSY) | A — psi stunt | **D** — psi sleight | U | A — psychic move |
| 28 | Program (INT) | U | **D** — *Program* | **D** — *Program* | A — hacking move |
| 29 | Provoke (SOC) | **D** — *Provoke* | **D** — *Provoke* | A — *Talk* (intimidation) | A — *Manipulate* / *Go Aggro* |
| 30 | Psychic Defence (PSY) | A — *Will* vs psi | **D** — psi defence | A — mental saves | A — *Resist* move |
| 31 | Psychokinesis (PSY) | A — psi stunt | **D** — psi sleight | A — psychic power | A — psychic move |
| 32 | Research (INT) | A — *Investigate* + *Lore* | **D** — *Research* | A — *Know* | A — *Investigate*-type move |
| 33 | Sneak (REF) | **D** — *Stealth* | **D** — *Infiltrate* | **D** — *Sneak* | A — *Act Under Pressure* |
| 34 | Survival (FIT) | A — *Survival* (FAE) / *Physique* | **D** — *Survival* | **D** — *Survive* | U |
| 35 | Tactics (INT) | A — *Lore* / create advantage | A — *Know* + *Tactics*-flavoured | A — *Lead* + *Know* | A — *Assess* |
| 36 | Talk (SOC) | **D** — *Rapport* | **D** — *Persuade* | **D** — *Talk* | A — *Manipulate* |
| 37 | Telepathy (PSY) | A — psi stunt | **D** — psi sleight | A — psychic power | A — psychic move |
| 38 | Trade (SOC) | A — *Resources* (not a skill) | A — reputation/Commerce | **D** — *Trade* | A — *Barter*-type move |
| 39 | Unarmed (REF) | A — *Fight* (no weapon split) | A — *Melee* covers unarmed | A — *Punch* | A — *Hack and Slash* |
| 40 | Work (INT) | A — *Crafts* | A — *Hardware* / profession | **D** — *Work* | U |

**The honest result:** NoöPunk's list is **nearest to EP2 (about 18 direct, 16 analogy, 2 unsupported)
and to CWN/SWN (about 15 direct, 19 analogy, 6 unsupported)**, and **furthest from Fate and PbtA**
(Fate: 9 direct, 22 analogy, 7 unsupported; PbtA: ~1 direct, 25 analogy, 13 unsupported — because
PbtA has *moves*, not a skill list).

**No two of these lists are identical.** In particular EP2 has *Infiltrate* where NoöPunk has
*Sneak*, and *Persuade* where NoöPunk splits *Talk / Lead / Perform*; CWN/SWN have *Administer*,
*Connect*, *Work*, *Trade*, *Lead*, *Perform*, *Punch*, *Stab*, *Fix* and *Exert* — several of which
are closer to NoöPunk than EP2's equivalents. A conversion must map **per skill**, which is what the
table does, not per system.

### 2.3 Dice distributions

| | Fate Core | EP2 | CWN/SWN | PbtA / The Veil |
| --- | --- | --- | --- | --- |
| Dice | **4dF** (Fate dice) | **1d10** | **2d6** + skill + attribute (or class) | **2d6** |
| Range | −4 … +4 | 1 … 10 | 2 … 12 | 2 … 12 |
| Mean | **0** | **5.5** | 7 | 7 |
| SD | **1.633** | **2.872** | 2.415 | 2.415 |
| Shape | steep, centred, extreme results ~1.2% | **flat** — every result equally likely | triangular, bell-peaked | triangular |

The load-bearing fact: **4dF's spread is 57% of 1d10's.** Under 4dF, competence dominates luck;
under a flat d10, luck dominates. Any move to Fate dice is therefore a *balance* decision, not a
cosmetic one (§6.2).

### 2.4 Difficulty levels and target numbers

| NoöPunk (current canon) | F | E | C | P |
| --- | --- | --- | --- | --- |
| 9 Simple | +0 *Fair* | ~10 trivial | 6 trivial | 6- |
| 13 Everyday | +2 *Good* | ~15 easy | 7-9 = success w/ cost | **7-9 partial success** |
| 15 Difficult | +4 *Great* | ~20 average | 10+ full success | 10+ full success |
| 17 Professional | +6 *Superb* | ~25 hard | — | — |
| 21 Heroic | +8 *Fantastic* | ~30 very hard | — | — |
| 24 Incredible | — (beyond ladder) | ~35 | — | — |
| 29 Legendary | — | ~40+ | — | — |

**Fate's ladder stops at +8 and PbtA has three outcomes, not seven DVs.** NoöPunk's seven-step
ladder is a **d10-shaped** ladder: it maps cleanly onto *none* of the four. This is the single
biggest conversion asymmetry and the reason §6 proposes recalibrated ladders rather than reused
ones.

### 2.5 Degree of success

| | Fate Core | EP2 | CWN/SWN | PbtA / The Veil |
| --- | --- | --- | --- | --- |
| Model | **shifts** (margin in 3s) | margin-based; MoS tiers | binary hit/miss (+crit on nat 20) | **three bands**: 6−, 7-9, 10+ |
| Partial success | via *succeed at a cost* | rare | rare | **first-class** (7-9) |
| NoöPunk today | margin deferred (`criticals: deferred`) | — | — | — |

**PbtA is the only family where partial success is the default texture**, which is why it is the
Narrativist corner: adopting its 7-9 band is the cheapest route to #217's "partial-success
consequences".

### 2.6 Opposed and assisted rolls

| | Fate Core | EP2 | CWN/SWN | PbtA / The Veil |
| --- | --- | --- | --- | --- |
| Opposed | both roll 4dF + skill; higher wins | aptitude+skill+d10 each; higher wins | usually a static save | usually **not** opposed; the fiction decides |
| Assisted | *create advantage* → +2; teamwork | teamwork bonus | assist bonus | *aid* move |

NoöPunk currently defines opposed as `STAT + Skill + 1d10` vs the same, with ties **deferred**.
Fate resolves ties by "the defender/target wins" convention; PbtA removes the tie entirely.

### 2.7 Resources and aspects

| | Fate Core | EP2 | CWN/SWN | PbtA / The Veil |
| --- | --- | --- | --- | --- |
| Narrative resource | **Fate Points** (invoke/compel) | Insight / Moxie / pools | Effort (SWN), System Strain | **Hold**, Strings, Obligation |
| Character descriptors | **Aspects** (high concept, trouble) | motivations, traits | foci/edges, backgrounds | playbook moves, **Beliefs** |

NoöPunk's current data has **no narrative-resource currency**, so this is net-new whichever centre
is chosen. Fate Points + Aspects is the centre's proposal; **Holds** and **Strings** are the
Narrativist analogues worth borrowing for the social layer (#220).

### 2.8 Backgrounds and lifepaths

| | Fate Core | EP2 | CWN/SWN | PbtA / The Veil |
| --- | --- | --- | --- | --- |
| Method | free-text aspects | **package-based lifepath** (background, career, faction, interest) | foci/edges + background | playbook choice |
| NoöPunk today | Lifepath-style, choose-or-roll (`RULEBOOK.md` §9) | — | — | — |

EP2's four-package lifepath is the closest structural match to NoöPunk's existing choose-or-roll
frame; Fate's aspects would *replace* it rather than extend it, and should be treated as a separate
decision.

### 2.9 Stunts, edges, foci, moves and PSI

| | Fate Core | EP2 | CWN/SWN | PbtA / The Veil |
| --- | --- | --- | --- | --- |
| Exception-based trait | **Stunt** (+2 or a rules exception) | sleights/traits/implants | **foci / edges** | **Moves** |
| Cost | refresh / stunt slots | points, gear | foci picks | playbook budget |
| PSI carrier | stunt or aspect | **discrete sleights** | separate power subsystem | a Move (or a psychic playbook) |

---

## 3. Labelling discipline — and where conversions are lossy

Every row above carries **D / A / U**. Three warnings attach to the whole table:

1. **Edition-dependent.** EP2's aptitude names changed between 1e and 2e (e.g. *Somatics* vs
   *Fitness/BOD*), and CWN/SWN differ from each other. A conversion that does not name the edition
   is not reproducible.
2. **Lossy by construction.** Mapping *Talk / Lead / Perform* onto a single Fate *Rapport* loses
   three distinct competencies; mapping Fate's *Lore* onto *Know + Research + Intelligence
   Analysis* inflates one. **Neither direction is lossless** and neither should be presented as a
   1:1 equivalence.
3. **Unsupported is an answer.** 13 NoöPunk skills have no PbtA counterpart because PbtA does not
   have a skill list. Marking that **U** is more useful than inventing a move for `Free Fall`.

---

## 4. Subsystem-by-subsystem comparison

For each: complexity · agency · genre fit · risk · what to adapt / avoid.

| Subsystem | F | E | C | P | Adapt / avoid |
| --- | --- | --- | --- | --- | --- |
| **PSI** | stunts/aspects: cheap, thin | **richest**, costly to run | separate subsystem, swingy | a move: thin but dramatic | **adapt** Fate's costliness + EP's structure; **avoid** importing EP psi metaphysics (NoöPunk has its own, #223) |
| **Combat** | abstract, fast, low crunch | detailed, slow | **concise, tactical** | fiction-first, no tactics | **adapt** CWN's brevity + NoöPunk's own wound ladder (#219); avoid OSR class assumptions |
| **Social** | aspects + *Rapport/Provoke* | skills only | *Talk/Lead/Connect* | **best-in-class** (moves, Strings, Beliefs) | **adapt** PbtA's texture; avoid its lack of mechanical depth for a simulationist goal |
| **Faction** | U (aspects at best) | reputation/faction mechanics | **faction turns — best-in-class** | U | **adapt** SWN faction turns; avoid level/HD scaffolding |
| **Cyberspace** | U as a subsystem | **most detailed** | CWN *Hacking* is concise | a move | NoöPunk already specifies four modes + graph hacking (#222); **borrow** CWN's brevity, avoid opaque theatre |
| **Investigation** | *Investigate* + create advantage | Research/Perceive | Notice/Know | **the PbtA investigation loop** | **adapt** the clue-forward loop; avoid bottleneck clues |
| **Cybernetics/transhumanism** | gear/stunts | **best-in-class** | gear + cyber | tags | **adapt** EP's breadth *as concepts only* (NC licence, §7) |
| **Advancement** | milestones | points/rep | **XP + foci** | XP triggers from fiction | **adapt** PbtA's fiction-driven XP triggers; avoid D&D levels |
| **GM procedure** | low | low | **generators, mission tools** | **MC moves/principles** | **adapt** both: OSR generators + PbtA principles; avoid railroading either way |

---

## 5. PSI as three different design objects

The issue requires these to be distinguished, because they are **not the same kind of thing**:

- **EP2 / SWN — discrete abilities.** A psi power is a discrete, acquired, individually rated thing
  with its own cost. Power is *possessed*. Counterplay is mechanical (psychic defence, strain).
- **Fate — a Stunt or an Aspect.** A psi effect is an *exception to the normal rules*, paid for out
  of a limited budget (refresh/stunt slots) and invokable. Power is *authored into the character's
  fiction*.
- **PbtA — a Move.** **A Move is not merely a power.** It is a *procedure*: a **trigger** ("when you
  open your mind to…"), a **roll**, and **choices/consequences** including hard ones. Its content
  is the situation, not a spell. Modelling PSI as a Move changes what PSI *is* in play — from a
  resource you spend to a moment you enter.

**Consequence for NoöPunk:** #223 has already formalised active/passive/combat PSI on the existing
check. The comparison says a Fate-first centre should carry PSI as **stunts plus a small
consequence economy**, and only *borrow* PbtA's trigger/choice structure for the fiction-facing
half — not replace the deterministic half, which #222 and #223 both require.

---

## 6. Two alternative Fate-first kernels (proposals — NOT canonical)

Both are **proposals for review**. Neither is implemented, and no number here overrides
`data/rules/core.json`.

### 6.1 The exact probabilities (computed, not estimated)

4dF is the sum of four dice each in {−1, 0, +1}; 81 outcomes:

| 4dF sum | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 | +4 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| count /81 | 1 | 4 | 10 | 16 | **19** | 16 | 10 | 4 | 1 |
| P(≥) | 100% | 98.8% | 93.8% | 81.5% | **61.7%** | 38.3% | 18.5% | 6.2% | 1.2% |

**4dF: mean 0, SD 1.633. 1d10: mean 5.5, SD 2.872.** Two consequences that decide everything else:

- **Expectation-matched DV shift.** To keep a legacy success chance, a Fate-dice DV must be
  **legacy DV − 5.5**: `9→3.5, 13→7.5, 15→9.5, 17→11.5, 21→15.5, 24→18.5, 29→23.5`.
- **The d10 gives a flat 10-point band per +1 rating; 4dF does not.** Under 1d10 each +1 rating is
  exactly +10 percentage points. Under 4dF the same swing is worth ~3 points at the top of the
  range, ~31 points in the middle, and ~31 again at the bottom. **A linear conversion cannot
  preserve both the centre and the tails.** That is a design decision, not arithmetic.

### 6.2 Kernel A — the Fate-native ladder

Attributes and Skills are each rated on a trimmed Fate ladder (**−1 … +5**, replacing 1–10), and a
check is `Attribute + Skill + 4dF` against:

| DV | 2 | 4 | 6 | 8 | 10 | 12 |
| --- | --- | --- | --- | --- | --- | --- |
| label | Simple | Everyday | Difficult | Professional | Heroic | Incredible |

Success chance by rating:

| rating (Attr+Skill) | DV 4 | DV 6 | DV 8 | DV 10 | DV 12 |
| --- | --- | --- | --- | --- | --- |
| +0 | 1.2% | 0.0% | 0.0% | 0.0% | 0.0% |
| +2 | 18.5% | 1.2% | 0.0% | 0.0% | 0.0% |
| +4 | **61.7%** | 18.5% | 1.2% | 0.0% | 0.0% |
| +6 | 93.8% | **61.7%** | 18.5% | 1.2% | 0.0% |
| +8 | 100% | 93.8% | **61.7%** | 18.5% | 1.2% |

**Balance consequences.** Ratings are small, so **every point matters enormously** — a +1 swing is
worth ~15-30 points near the centre, where the legacy d10 gave a flat 10. **Stacking must be
bounded** (a hard +2 cap on aspects/invokes, exactly as Fate does) or the ladder saturates at the
ends. A 1.2% floor and ceiling also means *automatic* success/failure is real: at rating +8 vs DV 4
the roll cannot fail, which the d10 system could never produce.

### 6.3 Kernel B — 1–10 preserved, Fate dice substituted

Attributes and Skills **stay 1–10** (author-locked attributes; the skill list is preserved
regardless). Check is `Attribute + Skill + 4dF` (range 2–20+4dF) against a **recalibrated** ladder
shifted by the expectation match:

| legacy DV | 9 | 13 | 15 | 17 | 21 | 24 | 29 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Kernel B DV | **4** | **8** | **10** | **12** | **16** | **19** | **24** |

**What this buys and costs.** Because the character side keeps its full 2–20 spread while the dice
spread halves, **competence dominates luck much more strongly than today**: the same characters
produce far more predictable outcomes and the flat 10-point band vanishes. Difficulty tuning
becomes *harder* for the GM, because the useful DV range widens to ~20 points while the dice only
contribute ±4. This is the option to prefer if the priority is *preserving existing character
numbers*; Kernel A is the option to prefer if the priority is *Fate-native simplicity*.

### 6.4 Worked comparable case (UNSA field agent)

*Agent: `INT 7`, `Investigation 4` → rating 11. Task: a Professional-grade forensic reconstruction.*

| System | Check | Success |
| --- | --- | --- |
| **Legacy (current canon)** | `11 + 1d10 ≥ 17` → needs 6+ on d10 | **50.0%** |
| **Kernel B (4dF, DV 12)** | `11 + 4dF ≥ 12` → needs 4dF ≥ +1 | **38.3%** |
| **Kernel A (rating ≈ +4, DV 6)** | `+4 + 4dF ≥ 6` → needs 4dF ≥ +2 | **18.5%** |

**Read this honestly: the three are not the same task.** The legacy 50% is the calibration target;
Kernel B lands ~12 points low at that DV (the rounding of `17 − 5.5` to an integer), and Kernel A
lands ~31 points low because a +4 rating is *not* equivalent to a legacy 11. Either kernel needs its
own calibration pass against a spread of legacy benchmarks before it can be called equivalent —
which is exactly why the issue forbids locking a formula now.

---

## 7. Source and rights matrix

Verified 2026-10-10. **A blocked or unverified row is recorded as unverified, not as a grant.**

| Source | Edition / version | Where verified | Licence | Commercially reusable? |
| --- | --- | --- | --- | --- |
| **Fate Core / FAE SRD** | official CC-BY SRD (ZIP) | `fate-srd.com/official-licensing-fate` | **CC BY** (the site offers CC-BY and OGL downloads and *recommends* CC) | **Yes, with attribution.** Note the site itself says *"Do not use the text on this site"* — the **downloaded SRD** is the licensed artefact, not the website text. Logos are **trademarks**: "Powered by Fate" needs the exact Evil Hat attribution line |
| **Transhumanity's Fate** | 2016 v1.1 | publisher page (issue) | **CC BY-NC-SA** | **No** — NonCommercial. Concepts and design lessons only; **no copied expression** |
| **Eclipse Phase (all releases)** | 2e | `eclipsephase.com/cclicense/` | **CC BY-NC-SA 4.0** *"unless noted otherwise"* — the page states **exceptions apply** | **No** — NC. Attribution to Posthuman Studios, LLC + link required for any reuse |
| **EP Rules Primer** | 2021 PDF | issue link | same NC family; **different scope from the full rules** | No — and note it is not the full rules |
| **Cities Without Number SRD** | community mirror `cwn.quadrifons.com` | mirror page | mirror says *"free, open-source, and public domain"* — **but it is a mirror and omits optional rules** | **Unverified at source.** Issue requires checking the **official CC0 SRD**; until then: **unverified** |
| **Stars Without Number Revised — Free Version** | free PDF | DriveThruRPG listing | **free-to-read, licence not established** | **No claim made.** Free availability is not an open licence |
| **Apocalypse World** | official site | issue link | **no universal PbtA SRD**; site offers playbooks/MC sheets | **Unverified** — conceptual use only |
| **Worlds of Legacy SRD** | 2020 PDF | issue link | **edition/licence not verified** | **Unverified** |
| **The Veil** | — | searched; no authoritative licence statement located | **not established in this pass** | **Unverified.** No official SRD should be assumed; #200 recorded the attached edition as CC BY-SA 3.0 — that remains an **author-stated classification**, not something this pass confirmed |
| **Fudge / Psi-Punk** | — | — | OGL 1.0a (designated OGC) / special licence | **Out of scope per #255**; must not enter the CC release |

**Bottom line for the CC target:** only **Fate Core's SRD** is cleanly adaptable today, under CC BY
with attribution. Everything else is either NC (EP, Transhumanity's Fate), unverified at source
(CWN, SWN, AW, The Veil, Worlds of Legacy) or out of scope (Fudge, Psi-Punk). **Concepts may inform
design; copied expression may not enter a commercially reusable CC release.**

---

## 8. Cross-references to existing repo work

| Existing artefact | Relationship | Action |
| --- | --- | --- |
| `docs/design/ISSUE_200_DIRECTION_2026-10-10.md`, `ISSUE_200_CC_RELEASE_GATE.md`, `ISSUE_200_KERNEL_PROTOTYPE.md`, `ISSUE_200_RESOLUTION_EXPERIMENT.md`, `ISSUE_200_CROSS_SYSTEM_CONVERSION.md` | #200's centre — **now superseded for future comparison decisions** by #255 | **Preserve.** Keep passing; flag the Fudge/Psi-Punk centre as superseded, do not delete |
| `docs/design/RPG_CONVERSION_REFERENCE.md` (298 lines) | existing conversion tables including RED | **Preserve**; overlaps §2 and should be merged into this document's structure only after review |
| `docs/rules/EP2_CONVERSION_MATRIX.md` (142 lines) | EP2 → NoöPunk port status | **Preserve**; supplies the EP2 column's honesty about partial ports |
| `data/rules/conversion_matrix.json` | machine-readable conversion rows | **Preserve**; candidate to consume these tables later |
| `data/rules/core.json` | the live kernel: `STAT + Skill + 1d10`, DV ladder 9/13/15/17/21/24/29, untrained −1, field −1 | **Unchanged by this document** |
| `data/rules/skills.json` (40 skills) | the canonical list mapped in §2.2 | **Unchanged.** §2.2 maps it; it does not re-author it |
| **#217** (core rules / −3…+3 migration) | owns the kernel decision this document gates | This document **informs** #217; it does not decide it |
| **#218–#232** (subsystem specs) | consume whichever kernel #217 approves | §4 says what to adapt per subsystem; #219–#230 have already landed procedures on the *current* kernel |
| **#144** (faction taxonomy) | faction comparison in §4 | Cross-referenced, not changed |
| **#158 / #159** (equipment policy; skill file) | §2.2 respects both | `skills.json` is the source of truth and is untouched |

### Conflicts identified, not resolved

1. **A centre conflict.** #200's documents describe a Fudge/Psi-Punk centre; #255 replaces it. Both
   are in the tree. **This document records #255 as current and #200 as superseded for future
   comparisons** — and does not rewrite #200's files, because #255 says to preserve them.
2. **A ladder conflict.** The current DV ladder is d10-shaped (7 steps, 9–29). Neither Fate (tops
   out at +8) nor PbtA (3 outcomes) can host it without recalibration (§6.3).
3. **A skill-granularity conflict.** #255 says the skill list "draws from" Transhumanity's Fate, EP
   and CWN. §2.2 shows it is **nearest to EP2 and CWN/SWN and furthest from Fate** — the list should
   not be described as Fate-derived.
4. **A "−3…+3" tension.** #213/#215 have already moved parts of the prototype to a −3…+3 scale while
   `core.json` still fixes 1–10 attributes. This document does not resolve it; it is flagged for
   #217.

---

## 9. Recommendation (for the author's decision — not an implementation)

**Recommended direction: Fate-first, as the centre — but with NoöPunk's own six attributes and the
existing 40-skill list on top of it, and with the d10 replaced only after a calibration pass.**

1. **Adopt the centre:** Fate's aspects, stunts, stress/consequences and fiction-first flexibility.
2. **Do not adopt Fate's unified skill model.** Keep six Attributes **and** separate Skills; §2.2
   shows the list is not Fate-shaped and should not be forced into it.
3. **Prefer Kernel B** (preserve 1–10) if existing character numbers and continuity matter most;
   **prefer Kernel A** if simplicity matters most. **Both need calibration against a spread of
   legacy benchmarks** (§6.4) before locking — a single worked case is not sufficient evidence.
4. **License guardrail:** only the Fate Core SRD is adaptable today. EP, Transhumanity's Fate, SWN,
   AW and The Veil are **not** cleared for copied expression in a commercial CC release.
5. **Nothing here is canonical.** No `data/rules/*` change, no `RULEBOOK.md` change, and no
   migration until the author records the decision on #255 / #217.
