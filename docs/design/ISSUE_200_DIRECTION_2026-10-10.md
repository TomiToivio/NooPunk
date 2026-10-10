# Direction record: issue #200 — GNS triangle, Fudge/Fate hybrid centre, CC licensing

**Status: author-directed direction record — RECORD ONLY.** `AGENTS.md` §4 is a protected
file, so the un-reservation this issue carries lands here, as with #197.

**This record does not migrate anything.** The issue says so itself: *"This is a specification
issue, not a claim that code or the rulebook have already migrated"* and *"No code changes
happen merely by updating it."* No LICENSE file is added, no die is changed, no subsystem is
implemented, and the locked `1–10 STAT + 1–10 Skill + 1d10` core is **not** superseded here.

Companions — canonical, shared with the sessions that landed #203/#204:
[`docs/sources/GAME_SYSTEM_RIGHTS.md`](../sources/GAME_SYSTEM_RIGHTS.md),
[`data/sources/game_system_rights.json`](../../data/sources/game_system_rights.json), and the
release gate [`docs/licenses/ISSUE_200_CC_RELEASE_GATE.md`](../licenses/ISSUE_200_CC_RELEASE_GATE.md).

**Reconciled across three parallel sessions, not duplicated.** #200 was worked by three PRs at
once — #203 (GNS canon + release gate), #204 (rights audit + ledger), #205 (this record).
The result is **one ledger, one audit, one release gate, and two guards with a deliberate
division of labour**: `test_issue200_rights_ledger.py` owns the ledger's shape, vocabulary and
audit inventory; `test_issue200_rules_engine_direction.py` owns this record, the no-relicense
rule, and a licence-string property over the canonical ledger. The second rights ledger and
audit that this session first wrote were **retired** rather than left to fork the record, and the
sources the #204 audit recorded as *blocked* were retrieved and folded into its second pass.

## 1. The design geometry

Three **equal** corners — a playtest goal, not page quotas and not mutually exclusive
mechanics: **Simulationism ~⅓, Narrativism ~⅓, Gamism ~⅓.**

| Corner | Influence | What NoöPunk takes |
| --- | --- | --- |
| Simulationism | **Eclipse Phase** | credible causal differences: cyberware, networks, AI, PSI, bodies, physical risk, cross-realm interaction |
| Narrativism | **Apocalypse World / The Veil** | fiction-first stakes, hard choices, social and emotional consequences, player agency, clocks |
| Gamism | **Cities Without Number / Stars Without Number** | fast legible procedures, generators, mission structure, meaningful risk/reward, encounter pacing |

**No ranking.** These are complementary *pressures*, not alternate engines.

**The centre** is one NoöPunk system homebrewed from **Fudge + Psi-Punk + Fate +
Transhumanity's Fate together**:

- **Fudge** supplies the **Attribute/Skill distinction** and flexible trait-ladder adjudication
  — the author's essential preference;
- **Psi-Punk** demonstrates psychic/cyber/astral subsystems built on that distinction;
- **Fate** supplies aspects, consequences, compels and narrative decisions;
- **Transhumanity's Fate** demonstrates a sophisticated transhuman setting expressed in Fate.

**The six STATs are not optional**: FIT, REF, INT, SOC, CYB, PSY. Attributes and Skills stay
**distinct**, the Skill vocabulary and campaign specialist-field policy stay as they are, and
the dice kernel (4dF vs mapped ratings vs legacy d10) is **a playtesting decision, not a
decision made here**.

## 2. Licensing — recommendation, not an act

**Recommended target: CC BY-SA 4.0.** Alternative CC BY 4.0. **Status: recommended, not
applied.**

The reason is concrete, not aesthetic. BY-SA 4.0 accepts **CC BY 3.0** and **CC BY-SA 3.0**
material in its compatibility pathway, so:

- the **Fate Core SRD** (CC BY 3.0) can be adapted with attribution, **and**
- **The Veil** (CC BY-SA 3.0) can be adapted under reciprocity.

Choosing **CC BY 4.0** would close the second door and forbid adapting The Veil's expression.
Since The Veil is one of the two named narrativist influences, that door matters.

**The exclusions are the point of the audit.** Fudge's SRD and Psi-Punk's SRD are **OGL 1.0a**
— Open Game Content cannot be relabelled Creative Commons. Eclipse Phase 2e and
Transhumanity's Fate are **CC BY-NC-SA** — NonCommercial cannot enter a commercially reusable
CC release. Apocalypse World grants **no CC license at all**. Those four contribute
**procedures and structural lessons**, independently implemented, and no expression.

Code is licensed **separately** (MIT / Apache-2.0 / GPL), never with a CC instrument.

## 3. Closed-source audit: what is actually in the tree

The issue says to remove *"claimed mechanical dependence on Cyberpunk RED"* and audit before
deleting. **Audited; the premise is stale, and nothing is deleted.**

**Finding: there is no RED baseline left to remove.** Issue **#111** already replaced the RED
chassis with an independent NoöPunk core, and `AGENTS.md` §15 states plainly that NoöPunk *"is
an independent RPG system"* and lists CP2020/RED as *"selective design references, not
automatic rules"*. The live mentions are:

| Where | What it is | Action |
| --- | --- | --- |
| `RULEBOOK.md` §9 | provenance: lifepath "inspired by the high-level choose-or-roll structure of Cyberpunk RED. It does not copy another game's tables or text." | **keep** — an attribution that already disclaims copying |
| `RULEBOOK.md` §1150 | a **prohibition**: do not inherit exploding 10s/fumbles/marginals from RED, CP2020, Fate, PbtA, EP or any other game | **keep** — this is the independence rule |
| `docs/design/RPG_CONVERSION_REFERENCE.md` | conversion/correspondence tables (#135), self-described as interoperability aids that import no catalogue | **keep** — NoöPunk-original authorship; deleting it would be the destructive blanket deletion the issue forbids |
| `rulebook/4_SOCIAL.md`, `docs/sources/SOCIAL_SYSTEM_SOURCES.md`, `rulebook/2_ATTRIBUTES.md` | design-reference and cross-reference notes | **keep** |
| `docs/archive/*` | warehouse material | **untouched** (never delete, never wholesale-port) |

**Conclusion: no copied RED expression exists and no baseline claim survives, so there is
nothing to delete.** The ledger records RED and the other closed systems as `no-reuse` so the
boundary is explicit rather than implied.

## 4. The guard conflicts: one real (now fixed), one that was never real

### 4.1 REAL, and fixed here — the canonical pole list contradicted the triangle

`docs/archive/DESIGN_PRINCIPLES.md` is the canonical principles document and is
**build-enforced as a set** with `AGENTS.md` §13 and `tests/test_design_principles.py`.

#203 rewrote its §1 to the #200 triangle (Simulationism → Eclipse Phase, Narrativism →
Apocalypse World / The Veil, Gamism → Cities Without Number / Stars Without Number) — and
**left invariant #2 saying the opposite**:

> *"Use **CY_BORG**, **Cyberpunk 2020**, and **The Sprawl** as the canonical reference poles."*

So the document contradicted itself, and the guard **could not see it**: the pole test asked
only whether the old names appear somewhere in the doc, and the stale sentence satisfied it.
A document-wide name check is satisfied by the paragraph you forgot.

Fixed: invariant #2 now names the #200 corners, `REFERENCE_POLES` is re-baselined to match, and
the guard gained **`test_the_canonical_poles_match_the_triangle`**, which is **sentence-scoped** —
it finds the sentence that declares the poles and requires the new corners *in that sentence*
while forbidding the superseded trio *in that sentence*. The name-only check is what failed, so
the replacement tests the fact rather than the vocabulary.

**Still the author's:** `AGENTS.md` §13.2 carries the same old pole list and is a **protected
file**. It has to move with the documented set, and no agent can write it. That is the one
outstanding item from this section.

### 4.2 Never real — `FORBIDDEN_CHASSIS`

My earlier report flagged `tests/test_issue32_rules_reset.py` as conflicting because its
`FORBIDDEN_CHASSIS` includes `fate` and `pbta`. Reading the assertion rather than the list
shows it forbids only *"X as the chassis"* and *"chassis is X"* — which is exactly right under
#200, where Fate is a **centre influence** that must never become the chassis. **Not a conflict;
nothing was changed.** Recorded here so a later session does not "fix" a guard that is doing its
job.

## 5. What is reserved, and what is not

| #200 asks for | `AGENTS.md` §4 today | Position here |
| --- | --- | --- |
| New resolution core (Fudge/Fate, 4dF or mapped) | §15 pins the `1–10 + 1d10` core | **spec + prototype only**; supersede only with approved migration and tests |
| Six STATs + distinct Skills | locked by #131 / #159 | **preserved** — the issue says not optional |
| Combat resolution, damage/health/armour/initiative | **reserved** | flag, do not implement |
| Cyberware / augmentation beyond the #158 package | **reserved** | flag |
| Psionic mechanics | **reserved** (psi = capability on the existing check) | flag |
| Advancement / XP | **reserved** | flag |
| Astral/Noöspace procedure, four cyber modes, social/law-enforcement procedures | lore-only today | **flag — the largest new mechanical surface** |
| CC license for rulebook/setting; separate code license | no LICENSE exists | **recommend + record; relicense is the author's act** |

## 6. Increment plan

1. **This record + the rights ledger + the closed-source audit.** *(this change)*
2. Engine specification: the Fudge/Fate-compatible core — 4dF vs mapped 1–10 — as a **DRAFT
   with calibration targets**, plus the playtest plan the issue asks for before locking.
3. Subsystem specifications, in the issue's order, each `DRAFT pending calibration`, inventing
   no lore and no numbers the issue has not authorised.
4. The rights ledger gains an entry **before** any ported text lands.
5. License/NOTICE/attribution map once the author selects the license.

## 7. What this record explicitly does NOT do

- It does not migrate the engine, the die, or any subsystem.
- It does not add a LICENSE file or relicense the repository.
- It does not re-baseline the two conflicting guards.
- It does not treat any OGL, NonCommercial or unlicensed source as reusable expression.
- It does not answer the open questions §2 above needs answered first.
