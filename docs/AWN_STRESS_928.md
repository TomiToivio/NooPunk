# Optional AWN Stress module (#928)

**Status:** Core implementation and GameState save/load wiring; UI and advanced addiction/scar adjudication remain follow-ups. **CWN is the unchanged rules kernel.**

Reference: Kevin Crawford, *Ashes Without Number Deluxe*, printed pages 56–58 (user-supplied copy). This is an original functional implementation and short reference, not a redistribution of the book.

## Activation
The module defaults off. Set `scenario.options.awn_stress = true` to activate in the case GameState, or instantiate `AwnStress.new(true)` for manual GM use. Existing saved games without `awn_stress` are accepted; new save files persist the module snapshot. Stress is tracked separately from the existing CWN cyberware Alienation module.

## Flow
Queue one or more incidents using `GameState.queue_stress_event(id)`, then call `GameState.resolve_scene_stress(d20)` **at scene end** with the actual CWN Mental-save d20. The return dictionary indicates `stable`, `saved`, `need_choice`, `breakdown_active`, or `disabled`. After `need_choice`, a player must select either `choose_breakdown(id)` or `harden(scar_id)`. The UI should solicit this explicitly rather than auto-picking.

AWN's core event values in the module include killing (2, with an extra 1d6 for the first kill supplied as `extra`), friend mortally wounded (1), friend dies (+2), major injury (+2), witnessing atrocities (1), and privation (2 per week). A game master must explicitly confirm contextual modifiers. Custom extra points are passed via `extra` or `custom_points`, and no end-of-scene Stress is applied during an ongoing Breakdown.

Stress checks occur strictly **above** Wisdom and start at −2, with additional checks −4, −6, etc. Successful checks do not erase Stress. Dropping to Wisdom or below clears escalation and ends Breakdowns. Hardening sets Stress to zero, blocks one more Stress per scene per Hardening, and records a unique persistent scar.

Restful days recover 1 Stress. Indulgence exchanges 1 System Strain for 1 recovered Stress. Supportive discussion uses a CHA/WIS + Heal/Lead total against 9 and risks +1 Stress to the helper on failure. A fulfilled major goal removes 1d10 Stress. Those calls are explicit so the UI can show the results and the GM can authorize them.

## NoöPunk additions (not AWN canonical)
`nhi_disclosure` +1, `ontological_shock` +2, `psi_intrusion` +2, `rogue_agi_atrocity` +2, `unsa_moral_injury` +2. Values are tuning proposals. PSI and ontological-shock story flags continue to be handled separately from Stress.

## Gaps and next steps
* Connect a visible HUD/GM scene end panel and a player selection dialog.
* Finish enforcing every scar/Breakdown effect in combat and social resolution. `effects(level)` exposes structured consequences, but rules adapters do not yet apply all of them.
* Implement detailed opt-in daily/monthly addiction lifecycle and missing-indulgence handling.
* Apply special exceptions for bloodthirsty recovery, dependent friend injury, penitent taboo, and the additive exception to first-kill modifiers with full encounter semantics.
* Review UI consent controls and use grounded fictional descriptions rather than mapping these labels onto medical diagnoses.
* Execute the Godot headless test suite in a Godot-equipped environment; not executed in this environment.
