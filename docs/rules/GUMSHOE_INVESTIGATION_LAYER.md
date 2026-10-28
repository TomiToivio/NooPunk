# The investigative layer: GUMSHOE on the CWN chassis (#704)

**Status: design record plus a first implementation.** `src/rules/investigation.py` and
`tests/test_investigation_layer.py` implement the discovery/interpretation/action split.
Nothing in the existing rulebook was rewritten.

---

## 0. Licensing, first because it binds

The GUMSHOE SRD is released by Pelgrane Press under **Creative Commons Attribution 3.0
Unported (CC BY 3.0)**. Two consequences, and the second is the one people forget:

1. **Attribution is required.** Any adaptation must credit *GUMSHOE SRD © Pelgrane Press*,
   with the licence named and linked.
2. **CC BY covers the text; it does not cover the marks.** "GUMSHOE", the Pelgrane logo and
   the game lines built on it are trademarks, and the SRD grants no right to use them in a
   product's title or branding. NoöPunk therefore uses the *method*, not the name.

**No SRD text is reproduced in this repository.** Everything below is our own description of
a mechanism, which is what "interoperable mechanics" means in `docs/rules/RULES_FOUNDATION_POLICY.md`.

### Note on the links in the issue

The PDF link given in #704 (`…/files/GUMSHOE_SRD_CC_3.pdf`) returned a **29-byte stub**
reading "Multisite support not enabled" on 2026-10-28. The working sources are:

- **v3 (2024-12-09), 303 pages** — <https://pelgranepress.com/gumshoe/files/GUMSHOESRDCC-3%20241209.pdf>
- earlier CC version — <https://pelgranepress.com/gumshoe/files/GUMSHOE%20SRD%20CC%20version.pdf>
- version history and licensing — <https://pelgranepress.com/2013/10/24/the-gumshoe-system-reference-document/>

## 1. What GUMSHOE actually asserts

Three claims carry the system, and only the first is usually quoted:

1. **Core clue per scene.** For each scene the GM designates the clue you absolutely need
   to reach the next scene. It is not gated behind an obscure ability, and **the designated
   ability is "just one possibility, not a straight jacket"** — if the players find another
   plausible route, the information is given anyway.
2. **A rating means competence, not a chance of failure.** Having any rating in a relevant
   investigative ability means you automatically obtain the information that moves the story
   forward. The die is not consulted for *whether you see it*.
3. **Spends buy more.** Points from an investigative pool can be spent for supplementary
   information and advantages — never to unlock the core clue.

The failure mode this exists to prevent is the classic detective-game dead end: the party
rolls badly, misses the one clue, and the session stops. GUMSHOE's answer is not "roll
better" but "do not roll for that".

## 2. Why this is a real collision with CWN, and how it is resolved

CWN is a roll-first engine: the check is the unit of play. Importing GUMSHOE naively would
create two competing procedures for the same fictional act — *do I roll to search the room
or don't I?* — which is the duplication this repository keeps having to undo.

The resolution is a **three-way split by purpose**, not by activity:

| purpose | who decides | mechanism |
|---|---|---|
| **Finding** a fact the world contains | the character's competency | **automatic**, no roll, no difficulty |
| **Interpreting** what the facts mean | the player | **no mechanic**; the system may classify evidence, never conclude |
| **Acting** on the facts | the dice | **CWN `2d6 + attribute modifier + skill`**, with time, Strain and danger as the stakes |

A search is therefore *not* one check. Deciding to search is free; the search yields what
the character is competent to notice; and the risky part — the guard coming back, the
patient waking, the lock that must be forced — is what rolls.

## 3. What the implementation enforces

`src/rules/investigation.py`:

- `Clue` — a fact with a scene, a competency and a kind (`core` / `optional`). A clue is
  never a conclusion.
- `Case.validate()` — refuses a case where **any scene has no core clue** (a dead end), where
  a scene's **only exit is gated behind an obscure competency**, or where a **lead points at
  a scene that does not exist**.
- `discover(...)` — returns the core clue plus every optional clue the investigator's own
  competencies cover. It takes **no roll parameter**, which is asserted by a test.
- `Investigator.spend(...)` — spends a rating for supplementary information; spending never
  removes competence, and an unrated ability cannot be spent.
- `Hypothesis` — records `supports` / `contradicts` / `neutral`, and **confidence is set only
  by the player**. A test asserts that evidence does not move it.

`hypotheses_remain_open()` always returns `True`. It exists so that the intent is written
down where a future refactor will look for it: the model does not solve the case.

## 4. Spends without a second currency

GUMSHOE's investigative pools are a resource. NoöPunk has an explicit standing rule against
adding a second track beside Trauma/Frail/Strain (D46), so pools are **not imported as
written**. The mapping proposed here:

| GUMSHOE spend | NoöPunk cost |
|---|---|
| extra detail beyond the core clue | **time** — a scene of mission time, which in a live case is a real cost |
| a favour, a records pull, a lab rush | **Strain** or money, whichever the fiction names |
| pushing past resistance | **the CWN check**, with its normal consequences |

This keeps spending meaningful without inventing a fourth resource bar.

## 5. Worked example — Lakkahaltia, mundane and anomalous

The psychiatric-hospital case is the right test because it must be genuinely ambiguous.

**Scene 1 — the ward.** Core clue: *the drip counter was reset by hand.* Competency:
Forensics, or Medicine, or simply asking the night nurse.
- *Mundane path:* a nurse covered a missed observation. Roster records confirm.
- *Anomalous path:* the reset coincides with a gap in the building's own logs, and the
  patient's account of the missing hours matches nothing in the drug record.
**Neither is confirmed by the clue.** The clue is a fact; the theory is the player's.

**Scene 2 — the night office.** Core clue: *the roster was changed twice.*
**Scene 3 — the patient interview.** No core clue: the scene yields what the interviewer is
competent to elicit, and what the patient chooses to say is fiction, not a check.

The mundane hypothesis can be *supported* by every scene and still be wrong. That is the
point: the system classifies evidence, and the table decides.

## 6. System influence matrix (first pass, deliverable of #704)

| system | retain | adapt | reject | why |
|---|---|---|---|---|
| **CWN** | attributes, skills, checks, combat, trauma, Strain, hacking | — | — | the engine; `src/rules/cwn_*.py` |
| **SWN** | psionics discipline/effort shape | technique access via package | duplicate psi engines | already implemented; #572 |
| **WWN** | projects, faction procedures | — | its magic economy | selective |
| **AWN** | hazards, scarcity | crisis-zone scope | mandatory bookkeeping everywhere | situational |
| **Eclipse Phase** | stress→trauma *shape*, identity/fork questions | conditions, not a track | a second harm track | D46/D49 |
| **GUMSHOE** | core-clue principle, competency-as-competence, spends | spends → time/Strain | a separate investigative pool | this document |
| **Fate** | aspects, compels | layer B only | the 4dF kernel as a baseline | D45 |
| **PbtA** | clocks, fronts | partial success (scoped, not adopted) | moves-as-catalogue | D50 |

## 7. Open decisions (author)

- **G1** — Does an investigative rating come from CWN skills (any level > 0), or from a
  separate competency list? Current implementation assumes the former, as a dict.
- **G2** — Are spends tied to time, Strain, or both? The table in §4 is a proposal.
- **G3** — Does a case ever gate a *scene* behind an action check (chase, forced entry), and
  if so, what happens on failure — a cost, or an alternative route?
- **G4** — How many optional clues per scene before the table drowns? No number is proposed.
- **G5** — Should `obscure` be a property of the clue or of the competency? It is currently
  on the clue, which lets a case be authored without editing the skill list.

## 8. What this does not do

It does not rewrite `rulebook/`, replace any CWN check, add a pool, or change character
creation. It does not quote the GUMSHOE SRD. It does not settle the attribute reskin
(#704's other half) — that remains a separate, larger decision.
