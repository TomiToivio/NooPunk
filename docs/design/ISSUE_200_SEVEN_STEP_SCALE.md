# Issue #200: Seven-step Fudge-style scale migration

**Author-requested conversion of the existing NoöPunk 1–10 Attribute and Skill ratings to −3 through +3, and migration of the seven current difficulty values to the same seven-step scale.** This document and `data/rules/fudge_scale_migration.json` are the new **scale crosswalk**, not an assertion that all digital runtimes and the check formula have migrated. The existing 1d10 implementation is explicitly a legacy compatibility path pending the separately approved, tested Fudge/Fate resolution cutover.

## Attributes and Skills

**Preserve separate attributes and skills.** FIT / REF / INT / SOC / CYB / PSY remain the six attributes. The canonical skill names, specialist fields and bindings remain intact. Rating conversion is identical for an Attribute or a trained Skill:

| Legacy | Seven-step |
| ---: | ---: |
| 1 | −3 |
| 2 | −2 |
| 3 | −2 |
| 4 | −1 |
| 5 | 0 |
| 6 | 0 |
| 7 | +1 |
| 8 | +1 |
| 9 | +2 |
| 10 | +3 |

This **draft monotone quantization** preserves extremes and represents midrange levels with zero. It necessarily collapses several old values, so **retain original numbers in stored characters until character-sheet/storage migration is finalized**. This is an independently authored NoöPunk mapping, not copied source text from Fudge. No decision to remove the difference between **untrained** versus trained Skills is implied: the existing untrained −1 rule must be reviewed explicitly, because −1 is now also a valid *trained* rating.

## Difficulties

| Current name | Legacy DV | New difficulty level |
| --- | ---: | ---: |
| Simple | 9 | −3 |
| Everyday | 13 | −2 |
| Difficult | 15 | −1 |
| Professional | 17 | 0 |
| Heroic | 21 | +1 |
| Incredible | 24 | +2 |
| Legendary | 29 | +3 |

The canonical difficulty **names** are preserved. These mappings preserve *rank*, not success probability. In particular, **do not evaluate `Attribute + Skill + 4dF >= difficulty` by silently assuming this table guarantees unchanged success odds**. Fudge/Fate resolution, Attribute-vs-Skill weighting, situational bonuses, trained-only rules, missing Skills, opposed tests, GM consequence bands and probability calibration are separate decisions. See `src/rules/kernel_prototype.py`, `docs/design/ISSUE_200_RESOLUTION_EXPERIMENT.md` and `docs/design/ISSUE_200_CROSS_SYSTEM_CONVERSION.md`.

## Runtime conversion procedure

1. Read versioned `data/rules/fudge_scale_migration.json` rather than inventing a second mapping.
2. Convert each of the six Attributes and each named Skill **separately** with `src/rules/issue200_scale_migration.py`.
3. Translate only one of the **seven named** legacy difficulty DVs; reject arbitrary values pending an explicit interpolation policy.
4. Retain source ratings and conversion version to avoid claiming a reversible map.
5. Develop a probability-calibrated Fudge/Fate kernel and adjust character creation, Academy default Skill 3, trained/untrained behavior, skill field-transfer modifiers, equipment bonuses and legacy JSON fixtures **together**.
6. Only after migration tests and author approval, change `data/rules/core.json`, `RULEBOOK.md` §4, `src/rules/core.py`, Godot and Concordia simultaneously. Existing tests pin active `1d10` for good reason. Do not allow a half-migrated runtime.

**Licensing:** The translation data and implementation are original NoöPunk work designed for the planned Creative Commons release; the table contains no copied Fudge/Psi-Punk OGL wording and no Eclipse Phase NC expression. Target CC license selection, provenance and actual publication remain separately gated.

**Validation:** `python -m unittest discover -s tests -p 'test_issue200_scale_migration.py'`; repository-wide GitHub CI must pass.
