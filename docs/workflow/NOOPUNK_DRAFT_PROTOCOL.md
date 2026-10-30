# The draft protocol (#814)

#814 is a **permanent meta-issue**: Tomi writes a draft for one manageable section or scenario, agents
implement it in two synchronized forms — the tabletop rulebook and the Godot computer RPG. This file
is the operating procedure for that cycle. It does not replace the issue; it makes the cycle
predictable.

**Tomi is the authorial source of truth.** Agents may raise ambiguities, trade-offs and conflicts
with the existing rules. Agents may **not** silently substitute their own design. If the draft is
silent on something the implementation needs, that is a question, not a licence.

## Where each thing lives

| the draft says… | the tabletop deliverable | the Godot deliverable |
| --- | --- | --- |
| a rule, procedure or number | `rulebook/` chapter (see `rulebook/README.md` for the map) | kernel under `godot/core/`, numbers in `data/rules/*.json` |
| a character option (background, edge, focus, skill) | the character-creation chapter | `godot/core/cwn_character.gd` + the option data |
| a scenario, mission or case | `scenarios/` or `rulebook/` scenario chapter | `godot/scenarios/<id>/` bundle + scene |
| a setting fact, faction, place | `rulebook/` setting chapter | only if it is load-bearing for a mechanic |

Three homes, one rule: a mechanic that both runtimes use lives **once**. `godot/core/` is the engine's
single rules tree (AGENTS.md §16); the tabletop chapter is the human-readable statement of the same
procedure, not a second implementation.

## The cycle

1. **Intake.** Tomi opens a child issue with the draft attached or quoted, and says which section it
   covers. If the scope is not one section, ask before starting. Paste the draft verbatim into the
   issue; never summarise it away.
2. **Read back.** Restate the draft as a list of decisions the implementation must honour, and list
   every ambiguity with the option each reading would imply. Post this on the child issue **before**
   writing code or prose. Wait for answers only on decisions that change behaviour; proceed on the
   rest and record the reading taken.
3. **Tabletop first** (AGENTS.md §14). Write the chapter or scenario text: procedure, example, edge
   cases, cross-references to the CWN/SWN baseline it modifies. Playable without software.
4. **Digital specification.** Numbers into `data/rules/*.json`, in the same shape the Python layer of
   record (`src/rules/`) uses. The JSON is the contract; both runtimes read it.
5. **Godot implementation.** One kernel in `godot/core/`, wired to its call sites, with the sheet or
   scene data it needs. No second copy, no parallel tree (AGENTS.md §16).
6. **Parity tests.** A behavioural test on each side of the contract:
   - Python: the rules module behaves as the JSON says (`tests/test_*_contract.py`).
   - Godot: the kernel behaves as the JSON says (`tests/godot/test_*.gd` or `godot/tests/test_*.gd`).
   - Tabletop↔Godot: the same worked example, with the same inputs and the same expected result, in
     both a rulebook example and a test. This is the only thing that catches "the book says one thing
     and the game does another".
7. **Ledger.** Record on the child issue: what was implemented, what was deliberately not, every
   departure from the draft with its reason, and the open questions for Tomi. Then PR with
   `Refs #<meta>` and `Closes #<child>` — never `Closes #814`.

## Definition of done, per child task

- [ ] The draft and its scope are linked from the child issue.
- [ ] Tabletop text updated, with CWN/SWN baseline references where the draft modifies upstream.
- [ ] Godot updated where the draft touches the computer RPG, in the single canonical tree.
- [ ] Contracts and tests: JSON ↔ Python ↔ Godot, plus the shared worked example.
- [ ] Departures and unresolved questions listed for Tomi's decision.
- [ ] PR reviewed and merged; the child issue closed and linked here.

## Non-negotiables inherited from the repo

- Upstream CWN/SWN material is used as mechanics and shape only; no reproduction of non-open text
  (see `docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md`).
- Keep one `project.godot`, one root title screen, one rules tree.
- Working paths are retired only after their call sites move; a passing suite in one tree is not
  evidence about another (AGENTS.md §16, #791).
- The meta-issue is never auto-closed, including through PR keywords.

## Current state this protocol builds on

- The mechanical floor is in place: CWN creation, combat (Shock, Trauma), Strain, injury, healing,
  hacking; SWN Effort, Torching, discipline ranks, technique picks.
- The protagonist is a **created level-1 field agent**, bridged to the session's sheet shape by
  `CwnCharacter.to_session_sheet()`; the party is 1–4 (`godot/core/party.gd`); Romppainen is a senior
  companion.
- Open decisions waiting on Tomi: the level-1 hit-point base (see
  `docs/godot/NOOPUNK_RULES_CUSTOMIZATION.md`), the NoöPunk background/edge/focus list, and the
  technique catalogue's canonical status.
