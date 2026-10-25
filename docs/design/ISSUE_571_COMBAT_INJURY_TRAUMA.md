# Issue #571 — combat, injury and trauma: CWN/SWN against the two live models

**Status: design record and measurement. Not rules. No mechanic is approved, changed or
implemented by this file.**

Part of the [#564](https://github.com/TomiToivio/NooPunk/issues/564) epic. This is the
sub-issue [#571](https://github.com/TomiToivio/NooPunk/issues/571) deliverable: the
side-by-side of CWN/SWN damage, Shock, Trauma, mortal injury, stabilisation and healing
against **layer A** (the legacy NoöPunk ladder) and **layer B** (the crossover's Fate
stress/consequences), with the lethality claim *measured* rather than asserted.

Everything numeric below comes from one executable tool,
[`tools/issue571_lethality_lab.py`](../../tools/issue571_lethality_lab.py), whose contracts
are [`tests/test_issue571_lethality_lab.py`](../../tests/test_issue571_lethality_lab.py).
Re-run it rather than trusting this page:

```bash
python3 tools/issue571_lethality_lab.py          # the tables below
python3 tools/issue571_lethality_lab.py --json   # the same numbers, machine-readable
```

`rulebook/` and `RULEBOOK.md` were not edited. `src/rules/physical_combat.py` was **consumed, not
duplicated**: the lab calls its `wound_state()`, `armor_steps()` and `opposed_target_number()`,
so the measurement cannot drift from the chapter's arithmetic.

---

## 1. What is actually live in this repository

| | Layer A — legacy RPG | Layer B — crossover |
| --- | --- | --- |
| Attack | `STAT + Skill + 1d10 ≥ DV` (`src/rules/core.py`) | `4dF + skill` vs opposition (`strategy_game/rpg/fate.py`) |
| Harm | one rung of the §51 ladder per attack: **Scratched → Wounded → Critical → Down** | Fate stress boxes + consequences (`strategy_game/RULEBOOK.md` §7) |
| Armour | shifts the rung **one step up**, never past Scratched (`rulebook/3_PHYSICAL.md` §Armor) | an aspect or permission; no numeric mitigation |
| Damage roll | **none** — the margin of success *is* the severity | **none** |
| Action economy | 3 AP on the shared clock, descending **REF** (`rulebook/18_CROSS_DOMAIN_STATE.md`) | one action per character per turn (#461/#482) |
| Status | canonical for layer A; every number PROVISIONAL | approved kernel (#389/#482); combat is queue row **D34**, propagation is **D35** |

Both live models are **roll-once, resolve-once**: there is no second damage roll and no
hit-point track anywhere in the repository. That single fact decides most of the verdicts in §6.

## 2. CWN as published — the text the comparison uses

Read from the CWN SRD on **2026-10-25** (the mirror at `cwn.quadrifons.com`; it states it is
the SRD of Kevin Crawford's *Cities Without Number*, is public domain, and that it omits the
optional magic rules and the *Antagonists & NPCs* section — recorded here because that
omission is why §6 has nothing to say about NPC statlines):

- **Attack** — `1d20 + base attack bonus + attribute modifier + combat skill level` vs the
  target's Melee or Ranged Armor Class.
  <https://cwn.quadrifons.com/rules-of-the-game/combat/attacks-in-combat/>
- **Damage** — weapon die + the weapon's attribute modifier; armour provides **Damage Soak**
  which is subtracted before the damage reaches the wearer.
  <https://cwn.quadrifons.com/gear-vehicles-cyberware/weapons/weapon-stats-and-definitions/>
- **Trauma** — on a lethal hit, roll the weapon's Trauma Die; if it meets the victim's Trauma
  Target (usually 6) the hit is Traumatic and its **total damage is multiplied** by the
  weapon's Trauma Rating.
  <https://cwn.quadrifons.com/rules-of-the-game/combat/damage-trauma-shock/>
- **Shock** — melee weapons only: if the target's melee AC is at or below the weapon's Shock
  rating, the target takes the listed Shock damage **even on a miss**.
- **Mortal Injury** — at 0 HP a PC is Mortally Injured and dies at the end of the **sixth
  round** unless stabilised (a `Dex/Heal` or `Int/Heal` check at difficulty `8 + rounds since
  the fall`); a PC who took a Traumatic Hit in the same scene must also make a Physical save
  or roll on the **d12 Major Injury** table.
  <https://cwn.quadrifons.com/rules-of-the-game/injury-healing-system-strain/mortal-injury-stabilization/>
- **Firearms and armour used here** — Heavy Pistol `1d8`, TD `1d6`, `x3`; Rifle `1d10+2`,
  TD `1d8`, `x3`; Shotgun `3d4`, TD `1d10`, `x3`. Ordinary Clothing AC 10 / Soak 0; Armored
  Clothing AC 16 / Soak 5 / Trauma Target +1; Light Armored Suit AC 16 / Soak 5 / TT +2.

## 3. Method, and its limits

Every figure is **exact enumeration over `fractions.Fraction`** — no sampling, no seed, so the
tool is deterministic and two runs cannot disagree (pinned by
`test_the_tool_is_deterministic`). Layer A enumerates the 10 faces of the check die (100 in
opposed mode); CWN enumerates the d20, the weapon dice and the Trauma Die; layer B enumerates
all 81 `4dF` outcomes.

Comparability is stated, not assumed:

- **Layer A "competent professional"** = `STAT 5 + Skill 5 = +10` on the 1–10 scales.
- **CWN "level-1 competent"** = BAB `+1` (level), attribute modifier `+1`, skill level `1` →
  `+3`. A hit-point total of **5** is an *input* (`--cwn-hp`), because CWN rolls `1d6 + CON`
  per level and this record compares shapes, not builds.
- **Soak order** is genuinely ambiguous in the SRD: it says soak subtracts incoming weapon
  damage, and that a Traumatic Hit multiplies "the total damage of the hit". The lab applies
  the multiplier first and Soak second, and exposes `--soak-before-trauma` for the other
  reading; `test_soak_order_is_an_explicit_input_not_a_hidden_default` proves the two orders
  differ, so the assumption is visible rather than buried.
- **Not modelled**: cover, aiming, burst fire, suppressive fire, encumbrance, multiple
  attackers, healing between exchanges, and CWN's NPC statline rules (omitted by the SRD
  mirror). None of those change the qualitative findings; all of them would move the decimals.

## 4. Measured results

### 4.1 Layer A, simple mode, `+10` attacker — where one attack puts the target

| DV | Scratched | Wounded | Critical | Down | removal (Critical+Down) | attacks to removal |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 9 (Simple) | 0 % | 30 % | 40 % | 30 % | **70 %** | 1.43 |
| 13 (Everyday) | 30 % | 40 % | 30 % | 0 % | **30 %** | 3.33 |
| 15 (Difficult) | 50 % | 40 % | 10 % | 0 % | **10 %** | 10.00 |
| 17 (Professional) | 70 % | 30 % | 0 % | 0 % | **0 %** | never |
| 21+ (Heroic and up) | 100 % | 0 % | 0 % | 0 % | **0 %** | never |

### 4.2 Layer A, advanced (opposed) mode — `+10` attacker vs `REF 5 + Fray 5`

Scratched 55 % · Wounded 30 % · Critical 14 % · Down 1 % → **removal 15 %**, 6.67 attacks.

### 4.3 Layer B (crossover), `4dF + 3` vs opposition 2 — outcome shape only

| Outcome | Probability |
| --- | ---: |
| failure | 18.5 % |
| tie — succeed at a minor cost | 19.8 % |
| success | 43.2 % |
| success with style | 18.5 % |

Layer B's *harm depth* is authored in `strategy_game/RULEBOOK.md` §7 and deliberately not
re-derived here: the crossover's combat numbers are queue row **D34** and its consequence
propagation is **D35**, both open.

### 4.4 CWN as published — `+3` attacker, 5 hit points, attribute modifier `+1`

| Weapon | Target | hit | traumatic | expected damage per attack | down in one hit | attacks to down |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Heavy Pistol | Ordinary Clothing (AC 10, Soak 0) | 70 % | 16.7 % | 5.13 | **48.1 %** | 1.89 |
| Heavy Pistol | Armored Clothing (AC 16, Soak 5, TT 7) | 40 % | 0 % | 0.50 | 0 % | 12.21 |
| Rifle | Ordinary Clothing | 70 % | 37.5 % | 10.41 | **65.6 %** | 1.52 |
| Rifle | Armored Clothing | 40 % | 25 % | 3.13 | 22.0 % | 4.12 |
| Shotgun | Ordinary Clothing | 70 % | 50 % | 11.90 | **69.5 %** | 1.44 |
| Shotgun | Armored Clothing | 40 % | 40 % | 4.12 | 23.5 % | 3.71 |

### 4.5 The proposed import — CWN's Trauma Die on top of layer A's ladder

Row 7 of `ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md` proposes taking Trauma "as injury adjudication".
Expressed executably (a Traumatic Hit escalates two rungs, the ladder equivalent of `x3`):

| DV | plain removal | removal with Trauma | Down, plain | Down with Trauma |
| ---: | ---: | ---: | ---: | ---: |
| 13 | 30 % | 45 % | 0 % | 26.2 % |
| 15 | 10 % | 25 % | 0 % | 18.8 % |
| 17 | 0 % | 11.2 % | 0 % | 11.2 % |

---

## 5. Findings

1. **Layer A's lethality is inverse to difficulty.** Removal falls from 70 % at *Simple* to
   0 % at *Professional*, because the margin of success drives severity while the same margin
   drives success. Attacking an easy target is more dangerous than attacking a hard one. This
   is a real property of the implemented arithmetic (`test_removal_becomes_impossible_above_the_reachable_margin`),
   not a reading error — and it is a design question, not a bug an agent may fix.
2. **Above DV 17 a competent attacker cannot remove anyone at all.** `Down` needs margin ≥ 9
   and `Critical` ≥ 5; a `+10` attacker rolls 11–20, so the best possible margin against DV 17
   is 3. Heroic and Legendary difficulties produce *only* Scratches. Deadliness therefore has
   to be bought with difficulty **steps below** the attacker's reach, or with opposed checks.
3. **The two tactical modes are arithmetically identical and distributionally different.**
   `tests/test_issue219_physical_combat.py` proves the *function* is shared, which is what the
   chapter claims; it does not claim, and the lab shows it is not true, that the two modes are
   equally lethal (30 % simple at DV 13 vs 15 % opposed against a matched defender).
4. **Layer A already has Shock's idea, without a second number.** A miss lands on
   **Scratched** — measured as 100 % at a hopeless DV. CWN needs a Shock rating and an
   AC comparison to reach the same fiction; layer A gets it from the band function.
5. **Layer A's armour and CWN's Soak do different things.** A one-step shift can never zero a
   hit; subtraction can. A Heavy Pistol never one-shots an Armor Clothed target (0 %), and
   12.21 attacks are needed instead of 1.89 — a 6.5× swing produced entirely by Soak 5.
   This is why **row 10 of the #564 matrix cannot be imported as written**: `rulebook/3_PHYSICAL.md`
   §Armor states armour's effect is "a **ladder step**, never a subtraction" and does not stack.
6. **NoöPunk is not less deadly than CWN at matched competence — it is differently deadly.**
   One pistol shot removes an unarmoured 5-HP CWN character 48 % of the time and an unarmoured
   NoöPunk character 30 % of the time at Everyday difficulty; but NoöPunk's *cumulative* risk
   does not exist (state, not counter), while CWN's does (1.89 attacks).
7. **Trauma on top of the ladder double-counts severity.** The margin band already encodes how
   badly the target was hit; the Trauma Die re-encodes it a second time and turns 26 % of
   Everyday-difficulty *Wounded* results into **Down**. It cannot make layer A "more realistic"
   — only harsher, by an amount the author would have to own.
8. **CWN's most portable idea is not damage, it is the clock after it.** "Mortally Injured,
   dies at the end of the sixth round unless stabilised at difficulty `8 + rounds`" converts a
   state (`Down`) into a scene-level countdown with a rising price. Layer A has the state
   (`Down`, "dying or dead without intervention") and only a provisional "within the scene"
   for the clock.

## 6. Verdicts per CWN element

`DEFER` means the author has not authored the number and an agent may not. Every verdict is a
recommendation; none is enacted.

| CWN element | Verdict | Rationale | What importing it would break |
| --- | --- | --- | --- |
| `1d20 + BAB + attr + skill` vs AC | **OMIT** | Kernel is #111's `1d10` for layer A and #389/#482's `4dF` for layer B; the die choice is #566's open decision, not this row's. | `src/rules/core.py`, every layer-A check test, `RULEBOOK.md` §4.1–4.2 |
| Damage dice + hit-point pool | **OMIT** | The ladder is explicitly *a state, not a counter*; a pool reverses that and re-opens §51. | `tests/test_issue219_physical_combat.py` (`ladder is a state`, `no previous state`), §51 |
| Damage Soak as subtraction | **OMIT** | Contradicts `rulebook/3_PHYSICAL.md` §Armor in terms ("never a subtraction", no stacking). | §Armor, the 219 armour tests, §51's mitigation rule |
| Trauma Die (×3 severity) | **OMIT on layer A**; **DEFER for layer B** | Double-counts the margin (§5.7). For the crossover, harm is Fate stress/consequences and D34 decides combat; an extra severity roll would sit beside an approved model. | layer A: the band thresholds; layer B: D34/D35, the approved Fate harm model |
| Shock damage on a miss | **KEEP NoöPunk's equivalent — import nothing** | Layer A already lands a miss on Scratched (§5.4). CWN's Shock needs a second number to say the same thing. | nothing; already implemented |
| Major Injury d12 table | **DEFER** | The *shape* — a named, lasting injury when a character goes down — fits the `Down` rung and pairs with #516's consequence names (D35's closed menu). The table itself is CWN expression **and** would need author-authored entries. | cannot be landed without D35 and an authored table |
| Mortal Injury + `6 rounds` death clock | **DEFER — highest-value candidate** | Gives `Down` a countdown and stabilisation a rising difficulty (`8 + rounds`). Must be re-expressed in layer A's currency (**exchanges**, not 6-second rounds) and the number is the author's. | §51's "within the scene"; D3's unauthored recovery/injury timings |
| Stabilisation `Dex/Heal` at `8 + rounds` | **MODIFY (proposal)** | Layer A already names First Aid as the stabiliser (§51, `rulebook/3_PHYSICAL.md`); adopting a *rising* difficulty needs only a DV step per elapsed exchange, which the ladder already supports. | nothing structural; a PROVISIONAL number |
| System Strain (cyber/healing budget) | **DEFER to #572/D36** | It is a *capacity* question, not a combat one; the crossover's D36 is the live row and it already rejected a strain number (option C4). | D36, `rulebook/5_CYBERNETIC.md` capability model |
| Non-lethal attacks skip the Trauma Die | **KEEP NoöPunk's** | Layer A's non-lethal play is first-class and picks a rung directly (§51, #219); there is no second roll to suppress. | nothing |
| NPCs die instantly at 0 HP | **DEFER** | The cheap "mook" rule is genuinely useful, but the consulted SRD mirror omits the Antagonists & NPCs section, so this record will not describe a rule it could not read. | NPC statlines are #568/#572 territory |
| Group initiative `1d8 + best DEX` | **OMIT** | Layer A's shared clock orders exchanges by descending **REF** and the order may not be forked across realms. | `rulebook/18_CROSS_DOMAIN_STATE.md` §Initiative, `test_the_action_costs_agree_with_the_shared_contract` |
| Main / Move / On Turn / Instant actions | **OMIT** | Layer A has a six-action, 3-AP economy on one clock for every realm; CWN's four types are a second economy. | `rulebook/18` §The shared action economy |
| Natural healing / First Aid / poisons | **DEFER** | Recovery timings are unauthored (D3 `status_consequence_rows`); CWN's numbers are for its own HP model. | D3 |

### SWN

SWN contributes **no** combat content to this record. Its `swn` SRD licence is
**not established** in this repository's rights ledger
(`data/sources/game_system_rights.json`, `stars-without-number-srd`, decision
`blocked-unverified`), so nothing from SWN may be adapted before that changes — see
`docs/sources/GAME_SYSTEM_RIGHTS.md` §"Stars Without Number — deliberately not promoted".
CWN's SRD is CC0 and scope-limited to the SRD; the rows above cite only the SRD.

## 7. What a migration would break, concretely

- **`tests/test_issue219_physical_combat.py`** (20 tests) pins the ladder, the band thresholds,
  the "state, not counter" property, armour's one-step rule and the shared action costs. Any
  HP/Trauma/AC import re-opens that file.
- **`rulebook/3_PHYSICAL.md`** §Attacking/§Armor/§Wounds and **`RULEBOOK.md` §51** are the
  authored sources those tests mirror; they would have to be edited by the author, not by an
  agent.
- **`rulebook/18_CROSS_DOMAIN_STATE.md`** owns initiative and the action economy for *every*
  realm; a combat-specific economy would fork the one clock the chapter forbids forking.
- **Layer B** would lose an approved model: #389 approved the Fate foundation and #482 the
  skills; D34 is the open row for combat, and it already recommends "zone conflict, one action
  + one reaction, taken-out ≠ death". CWN's action types and HP pool are not compatible with
  that shape.
- **Nothing breaks by *not* importing**: the lab shows the live models already produce lethal,
  non-cumulative, single-roll combat.

## 8. What stays open — the author's, not an agent's

1. **Is layer A's inverse lethality (finding 1) intended?** If not, the fix is in the band
   mapping (severity relative to the *attacker's* margin vs the *target's* defence), which is a
   rule change, not a conversion.
2. **Does `Down` get a clock?** CWN's sixth-round clock is the portable idea; its currency in
   layer A is exchanges, and its length is unauthored.
3. **Is a lasting-injury table wanted at all**, and if so is it authored fresh (canon, per
   `AGENTS.md` §1) rather than transcribed from CWN's d12 list?
4. **D34/D35** remain the crossover's: tactical action economy and whether consequences leave a
   mission.
5. **D3's `status_consequence_rows`** remain the recovery/injury timings for the strategy layer.

## 9. What this record does not do

- It does not choose a chassis, a die, a damage model or a death clock (#566 owns the first).
- It does not edit `RULEBOOK.md`, `rulebook/`, `src/rules/physical_combat.py` or any rule
  number; the lab consumes those and adds nothing to the runtime path
  (`src/rules/physical_combat.py` is `IS_CANONICAL = False` already).
- It does not import a single line of CWN prose, table or statblock: the SRD figures quoted in
  §2 are the *inputs to a measurement*, not text added to the game.
- It does not review PR #573 — the corrections it carries are recorded in that PR's thread.

— Ai (愛)
