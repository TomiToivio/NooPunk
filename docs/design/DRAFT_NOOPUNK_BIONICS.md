# DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED

# NoöPunk Bionics: engineered biology, not radiation mutants

> **Phase A research + draft (#1137).** Not a rule. Tomi edits, approves or replaces this document. No Python, no
> rulebook change, no CWN modification.

## 1. The author's requirements

Binding source: [`design/BIONICS.md`](../../design/BIONICS.md).

- Bionics are **biopunk and genetic engineering**: "biological not cybernetic machinery", so **a bionic character
  is not a cyborg**.
- "**AWN mutations are too over the top for NoöPunk: bionics are usually not visible at all.** But there is
  overlap. I don't think AWN radiation mutants are realistic."
- Range: from "taking a gene therapy pill" to "complicated medical procedures just like cybernetics", up to
  genetic engineering **before fertilisation** (hybridisation).
- **Three sources of the same kind of object:** human biotech, alien hybridisation, and activation of latent
  human genetics — the last being one of the three routes to PSI.
- A character **may not know she has them**. A hybrid may learn it when the Orion hive-mind contacts her, or when
  Europol tests her.

That last point is a design constraint, not flavour: concealment is the default and discovery is a **scene**.

## 2. Existing rules, and where the numbers would come from

| Source | Section target | Use | Rights |
|---|---|---|---|
| **CWN** | Character creation, cyberware, System Strain | **Base system. Never modified** | CC0 SRD |
| **AWN** | Mutations, positive/negative point costs | **Balance inspiration only** — evaluate before adopting | Unverified; no import |
| **SWN Deluxe** | Transhuman / transhuman tech | Comparison for continuity and shells | **No verified text licence**; shape only |
| **WWN** | — | Not used here | CC0 SRD |
| **Repo** | `src/rules/cwn_cyberware.py`, `data/rules/cwn_*.json` | Existing cyberware economy the draft must sit beside | Implemented |

**Do not manufacture AWN point values.** If the AWN mutation economy is adopted, it is adopted *after* someone
reads the book and records the exact section. Until then this draft proposes a shape, not numbers.

## 3. What differs from AWN mutations

| AWN mutation | NoöPunk bionic |
|---|---|
| Acquired by exposure, often radiogenic | **Deliberately chosen, purchased, prescribed or inherited** |
| Often visible, often stigmatised | **Usually invisible**; detectable by tests, not by looking |
| Random | Selected by the character, the clinician, or the parent |
| Point-buy with drawbacks | Cost in money, access, time, legality and risk — not necessarily drawbacks |
| Fantasy-flavoured powers | **Plausible 2045 biotechnology**, with exotic variants tagged separately |

The reason to keep AWN in the conversation at all is its **economy of positive and negative traits**, which is a
ready-made balance device. The reason not to import it wholesale is that NoöPunk bionics are engineered,
concealed, and often acquired before play.

## 4. Real-world anchors (evidence tiers)

| Claim | Tier | Note |
|---|---|---|
| Ex-vivo gene editing is an **approved clinical therapy** for sickle cell disease and β-thalassaemia (CASGEVY / exagamglogene autotemcel) | (a) established, approved | FDA pages verified for this draft: STN 125787, ages 2+; STN 125785, ages 12+ |
| Personalised **in-vivo** editing has been performed in named-patient settings | (b) experimental demonstrator | *NEJM* (2025), issue-provided; single cases, not a product |
| Somatic editing requires delivery vectors, conditioning, immune management, and months of clinical process | (a)/(b) | This is why "one pill" is **not** a route to arbitrary genome design |
| Germline editing of embryos is feasible in principle | (c) ethical/legal minefield | Illegal or tightly restricted nearly everywhere; in NoöPunk it is exactly the kind of thing a bureaucracy exists to refuse |
| A pill that grants a chosen complex trait | — | **Not established.** **[FICTION]** at the very edge of 2045 plausibility |

**Explicit statement for the rulebook:** there is **no established real-world one-pill route to arbitrary complex
genome redesign or superpowers.** Where the fiction needs one, it is labelled as fiction.

## 5. Draft catalogue shape (not numbers)

Two tiers, visibly separated in any rulebook text:

**Tier 1 — mundane-plausible (a/b anchors):**
- **Therapeutic edits** — correct a condition; no adventure-facing bonus, but a person who no longer has the
  condition is a different person socially.
- **Metabolic tuning** — sleep, temperature tolerance, endurance. Small, boring, very useful to an investigator.
- **Sensory refinement** — better hearing or night vision; a disadvantage in loud or bright environments.
- **Immune conditioning** — resistance to a specific hazard; visible in a medical test.
- **Latent-expression unlock** — the awakening route. **Eligibility for PSI, never a PSI effect in itself.**

**Tier 2 — exotic, tagged `[NHI]` or `[HYBRID]`:**
- Hybridisation traits; unusual pigmentation, unusual metabolism, unusual lifespan.
- **Always** flagged as faction/setting material, **never** in the default catalogue, **never** a player pick
  without explicit GM authoring.

## 6. Draft procedures

| Element | Draft |
|---|---|
| **Acquisition** | Requires a clinician, a facility, and time. Cost is money **and** access **and** legal exposure. A backstreet clinic is cheaper and riskier — a scene, not a discount |
| **Concealment** | Default **not visible**. Detection needs a medical test, a scan, or a specialist. Europol can test; so can a corporation |
| **Legality** | Registration law mirrors the author's PSI/ET/hybrid rules: permitted with paperwork, and unregistered is a crime |
| **Failure** | Off-target effects, immune reaction, incomplete expression. Failure is a **medical complication**, not a mutation table |
| **Reversibility** | Some edits are permanent. Say which, in the catalogue, before purchase |
| **System Strain** | Only where CWN already uses it for a comparable intervention. **Do not invent a second strain currency** |

## 7. Separation from the other four systems

| This is… | …not this |
|---|---|
| Bionics — modified biology | **CWN cybernetics** — machinery |
| Bionics | **Psychotronics** — a technological PSI interface |
| Bionics **may unlock eligibility** for PSI | Bionics **never contain a PSI mechanic**. No bionic telepathy |
| Bionics are usually invisible | Cyberware is usually visible; psychotronic implants are somewhere between |

**Anti-stacking:** a latent-genetics unlock does not grant an ability; it moves the character from "cannot" to
"can attempt", using the **same** PSI effect implementation as every other route.

## 8. Tabletop examples

1. **The pre-employment test.** Europol's medical finds a hybrid marker the character did not know about. No
   mechanics change; the character's entire legal situation does.
2. **The cheap clinic.** A witness bought endurance tuning at a backstreet clinic. The complication is the
   clinic's other customers, not the tuning.
3. **The unrevealed hybrid.** A PC carries a `[HYBRID]` tag known only to the GM; the Orion contact in Act 2 is
   the first time it matters.

## 9. Python model and interface (design only)

```python
# proposed, NOT implemented
@dataclass(frozen=True)
class Bionic:
    id: str
    tier: Literal["mundane", "exotic"]
    visible: bool                  # default False
    detectability: str             # "medical_test" | "scan" | "specialist"
    permanence: Literal["permanent", "reversible"]
    psi_eligibility: bool          # eligibility only — never an effect

def detect(bionic: Bionic, *, method: str) -> bool: ...
```

The one invariant worth testing in Phase C: **no `Bionic` may carry a PSI effect**, only an eligibility flag.

## 10. Open decisions for Tomi

1. Does a gene-therapy pill exist in 2045 for *simple* edits, or is all editing clinical?
2. Should bionics cost a CWN resource at all, or only money/access/legality?
3. Is hybrid status always detectable by Europol tests, or can it be hidden indefinitely?
4. Do bionics have drawbacks, or is cost enough? (AWN's negative traits are the alternative model.)
5. How much of the Sörnäinen/hybrid registration apparatus should be playable rather than background?

## 11. Bibliography

- Author: `design/BIONICS.md`.
- CWN Free Edition SRD — character creation, cyberware, System Strain (CC0, immutable).
- AWN Mutations — edition/section **to be recorded when an authorised copy is read**; no numbers adopted here.
- SWN Revised Deluxe, Transhuman — shape only; **no verified text licence**.
- FDA, CASGEVY (STN 125787 / 125785) — verified for this draft; ages 2+ and 12+ respectively.
- *NEJM* (2025), personalised in-vivo editing — issue-provided, tier (b).
- *Frontiers in Psychology* (2026) — critical review of quantum-consciousness claims (context for §4's fiction
  boundary).
- Internal: `src/rules/cwn_cyberware.py`, `docs/rules/CWN_IMMUTABLE_CORE_1068.md`.
