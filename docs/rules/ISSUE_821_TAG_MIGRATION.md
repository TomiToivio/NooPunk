# #821 tag migration — impacted files, crosswalk and open questions

Companion to `RULEBOOK.md` §3.3 and `godot/core/cwn_tags.gd`. This note records **what the change
touches**, so the next agent does not have to rediscover it, and states plainly which decisions are
the author's rather than the implementer's.

## What changes

| Area | Before | After |
| --- | --- | --- |
| Attributes | six (STR/DEX/CON/INT/WIS/CHA), score 3–18, modifier derived | **seven tags**, value −2..+2 stored and displayed directly |
| Character sheet | raw score plus modifier | **modifier only**; the raw 3d6 roll is not retained |
| Skills | Punch, Stab, Shoot, Fix, Heal, Program, Exert, Know | Unarmed, Melee, Firearms, Hardware, Wetware, Software, Strength, Stamina, Research, Noöware, … |
| Untrained | implicit | explicit: −1 **or** impossible, by task |
| Talk | one attribute | contextual: Empathy, Agency, or another by approach |
| Statuses | prose conditions | typed tags with duration, stacking and exclusivity |

## Impacted files

**Tabletop**

- `RULEBOOK.md` §3.3 (new); §3.2 marked superseded for player characters
- `rulebook/parts/` and `data/rules/rulebook_split_manifest.json` — regenerated, never hand-edited
- `data/rules/noopunk_adaptations.json` — `tag_attributes_seven`, status `approved`

**Godot**

- `godot/core/cwn_tags.gd` — new: typed tag model, bands, display, parse, statuses, Empathy boundary
- `godot/core/cwn_character.gd` — `generate_noopunk_attributes`, `skill_tag`, `skill_attribute`,
  `untrained_outcome`, `crosswalk_legacy_attributes`
- `godot/tests/test_tags.gd` — the parity suite (bands, display, parse, skills, statuses, boundaries)

**Not yet touched, and this is deliberate**

- `godot/core/cwn_rules.gd`, `combat.gd`, `cwn_combat_rules.gd` still use the CWN six attributes and
  `Punch/Stab/Shoot`. Rewiring combat onto the new tags is the next step and needs the crosswalk
  decision below, otherwise every NPC stat block silently changes meaning.
- Saved characters. No migration is written until §"Open questions" 4 is answered: a stored
  `{"STR": 12}` cannot be turned into a Fitness tag without deciding what STR + CON collapse to.

## Crosswalk

```
WIS → Agency, Empathy, Awareness      STR, CON → Fitness
DEX → Reflexes                        INT      → Cognition, Cyber
CHA → Empathy, Awareness, Agency
```

`Character.crosswalk_legacy_attributes()` returns the proposals **and** the list of new attributes fed
by more than one old score (`Fitness` from STR+CON, `Agency` from WIS+CHA, `Empathy` from WIS+CHA,
`Awareness` from WIS+CHA). It assigns no values; that is the author's ruling.

## Open questions (for Tomi)

1. **Untrained task classes.** Which actions are attempted at −1, and which are impossible without
   the skill? The kernel takes the answer as an argument and refuses to guess.
2. **Know.** What survives once Research is the generic information skill, and which domains remain?
3. **Work.** Which professional specialities exist?
4. **Legacy conversion.** How do several old scores collapse into one new tag (STR + CON → Fitness;
   WIS and CHA both feeding Agency/Empathy/Awareness)? Options include averaging, taking the higher,
   or a per-attribute table — this changes every existing character, so it is not an implementer's
   choice.
5. **Status catalogue.** The mechanism (duration, stacking replace/add, exclusivity) is implemented;
   no status list, severity scale or recovery rate is defined.
6. **Nonhuman and transhuman ranges.** Values above +2 are representable and never generated. What
   grants them, and what caps them?
7. **Connect.** The draft marks it as needing further design.

## Parity status

| Claim | Evidence |
| --- | --- |
| 3d6 bands are exact and never generate −3 | `test_tags.gd`, boundary checks at 3, 4, 7, 8, 13, 14, 17, 18 |
| Seven attributes, modifier-only | same suite |
| Display syntax, including Unicode (`Noöware-2`) | same suite; parse round-trips |
| Skill levels 0–4, untrained −1 vs prohibited | same suite |
| Talk contextual by approach | same suite, rapport→Empathy, authority→Agency, unset→open |
| Temporary statuses: replace, add, exclusive, expiry | same suite |
| Empathy −3 ineligible as PC; −2 eligible | same suite |
| Crosswalk reports ambiguity, assigns nothing | same suite |

Tabletop ↔ Godot difference: **none** in the numbers. The rulebook states the bands, the display and
the Empathy rule in prose; the game reads the same values from `cwn_tags.gd`.
