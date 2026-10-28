# #704 — audit, system influence matrix, licensing, attribute crosswalk

**Status:** design proposal for author review. Changes no rule, no schema and no code. Every licensing
statement is a finding from a document read on 2026-10-28, not an assumption; anything I could not
verify is marked **to verify**.

---

## 1. What the audit actually found

The first deliverable of #704 is an audit, and the audit's main result is uncomfortable: **the
repository currently carries two rule generations side by side, and the older one is still the one the
code reads.**

### 1.1 The governing rule text

`rulebook/WITHOUT_NUMBER_BASELINE.md` records the author decision of **26 October 2026** — *"For
beginning, use CWN/SWN/AWN/WWN system for everything. Make the stats, skills, all rules based on them.
We will modify later."* It declares itself the authoritative entry point and **supersedes earlier
numeric rules**, and `rulebook/NEW_EDITION.md` carries a banner saying the same.

Under that baseline:

- attributes are the CWN six — **STR, DEX, CON, INT, WIS, CHA**, on a **3–18** scale, modifier
  `−2 / −1 / 0 / +1 / +2` by band;
- the WN family is the default engine, with CWN settling overlapping general rules;
- NoöPunk's Physical / Social / Psychic / Cybernetic **describe the setting and do not supply extra
  character attributes** — the baseline says this in as many words.

### 1.2 What the software still contains

`data/rules/core.json` is still the superseded model:

| field | value in core.json | status under baseline v1 |
|---|---|---|
| `stats.final_list` | FIT, REF, INT, SOC, CYB, PSY (1–10) | superseded vocabulary |
| `skill_check` | `1d10 + STAT + Skill` vs 9–29 | superseded resolution |
| `skills.final_list` | 40 NoöPunk skills | superseded list |
| `stats._note` | "locked by author direction on issue #131 (2026-10-05)" | locked *then*, superseded **after** (26 Oct) |

The baseline document anticipates exactly this: *"existing software still requires migration."* So this
is not a contradiction to be resolved by picking a side — it is a **known, declared migration debt**.
It matters for #704 because any investigative mechanic I write against `core.json` would be written
against a superseded engine.

### 1.3 What is implemented, and where

| area | file | state |
|---|---|---|
| saves, Trauma, Shock, first aid | `src/rules/cwn_core.py` | implemented, SRD-cited |
| System Strain, cyberware install | `src/rules/cwn_strain.py` | implemented |
| major injuries | `src/rules/cwn_major_injury.py` | implemented |
| injury procedure | `src/rules/cwn_injury_procedure.py` | implemented |
| hacking | `src/rules/cwn_hacking.py` | implemented |
| advancement | `src/rules/cwn_advancement.py` | implemented |
| healing | `src/rules/cwn_healing.py` | implemented |
| drones | `src/rules/cwn_drones.py` | implemented |
| Foci | `src/rules/cwn_foci.py` | implemented (engine, not catalogue) |
| mental load / world view | `src/rules/mental_load.py` | implemented (#698) |
| narrative bands | `src/rules/narrative_layer.py` | implemented, 2d6 bands |
| **investigation** | — | **absent** (this issue) |
| **vehicles** | — | absent |
| **psionics (SWN)** | — | absent |

`strategy_game/` is the separate crossover game with its own rules layer; its `rpg/fate.py` is a
legacy 4dF prototype explicitly marked as such and is **not** an exception to the WN direction.
Investigation is not implemented anywhere, in tabletop or in Godot.

### 1.4 The one audit finding that needs the author

`core.json` and the baseline disagree on **dice, attribute scale and skill list** simultaneously. Until
that migration lands, every new module has to choose which generation it speaks. This proposal speaks
**baseline v1** (2d6, CWN six, 3–18) and touches `core.json` not at all, because that file's migration
is a decision with its own blast radius (sheets, NPCs, Godot, the 40 skills).

---

## 2. System influence matrix

| system | role | retain / adapt / optional / reject | boundary that keeps it from becoming a second engine | licence provenance |
|---|---|---|---|---|
| **CWN** | primary engine: character, skills, combat, gear, cyberware, hacking, missions, difficulty | **retain** | — | SRD **CC0**, verified in `data/sources/game_system_rights.json` |
| **SWN** | psionics: disciplines, techniques, Effort | **adapt** | Effort is spent inside the existing skill-check economy; no second resolution die; psychic *detection* produces clues, never conclusions | SRD **blocked-unverified** in the registry — design reference only, no text |
| **WWN** | exploration, factions, **major projects** | **adapt (selective)** | projects are the only clock-like structure allowed to gate long work; they do not replace skill checks | SRD **CC0**, verified |
| **AWN** | survival, scarcity, hazards, aftermath | **optional** | used only where a scenario calls for it; not compulsory bookkeeping | **blocked-unverified** in the registry — design reference only |
| **Eclipse Phase** | forks, resleeving, synthetic minds, ontological questions | **adapt ideas only** | no mechanical import; no proprietary text or tables | **proprietary** — out of scope for text reuse |
| **GUMSHOE** | investigation: core clues, investigative vs general abilities, spends, no dead ends | **adapt (this issue)** | guarantees **finding**, never **interpretation**; every GUMSHOE gain is expressed as an existing CWN skill use, not as a new ability score | SRD **CC BY 3.0**, verified (§3) |
| **Fate** | aspects, invokes, compels | **optional thin overlay** | one invoke per roll, grants a **band** not a number; never alters world state | SRD **CC BY 3.0**, verified |
| **PbtA** | partial success, GM moves, fronts, clocks | **selective** | the base resolution stays 2d6-plus-modifier; PbtA contributes *outcome vocabulary and pacing*, not a move list that replaces checks | **no CC grant established** for Apocalypse World text — ideas only |
| **Disco Elysium / Citizen Sleeper** | psychological dialogue, motives as mechanics | **inspiration only** | no mechanical import; no text | **proprietary** — ideas only |

**Rejected outright:** any proposal that makes investigation a single "roll to find the clue" check
(GUMSHOE exists precisely because that stalls), and any proposal that gives the psychic layer a
resolution of its own.

---

## 3. GUMSHOE licensing — what the SRD actually permits

Verified directly from **GUMSHOE SRD, Creative Commons version, 2024-12-09, 303 pages** (the URL in
#704 now returns "Multisite support not enabled"; the live file is
`https://pelgranepress.com/gumshoe/files/GUMSHOESRDCC-3%20241209.pdf`).

- **Licence:** Creative Commons **Attribution 3.0 Unported**. Adaptable with attribution; one-way
  compatible into a ShareAlike 4.0 work.
- **Required attribution**, which must sit in the same place and at the same size as NoöPunk's own
  copyright notice, in this wording:

  > "This work is based on the GUMSHOE SRD (found at
  > https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/), a product of Pelgrane
  > Press, developed, written, and edited by Robin D. Laws with additional material by Kenneth Hite and
  > Kevin Kulp, and licensed for our use under the Creative Commons Attribution 3.0 Unported license
  > (http://creativecommons.org/licenses/by/3.0/)."

- **Trademark:** "GUMSHOE" may be used in works produced under this licence, but never in a way that
  suggests endorsement by Pelgrane Press or Robin D. Laws. **The GUMSHOE logo may not be used.**
- **Other trademarks are NOT granted:** Esoterrorists, Mutant City Blues, Ashen Stars, Fear Itself,
  TimeWatch, Trail of Cthulhu, Night's Black Agents, Cthulhu Confidential, The Yellow King RPG. They
  may not appear in derivative works — so NoöPunk may not describe its investigation layer as
  "Trail of Cthulhu-style".
- **No SRD prose is copied into this proposal.** Sections are cited so a reader can check the claim
  against the source, exactly as the CWN modules do.
- **Vasama distinction:** a CC **BY** licence permits commercial use with attribution, unlike NoöPunk's
  own **BY-NC-SA** material. So GUMSHOE-derived mechanics are *not* automatically barred from Vasama —
  but Vasama must derive them from the SRD with its own attribution, not lift NC-licensed NoöPunk text.
- **To verify:** the exact ShareAlike interaction between BY 3.0 source material and NoöPunk's
  BY-NC-SA 4.0 collective work. My reading is that BY permits adaptation and the adaptor may license
  the adaptation more restrictively, with attribution preserved — but this is a licensing decision for
  Tomi, not something I assert.

Action: `data/sources/game_system_rights.json` gains a `gumshoe-srd` entry recording the above, because
the registry currently has **no GUMSHOE row at all** despite the system being named in #704.

---

## 4. Attribute crosswalk

### 4.1 The honest framing

#704 asks me to "explore renaming/reframing attributes" and lists **FIT/REF/INT/SOC/PSY/CYB** as an
existing candidate from #263. That candidate is **superseded**: the 26 October baseline replaced the
six NoöPunk STATs with the CWN six on a 3–18 scale, and said the four analytical layers do not supply
attributes. So the crosswalk is not a design choice between equals — it is **CWN six → NoöPunk
presentation**, plus a migration table for the superseded sheet.

### 4.2 The governing crosswalk (baseline v1)

| CWN | 3–18 | carries in NoöPunk | saves it feeds | skills it binds |
|---|---|---|---|---|
| **STR** | 3–18 | physical force, carrying, melee power | Physical | Athletics, Melee, Unarmed, Exotic |
| **DEX** | 3–18 | coordination, stealth, fine motor, shooting | Evasion | Guns, Sneak, Fray, Pilot, Free Fall |
| **CON** | 3–18 | endurance, resistance, **System Strain capacity**, cyberware tolerance | Physical | Survival, Athletics, First Aid |
| **INT** | 3–18 | reasoning, memory, technical work, forensics | Mental? *see 4.4* | Program, Hardware, Forensics, Medicine, Research, Investigation, Infosec |
| **WIS** | 3–18 | perception, judgment, resistance to deception | Mental | Perceive, Kinesics, Psychic Defence |
| **CHA** | 3–18 | presence, persuasion, command | Mental | Talk, Lead, Connect, Provoke, Deceive, Perform |

Three candidates were required. The other two are recorded as **comparisons, not options**, because the
baseline already decided:

**Candidate B — rename all six, change no number.** STR→FIT, DEX→REF, CON→TOL (tolerance), INT→INT,
WIS→PER (perception/judgment), CHA→SOC. Cost: cosmetic, but every existing document, sheet and test
that says STR/CON/CHA must be rewritten, and CWN citations become untraceable ("TOL" no longer matches
the SRD's CON). Benefit: vocabulary reads as near-future rather than fantasy. **Verdict: do not do this
while the CWN corpus is being ported** — it makes every ported rule need translation.

**Candidate C — keep six attributes, move CYB *off* the sheet.** Cybernetics is not an attribute; it is
(a) a **skill domain** (`Hardware`, `Interface`), (b) **installed state** (strain, slots, maintenance),
and (c) a set of **device statistics** (already declared: COMPUTE/INTERFACE/NETWORK are properties of
decks and implants, not people). Benefit: an unaugmented character is not mechanically deficient by
definition, which was #704's explicit worry. Cost: none mechanical; it is a clarification. **Verdict:
adopt as doctrine, and it is already the baseline's position** — recorded here because the superseded
`core.json` still lists CYB as a STAT and will mislead the next reader.

**Candidate A — verbatim CWN.** **Verdict: adopt for now.** It is what the baseline says, it keeps SRD
section citations checkable, and NoöPunk's distinctiveness lives in setting, factions and the four
analytical layers rather than in six letters.

### 4.3 What the migration touches

If `core.json` is migrated to baseline v1, these move together and must not be done piecemeal:

| surface | from | to |
|---|---|---|
| dice | `1d10 + STAT + Skill` | `2d6 + modifier + skill` |
| attribute scale | 1–10 | 3–18, modifier bands |
| attribute names | FIT/REF/INT/SOC/CYB/PSY | STR/DEX/CON/INT/WIS/CHA |
| skill list | 40 NoöPunk skills | CWN skill list (+ NoöPunk additions as declared extras) |
| saves | Physical/Evasion/Mental/Luck | CWN saves (already implemented in `cwn_core.py`) |
| derived | HP, strain capacity (CON), shock/trauma | recompute from CWN |
| consumers | `src/rules/*`, sheets, NPCs, Godot, tests, `strategy_game` adapters | re-verify |

`cwn_core.py` already implements the destination saves; `core.json` is the lagging side. That is the
whole migration.

### 4.4 One open question for the author

CWN's saves are **Physical (STR/CON), Evasion (DEX/INT), Mental (WIS/CHA)**. That mapping puts **INT**
in Evasion, which is unintuitive for a forensics-heavy investigator and may want a NoöPunk ruling later.
It is not blocking the investigation layer, and I have not changed it.

---

## 5. What this document does not do

It does not migrate `core.json`, does not name new attributes as canon, does not import GUMSHOE or any
other text, and does not close #704 — the issue's own instruction is that it stays open until decisions
and follow-up tracking are documented, and the playtest and Godot-regression criteria are not mine to
declare satisfied.
