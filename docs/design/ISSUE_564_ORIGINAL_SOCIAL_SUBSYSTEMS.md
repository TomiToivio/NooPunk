# Original NoöPunk social extensions (#564, #572)

**Status: opt-in executable prototype.** Source: `src/rules/noopunk_social_extensions.py`. Test: `tests/test_noopunk_social_extensions.py`. This is not the faction turn and does not replace the accepted tabletop/Fate rules.

The current `src/rules/noopunk_extensions.py` handles heterogeneous ubiquitous links and learnable natural PSI. The present module adds two *orthogonal* subsystems not supplied by the Without Number chassis:

**Local crisis:** each neighborhood, camp, institution or polity may independently track scarcity (0..6), trust (0..6) and hazard exposure (0..6). Start at 0/3/0. After an incident, apply supply loss/recovery, collaboration/conflict and exposure/detox. No assumption of global apocalypse; absence of a crisis record means no crisis rules invoked. Use a scene's existing RPG die for contested acts and adjust these tracks *only after* its observable outcome.

**NHI contact:** measure reciprocal exchange (-6..6) separately from retained autonomy (0..6). Trade may improve exchange while imposing dependency, so a prosperous treaty can still be coercive. Avoid classifying either Orion or Confederacy as a mechanical good/evil alignment. Political and psychic negotiations belong to the story/strategic boundary, not automatic attack rolls.

Both states serialize into plain dictionaries, have deterministic updates and retain bounds. These values are **prototype defaults**, subject to later author calibration. They contain no copied book text, copyrighted factions or external services. Tests are included in the existing Python CI discovery.

## Extension boundaries

- Hacking is **ubiquitous and heterogeneous**: wired, radio, mesh and mediated connections can form real multihop routes. Reachability and authorization are distinct. Neither an air gap nor a psychic association can silently become a data link.
- Natural PSI can be **learned by humans** with aptitude and practice. The SWN-style design inspiration is a finite committed Effort pool; implementation is independently written and does not borrow SWN's protected prose or powers. Psychotronic hardware and BCI are separate mediated capabilities.
- AGI containment, Noösphere gateways, and cybernetic cognition still need additional dedicated modules and integration tests. This change does not claim the full #564 migration is completed.
