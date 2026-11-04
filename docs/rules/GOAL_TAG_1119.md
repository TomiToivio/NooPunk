# The Goal tag — tabletop procedure (#1119)

One tag. One line on the sheet. No new dice, no new currency, no new engine.

```
Goal: <description> | owner: <character or faction> | horizon: short / medium / long | status: <note>
```

The Python side is `src/rules/goals.py` (the lifecycle) and the console verbs `goal`, `goals`,
`progress`, `award`. The level a goal's XP implies comes from `src/rules/cwn_advancement.py` — the CWN
table, not a second one. Nothing here changes a CWN attribute, roll, save, hit point or procedure.

## The five steps at a table

1. **Write the tag.** `Goal: Arrest Roy Batty | owner: Romppainen | horizon: short | status: new`.
   A horizon is one of `short` (completes in a scene or a case), `medium` (several scenarios) or
   `long` (a direction that may never close).
2. **Play CWN as written.** The tag never modifies a roll. Resolution uses unmodified Cities Without
   Number rules and any already-authorised optional mods.
3. **When something relevant happens, record it with the event that evidences it.** The five kinds are
   `progress`, `contribution`, `completed`, `failed`, `abandoned`. Write *what happened*, dated:
   `13.11. custody established, Batty in the Sörnäinen cells`.
4. **Retire or keep.**
   * `completed` on a short or medium goal **retires the tag** — cross it off the sheet.
   * `contribution` is only for `long` goals: the tag stays and the contribution is logged.
   * `failed` / `abandoned` also retire it, and **pay nothing**.
5. **Pay, if the table agrees.** A qualifying completion or contribution is worth **1 XP** (the code
   accepts 1–3 as a typo guard, not a balance ruling). Use the CWN XP total and level table. Record
   perks — a promotion, a liaison, a search warrant — as prose next to the tag, not as a mechanical
   bonus.

## Three rules that stop a tag becoming an economy

| rule | why |
| --- | --- |
| **One event pays once, per owner** | A case that advances three of a character's goals is still one case. The ledger keys on `(owner, event)`, so the second award is refused with a reason. |
| **A faction never receives character XP** | A faction is not a CWN character. It earns assets, access or standing, written down as a perk; its members earn their own XP by taking part. |
| **Attempts do not pay** | `progress` pays nothing, `contribution` is long-horizon only, and failing or abandoning pays nothing. Otherwise "we tried" becomes a farm. |

## The four worked examples

These are the examples the issue names, and the ones `tests/test_goals_1119.py` runs.

### 1. Short — `Have Sex Tonight` / `Arrest Roy Batty`

```
Goal: Arrest Roy Batty | owner: Romppainen | horizon: short | status: new
  → 13.11.  completed: custody established   (event: case:lakkahaltia)
  → award 1 XP                              (level 1 → still level 1 at 1 XP)
```

Cross the tag off. The 1 XP is CWN experience: three such cases reach **3 XP = level 2** on the fast
track, which is the fastest a goal can move a character and is also what an ordinary successful
mission pays.

### 2. Medium — `Get a Promotion`

```
Goal: Get a Promotion | owner: Romppainen | horizon: medium | status: new
  → 01.11.  progress   closed case 1 with both clues
  → 08.11.  progress   closed case 2 with both clues
  → 15.11.  progress   the board reads the file
  → 20.11.  completed  promotion signed         (event: board:2026-11-04)
  → award 1 XP
```

The three `progress` lines pay nothing. The promotion, the pay rise and the new access are the
institution's decision: write them as perks. A tag that handed out a rank would be replacing the
organisation with a loot table.

### 3. Long — `Prevent Human Extinction`

```
Goal: Prevent Human Extinction | owner: UNSA Helsinki field office | horizon: long | status: active
  → 04.11.  contribution  stopped a rogue-ASI breakout, preserved the containment evidence
  → award 1 XP to the participating character(s)  (one event, one payment)
  → 19.12.  contribution  a second, different intervention → another eligible event
```

The tag stays active; the goal may never be "completed", and the procedure does not ask it to be.
What pays is a **distinct, substantial** contribution, not the repetition of the same act — and not
the announcement of good intentions.

### 4. Faction — `Secure an institutional mandate`

```
Goal: Secure an institutional mandate | owner: UNSA field office | horizon: medium | status: new
  → 04.11.  completed  board:2026-11-04
  → perk: two additional field agents and a Europol liaison
```

`award` on a faction goal is **refused**: `unsa is a faction: faction rewards are assets, access or
standing, not character experience`. The agents who did the work may separately earn their own XP for
the cases they actually ran.

## What this deliberately does not do

Personality, mental state, reputation, bionics, psychotronics, conditions, modifiers, psi tags, a
universal tag framework, a rules DSL, goal dice or an automatic goal inference. Each is a later issue
with its own playable example, in the order the issue sets: **Goal → Reputation → Personality →
Bionics**, and psychotronics only when a scenario needs a device.

## The console, verb by verb

```
goal <owner> <horizon> <description>      add a tag; prefix a faction owner with faction:
goals                                     the active tags, each as its paper line
progress <goal> <kind> <event> [note]     progress|contribution|completed|failed|abandoned
award <goal> <event>                      pay CWN XP for a recorded completion/contribution
```

Same facts, same refusals, as the table. `tests/test_goals_console_1119.py` runs the four verbs, saves,
reloads, and checks that a save written before goals existed still loads with an empty log.
