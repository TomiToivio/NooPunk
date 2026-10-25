# The six worked examples (#572)

**Status: documentation. No rule, number or runtime behaviour is changed or approved.**
Scope settled by the #566 ruling (`docs/CWN_CHASSIS.md`): **layer A only, `1d10`, `FIT/REF/INT/SOC/CYB/PSY`,
no classes or levels.** Layer B keeps its approved Fate kernel.

This file does what #572's own gate asks for: for each of the six cases, state the tabletop example, name the
**executable check that already proves the mechanical claim** where one exists, and say plainly where none exists
and what would have to be authorized before one could.

The rule followed throughout: **a claim with a test is a guarantee; a claim without one is prose.** They are
labelled differently below.

---

## 1. Physical intrusion — **proved**

**Example.** The team needs a file on a machine in a building with no external network. Nobody can reach it by
address. They send someone in with a hand terminal, plug into a maintenance port, and act from there.

**What the model says.** A local access path reaches an isolated target *only* with someone physically on site;
the route is a new, specifically modelled path rather than a retroactive opening of everything disconnected.

**Proof.** `strategy_game/tests/test_cyber_access.py::test_a_local_path_reaches_an_isolated_target_only_with_someone_on_site`

## 2. Air-gapped target — **proved**

**Example.** A player asks to hack a lab that is air-gapped from the city network. The correct answer is not
"very hard" — it is **impossible from off-site**, in every era.

**What the model says.** No remote path reaches an isolated target in any of the three periods; the crisis
*removes reachability* rather than reducing capability; and an influence edge in the social graph is not a route.

**Proof.** three tests, because they guard three different mistakes:

- `test_no_remote_path_reaches_an_isolated_target_in_any_era` — the air gap itself;
- `test_the_crisis_removes_reachability_rather_than_capability` — the period changes *what is connected*, not how good the operator is;
- `test_an_influence_edge_is_not_a_route` — the one most likely to be argued at a table: knowing someone is not a TCP/IP connection.

## 3. Natural PSI attempt — **proved**

**Example.** A character with natural PSI attempts to perceive something at a distance. It resolves as an action
with a rating, modified by consensus and pressure — and it must not *create* PSI in a witness who lacks it.

**What the model says.** `rpg/psi.py` names modes of *action* (`TELEPATHY`, `REMOTE_PERCEPTION`,
`PRECOGNITION`, …), not a power list; the scene resolves on the one existing engine; and the outcome is
deterministic for a seed.

**Proof.** `test_psi_scenes.py::test_nothing_creates_innate_psi_in_the_witness`,
`test_both_checks_resolve_on_the_one_existing_engine`, `test_it_is_deterministic`.

**Why this matters for the epic:** PSI staying *natural* is a canon constraint (`#482`), and the test above is
what keeps a conversion from quietly making PSI contagious or virus-derived.

## 4. Psychotronic device — **documented, not proved**

**Example.** A character without natural PSI uses a psychotronic device to produce an effect. The device is
required; the operator's own PSI is not.

**What exists.** `PsiMode` and `CrossLayerEffect` can name the act and its interface, and #572's map already
records the design position: device access and effects are distinguishable from an innate ability.

**What does not exist.** No code path distinguishes *device-mediated* PSI from *innate* PSI, so there is nothing
to test. Creating one means deciding what a device costs, whether it can be used untrained, and how it interacts
with the existing pressure/consensus modifiers — all of which are **numeric subsystem decisions the #566 ruling
explicitly left `DEFER`**.

**What would unblock it:** an author ruling on device cost and permission, then one deterministic test
(device present → effect allowed; device absent → refused).

## 5. BCI-mediated message — **documented, not proved**

**Example.** Two characters with BCIs exchange a message. It is a *third* communications mechanism — neither
natural telepathy nor an ordinary network message — and it is mediated by an actual connection.

**What exists.** The design position (#572), `cross_domain_state.py`, and the connectivity model that decides
reachability before any check.

**What does not exist.** A BCI-specific channel in code. The honest question — *does a BCI need a live network
route, or only proximity?* — is a setting decision, not an implementation detail, and answering it by writing a
test would be inventing mechanics.

**What would unblock it:** the same ruling as #4 (what a BCI *is* mechanically), then a test asserting the channel
refuses when the connection model says there is no route.

## 6. Astral transition — **partially modelled**

**Example.** An effect crosses from one layer of the setting to another — the case `CrossLayerEffect` exists for.

**What exists.** `CrossLayerEffect` carries `source_layer`, `target_layer`, `interface`, `trigger`,
`consent_required`, `consent`, `reversible` and `provenance`, and `permitted` refuses a consent-required effect
that was not consented to. The consent gate is the same one psychosurgery applies.

**What does not exist.** An "astral" transition modelled end-to-end. The cross-layer *bookkeeping* is there; the
transition itself is not.

**What would unblock it:** deciding whether astral travel is a `CrossLayerEffect` instance or its own subsystem —
again a design ruling, and one that `noospace_projection.py`'s explicitly provisional status bears on.

---

## Summary

| # | example | status | evidence |
|---|---|---|---|
| 1 | physical intrusion | **proved** | `test_a_local_path_reaches_an_isolated_target_only_with_someone_on_site` |
| 2 | air-gapped target | **proved** | 3 tests, incl. `test_an_influence_edge_is_not_a_route` |
| 3 | natural PSI attempt | **proved** | 3 tests, incl. `test_nothing_creates_innate_psi_in_the_witness` |
| 4 | psychotronic device | documented | no code path — needs a device ruling |
| 5 | BCI-mediated message | documented | no channel in code — needs a BCI ruling |
| 6 | astral transition | partially modelled | `CrossLayerEffect` exists; the transition does not |

**Three of six are guarantees, three are prose.** That is the honest state, and the split is not arbitrary: the
three proved cases are the ones whose mechanics were already settled by earlier work (#344's reachability model,
#482's PSI constraints). The three unproved cases all wait on the same class of decision — what a device, a BCI
and an astral layer *cost* — which no agent may take.

No rule was changed to write this file.
