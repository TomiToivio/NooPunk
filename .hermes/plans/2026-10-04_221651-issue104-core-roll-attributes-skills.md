# Issue #104 — Core Resolution: Attributes + Skills, and the Stunt / Move Hybrid

> **For Hermes:** planning only. No RULEBOOK, code, or data changes land until the author
> clears GATE 1–3 below. Issue #104 is an umbrella that stays open; this plan covers its
> **first mechanical design decision** only — the common chassis — not the EP2 table-of-contents
> traversal (that is #104 Phase 2, a later increment).

**Goal:** decide and then implement NoöPunk's core task resolution, in which **Attributes and
Skills are separate statistics that can both modify the same roll**, on a Fate-style engine that
keeps EP2's attribute and skill vocabulary, plus a unified Stunt/Move concept.

**Architecture:** tabletop-first. `RULEBOOK.md` is the source of truth; `data/rules/core.json`
is the single runtime-readable constants file; `src/rules/core.py` and `src/godot/core_rules.gd`
read it; Concordia consumes the same model. No new engine, no parallel resolver (repo §7, §10).

**Tech stack:** Markdown canon, JSON constants, stdlib Python + `unittest` (no pytest), Godot 4
adapter, `gh` for the PR/comment.

---

## 0. Decision gates (nothing lands before these)

| Gate | Decision | Owner | Options |
| --- | --- | --- | --- |
| **GATE 1** | Rating scale: how Attribute and Skill combine | author | A / B / C (see §3) |
| **GATE 2** | Core die + outcome model | author | keep **2d6** vs move to **4dF**; **Fate shifts** vs **PbtA bands** vs hybrid |
| **GATE 3** | Stunt/Move taxonomy sign-off | author | accept/prune the 6 candidate categories (see §6) |

GATE 1 and GATE 2 are coupled: the die determines what scale is survivable (§3 is computed for
4dF; a 2d6 keep gives a different curve). Ask them together.

---

## 1. Verified current state (measured on `origin/main`)

Everything below was read from `git show origin/main:<path>`, not the working tree — the local
checkout is **20+ files dirty from a sibling session** and its `HEAD` (`fa57458`) is far behind
`origin/main` (`822eea7`, which already contains the merged #101 fix). `git worktree add` is
mandatory for any branch work.

| Fact | Where it lives | Status |
| --- | --- | --- |
| Six attributes **FIT REF INT CHA CYB PSY**, 3d6 generation, modifier table 3→−3 … 18→+3 | `data/rules/core.json` | Runtime canon. `AGENTS.md` §4 calls it "the old model … documented porting debt". |
| **2d6 + skill level + attribute modifier** vs **6/8/10/12/14+** | `data/rules/core.json` + `RULEBOOK.md` §4 | Author-specified. `AGENTS.md` §4: preserve until the author revises. |
| Skill levels **0..4** → +0..+4; unskilled = −1 or trained-only block | `data/rules/core.json` | Author-specified. |
| Skill **list** = 20 CWN names (Medical/Science renames) | `RULEBOOK.md` §5.3 **per the skill**, `AGENTS.md` §4 | `AGENTS.md` §4 claims the list is in "RULEBOOK.md §5.3" — **§5 is "Primary Eclipse Phase references"**: stale pointer, and §5.3 does not exist |
| **Four-system tag model** (Physical / Social / Cybernetic / Psychic), attributes as typed tags | `AGENTS.md` §4, `rulebook/2_ATTRIBUTES.md` (skeleton) | Declared "the canonical character direction" |
| **EP2 aptitudes** (6): COG, INT, REF, SAV, SOM, WIL | verified live, EP2 ch04 §4.1 | Not in NoöPunk anywhere yet |
| **EP2 active skills** (22) each with a *linked aptitude*, plus `Know: [Field]` | verified live, EP2 ch04 §4.19–4.20 | Not imported (`conversion_matrix.json` `skills-list`: "keep-as-open-vocabulary", "EP2's Active Skill List and Know Skills are not transcribed") |

---

## 2. Verified source facts this plan depends on

> **ADDENDUM 19:20, after a parallel session posted its own #104 review 15 s before mine.**
> A sibling review flagged the following, and I verified it from EP2 ch04 Step 6 — **it corrects
> this plan's §3.**
>
> EP2 Step 6 (live): *"Next, add the base aptitude values to their linked skills. The skills of
> Fray and Perceive have base values equal to their aptitude × 2. No final skill total (including
> aptitude) may exceed 80."* Aptitudes are 5–30; skill totals are capped at 80.
>
> **EP2's skill total = aptitude + trained points.** So treating EP2's attribute list *and* EP2's
> skill list as two independent modifiers **double-counts the aptitude** — and triple-counts on
> **Fray / Perceive**, where base = aptitude × 2, on exactly the two skills defence depends on.
> §3's Options A/B/C all treated the skill as an independent 0..+4 band, so they **miss this**.
>
> **Consequence:** the skill modifier must be the **trained component only**, and the conversion
> needs an explicit re-split of EP2 displayed totals back into (aptitude, trained). This belongs
> **ahead of** the scale decision — it is an arithmetic error, not a matter of taste.
> Treat §3's "span" numbers as *upper bounds on a naive sum*; the real recommendation is
> "narrow attribute + trained-skill component", which both reviews reached independently.

- **EP2 aptitudes (six, confirmed from ch04 §4.1):** Cognition (COG), Intuition (INT), Reflexes
  (REF), Savvy (SAV), Somatics (SOM), Willpower (WIL). They are **ego** stats. EP2 itself already
  does "no modifier for defaulting to aptitude, critical successes ignored". Range **5–30**;
  starting templates are 10–20 per aptitude and no score may exceed 30 or drop below 5.
- **EP2 active skills carry an explicit linked aptitude** (Athletics→SOM, Deceive→SAV,
  Fray→REF, Infosec→COG, Psi→WIL, …). EP2 *binds* skill→aptitude by default.
- **EP2 skill total = aptitude + trained points, cap 80; Fray/Perceive = aptitude × 2**
  (Step 6, verified). This is the double-count trap above.
- **Fate Core skills** (verified, fate-srd.com): ladder **Average +1 → Great +4**, a **pyramid**
  (one +4, two +3, three +2, four +1), **cap +4**, raisable for superhuman games. So Fate's *own*
  skill span is only **0..+4**.
- **4dF:** outcomes −4..+4, mean 0, **sd ≈ 1.633**, P(0) = 23.5%.
- **Licensing, verified:** Fate SRD content is **CC BY 3.0** (attribution-only; Fate™ and the
  Powered-by-Fate logo are reserved trademarks). EP2 is **CC BY-NC-SA 4.0**. NoöPunk is
  **noncommercial + attribution + ShareAlike** as a result (`docs/licenses/ECLIPSE_PHASE_HOMEBREW.md`).
- **Transhumanity's Fate is not on disk.** `docs/sources/EXTERNAL_SOURCE_LICENSES.md` records that
  the attached conversions are absent, so its mechanics must **not** be described from memory —
  cite it only as #104's own "obvious example" design reference (source-hierarchy rank 7).

---

## 3. The probability crux (why GATE 1 exists)

Computed from the exact 4dF distribution. This is the single most important design fact:

| Rating model | Span | In dice-sd units | Consequence |
| --- | --- | --- | --- |
| **A. attr −3..+3 + skill 0..+4** | 10 | **6.1 sd** | **Saturates.** At T=Fair(+2): maxed char **100%**, weakest **0%**. The dice stop mattering. |
| **B. attr −1..+1 + skill 0..+4** | 6 | 3.7 sd | Expert (attr+1,skill+4 → +5) **99%**, novice (attr−1,skill0 → −1) **6%** at T=2. Dice still matter at the tails. |
| **C. attribute *gates* skill** (roll uses one modifier) | 4 | 2.4 sd | Closest to Fate's native behaviour; "two modifiers" becomes narrative, not additive. |

Reference grid, P(success) for total modifier *m* vs difficulty *T*:

```
  m |   T=2   T=3   T=4   T=5
 -3 |    0%     0%     0%     0%
 +0 |   19%     6%     1%     0%
 +3 |   81%    62%    38%    19%
 +6 |  100%    99%    94%    81%
```

For calibration, the **current** NoöPunk engine (2d6 + mod ≥ 10) gives: mod +0 → 17%, +2 → 42%,
+4 → 72%, +6 → 92%. So the current engine already has a wide-but-not-saturated band; **Option A
on 4dF is much worse than what NoöPunk has today**, which is a strong argument against it.

**Recommendation to put to the author:** **B**, or **C** if the goal is that raw aptitude should
mostly set a ceiling/floor rather than stack. Both keep Attributes strictly separate from Skills,
which is the requirement the author actually stated — neither collapses competence into the skill
list the way Fate does. A is the literal "just add both" reading and is the one to talk him out of.

**Do not pick one.** Present §3 and wait (GATE 1).

---

## 4. Conflict register — findings that must be decided, not silently resolved

These are pre-existing repo contradictions that this work will collide with. Surface them in the
#104 comment; each needs an author call.

| # | Conflict | Evidence | Why it blocks |
| --- | --- | --- | --- |
| **C1** | **Two attribute systems** | `data/rules/core.json` + RULEBOOK §5.2: **FIT/REF/INT/CHA/CYB/PSY** (runtime canon). `AGENTS.md` §4 + `rulebook/2_ATTRIBUTES.md`: **four-system** Physical/Social/Cybernetic/Psychic. | Which one is "the full attribute list" to keep? The author said "use the full attribute list of Eclipse Phase" — that is a **third** list (COG/INT/REF/SAV/SOM/WIL). Three candidates, one decision. |
| **C2** | **Three different skill lists** | EP2 (22 active + Know fields, verified above) · CWN-20 (`RULEBOOK.md`, Medical/Science renames) · Fate (~18, plus the list is *flat*, not pyramidal). | The author said "use the Fate skill system otherwise" — but a Fate skill *list* is not what §5.3 has. Decide: keep the CWN-20 list, import EP2's 22, or author a Fate-shaped NoöPunk list. |
| **C3** | **Skill→attribute binding is currently FORBIDDEN** | `data/rules/core.json` `_notes`: "No permanent skill-to-attribute binding: the GM selects the attribute that fits the action". EP2 *requires* the binding (linked aptitudes). | "Attribute + Skill on top of each other" implies a pairing. The repo explicitly bans one. This must be lifted/re-defined deliberately. |
| **C4** | **The matrix's own unresolved question names this exactly** | `data/rules/conversion_matrix.json` → `unresolved_questions[0]` `four-system-vs-ep2-chassis`: *"Is the #51 four-system unified tag model … still the CHARACTER canon … or has it been retired in favour of an EP2-shaped character layer?"* `owner: author`, blocks "character sheet finalisation, skills list finalisation". | #104's core-roll decision is the same decision. Answering C1 answers this too. |
| **C5** | **`AGENTS.md` §4 says do NOT define these** | §4 "Until explicitly specified, do not define": attribute names/counts, derived statistics, additional skills or a rename/split/merge, which skills are unskilled vs trained-only, skill-to-attribute bindings, character creation… | An agent may not implement the chassis by itself. **The author's decision in #104 is the authorisation**; until it exists, code must not move. |
| **C6** | **EP2 attributes are NOT on Fate's scale** | EP2 aptitudes are a wide numeric band; Fate's ladder is −2..+8 with skills at +1..+4. | "Use EP2 attributes as modifiers" needs a conversion rule, and the scale question (GATE 1) *is* that rule. Also: `conversion_matrix.json` `modifier-cap` is EP2's **±60** — meaningless under 4dF, so that row's `keep` status is already wrong for a Fate engine. |
| **C7** | **Stunt vs Move is two different outcome philosophies** | Fate resolves with **shifts** (margin) and stunts that give **+2 under narrow circumstances** or permit a rules exception. PbtA resolves in **bands** (10+/7–9/6−) producing "success at a cost". | A unified Stunt/Move concept must also decide the **outcome model**. GATE 2b. |

---

## 5. What stays and what changes (proposed, pre-decision)

**Keep (per `AGENTS.md` §4, unchanged unless the author revises):** the 2d6 engine, 6/8/10/12/14+
ladder, level-0..4 scale, unskilled −1 / trained-only block, opposed tests with PC tie priority —
**if** GATE 2 keeps 2d6. If GATE 2 moves to 4dF, every one of these needs an explicit rewrite
decision, and the `AGENTS.md` §4 paragraph must be updated in the same change (it currently pins them).

**Add:** a separate Attribute modifier and Skill modifier on the same roll (§3); a defined
skill→attribute pairing rule (C3); the unified Move concept.

**Do not touch:** the CWN SRD boundary, the worldbook (§33), the design invariants, or any
runtime beyond what the author clears (tabletop-first gate, §14).

---

## 6. Proposed work order (after gates clear)

### Phase 0 — the decision record (no code)
- T1 Write the author's GATE 1–3 decisions verbatim into `RULEBOOK.md` §10 as a new
  "### 10.1 Core resolution (author decision <date>)" subsection, with provenance label.
- T2 Update `AGENTS.md` §4: replace the now-false reservation lines with a precise split (what is
  now specified vs still open) — the repo's own stale-inventory sweep pattern.

### Phase 1 — tabletop canon
- T3 `RULEBOOK.md` §5.2/§5.3: rewrite the attribute and skill sections to the decided model.
  Add the attribute table with the decided modifier band and the skill→attribute pairing rule.
- T4 Add a worked-example block (normative, per house style) for: skilled test, attribute-only
  test, unskilled, opposed, and one Move-augmented test.
- T5 `RULEBOOK.md` §9.1: update the character-sheet list to the decided attributes + skills.

### Phase 2 — runtime constants (one source, three readers)
- T6 `data/rules/core.json`: bump `_canon_revision`; add `attributes_v2` (decided list + band) and
  the pairing rule; keep the old block only if the author wants it as porting debt.
- T7 `src/rules/core.py`: implement the new modifier combination. Keep the existing public function
  name so existing tests keep meaning.
- T8 `src/godot/core_rules.gd`: read the same JSON keys (adapter holds no table).
- T9 `scripts/noopunk_text.py`: confirm the playable slice still runs against the new constants.

### Phase 3 — Stunt/Move hybrid (design experiment, then implement)
- T10 Author a canonical **Move record** in a `fixtures:`/experimental area:
  `{id, name, category, trigger, effect, cost, subsystem}` — six candidate categories from #104:
  Bonus / Permission / Triggered / Choice / Resource / Subsystem.
- T11 Test the taxonomy against ≥10 real EP2/NoöPunk abilities (e.g. EP2 traits, psi sleights,
  morph abilities) and record which categories survive. Expect to prune to 3–4.
- T12 Write the surviving Move definition into `RULEBOOK.md` (new subsection), with the rule for
  what makes something a Move rather than a plain bonus — mirroring Fate's stunt discipline (narrow
  circumstance, or a rules exception; never a general +N).
- T13 Implement deterministic Move *resolution* (not narrative text) in `src/rules/core.py`, and
  a guard test.

### Phase 4 — guards and examples
- T14 `tests/test_issue104_core_roll.py`: structure guard, **heading-text anchored** (never `## N.`).
  Assert: the decided attribute list is present; attribute and skill are distinct fields; the
  pairing rule exists; the Move definition exists; the old model is not silently restored.
- T15 Prove the guard bites (§8).

### Phase 5 — status bookkeeping
- T16 `data/rules/conversion_matrix.json`: update rows `action-resolution`, `character-sheet`,
  `skills-list`, `defaulting`, `superior-results`, `criticals`, `modifier-cap`,
  `lighter-rules-alternatives` to the new statuses and `rulebook_section`, and **resolve or
  re-point** `unresolved_questions[0]` (C4).
- T17 `docs/rules/EP2_CONVERSION_MATRIX.md` prose to match the table (the repo's half-landing trap:
  prose and table must move together, or `main` goes red).

### Phase 6 — Concordia (only after the tabletop rule is coherent)
- T18 `src/concordia_runtime/`: resolve against the shared model; no parallel ruleset.
- T19 `tests/test_concordia_runtime.py`: extend.
- T20 `RULEBOOK.md` §27 change ledger: add the row.

### Phase 7 — deliver
- T21 Push a branch `issue-104-core-roll-<slug>`, open a PR, run the 5 CI steps, and post the
  design-review comment on #104 (§9 template). Do **not** close #104 (umbrella; the author keeps it open).

---

## 7. Files likely to change

| File | Change |
| --- | --- |
| `RULEBOOK.md` §4, §5.2, §5.3, §9.1, §10, §27 | core roll, attribute/skill tables, Move definition, examples, ledger |
| `AGENTS.md` §4 (+ §13/§15 only if the die changes) | reservation-sweep, precise split |
| `data/rules/core.json` | new attribute block, combination rule, `_canon_revision` |
| `src/rules/core.py`, `src/godot/core_rules.gd` | modifier combination |
| `src/concordia_runtime/*` | later-phase alignment |
| `data/rules/conversion_matrix.json`, `docs/rules/EP2_CONVERSION_MATRIX.md` | statuses (table **and** prose) |
| `tests/test_issue104_core_roll.py` (new) | guard |
| `docs/sources/EXTERNAL_SOURCE_LICENSES.md` | Fate/Transhumanity's Fate attribution note |

---

## 8. Verification

Canonical 5 steps (not pytest):

```bash
python tests/validate_scaffold.py
python -m unittest discover -s tests -p "test_design_principles.py"
python tests/test_world_ideology.py
python -m unittest discover -s tests -p "test_*.py"
python scripts/noopunk_text.py --help && printf 'quit\n' | python scripts/noopunk_text.py --scenario issue74
python scripts/concordia_smoke.py
```

Baseline to beat: the suite is **679 tests OK** after #102 (was 665). Report the number you
actually measure.

**Guard-bites proof** (house rule — a guard that has only ever passed proves nothing): introduce
four regressions, confirm each FAIL, restore, confirm **byte-identical** via `md5sum`:
1. the attribute list deleted from RULEBOOK;
2. attribute and skill collapsed into one field in `core.json`;
3. the pairing rule removed;
4. the old attribute model restored under a new heading.

Two traps that have bitten this repo: `git checkout -- <file>` cannot restore an **untracked** file
(a new test file is untracked until `git add`) — back it up with `cp` and hash it; and stale
`__pycache__` can fake a failure after a correct restore — clear it before believing RED.

---

## 9. Proposed #104 comment (draft — post only after the plan is accepted)

> **Design review: Core Resolution + Attributes + Skills** (agent Ai (愛), <date>)
>
> Read your 19:12 plan comment; this implements its Phase 0 as a review, with one measured finding
> that changes the recommendation.
>
> **1. Verified state** — attributes exist twice (`core.json` FIT/REF/INT/CHA/CYB/PSY vs `AGENTS.md`
> §4 four-system); the skill list exists once (CWN-20); EP2's real aptitudes (COG/INT/REF/SAV/SOM/WIL)
> and its 22 active skills with linked aptitudes are **not in the repo at all**; `AGENTS.md` §4
> currently *forbids* defining attribute names and skill→attribute bindings. So "use EP2's full
> attribute and skill lists" is net-new import, and it needs C1–C5 resolved.
>
> **2. The measurement that matters** — on 4dF (sd 1.633), stacking a −3..+3 attribute **and** a
> 0..+4 skill spans 6.1 sd. At Fair(+2) a maxed character succeeds **100%** and the weakest **0%**:
> the dice stop mattering. Options B (attr ±1) and C (attribute gates the skill) keep both statistics
> separate without that. Recommendation: **B, else C** — A is the literal reading and I'd advise
> against it.
>
> **3. What I need from you** — GATE 1 (scale), GATE 2 (die: keep 2d6 or move to 4dF; shifts vs
> bands), GATE 3 (Move taxonomy). Then I write §10/§5 and port to `core.json` + Concordia in one PR.
>
> **4. Licensing** — Fate SRD is CC BY 3.0 (attribution, trademark reserved); EP2 is CC BY-NC-SA 4.0.
> Prefer original NoöPunk wording; record attribution.

---

## 10. Risks, tradeoffs, open questions

- **Biggest risk:** implementing before GATE 1–3 → inventing canon (`AGENTS.md` §1) and possibly
  turning `main` red (the prose-vs-table trap).
- **Coupled decision:** the die choice changes the answer to the scale choice. Ask together.
- **Three-list problem (C2):** "use the Fate skill system" cannot mean "use Fate's list" without
  discarding the CWN-20 list the repo already specified — needs an explicit call.
- **Move taxonomy may be over-designed:** six categories is a hypothesis; expect 3–4 to survive T11.
  Do not publish six as canon before testing.
- **`modifier-cap` ±60** is already inconsistent with a Fate engine — flag, don't fix silently.
- **Scope:** tabletop-first. Concordia/Godot changes are Phase 6 and must be cleared separately
  (`AGENTS.md` §14).

## 11. Deliberately NOT in this plan

- The EP2 section-by-section traversal (#104 Phase 2) — that is dozens of increments.
- Character creation, morphs, traits, psi, combat, hacking subsystems.
- Any change to §33 worldbook or the design invariants.
- Choosing GATE 1–3 on the author's behalf.
