# NoöPunk's own subsystems: the ubiquitous network and natural PSI (#572)

**Status: PROVISIONAL implementation + design record. Nothing here is canon, and every number is the
author's.**

`AGENTS.md` §4 reserves *hacking / cyberspace mechanics* and *psionic powers or psionic mechanics*
until the author defines original subsystems. **The author ruled on 2026-10-25** (#566, recorded in
[`ISSUE_566_ACCEPTANCE.md`](../design/ISSUE_566_ACCEPTANCE.md) and `docs/CWN_CHASSIS.md`):

1. **scope = layer A only**; layer B keeps its approved `4dF`;
2. **`1d10` stays** — `STAT + Skill + 1d10 ≥ DV` (#111), no die replaced;
3. **`FIT/REF/INT/SOC/CYB/PSY` survive**; `CHA` is not adopted;
4. **classes and levels declined**, with **Edges admitted** as the classless differentiation mechanism;

and three rulings that decide what kind of import this is: **hacking runs on a ubiquitous network**
("access is not the scarce thing; CWN supplies the resolution procedure only, never the access
model"), **PSI = the family's rules for a learnable natural human ability — Effort adopted, ontology
preserved**, and **new NoöPunk subsystems wherever the family has no equivalent**.

Both modules below implement exactly that direction. The *numbers* are still the author's (D41/D42),
and gates A–D stay open. It is a **proposal with running code**, not a
ratification: `IS_CANONICAL = False` in both modules, and the TUNING blocks below are the author's to
set.

| file | what it is |
| --- | --- |
| `src/rules/ubiquitous_network.py` | the reach gate, the era dial, the exposure economy |
| `src/rules/natural_psi.py` | disciplines, training, Effort-shaped cost, pressure, consensus |
| `tests/test_issue572_native_subsystems.py` | 22 code tests pinning both |

---

## 1. The design thesis: two ubiquitous fields, two different constraints

NoöPunk's setting has **two ambient networks**: the technical one (mesh, IoT, Safenet, the Blackwall)
and the psychic one (the Noösphere, Noöspace). The family's games have neither: CWN assumes a
*matrix* you enter, SWN a *ship computer* you slice, WWN a *spell list*. So the NoöPunk question is not
"can you reach the network" — in 2045 you almost always can — but:

- **technical ubiquity ⇒ exposure.** Everything logs. There is no concealment stat to buy; the only
  lever is how much of yourself you leave. That is `Exposure`.
- **psychic ubiquity ⇒ training.** Latent capacity is universal and unreliable (`rulebook/6_PSYCHIC.md`
  §6.1); what changes it is *practice*, not birth, not a class. That is `Training`.

Both subsystems therefore resolve on the **one canonical kernel** (`PSY`/`INT`/`CYB` + skill + `1d10`,
`src/rules/core.py`). Neither introduces a second die, a second action economy, or a class.

## 2. Hacking: the ubiquitous network

### 2.1 What canon already decides, and what was missing

`rulebook/22_CYBERSPACE_AFTER_THE_CRISIS.md` (#517) decides the geography:

- **five access classes** (§22.5.1) — how the operator *reaches* the target;
- **five connectivity classes** (#344, `strategy_game/data/connectivity.json`) — what the *target* is;
- the pairing table (§22.5.2) and its invariant: **`isolated` is reachable by class 1 only**, in every
  era, for every skill;
- class 5 (the quarantined old Internet) is a **containment breach**, a separate crime (§22.3.2);
- the four-tier opposition (ordinary security / Panopticon / Noösphere / Thanatos) means an encounter
  is *a scene with a price*, never a save-or-die (§22.6.4).

Missing: the arithmetic. `strategy_game/cyber.py` decides *whether* access is possible (the gate); it
does not model what an intrusion **costs**. This module adds exactly that and nothing else.

### 2.2 The reach gate (consumed, not re-decided)

`reach(target, access, era)` reproduces §22.5.2 as a table and adds the one thing the chapter states in
prose but does not encode: **the public network can be down**. Class 4 reaches nothing during the NHI
Crisis; class 3 still works. That single dial is what makes "ubiquity" a *setting* rather than a
guarantee, and it is why the crisis-era scenario can still have islands without an apocalypse.

Verified exhaustively by `test_the_table_matches_the_chapter_for_every_public_pair` and
`test_isolated_is_reachable_only_by_class_one_in_every_era`.

### 2.3 The exposure economy — what ubiquity costs

| quantity | TUNING constant | default |
| --- | --- | --- |
| AP per action (the **shared** clock, `rulebook/18`) | `TUNING_AP_PER_ACTION` | 1 of 3 per exchange |
| exposure for any attempt | `TUNING_EXPOSURE_PER_ACTION` | 1 |
| extra exposure per 2 points of margin | `TUNING_EXPOSURE_PER_MARGIN` | 1 |
| extra exposure for a failed attempt | (same constant, applied twice) | +1 |
| bought back by one Cover action | `TUNING_COVER_REDUCTION` | 2 |
| bands: quiet / watched / flagged / hunted | `TUNING_EXPOSURE_*_MAX` | 2 / 5 / 9 / beyond |

Three properties are contracts, not flavour:

1. **Exposure never falls except by Cover**, and never below zero (pinned).
2. **A failed attempt costs more than a quiet success** — carelessness is legible (pinned).
3. **The bands escalate in order** — a network that has noticed you is a different scene (pinned).

**Worked example** (non-canonical): an operator at `INT 5 / Program 5` on a `local_only` target via the
nearby envelope. `intrude(dv 15)` succeeds with margin +1 → 1 exposure, still quiet. A second action in
the same exchange is refused: AP do not carry. `cover()` spends the last AP and buys the exposure back
to zero — *the scene's shape is the spend order, not the die*.

### 2.4 What the family offered and why it was not imported

CWN's economy (cyberdeck CPU / Memory / Access, program verbs × subjects, Alert the Network) is a good
**procedure** and a wrong **ontology**: it presumes a discrete deck the operator carries and a target
you reach *as a network*, which is the opposite of NoöPunk's disconnected-device canon. Importing it
would make an air gap a difficulty rather than an impossibility, and would replace the exposure economy
(the setting's own pressure) with a hardware budget. WWN has no hacking at all; SWN and AWN are
licence-blocked for text and add nothing here.

## 3. PSI: a natural capacity that training makes reliable

### 3.1 What canon decides

- **PSI is natural, not viral** (§6.1) — a latent human capacity, weak and noisy in most people.
- **Training changes the probability** (§6.1) — the sentence this subsystem exists to implement.
- **The disciplines are the six canonical PSY skills** (#159): `ESP`, `Telepathy`, `Psychokinesis`,
  `Precognition`, `Psychic Defence`, `Noöspace`. There is no seventh "Psionics" skill and none is
  invented here.
- **Psychotronics is a separate channel** (§6.2): a device may amplify an operator, and a
  technology-mediated session is not natural PSI. This module deliberately does not model devices.

### 3.2 The three mechanics

| mechanic | what it does | why |
| --- | --- | --- |
| **Training** (`practice` hours → untrained / practised / mastered) | an untrained discipline is **refused before any die**; practised is usable; mastered costs one less psyche load on a failure | learnability is the mechanic, exactly as §6.1 says — and mastery is *reliability*, not a bigger number |
| **Effort** (committed capacity, `1 + PSY//2`, capped at 5) | a lasting effect holds capacity **until released**; an attempt may commit; release is explicit | the WWN **pattern** (CC0), independently implemented: a burden without a second hit-point track. NoöPunk's own `pressure` already exists; this gives it a budget |
| **Pressure & consensus** | failure and ties cost psyche load; witnesses shift the odds (capped ±2) | the Noösphere is social: an act is easier among believers, harder among doubters (§6.3.4's coincidence vocabulary) |

**What SWN would have imported wrongly**: a virus origin, a psychic *class*, a discrete power list, and
a separate psionics skill — four things that contradict §6.1 and #482's note that PSI is natural rather
than virus-derived. Its licence also forbids the text. What transfers is only the *shape* of a
committed cost, which WWN states in CC0 terms.

**Worked example** (non-canonical): a practitioner at `PSY 6`, `Telepathy 5`, 40 h of practice
(practised). `attempt(dv 15)` rolls `6 + 5 + 1d10`; a tie costs 1 psyche load and leaves a noetic trace.
Committing 2 Effort to "a watching thread" leaves `effort_free = 1` until it is released; a second 2-point
commitment is refused rather than overcommitted.

### 3.3 The TUNING block (the author's to set)

`TUNING_BASE_EFFORT 1` · `TUNING_PSY_PER_EFFORT 2` · `TUNING_MAX_EFFORT 5` ·
`TUNING_MIN_PRACTICE 20 h` · `TUNING_MASTERY_PRACTICE 120 h` · `TUNING_PRESSURE_PER_FAILURE 1` ·
`TUNING_PRESSURE_PER_TIE 1` · `TUNING_PRESSURE_RECOVERY_PER_SCENE 1` · `TUNING_BELIEVER_BONUS 1` ·
`TUNING_DOUBTER_PENALTY 1` · `TUNING_CONSENSUS_CAP 2`.

## 4. Subsystems with no family equivalent, mapped

The epic asks for explicit NoöPunk extensions where the family has **no** counterpart. For each: what
it does mechanically *today*, what the family offers, and what this round adds.

| extension | mechanical owner today | family equivalent | this round |
| --- | --- | --- | --- |
| **AGI / ASI** | `rulebook/22` §22.6 (three swarms), §22.7 AI law | none — SWN's AI tags are setting-specific and licence-blocked | **implemented as an opposition model** in `ubiquitous_network.py`: `OPPOSITION` (the four tiers' five columns as data), `can_notice()` (Thanatos needs a material path — no breach, no foothold, no appearance) and `scene_guarantees()` (leaves evidence, refusal is real, never save-or-die). No stat block, no numbers |
| **NHI contact** | `rulebook/11_ONTOLOGY.md`, `12_BEINGS.md`; scenario canon (§497) | none | **prose-only**: contact is an ontological event, and giving it a check would flatten it |
| **Noösphere / Noöspace** | `src/rules/noospace_projection.py`, `cross_domain_state.py` (both explicitly non-canonical) | none | **consumed, not promoted**: regions, navigation DV and elapsed-time arithmetic stay PROVISIONAL |
| **BCI cognition** | `strategy_game/cyber.py` reachability; `rulebook/5_CYBERNETIC.md` capability-level | CWN's System Strain is *bodily*, the wrong axis | **Effort is the candidate**: a sustained BCI load is committed capacity, not implant tolerance. Stays a proposal (queue D36) |
| **Crisis connectivity** | §22.4 Safenet, §22.5 geography, #344 classes | none | **the era dial**: `safenet_up()` and the ubiquity coverage table make "the network is down here" a switch, not a mood |
| **Psychotronics** | §6.2's continuum; `13_EQUIPMENT.md` lists devices | none | **separate channel, deliberately unmodelled** — a device-mediated session must not silently reuse natural-PSI rules |

### 4b. What the ruling admitted and this round did not build

The author admitted **Edges** as the classless differentiation mechanism, and that is now the largest
named-but-unbuilt piece: no Edge registry, no admission rule, no starting count exists in layer A
today. It is deliberately *not* improvised here, because count and frequency are **D23** and the
mechanism has to state what an Edge may do (a capability, a one-step shift, a permission) before any
list is written.

## 5. What stays the author's

Two queue rows are created by the TUNING blocks above, and neither is an agent's call:

- the **exposure bands and costs** (how loud is a failure, how much Cover buys back);
- the **Effort capacity curve and practice thresholds** (how fast a person becomes reliable).

Both are marked `TUNING_` in code, both are exercised by tests, and both are listed in
`docs/design/AUTHOR_DECISION_QUEUE.md`.

The **#566 gate is unchanged**: this round adds no class, no level and no second die, so it is
compatible with every branch of the decision — but if Q2 answers `2d6`, these two modules resolve on
`1d10` today and would need their kernel call swapped, which is exactly the one line both modules keep
isolated (`core.resolve_check`).

## 6. What this record does not do

- It does not lift the `AGENTS.md` §4 reservations by fiat; it records that the author asked for these
  subsystems and keeps every number PROVISIONAL until he sets it.
- It does not import CWN's deck economy, SWN's psionics, or any family text. WWN contributes a *shape*
  (committed Effort), which is CC0 and independently implemented.
- It does not touch `RULEBOOK.md`, `rulebook/`, or any existing runtime path.

## 7. Convergence: two prototypes landed for the same subsystem

A sibling session landed `src/rules/noopunk_extensions.py` (PR #593) on the same day, covering the same
territory. Both are merged, and leaving two engines would be the fork the repository forbids, so the
division is now explicit:

| module | role |
| --- | --- |
| `src/rules/noopunk_extensions.py` | **scenario-level link graph** — "is there an actual chain of hops from A to B", for authoring scenarios |
| `src/rules/ubiquitous_network.py` | **rules owner** — the §22.5.2 reach table, the era dial, the exposure economy |
| `src/rules/natural_psi.py` | **rules owner** — training, Effort, pressure, consensus on the one kernel |

One canon conflict is recorded rather than merged silently: `noopunk_extensions.DISCIPLINES` lists
seven names including `influence`, `healing` and `shielding`, which are **not** in the locked skill
vocabulary (#159 fixes six PSI skills). The module now carries a scope note saying so, and no rule may
be built on those three names until the author adds them.

## 8. The issue's four deliverables, checked

### 8.1 Every extension: owner, layer, and the "no equivalent" verdict (item 1)

Where the family has no equivalent the verdict is **KEEP-ORIGINAL by construction** — not a
preference, but the only logically available answer, because there is nothing to convert from.

| Extension | Owning layer | Owner artefact today | Family equivalent | Verdict |
| --- | --- | --- | --- | --- |
| **Natural PSI** | A: `src/rules/natural_psi.py` (367 lines). B: `strategy_game/rpg/psi.py` (367 lines) | Six `Discipline` values, `Training` tiers, Effort commitments, pressure | SWN's *rules pattern* (Effort); **not** its ontology | **KEEP-ORIGINAL ontology + ADOPT Effort** (author ruling 2026-10-25) |
| **Psychotronics** | A: `rulebook/17_NOETIC_PRACTICE_AND_CRYSTAL_TECH.md` (410). B: `strategy_game/psi_operations.py` (111) | Device-mediated path, usable without natural PSI | **None.** No WN book models device-mediated cognition with its social constraints | **KEEP-ORIGINAL by construction** |
| **Cybernetic cognition / BCI** | A: `src/rules/equipment_catalog_index.py` (69), `rulebook/5_CYBERNETIC.md`. B: `strategy_game/cyber.py` (453) | Connectivity model, BCI as a channel | CWN has implants and System Strain; **no** model of cognition-as-bandwidth | **KEEP-ORIGINAL for BCI by construction**; cyberware *capacity* is **D36** |
| **Intrusion / network access** | A: `src/rules/ubiquitous_network.py`. B: `strategy_game/cyber.py` | Reach table, era dial, exposure economy; reachability decided **before** any check | CWN presumes access is scarce and path-discovery is play | **KEEP-ORIGINAL by construction** — see §8.2 |
| **Noösphere / cross-domain** | A: `src/rules/noospace_projection.py` (433), `cross_domain_state.py` (273, **provisional**) | Single-locus prohibition, gateway and realm-action contract | **None.** No WN book has a realm ontology | **KEEP-ORIGINAL by construction**; provisional numbers must not be promoted |
| **AGI/ASI** | A: `rulebook/11_ONTOLOGY.md` (487), `12_BEINGS.md` (714) | Beings ontology, strategy/mission boundaries | SWN's AI/alien material is **not NoöPunk lore** | **KEEP-ORIGINAL by construction** |
| **NHI contact** | A: ontology + beings chapters | Contact as a setting-scale event, not a stat block | **None** | **KEEP-ORIGINAL by construction** |
| **Crisis scarcity / salvage** | A: campaign transition | Pre-collapse transition, **not** a universal Fall | AWN salvage is the closest thing | **DEFER** — optional comparison only |

The point of the "by construction" column: a conversion that produced a REPLACE verdict here would
have had to invent the replacement, and inventing it is canon invention. That is the failure mode
this issue exists to prevent.

### 8.2 What a network-access subsystem must add (item 2)

CWN's assumption and NoöPunk's are **incompatible at the root**, not in the details:

| | CWN | NoöPunk |
| --- | --- | --- |
| Is access scarce? | **Yes** — reachability is the gate and the fun | **No** — the network is ubiquitous |
| What is the interesting question? | Can I get in? Which path, which credential? | Who notices, how fast, and what it costs me socially |
| Default state of a target | Isolated until a path is found | Reachable unless something has severed it |

So the subsystem must add five things the family cannot supply — the contract in §2.1–§2.3:

1. **A reach classification per era** (isolated / local-only / proxied / networked), so ubiquity is a
   *measured property of the era*, not a constant — the crisis-era dial changes it.
2. **An exposure economy.** Ubiquity's cost is not access, it is visibility: every act raises
   exposure, and Cover buys it back. This is the mechanic CWN has no slot for at all.
3. **An alert ladder** with ordered bands, so escalation is legible on paper.
4. **A shared clock** (AP) that does not carry between scenes.
5. **A hard separation** between ordinary intrusion and a containment/Blackwall breach — the second
   is an offence with legal consequences, not a harder roll.

**Where the issue's own text is now superseded:** its parenthetical "disconnected devices, physical
ingress" described a default. The author's 2026-10-25 ruling makes ubiquity the default and
severance the *exception the crisis produces* — so physical ingress is still modelled (the courier
channel exists), but as a way to restore contact with a **partitioned** segment, not as the usual
precondition for every act. Deterministic either way.

### 8.3 PSI in each layer: skill, resource, permission, or subsystem (item 3)

| Layer | PSI is… | Permission gate | Resource | Resolution |
| --- | --- | --- | --- | --- |
| **A** (tabletop) | **a skill *and* a resource** — the six disciplines are skills (#159); Effort is the capacity | **training tier** (`UNTRAINED` refused **before any die**) | **Effort**, committed and released | `1d10` on the one kernel (`core.resolve_check`) |
| **B** (crossover) | **a permission** | capability tag | psi rating / consensus / pressure as modifiers and consequences — **no pool today** | Fate `4dF` |
| **C** (board) | not modelled | — | — | — |

**Natural, not virus-derived (#482), in both layers.** Psychotronics is a *separate* path: it needs a
device and may be used by someone without natural PSI, which is why it is not a discipline.

**What the Effort import does not change:** PSI is not rare, not a class feature, and not a second
progression track. The pool makes the price legible; it does not gate the ability.

### 8.4 Deterministic, offline, tabletop-convertible (item 4)

Verified rather than asserted:

- **No network or model dependency.** `natural_psi.py`, `ubiquitous_network.py` and
  `noopunk_extensions.py` import only `dataclasses`, `enum`, `random`, `typing` and `core` — grep for
  `requests|http|socket|urllib|openai|anthropic|llm` returns **nothing**.
- **Seeded replay is tested**, not hoped for: `test_the_same_seed_replays_and_a_different_seed_does_not`.
- **32 tests** across `test_issue572_native_subsystems.py` (27) and `test_noopunk_extensions.py` (5)
  pass on Python 3.11.
- Every value that affects play is a module-level `TUNING_` constant, so a table can print the same
  numbers and a save/load reproduces the same state.

### 8.5 The one thing this record cannot settle

`src/rules/noopunk_extensions.py` accepts **seven** discipline slugs, three of which — `influence`,
`healing`, `shielding` — are **not** in the locked six-skill vocabulary (#159). The module is a
scenario prototype and explicitly **not** the rules owner (`natural_psi.py` is), and its docstring
says no rule may be built on those three names. Recording it is the correct fix; **deleting them
would assert they are not canon, and promoting them would assert they are** — both are canon
decisions and neither is an agent's. Carried to `AUTHOR_DECISION_QUEUE.md` as **D43**.

— Ai (愛)
