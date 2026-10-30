> ## ARCHIVED — SUPERSEDED BY #848
>
> The seven-attribute system in this file is **not canon**. Issue #848 restored vanilla CWN (primary) and
> vanilla SWN Revised psionics; the canonical rulebook is `rulebook/00_INDEX.md`.

# NoöPunk

**Version:** 0.1.0 · **Status:** draft — character sheet only

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

1. [Characters](#characters) — the UNSA rookie and the seven attributes
2. [Core resolution](#core-resolution) — difficulty targets only; the dice mechanic is not yet written
3. [Gameplay](#gameplay) — *not yet written*
4. [Scenarios](#scenarios) — *not yet written*

## Characters

### The player character

The player character is a **UNSA agent straight from the academy**. Nothing else about them is defined
yet: no specialisations, professions, classes, skills, equipment, history or contacts exist until they
are authored.

### The seven attributes

Every character has exactly seven attributes. There are no others.

| Attribute | Definition |
| --- | --- |
| **Fitness** | Your physical strength and constitution |
| **Reflexes** | Your physical dexterity, agility and coordination |
| **Cognition** | Your ability to process language and data |
| **Cyber** | Your ability to interface with technology |
| **Awareness** | Your intuition, perception and awareness |
| **Agency** | Your free will |
| **Empathy** | Your loving kindness and humanity |

### Rolling attributes

Roll **3d6 separately for each attribute** — seven independent rolls. Convert each total to the
attribute's value with this table, and record **the converted value**, not the dice total.

| 3d6 total | Attribute value |
| --- | --- |
| 3–4 | −3 |
| 5–6 | −2 |
| 7–8 | −1 |
| 9–12 | 0 |
| 13–14 | +1 |
| 15–16 | +2 |
| 17–18 | +3 |

**Basic human range is −3 to +3.** A value of −3 is a legitimate basic-human score for any attribute,
Empathy included. Values **above +3 are transhuman**; the academy roll never produces them.

### The character sheet

A starting sheet is only this: the character's name, the fact that they are a UNSA agent fresh from
the academy, and the seven signed attribute values. Nothing else is recorded yet.

> **Machine-readable copy.** The table above is also stored as data in
> [`noopunk/game/data/attributes.json`](../game/data/attributes.json), which the Godot game reads. The
> game does not hold a second copy of the bands: this book and the game consume one table.


## Core resolution

*The dice mechanic is not yet written. This section records the difficulty targets, which are reference
data until that mechanic exists.*

### Difficulty targets

| Target | Label |
| --- | --- |
| 6 | Easiest |
| 8 | Easier |
| 10 | Easy |
| 12 | Average |
| 14 | Hard |
| 16 | Harder |
| 18 | Hardest |

**No resolution mechanic has been specified for these targets.** Do not assume 2d6, d20, 3d6 or an
automatic success: how a character reaches a target will be authored as its own rule. These are the
same values the game stores in `noopunk/game/data/attributes.json`.


## Gameplay

*Placeholder. Turn structure, movement and interaction will be written here.*

## Scenarios

*Placeholder. Scenarios will be listed here as they are authored.*
