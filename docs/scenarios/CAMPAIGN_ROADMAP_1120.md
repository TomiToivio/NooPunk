# Campaign writing pivot: roadmap, audit and review checkpoint (#1120)

> **Status:** scenario-writing proposal for author review. It implements nothing, changes no canon, and does not
> touch `design/CAMPAIGN_WRITING_PIVOT.md` — that file is the author's to write.
>
> The rule this whole document exists to serve: **write cases, not a universe bible.** Lore is a tool for play.

**Companions:** [Case 01 — The Tuesday Complaint](CASE_01_THE_TUESDAY_COMPLAINT.md) ·
[Campaign frame](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) ·
[Europol frame](../world/EUROPOL_HELSINKI_1114.md) ·
[CWN baseline](../rules/CWN_IMMUTABLE_CORE_1068.md) · [PSI boundary](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md)

---

## 1. The pivot, stated once

NoöPunk's next creative output is **playable cases**, not more setting. Everything already written — the alternate
history, the Crisis, the factions, Plato/EISS, the graphs, the PSI design — exists to make a Tuesday afternoon in
Helsinki *playable*, and none of it needs to be finished before a rookie takes her first complaint.

The experience the campaign sells is **multi-layered ontological shock**: the player does not understand what is
happening, her institution does not agree with itself, and even the narrative's apparent account can be
retracted — Philip K. Dick and Robert Anton Wilson, not a lore wiki.

**Starting position:** an ordinary Cities Without Number police investigation in Helsinki. Science fiction,
psychic phenomena and cosmic weirdness arrive **through cases and consequences**, one crack at a time. No exposition
dump, no compulsory grand quest, no fixed single explanation.

---

## 2. Audit — what already exists, and what it means for this work

| asset | what it provides | verdict |
|---|---|---|
| [`campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) | four-act campaign, the Act I vertical slice, the "Tuesday Complaint" **mission outline** (six scenes, procedures, failure states), downtime cycle, PSI unlock matrix | **the campaign spine.** Case 01 builds directly on §4.1 rather than inventing a second first mission |
| [`data/world/lakkahaltia_clues.json`](../../data/world/lakkahaltia_clues.json) | an **opening-case clue graph** from #897 (`manifest_discrepancy`, `witness_account`, …) with essential/optional flags, `requires`, `opens`, `contradicts` | **the schema to reuse**; its fiction is a different case (a manifest and a container yard), and it carries no prose |
| [`data/world/helsinki_locations.json`](../../data/world/helsinki_locations.json) | six canonical opening places, districts, start node | locations in Case 01 are drawn from these ids only |
| [`data/world/investigation_scene_intake.json`](../../data/world/investigation_scene_intake.json) | a generic, scenario-independent scene in the clue format | the format Case 01's clues are written in |
| [`tabletop/FIRST_CASE_TABLETOP.md`](../tabletop/FIRST_CASE_TABLETOP.md) | a **UNSA-era** paper procedure for "the first case" (2d6 checks, harm, strain) | older framing: the employer is now Europol, and this file predates #1114. **Do not extend it**; it is a paper-procedure reference, not the case |
| [`scenarios/01_FIRST_DAY_IN_OMAPPI.md`](01_FIRST_DAY_IN_OMAPPI.md) | a full first-day scenario (1 100 lines) in the Omappi setting | a **different campaign**; leave it alone |
| [`scenarios/THE_SAMPO_PROTOCOL.md`](THE_SAMPO_PROTOCOL.md) + annex | a complete investigation with an evidence annex | a **different case**, useful as a model of the evidence-annex format |
| [`rules/PSI_INVESTIGATION_BOUNDARY_1105.md`](../rules/PSI_INVESTIGATION_BOUNDARY_1105.md) | psi may not grant clues or open exits | binding on every case written here |
| [`design/DRAFT_GRAPH_SCENES_1164.md`](../design/DRAFT_GRAPH_SCENES_1164.md) | scene/episode schema, link records | the case's scene structure is compatible with it; no graph work is required to play the case |

### 2.1 The one real conflict: two "opening cases"

* **#897's clue graph** — a smuggling/injury case (manifest discrepancy, container yard, night bar, clinic record),
  complete as data, empty as fiction.
* **#1132's "Tuesday Complaint"** — a dead brother's employment record, complete as an outline, empty as clues.

Both are called the opening case. **Recommendation:** make **The Tuesday Complaint** Case 01 and reuse #897's clue
**schema**, then either keep `lakkahaltia_clues.json` as **Case 00 — a training case played in the academy
flashback**, or retire it. That decision is the author's; this roadmap assumes Case 01 = Tuesday Complaint, because
it is newer, has a full scene outline, and its "anomaly" resolves mundanely — which is the pivot's whole point.

---

## 3. The roadmap: six episodes, one crack each

Each episode is a **self-contained case**. Escalation is earned by what the players did in the previous one, not by
a schedule. Every episode keeps the same discipline: a grounded investigative question first, one modest
ontological crack second, and a GM ledger of what remains undecided.

| # | case | grounded question | the one crack | 50/25/25 in play |
|---|---|---|---|---|
| **01** | **The Tuesday Complaint** | Is a dead man being kept on a payroll, and by whom? | a record that updates itself after the death, for which there is a **mundane** answer — and a footnote that is not | normie sister wants closure; accelerationist fixer sells "continuity"; doomer colleague thinks it is fraud by foreigners |
| **02** | **The Paper That Was Filed Tomorrow** | Who signed a permit dated next week? | two archives disagree about a 2038 event, and the disagreement is **physically real** — one copy is older than the other | a normie who refuses to read it; a records clerk who has quietly catalogued forty such things; a doomer who wants the archive burned |
| **03** | **The Quiet Ward** | Why is a stabilisation clinic's success rate perfect? | psychotronic stabilisation **works** — and one patient is not stabilised, because something is talking to her | staff who believe in the service, a patient who does not, a family that wants the treatment anyway |
| **04** | **Hyvinkää, Night Shift** | Where did the maintenance crew of a dead factory go? | the Zone: AWN procedures activate, and the machine ecology is *polite* | a scavenger accelerationist, a survivor normie, a doomer who wants it burned |
| **05** | **The Courier's Head** | Who is carrying what, and why can nobody open it? | a data courier arrives with a memory that is not hers, and the Confederation and Orion both want it | everyone is right about a different part of it |
| **06** | **The Service** | What is the rookie actually for? | the Higher Self scene: the campaign's premise is reframed, not explained | the three endings: Officer, Envoy, Interpreter |

**Why this order:** 01 teaches CWN procedure; 02 teaches that the record lies; 03 teaches that the state's mercy is
real and dangerous; 04 teaches that the world outside the city has rules of its own; 05 teaches that the cosmic
players have interests; 06 asks what the character is for. No episode requires the next one to make sense.

**What the roadmap never does:** answer whether humanity branches, disappears or becomes something else. That
question stays open past the last episode.

---

## 4. The tone contract (scene-level tests)

The memoir's rule — *consistent consequences, flexible seriousness* — as six checkable registers. A scene fails if
it lands in the wrong column and stays there.

| register | passes when | fails when |
|---|---|---|
| **Everyday boredom** | the procedure is real and slightly dull; the city is doing its Tuesday | the scene is skipped because nothing "matters" |
| **Black comedy** | the joke is about an institution or a form, and someone pays for it | the joke is that ordinary people are stupid |
| **Satire of denial** | a witness's refusal is self-protective and human | the witness is a strawman |
| **Sympathy** | one person's stake is legible without explanation | the case's victim is a device for atmosphere |
| **Political tension** | two institutions are both defensible | one side is the villain by authorial decree |
| **Weirdness** | the impossible thing is specific, observed, and undecided | the impossible thing explains itself |

**One more:** no episode ends with a lecture. If a scene needs the setting explained to work, the scene is wrong.

---

## 5. The 50 / 25 / 25 field, at the table

Numbers describe **the city**, never a character's competence or morals. At the table they appear as **reactions to
the specific crack**, not as a faction the PC joins:

| the crack in play | a normie does | an accelerationist does | a doomer does |
|---|---|---|---|
| a record contradicts itself | insists the system is fine; asks about lunch | offers to sell the discrepancy to someone | says it proves the archives must be purged |
| a psychic event is witnessed | explains it as stress, or drinks about it | wants to know how to do it | wants the witness registered, or removed |
| a hybrid is identified | asks whether she is a good neighbour | asks what she can do | asks who authorised her existence |

**Each NPC carries a stance per paradigm**, not one alignment: a cyborg can deny NHI, a registered psychic can fear
ASI, a normie can support a biotech cure and reject aliens entirely.

---

## 6. What this issue owns, and what it does not

**Owns:** writing priority, the roadmap, the case manuscripts, the GM ledgers, the tone tests.

**Does not own:** CWN rules (#950's engine), the investigation module (#932), the AWN layer (#1109), the graphs
(#1178), psionics (#1178 §1), the Helsinki setting (#914/#1141), or the campaign frame (#1132). Links, not rewrites.

---

## 7. Review checkpoint

1. **This roadmap** — approve the six-episode shape, or cut it to three.
2. **Case 01** — approve the case, or send it back; the manuscript is written to be edited, and the ledger is where
   the author's decisions land.
3. **The opening-case conflict** (§2.1) — Tuesday Complaint as Case 01, and `lakkahaltia_clues.json` as Case 00 or
   retired?
4. **Rate of disclosure** — one crack per case is the proposal; the author may want two, or want 03 and 04 merged.

Only after 1–4: the Python translation (case graph + console/Evennia adapters + tests), which is a separate,
explicitly authorised step. **Nothing in this document is a rule.**
