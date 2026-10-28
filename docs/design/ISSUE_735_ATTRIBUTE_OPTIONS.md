# #735 — Reskin and possible expansion of the CWN/SWN attributes

**Design memo. No decision, no canon change, no code change.** This extends `#716`'s A/B/C framing
(keep / display aliases / full new set) with the structural question #716 did not open: *should the
mental and technological axes be split, and should anything new become an attribute at all?*

Everything below is a candidate. The author selects; until then the operative baseline stays
`STR / DEX / CON / INT / WIS / CHA` in `data/rules/without_number.json`.

---

## 1. What the repository already fixes

These are not opinions; they are the current data and code, and any option has to move them
deliberately or leave them alone.

| Surface | Current fact | Where |
| --- | --- | --- |
| Attribute set | six codes, 3–18 | `data/rules/without_number.json` → `attributes` |
| Generation | array `[14, 12, 11, 10, 9, 7]` (sum 63, the expected total of six 3d6) | same file |
| Modifier bands | 3 → −2, 4–7 → −1, 8–13 → 0, 14–17 → +1, 18 → +2 | `data/rules/wn_core.json` → `stats.modifier_table` |
| Resolution | 2d6 + attribute modifier + skill rank | `skill_check` |
| Saves | `16 − level − best pair`: Physical `STR+CON`, Evasion `DEX+INT`, Mental `WIS+CHA`, Luck none | `without_number.json` → `saves` |
| System Strain cap | equals **CON** | `src/rules/cwn_strain.py` |
| Max Effort | `1 + highest psychic skill + better of WIS or CON modifier` | `docs/rules/SWN_PSIONICS_ADAPTATION.md` |
| Skills | 40 named skills, each bound to an attribute; includes `Interface`, `Perceive`, `Talk`, `Connect`, `Kinesics`, `Investigation`, `Program` | `data/rules/skills.json` |
| Scenario validation | every scenario check's attribute must be in the baseline list | `tests/test_scenario_data.gd` |
| A second, legacy set | `FIT / REF / INT / SOC / CYB / PSY` on 1–10, still implemented | `data/rules/core.json` |

Two consequences follow immediately.

1. **`CYB` is not new to NoöPunk.** The legacy 1–10 layer already had a Cybernetics attribute; the WN
   baseline dropped it in favour of CWN's six. Proposing it again is a *re-introduction*, and the
   legacy layer is the evidence that it was tried and set aside.
2. **The flat 8–13 band is the real constraint on splitting.** It is why adding attributes costs less
   than intuition suggests, and why keeping the old array costs more. See §4.

---

## 2. Load-bearing audit: what each attribute actually does

A seventh or eighth attribute needs procedures to hang on. This table asks, for each current code,
which rules would break if it vanished, and what a new code would have to own.

| Code | Procedures it drives | If removed |
| --- | --- | --- |
| STR | melee attack/damage choice, **encumbrance capacity** (`Stowed = STR`), Physical save | encumbrance and melee both lose their base |
| DEX | ranged attack/damage choice, Evasion save, AC | the shooting half of combat loses its modifier |
| CON | **HP per level**, **System Strain cap**, Physical save, **Effort** | three separate subsystems lose their number |
| INT | most knowledge/tech checks, Evasion save, hacking (`Int/Program`) | the skill system's largest domain collapses |
| WIS | Mental save, **Effort**, perception/insight checks | psionics and resistance to manipulation lose their base |
| CHA | Mental save, social checks (`Talk`, `Connect`, `Lead`, `Provoke`) | the social half of investigation loses its modifier |

Now the proposed additions:

| Proposed | Would need to own | Exists today as |
| --- | --- | --- |
| **CYB / Interface / Tech** | cyberware tolerance, hacking aptitude, BCI | `System Strain` (limit), `Interface` + `Program` skills, `Hardware` |
| **EMP** | reading people, emotional connection | `Connect`, `Talk`, `Kinesics`, `Perceive` skills |
| **WIL** | mental discipline, resistance, psionic focus | `WIS` (Mental save, Effort), `Psychic Defence` skill |
| **PRE** | presence, coercion, performance | `CHA`, `Talk`, `Provoke`, `Lead`, `Perform` |
| **NOE / Noesis** | noetic sensitivity | `Noöspace`, `ESP`, `Precognition` skills; PSI techniques |

**The pattern is consistent:** every proposed "missing" attribute already exists as *skills plus a
procedure*. That is an argument for splitting only where the skills are overloaded — not for adding an
axis because the word is missing.

---

### 2.1 Which skill list each name comes from (added 2026-10-28)

The memo cites skill names from **three different vocabularies in this repository**, and only one of them
is the adopted baseline. Naming them matters, because several arguments above say "this concept is already
covered by that skill" — and the answer changes with the list.

| vocabulary | file | status |
|---|---|---|
| **WN baseline, 19 skills** — `Administer`, `Connect`, `Drive`, `Exert`, `Fix`, `Heal`, `Know`, `Lead`, `Notice`, `Perform`, `Program`, `Punch`, `Shoot`, `Sneak`, `Stab`, `Survive`, `Talk`, `Trade`, `Work` | `data/rules/without_number.json` (`primary: CWN 2023`) | **authoritative** under the 2026-10-26 ruling |
| **PSI six** — `ESP`, `Telepathy`, `Psychokinesis`, `Precognition`, `Psychic Defence`, `Noöspace` | `data/rules/skills.json`, locked by #159 | authoritative **as the psionic subsystem**, and deliberately *not* part of the 19 |
| **legacy 40** — `Interface`, `Hardware`, `Perceive`, `Provoke`, `Investigation`, `Kinesics`, … | `data/rules/core.json` | **superseded** by the baseline; do not cite as current |

**Consequences for the arguments above**, so nobody implements against a retired name:

- "CYB is already covered" holds through **`Program` and `Fix`** (WN baseline), not `Interface` / `Hardware`
  (legacy). Hacking still resolves as `INT` + `Program`.
- "EMP is already covered" holds through **`Connect`, `Talk`** and **`Notice`**, not `Kinesics` / `Perceive`.
- "WIL is already covered" holds through **`WIS`** (Mental save, Effort) plus **`Psychic Defence`** — but
  that last one is a PSI skill, so it belongs to the psionic subsystem rather than to the 19.
- `Investigation` and `Provoke` are legacy names for things now done with `Notice`/`Know` and
  `Talk`/`Lead` respectively.

None of this changes an option, a cost or a recommendation: the overload finding survives, because the WN
baseline's `Notice` still carries perception while `WIS` carries judgment and willpower. It changes only
which name to write in an implementation.

## 3. Option M — minimal reskin (six codes, presentation only)

Keep `STR / DEX / CON / INT / WIS / CHA` in every file, save, check and test. Change what the player
reads, via `attributes.names` only:

| Code | Display label |
| --- | --- |
| STR | **Body Power** (or Might) |
| DEX | **Coordination** (or Reflexes) |
| CON | **Resilience** (or Vitality) |
| INT | **Reason** (or Intellect) |
| WIS | **Awareness** (or Resolve) |
| CHA | **Presence** |

- **Cost:** one JSON map + sheet labels. No migration, no save version bump, no scenario changes.
- **Gains:** tone. The sheet stops reading as a D&D character.
- **Does not answer:** empathy vs will, cybernetic aptitude, or "humanity".
- **Risk:** `WIS` still means perception *and* willpower *and* psionic focus at once; a player who wants
  a warm, perceptive but weak-willed detective cannot express it except through skills.

This is the same thing as **#716's option B**, and it remains the cheapest reversible experiment.

---

## 4. Option S — split (eight attributes)

Proposed set, from the issue: **MIG, REF, VIT, INT, CYB, EMP, WIL, PRE**.

Mapping from the current six:

| Current | Becomes | Rule |
| --- | --- | --- |
| STR | MIG | rename only |
| DEX | REF | rename only |
| CON | VIT | rename only; **still HP, Strain cap and Effort source** |
| INT | INT | unchanged |
| WIS | **EMP + WIL** | split: EMP = reading/connecting with minds; WIL = discipline, resistance, psionic focus |
| CHA | PRE | rename only |
| — | **CYB** | new axis; must own something |

### The arithmetic problem, precisely

The modifier table is flat from 8 to 13, so the cost of a split is not "lower average modifier" — it is
**lost concentration** if the point budget stays, or **inflated totals** if it scales.

| Budget | Example array | Mean | Net modifiers |
| --- | --- | --- | --- |
| Six, sum 63 | `14,12,11,10,9,7` | 10.5 | +1, 0, 0, 0, 0, −1 → **0** |
| Eight, same 63 points | `12,11,10,9,8,6,4,3` | 7.9 | 0, 0, 0, 0, 0, −1, −1, −2 → **−4** |
| Eight, 84 points | `14,13,12,11,10,9,8,7` | 10.5 | +1, 0, 0, 0, 0, 0, 0, −1 → **0** |
| Eight, 96 points | `14,14,13,12,12,11,10,10` | 12.0 | +1, +1, 0 … → **+2** |

(The degenerate eight-stat spread `8,8,8,8,8,8,8,7` also sums to 63 and nets only −1 — but it has no
specialisation at all. The honest comparison is a spread that still lets a character be good at
something.)

So splitting is only free if the generation budget rises with the attribute count (8 × 10.5 = 84).
Keeping the six-stat array would quietly make every eight-stat character worse at everything — a
balance change disguised as a reskin.

### Other consequences

- **Saves must be re-paired.** Cleanest semantic mapping: Physical `MIG+VIT`, Evasion `REF+INT`,
  Mental `EMP+PRE`, Luck none. That leaves **WIL in no save**, so WIL would have to earn its place
  through Effort and resistance procedures — otherwise it is a stat only psions care about.
- **Effort** must name its source: `1 + psi skill + better of WIL or VIT` (replacing WIS/CON). This is a
  real rule edit, not a rename, and belongs in `docs/rules/SWN_PSIONICS_ADAPTATION.md` if chosen.
- **Skills must be re-bound** across 40 entries — every one currently points at a code.
- **NPC stat lines** (HD-based, no attributes) are unaffected, which is a hidden benefit: NPCs do not
  need migration.
- **CYB still has no procedure.** CWN's hacking is `INT/Program`; cyberware is gear + Strain. Adding CYB
  means inventing a new resolution path, which the issue explicitly warns against ("do not confuse
  aptitude with purchased implants, gear or learned hacking skills"). **Recommendation: do not make CYB
  an attribute; make it a derived value or leave it to `Interface`.**

### What S buys

Real mechanical separation of *warmth* from *will*, and a place for "humanity" that is not a morality
meter. That is the strongest thematic case in the issue. It is also the option that requires a new
save pairing, a new array, an Effort edit and a 40-skill re-bind.

---

## 5. Option H — hybrid: six attributes + derived tracks (recommended for deliberation)

Keep the six codes and all arithmetic. Add **tracks and derived values** for the concepts that are not
properly attributes:

| Concept | Modelled as | Why not an attribute |
| --- | --- | --- |
| Cybernetic load | **System Strain** (already) | it is a capacity, not a capability; gear already modifies it |
| Technological aptitude | **`Interface` + `Program` skills** | CWN resolves hacking as `INT/Program`; a CYB attribute would need a new procedure |
| Empathy | **`Connect` / `Talk` / `Kinesics` skills** | expressible at skill granularity today |
| Will / noetic focus | **`WIS` + `Psychic Defence`** | WIS already feeds Effort; splitting it is Option S's cost |
| Humanity / identity | optional **track** (0–10), never a modifier | a track can move with choices without rewriting every check |
| Noetic sensitivity | **derived**: `WIS modifier + highest psychic skill` (for gates/descriptions only) | keeps SWN's Effort formula intact |

Option H answers Q4 (empathy ≠ morality) and Q7 (terminology) without touching the resolution maths:
"Humanity" becomes a track that records alienation and augmentation, not a stat that punishes the player
for installing an arm.

It also keeps the Godot sheet and every save valid, which matters for the CRPG.

**Weakness:** it does not give the *table* a WIL/EMP split. A player cannot write "high empathy, low
will" on the sheet as numbers — only as skills and roleplay. Whether that is enough is exactly the
question for playtesting.

---

## 6. Option 7 — seven-stat compromise

Split only the overloaded axis: **MIG, REF, VIT, INT, EMP, WIL, PRE** (no CYB).

- Array for seven: `14, 13, 11, 10, 10, 8, 7` (sum 73 ≈ 7 × 10.5), or reuse 63 if weaker characters are
  acceptable.
- Saves: Physical `MIG+VIT`, Evasion `REF+INT`, Mental `EMP+PRE`; WIL earns Effort + resistance.
- Cost: half of Option S (one split, no new axis), but still a 40-skill re-bind and an Effort edit.
- This is the **cheapest way to get the empathy/will distinction**, which is the issue's first idea and
  its most thematically load-bearing one.

If the author wants exactly one structural change, this is the one with the best ratio.

---

## 7. Compatibility matrix

| Surface | M (reskin) | 7 (split WIS) | S (eight) | H (hybrid) |
| --- | --- | --- | --- | --- |
| Codes in data/saves | unchanged | 6 → 7 | 6 → 8 | unchanged |
| Array | unchanged (63) | new (≈73) | new (≈84) | unchanged |
| Modifier table | unchanged | unchanged | unchanged | unchanged |
| Saves | unchanged | re-paired (WIL out) | re-paired (WIL out) | unchanged |
| System Strain (CON) | unchanged | VIT | VIT | unchanged |
| Effort formula | unchanged | WIL+VIT | WIL+VIT | unchanged |
| Skills (40) | unchanged | re-bind all | re-bind all | unchanged |
| Scenario checks | unchanged | must add code to baseline list | same | unchanged |
| Existing saves | valid | migration | migration | valid |
| Godot sheet | label change | schema + migration | schema + migration | label change |
| NPC stat lines | unaffected | unaffected | unaffected | unaffected |
| Tabletop cost | near zero | one split to learn | two new axes to learn | near zero + one track |

---

## 8. Effort and psionics (Q3)

SWN's Effort is the one formula that touches two attributes at once:
`1 + highest psychic skill + better of WIS or CON modifier` (repo: `SWN_PSIONICS_ADAPTATION.md`).

- Under **M** and **H**: unchanged.
- Under **7** and **S**: `WIS → WIL`, `CON → VIT`, so `1 + psi skill + better of WIL or VIT`. This keeps
  the "mind or body" shape and is the only defensible reading once WIS is split — but it must be written
  down, because the alternative (Effort from EMP) would make willpower irrelevant to psionics.
- **Torching** and commitments are duration mechanics; they are unaffected by any option here.

---

## 9. Empathy vs Humanity (Q4)

Agree with the issue's premise: **empathy is not morality**, and no attribute should be a morality
meter. Concretely:

- An android with high **EMP** and no legal personhood is a coherent, interesting character.
- A charismatic manipulator has high **PRE** and low **EMP**, and should be *effective*, not punished.
- "Humanity" as a 0–10 **track** (Option H) can fall with alienation, augmentation or atrocities
  without changing a single die roll. If it ever modifies checks, it becomes a morality stat by the
  back door — avoid.

---

## 10. Investigation (Q5)

The repository already answers this in `docs/design/ISSUE_704_GUMSHOE_INVESTIGATION.md`: **core clues are
not gated behind a roll**; access and competence are permission, and rolls decide exposure, quality and
optional advantages. The attribute choice does not change that rule — it only changes *which modifier*
is added when a roll is genuinely uncertain.

The one thing to protect: keep **at least two independent routes** to every core clue, spread across
different attributes (social `EMP/PRE`, physical `REF`, deductive `INT`, noetic `WIS`). Under a split,
that spread gets *easier*, because there are more distinct modifier sources; under M/H it already works
through skills.

---

## 11. Terminology (Q7)

| Candidate | Reads as | Innate? | Trained? | Collides with |
| --- | --- | --- | --- | --- |
| Cybernetics | a field of medicine | no | yes | the *gear* ("cyberware"), which is the thing it would measure |
| Interface | a capability to connect | partly | yes | `Interface` **skill** already exists — an attribute of the same name is a genuine confusion |
| Tech | broad competence | partly | yes | nothing, but flat in tone |
| Willpower | self-control | yes | partly | `Psychic Defence` skill |
| Psyche | the whole mind | yes | no | the legacy `PSY` attribute (1–10 layer) — a different scale |
| Noesis | noetic insight | yes | partly | `Noöspace` skill, PSI disciplines |

**Verdict for discussion:** "Interface" is disqualified as an attribute while the skill exists; "Psyche"
collides with the legacy layer; "Willpower" is the clearest label for a discipline stat. If no
structural split happens, none of these need to become attributes at all.

---

## 12. Illustrative builds (Q6)

Six archetypes, using the current array and the seven-stat array, to show what each option can and
cannot express. Scores are assignments of the arrays, not rolled characters.

| Archetype | Six-stat (M, sum 63) | Seven-stat (7, sum 73) | What the sheet cannot say |
| --- | --- | --- | --- |
| Brilliant low-tech detective | INT 14, WIS 12, CHA 11, CON 10, DEX 9, STR 7 | INT 14, EMP 13, WIL 11, PRE 10, VIT 10, REF 8, MIG 7 | under M, insightful + warm + low-tech is all "WIS 12" |
| Augmented hacker | INT 14, DEX 12, WIS 11, CON 10, CHA 9, STR 7 | INT 14, REF 13, VIT 10, WIL 10, EMP 9, PRE 9, MIG 8 | no axis for implant tolerance in either; Strain + `Interface` carry it |
| Charismatic unempathic manipulator | CHA 14, INT 12, DEX 11, CON 10, WIS 9, STR 7 | PRE 14, INT 13, WIL 10, REF 10, EMP 9, VIT 9, MIG 8 | **7 expresses this cleanly; M cannot** |
| High-empathy android | WIS 14, CHA 12, INT 11, DEX 10, CON 9, STR 7 | EMP 14, WIL 12, INT 11, PRE 10, VIT 9, REF 9, MIG 8 | M's WIS 14 also makes it strong-willed — wrong for the concept |
| Unaided psychic | WIS 14, CON 12, INT 11, CHA 10, DEX 9, STR 7 | WIL 14, VIT 12, INT 11, EMP 10, PRE 10, REF 8, MIG 8 | under 7, Effort is WIL+VIT — a clean fit |
| Psionically capable but fragile | WIS 14, CON 7, INT 12, CHA 11, DEX 10, STR 9 | WIL 14, VIT 7, EMP 12, INT 11, PRE 10, REF 10, MIG 9 | M handles this *well* today (WIS high, CON low) |

The pattern: **M already expresses "strong mind, weak body"**; it fails specifically on
*empathy-vs-will* and *presence-vs-empathy*. That is a narrower failure than the issue's eight-stat
sketch implies, and it is exactly what the seven-stat option fixes.

---

## 13. Tabletop and Godot (Q8)

- **Data contract:** every option except M/H introduces a new code list, which means a save-version
  bump, a migration, a new array, re-bound skills and an updated `tests/test_scenario_data.gd` list.
  M and H change no schema.
- **One sheet, two runtimes:** the Godot sheet reads `without_number.json`; display aliases can live in
  the same file, so tabletop and CRPG cannot drift.
- **NPCs:** CWN NPCs use HD-based attack bonuses and no attributes, so no option touches them. That is a
  meaningful cost saving worth stating in any decision.

---

## 14. Recommendation for deliberation (not a decision)

1. **Do M now** if the only goal is tone. It is reversible, costs one map, and settles nothing else.
2. **If a structural change is wanted, take option 7 (split WIS into EMP + WIL), not option S.** It fixes
   the issue's strongest complaint (empathy ≠ will) at half the migration cost, and it keeps CYB out of
   the attribute list where it has no procedure to own.
3. **Do not add CYB as an attribute.** It duplicates `System Strain` (capacity) and `Interface`/`Program`
   (aptitude), and would require inventing a hacking resolution that CWN already defines as `INT/Program`.
4. **Model Humanity as a track, never a modifier.**
5. **Revisit option S only with playtest evidence** that seven attributes cannot express a character the
   table actually wanted to play.

What would change this recommendation: a playtest where a player repeatedly wants "high EMP, low WIL"
*and* the seven-stat sheet still cannot express it; or a decision to make cybernetic aptitude a real
resolution path (which would give CYB something to own).

---

## 15. Open questions for the author

1. Is the goal **tone** (M), **expressiveness** (7/S), or **a new subsystem** (CYB with its own
   procedures)? The answer decides everything below.
2. If WIS splits, should **WIL appear in a save** (Mental) or only in Effort and resistance — and if it
   is in the save, what does EMP do mechanically besides skills?
3. Is the **array** allowed to grow with the attribute count (63 → 73/84), or must total competence stay
   fixed (which makes new attributes a net weakening)?
4. Must existing **saves** keep working, or is a versioned migration acceptable for a pre-release game?
5. Does **"humanity"** need numbers at all, or is it prose plus a track?
6. Which of `Interface` / `Cybernetics` / `Tech` is acceptable given the existing `Interface` **skill**?
7. Should the **legacy `FIT/REF/INT/SOC/CYB/PSY`** layer be renamed to match, left alone, or retired?
8. Is **seven** the ceiling of table complexity the author wants, regardless of what eight would model?

## 16. Decision-queue entries this memo creates

- **D51** — attribute presentation: keep codes / display aliases / new set (#716's A/B/C).
- **D52** — structural choice: six / seven (EMP+WIL) / eight (+CYB) / six + derived tracks.
- **D53** — empathy and humanity: skills + skills / optional track / attribute.
- **D54** — CYB: attribute / derived / skill-only.

None is recorded as decided. **D51–D54 were added to `docs/design/AUTHOR_DECISION_QUEUE.md` on
2026-10-28** so the questions are tracked rather than living only in this memo. The substance above is
unchanged, and no row has an answer.

---

## 17. Decision recorded 2026-10-28

The author authorised closing this issue with the recommendation above adopted. **Option H.**

**D51 — six attributes stay canonical.** `STR / DEX / CON / INT / WIS / CHA` remain the codes,
the 3–18 scale, the modifier bands, the saves and every derived quantity. The genuine problem
was not missing axes but **overload in two places** — `WIS` carrying perception, judgement,
willpower and psionic focus at once; `CHA` carrying both presence and connection — and that is
answered by **derived tracks**, not by a wider attribute row.

*Rejected:* **S** (eight attributes) because the arithmetic in §3 shows a split is free only if
the generation budget rises with the attribute count; keeping the six-stat array would have made
every character quietly worse at everything. **7** for the same reason with one fewer axis.
**M** (pure cosmetic reskin) survives as the presentation layer of H rather than as a separate
option.

**D52 — EMP and Humanity are not the same axis, and neither is morality.** Empathy is a capacity;
morality is a judgement; an android with high empathy and no legal personhood is a coherent
character and must not be punished by the sheet. Humanity / Identity / Alienation is an
**optional track**, never a score that falls when you install cyberware.

**D53 — CYB is not an attribute.** Technological capacity is `System Strain` (how much the body
will take), aptitude is `Interface` / `Program` / `Hardware` (what the character has learned) and
gear is gear. As an attribute it would penalise unaugmented characters by definition.

**D54 — investigation never hangs on an attribute roll.** #704 already settles that a competent
investigator obtains a core clue without a check. The attribute question is therefore only *how
good the extra reading of the evidence is*, never whether the clue can be found. Any future
change that makes a clue roll-dependent has broken the investigation layer.

**What this does not do:** it changes no code, no rulebook, no `data/rules/*.json`, and no Godot
adapter. The six codes are untouched, so the 1,429-test suite and every stored character remain
valid. The presentation vocabulary (`Might / Reflexes / Vitality / Intellect / Presence`) and any
derived track are **later, separate** work items.

**Reversibility:** D51–D54 are provisional and reversible in one sentence, like the other design
records here. If playtesting shows the sheet cannot express a genuinely warm but weak-willed
character, promoting one derived track to a real attribute is a smaller change than walking back
an eight-stat redesign — and this document is where that argument lives.
