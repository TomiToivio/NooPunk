> **Rules superseded, 2026-10-26:** [Without Number baseline v1](../../rulebook/WITHOUT_NUMBER_BASELINE.md) is the current mechanical authority under the author’s explicit CWN/SWN/AWN/WWN instruction. Conflicting stats, skills, dice, custom rules and approval gates below are historical. Preserve the setting material. Existing software remains legacy until ported.

# Without Number family: NoöPunk rules direction (#615)

> **Status:** author-approved **design direction**, not a new executable engine, license choice, or permission to replace established rules. Implementation is tracked through [#564](https://github.com/TomiToivio/NooPunk/issues/564). The legacy RPG and crossover retain their distinct approved rules until separately migrated.

## Source priority and genre modules

The *Without Number* family is the **first source of comparison** for future NoöPunk tabletop mechanics: **Cities Without Number** (CWN) is primary and **Stars Without Number** (SWN) co-primary. **Worlds Without Number** (WWN) and **Ashes Without Number** (AWN) are setting-conditional modules, not alternative engines.

| Source | Fictional locations and pressures | Procedures to evaluate, not automatically import |
| --- | --- | --- |
| CWN | Helsinki/other cyberpunk cities, UNSA investigation, BCI, networks | urban missions, access constraints, cyberware, lethal consequences |
| SWN | solar-system colonies, extraterrestrials, NHI factions, PSI | alien/space encounter tools, psionics and Effort analogues, faction turns |
| WWN | Noösphere, interdimensional travel, Law of One-influenced weirdness | exploration, world tags, extraordinary Effort/Foci analogues; **not** generic fantasy magic |
| AWN | *local* NHI Crisis ruins, isolated territories and infrastructure failures | salvage, scarcity, survival, dangerous ruins; **not** a global Fall |

**One character, one current game's engine.** A character can traverse all four types of environments in a single scenario without changing sheets, dice conventions, advancement, or injury systems. Genre changes which situations and supplemental procedures arise, never which game is being played. The existing legacy RPG and crossover are **still separate games sharing a world** (AGENTS.md §0); this is **not** an authorization to merge them.

## Design influences and the three balances

- **Gamism/OSR:** risks, meaningful choices, resources and fair referee procedures, principally from CWN/SWN.
- **Simulationism:** causal, technological and transhuman consequences, inspired by *Eclipse Phase*.
- **Narrativism:** character stakes, narrative consequences and fiction-first techniques, inspired by *Fate Core*, *Transhumanity's Fate*, *Apocalypse World* and *The Veil*.

The **source hierarchy** names where we look first for mechanics; it does **not** specify percentages of play. The earlier [three-balances principle](archive/DESIGN_PRINCIPLES.md) describes equal *design* weight across Gamism, Simulationism and Narrativism, while #615 describes Gamism/OSR as a **mechanical backbone**. Treat this as a **wording/tension to reconcile editorially**, not as permission to replace the prior invariant with a numeric Gamism majority.

Fate/PbtA techniques, such as aspects, clocks, consequences and player-facing decisions, are candidates for compatible optional procedures; they are **not** an automatic second roll system. Eclipse Phase is a simulation and fiction reference; do not copy NC-licensed expressive content into the reusable core.

## Implementation compatibility ledger

These rows document **current defaults and explicit decisions**. A candidate marked **DEFER** needs a design review before implementation, even if a source game has a ready-made solution.

| Area | Existing NoöPunk authority | #615 direction | Decision / gate |
| --- | --- | --- | --- |
| Legacy core rolls | `src/rules/` and `data/rules/core.json`: 1d10 + STAT + skill vs DV | compare CWN procedures | **KEEP** existing resolution; **DEFER** any die change |
| Legacy attributes | FIT/REF/INT/SOC/CYB/PSY | maintain distinct NoöPunk identity | **KEEP**; do not restore historical CHA |
| Crossover RPG | `strategy_game/rpg/`: approved Fate/4dF under #389/#482 | Without Number as long-term comparison | **KEEP** Fate until a separately approved crossover migration |
| Skills and advancement | #22, later #159 and current per-game rules disagree | compare CWN skill bands, Edges/Foci | **DEFER** reconciliation; no bulk skill/class/level migration |
| Hacking and BCI | existing physical ingress, device distinctions and network constraints | CWN access inspiration | **MODIFY** in original NoöPunk terms after subsystem decision |
| PSI | natural powers, psychotronics and direct BCI | SWN/WWN Effort candidates | **DEFER** resource and competence formulas; preserve three pathways |
| NHI, contact and social systems | canonical NoöPunk factions, biological/social/psychic model | SWN faction procedures, WWN anomalies | **MODIFY** only after tabletop design and author sign-off |
| Crisis territories | no worldwide Fall, functioning institutions | AWN situational salvage/survival | **MODIFY** as opt-in scenario procedures |
| Aspects, fronts, clocks, complications | Fate and PbtA influences | narrative agency without parallel engine | **DEFER** optional rules and compatibility |
| Combat, trauma and progression | divergent legacy/crossover implementations | WN lethality and risk models | **DEFER** until #564 subsystem decisions and playtesting |

See [CWN_CHASSIS.md](../CWN_CHASSIS.md), [RPG_CHASSIS_INVENTORY.md](../RPG_CHASSIS_INVENTORY.md), and the open #564 implementation epic for detailed records.

## Mixed-genre tabletop playtest: one sheet, no invented mechanics

An UNSA investigator starts in **Helsinki** (urban digital evidence), travels to an **NHI Crisis exclusion zone** (resource and connectivity limits), visits an **extraterrestrial installation** (contact, negotiation and unusual PSI), and enters a **noetic realm** (altered perception and ontological uncertainty).

Run all four scenes using the **same existing game's character sheet and approved resolution rules**. For each scene the referee records: fictional stakes; which established skill/action handles it; which, if any, *proposed* genre procedure would improve play; whether it added tracking overhead; and whether it changed player agency or risk. No unapproved numerical modifier, new resource track, or source-book rule is required to conduct this first editorial playtest.

**Acceptance observation:** changing environments neither resets injuries nor replaces the dice engine, and all consequences persist. Follow up with actual playtest notes before moving any candidate from DEFER to MODIFY/KEEP.

## Gradual independence

1. **Inventory and provenance:** compare each existing subsystem against its inspiration (KEEP / MODIFY / REPLACE / OMIT / DEFER).
2. **Stable tabletop contract:** specify one core *within each approved game scope*, documenting any intentionally shared modules.
3. **Mixed-genre playtests:** measure speed, lethality, causal fidelity, narrative choices, cognitive burden and cross-setting coherence.
4. **Original NoöPunk system:** replace or reinterpret adopted procedures where playtest results justify it; version migrations and publish independent NoöPunk wording. Independence is **not** achieved by merely changing names.

Do not create documentation-matching automated tests. Test **executable** mechanics only when approved and implemented, per [AGENTS.md](../../AGENTS.md).

## Credits, reuse and release gate

> NoöPunk is an independent fictional setting and developing RPG project. Its intended tabletop mechanics draw primarily on *Cities Without Number* and *Stars Without Number* by Kevin Crawford / Sine Nomine Publishing, with setting-specific inspiration from *Worlds Without Number* and *Ashes Without Number*. Further inspirations include *Eclipse Phase*, *Transhumanity's Fate*, *Fate Core*, *Apocalypse World* and *The Veil*. NoöPunk is unofficial and is not endorsed by, or affiliated with, the cited creators or publishers.

This statement is a **credit and disclaimer, not a license**. Public SRDs, free editions and play aids have different reuse conditions. See the public-source links catalogued in [#615](https://github.com/TomiToivio/NooPunk/issues/615), the rights ledger `data/sources/game_system_rights.json`, [ATTRIBUTION_POLICY.md](../ATTRIBUTION_POLICY.md) and `docs/licenses/` before copying **any** text or release material. The project's own code/content license selection is **still undecided**. No third-party art, setting, protected prose or unverified text is authorized for import here.

## Editorial acceptance checklist

- [x] Hierarchy and four environment modules documented without changing existing game mechanics.
- [x] Legacy/crossover decisions cross-referenced, including explicit conflicts and deferred questions.
- [x] Initial provenance and adaptation ledger with nonautomatic reuse decisions.
- [x] Four-location tabletop playtest itinerary requiring only a single existing character sheet.
- [x] Candidate narrative/simulation techniques and release disclaimer recorded.
- [ ] Playtest with actual results and agree on unresolved mechanical decisions.
- [ ] Implement approved modules, add runtime behavioral tests, and migrate scenarios.
- [ ] Select/verify applicable licenses and release notices in the existing rights workflow.
