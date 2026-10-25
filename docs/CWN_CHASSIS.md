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

## Pending author rulings (#566)

- **Scope:** layer A, layer B or both? Layer C remains an independent board module unless separately changed.
- **Core dice:** keep 1d10, keep 4dF, adopt CWN 2d6, revive 3d6, or specify another mechanic? This is a design ruling, not a default.
- **Attribute vocabulary:** SOC versus CHA; layer B skill-only ratings versus character stats.
- **Classes/levels:** no standard class or character-level migration without explicit approval.

Until these are decided, no claim of a single unified playable kernel is warranted. In particular, **do not retcon an approved Fate crossover into a deprecated engine solely from this policy file**.

## Per-subsystem review template

For each item record: `subsystem | KEEP/MODIFY/REPLACE/OMIT/DEFER | rationale | exact CWN/SWN SRD reference and licence status | current file/implementation | migration status | author decision link`. Cover attributes, skills, check resolution, resistance/saves, initiative/actions, combat, injury/trauma/healing, armor/weapons/equipment, cyberware/BCI, hacking/access/Blackwall, drones/vehicles, chargen, advancement, encounters, investigation/social interaction, factions, NPCs, missions, and the biological/social/psychic NoöPunk extensions. If blocked by #566, write **DEFER** and the exact dependency; never fill gaps by importing default CWN rules.

## Compatibility and safety

Keep all current layer-specific character/scenario contracts stable while the decision is pending. Migrations require separate versioned adapters and reproducible non-LLM playthrough tests ([#570](https://github.com/TomiToivio/NooPunk/issues/570)), including Helsinki/UNSA and Ubiquitous Maniacs. Do not copy from uploaded commercial CWN/SWN editions or assume SWN text shares CWN SRD rights. Follow the rights audit in #569.

**This file restores the missing policy record only. It does not change the rules of play.**
