# WWN spell effects, batch 1 — the table procedure (#1085)

`data/rules/wwn_spell_effects.json` holds structured effects for the thirteen High Magic level-1
spells; `src/rules/wwn_spell_effects.py` resolves them. This page is the same thing with dice in your
hands, because a rule that cannot be played with paper is not a rule yet.

Source: the **WWN SRD**, CC0 (`data/sources/game_system_rights.json`). The rows paraphrase mechanics;
they do not reproduce SRD prose. The remaining 39 High Magic, 15 Elementalist and 16 Necromancer
spells have no effect row yet and are named as such — the resolver refuses them rather than guessing.

Whole-system coverage (classes, factions, travel, Deluxe blocks) is tracked once in
[`WWN_COVERAGE_1101.md`](WWN_COVERAGE_1101.md); this page owns only the spell-effect batch.

## The casting sequence at a table

1. **Prepare and spend the slot.** The spell must be prepared and the casting still unspent for the
   day (`wwn_high_mage.WWNMage.cast()` enforces this; on paper, cross off the cast).
2. **Check the casting conditions.** A Main Action, a free hand, a voice — unless the row says
   otherwise. `speed` is a Free action; `statis` is a Free spell and only if nothing else was cast
   this round.
3. **Name the target and roll the save**, if the row has one. The row gives the category
   (`physical` / `mental`) and what a success means: `half`, `negates the hit, per hit`,
   `the spell ends`, `the binding lasts one round`.
4. **Roll damage**, if the row has a formula. `1d8 per caster level` at level 3 is 3d8, not 1d8+3.
5. **Apply the note.** A `manual: true` row means the interesting part is the table's call; the note
   says what the mechanical scaffolding is (the illusion's phantasmal attackers, the beast's
   commands, the memory questions).

## The thirteen, as a quick reference

| spell | kind | save | the number that matters |
| --- | --- | --- | --- |
| Arcane Spark | damage | Physical, half | 1d8 per caster level; 1-HD NPCs die regardless |
| Blunt Contact | buff/debuff | Physical per weapon hit (creature form only) | creature: ⌈level/2⌉ rounds; weapon: rest of the Turn, no save |
| Control Animal | control | — | senses cost a Main Action; the beast will not fight |
| Create Illusion | illusion | Mental each round once disbelieved | level × 10-ft cubes; attackers ⌈level/2⌉, 1d8, AC 10 |
| Destroy Earth | damage/destruction | Physical, half (plant monsters only) | 1d10 per caster level; ordinary plant matter is destroyed |
| Detect Thoughts | information | Mental before each memory question | questions = caster level; a success ends the spell |
| Dominate Person | control | Mental − Magic skill | recast: prior subjects save unmodified |
| Dominate Sense | debuff | Mental | failure binds for the Turn, success for one round |
| Invisibility | buff | — | one hour per level; violent motion breaks it for everyone |
| See Magic | information | — | one Turn per character level; subtle readings at 8+ |
| Speed | buff | — | double movement; 1 System Strain per user |
| Statis | control | — | up to one day per level; 4 items of Encumbrance while frozen |
| The Wind of Final Repose | incapacitate | — | 4 HD or fewer fall unconscious in a 20-ft radius |

## What parity means here

The tests (`tests/test_wwn_spell_effects_1085.py`) and this table are the same facts in two forms:

* `test_arcane_spark_scales_one_die_per_caster_level` — the 3d8 above;
* `test_a_made_save_halves_when_the_row_says_half` — 9 becomes 4, floor division, not 5;
* `test_destroy_earth_only_damages_plant_creatures` — the save applies only to plant monsters;
* `test_a_control_spell_reports_its_save_and_penalty` — `Mental − Magic skill` is in the data, not in
  the referee's memory;
* `test_untranscribed_names_the_batch_boundary` — 70 spells still have no effect row, and the
  resolver says so by name.

CWN is untouched: nothing here is a CWN procedure, and no CWN number appears in the catalogue.
