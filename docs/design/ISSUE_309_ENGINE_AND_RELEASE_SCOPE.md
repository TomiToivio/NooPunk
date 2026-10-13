# #309 §8 — candidate engines, and the S1 release scope

**Status: research and a scope statement. Nothing here is approved.**

This record delivers the first two of the four items that `docs/design/VISION.md` still lists as
open under §9 — **candidate engines** and the **release-scope statement** — and it closes no item by
itself. It fixes **scope, not rules**: it selects no mechanic, no number, no threshold and no
canonical content, and no count in it is anything but a **provisional envelope for S0-A**.

- **The engine survey is a proposal for the author.** `VISION.md` §9 requires these findings to be
  kept **non-binding**, and `docs/design/VISION.md` §7a's seventh line makes the shipped game's
  tooling the author's call. The recommendation in §1.4 is evidence-backed and explicitly falsifiable;
  it is not a decision.
- **The scope statement in §2 is derived, not invented.** Every clause traces to `VISION.md` §7,
  §7a or §7b, which already landed. Where the source text leaves a count open, this record leaves it
  open and says so.

Sources read for this record: issue [#309](https://github.com/TomiToivio/NooPunk/issues/309) body and
all comments, [`AGENTS.md`](../../AGENTS.md), [`VISION.md`](VISION.md) §7 · §7a · §7b · §8 · §9,
[`strategy_game/docs/INTERFACE_SPIKE.md`](../../strategy_game/docs/INTERFACE_SPIKE.md),
[`NOOPUNK_GLOBAL.md`](NOOPUNK_GLOBAL.md) §11,
[`ISSUE_231_RELEASE_PACKAGING_GUARD.md`](../licenses/ISSUE_231_RELEASE_PACKAGING_GUARD.md),
`strategy_game/render/`, `strategy_game/tests/test_render_text.py`, `tools/release_packaging_guard.py`.

## 0. The constraint set both answers must satisfy

Stated once, so the two sections below can be read against it rather than restating it.

**From `VISION.md` §7a — hard requirements of the project, not aspirations:**

1. Source released under an **OSI-approved licence chosen by the author**, and it must be **possible
   to build and run the game from source with ordinary dependencies, offline, without an account and
   without a service.**
2. **Non-commercial sources stay out of the release** (Eclipse Phase-derived material, CC BY-NC-SA,
   and the EP2 homebrew prototype with it).
3. **Nothing proprietary is depended on** — no commercial game's code, assets or rules text is
   copied, linked or required.
4. Every third-party asset carries provenance; contributions are traceable.
5. **It must be moddable, and the data formats documented.**
6. Sustainability is an author decision; the core game is not paywalled.
7. **No feature may require a live service, a proprietary engine or a paid model provider to be
   playable.**

**From `VISION.md` §7b — the MVP's hard caps (provisional envelopes for S0-A):**

- **No engine work**: *2D or text-readable overhead map only. No 3D, no art production, no engine
  migration.*
- **One resolution mechanism, reused everywhere** — not one per pillar.
- No required model, service or account; optional LLM support is off by default and its absence must
  leave a complete game.
- No multiplayer, no space, no economy simulation, no mod UI — documented data files only.

**From `VISION.md` §8 — the non-goal that governs any dependency:**

- *Do not add a dependency that stops the game being built and run from source, offline, without an
  account and without a paid service.*

**Already landed, and binding on any renderer:**

- `strategy_game/docs/INTERFACE_SPIKE.md` §"The criteria" — six criteria, of which the load-bearing
  three for an engine choice are: **criterion 2** (no proprietary engine; Godot is MIT and therefore
  passes, a paid engine would not), **criterion 3** (no rule written twice: the Python engine stays
  authoritative and the UI animates the engine's *recorded* result; no rule belongs in a scene
  script), and **criterion 5** (a renderer consumes declared state through the reserved
  **`MapProvider`** seam and infers no borders, travel, control or ownership).
- `NOOPUNK_GLOBAL.md` §11 — recommends **Approach 2, "tabletop-like digital first"**: a board/card
  interface where *the computer transparently holds centralities, coupled system effects, hidden
  info, rival AI and event scheduling*, while the player keeps only the legible quantity conventions.
  It records that Approaches 1 (strict tabletop-complete core) and 3 (hybrid companion) survive as
  **design constraints** the digital game can still honour — a printed simplified subset, and an
  optional companion app that must state which turn operations stop working when it is switched off.

## 1. Candidate engines

### 1.1 The test a candidate must pass

A candidate is judged on five things, in this order. The first three are pass/fail; the last two rank
whatever survives.

| # | Test | Source |
|---|---|---|
| T1 | **Runnable from source, offline, without an account and without a service.** | §7a line 1; §8 |
| T2 | **No proprietary engine, no live service, no paid model provider required to play.** | §7a line 7 |
| T3 | **No rule written twice in two languages** — anything that renders must be a *view* over the authoritative Python engine's recorded results, with no rule in a scene script or in JavaScript. | INTERFACE_SPIKE criterion 3; §7b "one resolution mechanism, reused everywhere" |
| T4 | **Presentation ceiling** it can reach inside §7b's *"2D or text-readable overhead map only, no art production"* cap. | §7b |
| T5 | **Packaging, platform and provenance cost** it imposes on an offline, buildable-from-source release. | §7a lines 1, 4, 5 |

### 1.2 Candidates surveyed

Four families, named as the issue names them.

#### A. A pure-Python standard-library runtime

**What it is.** The authoritative simulation is Python using only the standard library; the board is
rendered as deterministic text (or as SVG/HTML written out as data), and no third-party distribution
is imported at runtime.

**Evidence that this is not a hypothesis but the current state.** `strategy_game/render/` exists as
its own subpackage with its own `__init__` and `__main__`; `TextMapProvider.describe(state)` fills the
reserved `MapProvider` seam and returns the board projection plus a renderer version, adding **no**
inferred key; `render_board_text(state)` renders the board; `python -m strategy_game.render
[--world FILE | --empty] [--cards] [--json]` is the entry point. The provider already emits a
**portable payload** (`--json`), which is what makes a second renderer additive rather than a second
engine.

**And the requirement is already mechanically protected.** `strategy_game/tests/test_render_text.py`,
class `OfflineImportTests`, runs a subprocess whose `sys.path` **carries no third-party
distributions** and imports `strategy_game.core`, `.view`, `.characters`, `.tabletop` and `.render`.
Its docstring names §7a as the requirement it enforces. That is an executable-code assertion
(`AGENTS.md` / [#271](https://github.com/TomiToivio/NooPunk/issues/271) permits it) and it is the one
test that actually holds T1 in place, rather than asserting it in prose.

| Test | Verdict |
|---|---|
| T1 | **Pass**, and guarded by a test today. |
| T2 | **Pass.** No engine, no service, no provider. |
| T3 | **Pass trivially** — it *is* the authoritative engine; there is no second language. |
| T4 | **Text-readable overhead map: pass.** §7b explicitly allows it. A *graphical* 2D map is beyond the stdlib alone. |
| T5 | **Lowest possible.** No bundled interpreter beyond Python itself, no dependency licences, no per-OS build matrix for S1-a. |

**Finding.** The stdlib runtime is not one candidate among four for the *authoritative core* — it is
the only family that passes T1 and T3 unconditionally. The open question is only what renders over
it, and §7b forbids answering that question with engine work inside S1-a.

#### B. Qt / PySide6 + `QGraphicsView`

**What it is.** A native desktop 2D view: a `QGraphicsScene`/`QGraphicsView` board fed by the same
`describe()` payload.

**Licence.** PySide6 is offered under **LGPLv3**, GPLv3 or a commercial licence. LGPLv3 is
OSI-approved and does not make the engine "proprietary" in §7a's sense; dynamic linking plus notices
is the normal compliance path. So this family is **not disqualified by §7a** — a distinction worth
making, because it is the one native-toolkit option that survives T2.

**Where it costs.** Qt ships large prebuilt binary wheels per platform; the release gains a binary
dependency, a dependency-licence notice obligation, and a per-OS packaging surface (T5). For a game
whose MVP is defined as *"2D or text-readable overhead map only; no engine work"* (§7b), adopting Qt
**inside S1-a** would be exactly the engine work §7b defers.

| Test | Verdict |
|---|---|
| T1 | **Pass**, with a pip-installable ordinary dependency; "offline" means the wheels must be present, which is the same position the repository already takes for `requirements.txt`. |
| T2 | **Pass.** Free software, no service, no provider. |
| T3 | **Pass only if it is a pure view.** The moment a `QGraphicsItem` computes a rule, it fails. |
| T4 | **High** — real 2D graphics, portraits and panels are reachable. |
| T5 | **Moderate.** Qt's own size and licence notices; three platform bundles. |

**Finding.** Legitimate for **S1-b/S1-c presentation**, out of scope for **S1-a** by §7b.

#### C. Python service + web canvas / SVG

This family splits into two, and the split is the whole finding.

**C1 — a *static* browser view over the engine's exported payload.** The engine writes the same JSON
it already emits (`--json`); a single HTML/JS/SVG file renders it. No server runs at play time.

| Test | Verdict |
|---|---|
| T1 | **Pass.** A local file opened in a browser needs no account, no service and no network. |
| T2 | **Pass.** No engine, and the browser is the platform, not a dependency of the build. |
| T3 | **Pass if the JS renders and never decides** — which is what consuming a *recorded* payload means: the projection is already the engine's answer, so there is no rule to duplicate. |
| T4 | **High and cheap** — 2D vector graphics, and by a wide margin the best accessibility and font/DOM story. |
| T5 | **Lowest of the graphical options.** No per-OS binary build at all; a browser is the runtime. |

**C2 — a Python service (Flask/FastAPI and friends) serving a web canvas.** The game needs a running
server process to be played.

> **DISQUALIFIED by §7a, not merely unfavoured.** §7a line 7: *no feature may require a live service
> … to be playable.* A required serving process is a live service under §7a line 1's *"without an
> account and without a service"*, and `INTERFACE_SPIKE.md` already rejected this family in its own
> option D for *adding a runtime dependency and a service, breaking criterion 1*.

**Finding.** C1 is the natural next renderer and is additive; C2 is out by the rules, whatever its
ergonomics.

#### D. Godot ↔ Python with an explicit structured command interface

**What it is.** The legacy Godot scaffold renders; Python stays authoritative; the two talk over an
explicit, documented, structured command interface rather than Godot calling into rule logic.

**Licence.** The MIT engine passes INTERFACE_SPIKE criterion 2 by name — *"Godot is MIT, so reusing
the legacy scaffold passes"*. `AGENTS.md` §3 additionally forbids deleting the scaffold, so
preservation is already the position.

**Where it costs — and the two traps.**

1. **The rule-written-twice trap.** A Python↔Godot bridge makes it *easy* to reimplement a rule in
   GDScript "just for the animation". INTERFACE_SPIKE criterion 3 is precisely the guard: Godot must
   be a **view** that animates the engine's *recorded* result, and no rule belongs in a scene script.
   The structured command interface is what makes that enforceable — an untyped bridge into engine
   internals is what makes it erodable.
2. **The S0 gate trap.** The Godot RPG scene is **behind Gate A** and therefore *not before the
   author rules*; `AGENTS.md` §14's tabletop-first porting gate applies. So Godot cannot be the S1-a
   renderer even if the author later chooses it for S1-b.

A third, smaller cost: a Godot project that requires the *editor* to build is heavier than "ordinary
dependencies"; an export-template path must be documented for the §7a guarantee to be auditable.

| Test | Verdict |
|---|---|
| T1 | **Pass with a documented export/build path**; the running Godot process is a local process, not a live service, so T2 is unaffected. |
| T2 | **Pass** (MIT). |
| T3 | **Pass only with the explicit structured command interface** — the condition in the candidate's own name. |
| T4 | **High**, and already scaffolded. |
| T5 | **Highest of the surviving options.** Engine build tooling, export templates, scene/asset provenance, a heavier repository. |

**Finding.** A legitimate **S1-b/S1-c view-only** candidate, preserved as an option, contingent on the
structured command interface and the author's decision — never a required part of S1-a.

#### E. Other families, classified

- **Proprietary/commercial engines** (Unity, Unreal, GameMaker and their kin), and a **total
  conversion of someone else's proprietary game** shipped as the product: **DISQUALIFIED by §7a** —
  line 3 (*nothing proprietary is depended on*) and line 7 (*no proprietary engine*), reinforced by
  §6's *"a total conversion must never be presumed releasable as a standalone product"*.
- **Any design where a paid model provider is required to play**: **DISQUALIFIED by §7a** line 7.
  A local, optional provider stays permitted precisely because §7b makes its absence leave a complete
  game — the disqualification is about *requirement*, not about models existing.
- **Hosted/cloud engines, managed game backends and authoritative-server-first architectures**:
  **DISQUALIFIED by §7a** (live service), and §8 forbids adding a dependency that breaks
  source-offline play.
- **A native rewrite** (Rust/C++ core, or any second implementation of the simulation):
  **not disqualified, but out of scope now.** It breaks nothing in §7a on licence grounds, yet it
  violates §7b's *no engine migration*, `AGENTS.md` §2 (one layer at a time) and §10 (prefer the
  smaller implementation), and it would put the rules in two languages — T3 — the moment the Python
  engine remained authoritative. Recorded as *available later*, not as a candidate.
- **Library additions that are not engines** — NetworkX, Pydantic, Mesa: permitted candidates under
  `VISION.md` §5, and `VISION.md` §14 states the discipline: *"Select libraries only when an approved
  requirement makes the standard-library approach inadequate."* They do not change the engine answer;
  they are a consequence of a rule selection that does not exist yet.

### 1.3 Disqualified, collected

For the record, so that a later proposal cannot present any of these as a live option:

| Disqualified | By |
|---|---|
| A required live service (hosted server, managed backend, service-based renderer) | §7a line 7; §7a line 1; §8 |
| A proprietary engine (Unity, Unreal, GameMaker, and any paid toolkit) | §7a lines 3, 7 |
| A required paid model provider | §7a line 7 |
| A total conversion of a proprietary game as the product | §7a line 3; §6 |
| Any NC-SA-derived material entering a distributable build | §7a line 2 |

### 1.4 Recommendation — **a proposal for the author, non-binding**

**Keep the pure-Python standard-library runtime as the authoritative engine through S1-a, and make
the static browser/HTML+SVG view (candidate C1, INTERFACE_SPIKE's own "option B — next step") the
recommended next presentation increment. Treat Qt/PySide6 (B) and Godot-as-a-view (D) as S1-b/S1-c
candidates that the author decides between, and treat the whole engine question as settled for S1-a
by §7b rather than by preference.**

The evidence, in the order it weighs:

1. **§7b already decided S1-a's renderer, and it is not an engine.** *"No engine work: 2D or
   text-readable overhead map only."* The recommendation only follows the landed text. Choosing Qt or
   Godot for S1-a would require the author to change §7b first.
2. **T1 and T3 are the two tests that cannot be traded, and only family A passes them
   unconditionally** — with a *test* holding T1 (`OfflineImportTests`), and no second language in
   which a rule could be written (T3).
3. **The next increment is already additive, which is the strongest available argument.** Because
   `TextMapProvider.describe()` emits a portable payload, C1 needs **no engine change and no new
   rule** — INTERFACE_SPIKE's own reason for putting option B next. An engine choice, by contrast,
   requires work before it can render anything.
4. **C1 dominates B and D on T5 and T4 jointly.** It reaches the best presentation ceiling at the
   lowest packaging and provenance cost, and imposes no per-OS build on a project whose §7a guarantee
   is *buildable from source*. It is also the only graphical option that keeps the
   *"one platform, many machines"* property a tiny team needs.
5. **`NOOPUNK_GLOBAL.md` §11's Approach 2 is the same architecture from the other direction.** Its
   justification is that *"the computer must carry the derived and hidden quantities"* while the
   player keeps the legible ones — which is a Python core plus a thin view, not an engine. Its
   Approach 3 (hybrid companion) survives as a constraint this recommendation honours: the same
   declared data can be printed, because the view consumes data rather than owning rules.

**What would falsify this.** Three things, and any one of them is enough to reopen the question:
(i) S1-b's *"appealing 2D interface"* (§7 S1-b) turning out to be unreachable in SVG/HTML to a
standard the author accepts; (ii) an approved rule requiring a rendering capability the payload
contract cannot express without a rule leaking into the view (T3); (iii) the author's own preference,
since §7a's last line makes the shipped tooling their call.

### 1.5 What this section does not decide

- **Not the engine.** A proposal, marked as one, explicitly non-binding per §9.
- **No rule, threshold, cadence or effect.** Gates A–D in `docs/RULE_SYSTEM_RESEARCH.md` are untouched.
- **Not the library set.** NetworkX/Pydantic/Mesa remain candidates and remain conditional on a rule
  selection that does not exist.
- **Not the scene, scenario or content** — no canonical actor, map or incident is named here.

## 2. The S1 release-scope statement

`VISION.md` §9 asks for *"exactly what S1 must contain to count as shippable, and what is explicitly
deferred to S2/S3."* This section states that, using only landed text.

### 2.1 The bar that decides everything: one loop, not three features

`VISION.md` §7b names the property, and it is quoted here because every clause below exists to
protect it:

> the three pillars must **feed each other in one loop**. A leader's decision changes faction
> standing; that changes discourse; that changes who cooperates; that creates the next personal
> decision. **If the pillars are three disconnected mini-games sharing a menu, the MVP has failed
> even if all three exist.**

That sentence is the acceptance test for S1-a. Three pillars exist and do not interlock → the
release does not count, however complete each pillar looks in isolation.

### 2.2 What S1-a must contain to count as shippable

S1-a **is** the MVP: `VISION.md` §7 states *"S1-a — first public playable: the MVP"* and §7b closes
with *"The MVP is the target of S1-a."* So the scope statement for S1-a is §7b plus S1-a's own three
lines, and nothing else. Concretely, in nine clauses:

1. **One small scenario containing the Strategy, Simulation and RPG pillars at reduced scale in a
   single loop** (§7 S1-a). Reduced scale means §7b's "It need **not** have yet" column: no deep
   economy or military stacks or tech tree; no full Laclau–Castells depth or measured-hegemony claim;
   no lifepath depth, large cast or dialogue trees.
2. **The interlocking property of §2.1 above, demonstrated.** Each pillar must read the others'
   output — *"removing any one of them would obviously break the game"* (§7b definition of done 3).
3. **One map, one scenario, one finite campaign, one sitting, with a real ending** (§7b hard caps).
   No second map and no campaign selector.
4. **One resolution mechanism reused everywhere, not one per pillar** (§7b hard caps).
5. **A legible overhead map with contextual panels, text-readable or 2D only, with no engine work**
   (§7, §7b). Per §1.4 that is satisfied today by the `render/` text view; a browser renderer would
   satisfy it too without adding an engine.
6. **A documented save format, and saves and loads** (§7 S1-a).
7. **A closing summary that explains what changed and why** (§7 S1); §7b's definition of done 2
   sharpens it to *"every meaningful change has an inspectable in-game reason"*.
8. **Runnable from source, offline, with no account and no service; no required LLM, database or
   network service** (§7 S1, §7a). This is the same clause the existing `OfflineImportTests` guards,
   so it is a release state the repository can already demonstrate.
9. **Published open source with a licence, a README, and a documented save format** (§7 S1-a) —
   **and this is the one clause that cannot be completed by an agent.**

### 2.3 The one S1-a clause that is blocked, and by what

Clause 9 says *"a licence"*. That licence does not exist yet, and three independent pieces of landed
evidence say so rather than one agent's opinion:

- `data/licenses/release_packaging_policy.json` carries `"status":
  "guard-scaffold-author-decision-still-open"` and `"author_decision_open": true`.
- `tools/release_packaging_guard.py` in `--mode public` **fails by design while that flag is true**,
  and its own documentation states the reason: *"The guard is meant to keep failing in public mode
  until the author selects a licence. That is the point: the failure is the record that the decision
  is still open."*
- Issue [#421](https://github.com/TomiToivio/NooPunk/issues/421) tracks the licence selection and the
  release-time clean-up, because #309 §9 asked for a carrier and nothing else had one.

**Consequence, stated plainly:** S1-a is *shippable in design and content* but *not releasable in
fact* until [#421](https://github.com/TomiToivio/NooPunk/issues/421) closes. A release cannot be
declared clean on an unmade licence choice, and the repository's own guard refuses to let anyone
pretend otherwise. That is the correct behaviour and this record does not work around it.

### 2.4 Explicitly deferred — what S1-a does not contain

**Deferred to S1-b** (from §7 S1-b, verbatim in substance): character creation and lifepath; leaders
and agents beyond the MVP's thin version; discourse and network play beyond the MVP's thin version;
geopolitics; scenario authoring; an appealing 2D interface; saves and replay; a complete
NHI-acceleration campaign; documented modding and scenario data formats.

**Deferred to S1-c** (§7 S1-c): balance and accessibility work; contributor documentation; a
contribution and provenance process; a content-licence statement; **a UGC/moderation policy, before
any community content pipeline opens**; optional bounded LLM character play, and only if it can be
switched off without losing the game.

**Deferred to S2** (§7 S2): fixes and balancing from real play; deeper political and institutional
simulation; richer character relationships; a scenario editor and a documented mod format; community
scenarios; optional bounded LLM-driven characters behind a clearly marked setting.

**Deferred to S3** (§7 S3): broader Earth strategy and, only on evidence of demand plus maintainers, a
selective off-world layer.

**Deferred to S4** (§7 S4): private and small co-operative play first; shared persistent worlds only
with a real operator, a real governance model and real economics. **Not planned.**

**Explicitly out of the MVP entirely** (§7b): procedural generation; deep economy or logistics;
dynastic succession; off-world content; multiplayer or persistence; LLM-driven NPCs as a dependency;
art, portrait or audio production; a polished UI framework; a scenario editor; an MMO-anything.

### 2.5 The provisional envelopes, kept provisional

§7b's caps are **scope envelopes, not rules**, and this record keeps them in exactly that status. The
counts below are **for S0-A to confirm, replace or tighten** — they are reproduced from §7b, not
proposed here, and no count is invented in this document:

| Envelope | §7b's provisional wording | Status |
|---|---|---|
| Maps | one | §7b |
| Scenarios, campaigns | one finite campaign | §7b |
| Session length | a single sitting, "minutes not hours", with a real ending | §7b |
| Regions, factions, named characters, events | **"the handfuls, not dozens"** — a content list longer than a page is out of scope | §7b |
| Resolution mechanisms | one, reused everywhere | §7b |
| Presentation | text-readable or 2D, no engine work, no art production | §7b |
| Saves | documented save format | §7 S1-a |
| Required services | none — no model, service or account | §7b, §7a |

The concrete region/faction/character/event/turn/save counts are **§9's own open item, "the MVP size
envelope … author-confirmed at S0-A"**, and they are not produced here, because producing them would
be inventing scope the author has reserved.

### 2.6 Honest dependencies that gate S1-a

Stated so that S1-a cannot be read as schedulable today. Each is a live track; **none of these
decisions is made here, and none of them is absorbed into #309.**

| Gate | Where it lives | Why S1-a cannot ship without it |
|---|---|---|
| The rules must be selected at all | [#295](https://github.com/TomiToivio/NooPunk/issues/295) / [#296](https://github.com/TomiToivio/NooPunk/issues/296) / [#297](https://github.com/TomiToivio/NooPunk/issues/297), recorded in `strategy_game/RULEBOOK.md`, which still says **NO RULES APPROVED** | §7b has no mechanics; S0-A is *"approval before runtime"*. A release of an unapproved ruleset is not the MVP. |
| The scenario's identity | **#338's M5 feasibility decision** (local-city #322 vs Global ultra-abstract Earth) | §7b allows exactly **one** scenario. **Which** one is #338's, and is deliberately **not** decided or absorbed here. |
| The licence pair and the clean-up | [#421](https://github.com/TomiToivio/NooPunk/issues/421) | Clause 9 above; verified mechanically by the packaging guard. |
| The engine/renderer choice | This record §1.4, as a proposal | §7b constrains S1-a to "no engine work", so S1-a is **not** blocked by it — S1-b is. |

### 2.7 What this section does not do

- It does not approve S1-a, schedule it, or assign it an owning issue — §7's release ledger keeps
  S1-a *unassigned* deliberately.
- It does not resolve the structural forks, the four — now five — recorded in
  [`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md), nor the
  `politics.py`/`political.py` reconciliation that `VISION.md` §14 step B and `AGENTS.md` §13 leave
  open. Those remain author decisions and remain separate.
- It names no number that §7b did not already state as provisional.
