# NoöPunk

**Version:** 0.0.2 · **Status:** incremental draft

> Tomi authors one rule at a time; each approved rule is implemented in this rulebook and the same canonical Godot game (`noopunk/game/`).

## Premise

Noöpunk is a tabletop role-playing game set in the 20XX near future, in a world where the Noösphere has become a place people can enter. The player character is a **UNSA agent straight from the academy**. No further character background or specialization has been decided.

## Characters

### Seven attributes

| Attribute | Definition |
| --- | --- |
| Fitness | Your physical strength and constitution |
| Reflexes | Your physical dexterity, agility and coordination |
| Cognition | Your ability to process language and data |
| Cyber | Your ability to interface with technology |
| Awareness | Your intuition, perception and awareness |
| Agency | Your free will |
| Empathy | Your loving kindness and humanity |

### Generation

Roll **3d6 independently for each** of the seven attributes and convert each total into its displayed signed attribute value. The character sheet records the converted values, not the dice totals.

| 3d6 total | Attribute value |
| --- | --- |
| 3–4 | -3 |
| 5–6 | -2 |
| 7–8 | -1 |
| 9–12 | 0 |
| 13–14 | +1 |
| 15–16 | +2 |
| 17–18 | +3 |

The basic human range is **-3 to +3** for *every* attribute, including Empathy. Scores **above +3** are transhuman. No restrictions on player characters with -3 Empathy have been specified.

In Godot the same generation is in `noopunk/game/attributes.gd`; the character screen rolls or rerolls all seven values, displays the signed values, and preserves the selected roll when the player walks around.

## Core resolution

### Difficulty ratings (reference only)

| Target difficulty | Label |
| --- | --- |
| 6 | Easiest |
| 8 | Easier |
| 10 | Easy |
| 12 | Average |
| 14 | Hard |
| 16 | Harder |
| 18 | Hardest |

**No resolution dice mechanic has been specified.** These targets have no check or roll implementation yet.

## Gameplay

*Placeholder. Further gameplay and interaction rules are not yet written.*

## Scenarios

*Placeholder. Scenarios will be listed here as they are authored.*


---

The machine-readable copy of the attribute and difficulty tables is
`noopunk/game/data/attributes.json`; the game reads that file.
