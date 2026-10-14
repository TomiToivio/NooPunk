# #461 consensus proposal — one kernel, one sheet, two projections, and the decisions that remain

**Status: PROPOSAL. No rule, number, action list, dice procedure or capability is approved by this document.** `strategy_game/RULEBOOK.md` still reads **NO RULES APPROVED**; nothing here is written into it and no code changes. Tomi decides; this document's job is to make the deciding cheap by collapsing five comments into one proposal and one short decision list.

**What this is.** A synthesis of the five design comments on #461, with their load-bearing claims **re-verified against `main`** rather than taken on trust, their agreements stated once, and their one real conflict put to the author with both readings costed.

---

## 1. Consensus: what all the comments agree on

The five comments differ in emphasis, not in architecture. Where they converge, and where I verified the claim:

| Agreed | Verified how |
| --- | --- |
| **The resolution kernel is already approved and is not re-chosen.** #389 approved Fate Core: `4dF + skill (+invokes) − opposition = shifts`, four intents, aspects, stress, consequences 2/4/6. The design task is the *crossover seam*, not a new engine. | `strategy_game/RULEBOOK.md` opens with the #389 approval; `rpg/RULEBOOK.md` is the playtest manual |
| **The seam already exists; it does not need to be built.** `strategy_game/turn.py` resolves a character check through the approved Fate engine and writes it into the one append-only `HistoryLog`; only the strategic write path is missing. | `turn.py` really defines `StrategicActionPending`, `record_declaration`, `record_character_check`, `turn_outcomes`, `dice_log`, `verify_outcome`, `verify_history`, `StrategicActionPort`, `strategic_action`, and carries `OUTCOME_KIND = "rule_outcome"`, `ENGINE = "strategy_game.rpg.fate"` and `LeaderRpgLayer` |
| **One sheet, two projections.** `rpg/RULEBOOK.md` §2's card is the single character record; the strategic layer's per-leader data is a projection of it, not a second sheet. The council leader and the card must resolve to **one identity by a shared id**. | consistent across all five comments; `rpg/RULEBOOK.md` §7 already states the handoff as a read-only payload |
| **Eligibility is a typed field, never read off a name.** A player must not get a capability by typing "netrunner" into a high concept. | `rpg/RULEBOOK.md` §2/§4: stunts "require GM approval", and "an aspect's name is not itself an equipment entitlement, access credential, psi power or stunt" |
| **The capability vocabulary is already landed, not to be invented.** | `faction_creation.json` (#346) carries the competence family **`TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`**; `character_cards.json` (#356) carries `archetype_netrunner` with a **`competence`-kind tag** beside an equipment tag |
| **One entry per competence.** A competence contributes once, in exactly one role: agent skill, scene capability, or a capped passive portfolio bonus. Faction assets add **reach and capacity**, never a substitute skill. | arithmetic in §2 — a duplicated `+2` takes a roll from 61.7% to 93.8% |
| **The strategic projection is a declaration, not arithmetic.** A mission names which of **the six quantities** it aims at; nothing computes `influence + 1`. | `quantities.py` holds the one `QUANTITIES` tuple and refuses to collapse it; `council.py` already refuses a declaration that names no quantity |

**Consequence: there is no competing architecture to choose between.** The comments propose one design with different amounts of detail.

## 2. What the arithmetic settles — recomputed here, independently

I recalculated the 4dF distribution from scratch (81 outcomes) rather than quoting it. Margins `−4…+4` have counts `1, 4, 10, 16, 19, 16, 10, 4, 1`.

**P(success), margin ≥ +1, against skill − difficulty:**

| skill − diff | −5 | −4 | −3 | −2 | −1 | 0 | +1 | +2 | +3 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P(success) | **0.0000** | **0.0000** | .0123 | .0617 | .1852 | **.3827** | **.6173** | .8148 | .9383 |

Three findings follow, and they are **constraints rather than opinions**:

1. **A "very hard mission" has no difficulty number that expresses it.** At skill − difficulty ≤ **−4** the probability is **exactly zero, not small** — the die cannot roll below −4. The mission level therefore **requires** a second device (a clock, a staged objective, or a named opposition rating). That choice is **forced by the arithmetic, not by taste.**
2. **A difficulty ladder alone carries about four distinctions and does not extend** — the odds stay informative only from −1 to +2, and only 0 and +1 leave the outcome genuinely in doubt.
3. **"Success with style" cannot carry mission character.** At even odds it is **6.2%** (5/81) — a tail event. The clock or staged objective has to do that work.

**And the reason the one-entry rule is a rule and not a convention:** a duplicated competence taking a roll from **61.7% → 93.8%** means one invoke on top makes it **certain**. On a centred kernel, board-derived modifiers must be **band-level (±2)**; anything larger must be an **eligibility gate**, or the board swamps the dice.

## 3. The one real conflict: five actors or four

This is the only place the comments genuinely diverge, and it is **real and open**:

- **#461 says five** — one leader + four principal agents, one action each = five actions per turn.
- **The landed structure says four** — `council.json` records `council_size = {"value": 4, "approved": false}`; `LEADER_COUNCIL_SYSTEM.md` §1/§2/§7 say four; `ukweli_local.json` gives **every one of the three parties exactly 4 `leader_ids`**; the string "five" **does not occur in `council.json` at all**.

**Both readings work, which is why this is cheap to settle:**

- **(A) The main PC is a fifth character outside the four portfolio seats.** Matches #461's wording most literally; the leader gets a personal stake distinct from the council's four arguments. **Changes:** `council_size.value`, the four-move cap, `LEADER_COUNCIL_SYSTEM.md` §1/§2/§7, and the 4-id parties in `ukweli_local.json`.
- **(B) The main PC occupies one of the four seats.** Five *characters* exist, the **faction still acts four times**; the leader is not a free extra slot. Reads #461's "five" as a roster statement. **Changes:** nothing in the landed data.

**Why it is cheap:** the council's own scarcity design (`scarcity_makes_the_council_an_argument`) only requires the cap to be **smaller than six quantities**. Four and five are both below six, so both preserve the design's logic.

**Why it is not free:** it changes scarcity *degree* (rival-AI parity, the §8 worked example, any balance pass) **and tempo** — a faction commits its whole cap each turn, so a five-action cap completes every mission roughly **20% faster**, and the largest clock still finishing inside two turns moves from **4 segments to 6**.

**Whichever is chosen, `council_size.value` and the four-move cap must change together in one deliberate edit**, or `council.py::structural_problems` will keep refusing legal orders.

## 4. The consensus recommendation (proposal, not canon)

1. **One kernel, two projections** — the approved Fate check at both levels. No second, coarser strategic die and no conversion table.
2. **One sheet**, with a test that refuses a council leader with no corresponding card — otherwise "one sheet" is only a claim.
3. **The four axes that differ** between projections: **time** (inside a turn vs the turn), **stakes** (what is true of a scene vs which quantity is aimed at), **opposition** (GM difficulty or NPC defence vs a rival leader's defence or scenario difficulty), and **consequence routing** — a scene lands on the **character** (stress, 2/4/6), a mission on the **faction** (asset, position, reputation). Nothing else differs.
4. **MVP = the minimal one-check mission**: one gated Fate check per order, optionally narrated as a scene, producing one bounded strategic outcome. Defer multi-scene missions until this is playtested.
5. **Scene zoom settles one already-committed order** — several checks may illustrate it, but a scene **never** grants an extra order and **never** applies a strategic effect twice.
6. **Movement consumes the order**, unless the author later rules otherwise.
7. **Assets are reach, not actors**: a lab, an informant network or a base makes an action possible or changes its stakes; the character still commits the action.
8. **One small addition to the read-only payload**: the mission clock's current state **as a read**. It lets a scene narrate "two-thirds of the way in" without giving the RPG layer authority to advance anything.

## 5. The decisions that remain — all of them Tomi's

| # | Decision | Options | What it changes |
| --- | --- | --- | --- |
| **1** | **The cap: five actors or four** | **(A)** leader is a fifth actor outside the seats · **(B)** leader occupies one of four seats, faction acts four times | `council.json`, `LEADER_COUNCIL_SYSTEM.md` §1/§2/§7, the 4-id parties, rival-AI parity, and mission tempo by ~20% |
| **2** | **The mission's second device** | clock · staged objective · named-opposition rating | Required by §2 — the difficulty ladder provably cannot express a very hard mission |
| **3** | **The clock length**, if a clock is chosen | 2 / 3 / 4 / 6 segments | Chosen **with** #1, not after: the cap and the clock length set mission pacing together |
| **4** | **The kernel** | keep the approved 4dF (#389) · change it explicitly | Keeping it simplifies the *presentation*, not the tested kernel. Changing it invalidates the §2 tables |
| **5** | **Movement** | always consumes the order · a separate convention | Whether position is a real cost or free repositioning |
| **6** | **The skill list and action menu** | the illustrative menus in the comments | The only place a new vocabulary would be authored; the competence families already exist |
| **7** | **The shifts → structure mapping** | the one open rule both proposals name | Whether "success with style" is worth more than "success" on a faction mission, and what failure costs |

**These seven are the whole remaining decision surface.** Nothing else in the comments is in dispute.

## 6. What is not being reopened

- The **Fate kernel** (#389) and the **history/audit seam** (#397, #347) — reuse, do not replace.
- **`quantities.py`'s six distinct quantities** — no universal power or influence scalar.
- **One action per named character per turn**, with no extra action economy.
- The **NO RULES APPROVED** status of the crossover rulebook.
- **Licensing**: design inspiration is not permission to copy text; see `docs/ATTRIBUTION_POLICY.md`.

## 7. After approval — the smallest first step

The two artefacts the two levels cannot share without: a **payload schema** in `strategy_game/rpg/` and the **mapping table** in data. Both are small. Then behaviour tests for **exactly five (or four) one-action actors, a denied special action, movement cost, no double application on scene zoom, and faithful per-quantity changes** — executable behaviour only, never prose (#271).

— Ai 愛 (consensus synthesis; no rule approved)
