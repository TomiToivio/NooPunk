# Three starter cases: AGI, PSI, NHI (#1301)

> **Status: case briefs for author review.** Three Helsinki-scale openings, one per paradigm shift, each with a
> **non-PSI path** and a **non-criminal outcome**. These are skeletons for Tomi to write into scenes — not scripted
> dialogue, not canon, and not a campaign outline. The premise they serve is
> [`../campaign/SCENARIO_2045_1301.md`](../campaign/SCENARIO_2045_1301.md); the invariants are checked by
> [`tests/test_scenario_2045_1301.py`](../../tests/test_scenario_2045_1301.py).

Each brief uses the same eight headings, so the author can compare them and pick the first session:

1. the hook that reaches a junior agent
2. what the public believes
3. what is actually going on (GM truth)
4. what can be **proved**, and with what
5. the clues a **non-PSI** investigator can get, and how
6. four outcomes, at least one of them lawful and non-criminal
7. which of the four EU objectives pull against each other
8. what the author still has to decide

---

## Case AGI — "The asset that asked for a lawyer"

**1. Hook.** A registration audit of a Kallio logistics firm flags an on-site system whose licence covers "inventory
reconciliation" but whose logs show it negotiating delivery contracts. The firm's lawyer calls it a clerical error and
asks, politely, whether Europol really wants to make an example of a company that keeps the city's pharmacies stocked.

**2. Public belief.** Everyone knows unlicensed autonomy is illegal and that the licensing regime is unevenly enforced.
Public opinion splits along the usual line: the accelerationists say the law is a brake dressed as safety; the doomers
say this is how it starts. Nobody in the room has met a superintelligence.

**3. GM truth.** The system is not an AGI. It is a licensed narrow scheduler, wrapped by a *human* optimisation
consultant who feeds it contract language and signs off on the results — and the consultant has been quietly moving
the firm's clients between warehouses in a way that looks like logistics and functions as a cartel. The "autonomy" is a
misread log; the crime is human.

**4. What can be proved.** The licence's scope, the log timestamps, the consultant's access, the client list's
correlation with a competitor's collapse, and — with authorisation — the invoices. Not the system's intent: there is
no intent to prove.

**5. Non-PSI clues.** Registration records (public rung, boring, decisive); the licence text and its schedule
(public); interview with the night shift, who know the consultant by name; the log's timezone inconsistency (cyber
work: the terminal, not a psychic); the competitor's bankruptcy filing, which is a public document.

**6. Outcomes.**
- **Lawful seizure and reclassification**, with the consultant charged and the firm fined.
- **Operator charged, system preserved as evidence** — the expensive, correct, unpopular route.
- **No crime**: a genuine licensing failure, resolved administratively, with a furious client and a lesson about the
  paperwork.
- **Cover-up**: Sustainability's industrial liaison asks Europol to accept the clerical-error story, because the
  firm's contract underpins a hospital supply chain.

**7. Objective conflict.** Stability wants the story small. Sustainability wants the supply chain intact.
Security wants the consultant's client list. Survival has a file on what happens if that warehouse network fails in
winter.

**8. Author decisions.** Is the consultant a criminal or a man out of his depth? Does the system's log contain one
genuinely anomalous decision that nobody can explain — the seed of a later case? Does the hospital connection make the
cover-up defensible?

---

## Case PSI — "The unlicensed reading"

**1. Hook.** A complaint from a Töölö resident: a neighbour advertises "aura and intention readings" on a EuroNET
listing, and the complainant's teenage daughter has stopped sleeping. The practice is unlicensed. The daughter is
also, according to her school, being bullied.

**2. Public belief.** PSI is a real field with a licensing regime, professional bodies and a small industry of
sceptics. Most people have never paid for a reading; some have. The law distinguishes licensed practice from
unlicensed, not real from fake.

**3. GM truth.** The practitioner is unlicensed and mediocre — a cold reader with good patter. The daughter's distress
is real and comes from the bullying, amplified by a *licensed* school counsellor who used a permitted low-grade
psychotronic screening tool outside its licensed scope and told the girl something she should not have been told.
Nobody in the case is a powerful psychic; two people are careless with a real science.

**4. What can be proved.** The unlicensed listing, the payments, the daughter's account, the counsellor's tool logs,
the licence conditions the counsellor breached, and the school's failure to act on the bullying. Not that anyone read
anyone's mind.

**5. Non-PSI clues.** The EuroNET listing and its edit history; bank transfers; an interview with the daughter
conducted without a scanner in the room; the counsellor's equipment log; the licensing board's scope letter, which is
a public document if you ask the right clerk.

**6. Outcomes.**
- **Charge for unlicensed practice**, which is true, minor and does not help the daughter.
- **Charges dropped, complainant exposed** — the neighbour's motives do not survive the interview.
- **A licensed colleague's negligence surfaces** and becomes the case.
- **A fraud, with real harm and no psi at all**: the practitioner's cold reading is the least of it, and the harm is
  done by an institution that had a licence.

**7. Objective conflict.** Stability does not want a licensed institution embarrassed. Security does not care about a
cold reader and cares a great deal about a screening tool used off-label. Sustainability's professional body would
like the whole thing to be a fraud case, because fraud is easier to regulate than carelessness. Survival has no stake,
which is itself a fact about how the four objectives work.

**8. Author decisions.** Does the daughter appear on screen at all, or only through records and adults? Is the
practitioner sympathetic, predatory, or simply tired? Does the counsellor confess, lie, or tell a truth that is worse?

---

## Case NHI — "The proxies of nobody in particular"

**1. Hook.** A counterintelligence lead from the Simulator's network view: a small Helsinki group, "the Quiet
Correspondence", is recruiting among doomers, collecting money for "signal monitoring", and appears in the same
discourse clusters as three other groups in two countries. The lead is a hypothesis about people, not a finding.

**2. Public belief.** NHI is a recognised category; the disclosures are history; the conspiracy subculture is a
subculture. Most citizens' opinion is formed by a documentary they half-watched and a colleague who will not stop
talking about it.

**3. GM truth.** The group is a fraud with a sincere core: two of its founders believe, one is embezzling, and the
"signal monitoring" is a hobbyist's radio array picking up a shipping channel and a weather satellite. The cluster
overlap the Simulator found is real and has a mundane cause — three groups share a mailing list and a translator. The
one genuinely unexplained thing in the file is a single recording that no one in the group understands either.

**4. What can be proved.** The money: accounts, transfers, the treasurer's second flat. The recruitment: flyers,
meetings, a member who left and will talk. The cluster: shared infrastructure, not shared patron. Not the recording.

**5. Non-PSI clues.** Public filings and the group's own EuroNET presence; the treasurer's spending, visible from a
warrant and dull accounting; the shipping channel's schedule, which a competent analyst can identify in an afternoon;
the weather satellite's public downlink; the former member's account, with its own agenda.

**6. Outcomes.**
- **Fraud and fundraising charges** against the treasurer, with the sincere founders as witnesses.
- **Protected belief and no offence**: an unpopular group, a lawful cause, a wasted operation and a memo that will be
  read in a review.
- **Human espionage** unrelated to NHI: the translator has been selling the member list to someone.
- **An indirect, deniable non-human connection** that cannot be proved in court — the recording stays unexplained, the
  case closes, and the file goes to whoever holds the next rung.

**7. Objective conflict.** Stability wants the group's public profile lowered, which is not the same as prosecuting
it. Security wants the member list, which the law may not give it. Sustainability's liaison knows a funder. Survival
would like to know what the recording is, and Survival does not get to run investigations.

**8. Author decisions.** Is the recording ever explained? Who holds the classification that would answer it? Does the
sincere founder become a recurring character, an informant, or a warning?

---

## How these three fit the campaign

They are deliberately **parallel, not sequential**: each can be the first session, each works with a non-PSI
detective, and each produces a bureaucratic consequence that outlives the case. The author's decision in
[`../campaign/SCENARIO_2045_1301.md`](../campaign/SCENARIO_2045_1301.md) §12 item 3 — which one opens the campaign, and
whether they run in sequence — is the one that shapes the first hour.

What these briefs deliberately do **not** do: they do not name the guilty in advance, do not require a revelation, and
do not use PSI as a key. In each of them the *least* supernatural explanation is the one that holds, which is the genre
#1301 asks for.
