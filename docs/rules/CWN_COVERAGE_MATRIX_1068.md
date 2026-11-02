# CWN coverage matrix (#1068)

**Measured against the CWN SRD** (cwn.quadrifons.com, cached locally) and the Python rules library
(`src/rules/`, `mud/nopunk_mud/`).

## How to read this, and what it is not

Status is **presence of an implementation and of tests**, established by module inventory plus a keyword audit of
all **118 SRD subsections**. It is **not** a formula-level fidelity audit: a module can exist and still round the
wrong way. The fidelity pass is the next job, and it has to be done subsystem by subsystem against the SRD text.

The first pass I ran reported "30/30 complete" and was worthless — it mapped only chapters 1–4 and asked whether
a filename contained a matching word. The second pass covered all six chapters and found a whole chapter missing.

## Chapters 1–5 — implementation present

| Chapter | Modules | Tests |
| --- | --- | --- |
| 1.1 Attributes · 1.2 Skills · 1.7 Final creation | `cwn_core`, `cwn_character`, `field_agent` | yes |
| 1.3 Backgrounds · 1.5 Edges · 1.6 Foci | `cwn_backgrounds`, `cwn_edges_foci`, `cwn_foci` | yes |
| 1.4 Contacts | `social`, `party` | yes |
| 2.1 Time · 2.7 Advancement | `cwn_mission_time`, `cwn_initiative`, `cwn_advancement` | yes |
| 2.2 Saves · 2.3 Checks · 2.4 Combat | `cwn_core`, `cwn_combat`, `cwn_combat_actions`, `cwn_attack_modifiers`, `cwn_trauma` | yes |
| 2.5 Injury, healing, strain | `cwn_healing`, `cwn_strain`, `cwn_major_injury`, `cwn_injury_procedure` | yes |
| 2.6 Chases · 3.9 Vehicles | `cwn_vehicles` | yes |
| 2.8 Crafting · 2.9 Encumbrance | `cwn_gear_mods`, `cwn_encumbrance` | yes |
| 3.1–3.4 Gear, armour, weapons | `cwn_equipment`, `equipment_catalog_index` | yes |
| 3.5 Drugs · 3.6 Cyberware · 3.7 Cyberdecks | `cwn_healing`, `cwn_cyberware`, `cwn_hacking`, `cwn_program_catalogue` | yes |
| 3.8 Drones | `cwn_drones` | yes |
| 4.1–4.5 Cyberspace, hacking, programs, demons, networks | `cwn_hacking`, `cwn_program_catalogue`, `ubiquitous_network` | yes |
| 5.1–5.6 Reactions, morale, animals, guards, gangs, hackers/pilots | `cwn_npcs` | yes |

## Chapter 6 — the chapter that was missing

The audit found `summon`, `spirit`, `spellcasting` and `graced` **zero times** in the rules library.

| Section | Status | Evidence |
| --- | --- | --- |
| **6.2.0 Summoners and Summoning** | **implemented now** (core) | `src/rules/cwn_summoning.py`, 11 tests |
| 6.2.1 Summoner Effort pool | missing | pool is an input to the module, not derived |
| 6.2.8 Spirit powers catalogue | missing | powers are free-text names today |
| **6.1.0 Mages and Spellcasting** | **missing** | no module |
| **6.3.0 The Graced** | **missing** | no module |
| **6.4.0 Magical Items** | **missing** | no module |

### What 6.2 implements, and why these were the lines to hold

- Effort cost = powers − Summon skill, **floored at 1**, **+1 per earlier summon in the scene**
- Total spirit HD at once ≤ character level
- Form tiers unlock at **1st / 5th / 9th**
- Commanding at **9 / 11 / 13** by how contrary the order is
- Banishing: opposed Cha/Summon, **1d8 per Summon skill level**, and an uncontrolled spirit is targeted at its
  skill bonus **+2**
- Dispel on the summoner's death; a spirit at 0 HP vanishes
- The published manifestation table, with spirit forms unable to harm creatures directly

Two rules were written *against* the temptation to simplify: the Effort floor (a high Summon skill can never make
a summon free) and the successive-summon surcharge (three quick summons cost 1, 2, 3 — not 1, 1, 1).

## Tabletop rulebook

There is **no standalone CWN tabletop rulebook document** in this repository. The matrix above proves the software
side only. For tabletop parity — the second half of #1068 — each row needs a documented procedure a group can run
with pencils and dice, and the mods must stay visibly separate from the core. That work has not been done.

## Next, in order

1. **Fidelity pass** on chapters 1–5: verify formulas against SRD text, subsystem by subsystem, and record each
   as verified rather than assumed.
2. **6.1 mages and spellcasting**, then **6.3 Graced**, then **6.4 magical items** — same treatment as 6.2.
3. **6.2.1 Effort pool** and **6.2.8 power catalogue** transcribed from the SRD.
4. **Tabletop rulebook sections** for every row, and a rule that a rule change moves its matrix row in the same
   pull request (#1054).
