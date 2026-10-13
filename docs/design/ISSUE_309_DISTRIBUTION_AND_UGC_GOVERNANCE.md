# #309 §8 — distribution, packaging and UGC governance

**Status: research and a proposal. Nothing here is approved, and no licence is selected.**

This record delivers the last two of the four items `docs/design/VISION.md` §9 still lists as open
under **#309 §8**: **distribution, price, storefront requirements, packaging and platform support**,
and **UGC governance research**. Its companion is
[`ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md`](ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md), which carries the
candidate-engine survey and the S1 release-scope statement.

**Why the split.** The four items are two questions asked twice: *what runs the game and what 1.0
must contain* (companion record) versus *how it reaches players and what others may add to it* (this
one). Every storefront conflict below is a constraint on the release scope, and every UGC question
below is a question about what may enter a package — so distribution and UGC governance share one
subject, the **built artifact and its terms**, while engines and scope share another, the **build and
its contents**. Splitting them the other way would have forced each half to restate the other's
facts.

**What this record does not do.** It selects no licence and invents no commercial model — both are
author decisions tracked in [#421](https://github.com/TomiToivio/NooPunk/issues/421). It fixes no
mechanic, number or threshold. It resolves none of the structural forks in
[`STRUCTURAL_FORKS_AND_DECISIONS.md`](STRUCTURAL_FORKS_AND_DECISIONS.md), does not touch the PSI
ruling [#345](https://github.com/TomiToivio/NooPunk/issues/345) or #338's M5 feasibility decision,
and modifies no guard, policy file or ledger — the findings below are **recorded**, not acted on,
because acting on them would be a licensing decision.

Sources: `VISION.md` §7 · §7a · §7b · §8 · §9, `AGENTS.md` §0 · §1 · §3 · §14,
[`ISSUE_231_RELEASE_PACKAGING_GUARD.md`](../licenses/ISSUE_231_RELEASE_PACKAGING_GUARD.md),
[`ISSUE_200_LICENSE_AND_NOTICE_PLAN.md`](../licenses/ISSUE_200_LICENSE_AND_NOTICE_PLAN.md),
`data/licenses/release_packaging_policy.json`, `data/sources/game_system_rights.json`,
`tools/release_packaging_guard.py`, `requirements.txt`, `.github/workflows/`, and the storefront
terms cited inline (retrieved 2026-10-13).

## 1. Distribution: how an offline, buildable-from-source game is published

### 1.1 The constraint §7a places on distribution

`VISION.md` §7 S1 already names the channels and leaves the choice open:

> Published on a realistic indie channel — itch.io, Steam or self-hosted — at whatever price or for
> free, as the author decides.

Two §7a lines bear on *how* any of those may be used:

- Line 1: source must be **buildable and runnable from source, offline, without an account and
  without a service.** → **No storefront may be required to play, and no channel may be the only way
  to obtain the game.**
- Line 7: **no feature may require a live service, a proprietary engine or a paid model provider to
  be playable.** → a storefront's client, SDK or account must never be load-bearing for play.

Both point the same way: **the canonical distribution is a plain, complete build plus the source,
and every storefront is an additional channel over that**, never a replacement for it.

### 1.2 The three families, assessed

| Channel | Cost to the author | Terms that touch the project | §7a verdict |
|---|---|---|---|
| **Self-hosted (git tag + GitHub Releases)** | none | none | **Passes unconditionally.** No third-party terms exist to conflict. |
| **itch.io** | free to use; pay-what-you-want with a minimum of 0 is supported | Publishers warrant they hold the rights to distribute, and grant itch.io a licence to host and promote | **Compatible**, with two caveats (§1.3). |
| **Steam** | Steam Direct: **US$100 per app**, plus a build/store pipeline | Steam Distribution Agreement + the Steamworks SDK's own access agreement | **Compatible only under conditions** (§1.3). **Not compatible with a copyleft code licence that must cover the Steam-bound build.** |

### 1.3 Storefront terms versus §7a and the NC-SA fence — the honest conflicts

Six conflicts, each verified against a primary source. None is a reason to avoid a storefront; each
is a reason a storefront cannot be the *only* distribution path.

**Conflict 1 — Steam's own open-source documentation bars copyleft code from a Steam build.**
Steamworks' *"Distributing Open Source Applications on Steam"* states, verbatim:

> The Steamworks SDK is incompatible with some open source licenses … **If your application contains
> third party open source code that is incompatible with the Steamworks SDK, then YOU MUST NOT
> DISTRIBUTE YOUR APPLICATION VIA STEAM.**

and:

> In general, permissive licenses that do not put any requirements on you to redistribute your
> modifications under an open source license work fine. Common permissive and acceptable licenses
> includes MIT License, BSD 3-clause and 4-clause, Apache 2.0 and WTFPL. … Generally, any license
> that has a so-called "copyleft" element will be problematic when combining code with the
> Steamworks SDK. The best-known example is GPL.

§9 of issue #309 leaves the software licence as **"MIT / Apache-2.0 / GPL-family to be evaluated and
approved separately."** So this is a **live, unresolved dependency between two author decisions**:
**if the author selects a GPL-family code licence *and* wants a Steam listing, the Steamworks SDK
cannot be combined with the code**, unless the author separately grants Valve different terms — which
is a legal decision, not an engineering one, and is explicitly **not** made here. The safe reading,
and the one this record recommends, is: **pick the code licence first (#421), then decide whether
Steam is available to it.**

**Conflict 2 — Steam introduces a proprietary SDK into the shipping pipeline.**
§7a line 3 (*nothing proprietary is depended on*) and line 7 (*no proprietary engine*) name *game*
engines, and a distribution SDK is a different class of dependency. Whether the Steamworks SDK falls
under §7a's "proprietary" prohibition is therefore **a genuine question and an author decision**, not
something this record can settle. What §7a *does* settle is the direction of the safe answer:
combined with §8's non-goal — *"do not add a dependency that stops the game being built and run from
source, offline, without an account and without a paid service"* — **the game must remain fully
buildable and playable with no Steamworks presence whatsoever.** A Steam build may be an *extra*
artifact; it may never be the artifact.

**Conflict 3 — the NC-SA fence becomes non-optional, and both storefronts say so in writing.**
itch.io requires publishers to *"affirm, represent, and warrant that they own or have the rights,
licenses, permissions and consents necessary to publish, duplicate, and distribute the submitted
content."* Steam requires the same warranty in its Distribution Agreement. §7a already rules
CC BY-NC-SA-derived material out of any distributable build. **A storefront does not create this
conflict; it removes the option of ignoring it.** The mechanical consequence is concrete and
verifiable: `tools/release_packaging_guard.py --mode public` **fails by design while the author's
licence decision is open** (§2.3), so a storefront submission cannot be honestly prepared before
[#421](https://github.com/TomiToivio/NooPunk/issues/421) closes.

**Conflict 4 — itch.io's licence grant is broad, and broader than many contributors expect.**
The itch.io ToS grants the platform:

> a worldwide, **non-exclusive**, royalty-free, **sublicensable and transferable** license to use,
> reproduce, distribute, **prepare derivative works of**, display, and perform the content in
> connection with the Service, including without limitation for promoting, redistributing in any and
> all media formats.

**Non-exclusive** is the operative word: it does not prevent the project from publishing the same
build and source elsewhere, and it does not relicense the game to third parties. But "sublicensable
and transferable" and "prepare derivative works" are a hosting grant of a width the author should
read before agreeing, because it attaches to the *uploaded build* as well as to promotional art. It
is the same class of grant any storefront requires; it is named here so it is not discovered late.

**Conflict 5 — pricing is an author decision, and price does not repair the NC-SA fence.**
§7a: *"The core game is not paywalled. Whether there is any commercial model at all — donations, a
paid expansion, nothing — is recorded here once the author decides it."* §7 also says *"at whatever
price or for free, as the author decides."* One trap worth naming: **offering the game for free does
not make NC-SA-derived material admissible.** CC BY-NC-SA's NonCommercial term governs uses of *the
licensed work*; folding NC-derived expression into a separately open-licensed game creates an
unresolved relicensing problem regardless of whether money changes hands. §7a already decided this
("never enters a distributable build"), and
[#421](https://github.com/TomiToivio/NooPunk/issues/421) carries the clean-up. **Not relitigated
here.**

**Conflict 6 — a Workshop-style UGC pipeline would open before the policy that must precede it
exists.** §7 S1-c requires *"a UGC/moderation policy before any community content pipeline opens."*
Adopting Steam Workshop at any earlier point would open a pipeline whose items the project cannot
provenance-check and cannot quarantine (see §4.5), while §7b's MVP explicitly allows only
*"documented data files"* and no mod UI. This is the one storefront feature that must stay closed
until S1-c regardless of which channel is chosen.

### 1.4 Recommendation — a proposal for the author

**Make the self-hosted build-and-source release the canonical channel; add itch.io as the primary
storefront if any is wanted; treat Steam as a contingent option whose availability depends on the
code licence chosen in [#421](https://github.com/TomiToivio/NooPunk/issues/421).**

Rationale, in order of weight: the self-hosted path is the only one with **no terms to conflict with
§7a** and it alone satisfies §7a line 1 in the strict sense (a storefront account is an account).
itch.io is the cheapest storefront whose terms do not prevent the project from shipping the source
itself, and it supports the price range §7 leaves open. Steam is worth having (discoverability, and
it is where a stranger looks) but it is the *only* candidate whose viability is conditional on a
licence the author has not yet picked.

## 2. Packaging

### 2.1 The source distribution — the §7a baseline

§7a requires buildable-from-source; it does **not** require prebuilt binaries. So the minimum honest
release artifact for S1-a is:

- a **git tag** plus the repository's own build instructions;
- the documented entry points (`python -m strategy_game`, and the renderer
  `python -m strategy_game.render` for the board);
- a **documented save format** (§7 S1-a);
- a `README` (§7 S1-a) and, once [#421](https://github.com/TomiToivio/NooPunk/issues/421) closes, a
  `LICENSE`/`NOTICE`.

**The dependency set that matters is not `requirements.txt`.** The repository's runtime requirements
file pins `gdm-concordia[ollama]` from a **git URL**, which is a network fetch at install time. That
is correct for CI and for the optional Concordia integration, and it is **not** the release
dependency set: for S1-a the release set is the **Python standard library alone**, which is exactly
what `VISION.md` §7b allows (*"No engine work: 2D or text-readable overhead map only"*) and what
`strategy_game/tests/test_render_text.py::OfflineImportTests` already proves by importing every
crossover module in a subprocess with no third-party distributions on `sys.path`. A release that
required `requirements.txt` would fail §7a line 1 and the offline test at the same time.

### 2.2 Optional binary distributions, and what they cost

Prebuilt binaries are a convenience, not a §7a requirement. Each adds an obligation:

| Artifact | What it adds | Provenance obligation |
|---|---|---|
| Python **wheel** | an install path for the package | package metadata, no bundled interpreter |
| **PyInstaller / Nuitka** bundle per OS | a bundled CPython | the PSF Licence notice **and** every bundled dependency's licence |
| A **browser view** (companion record §1.4) | nothing new | none — the browser is the platform |

The third row is worth stating: because the recommended next renderer is a static browser view over
the payload the engine already emits, **the cheapest graphical release needs no binary packaging at
all**, which is why the companion record weighs it so heavily.

### 2.3 The guard that gates every one of these — and its current state, measured

The repository already has the mechanical gate, and its state on `main` is a finding in itself.

```
python3 tools/release_packaging_guard.py --mode audit            # CI, full tree
python3 tools/release_packaging_guard.py --bundle bundle.txt --mode public   # the packaging gate
```

**Measured on `main`, 2026-10-13:** `--mode audit` returns **PASS: 0 error(s), 204 warning(s)** —
30 `documented-licence-mention`, 7 `quarantined-path-in-release-set`, 167 `unreviewed-material`.
`--mode public` **fails by design** while `data/licenses/release_packaging_policy.json` carries
`"author_decision_open": true`; the guard's own documentation states it is *"meant to keep failing in
public mode until the author selects a licence. That is the point: the failure is the record that
the decision is still open."*

**One packaging gap found while measuring, recorded and not fixed.** Of those 204 warnings,
**157 are paths under `strategy_game/`**, and the reason is structural rather than incidental: the
policy's `artifact_classes` cover `src/**`, `scripts/**`, `tools/**`, `tests/**`, `docs/**`,
`data/**`, `fixtures/**` and packaging plumbing — and **no artifact class covers `strategy_game/` at
all.** In `--mode audit` that is a warning; in `--bundle … --mode public` an uncovered path is an
**error** ("unreviewed third-party material must not ship"). So **the release set as currently
defined would reject the crossover game's own tree**, which is the very thing S1-a ships.

That is a real release-blocking gap, and it is **deliberately not fixed here**: adding an artifact
class to `data/licenses/release_packaging_policy.json` assigns a licensing category, which is
[#421](https://github.com/TomiToivio/NooPunk/issues/421)'s subject and the author's decision. This
record names it so it is not discovered during a release attempt.

The guard also does not answer whether a bundle is *lawful*; its documentation is explicit that it
answers only *"is this bundle internally consistent with the recorded rights position?"*, and the
release gate still calls for a release-stage legal review before publication. That remains a
pre-release step, not an agent check.

## 3. Platform support, realistically

**S1-a is platform-portable for free, because it has no platform.** The MVP's board is
text-readable; the only requirement is a Python 3 interpreter and a terminal. There is therefore
**no per-OS build, no binary, and no platform matrix** in the S1-a release — which is the cheapest
possible §7a position and the reason §7b's *"no engine work"* cap is a gift rather than a
restriction.

What the project can honestly claim at S1-a, and what it cannot:

| Claim | Honest status |
|---|---|
| **Runs from source on any platform with a supported Python 3** | Supportable, and the only claim that needs to be made. The repository's CI tests Python **3.12**; the local verification environment runs **3.10.12**. The published minimum should be whichever the author will actually test — an author decision. |
| **Prebuilt binaries for Linux / Windows / macOS** | **Not required by §7a and not worth claiming at S1-a.** Each is 3× the packaging and provenance work (§2.2), and the claim buys nothing that the source build does not already give a stranger. |
| **A graphical 2D interface** | S1-b. Once it arrives, portability depends on the renderer: a browser view is *one* artifact for every platform, Qt is one bundle per OS, Godot is one export template per platform. That ranking is a second, independent argument for the recommended renderer. |
| **Mobile, console, handheld-specific work** | **Out of scope, and nothing depends on it.** §7's *"Explicitly not planned"* and §7b's *"no MMO-anything"* are the governing lines. A browser view would happen to work on a handheld browser; that is a consequence, not a target. |

**Channel-side note, verified:** the repository already deploys `docs/` to GitHub Pages
(`.github/workflows/pages.yml`, on pushes to `main` touching `docs/**`). That is existing
infrastructure with no terms attached — a natural host for a static browser view if the author takes
the companion record's recommendation, and a concrete reason the recommendation is cheap rather than
speculative.

## 4. UGC governance research

### 4.1 The landed requirements that bind UGC

Four places already decide what UGC governance must contain; nothing here adds to them.

- `VISION.md` §5 (modding and UGC): *"data-driven events and entities, a documented scenario format,
  stable extension contracts, content provenance and licensing, moderation, optional publishing."*
- `VISION.md` §7a line 5: **"It must be moddable, and the data formats documented**, because an
  open-source indie game grows through its community, not through its budget."
- `VISION.md` §7 S1-b gate: *"other people can author scenarios without reading the source"*; §7
  S1-b deliverable: *"modding and scenario data formats documented"*.
- `VISION.md` §7 S1-c: a **UGC/moderation policy before any community content pipeline opens**, and a
  contribution and provenance process.
- `VISION.md` §7b: the MVP ships **no mod UI and no scenario editor** — *"documented data files
  only."*

And one hard boundary that does **not** move for UGC: `AGENTS.md` §1, *"author intent is canon"* — no
community contribution can create canon — plus `VISION.md` §7a's *"clear boundary between **code**
(tested, reviewable) and **canon, lore and rules prose** (which the author owns and reviews
editorially)."*

### 4.2 The extension surface a mod may act on

Derived from the above rather than proposed: through S1-a an extension touches **data**, not
semantics. That follows from three landed facts, not from preference:

1. §7b allows the MVP **documented data files only**, no mod UI and no scenario editor.
2. §7 S1-b's gate is *"author scenarios without reading the source"* — i.e. the surface is the
   documented data format, not an API into rule internals.
3. INTERFACE_SPIKE criterion 3 and §7b's *"one resolution mechanism, reused everywhere"* mean a mod
   that reimplemented a resolution rule would **fork the rulebook** — the same defect as writing a
   rule twice in two languages, and the same defect `AGENTS.md` §13 calls *"a **rules** difference is
   a defect: extract a shared specification rather than fork the rule."*

**Consequence for the UGC policy (a proposal):** the documented extension contract should expose
**content** — events, entities, scenario data, board data — and should *not*, at least through S1,
expose rulebook semantics. A mod extends a **scenario**; it does not amend the rules. This is a
governance position, not a mechanic: it selects no rule and changes none.

### 4.3 Community content licensing — the inbound/outbound problem

This is where UGC governance and [#421](https://github.com/TomiToivio/NooPunk/issues/421) meet, and
the honest finding is that **UGC governance cannot be finished before the licence pair is chosen.**

Every modder's work is separately copyrighted. Any real UGC policy therefore needs **three** licence
statements, and only two of them exist as questions today:

| Direction | What it is | Status |
|---|---|---|
| **Outbound — code** | the software licence of the engine | open, [#421](https://github.com/TomiToivio/NooPunk/issues/421) |
| **Outbound — content** | the licence of NoöPunk-original content and data | open, [#421](https://github.com/TomiToivio/NooPunk/issues/421) |
| **Inbound — contributions and mods** | the licence under which the project *accepts* community work into its own tree or release | **not defined anywhere; a genuine gap** |

The gap matters because it is not symmetric with the other two. A **permissive outbound** licence
plus an **NC-SA or otherwise-unstated inbound** contribution is a relicensing conflict: the project
would be redistributing work it has no clean right to redistribute. Conversely a **share-alike
outbound** licence makes certain inbound licences compatible and others not. So **the inbound
contribution licence is a function of the outbound pair, and cannot be chosen before it** — which is
precisely why it belongs to [#421](https://github.com/TomiToivio/NooPunk/issues/421) and not to this
record.

**Existing precedent, cited not decided:** [#421](https://github.com/TomiToivio/NooPunk/issues/421)
records that *Fate Core's CC BY 3.0* attribution is already shipped for the RPG layer. That is an
attribution arrangement for a *third-party* SRD, not an inbound-contribution policy, and the two
should not be conflated.

**A verified structural gap in the data model.** `strategy_game/provenance.py` defines
`ProvenanceKind` = **UNKNOWN · EVIDENCE · AUTHORED · GENERATED · SIMULATED**. Those are **data kinds**
— they say what sort of thing a record is. **None of them records a third-party licence term, a
source, or an attribution string**, and a search of the `strategy_game/` module tree finds no
licence or attribution field in the scaffold's data model at all. `VISION.md` §7a line 4 requires
every third-party asset to carry provenance and contributions to be traceable, and §9 requires
per-component source, edition, licence clause, reused quantity and reason. The existing machinery
that does this for the *repository's own* third-party material is
`data/sources/game_system_rights.json` + `docs/licenses/ISSUE_200_LICENSE_AND_NOTICE_PLAN.md` +
`tools/release_packaging_guard.py` — but that machinery works over **paths in this repository**,
not over content records inside a data file.

**So the honest statement of the gap is:** a contributed data file cannot currently carry the licence
metadata that §7a line 4 and §9 would require it to carry, and **adding that field is a licensing
decision**, because it must name a licence vocabulary that does not exist yet. It is therefore
[#421](https://github.com/TomiToivio/NooPunk/issues/421)'s to specify, and this record only names it.
(Note also the caution already recorded on #309: the five `ProvenanceKind` values are **data kinds**,
adjacent to but not interchangeable with the epistemic register of `RULEBOOK.md` §33.32. A licensing
field must not be folded into either.)

### 4.4 Attribution

`VISION.md` §7a line 4 and issue #309 §9 already state the obligation: record per-component source,
edition, licence clause, reused quantity and reason; acknowledge design inspirations by name without
implying endorsement; no "found it on the internet" art, music, fonts or text. The UGC-specific
consequence, in three parts:

1. **A mod must declare its own third-party assets** — the same rule the project holds itself to.
2. **Attribution must survive inclusion into a bundle.** A community work's notice cannot be
   swallowed by the host game's `NOTICE`; either the aggregate notice carries it or the item is not
   distributable. The existing `notices`/`artifact_classes` machinery in
   `data/licenses/release_packaging_policy.json` is the shape this would take, and **extending it is
   a licensing decision** ([#421](https://github.com/TomiToivio/NooPunk/issues/421)).
3. **Attribution does not promote content into canon.** Per `AGENTS.md` §1 and `VISION.md` §7a's
   code/prose boundary, a credited community contribution remains *fictional content under
   provenance*, never author canon.

The project's own attribution policy is explicitly **not yet written** —
[#421](https://github.com/TomiToivio/NooPunk/issues/421) names that as one of its four open items —
so this record specifies nothing about it beyond the UGC-specific requirement above.

### 4.5 How a community contribution meets the NC-SA clean-up obligation — the core finding

§7a line 2: NC-derived material (Eclipse Phase, CC BY-NC-SA, and the EP2 homebrew prototype with it)
*"stays **isolated, marked and attributed**, and never enters a distributable build. This is the
largest clean-up obligation before S1."* The repository enforces this mechanically today:

- **Quarantine list** in `data/licenses/release_packaging_policy.json` → `quarantined_paths`:
  `src/eclipse_phase_homebrew/**`, `src/concordia_runtime/ep2_*.py`, `scripts/ep2_*.py`.
- **Excluded licence decisions** → `verified-nc-sharealike`, `no-cc-grant-established`,
  `blocked-unverified`, `proprietary-out-of-scope`.
- **The gate** → a quarantined or uncovered path in an explicit release bundle is an **error**.

Four findings follow, and they are the whole of the UGC/NC-SA interaction:

**Finding 1 — a community contribution inherits the fence, and the fence is wider than "NC".**
A contribution that is NC-derived falls under `verified-nc-sharealike` and is barred identically. But
the ledger's vocabulary also excludes `no-cc-grant-established` (no CC grant found — *"reuse of
expression is NOT permitted on this evidence"*) and `blocked-unverified` (*"the authoritative page
could not be read … nothing may be imported"*). **A mod whose provenance cannot be established is
in the same position as NC-derived material**, because the project may not ship what it cannot
license. So UGC validation must be able to reach a *"provenance unknown → may not ship"* verdict, not
merely an *"is it NC?"* one.

**Finding 2 — a mod may not be a required dependency of a distributable build.**
The same logic that keeps EP2 out of the build keeps any unpurgeable mod out of it. A mod that the
game needs in order to function would make the release depend on material the project cannot
warrant, which is §7a line 2 and line 4 at once. This is a governance rule for S1-b/S2, and it is the
reason §7b permits *"documented data files only"* at MVP scale.

**Finding 3 — the guard cannot see a mod uploaded elsewhere, and the policy must say so rather
than pretend otherwise.** `tools/release_packaging_guard.py` audits **paths in this repository**. A
third-party mod distributed through itch.io, a forum or a Workshop is outside its reach. Therefore
the honest UGC policy must separate three things it currently does not distinguish:

- content the project **packages** — fully provenance-checked, guard-enforced;
- content the project **accepts into its own tree** — provenance-checked at contribution time, which
  is the *inbound licence* gap of §4.3;
- content the project **neither packages nor accepts** — the modder's own responsibility, with the
  game required to remain complete and playable without it.

Naming the third category is not a loophole; it is the only honest description, and it must be paired
with the requirement that **the game cannot require a mod to be complete** (§7b: *"its absence must
leave a complete game"*, stated there about models and equally true of mods).

**Finding 4 — the clean-up obligation is one-way and does not relax for free-of-charge distribution.**
§1.3 conflict 5 above. A community contribution does not create a route around §7a line 2, and a
free release does not either. `VISION.md` §7a is a *requirement of the project*: *"Any proposal that
breaks one of them is out of scope until the author changes this section."*

**Cross-link.** All of this lands in
[#421](https://github.com/TomiToivio/NooPunk/issues/421): the inbound contribution licence, the
content-licence statement, the attribution policy, the release-time clean-up, and — per §2.3 — the
missing `strategy_game/**` artifact class. **This record duplicates none of those; it supplies the
UGC-specific requirements those decisions must satisfy.**

### 4.6 Canon and rules conflicts

Recorded as governance questions with their governing rule attached, not as answers:

| Conflict | Where the rule already is | Consequence for UGC |
|---|---|---|
| **Canon**: may a mod establish setting fact? | `AGENTS.md` §1 (author intent is canon); `VISION.md` §7a (author owns prose) | **No.** Mod content stays fictional content under provenance. |
| **Rules**: may a mod change a rule? | `AGENTS.md` §0 (legacy rules do not carry over; importing a mechanic needs an approved conversion); `AGENTS.md` §13 ("a rules difference is a defect"); §7b (one resolution mechanism) | **No, through S1.** A rule-changing mod forks the rulebook. |
| **Legacy game**: may a mod pull legacy material in? | `AGENTS.md` §0; `VISION.md` §1 (rules are not shared, lore is, subject to author decisions) | A mod importing a legacy *mechanic* needs the same explicit author-approved conversion any other import needs. |
| **Two games, one repo**: which tree does a mod belong to? | `AGENTS.md` §0; `VISION.md` §11 | A crossover mod is not legacy material and must not be represented as such. |

### 4.7 Moderation, trust and multiplayer — deliberately deferred

`VISION.md` §15 already lists what must be decided *before any multiplayer release*: scenario-versus-
world canon, creator attribution and licences, content validation, moderation and appeals,
hidden-information access, griefing controls, server recovery, and incompatible-mod handling — *"a
provenance field alone does not solve them."* §7 S1-c requires the UGC/moderation policy before any
community pipeline opens; §7b forbids an MVP mod UI; S4 is *unscheduled and not planned* and
*"if it never happens, the game is unaffected."* **None of this is decided here**, and nothing above
should be read as a moderation design.

## 5. What this record refuses to decide

- **The licence pair.** Code licence and content licence are the author's, tracked in
  [#421](https://github.com/TomiToivio/NooPunk/issues/421). No licence is named, recommended or
  implied here.
- **The commercial model and the price.** §7a: *"Sustainability is an author decision, not an
  agent's."* §7 leaves price entirely open.
- **Whether the Steamworks SDK falls under §7a's "nothing proprietary".** Flagged as a genuine
  question (§1.3 conflict 2) and left to the author.
- **The artifact class for `strategy_game/`.** The gap is measured and named (§2.3); assigning the
  class is a licensing decision.
- **The inbound contribution licence and the attribution policy.** Named as gaps, assigned to
  [#421](https://github.com/TomiToivio/NooPunk/issues/421) (§4.3, §4.4).
- **Any mechanic, count, threshold or rule of the UGC/mod format.** §4.2 states a governance
  boundary — content, not semantics — and selects nothing.
- **#345's PSI ruling, #338's M5 feasibility decision, the structural forks, #328's party rulings,
  #322's leader seats.** Separate issues; not touched, not absorbed, not referenced as settled.

## 6. Verification

Everything factual above was measured on 2026-10-13, from a branch off `origin/main`:

- `python3 tools/release_packaging_guard.py --mode audit` → **PASS: 0 error(s), 204 warning(s)**
  (30 `documented-licence-mention`, 7 `quarantined-path-in-release-set`, 167
  `unreviewed-material`; 157 of the warnings are `strategy_game/` paths).
- No artifact class in `data/licenses/release_packaging_policy.json` matches `strategy_game` —
  checked programmatically.
- `data/licenses/release_packaging_policy.json` → `author_decision_open: true`.
- Quarantine globs and excluded-licence vocabulary read from the same policy file and from
  `data/sources/game_system_rights.json` (`decision_vocabulary`).
- `ProvenanceKind` = UNKNOWN · EVIDENCE · AUTHORED · GENERATED · SIMULATED, read from
  `strategy_game/provenance.py`; no licence/attribution field found in the `strategy_game/` module
  tree.
- `.github/workflows/python-scaffold.yml` (job `test`) and `.github/workflows/pages.yml` read
  directly.
- Storefront terms retrieved 2026-10-13 from Steamworks' *Distributing Open Source Applications on
  Steam* and itch.io's *Terms of Service*; quoted verbatim above.

**This is a Markdown-only change, and no test covers it.** Per `AGENTS.md` and
[#271](https://github.com/TomiToivio/NooPunk/issues/271), prose is reviewed editorially and by
playtesting, and no CI assertion, snapshot or schema lock may be added over it. The behavioural
suites are unaffected.
