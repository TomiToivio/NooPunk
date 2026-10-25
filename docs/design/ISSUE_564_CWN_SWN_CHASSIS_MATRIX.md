# Issue #564 — CWN/SWN chassis: measured baseline, disposition matrix, and the ruling it needs

**Status: design record and decision support. Not rules. No mechanic is approved or implemented by
this file.**

`strategy_game/docs/RULE_SYSTEM_RESEARCH.md` §"Gates" still reads: *"Until all relevant gates, no
gameplay mechanics are implemented."* Gate A (leader RPG rules), B (political-simulation
methodology), C (strategy rules) and D (integration contract) are all open. This document therefore
does what an agent may do — measure, compare, and put the choice in front of the author — and does
not do what it may not: choose a chassis or write mechanics.

---

## 1. What the epic asks for

Issue #564 wants NoöPunk's playable rules converted onto an adapted **Cities Without Number (CWN)**
chassis with **Stars Without Number (SWN)** brought in selectively. It asks for an inventory, a
CWN/SWN → NoöPunk mapping matrix over the epic's eighteen named subsystems (twenty-four rows, after
the four the first pass omitted — §4), a playable tabletop vertical slice,
a unified digital kernel, scenario migration, validation, and documentation cleanup — and it asks
that the work be **broken into linked sub-issues rather than landed as one rewrite**.

Three of them are executable now: the inventory, the matrix, and the breakdown. The rest wait on
the ruling in §6.

---

## 2. The measured baseline

Measured on `origin/main` at the time of writing. This repository holds **two games** (`AGENTS.md`
§0), and the difference matters for every row below.

| | Legacy NoöPunk RPG | Crossover game |
| --- | --- | --- |
| Rulebook | `RULEBOOK.md` (6,244 lines) + `rulebook/` | `strategy_game/RULEBOOK.md` (214 lines) |
| Core check | **`STAT + Skill + 1d10` vs Difficulty Value** | **`4dF + skill`**, four outcomes |
| Rated traits | 6 STATs at 1–10 **and** 40 skills | 6 individual skills (COG, INT, REF, SAV, SOM, WIL) |
| Kernel approval | living canonical rulebook, author-owned | Fate foundation approved (#389), six skills approved (#482) |
| Status | must not be rewritten | the game whose rules are still open |

Evidence: `RULEBOOK.md:41`, `:226`, `:324`, `:330`, `:332` all state `STAT + Skill + 1d10 vs
Difficulty Value`. `strategy_game/RULEBOOK.md:14` names the author-selected baseline as "Fate Core
four actions, 4dF + skill, character aspects, stunts, Fate points, stress and consequences", and
`:36` lists *Fate Core System* (CC BY 3.0) as **"the chassis … Implemented."**

**CWN's present standing in this repository is a conversion source, not a chassis.**
`docs/design/RPG_CONVERSION_REFERENCE.md` §"Cities Without Number → NoöPunk" (`:209`–`:247`) gives a
CWN attribute table (3–18 → STAT) and a CWN skill-level table (untrained / 0–4 → NoöPunk). It
converts *into* NoöPunk. Nothing adopts CWN's own kernel.

---

## 3. Three premises in the issue that the repository does not support

These are recorded here because the epic's constraints section states them as settled facts, and a
matrix built on them would be a matrix of the wrong system. **None of this is a criticism of the
intent** — it is the difference between "we agreed to this" and "we did this once, in a conversion
table".

### 3.1 `CHA` is not one of the six attributes

The issue names the attributes as *"FIT/REF/INT/CHA/CYB/PSY"*. The rulebook's sixth attribute is
**SOC**, not `CHA`: `RULEBOOK.md` uses `SOC` throughout its skill table (`:249`, `:251`, `:264`,
`:266`, `:275`, `:282`), and `CHA` appears nowhere in it. The decision queue also records the set as
*"the six 1–10 STATs … FIT/REF/INT/SOC/PSY/CYB"* (D29).

This is a one-word correction, but it matters: `CHA` is CWN's own attribute name, so writing `CHA`
into a NoöPunk ruleset silently imports CWN's attribute model through the back door.

### 3.2 There is no "present 3d6 core-check model"

The issue asks to retain *"the present 3d6 core-check/difficulty model"*. **No 3d6 core check
exists in this repository.** `grep -nE "3d6|3D6" RULEBOOK.md` returns **no matches**. The legacy
kernel is `1d10`; the crossover kernel is `4dF`.

Two readings remain possible and they are not equivalent:

- **(a)** the issue means *attribute generation* (3d6 for STATs) and the phrase has drifted onto the
  check by mistake;
- **(b)** it means a kernel this repository does not have, and the epic is proposing a **third**
  kernel.

Until that is answered, "retain the present 3d6 model" cannot be implemented, only guessed at.

### 3.3 #19 did not establish CWN as the starting chassis

The issue says *"#19 (closed) already establishes the CWN SRD as an open starting chassis and the
subsystem-by-subsystem KEEP / MODIFY / REPLACE / OMIT / DEFER process."*

What is on `main` is narrower, and partly the opposite. `docs/design/ISSUE_197_SCOPE_2026-10-10.md`
:30 quotes an **author directive** recorded from issue #197:

> *"Retain existing NoöPunk attributes, core dice/skill design, faction and reputation design unless
> another issue explicitly changes them. Do **not** import Shadowrun/Eclipse Phase/CWN mechanics
> wholesale."*

And the crossover's own rulebook names Fate Core as the chassis, *implemented*.

So the repository currently contains, in order of recency: an author directive against importing CWN
wholesale; an implemented Fate Core kernel (#389); six approved individual skills (#482); and a CWN
conversion table. **#564 is the newest statement and may well supersede all of it — but superseding
is a ruling, and an agent may not infer it.** This is the subject of §6.

One thing that is *not* in doubt: the KEEP/MODIFY/REPLACE/OMIT/DEFER vocabulary does exist in the
decision queue and is used throughout it (D3, D22, D29–D36). The matrix below uses it.

---

## 4. The disposition matrix

For each subsystem: what CWN (and, where it would enter, SWN) offers; the disposition against the
**measured** NoöPunk baseline; the rationale; the authoritative reference; and migration status.

Dispositions are proposals. `DEFER` means the subsystem cannot be decided before §6.

**Corrections of 2026-10-25, after the rows were first written.** Six rows below carried a premise
the tree does not support, or a verdict that a *measurement* contradicts; they are marked
**CORRECTED** and the evidence is in the row. The numbers for rows 6–8 and 10 come from
`tools/issue571_lethality_lab.py` and its record `ISSUE_571_COMBAT_INJURY_TRAUMA.md` (exact
enumeration, deterministic, 16 code tests), not from an argument.

**SRD references** in the tables are paths under `https://cwn.quadrifons.com/`, read on
**2026-10-25**. Rows 16–19 name the page the consulted mirror does **not** serve
(*Antagonists & NPCs* is omitted) or state that no counterpart exists, rather than inventing a
citation; every row that says "SWN" is licence-blocked (§5).

| # | Subsystem | CWN / SWN offers | Disposition | Rationale | Authoritative reference | Migration |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | **Attributes** | Six: STR/DEX/CON/INT/WIS/CHA, 3–18, `-1..+2` modifier band (SWN same) | **OMIT** as a set | NoöPunk's six are FIT/REF/INT/SOC/PSY/CYB and `SOC`/`PSY`/`CYB` carry meanings CWN's set has no slot for: `CYB` is cybernetic integration as a *rated* capacity and `PSY` is PSI capacity, not a wisdom score. Adopting CWN's names would delete the three attributes that make the sheet NoöPunk. | SRD `character-creation/attributes/`; `RULEBOOK.md` STAT section; `RPG_CONVERSION_REFERENCE.md:214` | none needed — the conversion table already maps CWN→NoöPunk |
| 2 | **Attribute generation** | 3d6 per attribute, or an array | **DEFER** — **CORRECTED** | There is **no live generation rule to keep**, and the live attribute scale is `1..10` (locked by #131, `data/rules/core.json`), not `3..18` — so the epic's "3d6 / −3..+3" premise describes the retired sketch. `data/rules/core.json` defines the six STATs, the check and the DV ladder, and no generator at all; `AGENTS.md` §4 records the old `FIT/REF/INT/CHA/CYB/PSY` sketch *and its 3d6 generator* as porting debt that survives only in the retired module (`src/rules/_retired.py`, "do not extend"). The issue's "3d6 generation" premise is the same stale premise §3.2 corrects, so this row cannot KEEP what does not exist. CWN's array (`14/12/11/10/9/7`) and a 3d6 roll are *options* for the author, never imports. | SRD `character-creation/attributes/`; `data/rules/core.json` (no `generation` key); `AGENTS.md` §4; `src/rules/_retired.py` | blocked: generation is an open design area |
| 3 | **Skills** | Level 0–4, `untrained` at `-1`, specialisations as narrow bonuses | **MODIFY — layer B only; KEEP layer A untouched** — **CORRECTED** | The row previously read #482's six Fate skills (`COG/INT/REF/SAV/SOM/WIL`) as *the* roster. Those six are **layer B's**, approved for the crossover; **layer A's roster is 40 skills at 1–10, locked by #159** (`data/rules/skills.json`, `RULEBOOK.md` §4.1) and is not in play here. What CWN's scale may inform is the crossover's six-skill allocation (D22/D23) — not the legacy 40. | SRD `character-creation/skills/`; `data/rules/skills.json` (#159); `strategy_game/rpg/skills.py` (#482); queue D22/D23 | layer A: none needed; layer B: conversion table exists |
| 4 | **Core resolution** | `2d6 + skill + attribute modifier` vs fixed targets (6 / 8 / 10), no opposed-roll culture | **DEFER** — and this is *the* decision | The legacy kernel is `1d10`, the crossover kernel is `4dF` and **approved**. Adopting 2d6 would retire an approved kernel and invalidate its tests. Queue D31 already lists "replace the kernel (2d6 or d10)" as option **D** and recommends against it. #564 must either accept D31's answer or explicitly overrule it. | SRD `rules-of-the-game/skill-checks/`; `RULEBOOK.md:41`; `strategy_game/RULEBOOK.md:14`; queue D31 | blocks items 5–13 |
| 5 | **Saves** | Attribute-based saves, rolled against a target | **MODIFY** | Worth taking *in shape*: a named save is faster to call than "roll this skill". Must be expressed in whichever kernel survives item 4 — a save is a check with a fixed trait, not a new dice convention. | SRD `rules-of-the-game/saving-throws/`; queue D31 outcome | after item 4 |
| 6 | **Initiative** | `1d8 + DEX` modifier, descending order | **OMIT (layer A)** — **CORRECTED** | Not "the legacy game already orders turns" vaguely: layer A orders **every realm** by **descending REF** on the one shared clock, and the chapter forbids forking it (`rulebook/18_CROSS_DOMAIN_STATE.md` §Initiative). A CWN d8 initiative would be a second order for the same clock. Layer B's D34 decides its own economy. | SRD `rules-of-the-game/combat/combat-initiative/`; `rulebook/18_CROSS_DOMAIN_STATE.md` §Initiative; #225 | none — already defined |
| 7 | **Combat** | Attack vs AC, **Shock** damage on a miss against low-armour targets, **Trauma Die** for lethal hits, action economy with move+act | **OMIT (layer A); DEFER (layer B)** — **CORRECTED** | Measured, not argued: (a) **Shock already exists in shape** — in layer A a miss lands on **Scratched**, 100 % of the time at a hopeless check, so CWN needs a second number to state the same fiction; (b) **layer A's margin already encodes severity** — the band function maps margin to rung, and adding the Trauma Die turns **26 % of Everyday-difficulty Wounded results into Down** (18.8 % at DV 15, 11.2 % at DV 17): a double count; (c) the action economy would be a second clock (`rulebook/18`, 3 AP). Layer B's combat is D34's and is already recommended as a Fate zone conflict. | SRD `rules-of-the-game/combat/`, `…/combat-actions/`, `…/attacks-in-combat/`; `rulebook/3_PHYSICAL.md` §Attacking/§Wounds; `rulebook/18_CROSS_DOMAIN_STATE.md`; `ISSUE_571_COMBAT_INJURY_TRAUMA.md` §4–§5 | layer A: none; layer B: D34 |
| 8 | **Injuries and trauma** | Trauma Die severity, mortal wounds, lingering injuries | **OMIT the Trauma Die; DEFER the two clock/table ideas** — **CORRECTED** | The Trauma Die is row 7's double count. What *is* worth taking is CWN's **clock after the injury**: "Mortally Injured, dies at the end of the sixth round unless stabilised at `8 + rounds since the fall`" converts layer A's `Down` state into a scene-level countdown with a rising price. It must be re-expressed in layer A's currency (**exchanges**, not six-second rounds) and its length is unauthored, so it is a question, not an import. The d12 Major Injury table is CWN expression *and* would need author-authored entries (`AGENTS.md` §1). | SRD `rules-of-the-game/combat/damage-trauma-shock/`, `…/injury-healing-system-strain/major-injuries/`; `RULEBOOK.md` §51; `rulebook/3_PHYSICAL.md` §Wounds; D3/D35 | blocked on D3/D35 |
| 9 | **Healing** | Time-based recovery, medical checks, cyberware-assisted healing | **DEFER** | NoöPunk's psychosurgery is a four-layer construct (Jungian + psychedelic + cybernetic + psychotronic) and healing must not flatten it into a medkit roll. CWN has nothing to say about it. Note the author has **not** authored the injury-recovery timings (D3 `status_consequence_rows`). | SRD `rules-of-the-game/injury-healing-system-strain/natural-healing-first-aid-poisons/`; queue D3; canon §psychosurgery | blocked on D3 |
| 10 | **Armour and equipment** | Armour as damage reduction with an encumbrance cost; gear lists with prices | **OMIT armour-as-reduction; DEFER encumbrance** — **CORRECTED** | Armour-as-reduction is a **canon conflict**: `rulebook/3_PHYSICAL.md` §Armor states armour's effect is "a **ladder step**, never a subtraction", that it does not stack, and that cover and armour apply in that order. Measured difference: a Heavy Pistol removes an unarmoured 5-HP CWN target in **1.89** attacks and needs **12.21** against Soak 5 — subtraction can zero a hit, a one-step shift cannot. Encumbrance is a reserved numeric area and stays `DEFER`. The *gear list* is not portable either: NoöPunk's signature objects are setting artefacts. | SRD `gear-vehicles-cyberware/armor/armor-types/`, `…/weapons/weapon-stats-and-definitions/`; `rulebook/3_PHYSICAL.md` §Armor; `RULEBOOK.md` §51/§52; `ISSUE_571_COMBAT_INJURY_TRAUMA.md` §5.5 | none for armour; encumbrance blocked |
| 11 | **Cyberware / BCI** | Cyberware with **System Strain** as a capacity limit | **MODIFY** | System Strain is the single most useful CWN import for this setting: it makes cybernetic cognition *cost* something, which is the whole point of a BCI that thinks with you. But queue D36 proposes "no capacity number, the implant is a permission plus a tag" and lists slots as the cheap alternative; a strain number was already rejected there as option C4. **This row and D36 are the same question** and must be answered together. | SRD `gear-vehicles-cyberware/cyberware/`, `…/cyberware/cyberware-alienation/`, `…/cyberware/system-strain/`; queue D36; canon §cybernetics | blocked on D36 |
| 12 | **Hacking / network access** | Hacking as a skill check against a target, with hardware and access prerequisites | **MODIFY — resolution procedure only; the access model stays NoöPunk's** | CWN's *prerequisite structure* — you need physical or credentialed access first — is exactly the "disconnected devices and physical ingress" the epic asks for, and it matches `ISSUE_222_CYBERSPACE_SCOPE.md`. The dice are item 4's problem. | SRD `hacking/hacking-mechanics/`, `hacking/programs/program-verbs/`; `ISSUE_222_CYBERSPACE_SCOPE.md` | after item 4 |
| 13 | **Drones and vehicles** | Vehicle operation as a skill; drone control as a check; vehicle combat as an extension | **DEFER** | NoöPunk has no vehicle subsystem today and the epic does not require one. Adding it would be inventing a subsystem the setting does not yet need. Revisit if a scenario calls for it. | SRD `gear-vehicles-cyberware/drones/`, `…/vehicles/`, `rules-of-the-game/combat/vehicle-combat/`; — | not started |
| 14 | **Character creation** | Pick attributes, pick skills, pick a **class/background**, roll or choose | **MODIFY** | The *procedure* is useful; the **class** is forbidden — the epic says no standard classes or levels, and #197 recorded "Geeks/Jocks/Freaks" as slang, explicitly *"not official or mandatory classes"*. NoöPunk's Lifepath framework (#144) is the creation spine and must not be replaced by a CWN background table. | SRD `character-creation/`, `…/backgrounds/`, `…/foci/`; #144; `rulebook/14_CHARACTER_GENERATION.md` §13.8; #197 scope | none — Lifepath is canonical |
| 15 | **Advancement** | XP thresholds, level-ups, skill point spends | **DEFER** | The epic forbids levels. Fate advances by milestone and refresh; CWN by XP and levels. These are incompatible and the choice is the author's. `RULEBOOK.md` §3 records skill allocation as unspecified and queue D23 records the 25-point / Great-cap baseline without approving a distribution. | SRD `rules-of-the-game/character-advancement/`; queue D23 | blocked on D23 |
| 16 | **Encounters** | Reaction rolls, morale, encounter distance, surprise | **MODIFY** | Morale and reaction rolls are cheap and improve a dialogue-first game: they give NPCs a reason to stop fighting. Encounter *distance* assumes a grid the tactical layer has not chosen (D38). | **no SRD page** — the consulted mirror omits the *Antagonists & NPCs* section, so reaction/morale is recorded from the index only; queue D38; `ISSUE_229_NARRATIVE_LAYER.md` | after item 7 |
| 17 | **Investigation** | No dedicated subsystem; CWN is combat-and-heist shaped | **OMIT the gap — KEEP NoöPunk's** | This is the epic's core requirement: *"retain investigative, dialogue-first, deadly-combat play."* CWN has nothing to offer here, so investigation stays NoöPunk's. There is no import to make. | **no SRD counterpart** — CWN has no investigation subsystem; `ISSUE_200_*`; `ISSUE_220_SOCIAL_PROCEDURES.md` | none |
| 18 | **Factions** | SWN's faction turn: assets, HP, attacks, goals on a faction scale | **DEFER to the strategy layer** | SWN's faction game is genuinely good and genuinely a *different* layer. NoöPunk already has a boundary: `rpg/boundary.py` refuses the join to `WorldState` on purpose, and #502 leaves `MissionOutcome.effects` empty. Importing SWN's faction turn would collapse the character-to-faction boundary the epic says to retain. Gate C governs the strategic layer and is open. | **no SRD counterpart here** — the faction turn is SWN's, and SWN is licence-blocked; `rpg/boundary.py`; queue D35; Gate C | blocked on Gate C |
| 19 | **NPCs** | Statlines as NPC stat blocks with hit dice | **MODIFY** | A statline convention is useful and queue D30 already contemplates keeping FIT…CYB as "the conversion vocabulary for NPC statlines". Hit *dice* are a level artefact and do not survive. | **no SRD page** — the mirror omits *Antagonists & NPCs*; queue D30 | after items 1 and 4 |
| 20 | **World and mission procedures** | SWN world tags, sector generation, mission generators | **OMIT** | NoöPunk's world is authored, not generated: an authored Helsinki/UNSA setting with canon institutions, and `AGENTS.md` §1 forbids inventing canon. A sector generator would manufacture setting, which is the one thing an agent may not do. SWN tags could inform a *naming* convention at most. | SRD `rules-of-the-game/scenes-rounds-mission-time/`; `AGENTS.md` §1; canon rulebook | none |

### Four rows the epic names that this matrix did not have

CWN procedures that are gaps on our side, each a candidate `MODIFY` rather than an `OMIT`. They are
added here because the epic's own subsystem list names them and a matrix that skips them reads as if
the question had been answered.

| # | Subsystem | CWN / SWN offers | Disposition | Rationale | Authoritative reference | Migration |
| --- | --- | --- | --- | --- | --- | --- |
| 21 | **Chases and pursuit** | A dedicated pursuit procedure with ranges, obstacles and a clock | **MODIFY (proposal)** | The clearest real gap: NoöPunk has **no** chase procedure at all, and a chase is one of the three things a scene can be (`rulebook/3_PHYSICAL.md` §"What a fight is made of" names chases only as time). CWN's *shape* — distance bands and a clock — fits layer A's difficulty-step vocabulary (`simple_target_number` already moves a step per cover/aim), so it can be expressed without a second engine. Numbers are unauthored. | CWN SRD `rules-of-the-game/chases-and-pursuit/`; `rulebook/3_PHYSICAL.md`; `rulebook/18_CROSS_DOMAIN_STATE.md` | not started; no code |
| 22 | **Scenes, rounds and mission time** | Three named time measures: scene, round (≈6 s), mission time | **MODIFY (proposal)** | Layer A has an **exchange** clock and a scene vocabulary, but **no mission clock** — nothing lets an infiltration *cost time*. CWN's third measure is one word and one rule; it would give #517's access/heat model and the action clock a shared unit. Must be named against the existing exchange, not instead of it. | CWN SRD `rules-of-the-game/scenes-rounds-mission-time/`; `rulebook/18_CROSS_DOMAIN_STATE.md`; #517 | not started; no code |
| 23 | **Program composition (verbs × subjects)** | Programs are a **Verb + Subject** pair with an Access cost | **MODIFY (proposal), layer A only** | Layer A has the escalation ladder (T0–T4, Trace/ICE) and the access classes but **no composition grammar**: an operator chooses a capability, not a program built from parts. The grammar is a naming/assembly convention over canon `Program`/`Infosec` checks, so it adds no dice and no new Skill — but it is a mechanical layer, so it needs the author's word. | CWN SRD `hacking/hacking-mechanics/`, `hacking/programs/program-verbs/`, `…/program-subjects/`; `rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md` | blocked on author approval |
| 24 | **Encumbrance, crafting and gear maintenance** | Encumbrance slots; crafting and maintaining mods | **DEFER** | Reserved numeric area (`AGENTS.md` §4: equipment statistics), and the capability-not-catalogue doctrine (`rulebook/13_EQUIPMENT.md` §12.1) is the opposite of a slot count. Recorded so the row is not silently missing. | `AGENTS.md` §4; `rulebook/13_EQUIPMENT.md` §12.1 | blocked: reserved |

### The Worlds Without Number and Ashes Without Number rows (#564 extension, 2026-10-25)

The epic was extended to the whole Without Number family, and the extension promised "a small number
of genuinely new rows (Effort as a committed-resource model; Foci↔stunts; mutations; Edges; salvage)".
Those rows were **not in this matrix** — the file had zero mentions of either book — so they are added
here, numbered on from row 24 and written to the same standard: measured against the tree, not argued.

| # | Subsystem | WWN / AWN offers | Disposition | Rationale | Authoritative reference | Migration |
| --- | --- | --- | --- | --- | --- | --- |
| 25 | **Effort** | WWN: a committed-resource pool. Max Effort = `1 + relevant skill level + the class's attribute modifier`; a *partial* class gets one fewer, minimum 1. Powers **Commit Effort for the duration** (reclaimable as an Instant action) or **for the scene** (returns only at scene end). Pools are tracked per class and do not mix. | **MODIFY (proposal) — the leading candidate for the PSI / cybernetic-cognition cost model (D36)** | It is the only model in the family where an *ongoing* effect keeps a resource tied up, which is what "the mind pays for the mind's work" needs: a sustained psychic or BCI burden is represented **without a second hit-point track**, and the duration/scene split gives two grades of persistence for free. Crucially the shape is **content-free** — it carries no spells and no psionics — so it does not drag in SWN's virus-derived psi ontology that row 18 and the canon rulebook reject. What it needs is re-expression in layer A's currency (**exchanges and scenes**), and the pool size is an unauthored number. | WWN SRD `1.0 Character Creation/1.4.0 Classes.html` — **CC0** | blocked on D36 (same question as row 11) + D40; no code |
| 26 | **Foci** | WWN: two-tier talents. First selection grants **Level 1**; selecting the same Focus again **adds Level 2** to Level 1. Any PC may take any Focus if the player can explain how they acquired it. | **MODIFY (proposal) — take the structure, never the catalogue** | A two-tier Focus is structurally identical to an approved **stunt plus its upgrade** (#389/#482), which means the crossover's stunt system does not need a new skeleton — it needs its existing one named consistently. The trap is the catalogue: WWN's Focus text is CC0 and therefore *legally* copyable, which makes it **more** important not to copy it, because NoöPunk's stunts must be authored for this setting (AGENTS.md §1) rather than ported from a fantasy default. | WWN SRD `1.0 Character Creation/1.6.0 Foci.html` — **CC0** | after the stunt catalogue exists; no code |
| 27 | **Mutations** | AWN: mutation points bought at creation, with **damaging mutations granting points** (a debt economy) | **DEFER — with a canon conflict to settle first** | Mutation-as-mechanic implies a **mutagenic cause**, and NoöPunk's PSI is explicitly natural rather than virus-derived. The epic's "growing stranger as the shocks accelerate" requirement may want this, but it needs the author to decide whether strangeness has a *mutagenic explanation* in canon or a panpsychic one — the two produce different fiction. Separately, **AWN has no SRD**, so its text is not CC0; the mechanic could be reproduced independently but that is a design act, not an import. | AWN Free Edition (2025, 257 pp) — **no SRD; no page citation is admissible until the licensing pass admits it** | blocked on canon + licence |
| 28 | **Edges** | CWN and AWN both answer advancement with **a single class plus Edges** instead of a class list | **DEFER — but the only family answer that is compatible with the epic's class ban** | It differentiates characters without **levels**, which is what the epic forbids. Whether one shared class still counts as "a class" is precisely the question rows 14–15 leave open, so this row is recorded next to them rather than decided. CWN's Edges are citable (subject to §5); AWN's are licence-blocked. | CWN SRD `character-creation/` (Edges path to be pinned by the licensing pass); AWN — **no SRD** | blocked on the class/level question (rows 14–15) |
| 29 | **Salvage and survival** | AWN: salvage, scarcity and survival procedures, built for three apocalypse models | **DEFER** | The *scarcity* framing is usable for crisis-era economy **without** implying a Fall, which canon requires (pre-Fall alternate timeline). But its text is licence-blocked, and the epic's "disconnected devices and physical ingress" need is already met by CWN's **access prerequisites** (row 12), so nothing here is load-bearing. Recorded so the omission is deliberate rather than an oversight. | AWN — **no SRD** | not started; blocked on licence |

**Net, and it is a licensing asymmetry rather than a design one.** WWN contributes two *structures*
(Effort, Foci) and is the **only one of the four whose SRD text may be copied verbatim** — which is
also why it is the one to copy least from, since the copyable material is fantasy content NoöPunk would
have to re-author anyway. AWN contributes genre procedures but **no SRD exists**, so no AWN text may
enter the tree at all; every AWN-derived row above is therefore either `DEFER` or a design act rather
than an import. CWN's SRD is the community compile described in §5.

### SWN: what actually enters

| SWN element | Disposition | Why |
| --- | --- | --- |
| Faction turn | **DEFER** | It is a strategic-layer engine, not an RPG subsystem, and Gate C is open (row 18). |
| World/sector generation | **OMIT** | Would generate canon (row 20). |
| Space travel, starships | **OMIT for now** | The epic says *"without prematurely turning the Earth-based game into a space campaign."* Nothing in NoöPunk needs a ship. |
| Classes (Warrior/Expert/Psychic) | **OMIT** | Forbidden by the epic and by #197's "not official or mandatory classes". |
| Psionics procedures | **DEFER** | NoöPunk's PSI is panpsychic and ontological, not a virus or a discipline tree (canon §QIP vs virus). CWN/SWN psionics are the wrong model. |
| Save categories, morale, reaction | **MODIFY** | Portable and cheap (rows 5, 16). |

**Net:** SWN contributes two adjudication habits and one strategic engine that is out of scope. It is
not a second rulebook here, which is what the epic asked for.

---

## 4b. The four-book family (added 2026-10-25)

CWN, SWN, **AWN** and **WWN** are one engine with per-book extensions, so they are disposed of as a
family rather than four times over.

**Shared by all four:** `2d6 + attribute modifier + skill` vs a target; `d20 + attack bonus` vs AC;
four saves (Physical, Evasion, Mental, Luck); Shock and Trauma for lethality; Foci as two-tier feat
packages; **Effort** as a committed-resource pool.

| Book | Adds | Disposition |
| --- | --- | --- |
| **CWN** | single class + Edges; hacking access prerequisites; cyberware + System Strain | **MODIFY** — rows 11, 12, 14 |
| **SWN** | Effort psionics; starships; faction turn; world/sector tags | **BLOCKED (licence)** — `blocked-unverified` in the rights ledger, so **nothing may be adapted**. CWN supplies the same saves and morale procedures (CC0-verified), so no capability is lost. Rows 18, 20 stay OMIT on setting grounds anyway. |
| **AWN** | single class + Edges; Trauma; mutations (bought with points; damaging ones grant points); salvage/survival | **MODIFY** — rows 21, 22 |
| **WWN** | Foci in full; Effort-based High/Low Magic; Legate tier; world tags | **MODIFY** Foci + Effort; **OMIT** magic and Legates |

Additional rows created by the family:

| # | Subsystem | Disposition | Rationale |
| --- | --- | --- | --- |
| 21 | **Effort as a committed-resource model** (WWN/SWN) | **ADOPT** — author ruling 2026-10-25: SWN's rules, for a learnable natural human ability | The one portable mechanic that solves "the mind pays for the mind's work" without a third stress track: a lasting PSI effect or an active BCI link *commits* capacity rather than subtracting a number. Replaces D36's three weak options with a fourth. Specified in `ISSUE_564_RULES_COMPATIBILITY_SPEC.md` §3.1. |
| 22 | **Mutations and salvage** (AWN) | **MODIFY** | Directly serves the epic's "growing stranger as the shocks accelerate" and crisis-era scarcity, and it does so **without implying a Fall** — the pre-Fall canon holds. Needs an authored source of mutation in the setting before it can enter play. |
| 23 | **Foci as a two-tier stunt shape** (WWN) | **MODIFY** | Stunts are approved but *"the full stunt catalogue"* is not (`strategy_game/RULEBOOK.md` §16). Foci supply a shape — two tiers, explicit prerequisite, no tree — not a mechanic. Spec §3.2. |
| 24 | **Edges as classless differentiation** (CWN/AWN) | **MODIFY — candidate answer to D23** | The family's own answer to "differentiate without classes", which is exactly what this epic requires. Spec §3.4. |
| 25 | **Four named saves** | **MODIFY** | Vocabulary, not arithmetic: a save is a check against a fixed trait under any kernel. `Luck` is a real tonal question — a game about structural power may want to refuse it. Spec §3.3. |

**Specification:** `ISSUE_564_RULES_COMPATIBILITY_SPEC.md` carries the procedures themselves, written
kernel-agnostically so that D40 chooses one line rather than rewriting the file. Combat, Shock,
Trauma and healing are **not** re-specified there — they are `ISSUE_571`'s.

**Licensing, per the repository's own ledger — not per an assumption.** `data/sources/game_system_rights.json`
(read by `tools/release_packaging_guard.py`) records each source with its evidence and access date:

| Source | Ledger decision | Consequence here |
| --- | --- | --- |
| **CWN SRD** | `verified-public-domain` (CC0, three agreeing readings, checked 2026-10-10) | SRD text **and** mechanics reusable; scope limited to the SRD. **This is the only book this epic may adapt today.** |
| **SWN** | `blocked-unverified` | **Nothing may be adapted.** Sine Nomine publishes a free *edition* for SWN, not an SRD; the CWN/WWN CC0 listings do not cover it. |
| **WWN** | **not yet in the ledger** | The SRD's own introduction waives copyright via **CC0** and states its purpose is to show *"exactly what I consider to be freely-usable game mechanics"*, including the right *"to use its text verbatim in a commercial product"*. Verified at the source — but it needs a **ledger entry with its access date** before this repo may rely on it, exactly as CWN has. |
| **AWN** | **not yet in the ledger, and unverified** | Published 2025. **No SRD availability is established.** Do not adapt its text until an entry exists. |

The licensing sub-issue is **#569**; nothing here presumes its outcome. Net effect: the epic is
**CWN-only in practice**, and the WWN/AWN material above is *candidate* material pending ledger
entries — which is why the family is described as one engine rather than treated as four available
sources.

## 5. Licensing

> **CORRECTED 2026-10-25.** The first version of this section said *"CWN and SWN SRDs are usable
> under their published SRD terms"*, which is **wrong for SWN** and contradicts this repository's
> own dated audit. The audit is not a to-do: it exists.

`data/sources/game_system_rights.json` (read by `tools/release_packaging_guard.py`, so it is not
decorative) records both sources with their evidence and access dates:

| Source | Decision in the ledger | What that permits |
| --- | --- | --- |
| **Cities Without Number SRD** (`cities-without-number-srd`) | `verified-public-domain` — **CC0**, three agreeing readings, `license_checked` 2026-10-10 | Reuse of **SRD text and mechanics**, with the scope limited to the SRD. Not the full book, not the art, not protected setting material. |
| **Stars Without Number** (`stars-without-number-srd`) | `blocked-unverified` — **not established** | **Nothing may be adapted.** No SWN SRD was located; what Sine Nomine publishes for SWN is a free **edition**, and the CWN/WWN CC0 listings do not cover it. |

Human-readable detail, same finding: `docs/sources/GAME_SYSTEM_RIGHTS.md` §"Cities Without Number
SRD — verified, CC0, and the scope is the point" and §"Stars Without Number — deliberately not
promoted". So **this epic is CWN-only in practice**: every row that says "SWN" above is either
`OMIT` (sector generation, starships, classes) or `DEFER` behind a licence that does not yet exist
(faction turn, psionics). The licensing sub-issue is **#569**; nothing here presumes its outcome.

- **Do not import full-book prose, art, protected settings or faction names.** The epic says this
  explicitly, and `docs/sources/ATTRIBUTION.md` is the place the attribution lands.
- A **licence is not selected** in this repository by an agent. Queue **D10** holds the licence pair
  and forbids agents from choosing it; a test asserts `LICENSE`/`NOTICE` do not exist.

---

## 6. The ruling this epic needs first

One decision gates items 4–9, 12, 15, 19 and every implementation step. It is **larger than D29 and
D31** because it asks whether the *implemented* chassis changes:

> **Is NoöPunk's playable kernel staying on Fate Core `4dF` (approved in #389, with six skills in
> #482), or is it being replaced by a CWN `2d6` chassis?**

**Correction of 2026-10-25 — the status quo is not one kernel, so the question above is one option
short.** Layer A (the canonical legacy rulebook, `RULEBOOK.md` + `rulebook/`) resolves on
**`1d10`** (`src/rules/core.py`, `data/rules/core.json` `_canon_revision: issue-111-d10-independent`);
layer B (the crossover) resolves on **`4dF`**. #564's "playable RPG rules" most plausibly names
layer A, so a row that offers only "stay on 4dF or move to 2d6" can be answered without ever
mentioning the kernel the epic is about. The four honest options are therefore
**1d10 (A) / 4dF (B) / 2d6 (CWN) / two kernels + one conversion appendix**, and **which layer #564
governs is #566's question**, which this section must not pre-answer.

- **Stay on 4dF** — then #564's CWN material enters as *adjudication procedures* (Shock, Trauma,
  access prerequisites, morale, saves) over the existing kernel, and the epic is largely a rules
  appendix plus subsystem issues. Cheapest, preserves every landed test, and matches D31's
  recommendation.
- **Move to 2d6** — then #564 supersedes #389/#482 and D31 option D, the Fate kernel becomes legacy,
  its tests are retired, and `strategy_game/RULEBOOK.md` is rewritten. This is the most expensive
  reversal on the board and needs the author's word in his own words.
- **Two kernels, one appendix** — D29's option (c) extended to dice: legacy `1d10`, crossover `4dF`,
  CWN as a third conversion source. Legible, and the least coherent as a product.

A secondary answer is needed for §3.2: **does "the present 3d6 core-check model" mean attribute
generation, or a third kernel?**

**Effect of the four-book extension on this choice (2026-10-25).** The `2d6` option is no longer
"CWN's engine": CWN, SWN, WWN and AWN are **one chassis with per-book extensions**, so adopting it is
adopting a single engine that already spans cyberpunk, space, fantasy and post-apocalypse — the same
range NoöPunk's own setting crosses (cities, crisis infrastructure, NHI contact). That makes it a
*coherent* option rather than a patchwork, which is the strongest argument the extension adds. It does
not change the price: the Fate `4dF` kernel stays **approved** until it is explicitly overruled, and
the extension's rows 25–29 are all gated on this answer and on D36/D40.

## 7. Proposed sub-issues

The epic asks for these explicitly, and they are separable. Each is small enough to review.

1. **#564-a — Kernel ruling record.** Land the answer to §6 in the decision queue and in
   `strategy_game/RULEBOOK.md`'s baseline line. Nothing else can start first. *(blocks all others)*
2. **#564-b — Damage adjudication: Shock and Trauma.** Express CWN's Shock/Trauma as injury
   adjudication over the surviving kernel, paired with the approved consequence ladder; no new
   damage numbers until D34/D35 answer.
3. **#564-c — Access-gated hacking.** Adopt CWN's prerequisite structure (physical or credentialed
   access before the check) into `ISSUE_222_CYBERSPACE_SCOPE.md`'s model.
4. **#564-d — Saves and morale.** Named saves and NPC morale/reaction, expressed in the surviving
   kernel's arithmetic.
5. **#564-e — Cyberware capacity.** Answer D36 and, if the answer is a limit, express it with CWN's
   System Strain *shape*.
6. **#564-f — Tabletop vertical slice.** A self-contained quickstart + character sheet + one worked
   investigation→hacking→PSI→combat loop, **after** 1–5. This is the epic's step 3 and it is author-
   reviewed, not tested (issue #271: tests are for executable code only).
7. **#564-g — Scenario migration.** Helsinki/UNSA and Ubiquitous Maniacs under the unified engine,
   with the legacy boundary documented. Epic step 5; depends on 6.

---

## 8. What this record does not do

- It does **not** choose a chassis, a dice convention, a damage model or a capacity limit.
- It does **not** approve a mechanic, and Gates A–D stay open.
- It does **not** claim #19 established CWN as a chassis, because the repository does not support
  that reading (§3.3).
- It does **not** edit `RULEBOOK.md`, `strategy_game/RULEBOOK.md`, or any rulebook section. Those are
  author-owned and, for the legacy file, canonical.

## 9. Author rulings (2026-10-25)

Three rulings from the author settle the character of the conversion. Recorded in full in
`docs/CWN_CHASSIS.md`; this section is the pointer so the matrix cannot be read as still-open advice.

1. **Hacking runs on a ubiquitous network.** Access is **not** the scarce thing, and no CWN-style
   reachability model is imported. `strategy_game/cyber.py` decides reachability *before* any check,
   and that ordering is canonical. **Row 12 is thereby corrected**: CWN's access-prerequisite
   structure is *not* adopted, and CWN supplies only the resolution procedure.
2. **PSI = SWN's rules, for a learnable natural human ability.** **Row 21 (Effort) moves from
   "leading candidate" to ADOPT.** The ontology stays NoöPunk's: natural, learnable, open to anyone —
   not a virus, not an implant, not a class feature.
3. **Where the family has no equivalent, author a NoöPunk-native subsystem.** The default for
   Noösphere/cross-domain state, psychotronics, NHI contact, AGI/ASI and crisis-era network topology
   is a new subsystem with its own spec, not prose and not a forced conversion row.

**Scope ruling:** #564 governs **layer A only**; `1d10` stays (#111), `4dF` stays for the crossover
(#389/#482). The 2d6 reversal is *not* taken — it would have touched 80 `1d10` sites across 41 files
plus 41 test files.

Gates A–D remain open. No number is approved by these rulings.
