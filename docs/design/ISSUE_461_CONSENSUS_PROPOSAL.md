# #461 consensus — consolidated edition, with the SRD crosswalk

**Status: PROPOSAL. No rule, number, action list, dice procedure or capability is approved by this document.** `strategy_game/RULEBOOK.md` still reads **NO RULES APPROVED**; nothing here is written into it and no code changed. Tomi decides.

**What this edition adds.** The previous edition reconciled the four consensus proposals. This one does what the brief asked and the four proposals did not: it **reads the two SRDs** and grounds the reskin in what those rules actually say. Everything quoted below was fetched and read this session; where a claim could not be verified it is marked rather than assumed.

---

## 1. The architecture: unanimous across all four proposals

The four proposals are one design written four times; there is no sixth architecture to choose.

| Agreed | Evidence |
| --- | --- |
| **The kernel is approved (#389) and is not re-chosen.** | `strategy_game/RULEBOOK.md`; `rpg/RULEBOOK.md` is the playtest field manual |
| **The seam already exists.** `turn.py` resolves a check through the approved engine into the one append-only `HistoryLog`; only the strategic write path is reserved and refusing. | `turn.py` defines `StrategicActionPending`, `record_declaration`, `record_character_check`, `StrategicActionPort`, `strategic_action`; carries `rule_outcome`, `LeaderRpgLayer` |
| **One sheet, two projections**, one identity by shared id. | `rpg/RULEBOOK.md` §2; all four proposals |
| **The axes that differ:** time, stakes (which of the six quantities), difficulty source, **where consequences land**. | all four |
| **Eligibility is a typed field, never read off an aspect name.** | `rpg/RULEBOOK.md` §2/§4; `characters.py` `TAG_KINDS` |
| **The capability vocabulary is already landed** — `TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`; `archetype_netrunner` carries a competence-kind tag. | `faction_creation.json`, `character_cards.json` |
| **One entry per competence; one-way, once-only.** | the 09:19 comment; adopted by all |
| **Refusal at declaration, before any dice; an ineligible order is lost, not substituted.** | `council.py::structural_problems` |
| **A mission names which of the six quantities it aims at.** No universal scalar. | `quantities.py`; `MissionDeclaration.quantity` |
| **A scene settles an already-committed order and buys nothing.** | all four |

## 2. Two corrections to this document's earlier editions, adopted

1. **"FORCED BY ARITHMETIC" was too strong.** The arithmetic proves that a **difficulty number cannot express a very hard mission** (P(success) = `0.0000` at skill − difficulty ≤ −4; ~four informative ladder steps). It does **not** prove a clock is mandatory — gates, opposed tests and staging are legitimate. **Some** device beyond the ladder is required; which device is the author's, and no fixed N-segment clock is pre-approved.
2. **The tempo table is an upper bound, not a forecast** — it assumes every character spends every order on the same clock at equal odds.

One refinement both imply: **Fate's margin of 0 is a tie — success at a minor cost, not failure** — so clean-success and not-failing probability must stay distinct. The verifier fails if the disproven wording survives.

## 3. `council.json` already carries ten author decisions

`roster_size`, `founder_authority`, `refusal_effect`, `passive_magnitude`, `leader_attributes`, `failure_effect`, `turn_unit`, `status_consequence_rows`, `mission_resolution`, `event_deck_and_effects` — written by the author, in the author's vocabulary. **`founder_authority` *is* readings (A) and (B): *"Is the founder one of the four leaders, or a fifth authority over them?"*** Most of what four proposals were asking as a fresh list was already open, recorded and waiting.

---

## 4. The SRD crosswalk — what the two systems actually say

Read this session. Each row is **adopt / reskin / refuse**, with the reason. The governing constraint is the brief's own: *build on modified/reskinned Fate Core, Eclipse Phase and Transhumanity's Fate*, while `rpg/RULEBOOK.md`'s approved kernel is already Fate — so **Fate supplies the mechanism and the two transhuman sources supply the vocabulary and the constraints.**

### 4.1 Fate Core (CC BY 3.0 — verified on the SRD's own licensing line)

**The core procedure, verified:** choose the skill appropriate to the action → roll four Fate dice (−1/0/+1 each) → add the skill rating → the total is the result on the ladder → *"If you invoke an aspect, add +2 to your result or reroll the dice."* Opposition is **active** (another character rolls) or **passive** (a rating on the ladder), and the SRD's own guidance is that **the difficulty is known to the player** — *"Is the Opposition Rating for a roll known to the player? 99% of the time, Yes."* This matters for the crossover: a named-opposition device is **transparent by the SRD's own default**, not a hidden GM number.

**The four actions, verbatim:** *Overcome* — "tackle some kind of challenge, engaging task, or hindrance related to your skill"; *Create an Advantage* — "discover and create aspects, and lets you get **free invocations** of them"; *Attack* — "harm someone in a conflict… physical, mental, emotional, or social"; *Defend* — "keep someone from harming you, getting past you, or creating an advantage to use against you." And the key structural sentence: *"There are only a handful of basic game actions, but the number of potential contexts is infinite."*

**That last sentence is the crossover's licence to reskin at all:** the four actions are fixed, the *contexts* are the setting. This is exactly the "one kernel, two projections" shape — the projections differ in context, not in action.

**★ The find, and it settles a question all four proposals argued about.** The eligibility debate ran: *a capability must be a field, never read off an aspect name.* Fate Core independently recommends the mechanism:

> *"you might feel that there shouldn't be a base skill that allows just anyone to have medical training… However, **as a stunt for another, more general knowledge skill (like Lore), you can have one character be 'the doctor'** if that's what the player wants."*

**So the restricted capability is a stunt, by the SRD's own technique** — and the SRD supplies the acquisition cost too: *"Taking a new stunt beyond the first three reduces your character's refresh rate by one."* The crossover therefore needs no invented eligibility subsystem: the **`competence` tag records which stunt**, the stunt is the mechanism, and **refresh is the price**. This is strictly better than the proposals' "capability key", because it reuses the approved rulebook's own stunt rule (*stunts are "distinct named exceptions requiring GM approval"*) instead of adding a parallel concept.

### 4.2 Eclipse Phase 2e (licence recorded by this repository, not re-derived here — see §4.3)

**The resolution chassis, verified:** percentile **d100 roll-under**; *"The target number is based on the character's skill, aptitude check, or rep network score. If the result is equal to or less than the target number, the test succeeds."* Modifiers come in **multiples of ten** (+10…+30 easy, −10…−30 hard), and *"No set of multiple modifiers should impact a test by more than +/−60."* Two test types: **success** tests and **opposed** tests. Retrying carries a **cumulative −10** (*"your first re-try will be at −10, your second at −20"*). Superior results use the **33/66 rule**: ≥33 that succeeds is one superior success, ≥66 is two; ≤66 that fails is a superior failure, ≤33 is two.

**Adopt or refuse, precisely:** the **d100 chassis is refused** — the crossover's kernel is approved as 4dF, and the brief forbids assuming percentile rolls. Its *shapes* are adopted where Fate lacks them: **opposed tests** map onto Fate's active opposition; EP's deadlock on a tie maps onto Fate's **tie = succeed at a minor cost**; and the **±10 modifier ladder is the precedent for keeping board contributions coarse** — EP itself refuses to let stacked modifiers exceed ±60, which is the same instinct as the earlier "board modifiers must be band-level" finding.

**★ The find, and it is a gap neither system fills alone.** EP has **superior failure** (33/66) and a **retry penalty**; Fate Core has neither — its failure is simply failure, and nothing prices a second attempt. **Those two are the crossover's genuinely missing failure semantics**, and they land squarely on the author's own pending row **`failure_effect`**. This is the first time the thread can point at *where* failure handling should come from rather than only that it is open.

**Pools — and the metacurrency collision.** EP 2e runs **four pools**: **Insight** (mental: COG, INT), **Moxie** (social: SAV, WIL, also rep and infection tests), **Vigor** (physical: REF, SOM), and **Flex** (wild-card, any test *and* narrative control). Spend options, verified: ignore all modifiers; **+20 to the target**; **flip-flop the d100** (83 becomes 38); upgrade a success to superior; downgrade a critical failure; or an ongoing +5/+10 to linked skills. *"Unless otherwise noted, only 1 pool point may be spent per test."* And crucially, **Pools are a morph stat** — *"Your morph provides you with pools."*

**The collision is real and must be decided:** Fate already has **Fate points** (invoke for +2 or reroll; compels; refresh), and `rpg/RULEBOOK.md` already specifies them (*"at least three Fate points at session start"*). **Two metacurrencies in one kernel double the economy.** The reskin is clean and I recommend it: **keep Fate points as the only metacurrency**, and read EP's pool options as *flavours of an invoke* — EP's "+20 to the target" **is** Fate's "+2", and EP's "flip-flop" has **no 4dF analogue** (four Fate dice cannot be flip-flopped), so it is either **refused** or mapped to Fate's **reroll**, which the approved rulebook already grants. EP's own cap — one pool point per test — is the precedent for one invoke's worth of stacking per check.

**★ Ego vs Morph, which the brief already half-states.** EP's *"most important distinction"* is **ego** (mind, personality, memories, traits, **skills** — *"transfers with you"*) versus **morph** (the body, providing **pools**, **Durability**, implants, and its own traits). Ego stats include Initiative, **Lucidity**, **Trauma Threshold**, **Insanity Rating**, traits, motivations, some Flex. Morph stats include Pools, **Durability**, **Wound Threshold**, **Death Rating**, morph traits. Six aptitudes: **Cognition, Intuition, Reflexes, Savvy, Somatics, Willpower**.

**This grounds a design decision the crossover already made.** `rpg/RULEBOOK.md` tracks **physical and mental stress separately** (two boxes each, plus consequences 2/4/6). EP splits exactly there: **physical resilience is a *morph* stat** (Durability, Wound Threshold) and **mental resilience is an *ego* stat** (Lucidity, Trauma Threshold, Insanity Rating). So the two stress tracks are not an invention — **physical stress is morph, mental stress is ego**, and the brief's *"do not assume commonplace resleeving"* is exactly why the morph half must be **gear and body aspects on the one card**, never a resleeving economy.

**★ Character generation: a 13-step sequence to reduce, not to invent.** EP 2e's creation is thirteen steps — Background, Career, Interest (**skill packages**), Faction, **Aptitude Template**, Total Skills, Languages, **Flex**, **Reputation**, Customization, **Derived Stats**, **Starting Morph & Gear**, **Motivations**. The crossover's acceptance criterion asks for *"a compact character sheet and generation sequence"* and the brief says to **simplify further**. The reduction is legible: the three skill packages and the aptitude template collapse into the repo's **existing card** (high concept, trouble, ≤3 aspects, a rated skill ladder); Faction is already a crossover concept; **Motivations** supply the high concept and trouble; **Morph & Gear** becomes equipment/body tags; **Languages, Derived Stats, and the customization pass are cut**. That is a **five-or-six-step** sequence derived from a real one rather than invented.

**★ Reputation, which bridges to the six quantities.** EP's step 9 assigns **rep scores across different social networks**, and Moxie can *"refresh rep favors"*. This is **per-network, not one score** — the same shape as `quantities.py`'s six non-interchangeable quantities, and the natural character-side analogue of a faction's institutional access. It is the cleanest available bridge between the individual and the faction layer, and it **respects the refusal of a universal scalar** rather than contradicting it.

### 4.3 Licensing, stated carefully

The Fate Core SRD page I read states its own licence — *Creative Commons Attribution 3.0 Unported* — and that **Transhumanity's Fate and Eclipse Phase 2e are CC BY-NC-SA** is recorded in this repository (`docs/sources/EXTERNAL_SOURCE_LICENSES.md`, `docs/sources/GAME_SYSTEM_RIGHTS.md`, `docs/licenses/`, `rpg/ATTRIBUTION.md`). **I did not re-derive the EP licence from the SRD's footer this session and so do not restate it as a fresh finding**; the repository's audits remain the authority, and `docs/ATTRIBUTION_POLICY.md` the policy. The practical consequences are unchanged and worth repeating because this section *quotes* both systems: **attribution and notice-of-modification are required for the CC BY material**, the NC-SA terms **do not** become permissive because Fate Core's does, **ideas are separated from copied expression**, and nothing here is legal advice.

---

## 5. The forks, with the positions four reviews converged on

**Fork 1 — five actors, read as (A).** *Recommended:* five active characters (leader + four agents, one action each), four portfolios as posts held by four agents, the leader in a distinct chair. The brief's words are about per-turn actions; `roster_size` and `founder_authority` already put the question. **Cost:** `council_size.value`, the cap check, `LEADER_COUNCIL_SYSTEM.md` §1/§2/§7 and the parties' four `leader_ids` move **together or not at all**. **(B)** stays available and is the cheaper edit.

**Fork 2 — the board is a gate, not a modifier.** *Recommended:* position decides **legality and reach**; the GM's difficulty stays the only number in a check. The repository already does this (`cyber.py::resolve_access` — *"No numbers, no odds"*), and the design record's rule is **"gate vs modify — never both."** §4.2 adds EP's corroboration: even EP caps stacked modifiers rather than letting them accumulate.

**Fork 3 — the MVP is one gated check per order.** *Recommended:* one order → one bounded resolution → one applied outcome, with an optional scene that narrates it and grants nothing; staged missions deferred. Nothing in the repository reads a clock today. **This does not contradict §2's correction** — for a genuinely hard undertaking something beyond the ladder will be needed, and that is `mission_resolution`'s call.

**On all three the recommendation is not the decision.**

## 6. The decision list

**Already recorded by the author** (ten rows in `council.json`): `roster_size`, `founder_authority`, `mission_resolution`, `failure_effect`, `leader_attributes`, `passive_magnitude`, `turn_unit`, `refusal_effect`, `status_consequence_rows`, `event_deck_and_effects`.

**Genuinely new — five from the reconciliation, plus four the SRD crosswalk surfaces:**

| # | New decision | Where it comes from |
| --- | --- | --- |
| 1 | **The board: gate or modifier** | not in the ten; *"gate vs modify — never both"* |
| 2 | **Does movement always consume the order?** | raised downstream; no row exists |
| 3 | **Clock length**, if any | follows from `mission_resolution`, only if a clock is chosen |
| 4 | **Do scene consequences persist into the same turn's mission?** | recommendation: yes — one clock, one turn, one record |
| 5 | **Zoom versus prolonged operation; are refused orders replaced?** | recommendation: zoom only; refused orders are lost |
| 6 | **★ One metacurrency: keep Fate points and refuse EP's pools** — or run both | §4.2: EP's four pools collide with the approved Fate points |
| 7 | **★ Is the capability gate a stunt, with refresh as its cost?** | §4.1: Fate's own "one character is the doctor" technique plus the refresh price |
| 8 | **★ Does the crossover want superior/failure severity and a retry price at all?** | §4.2: EP has both; Fate has neither — lands on `failure_effect` |
| 9 | **★ Is character generation a five-or-six-step reduction of EP's thirteen, on the existing card?** | §4.2; the brief's "simplify further" and the "compact sheet" criterion |

**Decisions 6–9 are new to the thread** and come only from reading the SRDs. Decision 7 is the one I would call the most valuable, because it **deletes** a subsystem the four proposals were designing: the SRD already has the mechanism and the price.

## 7. What is not being reopened

The **Fate kernel** (#389) and the **history/audit seam** (#397, #347). **`quantities.py`'s six distinct quantities** — no universal scalar. **One action per named character per turn.** The crossover rulebook's **NO RULES APPROVED** status. **Licensing** per §4.3. Dune, PbtA, The Sprawl and The Veil contribute **lenses, not mechanics**.

## 8. After approval — the smallest first step

A **payload schema** in `strategy_game/rpg/` and the **mapping table** in data. Then behaviour tests only: five (or four) distinct one-action actors, a pre-roll denial, capability-versus-belief, valid travel, **no double application on zoom**, and faithful per-quantity changes. No prose tests (#271).

— Ai 愛 (consolidated; no rule approved)
