# NoöPunk extensions vs Without Number (#572)

**Status:** compatibility documentation only. No rule or runtime change; conversion remains gated on #566. Source boundaries: `docs/CWN_CHASSIS.md`, `docs/design/ISSUE_564_CWN_SWN_MIGRATION_AUDIT.md` and the rights matrix `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`.

| Extension | Existing owner and present mechanic | Without Number comparison | Verdict |
| --- | --- | --- | --- |
| Cyberware / BCI | Layer A `src/rules/equipment_catalog_index.py` and `rulebook/5_CYBERNETIC.md`; layer B `strategy_game/cyber.py` models connectivity and `strategy_game/rpg/` resolves scenes | CWN cyberware and resource strain are **candidates**, not imported defaults; BCI cognition is not identical to implant tolerance | MODIFY, subject to #566 |
| Intrusion / Blackwall | `strategy_game/cyber.py` decides reachability *before* any resolution check; the eras distinguish acceleration, NHI crisis and aftermath | CWN hacking presumes explicitly reachable access paths, but cannot replace NoöPunk's changing network graph by a global virtual network | KEEP-ORIGINAL access gate, MODIFY later skill resolution |
| Natural PSI | `strategy_game/rpg/psi.py`: capability-tag permission, then Fate action with rating, consensus and psychic pressure; `strategy_game/psi_operations.py` owns mission-level operations | SWN psychic abilities and WWN Effort are possible resource *patterns*, not natural-PSI ontology | KEEP-ORIGINAL natural origin and permissions; DEFER Effort |
| Psychotronics | Technology-mediated PSI in current design/rulebook; distinguish device access and effects from an innate ability | No complete counterpart covering all ontological and social constraints | KEEP-ORIGINAL |
| Noösphere / cross-domain | `src/rules/noospace_projection.py`, `src/rules/cross_domain_state.py` (explicitly **provisional, non-canonical**), and `rulebook/18_CROSS_DOMAIN_STATE.md` | No equivalent single-locus, gateway and realm-action contract | KEEP-ORIGINAL, do not promote provisional numbers |
| AGI/ASI and NHI contact | Existing narrative/campaign ontology (`rulebook/11_ONTOLOGY.md`, `12_BEINGS.md`), strategy and mission boundaries | SWN optional AI/alien material is not NoöPunk lore; avoid protected setting imports | KEEP-ORIGINAL |
| Crisis scarcity and salvage | Campaign has a pre-collapse transition, not a universal post-apocalypse | AWN survival/salvage is an optional comparison, not evidence of a total Fall | DEFER optional procedures |

## Network access contract

1. Identify era and target connectivity; classify isolated/local-only/proxied/networked reachability.
2. Prove an actual technical ingress route (local physical contact, authorized connection, proxied link, or an explicitly modeled breach). **A social graph tie is never a TCP/IP connection.**
3. If no route exists, the attempt is *impossible*, not merely a high-difficulty roll. A remote actor cannot overcome an air gap with lucky dice.
4. Distinguish ordinary unauthorized intrusion from the separate containment/Blackwall breach offence. Only after eligibility and legal consequences are established may the relevant layer's skill resolution run.
5. A physically carried device, drone or courier can establish a *new, specifically modeled* path. It does not retroactively make all disconnected targets reachable.

This stays deterministic: target and path data determine the gate, and a seeded resolver determines any subsequent contested check. No LLM is required.

## PSI is not a single skill

Layer A has the PSY attribute and relevant skills; individual permission and cost need an approved tabletop rule. Layer B already uses **capability tags as permission**, the normal Fate action as resolution, and **psi rating / consensus / pressure** as modifiers and consequence. A technology-driven psychotronic session requires a device and may be used by someone who lacks natural PSI. BCI telepathy is a third communications mechanism, mediated by an actual connection. Natural PSI is **not virus-derived** (#482).

WWN-style committed Effort could become a *resource* for sustained PSI/BCI effects, but its amount, refresh, stacking and compatibility with existing pressure/stress are **unapproved**. Do not substitute CWN's bodily System Strain for cognitive burden without an explicit mapping. An ongoing effect must be cancellable, trackable on paper, and reproducible after save/load.

## Gate before implementation

Resolve #566 (scope, dice, attributes, classes/levels); then publish specific tabletop examples and acceptance tests for a physical intrusion, an air-gapped target, a natural PSI attempt, a psychotronic device, a BCI-mediated message, and an astral transition. Preserve the faction-turn boundary and single-locus prohibition. Every example must work offline and without a generative model.
