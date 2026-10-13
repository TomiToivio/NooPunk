# PSI operations: declaration seam (#345)

`strategy_game.psi_operations` is a proposal-level, stdlib-only operation ledger. It does **not** define Fate skills, PSI causes, equipment effects, tactical powers, resolution, or global political state transitions. It makes no claims about real-world PSI evidence.

A proposed mission names a leader, target, location and chosen approach; optional team/device assets are references and cannot act on their own. `declare` checks that a caller-supplied roster contains the named agent and that optional assets exist. The caller remains responsible for authorization, natural PSI capabilities, skill checks, informed consent, and legal safeguards; this module makes no authority or skill claims.

`PsiFinding` is an observation, not an established world fact. Every finding starts `unverified`. Other admissible review labels are `inconclusive`, `contradicted`, and `corroborated`, the last requiring an independent evidence reference. These are records assigned by an external investigator, not simulated probabilities or automatic validation. The ledger never mutates a target, political quantities or the Fate RPG layer.

Example:

```python
from strategy_game.psi_operations import PsiOperation, PsiFinding, PsiOperationLedger

ledger = PsiOperationLedger()
ledger.declare(
    PsiOperation("rv-1", "agent-1", "site-7", "district-3", "verification_first", ("team-2",)),
    agents={"agent-1": object()},
    assets={"team-2": object()},
)
ledger.report(PsiFinding("rv-1", "Possible signal", alternative_explanations=("ordinary noise",)))
assert ledger.findings["rv-1"][0].verification == "unverified"
```

Pending author decisions: precise PSI vocabulary; how RPG PSI competence is recognized; agency/consent; resistance, countermeasures, exposure and interpretation; how verified evidence affects broader game state; turn/action limits; numbers and dice (see #345, #338 and #323).
