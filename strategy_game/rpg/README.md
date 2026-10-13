# NoöPunk Global Strategy: Fate-based RPG layer

This is an **expanded, bounded implementation slice** of [issue #389](https://github.com/TomiToivio/NooPunk/issues/389). It is an independently importable Python module and **not yet a full implementation of Transhumanity's Fate**.

The authored decision is **Fate Core as the shared RPG resolution foundation**, with **Transhumanity's Fate and Eclipse Phase as design references**. The latter books' noncommercial Creative Commons conditions are not the same as Fate Core's CC BY license. This implementation is original Python code based on the Fate Core SRD, not a port or reproduction of their copyrighted prose, setting content, proprietary illustrations or character catalogues.

## NoöPunk continuity
- Entirely **different** fictional scenario and lore from Eclipse Phase; no automatic Fall, Firewall, exsurgent virus or posthuman ubiquity.
- Most humans have their **original biological bodies**. Cortical stacks and resleeving are **rare, experimental technologies**, defaulting to absent.
- PSI is **natural**, not virus-derived; many humans possess natural PSI. Abilities may be trained or augmented, but no illness flags are required.
- Cyber intrusion respects actual connectivity and local access; see [cyberspace design](../docs/CYBERSPACE_AND_CONNECTIVITY.md).
- RPG actions must remain separate from the unapproved strategy and political-simulation layer.

## Implemented
- Fate dice: four independent -1 / 0 / +1 faces.
- Fate's four action kinds: overcome, create advantage, attack, defend.
- Skill + dice versus difficulty; failure, tie, success and success with style.
- Narrative character aspects, stunts, equipment, Fate-point spend and +2 invocation.
- Basic physical/mental stress boxes and consequence slots.
- Optional physiological state, cortical stack/resleeving and innate PSI capability.
- One deterministic BCI cyber + precognitive PSI demonstration with the **same engine**.

## Not yet implemented (track in #389)
- Fate's full reroll invocation, temporary aspects with free invokes, compel/refresh economy.
- Detailed four-action outcome tables, tie costs, boost creation, attacks, opposition and teamwork.
- Complete damage/consequences/taken-out/concession exchange rules.
- Full character generation and stunts, aspects' narrative permission adjudication, GM scene UI.
- Cyber/PSI capability and countermeasure requirements, rare experimental resleeving procedures.
- Faction strategy turns, Laclau simulation, AI/GM NPC policies, integration with existing leader-card system.

## Added in the #389 completion pass
- **Attribution, made explicit and machine-readable:** [`ATTRIBUTION.md`](ATTRIBUTION.md) plus [`attribution.py`](attribution.py), which carries the Fate Core attribution, the unofficial notice and the upstream licence distinctions so a test asserts they are present. The licence NoöPunk *distributes* under stays the author's decision (licence gate #200) and is not chosen here.
- **Shared typed character TAGs:** `Character.tags` uses issue #346's vocabulary (`belief`, `competence`, `equipment`, `relationship`, `asset`, `goal`) through the same `Tag` type the faction and card layers use, with a duplicate guard and `tags_of_kind()`. No second tag scheme, so a doctrine is never read as a capability.
- **The adapter boundary to the unbuilt strategy layer:** [`boundary.py`](boundary.py) fills the reserved `strategy_game.ports.LeaderRPG` seam — sheets and seeded, replayable checks outward — and declares **in code** what this layer is not (turn cadence, faction action, resource economy, victory condition, political transition, discourse or network simulation). It joins nothing to `WorldState`.
- **A netrunning example** (`demo_netrunning`): a foothold first, then the intrusion check, on the same engine. The access step is explicit because issue #344 requires a credible connection rather than assuming remote reachability.
- **Tests:** [`tests/test_fate_rpg_boundary.py`](../tests/test_fate_rpg_boundary.py) covers the attribution constants, the tag vocabulary, the boundary payload and its declared exclusions, seeded replayability across the two demos, and a source-level check that these modules import none of the unapproved layers.

The public functions `roll_fate`, `resolve`, `skill_check` and `demo_investigation` are dependency-free. Use Python 3.10+.

```bash
python -m strategy_game.rpg           # the worked scene as JSON
python -m strategy_game.rpg --text   # the same report as reading text
python -m strategy_game.rpg --seed 7
python -m unittest strategy_game.tests.test_fate_rpg
python -c "from strategy_game.rpg.fate import demo_investigation; print(demo_investigation())"
```

## Run it: the worked scene

`python -m strategy_game.rpg` runs the layer's demonstrations in one payload and prints them: the
**investigation** (a cyber *overcome* and a PSI *create advantage* through the **same** engine, which is
issue #389's worked example), the two **BCI netrunning** examples, and — for every check — the dice as
they fell, the total, the shifts and the outcome, followed by what the table keeps. The module is
[`run.py`](run.py) and the entry point is [`__main__.py`](__main__.py). It is **noncanonical and
illustrative**: an example of the engine, not scenario canon, and it computes no strategy or political
mechanic. Its exclusions are read from [`boundary.py`](boundary.py) rather than restated, so the seam has
one home.

This added no coupling. `run.py` and `__main__.py` import only from inside `rpg/`; the layer's contract
in [`tests/test_rpg_boundary.py`](../tests/test_rpg_boundary.py) permits exactly two *types* to cross
from the strategy engine — the shared `characters` tag vocabulary anywhere, and the reserved port's
`core.WorldState` parameter type in the one file that fills the port — so the demonstration reaches for
neither.

## Licensing and sources
- Fate Core System SRD: https://fate-srd.com/fate-core
- Official Fate CC downloads and rules: https://fate-srd.com/official-licensing-fate
- Fate CC BY 3.0 guide: https://fate-srd.com/official-licensing-fate/cc
- Eclipse Phase 2e rules: https://eclipsephase.github.io/en/03/00-game-mechanics.html
- Publisher Eclipse Phase license: https://eclipsephase.com/cclicense/
- Transhumanity's Fate licensed sample: https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/176939-sample.pdf

**Fate attribution:** This work is based on Fate Core System and Fate Accelerated Edition (found at https://www.faterpg.com/), products of Evil Hat Productions, LLC, developed, authored, and edited by Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin, Mike Olson, Clark Valentine, Amanda Valentine, Fred Hicks, and Rob Donoghue, and licensed for our use under the Creative Commons Attribution 3.0 Unported license (https://creativecommons.org/licenses/by/3.0/).

NoöPunk is an independent fan-developed project and is not sponsored or endorsed by Evil Hat Productions or Posthuman Studios.
