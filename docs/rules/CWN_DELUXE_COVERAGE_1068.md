# CWN Deluxe coverage report (#1068)

> **Superseded:** [CWN_COVERAGE_1068.md](/docs/rules/CWN_COVERAGE_1068.md) is the one document kept up to date for this
> subject. This file is kept as history — it is a second answer to a question that already had one,
> and the counts in it disagree with the audited ones. Do not update it; update the canonical file.


Audit of the NoöPunk Python rules library against *Cities Without Number, Deluxe Edition*
(`CitiesWithoutNumber_Deluxe_Lightweight_081123.pdf`, 265 printed pages), performed against the book's
own page numbers, not against filenames. The machine-readable claims live in
`data/rules/cwn_rule_inventory.json`; `tools/cwn_rule_inventory_audit.py --check` resolves them and
`docs/rules/CWN_RULE_INVENTORY.md` is generated from them.

## Headline numbers

| status | rows | meaning |
| --- | --- | --- |
| implemented | **41** | Python module + at least one Python test, and the mechanic exists as the book states it |
| partial | **8** | a named piece of the rule is missing (listed below) |
| missing | **4** | no implementation (listed below) |
| not_applicable | **12** | GM advice, generator tables or setting material — nothing to implement |
| unverified | **0** | the inventory was rebuilt from the book this pass, so every row states what was actually checked; rows whose numbers I could not confirm were demoted to `partial` with the gap named rather than left vague |

65 rows cover all ten chapters, including the **Supplemental Material** chapter (pp. 226–259) that a
free-edition audit cannot see.

## Implemented in this pass (verified against the printed tables)

### Cyber Alienation — `src/rules/cwn_alienation.py`, pp. 226–231, 22 tests

| rule | implementation |
| --- | --- |
| Alienation gained per implant | `system_cost()` — System Strain rounded **up**, +2 for Nerveware, discounted eye/ear mods still cost 1 |
| Ceiling | `Alienation.maximum` = Wisdom + every syndrome's bonus |
| Chrome syndromes | all 12 from the printed table with their ceiling bonuses and effects |
| Syndrome cannot repeat | refused in `take_syndrome()` and in the constructor |
| Alienation check | `check(die)` — 1d20 at or under the score gains a point, at or over the ceiling asks for a Mental save |
| Cyber-induced psychosis | `mental_save(success=…)` → new syndrome or psychosis |
| Therapy | `therapy_week()` — one point for $2,000, never below what the chrome itself costs |
| Rescue from psychosis | `rescue_from_psychosis()` — chrome out, Alienation below Wisdom, Mental save with the therapist's best Heal/Talk |
| Optionality | the module imports nothing from the cyberware rules; a test asserts it stays that way |

### Magic in the city — `src/rules/cwn_magic.py`, pp. 231–236, 22 tests

| rule | implementation |
| --- | --- |
| Mage Effort | `mage_effort_max()` — better of Int/Wis + Cast, minimum 1 |
| Cyber allergy | `cyber_effort_penalty()` — each implant costs its strain **and at least one point**; the book's own example (2, 0, 0.5 → four points) is a test |
| Prepared slots | `prepared_slots()` — ceil(level/2) + Cast (the book's level-1 and level-10 examples are tests) |
| Commitments | `Commitment.DAY / SCENE / DURATION` with `refresh()`, `end_scene()`, `reclaim_duration()` |
| Casting conditions | one free hand, a voice, no damage/grapple that round — refused, not silently allowed |
| Interrupted cast | `struck_while_casting()` — spell lost, Effort wasted |
| Overcasting | the full six-band table, `1d20 + Cast + Con − 2` for day-commitment spells, strain per band, duration-cost spells lasting one scene |
| Summoner Effort | `summoner_effort_max()` — better of Con/Cha + Summon |
| Spirit accounting | `summoner_spirit_binding()` — Effort stays bound until the morning after dispelling |

Neither module changes a CWN core procedure: both are optional and self-contained, and both are
classified `cwn-core` in the rules constitution only because they *are* published CWN rules — a campaign
that ignores them behaves exactly as before, which is what the optionality tests check.

## Partial — what precisely is missing

| row | missing piece |
| --- | --- |
| contacts | the contact *network* rules (who knows whom, reaction over time) — granting works, the procedure has no test |
| megacorps | corporation-scale play is offered through the optional SWN faction engine, not a CWN rule |
| mission tags | tags exist as scenario data; no tag effects engine |
| pharmaceuticals | drug catalogue is data; addiction/recovery procedure is not modelled |
| magic in the city | the campaign frame is prose; the economy is implemented |
| summoners & spirits | Effort and binding accounting only — spirit *statistics and powers* are content not yet authored |
| corp guards / gangers / hackers & pilots | statlines live in the gear catalogue without dedicated statblock tests |
| magic-user foci | no module |
| — see also: | |

## Missing — the remaining implementation work

| row | printed page | what it needs |
| --- | --- | --- |
| Cyber Product Line Quirks | 227 | quirks are content, but the *rule* that a quirk changes a system's behaviour is unmodelled |
| Variant Humanity | 228 | variant human traits and their interaction with creation |
| Cheap Cyber | 232 | the cheap-cyber price/maintenance rule (tables are content; maintenance bookkeeping is not modelled) |
| Magic-User Foci | 247 | the mage-only foci |

The Graced (p248), magic items (p250) and summoner spirits (p240) were implemented in parallel and are now
counted as implemented — the inventory follows the tree, and the audit fails if it ever drifts.

These six are the honest remainder. Each needs the printed tables read and its own module + tests; none
of them may be guessed, and none of them touch the immutable core.

## What was *not* changed

- No CWN core mechanic was modified. `tools/rules_constitution_audit.py --check` still reports a clean
  baseline with no overlay import, and the four Deluxe additions are optional modules.
- No rulebook text was copied: every module states the arithmetic and paraphrases, citing printed pages.
- The existing `data/rules/cwn_compliance_matrix.json` (66 rows) stays as the SRD-level view; this
  inventory is the book-level one and is the one with an enforcing check.

## Maintenance

- After any rule change: update `data/rules/cwn_rule_inventory.json`, then
  `python3 tools/cwn_rule_inventory_audit.py --markdown > docs/rules/CWN_RULE_INVENTORY.md`, then
  `python3 tools/cwn_coverage_manifest.py` (the adapter-facing registry).
- `tests/test_cwn_rule_inventory.py` fails if the document drifts from the data, if a chapter disappears,
  or if any row claims `implemented` without a Python test.
