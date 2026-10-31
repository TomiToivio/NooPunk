# CURRENT PRIORITY — issue #950 (supersedes #946 and the Godot-first framing of #897)

**The Evennia MUD in `mud/` is the default target for all coding agents.** Godot is a secondary, maintenance-only
graphical implementation: it stays in the tree, it keeps working, and it is not where new game features go
unless a task explicitly names Godot.

1. **Default target:** `mud/` — Python, Evennia. Confirm the layout before editing.
2. **First deliverable:** a complete **single-player UNSA** story that runs with **zero LLM, zero Mesa, zero
   other players**, and no network dependency. Scripted NPCs, quests, clues, combat and saves must work
   headlessly.
3. **First engineering action:** the Godot → Evennia CWN migration and the linked-SRD coverage audit. The matrix
   is `data/rules/cwn_compliance_matrix.json`, rendered to
   [`docs/rules/CWN_COMPLIANCE_MATRIX_950.md`](docs/rules/CWN_COMPLIANCE_MATRIX_950.md) and validated by
   `tools/check_cwn_compliance.py`. It says `implemented` only where a test exists, and it marks the sections
   the linked SRD omits as `missing` rather than claiming them.
4. **Rulebook parity is compulsory:** a mechanic change lands with its matrix row, its test, and the
   corresponding tabletop text — or an explicit "no tabletop mechanics change".
5. **Godot is preserved, not deleted.** Do not route generic RPG features there. Do not rewrite its work
   unreviewed.
6. **Later phase:** multiplayer, Concordia-style LLM GM/NPCs, Mesa simulation and non-UNSA factions are not MVP
   prerequisites. The solo campaign comes first.

# FOUNDATIONAL AUTHOR DECISION — issue #897 (2026-10-31)

This decision supersedes the **presentation and gameplay** portions of #848 and older directives where they conflict. The **rules foundation remains the same**: published Cities Without Number (CWN) is permanently the primary OSR chassis; compatible Stars Without Number (SWN) psionics/space/factions and selective WWN/AWN material can extend it where appropriate. Do **not** propose or introduce a replacement core dice engine, attribute scheme, tactical framework or bespoke rulebook. Godot uses the repository-root `project.godot`, `scenes/main.tscn`, and `godot/core/` CWN rules. Historical 1d10/Fate prototypes are not authoritative.

**Only NoöPunk extensions may be homebrewed:** modular social relationships/reputation, LaclauGPT-style ideological factions, noösphere/Psyche/ontological shock, and clue-forward PbtA/GUMSHOE-inspired narrative procedures. These are optional **overlays** that invoke CWN rather than overwrite it. Player active PSI remains undecided: prefer passive/minor powers as a design hypothesis, not a locked rule.

## Images

Every picture follows [`docs/ART_DIRECTION_IMAGES.md`](docs/ART_DIRECTION_IMAGES.md): 1970s European comic
illustration, a lived-in Helsinki, and **no sci-fi background unless a scene asks for it and the story
justifies it**. Assets are resolved through `godot/core/image_library.gd`, never by a raw `res://images/...` path in a
scene, and `tools/image_manifest.py` is the checker (`python3 -m unittest tests.test_issue908_image_manifest`) and an
unapproved asset cannot be listed at all. Do not claim an image is imported until the binary is committed and the path resolves.

## Where the lock lives (added with the enforcement PR)

| Artifact | Owns |
| --- | --- |
| This directive | the decision an agent reads first |
| `docs/design/FOUNDATIONAL_LOCK_897.md` | what is locked, the four mechanic classes, the boundary, the narrative pivot |
| `docs/design/CORE_VS_MOD_MATRIX_897.md` | the per-mechanic inventory — **the only copy** |
| `docs/art/ART_BIBLE_1974.md` + `design_tokens.json` | the 1974 visual grammar |
| `docs/ART_DIRECTION.md` + `docs/ART_DIRECTION_IMAGES.md` + `images/manifest.json` | **#908**: the image library — read before generating or integrating artwork; only `approved` assets are loadable, checked by `tools/image_manifest.py` |
| `mods/noopunk/` | the overlays themselves — the only place homebrew rules may live |

**Boundary, enforced by test:** `godot/core/` may not import `mods/`; an overlay returns data and never
mutates a core result in place; a mod that needs a roll asks the core for it
(`tests/test_foundational_lock_897.py`).

**Dormant, not deleted:** the tactical top-down encounter stays in the tree, off the default path. Do not
delete it; do not build on it.

**Before writing anything:** check `git log origin/main --oneline -5` **and** open PRs. Three sessions in
this repository have built the same feature twice because that check happened at merge time instead of
first.

**Current Godot direction changes:** prioritize a Citizen Sleeper-inspired **location-node** Helsinki narrative campaign, discoverable destinations, dialogue/investigation, 1–4 UNSA-agent missions, CWN character sheet, graph-based CWN hacking (DROP-inspired interface) and non-tactical CWN combat resolution. **Suspend** tactical top-down development; preserve existing scenes, saves and tests as compatibility paths until deliberate tested migration. Do not create a second Godot project or delete working systems.

**Visual lock:** everything appears as an acid-fueled 1974 science-fiction vision of 2045: Hawkwind's *Space Ritual*, krautrock, **Zardoz > Barbarella > Rocky Horror**, Mœbius and Valérian. Later media influence mechanics and stories, not the graphic style. Avoid generic 1980s neon cyberpunk. Start from reusable color/type/UI tokens; use original or appropriately licensed assets.

**Agent handoff:** review `docs/design/ISSUE_897_FOUNDATIONAL_LOCK.md` and `docs/design/ISSUE_897_VISUAL_BIBLE.md` before implementation. This is an author decision, not a request to re-litigate rules. Preserve executable-code-only test policy and honest Godot runtime validation.

---

# CURRENT DIRECTIVE — read this first (issue #848, 2026-10-30)

**Vanilla CWN + vanilla SWN + one top-down Godot RPG. This supersedes every earlier restart or
custom-attribute instruction, including #827, #835 and the blank-rulebook plan.**

**Pinned baseline:** commit **`36092a5`** on `main` — the state in which the canonical Godot project
passes **760 headless checks, 0 failed**.

| Canonical artifact | Path |
| --- | --- |
| Rulebook | **`RULEBOOK.md`** (repository root) |
| Generated chapters | `rulebook/` — produced by `python tools/split_rulebook_twelve.py --apply`; never hand-edit |
| Godot project | **`project.godot`** (repository root) |
| Startup scene | **`scenes/main.tscn`** |
| Rules kernels | `godot/core/*.gd` |
| Rules data | `data/rules/*.json` |
| Godot tests | `godot/tests/run_tests.gd` |

**Rules are vanilla.** Cities Without Number is the primary system and governs general mechanics;
Stars Without Number Revised supplies psionics, space and factions where CWN is silent. Attributes
are STR/DEX/CON/INT/WIS/CHA. Character creation, classes, skills, checks (2d6), attacks and saves
(d20), combat, hacking, cyberware, equipment, progression and PSI follow the published rules as
written. Name the governing book for any subsystem you touch.

**Forbidden:** the seven-attribute Fitness/Cognition/Awareness/Agency/Reflexes/Cyber/Empathy design,
alternate difficulty systems, invented mechanics, reskinning, narrativist replacements, new Godot
projects, or starting another prototype.

**Superseded — preserved, not authoritative, do not extend:** `noopunk/` (the blank-rulebook restart),
`noopunk2/` if present, and any `restart/` tree. They remain in the repository as history. Do not
delete them, and do not build on them.

**Before writing anything:** check `origin/main`, name the module you are extending in the PR, and
confirm the project still passes `godot --headless --path . --script res://godot/tests/run_tests.gd`.

**Do not re-litigate this decision in code.** If something here looks wrong, raise it on #848.

---

# Godot single-project directive (2026-10-30; applies to every coding agent)

**ONE GODOT PROJECT:** the repository-root `project.godot` is the only Godot project. Do not create another `project.godot`, standalone demo, competing startup screen, or another save/state/rules engine for the same gameplay. All Godot branches and agents must target this project and its existing `scenes/main.tscn` launch flow. This directive governs the Godot implementation of the RPG; it does not merge the separately authorized Python `strategy_game/` crossover.

**Ownership and migration:** `godot/` is the primary live game, with `godot/core/` for game kernels and state, `godot/ui/` for views, `godot/scenarios/` for the original hospital case and `godot/tests/` for its engine tests. Existing `src/godot/` modules are *compatibility/integration modules* until individually ported or deduplicated, not permission to establish a second game. `scenes/lakkahaltia/ward.tscn` and `prototype.tscn` are existing compatibility fixtures. `scenes/campaign.tscn` is an existing campaign feature reachable from the **same** root menu; do not replace the canonical case or MVP. The project's approved tabletop Without Number baseline applies to every new mechanics implementation.

**Before writing:** inspect `project.godot`, `AGENTS.md`, `docs/godot/ARCHITECTURE_CONSOLIDATION.md`, `docs/godot/UNIFIED_IMPLEMENTATION.md`, and all existing matching scripts in **both** `godot/` and `src/godot/`. Search open PRs and issues for overlapping assignments. Name the canonical module you are extending in the PR. Rebase on current `main` before integration. Coordinate conflicting PRs rather than independently replacing the same file.

**Integration contract:** new user-facing gameplay must be launched by `scenes/main.tscn` through `godot/ui/main_menu.gd`, and must extend an existing scene/state/rules path. If another implementation already supplies the feature, reuse it, port unique behaviour with tests, and then retire its old entry point in the *same tested change*. No alias classes or competing sources of truth merely to hide duplication. Shared rule values come from existing `data/rules/` contracts. Never let legacy `src/godot/core_rules.gd` (old 1d10 mechanics) become the active rules baseline.

**State safety:** the existing hospital `GameState` autoload and the explicit campaign `NooPunkCampaignState` presently have different save schemas. Do not synchronize them by copying fields or make a second autoload. Keep them isolated until a tested versioned migration is implemented; one gameplay session must have exactly one owning state. Preserve player saves and both scenario histories.

**Verification before merging:** import with the pinned Godot version; run the root `godot/tests` suites, the playable integration and smoke checks, and affected `tests/godot` suites. Test actual scene transitions and save/load as executable behaviour. Preserve all existing routes while consolidating. Never claim two implementations were merged merely because their folders coexist or their tests pass. Do not add prose or lore CI gates.

**PR handoff:** list changed gameplay paths, the one canonical entry point, overlapping agents/PRs, migration or compatibility status, tested commands and results, and remaining duplication. If no engine runtime is available, say tests were not run. Never delete a live implementation without proving parity first.

# Current author override — 2026-10-26

Use `rulebook/WITHOUT_NUMBER_BASELINE.md` for all new rules work: CWN primary, SWN PSI/space/factions, AWN crisis survival, WWN otherworld exploration/projects. Standard STR/DEX/CON/INT/WIS/CHA, 3–18 scores, 0–4 skills, 2d6 checks, d20 combat/saves, and source character progression supersede older reservations below. The user explicitly authorized this change; do not ask again whether to preserve d10, Fate, FIT/REF/SOC/CYB/PSY, or the old skill list. Defer bespoke mechanics until later revisions. Keep both games’ world/scenario identities and preserve legacy software pending explicit ports. Tabletop-first and executable-code-only testing policies remain binding. No tests or CI gates for prose.

The earlier directions below are retained for context and apply only where consistent with this override.

# AGENTS.md

## NoöPunk agent rules

These rules are mandatory for coding and documentation agents working in this repository.

**Design invariants.** NoöPunk has three core design balances, documented once in
[`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md). They are project-level
invariants and are restated as binding rules in §13 below. Read that document
before changing rules, mechanics, or setting material.

### Automated tests policy: executable code only

Automated tests and CI assertions must exercise **executable game/software code** (Python, Godot, Concordia, game tools, runtime APIs and behavior). Do **not** add pytest/unittest tests, text-matching assertions, schema-locked canon checks, snapshot guards, or CI gates for **rules, lore, scenario prose, worldbuilding, canon, rulebook structure, design principles, or wording**. The author reviews those materials editorially and through tabletop playtesting; they are not code contracts. Do not recreate removed lore/rulebook tests under new names or add such checks to the code-test suite. Preserve the existing lore and archival material as documentation, not executable tests. When a tabletop mechanic is implemented as code, test the implementation's behavior, not whether prose matches a frozen version.

This policy also covers checks that are not unittest files: do not add documentation gates to `tools/`,
`scripts/`, GitHub Actions, release tooling or hooks, and do not reintroduce a removed documentation
test under a new name, in a renamed file, or as a "smoke" step. If a change removes a documentation
test, that is a **deletion of a test, never of the material the test described** — lore, rules, canon,
scenarios and archives stay.

**What to do instead.** Review creative material by (a) author editorial review, (b) discussion on the
relevant issue, (c) comparing overlapping sources by hand, and (d) **tabletop playtesting**. These are
human processes and must not be converted back into CI gates.

**Every participating agent** must carry this policy in its own NoöPunk-specific instructions and
skill files, wherever they live, and must report the paths it checked in the tracking issue. An agent
that cannot reach a private or external skill file must name the path and the blocker rather than
claim it was updated.

### 0. Active track: the NoöPunk × LaclauGPT crossover game

Directive: issue #306. **Two games, one shared world. Do not collapse them.**

- **Legacy NoöPunk RPG** — `RULEBOOK.md`, `rulebook/`, and the Godot/Concordia ports. Its rules,
  attributes, skill procedures, lifepath, character sheets and gameplay are **not** automatically
  rules of the crossover.
- **Crossover game** — an independently playable Python project in `strategy_game/`, designed to be
  translatable into a physical board/card/dice tabletop game. Its rulebook is
  `strategy_game/RULEBOOK.md`, which currently says **NO RULES APPROVED**; the scaffold code provides
  vocabulary, not playable mechanics.

What carries over, and what does not:

- **Existing world lore generally carries over** from `RULEBOOK.md` and `rulebook/` as canon
  background, subject to explicit scenario deviations and later author decisions. Preserve existing
  characters, institutions and NHI concepts; do not delete or casually overwrite legacy lore.
- **Legacy rules do not carry over.** Cross-references are fine. Importing a legacy mechanic into the
  crossover requires an explicit, approved conversion decision.
- **Timeline.** The crossover begins during the **acceleration toward the NHI Crisis** — recognisable
  everyday institutions and electoral politics that grow stranger as AGI, NHI-disclosure and PSI
  shocks accumulate. The legacy RPG's default later/post-crisis scenario is *not* the crossover's
  starting point, and the NHI Crisis must not be narrated as already resolved.
- **The legacy RPG is not rewritten, replaced or retired.** Changing it needs its own
  author-approved issue.
- New Weird is the overarching genre; Social Science Fiction and dark science-fiction comedy are
  deliberate tonal modes (#303).

Active design tracks: #282 (crossover parent and scaffold), #295 (leader mechanics), #296 (faction
strategy), #297 (discourse and information-network simulation), #302 (country-agnostic society),
#303 (tone, agent ontology, tabletop aesthetics), #304 (optional player agents, GM turns, Tarot),
#305 (paradigm-shift populist realignments), #306 (this directive).

Luhmann supplies differentiated social-system context, Castells supplies network/communication power,
and Laclau/Mouffe supplies contestation of signifiers and frontiers. These are **game inspirations,
not validated predictive transition laws.** Do not embed LaclauGPT's data pipelines, infrastructure or
empirical analyses as game runtime dependencies.

#### 0.1 New-session checklist

1. **Which game?** Legacy RPG or crossover. If a task is ambiguous, ask before editing.
2. **Read first:** the relevant rulebook entrypoint (`RULEBOOK.md`, or `strategy_game/RULEBOOK.md`)
   and the linked issue.
3. **Default new crossover coding and design work to `strategy_game/`.**
4. **Record design decisions** as proposals for author approval. Never invent mechanics, numbers,
   canon or typologies.
5. **Tests cover executable code only**, in either game — see the automated tests policy above.

### 1. Author intent is canon

Do not invent NoöPunk rules, mechanics, lore, history, factions, technologies, metaphysics, organizations, locations, character classes, archetypes, species, NHI categories, psionic powers, skills, attributes, combat systems, progression systems, equipment lists, economies, or world events unless the author has explicitly specified them.

When a required design decision is missing, prefer:
- a neutral placeholder,
- a generic interface,
- an empty data structure,
- a TODO explicitly marked as requiring author specification,
- or no implementation at all.

Do not "helpfully" complete undefined worldbuilding.

### 2. Advance one layer at a time

NoöPunk is intentionally developed slowly.

For each task:
1. implement only what the issue or author explicitly requests;
2. preserve extension points for later design;
3. do not expand scope into adjacent systems;
4. do not turn examples into canon;
5. do not infer mechanics from genre conventions.

The RPG scaffold and the reserved-area list are not permission to create a game system.

### 3. Tabletop first; Godot and Concordia are later ports

NoöPunk is **one computer RPG/simulation**, not separate tabletop, simulation and
videogame products ([`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md),
#48). The tabletop / Godot / Concordia distinction in this section is about notation
and runtime sequence, not about maintaining three products.

This section describes the **legacy NoöPunk RPG only** (see §0). The repository's second game, the
NoöPunk × LaclauGPT crossover in `strategy_game/`, is a separate game with its own rules, scenario and
timeline; the lore/rule boundary is in §0.

The **tabletop-style RPG rules/worldbook are the canonical design source** for NoöPunk.

Development order is binding:

1. define and refine the tabletop rule or world concept;
2. stabilize it through documentation and playtestable procedures;
3. only then convert it into a digital specification;
4. implement that specification in Godot and Concordia.

If a mechanic is unclear, incomplete, or internally inconsistent, fix the tabletop rule first. Do not let Godot, Concordia, UI code, prompts, or platform architecture accidentally invent the missing rule.

The intended RPG rules must ultimately be usable in tabletop, Godot, and Concordia. Game logic should therefore remain data-driven and engine-independent where practical.

Do not bury canonical rules inside scene scripts or UI code. Prefer separable domain data / rule definitions derived from RULEBOOK.md and the worldbook material.

Existing Godot and Concordia scaffolds must be preserved, not deleted, but they are later-stage implementation material until the relevant tabletop systems are stable.

### 4. Current reserved design areas

Issue #51 explicitly revises the earlier six-attribute reservation toward a four-system
ontology: **Physical / Social / Psychic / Cybernetic**. Issue #131 (2026-10-05) now locks
the final attribute names/counts to **six base STATs — Fitness (FIT), Reflexes (REF),
Intelligence (INT), Social (SOC), Cybernetics (CYB) and Psyche (PSY)** — on the **1..10**
scale (issue #111). The charisma/empathy/presence distinctions belong to the Social Systems
layer, and psychic detail to the Psychic Systems layer; cybernetic hardware properties
(processing, bandwidth, storage, hardening, etc.) are statistics of decks, implants, devices
and agents, not character STATs. The general STAT/Skill generation procedure remains unlocked; issue #144 defines the Lifepath framework, UNSA training structure and starting Faction Reputation allocation. Issue #158 now additionally defines the default Helsinki/UNSA Police Academy universal Skill package at rating 3, its capability-level standard augmentation package and its stat-free rookie field kit in `data/rules/unsa_academy.json` and `rulebook/5_CYBERNETIC.md`. `src/rules/tags.py`
remains a non-canonical prototype. The older FIT / REF / INT / CHA / CYB / PSY sketch and its
3d6 generator remain in the digital runtime only as documented porting debt.

Issue #111 supersedes the earlier 2d6 / level-0..4 direction. The active core direction is
an **independent NoöPunk 1–10 STAT + 1–10 Skill + 1d10 system**. Issue #131 locks the STAT
list. Issue #159 locks the canonical universal Skill vocabulary, field-specialization model,
default STAT bindings, and trained-only versus untrained-at--1 status in `RULEBOOK.md` §4.1
and `data/rules/skills.json`.

Issue #110 defines campaign-scoped specialist content under that newer direction. Its provisional skill vocabulary and fields may be documented and represented as data, but agents must not treat Eclipse Phase linked aptitudes, percentile values, or other EP2 numerical mechanics as current NoöPunk rules.

For the default Helsinki / UNSA campaign, only expose specialist fields that actual play needs. The machine-readable profile is `data/rules/campaign_skill_fields.json`; scenario-specific additions should extend the profile instead of creating giant universal catalogs.

Issues #171–#180 add **light, scoped content** in several of the areas below — **lists of
things with brief descriptions**, plus conceptual and light rules — without lifting the
reservation on numeric statistics or full subsystems. The lore and the main catalogs are
`RULEBOOK.md` §§44–50 and `rulebook/9_FIELD_CATALOGS.md`; the follow-up chapter consolidation
adds the **wound ladder** and **equipment list** (`RULEBOOK.md` §§51–52,
`rulebook/3_PHYSICAL.md`) and the expanded **Pauli–Jung / Atmanspacher** detail
(`rulebook/6_PSYCHIC.md`). This content defines **no per-item statistics, no full
combat/damage subsystem, no deep-hacking subsystem, no economy, and no interactive ASI
mechanics**; psi powers remain capabilities resolved with the existing Skill check, and Seity
and subsystem disentanglement remain lore/future-design only.

The earlier issue #17 BCI / Compute / Connection / Infosec cyberspace modifier framework is **withdrawn from active canon**. Do not port it. Hacking / cyberspace is DEFERRED until the author defines an original NoöPunk subsystem.

Until explicitly specified, do not define:
- derived statistics, or any per-layer STAT lists beyond the six base STATs locked by issue #131
- new specialist fields beyond those explicitly enabled by issue #159, a campaign profile, or a character/scenario requirement
- how many skills a starting character has, or at what levels, **except** the issue #158 default Helsinki/UNSA Police Academy package explicitly defined in `data/rules/unsa_academy.json`
- character creation beyond the Lifepath framework and Reputation allocation explicitly specified by issue #144
- character classes or archetypes
- combat resolution
- damage, health, wounds, armor, or initiative
- psionic powers or psionic mechanics
- NHI taxonomy or capabilities
- cyberware / augmentation rules beyond the capability-level standard UNSA package explicitly defined by issue #158
- equipment statistics (issue #158 defines standard rookie equipment availability/capabilities only, not numeric statistics)
- economy
- advancement / XP
- factions beyond the taxonomy and Helsinki-scoped campaign rules explicitly specified by issues #107, #122 and #144
- professions
- detailed geography
- quests or canonical plot
- social mechanics
- hacking / cyberspace mechanics, including whether the withdrawn BCI / Compute / Connection / Infosec concepts return
- vehicles
- magic or supernatural systems
- detailed simulation mechanics

Issue #107 now explicitly specifies the shared **Affect / Faction / Motivation / Reputation / Contacts** representation and the text-forward location/social/mission architecture. Treat [rulebook/4_SOCIAL.md](rulebook/4_SOCIAL.md) and [docs/design/GAMEPLAY_LOOP.md](docs/design/GAMEPLAY_LOOP.md) as author-specified for those areas. The exact persuasion formulas, Contact generation counts/tables, universal Affect-score increments, and propagation algorithms remain undefined.

These may be represented only by clearly empty extension points when needed by the requested architecture.

### 5. Setting constraints

Treat NoöPunk as an **alternate Eclipse Phase timeline set before the Fall**, combining Noösphere + Cyberpunk inside that transhuman setting.

Canonical anchors are: **20XX**, **Earth still exists**, **the Fall has not happened**, and **the technology level is broadly Eclipse Phase-level**.

The cyberpunk layer remains technological, political, economic, and social cyberpunk. Do not convert it into fantasy.

The speculative consciousness / NHI layer draws inspiration from sources identified by the author, including Teilhard de Chardin, **Ben Goertzel**, Alexander Wendt, Jacques Vallée, Dean Radin, Federico Faggin, and Donald Hoffman. Issue #154 makes Goertzel's Cosmism, patternism, Global Brain / mindplex work, and selected PSI/consciousness research an explicit design source while preserving NoöPunk's pluralism and epistemic uncertainty.

The issue #154 research map is `docs/design/COSMISM_NEUROPUNK_IA_AUDIT.md`. Treat its PRESENT / PARTIAL / MISSING / OPTIONAL labels as an audit and future-design roadmap, not permission to implement undefined mechanics or promote every speculative source claim to setting truth.

Do not present speculative setting assumptions as established real-world scientific facts.

### 6. Background timeline discipline

Canonical future dates are written as **20XX** unless the author explicitly says otherwise.

Ray Kurzweil's 2045 Singularity is a thematic and intellectual reference, not the canonical
date of the setting. Agents must not assign exact future dates on their own.

The background timeline is a set of **unordered paradigm shifts**, not a prediction of a
single future chronology. Treat the following as binding:

- describe the major changes that create the NoöPunk world without inventing exact dates;
- do not infer a global "first this, then that" sequence unless the dependency is explicit canon;
- do not turn a numbered list, document order, or vivid narrative example into chronology;
- keep Cyberpunk intensification, the AI/AGI revolution, the QIP/PSI scientific revolution,
  UFO/NHI Disclosure, and Noösphere emergence conceptually distinct even when they interact;
- **QIP/PSI must arise independently of UFO/NHI Disclosure**. Disclosure may later reshape
  its interpretation, but it is not the source of the scientific breakthrough;
- write canonical background at the level of paradigm shifts, geopolitical consequences,
  technologies, ideologies, scientific revolutions, and social transformations rather than
  minute-by-minute incident narration;
- preserve detailed raids, speeches, crisis sequences, national disclosure cascades, and
  other cinematic variants in `docs/archive/NARRATIVE_TIMELINE_VARIANTS.md`, not as the
  canonical chronology;
- if chronology is genuinely required by a specific scenario, label it as scenario-local or
  a narrative variant unless the author explicitly promotes it to canon.

### 6.1 Real people and fictional 20XX actors

Real-world scholars, scientists, philosophers, writers, and theorists may retain their real
names when NoöPunk is attributing ideas or intellectual influence.

Political, corporate, military, media, and celebrity figures acting **inside fictional
20XX** should normally be fictionalized. Preserve the recognizable social role or inspiration
when useful, but do not automatically carry a living real person into the future-history
narrative.

Examples of acceptable real-name attribution include Federico Faggin, Donald Hoffman,
Dean Radin, Jacques Vallée, Diana Walsh Pasulka, Alexander Wendt, and Ray Kurzweil when
cited as intellectual influences.

Archived drafts containing real public figures remain archive material; agents must not
silently restore them as active canon.

### 7. Retrocyberpunk tone is not a license to add lore

Recognized influences include old-school Cyberpunk, Shadowrun, Philip K. Dick, Hawkwind, and 1970s space psychedelia.

Those remain tonal/comparative references. **Eclipse Phase is also an influence, not NoöPunk's parent rules engine.** It remains valuable for transhuman technology, morphs/embodiment, mesh, reputation, space and existential-risk concepts. Use directly adapted EP material only within the applicable licensing and attribution boundaries, and preserve provenance rather than treating EP2 mechanics as automatic defaults.

### 8. Minimal Godot foundation

When asked to create the initial Godot RPG base, build only generic infrastructure needed for later author-defined systems, such as:
- a valid Godot project
- minimal project structure
- a bootstrap/main scene
- generic navigation or test scene if necessary
- reusable data/resource architecture
- save/load interface skeleton if explicitly useful and still content-neutral
- tests or validation appropriate to the scaffold
- documentation of extension points

Do not implement speculative gameplay systems merely to demonstrate architecture.

### 9. RULEBOOK.md is intentionally incomplete

RULEBOOK.md is the source for tabletop-compatible game rules as they are specified.

Agents may improve its organization and add explicitly requested rules, but must preserve unresolved sections as unresolved.

Never fill a blank section using "standard RPG rules."

### 10. Prefer reversible architecture

At this stage:
- keep dependencies minimal;
- avoid premature frameworks;
- avoid deep inheritance trees;
- avoid hard-coded canon;
- keep content separate from engine plumbing;
- make changes easy to replace after later design decisions.

When uncertain, choose the smaller implementation.


### 11. One RPG, three runtimes, developed in sequence

> **Scope (§0, issue #306):** this section governs the **legacy** NoöPunk RPG. The NoöPunk ×
> LaclauGPT crossover game in `strategy_game/` is a separate, independently playable project with its
> own rulebook and its own rules track. "One RPG, three runtimes" remains true of the legacy RPG; it
> is not a claim that NoöPunk is a single game.

NoöPunk is one RPG rules/world model. It is developed as **one computer
RPG/simulation**, and the three headings below are notation/runtime choices within
that single game rather than three products to maintain
([`docs/archive/NOOPUNK_AS_ONE_GAME.md`](docs/archive/NOOPUNK_AS_ONE_GAME.md), #48):

- tabletop-style notation — how the rules are written and read
- Concordia — the generative-agent / Game Master runtime
- Godot — a possible *future* frontend, not a planned parallel runtime

These are implementations of the same game, not separate rule systems, but they are **not developed in parallel by default**. The tabletop version comes first and acts as the executable human specification. Godot and Concordia follow as staged conversions after the relevant tabletop systems are stable.

Concordia-specific agents must not invent alternate mechanics, lore, statistics, or canonical facts to make simulation easier. If a shared rule or world concept is undefined, leave it undefined or use clearly non-canonical fixtures.

Godot and Concordia may have different adapters and runtime plumbing, but canonical rules/data should remain shared or convertible wherever practical.

### 12. Concordia and Ollama constraints

When implementing the Concordia runtime:

- use Google DeepMind Concordia as the agent-based simulation/RPG framework;
- design for local Ollama-served LLMs for GM and NPC agents;
- allow an optional human-controlled player to participate alongside LLM agents;
- keep the LLM provider behind a replaceable adapter/configuration boundary;
- do not hard-code a particular Ollama model as canon unless the author specifies one;
- do not create NPC personalities, factions, plots, psionic abilities, skills, additional attributes, or world facts unless explicitly specified;
- use deterministic shared code for dice and numeric resolution when available; never ask the LLM to invent dice outcomes or canonical numeric mechanics;
- do not let prompts silently become canon;
- keep prompts/configuration separate from canonical RPG rules and world data;
- preserve the same tabletop ↔ Godot ↔ Concordia rule semantics wherever practical.

The first Concordia implementation should be infrastructure only: runnable simulation plumbing, agent/GM interfaces, Ollama connection boundaries, optional human input, and empty world/rule hooks. Do not advance into substantive simulation design without a separate author task.

### 13. Preserve the three design balances

NoöPunk's canonical design invariants are documented once in [`docs/archive/DESIGN_PRINCIPLES.md`](docs/archive/DESIGN_PRINCIPLES.md). Every contributing agent must preserve them:

1. Preserve the **Gamism / Narrativism / Simulationism balance**, with issue #51's current priority: **Narrativist experience + Simulationist world + Gamist friction**.
2. Use **CY_BORG** (Gamism), **Cyberpunk 2020** (Simulationism), and **The Sprawl** (Narrativism) as the canonical reference poles; use **The Veil** as a complementary Narrativist reference.
3. Preserve **rules/mechanics parity** between Tabletop, Godot and Concordia wherever possible, while developing them in the order **Tabletop → Godot/Concordia** rather than in parallel.
4. Allow scenarios and medium-specific presentation to diverge.
5. Preserve the **Cyberpunk / Noösphere balance**.
6. Treat **UFO Disclosure, Psionics and Panpsychism** as the defining Noösphere paradigm shifts.
7. Treat **Shadowrun** and **Eclipse Phase** as comparative/design influences, not mechanical templates.
8. Do not silently redesign these balances. If an implementation requires a departure, document the reason explicitly.
9. Treat NoöPunk as an **independent rules system inspired by multiple games**. No external RPG supplies the default chassis; issue #111's 1–10 STAT + 1–10 Skill + 1d10 core is the active baseline.

Practical consequences:

- Prefer noösphere content that stays science-fictional, philosophical and speculative; do not let it become generic fantasy magic.
- Do not collapse the game into a single creative agenda. Narrativism is the foreground experience, Simulationism supplies persistent causal grounding, and Gamism supplies pressure and consequential choice.
- A scenario, mission, map, or presentation difference between Tabletop, Godot and Concordia is expected and permitted. A **rules** difference is a defect: extract a shared specification rather than fork the rule.
- Where a shared specification already exists (for example `data/rules/core.json` over `src/rules/core.py`), consume it rather than re-declaring the same values in a second runtime.

These invariants are binding on every agent, but they are **not** enforced by an automated test: per the policy above, tests cover executable code only, and creative documents are reviewed editorially and by playtesting. There is deliberately no build gate on document agreement.


### 14. Tabletop-first porting gate

Before implementing or extending a substantive Godot or Concordia gameplay system, agents must check:

1. Is the mechanic or world concept explicitly defined in the tabletop rules/worldbook?
2. Is its terminology and procedure coherent enough to play without software?
3. Are important edge cases documented or consciously left unresolved?
4. If not, stop at the tabletop layer and improve that source first.
5. If yes, convert it as **tabletop rule → digital specification → Godot implementation → Concordia implementation**.

Platform-specific differences must be documented as adaptations. They must not silently become new canonical rules.

Scenarios, UI, pacing, maps, presentation, automation, and other medium-specific features may diverge where appropriate. Core rules, mechanics, terminology, and world canon should not.

### 15. Independent-system rule and Eclipse Phase provenance

**NoöPunk is an independent RPG system inspired by multiple games. Eclipse Phase is not the current mechanical chassis.**

When adding or revising mechanics:

1. begin from the current author direction in issue #111 and RULEBOOK.md;
2. preserve the canonical 1–10 STAT + 1–10 Skill + 1d10 core unless explicitly revised;
3. use Cyberpunk 2020/RED, Eclipse Phase, Fate, PbtA, OSR/Cities Without Number, Citizen Sleeper, The Expanse and other games as selective design references, not automatic rules;
4. keep unresolved systems unresolved rather than importing a familiar solution from another game;
5. record directly adapted material with appropriate source, license and modification provenance;
6. prefer the smallest NoöPunk-native procedure that serves the game's human and Concordia/LLM play.

Setting work should preserve current 20XX / Earth-intact anchors unless the author explicitly revises them.

### Tomi's drafts: two synchronised implementations (#814)

Tomi is the authorial source of truth. When a draft arrives, read
[`docs/design/TOMI_DRAFT_WORKFLOW.md`](docs/design/TOMI_DRAFT_WORKFLOW.md) first.

- **One section or scenario per task.** No speculative expansion into neighbouring rules.
- **Two outputs:** tabletop text *and* the Godot implementation, expressing the same rules. Platform
  differences are documented, not smuggled.
- **Never fill a gap in the draft with a plausible invention.** An undecided mechanic is a question for
  Tomi; record it and stop.
- **Every draft gets its own child issue**, linked back to #814. Template:
  `.github/ISSUE_TEMPLATE/tomi_draft_child.md`.
- **Never close #814**, including via `Fixes`/`Closes` keywords in a PR.

## Godot rule-module ownership clarification (#791)

`godot/core/` is the canonical owner of CWN/SWN game-rule implementations. `src/godot/` remains a compatibility tree only. Port unique capabilities and preserve consumers and tests before retiring duplicates. The two catalogue APIs differ (instance ID lookup vs static named catalogue lookup), so do not mechanically repoint either caller. See `docs/godot/CANONICAL_GODOT_TREE.md` and `docs/godot/UNIFIED_IMPLEMENTATION.md`.


## SUPERSEDED: issue #827 restart — do not follow (#848, 2026-10-30)

> The section below is **obsolete**. It named `noopunk/rulebook/RULEBOOK.md` and
> `noopunk/game/project.godot` as the canonical artifacts; **#848 reversed that**, and the CURRENT
> DIRECTIVE at the top of this file is authoritative. `noopunk/` is preserved history only.
>
> Kept so the record of the decision survives, not as instruction.

## ~~NEW AUTHORITATIVE RESTART: issue #827~~

For all **new NoöPunk RPG development**, the canonical artifacts are `noopunk/rulebook/RULEBOOK.md` and the standalone minimal Godot project `noopunk/game/project.godot`. These two paths supersede the earlier root-project-only and #814 rules **for the restart**, while legacy files elsewhere remain preserved reference material. Do not extend older Godot or rulebook code for new tasks, and do not spawn other alternatives. Tomi defines one small feature at a time; update both of these SAME canonical artifacts together and verify their parity. Do not automatically import legacy CWN/SWN rules, seven attributes, lore, or frameworks. First milestone: blank rulebook and top-down player movement only. Keep meta-issue #827 open; close only implementation child issues. See `noopunk/README.md`.

## FOUNDATIONAL LOCK: CWN is the rules engine (#897, 2026-10-31)

**Permanent, and it outranks earlier ruleset directions.** CWN governs every procedure it covers, as
written. SWN/WWN fill gaps CWN does not cover, whole-procedure, one row each. NoöPunk material is a
**mod, never an edit**: it reads CWN state and adds narrative state, and may not change a CWN target
number, die, band or progression cost. Reskin is free; new mechanics are a documented mod with a test.

Canonical record and the core-versus-mod matrix: [`docs/rules/RULES_BASIS_LOCK.md`](docs/rules/RULES_BASIS_LOCK.md).
Baseline paths remain root `project.godot`, `scenes/main.tscn`, `godot/core/`, `data/rules/`.

No further core-rule replacement by default. Replacing CWN requires a separately approved foundational
decision; brainstorming a mechanic does not authorise it. The seven-attribute UNSA sheet (#835) is a
**mod**, not the baseline.


## Two games, one repository (#946)

**NoöPunk Godot** is the graphical game: `project.godot`, `godot/`, `scenes/`.
**NoöPunk MUD** is a separate text multiplayer game under `mud/` (Evennia + Python), sharing canon and CWN
rules but **no runtime**.

- Identify the target game before editing. MUD work stays under `mud/`; Godot work stays in the Godot tree.
- No cross-imports: `mud/` must not reference `res://`, `.gd` or `.tscn`; Godot code must not import `mud.*`.
  `tests/test_mud_godot_boundary.py` enforces both directions.
- CWN is shared input, never forked. Noösphere, ideology, social ties and ontological shock are modules on
  top of the baseline.
