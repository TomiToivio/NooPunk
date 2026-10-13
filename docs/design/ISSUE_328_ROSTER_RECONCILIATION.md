# Global roster reconciliation — 4 vs 7 vs 11 (issue #328)

**Status: RECORD ONLY. This document changes no canon, edits no data file, and picks no count.** It is the reconciliation a sibling session flagged as an open finding and deliberately left unowned. Documents are reviewed editorially and by playtesting, never by CI ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).

**Method.** All three registers were read on `origin/main` at `3d17524` and are quoted, not paraphrased. Timestamps are commit times from `git log`.

---

## 1. The three registers

| # | Artefact | Count | Provenance |
| --- | --- | --- | --- |
| **4** | [`data/world/un_parties.yaml`](../../data/world/un_parties.yaml) | 4 | legacy / later-setting institutional landscape |
| **7** | [`strategy_game/data/global_factions.json`](../../strategy_game/data/global_factions.json) | 7 | `3efa773`, **2026-10-12 18:19:53 +0300** (15:19 UTC), `status: author_canon`, `source_issues: [328, 329]` |
| **11** | **this issue, #328** | 11 | author revision in the issue body, **later** than the data file |

### Register 4 — a different taxonomy, and legitimately so

`un_parties.yaml` holds **Bioconservatives, Libertarian Party, United Earth Social Democratic Party, The Multitude**. **None of those four names appears among the eleven.** So 4-vs-11 is not a count mismatch — it is a different register, and `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §7 already assigns it: the *"United Earth/UN Parliament parties … belong to the broader legacy/later-setting institutional landscape."*

**Verdict on 4: no conflict.** It is a separate register, documented as such. Nothing to reconcile here beyond keeping the two from being merged by a future reader.

### Registers 7 and 11 — the same taxonomy at different granularity

Both are the crossover's **global paradigm factions**, both cite #328, and they map almost one-to-one:

| #328's eleven Parties | In the 7? | The data file's label |
| --- | --- | --- |
| 1. **CLAPP** — Conservative Libertarian Accelerated Profit Party | ✅ | `Accelerationists` |
| 2. **AHPL** — Alliance for Human and Posthuman Liberation | ✅ | `Cyborgists` |
| 3. **IADIE** — Intersectional Alliance against Discrimination, Inequality and Exploitation | ✅ | `Critical` |
| 4. **IHSF** — International Human Sovereignty Front | ✅ | `Doomers / Butlerian Jihad` |
| 5. **CSC** — Confederation of Sentient Civilizations | ✅ | `Confederacy Awakening / Galactic Ascension Movement` |
| 6. **Greater Orion Arm Co-Prosperity Sphere** | ✅ | `Orion / Grey Collaborative and Infiltration Networks` |
| 7. **MJ-12 / Continuity Directorate** | ❌ **absent** | — |
| 8. **AIC** — Autonomous Intelligence Collective (rogue ASI swarm) | ❌ **absent** | — |
| 9. **ERA** — Earth Restoration Alliance | ❌ **absent** | — |
| 10. **HSDC** — Human Survival and Defence Coalition | ❌ **absent** | — |
| 11. **CCSSP** — Citizen-Consumer's Social Stability Party | ✅ | `Normalcy Bloc` |

**So the 7 cover 7 of the 11, and 4 have no counterpart: MJ-12, the rogue ASI swarm, the Earth Restoration Alliance and the Human Survival and Defence Coalition.**

That is the whole finding. The 7 are not wrong; they are **incomplete relative to this issue's own later revision**, and the count difference is exactly 11 − 7 = 4.

---

## 2. Three defects, in order of severity

### (A) The serious one — the two artefacts disagree about the scenario's period

This issue's author revision states:

> **"Author revision:** Call all **eleven** global organizations **Parties**. **Treat the UN as an already established world government in this strategy scenario.**"

`ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §7 — written from this same issue's lineage — states the opposite:

> **"Temporal distinction:** the Ukweli parties exist in the **early/pre-NHI-Crisis crossover (~2027)**. The **United Earth/UN Parliament parties** … belong to the broader legacy/later-setting institutional landscape. **Do not presume a fully developed UN parliament or post-crisis political order exists at the crossover start**; mapping later parties is a *continuity hypothesis*, not a mandated timeline."

And the crossover's governing rule (#306) starts the game around **2027, in acceleration toward** the NHI Crisis, with the Crisis **unresolved and undated**.

**These cannot both hold.** If the UN is an already-established world government, the scenario is not the pre-crisis acceleration period; if it is the pre-crisis acceleration period, the UN world government does not exist yet. **This matters more than the count**, because it moves the setting's date rather than its roster — and a Global design ([#338](https://github.com/TomiToivio/NooPunk/issues/338)) will bind to whichever answer is chosen.

**It is not mine to resolve.** Note also that this issue's own editing rule — *"Where they contradict this heading and the updated primary naming table, **this author decision takes precedence**"* — is scoped to **this issue's** earlier sections, not to the rest of the repository, so it does not by itself settle a conflict with §7 and #306.

### (B) The roster is not closed at seven — the file's own open question has since been answered

`global_factions.json` asks, in its own `open_questions`:

> `"id": "roster_closed_at_seven"` — *"Is the roster closed at seven, or is the Confederacy Awakening an umbrella covering both the genuine-awakening and the Childhood's-End-cult readings?"*

That question was open when the file was written. **This issue's later revision answers the count half of it: not closed, at eleven.** The file's `open_questions` entry is therefore stale for the count, while remaining valid for the *umbrella* half, which is a different question and is still open.

### (C) Two `official_name` fields are stale — and only two

The data file's design is deliberate: **every one of the seven `official_name` values is `null`**, and the roster record §11 explains why — *"It also leaves every `official_name` **null**, which agrees with this record's position that the formal names are proposals awaiting your selection."*

That reasoning **still holds for most of them**: this issue's revision calls the eleven formal names *"working choices pending author approval"*. But it does **not** hold for one, where the author decided explicitly:

> *"Replace the provisional **Orion Directorate** designation with the official **Greater Orion Arm Co-Prosperity Sphere**."*

The file carries **no** formal name for the Orion entry. So that `null` is now **stale**, and it is the only one this document can show is stale on the evidence — the rest remain genuinely undecided, and I am not inferring decisions from a pending table.

---

## 3. Stale sentences, with locations

Precise, so they can be corrected or cleared one by one:

| Location | Sentence | Status |
| --- | --- | --- |
| `global_factions.json`, `note` | *"The **seven** global paradigm factions … the two issues state the same roster, and this file reconciles them into one"* | **now false** — #328 states eleven |
| `global_factions.json`, `open_questions` | `roster_closed_at_seven` | **answered** by #328's revision |
| `strategy_game/data/global_factions.json` | `official_name` on the Orion/Grey entry | **stale** — the author approved a formal name |
| `docs/design/ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §11, line 437 | *"**Both issues state the same seven-faction roster**"* | **now false** |
| `docs/design/ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §4 | ERA and HSDC appear as *"PROPOSAL — needs your selection"* families | consistent with the file's silence; **not** a defect |

### The roster record is also inconsistent with **itself**

Worth separating from the cross-file problems, because it needs no reference to any other artefact to demonstrate. That record uses "eleven" exactly **once**, in §5:

> **"V1 is three political parties, not eleven global playable factions."** (line 218)

and asserts, in §11:

> **"Both issues state the same seven-faction roster"** (line 437)

**One file, two counts.** §5 is talking about *playability* and §11 about the *roster*, so the two are reconcilable — but as written they are not reconciled, and §5's sentence is in fact the strongest evidence for the reading offered in **D2** below: the eleven exist as the world's actor set while only three are playable. That reading is available **inside this record**; it simply was never stated as such.

---

## 4. What the author needs to decide

**D1 — the period (blocking, and the reason this is not just a number).** Does the strategy scenario start **before** a UN world government exists (~2027, per #306 and roster §7), or **with the UN already established** (per this issue's revision)? Whichever it is, the other artefact has to be corrected deliberately, because a Global design will otherwise be built on one and documented against the other.

**D2 — the roster's granularity.** Does `global_factions.json` extend from 7 to 11, or do **MJ-12, the AIC/ASI swarm, the ERA and the HSDC** belong to a *second tier* — actors that exist in the world but are not first-class playable Parties at this stage? Note the source material supports either reading: this issue calls the eleven *"Parties"* operating at world-government level, while its own §5 says *"V1 is three political parties, not eleven global playable factions."* **My reading — offered, not taken:** the four are real actors, but they are *organizations and threats* rather than playable Parties, which is consistent with §5 and would leave the 7 as the playable roster and the 11 as the world's actor set.

**D3 — the Orion formal name.** Confirm **Greater Orion Arm Co-Prosperity Sphere** so the `null` can be filled; the other six formal names remain pending by design.

---

## 5. What this document deliberately does not do

- It **edits nothing**: not `global_factions.json` (author_canon), not `un_parties.yaml`, not the roster record, not any rulebook chapter, not this issue's body.
- It **chooses no count** and **resolves no timeline**. D1–D3 are rulings.
- It **adds no faction, name, mechanic, statistic or canon**. Every element above is quoted from an existing artefact or counted from one.
- It **does not treat the 4 as a defect** — that register is documented as separate, and merging it would be the actual error.
- It carries **no automated test**: this is prose and canon review ([#271](https://github.com/TomiToivio/NooPunk/issues/271)).
