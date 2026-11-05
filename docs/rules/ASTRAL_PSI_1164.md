# Astral graph and PSI permissions (#1164)

> **Deferred by [#1178](https://github.com/TomiToivio/NooPunk/issues/1178) (2026-11-05).**
> Astral Projection is scripted (sleeping OOBE, NDE, Monroe-style technology); the Astral Graph is
> not part of the current four-graph slice. This module remains a **prototype**, not runtime
> authority, and must not be wired into play until the Astral work is separately approved.

**Status: deferred prototype — issue #1164 remains open.**
This is the Astral/PSI add-on proposed in
[`docs/design/DRAFT_GRAPH_SCENES_1164.md`](../design/DRAFT_GRAPH_SCENES_1164.md) §7 and
[`docs/design/DRAFT_NOOPUNK_PSIONICS.md`](../design/DRAFT_NOOPUNK_PSIONICS.md). It does **not**
change CWN, SWN, WWN or AWN rules, and it does not add tabletop rulebook text.

## What was implemented

| Concern | Module | Contract |
| --- | --- | --- |
| Verb × Target permission | `src/rules/astral.py` → `PSI_MATRIX`, `permission()`, `authorize()` | Every cell exists; unspecified combinations are **DENIED**; `scripted` cells are never player actions |
| One-payer activation | `activate()` | Delegates the single Effort commitment to `src/rules/swn_psionics.Psychic`; no second resource pool |
| Projection state | `AstralState` | `embodied → overlay → projected → returned`, with a required physical anchor and named realm |
| Link strain | `AstralState.tick_scene()`, `strain()` | Three filled boxes mean “a scene of finding the way back”, not death |
| Astral graph | `AstralGraph`, `AstralNode`, `AstralEdge` | Fail-closed visibility (`gm_secret` needs both an act gate and a discovery record), explicit gates, no dangling edges |
| Clue boundary | `PsiAction.grants_investigation_clue` | Constant `False`; the module has no investigation import |

## Use

```python
from src.rules.astral import AstralState, PsiTarget, PsiVerb, authorize
from src.rules.swn_psionics import Psychic

psychic = Psychic(wisdom=14, constitution=10, disciplines={"Metapsionics": 1})
state = AstralState()
state.project(anchor="physical:kurvi-home", realm="astral:kurvi", psychic=psychic)

action = authorize(PsiVerb.PERCEIVE, PsiTarget.ASTRAL, state=state, unlocked=True)
assert action.permitted
```

`authorize()` answers only the permission question. The caller still supplies the CWN check,
range, duration, resistance and consequences. `activate()` commits one Effort for the action and
returns a denied `PsiAction` if the pool or the technique gate refuses it.

## Invariants the tests enforce

1. The matrix is complete (8 verbs × 7 targets = 56 cells), and no cell grants a clue.
2. `MANIFEST/PERSON` and other omitted cells are denied; `IMPRINT/MATTER` is scripted, not active.
3. An active cell still needs `unlocked=True`; astral targets need a projected/manifesting state;
   person-to-person contact needs consent.
4. Projection requires an anchor and a realm, commits exactly one Effort, and leaves the body
   anchor intact.
5. Three link boxes are a lost return, not death; state snapshots round-trip.
6. A `gm_secret` node is invisible until the act gate **and** discovery both open; travel is only
   to a visible, adjacent node with its gate open.
7. `src/rules/astral.py` does not import `src/rules.investigation`.

Run `python3.11 -m unittest tests.test_astral_1164`.

## Deliberately not implemented

- The full five-family graph registry, Markdown/YAML loader, NetworkX projection and scene
  transitions. This slice is the Astral layer only.
- The tabletop wording, a full SWN technique catalogue, WWN ritual integration, psychotronic
  device profiles and density-specific combat procedures.
- Any change to `design/graphs/README.md`, `design/graphs/RULES.md` or the canonical timeline.

The matrix, the `Metapsionics` default discipline and the effort cost are **proposals** in the
draft; Tomi's author decision is still required before they become tabletop canon.
