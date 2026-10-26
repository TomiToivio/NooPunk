# Rules foundation policy (#615)

**Status: governing design policy. It records decisions and conflicts; it changes no mechanic.**
Per this issue's own rule — *"Do not overwrite approved choices by implication; put proposed changes in a
comparison with dice probabilities and obtain a decision"* — every item below that would change play is
listed in the **conflict register** (§3) and left open.

Related: #564 (conversion epic), #19 (CWN foundation), #22 (skills), #566 (scope ruling), #569 (rights audit),
#572 (native subsystems).

---

## 1. The decision this issue makes

**The *Without Number* family is one coherent base chassis**, not four competing engines:

| Reference | Role | NoöPunk contexts | Candidate mechanics |
|---|---|---|---|
| **Cities Without Number** | **primary** | urban cyberpunk, UNSA fieldwork, ubiquitous hacking, BCI/cyberware, megacorps | core chassis, dangerous action, cyberware strain, network access, mission procedures |
| **Stars Without Number** | **co-primary** | solar-system expansion, extraterrestrial polities, NHI encounters, psionics, factions | psionics/Effort, alien contact, ships and colonies, faction turns |
| **Worlds Without Number** | situational | interdimensional/noetic science fantasy, astral regions, anomalous entities | exploration, weird realms, world tags, Effort/Foci analogues — with magic **reinterpreted** as setting PSI/psychotronics, never imported as fantasy cosmology |
| **Ashes Without Number** | situational | locally devastated regions after the NHI Crisis, infrastructure collapse, disrupted networks | salvage, scarcity, survival, mutations, trauma, hazards |

**Secondary influences, explicitly not parallel resolution systems:** Eclipse Phase (simulationist treatment of
transhumanity), Fate Core / Transhumanity's Fate (aspects, consequential hooks), Powered by Apocalypse —
*Apocalypse World* and *The Veil* (fiction-first triggers, complications, clocks, fail-forward).

**Mixed environments must work inside one adventure.** Helsinki cyberpunk → exclusion zone → alien outpost →
noetic realm must not require rebuilding characters or switching engines.

**Design balance:** gamism/OSR as backbone, simulationism selectively where it yields decisions, narrativism
selectively as complement. No fixed numerical split; evaluate by playtesting and a complexity budget.

## 2. What this settles, and what it explicitly does not

**Settles:** the hierarchy (one chassis, two situational toolkits), the four genre/location mappings, and the
principle that genre modules may coexist in a single encounter without duplicating skills, damage or progression.

**Does not settle — and says so:** the core die, the attribute list and scale, whether classes exist, whether
PSI follows SWN's structure, and whether the already-approved Fate layer survives. Those are §3.

## 3. Conflict-and-resolution register

The register exists because four documents currently describe NoöPunk mechanics in four vocabularies, and this
issue's instruction is to **document the conflict before touching the mechanic**. Nothing here is resolved by
this document.

| # | Conflict | What the documents say | What the tree says | Resolution required |
|---|---|---|---|---|
| **C1** | **Core die** | #615: CWN primary, whose checks are `2d6 + skill + modifier`. #564: "the present 3d6 core-check model". #566 (provisional): keep `1d10`. | Layer A `STAT + Skill + 1d10 ≥ DV` (#111, `src/rules/core.py`). Layer B `4dF` (approved #389/#482). **No 3d6 check exists.** | **A probability comparison, then an author decision.** This is the single largest open question; it decides whether #389/#482's kernel survives. |
| **C2** | **Attributes** | #615 lists both "FIT/REF/INT/CHA" and "SOC/CYB/PSY" as flagged. #564 says 3d6 generation, modifiers −3..+3. | `FIT / REF / INT / SOC / CYB / PSY`, scale **1..10**, locked by #131 (`data/rules/core.json`). No modifier band. `CHA` appears only in the retired sketch. | Confirm `SOC` and `1..10`; confirm or replace the modifier-band idea. |
| **C3** | **Classes and levels** | #615 does not authorise classes. CWN/AWN offer a *single* class + Edges. #564 forbids stock classes/levels. | No class or level field in the sheet. | Confirm the ban; if Edges-shaped differentiation is wanted, name it and author its entries. |
| **C4** | **PSI** | #615: SWN is co-primary and supplies "psionics/Effort". #572: PSI is a **learnable natural human ability**, SWN's *shape* adopted, its class structure and virus origin refused. | Canon §6.1 "natural, not viral"; `rpg/psi.py` names modes of action, not powers. | Reconcile "SWN psionics" with "natural and taught": adopt the cost-pool shape (already proposed), reject the discipline taxonomy as written. |
| **C5** | **Fate's status** | #615: Fate is a **secondary influence**, not a default resolution system. #389/#482: Fate Core is the **approved** kernel for the crossover's Layer I. | Layer B resolves on `4dF` and is documented as approved. | Either Fate is demoted (reversing two approvals) or #615's "secondary influence" is understood as *outside* layer B. Needs one sentence. |
| **C6** | **Hacking model** | #615: CWN "network access". #572: hacking is the **ubiquitous network** — abundant access, scarce safety; CWN contributes only the access-prerequisite habit. | `rulebook/22` §22.5 five access classes; `test_cyber_access.py` proves an air gap is never remotely crossable. | Confirm the ubiquitous-network framing; CWN's host-centric model is the wrong shape. |
| **C7** | **Genre modules vs one grammar** | #615 wants four modules coexisting in one encounter. The tree has two kernels and one board module. | Layers A/B/C as inventoried in #564. | Depends on C1: one grammar cannot be asserted while two kernels resolve differently. |

**The register's own rule:** no entry may be closed by editing a mechanic. Each closes with an author decision and,
for C1, a published probability comparison first.

## 4. Provenance and licensing matrix

Verified 2026-10-26. This is a **reuse boundary**, not a licence grant for NoöPunk itself. Do not copy from a
free edition; a free *read* is not a reuse right. Full detail: `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`.

| Influence | Public resource | Verified status | May enter the tree? |
|---|---|---|---|
| **CWN** | published SRD (DriveThruRPG 452790); community mirror | SRD published; the mirror omits sections, so cite the document | **SRD text yes** (within its terms); book prose, art, setting no |
| **SWN** | free revised edition | **no standalone public SRD identified** | **mechanics reimplemented only — no text, tables, art, setting** |
| **WWN** | official SRD (DriveThruRPG 473939); mirrors | **CC0 for the SRD material**; Latter Earth setting and excluded material reserved | **SRD text yes**; setting no |
| **AWN** | free edition | **no separately licensed public SRD identified** | **mechanics reimplemented only**; no text |
| **Fate Core** | official SRD downloads | **two options: CC-BY 3.0 or OGL**, with attribution; the website text is explicitly *not* the SRD source — use the official SRD files | **SRD text yes** under either option, with the required notice |
| **Transhumanity's Fate** | publisher release | **CC BY-NC-SA**; no separate SRD | **NC blocks a commercially licensed core** — inspiration only |
| **Eclipse Phase** | official downloads; community rules | EP2 generally **BY-NC-SA 4.0**; edition exceptions exist | **NC** — inspiration only for a commercial core |
| **Apocalypse World** | creator downloads, design articles | **no standalone SRD identified** | inspiration only |
| **The Veil** | creator pages, Kickstarter aids | **no SRD identified** | inspiration only |

**The consequence that matters:** layer B is Fate, which is **CC-BY** and therefore usable — but the
*simulationist* borrowings from Eclipse Phase and Transhumanity's Fate are **NC**, and those two are exactly what
§1 lists as secondary influences. Any NC-derived text must stay out of a planned commercially licensed core.
Design ideas are not text; the register keeps the two separate.

## 5. Credits and attribution (proposal, adopted into `README.md`)

NoöPunk is an independent fictional setting and developing tabletop RPG. Its current mechanics are primarily
based on and adapted from the *Without Number* family by Kevin Crawford / Sine Nomine Publishing — especially
*Cities Without Number* and *Stars Without Number* — with setting-specific elements informed by *Worlds Without
Number* and *Ashes Without Number*. Additional design influences: *Eclipse Phase*, *Transhumanity's Fate*, *Fate
Core*, and Powered by Apocalypse games, particularly *Apocalypse World* and *The Veil*. NoöPunk is an unofficial
fan/independent project, not endorsed by or affiliated with those publishers or creators.

**This is a credit and disclaimer statement, not a licence grant.** It does not permit reproducing any text,
table, art, name or other protected expression from those works.

## 6. Independence roadmap

| Stage | Goal | Gate |
|---|---|---|
| **A — transparent adaptation** | the KEEP/MODIFY/REPLACE/OMIT/DEFER matrix with exact source inspiration per subsystem | exists (#564 matrix); needs the §3 register folded in |
| **B — consolidated hybrid** | unified sheet, action economy, stress/trauma, faction interface, NHI/PSI/BCI, cross-genre rules; quickstart and playable scenarios | blocked on C1–C5 |
| **C — playtest and measure** | cyberpunk, NHI/space, noetic, crisis-zone and mixed-genre sessions; measure lethality, speed, decision depth, GM load, narrative agency, complexity | blocked on B |
| **D — independent rules** | replace or substantially reinterpret borrowed procedures with authored NoöPunk rules — **without equating independence with renaming** | blocked on C |

Versioning and migration aids are required at every stage: rules changes carry a version and a compatibility note.

## 7. What is deliberately not done here

- No mechanic, number or die changed.
- No conflict in §3 resolved.
- The mixed-genre worked example (acceptance criterion 4) and the optional narrative/simulation layers
  (criterion 5) are **not** in this document: both depend on C1, because an example must resolve on *some*
  kernel, and writing one now would silently pick a side.
