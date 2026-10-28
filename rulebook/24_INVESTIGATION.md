# 24. Investigation: finding, interpreting, acting

**Status: PROVISIONAL — proposed procedure (#704), not approved canon.** This chapter states the
investigation layer in tabletop terms; the design record is
[`docs/rules/GUMSHOE_INVESTIGATION_LAYER.md`](../docs/rules/GUMSHOE_INVESTIGATION_LAYER.md), the
executable form is `src/rules/investigation.py`, and the worked case graph is
`data/scenarios/lakkahaltia/case_graph.json`. Nothing here changes the core check, the skill list,
or any character's sheet.

## The three acts, kept apart

The failure this chapter exists to prevent is the classic detective dead end: the party rolls
badly, misses the one clue, and the session stops. The answer is not "roll better" — it is to stop
rolling for the thing that must not fail.

| act | who decides | mechanism |
| --- | --- | --- |
| **Finding** a fact the world contains | the character's competency | **automatic** — no roll, no difficulty, no failure |
| **Interpreting** what the facts mean | the player | **no mechanic**; the rules may classify evidence, never conclude |
| **Acting** on the facts | the dice | the core check (`2d6 + attribute modifier + skill rank`), with its stakes |

So a search is not one check. Deciding to search is free. The search yields what the character is
competent to notice. The risky part — the guard coming back, the patient waking, the lock that has
to be forced, the terminal that logs the query — is what rolls.

## Finding

- Every scene a case passes through carries at least one **core clue**: the fact without which the
  case cannot continue. A competent investigator receives it by looking.
- **Competency is the skill on the sheet.** Rank 0 is trained, so `Heal 0` is competent and
  receives the clinical clue; the absence of the skill is what untrained means. Competence is
  never a chance of noticing.
- **The listed skill is one route, not a straight jacket.** If the players propose another
  plausible method the character could actually carry out, the referee gives the information.
  Refusing because "that is not the skill on the card" is the rule being used wrongly.
- **A passive clue needs no declared search.** When the party is only passing through, whoever
  has the highest rank in the relevant skill notices it. Nobody has to sweep every corridor.
- **No dead ends.** A scene may not rest its only exit on an obscure specialism, and every lead
  must point at a scene that exists. The case-graph loader refuses both, so an authoring error is
  caught before play rather than at 2 a.m.
- **The party is the unit of coverage.** A case is written for a group; the referee checks before
  play that the group's skills reach each scene's core clue. One character being unable to read a
  network log is correct — the group having no route at all is a broken case.

## Benefits: extra information at a price

GUMSHOE buys supplementary information with spends from investigative pools. **NoöPunk does not
import those pools**: SWN Effort is the game's one spendable currency and CWN ranks are training,
not fuel, so a second pool would be a second economy. A **benefit** instead names the CWN price it
takes:

| price | example |
| --- | --- |
| a check under pressure | reading the protected backup before security arrives |
| a scene of time | an hour in the folklore archive while the ward closes |
| a favour or a contact | a night nurse talking off the record |
| money, Strain or access | a records pull, a lab rush, an unauthorised terminal |

The referee charges the price with the ordinary procedure for it. If the price cannot be paid,
**nothing is lost**: the core clue already stands, and a benefit is an extra, never a toll.

## Interpreting

- A **clue is a fact**: a timestamp, a discrepancy, a stain, a sentence somebody said. It is not a
  conclusion, and the case data has to read that way.
- A **hypothesis belongs to the player**. The sheet may record which clues support and which
  contradict a theory; nothing in the rules sets the player's confidence, and no roll decides what
  a character believes.
- **A case carries more than one reading.** A case graph is refused unless it holds at least one
  **mundane** and one **anomalous** hypothesis, because an anomaly has to have an ordinary
  explanation available. Both may be supportable by the same evidence; that is the point.
- **No diagnosis as truth.** A patient can describe an experience accurately and the explanation
  still be open. Psychiatric care is not evidence of unreliability, and illness is not a category
  of the paranormal.

## Acting

Everything dangerous is the ordinary game: announced difficulty, stated stakes, the core check,
its consequences, and the time and Strain it takes. Failure closes **a route**, not every route to
a fact that must be found — the referee offers another way at a cost rather than stopping the case.

## Writing a case

Five lines, then play:

1. the scenes the case passes through;
2. one core clue in each, reachable by an ordinary skill;
3. every lead pointing at a scene that exists;
4. at least two hypotheses, one mundane and one anomalous;
5. for each clue worth enriching, a benefit and its price.

The machine-readable shape is `noopunk-case-graph`; `data/scenarios/lakkahaltia/case_graph.json` is
a complete example over the existing Lakkahaltia case data.

## What this chapter deliberately does not do

- **No new skills, attributes or derived statistics**, and no investigative ability list of its own.
- **No pools and no spends.** A benefit's price is a CWN cost, paid by the CWN procedure that
  already covers it.
- **No second resolution mechanic.** Finding is free, acting is `2d6`, saves are `1d20`.
- **No truth resolution.** The rules never decide what happened; they decide who can find out what,
  and what it costs.
- **No roll for the core clue.** A test asserts that `discover()` has no
  roll, die, dice, rng or random parameter, so the rule cannot be quietly reversed in code.
