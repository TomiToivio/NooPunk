# #626 — the questions only the author can answer

**Status: decision support, not canon.** Each row states what canon already fixes, the options with
their consequences, and what unblocks once answered. Answering a row turns it into an acceptance record
and a PR; it does not require a new subsystem.

Companion: [`ISSUE_626_NORTHERN_NOOSPHERE.md`](ISSUE_626_NORTHERN_NOOSPHERE.md) (memo, canon conflicts,
ontology), [`../scenarios/626_SAMPO_PROTOCOL_PILOT.md`](../scenarios/626_SAMPO_PROTOCOL_PILOT.md) (the
playable draft these answers plug into). Queue rows **D40–D47** in
[`AUTHOR_DECISION_QUEUE.md`](AUTHOR_DECISION_QUEUE.md) carry these one sentence at a time.

---

## Q1 — Europol, Finnish police and UNSA: what is the mandate?

**Canon already fixes this.** Europol has exactly one **NHI Desk**: one analyst, a filing cabinet, a
basement office in The Hague, "a unit that officially doesn't exist"; **coordinating authority, not
direct** — it works *through* member-state police, and canon states Europol has no AGI branch, no PSI
branch, no triple mandate and no psi-rated agents
(`legacy/ubiquitous_maniacs/docs/reference/laclaugpt/HELSINKI.md`). UNSA is the Helsinki campaign frame
(`rulebook/20_FIRST_CONTACT_AND_PSI_AWAKENING.md` §5, beat 9).

| Option | What it costs |
| --- | --- |
| **A. Desk grows under joint-investigation-team cover** (recommended shape) | nothing in canon moves; the growth is a story event. A multi-person team is then a *result*, not a premise — which also means the pilot's Act 1 team can be smaller than the memo's six roles |
| **B. New standing Europol cell** | contradicts the one-analyst Desk; requires an explicit canon edit and a reason nobody noticed a new unit |
| **C. National unit with Europol liaison** | cheapest legally, weakest for the memo's "cross-border cluster" premise |

**Unblocks:** the pilot's team composition and who may arrest, search or compel — today the police
investigator holds those powers and the coordinator does not.

## Q2 — Who is "Dr. Inspector Harri Romppainen"? (and *which* Romppainen?)

**Canon is split, and this is the memo's real continuity problem.**

| Carrier | Says |
| --- | --- |
| `docs/scenarios/01_FIRST_DAY_IN_OMAPPI.md` | *"draft scenario names except for Dr. Harri Romppainen"* — so the name is deliberate; he is the one who "requested a graduate", and he solves cases through psychology rather than as a generic detective |
| `docs/archive/NARRATIVE_TIMELINE_VARIANTS.md` | "Dr./Inspector **Harri S. Romppainen**, Supo, PhD in psychology" — archived variant, not canon chronology |
| `legacy/ubiquitous_maniacs/TERAPIASESSIO.md` + 126 files in the legacy tree | Romppainen as a **patient**: "vielä dissosioituneessa sivupersoonassaan", a lab subject |

| Option | What it means |
| --- | --- |
| **A. Same man, and the unit is staffed by someone whose dissociation is the case** | strongest dramatically: his competence and his illness are one question, and the memo's ethics rule is embodied by the leader. Most expensive: it commits canon to his treatment, recovery and reliability |
| **B. Different man, same name** | cheap and safe; the legacy patient stays untouched, the investigator is new. Costs the resonance |
| **C. The memo's slip: he is a patient consulted as a witness, and the "investigator" framing is dropped** | preserves both carriers exactly; loses the memo's protagonist |
| **D. Same man, integrated and recovered, leading the unit** | keeps the name and the unit; asserts a clinical outcome canon has never stated — the largest unearned claim of the four |

**Sub-question the memo asks and canon leaves open:** how does *Dr. Inspector* work — a medical doctor
with police authority, or two titles from two systems? The pilot deliberately writes the role as
"clinician + a separate investigator with the powers", so it plays under any answer.

**Unblocks:** naming anyone else in the unit (a leader's identity fixes the chain of command), and whether
the leader can be a player character.

## Q3 — Is the cell the precursor of Helsinki UNSA, a partner, or its own campaign?

Canon's 2045 present already opens with the player leading a faction from the **Helsinki Field Office**
with Laura Falk ("Minerva") as a party agent. Options: **precursor** (the cell's failure or success
explains why UNSA exists), **partner** (two bodies, one case, competing files), **separate** (its own
campaign, no crossover). Precursor is the only one that spends canon; separate is the only one that costs
nothing.

**Unblocks:** whether UNSA appears in the pilot as a referral partner (as drafted) or as a rival.

## Q4 — How much *Maniac* is imported?

The memo itself flags the ambiguity: Norwegian original (2014) and Netflix adaptation (2018) differ in
tone, in the trial's ethics and in what the shared simulation is *for*. Options: **thematic only**
(psychiatry, trial ethics, shared imagery — no plot), **one specific work as touchstone** (naming which),
**both, deliberately contrasted**. The pilot as drafted uses thematic only, which is the only option that
commits to nothing.

**Unblocks:** how much of Act 2 is a homage and how much is original — and therefore the attribution
review.

## Q5 — Are patients witnesses, victims, investigators, recurring NPCs, or playable?

Canon has no hospital cast. Options: **witnesses only** (safest: they are people with accounts, not
mechanics), **witnesses + one recurring patient** (gives the series a face), **one playable patient**
(the ethics rule becomes a live constraint at the table: your own character's credibility is at stake).
The pilot supports all three; it names no patient so that option 2 or 3 stays open.

**Unblocks:** the pilot's session-2 and session-4 scene ownership, and whether a patient character sheet
ever exists.

## Q6 — How many anomalies may be verified before the Crisis tipping point?

This is a *setting-scale* question with mechanical consequences: if verification is possible, then the
pipeline (evidence → substantiation → institutional response) needs a threshold; if it is never possible,
the setting stays permanently contested and no faction can be proven right. The pilot's design assumes
**demonstrated ≠ confirmed**: the team can substantiate that an account is structurally anchored to a
place (E13), never that a nonhuman intelligence exists.

**Unblocks:** whether any future case may end with the word "confirmed" — and with it, whether the NHI
Crisis is a reveal or a permanent condition.

## Q7 — Is the Sampo one artefact, a class, a misread legend, or observer-dependent?

Three readings are already drafted in the memo (§3 of the planning doc): scientific / noetic / political.
Adding "a class of technology" or "different things to different observers" changes what the pilot's Act 4
can do: a single artefact supports a heist plot; a class supports an economy; observer-dependence supports
the Vallée-style reading the memo prefers. The pilot is written so the site's *reading* is contested and
never resolved, which survives all four.

**Unblocks:** whether later material may name a second Sampo-like site.

## Q8 — Do medical phenomenology and data analysis become core investigative mechanics?

Today the mechanics are the WN kernel plus the evidence ledger (`src/rules/investigation_evidence.py`,
provenance + custody, deterministic, no automated proof). Making *phenomenology* a mechanic means a
clinical-differential procedure with its own cost — and canon has no such subsystem. Making *data
analysis* one means cohort comparison as a procedure (E7/E13 are written as exactly that).

**Licensing constraint that shapes the answer** (`docs/rules/RULES_FOUNDATION_POLICY.md` §4, full detail
in `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`): CWN and WWN publish SRD text that may be used
within its terms; **SWN and AWN have no separately licensed public SRD**, so their mechanics may be
reimplemented but their text, tables and trade dress may not be copied. Any "SWN-style Effort" or
"AWN-style hazard" in NoöPunk therefore has to be *NoöPunk's own wording over a borrowed shape* — which is
cheaper than it sounds, and is an argument for keeping these two procedures original rather than
borrowed.

**Unblocks:** whether the pilot stays a scenario document or becomes a `strategy_game/casework` case with
code — which would then need tests, because it would be code.

---

## What answering these does *not* require

No canon edit is needed to play the pilot. Every question above is written so the draft plays under any
answer: the team is described by role, the ward is generic, patients are unnamed, the faction that arrives
is the author's choice, and the case's truth is never stated. Answers change *what the material claims*,
not whether it can be run.
