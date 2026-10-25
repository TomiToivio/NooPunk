# Six offline, tabletop-convertible extension scenes (#572)

**Status:** worked interface examples, not new calibrated rules. They are deliberately *non-numeric* wherever #566 and related PSI cost decisions have not approved thresholds. Use the already-existing layer's resolver after eligibility gates, never invent a second die. Each scene has inputs, a gate, an observable result and a replay expectation.

## 1. Local physical intrusion

- **Given:** UNSA operative stands at an isolated clinic terminal with authorized physical access and a cable.
- **Gate:** operator physically present; terminal is accessible on a *local* port; route is declared before the skill test.
- **Action:** attempt to read the incident register; under layer B pass permitted action to Fate resolver, under layer A use its current 1d10 core when an approved skill mapping exists.
- **Observable:** evidence gained on success; a failed test changes time/exposure but never fabricates remote reach.
- **Replay:** same terminal/path/character/seed yields identical access ruling and check result.

## 2. Air-gapped remote intrusion

- **Given:** same terminal, operator is elsewhere, no proxy or physical agent on site.
- **Gate:** absent path means **BLOCKED before dice** in every era, including before the Crisis.
- **Observable:** no data and no skill-roll event, regardless of high CYB skill. A Castellsian *social tie* is not a technical path.
- **Replay:** same result under any random seed. Introducing a drone later creates a new separately assessed ingress path.

## 3. Natural PSI (telepathic impression)

- **Given:** naturally PSI-capable investigator with a qualifying capability tag in a conversation.
- **Gate:** natural capability permits an attempt, not an automatic success. A merely sympathetic belief tag does not confer the ability.
- **Action:** layer B resolves through `strategy_game/rpg/psi.py` with the existing Fate skill, rating, consensus and psychic pressure; layer A waits for approved skill/cost specification.
- **Observable:** an interpretable impression or a failed/partial attempt, with pressure tracked by the owning subsystem; no fact is invented solely by the test.
- **Replay:** matching character, context and seed produce matching mechanical outcome.

## 4. Psychotronic device

- **Given:** investigator without natural PSI uses an authorized psychotronic sensor and a target within the instrument's declared operational envelope.
- **Gate:** operational and powered device, real target access and necessary training/permission; **never retroactively grant natural PSI**.
- **Action:** use the owning equipment/test contract. Device output remains a measured observation, not telepathy by innate capability.
- **Observable:** observation, noise, or device failure recorded, with device provenance.
- **Replay:** fixed inputs/seed and device state reproduce the same instrumental outcome.

## 5. BCI-mediated message

- **Given:** two consenting agents with active compatible interfaces and a working link.
- **Gate:** check actual connection and permission first; no link means no message, even if both have advanced cyberware.
- **Action:** transfer a bounded message through the device channel; when deception/interference is contested, resolve via that layer's existing check system.
- **Observable:** delivered message and channel provenance; do not call it innate PSI or model bodily System Strain as mental effort.
- **Replay:** serialization preserves link state, consent, payload and any seeded contested result.

## 6. Astral transition

- **Given:** embodied agent seeks projection into Noöspace.
- **Gate:** `src/rules/cross_domain_state.py` is currently **provisional**; in that model an agent has exactly one locus and must use an allowed transition. The model never authorizes simultaneous full physical and astral action.
- **Action:** enter projected state only when the campaign invokes the provisional domain rules; from there a cross-realm action needs a *declared gateway*, not a lucky die.
- **Observable:** physical-body exposure, no simultaneous action in two realms, and eventual return to embodied state before cyber immersion.
- **Replay:** transitions are deterministic, with no external model or online dependency.

## Acceptance and implementation boundaries

- Layer A uses its existing STAT/Skill/1d10 resolver; layer B's Fate mode remains a separate approved game. These examples bridge narrative **contracts**, not the dice systems.
- A successful skill check never bypasses a failed connectivity, capability or realm-permission gate.
- No imported Without Number prose, item lists, powers, creature statistics or factions.
- Resource economy for sustained PSI/BCI, injury/trauma calibration and character progression remain **DEFER** until separately approved. Example checks are portable to paper; existing executable tests `strategy_game/tests/test_cyber_access.py`, `strategy_game/tests/test_psi_scenes.py` and `tests/test_issue225_cross_domain_state.py` exercise portions of the current implementation, not this entire narrative suite.
