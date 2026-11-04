# NoöPunk Bionics: AWN Mutations Reinterpreted as Biopunk Engineering

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED.** Issue [#1137](https://github.com/TomiToivio/NooPunk/issues/1137); researched 2026-11-04. Planning only; do not implement, modify the CWN core, or copy a published ruleset. **Evidence labels:** [E] empirical/approved; [X] experimental; [H] contested theory or parapsychology; [F] fictional 2045 premise; [P] draft mechanics. Tomi edits this proposal first, then separately authorizes matching tabletop and Python implementation.

## Preflight: what already exists for this subsystem

- **Author canon — binding:** [`design/BIONICS.md`](../../design/BIONICS.md) — bionics are biological, not
  cybernetic ("does not make a character cyborg"), **usually not visible at all**, and one of the three PSI
  sources (latent genetics / hybridisation / psychotronics).
- **Not this:** `src/rules/cwn_cyberware.py` is machinery; Psychotronics is a device interface. Both are separate
  subsystems and neither may be folded into bionics.
- **Campaign anchor:** `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` §2.1 fixes the rookie's issued kit, which is
  where a latent bionic or hybrid marker would be discovered.

## Core idea
**[P]** Reuse the **mechanical shape** of AWN Mutations for **deliberately engineered biological traits**, with source/visibility/treatment and availability tags, not the fiction of accidental radiogenic monsters. Same effects for human gene editing, alien hybridization and dormant human potential, but distinct provenance and legal/social consequences. Biological modification is **not cyberware** and does not by itself imply a conscious-machine implant. See author's [BIONICS.md](../../design/BIONICS.md).

## Published-rule source comparison
- **AWN Deluxe Mutations**, printed pp.16–25: beneficial/negative mutations, Mutation Points, selection randomness/choice, stigmas, some activated abilities and strain; read exact entries and costs from the authorized book before proposing matching mechanical equivalence. The source's mandatory mutation stigma and randomness are **not accepted as NoöPunk defaults**.
- **AWN Deluxe Mentalist**, printed pp.264–269: some mutation-like effects may actually be better resolved as Mentalist/PSI; **do not duplicate** Telepathy via both a mutation and psychic class.
- **SWN Revised Deluxe Transhuman**: compare posthuman bodies, augmentations and identity/biological transfer where the actual licensed edition supports them; **verify chapter/edition and specific text before pricing**, rather than inventing a "Transhuman Point" cost.
- **CWN**: baseline human attributes, skills, cyberware and System Strain are immutable. A bionic trait adds explicit new ability/permission only; any +1 modifier must have a bounded defined scope and stacking rule.

## Scientific plausibility check (as of 2026-11-04)
| Tier | Real-world anchor | Fictional extrapolation |
|---|---|---|
| [E] Targeted ex vivo edited cell therapy | FDA **Casgevy** approvals since 2023, expanded to children age 2+ in July 2026: https://www.fda.gov/vaccines-blood-biologics/casgevy ; https://www.fda.gov/news-events/press-announcements/fda-approves-first-gene-therapy-young-children-sickle-cell-disease | Biopunk clinics offering specialist treatments, but real intervention is an involved medical treatment, not a generic pill for super-strength |
| [X] Individualized in-vivo editing | Personalized CPS1 deficiency editing case, *NEJM* (2025): https://www.nejm.org/doi/full/10.1056/NEJMoa2504747 ; NIH assessment https://www.nih.gov/news-events/nih-research-matters/infant-rare-disease-receives-customized-gene-therapy | 2045 targeted treatments can be more routine, but delivery, variable targeting and follow-up remain plausible complications |
| [X] Brain/gene associations | Human traits like intelligence, endurance and temperament are generally multifactorial and environment-dependent | Precise one-gene "intelligence boost" or total personality rewrite is not demonstrated |
| [H/F] Dormant PSI genetics and alien hybridization | No established human genetic locus for telepathy, and no verified alien hybrid programmes | Explicitly *in-universe*: rare latent PSI expression, NHI hybrid biological design and awakener events |
| [F] Exuberant AWN effects | Physics-breaking mutations belong to a genre toolbox | Reserve exotic phasing/force fields as NHI-tech or PSI powers requiring independent approval |

## Rule design proposal
1. **Bionic Trait** with `id,source,procedure,visibility,detectability,tier,prerequisites,benefit,cost,risks,legacy_awn_reference`. Sources = `engineered_human | hybrid | dormant_trait | exotic_nhi`.
2. **Acquisition:** planned selection at legitimate clinic by default; **[OPEN]** use an adapted **AWN-style point budget** for starting/replacement traits, with no fake mutation lottery. Clinical access, money, body compatibility, training time, lawful permit and procurement rules matter; rare developmental variants may require germline-stage construction. More plausible minor interventions can be convenient oral/infusion therapies **in 2045 fiction only**, but do not assert instantaneous universal editing.
3. **Visibility:** **Concealed is default**, not automatically `Stigma`; `Detectable by genetic scan` is separate from external appearance. More overt cosmetic and exotic traits are intentionally optional. If removing stigma enhances power, balance via eligibility/cost/scan risk, not free mechanical advantage.
4. **Negative effects:** AWN negative mutations are **not** mandatory drawbacks for ordinary elective care. Explicit experimental complications (immune reaction, unstable expression, delayed onset, fertility or off-target risk, social stigma) are scene-specific/tagged. Do not force a degrading genetic stereotype.
5. **Effect catalogue (small first-pass):** `Low-Light Vision` (sensory augment), `Pathogen Resistance` (bounded save interaction), `Improved Recovery` (bounded CWN healing/System Strain interaction only after audit), `Metabolic Efficiency` (AWN scarcity environment only), `Spatial Orientation` (specific Notice/Survive applications), `Neural Interface Compatibility` (eligibility for a device but **not free PSI**). All costs/bonuses **TBD pending author approval and edition verification**.
6. **Exotic-only [F]:** radical body morphing, unusual alien sensory modalities and inherited hybrid traits require research-specific limits; **no free telekinesis, immortality, teleportation or astral projection** by saying "genes".
7. **PSI linkage:** latent bionic trait may confer `EligibleForPsiAwakening`, but **the activated Telepathy/Defence/Astral effect is defined only in the PSI module**. Three sources (latent human, hybrid, psychotronic-assisted) share one effect library and distinct origin tags.
8. **Compatibility:** no stacked alternate mutation HP/damage rules; CWN core handles saves and injury. Check System Strain load for any surgery/biological burden against current CWN APIs, not a new automatic genetic Strain tax. Reuse AWN hazard rules only in affected regions.

## Campaign fit
- **Act I:** normal rookie; BCI/psychotronic implants are *not* Bionics. No mandatory bionic enhancements.
- **Act II:** a discovered dormant genotype or experimental biometric inconsistency may be a **scripted clue**, not an automatic proof of alien ancestry; pre-authored awakening unlocks a PSI effect in its own module.
- **Act III:** clinics, illegal hybrid trafficking and research facilities create *investigative decisions*. Elective enhancements optional where legal and available.
- **Act IV:** more advanced hybrid/NHI variants could become available after author approval, without replacing SWN PSI.

## Tabletop example
A clinical laboratory detects an unexpected inherited allele in the rookie. Mark `Latent Trait: Unidentified` (GM-only) and `Medical Follow-up Required` if disclosed. No combat bonus or telepathy is granted. Later, the authored awakening changes eligibility and unlocks the approved Telepathy technique through **PSI**, while tests on the allele may affect social reputation and regulatory disclosure. The same rules work if a different character acquired a purchased sensory enhancement via elective therapy.

## Data/API proposal, not implementation
`BionicTrait{trait_id,source,delivery,visibility,detectability,benefit_id,risks,unlock_condition,consent,legal_status}`; `BionicProcedure{availability,facility,price_or_resource,clinical_stage,followup}`; `grant_trait` / `activate_latent_trait` / `apply_wn_effect` operate as adapters around existing CWN checks. Do not mirror the whole AWN mutation catalogue or reuse proprietary text.

## Alternatives for Tomi
- Is Bionics acquisition point-priced (AWN-inspired), resource-priced (CWN equipment), or hybrid by type? **Recommend** money/access for elective procedures, explicit budget for unusual starting traits, and tags for dormant discoveries.
- Should all humans have latent PSI, with activation gated by experience, while hybrids receive reliably earlier activation? This is author's fiction, not scientific fact.
- Does the first rookie have a known Bionic treatment, or only an unknown latent trait?
- Are adverse effects randomly rolled for risky experiments, or fixed by procedure design? Prefer fixed probability only if author wants gameplay risk.
- How much of SWN transhuman embodiment/resleeving should be separated into its own later module rather than overloaded into this human-bionics draft?

**Next gate:** Tomi edits this draft; then future implementation adds tabletop and Python parity/tests in the same approved PR.

---

## Merged review pass — what this section adds

A second draft of this same subsystem was written in parallel on the same day; this file and that one were
reconciled rather than shipped twice. The earlier text above stands as the base. The sections below are the
material it did not contain: quantified procedures, the audit results, and the decisions that need a number
rather than a principle.

### Three acquisition routes, because "how you got it" is the character

| route | fiction | who can get it | cost | failure mode |
|---|---|---|---|---|
| **prescribed therapy** | a clinician, a diagnosis, a course of treatment | anyone with access and a reason | time, money, side effects, a permanent medical record | the condition returns; the record exists |
| **elective procedure** | a clinic, a surgeon, an anaesthetic | anyone who can pay and consent | surgery difficulty, recovery, complications (CWN-shaped) | the same complication table as cyberware, with biological entries |
| **prenatal design / hybridisation** | decided before birth by parents, a corporation or an alien programme | **nobody chooses this for themselves** | it is not a purchase; it is a backstory | illegal, undocumented, often unknown to the character |

Plus a fourth that is not a route at all: **latent activation** — something always there that turns on under
stress. It belongs to the GM until the character learns what it is.

This is what keeps the author's brief honest. The brief says a character may not even know she has bionics; a
purchase model cannot produce that, and a discovery model can.

### Where the balance comes from when nothing is visible

AWN's mutations are evident, and their price is stigma. NoöPunk's are concealed, so the price has to be three
other things — all of them fictional, none of them a points deficit:

1. **detection** — a scan, a blood test, a record; being found out is the cost;
2. **supply** — a clinician, a prescription, a maintenance interval; supply is leverage;
3. **obligation** — whoever provided it now has an interest in you.

An elective bionic with no detection risk, no supply line and no obligation is simply a free advantage, and
should be refused at the table.

### Eligibility is a boolean, never a bonus

`eligibility(bionic, effect) -> bool` answers only "may this character attempt it". The effect itself is priced
by the psionics procedures. A test must assert that a bionic can never create a second Telepathy implementation,
and that a hybrid's telepathy resolves through the same code path as an awakening's.

### Implementation notes

* Surgery routes **reuse** `cwn_cyberware`'s surgery/complication functions rather than copying them; a test
  asserts the same function is called.
* No invented prices: the procedure returns difficulty and time, and money comes from CWN or the author.
* Every trait carries `source` (`engineered_human | hybrid | dormant_trait | exotic_nhi`), so a save file can
  always answer "why can she do that".
