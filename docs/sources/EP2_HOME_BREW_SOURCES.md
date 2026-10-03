# Eclipse Phase 2E homebrew sources

This file records sources used for the issue #60 Concordia prototype.

## Primary rules references

- EP2 online rules: https://eclipsephase.github.io/en/01/00-infamy.html
- How to Play / d100 tests / 33-66 rule / criticals / defaulting:
  https://eclipsephase.github.io/en/03/01-how-to-play.html
- EP2 Quick-Start Rules:
  https://eclipsephase.com/wp-content/uploads/2024/02/PS10001_EclipsePhaseSecondEdition_QuickStartRulesAcrimony_Nov2023.pdf
- EP2 Rules Primer:
  https://www.eclipsephase.com/wp-content/uploads/2021/12/EclipsePhaseSecondEdition_RulesPrimer.pdf
- Eclipse Phase Creative Commons information: https://eclipsephase.com/cclicense/

## Character and data references

- Eclipse Helper character generator: https://arokha.com/eclipsehelper/chargen/1
- Artemystra Eclipse Phase data: https://github.com/Artemystra/eclipsephase
- Eclipse Phase 2 tools: https://github.com/ralfbiedert/eclipse-phase-2-tools

These external projects are references only until their individual licenses and
provenance have been checked. No external code or large data set is imported by
the initial issue #60 implementation.

**That check has now been carried out**: see
[`EXTERNAL_SOURCE_LICENSES.md`](EXTERNAL_SOURCE_LICENSES.md) (machine-readable record in
[`data/sources/external_sources.json`](../../data/sources/external_sources.json)). Headline
results: the EP2 online rules and Quick-Start are importable as EP-derived material;
`ralfbiedert/eclipse-phase-2-tools` and the Eclipse Helper generator are **not** (no license
found and split terms respectively); the PbtA conversion could not be verified and is
neither importable nor cleared; the four attached conversions named by the issue are not
present on disk.

## Initial implemented rules provenance

The first kernel is a compact reimplementation of public EP2 rules concepts rather
than copied rulebook prose: percentile roll-under tests; 33/66 superior results;
critical doubles with 00/99 absolutes; defaulting suppressing critical successes;
+/-60 modifier cap; Insight/Moxie/Vigor/Flex pool categories; and common pool test
manipulations (+20, ignore modifiers, flip-flop, upgrade success, downgrade critical failure).
