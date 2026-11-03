# Psychic powers must not shortcut an investigation (#1105)

#1105 asks for one demonstration in particular:

> Demonstrate a human UNSA investigator interacting with a psychic informant and an NHI psychic without turning
> routine investigations into automatic mind-control shortcuts.

This document records how that boundary is held, and the test that holds it:
`tests/test_1105_psi_investigation_boundary.py`.

## The boundary

Two systems touch the same fiction and must never touch each other in code:

| System | Module | What it decides |
|---|---|---|
| Investigation (CWN) | `src/rules/investigation.py` | Which clues a competent investigator gets, and whether a scene can be left |
| Psionics (SWN shape) | `src/rules/swn_psionics.py`, `src/rules/psionics.py` | What Effort a psychic spends and what a technique costs |

The investigation resolver grants clues for **competence plus declared access and inquiry, with no roll**.
Adding a psychic input to it would make a psychic character an oracle, and every case would stop being a case.

## Three guarantees, three places to break them

1. **The signature.** `discover()` takes a case, a scene, an investigator, and declarations of access and
   inquiry. It has no psi, psychic, effort, technique or discipline parameter. The test fails if one appears.
2. **The import graph.** `investigation.py` does not import psionics, and neither psionics module imports
   investigation. Both directions are checked by AST, because a lazy import inside a function would slip past
   a grep of the module header.
3. **The behaviour.** On the scenario below, a psychic with no investigative skills discovers exactly what an
   unqualified bystander discovers — nothing. A psychic standing next to a mundane agent does not change that
   agent's result at all.

All three were proven to fail when broken: adding `psychic: bool = False` to `discover()` turns the test red.

## The scenario

`the_informant_and_the_visitor` — original NoöPunk fiction, no SWN text.

| Scene | Core clue | Gate |
|---|---|---|
| `clinic` | The appointment ledger shows one visitor under two names | `Administer` |
| `ward` | The drip counter was reset by hand after the last round | `Forensics` + access `ward` + inquiry `search` |
| `interview` | The informant says the visitor was "already knowing what I was going to say" | `Empathy` + declared `interview` |
| `bunker` | A rack of psychotronic helmets, warm, tagged with a field-office code | `Science` + access `bunker` + inquiry `search` |

A mundane UNSA field agent walks `clinic → ward → interview → bunker` and the case closes. The test asserts
exactly that path, in that order, with nothing but competence and declared procedure.

The informant is a **scene with a gated clue**, not a mind to be read. She yields her fact because the author
put it there and the investigator declared an interview — not because anyone is psychic. That is the distinction
#1105 is protecting: the psychic informant is a source of *evidence*, and evidence still has to be obtained the
way evidence is obtained.

## What this does not claim

- It does not claim psychic powers are useless in an investigation. A psychic can act, protect, misdirect or
  fail dramatically; the boundary is that psi does not **grant clues** and does not **open exits**.
- It does not model the NHI psychic at all. The bunker scene is an ordinary scene about a person who has been
  in contact with something; making it exempt from investigation rules would be the very shortcut this
  forbids.
- It is not a rules-fidelity claim about SWN. Nothing in this scenario is SWN's text, and per
  `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md` it must not be.

## Running it

```sh
python3 -m pytest tests/test_1105_psi_investigation_boundary.py -q     # or:
python3 -m unittest discover -s tests -p 'test_1105_psi_investigation_boundary.py'
```

Both collect the same 11 tests. The second is what CI runs — a bare `def test_*()` here would be invisible to it.
