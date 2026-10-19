# Issue #516 — reference-to-mechanic matrix (decision aid, not rules)

**What this file is.** Issue #516 names one additional design deliverable an agent can legitimately
produce: *"document a short reference-to-mechanic matrix for these games: what NoöPunk should adopt,
simplify, avoid, and which layer each influence informs."* This file is exactly that matrix, for the
seven tabletop influences and the seven named computer-game influences, grounded in what the
repository already contains.

**What this file is not.** It decides **no rule, mechanic, stat, skill, resolution system, damage
model or balance**. Every ADOPT/SIMPLIFY/AVOID cell is a *candidate observation* for **Tomi, the
author and final decision-maker**, per the issue's own constraint: *"This is a human-led design
decision. AI may provide comparisons, prototypes and critique, but must not autonomously choose or
declare the final rules canonical."* Nothing here opens rulebook canon. Nothing here becomes
playable or approved except by author direction recorded in the issues.

**Reading convention.**
- **ADOPT** — borrow as design influence (possibly as CC-licensed *mechanic*, where the source
  licence permits and the repo already does so). Not an authorisation to implement.
- **SIMPLIFY** — keep the idea, reduce its mechanical footprint relative to the source.
- **AVOID** — reject or guard against importing.
- **LAYER** — which runtime the influence informs: **N** = narrative RPG scene (#502 Phase 1),
  **T** = four-agent tactical mission (#515), **S** = faction / grand strategy (#502, #461).
- "already in repo" lines describe **existing, verified facts** about files and issues — they are
  status, not new canon.

---

## Part 1 — The seven tabletop influences

| # | Influence | ADOPT | SIMPLIFY | AVOID | LAYER |
|---|---|---|---|---|---|
| 1 | **Fate Core** | Four actions (Overcome / Create an Advantage / Attack / Defend) and the Outcome ladder — already the approved one-kernel resolver; aspects as fiction that grants *permission or consequence*, and compels that pay the player for complications | Skill pyramid → the six broad individual skills + stunts + competence tags already on the sheet; stunts' full mechanical enumeration; possibly the +2/reroll invoke wording (see Q7) | A second skill catalogue under a Fate label; uncapped aspect stacking (the #229 prototype measured the auto-success exploit); treating Fate Core as anything but the CC BY engine | N (procedures) — resolver underneath T and S |
| 2 | **Transhumanity's Fate** | The six aptitudes as the individual skill vocabulary — already the author's #482 decision, in `strategy_game/rpg/skills.py`; compact-playset cast/mission scale; gear as named permission, not a bonus ledger (default biological body, optional stack — already in `fate.py`) | Morph and augment bookkeeping → few sheet states (body / resleeved / cortical_stack flags already exist); its conflict subsystems → the one kernel | All Transhumanity's Fate lore (Firewall, the Fall, virus-based PSI, presumed resleeving) — #482's nonnegotiable setting separation; its CC BY-NC-SA prose in this repo | N; character model carried into T |
| 3 | **Eclipse Phase 2e** (25% simulationist priority) | The aptitude *model provenance* (already Fate-rated per #482); permission-gated PSI (natural PSI + capability before any roll — already in `fate.py`); simulationist consequence thinking: reachability/access as fiction (#344), wounds persisting as state, stacks/resleeving as costly options not defaults | Percentile maths and pools → ladder-adjacent expression; morph catalogues → the deferred transhuman list in `rulebook/2_ATTRIBUTES.md`; its subsystem sprawl → only what scenes need | Any percentile import (#482: EP is a comparative reference, "not imported percentile mechanics"); EP setting/history/PSI origin; NC-licensed text; making EP the chassis (worldbook note, §15) | Simulationist texture of all three; strongest on wound/lethality truth-model in T and PSI/cyber permissions in N |
| 4 | **Cities Without Number** (25% gamist priority, primary) | Edges as a chargen vocabulary candidate — `rulebook/14_CHARACTER_GENERATION.md` §13.8 names CWN-spirit Edges and leaves their existence as a separate unsettled question; brief/mission/scene procedure shape; tag–aspect economy as bounded tags | Full feat/class advancement frame; item economy and CR bookkeeping → existing tags/aspects/equipment-as-permission | Character classes (repo intent: *an assemblage, not a class*, §13.1); level-driven stat inflation before the author chooses advancement (Q8) | T mission structuring; S operation turn-loop (kin to `strategy_game/projects.py`'s check → throughput → clock) |
| 5 | **Stars Without Number** | The faction-turn *pattern* — a periodic beat where faction actions update one shared world state — as a pattern only; the repo already has the world-state interface and one-writer rule (#502) and the project engine (#506) in its place | Its full faction mini-game → one agent-lead check + faction throughput + project clock per operation, as `projects.py` already implements | A second, parallel faction game on its own rules — the repo refuses a second resolution path (`projects.py` module docstring); divergent faction-state silos | S |
| 6 | **Worlds Without Number** | Campaign/legend scaffolding as GM prep craft: layered region/faction/question generation, "heroics vs mundane" mode thinking as *framing*, not mechanics | Its attribute/skill/d20 frame → not imported; the mode split → one mode with fictional permission gates | Importing a d20 stat+skill frame alongside the ladder question (Q3/Q4) — that would pre-empt the author's resolution decision | N (prep scaffolding); lightest mechanical footprint of the three |
| 7 | **Powered by the Apocalypse — selected: *Apocalypse World*, *The Veil*, *The Sprawl*** (per #461's own named trio) | From *Apocalypse World*: the move-result structure of mixed success — already expressed as the Outcome ladder plus #229's band GM moves (reward / cost / complication / escalate); MC-move adjudication; fiction-first "say what you do, then resolve". From *The Veil*: transhuman/psi-adjacent subject matter proximity for what moves-as-capabilities might be about. From *The Sprawl*: mission-frame structure (opposition, clocks, scored operations) as experience reference for T | Full playbook+playbook-move rules → capabilities/stunts/competence tags; per-move stat modifiers → the one kernel; long condition clock stacks → Q6's single decision | Named move text and prose (copyright, and #461 explicitly: "not copying/recycling their rules or prose"); playbooks as classes (no classes, §13.5); mechanic-count sprawl | N (50% narrativism lives here) |

**Grounding notes (Part 1).**

- The approved playtest kernel is `strategy_game/rpg/fate.py`: 4dF, `Action` × `Outcome`
  (failure / tie / success / success with style), shifts, a *single* resolver used by cyber, PSI,
  dialogue and combat (`skill_check`), stress boxes and 2/4/6 consequences, fate-point/refresh
  discipline. `strategy_game/rpg/RULEBOOK.md` documents it as Fate Core (CC BY) based, with
  Transhumanity's Fate and EP 2e as reference-only (NC-SA, prose not included, §8).
- `strategy_game/rpg/skills.py` fixes the individual layer to COG / INT / REF / SAV / SOM / WIL
  (EP 2e aptitudes as Fate-rated skills, #482) and refuses cross-layer skill names and the
  unapproved strategic roster at check time — the "one sheet, two scales" the issue's cross-layer
  requirement leans on.
- `rulebook/NEW_EDITION.md` is the first-edition ledger: six attributes FIT/REF/INT/SOC/PSY/CYB,
  "resolution dice, difficulty numbers and advancement values have not yet been chosen", no
  mandatory battle grid, investigation/relationship/Psyche as central systems.
- `rulebook/19_NARRATIVE_LAYER.md` (#229) is the *provisional* narrativist overlay: aspect anatomy
  (permission / modifier / consequence classes), one-ladder-step invocations capped at one per roll,
  a 0–3 unnamed spendable pool, band GM moves, and the no-stress-track rule consistent with §51.
  Note it and `rpg/RULEBOOK.md` §4 currently *disagree* on invoke arithmetic — that is Q7.
- `strategy_game/projects.py` (#506 Phase 1) is the strategic instance of the same kernel:
  agent-lead check (faction-agent context) → faction throughput → `ProjectClock`, with every
  number marked `TUNING_` and carried as row **D27** of `docs/design/AUTHOR_DECISION_QUEUE.md`.

---

## Part 2 — The computer-game influences (the issue's three grouped headers, seven names)

The issue distributes these across three headers — *RPG adventures and character-driven
storytelling* (2), *Tactical squad missions* (3), *Faction and grand strategy* (2) — and directs
they be used "as experience and design references… not as additional rulesets to copy wholesale."
This file covers all **seven** named titles.

| # | Influence | ADOPT | SIMPLIFY | AVOID | LAYER |
|---|---|---|---|---|---|
| 8 | **Citizen Sleeper** | Clocks as visible pressure — the repo already carries project clocks (`projects.py`) and #506 names "the Citizen Sleeper-style clock"; per-cycle scarce-arc choices as the experience the one-action-per-character turn ledger should deliver; meaningful choices under pressure with compact interactions | Its cycle/need/decay economy → a small set of clocks and a per-turn action ledger; its dice-cycle as *feel*, not a second RNG path | A full survival/economy sim; clock proliferation (one clock per state); setting import | N; clock propagation pattern links N → S |
| 9 | **Disco Elysium** | Skills-as-perspective dialogue and investigative noncombat play as the design goal — directly the issue's design question ("make dialogue, investigation, PSI and hacking as engaging as combat with one lightweight underlying rules system"); meaningful failure as narrative material; psychologically distinct characters (already central: NEW_EDITION §4–§5) | Its 24-skill interior cabinet → the six broad skills + tags; its passive-check engine → checks only when uncertainty is interesting | Skill-as-voice copy and its setting; passive-skill explosion; any percentile-2d6 special case | N |
| 10 | **X-COM** | Persistent consequences propagating (injuries feed forward — #515 already requires it); high-stakes squad selection and mission commitment; cover/positioning/action economy as the T layer's *goals*, expressed through the same kernel | Hit-chance per-weapon maths → kernel checks with fiction-first permission; base-building/meta economy → the strategic layer's own engines (#506) | A competing combat mini-RPG with its own stats or to-hit table (the issue's stated fear); mandatory tactical battles per quest | T |
| 11 | **Cyber Knights: Flashpoint** | Stealth/infiltration as a first-class *alternative solution*, not a combat variant; pre-mission planning/commitment; security systems as world state (kin to the existing connectivity/#344 model) | Its gear/tech depth → equipment-as-permission + competence tags; elaborate stealth state machines → permission + consequence aspects | Per-system hacking minigames — the repo's rule is foothold-before-roll and **no second mechanic** (`fate.py` demos) | T |
| 12 | **Shadowrun: Dragonfall** | The binding exemplar: one four-character team whose sheets, dialogue, exploration, hacking and combat are *the same characters* in scene and on the map — exactly #515's "avoid inventing a second full ruleset"; hub-world social texture as an N-layer beat between missions | Its karma/build progression → whatever Q8 decides; its long combat sequences → "fast, dangerous" per the issue's constraints | Run-and-gun as default (first edition is investigation-first, NEW_EDITION §8); two stat systems for tactical vs scene play | T + N (the bridge) |
| 13 | **Crusader Kings III** | Characters, relationships, traits and personal agendas driving faction politics — the repo already makes relationships and Psyche central systems (NEW_EDITION §4–§5) and #502 makes the PC the *faction leader from the start*; emergent narrative from character-first simulation | Scheme/council machinery → one check + one consequence per strategic operation (as `projects.py`); its depth → staged per the #502 roadmap | Importing dynasty/marriage/intrigue depth wholesale ahead of the author's staged plan | S |
| 14 | **Terra Invicta** | The councilor pattern — #461 already fixes it in author language: five characters (leader + four agents), one action each per turn, generic vs capability-gated special actions, abstract strategic map; long-horizon faction strategy and geopolitical consequence propagation | Its deep simulation (control points, ideological drift) → the three *stages* of #502: thin faction state → organizational board → grand strategy | Starting deep: the roadmap (#502) explicitly phases it; an independent agent-skill economy beside the pending #482 roster | S |

**Grounding notes (Part 2).**

- #502 (closed, the roadmap) fixes the sequencing and the PC premise; #515 (open) fixes the
  four-character tactical map and the reuse requirement ("Reuse NoöPunk's existing lightweight
  Fate-inspired stats, tags, actions, wounds and mission consequences wherever feasible").
- `strategy_game/projects.py` is today's S-layer instantiation of the Terra Invicta-councillor
  pattern: one action per character per turn (`rpg/roster.TurnLedger`), checks on the one kernel,
  institutional throughput, multi-turn clocks, tuning numbers pending (D27).
- The issue's own design questions (one per header) are mirrored by Q11, Q13 and Q14 below.

---

## Part 3 — Questions this matrix cannot answer — for the author

**Everything below is an open decision this matrix exposes but must not make.** None of these is a
recommendation; they are stated as questions because #516's deliverable is Tomi's documented,
playtested, signed-off ruleset. Where repo state is named, it is stated as fact of what exists, not
as an answer.

1. **Unified core resolution.** Is the approved 4dF shifts engine (`strategy_game/rpg/fate.py`) the
   single unified resolution mechanic for all domains the issue lists — social, investigative,
   physical, cyber and astral/PSI — and all three layers, or does the core-tabletop edition replace
   or re-derive it?
2. **Degrees of success.** Do outcomes stay the four-band Fate ladder (failure / tie / success /
   success with style), become the #229 band vocabulary (reward / cost / complication / escalate),
   or use some other degree structure — and do tie rules exist everywhere (see the pending tie
   question in `AUTHOR_DECISION_QUEUE.md` D27: `projects.py` currently grants a tie *no* progress)?
3. **Surviving stat model.** `strategy_game/rpg/skills.py` fixes the crossover individual layer to
   COG/INT/REF/SAV/SOM/WIL (Fate-rated, #482), while `rulebook/NEW_EDITION.md` §1 and
   `rulebook/2_ATTRIBUTES.md` carry FIT/REF/INT/SOC/PSY/CYB (1–10, native). Which is the surviving
   character model of the core tabletop/computer RPG — one of the two, both as two named contexts of
   one sheet, a merged mapping, or something the author defines — and if both, what is the mapping?
4. **Numeric engine.** `rulebook/2_ATTRIBUTES.md` retains the #111-era `STAT + Skill + 1d10` line;
   the approved crossover kernel uses `4dF + skill` against the ladder, #229 speaks of a pending
   scale migration (-3…+3 core), and `docs/design/ISSUE_200_SEVEN_STEP_SCALE.md` explores one. Which
   numeric engine is canon, and what converts between the incumbent artefacts?
5. **Skill-list size.** Is the individual layer capped at the six broad skills (specialities only as
   stunts / competence tags, per #482), and how many skills may the *strategic agent* roster carry
   (it is a proposal in `strategy_game/data/strategic_skills.json`, still unapproved)?
6. **Wound / stress model.** Fate-style stress boxes + 2/4/6 consequences (`fate.py`),
   #229's no-stress-track harm vocabulary (`RULEBOOK.md` §51: consequences as states, not
   arithmetic), PbtA-style condition lists, or Citizen-Sleeper-style clocks — which single model (or
   which deliberate per-layer split) does the author approve, and how do wounds persist across
   scenes and into T/S as #515 requires?
7. **Aspect economy.** `rpg/RULEBOOK.md` §4 grants invoke = **+2** (or reroll); `rulebook/19_NARRATIVE_LAYER.md`
   (#229) caps invocations at **one ladder step, once per roll**, with a provisional unnamed 0–3
   pool, citing its own measured exploit data. Which arithmetic is canon for the core RPG, and does
   the resource pool get its canon name?
8. **Advancement.** No advancement system is approved anywhere in the repo (14_CHARACTER_GENERATION
   §13.11 explicitly defers it). Which advancement approach applies, does it touch the individual
   ladder, the strategic ladder, or both, and does it advance via XP, milestones, fiction triggers
   or clocks?
9. **The SCIENCE question (#506 / #507).** The author's 2026-10-16 ruling binds research to **one**
   general science rating, resolved in the strategy context, with no discipline-specific numeric
   skills and no extra rated knowledge ladders. Does #516's core-RPG work ratify that ruling verbatim
   (science never becomes an individual seventh skill; subjects stay project metadata), and is any
   individual-scene expression of scientific competence wanted beyond tags?
10. **Edges / tags formal existence.** #197 names CWN-spirit Edges as a *separate mechanical question
    it does not settle*. Do Edges exist as stunts, as competence tags, as a new authored category —
    and do they cost anything (chargen budget, advancement currency, or free labels)?
11. **PbtA move surface.** Are capability-gated "special actions" (#461: netrunners attack, psykers
    remote-view; enforced today by `require_capability`) expressed as stunts, as authored moves with
    mixed-success ladders, or only as kernel checks gated by capabilities — and is any playbook-style
    move-set wanted at all, given no-classes?
12. **NPC / NHI representation.** `rulebook/2_ATTRIBUTES.md` models absent layers as N/A (null) with
    11+ effective for superhuman performance; `fate.py` defaults unknown names to +0 and carries no
    N/A state. How are NPCs, NHI, AGI and multi-layer entities represented on the one sheet, and
    which model governs opposition ratings?
13. **Tactical binding (#515).** Does tactical combat on the #515 map resolve on the same kernel
    (checks with fiction-first permission), or is a grid-derived procedure (initiative, action
    points, cover states) layered *on top of* it — and if the latter, what may the grid layer add
    without becoming the "competing combat game" the issue forbids?
14. **Strategic binding (#502 / #506).** Does the author accept the Phase-1 pattern — agent-lead
    check → faction throughput → project clock, with the `TUNING_` numbers now pending as row D27 —
    as the S-layer resolution, and how do mission results (injuries, intelligence, resources,
    political consequences) convert into faction state, by which interface and with whose approval?
15. **GM adjudication surface.** How much of the #229 GM-move / compel structure (and #304's
    controller model) is canon *before* the core ruleset is approved, and where does the LLM-seam
    rule ("propose, never resolve") get restated in the core tabletop rules?
16. **Edition sequencing.** `NEW_EDITION.md` defers tactical-grid combat to a later optional
    expansion; #515 is open and #502 Phase 2/3 run ahead. In what order does the author want the
    core ruleset, the tactical overlay and the strategic expansion approved and playtested, and
    which worked examples (the issue lists five) gate the sign-off?

---

*Provenance: drafted 2026-10-19 on origin/main 00a39b6 as input to issue #516 (agent-assisted
research artefact; per #516 the author alone chooses and must explicitly approve what becomes
canonical). Repo policy #271: no tests for this document. No commit made; the branch state is left
for the author to review.*