# Four UN parties and Reality Tunnels (issues #469, #470)

**Status: implemented as descriptive content and a read-only Python interface, not as strategy rules.**

The 2045 default UN parliamentary layer has four starting parties: **Libertarian Accelerationist Party**, **True Humans Party**, **Unity, Security and Stability Party**, and **The Noösphere**. Additions are permitted later; four is a *starting roster*, not a global cap on political actors.

- `../../data/world/un_parties.yaml`: party names, descriptive constituencies and legacy mappings. The previous UESDP/USSP succession and Multitude/Noösphere merger questions remain explicitly unresolved. No false history was invented.
- `../data/un_political_discourse.json`: separate issue-specific positions, nodal points, articulated demands, antagonistic frontiers, internal schisms and reality-tunnel interpretations for the four parties. Claims like alleged Grey control are not narrator-verified facts.
- `../un_political_discourse.py`: read-only loader and common-event perspective view. The returned stance is pre-authored text, **not** simulated opinion change.
- `../data/global_factions.json`: the pre-existing seven *paradigm* formations remain untouched; UN parties and other actor kinds must not be conflated.

## Narrative usage

Present an event with an evidence status (observed, corroborated, contested, alleged, or unknown), then consult each party's different reading. For example the **Harvest proposal** could be framed as accession, unmanaged danger, conditional diplomacy or commercial opportunity. Preserve uncertainty about NHI motives and retain internal dissent. Signifiers such as *humanity* and *security* can be contested without automatically being *empty* signifiers.

This maps **Laclau/Mouffe** (demands, nodal points, floating signifiers, contingent hegemony) and **Robert Anton Wilson** (Reality Tunnels) to authored narrative data. The underlying LaclauGPT paper stays separate; no empirical ideology classification is imported. The 2026 ideological families supply background inspiration, not causal forecasts.

## Boundaries

The 2045 start is fixed. Background developments remain unordered **20XX** entries. Three PSI/NHI shifts remain distinct (soft/noetic, Confederacy contact, Orion conflict). PSI ability is not inferred from a creed; suspicion is not proof of hybrid identity. No new faction turns, metrics, probabilistic updates, alliances, election formulas, ideological scores, or actor capabilities have been approved by these issues.

Example from repository root:

```python
from strategy_game.un_political_discourse import interpret_event
print(interpret_event("confederacy_harvest_offer"))
```

More UN parties can be added as new entries with unique identifiers, without changing the loader or the historical paradigm-faction register.
