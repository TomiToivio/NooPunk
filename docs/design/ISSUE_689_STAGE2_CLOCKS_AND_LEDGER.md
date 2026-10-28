# Stage 2 — clocks and the paradigm ledger (#689)

**Status: PROVISIONAL specification.** Two state machines, no new dice. Nothing here edits the
rulebook; both are designed to be read by existing procedures and, later, by code.

---

## 1. Clocks

A clock is a named track of **4 or 6 segments**. It exists so that pressure accumulates visibly and
the table can see the world moving before it arrives.

| clock | segments | fills when | fires when full |
|---|---:|---|---|
| **Legwork** (per investigation) | 6 | the characters spend time, ask around, run down leads | the answer arrives — *and so does the opposition* |
| **Exposure** (per noetic event) | 4 | characters reach into the noösphere, or linger at a threshold | Stage 3 exposure, tier = segments filled |
| **Institutional attention** (per character) | 4 | legality falls, or conspicuous tech is used in public | a faction acts on the character directly |
| **Front** (per antagonist) | 6 | the antagonist is left unopposed | the antagonist's plan completes |

**Rules that keep clocks from becoming a second game:**

1. **One clock per question, never two.** If two clocks would fill on the same event, the table picks
   the one that matters and says so.
2. **A clock never rolls.** It fills when the fiction says it filled.
3. **Filling a clock is a consequence, not a punishment** — it must produce a scene, not a penalty.
4. **Clocks are public.** Hidden progress is bookkeeping, not drama.

**PROVISIONAL:** the 4/6 split.

## 2. The paradigm ledger

The genre model is **not four rulebooks**. It is one record, two integers per genre, read by existing
mechanics.

| genre | capability (0–5) | legitimacy (0–3) |
|---|---|---|
| **CWN — cyberpunk** | AGI, BCI, augmentation | legality, oversight, insurance |
| **SWN — science fiction** | disclosure, psionics, orbital presence | public acceptance, treaty status |
| **WWN — interdimensional** | noetic access, threshold tech | mainstream credibility |
| **AWN — post-apocalyptic** | institutional capacity, UN authority | state capacity in rogue regions |

**Movement — the two-forward, one-back rule:**

- An arc's outcome advances **capability by +2** in the genre it was fought in.
- The same arc **removes −1 legitimacy** from that genre, always, even on success.
- Legitimacy recovers by +1 only through an explicit institutional act (a treaty, a licence, a public
  inquiry, a trial that goes the right way) — which is itself a scenario.

So progress is never free, and the backlash is *always* in the same register. A cyberpunk arc that
unlocks wetware also criminalises it one step further.

## 3. What the ledger does mechanically (four readings, none new)

1. **Legality and price.** Capability high + legitimacy low = the frontier tech works and is illegal:
   black-market premium, police attention, a **Gamist** cost for the best tool in the box.
2. **Who will talk to you.** Contacts and factions gate on legitimacy — **Simulationist** consequence.
3. **Shock difficulty.** Society's baseline integration tier sets the starting penalty for Stage 3
   exposure. A society whose capability outran its legitimacy produces shocks for everyone.
4. **Compels.** A character whose standing depends on an institution gets compelled the moment that
   institution reverses — the **Narrativist** payoff, driven by world state instead of referee whim.

## 4. Worked example

> The arc ends: the characters expose an AGI that had been answering as a person.
> **CWN capability 2 → 4** (the tech is now proven), **CWN legitimacy 2 → 1** (it is now a criminal
> matter). Reading 1: the wetware that was a licence is now a black-market purchase at +50 % and a
> police flag. Reading 4: the character who works for the regulator is compelled this session — their
> employer now denies the thing they just proved.
>
> Next exposure in this city starts at **tier 2**, because the city's integration lags its capability.

## 5. The 20XX rule

The fiction says **20XX**. `2045` appears only as internal design shorthand and is **never printed in
fiction** — the setting prophesies nothing. Any document that needs a date uses `20XX` unless it is a
design memo, and even then the date must be labelled as shorthand.

## 6. Ownership (open question, P6)

The genre record currently lives in `strategy_game/data/genre_paradigms.json`. Whether the RPG reads
that file or owns its own copy is the author's call: **one file, one taxonomy** is the rule, but which
file is not yet decided.

## 7. What Stage 2 does not do

No rulebook edit, no code, no tests. It specifies state, not implementation.
