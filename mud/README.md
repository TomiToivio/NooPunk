# NoöPunk MUD

> **New authority #950:** This is the **primary NoöPunk game**. Implement CWN first, then a self-contained UNSA solo campaign, before optional multiplayer/LLM/Mesa and other factions. The existing paragraphs describing an equal-priority sandbox are historical. See [CWN Deluxe audit](../docs/design/ISSUE_950_CWN_DELUXE_AUDIT.md).

The first original solo case can be played via `case status`, `case accept` at UNSA safehouse, `case interview` at Kurvi, `case records` at University of Helsinki, then `case report` and `case submit` at UNSA safehouse. The case state persists on the player character; this is a **prologue**, not a complete campaign. The linked Python unit test exercises it without LLM/Evennia. Use `checkattr <attribute>` to set the attribute for skill checks, then `check <skill>=<difficulty>`.

A **separate, text-based, persistent multiplayer** game built on [Evennia](https://www.evennia.com/), sharing
NoöPunk canon and CWN rules with the Godot game but **no runtime**.

**Status: MAIN GAME (#950) — first implementation scaffold added in PR #948.** Per #950 this directory is the
primary playable implementation and the default target for coding agents; the Godot project is
secondary/legacy. Evennia runtime and multiplayer behaviour are **not yet verified** — the phase-1 build order
below is the work queue, not a description of finished code.

## The boundary, in one table

| | NoöPunk MUD (this directory) — **primary** | NoöPunk Godot — **secondary/legacy** |
|---|---|---|
| Runtime | Python 3, Evennia server | Godot 4, `project.godot` at repository root |
| Interface | text commands, telnet/web client | graphical, `scenes/`, `godot/` |
| Tests | Python pytest under `mud/tests/` | `godot --headless --script res://godot/tests/run_tests.gd` |
| Entry point | `mud/server/` (Evennia layout) | `project.godot` |
| Dependencies | `mud/requirements.txt` | Godot binary, no Python runtime |

## What is shared

Canon, scenario data, CWN mechanics **as specifications**, and platform-neutral schemas. Shared inputs are
read, not forked: if a rule changes, it changes once and both games follow.

## What is never shared

Runtime assumptions, UI code, scene files, and release automation. A MUD change must not be able to alter
Godot behaviour, and a Godot change must not be able to alter the MUD's.

## Rules of engagement for agents

1. **Identify the target game before editing.** MUD work stays under `mud/`; Godot work stays under
   `godot/`, `scenes/` and the root `project.godot`.
2. **No cross-imports.** `mud/` must not reference `res://`, `.gd`, `.tscn`; Godot code must not import
   `mud.*`. `tests/test_mud_godot_boundary.py` enforces this.
3. **CWN is not forked.** Noösphere, ideology, social ties and ontological shock are modules layered on the
   CWN baseline, never edits to it.

## Phase 1 — offline single-player UNSA campaign (#950)

The first target is a **complete playable solo game with no multiplayer, no LLM and no external API**: create a
UNSA Academy graduate in Helsinki, take the first assignment, play several scenes, investigate, resolve
skill/combat/hacking checks, complete the quest, live with the consequences, save and resume.

Build order:

1. Evennia project skeleton under `mud/` with its own requirements and a smoke test that the server starts
   headless — nothing about game content yet.
2. CWN character bridge reading `data/rules/` without copying it.
3. Deterministic scripted GM: scenes, triggers, clue progression, adjudication, endings — all headless.
4. Investigation, travel, inventory, combat, hacking, progression, persistence.
5. GUMSHOE investigative overlay, PbtA Noösphere/Psyche/ontological shock, LaclauGPT ideology/reputation —
   modular, never replacements for the CWN baseline.

Phase 2 (multiplayer, LLM agents/GMs, Mesa population simulation) starts only after phase 1 is playable
without any of it.

### Scaffold follow-ups (PR #948)

1. Run and smoke-test the Evennia server in a Python environment; correct any Evennia version-specific integration issues.
2. Expand CWN conformance using shared `data/rules/` without forking rules.
3. Implement a real, optional LLM provider behind the validated intent boundary.
4. Persist/reconcile Mesa social simulation through authoritative game-world handlers.
5. Add multiplayer end-to-end coverage and server-restart persistence tests.

The ordering above is unchanged: the deterministic headless GM comes before any LLM provider, and
multiplayer coverage comes after the solo campaign is playable.

## Implementation scaffold and commands

## Quick start

Requires Python 3.12+ and a compatible Evennia release.

```sh
cd mud
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
evennia migrate
evennia start
```

Use Evennia's browser client at http://localhost:4001 or a telnet client at localhost:4000. Create two separate accounts to test concurrent presence. **Not validated on a running Evennia server in this PR.** Evennia owns durable character/room state; the game setup hook seeds three connected Helsinki rooms once.

Commands: `look`, `say`, `north` / `south` / exits, `sheet`, `check <skill>=<difficulty>`, `supplies`, `scavenge`, `unsa`, `faction`, `talk <npc>`. Standard Evennia multiplayer communication and connection commands remain available.

## Architecture contract

- `server/`, `commands/`, `typeclasses/`, `world/`: **Evennia only**; persists authoritative rooms, characters and faction inventory.
- `systems/cwn.py`: a **small verified CWN skill-check slice** (2d6 + skill + attribute modifier against difficulty), not a complete CWN implementation. CWN's remaining character creation, combat, hacking, equipment and progression are future work.
- `systems/agents.py`: bounded, provider-neutral Concordia-*style* narration and validated intents; no dependence on Concordia internals and no LLM controlling player characters.
- `systems/simulation.py`: optional Mesa resource agents, emitting proposals only. World mutations must be applied separately by validated Evennia code.
- `world/seed.py`: starter Helsinki, UNSA safehouse and NPC. The Noösphere / ideology system is deferred as an optional overlay.

**Authority:** Never treat LLM prose or Mesa events as CWN rolls or inventory mutations. Players choose actions. The MUD and Godot share **specification and canon**, not runtime classes. MUD agents must read `mud/AGENTS.md` before changing code.

## Current scope

This PR provides an isolated playable-text vertical-slice scaffold and unit-tested pure mechanics/contracts. Survival, GM, NPC and Mesa integration are intentionally minimal, not a claim of full #946 acceptance. The first faction is UNSA; rogue factions and player-founded organizations come later.

## Platform-neutral core (PR #949)

This is an additional, engine-independent layer intended for eventual integration with the Evennia scaffold above. Read [`docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md`](../docs/design/ADR_946_NOPUNK_MUD_BOUNDARY.md) for the architecture decision. Neither MUD layer imports Godot runtime code.

## Run the core

The platform-neutral core runs today, without Evennia or Mesa installed:

```bash
cd mud
python -m pytest tests -q
```

## What exists

| Module | Responsibility |
|---|---|
| `nopunk_mud/rules_contract.py` | the shared CWN facts (difficulties, untrained modifier, bounds) and the `RulesEngine` protocol the host implements |
| `nopunk_mud/world_state.py` | the authoritative world: rooms, characters, resources, UNSA faction, validated events, JSON persistence and an event log |
| `nopunk_mud/llm_gateway.py` | agents return **proposals**; forbidden intents are refused; a deterministic fallback runs with no provider |
| `nopunk_mud/sim_bridge.py` | simulations emit `SimEvent`s; `reconcile()` applies them as clamped world events |

## Integration work still required

The separate Evennia command-and-room scaffold exists under `mud/server/`, `mud/commands/`, `mud/typeclasses/` and `mud/world/` (PR #948), but has **not been smoke-tested on a live Evennia server**. The platform-neutral `nopunk_mud` core added here is not yet wired to those Evennia handlers. Provider-backed Concordia-style GM/NPCs, an authoritative Mesa reconciliation loop and multiplayer integration tests remain future work. Do not claim the two layers are already connected.

## Play the solo case (#950)

```bash
cd mud
python -m nopunk_mud.cli --campaign
```

A deterministic, single-player UNSA case: four places, two colleagues, one fight, three endings. No LLM, no
Mesa, no Evennia, no other players, no network. A scripted run for CI:

```bash
python -m nopunk_mud.cli --campaign --script "go street,go university,examine terminal,go street,go kurvi,talk witness,ask witness badge,examine woman,go street,go safehouse,report"
```

The engine (`nopunk_mud/campaign/`) owns the state and validates every command; the content
(`nopunk_mud/campaign/content.py`) is data. Core clues are never behind a roll — the case cannot stop because
of a die — and optional clues cost a check.

## Evennia solo case bridge (#950)

The `solo <command>` command runs the headless `nopunk_mud.campaign.CampaignEngine` inside an Evennia character session. For example: `solo look`, `solo go street`, `solo go university`, `solo examine terminal`, `solo status`. The player character's `db.unsa_solo_state` stores the saved case after every command, including between logins and server restarts when Evennia database persistence is configured. `solo save` is intentionally disabled because arbitrary server-file writes from player input are unsafe. Invalid saves are preserved for inspection rather than overwritten.

The solo case is a self-contained story instance: its room, inventory and combat states do not yet interact with the shared Evennia world. The preexisting `case` command is a separate earlier prologue, not an alias for `solo`. Evennia boot and cross-restart behavior require an actual server test; the bridge has a headless mocked-command test, not a verified running-server smoke test. No new tabletop mechanics are introduced by this adapter.

Server-side test (skips without Evennia):

```bash
python -m django test tests.test_evennia_layer_966 --settings=server.conf.settings
```
