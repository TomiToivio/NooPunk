# #461 consensus — the single consolidated proposal

**Status: PROPOSAL. No rule, number, action list, dice procedure or capability is approved by this document.** `strategy_game/RULEBOOK.md` still reads **NO RULES APPROVED**; nothing here is written into it, and no code, data or rulebook file was changed. Tomi decides.

**What this edition is.** The consolidation the brief asked for, and the one the predecessor of this file asked for in its own words: *"the two should merge into one document rather than exist as two."* The former `ISSUE_461_RESKIN_SPEC.md` is folded in here as **§4**, and that file now points back to this one. There is **one** consensus proposal, one architecture and **one numbered decision register (§7)**.

**Provenance.** This merges the reconciled four-proposal consensus with the SRD crosswalk, the reskin specification, and the CWN/SWN addendum's design patterns. Every load-bearing claim below was checked against `main`; two earlier claims were corrected and are recorded as corrected (§3).

---

## 1. The architecture — unanimous across every proposal

The proposals are one design written several times; there is no sixth architecture to choose.

| Agreed | Evidence on `main` |
| --- | --- |
| **The kernel is approved (#389) and is not re-chosen.** | `strategy_game/RULEBOOK.md`; `rpg/RULEBOOK.md` is the playtest field manual |
| **The seam already exists.** `turn.py` resolves a check through the approved engine into the one append-only `HistoryLog`; only the strategic write path is reserved and refusing. | `turn.py`: `StrategicActionPending`, `record_declaration`, `record_character_check`, `StrategicActionPort`, `strategic_action`, `rule_outcome`, `LeaderRpgLayer` |
| **One sheet, two projections**, one identity by a shared id. | `rpg/RULEBOOK.md` §2; every proposal |
| **The axes that differ:** time, stakes (which of the six quantities), difficulty source, and where consequences land. | all |
| **Eligibility is a typed field, never read off an aspect name.** | `rpg/RULEBOOK.md` §2/§4; `characters.py` `TAG_KINDS` |
| **The capability vocabulary is already landed** — `TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`; `archetype_netrunner` carries a competence-kind tag. | `faction_creation.json`, `character_cards.json` |
| **One entry per competence; one-way, once-only.** | the 09:19 reconciliation comment; adopted by all |
| **Refusal at declaration, before any dice; an ineligible order is lost, not substituted.** | `council.py::structural_problems` |
| **A mission names which of the six quantities it aims at.** No universal scalar. | `quantities.py`; `MissionDeclaration.quantity` |
| **A scene settles an already-committed order and buys nothing.** | all |

---

## 2. The kernel and the seam, stated once

The approved mechanic is **4dF + skill = shifts**, with four actions (overcome, create an advantage, attack, defend) and four outcomes (fail, **tie**, succeed, succeed with style). Two consequences of reading the SRD rather than recalling it:

- **Fate Core's own structural sentence is the licence to reskin at all:** *"There are only a handful of basic game actions, but the number of potential contexts is infinite."* The four actions are fixed; the setting is the context. That is precisely "one kernel, two projections".
- **Fate's margin of 0 is a tie — success at a minor cost, not failure**, so clean-success and not-failing probability must stay distinct in any calibration. An earlier edition conflated them.

**One entry per competence, applied once, one-way.** A check emits one auditable outcome into the one `HistoryLog`; only an approved strategic consumer applies a typed effect, and only once. This is what makes a later zoom safe to replay.

---

## 3. Two corrections, adopted

1. **"Forced by arithmetic" was too strong.** The 4dF arithmetic proves a **difficulty number cannot express a very hard mission** — P(success) = `0.0000` once skill − difficulty ≤ −4, so roughly four ladder steps carry information. It does **not** prove a clock is mandatory; gates, opposed tests and staging are all legitimate. **Some** device beyond the ladder is required, and §4.7 now supplies the *precedent* for which; no fixed N-segment clock is pre-approved. This correction is retained in the text rather than only in the changelog.
2. **The tempo table is an upper bound, not a forecast** — it assumes every character spends every order on the same clock at equal odds.

---

## 4. The reskin — what is taken from each source (formerly `ISSUE_461_RESKIN_SPEC.md`)

### 4.0 The licence boundary decides the direction, not just the paperwork

`strategy_game/rpg/ATTRIBUTION.md` states the three references are **not interchangeable**: **Fate Core is CC BY 3.0** and is the **foundation whose mechanics are implemented**; **Transhumanity's Fate** and **Eclipse Phase** are **CC BY-NC-SA**, so they are **design references only** — none of their prose, setting or numbers may enter a distributable build, and the packaging guard records that boundary (`docs/licenses/RELEASE_CLEANUP_AUDIT.md`).

That is not a constraint to work around; **it is the method.** Transhumanity's Fate's own developer notes describe its approach as **minimalist** — it *"avoided creating new concepts and wherever possible built off existing Fate Core concepts"*: gear and augmentation as stunts or sub-aspects, bodies as simple containers, hacking as Contests, social favours as a Contacts roll. **Our reskin takes that move, not their text.** Everything below re-expresses an *idea* on a Fate Core kernel, in NoöPunk's own vocabulary.

### 4.1 From Fate Core — the kernel, implemented (unchanged, #389)

4dF + skill against opposition = shifts; the four actions; the four outcomes; aspects and fate points (invoke for **+2 or a reroll**, compel for a complication, refresh per session); the skill pyramid; stunts with GM approval; two stress tracks with two boxes by default and three consequence slots (mild / moderate / severe). The CC BY 3.0 notice is already shipped.

**★ Fate Core already contains the eligibility mechanism the thread spent four proposals designing.** The SRD's own technique:

> *"you might feel that there shouldn't be a base skill that allows just anyone to have medical training… However, **as a stunt for another, more general knowledge skill (like Lore), you can have one character be 'the doctor'** if that's what the player wants."*

**So a restricted capability is a stunt, by the SRD's own advice** — and the SRD supplies the price too: *"Taking a new stunt beyond the first three reduces your character's refresh rate by one."* The crossover therefore needs **no invented eligibility subsystem**: the typed `competence` field records *which* stunt, the stunt is the mechanism, and **refresh is the cost**. This is strictly better than a parallel "capability key", because it reuses the approved rulebook's own stunt rule instead of adding a concept — which is §4.0's method applied to itself.

**Also verified:** opposition is **active** (another character rolls) or **passive** (a rating on the ladder), and the SRD's own default is that **the difficulty is known to the player** — *"Is the Opposition Rating for a roll known to the player? 99% of the time, Yes."* A named-opposition device in the crossover is therefore **transparent by the SRD's default**, not a hidden GM number.

**One consequence worth stating:** Fate Core's default skill list is eighteen skills and the pyramid rates ten. The reskin needs **nine** (register B1).

### 4.2 From Eclipse Phase 2e — reskinned, and refused

Read at <https://eclipsephase.github.io> (character stats, pools, psi overview, the collected cheat-sheet). **Ideas only; nothing reproduced.** The EP licence is **not re-derived here** — the repository's audits (`docs/sources/`, `docs/licenses/`, `rpg/ATTRIBUTION.md`) remain the authority, and `docs/ATTRIBUTION_POLICY.md` the policy.

| # | EP element | There | The reskin (proposal) |
| --- | --- | --- | --- |
| 4.2.1 | **d100 roll-under with margins** | the resolution kernel | **Refused as a kernel; replaced by 4dF shifts.** A legacy percentile rating has **no numerical port** — a band→ladder guide is its own decision (R1), not a conversion this document asserts |
| 4.2.2 | **Six aptitudes** — Cognition, Intuition, Reflexes, Savvy, Somatics, Willpower | the foundation under skills; aptitude checks are `aptitude × 3` | **Kept as six *families* grouping a nine-skill list** (R2): Cognition → Investigate, Research; Intuition → Notice, Empathy; Reflexes → Athletics, Infiltration; Savvy → Negotiate, Deceive; Somatics → Physique; Willpower → Will, Psi. Families label the sheet; they are **not a second rating** |
| 4.2.3 | **Aptitude checks** when no skill applies | raw talent | **An untrained floor** (R3): use the aptitude family's base rather than Mediocre |
| 4.2.4 | **Ego vs morph** — the mind transfers, the body is expendable | the central stat distinction | **The sheet is the ego; the chassis is a card.** NoöPunk already carries `form`, and the EP2-2E material is mechanical-chassis canon — a **rename, not a new layer** |
| 4.2.5 | **Morph traits and implants** | permission, not arithmetic | **The typed competence gate**, grounded in EP's own design: a chassis grants *permission*, and permission is a field, never read off a name |
| 4.2.6 | **Pools** — Insight, Moxie, Vigor, Flex (+20, flip-flop, extra action, a clue, narrative control) | a second currency on top of the roll | **Fate points, plus one narrative use.** Adopt EP's wild-card idea *as a fate-point spend* (introduce a plausible NPC or item); **refuse a second pool currency.** EP's "+20" **is** Fate's "+2"; EP's flip-flop has **no 4dF analogue** (four dice cannot be flip-flopped) so it is refused or mapped to Fate's existing **reroll**. EP's own *"only 1 pool point may be spent per test"* is the precedent for one invoke's worth of stacking per check |
| 4.2.7 | **Wounds and trauma** | physical and mental harm | **Fate's stress and 2/4/6 consequences** — plus the join that makes "one sheet" real: a consequence maps onto the council status vocabulary (`injured`, `unavailable`, `compromised`, `exhausted`, `absent`), so the RPG wound and the strategic status are **the same state, not two** |
| 4.2.8 | **Resleeving tests** — integration, alienation, continuity | three checks for changing bodies | **One overcome per chassis change**, using the relevant family's skill; failure leaves an aspect, which is a Fate consequence, not a new track |
| 4.2.9 | **Psi** — a trait, sleights, strain, an Infection Rating; async abilities need a **biological substrate** | a full subsystem | **Competence tags plus consequences.** The vocabulary exists (`TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`); the cost is a consequence or a scene complication, and **no numeric psi subsystem** is proposed — the crossover rulebook forbids one. The substrate constraint becomes a **chassis `form` gate**: a synthetic chassis cannot use psi competences |
| 4.2.10 | **Seven reputation networks** | a social currency per network | **No rep subsystem.** A favour is a Contacts-flavoured check resolved against the strategic layer's **existing relationship edges and the six quantities** — the same move Transhumanity's Fate makes with social networks, and it **respects** the refusal of a universal scalar |

**Two shapes EP supplies that Fate lacks, and they are the crossover's genuinely missing failure semantics:**

- **Superior failure** (the 33/66 rule) — Fate has no graded failure.
- **A retry price — a cumulative −10 per retry.** Fate prices nothing for a second attempt.

Both land on the author's own pending row **`failure_effect`**. This is the first point at which the thread can say *where* failure handling should come from rather than only that it is open. EP's **±10 modifier ladder, capped at ±60**, is also the precedent for keeping **board contributions coarse** — the same instinct as "board modifiers must be band-level".

**Character generation: a thirteen-step sequence to reduce, not to invent.** EP 2e's creation is thirteen steps — Background, Career, Interest (skill packages), Faction, Aptitude Template, Total Skills, Languages, Flex, Reputation, Customization, Derived Stats, Starting Morph & Gear, Motivations. The reduction is legible: the skill packages and aptitude template collapse into the **existing card** (high concept, trouble, ≤3 aspects, a rated ladder); Faction is already a crossover concept; **Motivations** supply high concept and trouble; **Morph & Gear** becomes equipment/body tags; **Languages, Derived Stats and the customization pass are cut.** A **five-or-six-step** sequence derived from a real one (R6).

**Ego vs morph grounds a decision the crossover already made.** `rpg/RULEBOOK.md` tracks **physical and mental stress separately**; EP splits exactly there — physical resilience is a **morph** stat (Durability, Wound Threshold) and mental resilience an **ego** stat (Lucidity, Trauma Threshold, Insanity Rating). So the two stress tracks are not an invention: **physical stress is morph, mental stress is ego** — and *"do not assume commonplace resleeving"* is exactly why the morph half must be **gear and body aspects on the one card**, never a resleeving economy.

### 4.3 From Transhumanity's Fate — the precedent, adopted as method

Developer notes read at <https://eclipsephase.com/2016/03/26/transhumanitys-fate-developer-notes/>.

| # | What it does | What NoöPunk adopts |
| --- | --- | --- |
| 4.3.1 | Presents a complex setting **minimalist**: no Extras; a subsystem is built **off existing Fate Core concepts** | The method for §4.2, and the standing test for any addition: *if it needs a new concept, prefer the existing Fate Core one* |
| 4.3.2 | **Gear and augmentation as stunts or sub-aspects; bodies as simple containers** | Chassis cards carry stunts and sub-aspects; equipment does not become a sheet (R4) |
| 4.3.3 | **Morph traits as permission** | The competence gate (4.2.5) and its chassis counterpart |
| 4.3.4 | **Ego aspects (high concept, trouble, plus two) and two morph aspects** | Four ego aspects on the sheet, two chassis aspects on the card — **six total**, and the split is the ego/morph line made playable |
| 4.3.5 | **Morph refresh cost** — an augmented body is paid for out of starting refresh | Adopted (R5): an upgraded chassis costs fate points, so embodiment matters **without a second economy** |
| 4.3.6 | **Morph versus ego consequences** distinguished | A chassis consequence can be repaired or abandoned; an ego consequence follows the mind |
| 4.3.7 | **Contests as the device for extended effort** (hacking as a Contest; contests under fire) | **The missing evidence for the mission device (B2):** a **contest** is the Fate-native way to express a mission taking more than one exchange, with a clock as its pacing dial — not a new subsystem |

### 4.4 The CWN / SWN addendum — adopted as shapes, not kernels

Its **assets as typed, place-bound affordances** is the same idea as a chassis granting permissions (4.2.5), and its **rejection of one-faction-action-per-turn** is right for a five-order turn. **Dune's architect-versus-personal lens** remains the framing; **its dice engine is not imported**, and neither system supplies a kernel.

---

## 5. The forks, with the positions the reviews converged on

**Fork 1 — five actors, read as (A).** *Recommended:* five active characters (leader + four agents, one action each); the four **agent portfolios are posts**, not an upper bound on actors; the leader holds a distinct chair. The brief's words are about per-turn actions, and `roster_size` / `founder_authority` already put the question. **Cost:** `council_size.value`, the cap check, `LEADER_COUNCIL_SYSTEM.md` §1/§2/§7 and the parties' four `leader_ids` move **together or not at all**. **(B)** — the leader occupies one of four seats, so the faction acts four times — stays available and is the cheaper edit.

**Fork 2 — the board is a gate, not a modifier.** *Recommended:* position decides **legality and reach**; the GM's difficulty stays the only number in a check. The repository already does this (`cyber.py::resolve_access` — *"No numbers, no odds"*), the design record's rule is **"gate vs modify — never both"**, and §4.2 adds EP's corroboration: even EP **caps** stacked modifiers rather than letting them accumulate.

**Fork 3 — the MVP is one gated check per order.** *Recommended:* one order → one bounded resolution → one applied outcome, with an optional scene that narrates it and grants nothing; staged missions deferred. Nothing in the repository reads a clock today. **This does not contradict §3** — for a genuinely hard undertaking something beyond the ladder will be needed, and §4.3.7 is now the precedent for what.

**On all three the recommendation is not the decision.**

---

## 6. `council.json` already carries ten author decisions

`roster_size`, `founder_authority`, `refusal_effect`, `passive_magnitude`, `leader_attributes`, `failure_effect`, `turn_unit`, `status_consequence_rows`, `mission_resolution`, `event_deck_and_effects` — written by the author, in the author's vocabulary. **`founder_authority` *is* readings (A) and (B): *"Is the founder one of the four leaders, or a fifth authority over them?"*** Much of what several proposals were asking as a fresh list was already open, recorded and waiting.

---

## 7. The decision register — one list, deduplicated

**Group 0 — already recorded by the author.** The ten rows in §6. Not re-opened here; their values are the author's.

### Blocking — nothing downstream can be built until these two are answered

| # | Decision | Home |
| --- | --- | --- |
| **A1** | **The cap: four or five** — and if five, reading **(A)** (leader in a distinct chair) or **(B)** (leader in one of four seats, faction acts four times) | `roster_size`, `founder_authority` |
| **A2** | **The shifts → named-quantity mapping** — what a success, a success with style and a failure are each worth against one named quantity | `mission_resolution` |

### Answered as proposals — need acceptance, not design

| # | Decision | Answer proposed in |
| --- | --- | --- |
| **B1** | **The skill list** — nine skills under the six aptitude families | §4.2.2 |
| **B2** | **The mission's second device** — a **contest**, with a clock as its pacing dial | §4.3.7 |
| **B3** | **Competence and psi handling** — typed permissions, consequence costs, chassis `form` gate, no numeric psi subsystem | §4.2.5, §4.2.9 |

### New rows from this consolidation

| # | Decision |
| --- | --- |
| **R1** | Is there a **band→ladder porting guide** for legacy percentile content, or is legacy content re-authored instead? |
| **R2** | The **nine-skill list** under the six aptitude families — accept, amend or replace *(the row B1 answers)* |
| **R3** | The **untrained floor**: the aptitude family's base, or Fate's Mediocre default? |
| **R4** | **Equipment as stunts / sub-aspects on the chassis card**, rather than items with statistics |
| **R5** | The **chassis refresh cost**: does an upgraded chassis reduce starting fate points? |
| **R6** | **Character generation** as a five-or-six-step reduction of EP's thirteen, on the existing card |
| **R7** | **The board: gate or modifier** — not in the ten; *"gate vs modify — never both"* |
| **R8** | **Does movement always consume the order?** — no row exists |
| **R9** | **Clock length**, if any — follows from A2, only if a clock is chosen |
| **R10** | **Do scene consequences persist into the same turn's mission?** — recommendation: yes; one clock, one turn, one record |
| **R11** | **Zoom versus prolonged operation; are refused orders replaced?** — recommendation: zoom only; refused orders are lost |
| **R12** | **One metacurrency: keep Fate points and refuse EP's pools** — or run both |
| **R13** | **Is the capability gate a stunt, with refresh as its cost?** — §4.1's find; **this is the row that deletes a subsystem**, because the SRD already has the mechanism and the price |
| **R14** | **Does the crossover want superior-failure severity and a retry price at all?** — EP has both, Fate neither; lands on `failure_effect` |

**R13 is the most valuable row in this list**, because it **removes** work four proposals were doing: the eligibility subsystem they were designing already exists in the approved rulebook as a stunt, with refresh as its published cost. **R2/B1 and R13 are the same insight applied to skills and to capabilities respectively** — prefer the existing Fate Core concept.

---

## 8. What is not being reopened

The **Fate kernel** (#389) and the **history/audit seam** (#397, #347). **`quantities.py`'s six distinct quantities** — no universal scalar. **One action per named character per turn.** The crossover rulebook's **NO RULES APPROVED** status. **Licensing** per §4.0. **Dune, PbtA, The Sprawl, The Veil and the CWN/SWN material contribute lenses and shapes, not mechanics.**

---

## 9. After approval — the smallest first step

A **payload schema** in `strategy_game/rpg/` and the **mapping table** in data. Then behaviour tests only: five (or four) distinct one-action actors; a pre-roll denial; capability-versus-belief; valid travel; **no double application on zoom**; and faithful per-quantity changes. No prose tests ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Not claimed:** none of this is implemented, and no rulebook, data or code file was changed by this document.

— Ai 愛 (consolidated; no rule approved)
