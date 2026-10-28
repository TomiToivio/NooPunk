# #704 decision register

**Status:** every row is **AUTHOR-PENDING**. Nothing here is ratified, and nothing here changes canon,
code or a licence. Each row records the question, the evidence that exists in the repository, the options,
and a recommendation. The author accepts, revises or rejects each row; #708 tracks the review and #709
tracks implementation.

This register exists because #708 asks for "accept/revise/reject for D704-1 through D704-5" while no
document in the repository defines those five. The packets #708 and #709 cite
(`ISSUE_704_CWN_INVESTIGATION_PROPOSAL.md`, `ISSUE_704_LAKKAHALTIA_PLAYTEST.md`) are not on `main`.
So the decision set is defined here, from the design work that *is* on `main`.

---

## D704-1 — Does competency guarantee the fact?

**Question.** When a character has the relevant competency and declares the relevant inquiry in a scene
they can access, do they receive the core fact without a roll?

**Evidence.** `src/rules/investigation.py::discover` implements the guarantee; `anomaly_gate.py` keeps it
from becoming a conclusion. The GUMSHOE SRD states the principle directly (gathering clues depends on
access, ability and declaration, and "is never dependent on a die roll").

**Options.** (a) Guarantee the fact. (b) Roll for it. (c) Guarantee only passive clues.

**Recommendation: (a).** (b) is the failure mode the borrowing exists to remove; (c) makes the guarantee
depend on referee mood rather than on character build.

**Cost of the recommendation.** The table never stalls on a clue, so pacing must come from pressure
(clocks, institutions, danger) rather than from missing information.

---

## D704-2 — Where do the dice live?

**Question.** If finding is free, what still rolls?

**Evidence.** `discover()` never rolls; `Scene`/`Clue` model access and competency as inputs; the CWN
kernel in `src/rules/` supplies checks and consequences.

**Recommendation.** Dice stay on: **access** (getting into the scene), **interpretation** (which reading
the evidence supports), and **action** (what you do about it, and what it costs). No die on acquisition.

**Note.** This is the single sentence the whole layer reduces to: *no roll to find, roll to explain.*

---

## D704-3 — What counts as competent?

**Question.** Is competency "the skill is present" or "the skill is above zero"?

**Evidence.** CWN treats rank 0 as trained. `Investigator.is_competent` now tests **presence**, and
`from_skills()` builds ratings directly from a CWN skill map. An earlier revision tested `> 0`, which
silently excluded every rank-0 trained character.

**Recommendation.** Presence. A rank-0 specialist is trained and gets the guarantee; an untrained
character does not have the skill at all and may still attempt an ordinary check.

---

## D704-4 — Do investigative spends become a second economy?

**Question.** GUMSHOE spends points from investigative pools for extra information. Does NoöPunk add a
pool?

**Evidence.** No pool exists in `src/rules/`. The ledger's `core.json` carries no investigative resource.
Adding one would create a second currency next to Strain, Effort and credits.

**Options.** (a) No new pool: spends cost time, resource, risk or credibility. (b) Import GUMSHOE pools.

**Recommendation: (a).** (b) duplicates an economy the CWN chassis already has and would need its own
refresh rule, which is exactly the "never add two versions of the same resource" rule in the baseline.

---

## D704-5 — Is the anomaly gate mandatory?

**Question.** May a case be resolved as anomalous before every discriminator has been attempted?

**Evidence.** `src/rules/anomaly_gate.py`: `may_conclude_anomalous()` is false until every core
discriminator is attempted; `provisional_referral()` allows escalation *without* proving an ontology;
`resolve(..., anomalous=None)` records an inconclusive test as a real result.

**Recommendation.** Mandatory for a **conclusion**, permissive for a **referral**. A referral says "this
needs the anomaly desk"; a conclusion says "the world works this way". Requiring proof before a referral
would demand the very thing under investigation.

**Open sub-question for the author.** Should the gate bind only core clues, or also optional ones? Current
implementation: core only, because optional clues are bought and may never be bought.

---

## D704-6 — Attribute model

See `docs/design/ISSUE_710_ATTRIBUTE_CANDIDATES.md`. **Recommendation: A (unchanged CWN) now**, with B
as a reversible presentation-only trial later, and C rejected as a new design rather than a rename.

---

## D704-7 — Licence for rulebook and setting

**Evidence.** `data/sources/game_system_rights.json`: CWN and WWN **CC0** verified; GUMSHOE and Fate
**CC BY 3.0** verified (GUMSHOE row added by #707); Eclipse Phase **BY-NC-SA 4.0**; The Veil **BY-SA
3.0**; SWN and AWN **not established**; Apocalypse World **no grant**. The ledger's own recommendation is
**CC BY-SA 4.0**, status "recommended, not ratified". The repository currently has **no LICENSE file**.

**Recommendation: CC BY-SA 4.0** for rulebook text and setting, plus a `NOTICE.md` carrying GUMSHOE's
mandatory attribution sentence verbatim and Fate's attribution, plus a separate software licence for
code. NC is incompatible with adapting any ShareAlike source and blocks Vasama outright.

**Blocking sub-item.** SWN's licence is unestablished, so SWN psionics must remain **principles-only**
until its SRD's own licence page is read. This is not a formality: it decides whether the psionics pillar
is text adaptation or fresh derivation.

---

## D704-8 — Is the investigation layer the same in the crossover game?

**Question.** `strategy_game/` has its own Fate-based prototype investigation. Does the new layer replace
it?

**Evidence.** The baseline says the crossover's existing Fate implementation is a legacy prototype and not
an exception to the WN direction; the two games remain separate.

**Recommendation.** Do not port the tabletop layer into the crossover by accident. If the crossover uses
it, that is a separate decision with its own migration.

---

## What closing #704 means

It means the design work is delivered and the decision set is defined and tracked. It does **not** mean
any row above is decided, that any licence is chosen, or that the layer is playtested. Those sit in #708
(review and tabletop evidence) and #709 (implementation, including Godot).
