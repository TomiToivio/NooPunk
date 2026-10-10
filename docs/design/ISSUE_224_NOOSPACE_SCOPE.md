# Issue #224 — astral projection and Noöspace travel

**Status: PROVISIONAL procedure. Every number in this record is a placeholder for author
calibration.** `AGENTS.md` §4 reserves psionic mechanics; #224 asks for the *procedure*, so the
values are marked and the author owns the final form. The ontology is not mine to touch — it is
canon in `RULEBOOK.md` §40.4 (#119).

| Artifact | Role |
| --- | --- |
| `rulebook/6_PSYCHIC.md` §6.12 | the procedure, for the table |
| `src/rules/noospace_projection.py` | the executable invariants, for the tests |
| `tests/test_issue224_noospace_projection.py` | the guard |
| `rulebook/18_CROSS_DOMAIN_STATE.md` | the state machine and economy — **consumed, not restated** |
| `RULEBOOK.md` §40.4 | the Noöspace ontology (#119) — **consumed, not restated** |

## What already existed

§40.4 canonized the ontology: Noöspace **is** the Astral Plane and the Conscious Agent Network;
five regions (near / collective-unconscious / biospheric / Noöspheric / deep); navigation by
resonance rather than distance; perceptual compression; the access list; Noetic weather.
§6.4.4 had a dream/astral stub. §18 (issue #225) had the four-state machine and the shared AP
economy, and its own appendix already said *"full projection (#224) consumes that contract"*.

Missing: the procedure. Entry, depth, navigation, encounters, perception, vulnerability and
return — and the permission boundary.

## Decisions, and why

**Projection is a state, not a Skill roll.** §18 owns the four states. A projection that
"rolled well enough" to leave the body would fork the machine, and it would also break the
body rule: the state, not the roll, decides reach. The tests assert that `astral_realms()`
defers to #225 and returns exactly `{noospace}`.

**The body is present, uncontrolled and reachable — by others.** This is the design tension
that makes projection interesting rather than dominant: the projected character cannot defend
their own body, so *someone else must*, and the chapter says so in the positive ("others can
defend the body"). `check_remote_action` raises `CrossDomainError` for a Physical or Social
reach, which is the permission boundary the issue asks to test.

**Navigation consumes resonance, never distance.** §40.4.3 is explicit that near/far are human
metaphors for resonance and cognitive accessibility. A `navigation_dv` that quietly took a
distance argument would contradict canon, so a test inspects the function's source for
`distance`/`metres` and requires them absent.

**Deeper is less reliable, strictly.** §40.4.3's governing rule — "the deeper Noöspace becomes,
the less reliable human categories become" — is encoded as two strictly monotone tables
(reliability falling, uncertainty rising), asserted as strictly monotone rather than merely
sorted, so a flattening edit cannot pass.

**Information is ambiguous by default.** §40.4.1 says the experiencer is "not necessarily
inventing a private fantasy world" — which cuts both ways. So an uncorroborated perception is
`AMBIGUOUS`, and the only route to `SHARED_NOOSPACE` is corroboration by a witness **inside the
same region**. This is the same anti-shortcut rule as sensors and identity verification:
evidence with a confidence, never a verdict.

**Return is not one thing.** Voluntary return costs the Exit action; snap-back is free but
leaves a mark; severance is the worst. Aftermath uses §51's wound vocabulary, so this section
cannot smuggle in a new condition ladder.

## What this does NOT do

- No new PSI powers, no PSI point economy, no spell list.
- No region beyond §40.4.3's five; no Noetic being created here.
- No per-item psychotronic statistics (#221/#228).
- No `RULEBOOK.md` edit: it is the split root behind three generated artifacts
  (`rulebook_parts/`, `rulebook/parts/`, `docs/rulebook_segments/`), so the chapter files are
  the right home — as #222, #225 and #249 all do.
- No calibration. Every number is provisional.

## Verification

- `tests/test_issue224_noospace_projection.py` guards the module and the chapter.
- The permission boundary is proven by a raising test, not by inspection.
- Consumption of #225 is proven by patching `cross_domain_state.AP_COSTS` and requiring the
  projection side to follow it.
