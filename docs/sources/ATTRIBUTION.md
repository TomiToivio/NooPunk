# Attribution and notices

**Status: generated. Do not edit by hand.**

Parent epic [#200](https://github.com/TomiToivio/NooPunk/issues/200); work package
[#231](https://github.com/TomiToivio/NooPunk/issues/231). Regenerate with
`python3 tools/issue231_attribution.py`; a guard fails if this file is out of date.

## Licence of this work

**Not yet chosen.** Issue #231 acceptance criterion 1. CC BY-SA 4.0 is recommended for the rulebook and original setting because it can adapt The Veil's CC BY-SA 3.0 text; CC BY 4.0 cannot. Source code is licensed separately.

| Component class | Candidate |
| --- | --- |
| Rulebook and original setting | CC BY-SA 4.0 (recommended) |
| Source code | pending-author-decision |

Until the choice lands, nothing in the repository may be redistributed as if licensed.

## Required attributions

These grants are conditional on attribution, so the notices below are obligations rather
than courtesies. They are derived from `data/sources/game_system_rights.json`.

| Work | Licence | Notice |
| --- | --- | --- |
| Fate Core System Reference Document (fate-srd.com) | CC BY 3.0 Unported | Fate Core System (c) Evil Hat Productions, LLC -- CC BY 3.0 Unported |
| The Veil / The Veil: Cascade (Samjoko Publishing) | CC BY-SA 3.0 (Unported) for the text | Contains material adapted from *The Veil*, by Fraser Simons (Samjoko Publishing), licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported licence. |

## Courtesies

Public-domain or licence-free material, credited because it deserves to be.

| Work | Licence | Notice |
| --- | --- | --- |
| Cities Without Number System Reference Document (Kevin Crawford / Sine Nomine) | CC0 (public-domain dedication) | None required (CC0). Courtesy credit proposed: game procedures informed by the Cities Without Number System Reference Document (Sine Nomine Publishing), released under CC0 1.0 Universal. Scope: the waiver covers the SRD, not the published book. |

## Shipped components

What this repository ships, and what each part owes.

| Component | Kind | Licence | Attribution | Third-party inputs |
| --- | --- | --- | --- | --- |
| `rulebook-text` | prose | pending-author-decision | yes | fate-core-srd, the-veil |
| `rulebook-parts` | prose-generated | inherits:rulebook-text | no | — |
| `rulebook-segments` | prose-generated | inherits:rulebook-text | no | — |
| `rules-code` | code | pending-author-decision | yes | — |
| `rules-data` | data | inherits:rulebook-text | no | — |
| `tests` | code | inherits:rules-code | no | — |
| `godot-scaffold` | code | pending-author-decision | no | — |
| `docs` | prose | inherits:rulebook-text | no | — |
| `scenes` | data | inherits:rulebook-text | no | — |

## Not shippable as inputs

Non-commercial, proprietary, no established CC grant, or unresolvable OGL terms. #231 criterion 3 requires any incompatible expression to be isolated or independently rewritten; until that audit is complete these are inspiration, not inputs.

`eclipse-phase-2e`, `transhumanitys-fate`, `fudge-ogl-srd`, `fudge-1995-pdf`, `psi-punk`, `stars-without-number-srd`, `apocalypse-world`, `cyberpunk-red-2020`, `cy-borg`, `shadowrun`, `other-proprietary-tabletop`, `computer-game-references`

## Open items

- Criterion 1: the CC BY-SA 4.0 vs CC BY 4.0 choice is the author's, as is the code licence.
- Criterion 3: artwork and trademark verification has not been performed; the repository currently ships no artwork.
- Criterion 3: no NC/OGL expression has been found in the shipped text, but the isolation audit is not complete for the two NC role-playing sources.
