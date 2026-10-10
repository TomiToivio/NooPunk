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
---

## Appendix A — the first increment, preserved verbatim

_This appendix is the earlier `COMPARISON.md` that was **concatenated** onto the document above when the issue's PRs merged (it arrived as a second whole document: a second H1 and a second §1–§8, so every section number was defined twice). It is kept whole so nothing is discarded — #255 asks that agents' additions be reconciled **without discarding content** — and its headings are prefixed `A.` so they can no longer collide with the body above. Its unique material is §9 (playtest scenarios) and §10 (dependencies/coordination)._


**Status: IN PROGRESS.** This is a research/design gate, not a rule change. **No rule becomes
canonical from this document**, and nothing here authorises edits to `RULEBOOK.md`,
`data/rules/*` or any merged implementation. Author direction (2026-10-10): *drop Fudge/Psi-Punk
as a foundation; compare four families; write `COMPARISON.md` before committing to a core rules
conversion.*

> **Superseded premise, marked not deleted.** Issue #200's centre was **Fudge + Psi-Punk + Fate**.
> #255 supersedes that **for future comparison decisions**: Fudge is **out of scope** as an active
> source or chassis, Psi-Punk likewise, and #200's proposal is history rather than a baseline.
> Prior implementation work that assumed the old centre — including
> `docs/design/ISSUE_217_RESOLUTION_SEMANTICS_2026-10-10.md`, which proposed a partial-success
> policy for the Fudge-derived ladder — is **preserved untouched until audited** and is downstream
> of a premise that no longer holds. This document does not delete it and does not reconcile it.

---

## A.1. Goals, design triangle, trade-offs, and scope boundaries

### A.1.1 What this document is for

To decide **which family supplies the chassis**, how the four families' concepts map onto NoöPunk's
canonical six Attributes and 40 Skills, and what a conversion costs — *before* anything is locked.
The deliverable is a comparison, a set of conversion tables with honest labels, at least two
alternative numeric kernels with probabilities, and a rights matrix.

### A.1.2 The GNS design triangle (a heuristic, not a classification)

GNS is a **subjective design map, not an objective rating**, and every game named here mixes
agendas. It is used here only to spread the design space.

| Position | Family | What it contributes | What it costs |
| --- | --- | --- | --- |
| **Centre — preferred chassis** | **Fate Core** (and *Transhumanity's Fate* as its transhuman application) | narrative aspects, stunts, stress/consequences, flexible actions | too simple as-is; **six separate Attributes AND separately rated Skills are mandatory**, which Fate Core does not provide |
| **Simulationist corner** | **Eclipse Phase 2e** | rich transhuman, hacking, PSI, injury, equipment and existential-risk procedures | too complex to import wholesale; **NC licence** |
| **Gamist corner** | **Cities Without Number / Stars Without Number** | concise playable OSR tactics, backgrounds/edges or foci, skills, mission and faction tools | avoid excessive D&D class/level assumptions; **SWN's free edition is not an open SRD** |
| **Narrativist corner** | **PbtA — The Veil, Worlds of Legacy** | fiction-first moves, hard choices, relationships, consequences, character drama | narrativist play must be explained to readers new to it; **AW itself grants nothing** |

Author's steer on the Narrativist corner: **The Veil is more thematically pertinent than
Apocalypse World** — and the rights matrix below shows this is also the corner where the licensing
is *cleanest* to reuse.

### A.1.3 The trade-off this comparison exists to expose

**The preferred centre contains a NonCommercial work.** The author locks the chassis to *Fate Core
/ Transhumanity's Fate* — but **Transhumanity's Fate is CC BY-NC-SA**, so it cannot be copied into
NoöPunk's Creative Commons release. Fate Core itself is **CC BY and explicitly *not* viral**, so it
*can*.

That is the central tension of this issue and it shapes everything else:

- **Fate Core supplies the reusable chassis** (aspects, stunts, stress/consequences, flexible
  actions) with attribution as the only obligation.
- **Transhumanity's Fate and Eclipse Phase 2e supply design study, not expression.** They may be
  read to understand how a transhuman Fate game handles morphs, PSI, hacking and existential risk;
  their text may not enter the work.
- **Anything whose only clean source is an NC book must be re-expressed from the mechanics**, which
  is what CWN's CC0 SRD explicitly permits and what EP/Transhumanity's Fate do not.

### A.1.4 Author-locked requirements (carried here as constraints, not proposals)

1. Base on **Fate Core / Transhumanity's Fate**; **do not copy NC-licensed Transhumanity's Fate
   text**.
2. Exactly **six independently rated Attributes — FIT / REF / INT / SOC / PSY / CYB** — and
   **Attributes distinct from Skills**.
3. **Preserve the existing NoöPunk Skill list** (`data/rules/skills.json`, 40 skills). Its lineage
   is *identified* as drawing on Transhumanity's Fate, Eclipse Phase and CWN — **the tables below
   verify alignment rather than assert that those systems have identical lists**.
4. **Research conversions before choosing** dice formula, attribute/skill scaling, difficulties,
   movement, stress or progression. No silent rule switches; no arbitrary 1:1 mappings.
5. **No Fudge** in recommended active sources or chassis; where history is compared, mark it out of
   scope and distinguish #200's outdated proposal.

### A.1.5 Scope and licence boundaries (summary; the matrix is §7)

- **Reusable in a commercial CC release:** Fate Core SRD (**CC BY**, not viral), Cities Without
  Number SRD (**CC0**), Worlds of Legacy SRD (**CC BY**).
- **Reusable with a ShareAlike obligation:** The Veil / Cascade (**CC BY-SA 3.0**) — and it carries
  a **per-portion carve-out** (see §7).
- **Not reusable — design study only:** Eclipse Phase 2e and *Transhumanity's Fate* (**CC BY-NC-SA**).
- **No grant at all:** Apocalypse World (playbooks/moves/MC sheets are free to read; there is no
  universal PbtA SRD), and Stars Without Number's **free edition, which is a book, not an SRD**.
- **Out of scope:** Fudge, Psi-Punk (OGL) — superseded by #255.

---

## A.2. Attribute conversion table

A “counterpart” means analogous use, **not equivalent numbers or a fixed formula**. Fate Core has **skills**, not core attributes; EP uses **aptitudes**, with skills in addition; CWN/SWN have D&D-like attributes + skills; PbtA/The Veil usually roll moves using a broad stat or emotion, with no independent universal skill bonus.

| NoöPunk stat | Fate Core skills typically involved | Eclipse Phase 2E aptitude area (conceptual) | CWN / SWN attributes | PbtA / The Veil |
|---|---|---|---|---|
| **FIT** Fitness | Physique, Athletics, Fight | SOM (somatics) | Strength, Constitution | body-related stat / emotional condition depending on move |
| **REF** Reflexes | Athletics, Shoot, Drive | REF (reflexes) | Dexterity | action-based move with relevant stat/emotion |
| **INT** Intelligence | Lore, Investigate, Notice | COG (cognition), INT (intuition) | Intelligence, Wisdom | investigation move / relevant emotion |
| **SOC** Social | Rapport, Empathy, Deceive, Provoke | SAV (savvy) | Charisma | social move / emotional condition |
| **PSY** Psyche | Will plus supernatural Aspect/Stunt | WIL (willpower); psi uses additional game-specific systems | Wisdom/Charisma; SWN psychic class/powers separate | custom psychic move plus fictional permissions |
| **CYB** Cybernetics | Lore, Crafts, Burglary + gear/Aspect | COG/INT and Infosec/Interface/Programming; hardware is separate | Intelligence + Program/Fix; SWN technical skills | interface/hacking move, hardware narrative permission |

**Important:** NoöPunk CYB is a **character stat**, while `Interface / Network / Compute` are **hardware properties**, not extra character attributes. EP's aptitudes are not just “Fate stats” with the numbers changed. PbtA's triggers/procedures cannot be represented with a single numerical column.

## A.3. Complete canonical skill vocabulary: cross-system *concept* mapping

This comparison enumerates **every** name from `data/rules/skills.json` at the time of drafting. **These are provisional analogies**, not confirmed identical official skill names: EP entries may vary by edition; Fate examples are from its broad skill model; CWN and SWN lists differ; PbtA examples are proposed possible *types of moves*, not official The Veil moves. “No direct match” must remain an explicit gap.

| NoöPunk skill | Stat | Fate analogue | Eclipse Phase analogue | Without Number analogue | PbtA / The Veil move analogy |
|---|---|---|---|---|---|
| Administrate | INT | Resources, Contacts | Administration | Administer | institutional move |
| Athletics | FIT | Athletics | Freerunning | Exert | act under fire |
| Connect | SOC | Contacts | Networking | Connect | relationship move |
| Counterintelligence | INT | Investigate, Notice | Infosec, Investigation | Notice, Connect | counterspy move |
| Deceive | SOC | Deceive | Deceive | Talk | deceive move |
| ESP | PSY | Notice + Stunt | Psi sleight | SWN psychic ability; CWN none | psychic move |
| Exotic Skill | Variable | Stunt / permission | Exotic Skill | Work / special skill | custom move |
| First Aid | INT | Lore + Stunt | Medicine | Heal (CWN) | healing move |
| Forensics | INT | Investigate | Investigation | Notice, Know | clue move |
| Fray | REF | Athletics, Fight | Fray | Exert, Punch | defend move |
| Free Fall | FIT | Athletics | Free Fall | Exert, Pilot | zero-g move |
| Guns | REF | Shoot | Guns | Shoot | combat move |
| Hardware | CYB | Crafts | Hardware | Fix | repair move |
| Infosec | CYB | Burglary, Lore | Infosec | Program | security move |
| Intelligence Analysis | INT | Investigate, Lore | Research, Investigation | Know, Notice | assess threat move |
| Interface | CYB | Lore + Stunt | Interface | Program | interface move |
| Investigation | INT | Investigate | Investigation | Notice, Know | investigate move |
| Kinesics | SOC | Empathy | Kinesics | Notice, Talk | read a person |
| Know | INT | Lore | Academics / skill field | Know (CWN) | expertise move |
| Lead | SOC | Rapport, Provoke | Persuasion / Leadership | Lead | lead move |
| Medicine | INT | Lore + Stunt | Medicine | Heal (CWN) | heal move |
| Melee | FIT | Fight | Melee | Stab | attack move |
| Noöspace | PSY | Aspect + Stunt | no direct match | no direct match | bespoke projection move |
| Perceive | PSY | Notice | Perception | Notice | read situation |
| Perform | PSY | Rapport + Stunt | Art | Perform | perform move |
| Pilot | REF | Drive | Pilot | Drive / Pilot (SWN) | vehicle move |
| Precognition | PSY | Stunt | precognition-related sleight | SWN psychic power analogy | premonition move |
| Program | CYB | Lore, Crafts | Programming | Program | hack move |
| Provoke | SOC | Provoke | Intimidation | Talk, Lead | apply pressure move |
| Psychic Defence | PSY | Will + Stunt | psi resistance | SWN psychic resistance | resist psi move |
| Psychokinesis | PSY | Stunt | psychokinetic sleight | SWN telekinesis power | psychic move |
| Research | INT | Investigate, Lore | Research | Know | research move |
| Sneak | REF | Stealth | Infiltration | Sneak | sneak move |
| Survival | INT | Survival | Survival | Survive | survive move |
| Tactics | INT | Lore, Notice | Tactics | Lead, Know | battle plan move |
| Talk | SOC | Rapport | Persuasion | Talk | persuade move |
| Telepathy | PSY | Stunt | telepathy-related sleight | SWN telepathy discipline | mind-contact move |
| Trade | SOC | Resources, Rapport | Networking / Profession | Trade | trade move |
| Unarmed | FIT | Fight | Unarmed Combat | Punch | attack move |
| Work | Variable | Lore, Crafts | Profession / field | Work | career move |

**Notes:** `Exotic Skill` and `Work` are fielded/variable; `Know`, `Medicine`, `Hardware`, `Pilot`, `Perform` have field specializations in the current catalog. Neither the Transhumanity's Fate, Eclipse Phase, nor CWN skill list is *literally identical* to the NoöPunk list: record nearest functional correspondence and mismatches. Exact page-by-page validation remains an explicit review task.

## A.4. Dice, thresholds, degrees of success: conversion *framework*, not a conversion formula

| Topic | Fate Core | Eclipse Phase 2E | CWN / SWN | PbtA / The Veil | NoöPunk open design question |
|---|---|---|---|---|---|
| Randomizer | 4 Fate dice (`-1,0,+1`) | d100 roll-under | Commonly 2d6 skills and d20 attack rolls | Typically 2d6 + stat/emotion | One kernel across all subsystems? |
| Skills & attributes | Skill rating; no standard separate attribute | Aptitude + skill base/target; percentile resolution | Separate attribute modifier and skill rating | Usually no universal skill ratings | Preserve both, avoid runaway stacked bonuses |
| Difficulty | Ladder with opposition/target numbers, shifts | Target number, modifiers and success quality | 2d6 checks vs difficulty; combat differs | 6-/7–9/10+ bands (typical, game-specific) | Translate outcome *frequency*, not bare integers |
| Degrees | Fail, tie, succeed, succeed with style | Success/critical/superior result and failure gradations | Often binary checks, specific combat exceptions | Miss, mixed, strong hit | Which narrative costs can accompany success? |
| Assistance | Teamwork and advantages/aspects | Bonuses, assistance, gear, teamwork | Aid or modifier by edition and procedure | Aid/interfere move or fiction | Cap stacking and make collaboration meaningful |
| Metacurrency | Fate Points | Pools/moxie-like resources | Effort for some psychic systems; no universal Fate Points | Usually fictionally triggered moves, some playbook resources | Do resource pools overlap? |

**4dF exact distribution (81 equally likely combinations):**

| 4dF result | -4 | -3 | -2 | -1 | 0 | +1 | +2 | +3 | +4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Outcomes / 81 | 1 | 4 | 10 | 16 | 19 | 16 | 10 | 4 | 1 |

A Fate outcome of **+2 net modifier** has a higher success probability against the same target than +0; adding a second unrestricted +2 attribute would substantially change standard Fate target expectations. Do **not** equate EP “60% skill” to Fate “+3” or CWN “level 3”: these are different distributions and target settings.

### Two explicit Fate-first kernels to playtest (both DRAFT)

**Kernel A: bounded additive attributes + skills.** `4dF + A + S`; proposed example ranges `A ∈ [-2,+2]`, `S ∈ [0,3]`. Calibrate difficulty and cap stacked temporary bonuses. *Pros:* both matter every check. *Risk:* very large modifiers relative to 4dF spread, and over-specialization.

**Kernel B: skill-led with attribute edge.** `4dF + S + conditional A`; conditional attribute contribution is **capped** (e.g. +1/0/-1) when attribute especially helps or hinders the specific approach. All stats are rated separately and determine capacity, resistance, fictional access and bounded bonuses. *Pros:* closer to Fate core odds. *Risk:* attributes may feel underused if triggers unclear.

These are **hypotheses, not rules**. When stress-testing, vary target shifts, qualified opponent, gear, teamwork, Fate Point invokes, cyber/psi edge use, expert vs newcomer and PvP.

**Shared example for testing:** An UNSA academy graduate with INT +1, Research 2 examines an Orion-linked forensic dossier. Against a proposed target 3 with neutral dice: Kernel A total 3 = success/tie boundary depending chosen formal rules; Kernel B total 3 if conditional +1 applies. A senior analyst with INT +2 and Research 3 would gain +5 in A, versus at most +4 in B: compare rates of success at *all* difficulty tiers. Fate's real tie and style outcomes must be chosen explicitly before final odds tables.

## A.5. Difficulty conversion by *task meaning* (illustrative)

| Fictional difficulty | Fate-style target example | EP2 approach | CWN/SWN approach | PbtA / The Veil approach |
|---|---|---|---|---|
| Routine for trained agent | +0 / +1 opposition | Easy threshold with beneficial modifiers | Lower skill-check DV | Usually no roll unless dramatic stakes |
| Professional challenge | +2 / +3 opposition | Ordinary test with relevant modifiers | Standard skill-check DV | Trigger a move, 7–9 has meaningful cost |
| Elite / resistant opponent | +4 / +5 opposition | Contest or penalty for difficult conditions | Higher DV or opposed check | Opponent/threat moves and snowball |
| Exceptional / NHI anomaly | +6+ if roll is allowed | Heavy penalty or impossible without permission | High DV / required specialist capacity | Fictional positioning or specialist move required |

This table deliberately avoids claiming numerical equivalence. Before implementing any conversion, calculate percentiles for typical beginner/competent/expert agents and verify plausible task permissions.

## A.6. Subsystem comparisons and recommendations to investigate

| Subsystem | Fate / Transhumanity's Fate | Eclipse Phase | CWN / SWN | PbtA / The Veil | NoöPunk research hypothesis |
|---|---|---|---|---|---|
| **PSI** | Aspect for psychic identity/permissions; Stunt for a defined exception; stress/consequence costs | Separate psi abilities/sleights, aptitude/skill interactions, costs/risks | SWN disciplines/powers and Effort as explicit resource | A psychic Move triggers from a fictional action and determines 3-tier consequences | Separate **capability/permission**, **check** and **cost**; avoid psi = unrestricted bonus |
| **Combat** | Zones, four actions, stress/consequences and concession | More detailed action timing, injuries, range and gear | Clear rounds, attacks, damage and tactical choices | Harm, fiction-first threat and mixed-result escalation | Test meaningful tactics without EP tactical burden |
| **Social** | Rapport/Deceive/Provoke, aspects and social conflict | Networking, reputation, motivations and social skills | Talk, Connect, Lead and contacts/factions | Emotional stakes, debt/relationship and social moves | Model trust, warrants, diplomacy, obligation, ideology |
| **Factions** | Campaign aspects, extras, consequences and milestones | Organizational networks/reputations | Faction turn, assets, goals, actions | Fronts/threats/clocks, evolving relationships | Preserve existing NoöPunk faction/reputation rules; compare separately |
| **Cyberspace** | Advantage, contests, challenges with technical Stunts | Distinct mesh hacking, infosec, AI and network systems | CWN Program/Fix and hacking procedures; SWN technical actions | Fictional cyber move, costs and exposure | Explicit network topology, privileges and separate hardware Interface/Network/Compute |
| **Investigation** | Discover/create advantage; compel complications | Professional investigative skills/gear | Skill checks, GM procedures | Clue-revealing moves, partial hits and costs | Essential clues cannot disappear on one failed roll; maintain evidence chain |
| **Transhumanism** | Body/identity as Aspects/extras | Morphs/resleeving/augmentation identity | Cyberware and SWN optional AI/transhuman tech | Relationship/identity consequences | Emerging, uneven adoption; don't import whole Eclipse Phase setting |
| **Advancement** | Milestones, skill rearrangement, Stunts | Skills, pools, gear and bodily changes | XP and level advancement | End-of-session questions and playbook growth | Classless lifepath; both expertise and life-altering experiences |

### PSI power, Stunt and Move: important non-identity

An **Eclipse Phase psi sleight** or **Stars Without Number psychic power** typically establishes a concrete capability with eligibility/cost rules. A **Fate Stunt** is a narrowly framed exception or special bonus, often justified by an Aspect. A **PbtA Move** is a triggered procedure that says what happens when a player acts in specific circumstances, including mixed outcomes and GM reactions. They are *not interchangeable units*: one power might need an **Aspect (identity) + Stunt (permission) + skill test (ability) + move-like 7–9 consequence text (narrative price)**. This is a conceptual composition, not a suggestion to run four independent resolution rolls.


## A.7. Source and rights matrix

Verified **2026-10-10** at the sources linked by the issue. "Reusable" means *the text may be
reproduced in a commercial Creative Commons release*.

| Source | Edition / URL | Licence (as stated at source) | Commercial reuse | Obligations and scope limits |
| --- | --- | --- | --- | --- |
| **Fate Core SRD** | fate-srd.com — official licensing + CC-BY SRDs (ZIP) | **Creative Commons Attribution (CC BY)**, Unported | **Yes** | *"the most liberal one possible"*, explicitly **not viral** — derived content need not be CC. Requires the **attribution bloc supplied at the top of each SRD file** on the copyright page. |
| **Transhumanity's Fate** | legacy.eclipsephase.com releases page | **CC BY-NC-SA** (per EP licensing; page requires Fate Core) | **No** | NonCommercial blocks commercial reuse. **Design study only — no text.** |
| **Eclipse Phase 2e** | eclipsephase.com/cclicense | **CC BY-NC-SA** unless noted otherwise; "exceptions noted below" | **No** | Attribution to **Posthuman Studios, LLC**; derivatives under the same licence; NC blocks commercial. Per-release exceptions exist and must be checked per release. |
| EP online reference | eclipsephase.github.io | derived from EP | **No** | Inherits the NC licence of its source. |
| **Cities Without Number SRD** | DriveThruRPG product 452790 (Sine Nomine, official) | **CC0 1.0** — *"a Creative Commons 0 waiver allowing downloaders to copy, modify, reproduce, or otherwise use it for both personal and commercial purposes"* | **Yes** | The publisher states CC0 waives his claim on *"that specific verbiage"*. **Scope: the full SRD, but not all parts of the original book.** |
| **Stars Without Number (revised, free version)** | DriveThruRPG product 230009 | **No licence statement found** — a free edition of the **book** | **No** | **Free-to-read is not an open licence.** No SRD exists to verify; Sine Nomine publishes SRDs for CWN and WWN, not SWN. |
| **Apocalypse World** | lumpley.games/apocalypseworld | **No CC grant on the page** | **No** | Free playbooks, moves and MC sheets to *read*; the page grants no reuse. **There is no universal PbtA SRD.** |
| **Worlds of Legacy SRD** | ufopress.co.uk PDF | **Creative Commons Attribution (CC BY)** | **Yes** | *"all you need to do is put the attribution provided below clearly in your work"* — no fees, **no requirement to license your own work CC**. Licensing moniker: **"Worlds of Legacy"**. |
| **The Veil / Cascade** | samjokopublishing.com (text), DriveThruRPG | **CC BY-SA 3.0 Unported** | **Yes**, with ShareAlike | **Per-portion carve-out:** the licence paragraph itself records that *"some moves are either tweaked or lifted straight from Apocalypse World"* — that permission was granted **to that project**, so those portions are unavailable even though the surrounding text is licensed. Adopting The Veil text imposes **ShareAlike on the whole work**. |
| **Fudge / Psi-Punk** | — | OGL (cannot be relabelled CC) | **No** | **Out of scope** per #255. Retained only as history. |

### A.7.1 What the matrix decides

1. **The chassis can be licensed cleanly.** Fate Core is CC BY and not viral, so a Fate-first
   NoöPunk can be released commercially under Tomi's chosen licence with an attribution bloc and no
   copyleft surprise. This is the single most important fact in this document.
2. **Two of the four families are study-only.** EP2 and Transhumanity's Fate are the richest
   sources for the transhuman and PSI material and **none of their text may be used**. Every
   mechanic traced to them must be re-expressed, and the tracing must be recorded.
3. **The Gamist corner is the most permissive and the least open at the same time.** CWN's SRD is
   **CC0** (no obligations at all), while SWN's free edition grants **nothing** — the two are
   routinely conflated because they share a publisher.
4. **The Narrativist corner is usable — but only one of its three routes is clean.** Worlds of
   Legacy (CC BY) is unconditionally reusable; The Veil (CC BY-SA) would put the whole work under
   ShareAlike; Apocalypse World grants nothing.
5. **A Fate Core + CWN + Worlds of Legacy combination is licence-compatible** with a commercial CC
   release. A Fate Core + The Veil combination forces ShareAlike on everything.

### A.7.2 Retrieval honesty

- **Verified at source:** Fate licensing page and its CC-BY guide; EP licensing page;
  Transhumanity's Fate release page; CWN SRD official DriveThruRPG listing; SWN free-edition
  listing; Worlds of Legacy SRD PDF; The Veil licence paragraph; Apocalypse World page.
- **Not retrieved in this pass:** the EP licensing page's per-release *exceptions* list, and The
  Veil: Inheritance QuickStart's separate terms. Both are recorded as **unverified** rather than
  assumed, and neither is relied on above.

---

## A.8. Cross-references to existing work (do not overwrite)

| Artefact | What it already provides | How this document uses it |
| --- | --- | --- |
| `data/rules/skills.json` | the **40 canonical Skills** with `stat`, `untrained` and `fielded` flags; `untrained_modifier: -1`; the field-substitution rule | the canonical side of every skill mapping in §3 |
| `docs/design/RPG_CONVERSION_REFERENCE.md` | EP2→NoöPunk and CWN→NoöPunk STAT correspondence, skill references, conversion procedure | the starting point for the Simulationist and Gamist columns; **consume, do not rewrite** |
| `docs/design/ISSUE_200_CROSS_SYSTEM_CONVERSION.md` | the five-family conversion lab and its three dimensions | the conversion algorithm §2 builds on |
| `docs/design/ISSUE_200_KERNEL_PROTOTYPE.md` | three attribute+skill kernels with measured probabilities, the ladder, opposed checks, modifier stacking, lethality | §6 starts from these rather than restarting |
| `docs/sources/GAME_SYSTEM_RIGHTS.md` + `data/sources/game_system_rights.json` | the dated, guarded provenance ledger | the authoritative rights record; §7 above is the summary, that ledger is the source |
| Issues **#217–#232** | the domain work packages (core rules, chargen, physical, social, cybernetic, psychic, astral, cross-domain, UNSA, beings, equipment, narrative, GM toolkit, CC release, consolidation) | the chapters the comparison must ultimately feed; **#217 is now downstream of a superseded centre** |

### A.8.1 Conflicts found (recorded, not resolved)

- **#217's resolution semantics were designed against the superseded Fudge/Fate ladder.** The
  untrained −1 rule matches canon (`skills.json` `untrained_modifier: -1`), but the ladder and the
  partial-success policy are premises from #200's old centre. Flagged for audit; **not deleted**.
- **#200's direction record and the kernel prototype** both name Fudge/Psi-Punk as the centre.
  #255 supersedes that for future comparison decisions; the documents stay as history.
- **The rights ledger already records** the EP/Transhumanity's Fate NC boundary and The Veil's
  per-portion carve-out. §7 agrees with it; no ledger edit is proposed here.

---

## Roadmap for the remaining sections

Committed in small reviewable increments, per the issue's collaboration requirements:

- [x] **§1** goals, triangle, trade-offs, scope boundaries — *this increment*
- [x] **§7** source and rights matrix — *this increment*
- [x] **§8** cross-references and conflicts — *this increment*
- [ ] **§2** side-by-side conversion tables: six Attributes and the **full 40-skill list** against
      each of the four families, labelled *direct correspondence / conceptual analogy /
      unsupported*, marking **no counterpart** where none exists
- [ ] **§3** the same tables with lossiness and edition-dependence spelled out
- [ ] **§4** domain comparisons — PSI, Combat, Social, Faction, Cyberspace/hacking, investigation,
      cybernetics/transhumanism, advancement, GM procedure — by complexity, agency, genre fit, risk
- [ ] **§5** PSI as four distinct design concepts: EP/SWN discrete abilities, Fate Stunt/Aspect,
      PbtA Move (a Move has triggers, choices and consequences, and is *not* merely a power)
- [ ] **§6** at least two alternative Fate-first numeric kernels with probability analysis, target
      recalibration, stacking/balance and a worked comparable UNSA case


## A.9. Specific scenarios for apples-to-apples playtests

1. **UNSA interview:** Friendly Confederacy contact offers vital intelligence only if the agents promise confidentiality that may constrain human sovereignty. Test social competency vs voluntary compromise and faction response.
2. **Orion proxy investigation:** Investigators track a donor network via interviews, open-source evidence, forensics and cyber intrusion. Core clue must be discoverable, with consequences escalating on risk.
3. **PSI incident:** Academy-trained psychic probes missing-time impressions; learn something partial and ambiguous without automatic mind-reading truth. Test stress, countermeasures and agency.
4. **Cybergraph operation:** Hacker penetrates one endpoint only where a real authorized/vulnerable technical path exists; compromise does not automatically grant brain access.
5. **Physical crisis:** Rescue civilians from a contaminated anomaly zone with limited rounds, gear constraints, teammates and negotiable risks.

Track median resolution time, number of rule lookups, tactical decisions, meaningful narrative choices, modifier stacks, success rates, safety/agency and GM improvisation burden.

## A.10. Dependencies, coordination, deliverables

- [#200](https://github.com/TomiToivio/NooPunk/issues/200) is an existing parent *implementation* epic. Its Fudge/Psi-Punk center conflicts with #255's new author direction. **Do not destructively rewrite #200 or mass-delete implementation artifacts**; raise a resolution comment and use separate approved follow-up change.
- [#217–232](https://github.com/TomiToivio/NooPunk/issues/217), [#144](https://github.com/TomiToivio/NooPunk/issues/144), [#158](https://github.com/TomiToivio/NooPunk/issues/158), [#159](https://github.com/TomiToivio/NooPunk/issues/159) contain pre-existing work. Preserve valid contributions and flag conflicts with the latest decision.
- Candidate future *decision record* must pin: chosen kernel, trait/skill ranges, challenge ladder, stress handling, resources, Stunt and PSI mapping, advancement, and licensing; **none decided merely by this research**.
- Before merge verify: all **40** skills mapped; six attributes; four families; difficulty, PSI/combat/social/faction/cyberspace tables; sources and license caveats; no canonical rule changes.
