# Case 01 — *The Tuesday Complaint* (full manuscript, #1120)

> **Status: authored scenario draft for Tomi's review.** Not canon, not implemented, and not a rulebook chapter.
> It is written to be marked up: the case, the ledger and the tone checks are all editable, and the decisions that
> belong to the author are flagged **[AUTHOR]**.
>
> Companion: [campaign roadmap](CAMPAIGN_ROADMAP_1120.md). Campaign frame:
> [`CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) §4.1 — this manuscript is that
> outline made playable, not a second first mission.

---

## 1. The case in one paragraph

A Lithuanian woman files a data-protection complaint: her brother has been dead for eleven months and his
employment record keeps updating. Europol's interest is a cross-border data-integrity problem. The human truth is
that a family is being billed for the privilege of not being deleted — and that somewhere in the chain a clerk, a
dispatcher and a small identity shop have built a quiet business out of *continuity*. Nothing supernatural happens.
One footnote is unexplained, and nobody in the case is lying about the same thing.

**Why this case first:** it teaches every CWN procedure the campaign needs — records, interview, surveillance, one
short violent confrontation that is a **failure state**, not a climax — and its anomaly resolves mundanely. The
player learns that the world is crooked before she learns that it is strange.

---

## 2. Cast

| who | role | what they want | what they will not say |
|---|---|---|---|
| **Rūta Balčiūnaitė** (41) | the complainant; the dead man's sister | to be allowed to grieve, and to stop the invoices | that she has kept paying them, out of a superstitious hope she is ashamed of |
| **Mikko Aalto** (34) | clerk at the Kurvi freight office | to keep a boring job | that he processes the "continuity" accounts and thinks of them as filing |
| **Vesku Ranta** (52) | night dispatcher, depot | to be left alone | that he sells the depot's spare hours as a labour record, for cash |
| **Sanna Kivelä** (29) | Europol liaison officer, Finnish police secondment | the case closed quietly | that a Finnish colleague asked her to bury it, and why |
| **"Continuity" broker** — *name only in play* | runs the small identity shop | to stay small | everything; he is the case's only true antagonist and he never raises his voice |
| **Agent Laura Wendt** | the rookie's partner | to teach without humiliating | that she has seen a continuity file before |
| **Dr. Harri S. Romppainen** | team leader | the paperwork correct | what the footnote reminds him of |

**On names:** Wendt and Romppainen are campaign canon; the others are this manuscript's and may be replaced. **[AUTHOR]** if any of them should be Finnish-Swedish, Russian-speaking, or from a specific Helsinki community, say so — the case does not depend on it, but the city does.

---

## 3. Locations

| in the case | canonical id | note |
|---|---|---|
| the office, the complaint lands | `unsa_hq_ratakatu` (labelled "Europol Helsinki Field Office · Ratakatu") | the address is settled in the data now; older docs call it UNSA |
| the freight office | `kurvi` | the district node; the office itself is a room inside it |
| the depot at night | *`vallila_depot` — **does not exist yet*** | the case gives a canonical fallback: the `kurvi` freight yard. Adding the depot is a one-line data change and needs approval, not a new subsystem |
| a drink that goes wrong | `olutravintola_putki` | |
| the stairwell | `home_helsinginkatu` | the confrontation happens where she lives, which is the point |
| the archive nobody indexes | `unsa_underground` | one scene, late, optional |

---

## 4. The six scenes

Each scene lists: what the player can declare, which CWN skill resolves it, which clues it yields, and what failure
costs. **No essential clue is behind a roll** — that is the investigation module's rule, not this case's invention.

### Scene 1 — The complaint (office, Tuesday morning)

The file is 40 pages of a Lithuanian social-security dispute forwarded by three agencies, each of which has already
decided it is not theirs.

| declaration | procedure | yields |
|---|---|---|
| read the file | **Administer**, access `office` | `clue:complaint` (essential) — the record updated four days after death |
| check the agency chain | **Administer** or **Connect** | `clue:agency_chain` (essential) — three agencies, three disclaimers, one gap |
| ask why Europol has it at all | **Know** (Law & Intelligence) | `clue:jurisdiction` (optional) — a cross-border data-integrity hook, thin but real |
| read the invoices in the annex | **Administer**, inquiry `search` | `clue:invoices` (essential) — a monthly charge to a dead man's account |

**The footnote.** Page 31, in 7-point type: the updates are *manual*. Someone is typing them. That is the case's
first true fact and it is available without a roll, which means the player can have it in the first ten minutes and
still not know what it means.

**Failure is interesting because:** the file can be read carelessly — a failed Administer means the footnote is
missed *now* and surfaces later from a colleague, which is worse, because by then someone has noticed the query.

### Scene 2 — Kurvi (the freight office)

Rows of desks, a kettle, a laminated notice about GDPR that nobody has read.

| declaration | procedure | yields |
|---|---|---|
| interview Mikko Aalto | **Talk**, access `interview` | `clue:continuity_file` (essential) — the account is filed under "continuity", a category that does not exist in the system |
| watch the office while waiting | **Notice** | `clue:second_desk` (optional) — a second keyboard, older, still warm |
| press him about who pays | **Talk** check | `clue:broker_name` (optional) — a first name and a district |
| ask about the sister | **Connect** or **Talk** | `clue:sister_pays` (essential) — Rūta has been paying, and is ashamed |

**Failure is interesting because:** pushing Aalto too hard closes him permanently — he is not brave, he is tired, and
a bad interview makes him transfer the file to a colleague who cannot be found. The clue stays reachable; the
*time* does not.

### Scene 3 — The depot, 02:40

The canonical fallback is the Kurvi freight yard. If the depot is added, it is a tram shed with a night dispatcher,
two idling trams and a heater that sounds like breathing.

| declaration | procedure | yields |
|---|---|---|
| interview Ranta | **Talk**, access `interview` | `clue:spare_hours` (essential) — the depot sells unworked hours as labour records |
| tail a van leaving the yard | **Sneak** / **Drive** | `clue:drop_address` (optional) — a Konala lock-up |
| check the yard's records | **Administer**, access `depot_records` | `clue:payroll_gap` (essential) — the hours are billed to nine people, two of whom are dead |
| photograph the yard without authorisation | **Sneak** | `evidence:unauthorised_photo` — usable, and **inadmissible** |

**Failure is interesting because:** the unauthorised photograph is exactly the kind of thing that closes a case at
trial. The scene gives the player a real advantage and a real cost, and does not tell her which it was.

### Scene 4 — The liaison (office, the same week)

Sanna Kivelä does not want the case closed because she is corrupt. She wants it closed because a Finnish colleague
asked, and because she has seen what happens to a junior officer who makes an interagency problem public in her
first month.

| declaration | procedure | yields |
|---|---|---|
| argue jurisdiction | **Know** (Law & Intelligence) | `clue:liaison_pressure` (essential) — informal pressure, no paper |
| offer a trade | **Talk** | `clue:colleague_name` (optional) — the colleague who asked |
| go over her head | **Lead** or **Administer** | `flag:escalated` — the case survives; the relationship does not |
| drop it | — | `flag:dropped` — a valid ending (§6) |

### Scene 5 — The stairwell

A man is waiting on the landing of the Helsinginkatu flat. He is not a professional. He has a knife because he is
frightened, and he is frightened because the broker told him the police had already been paid.

**This is not a climax.** It is a CWN combat scene whose best outcome is that nobody is seriously hurt, and whose
worst is that the rookie is hospitalised and the case continues without her for a week.

| declaration | procedure | outcome |
|---|---|---|
| talk him down | **Talk** (contested) | he surrenders; `flag:broker_scared` |
| draw and challenge | **Shoot** / initiative | CWN combat; the case does not end here either way |
| retreat and call it in | **Exert** / movement | he runs; the case slows; `flag:runner` |

**Failure is interesting because:** the campaign's first violence should read as *administrative catastrophe* —
injury reports, a review, a partner who is angry in the way that means she cares.

### Scene 6 — The file, the family, the pension

Three lawful resolutions, none clean:

1. **Prosecute the broker.** The continuity shop closes; the invoices stop; Rūta loses the last thing that was still
   sending her brother's name to a machine, and says thank you in a way that does not sound like thanks.
2. **Regularise the scheme.** The family is transferred to a legal survivor benefit after a six-month gap; the
   broker walks because the scheme becomes policy; Kivelä is promoted for "solving a systemic issue".
3. **Hand it to the Finns and walk away.** The case leaves Europol; the player keeps the footnote; the footnote is
   the first thing she cannot explain, and nothing further happens in this episode.

**No correct belief.** The case does not say whether the continuity business is fraud, mercy, or both. It says what
each resolution costs and who pays.

---

## 5. Clue table (the schema the Python step will use)

The `requires` / `opens` / `contradicts` fields are the ones `data/world/lakkahaltia_clues.json` already uses.

| id | essential | competency | access | inquiry | opens | contradicts |
|---|---|---|---|---|---|---|
| `complaint` | yes | Administer | office | read | scene 2 | — |
| `agency_chain` | yes | Administer / Connect | office | read | scene 4 | `official_disclaimer` |
| `invoices` | yes | Administer | office | search | scene 2, scene 4 | — |
| `continuity_file` | yes | Talk | interview | interview | scene 3 | `official_disclaimer` |
| `sister_pays` | yes | Connect / Talk | interview | interview | scene 6 | — |
| `spare_hours` | yes | Talk | interview | interview | scene 6 | — |
| `payroll_gap` | yes | Administer | depot_records | search | scene 5 | `continuity_file` |
| `liaison_pressure` | yes | Know | — | — | scene 4, scene 6 | `agency_chain` |
| `second_desk` | no | Notice | — | — | scene 3 | — |
| `broker_name` | no | Talk | interview | — | scene 5 | — |
| `drop_address` | no | Sneak / Drive | — | — | scene 5 | — |
| `colleague_name` | no | Talk | interview | — | scene 4 | — |

**Contradiction, deliberately planted:** `continuity_file` and `payroll_gap` agree that nine people are billed, but
they disagree about **which nine**. One of the nine has no file anywhere, and the case never resolves who they are.
That is the episode's single crack (§7).

---

## 6. The GM epistemic ledger

The document that lets a GM run an uncanny case without being confused. Five columns, because the setting
distinguishes five different kinds of claim.

| # | what is observed | who reports it | what they believe | what it actually is (authorial) | status at the table |
|---|---|---|---|---|---|
| 1 | a dead man's record updates | the sister, the agency, the file | fraud, error, or a bureaucratic ghost | a clerk typing entries for a paid service | **true**, mundane, provable |
| 2 | page 31: the updates are manual | the file itself | nobody reads it | the case's actual hinge | **true**, discoverable without a roll |
| 3 | the agency chain denies responsibility | three agencies | each believes another one owns it | a real jurisdictional gap, exploited | **true** |
| 4 | the liaison wants it closed | Kivelä | professional caution | a colleague's informal request | **true**, and unprovable — no paper |
| 5 | nine people are billed, two dead | the depot records | a fraud ring | a small cash scheme among tired people | **true** |
| 6 | one of the nine has no file | `payroll_gap` | an error | **undecided by design** — the author has not decided, and the case does not need it | **undecided** |
| 7 | the rookie dreams of a corridor that is not a corridor | her own sleep | stress | **undecided by design** — it may be nothing, and it is the first thing the campaign will later refuse to explain | **undecided** |
| 8 | the broker says "the police were already paid" | the man on the stairs | that he was told the truth | **undecided** — he may have been lied to, or not | **contested** |

**The rule for the GM:** columns 1–4 are safe to state as fact; column 5 is the case; columns 6–8 are the parts you
are forbidden to explain, even to yourself. If the players ask, the honest answer is "nobody in this room knows."

**The dream.** One dream, at the end of the week: a corridor of doors that open onto the same room, and a voice that
says her name in the wrong language. It has no mechanical effect, no clue, no roll and no explanation. If the
player ignores it, it is stress. If she writes it down, she will be right later.

---

## 7. The single crack

Every episode in the roadmap has **one** thing the case cannot explain. Here it is item 6: **a ninth person on a
payroll, with no file, no name, and no invoice.** The clerks call the line "continuity"; the broker calls it a
courtesy; the depot calls it an hours error. Nobody in the case is lying about it, and nobody can produce the person.

It does not need a solution. It is the hook for Case 02 — *the paper that was filed tomorrow* — where the archives
disagree about whether that person ever existed.

---

## 8. The 50 / 25 / 25 at this table

| who | what they do with the complaint |
|---|---|
| **a normie** — Kivelä's colleague, the desk sergeant, the sister's neighbour | "It's a data error. Have you seen the hockey?" They keep the office running, and one of them quietly helps. |
| **an accelerationist** — the broker, a colleague with a side business, a witness who admires the scheme | "Continuity is a service. The state just hasn't legalised it yet." Some of them are predators; some are trying to keep a family afloat. |
| **a doomer** — a colleague who thinks the whole city is rotten, a neighbour, a man on a landing | "This is what they do. It's the foreigners, the machines, the whole thing." He is wrong about the cause and right that something is wrong. |

**No stance is the moral default and no stance is a competence level.** The doomer can be the best investigator in
the room; the accelerationist can be the most generous person in the case.

---

## 9. Tone checks against the scenes

| scene | register target | if it drifts |
|---|---|---|
| 1 | **everyday boredom** with one cold detail | it becomes a briefing; cut exposition, keep the footnote |
| 2 | **satire of denial** and **sympathy** in the same interview | Aalto becomes a clown; he is tired, not stupid |
| 3 | **procedure**, slightly absurd | it becomes a heist; nobody is cool at 02:40 |
| 4 | **political tension**, no villain | Kivelä becomes corrupt; she is afraid |
| 5 | **real stakes**, no heroics | it becomes an action beat; the knife is a frightened man's |
| 6 | **sympathy**, three costs | it becomes a lecture on data protection; end on the sister |

**The failure test for the whole case:** if a player finishes it thinking "so the point was that bureaucracy is
bad", the case failed. If she finishes it thinking "I don't know whether I helped that woman", it worked.

---

## 10. What the Python step will need — after approval only

Not now, and not in this issue's scope unless Tomi says so. When approved, the case becomes:

* a **case graph** in the schema `src/rules/investigation.py` already loads (`case_id`, `scenes[]` with `clues[]`,
  plus `hypotheses[]` — the loader requires at least one **mundane** and one **anomalous** hypothesis, which this
  case has: "fraud ring" versus "something stranger"), and
* a **scene/flag structure** compatible with the graph work (#1178), and
* tests asserting the essential clues are granted without a roll, that the ninth-person clue is reachable from both
  the depot and the freight office, and that no psi path exists.

That is a separate, explicitly authorised change. **Nothing here is a rule.**

---

## 11. Open decisions for the author

1. **The complainant's name and community** — keep Rūta Balčiūnaitė, or make her Finnish-Lithuanian, Estonian, or something else?
2. **The depot** — add `vallila_depot` to the location data, or keep the Kurvi yard fallback?
3. **The ninth person** — leave undecided (recommended), or decide now and write Case 02 backwards from it?
4. **The broker** — does he appear, or is he only a name and a bank account?
5. **The stairwell** — is the knife right for the first violence of the campaign, or too much for episode one?
6. **The dream** — keep it this small, or cut it entirely and let Case 02 be the first crack?
7. **Kivelä** — seconded Finn, Europol career officer, or a local hire who owes someone?
