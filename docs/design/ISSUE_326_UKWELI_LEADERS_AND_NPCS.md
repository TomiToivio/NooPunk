# Ukweli faction leaders and NPCs: Sir Mars Eldrich and the Eldrich dynasty (#326)

**Status: PROPOSAL — design-level content only.** No mechanic, no statistic, no threshold and no
action economy. `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**; the four-leader economy
belongs to #323 and is not restated here as fact. This document is the human-readable companion to
`strategy_game/data/ukweli_leaders.json`, which carries the same content as data with an executable
validator (`strategy_game/leaders.py`, `tests/test_ukweli_leaders.py`).

It builds on the PROPOSAL comment of 15:39 on this issue rather than replacing it. Its central stance —
**fill only Mars, leave the other seats as declared blanks, because inventing individuals is what #325
and `AGENTS.md` §1 forbid** — is kept.

---

## 1. What already existed before this work

Three things the issue asks for are **already on `main`**, and this design consumes them instead of
re-authoring them:

| Already landed | Consequence |
| --- | --- |
| **Sir Mars Eldrich is a canonical character card** (`data/character_cards.json`, PR #363) | The roster carries a `card_ref` to it. It does not restate, extend or re-author his card. |
| **The twelve leader seats already exist** (`data/ukweli_local.json`: `cpu1`–`cpu4`, `uip1`–`uip4`, `ulp1`–`ulp4`) | The roster **annotates** those records with the institutional tie each seat needs. It invents no leader id. |
| **The four portfolios already exist** (`politics`, `networks`, `operations`, `research`) | Reused verbatim, with each faction covering all four exactly once. |

A test asserts all three: that every seat resolves to an existing record, that seat portfolios agree
with those records, and that the roster's seat ids are exactly the existing set.

---

## 2. The dynasty: three eras, one playable present

| Generation | Status | What the scenario keeps |
| --- | --- | --- |
| **Sir Uranus Eldrich** (19th c.) | historical — **invocable, not agentic** | an **unsettled archive**. The scandal stays allegations; the mansion stays a source of Gothic and New Weird folklore, archival investigation, conspiracy claim **and misleading clue**, with no predetermined supernatural revelation. |
| **Sir Mercury Eldrich** (1964) | historical — **invocable, not agentic** | a **standing obligation with no owner**. He facilitated a peaceful transition rather than bestowing it; the debt is inherited in **both** directions and either side may call it in. |
| **Sir Mars Eldrich** (present) | present — agentic, **but not a council seat** | an **attention economy with a balance sheet**: money, media, inventions, a space venture, and a party relationship that stays formally autonomous. |

Each dead generation is a **library of event hooks**, not a character competing for action slots. A
test enforces this: a historical person who holds a council seat is reported as a defect, and only the
`present` person may carry a live `card_ref`.

### The 1964 invariants

Held as canon constraints on Mercury's entry, because the issue makes them acceptance criteria:
independence stays **1964**, stays **peaceful**, stays **CPU-led**, and British enterprises were
**negotiated into protection** rather than expropriated. What must *not* be asserted: that independence
was granted by the Eldrich family, or that the CPU owes the firm anything that was not negotiated.

### What must not be asserted about Mars

The legacy register contains his *later* fate. `AGENTS.md` §0 forbids narrating the NHI Crisis as
resolved, so the roster records his guard explicitly: **not** that the Mars ruins are proven artificial,
**not** that stargates or anomalous transport exist, and **not** that his patronage makes the party his
instrument. In the present day his Mars venture reads as publicity plus real engineering economics —
launch cadence, insurance, freight, orbital logistics, contracts. The player sees the seed and **cannot
prove the harvest.**

---

## 3. Relationship edges

Tabular, no new quantity. Trust is left `null` except where the existing data already carries one.

| From | To | Kind | Note |
| --- | --- | --- | --- |
| `sir_mars_eldrich` | `ulp` | patronage | funds and publicly supports the party, which stays formally autonomous — derived from the landed card |
| `sir_mars_eldrich` | `sympathetic_media` | patronage | publicity is not endorsement, and reach is not votes |
| `sir_uranus_eldrich` | `sir_mercury_eldrich` | dynastic succession | historical; the firm passes to the second generation |
| `sir_mercury_eldrich` | `cpu` | **inherited obligation** | the 1964 bargain is inherited in both directions |
| `sir_mars_eldrich` | `cpu` | rivalry | patron of the opposition, and **not sovereign over the port** |

---

## 4. The twelve seats, left deliberately empty

Each faction has four seats, each seat carries the four-portfolio assignment it already had plus a
proposed **institutional tie** — *and no person*. Every entry is marked
`TODO: requires author specification`.

This is the load-bearing decision. Specifying the **shape** and refusing to fill it is what lets #324's
deliverable D and #327's cross-tab be written later without either pass inventing people. A test fails
if any seat carries a person.

| Faction | politics | networks | operations | research |
| --- | --- | --- | --- | --- |
| **cpu** | state apparatus, governing record | labour and mass organisations | port, industry, resource base | universities, technical intelligence |
| **uip** | rural and communal bodies | religious and civic associations | land, agriculture, coastal economy | cultural and historical institutions |
| **ulp** | parliamentary opposition role | business, property, private sector | enclave economy, offshore arrangements | private research, tech investment, sympathetic media |

The independent-NPC slot is likewise declared and **left empty**, with its template recorded, and
`already_covered_elsewhere` notes that Mars is already an independent patron with a canonical card.

---

## 5. Event hooks — five candidate interactions

Kept as invocable hooks, each naming the generation it draws on, so a dead generation generates fiction
without acting:

| Hook | Era | Drawn from | Strategic shape |
| --- | --- | --- | --- |
| The Independence Bargain | historical | Mercury | leaked papers fuel competing readings of liberation, pragmatism, compromise and privilege |
| The Island's Charter | present | Mars | legitimacy, jobs, investment and party relations move together |
| The Latest Eldrich Invention | present | Mars | publicity converts to influence, with reputational risk |
| A Mars Mission | present | Mars | a real, expensive commitment a government can tax, subsidise or nationalise the optics of |
| The Uranus Papers | historical | Uranus | no predetermined revelation; the archive may mislead |

A test asserts that a historical hook is drawn from a historical person, and that every hook reference
resolves.

---

## 6. A finding worth your attention: the party has two names

The libertarian party is **`ulp` — "Ukweli Libertarian Party"** in the scaffold data
(`data/ukweli_local.json`), and the landed Eldrich card gives his `faction_ids` as `["ulp"]`. But
`docs/world/PEOPLES_REPUBLIC_OF_UKWELI.md` uses **`LFP` — "Libertarian Freedom Party of Ukweli"**, and
that document explicitly flags the conflict as *awaiting your word*.

**This roster uses the existing data id `ulp`**, because the scaffold and the landed card both already
use it and inventing a fourth party id would fork the data. The label question is surfaced in
`naming_note` and left **open** — with a `TODO` — rather than silently resolved. A test asserts the
conflict is surfaced and *not* resolved, so neither name can quietly win.

---

## 7. Canon, allegation, propaganda

Three registers, kept distinct in the data itself. Every dynasty person carries an `evidence_classes`
list and a `what_must_not_be_asserted` guard, and a test requires both to be non-empty. That is the
mechanism that stops a claim drifting upward into canon by repetition: Uranus's scandal is
`allegation`, the mansion's reputation is `folklore`, Mercury's bargain is `canon` for its terms and
`interpretation` for its moral weight, and Mars's venture is `canon` for the economics and silent on
the outcome.

---

## 8. Scope compliance

- **No extra leader mission slots:** four seats per faction, per #323. No member count adds a slot.
- **No second statistical system:** no score, rating, track or influence quantity appears anywhere —
  a test greps for numeric-looking field names and for `hegemony_score` / `influence_track` /
  `power_track` / `victory_points`, and the existing `skill` field is deliberately **not** restated or
  extended here.
- **Standalone:** the module imports no LaclauGPT code and needs no optional dependency.
- **No existing file rewritten:** this adds `data/ukweli_leaders.json`, `leaders.py`, its tests and this
  document.

---

## 9. Open questions for the author

1. **`ulp` or `LFP`?** Settling it changes the label and the documents together (see §6).
2. **Does Mars ever take a council seat?** If so it consumes one of the four action slots under #323.
3. **Are the twelve institutional ties right?** They are proposals; the seats stay empty until filled.
4. **Which generation's secrets stay unresolved forever** — Uranus's archive, Mercury's bargain, or
   both?
