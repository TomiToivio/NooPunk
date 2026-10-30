# CWN/SWN reskin inventory (#747)

**Status:** proposal, not canon. Every row awaits the author's ruling. The rule that governs it
(`AGENTS.md`, `rulebook/WITHOUT_NUMBER_BASELINE.md`): CWN is the chassis, SWN supplies psionics, and no
reskin may change a procedure without saying so.

Vocabulary used below:

- **as-is** — the rule runs exactly as published; the setting renames nothing that affects play.
- **reskin** — the same numbers, dice and economy, with NoöPunk fiction and names on top.
- **change** — a genuine mechanical delta, which must be justified, minimal, and carry a consequence.

What already exists (measured): **20 CWN modules, 413 tests**, plus three psionics modules — so most of
this inventory is about *naming and emphasis*, not implementation.

## 1. Character and progression

| Subsystem | Source | In repo | Proposal | Why |
|---|---|---|---|---|
| Six attributes (STR/DEX/CON/INT/WIS/CHA) | CWN 1.1 | `cwn_core.py` | **as-is** | The baseline already forbids stat renames; six stats stay six stats. |
| Background packages | CWN 1.3 | `cwn_backgrounds.py` | **reskin** | Keep the package mechanics; write NoöPunk backgrounds (UNSA analyst, psychotronic technician, street fixer) using the same shape. |
| Edges and foci | CWN 1.4–1.5 | `cwn_edges_foci.py`, `cwn_foci.py` | **as-is** mechanics, **reskin** names | Foci are the crunch players read first; renaming them badly is worse than leaving them. Only a handful need NoöPunk names. |
| Skills | CWN 1.2 | `data/rules/skills.json` | **as-is** | Adding `Psychotronics` as a *new* skill is a change, not a reskin — see §5. |
| Advancement | CWN 1.6 | `cwn_advancement.py` | **as-is** | |

## 2. Resolution

| Subsystem | Source | In repo | Proposal | Why |
|---|---|---|---|---|
| 2d6 skill checks vs difficulty | CWN 2.1 | `cwn_core.py` | **as-is** | Never touch. |
| Saves | CWN 2.2 | `cwn_core.py` | **as-is** | |
| d20 attacks vs AC | CWN 2.3 | `cwn_combat.py` | **as-is** | "Two ACs" (melee/ranged) is vanilla CWN, not a NoöPunk invention. |
| Trauma and major injury | CWN 2.4 | `cwn_trauma.py`, `cwn_major_injury.py` | **as-is** | |
| System Strain | CWN 3.6 | `cwn_strain.py` | **as-is** | |

## 3. Gear and cyberware

| Subsystem | Source | In repo | Proposal | Why |
|---|---|---|---|---|
| Equipment catalogue, encumbrance | CWN 3.1–3.3 | `cwn_equipment.py`, `cwn_encumbrance.py` | **as-is** | Invented gear is explicitly disallowed by #751. |
| Cyberware and mods | CWN 3.6 | `cwn_gear_mods.py` | **reskin** fiction only | The catalogue stays; NoöPunk adds *brands*, not new effects. |
| Drones, vehicles | CWN 3.8, 3.9 | `cwn_drones.py`, `cwn_vehicles.py` | **as-is** | |

## 4. Hacking

| Subsystem | Source | In repo | Proposal | Why |
|---|---|---|---|---|
| Access pool, security ladder, connection penalties, alert clock | CWN 4.2–4.3 | `cwn_hacking.py` | **as-is** | Already transcribed with citations. |
| Verbs, Subjects, programs, CPU slots | CWN 4.3.2–4.3.4 | **absent** | **as-is once transcribed** | #752's blocker. Do not invent a "trace die" or a two-action minigame: the SRD has an action economy already. |
| NoöPunk flavour | — | — | **reskin** node names only | The network graph is scenario state, not a rules object. |

## 5. The only places a *change* is tempting, and the cost of taking them

| Tempting change | If adopted | Consequence |
|---|---|---|
| A `Psychotronics` skill | new skill row + baseline deviation | Every published check, focus and background that references Program/Know would need an alternative; the change must be recorded in `WITHOUT_NUMBER_BASELINE.md`, not slipped in. |
| PSI as a seventh attribute or a save | replaces SWN's Effort economy | Breaks the one thing SWN psionics does well, and Romppainen must not become psychic by default (#751). Prefer SWN's Psychic/Partial Psychic classes. |
| A bespoke "Noösphere" resource track | new subsystem | Needs author ruling before implementation; the safest first version is *fiction only*. |
| A custom initiative or hacking action economy | touches the chassis | Refused by #751/#752 unless the source says otherwise. |

## 6. What this inventory is not

- It is not a ruling. Rows marked **reskin** propose fiction; the numbers stay as published until the
  author says otherwise.
- It is not a promise that every CWN chapter is implemented. The measured coverage lives in
  [`../CWN_COVERAGE_MATRIX.md`](../CWN_COVERAGE_MATRIX.md) once that lands, and the hacking catalogue is
  still absent.
- It does not resolve the SWN licensing question: SWN Revised has no verified grant in
  `data/sources/game_system_rights.json`, so psionics stays original expression, not transcription.

## 7. Suggested first reskin pass (smallest useful slice)

1. Three NoöPunk **backgrounds** built from existing packages (§1).
2. A dozen **focus names** re-skinned without touching their text mechanics.
3. **Brands** for existing cyberware and decks — names, no new effects.
4. Node names and deck naming for the hacking screen, once #752's rules land.

Nothing in that list requires a mechanical delta, which is the point.
