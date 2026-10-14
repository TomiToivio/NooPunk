# Four UN parties and Reality Tunnels (issues #469, #470)

**Status: implemented as descriptive content and a read-only Python interface, not as strategy rules.**

The 2045 default UN parliamentary layer has four starting parties: **Libertarian Accelerationist Party**, **True Humans Party**, **Unity, Security and Stability Party**, and **The Noösphere**. Additions are permitted later; four is a *starting roster*, not a global cap on political actors.

- `../../data/world/un_parties.yaml`: party names, descriptive constituencies and legacy mappings. The previous UESDP/USSP and Multitude/Noösphere succession questions remain explicitly unresolved. No false history was invented.
- `../data/un_political_discourse.json`: separate issue-specific positions, nodal points, articulated demands, antagonistic frontiers, internal schisms and reality-tunnel interpretations for the four parties. Claims like alleged Grey control are not narrator-verified facts.
- `../data/global_factions.json`: the pre-existing seven *paradigm* formations are untouched, and the four UN parties are now recorded **beside** them in a second register (`un_parliamentary_parties`) that reuses the same schema — stances, core signifiers, axis defaults, kind, plus a qualitative six-quantity profile. Whether the four belong in the paradigm register at all stays open (see below).
- `../data/paradigm_event_seeds.json`: each of the eleven authored seed cards now carries the four parties' readings of that one event — what each believes is happening, what it counts as evidence, whom it trusts, what it does, and how it justifies itself.
- `../un_political_discourse.py`: read-only loader and common-event perspective view. The returned stance is pre-authored text, **not** simulated opinion change.
- `../paradigm_readings.py`: read-only reader for the event surface. `readings_for("<event id>")` returns the four readings of one seed; an event nobody authored raises rather than being synthesised.

## Which file is authoritative for what

One roster, three records, stated so they cannot drift silently:

| Question | Authoritative record |
|---|---|
| Who the UN parties are, their positions and what legacy entries they amend | `data/world/un_parties.yaml` |
| Each party's paradigm stances, core signifiers and six-quantity profile | `strategy_game/data/global_factions.json` (`un_parliamentary_parties`) |
| Each party's Reality Tunnel and discourse prose | `strategy_game/data/un_political_discourse.json` |
| How a party reads a specific event seed | `strategy_game/data/paradigm_event_seeds.json` |

The stances are recorded in two files by design — the discourse record existed first and is kept consistent with the register — and the register wins where the two ever disagree. **The register question itself is not answered:** whether these four parties sit inside the paradigm register, and how the 4 / 7 / 11 counts relate, is carried as an author decision (`docs/design/AUTHOR_DECISION_QUEUE.md` rows D9 and D17).

## Two questions, kept apart

An *event* has an event-level status — **observed, corroborated, contested, alleged, unknown** — already in use in the repository. A faction's *reading* of that event has an epistemic kind of its own, and these are the five issue #469 asks for, declared once in `paradigm_event_seeds.json` as `reading_vocabulary`:

- **demonstrated in-world fact** — the reading rests on a fact the setting has established;
- **credible but incomplete evidence** — the reading argues from partial but credible evidence;
- **propaganda** — the reading is asserted for power or advantage rather than from evidence;
- **delusion** — the reading is held against the evidence, by motivated denial or by certainty the evidence does not carry;
- **open mystery** — the reading treats the matter as unresolved, as it is.

Classifying a reading is a narrative judgement, not a rule, and each classification carries its reason in the data where the judgement is contestable. No status changes, decays or resolves anything: there is no clock, probability, threshold or effect.

## The Laclauian vocabulary, applied where it earns its place

The vocabulary is defined once (`reading_vocabulary.laclau_terms`) and attached only to the cards where a specific candidate discourse carries it — the extraterrestrial economic zone (**sovereignty**), the hybrid rumour (**humanity**), the accession terms (**freedom**), the Butlerian raid (**survival**). On the other seven cards the readings are four positions on an event and the signifier is left `null` with the reason stated, because issue #469 asks for this vocabulary to be applied to specific discourses, **not hung on everything**.

Two of #469's own warnings are enforced as text rules:

- **Ambiguity alone is not sufficient for an empty signifier.** None is asserted anywhere on this surface. The design record names one candidate — the True Humans' *humanity*, which holds only while the alliance's three legs disagree about the enemy — and it is left in the author-gated field of `global_factions.json` for Tomi to confirm or drop.
- **Difference is not an enemy frontier.** Each card states what must *not* be turned into an antagonistic frontier, and the two physical NHI blocs are never merged into one pro/anti-alien axis. Where two factions simply disagree about evidence or interest, the record says so.

## Narrative usage

Present an event with an evidence status (observed, corroborated, contested, alleged, or unknown), then consult each party's different reading. For example the **Harvest proposal** could be framed as accession, unmanaged danger, conditional diplomacy or commercial opportunity. Preserve uncertainty about NHI motives and retain internal dissent. Signifiers such as *humanity* and *security* can be contested without automatically being *empty* signifiers.

This maps **Laclau/Mouffe** (demands, nodal points, floating signifiers, contingent hegemony) and **Robert Anton Wilson** (Reality Tunnels) to authored narrative data. The underlying LaclauGPT paper stays separate; no empirical ideology classification is imported. The 2026 ideological families supply background inspiration, not causal forecasts.

## Author-gated

Everything below is a question for Tomi, deliberately left unset — no magnitude, value or mechanic was invented to fill it:

- **The succession question.** Is the Unity, Security and Stability Party a renaming of the United Earth Social Democratic Party, a recharacterisation of it, an evolution of it, or a different party in the legacy slot? The centre-left legacy record and the authoritarian-conservative description are left in visible tension (`data/world/un_parties.yaml`, `position_status`). Is The Noösphere the Multitude renamed and re-topped by the reformed CCP, or a successor coalition?
- **The register question.** Are the four UN parties inside the paradigm register or a register of their own (`AUTHOR_DECISION_QUEUE.md` D9, D17)? No count is asserted anywhere.
- **Magnitudes.** Which of the six quantities each party holds is recorded qualitatively; how much of each it starts with, and what moves one, is not set. There is no scalar "influence" (docs/design/NOOPUNK_GLOBAL.md section 7).
- **Effects.** A reading carries no difficulty, cost, rate, cap, clock or effect. Issue #469's rule stands: no new mechanic is locked without the author's approval.
- **The roster's size.** `open_for_future_parties: true` remains true and no list length is set.

## Boundaries

The 2045 start is fixed. Background developments remain unordered **20XX** entries. Three PSI/NHI shifts remain distinct (soft/noetic, Confederacy contact, Orion conflict). PSI ability is not inferred from a creed; suspicion is not proof of hybrid identity. No new faction turns, metrics, probabilistic updates, alliances, election formulas, ideological scores, or actor capabilities have been approved by these issues. `strategy_game/RULEBOOK.md` still says no rules are approved.

Example from repository root:

```python
from strategy_game.paradigm_readings import readings_for
for reading in readings_for("alien-economic-zone"):
    print(reading.faction, "|", reading.epistemic_status, "|", reading.reads)
```

More UN parties can be added as new entries with unique identifiers, without changing the loaders or the historical paradigm-faction register.
