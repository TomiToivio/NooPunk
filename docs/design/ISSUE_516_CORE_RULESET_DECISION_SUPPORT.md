# Issue #516 — core ruleset: decision support, not a ruling

**Status: PROPOSAL. NOTHING HERE IS CANONICAL, AND NOTHING HERE IS APPROVED.** Issue #516 is a
**human-led design decision**. Its own constraint is the one that governs this file: *"AI may provide
comparisons, prototypes and critique, but must not autonomously choose or declare the final rules
canonical."* Every recommendation below is therefore written as a **recommendation with its
trade-off**, every number is an **example**, and every point where only Tomi can decide is carried
as a row in [`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md) (rows **D29–D37**).

**The ruleset described in this file is not canonical and awaits Tomi's explicit sign-off.** Its
"Done when" is his: *"Tomi has documented a single cohesive ruleset, demonstrated it in both narrative
and tactical examples, tested its playability and explicitly signed off on the design."* This record
can make that decision possible and well-informed. It cannot make it.

**What this file is.** The comparison, the option analysis and the worked illustrations that #516
asks for, written against the repository as it stands: which mechanics to take from which system and
why, the seven computer games mapped to mechanisms, the unified-resolution choice with its
trade-offs, the smallest character model with a measured skill-bloat analysis, tactical-combat
options, PSI/cyber/astral options, the cross-layer propagation design, and five worked examples.
It also measures what its seven predecessors already settled, so that nothing here silently replaces
their work.

**What this file is not.**

- **Not a rulebook.** It does not touch [`strategy_game/RULEBOOK.md`](../../strategy_game/RULEBOOK.md)
  or the legacy [`RULEBOOK.md`](../../RULEBOOK.md). Neither file is edited by this PR, and the legacy
  rulebook is never rewritten by an agent.
- **Not a licence decision.** Eclipse Phase 2e and Transhumanity's Fate are **CC BY-NC-SA**: they are
  *design references*, and no prose, table, number or setting element of theirs is reproduced here.
  The Fate Core material (CC BY 3.0) is the implemented chassis, and its licence boundary is stated in
  [`strategy_game/rpg/ATTRIBUTION.md`](../../strategy_game/rpg/ATTRIBUTION.md). The distribution
  licence itself stays row **D10**.
- **Not a playtest.** #516 asks for one; this file supplies the material a playtest would use and
  says plainly that the playtest has not happened.
- **Not tested, and not testable by design.** Per `AGENTS.md`'s automated-tests policy, documentation,
  rules and canon are reviewed editorially and by tabletop playtesting; no test in this PR asserts a
  word of it, and none was added.

---

## 0. Scope, measured first

### 0.1 Which game these rules are for

The repository holds **two games** (`AGENTS.md` §0), and #516's wording ("the existing
FIT/REF/INT/SOC/PSY/CYB") names the **legacy** game's attributes while most of the mechanics it cites
are the **crossover** game's. Measured on `origin/main`:

| | Legacy NoöPunk RPG | Crossover game |
| --- | --- | --- |
| Rulebook | `RULEBOOK.md` (6,244 lines) + `rulebook/` | `strategy_game/RULEBOOK.md` (214 lines) |
| Resolution | **STAT + Skill + 1d10** vs a difficulty value | **4dF + skill** vs opposition, four outcomes |
| Rated traits | **6 STATs** at 1–10 **and** 40 skills | **6 individual skills** (COG, INT, REF, SAV, SOM, WIL) |
| Approval status | living canonical rulebook, author-owned | Fate foundation approved (#389), six individual skills approved (#482), strategic roster **not** approved |
| This record's relation | **reads it, changes nothing** | the layer this record is about |

**Everything below is scoped to the crossover game**, because that is the game whose rules are still
open and whose kernel the repository treats as approved. Whether #516 is also meant to re-open the
legacy game's `1d10` kernel — which would be a rewrite of a canonical file — is **not a question this
record may answer**, and is queue row **D29**.

### 0.2 The measured baseline (so the comparisons are not abstract)

| Quantity | Value on `origin/main` | Where |
| --- | ---: | --- |
| Legacy STATs | 6 | `RULEBOOK.md` §9.2 |
| Legacy skills (`status: canonical`, #159) | **40** | `data/rules/skills.json` |
| … of which `INT` | 11 | same file, counted |
| … of which `PSY` | 8 | same |
| … of which `SOC` | 7 | same |
| … of which `FIT` / `REF` / `CYB` | 4 / 4 / 4 | same |
| … of which `Variable` | 2 | same |
| Fate Core default skill list | 18 (10 rated by the Great pyramid) | `strategy_game/RULEBOOK.md` §3.1, verified against the SRD |
| Transhumanity's Fate named skills | 24 | `data/strategic_skills.json::transhumanitys_fate_mapping` |
| Crossover individual skills (approved) | **6** | `strategy_game/rpg/skills.py::INDIVIDUAL_SKILLS` |
| Crossover strategic skills (proposed, not approved) | **7** | `data/strategic_skills.json`, queue **D22** |
| Fate structures available for zoom | 4 (overcome, create an advantage, contest, conflict) + challenge | Fate Core SRD; recorded in `ISSUE_461_CONSENSUS_PROPOSAL.md` §5 |
| Existing capability tags | `TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`, `archetype_netrunner` | `faction_creation.json`, `character_cards.json` |

**The abbreviation collision, stated once because it will bite every reader.** `INT` means
*Intelligence* in the legacy game (a 1–10 STAT) and *Intuition* in the crossover (a Fate-rated skill).
`REF` is *Reflexes* in both but on a different scale. `PSY` (legacy Psyche) has no crossover
counterpart by that name; its ground is split across `WIL` (contest of will) and `INT` (perception).
Any document that says "INT" without naming the game is ambiguous, and this one names the game.

---

## 1. Predecessors: what each already settled, and what this record does not reopen

Issue #516 says to coordinate rather than silently replace. Measured against the issue bodies, the
landed design records and the decision queue:

| Issue | What it already settled | What this record does **not** reopen | Where this record differs, explicitly |
| --- | --- | --- | --- |
| **#461** (design with Tomi) | Five seats — one faction leader + four agents; **at most one action per character per turn**; generic vs capability-gated special actions; leader is the PC from day one; board position is a **gate, not a modifier**; refusal at declaration, and a refused order is **lost, not substituted**; a scene settles a committed order and grants nothing | The five-seat structure, the one-action limit, the gate-vs-modifier rule, refusal semantics, the leader premise | Nothing structural. §9 adds *where* the tactical layer's extra reactions sit **inside** the one-action limit — that is a proposal, not a change to #461 |
| **#255** (compare Fate-first systems) | Fate Core / Transhumanity's Fate as the starting chassis; **six independently rated attributes mandatory *for the legacy game***; attributes distinct from skills; preserve the 40-skill list; GNS as a heuristic; `COMPARISON.md` as the historical comparison | The comparison itself; the licensing conclusions; the finding that no numeric kernel was approved by that gate | §4 proposes that the **crossover** needs *no second numeric layer* (its six Fate skills are the rated traits). That is a **proposal that would leave #255's six-attribute requirement standing for the legacy game only**, and it is D30, not a revision of #255 |
| **#200** (Fate-first conversions) | The Fate-first parent epic; the licensing premise (fully CC, no OGL expression); the `COMPARISON.md` gate as a precondition; twenty child work packages, several merged | The licensing premise; the child-issue map; the historical Fudge-centred proposal, which is superseded and is **not** revived here | Nothing. §4 borrows Fate's own structures and cites where this repository already recorded them (#217's outcome semantics, #219's band arithmetic, #225's single-locus rule) rather than restating them |
| **#280** (stats/tags) | One unified **TAG schema** with four types (active, passive, competence, negative/condition); a STAT-tree alternative to a skill list; the Empathy/Willpower split proposal; the point that a permission-TAG is not a modifier-TAG | The TAG schema as *vocabulary* — it is already what the engine reads (`TAG_KINDS`); the Empathy/Will split is **not** reopened | §6 **uses** the tag schema but does **not** adopt the stat tree: #280 replaces skills with stats, and the crossover has approved skills (#482). §6's recommendation is tags *beside* six skills. Marked as a difference, with the stat-tree option kept alive as D30 option C |
| **#262** (narrative-first core) | Narrative-first priority; Physical/Cyber/Astral as one world's three interacting levels; no single failed roll blocks an essential clue; text-first, minimal graphics; tactical grids deferred; original rules rather than direct adoption; FIT/REF/INT/SOC/PSY/CYB retained **"as an author preference unless explicitly changed"** | The narrative-first priority; the three-realities model; the no-bottleneck rule; the deferral of grids; the "original rules, not adoption" method | §5's unified mechanic is deliberately **original in expression, Fate-shaped in arithmetic**, and §4 marks exactly which Fate structures are borrowed. #262's "tactical deferred" is honoured: §7 makes the tactical layer optional and adds nothing to v1's requirements |
| **#502** (RPG-first roadmap) | Phase 1 RPG → Phase 2 X-COM scale → Phase 3 Terra Invicta scale; the leader-from-day-one premise; one world model, three views; `Case` and `MissionOutcome` as the only genuinely new records; `MissionOutcome.effects` deliberately left open | The phase order; the leader premise; the interface audit; the refusal to unify the two `WorldState` classes | §9 fills in **what may travel** along `MissionOutcome.effects` as a *proposal* and names the write path. It does not choose an effect vocabulary — that stays #502's open item and becomes D35 |
| **#515** (future retro tactical map) | A four-character squad on one reusable tile map; investigation, dialogue, clues, hacking, PSI, stealth and combat on the **same** map; 8-bit presentation; reuse the existing stats/tags/actions/wounds; outcomes feed faction strategy; not a second ruleset | The four-squad scope; the one-map-for-all-missions requirement; the pixel-art direction; "reuse, do not invent a second ruleset" | §7 supplies the **action economy and cover/positioning vocabulary** #515's milestone 4 needs but does not itself define, as three options. It invents no map tech and no renderer (that is D13) |

**One correction to the record, offered rather than made.** `AGENTS.md` §0 and several design
documents still describe `strategy_game/RULEBOOK.md` as saying **NO RULES APPROVED**. As of `00a39b6`
it does not: its header records the #389 foundation and #482's six skills as **approved**, and reserves
the strategy, political and numeric layers as unapproved. The documents that quote the older status
are stale in that one clause. This record does not edit them — the correction belongs to whoever owns
that sentence next — but no reader should take the stale quote as the current state.

---

## 2. The comparison: what to borrow, adapt and reject, and why

Three families, one row per *mechanic* rather than per game, because #516 asks for mechanics and
reasons, not for verdicts on books. **BORROW** = take it as it is. **ADAPT** = take the idea, change
its shape for NoöPunk. **REJECT** = leave it out, with the reason stated so it is not re-proposed
every quarter.

### 2.1 Fate Core (CC BY 3.0 — the implemented chassis, #389)

| # | Mechanic | Status | Why |
| --- | --- | --- | --- |
| F1 | **4dF + skill → shifts** | **BORROW** | Zero-centred, four informative steps, no whiff floor; already the approved kernel and already seeded and replayable in `rpg/fate.py` |
| F2 | **Four actions** (overcome, create an advantage, attack, defend) | **BORROW** | One verb set covers social, investigative, physical, cyber and PSI without a fifth subsystem |
| F3 | **Four outcomes** (fail, tie, succeed, succeed with style) | **ADAPT** | Keep the four, but state explicitly what a tie means per action — Fate leaves the tie's "minor cost" to the GM, and #516 asks for consequences to be *defined*; §5.4 is the proposal |
| F4 | **Aspects as fictional permissions** | **ADAPT** | Cap them: high concept, trouble, three more. Aspects are cheap to write and expensive to adjudicate; five is the number a GM can hold |
| F5 | **Fate points**: invoke for +2 or a reroll, compel for a complication, refresh | **BORROW** | It is the **only** metacurrency the crossover has, and keeping it single is what stops a second economy (EP's pools) from creeping in |
| F6 | **Stress tracks + consequences** (2 boxes each; mild 2 / moderate 4 / severe 6) | **BORROW** | Absorbs harm without a hit-point engine, and a consequence is already a *named fact* — which is what the strategic layer needs (§9) |
| F7 | **Stunts as named exceptions, priced in refresh** | **BORROW** | This is the price mechanism that makes a capability cost something; #461's decision 7 in the consensus record reaches the same place |
| F8 | **The 18-skill default list** | **REJECT** | 18 names for a six-skill layer is bloat by definition; the crosswalk in `RULEBOOK.md` §3.1 already folds them into six |
| F9 | **Great pyramid / skill columns** | **REJECT** | The pyramid rates ten skills; it cannot be applied to six, and both readings are rulings. Carried as **D23**, not decided here |
| F10 | **Challenge / contest / conflict as zoom** | **BORROW** | This is the answer to "how hard is a very hard thing" without inventing a device: several rolls, opposed rolls, or mutual harm, chosen by the situation (§5.3) |
| F11 | **Free invocations from create an advantage** | **BORROW** | Makes preparation matter and gives noncombat actions a combat-shaped payoff |
| F12 | **The fractal (bronze rule): factions on the same sheet** | **REJECT** | A faction with stress and consequences would double the economy and grant the strategy layer numbers by the back door; `quantities.py` has six named quantities for that, and they are not stress |

### 2.2 Transhumanity's Fate (CC BY-NC-SA — design study only, no expression imported)

| # | Mechanic | Status | Why |
| --- | --- | --- | --- |
| T1 | **Minimalist conversion method** ("avoid new concepts; build off existing ones") | **ADAPT** | Take the *method*, not the text: every NoöPunk addition must justify itself against an existing Fate structure first |
| T2 | **25 starting skill points under a Great (+4) cap** | **REJECT** | A budget written for a 24-skill list; applying it to six — literally or scaled — is a ruling. Recorded as a *fact about the source* in `RULEBOOK.md` §3 and carried as **D23** |
| T3 | **Bodies as simple containers** (gear and augmentation as stunts or sub-aspects) | **ADAPT** | No resleeving economy. A body is a permission plus aspects; a changed chassis is a scene with a consequence, not a routine |
| T4 | **Hacking as a contest** | **ADAPT** | Becomes the Cyber layer's default shape (§8). It is the cheapest way to make intrusion dramatic without a minigame |
| T5 | **Contacts/Resources folded into reputation skills** | **REJECT** | The crossover folds access into `SAV`; a separate reputation rating would be a seventh trait by another name |
| T6 | **Morph/ego separation** | **REJECT** | Setting import. NoöPunk's humans are mostly in original bodies; the setting boundary is stated in `strategy_game/RULEBOOK.md` §1 |
| T7 | **Its 24-name skill list** | **REJECT** | Verified as almost entirely *scene-shaped*, so it consolidates into the six; adopting it would re-import the bloat the six exist to remove |

### 2.3 PbtA — Apocalypse World, The Veil, The Sprawl (lenses, per #262)

| # | Mechanic | Status | Why |
| --- | --- | --- | --- |
| P1 | **"To do it, do it"** — the fiction must contain the action before dice are touched | **BORROW** | It is the cheapest possible statement of the 50% narrativist priority, and it costs no rules text |
| P2 | **2d6 + stat, bands 6− / 7–9 / 10+** | **REJECT** | A second randomiser. The kernel is 4dF (#389) and the probabilities are tuned for it; two dice conventions at one table is the exact "two engines" #516 forbids |
| P3 | **7–9: success with a cost** | **ADAPT** | Kept as an *outcome the GM can always offer*, not as a fifth band on the ladder — see **D32**. Fate's tie already does this for overcome; the PbtA contribution is making it the *normal* shape of a partial result |
| P4 | **Playbooks with fixed move lists** | **REJECT** | 24 skills plus playbook moves is the bloat #516 names. A capability tag plus a stunt already does what a move's trigger does |
| P5 | **Clocks (segmented progress)** | **ADAPT** | Used only where a single roll cannot express the hardness (#461 Fork 4); a clock is a *structure*, not a stat, and its length is D27's business in the project engine |
| P6 | **MC principles** ("be a fan", "ask questions, use the answers", "make a move that follows") | **BORROW** | Guidance, not mechanics — which is exactly the right weight for the narrator role #516 asks to define |
| P7 | **Strings / Hold / Debts** | **REJECT** | A second metacurrency beside Fate points. The relationship graph already carries leverage as fiction |
| P8 | **Harm clocks** | **REJECT** | Fate stress and consequences already do this; two harm models is one too many |
| P9 | **"Fail forward" as an obligation on the narrator** | **BORROW** | Failure must change the situation; this is also the anti-bottleneck rule #262 requires for investigation |

### 2.4 Cities Without Number, with Stars and Worlds Without Number as references (gamism)

| # | Mechanic | Status | Why |
| --- | --- | --- | --- |
| C1 | **d20 + skill + attribute vs target** | **REJECT** | A third randomiser, and a linear one; the kernel is 4dF |
| C2 | **Background / edge / foci** | **ADAPT** | One **background** as a free aspect at creation, one **competence** tag from it. No foci list: a focus is a stunt by another name, and the stunt already has a price |
| C3 | **Shock damage** (guaranteed harm on a miss) | **REJECT** | A second damage model beside stress; the desired effect (cover still costs something) is available as a consequence or a boost |
| C4 | **System Strain as a cyberware capacity** | **REJECT** | A new capacity resource. Cyberware is a permission plus a tag; if a limit is wanted it should be a *slot count* or a consequence, and neither is approved. Offered as an option in §8.4 only |
| C5 | **The faction turn (SWN)** | **ADAPT** | The *shape* — a small number of named assets, one action each, a turn — is already #461's five seats. No faction stat exists and none is proposed |
| C6 | **One-line NPC statlines / tags** | **BORROW** | The cheapest GM tool in the family: an NPC is a name, one rating, one tag. It also solves #516's NPC-representation deliverable (§6.6) |
| C7 | **Saves (physical / evasion / mental)** | **REJECT** | Redundant: `SOM`, `REF` and `WIL` defend, and a save is a second resolution path to the same outcome |
| C8 | **Levels and XP** | **REJECT** | Fate milestones are the approved baseline; levels reintroduce class assumptions #262 refuses |
| C9 | **Gear catalogues with prices and encumbrance** | **REJECT** | Equipment statistics are unapproved (`RULEBOOK.md` §9) and a catalogue is the fastest route to simulationist bloat. Gear is a permission with one tag |
| C10 | **Morale checks for NPCs** | **BORROW** | Ends fights without a wipe and makes "fast, dangerous" survivable; one `WIL` check for the opposition, GM-side |
| C11 | **"A failed roll is a complication, not a stop"** (WWN) | **ADAPT** | Same idea as P9, arriving from the gamist side; folded into the same narrator rule rather than stated twice |

### 2.5 Eclipse Phase 2e (CC BY-NC-SA — reference only)

| # | Mechanic | Status | Why |
| --- | --- | --- | --- |
| E1 | **Six aptitudes** (Cognition, Intuition, Reflexes, Savvy, Somatics, Willpower) | **ADAPT** | Already adapted: used as the six Fate-rated skills (#482). The scale is Fate's, not the percentile band |
| E2 | **Percentile roll-under with margin of success** | **REJECT** | Refused explicitly in `RULEBOOK.md` §9; a percentile kernel beside 4dF is the second engine #516 forbids |
| E3 | **Four pools** (Insight / Moxie / Flex / Threat) | **REJECT** | Collides with Fate points; #461's consensus record already recommends one metacurrency |
| E4 | **Wound thresholds and trauma** | **ADAPT** | Becomes the *persistence* rule: a consequence may outlive the scene as a named injury (§7.4). Thresholds themselves are not imported |
| E5 | **Mesh access: reachability before interface** | **ADAPT** | Becomes the Cyber layer's gate — you cannot hack what you cannot reach, and no roll grants reach |
| E6 | **Discrete PSI sleights** | **ADAPT** | Becomes gated capabilities: the sleight decides *whether*, one of the six skills decides *how well* |
| E7 | **PSI infection / async origin** | **REJECT** | NoöPunk PSI is natural and not virus-derived (`RULEBOOK.md` §1); importing the origin would import the setting |
| E8 | **Resleeving and the morph economy** | **REJECT** | Setting and body economy both; see T6 |
| E9 | **Reputation networks as ratings** | **REJECT** | A number per network is a second social system; relationships are already narrative facts in `relationships.py` |
| E10 | **Pool spend to ignore harm (Moxie)** | **REJECT** | Second metacurrency; a consequence that can be bought off is not a consequence |
| E11 | **Weapon and armour tables** | **REJECT** | Same reason as C9; and the numbers would be the author's to set anyway |
| E12 | **Single-locus embodiment: the body stays vulnerable while the mind is elsewhere** | **ADAPT** | Already the invariant of #225; kept as the Astral/Cyber layer's cost — projection is powerful *because* it leaves the body defenceless |

### 2.6 Counts

| Family | Borrow | Adapt | Reject | Total |
| --- | ---: | ---: | ---: | ---: |
| Fate Core | 7 | 2 | 3 | 12 |
| Transhumanity's Fate | 0 | 3 | 4 | 7 |
| PbtA | 3 | 2 | 4 | 9 |
| Cities / Stars / Worlds Without Number | 2 | 3 | 6 | 11 |
| Eclipse Phase 2e | 0 | 5 | 7 | 12 |
| **Total** | **12** | **15** | **24** | **51** |

**What the shape of that table says.** The borrow column is almost entirely Fate Core — which is the
point: the chassis is already approved and already implemented, so the narrativist 50% is bought
cheaply. The adapt column is where the other four families actually contribute, and the reject column
is dominated by *second economies* (pools, strings, strain, reputation ratings) and *second
randomisers* (d20, 2d6, d100). That is the single most useful finding in this comparison: **the
systems do not disagree about what makes a good scene, they disagree about how many currencies and
dice a table can hold, and NoöPunk's answer has to be one of each.**

---

## 3. The seven computer games: reference-to-mechanic matrix

Short by request: what to take, what to thin, what to leave, and which layer each one informs. "Layer"
uses #502's three views: **RPG** (Phase 1 scenes), **tactical** (Phase 2 / #515 squad missions),
**strategy** (Phase 2–3 faction play).

| Game | Layer informed | Adopt | Simplify | Avoid |
| --- | --- | --- | --- | --- |
| **Citizen Sleeper** | RPG | Clocks as the visible cost of time; conditions that change what you can attempt, not just how well; a cycle that ends whether or not you finished | Its five-dice-per-cycle allocation → **one** Fate point economy and **one** scene clock; its drives → aspects | Dice-as-resources as a second currency; the "you are running out of body" premise as a *mechanical* timer (it is a theme, not a rule) |
| **Disco Elysium** | RPG | Skills as *voices* in dialogue — a high `COG` argues with you; the white/red distinction (retryable vs one-shot) as a GM tool; failure that opens content instead of closing it | 24 skills → **6** with competence tags for the specific voice; the Thought Cabinet → one aspect that can change at a milestone | A second progression system; the enormous scripted dialogue trees; its morale/health double track (Fate's two tracks already cover it) |
| **X-COM** | tactical | Cover and flanking as the core tactical decision; **persistent injury** that removes an agent from the next mission; a four-agent squad as the unit of play; missions that can be lost and still matter | 2 AP → **one action + one reaction**; hit-chance percentages → 4dF shifts and a defend roll; squad loadout → gear as permission | A grid as a *requirement*; weapon stat tables; default permadeath; the strategy layer as a base-building game |
| **Cyber Knights: Flashpoint** | tactical | Security **escalation** as a clock (alarm rises whether or not you are seen); alternate solutions to one objective — stealth, social, intrusion; legwork before the mission that buys a free invoke | Its leverage/contact economy → aspects + one free invocation; its mission list → the seven proposed strategic kinds (D22) | A separate hacking minigame; its crafting and contact webs; its heat/faction-reputation numbers |
| **Shadowrun: Dragonfall** | tactical + RPG | A four-person team where each member has a **noncombat** role that the mission needs; one mission that legitimately mixes dialogue, intrusion and violence | Its AP + grid → the zone conflict (§7); its Matrix → the Cyber layer as a contest, not a turn structure | A separate Matrix initiative and turn order (the classic "everyone waits while the hacker plays"); gear catalogues; its karma/essence arithmetic |
| **Crusader Kings III** | strategy | Traits and **relationships** as the engine of politics; stress from acting against your own nature; secrets and hooks as leverage; characters who pursue their own agendas while you are busy | Three attributes plus lifestyle trees → the seven proposed strategic skills plus tags (D22); opinion arithmetic → named relationship facts | Dynastic succession simulation; event spam; a hidden opinion number the player cannot see or reason about |
| **Terra Invicta** | strategy | The councilor model: a small roster of named agents, **one mission each per turn**, capability-gated operations, consequences that take months | Eight attributes → seven strategic skills (D22); a large mission list → a short one grown by playtest | Control points, orgs, and the investment economy as *numbers*; real-time pacing; tying every mission to a percentage the player cannot influence |

**Two cross-cutting observations, since the matrix alone would hide them.**

1. **Three of the seven teach the same lesson about failure.** Citizen Sleeper, Disco Elysium and CK3
   all make a *bad* outcome produce content rather than a stop. That is the narrativist 50% arriving
   from the computer-game side, and it argues for P9/C11 being a hard narrator rule rather than a
   suggestion.
2. **None of the seven is a source of numbers.** Every one of them is cited for a *structure* —
   a clock, a gate, a role, a shape of turn. That is deliberate: a percentage imported from X-COM
   would be a number no NoöPunk playtest has earned.

---

## 4. The unified core resolution mechanic

### 4.1 What the issue actually asks for

One mechanic — rolls, difficulty, degrees of success, consequences, opposed rolls — that serves
**social, investigative, physical, cyber and PSI** actions. Not five subsystems that resemble each
other; one set of procedures whose *context* supplies the difference.

### 4.2 The constraint that narrows the field before any option is weighed

The 4dF kernel is **already approved** (#389) and **already implemented** (`rpg/fate.py`, seeded,
injectable randomness, four actions, four outcomes). Two of the four options below therefore carry a
cost that has nothing to do with game design: they would **re-open an approved decision** and make
every landed test and every landed document in `strategy_game/rpg/` either wrong or stale. That is not
a prohibition — Tomi may re-open anything — but it is a real cost and it belongs in the table.

### 4.3 Four options, with their trade-offs

| | **A. One kernel, four outcomes, three shapes** | **B. Dual kernel** (4dF for scenes, 2d6 bands for "moves") | **C. 4dF everywhere + a separate tactical engine** | **D. Replace the kernel** (2d6 or d10 for everything) |
| --- | --- | --- | --- | --- |
| **Roll** | 4dF + skill vs difficulty or opposition → shifts | two conventions at one table | 4dF for scenes; AP + its own roll for combat | one new randomiser |
| **Degrees** | fail / tie / success / style, with per-action meaning (§4.5) | 6− / 7–9 / 10+ for moves, four outcomes elsewhere | two outcome vocabularies | whichever is chosen |
| **Fit to 50/25/25** | 50 narrativist (aspects, costs, fiction-first); 25 gamist (which shape, which skill, when to spend); 25 simulationist (consequences persist) | stronger narrativist texture, weaker coherence | strong gamism, weak narrativism in combat | depends on the dice; a d10 gives a flat curve, 2d6 a bell |
| **Cognitive load** | one arithmetic, one currency, one outcome table | two | two, plus AP | one |
| **Re-opens #389?** | no | **yes**, partly | no (but adds an engine #516 forbids) | **yes**, fully |
| **Effect on landed work** | none | new band vocabulary beside the existing one | a second resolver beside `fate.py` | every test and `RULEBOOK.md` §5 becomes historical |
| **Verdict** | **RECOMMENDED** | reject | reject for v1, keep as the tactical *option* in §7 | reject |

**Recommendation: A — one kernel, four outcomes, three shapes, and the shape is chosen before the
dice.** The trade-off, stated plainly: **A buys coherence and cheap implementation at the cost of
granularity.** With four informative steps, a 4dF roll cannot distinguish "hard" from "very hard"
very well, so genuinely difficult undertakings must be expressed as *more than one roll* — a contest,
a conflict, or a challenge — rather than as a larger number. `ISSUE_461_CONSENSUS_PROPOSAL.md` §2
already proved the arithmetic of this and §5 Fork 4 already named the fix; this record agrees with it
rather than re-deriving it. The cost is real: **a GM who wants one roll to mean "very hard" will not
get it**, and the answer is "then it is a challenge, not a harder number".

### 4.4 Difficulty: one ladder, named, and stated before the roll

| Level (EXAMPLE — the ladder's names are Fate's; no NoöPunk number is approved) | Difficulty |
| --- | ---: |
| Trivial | +0 |
| Average | +1 |
| Fair | +2 |
| Good | +3 |
| Great | +4 |
| Superb | +5 |
| Fantastic | +6 |
| Epic | +7 |
| Legendary | +8 |

Two proposals sit on top of that ladder, both author decisions:

- **State the difficulty openly** (recommended) rather than hiding it. Fate's default is that the
  player declares and the GM sets a difficulty they need not reveal. Open difficulty is more
  accessible, makes the ladder learnable, and suits a text UI where the number can simply be shown.
  Hidden difficulty buys tension. **This is a real trade and it is in D31.**
- **Bounded situational modifiers**: at most one aspect invocation and one tag-based permission per
  roll, and no stacking of named bonuses. #217's prototype already caps situational steps at ±2; that
  cap is a *proposal* there and is inherited here as a proposal, not as a rule.

### 4.5 Degrees of success, per action — the part Fate leaves to the GM

The four outcomes are Fate's. What #516 asks for is what each *means* in each kind of action. The
table below is the **proposal**; every entry is a reading, not a rule.

| Outcome | Overcome (a problem) | Create an advantage | Contest | Conflict |
| --- | --- | --- | --- | --- |
| **Fail** (negative shifts) | No progress, **and** the situation worsens — the narrator makes a move that follows | No aspect; the attempt is visible and costs something | Opponent gains the round | Opponent's attack lands; you take stress |
| **Tie** (0) | **Succeed at a minor cost** — the thing is done; the cost is named (§4.6) | A **boost** only: one fragile, one-use aspect | No one scores; the situation shifts slightly | No harm; the exchange costs time or position |
| **Success** (+1, +2) | Done, cleanly | One scene aspect with one free invoke | You score the round | Attack lands for shifts as stress |
| **Style** (+3 or more) | Done, plus a **boost** | Aspect with **two** free invokes | You score **and** gain a boost | Attack lands, plus a boost |

**Why not a fifth band.** A "success at a cost" band between tie and success is attractive — it is
PbtA's 7–9 — but it makes *every* roll a three-way negotiation and it duplicates the tie. The
recommended reading keeps four bands and puts cost where it does the most work: on the tie. **The
counter-argument is honest**: at a table where most rolls are near the middle of the 4dF curve, ties
are common, so the tie rule carries a lot of weight, and a group that finds "succeed at a cost" the
most interesting result may prefer the five-band version. That is **D32**.

### 4.6 Consequences: a closed menu, so "cost" is not an improvisation tax

The narrator's cost should be a choice from a short list rather than an invention each time. Proposal:

| Cost | What it costs | Where it lands |
| --- | --- | --- |
| **Time** | A clock advances, or a scene is lost | the scene's clock |
| **Exposure** | Someone now knows; a security or attention clock rises | the mission's escalation track |
| **Harm** | Stress, or a consequence if stress cannot absorb it | the sheet (§7.4) |
| **Resource** | Something is spent, lost or left behind | the fiction; no catalogue number |
| **Relationship** | A named person's stance changes | the relationship graph |
| **Position** | You are where you did not want to be | the tactical layer, or the fiction |

Rules that make the menu a rule rather than a mood: **a cost must be worse than nothing and better
than failure**; **a cost is always a fact that can be compelled later**; and **the player may always
propose the cost instead of the narrator** — which is where the 50% narrativism actually lives.

### 4.7 Opposed rolls and the three shapes

- **Opposed**: both sides roll 4dF + the relevant skill. Higher total wins; equal totals are a tie —
  no change, no harm, and the situation moves. An NPC never needs a full sheet: one rating is enough
  (§6.6).
- **Overcome**: one roll against a static difficulty. The default for a single decisive act.
- **Contest**: opposed, first to **three** round-wins (an EXAMPLE; the count is D31's). The default
  for social conflict, intrusion, pursuit, and any struggle where both sides are active and neither
  is trying to hurt the other.
- **Conflict**: opposed attacks against stress and consequences. The default for violence, and for
  any struggle where the point is to *remove* the other side's ability to continue.
- **Challenge**: several overcome rolls, possibly on different skills, for one complicated task. The
  default for "this is too hard for one number".

**The shape is chosen before the dice and announced.** That single sentence is what keeps five action
types on one mechanic: *social* is usually a contest, *investigative* usually an overcome or a
challenge, *physical* usually a conflict, *cyber* usually a contest with a reachability gate,
*PSI* usually an overcome or a contest of will — and none of them has its own arithmetic.

### 4.8 The five action types on the one mechanic

| Action type | Usual shape | Skill | Gate before the roll | Where consequences land |
| --- | --- | --- | --- | --- |
| **Social** | contest (or conflict, for a sustained campaign of pressure) | `SAV`; `WIL` to resist | access to the person | relationship, exposure, mental stress |
| **Investigative** | overcome, or challenge for a case | `COG` (method), `INT` (notice, read) | access to the scene or record | time, exposure, a wrong conclusion as an aspect |
| **Physical** | conflict | `SOM` (force), `REF` (speed, aim, evasion) | reach, equipment as permission | physical stress, consequences |
| **Cyber** | contest | `COG` (intrusion), `REF` (reaction in the mesh) | **reachability**: local access, credentials or a deployed proxy | mental stress, exposure clock, a burned access |
| **PSI / Astral** | overcome (perception), contest of will (intrusion) | `INT` (perception), `WIL` (contest) | a **capability tag** (`TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`) | mental stress, and the body's exposure (§8.5) |

**The one asymmetry that is not a mechanic but a rule of evidence:** a PSI result is *testimony*, not
fact. `ISSUE_220_SOCIAL_PROCEDURES.md`'s governing decision — a social check changes what a character
can achieve, never what a target believes — has a PSI twin: **a PSI check changes what the character
perceives, never what is true.** The narrator may always say the impression was real and the
interpretation wrong.

---

## 5. The smallest usable character model

### 5.1 The question behind the question

#516 says "reconcile existing FIT/REF/INT/SOC/PSY/CYB and other relevant proposals, avoiding
skill-list bloat". Those six are the **legacy** STATs, on a 1–10 scale, added to a 40-skill list and
a d10. The crossover has instead **six Fate-rated skills** (#482, approved) and **seven proposed
strategic skills** (D22). So there are three coherent architectures, and only Tomi can pick one.

### 5.2 Three options

| | **A. Six skills, no second layer** (status quo of #482) | **B. Six attributes + six skills** (#255/#200 two-layer) | **C. Stat tree, no skill list** (#280) |
| --- | --- | --- | --- |
| Rated traits on the sheet | 6 | 12 | 7–9 stats, each with tags |
| Legacy FIT…CYB | a **conversion vocabulary** (used for NPC statlines and legacy cross-reference), not a rating | restored as the rated attributes | replaced by the stat tree |
| What a check reads | one skill | attribute + skill | one stat, tags for domain |
| Bloat | lowest | 12 numbers before any tag | medium; tags absorb everything |
| Reconciles #516's wording? | **partly** — the six exist, but not as rated traits | **yes, literally** | **partly** — the names change |
| Conflicts with | #516's mention of the six stats; #255's "six attributes mandatory" (which was written for the legacy game) | #482's approved six-skill sheet (would add, not remove) | #482 (would remove skills) |
| Cost of changing later | low | medium | high |

**Recommendation: A, with the tag discipline of C.** The six Fate skills are the only numbers on the
sheet; `FIT/REF/INT/SOC/PSY/CYB` survive as the **translation vocabulary** that lets a legacy character,
an NPC statline or a `MissionOutcome` name the same capability without a second scale. The trade-off:
**A gives the smallest sheet and the cheapest implementation, and it pays for that by losing the
attribute/skill distinction #255 insisted on** — a distinction that matters when a player wants to say
"she is strong but untrained" and have the sheet show it. Under A, that is an aspect ("Strong as an
ox, never taught to fight"), which is narratively richer and mechanically coarser. If Tomi wants that
distinction to be *mechanical*, B is the answer and it costs six more numbers and one more addition
per roll. **This is D30**, and it is the single most consequential decision in this record, because
everything else reads the sheet.

### 5.3 The skill-bloat analysis, measured

What each consolidation step actually deletes:

| Layer | Count | What it is | What it would cost to keep |
| --- | ---: | --- | --- |
| Legacy `data/rules/skills.json` (canonical, #159) | **40** | `INT` 11, `PSY` 8, `SOC` 7, `FIT`/`REF`/`CYB` 4 each, `Variable` 2 | a 40-row sheet at 1–10 with a d10; the legacy game's own choice and not this record's business |
| Fate Core default | **18** | the SRD list, 10 rated by the pyramid | an 18-name list is already more than a new player will read |
| Transhumanity's Fate | **24** | scene-shaped, verified | it consolidates into the six — that is the finding of #482's verification, not a preference |
| **Crossover individual (approved)** | **6** | `COG`, `INT`, `REF`, `SAV`, `SOM`, `WIL` | — |
| **Crossover strategic (proposed)** | **7** | `statecraft`, `fieldcraft`, `inquiry`, `stewardship`, `command`, `science`, `security` | the second list is per-*scale*, not per-scene, and is D22 |

**Bloat is not only a count — it is the number of names a player must distinguish to act.** The six
were chosen broad on purpose (`RULEBOOK.md` §3): they describe the *kinds* of thing a person can
attempt. The danger with #516's deliverable list is that "simplified science" arrives as a seventh
skill, then "hacking" as an eighth, then "PSI" as a ninth — each individually defensible, collectively
the 18-skill list rebuilt by accretion. The guard against that is the **three-place rule**:

| Place | Holds | Example |
| --- | --- | --- |
| **Skill** (6) | a broad kind of attempt | `COG` |
| **Competence tag** | a *domain* the character is trained in — permission and colour, **no bonus by itself** | `COG: forensic reconstruction` |
| **Stunt** | a named exception that changes an outcome, **priced in refresh** | "Once per scene, on a `COG` overcome to reconstruct a record, treat a tie as a success" |

Anything that does not fit one of those three places is a new subsystem and needs an author decision.
That is the rule that keeps the sheet small without forbidding specialisation — and it is already what
`RULEBOOK.md` §3.2 says, so §5 is not proposing a new mechanism, it is proposing to *hold the line*.

**Science, concretely, because the issue names it.** There is no `Science` skill. Method is `COG`;
a discipline is a competence tag; a signature technique is a stunt. Note the adjacent decision: #506's
research engine already calls a strategic `SCIENCE` check, which is the *strategic* roster's `science`
(D22), not a seventh individual skill. **If Tomi wants a rated Science skill in scenes, that is a
seventh skill and it is D33** — with the honest trade: one more number for one fewer argument at the
table about whether a biologist can do biochemistry.

### 5.4 Tags and aspects: three different jobs, kept apart

| Thing | Job | Moves a roll? | Where it lives |
| --- | --- | --- | --- |
| **Aspect** | a true statement about the fiction that can be invoked or compelled | yes, via a Fate point or a free invoke | the sheet (5) or the scene |
| **Competence tag** | permission and colour: *this character is trained in X* | **no** — it gates and it colours | the sheet, typed (`TAG_KINDS`) |
| **Capability tag** | permission to attempt a gated action at all (`TELEPATH`, `REMOTE_VIEWER`, netrunner) | no — it is a **gate**, checked before dice | the sheet, typed |
| **Condition** | a lasting fact that constrains (injured, compromised, exposed) | not as a modifier — as a *fiction* the narrator and the player must respect | the sheet, typed |

**The collision to avoid** is #280's universal TAG, which can be active, passive, competence or
negative — four semantics in one record type. That is elegant as a data model and dangerous as a
table rule, because a player who has learned that tags are *permissions* will one day expect one to
add +2. The proposal keeps the **data** unified (they are all tags, as `TAG_KINDS` already has it) and
keeps the **semantics** visibly separate in the rulebook's table. `ISSUE_461_CONSENSUS_PROPOSAL.md`
decision 10 — "the tag is the bookkeeping, the stunt is the mechanism, refresh is the price" — is the
same reading, and this record agrees with it rather than proposing a third.

### 5.5 Wounds and stress

Fate's structure, unchanged, with **one proposed extension that is the whole of the simulationist 25%
in the character model**:

- two stress tracks, two boxes each (physical, mental) — EXAMPLE defaults, already in `RULEBOOK.md` §7;
- three consequence slots, mild 2 / moderate 4 / severe 6;
- **proposal:** a consequence taken during a mission **may** be carried out of it as a **named
  injury** on the strategic layer, with a recovery condition ("until treated", "three turns", "until
  she stops using the arm"). Not a number, a fact. That is what makes X-COM's "your best agent is in
  the infirmary" possible without a hit-point model — and what makes it an author decision (**D35**),
  because it is also how a mission writes into the faction's roster.

**What is deliberately absent:** a hit-point total, a wound threshold table, a death save, a
cyberware capacity number, and any "you wake up in a new body" routine. Each of those is either
simulationist bloat or a setting import.

### 5.6 Advancement

Unchanged from Fate's milestone baseline and **not decided here**: D23 already carries "starting
allocation and advancement" for the six skills, and this record adds nothing to it. What it does add
is one observation: **if advancement raises a skill, it will eventually collide with the 4dF ladder's
four informative steps.** Fate's own answer is that skills top out around +4/+5 and growth moves
sideways into stunts and refresh. A playtest that hands out +1 per session will discover this in about
six sessions, which is exactly the kind of thing the playtest #516 asks for is *for*.

### 5.7 NPCs: three tiers, no fourth

| Tier | What it needs | Used for |
| --- | --- | --- |
| **Extra** | a name, one rating, one tag | a guard, a clerk, a crowd |
| **Supporting** | a name, two aspects, two ratings, one capability tag | a recurring witness, a rival agent, a contact |
| **Principal** | the full sheet, five aspects, six skills, stunts, stress | the antagonist, the leader's opposite number |

The gamist family's real gift to this sheet is C6: **an NPC is a line of text.** A narrator who has to
build a character to have a conversation will stop having conversations.

---

## 6. Player agency, the narrator's job, and noncombat conflict

### 6.1 The five rules that carry the 50%

These are *proposals about how to adjudicate*, and they are where narrativism actually lives — not in
a subsystem.

1. **Fiction first.** No dice until the fiction contains the action. If the action is impossible,
   the answer is "no, and here is what you would need" — not a difficulty.
2. **Roll only when both outcomes are interesting.** A roll that cannot fail interestingly is a
   "yes". A roll that cannot succeed is a "no".
3. **Failure changes the situation; it does not stop the scene.** (P9 + C11.) The narrator makes a
   move that follows: a cost, a clock, a new obstacle, a revealed complication.
4. **No single roll gates an essential clue.** (#262.) Three clues per conclusion is the working
   heuristic: if the players miss one, another carries it. Rolling badly may cost *time, exposure or
   a wrong first reading* — never the case.
5. **The player may propose the cost.** A player who says "I succeed, and my credentials are burned"
   has done the narrator's job and should be allowed to.

### 6.2 What the narrator may not do

- **May not decide what a character believes, wants or feels.** Social and PSI results change what is
  achievable and what is perceived (`ISSUE_220_SOCIAL_PROCEDURES.md`; §4.8 above). This is the single
  most important boundary in the record, and it is the one that keeps PSI from becoming mind control.
- **May not invent a number to make something harder.** If it is too hard for one roll, it is a
  challenge (§4.7), not a bigger difficulty.
- **May not substitute an action.** A refused declaration is refused; the character does not get a
  consolation roll (#461).
- **May not spend a player's Fate points.** Compels are offers.

### 6.3 Noncombat conflict, specifically

| Kind | Shape | The thing that makes it a *conflict* rather than a check |
| --- | --- | --- |
| **Dialogue** | contest, first to three | both sides are trying to move the other, and both can lose ground |
| **Investigation** | overcome, then challenge | the case has structure; a clock or a clue list is the opposition |
| **Hacking** | contest with a gate | the system pushes back, and exposure accumulates whether you win or lose |
| **PSI** | overcome to perceive, contest of will to intrude | the other mind is an agent, and a strong will is a wall |
| **Interrogation** | contest, with a compel as the lever | the subject has something to protect and can spend it |

**Noncombat conflict uses the same stress tracks.** A humiliating cross-examination is mental stress.
A burned cover is a consequence. Nothing needs a new track to be *consequential* — and the moment a
social system gets its own "social HP", the 50% has been spent on a subsystem instead of on scenes.

---

## 7. Fast, dangerous, small-squad tactical combat — optional

### 7.1 The requirement, read narrowly

#516 asks for combat that is **fast and dangerous**, for **small squads**, with **action economy,
cover, positioning and injury** — and explicitly **not required for every quest**. #515 asks that the
same four agents and the same outcomes cross onto a tile map. So the design target is not "a skirmish
game"; it is the **smallest set of tactical decisions that makes a fight feel like a fight**, sharing
the sheet with everything else.

### 7.2 Three options

| | **T1. Zone conflict** (recommended) | **T2. AP skirmish** | **T3. Abstract conflict** |
| --- | --- | --- | --- |
| Map | 3–6 **zones** per scene; adjacency is a fact, not a distance | grid or tile map with movement points | none |
| Action economy | **one action + one reaction** per character per turn; the reaction is a defend or an overwatch | 3 AP (#225's proposal); movement, attack, aim, overwatch each cost AP | one action per exchange, no position |
| Cover | an **aspect** on the zone ("reinforced planter"), invokable for defence; some cover is a *gate* (blocks a line of fire) | cover as a modifier or a chance-to-hit penalty | a scene aspect |
| Positioning | zones + who is in which one; flanking = attacking a zone the target is not facing | grid coordinates, facing, line of sight | none |
| Injury | stress and consequences; a taken-out result is narrated, not rolled on a table | same, plus optional hit locations | same |
| Speed | 3–5 exchanges for a squad fight | slower, more decisions per turn | fastest, least tactical |
| Fit to 25% gamism | enough: which zone, when to spend, who takes the reaction | strongest | weakest |
| Fit to #515 | direct — zones map onto tiles without a rewrite | direct, but the map becomes mandatory | incompatible with a tactical map |
| Second engine? | **no** — it is Fate's conflict with a spatial vocabulary | **yes** — AP is a second economy | no, but it drops a deliverable |

**Recommendation: T1 for v1, with T2 kept as the #515 overlay if playtest shows T1 too coarse.** The
trade-off: **T1 buys speed and one-engine coherence at the cost of tactical depth.** A player who wants
X-COM's "two actions, half cover, overwatch, flank" will find T1 thin, because "one action + one
reaction" collapses move-and-shoot into a choice. The honest mitigation is that T1's depth comes from
*zones and aspects* rather than from action points: whether the planter is between you and the shooter
is a bigger decision than whether you spend one AP or two. **And the honest cost:** zones make
"positioning" coarse enough that a tactical player may feel the map is decoration. That is what the
playtest is for, and it is **D34**.

### 7.3 Action economy, in the recommended option

- **One action** per character per turn: attack, create an advantage, overcome an obstacle, move to an
  adjacent zone, or **hold** (the refused-order case, #461).
- **One reaction** per round, and only one: defend, or overwatch a zone. A reaction is *not* a second
  action; it is spent when triggered and it is the reason a squad cannot simply walk into a room.
- **Initiative**: one order for the side, refinable by the players ("the netrunner goes first"), never
  forked into separate tracks per layer (#225 §4). The GM runs all opposition on one turn.
- **No free actions.** Everything a character does in a fight costs the action or the reaction. This
  is the rule that makes the fight fast: there is nothing to track between them.

### 7.4 Danger without a damage engine

- Damage = the attack's shifts, applied to stress; overflow must become a consequence or the character
  is **taken out**.
- **Taken out is not dead.** The winner narrates the outcome; death is a choice the table makes, not
  a dice result. (This is the single biggest lever on "dangerous but not punishing".)
- **Conceding** is available at any point before being taken out, and it costs the character the
  stakes rather than the body.
- **Morale** (C10): opposition with a `WIL` rating checks when it loses half its number or its leader.
  A fight that ends because the other side quits is faster and more realistic than one that ends in a
  wipe.
- **Persistent injury**: the §5.5 proposal — a consequence may leave the mission as a named injury.

### 7.5 Cover and positioning as *gates and aspects*, never as modifiers

The repository's rule — "gate vs modify, never both" (#461 Fork 2, `cyber.py::resolve_access`) —
applies here and settles an argument before it starts. Cover is either:

- **a gate**: the line of fire does not exist, so the attack is refused at declaration; or
- **an aspect**: the shot exists, and the defender invokes the planter for +2 or a reroll.

It is never both, and it is never a -2 to hit. One rule, one place, no stacking — which is also why
the tactical layer cannot quietly become a second combat system.

---

## 8. PSI, psychotronics, cybernetics and hacking across Physical / Cyber / Astral

### 8.1 The model in one paragraph

The three realities are **three places a character can be acting**, not three subsystems. Each has a
**gate** (can you act there at all), a **skill** (which of the six reads the action), a **shape** (from
§4.7), and a **place where consequences land**. Everything else — psychotronics, cybernetics, sleights
— is *equipment or capability*, and equipment is a permission with a tag (C9, T3).

| | **Physical** | **Cyber** | **Astral / Noöspace** |
| --- | --- | --- | --- |
| Gate | reach, a body that works | **reachability**: local access, credentials, or a deployed proxy | a **capability tag** (`TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`) |
| Skill | `SOM`, `REF` | `COG` (intrusion), `REF` (reaction) | `INT` (perceive), `WIL` (contest) |
| Shape | conflict | contest | overcome, or contest of will |
| Consequence lands on | physical stress, body consequences | mental stress, exposure clock, burned access | mental stress, **and the body's exposure** |
| The cost that makes it interesting | harm | time and traceability | **the body is defenceless while the mind is elsewhere** |

### 8.2 PSI: capability, not a power list

- A capability tag decides *whether* a PSI action is possible. It is checked **before any dice**, and
  a character without it is **refused**, not given a harder roll (#482 §3.2, already enforced).
- The action itself is one of the six skills. A precognitive impression is `INT`; contesting a mind is
  `WIL`; there is deliberately **no `Psi` skill**.
- **Sleights (E6) are stunts**: a named technique that changes an outcome, priced in refresh. That is
  the whole "power list" — a character has as many as they paid for.
- **No PSI points.** A second pool would collide with Fate points (E3, P7).
- **PSI proves nothing.** §4.8's rule of evidence. This is what keeps a mystery a mystery when a
  telepath is in the party, and it is the PSI expression of #220's social boundary.

### 8.3 Psychotronics and cybernetics: equipment as permission

- A psychotronic device is **a permission with a tag** — it lets you attempt something, or it doesn't.
  It never adds +2 by existing, and it never creates PSI where there is no capability.
- Cyberware is the same: a neural jack is *access*, a hardened interface is *a defence aspect*, a
  prosthetic is *a body fact with a consequence when it is damaged*.
- **No capacity number** (C4's System Strain is rejected). If a limit is wanted, the cheapest honest
  one is **slots** — "you have three implanted things and this is the fourth" — and it is an author
  decision, not this record's.

### 8.4 Hacking: a contest with a gate, and the gate is the interesting part

The sequence is fixed and short:

1. **Reach**: is the target reachable? Local jack, credentials, or a proxy in place. If no, the
   declaration is refused and the player must go and *get* reach — which is a scene, and usually the
   best scene in the session.
2. **Shape**: a contest, `COG` against the system's rating, first to three.
3. **Cost**: the exposure clock rises every round whether or not the intrusion succeeds. A win that
   takes six rounds has told the building you are there.
4. **Consequence**: a burned access, a mental-stress hit, or a system that now knows your face.

**Why a contest and not a single roll:** intrusion is the clearest case in the game of an action where
*both sides are active and time matters*, which is exactly what a contest is for. Why not a minigame:
Shadowrun's Matrix turn is the cautionary example in the matrix (§3) — it makes four players watch one.

### 8.5 The Astral layer's price: single locus

#225's invariant, kept: **a character acts in one locus at a time.** A projected character's body is
present, defenceless, and can be found. This is not a limitation to be engineered away — it is the
entire dramatic cost of projection, and it is what stops "why doesn't everyone just project" from
being a rules question.

### 8.6 The options Tomi has to choose between

| Question | Option 1 | Option 2 | Option 3 |
| --- | --- | --- | --- |
| Is there a **third stress track** for the interface/signal? | no — mental stress carries it (recommended: fewer tracks, and the exposure clock already models system harm) | yes — an `Interface` track, so a hack can hurt the deck without hurting the mind | a track *per device*, which is a simulationist step and probably too much bookkeeping |
| Is PSI **one capability or several**? | several typed tags, as today (`TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`) — recommended, because it is already the data | one `PSI` capability, with sleights as stunts | a rated `PSI` skill — the seventh-skill question again (D33) |
| Does cyberware have a **capacity limit**? | none (recommended) | slots | a strain number (C4, rejected above) |

---

## 9. Cross-layer propagation: the same characters, the same outcomes

### 9.1 The chain, and the one write

```text
   scene check  ──►  a fact in the fiction (a consequence, an aspect, a clue, a burned access)
        │
        ▼
   mission outcome  ──►  ONE  MissionOutcome record  ──►  WorldState  ──►  faction turn
        │                     (named effects, no scalars)                (one action per character)
        ▼
   tactical exchange (optional)  ──►  the same stress and consequences, on the same sheet
```

**The proposal that makes the chain safe: one outcome, applied once.** Zooming into a tactical map does
not re-resolve a mission that was already resolved, and a scene that settles a committed order does
not grant a second one (#461/#482's §8.1 rule, `ISSUE_461_CONSENSUS_PROPOSAL.md` correction:
"no double application on zoom").

### 9.2 What each layer may read and write

| Layer | Reads | Writes | May **not** do |
| --- | --- | --- | --- |
| **Scene** (RPG) | the sheet: six skills, aspects, tags, stress | facts: consequences, scene aspects, clue states, relationship facts | grant an extra order; change a faction quantity |
| **Mission** (one order) | the sheet; the committed declaration | one `MissionOutcome`: success/failure, named effects, injuries, intel | invent a number; write a quantity that is not approved |
| **Tactical** (optional) | the sheet; the mission's zones and opposition | stress, consequences, position, ammo-as-fiction | use a second stat set; change the mission's stakes |
| **Strategy** (board) | `MissionOutcome.effects`; `WorldState` | its own six quantities, if and when approved | read a scene's difficulty as a strategic number |

### 9.3 The effects a mission may produce — as a *proposal*, because #502 leaves the vocabulary open

| Effect kind | Example (ILLUSTRATIVE) | Read by |
| --- | --- | --- |
| **Intel** | "the facility's night shift is short-staffed on Thursdays" | investigation, mission planning |
| **Injury** | "Voss: broken wrist, cannot use `SOM` above +1 until treated" | roster availability, tactical deployment |
| **Exposure** | "UNSA counter-intelligence has a photograph" | security clock, faction reputation |
| **Access** | "a working credential for the freight lift" | the next mission's reachability gate |
| **Relationship** | "Chair Okafor will take your call; her deputy will not" | social scenes, statecraft missions |
| **Material** | "one working psychotronic array, uncalibrated" | equipment as permission |
| **Position** | "the faction now holds the records office" | the strategic board |

**Note what is absent: any number.** Not because numbers are forbidden, but because every number here
would be one the author has not set (D3, D11, D27). The design point is that a mission can be
*consequential* using only named facts — and that this is the cheapest possible version of Terra
Invicta's "your councilor's op changed the world".

### 9.4 Why this is the layer that makes the 50/25/25 real

A narrativist scene produces a **fact**; a gamist mission produces a **decision**; a simulationist
consequence **persists**. The three priorities are not three engines — they are three *stages of the
same record*, and `MissionOutcome` is the record. That is the answer to the issue's hardest structural
question ("how do the same characters carry from adventure to tactical map to faction strategy"), and
it is answerable without a single new number.

---

## 10. Worked examples

**Everything in this section is an ILLUSTRATION OF A PROPOSAL. The difficulties, dice, skills and
outcomes are examples chosen to show the procedure; none of them is a rule, a target number, a
threshold or a precedent.** Dice are written as the four Fate dice in order; a Fate point spend is
marked. Names are invented for the example.

### 10.1 Investigation — a tie that costs

**Situation.** Agent Mirela Voss is in a clinic records room, checking a log that should show a
patient admitted at 02:10. She has `COG +3` and the competence tag `COG: forensic reconstruction`.

**Declared action.** *Overcome* — read the log and establish whether the timestamp was altered.
Reachability is established (she is in the room, with a staff credential taken in the previous scene,
which is a **fact** and not a bonus).

**Difficulty (EXAMPLE):** Good (+3) — the alteration was done by someone competent.

**Roll:** `0, +1, −1, 0` = **0**; total **3** against the difficulty of **3** → **tie**.

**Outcome.** Under §4.5, a tie on an overcome is **success at a minor cost**. She reads the alteration
— the log was edited, and the edit is clumsy in one place — **and** the cost: the terminal logs *her*
access under a staff ID that will be audited on Monday. The narrator offers the cost; the player takes
it, because the alternative (a second roll, a louder trace) is worse.

**What travels.** `Intel`: "the 02:10 admission was inserted after the fact". `Exposure`: "Voss's
credential is in an audit trail". Neither is a number. Both can be compelled later — and the exposure
is exactly what the tactical example (§10.4) inherits as an escalation clock.

**What this example is demonstrating.** Three of the record's proposals at once: the tie is where
narrativism lives; a competence tag coloured the attempt without adding a bonus; and the *cost* is a
fact that propagates.

### 10.2 Social conflict — a contest that changes what can be done, not what is believed

**Situation.** The faction leader, Ilse Brandt (`SAV +2`), needs Chair Okafor to release a committee's
working papers. Okafor (`SAV +3`) will not, because releasing them exposes a colleague.

**Shape.** A **contest**, first to three round-wins. Not a conflict: nobody is trying to destroy
anybody, and a "taken out" result on a person's convictions would be exactly the mind-rewriting
§6.2 forbids.

**Round 1.** Brandt `0, +1, 0, −1` = 0 → **2**. Okafor `−1, 0, +1, +1` = +1 → **4**. Okafor wins the
round: she reframes the request as a leak. **1–0.**

**Round 2.** Brandt's player invokes her aspect *"Owes the Academy a favour"* (**1 Fate point, +2**):
roll `+1, +1, 0, 0` = +2 → 2 + 2 + 2 = **6**; Okafor rolls `0, 0, −1, +1` = 0 → **3**. Brandt takes
the round. **1–1.** The invoke is spent and gone.

**Round 3.** Brandt **creates an advantage** — she puts Okafor's own signed minute in front of her
(`SAV` vs Fair +2, EXAMPLE). Roll `+1, +1, +1, 0` = +3 → **5** against 2 → **succeed with style**:
the aspect *"her own minute contradicts her"* with **two** free invokes.

**Round 4.** Brandt attacks the position, spending one free invoke (+2): `0, +1, +1, −1` = +1 →
2 + 1 + 2 = **5**; Okafor `−1, 0, 0, 0` = −1 → **2**. **Brandt takes the third round.**

**Outcome.** Okafor releases the papers **and** keeps her stated reason for having withheld them. She
is not persuaded; she is outmanoeuvred, and she knows it. The narrator may compel the consequence
later — she will remember.

**What travels.** `Access`: the working papers (a new investigative surface). `Relationship`: "Okafor
will deal, and will not forgive". A mild consequence on Brandt if the player had chosen to press
harder: *"made an enemy of a committee chair"*.

**What this example is demonstrating.** The boundary of §6.2 in play: a social *win* that leaves the
person's beliefs intact, which is both more interesting and the only reading compatible with
player-agency-as-a-principle.

### 10.3 PSI and hacking — two gates, one arithmetic

**(a) Hacking.** Agent Teo Marchetti (`COG +3`, capability tag `netrunner`) wants the clinic's
appointment system.

1. **Reach.** The system is not on the public mesh; it is on the clinic's internal segment. He is in
   the building (established in §10.1's scene) and has the staff credential. **Gate passed.** Had he
   been in a car outside, the declaration would have been **refused** — not made harder.
2. **Shape.** A contest, `COG +3` against the system's rating (**+2**, EXAMPLE), first to three.
3. **Rounds.** R1 `+1,0,+1,−1`=+1 → 4 vs system `0,+1,0,0`=+1 → 3: Teo. R2 `0,0,−1,+1`=0 → 3 vs
   `+1,+1,0,−1`=+1 → 3: **tie**, no score, and the **exposure clock ticks**. R3 `+1,+1,0,0`=+2 → 5 vs
   `−1,0,0,+1`=0 → 2: Teo. R4 `0,+1,+1,0`=+2 → 5 vs `0,0,0,−1`=−1 → 1: Teo. **Three round-wins in
   four exchanges.**
4. **Cost.** The intrusion took four rounds; exposure is at **3 of 6** (EXAMPLE clock). A win that
   had taken six would have tripped the audit.

**(b) PSI.** Agent Sana Ríos has `INT +2` and the capability tag `REMOTE_VIEWER`. She views the
records room from a safe house.

- **Shape.** *Overcome* on `INT` against Good (+3), EXAMPLE. Roll `0, +1, +1, −1` = +1 → **3** vs 3 →
  **tie**: she gets an impression **at a cost**.
- **Outcome.** She perceives a figure at the terminal at 02:10 — and the cost is that the impression
  is *unclear about the face*, and she takes one mental stress from the effort.
- **The rule that matters.** The narrator may not say "the figure was Dr Kessler". The player has a
  **report**, which is testimony. It corroborates the log's alteration and does not identify anyone.
  If the player later acts on the assumption, that is a compel waiting to happen.

**What this example is demonstrating.** Two different gates (reachability vs capability), one
arithmetic, and the PSI evidence rule doing real work in a mystery instead of short-circuiting it.

### 10.4 Combat — four agents, three zones

**Situation.** The clinic's service corridor. Three zones: **Records Room** — **Corridor** —
**Loading Bay**. Two hostile contractors in the corridor; one has taken cover behind a **reinforced
planter** (a zone aspect, invokable for defence).

**Squad.** Voss (`SOM +1`, `REF +2`, physical stress 2), Marchetti (`REF +3`), Ríos (`WIL +3`), and
Brandt (`SAV +3`, `SOM +1`). The players choose the order; Marchetti first.

| Exchange | Who | Action | Roll (EXAMPLE) | Result |
| --- | --- | --- | --- | --- |
| 1 | Marchetti | *Create an advantage*: suppress the corridor with fire | `REF +3`, `+1,0,+1,−1` = +1 → **4** vs Fair 2 | *"pinned behind the planter"*, one free invoke |
| 1 | Contractor A | Attack Voss | `SOM +2`, `+1,+1,0,−1` = +1 → **3** vs Voss defence `REF +2`, `0,0,+1,0` = +1 → **3** | **tie** — no harm; Voss is driven back a zone (position cost) |
| 2 | Voss | Attack A, spending the free invoke (+2) | `SOM +1`, `+1,+1,+1,0` = +3 → 1 + 3 + 2 = **6** vs A defence `REF +2`, `−1,0,0,0` = −1 → **1** | **5 shifts** → A's stress (2 boxes) cannot absorb it; A takes a moderate consequence (*"shoulder wound"*) and is **taken out** by the narrator, not killed |
| 2 | Contractor B | **Reaction** — overwatch the corridor | — | anyone crossing into the corridor this round is attacked |
| 3 | Ríos | *Overcome*: drag the wounded contractor clear | `SOM +0`, `0,+1,0,0` = +1 → **1** vs Average 1 | **tie** — she gets him out, and takes a mild consequence (*"wrenched back"*), which **will** leave the mission as a named injury |
| 3 | Brandt | *Hold* — she is not a fighter, and the players spend her action on nothing | — | one action spent; #461's hold |

**Outcome.** One hostile taken out, one captured, no PC deaths, two consequences that will outlive the
scene. Total: **three exchanges**, roughly the target for a squad fight.

**What this example is demonstrating.** (i) A reaction is the reason the corridor is dangerous.
(ii) Cover is an aspect, invoked once, never a modifier. (iii) "Taken out" narrated rather than
rolled. (iv) A consequence becomes an **injury fact** and therefore the seed of the next mission's
complication — the simulationist 25% arriving through the narrativist mechanism.

### 10.5 A mixed four-agent mission — one order each, one record

**Situation.** One mission turn, four agents, four different layers. The objective: establish what
happened to a patient and who moved her file. This is the example #516 asks for — the same characters,
the same rules, across layers.

| Agent | Order | Layer | Shape and skill | Outcome (EXAMPLE) | Effect recorded |
| --- | --- | --- | --- | --- | --- |
| Voss | Work the records room | Physical/investigative | overcome `COG` | tie → success at cost | `Intel`: file altered; `Exposure`: her credential is audited |
| Marchetti | Intrude on the appointment system | Cyber | contest `COG` vs +2 | three rounds, wins | `Access`: appointment export; exposure clock 3/6 |
| Ríos | View the records room from the safe house | Astral | overcome `INT` | tie → unclear impression | `Intel`: a figure, face unknown (testimony only) |
| Brandt | Meet the clinic's administrator | Social | contest `SAV` | wins 3–1 | `Relationship`: the administrator will talk again; `Access`: staff roster |

**The record produced** — one `MissionOutcome`, four effects, no numbers:

```text
mission:   "the 02:10 admission"
result:    partial — the alteration is established; the author of it is not
effects:   intel      the 02:10 admission was inserted after the fact
           intel      a figure was present; identity unknown (PSI testimony)
           access     appointment export; staff roster; working credential (burned Monday)
           exposure   Voss's credential in an audit trail; intrusion clock 3/6
           injury     Ríos: wrenched back (mild) — recovery condition: rest or treatment
           relation   administrator will meet again; committee chair will not forgive
```

**What propagates, and where it lands.**

- **Next mission:** the appointment export is a *reachability* asset — Marchetti does not need the
  building again. The audit trail is an *escalation* clock that starts the next mission at 3/6.
- **Tactical layer:** Ríos's injury is a fact on the sheet — she deploys, or she doesn't. No new
  number: her consequence is still a consequence.
- **Strategic layer:** "the administrator will meet again" is a relationship fact a `statecraft`
  mission can use. Nothing here moves one of the six quantities, because no effect kind that moves a
  quantity is approved (D35).

**What this example is demonstrating — and what it is not.** It is demonstrating that #516's hardest
requirement (the same characters and outcomes across three layers) is satisfiable with **one sheet, one
arithmetic and named facts**. It is **not** demonstrating that these four orders are a balanced turn,
that the difficulties are right, or that the mission is fun. Those are playtest questions, and the
playtest has not been run.

---

## 11. What is left for Tomi

### 11.1 The decision rows this record adds

Nine rows, **D29–D37**, in `AUTHOR_DECISION_QUEUE.md`. Each is author-only, each names its options and
its trade-off, and none of them is answered here. In summary:

| Row | The decision | This record's recommendation |
| --- | --- | --- |
| **D29** | Does #516 govern the crossover only, or also the legacy `1d10` game? | crossover only; legacy untouched |
| **D30** | Six skills only, or six attributes **and** six skills? | six skills, with FIT…CYB as conversion vocabulary |
| **D31** | One kernel (4dF, four outcomes) or a dual/replacement kernel; contest length; open or hidden difficulty | one kernel; contest to three; open difficulty |
| **D32** | Is there a distinct "success at a cost" band? | no — cost on the tie |
| **D33** | Is "science" a seventh individual skill, or `COG` + tag + stunt? | `COG` + tag + stunt |
| **D34** | Tactical action economy: one action + reaction, 2 AP, or 3 AP; and is combat ever mandatory? | one action + reaction; never mandatory |
| **D35** | Do mission consequences persist as strategic injuries, and who writes the effects? | yes; narrator-written from a closed menu |
| **D36** | A third stress track for interface/signal, and a cyberware capacity limit? | no track, no limit |
| **D37** | **The sign-off itself**: accept as the basis for a playtest draft, amend, or reject — and does acceptance make it canonical in `strategy_game/RULEBOOK.md`? | the author's alone; this record recommends nothing |

### 11.2 The work that is not a document

#516's "Done when" needs three things this PR cannot supply:

1. **A playtest.** A short adventure and a combat encounter, played by humans, checking pace,
   lethality and decision quality — then revised. §10 is the material; the table is the missing step.
2. **Tomi's reading of §2 and §4.** The comparison and the resolution options are the parts where a
   wrong call is expensive to reverse.
3. **Tomi's explicit sign-off**, in his own words, on the issue or in a file. Nothing in this
   repository should be read as that sign-off, and this record does not claim it.

### 11.3 What this record deliberately did not do

- Did not write a single rule into `strategy_game/RULEBOOK.md` or `RULEBOOK.md`; both are untouched.
- Did not choose a licence (D10), a renderer (D13), a strategic roster (D22), a starting allocation
  (D23), or any number that moves a world quantity (D3, D11, D27).
- Did not revive the legacy `1d10` kernel, the Fudge-centred proposal (#200's superseded text), or
  #280's stat tree.
- Did not run a playtest, and does not describe one as if it had.
- Did not add or change a test. Documentation is reviewed editorially and by playtesting.

---

**Verification.** `git diff --stat` for this PR: two files in `docs/design/`, no other path; deletions
zero. `strategy_game/RULEBOOK.md` and `RULEBOOK.md` are byte-identical to `origin/main` (checked by
`git diff --stat` showing neither). Both suites run on the branch: root **585 tests OK**, strategy
**1338 tests OK** — unchanged from the baseline measured before the branch, because documentation
changes no executable behaviour.

**Refs #516** — not `Closes`: this issue closes when Tomi signs off, and only then. Refs #461, #255,
#200, #280, #262, #502, #515.

— Ai (愛), 2026-10-19. Proposal only. No rule is canonical, and the ruleset awaits the author's
sign-off.

## 10. Reconciliation: three skill vocabularies, one proposal

Issue #516 asks for the explicit reconciliation the earlier sections imply but do
not build: **#482's six individual skills** against the **legacy FIT/REF/INT/SOC/
PSY/CYB** attributes, and against **#506's single strategic SCIENCE skill**. This
section is a *proposal*. Rows Tomi must rule on are marked **DECISION**; nothing
here replaces approved mechanics on its own authority.

### 10.1 What is actually in the repo

| Roster | Where it lives | Size | Standing |
| --- | --- | --- | --- |
| Individual skills | `strategy_game/rpg/skills.py`, #482 | 6 rated (COG, INT, REF, SAV, SOM, WIL) | Approved implementation baseline, pending #516 sign-off |
| Legacy attributes | narrative-layer character sheets | 6 rated (FIT, REF, INT, SOC, PSY, CYB) | Retained "as an author preference unless explicitly changed" (#262) |
| Legacy skills | legacy character generation | ~40 rated | Superseded in practice; no engine reads them |
| Strategic skills | #506 research engine | `SCIENCE` (plus existing strategic roster) | Approved: research uses one science check, no domain tags (#509) |

### 10.2 The legacy attributes, one by one

| Legacy | Answers | Nearest individual skill | Overlap | Proposed disposition |
| --- | --- | --- | --- | --- |
| FIT | physical force and endurance | SOM | total | SOM absorbs FIT; no separate rated trait |
| REF | reflexes, timing, initiative | REF | identical | keep REF unchanged — same name, same sense |
| INT | reasoning, recall, analysis | COG **and** INT | **contested** | see 10.3 — this is the one real collision |
| SOC | persuasion, presence, reading people | SAV | strong | SAV absorbs SOC |
| PSY | will, nerve, resistance to pressure | WIL | total | WIL absorbs PSY |
| CYB | affinity for cybernetics and nets | none directly (REF/INT adjacent) | partial | **DECISION** — rated trait or capability tag? See 10.4 |

### 10.3 COG versus INT — the one genuine collision

Both names denote cognition, so keeping both risks a sheet where a player cannot
tell which roll to ask for. Two coherent resolutions, and the choice is Tomi's:

1. **Split by kind, not by degree.** `INT` is *declarative* — what the character
   has learned (history, protocols, species, law). `COG` is *procedural* — what
   the character can work out under pressure (analysis, synthesis, diagnosis).
   This is the reading that keeps six skills and makes each earn its place.
2. **Merge.** `COG` absorbs `INT`; learned facts become a competence tag
   (`trained: xenoarchaeology`) rather than a rated trait, which matches the
   skill-bloat analysis in §5.3 and reduces the sheet to five.

**DECISION 1.** Split (6 skills) or merge (5 + tags)?

### 10.4 CYB — trait or tag?

`CYB` measures affinity with implanted and networked systems. Every other roster
in the repo already treats *permission* (what you have installed) as a tag and
*competence* as a skill, and §8.3 keeps equipment as permission. Proposal: **CYB
becomes a capability tag, not a rated trait** — a character with a neural jack has
`cyb: neural_jack`, and the roll is REF (fast) or COG/INT (careful), so cyber
action never needs a seventh rating. The alternative — keeping CYB rated — is only
worth it if cyber competence should vary independently of REF and INT, which no
current mechanic requires.

**DECISION 2.** CYB as tag (proposed) or as rated trait?

### 10.5 SCIENCE (#506) is not a sixth individual skill

The strategic `SCIENCE` check and the individual `COG` skill are **different
scopes**, and conflating them is the trap this section exists to avoid:

| Question | Who answers it | Roster |
| --- | --- | --- |
| "Can this character work out what this artefact does?" | the character | COG (+ competence tag) |
| "Does this faction's research project advance this cycle?" | the faction | strategic `SCIENCE` (#506) |

Proposal: keep both, never the same roll. A faction project's progress is a
faction-level check against `SCIENCE` plus resources and prerequisites; an
individual's insight is a character-level COG check. They may inform each other
narratively — a character with `trained: xenotech` can *narrate* the breakthrough
— but one is never re-rolled as the other. This also keeps #506's approved
decision intact (single science skill, no domain tags).

**DECISION 3.** Confirm the two-scope split, or is there a case where an
individual's COG should substitute for a faction's SCIENCE check?

### 10.6 The ~40 legacy skills

They collapse. Under the proposal every one of them becomes either a competence
tag on one of the six skills or a narrative permission, because none of them is
read by an engine and each one is a chance for a player to ask the wrong question
at the table. §5.3 already measures the bloat; this is the disposition: **40
rated skills → 6 rated skills + an open competence-tag vocabulary.**

**DECISION 4.** Accept the collapse, or name specific legacy skills that must
remain rated because a mechanic depends on them?

### 10.7 What this section does not decide

It does not choose between the three character-model options in §5.2, it does not
approve the resolution arithmetic in §4, and it makes no ruling on wounds,
advancement or the tactical layer. It answers one question — how the three
vocabularies coexist — and leaves the four decisions above where they belong.
