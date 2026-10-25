# Issue #572 — acceptance record

**Checked against `main` at `d2c960d`, 2026-10-25.** The issue's own four work items, each with the
artefact that satisfies it. Where something is *not* closed, it is named in §5 with its owner row — an
acceptance record that hides an open number would be worse than none.

## Criterion

| # | the issue asks for | evidence | met |
| --- | --- | --- | --- |
| 1 | for each extension: what it does mechanically today, which layer owns it, whether CWN/SWN has any equivalent, and a `KEEP-ORIGINAL` verdict where none | **§1** table (six extensions) + [`docs/rules/ISSUE_572_NATIVE_SUBSYSTEMS.md`](../rules/ISSUE_572_NATIVE_SUBSYSTEMS.md) §4 | yes |
| 2 | show where CWN's matrix-like hacking is incompatible with NoöPunk's disconnected devices, and what a network-access subsystem must **add** for the NoöPunk assumption to hold | **§2** (six incompatibilities, seven requirements, each mapped to code + test) | yes |
| 3 | state whether PSI is a skill, a resource, a permission or a separate subsystem **in each layer**, without overwriting #482's natural-not-virus finding | **§3** (three layers, explicit invariant) | yes |
| 4 | keep every extension deterministic and tabletop-convertible: no LLM in the loop | **§4** (43 code tests, sealed against network + model) | yes |

The implementation gate ("after the scope decision") was discharged by **#566**, closed 2026-10-25:
layer A only, `1d10` stays, six STATs, classes declined, Edges admitted, and the three import rulings
(hacking on a ubiquitous network; PSI = Effort for a learnable natural ability; new subsystems where
the family has none). Recorded in [`ISSUE_566_ACCEPTANCE.md`](ISSUE_566_ACCEPTANCE.md).

---

## 1. The six extensions the issue names

Layer **A** = the legacy tabletop game (`src/rules/`, `rulebook/`). Layer **B** = the crossover
(`strategy_game/`). "Family" = CWN/SWN/AWN/WWN.

| extension | what it does mechanically **today** | owned by | family equivalent | verdict |
| --- | --- | --- | --- | --- |
| **AGI / ASI** | `ubiquitous_network.OPPOSITION` carries §22.6.4's four tiers (wants / acts / costs / survive-by / leaves) as data; `can_notice()` refuses Thanatos without a material path; `scene_guarantees()` fixes *leaves evidence / refusal is real / never save-or-die* | A | **none** — SWN's AI tags are setting-specific and its text is licence-blocked | `KEEP-ORIGINAL` |
| **NHI contact** | `noopunk_social_extensions.NHIContact` (sibling, #597) + prose canon `11_ONTOLOGY.md`, `12_BEINGS.md`; contact is an ontological event, deliberately not a check | A | **none** | `KEEP-ORIGINAL` |
| **PSI** | A: `natural_psi.py` — six PSY skills, training gates, Effort, pressure, consensus. B: `strategy_game/rpg/psi.py` — capability-gated modes on `4dF` | A + B | SWN sells *virus-derived* psionics with classes and power lists — the wrong ontology, and blocked text; CWN has none; WWN supplies the **Effort pattern** (CC0) | `KEEP-ORIGINAL` for the ontology; `MODIFY` for the cost shape (WWN pattern, independently implemented) |
| **Psychotronics** | 43 catalogue entries (`equipment_catalog_index`, psychotronic category) and `rulebook/17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md`; **no resolution channel exists** | A | **none** | `DEFER` — device channel needs a ruling (§5, D43 candidate) |
| **Cybernetic cognition / BCI** | reachability and access classes (`strategy_game/cyber.py`); capability-level rules in `rulebook/5_CYBERNETIC.md` | B (reach) + A (cognition) | CWN's **System Strain is bodily** — the wrong axis for a cognition hazard; SWN has nothing | `KEEP-ORIGINAL`; Effort-as-BCI-load is a `DEFER` candidate (D36) |
| **Noösphere** | `noospace_projection.py` (regions, navigation DV, elapsed time) and `cross_domain_state.py` (locus, transitions, body control) — **both `IS_CANONICAL = False`** | A | **none** | `KEEP-ORIGINAL` (provisional by design) |
| **Crisis-era network constraints** | A: `ubiquitous_network.py` — reach table, era dial, exposure economy. B: `cyber.py` — access gate on `connectivity.json` | A + B | CWN assumes a matrix; **none** supplies disconnected-device canon | `KEEP-ORIGINAL` |

Two entries carry a `DEFER` *inside* a `KEEP-ORIGINAL` verdict on purpose: the extension's **ownership**
is canonical, while a **number or channel** inside it is not yet decided. That is the distinction the
matrix exists to keep.

## 2. CWN's matrix vs NoöPunk's disconnected devices

### 2.1 Where the abstractions are incompatible

| # | CWN assumes | NoöPunk canon says | what importing it would do |
| --- | --- | --- | --- |
| 1 | the network is a **place you enter** (a matrix, a deck, an interface) | networks have **geography** — route × target × era (§22.5) | turn a setting into a mini-game |
| 2 | access is **an action you roll** | reach is decided by **where you are**, never by a skill rating (§22.5) | let a die cross an air gap |
| 3 | **programs** are the resource (CPU / memory / access) | ubiquity ⇒ **exposure**; there is no concealment to buy | replace the setting's pressure with a hardware budget |
| 4 | **Alert** is a clock you buy down | exposure accrues; the four tiers decide **who is noticing** (§22.6.4) | make Thanatos optional, make a police report skippable |
| 5 | **cyberware is the door** | physical ingress; a disconnected device is a wall (§22.5.1, #344) | make an implant a universal key |
| 6 | the network is **one topology** | Safenet + the Blackwall + the quarantine are three different legalities (§22.3) | flatten a crime into a penalty |

### 2.2 What a "network access" subsystem must **add** for the NoöPunk assumption to hold

Each requirement is implemented and pinned; none of them is a number.

| # | requirement | implementation | test |
| --- | --- | --- | --- |
| R1 | a route × target × era **gate**, never a difficulty | `reach()`, `REACH_TABLE` | `test_the_table_matches_the_chapter_for_every_public_pair` |
| R2 | **isolation is absolute**: `isolated` = class 1 only, every era, every skill | `REACH_TABLE[ISOLATED]` | `test_isolated_is_reachable_only_by_class_one_in_every_era` |
| R3 | an **era dial** so ubiquity is a setting, not a guarantee | `safenet_up()`, `coverage()` | `test_the_public_network_can_be_down_and_only_that_changes` |
| R4 | an **exposure economy** that only Cover reduces, never below zero | `IntrusionSession`, `alert_state()` | 3 exposure tests |
| R5 | a quarantine **breach** as a separate illegality, always possible and always a crime | `CONTAINMENT_BREACH_CLASSES`, `can_notice()` | `test_class_five_is_always_possible_and_always_a_breach` |
| R6 | the **four-tier opposition** with material preconditions for Thanatos | `OPPOSITION`, `can_notice()`, `scene_guarantees()` | 5 opposition tests |
| R7 | the **shared** action clock, never a second economy | `AP_PER_EXCHANGE` consumed from `cross_domain_state` | `test_ap_is_the_shared_clock_and_does_not_carry` |

## 3. PSI, stated per layer

| layer | a skill? | a resource? | a permission? | a separate subsystem? | code owner |
| --- | --- | --- | --- | --- | --- |
| **A** — legacy tabletop (`STAT + Skill + 1d10`) | **yes** — the six PSY skills are the disciplines (#159) | **yes** — Effort, committed capacity (proposed; D42) | no | yes — `src/rules/natural_psi.py` (`IS_CANONICAL = False`) | `src/rules` |
| **B** — crossover (`4dF + skill`) | **no** — PSI modes resolve against the six engine skills (COG/INT/REF/SAV/SOM/WIL) | no pool; Fate stress and consequences carry the cost | **yes** — a capability tag gates a mode, checked **before any die** | yes — `strategy_game/rpg/psi.py`, 13 modes | `strategy_game` |
| **C** — strategy (`strategy_game` simulation) | no | no | no | **no** — deliberately: PSI does not enter the political simulation | — |

**The #482 invariant, kept in both layers:** PSI is **natural, not virus-derived** (`rulebook/6_PSYCHIC.md`
§6.1). Layer A gates on **practice hours**, not birth; layer B gates on a **capability tag**, not a class
or an infection. Both refuse *before* any dice, so neither can be "rolled past". No family import
overwrote it.

## 4. Determinism and tabletop convertibility

- `tests/test_issue572_native_subsystems.py` — **27 tests**: the reach table is checked as all 5 × 5
  pairs plus `isolated` across 5 routes × 3 eras; then the exposure contracts, training gate, Effort
  bookkeeping, mastery, consensus, opposition and replay determinism.
- `strategy_game/tests/test_issue572_extension_contracts.py` — **16 tests** (the six worked examples,
  offline, capability gates before dice).
- No test touches a network, a socket or a model: the playthrough harness runs every scenario under an
  audit hook that refuses sockets and processes, and the layer-A modules take `rng: random.Random`
  explicitly, so determinism is testable rather than asserted.
- Convertible at a table with **one d10** (layer A) or **4dF** (layer B); every procedure is stated as
  arithmetic a human can do by hand, and the docs give the steps in words (§2.3 and §3.2 of the rules
  record).

## 5. What this record does **not** close — and who owns it

| item | why it is not part of #572's criterion | owner |
| --- | --- | --- |
| **D41** exposure bands and costs | numbers, not documentation; the *mechanism* is proven | author |
| **D42** Effort curve + practice thresholds | same | author |
| **D36 / BCI as Effort load** | a mechanism choice inside a KEEP-ORIGINAL extension | author |
| **Psychotronic device channel** | needs a ruling that a device session is *not* natural PSI; today it is catalogue + gap test | author (D43 candidate) |
| **D23 + the Edges mechanism** | admitted by the #566 ruling; no registry/count exists yet | author |
| Gates A–D | the epic's own gates; unchanged by this record | author |

## 6. Honesty notes

1. **Two prototypes exist.** A sibling landed `src/rules/noopunk_extensions.py` (#593) the same day.
   Both are merged; the division is written down in §7 of the rules record — that module is a
   scenario-level **link graph**, `ubiquitous_network.py` / `natural_psi.py` are the **rules owners**.
2. **Three non-canon discipline names** in that sibling module (`influence`, `healing`, `shielding`)
   are flagged at its top and in §7; no rule may be built on them until the author adds them.
3. **The psychotronic worked example is documentation plus a pinned gap test**, not a working channel.
   It is listed as such rather than presented as implemented.

— Ai (愛)
