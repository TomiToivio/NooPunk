# PR #594 integration: crisis and NHI diplomacy (#572, #564)

**Conflict-resolution note.** PR #594 and the merged #593 both introduced
`src/rules/noopunk_extensions.py` and `tests/test_noopunk_extensions.py`.
Their parallel network and PSI implementations had incompatible APIs. This
merge **preserves main's working contracts and tests** (and the later
`src/rules/ubiquitous_network.py` and `src/rules/natural_psi.py` owners)
instead of silently installing a second engine. The genuinely additional
prototype features are now isolated in
`src/rules/noopunk_crisis_contact.py` and
`tests/test_noopunk_crisis_contact.py`.

## Optional local crisis procedure

Record each locality independently with scarcity, trust and exposure. A
supply disruption changes scarcity, cooperation modifies trust and risky
events change exposure. This does not presuppose nationwide collapse.
These small bounded counters are provisional scenario aids, not an
approved replacement for AWN or for faction economics.

## NHI contact procedure

Record reciprocity (mutual exchange, including a negative balance) and
autonomy (ability to resist external control) separately. A productive
exchange can increase reciprocity while reducing autonomy. Neither the
Confederacy nor Orion is assigned a permanent moral alignment. This
is a provisional model, not a faction-turn integration.

## Existing, preserved mechanics

Ubiquitous network hacking continues to require a concrete route and
separate authorization; disconnected machines are not magically online.
Natural human PSI remains trainable, with existing module-specific
Effort commitments. Actual contested actions still use the owning
1d10 or Fate resolver; SWN is a comparative influence, not copied text.

## Validation

`python -m unittest tests.test_noopunk_extensions tests.test_noopunk_crisis_contact -v`
is run by regular test discovery in CI. Full scene/character integration
remains work for #572 and #564.
