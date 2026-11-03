# AWN Stress and survival — the paper procedure

Two AWN subsystems in this repository are implemented in Python and were, until now, missing their
paper-and-dice counterpart: the **Stress track** and **crisis-zone survival**. This page is that counterpart.
It is a table procedure, not a table: it needs the book for the printed values (AWN pp.56–63), and the
values the code uses live in `data/rules/awn_stress.json` and `data/rules/awn_survival.json`.

Sources: *Ashes Without Number, Deluxe Edition* (Kevin Crawford), pp.56–63. The text below is an
independently written procedure; the book's prose and tables are not reproduced.

## Stress

**What it is.** A second resource for life after the fall, separate from CWN System Strain. It does not
replace Strain, heal hit points, or gate CWN actions. A character can be at zero Strain and maxed on
Stress, or the reverse.

**Track it in six boxes**, one per point, plus a threshold box for the character's current maximum.

1. **Gain Stress** when the GM calls a Stress event (violence, privation, an ontological shock, an NHI
   encounter, sleep lost to the siege). Each event has a printed amount; write it in and add.
2. **Compare to the threshold.** While Stress is at or below the threshold, play continues normally.
3. **Over the threshold.** The character takes the printed penalty for being over — the tracker's
   `penalty()` is what the sheet shows — and is eligible for a breakdown result.
4. **Harden** at a milestone the GM and player agree on: one point of the track becomes permanently paid,
   raising the threshold. Hardening is a change to the character sheet, not a refresh.
5. **Recover** with the printed conditions (rest, safety, care): the tracker's `recover()` steps the track
   down. The book's own recovery rules decide how much and how often.
6. **A new day** advances the clock, expires what expires, and is what the Python `next_day()` does.

**Worked example.** Mira has 14 Stress against a threshold of 12 after a night in a flooded shelter, so she
is over by 2 and takes the printed penalty. The next scene she is not asked to roll a second time for the
same cause: one event, one gain. After two days of food and sleep she recovers 2 and is back at the
threshold — still hardened by nothing, still one bad night from over again.

**With AWN off**, the track does not exist. `is_enabled()` is the switch; a campaign that has not entered a
collapsed region never opens the sheet.

## Survival: travel, scouting, supplies, privation

**What it is.** The cost of moving through a crisis zone: hours, food, water, and what happens when they run
out. It runs on **CWN's** attributes and skills; only the resources are AWN's.

**A travel day, in order:**

1. **Pick the terrain** — `terrain()` gives its movement cost and encounter profile.
2. **Spend hours** — `travel_hours()` for the route; `hexes_per_day()` for how far that gets a party.
   A day that runs long is a day that costs supplies.
3. **Check for encounters** where the terrain and the region's state call for it — `encounter_check()`.
4. **Scout** if the party split off a scout: `scouting_days()` and `going_astray_difficulty()`; a failed
   Navigation-style check means the day is spent and the party is where it started (`goes_astray()`).
5. **Eat and drink.** `food_encumbrance()` says what carrying the supplies costs in the CWN encumbrance
   system; a party that did not carry them is out of them.
6. **Pay for privation** if supplies are gone: `privation_strain()` applies CWN System Strain, and
   `starvation_death_save_needed()` says when it turns lethal. `forage()` is the way back — the GM sets the
   difficulty from the terrain rather than inventing one, because the book does not print a table for it.

**Worked example.** A three-person party crosses broken farmland (2 days, 16 hours) with two days of water.
Day one is uneventful. On day two the scout fails the route check, the day is lost, and the water is gone:
one point of privation Strain each, and the next day without water is a death-save day, not a Strain day.

## What is not covered

* AWN's own **addiction** procedure (p.58) is not transcribed; the tracker's recovery steps exist, the
  addiction ladder does not.
* AWN's **disease** (p.54) and **radiation** (p.55) procedures are unimplemented.
* The **enclave turn** (pp.104–135) — Power, Cohesion, Dominion, Interest, actions — is not implemented.
  The NoöPunk ledger records enclaves as dated actors; it does not play AWN's turn.

Each of those is a row in `data/rules/awn_traceability.json` marked `missing` or `partial`, with the page
cited. A paper procedure that pretended otherwise would be worse than no procedure.
