# The attribute reskin: decision (#716)

**Status: decision recorded. Nothing is migrated; no save format, schema or canonical code changes.**

## Decision

**A is retained. `STR / DEX / CON / INT / WIS / CHA` stay canonical.**

**B is available and not authorised.** If the fantasy-coded vocabulary becomes the thing that
hurts most, B is the cheap fix: display labels (`Body Power / Coordination / Resilience /
Reason / Awareness / Presence`) over **retained** keys. It is reversible by deleting a table.

**C is not adopted.** A new attribute set is a mechanical replacement, not a reskin, and the
repository-specific cost is concrete: `data/rules/without_number.json` carries
`attributes.names`, `saves.attributes` and `modifier_upper_bounds`; `wn_core.py`, `cwn_core.py`
and every case/NPC stat line key off the six codes; `tests/test_scenario_data.gd` asserts that
every scenario check names a known attribute. A rename is therefore **a data migration with a
validation surface**.

## The two sub-questions #716 raises

**Is CYB an attribute?** No. As an attribute it penalises unaugmented characters by
definition. It is better modelled as equipment/interface or as a skill domain — and the
existing cyberware rules already treat augmentation as gear plus Strain.

**Is PSY one thing or two?** Two. Ordinary judgement belongs with `WIS`; trained psionics is
the SWN-shaped Effort/discipline model (#572), gated by a package. Merging them would let a
competent investigator also be a psychic by sheet layout alone.

## Reversibility

This decision is **provisional and reversible in one sentence**, like the other records here.
If B is later chosen, it is a presentation pass and this document needs one line changed; if C
is ever chosen, it returns as its own design with a migration plan that preserves characters
rather than rescaling them.

## What would reopen it

- a playtest where players consistently misread the sheet (that is B's trigger)
- a mechanical need for resilience separable from strength (that is the 7-stat trigger)
- anything in #712's checklist failing for A — none does
