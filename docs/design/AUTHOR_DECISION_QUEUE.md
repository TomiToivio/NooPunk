# Author decision queue — what is blocking the open NoöPunk issues

**What this file is.** A consolidation, not a design. Every row is condensed from the issue that
carries it. Nothing here is canon, a mechanic, a name or a ruling: each row is a **question only the
author can answer**. Answering one turns it into a criterion check, an acceptance record, a PR and a
close.

**Board status (2026-10-14, seventh update).** No issue open: **#323** closed on the defer-and-close rule
after its acceptance record was corrected so that every criterion is labelled accurately — its criterion 2
is **met** (the §4 mission column is refused by name in `structural_problems`), and the rule-dependent rows
carry their deferrals as deferrals. **#338 closed** (#436
closeout), **#309
closed on author direction** — the author asked for it by name, which overrides the earlier *"open by
design"* note below, and closing cost nothing because its acceptance criteria are met and all ten of its
§8 artifacts now exist as files. **#421 closed on author direction** after items 3 and 4 landed (#429 and
`docs/ATTRIBUTION_POLICY.md`) — but it closed **carrying** its items 1 and 2 rather than resolving them,
because those are decisions. The licence pair is row **D10** and the commercial model is row **D16**, both
written out with the mechanical enactment steps in `ISSUE_421_ENACTMENT_AND_COMMERCIAL_MODEL.md`. **The
release gate still refuses a clean public release on `licence-decision-open`: closing the tracking issue
does not unblock it, and the board says so.**

**Eighth update (2026-10-15):** issue **#447**'s two standing author decisions are carried below as rows
**D25** and **D26**. They are the only rows this update adds and nothing already on the board changed:
#447 stays open on them together with the author's reserved prologue text, and
`ISSUE_447_ACCEPTANCE.md` states that remainder as a remainder rather than labelling it met.

**Ninth update (2026-10-16):** issue **#506**'s Phase 1 lands the shared strategic-project engine and
its research instance, and that makes two conventions and one open question board rows: **D27** (the
dice band and the work scale — four `TUNING_` numbers, and whether a Fate tie should ever grant
progress) and **D28** (whether a matched domain TAG or a named ideological prohibition should ever
*do* anything, rather than being reported). Nothing already on the board changed and no row is closed
by them: both rows describe code that runs today with the numbers it has and no more. The design
record is `strategy_game/docs/RESEARCH_PROJECTS.md`; the contracts are
`strategy_game/tests/test_research_projects.py`.

**Tenth update (2026-10-19):** issue **#516** asks the author to document and sign off a single core
ruleset. Nine rows are added — **D29–D37** — because the issue's decision surface is genuinely wider
than the four rows already on the board (**D22** the strategic roster, **D23** allocation and
advancement, **D27** the project dice band, **D28** whether a domain TAG may *do* anything). The
record is [`ISSUE_516_CORE_RULESET_DECISION_SUPPORT.md`](ISSUE_516_CORE_RULESET_DECISION_SUPPORT.md):
a comparison, a seven-game reference matrix, four resolution options, three character-model
architectures, three tactical options, and five worked examples — **all proposals**, and it writes no
rule into either rulebook. Nothing already on the board changed, and no row closes: **D37 is the
sign-off itself**, and until it is answered the ruleset described there is not canonical.

**#347** closed on the defer-and-close rule — six of its ten criteria are met with measured evidence
(including the ten-kind example set and the data-only authoring contract), and the four that depend on
choosing a renderer are carried as row D13. **#346** closed on the defer-and-close rule — the card layer
it needed was verified to exist (`faction_cards.py`, four card types, 27 tests OK), and its two
rule-dependent criteria are stated as **deferred** in `ISSUE_346_ACCEPTANCE.md` and carried as row D11.
Since the first queue, **#325**, **#345**, **#346** and **#282** closed once, **#322** closed on the
defer-and-close rule the author authorised on 2026-10-13, and **#323** was closed on that same rule,
**reopened** when its record presented criterion 2 (*"unavailable leaders cannot execute one"*) as met while
the code only **reported** it, and **re-closed on 2026-10-14** once the refusal became real in
`structural_problems()` and the record was corrected to say so: on that row the deferral had not been
stated as a deferral, which is the rule's own condition. **D3 carries #323's decisions** — the §4 row
*timings and magnitudes* now gate no criterion of #323 — and nothing was approved or changed in substance.

## Live rows

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D3 | **#323's decisions**: the committed-resource ceiling (one shift, spent either way); **+1** as the portfolio-bonus ceiling; one turn without the bonus on reassignment; the two affected mission kinds (negotiate difficulty-down / organise difficulty-up); deck size six-to-eight; no event ends in dialogue alone. Full text: `ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md`; per-criterion labels: `ISSUE_323_ACCEPTANCE.md`. Separately, §4's *row timings and magnitudes* (injury recovery, the compromised reduction, exposure risk) stay unauthored (`status_consequence_rows`), but §4's *mission column* is enforced in `structural_problems`, so they gate no criterion of #323. | #323's deferred criteria (3's amplification, 4's magnitude, 6, 7) | *accept* / *amend* each |
| D4 | The eleven global parties' formal names and colloquial labels; self-name versus hostile exonym. | #328's checkpoint 1 | *ratify as drafted* / *rename* |
| D5 | MJ-12 continuity: when it starts, what it controls, why it qualifies as a Breakaway Civilization; human-led or not; internal factions; relation to disclosure, the Confederacy, Orion, the Swarm. | #328's checkpoints 2–3 | *decide* |
| D6 | The ASI swarm's origin, objectives and autonomy; whether any human network is voluntary or coerced. | #328's checkpoint 4 | *decide* |
| D7 | Confirm the three Ukweli party ↔ global-current affinities as **starting tendencies**, not fixed memberships. | #328's checkpoint 5 | *yes* / *no* |
| D8 | Reconcile the legacy UN party records with the established UN world government and eleven Parties. | #328's checkpoint 6 | *decide* |
| D9 | **The register ruling:** which of the three readings is canonical — A (same register, coarser: 7 → 11), B (two orthogonal registers), C (competing rosters) — and whether the four unpaired Parties belong in the paradigm stratum at all. The four are MJ-12 / Continuity Directorate, the rogue ASI swarm / AIC, the Earth Restoration Alliance, and the Human Survival and Defence Coalition. | #328's central open question (`roster_closed_at_seven`), #338's roster work | *A* / *B* / *C* |
| D10 | **Licence selection** — the pair: 1a software (MIT / Apache-2.0 / GPL) and 1b content (CC BY-SA 4.0 recommended, CC BY 4.0 alternative). Was tracked by #421; **#421 is now closed and this queue carries it**, because a tracking issue cannot track a decision the author has not made. Agents are forbidden to choose a licence or create `LICENSE` / `NOTICE`, and a test asserts those files do not exist. Enactment is mechanical and is written out in `ISSUE_421_ENACTMENT_AND_COMMERCIAL_MODEL.md` §2 — creating the files, setting `author_decision_open` to false (that single field clears the release gate), and three named tests changing. | the release gate, D14, S1 | *pick 1a + 1b* |
| D16 | **The commercial model**: free / paid / paid-with-free-earlier-builds. Smaller than it looks, and safely deferrable longer than D10 — **price does not change what may legally be in the build**; the licence pair and the NC-SA exclusion do. Constraints that bind: no required service or paid provider, and `LICENSE`/`NOTICE` must ship inside the artifact. §8 item 6 and `ISSUE_421_ENACTMENT_AND_COMMERCIAL_MODEL.md` §3. | S1 publishing work | *decide* |
| D11 | **The rules gate**, one row because it is one decision: #323's decisions (D3) plus #346's two rule-dependent criteria — abstract mission resolution, and first-turn resource constraints. `RULEBOOK.md` still says NO RULES APPROVED. | per-stage PRs for both issues | *approve* / *refuse* |
| D13 | **The renderer decision** — which renderer becomes the playable UI. `docs/INTERFACE_SPIKE.md` records the evaluation and recommends text-first with the browser next over the same payload, keeping Godot as a view; the pick is the author's. | #347's playable UI, Helsinki opening and playtest (criteria 5, 6, 8, 10) | *text* / *browser* / *Godot* |
| D14 | **Distribution for the indie release**: channels (itch.io / Steam / self-hosted), price including free, storefront requirements, packaging and platform support. §8 item 6. The evaluation lives in `ISSUE_309_DISTRIBUTION_AND_UGC_GOVERNANCE.md`; the choice is the author's. | S1 publishing work | *pick channels + price* |
| D15 | **#309's §8 item 1 verification**: the vertical-slice pitch in `ISSUE_309_VERTICAL_SLICE_AND_EVENT_FLOW.md` is a pitch, not an approval. Rule on whether the four-press turn it describes is the shape S1-a should build toward. | S1-a's interface work | *yes* / *amend* |
| D12 | **The #346 canon set**: the cultural-axis choice; NHI contact policy apart from named diplomacy; EFTZ structures; the ARV-by-1981 timeline; two Soviet-program successor factions; breakaway civilizations; the fourfold evidence categories; the Law-of-One political reading and its Confederate Social Memory Complex; Soviet–Confederacy and US–Orion relations; and the Cosmist International set (founder identity, manifesto, Helsinki status, introductory scene). Full list: `ISSUE_346_ACCEPTANCE.md`. | the authored campaign content | *decide in any order* |
| D17 | **The four 2045 UN parties** (Tomi, 2026-10-14/#470), carried because the records leave each part visibly unresolved rather than answering it. (a) **Succession**: is the Unity, Security and Stability Party a *rename*, a *recharacterisation*, an *evolution* or a *replacement* of the United Earth Social Democratic Party — whose legacy record is centre-left while the successor reads authoritarian-conservative — and is The Noösphere The Multitude renamed and re-topped by the reformed CCP, or a successor coalition? Recorded in `data/world/un_parties.yaml` as `position_status: pending_author_review` and `legacy_mapping_status`; the earlier revision that recorded `position: governing_continuity` answered (a) silently and has been reverted to the legacy value. (b) **Register**: do the four sit in the paradigm register or a register of their own (this is D9's question applied to these four)? They are held *beside* the seven in `strategy_game/data/global_factions.json` (`un_parliamentary_parties`), not inside `factions`, so that no count is asserted. (c) **Magnitudes**: which of section 7's six quantities each party holds is recorded qualitatively; no starting value, weight or move is set, and no scalar "influence" exists. | #470's roster and #469's readings surface; D9 | (a) *rename* / *recharacterise* / *evolve* / *replace*; (b) *same register* / *separate register*; (c) *set magnitudes later* |
| D18 | **The roster's scope, and the 2026 baseline's missing half.** Complete roster at start or the starting four (`un_parties.yaml` allows future parties); whether the NHI polities (UCCC, Greater Orion Arm Co-Prosperity Sphere) belong on this roster or stay external powers; and whether the previously proposed non-UN projects — decolonial digital sovereignty, the sovereign-citizen network, post-growth, human-security institutions — are currents inside the four, non-UN actors, or dropped. **The evidence:** the 2026 baseline in `REALITY_TUNNELS.md` §3 is US and European only; the non-Western pass in `ISSUE_470_FACTION_DEPTH_AND_THE_2026_GAP.md` §3 shows the AU's data-sovereignty programme (*"governance without leverage"*, nonbinding strategy) and the Indigenous anti-data-centre movement (100+ tracked projects, "data colonialism") are **not well represented by any of the four as written**. Accept that bias, or address it? | #470's roster boundary; #346; the 2026 baseline | *starting four* / *complete* ; *on roster* / *external* ; *currents* / *non-UN actors* / *dropped* ; *accept the bias* / *address it* |
| D19 | **The True Humans Party's record**: how the issue's style references (Unabomber, Linkola, Yudkowsky) are filed — §6.1 attribution row, `references` entry or `tone` note — and whether the faction's exterminationist plank, already carried with the not-endorsed marking in the runtime data, stays its **extremist wing / end state** or the legacy record's *"aggressive defence… militarism"* is hardened to match. `RULEBOOK.md`'s tone rule holds either way: real infiltration does not make every conspiracy theory true, and witch hunts coexist with genuine threat. | the roster's tone; #470's extremism criterion | *file as §6.1 attributions* ; *keep as the extreme wing* / *harden the legacy line* |
| D20 | **#469's remaining approvals**: which signifiers are canonical per faction (the record offers one reading — *humanity* tendentially empty in the True Humans Party only, since only there is it articulated to a wide chain of demands rather than merely vague); whether the narrative-style guidance is adopted as written; and how literally the Reality Tunnel portraits become shipped voice. | #469's remaining criteria | *accept* / *amend* each |
| D21 | **Do the four factions' missing #470 criteria enter the data?** The merged record carries positions, tunnels, stances, fault lines, currents and endgames — but **not** 2026 ancestry, #346 TAG sets, allies/antagonists or national/UN strategy, all of which #470's acceptance criteria name. `ISSUE_470_FACTION_DEPTH_AND_THE_2026_GAP.md` §1–§2 supplies them, drawn only from existing TAGs. Adopt into `un_parties.yaml` / `un_political_discourse.json`, keep as a design record, or amend? | #470's remaining criteria; #346 | *adopt into the data* / *keep as a record* / *amend* |
| D22 | **The strategic agent skill roster (#482).** Issue #482 **approves** the RPG foundation and exactly six individual skills (COG, INT, REF, SAV, SOM, WIL) — that half is not open. It does **not** approve a strategic roster: `strategy_game/data/strategic_skills.json` proposes seven (`statecraft`, `fieldcraft`, `inquiry`, `stewardship`, `command`, `science`, `security`), the mission kinds each checks, and an 18-row mapping from the verified Fate Core skill list, all with `status: PROPOSAL`. The five-seat structure (one leader + four agents, one action per character per turn) is stated by #482 and implemented; mission difficulty, cost, cadence and effects stay with D3/D11. That mapping is expressed against Fate Core's list, and the work's own list has since been **verified** (`transhumanitys_fate_mapping`): 24 names, matching the work's own skill-list pages as reproduced in three independent copies, with the once-unresolved count explained as the work's 25 *starting skill points* rather than a skill count. That narrows this row: the finding is that the work's list is almost entirely scene-shaped and consolidates into the six individual skills, so the seven cannot be derived from it. What stays open is the ruling itself — **accept / amend / replace** — not a missing source. | #482's remaining criteria; Gate C | *accept* / *amend* / *replace* (the TF-list check is done) |

| D23 | **The six individual skills' starting allocation and advancement (#482).** Fate Core's Great pyramid rates ten distinct skills and cannot be copied literally to the six-skill roster. `RULEBOOK.md` §3 records allocation as unspecified, with no distribution invented. **The adopted baseline's own method is now recorded** (verified from the work's front matter): **25 starting skill points under a Great (+4) cap**, with Fate Core's **Skill Columns** rule as its stated alternative to the pyramid - a budget written for a 24-skill list, so applying it to six, literally or scaled, is a ruling either way. The computed consequences of the plausible six-slot distributions are on #482. | #482 allocation and advancement; `RULEBOOK.md` §3 | *pick a six-skill distribution* / *leave to the GM* / *amend* |
| D24 | **Step 1 of #468: which 2045 opening snapshot is the default?** Issue #468's own step-1 deliverable asks for 2-3 short post-crisis openings with one explicitly recommended, and for the choice to wait on Tomi before anything is treated as canon. `docs/design/ISSUE_468_STEP1_OPENING_SNAPSHOTS.md` supplies three. **A "The Quarantine Belt"**: a managed emergency - a cordon that works, and must keep being renewed. **B "The Empty Seat"**: the mandate that would settle the post-crisis order was never delivered, so competition is rational and total war is not; recommended, because it needs no new canon, fits one city, and makes the signifier model load-bearing from turn one. **C "The Recovery Boom"**: reconstruction that worked, financed by the Confederacy, with a lien on it. All three obey the dated convention (2045; unordered `20XX` background; no completed Fall), keep the four playable factions and the three non-playable NHI powers, and propose one city and its region as the smallest playable map. Steps 2 and 3 of #468 wait on this row. | #468 step 1; #470's roster; #479's mechanics | *A* / *B* / *C*, or *amend* |
| D25 | **#447: which rulebook owns the Tommy Pilgrim introduction and the Event Cards section?** The author direction says *"the rulebook"* and there are two candidates. Both currently sit in the **legacy canonical `RULEBOOK.md`** — **§1.4** *"How this book came to exist: Tommy Pilgrim, 1974"*, placed at the end of the introduction so it frames the scenario and displaces nothing, and **§2.2** *"Event cards: how this history reaches the table"* — because that is the file whose scenario the introduction precedes and whose §35 source map the author asked to extend. The **crossover** rulebook is the other candidate, and the arguments point there: the eleven authored `event_card_seeds` the §2.2 text consumes live in `strategy_game/data/global_factions.json`, `docs/design/NOOPUNK_GLOBAL.md`'s turn table already has a *"Draw/resolve 1 event card"* row, Layer II reserves systemic events, and #389 gave the crossover an approved Layer I. Moving the two sections is a move plus a regeneration of `rulebook/parts/` and of the split manifest. Note this is also the one half of #447's Event Cards criterion that no artefact answers: the sequencing (*default timeline first, variability later*) and the reuse obligation are recorded; the **ownership** is not. | #447's Event Cards criterion (its *"names which rulebook owns it"* half); the rulebook structure | *name the rulebook* |
| D26 | **#447: does *The Iron Dream* (Norman Spinrad, 1972) join the locked in-universe visual/literary hierarchy?** It is already recorded as an **influence**: `RULEBOOK.md` **§35.3** carries it with its real-versus-fictional authorship stated (real author: Spinrad; the inner novel's fictional author: an alternate-history Adolf Hitler who emigrated in 1919), and the specification's **§3.4** records the three devices borrowed from it. It is **not** in the locked hierarchy (PKD / Wilson / Le Guin), because that section's rule is to include only the named reference set and no document adds a reference to itself. Its **1972** date permits promotion — it precedes Pilgrim's 1974 download, unlike *Cosmic Trigger* (1977) and *The Shockwave Rider* (1975) — which would make it a fourth *in-universe* influence, i.e. something Pilgrim had read before the download. *Smallest useful answer:* accept as a fourth slot, or leave it out-of-universe where the author named it. | #447's *Iron Dream* placement; the presentation layer's hierarchy in spec §2.2 | *accept as a fourth slot* / *stay out-of-universe* |
| D27 | **The strategic-project conventions of #506 Phase 1: the dice band and the work scale.** The engine needs three numbers and an author's ruling on a fourth case. `strategy_game/projects.py` marks them all `TUNING_`: the segments a clock starts from (**8**), the segments each step of check difficulty adds (**2**), and the ceiling (**20**) — so `clock_for_difficulty(2)` is issue #506's own worked example of **12 work units** (3/12, then 6/12). The fourth is the **success with style** bonus (**1 segment**), deliberately smaller than the committed throughput of the worked examples, because the issue requires the lead's check to allow only "limited quality/special-success effects" and never to replace institutional capacity. Related and unanswered: a Fate **tie** is "succeed at a minor cost", so the engine grants **no** segments and reports the tie — a tie rule may be wanted, and none is approved. The design record is `strategy_game/docs/RESEARCH_PROJECTS.md` §5; the contracts are in `strategy_game/tests/test_research_projects.py`. | the dice bands, capacity normalisation and duration balance #506 leaves open; the numbers any playtest of the Phase 1 slice is read against | *accept as tuned* / *amend the four numbers* / *rule on ties* |
| D28 | **What a domain TAG and an ideological prohibition should *do*.** Two facts about a programme are recorded and deliberately inert today. (a) **Domain TAGs**: #506 asks the SCIENCE check to "adapt to existing NoöPunk character sheet: SCIENCE plus relevant domain TAGs such as Forensics, Parapsychology, Engineering". The engine reports `domain_tags_matched` / `domain_tags_missing` on every turn and no tag moves the check, the throughput or the difficulty — because `rpg.skills.specialist_supplement` already rules that a tag which moved a roll would be an unapproved mechanic, and because the alternative is a bonus stacking with the roster's own ratings. (b) **Prohibitions**: a `TechNode` can declare `prohibited_by` belief labels, and `research.prohibitions_for` reports those the faction's own members hold at the moment it completes the programme — a Butlerian faction is told its new understanding contradicts its doctrine. Nothing is blocked: the programme runs and completes anyway. So the row is whether either should ever *do* something — a TAG that shifts the check, a matched domain that shifts the throughput, a prohibition that hard-gates a project or costs something. Both halves share one ruling because both are "a recorded fact becomes a mechanic". | the crossover's science-vs-doctrine texture; any use of domain TAGs in play; the Branching-research criterion of #506 that asks research to reflect ideological prohibitions | *leave both as reports* / *rule each into a mechanic* |
| D29 | **#516's scope: which game does the ruleset govern?** The issue names "the existing FIT/REF/INT/SOC/PSY/CYB" — the **legacy** game's six 1–10 STATs — while most mechanics it cites belong to the **crossover**, whose six Fate-rated skills #482 already approved. `AGENTS.md` §0 forbids collapsing the two games, and the legacy `RULEBOOK.md` is canonical and author-owned. Three readings: (a) **crossover only** — the legacy `STAT + Skill + 1d10` kernel is untouched and #516's mention of the six STATs is a vocabulary reference; (b) **both games** — unify on one kernel, which means rewriting the legacy rulebook and retiring the 1d10 check; (c) **two games, one conversion appendix** — leave both kernels and publish a STAT↔skill crosswalk. **Trade-off:** (a) is cheapest and changes nothing already approved, but leaves #516's own wording only half-answered. (b) is the most coherent product and the most expensive reversal, and it would make 40 legacy skills and every legacy test historical. (c) buys legibility for a dual-kernel repository at the price of a third document. **Recommendation: (a)**, recorded in the record's §0.1. | every other row below; the whole record's scope | *crossover only* / *both* / *conversion appendix* |
| D30 | **The trait architecture: six skills, or six attributes *and* six skills?** #482 approved **six individually rated Fate skills** (COG, INT, REF, SAV, SOM, WIL) and the sheet is built on them. #255 required "exactly six independently rated Attributes FIT/REF/INT/SOC/PSY/CYB, keep attributes distinct from skills" — written for the legacy game. #280 proposed the opposite of a skill list: a stat tree with universal TAGs. Three options: **A** six skills only, with FIT…CYB kept as the **conversion vocabulary** for NPC statlines and legacy cross-reference; **B** six attributes + six skills (12 rated traits, one more addition per roll, restores "strong but untrained" as a mechanic); **C** #280's stat tree, tags instead of skills. **Trade-off:** A is the smallest sheet and the cheapest implementation, and it loses the attribute/skill distinction that lets a sheet say "strong but untrained" — under A that becomes an aspect. B keeps the distinction and costs six numbers plus a second scale to keep synchronised. C fits #280 and would remove the approved six skills. **Recommendation: A with C's tag discipline** (permission tags, competence tags and conditions kept visibly distinct). This is the most consequential row on the board for #516 because every other mechanic reads the sheet. | #516's character model; the sheet; NPC statlines; every worked example; any future legacy↔crossover conversion | *A* / *B* / *C* |
| D31 | **The unified core resolution mechanic, and its three sub-choices.** #516 asks for **one** mechanic for social, investigative, physical, cyber and PSI actions. The 4dF kernel is already approved (#389) and implemented, so two of the four options carry the cost of re-opening it. Options: **A** one kernel — 4dF + skill, four outcomes, shapes chosen before the dice (overcome / create an advantage / contest / conflict / challenge), recommended; **B** dual kernel (4dF for scenes, 2d6 bands for "moves"); **C** 4dF for scenes plus a separate AP tactical engine; **D** replace the kernel (2d6 or d10). Sub-choices inside A: **contest length** (first to three round-wins, recommended, or two, or a fixed number of exchanges) and **whether difficulty is stated openly** (recommended for accessibility and for a text UI) or hidden (Fate's default, more tension). **Trade-off:** A buys one arithmetic and one currency at the cost of granularity — four informative steps cannot distinguish "hard" from "very hard", so genuinely hard undertakings must become *more than one roll* (a contest, a conflict, a challenge) rather than a bigger number; `ISSUE_461_CONSENSUS_PROPOSAL.md` §2 proved that arithmetic and §5 Fork 4 named the fix. B buys PbtA texture and costs a second dice convention at one table. C is the "two engines" #516 forbids. D invalidates every landed test and `RULEBOOK.md` §5. **Recommendation: A, contest to three, open difficulty.** Full option table: record §4.3–§4.7. | every action type; all worked examples; the rulebook's §5 | *A* (and its two sub-choices) / *B* / *C* / *D* |
| D32 | **Is there a distinct "success at a cost" band?** Fate has four outcomes and puts "succeed at a minor cost" on the **tie**; PbtA puts its most interesting result at 7–9, between failure and clean success. Under 4dF most rolls land near the middle, so the tie carries a lot of weight. Options: (a) **four bands, cost on the tie** (recommended) — the legacy prototype modules already share one margin→band function (`social.band_for_margin is physical_combat.band_for_margin`), so this keeps physical, social and cyber on one band vocabulary; (b) **five bands**, inserting success-at-cost between tie and success; (c) cost is always **player-chosen**, with no narrator default. **Trade-off:** (a) keeps one band table across physical, social and cyber and makes the tie the dramatic moment; it also means a table that finds ties dull has no partial-success texture at all. (b) is the most PbtA-shaped and needs the band function changed in three modules plus the rulebook, and it makes every roll a negotiation. (c) maximises agency and puts the burden on players who freeze. **Recommendation: (a)**, with the cost menu in record §4.6 as narrator guidance. | the outcome table; #219/#220's shared band function; the worked examples | *four bands* / *five bands* / *player-chosen* |
| D33 | **Is "simplified science" a seventh individual skill?** #516 asks for "skills (including simplified science)" and #506 already calls a strategic `SCIENCE` check — which is the *strategic* roster's `science` (D22), not an individual skill. Three options: (a) **no Science skill**: method is `COG`, a discipline is a `competence` tag (`COG: biochemistry`), a signature technique is a stunt priced in refresh — recommended, and it is what `RULEBOOK.md` §3.2 already says; (b) **a seventh individual skill `Science`**, so a specialist is visibly rated and no table argument is needed about whether a biologist can do biochemistry; (c) **split COG** into `Science` and `Analysis`. **Trade-off:** (a) holds the sheet at six and keeps the three-place rule (skill / competence tag / stunt), at the cost of a specialist's competence being invisible in the numbers — a player who wants "world-class chemist" on the sheet gets a tag and a stunt, not a +4. (b) is one number for one real argument, and it opens the door the record warns about: hacking next, then PSI, then the 18-skill list rebuilt by accretion. (c) is (b) with more surgery. **Note the adjacency to D28**: D28 asks whether a *matched tag* may move a check; this row asks whether the specialism is a rating at all. Answering (a) makes D28 more pressing, not less. | #516's character model; #506's SCIENCE check naming; the sheet | *no Science skill* / *seventh skill* / *split COG* |
| D34 | **Tactical combat: action economy, and whether a fight is ever compulsory.** #516 wants combat "fast, dangerous", for small squads, with action economy, cover, positioning and injury — and **not required for every quest**. #515 needs the same four agents on a tile map. Options: **T1 zone conflict** — 3–6 zones, **one action + one reaction** per character per turn, cover as an *aspect* (invokable) or a *gate* (line of fire blocked), never a modifier; recommended. **T2 AP skirmish** — #225's 3 AP, movement and attacks costing AP. **T3 hybrid** — 2 AP (one move, one act). Plus the separate question: **is combat ever mandatory** (recommended: never — every mission must be completable without a fight, and a fight must be losable), and **is "taken out" death** (recommended: no — the winner narrates, and death is a table choice). **Trade-off:** T1 is fast and needs no second engine, and it collapses move-and-shoot into one decision, so a tactical player may find the map decorative. T2 is the most X-COM-like and adds a second action economy beside #461's one-action-per-turn, which is the "competing combat game" #516 forbids. T3 sits between and still doubles the economy. **Recommendation: T1, combat never mandatory, taken-out ≠ dead.** Record §7.2–§7.4. | #515's combat milestone; #516's combat deliverable; #219; how "dangerous" is calibrated | *T1* / *T2* / *T3* (+ the two yes/no questions) |
| D35 | **Do mission consequences persist into the strategic layer — and who writes them?** #516 asks for injury and for outcomes that propagate; #502 leaves `MissionOutcome.effects` deliberately empty (its §5), and #515 wants wounds to feed faction strategy. Today a Fate consequence ends with the scene, `rpg/boundary.py` refuses the join to `WorldState` on purpose, and `MissionDeclaration.outcome` is documented as staying empty. Options: (a) **consequences may leave a mission as named injuries** with a *recovery condition* rather than a number ("until treated", "three turns", "until she stops using the arm"), and the narrator writes effects from a **closed menu** (record §9.3: intel, injury, exposure, access, relationship, material, position) — recommended; (b) consequences stay in the scene and the strategic layer reads nothing; (c) a **fixed effect vocabulary** with magnitudes, which is #502's wiring task and would need the numbers D3/D11/D27 do not yet have. **Trade-off:** (a) makes X-COM's "your best agent is in the infirmary" possible with no hit-point model and no new number, at the cost of the strategic layer reading prose it must be told how to interpret. (b) is the status quo and makes missions inconsequential. (c) is the most machine-actionable and is blocked on numbers that are not approved. **Note:** this is adjacent to D3's `status_consequence_rows` and #323's timings, but it is not the same question — that one is about council status, this one is about the RPG→world write path. | #515's outcome wiring; #502's `MissionOutcome.effects`; #516's propagation deliverable | *named injuries + closed menu* / *scene-only* / *numbered vocabulary* |
| D36 | **Cyber and Astral harm: a third stress track, and a cyberware capacity limit?** The sheet has **physical** and **mental** stress. A failed intrusion or a PSI contest currently lands on mental stress, and the exposure clock models the system's counter-pressure. Options for the track: (a) **no third track** (recommended) — mental stress plus the exposure clock already carry it; (b) an **`Interface`/`Signal` track** so a hack can damage the deck without hurting the mind; (c) a track **per device**, which is simulationist bookkeeping the table will not maintain. Options for cyberware: (i) **no capacity number** (recommended) — the implant is a permission plus a tag; (ii) **slots** ("three implanted things, and this is the fourth"); (iii) a **strain number** — rejected in the record as C4. **Trade-off:** (a)+(i) is the fewest numbers and keeps "the mind pays for the mind's work"; it also means a character's deck never takes damage, which some tables will find thin. (b) gives cyber conflict its own attrition and adds a third track to every sheet for a subsystem only some characters use. (ii) is one honest limit with no arithmetic, and it is the cheapest way to make cyberware a choice rather than an accumulation. | #516's PSI/cyber deliverable; hacking and PSI scenes; the sheet | *track: none / Interface / per-device* ; *capacity: none / slots / strain* |
| D37 | **The #516 sign-off itself.** The issue's "Done when" is that Tomi has documented a single cohesive ruleset, demonstrated it in narrative **and** tactical examples, tested its playability and **explicitly signed off**. The record supplies the comparison, the options and five worked examples; it supplies neither the playtest nor the sign-off, and it says so. Options: (a) **accept as the basis for a playtest draft** — the nine rows above answered *or* left as they are, and the record becomes the draft's spine; (b) **amend** — answer D29–D36 with changes and the record is revised before any playtest; (c) **reject** — the comparison stands as research and the core stays open. A separate sub-question that only the author can answer: **does acceptance make the ruleset canonical in `strategy_game/RULEBOOK.md`**, and if so by whose hand — the author's edit, or an agent writing the approved sections afterwards? Nothing in the repository should be read as that sign-off until it exists in his own words. | #516's closure; the playtest; anything written into either rulebook | *accept as draft* / *amend* / *reject* ; and *who writes the rulebook* |
| D38 | **#515's tactical-map renderer — and with it the tile interchange.** #515's first milestone is a spike that chooses **renderer, grid/tile format and mission-data schema**. Two of the three landed as engineering and change nothing about the rules: the renderer-independent mission layer (`strategy_game/tactical/`, 95 tests) and the tile format (ASCII `.`/`#`/`+` rows inside a JSON mission document). What is the author's: **what draws the board.** `strategy_game/docs/TACTICAL_MAP_SPIKE.md` §8 recommends **Python/Pygame rendering the in-process rules, with Tiled as the map editor when authored maps are needed**, keeping **Godot 4's tilemap as a documented view** over the same Python session. The reason is T3 (`INTERFACE_SPIKE.md`/#309: no rule written twice) and H (headless `unittest` in the CI this repository already runs): only the in-process option satisfies both *structurally*, with no bridge at which a rule can be re-derived in a second language. The stated trade: give up Godot's tile editor, `AStarGrid2D` and self-contained exports, and accept a small renderer you own plus per-platform Python packaging (PyInstaller/Nuitka). **Godot with the rules in GDScript is disqualified**, not merely expensive — `AGENTS.md` §3/§13 and #515's own *"avoid inventing a second full ruleset"*. **This is not D13**: D13 picks the playable UI for #347 (text/browser/Godot), D38 picks the tactical map's renderer, and the spike keeps both answers open. | nothing yet, and deliberately so — #515's rendering milestones (click-to-move UI, combat, Physical/Cyber/Astral cues) and the tactical half of the vertical slice; #515 stays open on its later milestones whether or not this row is answered | *Pygame + Tiled* / *Godot 4 tilemap as a view* / *amend* |
| D39 | **#506 Phase 2's magnitudes: what a capacity investment buys, how far it can go, how hard sabotage lands — and whether supporting personnel should bound a project.** Issue #532's buildable core adds the organisation around the project engine (concurrent projects, assignment, facilities, recruitment, bottlenecks, sabotage, the mission↔research loop) and needs four numbers/cases that are the author's, all marked `TUNING_` and all **derived from an existing quantity** so no convention is mistaken for canon. (a) **An investment raises one resource kind by 1 unit**, derived from Phase 1's three-unit throughput (an investment is a third of a turn's work). (b) **The ceiling is 4 units added per kind**, derived from `AGENT_CAPACITY` — the approved one-leader-plus-four-agents roster — so the faction's own seats bound its growth. (c) **A sabotage set-back adds 1 segment to the clock's total work**, derived from `TUNING_STYLE_BONUS_SEGMENTS`; how many consequences land reuses the approved Fate ladder (none on failure/tie, one on success, two on success with style) and defines no new band. (d) **Assigned support personnel are reported, never rated**: a supporter moves neither the check nor the throughput, and the availability rule treats Fate's "taken out" and an unrecovered consequence as making a lead unavailable — no severity threshold exists. **Related and unanswered:** should a supporter ever *bound* a project's usable throughput (the X-COM "you have the lab but not the staff" case)? That is the one place where the honest reading might need a mechanic rather than a report. **None of this touches D27** (the Phase-1 dice band and work scale) or **D28** (what a domain TAG or an ideological prohibition should do); both stay open and unchanged. The record is `strategy_game/docs/STRATEGIC_OPERATIONS_PHASE2.md` §8; the contracts are `strategy_game/tests/test_operations_phase2.py`. | any playtest of the Phase-2 organisation slice; how expensive growth is; how punishing a rival's disruption is; whether personnel ever becomes a constraint with teeth | *accept as tuned* / *amend the four numbers* / *rule on supporting personnel* |

| D40 | **The chassis ruling behind #564.** #564 asks for NoöPunk's playable rules to be converted onto an adapted **CWN** chassis with selective **SWN**. That collides with three settled facts: the crossover's **Fate Core `4dF`** kernel is *approved and implemented* (#389, `strategy_game/RULEBOOK.md:36` "the chassis … Implemented"), six individual Fate-rated skills are approved (#482), and a prior author directive recorded in #197 says *"Do **not** import Shadowrun/Eclipse Phase/CWN mechanics wholesale"* (`ISSUE_197_SCOPE_2026-10-10.md:30`). CWN's present standing is a **conversion source** (`RPG_CONVERSION_REFERENCE.md:209`–`:247`), not a chassis. Two further premises in the issue do not match the repository: the sixth attribute is **SOC**, not `CHA` (the issue names `CHA`, which is CWN's own attribute), and **no 3d6 core check exists** — `grep "3d6" RULEBOOK.md` returns nothing; the legacy kernel is `1d10` and the crossover's is `4dF`. The question, therefore: **is the kernel staying on `4dF` with CWN/SWN entering as adjudication procedures (Shock, Trauma, access prerequisites, saves, morale), or is it being replaced by CWN's `2d6` — which would retire an approved kernel and its tests?** This is larger than D29 (which game) and D31 (which mechanic), because it decides whether an approved chassis is re-opened. A secondary answer is needed inside the same row: does *"the present 3d6 core-check model"* mean **attribute generation**, or a **third kernel**? Full analysis, the 24-row disposition matrix and the proposed sub-issue breakdown: `ISSUE_564_CWN_SWN_CHASSIS_MATRIX.md`. | every implementation step of #564 (§4 items 4–9, 12, 15, 19 and the vertical slice); `strategy_game/RULEBOOK.md`'s baseline line; the Fate kernel's tests | *stay on 4dF + CWN as procedures* / *stay on **1d10** (layer A) + CWN as procedures* / *move to 2d6* / *two kernels, one appendix* ; and *3d6 = generation* / *3d6 = third kernel* |

| D41 | **The ubiquitous-network exposure economy (#572).** `src/rules/ubiquitous_network.py` makes the setting's ubiquity cost *exposure* rather than concealment: 1 per attempt, +1 per 2 points of margin, +1 again on a failure, Cover buys back 2, and the alert bands sit at 2 / 5 / 9 / beyond. The four numbers and the band edges are the author's; the module is `IS_CANONICAL = False` and every one is a `TUNING_` constant. **Why it needs a ruling rather than a default:** these are the numbers that decide whether the network is a background pressure or the scene's antagonist, and the canon chapter (§22.6.4) says an encounter must be "a scene with a price" without defining the price. The reach gate itself needs no ruling — it is §22.5.2 transcribed and exhaustively tested. | any playtest of the intrusion procedure; how loud a failed attempt is; whether Cover is worth an AP | *accept as tuned* / *amend the four numbers* / *replace exposure with a different pressure* |
| D42 | **Natural PSI's Effort curve and training thresholds (#572).** `src/rules/natural_psi.py` gives a natural, learnable capacity an arithmetic: capacity `1 + PSY//2` capped at 5; **20 h** of practice to use a discipline, **120 h** to master it (unsupervised hours count half); a failure or a tie costs 1 psyche load; recovery 1 per scene; consensus ±1 per witness capped at ±2; mastery removes one point of failure cost, never adds a bonus. This row also carries the **`AGENTS.md` §4 reservation**: psionic mechanics were reserved until the author defined them, and the 2026-10-25 direction ("PSI as in SWN rules but learnable natural human ability") is the request that opens it — the numbers are still his. | any playtest of the PSI procedure; whether PSI stays capability-only or gains this cost model | *accept as tuned* / *amend the curve and thresholds* / *keep PSI capability-only* |

## Rows deferred on closure (kept so the closures are honest)

- **#322's authorial remainder** — the **twelve named people** (the structure is complete: three
  factions × four seats × four portfolios; `ukweli_leaders.json` still carries 14 *requires author
  specification* fields, and the executed history names a leader as `CPU Chair`), the M4
  organisational-evolution rules, the research/adoption mechanic, and the rival-AI / win-loss criteria.
  See `ISSUE_322_ACCEPTANCE.md`.
- **#325's ratification rows** — the four conflicts as options, and Freedom Colony's legal autonomy.
- **#328's checkpoint 7** — documenting separate organization / party / ideological-current /
  nonhuman-actor records: a post-approval task that cannot precede D4–D9.

**Eleventh update (2026-10-19):** issue **#515**'s first milestone lands a renderer-independent mission
layer, its tile format and its mission-data schema (`strategy_game/tactical/`, 95 new tests, design
record `strategy_game/docs/TACTICAL_MAP_SPIKE.md`), which makes exactly one new question a board row:
**D38** — what draws the tactical board. The spike recommends Python/Pygame rendering the in-process
rules with Tiled as the map editor, and keeps Godot 4's tilemap as a documented *view*; the pick is the
author's. **D38 is not D13**: D13 decides the playable UI for #347 (text/browser/Godot), D38 decides
the tactical map's renderer, and neither answer is pre-empted by the other. Nothing already on the
board changed, and #515 stays open on its later milestones whether or not the row is answered.

**Twelfth update (2026-10-22):** issue **#532**'s buildable core lands #506 **Phase 2** — the
organisation around the project engine: concurrent projects on one capacity pool, personnel assignment,
bounded facility and recruitment investments, bottleneck remedies, opposition sabotage that cannot
delete completed progress, and the mission↔research loop (`strategy_game/operations.py`, 83 new tests,
design record `strategy_game/docs/STRATEGIC_OPERATIONS_PHASE2.md`). It makes exactly one new question a
board row: **D39**, the four Phase-2 magnitudes and the open case of whether assigned support personnel
should ever bound a project's usable throughput. Every figure is a `TUNING_` parameter derived from a
quantity that already existed (Phase 1's three-unit throughput, `AGENT_CAPACITY`,
`TUNING_STYLE_BONUS_SEGMENTS`), so nothing is decided by being written down. **D27 and D28 are
untouched**: the Phase-1 dice band, work scale and tie rule stand exactly as they were, and no domain
TAG or ideological prohibition is read by anything new. Phase 3 (the branching technology DAG, faction
divergence, trade, espionage) stays unbuilt.


## Not a deferral case

- **#338** is a *living design diary*: ~90 checkboxes accumulated across many author addenda, most of
  them proposals for author approval. Closing it by deferral would be hollow, so it stays open until
  the author rules on its design or its own gates.
- **#309** was listed here as *"the umbrella: open by design"*, and that was right until the author asked
  for it by name on 2026-10-13. Closing it is **not** a deferral: its own acceptance criteria are met
  (it serves as a coherent, reusable north-star vision, referenced across the design docs), all ten of its
  §8 artifacts now exist as files, and its only remaining items are author decisions carried as rows D10,
  D14 and D15. Nothing was lost by closing it, which is the test this section exists to apply.

## #626 — Northern Noösphere + the psychiatric-origin NHI team (rows D43–D50)

Eleventh update (2026-10-26). Issue **#626** is a planning memo, not canon, and it closes with eight
questions it explicitly leaves to the author. They are carried here one sentence at a time so answering
one does not require re-reading the memo. The decision support is
[`ISSUE_626_OPEN_QUESTIONS.md`](ISSUE_626_OPEN_QUESTIONS.md); the playable draft that survives any answer
is `docs/scenarios/THE_SAMPO_PROTOCOL_EVIDENCE_ANNEX.md`. **No row asks for a new subsystem**, and none blocks
play: the pilot is written so that every answer changes what the material *claims*, not whether it runs.

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D43 | **#626's institutional home.** Europol canon has exactly one **NHI Desk** (one analyst, The Hague basement, coordinating authority only, no PSI/AGI branch); UNSA holds the Helsinki frame. Options: the Desk grows under joint-investigation-team cover (canon unchanged, team size becomes a story event) / a new standing Europol cell (contradicts the Desk) / a national unit with a Europol liaison (weakest fit for "cross-border cluster"). | the pilot's team composition, and who may arrest, search or compel | *joint investigation team* / *new cell* / *national unit* |
| D44 | **Which Romppainen leads (if any).** `docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md` names Dr. Harri Romppainen deliberately; `docs/archive/NARRATIVE_TIMELINE_VARIANTS.md` has him as Supo, PhD psychology; the Ubiquitous Maniacs legacy corpus has him as a **patient**, "vielä dissosioituneessa sivupersoonassaan". Options: same man, his dissociation is the case / different man, same name / he is a consulted witness and the "investigator" framing is dropped / same man, integrated and recovered. | every other named role in the unit, and whether the leader can be a player character | *same man* / *different man* / *witness only* / *recovered* |
| D45 | **The cell's relation to Helsinki UNSA.** Precursor (its failure or success explains UNSA's existence) / partner (one case, competing files) / separate campaign (no crossover). | whether UNSA is the pilot's referral partner or its rival | *precursor* / *partner* / *separate* |
| D46 | **How much *Maniac* is imported.** The memo itself leaves the touchstone ambiguous (Norwegian original 2014 vs Netflix 2018). Options: thematic only (psychiatry, trial ethics, shared imagery — no plot) / one named work as touchstone / both, deliberately contrasted. | how much of the pilot's Act 2 is homage, and therefore the attribution review | *thematic only* / *name the work* / *both* |
| D47 | **What patients are.** Witnesses only / witnesses plus one recurring patient / one playable patient (their credibility becomes a live constraint at the table). | the pilot's session-2 and session-4 scene ownership; whether a patient character sheet ever exists | *witnesses* / *recurring* / *playable* |
| D48 | **How many anomalies may be verified before the Crisis tipping point.** If verification is possible, the evidence → substantiation → institutional-response pipeline needs a threshold; if it is never possible, the setting stays permanently contested and no faction can be proven right. The pilot assumes **demonstrated ≠ confirmed** (a place-anchored account can be substantiated; a nonhuman intelligence cannot). | whether any future case may end with the word "confirmed", and whether the Crisis is a reveal or a permanent condition | *never confirmed* / *threshold* / *confirmable late* |
| D49 | **The Sampo's ontology.** One artefact / a class of technology / a misread legend / different things to different observers. The memo drafts three readings (scientific, noetic, political) and forbids settling them; a single artefact supports a heist plot, a class supports an economy, observer-dependence supports the Vallée-style reading the memo prefers. | whether later material may name a second Sampo-like site | *one* / *class* / *legend* / *observer-dependent* |
| D50 | **Are medical phenomenology and data analysis core mechanics?** Canon has the WN kernel and the evidence ledger (`src/rules/investigation_evidence.py`), and no clinical-differential or cohort-comparison procedure. Making either a mechanic means a new subsystem; the licensing boundary already recorded on this board is unchanged (SWN and AWN stay `blocked-unverified`, so any "Effort" or hazard procedure must be NoöPunk's own wording over a borrowed shape). | whether the pilot stays a scenario document or becomes a `strategy_game/casework` case with code and tests | *prose only* / *clinical procedure* / *data-analysis procedure* |
| D51 | **Attribute *presentation*: do the codes change, or only the labels?** `ISSUE_735_ATTRIBUTE_OPTIONS.md` §3 (Option M) describes a reskin that touches nothing mechanical: STR→Might, DEX→Reflexes, CON→Vitality, INT→Intellect, WIS→Psyche/Insight, CHA→Presence, with `STR…CHA` still the canonical identifiers in data, saves and rules text. The cost is a labelling pass plus the risk of a half-renamed tree; the benefit is tone at zero balance risk. This is #716's A/B/C seen from the presentation side — answering one answers the other. | any renaming pass, sheet labels, and #716's closed-but-undecided A/B/C | *keep codes* / *display aliases only* / *new codes* |
| D52 | **Attribute *structure*: six, seven, eight, or six plus derived tracks?** The memo's load-bearing finding is that the gap is **overload, not missing axes**: WIS already carries perception, judgment, willpower and psionic focus, and CHA carries both presence and connection. Splitting WIS into EMP+WIL gives seven; adding CYB gives eight; the hybrid keeps six and moves the new concepts into derived tracks (§5). The arithmetic decides the feel: the modifier table is flat from 8 to 13, so a split costs *concentration*, not average. Two sub-questions ride on the answer — whether WIL appears in a save or only in Effort and resistance, and whether the point array grows with the count (63 → 73/84; if it does not, new attributes are a net weakening). | the whole attribute architecture; save pairings; array design; everything downstream of D51 | *six* / *seven (EMP+WIL)* / *eight (+CYB)* / *six + derived tracks* |
| D53 | **Empathy and humanity: attribute, track, or skills only?** Canon already resolves empathy through `Connect`, `Talk`, `Kinesics` and `Perceive`, so a new EMP attribute would duplicate them. The memo also insists empathy is **not morality**: an android, hybrid or augmented character can be empathetic. The question is whether *humanity / identity / alienation* needs numbers at all, or belongs in prose plus an optional track rather than a meter that would quietly become an alignment score. | any humanity or alienation subsystem; the android and manipulator builds in §12 | *skills only* / *optional track* / *EMP attribute* |
| D54 | **CYB: attribute, derived statistic, or skill-only?** `System Strain` already prices the body's cost, and CWN resolves hacking as `INT/Program` with `Interface` / `Program` / `Hardware` as aptitude — so a CYB attribute risks counting the same thing twice and penalising unaugmented characters by definition. The counter-case is that technological intuition is a real axis the six cannot express. Terminology rides along: `Interface` is already a skill, so an attribute called Cybernetics or Tech must not collide with it. | any CYB attribute or derived track; the augmented-hacker build in §12; terminology in §11 | *attribute* / *derived* / *skill-only* |

## #747 — the reskin review (rows D55–D57)

Thirteenth update (2026-10-30). Issue **#747** asks for a chapter-by-chapter review of CWN/SWN and a
minimal reskin. The disposition matrix re-derived against the 2026-10-26 baseline is
[`ISSUE_747_WN_RESKIN_MATRIX.md`](ISSUE_747_WN_RESKIN_MATRIX.md): **21 of its 30 rows are AS-IS or
AS-IS-with-optional-scope**, four are NoöPunk-native modules that already exist and switch off
independently, two are cosmetic, and **one is a genuine conflict between two rulings**. These three
rows are what that review cannot settle by itself. None of them blocks play today.

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D55 | **The hacking access model.** Two rulings are both on record: #566 (2026-10-25, `docs/CWN_CHASSIS.md`) says *"CWN's matrix-like reachability **is not adopted** … access is not the scarce thing"*; the 2026-10-26 `WITHOUT_NUMBER_BASELINE.md` §6 says *"**Access and reachability first**, then the actual source procedure"*. They decide different games: a scene that begins with "can you reach it?" versus one that begins with "you are already inside — what does it cost you?". The code carries both sides (`src/rules/cwn_hacking.py` preconditions vs `src/rules/ubiquitous_network.py` exposure economy), and #749's Godot slice implements a reach→access→program→trace chain with calibrated numbers. | #752's node-link hacking screen; every intrusion scene in both games; whether `ubiquitous_network.py` or `cwn_hacking.py` is the reference for reachability | *ambient network (access is not scarce)* / *reachability first (source)* / *ambient, but reach is still a scene-level fact* |
| D56 | **The reskin pass itself.** D51 left the attribute *presentation* deferred as its own work item: do the six display aliases ship (STR→Might, DEX→Reflexes, CON→Vitality, INT→Intellect, WIS→Psyche/Insight, CHA→Presence), and does the same pass rename skills, gear and NPC job titles for a 2045 Nordic setting — with `STR…CHA` and every existing identifier unchanged in data, saves and rules text? | any renaming work; character-sheet labels; #747's rows 29–30 | *keep codes and source vocabulary* / *display aliases only* / *aliases + skill and gear vocabulary* |
| D57 | **Whether any MINOR-MOD departure is approved.** After the re-derivation only one row is a departure, and it is not a NoöPunk design choice but a contradiction (D55). Approving none keeps NoöPunk literally "CWN/SWN as-is" plus four optional native modules; approving one requires the source rule, the ruling that forces it and the file it lives in. | the overlay document `rulebook/NOOPUNK_WN_OVERLAY.md`, whose deviations table is empty until this is answered | *approve none (overlay = hierarchy + vocabulary + optional modules)* / *approve the rows you name* |

## #928 — two Stress engines on `main` (row D58)

Fourteenth update (2026-10-31). Issue **#928** was implemented **twice within minutes** by two sessions —
PR #930 (an overlay in `mods/noopunk/`) merged first, PR #929 (a core module wired into `GameState`)
merged second — and both are on `main` at `1010ab8`. They agree on the spine of the rule and differ on
participation, the addiction lifecycle, the scar exceptions, where the values live, and **whether
ontological shock is Stress at all**: #928's own text says keep the two distinct, the overlay routes it to
the Psyche module, the core module scores it +2. Neither session can resolve the duplication alone: the
overlay may not import `godot/core/` and the core may not import `mods/`, so a single engine means one of
the two placements has to lose. The record is
[`AWN_STRESS_RECONCILIATION_928.md`](AWN_STRESS_RECONCILIATION_928.md); `main` is green with both
(1822 Godot checks, 1652 Python tests), so this gates nothing today.

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D58 | **Which layer owns the AWN Stress rule — core or `mods/`?** (a) **Core owns it and the overlay retires** (recommended): `godot/core/awn_stress.gd` reads `data/rules/awn_stress.json`, absorbs participation, the addiction lifecycle, the three scar exceptions and the seven labelled NoöPunk triggers (minus any ontology-shock entry), and `mods/noopunk/stress.gd` is deleted with the screen re-homed under `godot/ui/`. This is the house pattern — AWN is an imported *published* subsystem like `cwn_*`/`swn_*`, NoöPunk code already lives in core (`noopunk_tags.gd`), and #848 names only the homebrew overlays as `mods/` material. (b) **Overlay owns it and the core module retires** — blocked unless `GameState` loses the Stress API, because core may not import `mods/`. (c) **Both stay** — cheapest today, and it needs the ontology-shock question answered one way plus one contract read by both; two arithmetics and two save formats is the drift `UNIFIED_IMPLEMENTATION.md` exists to stop. The sub-question either way: **is ontology shock Stress (+2), or does it stay the Psyche module's business and out of the Stress table?** | nothing today (no rule is applied to a sheet yet); every future AWN Stress change, which otherwise has to be made twice; the #689 Psyche boundary | *core owns it, overlay retires* / *overlay only (re-opens the #897 lock)* / *both stay* ; and *ontology shock: Stress or Psyche only* |

## #932 — the GUMSHOE investigation mod (rows D59–D60)

Fifteenth update (2026-10-31). Issue **#932** is a design deliverable whose proposal landed as
`ISSUE_932_GUMSHOE_CWN_UNSA_MOD.md` (PR #933); `docs/design/ISSUE_932_ACCEPTANCE.md` now checks that
proposal against the supplied book and against the investigation layer **already implemented** in #704
and #707. Two things follow. First, most of the proposal is not new work: the core-clue guarantee
(no roll, no spend), the discovery/interpretation split, the refusal of a spend pool, the CWN-skill
basis and the alternative-method rule are code with tests, so the open implementation surface is only
the five unrepresented clue types (floating, leveraged, pipe, restricted, timed) and the expertise tags,
and none of it is authorised yet. Second, the approvals the issue asks for are author calls, and two of
them were not on the board: the tags, and the institutional conversion. (The spend/resource question is
already **G2** in `docs/rules/GUMSHOE_INVESTIGATION_LAYER.md` §7, and G1 records the one place where the
implementation is deliberately more generous than the book: GUMSHOE needs a *positive* rating to hand
over a core clue, while NoöPunk counts CWN rank 0 as trained.)

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D59 | **Approve the investigative crosswalk and the expertise tags.** The crosswalk maps all **40** book investigative abilities and the 13 general ones onto CWN skills, backgrounds and Foci as *suggested approaches*, never gates — completeness is verified against the book's own ability list; what is open is whether the mapping is the one to print, and whether the 2–4 **expertise tags** per character are adopted as free descriptive prompts (recommended) or dropped. Tags add no dice, points or progression; adopting them changes no rule, only what the GM reads off the sheet. | the GM reference page, and whether `Investigator` ever grows a tag field | *accept the crosswalk as printed* / *tweak named rows* ; *tags yes* / *tags no* |
| D60 | **Approve the GUMSHOE-generic → NoöPunk institutional mapping.** UNSA as the investigating agency with its own case file and support staff; human collaborators and hostile factions as organised adversaries; NHI/noetic phenomena **classified case by case**; evidence security and its ethical dilemma as the containment question; a recurring Helsinki base with local contacts under the NPC supervisor. The rule that must survive any approval: a case may be a hoax, a misidentified phenomenon, institutional malfeasance, rogue-AGI activity, human conspiracy **or** genuinely inexplicable, and the characters' beliefs are never evidence. | the scenario/campaign layer, and what the pilot case may assume | *approve as mapped* / *amend named rows* |

## #932 follow-up — which module owns discovery (row D61, narrowed)

Seventeenth update (2026-10-31). #939 (the notebook's SRD clue procedures) and #940 (the screen, plus
`Gumshoe.ratings_from_sheet`) landed after this row was written, and #940 **answered the half of it that was
about the rating gate**. `rating = rank + 1` (an untrained skill, rank -1, is 0) means a CWN rank of 0 — which
CWN already calls trained — becomes a GUMSHOE rating of 1, which the SRD already calls competent. The two
systems stop disagreeing, no second advancement track is created, and G1 no longer needs to describe a
divergence: there is none left to describe. That half is **settled by construction**, not by a ruling.

What remains is the other half, and it is smaller than it looked: the repository still has **two procedures
that both claim to decide whether a clue is found** — `src/rules/investigation.py` with
`godot/core/investigation_adapter.gd` (competence by presence, no pool, benefits priced in CWN costs) and
`mods/noopunk/gumshoe_investigation.gd` with the new screen (rating ≥ 1, a pool spent only on benefits). A
core clue never depends on a roll or a spend in either, so nothing is broken; but a table must not run both
and an agent must not extend both.

Underneath it is a **data** question that will bite before the rules question does: the screen reads
`data/world/investigation_scene_intake.json`, where a clue names a GUMSHOE ability directly
(`"ability": "bureaucracy"`), while `case_graph.json` names a **CWN competency** and is read by the adapter
and the notebook. Nothing checks that every competency a case asks for is covered by some ability, and one
is not — `Survive` (the `night-air` clue) maps to none of the sixteen. Latent today because the screen does
not read case graphs.

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D61 | **Which module owns discovery, and which shape does a clue carry?** (a) **The adapter owns discovery, the overlay only prices benefits** (recommended): `investigation.py` stays the rule, #935's pool is an optional module, one line in each file says so, and the screen reads a case graph through the adapter. (b) **The overlay owns discovery**: the adapter retires for investigation use and `Investigator`'s no-pool test is retired on purpose. (c) **Both stay, per campaign**: acceptable only if each file names the other and the screen records which one a scene used. Independent of (a)/(b)/(c): **unify the clue shape** — either a clue names a GUMSHOE ability or a CWN competency, not both, and a test then fails when a case asks for a competency no ability covers (`Survive` is the living example). | any further work on either module; what a scenario author may assume about spending; whether the screen ever reads a case graph | *adapter owns discovery* / *overlay owns discovery* / *per campaign, both named* ; and *abilities* / *competencies* as the one clue shape |

## #943 — the Noösphere / ontological-apocalypse module (rows D62–D64)

Eighteenth update (2026-10-31). #943 asked for a PbtA-inspired narrative overlay on the CWN chassis.
The module is [`ISSUE_943_NOOSPHERE_APOCALYPSE.md`](ISSUE_943_NOOSPHERE_APOCALYPSE.md), the criterion walk is
[`ISSUE_943_ACCEPTANCE.md`](ISSUE_943_ACCEPTANCE.md), and the executable half is `mods/noopunk/noosphere.gd`
with 46 assertion rows in `godot/tests/test_noosphere_943.gd`. It adds no dice, no modifier, no second cost
track and no new move; it keeps a percept/hypothesis record and an event-driven, reversible clock.

Two things need the author rather than another agent. The first is approval of the extension: **D50** already
rules that PbtA contributes clocks and nothing else *yet*, and this module goes further around the dice
without touching them. The second is a procedural deviation worth an explicit ruling rather than a silent
inheritance: the first increment merged a GDScript module **before** the design document existed, which is the
opposite of #943's own eleventh criterion. The module changes no rule and imports nothing from `godot/core/`,
so the deviation cost a merge and not a rule — but whether it stays in `main` is the author's.

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D62 | **Approve the module, and in what form?** (a) **Approve as written**: an isolated overlay module plus the design document, no rulebook chapter until a playtest exercises a clock to its terminal segment. (b) **Approve the document only**: hold `mods/noopunk/noosphere.gd` out of `main` until a chapter exists, keeping the 46 test rows as the specification. (c) **Refuse the extension beyond D50 and keep clocks only**: drop N1–N3, keep the clock, and the module shrinks to a state machine. D62 also covers the deviation: the module landed before its design was reviewed, against #943's criterion 11. | any further work on the module; whether `mods/noopunk/noosphere.gd` is canonical, provisional or removed; whether a rulebook chapter may be drafted | *approve both* / *document only* / *clocks only* |
| D63 | **Which clocks ship, and how long are they?** §9.2 proposes five (NHI disclosure, rogue ASI acceleration, cyber-psychic convergence, UNSA authority, local crisis) at the 4/6 segments of the #689 spec. A published campaign would need three to five of them named, and a rule for what happens when two fill on the same event. The named clocks are proposals, not timeline: the disclosure clock's terminal segment is the panic depth of `RULEBOOK.md` §41.1, which is a *regional* condition, not a global one. | what a scenario author may assume about escalation; whether a case may declare its own clock count | *all five, 4/6 as specced* / *name a subset* / *local crisis only* ; and *one clock per question, table decides* / *a fixed precedence* |
| D64 | **May any of *The Veil*'s text ever be quoted?** The book licenses its **text** CC BY-SA 3.0 and reserves its art separately; *Apocalypse World* 2e establishes no open licence at all. The module as written quotes neither and re-expresses mechanics with page references, which keeps the tree clear of ShareAlike. Quoting a paragraph of *The Veil* would put ShareAlike obligations on the file that carries it — and `tests/test_third_party_expression_absent.py` exists precisely because expression once entered this tree and had to be removed. | whether the design documents may quote, and the licence status of any document that does | *no quotations, ever* / *quote and accept ShareAlike in that file* / *quote only from the CC BY-SA text and mark the file* |

## #1006/#1007 — module tiers and the reveal ladder (rows D68–D69)

Twenty-second update (2026-11-01). The constitution (#1006) landed with a source-level registry and an
overlay registry; this adds the two things neither could check: **every module under `src/rules/` is now
classified exactly once** (`data/rules/rules_constitution.json` → `module_tiers`, guarded by
`tools/rules_constitution_audit.py --check` and `tests/test_rules_constitution_modules.py`, which runs the
baseline with every overlay module import-blocked), and **the content ladder is data**
(`data/world/reveal_ladder.json`, `tests/test_reveal_ladder.py`).

Two questions are open, and neither is a rules redesign:

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D68 | **May a NoöPunk mod add a new *skill*?** The constitution says a mod may not touch CWN's skill list. Empathy or Awareness as **additional mod skills** — never replacing `Notice`, `Know` or `Work` — is the one place where "overlay, not edit" is arguable, because a skill is a shared vocabulary rather than a procedure. The alternative is to express the same ground through existing skills plus typed competence tags. | any character-sheet skill field; how an investigator's empathy or anomaly-awareness is modelled in the MUD | *mod skills allowed, additive only* / *existing skills plus tags* / *no new skills, ever* |
| D69 | **Which optional-source modules ship?** `wwn_projects.py` (WWN) and `awn_survival.py` (AWN) exist, pass their tests and are tiered `optional-source`. Whether the base game includes them, or they stay opt-in modules a campaign enables, is a content decision rather than a mechanical one. | what a new player gets by default; which chapters describe the shipped game | *both opt-in* / *AWN survival in, WWN projects opt-in* / *both in the base* |

## After an answer

Each answered row becomes: a criterion check against `main` → an acceptance record in
`docs/design/ISSUE_<n>_ACCEPTANCE.md` → PR → merge → close. A row answered *"defer"* or *"out of
scope"* closes its issue just as cleanly, because the record then states the deferral rather than
pretending the item was met.

— Ai (愛)

## Answered rows

- **D40 — ANSWERED 2026-10-25.** *Is the kernel staying on Fate `4dF` (#389, six skills #482), or
  being replaced by CWN's `2d6`?* Answer: **neither is replaced.** #564 governs **layer A only**;
  `1d10` stays (#111) and `4dF` stays for the crossover. The 2d6 reversal is not taken — it would
  have touched 80 `1d10` sites across 41 files and 41 test files. Classes and levels are declined;
  **Edges are admitted**. Record: `ISSUE_566_ACCEPTANCE.md` and `docs/CWN_CHASSIS.md`.

## Row raised 2026-10-25

- **D43 — PSI discipline vocabulary.** `src/rules/noopunk_extensions.py` (a scenario prototype,
  explicitly **not** the rules owner — `natural_psi.py` is) accepts seven discipline slugs;
  `influence`, `healing` and `shielding` are **not** among the six locked PSI skills (#159: ESP,
  Telepathy, Psychokinesis, Precognition, Psychic Defence, Noöspace). The conflict is already
  recorded as prose in `docs/rules/ISSUE_572_NATIVE_SUBSYSTEMS.md` §7, and the module carries a scope
  note saying no rule may be built on those three names. **What is missing is the decision itself:**
  are they admitted (and if so, as skills of their own or as capability tags under an existing
  skill), or dropped? Deleting them from the prototype asserts they are not canon; keeping them
  without a ruling leaves a trap for the next implementer. Both are canon calls, so neither is taken
  here. Siblings queued D41 (exposure economy) and D42 (Effort curve) from the same round; this row
  is the third and the only one that is a canon question rather than a balance question.

- **D40 — SUPERSEDED 2026-10-26.** The answer recorded on 2026-10-25 (*"layer A only, `1d10`
  stays"*) is replaced by the author's ruling: *"use CWN/SWN/AWN/WWN system for everything. Make the
  stats, skills, all rules based on them. We will modify later."* The tabletop baseline is now the
  Without Number engine (`2d6 + attribute modifier + skill level`), with the WN attribute set.
  See `docs/design/RULING_2026-10-26_WN_BASELINE.md`. The licensing boundary is unchanged: SWN and
  AWN stay `blocked-unverified`, so the engine is implemented from the CC0 CWN/WWN SRDs.

- **D41 — the optional narrative layer survives the Without Number baseline, re-anchored on
  `2d6`.** Its two safety rules were justified on the retired 4dF kernel; re-measured on the
  real dice, a +2 invoke at DV 8 is worth **+30.6 pp** against 4dF's **+32.1 pp**
  (`docs/design/NARRATIVE_LAYER_2D6_CALIBRATION.md`, `tools/narrative_layer_2d6_calibration.py`).
  `rulebook/19_NARRATIVE_LAYER.md` and `src/rules/narrative_layer.py` must be rewritten
  against `2d6 + attribute modifier + skill` / `6·8·10·12·14`.

- **D42 — one invoke per roll; aspects never stack.** Four stacked steps reach 91.7% at the
  standard difficulty, which is worse than certainty: failure then reads as bad luck rather
  than as a broken rule.

- **D43 — an aspect's worth is difficulty-dependent.** +16.7 pp at DV 8, +0.0 pp at DV 14.
  Any rule pricing an aspect as a fixed "+X" must name the difficulty.

- **D44 — no second dice system. Closes C1.** Checks on `2d6`; attacks and saves on the CWN
  `d20`; `4dF` survives only inside `strategy_game/` as legacy.

- **D45 — Fate is retired as a baseline, not as vocabulary. Closes C5.** The aspect/compel
  *shape* is kept; the kernel is not. Any note describing Fate Core as the approved kernel
  predates the 2026-10-26 ruling and must not be reapplied by implication.

- **D46 — PROVISIONAL: mental load is conditions, not a track.** No second harm economy
  beside CWN's Trauma / Frail / Strain. A condition constrains choices; it does not drain a bar.

- **D47 — PROVISIONAL: the four-layer exposure model** — observable event → acute response →
  persistent condition → worldview state.

- **D48 — worldview change is a player decision, never a failed save.** A contradicting shock
  presents a choice with two different costs; a roll may never overwrite a conviction.

- **D49 — EP-grade stress/trauma/disorder is deferred, not rejected**, and only revisited when
  a written case demonstrably cannot be carried by conditions.

- **D50 — PbtA contributes clocks only.** Moves-as-catalogue refused; partial success not
  adopted.

- **#689 design gate closed** by these records (`docs/design/DECISION_689_NARRATIVE_AND_MIND.md`).
  D46–D50 are provisional and reversible in one sentence. Implementation is not authorized:
  follow-up issues carry it, each with executable tests.

- **D51 — the codes stay; only the presentation vocabulary is deferred.** `STR / DEX / CON / INT / WIS /
  CHA` remain canonical identifiers in data, saves and rules text. The Might / Reflexes / Vitality /
  Intellect / Presence wording is a **later, separate work item**, so no sheet, save or schema moves
  today. (The queue's D51 is *presentation*; §18 of `ISSUE_735_ATTRIBUTE_OPTIONS.md` records the same
  decision in the same words.) **PROVISIONAL.**

- **D52 — six attributes remain canonical; overload is answered by derived tracks (Option H).**
  `WIS` carries perception, judgement, willpower and psionic focus at once; `CHA` carries presence
  and connection. That is two overloaded attributes, not three missing axes. An eight-attribute
  split was rejected on arithmetic: it is free only if the generation budget rises with the count
  (`docs/design/ISSUE_735_ATTRIBUTE_OPTIONS.md` §3). **PROVISIONAL.**

- **D53 — EMP is not Humanity, and neither is morality.** Empathy is a capacity; morality is a
  judgement; an android with high empathy and no legal personhood is coherent. Humanity / Identity /
  Alienation is an **optional track**, never a score that falls when cyberware is installed.
  **PROVISIONAL.**

- **D54 — CYB is not an attribute.** Capacity is `System Strain`, aptitude is `Program` / `Fix`
  (`Interface` / `Hardware` are the retired names — see the memo's §2.1), and the rest is gear. As an
  attribute it penalises unaugmented characters by definition. **PROVISIONAL.**

- **Standing constraint, not a queue row — investigation never depends on an attribute roll.** A
  competent investigator obtains the core clue without a check (#704). Attributes govern the quality of
  the *extra* reading of evidence, never whether the clue exists. This needs no decision because it is
  already the implemented rule; it is recorded here so a later attribute change cannot quietly break it.

- **#735 closed** on these four records. No code, rulebook or data change: the six codes are
  untouched, so every stored character and the full test suite remain valid.
