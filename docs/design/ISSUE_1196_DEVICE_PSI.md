# Issue #1196: device PSI accounting slice

This change implements **only item 4** of the deferred issue. It does not declare the other five items complete.

## Contract

A psychotronic implant or equipment record can confer a **temporary effect** even outside the PC's selectable Telepathy/Telekinesis disciplines. The existing `psi_access.device_grant(ability, source=equipment_id)` value records that entitlement, and `Psychic.commit_device_grant` reserves any *published, explicitly specified* Effort cost in the **same** pool as SWN psychic techniques.

The caller must supply (1) an existing `Grant`, (2) the identifiers of **currently active/equipped** devices, (3) an explicit positive Effort amount and (4) an SWN `Duration`. A grant is rejected when the equipment is inactive, a cost/duration is missing or invalid, a key is duplicated or Effort is exhausted. The standard `end_scene`, `rest` and snapshot functions still govern reservations.

This does **not** infer that all equipment uses personal Effort. Only devices whose own equipment definition explicitly charges the character's SWN Effort should call this method. Device-internal charges, battery/consumable costs and free effects belong to their existing equipment rules and should not create fake psychic Effort commitments. No technique descriptions or new prices are invented here.

```python
from src.rules.psi_access import device_grant
from src.rules.swn_psionics import Duration, Psychic

character_psi = Psychic(wisdom=14, constitution=12, disciplines={"Telepathy": 1})
grant = device_grant("medical PSI effect", source="implant-17")
# A scenario adapter validates the equipment catalogue and the currently equipped devices.
character_psi.commit_device_grant(
    "implant-17:use-1", grant,
    active_sources={"implant-17"},
    amount=1,  # illustrative only: real price MUST come from equipment definition
    duration=Duration.SCENE,
)
```

**Security and authority boundary:** a `Grant` is an entitlement token supplied by an already validated equipment definition, not player-submitted ability text. The current function only checks active-source membership; the caller remains responsible for verifying catalogue ownership, model-specific effect permissions and equipment requirements. It does not turn an effect into a selectable discipline, alter a character's class, change learned skills or provide an extra resource pool. CWN remains the action authority.

## Explicitly deferred

1. **Astral:** scripted Story scenes unless one authored scene actually needs navigable astral locations; projected actors are occupants, not astral nodes.
2. **Mutant:** no NPC mutation tables until AWN edition/source verification; mutation, PSI and ancestry remain independent.
3. **Mentalist / Spellcaster / Summoner:** no cross-system prerequisites or resource merging before the printed systems are checked.
4. **Psychic Training Focus:** keep the unavailable gate until an authorised rules reference verifies all level benefits and retrospective rules.
5. **Runtime navigation:** console/Evennia cross-view actor mapping is not implemented in this slice. Use the seven checks in `docs/tabletop/WORLD_GRAPHS_1178.md`, especially the single-sheet identity invariant.

Issue #1196 should remain **open** for these independent scopes.
