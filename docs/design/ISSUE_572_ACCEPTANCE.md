# Issue #572 — acceptance record

**Documentation issue, part of the #564 epic. Checked against `origin/main` at `d2c960d`.**

## Criterion check

#572's own "The work" is four items, plus a gate. Each is checked against the tree, not against
intent.

| # | Requirement | Evidence | Met |
| --- | --- | --- | --- |
| 1 | For each extension: what it does mechanically today, which layer owns it, and whether the family offers any equivalent — with "no equivalent" recorded **as KEEP-ORIGINAL by construction**, not forced into a REPLACE | `docs/rules/ISSUE_572_NATIVE_SUBSYSTEMS.md` §8.1 — eight extensions, each with owning layer, owner artefact, family equivalent and verdict | **yes** |
| 2 | Show where CWN's matrix-like assumption and NoöPunk's assumption are incompatible, and **what a network-access subsystem must add** | §8.2 — a three-row incompatibility table plus the five things the subsystem must supply; backed by the reach gate, exposure economy, alert ladder, shared clock and breach separation in §2 | **yes** |
| 3 | State whether PSI is a **skill, a resource, a permission, or a separate subsystem** in **each layer** | §8.3 — per-layer table (A: skill **and** resource; B: permission; C: not modelled), with the permission gate and resolution kernel named for each | **yes** |
| 4 | Keep every extension deterministic and tabletop-convertible: **no LLM in the loop** | §8.4 — grep for `requests|http|socket|urllib|openai|anthropic|llm` across the three modules returns **nothing**; seeded replay pinned by `test_the_same_seed_replays_and_a_different_seed_does_not`; 32 tests green on 3.11 | **yes** |
| Gate | Documentation now; implementation after the scope decision | Scope was decided in **#566** (layer A only, `1d10`, Edges admitted) and recorded in `docs/CWN_CHASSIS.md`; the two subsystems landed under **#593/#595** | **satisfied** |

## What was already there, and what this round added

The map (§§1–7) and both subsystems (`src/rules/ubiquitous_network.py`,
`src/rules/natural_psi.py`) landed under **#593**, **#595** and **#598** from other sessions. This
round did not re-derive them; it closed what the issue actually asked for and was still missing:

- **§8.1** the by-construction verdict table with layer ownership — the issue's item 1 had no table.
- **§8.2** the incompatibility table and the five required additions, phrased against the author's
  ruling rather than the issue's original parenthetical.
- **§8.3** the per-layer PSI classification — the document stated canonical facts but never answered
  "skill, resource, permission, or subsystem" layer by layer.
- **§8.4** determinism evidence. Before this round the document had **zero** mentions of
  deterministic/offline/no-LLM, which was a stated requirement.

## One correction to the issue's own premise

The issue says NoöPunk assumes *"disconnected devices, physical ingress."* The author's ruling of
2026-10-25 makes the **ubiquitous network** the default and severance the exception the crisis
produces. §8.2 records this explicitly: physical ingress is still modelled (the `courier` channel),
but as the way to reach a **partitioned** segment — not as the precondition for every act. Leaving
the issue's wording unqualified would have re-imported the CWN assumption the ruling rejected.

## Carried forward, not silently dropped

- **D43 — PSI discipline vocabulary.** `src/rules/noopunk_extensions.py` (a prototype, explicitly
  not the rules owner) accepts seven slugs; `influence`, `healing`, `shielding` are not in the locked
  six (#159). Deleting them would assert they are not canon; promoting them would assert they are.
  Both are canon decisions, so neither is taken — the row is in the queue.
- **D36** — Effort capacity curve and exposure bands remain `TUNING_`, author's to set.
- **D23** — Edges admitted but unbuilt; count and frequency are the author's.

## What this does not do

No rule is approved, no number filled, no canon invented, and no third-party expression imported
(SWN stays `blocked-unverified`; Effort is an independent implementation of a described mechanic).
