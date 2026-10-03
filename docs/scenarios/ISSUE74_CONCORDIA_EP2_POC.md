# Issue #74: Concordia + Eclipse Phase proof of concept

This is the deliberately small experiment requested in issue #74.

## What it is

The prototype uses the existing NoöPunk stack rather than creating a parallel game:

- the text RPG loop in `text_game`;
- the EP2-derived deterministic rules kernel already introduced by issue #60;
- the existing Concordia-compatible Ollama controller for important conversational NPCs;
- an ordinary scripted NPC in the same room to test mixed agent types;
- explicit world state and event resolution in Python.

The scenario is set in **20XX**, in the current alternate pre-Fall Eclipse Phase continuity. It uses only already-recorded NoöPunk lore. Generic roles such as “contact analyst” and “archive technician” are interface roles, not new factions or hidden setting canon.

## Mission

You are in a single contact-analysis room on Earth.

Your task is to authenticate and take custody of the **SETI signal record** that counts as the seventh detected extraterrestrial civilization. The room also contains the unresolved classification dossier concerning Noetics, Plasmoids, and Constructs.

This intentionally exercises only a thin vertical slice:

- investigation with `Perceive`;
- technical / mesh-style work with `Interface`;
- social resolution with `Persuade`;
- optional LLM conversation and natural-language intent parsing;
- ordinary scripted NPC dialogue;
- deterministic EP2-derived dice resolution;
- item/world-state change and scenario completion.

Combat remains available through the shared engine, but the scenario does not force a fight. Psionics are deliberately **not** invented here. The point of #74 is to discover which mechanics are worth keeping before adding another subsystem.

## Run without an LLM

```bash
python scripts/noopunk_text.py --scenario issue74
```

This path is fully playable with deterministic mechanics and scripted dialogue.

Useful commands:

```text
look
sheet
talk technician hello
test skill Perceive roll 40
test skill Interface roll 40
test social Persuade vs analyst roll 20
take signal-record
inventory
```

## Run with Concordia/Ollama

Install the pinned Concordia dependency and run Ollama as documented by the project, then:

```bash
python scripts/noopunk_text.py --scenario issue74 --ollama --llm-gm
```

In this mode the **contact analyst** is controlled through the existing Concordia-compatible language-model adapter. Free-form player intent can also fall back to the LLM intent translator when it is not already a valid command. Dice, targets, modifiers, harm, inventory, and completion remain deterministic code-owned state.

## Example playthrough

A minimal deterministic run can look like:

```text
> look
Earth / Contact Analysis Room ...

> test skill Perceive roll 40
skill: success ...

> test skill Interface roll 40
skill: success ...

> talk technician Is the signal authentic?
The signal record is genuine archive material ...

> test social Persuade vs analyst roll 20
social: ...

> take signal-record
Taken: SETI signal record.
Scenario objective completed.
```

The exact opposed-test winner may vary unless both sides' rolls are pinned through the lower-level test helpers. The key invariant is that the rules kernel, not the LLM, resolves the contest.

## What this prototype teaches us

### Mechanics that fit well

- **Percentile skill checks** map cleanly to deterministic code and are easy for an LLM to request without letting it invent outcomes.
- **Explicit character sheets and pools** are inspectable and serializable.
- **Social, technical, and combat checks** can share one resolution seam.
- **LLM NPCs and simpler NPCs can coexist** because both emit actions into the same engine.
- **Natural-language input belongs above the rules layer**. The LLM may translate intent, but code owns legality and state changes.

### Mechanics that already look heavy for NoöPunk

- Full EP2 catalogs, morph detail, equipment economics, augmentation bookkeeping, and exhaustive subsystems would add a lot of state before the simulation proves it needs them.
- Pool complexity should remain under observation. If agents do not use multiple pools intelligently, simplify them.
- Opposed checks are useful, but their consequences should stay explicit rather than being improvised by narration.

### What should stay deterministic

Keep these in code:

- legal actions;
- character statistics;
- dice;
- modifiers;
- opposed-test resolution;
- harm/stress state;
- inventory and world-state mutations;
- scenario completion.

Use LLMs for:

- dialogue;
- intent translation;
- interpretation of already-resolved facts;
- high-level NPC choice among legal actions;
- brief narration.

That split is the strongest result of the experiment. Concordia works best as the **agency and narrative layer around a deterministic RPG kernel**, not as the rules engine itself.

## Licensing

No Eclipse Phase rules prose is copied here. The prototype calls the repository's existing EP2-derived homebrew code and follows the licensing/provenance boundary already documented under `docs/sources/` and `docs/licenses/`.

Eclipse Phase is created by Posthuman Studios. EP-derived material in this repository remains subject to the applicable Creative Commons attribution, noncommercial, and ShareAlike requirements already recorded by the project.
