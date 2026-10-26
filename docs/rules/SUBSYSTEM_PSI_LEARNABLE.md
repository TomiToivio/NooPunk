# PSI: SWN-shaped, natural and learnable

**Status: design specification. No cost, cap or progression number is approved.**
Owner layer: **A**, per the #566 ruling. Layer B's PSI (capability tags, Fate action, rating/consensus/pressure)
is **approved (#482) and unchanged**.

## 1. The two author rulings this encodes

> **Scientific framing (not rules):** the field-coupling vocabulary this subsystem borrows, and its limits, are recorded in [`docs/research/SOUL_AS_QUASI_FIELDS_NOTES.md`](../research/SOUL_AS_QUASI_FIELDS_NOTES.md). That note is a preprint-based framework, not evidence; the rules below stand on their own.

1. **PSI is learnable.** It is a human capacity that can be trained, taught and practised — not a birthright,
   not a class feature, not a mutation, and not a virus. Canon already supports this and is the reason the
   structure below is a *training* structure rather than a talent list:
   - `rulebook/6_PSYCHIC.md` §6.1 — "PSI is natural, not viral";
   - `rulebook/21_PSI_PARADIGM_SHIFT.md` — perception, dreams, selfhood and **training** shift together, and
     "public breakthroughs in experimentation, interpretation, **training** and psychotronic assistance change
     the scale of attention and institutional response".
2. **The *shape* is SWN's.** Not its ontology, not its psionic disciplines as written, and not the assumption
   that psi is a separate character class. SWN's mechanical shape is: a small number of *core capabilities*
   everyone with the gift shares, a **cost pool** that is spent and committed, and *techniques* that are learned
   individually.

## 2. What is adopted, and what is refused

| SWN element | disposition | why |
|---|---|---|
| **Cost pool, spent and committed** | **ADOPT the shape** | It is the same shape as WWN's Effort (matrix row 25): an ongoing effect keeps resource tied up, so a sustained psychic burden costs without a second hit-point track. The pool is *content-free*, so it carries no SWN ontology. |
| **Core capability before techniques** | **ADOPT the shape** | Learning is staged: a character can perceive before they can act. This is what makes "learnable" meaningful rather than cosmetic. |
| **Techniques learned individually** | **ADOPT, author the list** | The list is NoöPunk content and must be authored here (AGENTS.md §1). No SWN technique text enters. |
| **Psionic "disciplines" as a taxonomy** | **MODIFY** | NoöPunk's `rpg/psi.py` already names **modes of action** (`TELEPATHY`, `REMOTE_PERCEPTION`, `PRECOGNITION`, `PSYCHOKINESIS`, `RESONANCE`, `SYNCHRONICITY`, `RITUAL`, `SHARED_DREAM`, `PSYCHOSURGERY`, `PSYCHIC_HACKING`, `NOETIC_DEFENSE`, `NOETIC_RECONNAISSANCE`) — each a *kind of act*, not a power. That vocabulary is canon for layer B and is the right vocabulary for layer A too. |
| **"Psychic" as a class** | **REFUSE** | #566 declines classes; PSI is a capacity, not a role. |
| **Virus / infection origin** | **REFUSE** | Canon §6.1. Any conversion that makes PSI contagious has broken the setting. |
| **SWN discipline text, names, tables** | **REFUSE** | SWN has **no verified SRD licence** (see `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`). Mechanics may be reimplemented independently; text may not. |

## 3. The learning model

Four stages, because "learnable" has to mean something at a table:

1. **Latent** — the capacity is present but unusable under pressure. Evidence is ambiguous: a dream, a hunch, a
   coincidence. The character cannot yet act.
2. **Perceptive** — perception works (the `INTUITION`, `REMOTE_PERCEPTION`, `SYNCHRONICITY` modes), still
   unreliable. This is where most trained people stop.
3. **Practised** — techniques are learnable individually, and each has a cost. Reliability is a function of
   practice, not of level.
4. **Mastery** — the character can commit resource for sustained effects and can teach. Teaching is the
   reproduction condition of the whole subsystem: **PSI spreads through people, not through exposure.**

Stage 4's "can teach" is deliberate. It makes PSI a social phenomenon — schools, lineages, frauds, licenses,
state registries — which is the political content the setting wants, and it is the mechanism by which the
capability becomes *ubiquitous* without becoming *viral*.

## 4. What PSI is not allowed to do

These are the constraints that keep the subsystem from eating the game:

- **It does not make investigation obsolete.** `rulebook/21` §"Limits": most sessions are partial, ambiguous or
  inconclusive; counter-PSI, contradictory testimony, limited reach, privacy rights and deceptive entities apply.
- **It does not prove anything.** A psychic impression is *evidence*, not a verdict; the existing uncertainty
  vocabulary governs.
- **It does not erase consent.** Effects that change another person cross `CrossLayerEffect`'s gate
  (`consent_required`), the same gate psychosurgery uses.
- **It does not stack with technology for free.** Psychotronic assistance is a distinct entry mode (canon §6.2)
  and its interaction with the cost pool is unauthored.
- **It does not create innate PSI in a witness.** Already proved:
  `test_psi_scenes.py::test_nothing_creates_innate_psi_in_the_witness`.

## 5. What is deliberately left open

`rulebook/21` already declares these unresolved, and this document does not resolve them:

- **specific training costs** and time;
- the **size and refresh** of the cost pool;
- whether the pool is one number or per-mode;
- the **technique list** and each technique's cost;
- whether psychotronic devices add to the pool, draw from it, or bypass it;
- whether the crossover will ever track noetic resources mechanically (canon says it may not).

## 6. Testable contract

Structure can be tested before any number is authored:

1. **Learnability is staged** — a Latent character cannot perform a Practised action; the refusal is a
   permission failure, not a high difficulty. (A refusal, not a penalty: same discipline as the access gate.)
2. **Cost is committed, not merely spent** — an ongoing effect holds resource until released, and releasing is
   an explicit act.
3. **Consent gate** — a consent-required effect without consent is `permitted == False`, not a failed roll.
4. **No contagion** — witnessing never grants or improves PSI.
5. **Determinism** — the same seed and the same declared state produce the same outcome.

Item 5 already holds for layer B (`test_psi_scenes.py::test_it_is_deterministic`); items 1–4 are the new
subsystem's acceptance tests.
