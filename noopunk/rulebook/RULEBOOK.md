# NoöPunk

**Version:** 0.0.1 · **Status:** blank draft

> This rulebook is intentionally empty. It exists so that rules can be written into it one at a time,
> together with the game, instead of being generated wholesale.

## Premise

Noöpunk is a tabletop role-playing game set in the 20XX near future, in a world where the Noösphere has
become a place people can enter. This paragraph will be replaced when the author supplies the real
premise; until then it is a placeholder and carries no rules weight.

## How this book is written

Every rule in this book arrives from Tomi, one piece at a time, and is implemented in the accompanying
Godot game in the same pass. Nothing is added here speculatively — no attribute tables, no skill lists,
no combat, psionics, hacking, factions or scenarios — until that specific piece is authored.

## Contents

1. [Characters](#characters) — *not yet written*
2. [Core resolution](#core-resolution) — *not yet written*
3. [Gameplay](#gameplay) — *not yet written*
4. [Scenarios](#scenarios) — *not yet written*

## Characters

*Placeholder. Character creation rules will be written here.*

## Core resolution

*Placeholder. The dice mechanic will be written here.*

## Gameplay

*Placeholder. Turn structure, movement and interaction will be written here.*

## Scenarios

*Placeholder. Scenarios will be listed here as they are authored.*

## 1. Character creation: a UNSA agent from the academy

The player character is a **UNSA agent straight from the academy**. Nothing else about the character
is defined yet: no specialisations, professions, classes, skills, equipment, history, careers,
factions or NPCs.

### 1.1 The seven attributes

| Attribute | Definition |
| --- | --- |
| **Fitness** | Your physical strength and constitution |
| **Reflexes** | Your physical dexterity, agility and coordination |
| **Cognition** | Your ability to process language and data |
| **Cyber** | Your ability to interface with technology |
| **Awareness** | Your intuition, perception and awareness |
| **Agency** | Your free will |
| **Empathy** | Your loving kindness and humanity |

### 1.2 Generation: 3d6 per attribute

Roll **3d6 separately for each attribute**, then convert the total into the displayed value:

| 3d6 total | Attribute |
| --- | --- |
| 3-4 | -3 |
| 5-6 | -2 |
| 7-8 | -1 |
| 9-12 | 0 |
| 13-14 | +1 |
| 15-16 | +2 |
| 17-18 | +3 |

The character sheet presents the **seven converted signed values**, not the raw 3d6 totals.

**Basic human range: -3 to +3.** Above +3 is transhuman. A score of -3 is legitimate for any
attribute, including Empathy.

### 1.3 Difficulty ratings

| Target | Label |
| --- | --- |
| 6 | Easiest |
| 8 | Easier |
| 10 | Easy |
| 12 | Average |
| 14 | Hard |
| 16 | Harder |
| 18 | Hardest |

**Reference only for this milestone: no resolution dice mechanic has been specified for these
targets.** Do not infer one from the generation dice.

### 1.4 Single source of truth

The attribute list, generation table and difficulty ratings are published machine-readably in
[`noopunk/game/data/attributes.json`](../game/data/attributes.json). The Godot game loads that file
and builds its sheet from it, so this chapter and the game cannot disagree.
