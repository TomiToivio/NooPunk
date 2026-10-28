# Issue #689: CWN narrative graft, ontology and psychiatric drama — first design audit

**Status:** research and proposal, **not a rules change**. 2026-10-28. Parent: [#689](https://github.com/TomiToivio/NooPunk/issues/689). Read this alongside [the authoritative baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md) and [existing optional narrative layer](../../rulebook/19_NARRATIVE_LAYER.md).

## Confirmed repository facts and immediate incompatibilities

1. The 2026-10-26 author decision uses CWN's **STR/DEX/CON/INT/WIS/CHA**, 19 ordinary skills and `2d6 + attribute modifier + skill rank` versus difficulty **6, 8, 10, 12, 14+**. Attack and saves use **d20**. PSI, hacking, physical trauma and resource economies remain governed by their WN family chapters.
2. `rulebook/19_NARRATIVE_LAYER.md` is an existing **optional** five-field aspect/GM procedure. **Do not create a new competing aspect layer**. Its resolution paragraph still assumes `STAT + Skill + 1d10` and its one-step / +2 caution was calibrated using **4dF**, so it cannot simply be applied to the new baseline.
3. `src/rules/narrative_layer.py` explicitly says `IS_CANONICAL = False` and `core.py` does not import it. Its `BAND_TO_MOVE` labels are `brutal/severe/solid/glancing`, not WN margins. Passing its current tests does not validate WN parity.
4. The baseline forbids **parallel harm/stress tracks, second advancement or economy, and universal identity/consciousness meters**. Any A/B/C mind model below is therefore research, not implicit permission to add numeric state.

## Quantitative 2d6 sanity check

For a **difficulty 8** CWN check (2d6 + modifiers >= 8), the 36 equally likely die pairs give:

| Sum modifier | Number of successes | Success probability | Increase from unmodified |
|---|---:|---:|---:|
| 0 | 15/36 | 41.67% | baseline |
| +1 | 21/36 | 58.33% | +16.67 percentage points |
| +2 | 26/36 | 72.22% | +30.56 percentage points |
| −1 | 10/36 | 27.78% | −13.89 percentage points |
| −2 | 6/36 | 16.67% | −25.00 percentage points |

These figures **depend on difficulty and existing bonuses**. On WN, a +1 aspect is not the same as one Fate ladder result, and +2 can be a very large boost. Proposed invariant: *never add a new, stackable aspect modifier outside the existing WN circumstance ceiling*. Even an optional +1 must specify whether it **replaces or consumes** an existing situational modifier and must be playtested. Prefer **permission and consequence tags** first, with *no numeric invoke*.

## A/B/C mind models, compared against canon

| Option | Mechanics shape | Benefits | Risks / status |
|---|---|---|---|
| **A. Condition/tag model (lowest impact)** | Record the **observable event**, a temporary **reaction**, a cancellable **condition**, and the character's **interpretation** as separate descriptive fields. Existing WN mental save/skill checks apply where fictional danger warrants a roll. | No parallel mental HP; tabletop easy; preserves epistemic ambiguity; reuses the optional aspect schema. | Conditions need scope/duration/cancellation and a firm rule against arbitrary penalties. **Recommended for first paper playtest, not adopted.** |
| **B. Two orthogonal axes (CWN override required if numeric)** | Distinguish **coping load** from **worldview certainty**. Prefer descriptive categories to counters; beliefs remain player-controlled, not dictated by saves. | Directly supports 'calm but convinced of impossible reality' vs 'frightened yet correct'. | Numeric Stability/Insight would violate the no-extra-meter principle unless author changes baseline. **Research alternative.** |
| **C. EP-grade mental stress track** | Stress accumulation → trauma → enduring condition with explicit recovery and identity/ego effects. | Strong simulationist causal detail for severe neural manipulation, body-copy events. | Conflicts with WN prohibition on parallel tracks, adds bookkeeping and may stigmatize psychiatric conditions. **Defer unless specifically authorized.** |

### Recommended first pass: Option A test, not canon

Case: **Romppainen interviews witnesses at a Helsinki psychiatric hospital**. An impossible BCI timestamp is logged as **evidence**; three incompatible accounts are tracked as **interpretations/hypotheses**, not resolved by a hidden sanity roll. An acute startle is a **reaction**, while a lasting loss of trust in the hospital director is a **relationship condition**; the player's beliefs change only by choice. A preexisting **case escalation clock** advances on concrete events (e.g., hospital security learns of the investigation), not simply because the GM needs drama.

**Agency / safety:** Psychiatric confinement, diagnosis, memory tampering and body horror require content controls and noncoercive opt-outs. A patient having a psychiatric diagnosis is neither evidence against their testimony nor proof of paranormal contact. Clearly distinguish a character's belief from objective evidence and fictional truth.

## Narrow narrative procedures worth piloting

- **Question-driven investigation** (*Apocalypse World*, *The Veil*): a Notice/Know/Talk check changes *risk and richness* of leads; essential clue access is not locked behind one failed roll.
- **Threat/case clocks** (*The Sprawl*, AW): front owner, segments, trigger, consequence, cancellation; reuse existing hacking and investigation alert/progress state instead of adding redundant clocks.
- **Aspect permissions and player-accepted dilemmas** (*Fate Core*, *Transhumanity's Fate*): existing aspect structure, no blanket modifier or extra Fate-point currency until economy decisions are reviewed.
- **Ego/morph/BCI identity differences** (EP2, TF): represent physical device access, mental continuity claims and evidence as *distinct fictional things*. Natural PSI, psychotronics and BCI have distinct access and costs using published specialist rules.
- **Session debrief** (AW): three non-mechanical questions: What did we learn? Whose trust changed? What is no longer certain? No alternative XP award.

## Decision gate and falsification criteria

**Before code:** Decide (1) whether any numeric outcome band is allowed on WN, (2) whether aspect invocations have *any* numerical effect, (3) whether there is an independent narrative currency, (4) whether condition tags alone are sufficient for the psychiatric campaign, (5) if/when numeric mind axes are permitted, and (6) whether any conditions must be represented in a structured CRPG state.

**First playtest** (tabletop without AI, then reproduce in a deterministic computer fixture):
- Two investigators with the **same WN sheet** but different prior beliefs confront the same evidence. They should have meaningfully different *choices*, without different secret skill numbers.
- Run the psychiatric interview, investigation, anomalous BCI trace, and NHI encounter twice (Option A on/off). Log decision quality, time per scene, GM burden, number of extra counters, and required clue discovery.
- Reject a graft if it changes dice probabilities without review, forces character beliefs, causes a duplicate resource/clock/harm system, conceals a mechanical outcome in AI prose, or cannot run at a table without LLM support.

## Sources, reuse and crosslinks

Uploaded source books considered by #689: *Apocalypse World 2e*, *The Sprawl*, *The Veil*, *Fate Core*, *Transhumanity's Fate*, *Eclipse Phase 2e*, plus *Cities/Stars/Worlds/Ashes Without Number*. Treat non-SRD books as **reading references, not source text to copy**.

- [CWN community SRD](https://cwn.quadrifons.com/) and [official SRD listing](https://www.drivethrurpg.com/en/product/452790/cities-without-number-system-reference-document)
- [Fate Core SRD](https://fate-srd.com/fate-core) and [official licensing guide](https://fate-srd.com/official-licensing-fate)
- [Apocalypse World creator downloads](https://lumpley.games/apocalypseworld/), [PbtA design essays](https://lumpley.games/articles/)
- [Eclipse Phase official downloads](https://eclipsephase.com/dl/), [Transhumanity's Fate publisher page](https://legacy.eclipsephase.com/releases/transhumanitys-fate)
- [Issue #615](https://github.com/TomiToivio/NooPunk/issues/615) source/licensing matrix; [#564](https://github.com/TomiToivio/NooPunk/issues/564) conversion; [#229](https://github.com/TomiToivio/NooPunk/issues/229) narrative; [#689](https://github.com/TomiToivio/NooPunk/issues/689) consolidated register.

**Next deliverable:** after author review, calibrate the approved option in the existing WN code path, with actual unit tests. **No rules or executable code have been changed in this research PR.**
