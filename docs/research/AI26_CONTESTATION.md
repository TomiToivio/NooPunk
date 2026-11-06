# Paired AI26 contestation experiment

Run from the repository root with Python 3.11+. The default fixture uses two invented claims about who should control AI. All people, affiliations and organizations are synthetic.

    python -m src.simulation.ai26_experiment > experiment.json
    python -m unittest discover -s tests -p test_ai26_contestation.py -v

For reviewed imports, put the upstream LaclauGPT-Data-Analysis package on the Python path and install its dependencies. Pass one canonical JSON file and two researcher-selected relation IDs with --canonical FILE --relation ID1 ID2. The researcher must justify treating these relations as competing projects. Outputs include evidence quotations, provenance and reviewer details. Keep empirical output in the research environment and choose a fresh output filename.

| Origin | Source and use |
|---|---|
| Observed | The canonical evidence ID, source URL and quotation or source reference anchor an interpretation. |
| Inferred | Reviewed relations and discourse-object endpoints preserve their IDs, uncertainty, confidence and review status. A frontier or collective subject retains its upstream interpretation. |
| Synthesized | The default fixture supplies two claim IDs. In both modes the alternating organizations, membership roster and initial assignments are assumptions. |
| Simulated | A canonical system Event records each directed outreach and affiliation change. Each snapshot gives the member-to-organization edges and the communication event for that turn. |

The adapter reuses CanonicalRecord.model_validate from canonical.py (schema 1.2.0). It accepts only explicit analysis.relations between supported discourse objects. Chains, the Formula of Populism, and antagonisms have separate upstream representations. They require separate research designs. Abstentions, dangling evidence and unapproved relations prevent a run. The projection includes source context for audit. No author identity becomes an actor.

## Behavioral assumptions and interpretation

Each institution has capacity for one contact every other turn. Members begin evenly divided (the first organization receives the extra member for odd populations). On receipt of a competing claim a member switches affiliations with probability p. This assumes institutional outreach can induce immediate realignment. The same random contacts and draws are used across probabilities for each seed. A probability of zero provides the control. The CLI compares 0, 0.25 and 0.75 across seeds 1, 2 and 3 by default. These values are uncalibrated.

Reach is the fraction of people contacted at least once. Incoming contact count describes each person's network position. Coalition size counts memberships. With 12 people, 24 turns and seed 1, all three conditions reached 10 people. The final coalition counts were 6/6, 6/6 and 7/5. Individual switches occurred even where final totals matched the control. These are consequences of the scenario assumptions. Hegemony, equivalence and populism require independent interpretive evidence.

A local trial with 100 people, 100 turns, seed 1 and p=0.25 generated 114 events in about 8 ms with 476 KB peak traced Python allocations (excluding JSON serialization and interpreter startup). Full affiliation snapshots cost space proportional to population times turns. Compare deterministic JSON or its SHA-256 across repeated runs using the same Python version.

## Future passive interface

A future consumer may subscribe to serialized events using simulation_id, turn and event_id, preserving within-turn log order. It may propose a command for a separate experimental run. The researcher would explicitly authorize and record any intervention. Consumers have read-only access to empirical evidence and completed runs.
