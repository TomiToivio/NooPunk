# Issue #200: noncanonical resolution experiment

**Status:** design experiment, **not playable canon**, not an official Fudge or Fate adaptation. No third-party rule text was copied, and no existing runtime is migrated.

## What is being compared

The current rules use **STAT + Skill + 1d10 vs Difficulty Value**. The author now requests an independent Fudge/Psi-Punk/Fate/Transhumanity's Fate-inspired rule system preserving **six separate character Attributes** (FIT/REF/INT/SOC/CYB/PSY) and the existing **Skill names and specializations**.

The lab in `src/rules/issue200_resolution_lab.py` compares two *mathematically explicit experimental* functions, given identical (1–10) stat, skill and difficulty inputs:

- **Legacy benchmark:** stat + skill + flat d10 + optional situational value versus target.
- **Fudge-style benchmark:** stat + skill + the sum of four equally likely -1/0/+1 outcomes + optional situational value versus target.

These are **not equally calibrated scales**. In particular, d10 averages 5.5 while 4dF averages zero. The lab deliberately does **not** pretend that equal raw target numbers mean equal difficulty; a separate difficulty-scale mapping must be designed and playtested. It also does not silently adopt Fudge's adjectives, Fudge Points, Fate Points, Aspects, Stunts, criticals, opposed resolutions, partial successes, action points or damage systems.

## Exact probability example (Stat 5, Skill 5)

| Target | Existing 1d10 benchmark | Experimental 4dF benchmark |
| --- | --- | --- |
| 10 | 100% | 50/81 ≈ 61.73% |
| 14 | 70% | 1/81 ≈ 1.23% |
| 16 | 50% | 0% |

The strong difference shows why **difficulty conversion cannot simply retain the existing DV numbers**. The models have different variances and centers. That is a *design research finding*, not a balance recommendation.

## Next decisions before canonical integration

1. Author chooses whether the core should use Fudge dice or an independently authored numerical equivalent, and whether the existing 1–10 ratings are preserved, compressed or mapped to ladder labels.
2. Test a calibrated difficulty crosswalk with opposed checks, trained/untrained states, cyber hardware Interface/Network/Compute and player-visible success odds.
3. Compare consequences and player agency using original narrative options inspired by the **CC BY Fate SRD**, plus independent PbtA/The Veil ideas. No NC Eclipse Phase or Transhumanity's Fate expression may be imported into a commercial-compatible CC ruleset.
4. Only then write a tabletop rule and controlled runtime migration. Keep Godot, Python and Concordia aligned; the LLM may narrate, not fudge numerical results.

Run the focused tests: `python -m unittest discover -s tests -p 'test_issue200_resolution_lab.py'`. These test the prototype in isolation; existing canonical test behavior is untouched.

References: [#200](https://github.com/TomiToivio/NooPunk/issues/200), [CC release gate](../licenses/ISSUE_200_CC_RELEASE_GATE.md), [canonical design principles](../archive/DESIGN_PRINCIPLES.md).
