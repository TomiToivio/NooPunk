# Issue #747 — NoöPunk as a CWN/SWN reskin: the disposition matrix, re-derived

> **Status: decision support, not rules.** This file classifies every subsystem against the
> **current** baseline and leaves the classification of each row to the author. It authors no
> mechanic, changes no number, and approves nothing. Authority remains
> [`rulebook/WITHOUT_NUMBER_BASELINE.md`](../../rulebook/WITHOUT_NUMBER_BASELINE.md) and `AGENTS.md`.

**Measured on:** `origin/main` = `263acf9` (30 Oct 2026). **Python:** 1452 tests OK. **Godot 4.7.2:**
239 slice checks + 264 rule checks, 0 failures.

---

## 1. Why this replaces the old matrix rather than extending it

`docs/design/ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` holds a 24-row disposition matrix built on
2026-10-25. **On 2026-10-26 the author replaced the baseline it measured against.** The rows
therefore classify the right subsystems against the wrong engine:

| row | what it concluded | why it no longer holds |
| --- | --- | --- |
| 1 Attributes | **OMIT** CWN's six — "NoöPunk's six are FIT/REF/INT/SOC/PSY/CYB" | the six are `STR/DEX/CON/INT/WIS/CHA` (§2), and `CYB`/`PSY` fold into `INT`/`WIS` (§5) |
| 4 Core resolution | **DEFER** — "this is *the* decision" | decided: `2d6 + modifier + rank`, ladder 6/8/10/12/14 (§4) |
| 7 Combat | **OMIT (layer A)** — Shock "already exists in shape" | CWN Shock/Trauma/action economy adopted (§6) |
| 10 Armour | **OMIT armour-as-reduction** — "a ladder step, never a subtraction" | CWN armour adopted; the ladder belongs to the retired kernel |
| 14 Creation | "the **class** is forbidden" | CWN operator, Edges and Foci adopted (§5) |
| 15 Advancement | **DEFER** — "the epic forbids levels" | CWN advancement adopted (§5) |

Its measurements stand and remain worth reading; its **verdicts do not**. The honest summary is that
the epic was written for a different game, the game changed, and **almost every row now defaults to
AS-IS** — which is precisely the classification this issue asks for.

Related superseded carriers, all now bannered in this PR or already bannered in place:
`docs/CWN_CHASSIS.md` (its own "SUPERSEDED 2026-10-26" section), `docs/RPG_CHASSIS_INVENTORY.md`,
`docs/rules/RULES_FOUNDATION_POLICY.md`, `docs/rules/ISSUE_564_FOUR_BOOK_TABLETOP_PROCEDURES.md`,
`rulebook/00_START_HERE.md` (header banner, but its line 10 still contradicted it until this PR).

---

## 2. The five verdicts, and the one rule that keeps them honest

| verdict | means |
| --- | --- |
| **AS-IS** | the source procedure **is** the rule. NoöPunk adds no text to it. This is the default and should be most rows. |
| **RESKIN** | the procedure is unchanged; only what a player *reads* changes (names, labels, flavour). Never an identifier, never a number. |
| **MINOR-MOD** | NoöPunk deliberately departs from the source in a way that changes play. Requires (a) the source rule, (b) the existing NoöPunk ruling that forces it, (c) the file where it lives. |
| **OPTIONAL-NEW** | a NoöPunk-native module the source does not cover. Independently switchable; never a replacement for the core engine. |
| **DEFER** | the question is open. **DEFER is not a decision to keep the source.** |

Rules applied to every row below:

1. **No new number.** A MINOR-MOD row without an author ruling or a measurement stays DEFER.
2. **Licence first.** CWN and WWN SRD text is **CC0**; `SWN` and `AWN` have **no verified SRD**
   (`docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`), so they contribute *shape only* — no text,
   no power names, no tables.
3. **The author column ships empty.** This is a marking sheet, not a ruling.
4. `playtest` is `—` on every row because **no tabletop playtest of the overlay has been run yet**.
   That column is the reason the issue exists; it is not a column to fill in by guessing.

---

## 3. The matrix

`impl` = the Python implementation of record; `tests` = the count in its test file. Godot status is
what the engine can do **today** (after #749's slice landed).

| # | subsystem | source · licence | impl · tests | verdict | proposed delta | tabletop impact | digital impact | author | playtest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Attributes: six, 3–18, −2…+2 | CWN `character-creation/attributes` · CC0 | `cwn_character.py` · 19 | **AS-IS** | none | none | kernel ✓ (`cwn_rules.gd`) | | — |
| 2 | Attribute generation (3d6 in order + one 14, or 14/12/11/10/9/7) | CWN · CC0; baseline §2 | `cwn_character.py` · 19 | **AS-IS** | none; the array is an option, not a variant | none | ✗ no creation UI | | — |
| 3 | Skills: 19 skills, rank 0–4, untrained −1 | CWN `character-creation/skills` · CC0 | `wn_core.py` · 19 + 32 contract | **AS-IS** | none | none | kernel ✓ | | — |
| 4 | Task resolution: `2d6 + mod + rank` vs 6/8/10/12/14 | CWN `rules-of-the-game/skill-checks` · CC0 | `wn_core.py` · 19 | **AS-IS** | none | none | ✓ (`rules_adapter.gd`) | | — |
| 5 | Opposed checks, assistance (+1 max), circumstances (±2) | CWN · CC0 | `wn_core.py` · 19 | **AS-IS** | none | none | ✓ | | — |
| 6 | Saves: `16 − level − best mod`, nat 1/20 | CWN `saving-throws` · CC0 | `wn_core.py` · 17 | **AS-IS** | none | none | ✓ | | — |
| 7 | Attacks: `1d20 + bonus + mod + rank` vs Melee/Ranged AC | CWN `attacks-in-combat` · CC0 | `cwn_combat.py` · 6, `cwn_attack_modifiers.py` · 10 | **AS-IS** | none | none | total ✓; modifiers ✗ | | — |
| 8 | Initiative, rounds, Move + Main, On Turn, Instant | CWN `combat/` · CC0 | `cwn_combat_actions.py` · 16 | **AS-IS** | none | none | partial (`combat.gd`, #755) | | — |
| 9 | Damage, Shock, Trauma die/rating, mortal wounds | CWN `damage-trauma-shock` · CC0 | `cwn_core.py` · 47, `cwn_trauma.py` · 21 | **AS-IS** | none | none | ✗ in Godot | | — |
| 10 | Healing, first aid, stabilization, Frail | CWN · CC0 | `cwn_healing.py` · 28, `cwn_injury_procedure.py` · 15, `cwn_major_injury.py` · 14 | **AS-IS** | none | none | partial | | — |
| 11 | System Strain | CWN `system-strain` · CC0 | `cwn_strain.py` · 18 | **AS-IS** | none. It is the capacity track (D36 answered in kind by the baseline) | none | partial | | — |
| 12 | Gear, armour, encumbrance, prices | CWN `gear` · CC0 | `cwn_equipment.py` · 11, `cwn_encumbrance.py` · 13, `data/rules/cwn_equipment.json` | **AS-IS** | none | none | ✗ (data, no reader) | | — |
| 13 | Mods, crafting, maintenance, +3 cap | CWN `crafting` · CC0 | `cwn_gear_mods.py` · 35 | **AS-IS** | none | none | ✗ | | — |
| 14 | Vehicles, vehicle combat, chases | CWN `vehicles` · CC0 | `cwn_vehicles.py` · 41 | **AS-IS** | **optional module**: runs only when a scenario needs it | none | ✗ | | — |
| 15 | Cyberware: cost, Strain, alienation | CWN `cyberware` · CC0 | `cwn_strain.py` · 18 | **AS-IS** | none. `CYB` is not an attribute (D54) — the source already agrees: Strain is the limit | none | ✗ | | — |
| 16 | **Hacking: access model** | CWN `hacking/cyberspace-basics/#access` · CC0 | `cwn_hacking.py` · 16, `ubiquitous_network.py` (D41) | **MINOR-MOD — the one real disagreement** | see §4.1: the 2026-10-25 ruling said access is ambient; baseline §6 says "access and reachability first". Both are on record and they conflict | large: it decides whether reachability is a scene | `hacking.gd` (#755) implements a reach→access→program→trace chain with **calibrated numbers** | | — |
| 17 | Hacking: Access pool, Security 7–10/12, connection penalties, Alert clock | CWN `hacking-mechanics/` · CC0 | `cwn_hacking.py` · 16 | **AS-IS** | none; the Verb catalogue stays scenario data (nothing author-ruled exists) | none | ✗ rules not ported; #752 | | — |
| 18 | Drones | CWN `drones` · CC0 | `cwn_drones.py` · 18 | **AS-IS** | optional module | none | ✗ | | — |
| 19 | PSI: disciplines, Effort, techniques, prerequisites | **SWN Revised** · `blocked-unverified` — shape only | `swn_psionics.py` · 5, `psionics.py`, `swn_progression.py` · 4 | **AS-IS (mechanics) + RESKIN (ontology)** | NoöPunk keeps PSI as a **learnable natural human capacity**; SWN's rarity/class-exclusivity is explicitly not imported. Technique names are NoöPunk-authored (`data/rules/psionics_techniques.json`, file-level `is_canonical: false`) | one: who may learn it | pool + gate ✓; technique catalogue partial | | — |
| 20 | Starships, space travel, space combat | SWN · shape only | `swn_starships.py` · 4, `swn_sector.py` | **AS-IS (procedure), OPTIONAL (scope)** | activate only for a scenario that leaves Earth | none | ✗ | | — |
| 21 | Factions and faction turns | SWN · shape only | `swn_faction_turn.py`, `swn_faction_operations.py` · 5 | **OPTIONAL — separate layer** | stays the strategy game's (`strategy_game/`), not the legacy RPG's. One faction system, never two | boundary rule | ✗ | | — |
| 22 | NPCs, morale, reaction, missions | CWN NPC/mission · CC0 (mirror omits *Antagonists*) | — no module; `first_case_drill.py` · 27 names the convention | **AS-IS** | stat-line convention only, no hit dice | none | partial | | — |
| 23 | Survival, supplies, hazards, settlements | **AWN** · no verified CC0 | `awn_survival.py`, `data/rules/awn_survival.json` | **AS-IS (shape), OPTIONAL (scope)** | local conditions feed the same HP/saves; no second wound economy | none | ✗ | | — |
| 24 | Otherworld exploration, major projects | **WWN SRD** · CC0 | `wwn_projects.py` | **AS-IS (procedure), OPTIONAL (scope)** | one expedition clock per expedition; no duplicate progress with the faction turn | none | ✗ | | — |
| 25 | **Investigation: core clues are not rolled** | CWN has no such subsystem · NoöPunk native (#704) | `investigation.py` · 17, `investigation_evidence.py` · 11, `case_graph` · 21 | **OPTIONAL-NEW (the issue's own GUMSHOE ask)** | clues are obtained by access + approach + competence; dice decide risk, time, exposure and extra insight. No parallel investigative skill, no replacement dice | large, and it is already canon-adjacent | ✓ (`investigation_adapter.gd`) | | — |
| 26 | **Narrative layer: aspects, compels, clocks** | NoöPunk native (#689) · — | `narrative_layer.py`, `narrative_moves.json`, `rulebook/19_NARRATIVE_LAYER.md` | **OPTIONAL-NEW** | one invoke per roll, never stacking; aspects never a fixed "+X" without naming the difficulty; clocks only, no PbtA moves; Fate is retired as a **kernel**, kept as **vocabulary** | medium | ✗ | | — |
| 27 | **Noetic / anomalous effects** | NoöPunk native + WWN shape | `rulebook/17`, `21`; `anomaly_gate.py` | **OPTIONAL-NEW** | SWN PSI first; WWN only when explicitly selected; never spell access through ordinary skills | medium | ✗ | | — |
| 28 | AGI, NHI, BCI, identity, consciousness | NoöPunk native (baseline §6, last row) | lore + `swn_transhuman.py`, `swn_true_ai.py` | **OPTIONAL-NEW** | **no** universal intelligence, consciousness or identity meter | large | ✗ | | — |
| 29 | Attribute **presentation** (labels only) | — | D51 (provisional) | **RESKIN — deferred as its own work item** | Might / Reflexes / Vitality / Intellect / Psyche / Presence as *display* aliases; `STR…CHA` stay the identifiers in data, saves and rules text | none mechanically; tone only | none if codes are untouched | | — |
| 30 | Skill labels, gear flavour, organisation names | — | — | **RESKIN — undecided** | a NoöPunk vocabulary pass over 2045 Nordic institutions; no mechanical name may change | tone only | none | | — |

**Reading the table as a whole.** 21 of 30 rows are AS-IS or AS-IS-with-optional-scope. That is the
answer to "is NoöPunk a reskin?": **the engine is the source's**, four modules are NoöPunk-native
and independently switchable, one row is a genuine disagreement, and two rows are cosmetic and
undecided.

---

## 4. Where the repository still contradicts itself

### 4.1 The hacking access model — the one load-bearing conflict (row 16)

Two author rulings are both on record and they point opposite ways:

| ruling | says |
| --- | --- |
| #566, 2026-10-25 (`docs/CWN_CHASSIS.md`, "Three further author rulings" §1) | *"CWN's matrix-like reachability **is not adopted**. NoöPunk's assumption stands: the network is ambient, so **access is not the scarce thing**."* |
| `WITHOUT_NUMBER_BASELINE.md` §6, 2026-10-26 | *"Hacking, programs, decks, security, drones — **Access and reachability first**, then the actual source procedure."* |

Both are in canon carriers, and the second is the later document but does not mention reversing the
first. This is not a documentation nit: it decides whether a hack scene begins with "can you reach
it?" or with "you are already inside; what does it cost you?" — which is also the difference between
`cwn_hacking.py`'s reachability preconditions and `ubiquitous_network.py`'s exposure economy.

**It is an author question, queued as D55 below, and it gates #752.** Nothing in this PR resolves
it; #752 must not ship a hacking screen that silently picks a side.

### 4.2 Statements that were true yesterday

Fixed in this PR:

- `rulebook/00_START_HERE.md:10` still said *"**The resolution formula is UNDECIDED.**"* under a
  header banner saying the opposite. Rewritten to point at the baseline.
- `docs/rules/WN_BASE_SYSTEM.md` §"migration queue" listed **M1 action economy, M3 System Strain, M7
  generation, M8 advancement** as *author decisions*. The 2026-10-26 baseline settled all four in
  favour of the source (§2 generation, §5 advancement, §6 cyberware/Strain and action costs). What
  remains open for them is **porting**, not deciding. The queue now says so.

Bannered in this PR (their verdicts are superseded; their measurements are not):

- `docs/design/ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md`
- `docs/rules/SWN_CHAPTER_CONVERSION_MATRIX.md`
- `docs/RPG_CHASSIS_INVENTORY.md`

Noted, deliberately **not** fixed here:

- `rulebook/00_INDEX.md`'s "Per-domain detail chapters" list is partial and unsorted (it omits 10,
  11, 12, 13, 14, 15, 18, 19, 20 and 23, and lists 24 before 22). Touching it is a separate editorial
  pass; folding it into this PR would hide a real staleness inside an unrelated change.
- `docs/design/ISSUE_516_REFERENCE_MATRIX.md:52` quotes the old "dice not yet chosen" position as
  history. That is correct in context; it is only listed so a later grep does not re-open it.

---

## 5. Author decisions this matrix creates (queued, never answered here)

Highest existing row is **D54**. These are appended to
`docs/design/AUTHOR_DECISION_QUEUE.md`:

| # | question | blocks |
| --- | --- | --- |
| **D55** | **The access model**: is the network ambient (access is not scarce; the scene is about cost, exposure and consequences) or is reachability a prerequisite (access is the first question)? #566 says ambient; the 2026-10-26 baseline §6 says reachability first. | #752's hacking screen; `cwn_hacking.py` vs `ubiquitous_network.py`; every intrusion scene |
| **D56** | **The reskin pass**: adopt the display aliases of D51 (Might / Reflexes / Vitality / Intellect / Psyche / Presence) and a NoöPunk vocabulary for skills and gear, with `STR…CHA` staying the identifiers — or keep the source vocabulary everywhere? | rows 29–30; any naming work; sheet labels |
| **D57** | **Which MINOR-MOD rows are approved**: today only row 16 exists, and it is not a proposal but a contradiction between two rulings. Approve a departure, or close the row as AS-IS and keep the source? | the overlay document (`rulebook/NOOPUNK_WN_OVERLAY.md`); any future deviation |

---

## 6. Verification and what this does not claim

What was checked: every `impl` path exists on `main`; every test count is the number of `def test_`
in that file; the four suites in §1 pass on the pinned engine; every relative link in the touched
documents resolves; the diff is insertions plus the one false sentence that had to change.

What this does **not** claim:

- it does not claim CWN/SWN coverage — most AS-IS rows are implemented in Python and **absent in
  Godot**, and §4 of #749's coverage matrix is where that gap is measured;
- it does not approve a single MINOR-MOD, including row 16;
- it does not playtest anything, and the `playtest` column stays empty until a tabletop session of
  the overlay runs;
- it does not decide D55–D57. Those are the author's, and answering one turns it into an acceptance
  record, a PR and a close.
