# CWN/SWN chassis policy for NoöPunk

> **Status:** design provenance and decision ledger, not a runtime conversion. Parent epic [#564](https://github.com/TomiToivio/NooPunk/issues/564); restoration [#567](https://github.com/TomiToivio/NooPunk/issues/567). **Do not use this document to infer that a proposed change is already implemented.**

## Sources and precedence

- [#19](https://github.com/TomiToivio/NooPunk/issues/19) establishes the **Cities Without Number SRD** as an open *starting point*, **not** a straight CWN clone, and defines the subsystem review policy.
- [#22](https://github.com/TomiToivio/NooPunk/issues/22) records a **MODIFY** decision for the skill subsystem and forbids incidental redesign of neighboring systems.
- [#111](https://github.com/TomiToivio/NooPunk/issues/111) and [#131](https://github.com/TomiToivio/NooPunk/issues/131), as recorded in `data/rules/core.json`, establish the later independent 1d10 kernel and FIT/REF/INT/SOC/CYB/PSY attributes for the legacy tabletop rules.
- [#389](https://github.com/TomiToivio/NooPunk/issues/389) and [#482](https://github.com/TomiToivio/NooPunk/issues/482) are the approved Fate baseline for the crossover RPG.
- [RPG_CHASSIS_INVENTORY.md](RPG_CHASSIS_INVENTORY.md) inventories current implementations and the contradictions between the earlier issues and the present repository.
- [#566](https://github.com/TomiToivio/NooPunk/issues/566) is the **open author decision** on which layers to unify and what dice/attributes/classes to use.

The current implemented rulebooks and code remain authoritative for gameplay **until** a later explicitly approved decision and corresponding migration changes them. This document distinguishes **historical design intent** from **present executable behavior**.

## Design policy from #19

CWN SRD: https://cwn.quadrifons.com/

NoöPunk begins with the *open* CWN SRD as a comparison and potential reusable mechanical chassis, then deliberately evaluates **each subsystem**, adopting only what fits a heavily modified, original game. No subsystem is automatically inherited. Only material actually covered by the applicable open SRD terms may be copied or adapted. The commercial book, protected setting, factions, characters, prose, art and other games' expression may not be imported merely because those works inspire NoöPunk. **An online rules page is not, by itself, proof of an open licence.** See the separate audit [#569](https://github.com/TomiToivio/NooPunk/issues/569) before any textual reuse.

Cyberpunk 2020, Eclipse Phase, Shadowrun, The Sprawl and CY_BORG are **comparative design influences**, never automatic implementation or text sources (#19). SWN is likewise optional and conditional in #564: spacefaring or science-fiction procedures enter only when mechanically needed; the initial campaigns remain Earth-based.

For each subsystem record one of:

| Decision | Meaning |
| --- | --- |
| **KEEP** | Use an SRD subsystem essentially intact, subject to actual licence verification. |
| **MODIFY** | Adapt a useful structure into original NoöPunk rules. |
| **REPLACE** | Use a different NoöPunk-specific system. |
| **OMIT** | Do not include the proposed subsystem. |
| **DEFER** | Record an unresolved decision; do not silently implement a default. |

Required review sequence: compare source, examine existing author decisions, write and stabilize a **tabletop** rule, then specify/test and finally port to Godot or Concordia. No bulk engine migration or automatic CWN/SWN class, level, saving throw, or 2d6 adoption. Track individual reviews in [#568](https://github.com/TomiToivio/NooPunk/issues/568).

## Skills: #22 = MODIFY (historical approved decision)

[#22](https://github.com/TomiToivio/NooPunk/issues/22) specifies trained skills at **levels 0 through 4**, distinct from **unskilled**: unskilled permitted attempts receive **−1**; trained-only attempts are **BLOCKED**. Trained level 0 adds +0, level 1 adds +1, through level 4 adding +4. This superseded the then-temporary model where level 0 meant unskilled. Do not confuse it with the *attribute scale*, and do not migrate other subsystems by implication.

#22's initial CWN-inspired list was: Administer, Connect, Drive, Exert, Fix, **Medical** (from Heal), **Science** (from Know), Lead, Notice, Perform, Program, Punch, Shoot, Sneak, Stab, Survive, Talk, Trade and Work. It does **not** authorize any other renames, splits, or additions at that stage. It explicitly deferred specializations (e.g. Science/Work fields), background picks, repeat picks, caps, XP costs, Focus benefits, NPC bonuses, and advancement. It kept CYB plus skill plus separately reviewed equipment/context modifiers for cyberspace; Program was a candidate, not a universal hacking rule.

**Important newer-state distinction:** `data/rules/core.json` and `data/rules/skills.json` contain a *different*, later #159 universal skill vocabulary, and the independent #111 1d10 kernel describes stats/skills on a 1–10 scale. `strategy_game/rpg/` implements Fate-rated skills. **Do not silently overwrite any of these with the historical #22 list.** The mapping matrix must reconcile #22 and those subsequent decisions explicitly, identifying migrations and author approval as necessary.

## Attributes and check resolution: decisions still open

In #19/#22, the *then-current design intent* named FIT/REF/INT/**CHA**/CYB/PSY, ordinary human 3d6 attribute generation, −3…+3 human modifiers, and **3d6 + attribute modifier + skill** checks, preserving the existing difficulty ladder. Those statements remain a historical design record, **not an accurate description of the present executable rules**.

The [current inventory](RPG_CHASSIS_INVENTORY.md) documents:

| Implemented layer | Rating model | Resolution | Status |
| --- | --- | --- | --- |
| Legacy tabletop (`src/rules/`, `RULEBOOK.md`) | FIT/REF/INT/**SOC**/CYB/PSY | STAT + Skill + **1d10** versus DV | Independent since #111; canonical within that layer |
| Crossover RPG (`strategy_game/rpg/`) | COG/INT/REF/SAV/SOM/WIL skills | **4dF** + rated skill | Approved Fate design under #389/#482 |
| Board/tactical (`strategy_game/tabletop/`) | Dice notation and cards, not player stats | Generic dice pools | Separate supported layer, **not** an RPG chassis |

The 3d6 helper in `src/rules/_retired.py` generates attributes, **not core checks**. SOC is an intentional later replacement of CHA in the legacy layer. Existing code should remain unchanged while [#566](https://github.com/TomiToivio/NooPunk/issues/566) is open. The epic's request to preserve a “present 3d6 core check” cannot be achieved by preserving an implemented behavior that does not exist.

## Ruling (#566, 2026-10-25) — **CONFIRMED by the author**, and reversible by one word

*Confirmed 2026-10-25 by explicit author choice, not inherited from the provisional record. The scope answer below is now final for #564: **layer A only**, `1d10` stays, `4dF` stays for layer B. The provisional framing was correct and is no longer provisional.*

The epic was asked for three times while this stayed open, so the conservative answer was taken rather than a
fourth request for one line. **Every item below is a scoping statement, not a rewrite: no die changes, no test is
retired, and no approved decision is reversed.** If the author says otherwise, the reversal is a single
follow-up issue — that is what makes this safe to take provisionally.

| question | ruling | why this one |
|---|---|---|
| **Scope** | **Layer A only.** Layer B stays the approved Fate crossover (#389/#482). Layer C remains an independent board module. | It is the only answer that reverses nothing. "Both + one die" requires retiring an approved kernel, re-authoring every DV and wound band and rewriting `strategy_game/RULEBOOK.md` — too large to take as a default. |
| **Core dice** | **Keep `1d10`** for layer A (`STAT + Skill + 1d10 ≥ DV`, #111). `4dF` remains for layer B. | The Without Number family's value here is *procedures*, not a die: Effort, Foci, Shock/Trauma, access prerequisites, morale, mission clock — all expressible over the existing kernel. A die swap re-derives every threshold for no mechanical gain. |
| **Attributes** | **Keep `FIT / REF / INT / SOC / CYB / PSY`.** No `CHA`, no adoption of `STR/DEX/CON/INT/WIS/CHA`. | `CYB`, `PSY` and `SOC` have no slot in the WN six; adopting that set would delete the three attributes that make the sheet NoöPunk. |
| **Classes / levels** | **Declined.** No class field, no levels, no XP thresholds. **Edges are admitted** (author ruling 2026-10-25): classless, purchased, author-authored entries — the *structure* of "one shared frame + purchased traits" the earlier text anticipated, now named. | The epic forbids them; AWN's text is not reusable (no SRD, #569) and CWN's is CC0 but still third-party expression. |

**What this unblocks:** rows 5, 12, 16, 22 and 25 of the matrix can be written as procedures over the existing
kernel; rows 1, 14, 15 and 28 close; #572's worked examples can be authored against a settled scope.

**What it does not do:** it does not claim a single unified kernel for the whole project. Layer A and layer B
still resolve differently, and the honest description is *one setting with two playable layers*, with this file
as the conversion appendix between them. If the author wants one game with one die, that is the reversal above.

**Precedent note:** this ruling must not be cited as author approval for any *mechanic*. It settles scope and
vocabulary only; every numeric subsystem remains `DEFER` until the author rules on it.

## Per-subsystem review template

For each item record: `subsystem | KEEP/MODIFY/REPLACE/OMIT/DEFER | rationale | exact CWN/SWN SRD reference and licence status | current file/implementation | migration status | author decision link`. Cover attributes, skills, check resolution, resistance/saves, initiative/actions, combat, injury/trauma/healing, armor/weapons/equipment, cyberware/BCI, hacking/access/Blackwall, drones/vehicles, chargen, advancement, encounters, investigation/social interaction, factions, NPCs, missions, and the biological/social/psychic NoöPunk extensions. If blocked by #566, write **DEFER** and the exact dependency; never fill gaps by importing default CWN rules.

## Compatibility and safety

Keep all current layer-specific character/scenario contracts stable while the decision is pending. Migrations require separate versioned adapters and reproducible non-LLM playthrough tests ([#570](https://github.com/TomiToivio/NooPunk/issues/570)), including Helsinki/UNSA and Ubiquitous Maniacs. Do not copy from uploaded commercial CWN/SWN editions or assume SWN text shares CWN SRD rights. Follow the rights audit in #569.

**This file restores the missing policy record and records one provisional scope ruling. It does not change the rules of play.**

---

## Three further author rulings (2026-10-25) — what kind of import this is

The four answers above settle *scope*. These settle *character*, and two of them reverse earlier
agent recommendations.

### 1. Hacking runs on a **ubiquitous network**, as NoöPunk already has it

CWN's matrix-like reachability **is not adopted**. NoöPunk's assumption stands: the network is
ambient, so **access is not the scarce thing**. `strategy_game/cyber.py` already decides reachability
*before* any resolution check, and that ordering is canonical.

**Consequence:** CWN contributes the *resolution procedure* for an intrusion, never the *access
model*. Any row that made "can you reach it?" the interesting question imports the wrong setting.
This **supersedes** the earlier suggestion in `ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` that CWN's
access prerequisites could stand in for physical ingress.

### 2. PSI = **SWN's rules**, for a **learnable natural human ability**

- **Mechanically:** SWN's structure — **Effort** as a committed pool, techniques that commit and
  release it.
- **Ontologically:** a **natural human ability that can be learned**. Not a virus, not an implant,
  not a class feature, not a caste-exclusive discipline.

So **Effort is adopted** and NoöPunk's origin story is preserved as the fiction. This supersedes
"DEFER Effort" in `ISSUE_572_NOOPUNK_EXTENSIONS.md` and answers the PSI half of **D36**.

**Must not follow the import:** that PSI is rare, that it is a separate progression track, or that
only a psychic class may hold it. Anyone may learn it; the pool makes the price legible.

**Licensing note:** using SWN's *rules pattern* is not permission to copy SWN text, tables or
technique names — SWN stays `blocked-unverified` (#569). Effort must be implemented independently from
the described mechanic.

### 3. Where the family has **no equivalent**, author a **new NoöPunk subsystem**

The default is no longer "KEEP-ORIGINAL and leave it as prose". If CWN/SWN/AWN/WWN has no equivalent,
the answer is a **NoöPunk-native subsystem** of its own, not a forced conversion row.

Directly affected: Noösphere / cross-domain state, psychotronics, NHI contact, AGI/ASI, crisis-era
network topology. Each needs its own spec, and each must stay deterministic and tabletop-convertible
(no LLM in the loop, per the #570 harness).

---

## Still open after these rulings

| Question | Where |
| --- | --- |
| Effort pool size, and what overspend costs | D36 (PSI half answered in kind; numbers `OPEN`) |
| Does an implant have a capacity limit (non-PSI half)? | D36 |
| How many Edges, how often, chosen or Lifepath-bound? | D23 |
| Which access tiers a ubiquitous network distinguishes, and what each unlocks | #572 |
| The subsystem specs themselves | #572 |

Gates A–D stay open. Nothing here approves a number.
