# The controller / proposal boundary (issue #304, step 1)

**Status: structure only. No rule, canon, mechanic, number or card is decided here.**
`strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**, and the rule-authoring gates in
[`RULE_SYSTEM_RESEARCH.md`](RULE_SYSTEM_RESEARCH.md) remain open.

This note records what was implemented, why the boundary has the shape it has, and what was
deliberately left to the author. It is a design record, not a contract; the executable contracts are
in `strategy_game/tests/test_agent_boundary.py` (per `AGENTS.md` / #271, tests cover code, never
prose).

## What landed

`strategy_game/controllers/` — a stdlib-only subpackage implementing step 1 of the sequenced plan in
the design comment on #304. It is the *proposal-side* structure of the turn architecture:

| Piece | What it is | What it is not |
| --- | --- | --- |
| `MoveProposal` | A controller's declaration for one leader: identity, a **required** `leader_id`, an **open-string** `action_code`, a declared target, declared resource *names*, free-text rationale, provenance defaulting to `UNKNOWN` | No result, no numbers, no action set |
| `ProposalRecorder` / `ProposalLog` | Stores proposals **as data only**, after an authorisation check | It never applies one; it is never given a `WorldState`/`TableState` at all |
| `Controller` protocol | The *behavioural* boundary behind the signature-only `ports.AgentProvider` seam | Not a rule; not an adapter |
| `ControllerRegistry` | Which controller commands which leader; **at most one authoritative controller per leader**, enforced | A boundary map, not a rulebook |
| `NullAgentProvider` | The default: proposes nothing, commands nothing, needs no model | — |
| `ScriptedAgentProvider` | Deterministic, RNG-free, model-free controller over a fixed script | Not an AI, not a policy |
| `controller_from_adapter` | The **capability-gated** optional-loading seam: absent → `None` (game stays complete), present → explicitly refused | It never hard-imports ollama/concordia |

`python -m strategy_game.controllers` prints a deterministic, model-free demonstration: one
illustrative scripted controller declares one move per leader, the recorder stores them, the log
replays exactly, and the authoritative world state is shown before and after to be unchanged.

### Why this name, and not `agents/` or `session.py`

* `strategy_game/agents.py` **already exists** — it is issue #303's agent/card ontology reader, so a
  package named `agents/` would collide with it.
* The design comment on #304 warns that adding a second set of names for concepts the scaffold
  already owns (`Controller` over `AgentRunner`, `SessionState` over `WorldState`) is how a
  *competing state engine* starts. `controllers/` names the new thing (a controller) without minting
  a rival `SessionState`, so no second session/state type exists.

Following the `tabletop/` precedent, this subpackage has its own `__init__` and `__main__`:
`strategy_game.__all__` and the CI-pinned key set of `python -m strategy_game` are **untouched**.

## How "a proposal cannot mutate authoritative state" is proven

Not by promise — by construction, checked in code:

1. `ProposalRecorder.record(self, proposal)` **takes no world or table state**. It has no handle to
   mutate, and the test asserts the signature, so a later change that adds one fails a test.
2. The recorder's only mutable state is its own `ProposalLog`.
3. The test snapshots `WorldState.to_json()` and `TableState.to_json()` before and after recording
   and asserts they are byte-identical — **including in a subprocess where `ollama` and `concordia`
   are made unimportable**, so the guarantee holds with no model provider present.
4. Replay reads the stored declarations and imports nothing optional (`sys.modules` is asserted).

This is the shape Willison's dual-LLM pattern calls the one safe crossing: a proposal is a
*validated, structured* output, whereas a narrated scene is untrusted text that may be stored as
`GENERATED` content but can never be read back as a transition.

## Left to the author — recorded, not invented

These appear in code as `strategy_game.controllers.proposals.PENDING_AUTHOR_RULINGS`:

* **The approved action set.** `action_code` stays an open string; `APPROVED_ACTION_CODES` is
  declared *empty*, so "nothing approved yet" is a visible value rather than a guessed default verb.
* **The resolution core.** No `ResolvedMove`, no threshold, no success/failure. Resolution is the
  deterministic engine's job; this unit implements none of it.
* **The Game Master's closed menu of intervention types.** No `GMIntervention` record is invented.
* **Hidden-information rules** (what a controller may read, and when). Needed at a physical table
  too — it is a state-visibility rule, not a networking problem.
* **Online multiplayer transport.** An offline open-source game may not assume a server (VISION §5,
  §7). Hotseat / pass-the-save-file is the transport-free form and needs nothing here.
* **The NoöPunk Tarot deck's meaning, composition and any mechanical effect** — reserved by #304.

Also untouched: the `politics.py` vs `political.py` fork and the 4/7/11 global-roster discrepancy.
Both are author rulings, and this layer was kept clear of them.
