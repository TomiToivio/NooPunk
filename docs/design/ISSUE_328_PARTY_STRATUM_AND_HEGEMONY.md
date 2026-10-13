# Issue #328 — the Party stratum, the four unpaired Parties, and office vs discursive hegemony

**Status: PROPOSAL / analysis only. No count is picked, no timeline is resolved, no field is filled,
no roster is added, no file is edited.** This record makes the author's decision **expressible**; it
does not make it. Documents are reviewed editorially and by playtesting, never by CI
([#271](https://github.com/TomiToivio/NooPunk/issues/271)). Legacy canon is untouched
([#306](https://github.com/TomiToivio/NooPunk/issues/306)); the setting is **20XX** and no exact date
is invented here.

**Relationship to what already landed.** [`ISSUE_328_ROSTER_RECONCILIATION.md`](ISSUE_328_ROSTER_RECONCILIATION.md)
does the 4 / 7 / 11 **measurement** and puts three decisions to the author (D1 period, D2 granularity,
D3 Orion name). This document does **not** repeat that measurement. It adds four things the earlier
records only gestured at: the **entity-kind analysis** that explains *why* four entries do not fit,
the **three readings** as explicit OPTIONS, the **office vs discursive-hegemony** distinction
grounded in the six quantities, and the **UN-world-government premise** framed as a specific
seats/office question.

**Marks.** `[CANON]` = quoted from an existing artefact or the issue body.
`[PROPOSAL]` = this document's own reading, offered, not taken.

---

## 1. Fact vs interpretation, kept apart

- **Fact (measured).** `data/world/un_parties.yaml` holds **4** parties. `strategy_game/data/global_factions.json`
  holds **7** factions. Issue #328's own body carries an **11-row** Party table. Those three counts
  are facts about artefacts.
- **Interpretation.** That the 7 and the 11 are *"the same roster"*; whether the four unmatched are
  **missing**, a **second tier**, or a **different register**; **which list is canonical**. All four
  are readings, and the last is the author's alone.

The data file's own `open_questions.roster_closed_at_seven` (*"Is the roster closed at seven …?"*)
is the standing proof that the count was **open when the file was written** — so the "same roster"
claim is a reading, not a measurement.

---

## 2. The four unpaired Parties `[CANON]` — what #328 says they are

Seven of the eleven map near one-to-one to the 7's entries. The four with **no counterpart** are
quoted here from #328's own register, not paraphrased:

| # | Party (as #328 names it) | #328's own kind/leadership line | #328's own decisive line |
| --- | --- | --- | --- |
| 7 | **MJ-12 → Continuity Directorate** | **human-led** old secret network evolving into *"a potentially sovereign Breakaway Civilization, not a conventional party"* | *"Do not automatically place it on left/right axes"* (§6.3) |
| 8 | **Autonomous Intelligence Collective (AIC)** (the rogue ASI swarm) | **NHI-led** in the broad nonhuman-intelligence sense: rogue ASI swarm, with collaborators and unwilling proxies; *"distinct from Orion"* (§6.4) | *"a separate faction"*, a machine-led actor (§6.4) |
| 9 | **Earth Restoration Alliance (ERA)** | human-led coalition of green parties, climate networks, conservationists, ecological radicals, Archaic Revival communities | its decisive additional axis is *"biosphere versus technological civilization"* (§4.1) |
| 10 | **Human Survival and Defence Coalition (HSDC)** | human-led security and preparedness alliance; *"explicitly not a Butlerian extermination program"* | its essential axis is *"risk/security versus openness"*, *"not party tribalism"* (§4.2) |

These four are **real actors in the author's register**. The question this document keeps open is
*narrower*: whether they belong to the **paradigm stratum** the 7 encode.

---

## 3. The entity-kind analysis `[PROPOSAL]` — why the 7's own axis cannot hold the four

`global_factions.json` declares exactly three `entity_kinds`: **`human_ideological_formation`** (A–D),
**`nhi_aligned_formation`** (E, F), **`latent_public`** (G). That axis answers *"which paradigm-stance
formations contest the AGI/PSI/NHI shift"* — it is a **paradigm** taxonomy, drawn on the compass plus
paradigm positions.

The four exceptions do not sit on that axis:

- **MJ-12** is human-led, so it is not `nhi_aligned_formation`; but it is **not a paradigm-stance
  formation on the compass at all** — canon forbids compass placement. Its power is *pre-existing
  institutional continuity and information asymmetry*, which the paradigm axis has no term for.
- **AIC** is machine-led — closer to `nhi_aligned_formation` — but #328 separates it from Orion and
  from the human formations: it is *"a separate faction"*, and its human component is explicitly
  *non-consenting* (collaborators, the deceived, the compelled, the freed). Being coerced is not the
  same kind of membership as believing.
- **ERA** is human-led and *is* arguably a stance on the paradigm shift, but its **decisive axis is
  biosphere-vs-technology**, not the compass the other four human formations share.
- **HSDC** is human-led with a stance, but its **decisive axis is risk/security-vs-openness**, and it
  *"allows diplomacy and selective technology"* — the opposite of the Butlerian reading it is
  sometimes filed under.

**So the honest structural statement is:** the 7's `entity_kinds` axis can hold seven entries and
cannot hold these four without a **new kind**. That is a *category* difference, not a *count* error.

---

## 4. The relationship — three readings, presented, not chosen `[PROPOSAL]`

### Reading A — same register, coarser (granularity / count)
Both cite #328 and both are called "the crossover's global register", so the 7 is an earlier,
incomplete encoding of the same list, and the fix is to extend **7 → 11**.
- **For:** seven of eleven match by role; the file's `note` claims *"the same roster"*; its own open
  question asks whether it is closed at seven.
- **Against:** the four extras match nothing at all, and the file's `entity_kinds` is a **paradigm**
  taxonomy, not an organisational one.

### Reading B — two orthogonal registers (entity-kind / tier)
The **7** answer *"which paradigm-stance formations contest the AGI/PSI/NHI shift"* (compass +
paradigm positions). The **11** answer *"which Parties hold world-government-level organisational
power"* (an organisational/institutional taxonomy, including covert continuity bodies and a defence
coalition). They overlap where a paradigm faction is also a Party, and are not the same axis.
- **The discriminating evidence is the four extras**, and it is canon (§3): none of the four sits on
  the paradigm-shift compass the 7 encode.
- Under B the roster is not "extend to 11" but "the 7 are the paradigm stratum, the 11 are the Party
  stratum, and 4 Parties have no paradigm-stratum entry (for MJ-12, none possible by canon)."

### Reading C — competing rosters (authorial choice)
#328's own editing rule makes "the eleven" the later word; the data file is `author_canon` and says
seven. Both cannot be the canonical roster, so one supersedes, or one is a narrowed view of the other.
The reconciliation record's **D2** ("the four are real actors but a *second tier*; the 7 remain the
playable roster, the 11 the world's actor set") is a specific version of C. This document neither
adds to nor contests it.

---

## 5. How this document characterises 7-vs-11, without resolving it `[PROPOSAL]`

The overlap is real and near-exact for seven entries, so the two are **not unrelated rosters**; but
the four exceptions are **entity-kind exceptions**, so the two are **not one register with a miscount**
either. The honest label is:

> **One shared taxonomy for seven entries, plus a category difference for four.**

That is why the choice among A, B and C is the author's and why this document makes none of them.
*(Offered, not taken: B is the only reading that accounts for the four exceptions without calling the
`author_canon` file "wrong"; A is the only reading that keeps a single register. The author decides.)*

**This document adds no fourth roster.** It restates the 7 and the 11 as they already exist and names
the four exceptions; it does not invent a twelve-entry list, a merged list, or a canonical pick.

### One entity-kind conflict *inside* the mapping — the Normies
The reconciliation record maps #328's Party #11 (CCSSP / Normies) to the 7's `Normalcy Bloc`. But the
two issues disagree about **what kind of thing it is**:
- **#328 (author revision, latest):** *"It is now an organized Party with political interests and
  agency … Normies are now Party #11."*
- **#329 §3.G and `global_factions.json`** (`kind: latent_public`, field `not_a_party`): *"do NOT
  make it a single organised party; treat it as a cross-faction sociological tendency / latent
  constituency."*

If the Normies are a Party, the 7's `latent_public` kind is wrong for them; if they are a latent
tendency, #328's "Party #11" label is. This is an **entity-kind conflict**, not a count one — flagged,
not resolved.

---

## 6. Office vs discursive hegemony, grounded in the six quantities `[CANON]`

`docs/design/NOOPUNK_GLOBAL.md` **§7** keeps six things in six fields, with six component
conventions: **#1 opinion/support**, **#2 organisational membership/resources**, **#3 legislative
representation (seats)**, **#4 office & government control**, **#5 institutional access**,
**#6 Laclauian discursive hegemony**. The non-identity that answers this issue's title:

> **Holding office (#4) ≠ holding discursive hegemony (#6).**

- **Office** is #4 — markers on board slots for *who holds which executive function*.
- **Discursive hegemony** is #6 — the **articulation graph itself**: *which articulation is nodal,
  where the frontier runs.* In `strategy_game/politics.py` that is `Signifier.kind`
  (`SignifierKind`: **nodal / floating / empty**, with `UNSPECIFIED` as the default) and
  `RelationLayer` (**articulation / equivalence / antagonism**). It is *"not a scalar; not ownership;
  not popularity; not control"* (§7).
- §7 states the non-identity directly: *"A faction can hold the #6 nodal signifier and lose
  everything else — hegemony in meaning is not power."* A faction can win an election (#3 / #4) and
  still lose the frontier; it can fix the meaning of *Humanity* (#6) and hold no office at all.

**Where the paradigm shifts land.** `data/paradigm_shifts.yaml` gives the process: dislocation →
competing explanations → competing signifiers → chains of equivalence → frontiers → antagonism →
attempts at hegemony → temporary institutional order. A shift (AGI / PSI / NHI) is a **dislocation**:
it moves **#1 (opinion)** and **#6 (meaning) first**, because it unsettles what the existing
signifiers denote, and it moves **#3 / #4 (seats / office)** only at the next institutional window.
The six quantities are precisely what keep *"who won the shift?"* from collapsing into one number —
and #328's title word **"hegemony"** is the #6 field, not a scoreboard.

---

## 7. The UN-world-government premise is a #3 / #4 question, not a settled one `[PROPOSAL]`

#328's revision says *"Treat the **UN as an already established world government** in this strategy
scenario."* `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md` §7 — from this same issue's lineage — says the
opposite: the UN Parliament material belongs to the **legacy/later-setting** landscape and *"Do not
presume a fully developed UN parliament or post-crisis political order exists at the crossover
start."* The crossover starts in the acceleration toward the NHI Crisis, unresolved and undated (#306).

Read through §7's quantities, the premise is not a mood; it is a specific claim about **#3 and #4**:

- If the UN is an **already-established world government**, the eleven Parties are world-level holders
  of **#3 (seats)** and **#4 (office)** at game start.
- If it is **not yet** (per #306's pre-crisis start and roster §7), then at world level the parties
  hold **#1 / #2 / #5 / #6** — support, membership, institutional access, discourse — while
  world-level **#3 / #4 do not yet exist**; the seats/office game is *local*, in Ukweli's three
  parties.

So the period question (D1 in the reconciliation record) is **precisely a #3 / #4 question** — which
is why it should be settled before any Global design binds to a count or a board. And the Normies'
entity-kind conflict (§5) has a matching §7 consequence: as an organised Party they can hold **#3
seats**; as a latent public they are purely **#1 opinion** with no #3 / #4 / #5 — §7's *"#1 support ≠
#3 seats"*, made concrete.

---

## 8. Null-with-a-reason: what this document leaves empty

Following the convention *"a field is null with a reason rather than being filled in"*
(`global_factions.json`), this record fills nothing the author left open and invents nothing to
close a gap. Specifically it does **not** fill:

- the **Orion formal name** (the reconciliation record already logs the approved *"Greater Orion Arm
  Co-Prosperity Sphere"* for the author; writing it into an `author_canon` file is the author's call);
- MJ-12's relation to disclosure / the Confederacy / Orion / the Swarm;
- the AIC's origin or autonomy, or whether any of its human network is voluntary versus coerced;
- ERA's or HSDC's internal structure;
- any Party name, and any **count**.

**A precision worth recording.** The reconciliation record and the roster record describe *"every one
of the seven `official_name` values is `null`"*. Measured, **`global_factions.json` carries no
`official_name` key at all** (zero occurrences). "Absent" and "null" are different facts; the reason
nothing is filled is that #328 §8 lists the name fields as *"suggested representations, not
implemented schemas"*, and no file implemented them.

---

## 9. What this document is blocked on — the author's ruling

Closure of #328 turns on the author's own checkbox list, *"F. Small MVP implications and decisions
still open"*, every item of which is a ruling or a post-approval task:

1. Author review / rename formal names and colloquial labels; specify self-name vs hostile exonym.
2. Specify fictional MJ-12 continuity — when it starts, what it controls, when and why it is a
   Breakaway Civilization.
3. Decide if MJ-12 remains human-led, whether it has internal factions, and its relationship to
   disclosure, the Confederacy, Orion and the Swarm.
4. Decide the origin / objectives / autonomy of the ASI swarm, and whether any human network is
   voluntary versus coerced.
5. Confirm the three Ukweli party ↔ global-current affinities as **starting tendencies**, not fixed
   memberships.
6. Reconcile existing legacy UN party records with the now-established UN world government and the
   eleven global Parties.
7. After approvals, optionally document separate organization / party / ideological-current /
   nonhuman-actor records; **no new gameplay/statistics until separately approved**.

This record makes items 1–4, 6 and 7 *expressible as choices* by supplying the entity-kind analysis
(§3), the three readings (§4) and the #3 / #4 framing (§7) — but it can **rule on none of them**. The
single criterion genuinely blocked on the author is the roster ruling itself: **which of A / B / C is
canonical, and whether the four unpaired Parties (MJ-12, AIC, ERA, HSDC) belong in the paradigm
stratum at all.** Until that is the author's, #328 stays open.

---

## 10. Boundaries this record holds

- **No mechanic, number, threshold, count, name or roster entry is added**; no data file is edited —
  not `global_factions.json` (`author_canon`), not `un_parties.yaml`, not `ISSUE_328_GLOBAL_FACTIONS_ROSTER.md`,
  not this issue's body, not any rulebook chapter.
- **It picks no reading and resolves no timeline.** A, B, C and D1–D3 are the author's.
- **It adds no fourth roster** and does not silently merge the 4, the 7 or the 11.
- **No automated test** over this prose ([#271](https://github.com/TomiToivio/NooPunk/issues/271));
  no exact date invented (`AGENTS.md` §6 — the setting is 20XX; any "~20xx"-style figure would be
  quoted from #306, not assigned here); legacy canon untouched (#306).
