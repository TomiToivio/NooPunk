# #689 Final planning disposition: narrative and ontological shock (20XX)

**Disposition:** Planning complete, **implementation intentionally deferred**. This is a recommendation with explicit author decision gates, not an adopted mechanic or a change to the [Without Number baseline](../../rulebook/WITHOUT_NUMBER_BASELINE.md). Source comparison and candidate register: [#689](https://github.com/TomiToivio/NooPunk/issues/689); initial compatibility audit: [ISSUE_689_FIRST_COMPATIBILITY_AUDIT.md](ISSUE_689_FIRST_COMPATIBILITY_AUDIT.md); re-anchoring: [ISSUE_689_STAGE0_REANCHOR.md](ISSUE_689_STAGE0_REANCHOR.md); [2d6 calibration](NARRATIVE_LAYER_2D6_CALIBRATION.md).

## Priority and recommendation

| Source | KEEP (existing) | PROPOSE (not canon) | REJECT/DEFER |
|---|---|---|---|
| CWN/SWN/WWN/AWN | CWN attributes, 19 ordinary skills, 2d6 checks; d20 attack/saves; existing harm, strain, PSI and hacking; optional specialist modules | No additional default kernel | Classes/stunts/second skill tree, second harm system |
| Apocalypse World | Fiction-first authority, meaningful risk, investigation prompt questions, GM agenda | Named case procedures with explicitly bounded trigger/outcome | Universal 6-/7–9/10+ table overriding CWN difficulty |
| The Sprawl | Existing case/alert state, mission and faction procedures | Legwork / action / recovery scene framing, *reuse* alert and front clocks | Duplicate corporate, action or harm trackers |
| The Veil | Affect/relationship descriptions; content controls | Emotion tags as **permissions/compel prompts**, no stat substitution | Emotions replacing the WN attributes or adding unpriced modifiers |
| Fate Core | Existing **optional** narrative layer #229, cancellable aspect tags | One optional player-accepted dilemma; setup actions and sheet rewrite scenes | 4dF, Fate skill pyramid, mandatory Fate points |
| Transhumanity's Fate | Existing ego/physical-device boundary in setting | Conditions and identity recovery as scene-oriented consequences | Import of NC text, independent morph/stress engine |
| Eclipse Phase 2E | Causal models for neural intrusion, identity/continuity, trauma | Case-specific nonnumeric condition taxonomy | Percentile core, Lucidity/Insanity meter, universal clinical diagnoses |

**Recommended default experiment:** Option A, **event → acute response → cancellable condition → player-authored interpretation**. Observable evidence is separate from interpretation; being distressed is neither a sign that a witness is wrong nor evidence for PSI. The character's own beliefs cannot be rewritten by a failed die roll. The option uses existing CWN checks, saves, HP, injury and System Strain; nothing in this memo authorizes a second psychological HP track.

**Alternative B:** two descriptive axes, *coping* and *epistemic certainty*. Numeric axes remain prohibited unless the author overrides the no-new-meter rule. **Alternative C:** EP-grade stress/trauma simulation is deferred for the same reason, plus complexity and framing concerns.

## Explicit implementation decisions (all UNANSWERED)

1. **Layer:** retain/re-anchor existing `rulebook/19_NARRATIVE_LAYER.md`, or retire it? Recommendation: retain as optional and migrate **only if approved**. It currently contains obsolete 1d10/4dF calibration.
2. **Outcome bands:** entirely opt-in to investigative/social/PSI scenes, or no bands? Recommendation: do not impose new bands on WN combat and saves.
3. **Psychological shape:** A (non-numeric conditions), B (two axes), or C (EP track)? Recommendation: A.
4. **Aspect economy:** no currency / existing provisional 0–3 pool / another narrowly specified arrangement? Recommendation: **no separate currency initially**; player agency outranks gamified compels.
5. **Emotion states:** fiction/permission only, limited roll modifier, or omit? Recommendation: fiction/permission.
6. **Paradigm ledger owner/scale:** use a single taxonomy across RPG and strategy without a new genre-specific resolution engine. Author has not approved 0–5/0–3 dials.
7. **Moves:** small closed GM prompt vocabulary versus generic free-form CWN adjudication? Recommendation: optional scene prompts, no duplicate character action set.
8. **Integration:** optional character-sheet reflection versus restoration/reset; avoid involuntary ideology revision.
9. **Concession:** available only when a credible fictional exit and known cost exist.
10. **Digital parity:** no LLM required for rules; deterministic event log, explicit choices; AI may narrate but not invent numeric modifiers.

Record approvals in the existing [author decision queue](AUTHOR_DECISION_QUEUE.md) or an implementation issue. **This planning issue is complete when the options and gates are documented, not when unanswered decisions are silently treated as yes.**

## Concrete tabletop/CRPG test protocol (NOT YET EXECUTED)

Use existing `data/scenarios/lakkahaltia/chassis_drill.json`, `src/rules/first_case_drill.py` and `tests/test_first_case_drill.py` as a **future fixture**, not evidence that this new layer was tested.

| Test | Input/control | Observable outcome | Reject when |
|---|---|---|---|
| Psychiatric-hospital interview | Two investigators, same CWN skills, distinct declared beliefs; no narrative tags vs Option A | Clue access; player decision differences; scene time and bookkeeping | A failed roll hides indispensable clue, a diagnosis means dishonesty, or beliefs are forced |
| BCI timestamp anomaly | Identical event/evidence, competing mundane/tech/PSI/IDH hypotheses | Event, interpretation and acute response persist distinctly | GM/LLM declares one hypothesis true without evidence |
| Front escalation | Predeclared clock triggers during investigation and security response | One observable case clock ticks only on its triggers | Duplicate clocks or opaque escalation |
| NHI/PSI/contact | Existing SWN discipline and prerequisites versus untrained investigator | Specialist capability permission remains binding | Narrative tags grant forbidden PSI or bypass Effort |
| Crisis zone | Existing AWN hazards and CWN HP/System Strain | Same WN sheet and physical danger | Second stress/harm pool, overridden lethality |
| Consent/content controls | Opt-out during psychiatric coercion or memory-tampering scene | Scene can skip/reframe without rules penalty | Opt-out punished by lost clues, XP or forced condition |
| Digital parity | Serialize explicit inputs, dice seed, event log and selected branch | Reproduce same rule result in tabletop fixture and CRPG | LLM-selected modifier or hidden state |

**Measurement sheet:** rolls/scene, seconds/scene, number of new counters, GM interventions, required-clue discovery, material player choices, number of forced interpretations, CWN success rates, save/load parity. Run baseline A-off and proposed A-on with comparable scenes, before implementation sign-off. **No playtest claims are made here.**

## Worked non-mechanical scene

In *Etsivä Romppainen ja Lakkahaltian Salaisuus*, Dr. Inspector Romppainen interviews a patient and a night porter at a Helsinki hospital. Both recall an impossible visitor, but their timelines disagree. The investigator's **Notice** or **Talk** uses existing CWN resolution. A security incident is recorded as *observable evidence*; the claim “an interdimensional entity did it” is only one *interpretation*. A shocked partner may gain a descriptive, cancellable condition such as “Distrusts hospital records,” without an automatic penalty or being labelled mentally ill. The hospital's response advances only if the stated trigger occurs. Evidence and competing hypotheses remain open; the player decides what the character believes. Agency, clues, escalation and physical danger all remain inspectable without a generative AI GM.

## Source and licensing boundary

References: [Fate Core SRD](https://fate-srd.com/fate-core), [Fate licensing](https://fate-srd.com/official-licensing-fate), [Apocalypse World creator resources](https://lumpley.games/apocalypseworld/), [CWN SRD](https://www.drivethrurpg.com/en/product/452790/cities-without-number-system-reference-document), [Eclipse Phase downloads](https://eclipsephase.com/dl/), [Transhumanity's Fate](https://legacy.eclipsephase.com/releases/transhumanitys-fate). See [#615](https://github.com/TomiToivio/NooPunk/issues/615) for extended free/SRD references. Free access to a rulebook is **not** blanket permission to copy. Eclipse Phase and Transhumanity's Fate have NC/SA reuse restrictions; do not transplant their protected expression into potentially commercial NoöPunk content.

## Completion statement

- **Completed:** consolidation of #686/#687/#688 into #689; conflict audit; exact 2d6 recalibration and tests from earlier merged PRs; comparative matrix; design recommendation; licensing cautions; falsifiable future playtest design; explicit unresolved author decisions.
- **Not done or claimed:** tabletop sessions, Godot integration, final author sign-off on mechanics, actual mind-system implementation, replacement of old narrative code. These are separately gated future work.
- **Closing #689** closes the **proposal-only research deliverable**, not the future feature roadmap.
