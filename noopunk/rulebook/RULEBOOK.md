# NoöPunk

**Version:** 0.0.2 · **Status:** draft, rules 1 of N

> This rulebook is written into one piece at a time, together with the game. Only what follows has been
> decided; everything else is blank on purpose.

## Premise

Noöpunk is a tabletop role-playing game set in the 20XX near future, in a world where the Noösphere has
become a place people can enter.

You play a **UNSA agent, fresh from the academy**.

## What exists so far

1. Seven attributes and how a new agent's values are rolled (§1).
2. A difficulty scale (§2) — reference only; no dice mechanic resolves against it yet.

Nothing else is defined: no skills, checks, combat, injury, inventory, experience, encounters,
equipment, academy specialisations, professions, classes, backgrounds or NPCs.

## 1. The seven attributes

| Attribute | Definition |
| --- | --- |
| **Fitness** | Your physical strength and constitution. |
| **Reflexes** | Your physical dexterity, agility and coordination. |
| **Cognition** | Your ability to process language and data. |
| **Cyber** | Your ability to interface with technology. |
| **Awareness** | Your intuition, perception and awareness. |
| **Agency** | Your free will. |
| **Empathy** | Your loving kindness and humanity. |

### Rolling a new agent

Roll **3d6 separately for each of the seven attributes**. Convert each total to the attribute's value
with this table:

| 3d6 total | Attribute |
| --- | --- |
| 3–4 | −3 |
| 5–6 | −2 |
| 7–8 | −1 |
| 9–12 | 0 |
| 13–14 | +1 |
| 15–16 | +2 |
| 17–18 | +3 |

The character sheet shows the **converted signed value** — `Fitness+2`, `Empathy-3`, `Agency+0`. The
raw 3d6 total is not a stat; it exists only to be converted.

**Basic human range:** −3 to +3. A new agent's rolls cannot leave it. **Above +3 is transhuman.** −3 is
a legitimate basic-human score for every attribute, Empathy included.

Rerolling is a fresh set of seven rolls; a rerolled sheet replaces the previous one, and a sheet that
has been rolled is kept as the character walks into a scene.

### One table, two readers

The table above is the single source of truth, and it is also machine-readable at
**`noopunk/game/data/attributes.json`** — the same file the game reads. If the book and that file ever
disagree, that is a defect, not a variant rule.

## 2. Difficulty ratings

| Target | Label |
| --- | --- |
| 6 | Easiest |
| 8 | Easier |
| 10 | Easy |
| 12 | Average |
| 14 | Hard |
| 16 | Harder |
| 18 | Hardest |

**No resolution mechanic is defined yet.** These targets are reference data: what a roll is made with,
whether a check is rolled at all, and what a character adds to it are all undecided.

## 3. Undecided, deliberately

- The resolution dice mechanic for a difficulty target (2d6, d20, 3d6 or automatic — *not chosen*).
- Skills and skill checks.
- Combat, injury, healing, strain.
- Inventory, equipment and money.
- Experience and advancement.
- Encounters, NPCs and scenarios.
- Academy specialisations, professions, classes, backgrounds and history.

Each arrives only when the author supplies it, and each is implemented in `noopunk/game/` in the same
change that writes it here.
