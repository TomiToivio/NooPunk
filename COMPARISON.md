# COMPARISON.md — cross-system comparison before locking the NoöPunk core

**Status: generated comparison gate. Nothing in this file is canonical.**

For [#255](https://github.com/TomiToivio/NooPunk/issues/255), parent epic
[#200](https://github.com/TomiToivio/NooPunk/issues/200). Regenerate with
`python3 tools/issue255_comparison_report.py`; a guard fails if this file is out of date.

## 1. Purpose, GNS triangle and scope

Author direction (2026-10-10): **drop Fudge/Psi-Punk as a foundation**, compare four
families, and decide a Fate-first direction **before** committing to a core conversion.
This is a research gate. It does not rewrite the rulebook, the code, or merged work.

The triangle below is a **subjective design map, not a classification**. Every one of these
games mixes agendas; the corners name which tendency each family serves best.

| Corner | Family | What it does best | Why it is not adopted wholesale |
| --- | --- | --- | --- |
| **Centre** | Fate Core / Transhumanity's Fate | aspects, stunts, stress/consequences, flexible actions | too simple as-is: **six separately rated Attributes AND separately rated Skills are mandatory** |
| **Simulationist** | Eclipse Phase 2E | transhuman, hacking, PSI, injury, equipment, existential risk | too complex to import, and **NC-licensed** |
| **Gamist** | Cities / Stars Without Number | concise OSR tactics, backgrounds/edges/foci, mission and faction tools | carries D&D-adjacent class/level assumptions NoöPunk does not want |
| **Narrativist** | PbtA / The Veil | fiction-first moves, hard choices, relationships, drama | changes the game's *type*, not just its numbers; The Veil is more thematically pertinent than Apocalypse World |

### Scope and licence boundaries

- The centre is **built on** Fate Core, but **Transhumanity's Fate text is NC and is not copied**.
- **Fudge is out of scope** as an active chassis. The #213/#215 kernel prototype that consumes
  a Fudge/Fate ladder mapping is **superseded for future comparison decisions and preserved
  untouched** for audit, per this issue. #200's own Fudge/Psi-Punk centre is superseded the
  same way, and this file says so rather than quietly rewriting it.
- No rule here becomes canonical. Deliverable 6 is explicitly a draft of alternatives.

## 2–3. The canonical skill list against all four families (40 skills, full mapping)

*Every* skill in `data/rules/skills.json` is mapped into *every* family. Rows are labelled
`direct` (comparable mechanic and scope), `analogy` (partial overlap, or a different mechanic
type entirely) and `unsupported` (no counterpart). The labels exist because #255 forbids
claiming the lists are identical; they are not, and a conversion is lossy even when it is
`direct`, because the numeric scales differ.

| Family | Role | direct | analogy | unsupported |
| --- | --- | --- | --- | --- |
| Fate Core / Transhumanity's Fate | centre (preferred starting chassis) | 12 | 28 | 0 |
| Eclipse Phase 2nd Edition | simulationist corner | 20 | 18 | 2 |
| Cities Without Number / Stars Without Number | gamist corner | 19 | 15 | 6 |
| PbtA / The Veil | narrativist corner | 2 | 38 | 0 |

### Verification status, per family

- **Fate Core / Transhumanity's Fate** — Fate Core's skill list verified against the CC BY 3.0 SRD as recorded in data/sources/game_system_rights.json. Which skills Transhumanity's Fate ADDS (as opposed to inheriting) is INFERRED from its Eclipse Phase lineage, not read from its text, which is NC-licensed and not reproduced here.
- **Eclipse Phase 2nd Edition** — The active-skill names below are INFERRED from the EP2 lineage and the open online reference; the exact list was not re-read from eclipsephase.github.io during this pass. Treat EP2 column names as strong analogies, not quotations.
- **Cities Without Number / Stars Without Number** — The CWN/SWN skill list below is a well-established shared list and was NOT re-verified against the official CC0 SRD during this pass, per #255's warning to verify from the original rather than a mirror. Recorded as the next verification step.
- **PbtA / The Veil** — Move names below are the generic PbtA idiom, chosen so a reader unfamiliar with narrativist play can see the shape. The Veil's EXACT move list and attribute names were NOT verified against the publisher text; no official SRD is invented here, as #255 requires.

### Full mapping

| NoöPunk skill | STAT | Fate Core / Transhumanity's Fate | Eclipse Phase 2nd Edition | Cities Without Number / Stars Without Number | PbtA / The Veil |
| --- | --- | --- | --- | --- | --- |
| Administrate | INT | Resources `analogy` | *no counterpart* `unsupported` | Administer `direct` | Negotiate / requisition move `analogy` |
| Athletics | FIT | Athletics `direct` | Athletics `direct` | Exert `analogy` | Defy Danger / Act Under Pressure `analogy` |
| Connect | SOC | Contacts `direct` | *no counterpart* `analogy` | Connect `direct` | Reach out to a contact `analogy` |
| Counterintelligence | INT | Investigate `analogy` | *no counterpart* `analogy` | *no counterpart* `analogy` | Read a situation (threat) `analogy` |
| Deceive | SOC | Deceive `direct` | Deceive `direct` | Talk `analogy` | Lay down a lie / manipulate `analogy` |
| ESP | PSY | an aspect or stunt `analogy` | Psi `analogy` | *no counterpart* `unsupported` | Open your mind move `analogy` |
| Exotic Skill | Variable | stunt `analogy` | Exotic Weapon (narrower) `analogy` | foci `analogy` | playbook move `analogy` |
| First Aid | INT | *no counterpart* `analogy` | Medicine `analogy` | Heal `direct` | Patch someone up `analogy` |
| Forensics | INT | Investigate `analogy` | *no counterpart* `analogy` | Heal `analogy` | Investigate a scene `analogy` |
| Fray | REF | Athletics `analogy` | Fray `direct` | Exert `analogy` | Defy Danger `analogy` |
| Free Fall | FIT | Athletics `analogy` | Free Fall `direct` | Exert `analogy` | Defy Danger `analogy` |
| Guns | REF | Shoot `direct` | Guns `direct` | Shoot `direct` | Fire / shoot move `analogy` |
| Hardware | CYB | Crafts `analogy` | Hardware `direct` | Fix `direct` | tinker / repair move `analogy` |
| Infosec | CYB | Crafts (or a subsystem) `analogy` | Infosec `direct` | Program `analogy` | jack in / hack move `analogy` |
| Intelligence Analysis | INT | Investigate `analogy` | *no counterpart* `analogy` | Know `analogy` | Read a charged situation `analogy` |
| Interface | CYB | Interface (Transhumanity's Fate) `analogy` | Interface `direct` | *no counterpart* `analogy` | use the machine move `analogy` |
| Investigation | INT | Investigate `direct` | *no counterpart* `analogy` | Notice `analogy` | Investigate a mystery `analogy` |
| Kinesics | SOC | Empathy `direct` | Kinesics `direct` | *no counterpart* `analogy` | Read a person `direct` |
| Know | INT | Lore `direct` | Know `direct` | Know `direct` | Spout lore / know things `analogy` |
| Lead | SOC | *no counterpart* `analogy` | *no counterpart* `analogy` | Lead `direct` | Command / inspire move `analogy` |
| Medicine | INT | *no counterpart* `analogy` | Medicine `direct` | Heal `direct` | treat a wound move `analogy` |
| Melee | FIT | Fight `direct` | Melee `direct` | Stab `direct` | mix it up / hand-to-hand `analogy` |
| Noöspace | PSY | an aspect `analogy` | *no counterpart* `unsupported` | *no counterpart* `unsupported` | a custom 'enter the noösphere' move `analogy` |
| Perceive | PSY | Notice `direct` | Perceive `direct` | Notice `direct` | Read a situation `analogy` |
| Perform | PSY | *no counterpart* `analogy` | *no counterpart* `analogy` | Perform `direct` | perform / sway move `analogy` |
| Pilot | REF | Drive `analogy` | Pilot `direct` | Pilot `direct` | drive / fly move `analogy` |
| Precognition | PSY | an aspect or stunt `analogy` | Psi `analogy` | *no counterpart* `unsupported` | a custom precognition move `analogy` |
| Program | CYB | Crafts `analogy` | Program `direct` | Program `direct` | write software move `analogy` |
| Provoke | SOC | Provoke `direct` | Provoke `direct` | Talk `analogy` | Provoke / intimidate `direct` |
| Psychic Defence | PSY | Will `analogy` | Psi (opposed) `analogy` | *no counterpart* `unsupported` | resist influence move `analogy` |
| Psychokinesis | PSY | an aspect or stunt `analogy` | Psi `analogy` | *no counterpart* `unsupported` | a custom telekinesis move `analogy` |
| Research | INT | Investigate or Lore `analogy` | Research `direct` | Know `analogy` | look it up / gather info move `analogy` |
| Sneak | REF | Stealth `direct` | Infiltrate `direct` | Sneak `direct` | Act Under Pressure / sneak move `analogy` |
| Survival | INT | Survival (or Lore) `analogy` | Survival `direct` | Survive `direct` | forage / endure move `analogy` |
| Tactics | INT | *no counterpart* `analogy` | *no counterpart* `analogy` | *no counterpart* `analogy` | Read a situation (battle) `analogy` |
| Talk | SOC | Rapport `direct` | Persuade `direct` | Talk `direct` | Persuade / manipulate `analogy` |
| Telepathy | PSY | an aspect or stunt `analogy` | Psi `analogy` | *no counterpart* `unsupported` | a custom telepathy move `analogy` |
| Trade | SOC | Resources `analogy` | *no counterpart* `analogy` | Trade `direct` | bargain move `analogy` |
| Unarmed | FIT | Fight `analogy` | Melee (unarmed) `analogy` | Punch `direct` | hand-to-hand move `analogy` |
| Work | Variable | an aspect `analogy` | *no counterpart* `analogy` | Work `direct` | playbook / background `analogy` |

## 4. Subsystem comparison

| Subsystem | Fate Core / TF | EP2 | CWN / SWN | PbtA / The Veil | What NoöPunk should adapt |
| --- | --- | --- | --- | --- | --- |
| **PSI** | an aspect or stunt granting permission | discrete sleights under one Psi skill | none by default | a move with triggers and consequences | adapt the **permission** model; avoid statting every power |
| **Combat** | one attack skill per genre, stress absorbed by consequences | detailed, lethal, initiative-driven | concise and tactical | fictional positioning drives outcomes | adapt CWN's concision inside Fate's consequence frame |
| **Social** | Rapport/Provoke/Empathy plus aspects | Persuade/Deceive/Kinesics | Talk only | a dedicated social move with hard choices | adapt: PbtA's social move is the clearest single idea here |
| **Faction** | aspects and a faction sheet | reputation and favors | faction turn | fronts and clocks | adapt CWN/SWN's faction tools; they are already procedural |
| **Cyberspace / hacking** | a TF subsystem, not a skill | Interface + Infosec vs security | Program | a jack-in move | adapt: NoöPunk's two-skill split matches EP2's shape without its complexity |
| **Investigation** | Investigate | Know/Research/Perceive | Notice | Investigate a mystery | **NoöPunk's core fantasy** — adapt the explicit procedure, not a skill alone |
| **Cybernetics / transhumanism** | aspects and stunts | morphs and resleeving, fully procedural | minimal | gear as fiction | adapt EP2's *concepts*; its procedures are the complexity to avoid |
| **Advancement** | milestones, refresh, skill pyramid | points and rep | XP and foci | playbook advances | adapt Fate milestones; they fit the UNSA academy frame |
| **GM procedure** | aspects, compels, create an advantage | scenario and X-risk tools | mission and faction generators | agenda, principles, moves | adapt PbtA's *agenda and principles* almost verbatim |

## 5. PSI as three different design objects

The same fiction — a psychic investigator — is three different objects depending on family,
and conflating them is the commonest conversion error:

- **EP2 / SWN — a discrete ability.** A power you have or lack, with its own rules text. Easy
  to balance, hard to make feel personal, and NC-licensed in EP2's case.
- **Fate — a stunt or an aspect.** A *permission plus a small, bounded edge*. Cheapest to
  write and the closest to NoöPunk's existing 'light description, not full stats' doctrine.
- **PbtA — a move.** A move is **not merely a power**: it has a trigger, a roll, and a list of
  outcomes including hard choices and consequences. It produces *story* rather than a result.

NoöPunk's own psi skills (ESP, Telepathy, Psychokinesis, Precognition, Psychic Defence,
Noöspace) already look like EP2's roll-plus-discipline split, which is the shape to keep; the
open question is whether a specific power is a **stunt** (Fate) or a **move** (PbtA).

## 6. Two alternative Fate-first kernels — DRAFT, not canonical

Both kernels keep six separately rated Attributes and separately rated Skills, and both use
**4dF**. They differ in how the two ratings combine, which turns out to be the decisive choice.

**Kernel A — additive, capped at 4.** `4dF + ladder(STAT) + ladder(Skill)`, where the
ladder maps 1–10 to −1…+3. Both ratings always count.

**Kernel B — single-axis.** `4dF + higher(STAT, Skill)`, plus 1 only when the weaker rating is
a real competence. Deliberately non-additive.

### 4dF, exactly (81 equiprobable outcomes)

| Total | Probability | At least this |
| ---: | ---: | ---: |
| -4 | 1.2% | 100.0% |
| -3 | 4.9% | 98.8% |
| -2 | 12.3% | 93.8% |
| -1 | 19.8% | 81.5% |
| +0 | 23.5% | 61.7% |
| +1 | 19.8% | 38.3% |
| +2 | 12.3% | 18.5% |
| +3 | 4.9% | 6.2% |
| +4 | 1.2% | 1.2% |

### Why "bounded" cannot mean Fate's customary +2

| Modifier | P(success vs DV 0) | Gain over +0 |
| ---: | ---: | ---: |
| +0 | 61.7% | 0.0% |
| +1 | 81.5% | 19.8% |
| +2 | 93.8% | 32.1% |
| +3 | 98.8% | 37.0% |
| +4 | 100.0% | 38.3% |
| +5 | 100.0% | 38.3% |
| +6 | 100.0% | 38.3% |

Only **63.0%** of 4dF outcomes fall within ±1, so a +1 is worth **19.8 points** of success
probability and a +2 is worth **32.1**. At **+4** the bonus alone guarantees success against
DV 0, because 4dF cannot roll below −4. That is the "uncapped numerical exploit" #200 names,
and it is why Kernel A caps.

### Difficulty recalibration

The canonical DV ladder (9/13/15/17/21/24/29) is calibrated for `STAT + Skill + 1d10` and
**cannot be reused** under 4dF. Baselines: a starting operative (STAT 5 + Skill 3 = 8) and a
competent specialist (STAT 7 + Skill 6 = 13). Its top end deliberately exceeds what an
ordinary operative can reach, so those rows show `—`: that is the ladder working as designed,
not a gap in the conversion.

| Difficulty | NoöPunk DV | start (8) | specialist (13) | 4dF DV at +1 | +2 | +3 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Simple | 9 | 100.0% | 100.0% | -4 | -4 | -4 |
| Everyday | 13 | 60.0% | 100.0% | -4 | -4 | -4 |
| Difficult | 15 | 40.0% | 90.0% | -1 | 0 | 1 |
| Professional | 17 | 20.0% | 70.0% | 1 | 2 | 3 |
| Heroic | 21 | 0.0% | 30.0% | 2 | 3 | 4 |
| Incredible | 24 | 0.0% | 0.0% | 6 | 7 | 8 |
| Legendary | 29 | 0.0% | 0.0% | 6 | 7 | 8 |

### Worked UNSA case

Junior Investigator, first session: STATs `{'FIT': 5, 'REF': 5, 'INT': 7, 'SOC': 6, 'CYB': 5, 'PSY': 4}`,
skills `{'Investigation': 3, 'Research': 3, 'Kinesics': 2, 'Talk': 2, 'Perceive': 2}`.

| Check | STAT | Kernel A | Kernel B |
| --- | --- | ---: | ---: |
| Investigation | INT 7 | +2 | +2 |
| Research | INT 7 | +2 | +2 |
| Kinesics | SOC 6 | +0 | +1 |
| Talk | SOC 6 | +0 | +1 |
| Perceive | PSY 4 | -1 | +0 |

**The measured argument against Kernel B.** For an INT 7 investigator, Kernel A gives
Investigation 3 a bonus of **+2** and Perceive 2 a bonus of **+1** — the trained
skill counts. Kernel B gives both **+2**, because the single-axis rule discards the
weaker rating entirely: once the STAT dominates, investing in the skill changes nothing.
Kernel B is not a gentler Kernel A; it deletes the Attribute-versus-Skill distinction that
#255 requires NoöPunk to preserve. **Recommendation: Kernel A**, subject to author approval.

## 7. Sources and rights matrix

| System | Licence | Commercially reusable? | Role here |
| --- | --- | --- | --- |
| Fate Core System Reference Document (fate-srd.com) | CC BY 3.0 Unported | yes | centre chassis |
| Transhumanity's Fate (Eclipse Phase for Fate) | CC BY-NC-SA 3.0 (author-stated) | no | centre (NC: not copyable) |
| Eclipse Phase 2nd Edition | CC BY-NC-SA 4.0 | no | simulationist corner |
| Cities Without Number System Reference Document (Kevin Crawford / Sine Nomine) | CC0 (public-domain dedication) | public domain | gamist corner |
| Stars Without Number (Kevin Crawford / Sine Nomine) | NOT ESTABLISHED from an authoritative source | no | gamist corner |
| The Veil / The Veil: Cascade (Samjoko Publishing) | CC BY-SA 3.0 (Unported) for the text | yes | narrativist corner |
| Apocalypse World (D. Vincent and Meguey Baker) | NO CC GRANT ESTABLISHED -- all rights reserved with a per-request permission policy for words | no | narrativist corner |
| Fudge OGL System Reference Document | OGL 1.0a for designated Open Game Content | no | OUT OF SCOPE |

Transhumanity's Fate and Eclipse Phase 2E are **CC BY-NC-SA** and therefore inspiration
only: their expression cannot appear in a commercially released CC NoöPunk. The CWN SRD is
**CC0** and reusable, but must be verified from the official SRD rather than a mirror. The SWN
free edition is free-to-read and **not automatically an open SRD**. There is no universal PbtA
SRD: Apocalypse World has no CC grant, and The Veil's licence covers its text, not a SRD.
Full per-source detail is in `docs/sources/ATTRIBUTION.md` and
`data/sources/component_rights.json`.

## 8. Cross-references and conflicts

| Existing work | Relationship to this comparison |
| --- | --- |
| #200 | parent epic. Its Fudge/Psi-Punk centre is **superseded for future comparison decisions**; prior implementation is preserved, not deleted |
| #207 | exact odds on the raw scale — still valid as arithmetic |
| #213/#215 | the author-directed 1–10 ladder and its kernel prototype: **superseded as a chassis choice**, preserved for audit |
| #217–#232 | subsystem chapters. This file does not rewrite them; it names what a Fate-first pass would touch |
| #233 | aspects / narrative resource / consequence prototype — the Fate-side work, and the source of the stacking measurement quoted above |
| #231 | rights ledger and attribution. The rights matrix here derives from it |
| #144 | faction taxonomy — relevant to the Faction row above |
| #158, #159 | referenced by #255; not restated here |

### Conflicts identified, not resolved

- **Fudge/Psi-Punk vs Fate-first.** Author direction supersedes the earlier centre. The
  prototype files are left in place, so the repository currently contains both a
  Fudge-ladder prototype and this Fate-first comparison. That is intentional until audited.
- **Two numbering runs in `RULEBOOK.md`** (core 1–9 and extended canon 1–54) mean a bare
  `§N` reference is ambiguous for 1–9. Recorded in `docs/design/RULEBOOK_STRUCTURE.md`.
- **NC contamination risk.** Any conversion that quotes Transhumanity's Fate or EP2 text
  would breach the CC release target. The guard in `tests/test_issue255_comparison.py`
  checks this file names them only as sources.

### Not done here

- No migration, no renumbering, no rewrite of the rulebook or the code.
- The EP2, CWN and The Veil column names carry explicit verification caveats in the data file. Re-reading those sources against their official texts is the next step.
- 40 skills mapped; 40 rows in the data file; 4 families. Raw data: `data/rules/skill_mapping_crosssystem.json`.
