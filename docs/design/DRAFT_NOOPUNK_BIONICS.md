# DRAFT — NoöPunk Bionics: deliberate biological enhancement, not radiation mutation

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED**
>
> Phase A of [#1137](https://github.com/TomiToivio/NooPunk/issues/1137). Proposal only: no Python, no rulebook
> chapter, no equipment entry, no CWN change. This document exists to be edited or rejected by the author.
>
> Companion drafts: [Psionics](DRAFT_NOOPUNK_PSIONICS.md) · [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md) ·
> [Europol rookie](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md) ·
> [Tags](DRAFT_NOOPUNK_CHARACTER_TAGS.md).

**Evidence key:** **[a]** established clinical technique · **[b]** experimental demonstrator with limits ·
**[c]** contested hypothesis · **[d]** NoöPunk fiction.

---

## 1. What the author already decided

From [`design/BIONICS.md`](../../design/BIONICS.md), which is binding and predates this draft:

* Bionics is **"similar to AWN mutations"**, but it is **biopunk modification of a human being**.
* **"AWN mutations are too over the top for NoöPunk: bionics are usually not visible at all."** The author
  rejects **radiation mutants** as unrealistic.
* The same system covers **human technology**, **alien hybridisation**, and **latent human genetics awakening**.
* **It is not cybernetics.** "So bionics does not make a character cyborg."
* Range: "as simple as taking a gene therapy pill", or "complicated medical procedures just like cybernetics",
  up to "the most extreme modifications … done before fertilization (hybridization)".
* **A character may not know she has them** — a hybrid can learn it when the Orion hive-mind contacts her, or
  when Europol tests her.
* Bionics **overlaps PSI**: some modifications grant lesser abilities, some unlock actual PSI. It **explains
  where the PSI came from** — and it is one of the three sources, never a fourth.

Everything below is an attempt to make that a **table procedure**. Where the author's note is silent, this draft
proposes and marks it.

---

## 2. Existing rules and the exact comparison

| source | edition / location | what it gives | what we borrow | what we refuse |
|---|---|---|---|---|
| **AWN Mutations** | *Ashes Without Number (Deluxe)*, **Mutations p. 16**, Negative Mutations **p. 18**, Positive Mutations **p. 20** | mutation points, positive/negative trade, physical oddities | the **point-buy shape** as a balance *inspiration*; the idea that a drawback funds a benefit | radiation origin, visible stigma, obligatory weirdness |
| **SWN Transhuman** | *Stars Without Number (Revised Deluxe)*, **Transhuman Campaigns p. 248**, Character Generation **p. 253**, Transhuman Polities **p. 262**; Cyberware **p. 82** | a campaign frame where bodies are chosen; species/culture as packages | the *frame* — enhancement as a normal life choice with social and legal texture | its setting, its polity politics, its xenobiology |
| **CWN cybernetics** | SRD §Cyberware; `src/rules/cwn_cyberware.py`, `cwn_strain.py` | surgery, cost, strain, complications, removal | the **acquisition grammar** (procedure → difficulty → complication → cost) | nothing — cybernetics stays machinery; bionics must not borrow its resource |
| **CWN core** | [`CWN_IMMUTABLE_CORE_1068.md`](../rules/CWN_IMMUTABLE_CORE_1068.md) | attributes, skills, saves, combat, advancement | the whole resolution spine | any change to it |
| **NoöPunk tags** | `data/rules/noopunk_tags.json` | typed tags with duration, source, stacking | bionic effects as **tags**, drawbacks as **status tags** | a second stat block per implant |

**The design consequence of "not visible":** AWN mutations are *evident* — that is their whole aesthetic and their
balance (people react, institutions hunt). NoöPunk bionics are *invisible by default*. If the drawback is not
visible stigma, the balance must come from somewhere else. Three candidates:

1. **Detection risk** — a test, a scanner, a blood sample can find it; being found is the cost.
2. **Maintenance** — a modification needs a clinician, a prescription or a supply, and supply is leverage.
3. **Eligibility instead of power** — a bionic may only *unlock* something (PSI, resistance, recovery), and the
   something still has to be paid for elsewhere.

This draft uses all three and **never** uses "it looks weird" as the price.

---

## 3. Real-world anchors, with their limits

| claim | tier | source (date) | limit |
|---|---|---|---|
| Ex-vivo CRISPR therapy for sickle cell / β-thalassaemia is **approved** | **[a]** | FDA supplemental approval of Casgevy for ages ≥2 (press release, content current 1 Jul 2026), https://www.fda.gov/news-events/press-announcements/fda-approves-first-gene-therapy-young-children-sickle-cell-disease | **autologous stem cells, full myeloablative conditioning** (chemotherapy-grade), hospitalisation, mucositis and febrile neutropenia as common harms. Not a pill |
| **Patient-specific, in-vivo** base editing has treated one infant | **[b]** | *NEJM* 392(22):2235–2243 (published 15 May 2025), https://www.nejm.org/doi/full/10.1056/NEJMoa2504747 | N=1; bespoke design for one variant; **lipid-nanoparticle delivery to the liver**; two infusions; regulatory approval obtained for that one therapy |
| Somatic gene editing has off-target and immune risks | **[a]** (established as risk classes) | clinical literature summarised in the above | must be stated in any fictional catalogue; a "no side effects" modification is a lie |
| Germline editing is illegal in most jurisdictions and ethically contested | **[a]** (legal fact) / **[c]** (ethics debate) | national law and the 2018 He Jiankui case | NoöPunk's prenatal design is therefore **criminal** in the EU, which is a plot, not a menu |
| Whole-genome "designer" rewrites | **fiction [d]** | — | no established route to arbitrary complex redesign; the setting may have one, and should say it is experimental, expensive and mostly fails |

**What this forbids in the draft:** a single injection that grants superhuman strength; a modification with no
delivery problem; a bionic that works better the more you buy; and any implication that current medicine can do
what the setting's clinics do.

---

## 4. The three acquisition routes

Bionics are not one thing bought one way. Three routes, three costs, three kinds of consent.

| route | fiction | who can get it | cost | failure mode |
|---|---|---|---|---|
| **Prescribed therapy** | a licensed clinician, a diagnosis, a course of treatment | anyone with access and a reason | time, money, side effects, a record in a medical database | the condition returns; the record exists |
| **Elective procedure** | a clinic, a surgeon, an anaesthetic | anyone who can pay and sign | surgery difficulty, recovery, complications (CWN-shaped) | the same complication table as cyberware, with biological entries |
| **Prenatal design / hybridisation** | decided before birth, by parents, a corporation or an alien programme | **nobody chooses this for themselves** | it is not a purchase; it is a backstory | illegal, undocumented, and often unknown to the character |

The third route is the one that makes NoöPunk's PSI biology coherent: **hybrids and latent-gene awakenings are
not elective**. A player may *discover* one; a player may not *shop* for one.

**Latent activation** is a fourth thing that is not a purchase at all: a modification that was always there and
turns on under stress. It is the cheapest and the most dangerous, and it belongs to the GM until the character
learns what it is.

---

## 5. Draft catalogue shape: two tiers, no stat blocks

The issue asks for "a minimal catalogue of mundane-plausible enhancements and separately tagged exotic
NHI/hybrid variants". This draft proposes **categories with one tag each**, not a price list.

### 5.1 Mundane-plausible [d, extrapolating from a]

| category | effect, as a tag | drawback | concealment |
|---|---|---|---|
| **Metabolic tune** | a status tag that resists fatigue or hunger for a day | needs a supply; withdrawal is a scene | invisible; detectable by blood test |
| **Somatic resilience** | one step better on a healing or recovery check, once per case | slow onset; expensive | invisible |
| **Sensory tuning** | a bonus to Notice in one narrow band (low light, low sound) | oversensitive: a penalty in the opposite band | invisible |
| **Latent-gene marker** | **eligibility** for PSI, nothing else | it does nothing until something wakes it | invisible until tested |
| **Hybrid lineage** | eligibility for PSI **and** an NPC faction's interest in you | you did not consent; someone else did | invisible, until someone recognises it |

Each row is a **tag with a source**, exactly like `data/rules/noopunk_tags.json` — no attribute changes, no new
pools, no separate damage model.

### 5.2 Exotic / NHI [d]

Kept strictly separate and **flagged in the tag's source field** (`source: nhi_hybrid`):

* abilities that look like PSI but are **biological** (a hybrid's telepathy is still resolved by the psionics
  procedures — one implementation, two origins);
* regeneration or resistance that is **not** a hit-point multiplier but a scene-level permission ("this wound
  closes over a day");
* anything the Orion programme would build. These are **antagonist capabilities first** and player options only
  by author decision.

**AWN's economy is not adopted wholesale.** AWN's positive/negative mutation trade is a *balance* device for a
game where mutations are forced on you. NoöPunk's bionics are **chosen, paid for, concealed and legal-or-not** —
a different economy. The draft borrows the *idea* that a drawback can fund a benefit, and prices the drawback in
**detection, supply and obligation** instead of points.

---

## 6. Two tabletop examples

**Example A — the elective procedure.**
A rookie wants low-light vision after a night case. It is a clinic visit: a CWN-style procedure check, a
complication roll, two days of recovery, and a medical record that exists forever. Mechanically she gains a tag
`eyes: tuned_low_light` and a status tag `recovering: 2 days`. No attribute changes. In Act II, a Europol
biometric scan reads the record and asks why an officer has an unregistered modification.

**Example B — the thing she did not choose.**
A suspect's blood work shows a marker the lab has seen eleven times before. The character is not the suspect —
she is the *officer* who ran the test, and the marker is hers. The GM now has a `latent_gene` tag with
`source: unknown`, and the player has a question. Nothing mechanical happens until Act II's awakening, when the
tag becomes eligibility for telepathy — and the eligibility is the *only* thing the bionic gave her.

---

## 7. Python model / interface proposal (design only — Phase B)

```
src/rules/noopunk_bionics.py
    @dataclass Bionic(kind: str, tier: str, source: str, tags: Sequence[str], drawback: str)
    def eligibility(*, bionic: Bionic, effect: str) -> bool        # PSI eligibility, not a power
    def procedure_cost(*, tier: str) -> dict                       # difficulty/cost, no invented prices
    def concealment(*, bionic: Bionic, test: str) -> str           # invisible | detected | documented
    def detect(*, bionic: Bionic, method: str) -> bool
```

Rules:

* **Eligibility is a boolean, never a bonus.** `eligibility` answers "may this character attempt the effect",
  and the effect's own module prices it.
* **No second resolution.** Procedure costs reuse `cwn_cyberware`'s surgery/complication functions where the
  fiction is surgery; a test must assert the bionic path calls the same function, not a copy.
* **No prices invented.** `procedure_cost` returns difficulty and time; money comes from CWN's economy or the
  author's decision.
* **One origin per tag.** `source` is mandatory, so a save file can always answer "why can she do that?"

---

## 8. Interaction and precedence

| with | rule |
|---|---|
| **CWN cybernetics** | separate: machinery vs biology. A character can have both, and they cost different things (strain vs supply/detection). |
| **Psionics** | bionics grant **eligibility**, never a parallel mechanic. A hybrid's telepathy is the telepathy draft's procedure. |
| **Psychotronics** | a device is external technology; a bionic is the body. A bionic never needs an operator. |
| **AWN** | comparison only. Nothing from AWN's mutation lists is imported as text or numbers. |
| **Tags** | every bionic effect is a tag with a `source`; drawbacks are status tags. |
| **Acts** | I: none, unless the pregen carries an undiscovered marker. II: first anomaly, first test, first question. III: elective or coercive procedure becomes available. IV: exotic/hybrid capabilities surface, as threat and as revelation. |

---

## 9. Open decisions for Tomi

1. **Do bionics have a points budget at all**, or are they entirely fiction + tags? (The draft leans tags.)
2. **Is the drawback always detection/supply/obligation**, or may some bionics be simply better with no cost?
3. **Can a player buy a bionic mid-campaign**, and does that require a clinic scene every time?
4. **Prenatal design:** backstory only, or a late-campaign revelation that the protagonist is one?
5. **How much of AWN's positive/negative trade survives** as a balancing instinct?
6. **Are hybrid markers the same test** as latent-gene markers, or two different institutional procedures?
7. **Do bionics interact with System Strain at all?** Recommendation: no — keep the resources distinct.

---

## 10. Bibliography (checked in this pass)

| source | date | status |
|---|---|---|
| FDA — Casgevy supplemental approval, ages ≥2 | content current 1 Jul 2026 | confirmed, read in full |
| *NEJM* 392(22):2235–2243 — patient-specific in-vivo base editing | 15 May 2025 | summary and metadata confirmed; body paywalled |
| AWN Deluxe — Mutations p. 16, Negative p. 18, Positive p. 20 | — | page anchors from `data/rules/awn_sections.json` |
| SWN Revised Deluxe — Transhuman Campaigns p. 248, CharGen p. 253, Polities p. 262, Cyberware p. 82 | — | page anchors from `data/rules/swn_sections.json` |
| He Jiankui germline case (2018) | 2018–2019 | cited as legal/ethical context; not re-verified in this pass |
| `design/BIONICS.md` | author, undated | the binding brief; quoted, not paraphrased away |
