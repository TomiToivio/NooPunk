# CWN pharmaceuticals: tabletop ↔ Python (#1068)

**Published rule source:** https://cwn.quadrifons.com/gear-vehicles-cyberware/pharmaceuticals-street-drugs/

This file adds an executable cross-reference, **not** a new house-rule or replacement for the CWN drug catalogue. Python: `src/rules/cwn_pharmaceuticals.py`. Tests: `tests/test_cwn_pharmaceuticals_1068.py`.

## Tabletop procedure

Administering a chem consumes one Main Action. Compare the administrator's Heal rank with the drug's minimum listed in the published pharmaceutical table. A listing of **None** needs no training; numeric 0 requires Heal-0. The first Lurch dose of the day requires Heal-0, the second Heal-1, the third Heal-2, and so forth.

If a dose would push the recipient beyond maximum System Strain, its beneficial effect does not occur, but its adverse effects still apply. Where several drugs grant the same kind of bonus, use only the highest applicable bonus, not their sum.

For Panacea when included in First Aid, double the HP recovered with a minimum of 6 HP. For a Trauma Patch, use an Int/Heal or Dex/Heal check at difficulty 6, increasing by 1 for each full round after the patient went down; a patch cannot help at six rounds or later and cannot stabilize victims downed by poison/disease or dismembered by heavy weapons/explosives.

**Paper example:** A character who has already taken two Lurch doses today needs an administrator with Heal-2 for dose three. A patient at Strain 4 of 5 gets no benefit from a drug that would add 2 Strain, even if the administrator meets the required Heal rank.

Other drug-specific effects remain governed by the published source, not generic code in this module. This partial implementation does **not** resolve all of issue #1068 or certify tabletop parity.
