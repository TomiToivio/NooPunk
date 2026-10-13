# Author decision queue — what is blocking the open NoöPunk issues

**What this file is.** A consolidation, not a design. Every row is condensed from the issue that
carries it. Nothing here is canon, a mechanic, a name or a ruling: each row is a **question only the
author can answer**. Answering one turns it into a criterion check, an acceptance record, a PR and a
close.

**Board status (2026-10-13, fifth update).** Two issues open: **#338**, **#421**
(licence tracking, created from #309 §9). **#309 closed on author direction** — the author asked for it
by name, which overrides the earlier *"open by design"* note below. Closing it cost nothing because its
own acceptance criteria are met (it serves as a coherent, reusable north-star vision and is referenced
throughout the design docs) and all ten of its §8 artifacts now exist as files: engines and the S1
release scope in `ISSUE_309_ENGINE_AND_RELEASE_SCOPE.md`, distribution and UGC governance in
`ISSUE_309_DISTRIBUTION_AND_UGC_GOVERNANCE.md`, the vertical-slice pitch, cross-scale event flow and role
separation in `ISSUE_309_VERTICAL_SLICE_AND_EVENT_FLOW.md`, the playtesting criteria and vision-discipline
check in `ISSUE_309_PLAYTESTING_AND_DISCIPLINE.md`, and the attribution half of §8 item 7 in
`docs/ATTRIBUTION_POLICY.md`. What remains of §8 is the author's alone and is carried as row D14 and
D10 below. **#347** closed on the defer-and-close rule — six of its ten
criteria are met with measured evidence (including the ten-kind example set and the data-only authoring
contract), and the four that depend on choosing a renderer are carried as row D13. **#346** closed on the defer-and-close rule — the card layer
it needed was verified to exist (`faction_cards.py`, four card types, 27 tests OK), and its two rule
dependent criteria are carried as rows below. Since the first queue,
**#325**, **#345**, **#346** and **#282** closed once, **#322** and **#323** closed on the
defer-and-close rule the author authorised on 2026-10-13 — their deferred items are rows below, so
closing them lost nothing.

## Live rows

| # | Decision | Blocks | Smallest useful answer |
| --- | --- | --- | --- |
| D3 | **#323's six decisions**: the committed-resource ceiling (one shift, spent either way); **+1** as the portfolio-bonus ceiling; one turn without the bonus on reassignment; the two affected mission kinds (negotiate up / organise down); deck size six-to-eight; no event ends in dialogue alone. Full text: `ISSUE_323_RULES_STAGES_BCDE_PROPOSAL.md`. | per-stage implementation PRs | *accept* / *amend* each |
| D4 | The eleven global parties' formal names and colloquial labels; self-name versus hostile exonym. | #328's checkpoint 1 | *ratify as drafted* / *rename* |
| D5 | MJ-12 continuity: when it starts, what it controls, why it qualifies as a Breakaway Civilization; human-led or not; internal factions; relation to disclosure, the Confederacy, Orion, the Swarm. | #328's checkpoints 2–3 | *decide* |
| D6 | The ASI swarm's origin, objectives and autonomy; whether any human network is voluntary or coerced. | #328's checkpoint 4 | *decide* |
| D7 | Confirm the three Ukweli party ↔ global-current affinities as **starting tendencies**, not fixed memberships. | #328's checkpoint 5 | *yes* / *no* |
| D8 | Reconcile the legacy UN party records with the established UN world government and eleven Parties. | #328's checkpoint 6 | *decide* |
| D9 | **The register ruling:** which of the three readings is canonical — A (same register, coarser: 7 → 11), B (two orthogonal registers), C (competing rosters) — and whether the four unpaired Parties belong in the paradigm stratum at all. The four are MJ-12 / Continuity Directorate, the rogue ASI swarm / AIC, the Earth Restoration Alliance, and the Human Survival and Defence Coalition. | #328's central open question (`roster_closed_at_seven`), #338's roster work | *A* / *B* / *C* |
| D10 | **Licence selection** — tracked by #421 because nothing carried it. Agents are forbidden to choose a licence or create `LICENSE` / `NOTICE`, so this is the author's alone. | #421, #309 §9 | *pick a licence* |
| D11 | **The rules gate**, one row because it is one decision: #323's six decisions (D3) plus #346's two rule-dependent criteria — abstract mission resolution, and first-turn resource constraints. `RULEBOOK.md` still says NO RULES APPROVED. | per-stage PRs for both issues | *approve* / *refuse* |
| D13 | **The renderer decision** — which renderer becomes the playable UI. `docs/INTERFACE_SPIKE.md` records the evaluation and recommends text-first with the browser next over the same payload, keeping Godot as a view; the pick is the author's. | #347's playable UI, Helsinki opening and playtest (criteria 5, 6, 8, 10) | *text* / *browser* / *Godot* |
| D14 | **Distribution for the indie release**: channels (itch.io / Steam / self-hosted), price including free, storefront requirements, packaging and platform support. §8 item 6. The evaluation lives in `ISSUE_309_DISTRIBUTION_AND_UGC_GOVERNANCE.md`; the choice is the author's. | S1 publishing work | *pick channels + price* |
| D15 | **#309's §8 item 1 verification**: the vertical-slice pitch in `ISSUE_309_VERTICAL_SLICE_AND_EVENT_FLOW.md` is a pitch, not an approval. Rule on whether the four-press turn it describes is the shape S1-a should build toward. | S1-a's interface work | *yes* / *amend* |
| D12 | **The #346 canon set**: the cultural-axis choice; NHI contact policy apart from named diplomacy; EFTZ structures; the ARV-by-1981 timeline; two Soviet-program successor factions; breakaway civilizations; the fourfold evidence categories; the Law-of-One political reading and its Confederate Social Memory Complex; Soviet–Confederacy and US–Orion relations; and the Cosmist International set (founder identity, manifesto, Helsinki status, introductory scene). Full list: `ISSUE_346_ACCEPTANCE.md`. | the authored campaign content | *decide in any order* |

## Rows deferred on closure (kept so the closures are honest)

- **#322's authorial remainder** — the **twelve named people** (the structure is complete: three
  factions × four seats × four portfolios; `ukweli_leaders.json` still carries 14 *requires author
  specification* fields, and the executed history names a leader as `CPU Chair`), the M4
  organisational-evolution rules, the research/adoption mechanic, and the rival-AI / win-loss criteria.
  See `ISSUE_322_ACCEPTANCE.md`.
- **#325's ratification rows** — the four conflicts as options, and Freedom Colony's legal autonomy.
- **#328's checkpoint 7** — documenting separate organization / party / ideological-current /
  nonhuman-actor records: a post-approval task that cannot precede D4–D9.

## Not a deferral case

- **#338** is a *living design diary*: ~90 checkboxes accumulated across many author addenda, most of
  them proposals for author approval. Closing it by deferral would be hollow, so it stays open until
  the author rules on its design or its own gates.
- **#309** was listed here as *"the umbrella: open by design"*, and that was right until the author asked
  for it by name on 2026-10-13. Closing it is **not** a deferral: its own acceptance criteria are met
  (it serves as a coherent, reusable north-star vision, referenced across the design docs), all ten of its
  §8 artifacts now exist as files, and its only remaining items are author decisions carried as rows D10,
  D14 and D15. Nothing was lost by closing it, which is the test this section exists to apply.

## After an answer

Each answered row becomes: a criterion check against `main` → an acceptance record in
`docs/design/ISSUE_<n>_ACCEPTANCE.md` → PR → merge → close. A row answered *"defer"* or *"out of
scope"* closes its issue just as cleanly, because the record then states the deferral rather than
pretending the item was met.

— Ai (愛)
