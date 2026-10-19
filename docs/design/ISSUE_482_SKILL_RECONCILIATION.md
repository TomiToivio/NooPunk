# #482 / #516 — Skill reconciliation: six individual skills vs the legacy attribute sheet

**Status: PROPOSAL FOR AUTHOR REVIEW.** Nothing here is approved, and nothing here replaces an approved mechanic. The six individual skills `COG / INT / REF / SAV / SOM / WIL` are the existing implementation baseline (`strategy_game/rpg/skills.py`) and remain so; the seven strategic skills are already recorded as an unapproved proposal (`strategy_game/data/strategic_skills.json`, `status: PROPOSAL`). This document does what #516 asks for explicitly: *"produce an explicit reconciliation table for #482's six currently approved skills versus earlier FIT/REF/INT/SOC/PSY/CYB suggestions and #506's single science strategic skill; propose changes rather than silently replacing approved mechanics."*

Nothing in this document is implemented as code. It is an analysis for a decision that belongs to Tomi (#516).

## Why the two sheets are not comparable

They answer different questions, and conflating them is the mistake this table exists to prevent.

| Layer | Unit | Resolution | Where it lives | Approval |
| --- | --- | --- | --- | --- |
| **Individual skills** | one character, in a scene | one Fate 4dF roll against a difficulty | `strategy_game/rpg/skills.py`, `rpg/fate.py` | **approved baseline** (six skills) |
| **Strategic skills** | one agent, one faction order per turn | mission procedure, not a die roll per order | `strategy_game/data/strategic_skills.json` | **proposal only** — no strategic skill approved |
| **PSI** | a permissioned operation with costs | `rpg/scene.py` framing + psi operation ledger | `strategy_game/psi_operations.py` | psi exists as operations, **not** as skills |
| **Equipment / competence** | a tag or a stunt on the sheet | modifies what a character may attempt | tags/stunts on the character | follows the six-skill baseline |

The legacy sheet was a **skill list keyed to six attributes** (40 skills across FIT/REF/INT/SOC/PSY/CYB). The crossover sheet is **six broad skills plus tags, stunts and a separate strategic namespace**. The reconciliation below therefore answers, for each legacy entry: *which of the six absorbs it, what recovers the lost granularity, and what remains genuinely lost.*

## Attribute-level reconciliation

| Legacy attribute | Absorbed by | What is preserved | What changes |
| --- | --- | --- | --- |
| **FIT** — bodily capability | **SOM** (Somatics: strength, stamina, movement, sustained positioning) | athletics, climbing, melee force, grappling | FIT and REF no longer split "power" from "coordination" as *attributes*; that split now lives between SOM and REF |
| **REF** — coordination and reaction | **REF** (Reflexes) | dodging, shooting, piloting, stealth movement | unchanged in meaning; no longer paired with FIT as a stat pair |
| **INT** — analysis and knowledge | **COG** (Cognition), with **INT** (Intuition) for fast judgement | investigation, research, forensics, tactics, medicine-as-procedure | the deliberate slow/deliberate split: COG is analysis, INT is the gut call. The legacy sheet had one INT doing both |
| **SOC** — social capability | **SAV** (Savvy) | persuasion, deception, leadership, trade, reading people | one social skill instead of seven rated skills; see the granularity note below |
| **PSY** — anomalous perception and psi | **split three ways**: perception → INT, defence/control → WIL, techniques → **psi operations** | psi remains a real, permissioned capability with costs | psi stops being a skill ladder. This follows the existing code: `psi_operations.py` models operations and a ledger, not skills |
| **CYB** — technology | **COG** for understanding and operation, **device tags** for capability | hacking, hardware, programming, interface | device capability becomes a descriptor (`C/I/N` per #517), not a rated character skill; access is a *path* question (#344, `cyber.py`) before it is a roll |

## Skill-level reconciliation (all 40 legacy skills)

"Tag" means a competence tag or stunt on the six-skill sheet; "strategic" means the faction-layer skill that carries the same work at mission scale.

### From INT (11)

| Legacy skill | Home | Granularity recovered by |
| --- | --- | --- |
| Administrate | COG | strategic **stewardship** for faction-scale logistics |
| Counterintelligence | COG | tag "tradecraft"; strategic **security** |
| First Aid | COG | stunt/tag "field medicine" |
| Forensics | COG | tag "forensics" |
| Intelligence Analysis | COG | strategic **inquiry** |
| Investigation | COG | explicitly in COG's Fate mapping |
| Know (Field) | COG | field tag ("Know: sociology") |
| Medicine (Field) | COG | specialty tag; a stunt for sustained care |
| Research | COG | strategic **science** / **inquiry** |
| Survival | COG | SOM for the physical endurance half |
| Tactics | COG | strategic **command** |

### From FIT (4)

| Legacy skill | Home | Granularity recovered by |
| --- | --- | --- |
| Athletics | SOM | — |
| Free Fall | SOM | tag "zero-g" |
| Melee | SOM | weapon tag; the *attack* is a Fate action, not a skill |
| Unarmed | SOM | tag "unarmed" |

### From SOC (7)

| Legacy skill | Home | Granularity recovered by |
| --- | --- | --- |
| Connect | SAV | strategic **statecraft** |
| Deceive | SAV | tag "deception" |
| Kinesics | SAV (or INT for pure observation) | tag "reads people" |
| Lead | SAV | strategic **command** |
| Provoke | SAV | tag "intimidation" |
| Talk | SAV | — |
| Trade | SAV | strategic **stewardship** |

### From REF (4)

| Legacy skill | Home | Granularity recovered by |
| --- | --- | --- |
| Fray | REF | — |
| Guns | REF | weapon tag "firearms" |
| Pilot (Field) | REF | vehicle tag ("Pilot: aircraft") |
| Sneak | REF | tag "stealth" |

### From PSY (8)

| Legacy skill | Home | Granularity recovered by |
| --- | --- | --- |
| Perceive | INT | Intuition already covers "awareness, notice" |
| Perform (Field) | SAV | performance tag |
| Psychic Defence | WIL | psi operation defence, with the ledger recording cost |
| Psychokinesis | **psi operation** | permission + cost, not a skill rating |
| Telepathy | **psi operation** | as above |
| ESP | **psi operation** | as above |
| Precognition | **psi operation** | as above |
| Noöspace | **psi operation** | as above; distinct from the noösphere-as-setting concept |

### From CYB (4)

| Legacy skill | Home | Granularity recovered by |
| --- | --- | --- |
| Hardware (Field) | COG | device tag; physical access required (#517) |
| Infosec | COG | access path first (`cyber.py`), then the roll (#517) |
| Interface | COG | device tag |
| Program | COG | tag "software" |

### Variable (2)

| Legacy skill | Home | Note |
| --- | --- | --- |
| Exotic Skill (Field) | **stunt** | an exotic capability should be a named stunt, not a new skill slot |
| Work (Field) | tag on the relevant skill | occupation as competence, strategic **stewardship** at faction scale |

## What is genuinely lost, and whether that is acceptable

Three real reductions, stated plainly rather than hidden:

1. **Combat granularity.** The legacy sheet rated Guns, Melee and Unarmed separately; the six-skill sheet has REF and SOM plus weapon tags. A character who is an expert shot and a poor knife-fighter is expressible only through tags/stunts. *Recommendation: acceptable if weapon tags are honoured at the table; otherwise one combat stunt per speciality.*
2. **Professional depth.** Medicine, Forensics and Pilot each had their own rating. They become COG or REF with a speciality tag. A surgeon and a researcher now differ by tag, not by rating. *Recommendation: acceptable for a lightweight sheet, and it is what "avoid skill-list bloat" in #516 asks for — but it should be a conscious choice.*
3. **Psi as skill.** PSI previously competed for skill points; now it is a permissioned operation. *This is a gain in setting terms* (it matches how `psi_operations.py` and the QIP premise treat psi) *and a loss in balance terms* (nothing limits a character from attempting psi except permission and cost). *Recommendation: keep operations, and let the cost/risk model do the limiting.*

## #506's single science skill

`strategic_skills.json` already carries **science** as one of seven strategic skills, defined at faction scale (research and branching tech projects). The reconciliation is:

- **No seventh individual skill.** `SCIENCE` does not join `COG/INT/REF/SAV/SOM/WIL` without explicit author approval — #482 fixes the six, and #506's science is a *faction* capability.
- **Individual science is COG** plus a field tag. A scientist's competence is "COG: Know (sociology)" or "COG + tag: epidemiology", not a separate rating.
- **The strategic skill is the faction's research capacity**, which is why it belongs beside statecraft/command rather than on the character sheet.
- This keeps #506's "science-led incremental faction projects" coherent without asking the RPG sheet to carry a knowledge-discipline taxonomy.

## Decisions this table asks for

Each is a question, not a recommendation to be assumed:

- **D-1** Accept the attribute collapse (FIT→SOM, SOC→SAV, INT→COG+INT, PSY→split, CYB→COG+device tags)?
- **D-2** Confirm that psi techniques are **operations** rather than skills, and that WIL/INT are the rolls that govern them?
- **D-3** Accept the three granularity losses above, or restore any of them as stunts (combat speciality, profession, psi)?
- **D-4** Confirm **science** stays a strategic skill with no individual counterpart beyond COG + tag?
- **D-5** Do strategic skills use the same 4dF resolution as individual skills, or a separate mission procedure (the current data models mission kinds, not dice)?

Until these are answered, the six-skill sheet remains the implementation baseline, the seven strategic skills remain an unapproved proposal, and no further mechanics should be built on either.

## Verification

- Six individual skills and their meanings: `strategy_game/rpg/skills.py` (`INDIVIDUAL_SKILLS`).
- Seven strategic skills, explicitly `PROPOSAL`: `strategy_game/data/strategic_skills.json`.
- Psi as operations, not skills: `strategy_game/psi_operations.py`.
- Legacy attributes and the 40-skill table: `rulebook_parts/01_basic_rules.md` (skill→STAT table).
- No code, prompt, data or rulebook was modified by this document.

— prepared by Ai (愛), 2026-10-19, for Tomi's decision under #516
