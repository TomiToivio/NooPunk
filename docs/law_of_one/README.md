# Law of One RPG — a separate game, not a NoöPunk chapter

This directory holds the **Fourth-Density Law of One RPG**: its own rulebook, its own rules namespace, its own
tests. It is deliberately *not* part of the NoöPunk game, and the separation is a hard rule from issue #1124,
not a preference:

> Keep the Law of One RPG rulebook completely separate from the NoöPunk RPG rulebook. Do not append Law of One
> content to the NoöPunk tabletop rulebook, move CWN rules into Law of One, patch NoöPunk's main character
> sheet, or merge the books/code now.

Merging, reskinning and any NoöPunk integration are a **later, explicitly authorised task**. Until then:

| rule | where it is enforced |
|---|---|
| No Law of One content in `RULEBOOK.md` or `rulebook/` | review; and this directory is the only home for it |
| No Law of One content in `src/rules/` (the CWN/SWN/WWN/AWN namespace) | `tools/law_of_one_inventory_audit.py` fails if `src/law_of_one` or `law_of_one/` exists **before** Phase 2 is authorised |
| No NoöPunk or CWN mechanics inside this game | this game defines no attributes, skills, hit points, combat or equipment |
| No shared save format | Phase 3 will define its own |

## Phase status

| phase | what it is | state |
|---|---|---|
| **1. Inventory** | a source-linked list of every Law of One-specific rule, its disposition, and the smallest procedure that would serve it | **done — awaiting review** |
| 2. Standalone rulebook | a playable, lightweight narrativist game | blocked on the review of Phase 1 |
| 3. Code and tests | the same rules in a small Python package | blocked on Phase 2 |
| 4. NoöPunk integration | a separate, authorised decision | not started; out of scope here |

## What is here now

| file | what it is |
|---|---|
| [`RULES_INVENTORY.md`](RULES_INVENTORY.md) | **the Phase 1 deliverable**: 45 concepts, each with its source citations, faithful meaning, disposition, minimal procedure, state fragment, interactions, non-goals and open questions. Generated — edit the data. |
| [`COVERAGE_MAP.md`](COVERAGE_MAP.md) | every required source concept mapped to the rows that carry it, plus the pages deliberately left out and why. Generated. |
| [`CATEGORY_AND_DEFINITION_COVERAGE.md`](CATEGORY_AND_DEFINITION_COVERAGE.md) | all 39 categories and all 20 definition subcategories, each with a disposition — closes the two source indexes the issue names. |
| [`EXAMPLES_AND_MILESTONES.md`](EXAMPLES_AND_MILESTONES.md) | proposed Awareness bands and the four hard adjudication cases (autonomy, boundaries, good-intention failure, coercion). |
| `../../data/law_of_one/rules_inventory.json` | the rows themselves |
| `../../data/law_of_one/source_coverage.json` | the coverage contract the audit enforces |
| `../../data/law_of_one/entity_catalogue.json` | a *seeded* catalogue of named beings and civilizations: source-attested only, with the uninventoried remainder listed as a gap |
| `../../tools/law_of_one_inventory_audit.py` | renders both documents and fails on coverage gaps, missing citations, an unmechanised concept with no stated treatment, or a Phase 2 implementation appearing early |

Nothing in this directory is canon for NoöPunk, and nothing in it is CWN, SWN, WWN or AWN.

## Paths proposed for the later phases

Chosen to be unique and non-overlapping with anything in the repository today:

```
docs/law_of_one/            this rulebook (separate artifact)          exists
src/law_of_one/             Python package                             Phase 3, currently absent by design
tests/test_law_of_one_*.py  its tests                                   Phase 3
data/law_of_one/            inventory, coverage, entity catalogue      exists
```

`src/law_of_one` rather than `src/rules/law_of_one` is deliberate: `src/rules` is the published Without
Number rules library, and this game must never be importable as if it were one of those systems.

## The design stance in one paragraph

The player is a newly awakened **fourth-density, positively polarised** being. Play is
Catalyst → free choice → consequence → Integration → evolution, with three slow 0–10 scores (Polarization,
Awareness, SMC Connection), plain-language Distortion tags, six usable energy centres and a derived violet
register, a physical/astral pair of realms, and a group sheet for the social memory complex. There is no XP, no
combat system, no equipment list and no character class: those belong to a host game, if this ever has one.
