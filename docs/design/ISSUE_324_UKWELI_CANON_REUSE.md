# The Republic of Ukweli — canon recovery and reuse inventory (issue #324, deliverable A)

**Status:** design record. **No mechanic, number, statistic or name decision is introduced here.** Lore and design documents are reviewed editorially and by playtesting, never by CI ([#271](../..), `AGENTS.md`).

**Purpose.** Deliverable A of [#324](https://github.com/TomiToivio/NooPunk/issues/324): *"recover existing Republic of Ukweli material and publish a concise setting canon/reuse note with provenance"*, as a **retain / adapt / retire** inventory with source links and conflicts flagged — before any scenario text is written.

---

## 1. Correction to the issue's premise (the search, and why it failed)

The issue states: *"The current default-branch code search did not surface Ukweli text, so investigate other locations/history before designing from scratch."*

That finding is correct **only for a filename search**, and it changes what this issue is. Verified by:

```bash
git ls-tree -r --name-only origin/main | grep -i ukweli     # -> nothing: no file is NAMED Ukweli
git log --all --oneline -S "Ukweli" --format="%h %ad %s"    # -> two commits, both dated today
git grep -in "ukweli" origin/main -- .                      # -> content exists in three files
```

So:

- **No file is named after Ukweli**, which is exactly what a filename/code search reports — hence the "not surfaced" result.
- **Ukweli content is present on `main`**, and it is not ancient lore: it landed **today**, through [#328](https://github.com/TomiToivio/NooPunk/issues/328) (#330/#331/#332).
- **There is a five-issue Ukweli cluster**, not one issue: [#324](https://github.com/TomiToivio/NooPunk/issues/324) (this one), [#325](https://github.com/TomiToivio/NooPunk/issues/325), [#326](https://github.com/TomiToivio/NooPunk/issues/326), [#327](https://github.com/TomiToivio/NooPunk/issues/327), [#328](https://github.com/TomiToivio/NooPunk/issues/328).

**Consequence for this issue: nothing needs to be recovered from deep history or the warehouse.** The old material this issue was written to rescue does not exist; the *new* material does, and it is more detailed than the issue assumed. This note therefore re-tasks deliverable A from **archaeology** to **reconciliation** — which is the harder and more useful job, because the sources disagree (§4).

Searched and found nothing: all refs (`git log --all -S`), all filenames, `books/`, `ubiquitous_maniacs/`, `docs/archive/`. **Retire nothing as "old canon" — there is no old canon to retire.**

---

## 2. Sources, in precedence order used by this note

| # | Source | Path / link | What it holds | Register |
| --- | --- | --- | --- | --- |
| S1 | #325, *Design the People's Republic of Ukweli* | issue [#325](https://github.com/TomiToivio/NooPunk/issues/325) | history, society, institutions, economy, the three parties, NHI/PSI folklore | **the dedicated setting issue** |
| S2 | #326, *Ukweli faction leaders and NPCs* | issue [#326](https://github.com/TomiToivio/NooPunk/issues/326) | Sir Mars Eldrich, the Eldrich dynasty, Eldrich Island, LFP funding | characters |
| S3 | #328 roster record §4–§8 | [`docs/design/ISSUE_328_GLOBAL_FACTIONS_ROSTER.md`](ISSUE_328_GLOBAL_FACTIONS_ROSTER.md) | Ukweli scope (**CANON**), party↔global-current affinities, temporal distinction | global roster |
| S4 | crossover package record | [`strategy_game/docs/GLOBAL_FACTIONS.md`](../../strategy_game/docs/GLOBAL_FACTIONS.md) §5 | Ukweli party mapping to global currents | global roster |
| S5 | authored data | [`strategy_game/data/global_factions.json`](../../strategy_game/data/global_factions.json) | machine-readable roster, `ukweli_party_mapping` | global roster |
| S6 | #327, *Ideological realignment in Ukweli* | issue [#327](https://github.com/TomiToivio/NooPunk/issues/327) | 2026 cleavages × the three paradigm complexes | analysis |

**Naming precedence already ruled:** where the *two global-roster registers* differ, **#329's names take precedence** over #328's ([S3 §11](ISSUE_328_GLOBAL_FACTIONS_ROSTER.md)). That ruling is about the **seven global factions only** and does *not* settle §4 below.

---

## 3. Reuse inventory

### 3.1 RETAIN — established, consistent across sources

| Element | Canon | Source |
| --- | --- | --- |
| **New Ukweli** | the glossy, high-rise, high-connectivity modern port/CBD city | S1 |
| **One port city + surrounding islands + limited environs**; wider republic exists off-board | the playable arena | S1, issue #324 |
| **CPU — Communist Party of Ukweli** | incumbent liberation party, governing since independence, wins *democratically* | S1, S3 §7 |
| **UIP — Ukweli Identity Party** | ethnic-nationalist / rural-populist challenger | S1, S3 §7 |
| **Independence in 1964**; Omani → Portuguese → British colonial sequence; nonalignment | fictional chronology | S1 |
| **Post-Soviet genuine multiparty democracy** with civil liberties, independent media, courts | not a sham; not a dictatorship | S1 |
| **"Not quite Cuba, comrade."** | the setting's own joke about outside misreading | S1 |
| **Eldrich Corporation** — world-scale shipping firm, owned by an eccentric British aristocrat | Sir Mars Eldrich (S2); the firm S1 describes | S1, S2 |
| **NHI/PSI as longstanding local folklore** with varied interpretations, plus an **exclusion island** | local shamanic/folk traditions read in-fiction as NHI/PSI related | S1 |
| **Infrastructure as network nodes**: port, international airport, undersea cables, fishing fleet, satellite links | model as nodes/vulnerabilities, **not** as individual units | S1 |
| **Exactly three playable parties — CPU, UIP, LFP** | no eleven-faction opening; a global faction enters only via one character, a news event, an alliance, a cell or scenario pressure | S3 §4, S4 §5 |

### 3.2 ADAPT — established, but must be re-scoped to ~2027

| Element | Adaptation required | Source |
| --- | --- | --- |
| **Three-party starting lineup** | keep three; drop the issue's implied fourth-party option | S1 vs #324 §D |
| **Eldrich Island / Eldrich Mansion** | legal + physical relation to the referenced **Freedom Colony** is explicitly **undefined** — resolve or keep flagged | S2 |
| **Party ↔ global-current affinities** | **starting tendencies only**, never fixed memberships; the crossover start precedes any developed UN parliament | S3 §7 |
| **Late-setting institutions** (`un_parties.yaml`, UN party families, Breakaway Civilization) | later-setting **continuity hypotheses**; must not be assumed to exist at the ~2027 start | S3 §7 |
| **The exclusion island** | exists as folkloric/setting fact; its *mechanics* are unapproved | S1 |
| **Local research** | acquiring/adapting/deploying global tech and contesting its **political meaning** — not global R&D | issue #324 |
| **Economic scale** | borrow Singapore's connectivity *dynamics*, not its scale; Mumbai's contrasts, not its megacity population | issue #324 |

### 3.3 RETIRE — superseded or out of scope

| Element | Why retired here | Source |
| --- | --- | --- |
| **"Wholly anonymous city" as the default scenario** | #324's whole point is to replace it with Ukweli; keep the generic schema for later cities | issue #324 |
| **"Republic of Ukweli" as the formal name** | superseded by **People's Republic of Ukweli** (S1 states it as *Official name*) — **flagged in §4.1**, not silently changed | S1 |
| **Eleven global playable factions in the MVP** | explicitly excluded: *"V1 is three political parties, not eleven global playable factions"* | S3 §5 |
| **UNSA/post-crisis assumptions at scenario start** | the crossover begins ~2027, pre-NHI-Crisis | S3 §7 |

### 3.4 NOT RECOVERABLE — proposed new, must be labelled as such

Nothing was found for these, and inventing them would violate the issue's own instruction. They are **new proposals**, to be marked as proposals wherever they appear:

- the 6–8 **named** playable locations and their place names (§C of this issue);
- the **ferry/bridge/boat routes and access costs** between them;
- **starting values** for locations and factions;
- the **event deck** (maritime trade, technology diffusion, migration, religion, geopolitics, AI/NHI/PSI controversy);
- the **four leaders per faction** — #326 owns Sir Mars Eldrich and the dynasty; the remaining named leaders are **#326's**, not this issue's;
- **polarizing local issues** for the starting situation;
- the **vertical slice** and its results log.

---

## 4. Conflicts that need the author — do not settle these in scenario text

### 4.1 The name of the state — **the significant one**

- **#324** (this issue) says **"Republic of Ukweli"** throughout.
- **#325** states: *"**Official name: People's Republic of Ukweli.** The name reflects its communist independence tradition and the longevity of its governing party, **not** a present-day one-party dictatorship."*
- **#328/#331/#332** and `GLOBAL_FACTIONS.md` say **"New Ukweli"** only, without naming the state.

**Reading offered, for confirmation:** *People's Republic of Ukweli* is the formal name and *Ukweli* / *New Ukweli* the everyday register — which is also what the setting's own joke ("Not quite Cuba, comrade") depends on, since the joke only works because the formal name misleads.

**Why this is flagged and not fixed:** the two forms are not stylistic variants. "People's Republic" carries a specific claim about the state's self-understanding and its post-independence history, and it is the form the *dedicated setting issue* marks explicitly as the official name. #324's "Republic" reads as ordinary shorthand written before #325 landed. If the intent was the plainer "Republic of Ukweli" as the formal name, then #325's sentence is the error and both the issue and §3.3 here must change deliberately, in one breath. **Awaiting your word; the scenario document uses the #325 form and says so.**

### 4.2 The libertarian party's name

| Form | Where |
| --- | --- |
| **LFP — Libertarian Freedom Party of Ukweli** | #325 (setting authority), #326 (leaders) |
| **ULP — Ukweli Libertarian Party** | #328's roster record, `GLOBAL_FACTIONS.md` §5, `global_factions.json` |

**Recommendation:** **LFP**, on two grounds — both the dedicated setting issue and the character issue agree on it, and #328's own §11 precedence ruling was written about the *global-faction* register, not about Ukweli's parties. This is a recommendation, not a change: `global_factions.json` is authored data and I have not touched it.

### 4.3 Eldrich Island vs the Freedom Colony

S2 states the relationship is **undecided** ("they may be the same enclave, adjacent areas, or separate linked places"). The map schema in deliverable C cannot place both without a decision, so C is blocked on this until it is ruled on or C keeps one as a clearly-marked proposal.

### 4.4 The four-leader roster is #326's, not this issue's

#324 §D asks for "3 factions with 4 leaders each, a few important non-leader NPCs". #326 is *Design Ukweli faction leaders and NPCs* and already owns Sir Mars Eldrich and the Eldrich dynasty. **This issue should not name leaders.** §D's leader roster is therefore **deferred to #326**, and this issue consumes whatever #326 produces.

---

## 5. Continuity to the ~2027 start

The recycle must not drag the future in:

- **Keep:** the CPU's democratic incumbency, New Ukweli, the Eldrich firm, the three parties, the folkloric NHI/PSI traditions, the exclusion island, the island geography, the nonaligned diplomatic habit.
- **Do not import as already true:** a developed UN parliament; UNSA; the UNSA Helsinki agent RPG; the Breakaway Civilization as an established actor; the NHI Crisis as resolved; any post-crisis political order. These are **later-setting** material and enter, if at all, as pressures and hypotheses.
- **Distinguish four things that a scenario must never merge** (S3 §7): a party's declared manifesto, a leader's hidden allegiance, a covert sponsor, and the actual voter base.

---

## 6. What this note deliberately does not do

- It changes **no** canonical file. It corrects nothing, and it retires nothing older than the crossover start.
- It invents no place name, route, number, faction, leader or event — §3.4 lists what is genuinely missing instead.
- It adds **no** mechanic or statistic, and touches **no** engine code (S0-A: mechanics await author approval, `docs/design/VISION.md` §7).
- It carries **no** automated test: lore and design documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).
- It does not resolve §4. Those are rulings.

**Next units for #324, in the issue's own order:** B — the scenario document (`docs/scenarios/UKWELI_LOCAL_SCENARIO.md`), written against this inventory; C — the generic location schema plus the Ukweli configuration (blocked on §4.3); then D (consuming #326), E, F, G.
