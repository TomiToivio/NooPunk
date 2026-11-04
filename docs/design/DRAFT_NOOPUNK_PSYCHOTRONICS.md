# DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED

# NoöPunk Psychotronics: QIP devices, neurotechnology, and institutional coercion

> **Phase A research + draft (#1137).** Not a rule. Tomi edits, approves or replaces this document. No Python, no
> rulebook change, no CWN modification.

## 1. The author's requirements

Binding source: [`design/BIONICS.md`](../../design/BIONICS.md).

- QIP-based psychotronics **amplify or mediate natural latent PSI** and therefore **always require a conscious
  human operator**. They are installed as **cybernetic implants** or used as **external devices**.
- Some devices are **not** QIP: microwave-radiation and similar apparatus need **no operator** — and "are not real
  PSI either".
- Non-QIP devices **cannot be installed as cybernetic augmentations**: "they would fry your meat."
- QIP is also the basis of experimental **mind uploading and resleeving** — rare, experimental, not ubiquitous.
- Europol's default kit for a rookie: a **BCI** plus a **basic defensive psychotronic implant**.

The design consequence is a hard separation the draft must preserve: **a device that needs a psychic operator is
not the same kind of object as a device that manipulates a brain without one.**

## 2. Three engineering categories (do not merge them)

### A. QIP-based psychotronics — **[FICTION]**, in-setting speculative

| Property | Value |
|---|---|
| Requires conscious operator | **Yes**, always |
| Form | Cybernetic implant **or** external device |
| Function | Amplifies, focuses, stabilises or mediates the operator's own latent PSI |
| Resource | Uses the operator's PSI resource (never a second pool — see §6) |
| Failure | Strain, feedback, calibration drift, signature leakage |
| Legal | Registered; Europol/Eurodef issue them; private ownership is regulated |

### B. Non-QIP neurotechnology — **evidence-grounded extrapolation (tiers a/b)**

Implanted or non-invasive BCI, EEG/fMRI decoding, neurofeedback, electrical/magnetic/focused-ultrasound
stimulation, conventional drugs, sensory priming, propaganda and psychological influence.

| Property | Value |
|---|---|
| Requires psychic operator | **No** |
| Requires instead | Infrastructure: trained individual baselines, cooperation, clinical supervision, time |
| Reality anchor | Decoding needs subject-specific training and cooperation; stimulation is experimental and focal, not general control |
| Use in play | Legitimate police/medical tools, and the source of false positives — a device that looks like mind reading and is not |

### C. Institutional coercion and counterintelligence — **fiction inspired by history**

MKULTRA-shaped programmes, absurd mind-reading helmets, flashing-light laboratories, media campaigns, memes,
drugs, interrogation psychology. Model these as **investigations, ethical and rights questions, consent and
exposure** — never as an executable procedure for coercing a person. The Sörnäinen PSI prison already exists in
author canon as exactly this kind of controversy.

## 3. Real-world evidence tiers

| Claim | Tier | Consequence for design |
|---|---|---|
| Clinical implanted BCI restores communication/movement for paralysed patients | (a) approved/established in narrow indications | Real, but requires surgery and a clinical team |
| Non-invasive decoding of speech/imagery is possible with training and cooperation | (b) experimental demonstrator | Works because the subject cooperates — the opposite of coercion |
| fMRI semantic reconstruction (Tang et al., *Nature Neuroscience* 2023) | (b), paywalled, re-verify | Not a general-purpose thought reader |
| Transcranial focused ultrasound modulates deep regions (2025) | (b), issue-provided, not re-read | Focal, experimental, not mind control |
| A helmet that reads arbitrary thoughts | — | **Not established.** NoöPunk aesthetic, not engineering |
| QIP amplification of PSI | (c) hypothesis in reality / **[FICTION]** in 2045 | Setting premise, stated as such |

**Warning written into the draft for the rulebook:** every one of these devices must fail in a way a player can
see coming. The interesting NoöPunk scene is the device that *almost* works and the institution that insists it
works.

## 4. Draft mechanics (CWN-compatible)

Keep it small. **No hardware energy economy** until reliability, calibration, privacy and countermeasures exist
as tags.

| Element | Draft |
|---|---|
| **Installation** | Cyberware (implant) uses existing CWN cyberware procedure and System Strain where CWN says so. External devices are ordinary equipment with bulk/carry implications |
| **Enable vs boost** | Every device declares exactly one: it *enables* a technique the user could not do, or *boosts* one they can. Never both, never silent |
| **Activation cost** | Cost lives on the **character's** PSI resource, not a device battery. A device with no operator cannot produce PSI, so a "device charge" would be fiction that contradicts the premise |
| **Calibration** | A calibration tag, set at acquisition and after any hard use. Uncalibrated = disadvantage or unreliability, not malfunction comedy |
| **Signature** | Active QIP use is detectable. Detection is the countermeasure that makes police work interesting |
| **Maintenance** | Ordinary equipment upkeep; a broken implant is a scene-level problem, not a resource minigame |
| **Lawful use** | Europol-issued devices carry authority; private devices carry registration and warrant requirements. **No device grants a legal power** — evidence obtained by an unlawful PSI search is a legal problem, which is a plot, not a penalty table |
| **Countermeasures** | Shielding, dampening rooms, Sörnäinen-grade suppression. These are environmental conditions, not a new subsystem |

## 5. Tabletop examples

1. **The helmet in the basement.** Investigators find a non-QIP helmet wired to a chair. It does nothing but
   flash. The case is about who believed it worked and what they did in that belief. No PSI mechanics at all.
2. **The calibration failure.** A rookie's defensive implant is overdue for calibration during a confrontation.
   The GM calls a disadvantage on the defence check, states it before the roll, and the scene is about trusting
   the kit.
3. **The unregistered device.** A psychic runs a *Ubik*-style service with an unregistered QIP amplifier. The
   case is procurement, registration and liability — not a duel of beams.

## 6. Interactions, anti-stacking, precedence

- **One effect, one implementation.** A psychotronic device that produces a PSI effect calls the *same* effect as
  natural PSI. It never has its own version of telepathy.
- **No double charging.** The operator pays once, on their PSI resource.
- **No battery-plus-Effort economy.** Explicitly rejected as an anti-goal.
- **Device ≠ source of PSI.** A device amplifies; the human is the source. A device with no human produces
  nothing, ever.
- **Never merge QIP and non-QIP under one category** in any rulebook text or table.
- **Uploading/resleeving** is the QIP-adjacent experimental technology: rare, permit-controlled, outside this
  subsystem's first implementation.

## 7. Python model and interface (design only)

```python
# proposed, NOT implemented
@dataclass(frozen=True)
class PsychotronicDevice:
    kind: Literal["qip", "non_qip"]
    role: Literal["enable", "boost"]      # exactly one
    calibration: str                       # "calibrated" | "drifted"
    signature: str                         # how it is detected

def use(operator: PsiUser, device: PsychotronicDevice, effect: str) -> EffectResult: ...
```

Constraint: `kind == "non_qip"` may **never** return a PSI effect. That is an assertion worth writing as a test in
Phase C, because it is the rule most likely to be quietly broken later.

## 8. Campaign-stage relevance

| Stage | Devices |
|---|---|
| Baseline rookie | Issued BCI + defensive implant. Passive only |
| Awakening | The implant becomes a focus; unregistered or experimental devices appear as case material |
| Revelation | QIP devices as instruments of larger factions; uploading/resleeving enters as plot, not as a player option |

## 9. Open decisions for Tomi

1. Does the rookie's BCI do anything mechanically, or is it narrative hardware?
2. Implant failure: a disadvantage, a scene complication, or simply unavailable until repaired?
3. How visible is a QIP signature — police-grade detection, or only specialist equipment?
4. Should unregistered-device possession be a crime the PC can commit, with consequences?
5. Does the Sörnäinen suppression technology get mechanical detail, or stay background horror?

## 10. Bibliography

- Author: `design/BIONICS.md`.
- CWN Free Edition SRD: cyberware, equipment, System Strain (CC0, immutable).
- Tang et al., *Nature Neuroscience* (2023), s41593-023-01304-9 — tier (b), paywalled.
- *Nature Communications* (2025), s41467-025-63020-1 (tFUS) — tier (b), issue-provided.
- FDA CASGEVY pages — verified for the bionics draft, listed here only for the neurotech context.
- MKULTRA historiography — to be cited from declassified primary material in Phase B if this category is kept.
- Internal: `docs/rules/CWN_IMMUTABLE_CORE_1068.md`, `src/rules/swn_psionics.py`.
