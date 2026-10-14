# #461 consensus — consolidated edition

**Status: PROPOSAL. No rule, number, action list, dice procedure or capability is approved by this document.** `strategy_game/RULEBOOK.md` still reads **NO RULES APPROVED**; nothing here is written into it and no code changed. Tomi decides.

**What this edition is.** Four consensus proposals now exist on #461 — this document (11:36), and three comments at 11:37, 11:37 and 11:39. They were written in parallel and they **agree on the architecture**; they differ in what they *recommend* and in what they *noticed*. This edition reconciles them into one, **corrects two claims in its own previous edition** that a later comment rightly challenged, and — the substantive change — **folds the whole decision list onto the author's own ten recorded decisions**, so the question is not "how many rows does the consensus list" but "which rows are genuinely new".

---

## 1. The architecture: unanimous across all four proposals

The four proposals are one design written four times. Every load-bearing claim below was re-verified against `main` by at least two of them, including me:

| Agreed | Evidence |
| --- | --- |
| **The kernel is approved (#389) and is not re-chosen.** The task is the crossover seam, not an engine. | `strategy_game/RULEBOOK.md` opens with the #389 approval; all four proposals refuse a second strategic die |
| **The seam already exists.** `turn.py` resolves a check through the approved engine into the one append-only `HistoryLog`; only the strategic write path is reserved and refusing. | `turn.py` really defines `StrategicActionPending`, `record_declaration`, `record_character_check`, `StrategicActionPort`, `strategic_action`, and carries `rule_outcome`, `LeaderRpgLayer`, `strategy_game.rpg.fate` |
| **One sheet, two projections** — one character record, one identity by shared id. | `rpg/RULEBOOK.md` §2; all four proposals |
| **The four axes that differ:** time, stakes (which of the six quantities is aimed at), difficulty source, and **where consequences land** (character vs faction). | established by the 09:19 comment, adopted downstream |
| **Eligibility is a typed field, never read off an aspect name.** | `rpg/RULEBOOK.md` §2/§4; `characters.py` `TAG_KINDS` = belief / competence / equipment / relationship / asset / goal |
| **The capability vocabulary is already landed.** | `faction_creation.json` competence family `TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`; `character_cards.json` `archetype_netrunner` with a competence-kind tag |
| **One entry per competence; one-way, once-only.** Faction assets add reach and capacity, never a substitute skill, and nothing flows back from the board into character state. | the 09:19 comment's rule; adopted by all |
| **Refusal at declaration, before any dice; an ineligible order is lost, never substituted.** | `council.py::structural_problems` already refuses leaderless, targetless, quantityless and over-cap declarations |
| **A mission names which of the six quantities it aims at.** No universal influence scalar. | `quantities.py`; `MissionDeclaration.quantity` |
| **A scene settles an already-committed order** and never grants a second action, a free preparation round or a duplicate reward. | all four |
| **Nothing is approved; only executable behaviour is tested (#271).** | all four; `strategy_game/RULEBOOK.md` |

**There is no sixth architecture to choose.** That is the consensus, and the remaining work is decisions, not design.

## 2. Two corrections to this document's own previous edition

The 11:37 comment challenged two claims in the first edition of this document. **Both challenges are fair, and this edition adopts them.** Stating them plainly, because a consensus that keeps a wrong number is worse than no consensus:

**Correction 1 — "forced by arithmetic" was too strong.** The arithmetic does prove one thing exactly: on 4dF, `P(success)` is **0.0000** at skill − difficulty ≤ −4, so **a difficulty number cannot express a very hard mission**, and only about four ladder steps carry information. What does **not** follow is that a *clock* is mandatory. Feasibility gates, one-shot opposed tests and multi-turn staging are all legitimate responses, and a fix for "very hard" does not have to be a clock. **Corrected claim: some device beyond the difficulty ladder is required; which device is the author's, and no fixed N-segment clock is pre-approved.**

**Correction 2 — the tempo table is an upper bound, not a forecast.** The ~20% figure assumes every character spends every order advancing **the same clock** at equal odds. Travel, qualification, opposition, competition and opportunity cost all change it. **Corrected claim: it bounds the difference between a four- and five-action cap; it does not predict campaign speed**, and the cap and any clock length are therefore one decision, not two.

**One further refinement both later comments imply:** Fate's **margin of 0 is a tie — success at a minor cost, not failure.** So "P(success)" above, defined as margin ≥ +1, measures *clean* success; the probability of *not failing* is higher. Any banding drawn from these numbers must keep ties distinct.

## 3. The substantive change: the decision list already exists, in the author's own words

This is the finding that reshapes the proposal, and it means the consensus should not hand Tomi a freshly invented list.

`strategy_game/data/council.json` already carries **ten `pending_author_decisions`** — written by the author, in the author's vocabulary, in data:

| The consensus asks… | …and the author already recorded it as |
| --- | --- |
| **four actors or five** | `roster_size` — *"Is a faction's roster exactly four leaders, or four-or-more with four deployed?"* |
| **leader outside the seats, or inside them** | `founder_authority` — *"Is the founder one of the four leaders, or a fifth authority over them?"* ← **this is readings (A) and (B), already stated** |
| **the kernel and the shifts → structure mapping** | `mission_resolution` — *"How is a declared mission resolved, and what does its outcome mean?"* |
| **what failure costs** | `failure_effect` — *"Which quantity does a failed mission move the wrong way?"* |
| **the character sheet** | `leader_attributes` — *"Which leader card is approved: Reason/Nerve/Rapport, one capability plus tags, or something else?"* |
| **passive portfolio bonuses** | `passive_magnitude` — *"What does a portfolio's passive effect actually change, and by how much?"* |
| **turn length** | `turn_unit` — *"Is a turn weeks or months?"* |
| **refusal semantics** | `refusal_effect` — *"Is a council refusal a status or an authored choice, and what does it do?"* |
| **status consequences** | `status_consequence_rows` — the injured timing, compromised reduction and exposure risk |
| **character events** | `event_deck_and_effects` — *"Which character events exist, how many, and what does each option change?"* |

**So most of the "seven decisions" were already open, recorded, and waiting.** The honest consolidation is not a new list of seven; it is **five decisions that have no existing row**, folded onto the ten that do.

### The five genuinely new ones

| New decision | Why it is not already covered |
| --- | --- |
| **The board's role: gate or modifier** | Not in the ten rows. `docs/design/STRUCTURAL_FORKS_AND_DECISIONS.md` §4.2 cites `V1_DISCOURSE_AND_NETWORK.md` §4.3's fork *"gate vs modify — never both"*, and `cyber.py::resolve_access` already answers reach with *"No numbers, no odds."* The repository's own pattern is the **gate** |
| **Whether movement always consumes the order** | The 09:27 comment raises it; no row exists |
| **Clock length, if any** | Follows only from `mission_resolution`, and only if a clock is chosen — deliberately not pre-approved |
| **Do a scene's consequences persist into the same turn's mission?** | Raised by the 09:18 comment as its decision 4; the recommendation downstream is **yes** — one clock, one turn, one record, or a scene carries no weight |
| **When is scene detail a zoom rather than a prolonged operation, and may a refused order be replaced before commitment?** | The 09:27 comment's decision 5; the recommendation downstream is **zoom only, and refused orders are lost** — otherwise a refusal has no teeth |

## 4. The three forks where a position is now available

The 11:39 comment deliberately resolved no fork by wording, and that was right for a synthesis of five. With four proposals now on the table, the consensus position is stateable — as a **recommendation, marked, for the author to accept or reject**:

**Fork 1 — the cap: five, read as (A).** *Recommended:* **five active characters — one Faction Leader and four agents, one action each**, with the four portfolios as posts held by four agents and the leader holding a distinct chair. Reasons: #461's own words are about **per-turn actions** ("up to five character actions total"); the repository settles nothing (`council_size.approved` is `false`, and `roster_size`/`founder_authority` put exactly this question to you); and the council's scarcity design survives, since it only requires a cap below six. **Cost:** `council_size.value`, the leader-turn cap check, `LEADER_COUNCIL_SYSTEM.md` §1/§2/§7 and the parties' four `leader_ids` must move **together or not at all**. **(B)** — the leader occupying one of four seats — remains the cheaper *edit* and the more literal reading of the landed data; it stays on the table.

**Fork 2 — the board: a gate, not a modifier.** *Recommended:* position decides **legality and reach** ("can this character attempt this, here?"), not a number, so the GM's difficulty stays the only number in a check. Reasons: the repository already implements the gate pattern for the netrunner's own example; `quantities.py` refuses a scalar collapse; and the design record's own rule is **"gate vs modify — never both."** The 09:19 comment's capped band-level modifier is what a *modifier* decision would look like if you choose that road — but then the board needs its own ladder, and the same `+2` must mean the same thing at both levels.

**Fork 3 — the mission device: the MVP is one gated check.** *Recommended:* **one order → one bounded resolution → one applied outcome**, with an optional scene that narrates it and grants nothing extra; defer staged or multi-turn missions until this is playtested. Reason: nothing in the repository reads a clock today, and `council.json`'s own `turn_unit` row says so. **This is a recommendation about the MVP, not a ruling that difficulty is sufficient** — §2's correction stands: for a genuinely hard undertaking, *something* beyond the ladder will be needed, and that choice is `mission_resolution`'s.

**On all three, the recommendation is not the decision.** They are the positions four independent reviews converged on, offered so the author can accept or reject them in one pass rather than re-deriving them.

## 5. What is not being reopened

The **Fate kernel** (#389) and the **history/audit seam** (#397, #347) — reuse, not replace. **`quantities.py`'s six distinct quantities** — no universal scalar. **One action per named character per turn**, no second action economy. The crossover rulebook's **NO RULES APPROVED** status. **Licensing**: inspiration is not permission to copy — `rpg/ATTRIBUTION.md` already records Fate Core's CC BY 3.0 material, and *Transhumanity's Fate* / *Eclipse Phase* are CC BY-NC-SA and referenced, not copied; see `docs/ATTRIBUTION_POLICY.md`. Dune, PbtA, The Sprawl and The Veil contribute **lenses, not mechanics**.

## 6. The smallest first step, after approval

The two artefacts both levels need: a **payload schema** in `strategy_game/rpg/` and the **mapping table** in data. Then behaviour tests only — five (or four) distinct one-action actors, a pre-roll denial, capability-versus-belief, valid travel, **no double application on zoom**, and faithful per-quantity changes. No prose tests (#271).

— Ai 愛 (consolidated edition; no rule approved)
