# The Sampo Protocol — playable pilot draft (#626)

**Status: playable draft for playtesting, not canon.** No new named characters, no mandates, no dates,
no rules changes. Names below are **placeholders** until the author rules; the people, the ward and the
outcome of this case are fiction written for the table, exactly as `strategy_game/casework/kallio.py`
treats the canonical 2045 frame.

Companion documents: the planning memo and its canon conflicts in
[`../design/ISSUE_626_NORTHERN_NOOSPHERE.md`](../design/ISSUE_626_NORTHERN_NOOSPHERE.md), the author-only
questions in [`../design/ISSUE_626_OPEN_QUESTIONS.md`](../design/ISSUE_626_OPEN_QUESTIONS.md), and the
mechanical baseline in [`../rules/WN_BASE_SYSTEM.md`](../rules/WN_BASE_SYSTEM.md).

---

## 0. What this pilot is for

It tests one thing the setting claims and has never yet had to prove at a table: **a case that can
legitimately end "this was illness", "this was fraud", "this was an intelligence we do not understand" —
and the players cannot tell which is which until they have done the work.** The design obligation is
that the anomalous reading is never handed to them by the plot.

Two rules for the person running it:

1. **The anomaly is not the reward for solving the mystery.** Credibility is the reward; truth may stay
   contested after the last scene, and that is a finished case.
2. **Every red herring is cleared by evidence, never by narrator fiat.** If a false lead cannot be
   disconfirmed by something the players can find, it does not go in.

## 1. Shape of play

| element | value |
| --- | --- |
| Players | 3–5, each running one team member; one may run a patient as a second character in scenes 2 and 4 if the table wants it |
| Sessions | 4 (one per act); 3 if the table skips the cross-border leg |
| Frame | the 2045 campaign present; the team is working a cluster referred from a Helsinki ward |
| Unit of progress | **evidence entries in the ledger**, not plot beats |
| Failure state | no total failure; failure means the team substantiates less, or pays a cost in trust, consent or safety |

**Team roles to fill (unnamed on purpose).** A clinician (psychiatrist or clinical psychologist); a
forensic neuropsychologist; a police investigator holding the actual Finnish police powers; a
digital/BCI forensics officer; a folklorist or historian of religion; optionally the PSI-sensitive
specialist. Whoever coordinates with Europol does not thereby gain arrest powers — the police
investigator is the one who acts.

**Ledger.** Every find enters the existing evidence ledger (`src/rules/investigation_evidence.py`):
`provenance` is one of `physical`, `digital`, `testimony`, `psi_lead`, `other`, and each entry carries
*where*, *who collected it* and *a custody event*. Nothing the team "just knows" is evidence, and a
`psi_lead` is never proof — it is a reason to go and look somewhere.

## 2. Checks

WN kernel only (`docs/rules/WN_BASE_SYSTEM.md`): `2d6 + attribute modifier + skill level ≥ difficulty`,
ladder **6 simple · 8 significant · 10 expert · 12 master · 14 extreme**. Attributes are the six canon
ones (INT, WIS, CHA, DEX, CON, STR).

Difficulty is set by **how much the entry can substantiate**, not by how important it is:

* **6** — an obvious, already-present detail (what the chart says, who was on shift).
* **8** — needs competence: matching two records, reading a protocol correctly.
* **10** — needs expertise: a clinical differential that survives scrutiny, a technical claim verified.
* **12** — contested: a patient's account that contradicts the record, a trace with a plausible innocent explanation.
* **14** — the case's hardest single substantiation; success here is the difference between a report and a finding.

A failed check does not withhold the clue in most cases: it yields it **with a defect** (wrong collector,
broken custody, an unverified date) so the ledger shows the cost later. Only the three entries marked
*[gated]* below are lost on failure, and every one has a second route.

Skill names follow the WN vocabulary once #615 settles it; until then read "an INT-know check" as "the
appropriate knowledge skill at its current name".

## 3. Act 1 — Riget (the ward)

Setting: a Helsinki university-hospital psychiatric unit mid-renovation, plus a regional hospital two
hours away that is slated for closure. Staff are competent and tired; two departments hate each other;
the paperwork is absurd and matters.

Scenes: shift handover; the ward round; the patient who is not on the list; the night incident; the
records request that the department head stalls.

| # | Evidence | Provenance | Where / how | What it substantiates | What it falsely suggests | Check |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Three admission notes, three wards, same described structure | digital | records audit, three hospitals | the cluster exists across institutions | a shared published source | INT, diff 8 |
| E2 | The ward's own copy of a 1990s place-name survey | physical | ward library, bottom shelf | one motif detail existed locally before the patients | the patients read it | INT, diff 6 |
| E3 | Patient A recalls a room she never entered, with one wrong detail | testimony | interview, trauma-informed, consent first | the account has internal structure and an error | telepathy | WIS, diff 10 |
| E4 | Night-shift log gap of 34 minutes | physical | paper log, nurse's station | someone was present who is not recorded | an abduction | INT, diff 6 |
| E5 | The unaccounted patient's file is sealed by a research ethics board, not by psychiatry | physical | records office | the patient arrived through a **study**, not through the ward | a conspiracy in the hospital | INT, diff 10 |

Act 1 ends when the team has E5. Until then the case looks like ward gossip, which is the point.

**Cost hook.** Each interview conducted without proper consent costs the team a **trust token** with the
ward staff; three lost tokens and the department head stops cooperating, closing the fastest route to
E5 (the slow route, through the ethics board, remains).

## 4. Act 2 — Maniac (the trial)

Setting: a neurostimulation / BCI trial with industry funding, its consent forms, its washout failures
and its imagery archive.

| # | Evidence | Provenance | Where / how | What it substantiates | What it falsely suggests | Check |
| --- | --- | --- | --- | --- | --- | --- |
| E6 | Consent form v3 removes the clause about "shared imagery" | digital | trial document history | the imagery was **expected**, then de-emphasised | the trial caused it | INT, diff 8 |
| E7 | Imagery from two patients, different sites, 91 % structural similarity | digital | trial archive, similarity run | the experience is not idiosyncratic | the machine is broadcasting | INT, diff 10 |
| E8 | One patient's imagery predates their enrolment | digital | device logs vs. session dates | the phenomenon is **not** device-caused | log tampering | INT, diff 12 |
| E9 | Washout protocol was shortened to hit a funding milestone | physical | lab notebook, printed | misconduct exists, independent of any anomaly | misconduct explains everything | INT, diff 8 |
| E10 | A staff member's private note: "they describe our forest site, we never published it" | testimony | a researcher who wants out | a location the trial never disclosed | the researcher is the source of the leak | CHA, diff 10 |

Act 2 ends with E8 or E10. **E8 is the load-bearing clue of the whole pilot**: it kills the simplest
technical explanation without replacing it with an anomalous one.

## 5. Act 3 — X-Files (the archive and the permit)

Setting: the cross-border leg — a briefing in The Hague, a sister cohort in another member state, an
archive that was never digitised, and a municipal permit office in eastern Finland.

| # | Evidence | Provenance | Where / how | What it substantiates | What it falsely suggests | Check |
| --- | --- | --- | --- | --- | --- | --- |
| E11 | A 1987 research station was built on the described site, closed 1994 | physical | municipal permit history | the described structure **existed** | it still exists | INT, diff 6 |
| E12 | The closure report's annex is missing from every copy but one | physical | regional archive, 2 h drive | something was removed deliberately | the state covered up an anomaly | INT, diff 12 |
| E13 | The sister cohort's details are 80 % identical, and differ exactly where the 1987 site's layout differs | digital | comparison across cohorts | the accounts are anchored to a **place**, not to a text | a shared delusion | INT, diff 12 |
| E14 | The station's comms mast was licensed to a defence contractor | digital | regulator's public register | a present-day interested party exists | the contractor is the villain | INT, diff 8 |
| — | The environmental inspector's permit history *[the very Finnish beat]* | testimony | municipal office, unannounced visit | E11 and E14 without a warrant or a favour | — | CHA, diff 6 (or none, if the team asks politely) |

Two of the memo's threads meet here: the **bureaucratic route** (permits, registers, annexes) is faster
and less glamorous than the intelligence route, and rewards the team that treats a municipal official as
a person with a filing system rather than an obstacle.

## 6. Act 4 — Northern Noösphere (the site)

Setting: a forest research station, a dead mast, a faction arrival, and a folklorist who is careful with
what a tradition does and does not mean.

| # | Evidence | Provenance | Where / how | What it substantiates | What it falsely suggests | Check |
| --- | --- | --- | --- | --- | --- | --- |
| E15 | Local place tradition names the site, but for a *boundary*, not a treasure | testimony | village, elder, with consent and a translator if needed | the tradition is about crossing, not abundance | the Sampo is buried there | WIS, diff 8 |
| E16 | Speech changes the anomaly's behaviour *only* when it names relations, not when it names objects | psi_lead | structured on-site protocol, repeated | language is operative, and not as a password | the right word opens a door | INT, diff 14 *[gated: second route = E15 + E12]* |
| E17 | The station's array is still powered, from a source nobody registered | physical | site survey | the site is maintained by someone | the contractor runs it | INT, diff 10 |
| E18 | A faction's own instrumentation, abandoned mid-use | other | site, after the arrival | a rival reading of the site is being tested, not just claimed | the faction caused the phenomenon | INT, diff 8 |

**No scene in Act 4 settles what the site is.** The three readings (scientific, noetic, political) each
account for a different subset of E11–E18, and the table should be able to argue for at least two of them
at the end.

## 7. Red herrings, and how each is cleared

| False lead | Why the table will chase it | Disconfirming evidence | When it is available |
| --- | --- | --- | --- |
| **Information leakage in the ward** | it explains everything cheaply | E2 (the survey predates the patients) + E13 (geography, not text) | Act 1 → Act 3 |
| **The device broadcasts the imagery** | E7 is uncanny | E8 (imagery predates enrolment) | Act 2 |
| **Research misconduct explains the case** | E9 is real and damning | misconduct is *proved* and still leaves E1, E13 unexplained | Act 2 → Act 3 |
| **The contractor is behind it** | E14 and E17 point at them | the contractor's own site logs show the phenomenon preceding its interest | Act 3 → Act 4 |

A table that stops at a red herring still has a case — a fraud case, an ethics scandal — but it is a
lesser ending, not a wipe.

## 8. Branch points and endings

Four decision points, each of which is a **choice about consequence**, not about solving:

1. **D1 — safeguarding vs. speed** (Act 1): suspend the interviews and lose a session, or continue and
   spend trust.
2. **D2 — the patients' story** (Act 2): keep it in the clinical record (protects them, buries it), or
   move it into the investigative file (exposes them, preserves evidence).
3. **D3 — who owns the site** (Act 3–4): refer to UNSA, keep it inside the Europol cell, or hand it to the
   municipality as a land-use matter.
4. **D4 — the intelligence** (Act 4): negotiate, contain, or cut the site off.

| Ending | Trigger | What the team gets | What it costs |
| --- | --- | --- | --- |
| **A. The careful report** | E13 + E15 substantiated, D2 kept clinical | the cluster is documented without exposing patients; no anomalous claim is made | the case is filed as "unexplained, monitored"; nobody is helped now |
| **B. Publish** | E8 + E12 + any two of E11/E13/E16, D2 → investigative file | the misconduct and the site's history become public | patients are identified; two careers end; the site is sealed by others |
| **C. Contain with UNSA** | D3 → UNSA, E17 or E18 | the site is secured, the cluster stops growing | the team loses the file; the patients become a security matter |
| **D. Stop the experiment** | E9 + E6 + E10, D3 → keep local | the trial is halted, the researcher protected as a witness | the anomaly is untouched and unstudied |
| **E. Negotiate** | E16 *or* (E15 + E18), D4 → negotiate | something answers, on its own terms, and keeps answering | the answer is not a finding: no report can carry it, and the team is changed |

**No ending is a reveal.** A, D and B can be played with the anomaly never confirmed; C and E can be
played with illness excluded. The case file never states which is true, because the team cannot know.

## 9. What a null result looks like

For each act, the honest failure mode — useful for the person running it, and the reason the case is
about method rather than monsters:

* Act 1 null: the cluster is ward culture; E1 is one enthusiastic nurse, E5 is an ordinary ethics
  dispute. Case closes as an audit.
* Act 2 null: E8 comes back *not* predated; the imagery is device-shaped after all. Case closes as
  a device-safety finding.
* Act 3 null: E11's site is unrelated geography; E13's 80 % is publication contamination. Case closes as
  a folklore-driven delusion with a real fraud attached.
* Act 4 null: E16 fails twice; the site is a maintained industrial remnant. Case closes as trespass,
  fraud and one very patient contractor.

Any of these is a finished, playable case. If a table reaches one, the anomaly was not disproved — it was
not demonstrated, which is a different sentence and the one the setting needs.

## 10. Open items this draft does not decide

Carried to [`../design/ISSUE_626_OPEN_QUESTIONS.md`](../design/ISSUE_626_OPEN_QUESTIONS.md): the unit's
institutional home, whether the leader is the canon patient or another person of the same name, how far
the *Maniac* touchstone is imported, whether patients are playable, and how many anomalies may be
confirmed before the Crisis tipping point. This draft is written so that **any** answer to those leaves
the case playable: the team is described by role, the ward is generic Helsinki, the faction that arrives
is whichever one the author wants, and no patient is named.
