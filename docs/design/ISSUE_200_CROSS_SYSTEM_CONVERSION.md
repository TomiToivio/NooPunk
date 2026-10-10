# Issue #200: Cross-system rating conversion lab

**Experimental, noncanonical, independently authored.** This is a comparison tool, **not** a new NoöPunk core resolver and **not** a claim that the original games' scores are mathematically equivalent. No third-party tables or protected prose were reproduced.

Code: [`src/rules/issue200_cross_system_converter.py`](../../src/rules/issue200_cross_system_converter.py). Tests: [`tests/test_issue200_cross_system_converter.py`](../../tests/test_issue200_cross_system_converter.py). It complements the earlier exact-dice experiment [`ISSUE_200_RESOLUTION_EXPERIMENT.md`](ISSUE_200_RESOLUTION_EXPERIMENT.md) and the older EP2 **subsystem provenance/status** matrix. Those solve different problems.

## Five families and three dimensions

| Family | Attribute interpretation | Skill interpretation | Difficulty interpretation |
| --- | --- | --- | --- |
| **NoöPunk legacy** | 1–10, six separate FIT/REF/INT/SOC/CYB/PSY | 1–10, canonical skill list unchanged | The seven **current** DV anchors 9/13/15/17/21/24/29, easiest to hardest |
| **Fudge-inspired** | Experimental -3..+3 adjective-ladder index | Experimental -3..+3 adjective-ladder index | Experimental -3..+3 target ladder; actual game may use another ladder |
| **Fate-inspired** | Experimental -2..+8; **Fate Core does not have default separate character Attributes** | Experimental -2..+8 | Experimental -2..+8; Fate mechanics are not imported |
| **Eclipse Phase-inspired** | Experimental aptitude anchors 5,10,...,40, **not character-attribute equivalence** | Experimental percentile test-rating anchors 0,5,...,100 | Experimental **target success percentage** 90,75,60,45,30,20,10: high is *easier*, low is *harder* |
| **Cities/Stars Without Number-inspired** | **Attribute modifier** -2..+2, **not raw 3d6 ability score** | Experimental training ladder -1..4 | Experimental target numbers 6,8,10,12,14,16,18 |

Every external scale here is a **selected illustrative prototype range**, not authoritative reproduction of an individual edition or a promise of cross-game balance. Fudge/Fate's actual modifiers, EP percentile checks and *Without Number* 2d6 skill checks have substantially different probability models, as do Attribute+Skill summations. The converter deliberately does **not** interchange raw underlying mechanics, condition modifiers, opposing checks, health, initiative, PSI power magnitude or cyber hardware statistics.

## Conversion algorithm

1. Pick dimension **attribute**, **skill**, or **difficulty**. Never convert a composite character check as if it were one rating.
2. Validate the source value against **explicit representative anchors**, not arbitrary clamping.
3. Place that source value at an exact rational **ordinal quantile** along its family's ordered scale.
4. Map to the nearest target anchor. Ties round toward the **lower relative rank**. The endpoints stay endpoints.
5. Return `target_value`, `source_quantile`, `lossy: true` and an explicit `EXPERIMENTAL_ORDINAL_NOT_RULE_EQUIVALENCE` status. Identity conversions are exact and not lossy.
6. An EP **difficulty percentage** is ordered inversely to a difficulty value: 90% easy and 10% hard. This semantic inversion is tested.

For example, current NoöPunk DV **9 (Simple)** maps to experimental EP difficulty **90**; DV **29 (Legendary)** maps to **10**. These are **labels on an ordinal comparison scale**, **not** calculated probabilities of a NoöPunk character succeeding in Eclipse Phase.

### Why not directly compute equivalent success probabilities?

A character's success rate depends on **both ability and difficulty** and the game's full roll mechanic. For the old NoöPunk engine, `STAT + Skill + 1d10 >= DV`. Fudge-style 4dF, Fate outcomes, EP roll-under percentile and Without Number 2d6 cannot be calibrated by a single rating crosswalk. A future phase can define **probability-preserving target-specific conversions**, requiring verified public or CC-compatible mechanics specifications, separately audited source attribution and explicit decisions about crits, degrees of success and modifiers.

This lab is therefore intended for **NPC porting drafts, balancing conversations and comparing relative training tiers**. Do not feed its output into live tabletop/Godot/Concordia actions as canonical ratings without an approved migration.

## Sample use

```python
from src.rules.issue200_cross_system_converter import convert, compare_all

fudge_skill = convert(7, "noopunk", "fudge", "skill")
comparison = compare_all(17, "difficulty")
print(fudge_skill.target_value, fudge_skill.lossy)
print({name: result.target_value for name, result in comparison.items()})
```

NoöPunk's six Attributes remain distinct, and the Skill list (including specializations) is not altered. A skill **name** mapping requires semantic matching by field and action, *not* mechanical equivalence: e.g., a source-game “Hacking” skill may cover only some NoöPunk `Infosec`, `Interface` or `Hardware` actions. Species, morphs, psi techniques, armor and damage require their **own qualitative mapping** before numerical translation.

## Licensing and implementation safety

The converter is **original NoöPunk mathematical code** using generic public gaming concepts, rather than importing Fudge/Psi-Punk OGL protected text or Eclipse Phase/Transhumanity's Fate NC-licensed expression. Its ranges are independently specified experimental anchors, **not official conversion tables**. See [CC release gate](../licenses/ISSUE_200_CC_RELEASE_GATE.md) and [rights ledger](../sources/GAME_SYSTEM_RIGHTS.md). Final CC license and any resulting code license remain for project governance.

## Next work in #200

- [ ] Verify precise game-edition anchors with permitted public/CC SRD references; record per-system license, edition and evidence. Where a source is NC/OGL-only, use independent description rather than copied protected expression.
- [ ] Decide NoöPunk's new Fudge/Fate hybrid trait scale, dice kernel and target success distribution.
- [ ] Introduce **probability-equivalent** conversions that accept *attribute + skill + difficulty + modifiers + dice model* together, with explicitly documented unavoidable approximation error.
- [ ] Add semantic Skill-to-Skill maps after review of the NoöPunk vocabulary, specialization and each source's concept coverage.
- [ ] Extend conversions to health/injuries, equipment, cyber Interface/Network/Compute and PSI effect tiers only after those native mechanics become playable canon.
- [ ] Add tabletop examples and digital parity fixtures after author approves the canonical migration.

To test: `python -m unittest discover -s tests -p 'test_issue200_cross_system_converter.py'`.
