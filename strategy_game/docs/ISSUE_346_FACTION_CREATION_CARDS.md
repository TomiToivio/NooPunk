# Issue #346: faction creation cards and optional anomalous contact

**Status:** editable tabletop design prototype, **not approved strategy mechanics**. This record operationalizes the author-specified choices in [#346](https://github.com/TomiToivio/NooPunk/issues/346), without assigning stats, probabilities, starting resources, canon identities, or success thresholds. It concerns the **crossover game** in `strategy_game/`, not the legacy RPG. The approved Fate-based character-RPG slice is separate: see `strategy_game/rpg/RULEBOOK.md`.

Cross-cutting constraints: [three design balances](../../docs/archive/DESIGN_PRINCIPLES.md); [strategy rulebook](../RULEBOOK.md); [global parties](../docs/GLOBAL_FACTIONS.md); [PSI design](../../docs/design/ISSUE_345_PSI_RECONCILIATION.md). The story is grounded in social science and character choice; technological claims require plausible constraints; deep Science Fantasy is rare. All supernatural classifications below are **in-world hypotheses or optional fiction**, never real-world scientific claims.

## A. One editable tabletop faction card

Each card has five **independent qualitative positions**. Mark one of `strong first / moderate first / mixed or undecided / moderate second / strong second` for **each** axis, or leave `unknown` if the player lacks information. These are descriptive **labels, not numerical modifiers**.

| Axis | First pole | Second pole | Question this asks |
| --- | --- | --- | --- |
| Economy | Left / collective, egalitarian | Right / private ownership, market accumulation | Who owns and distributes resources? |
| Culture | Liberal / progressive, pluralist | Conservative / traditionalist, continuity | How does the faction view changing social norms? |
| AGI / technology | Precautionary, restrictions, possible AGI prohibition | Acceleration and technological transformation | What pace and guardrails does it want? |
| NHI contact | Isolation or resistance | Contact and integration | What general contact policy does it favor? |
| PSI / consciousness | Materialist, skeptical | Idealist, panpsychist, PSI-open | What beliefs frame mind and consciousness? |

**Explicit axis decision for the MVP:** use the author's *cultural liberal/conservative* axis. This is **not** the Political Compass's authoritarian/libertarian axis. Governance stances (authoritarian, parliamentary, direct democratic, anarchist, civil-liberties-oriented) belong in separate doctrine TAGs. Adding a sixth axis is **deferred**, not assumed approved.

Fields printed on the card:
- Name, public description, self-declared ideology, **actual agenda (GM-private if unknown)**, and the five axis labels.
- **TAGS** separated by type (below); at least a goal, a red line, and a distinguishing doctrine are prompts, **not a cost or compulsory build quota**.
- **NHI diplomacy** as a separate list of named counterparties, each with an overt relationship and optional GM-secret actual relationship. **Never** infer the relationship from the contact axis.
- Leader character reference and their **own** positions/TAGs; optional field agents, advisers, assets, institutions and research links as separate cards.
- Discursive **demands, signifiers, antagonisms, narratives**, and **network ties** as text/links, not a computed hegemony score.
- Evidence visibility: public claim / witnessed / documented / contested / classified or unknown. Do not print secret cosmology on player-facing cards.

### Typed TAG vocabulary (proposal, compatible with #389's shared TAG direction)

The same structural fields `id`, `label`, `type`, `scope`, `description`, `visibility`, `source_or_evidence`, and `narrative_use` can appear on faction or character cards. These are **documentation fields**, not a second game engine. Any concrete syntax and compatibility with `strategy_game/rpg/` must be reviewed before code integration.

| Type | Faction example | Character example | Meaning; expressly **not** |
| --- | --- | --- | --- |
| `doctrine` | `AUTONOMIST_MARXIST` | `MATERIALIST` | A declared or privately held belief; **not** a skill or automatically true |
| `ability` | _not applicable_ | `REMOTE_VIEWER` | Individual practiced capability; **not** proof of philosophical idealism |
| `asset` | `REMOTE_VIEWING_TEAM` | `BCI_DEVICE_ACCESS` | Controlled organizational/person equipment or team; **not** an innate ability |
| `relationship` | `ORION_TRADE_PARTNER` (if discovered) | `GOVERNMENT_CONTACT` | A situated, changeable tie; **not** immutable ideological affinity |
| `goal` | `DEFEND_HUMAN_AUTONOMY` | `DISCLOSE_UFO_SECRETS` | A pursued outcome; **not** an achieved fact |
| `red_line` | `NO_AUTONOMOUS_AGI` | `NO_FORCED_AUGMENTATION` | An explicitly stated limit; **not** a forced game restriction |
| `history` | `LABOR_ORGANIZING` | `ACADEMIC_FOUNDER` | Prior experience/provenance; **not** a bonus without approved rule |

Possible *narrative uses* are unlocking a conversation or mission, identifying a recruit's stated interest, exposing a disagreement, motivating an operation, or, **only once approved**, affecting a check. TAGs do **not** silently grant numeric bonuses, lock alliances, confer character attributes or declare a species' ethics.

**Compatibility example:** A faction can have `PSI_RESEARCH` (doctrine/goal) and an `REMOTE_VIEWING_TEAM` (asset); only an individual who actually possesses `REMOTE_VIEWER` (ability) can claim that capability. Character capabilities remain governed by the eventual approved RPG model. Names in this document are example design labels, not approved universal enum values.

### NHI counterparties are not one diplomacy slider

For known contacts, list the **Confederacy/Zookeepers**, the **Greater Orion Arm Co-Prosperity Sphere**, and, only if established in the scenario, specific independent entities. For every *known* counterparty record public posture, last-known evidence, current relationship and an optional hidden GM fact. `Unknown` is a valid and often preferable state. No starting faction card gives the player automatic knowledge of covert NHI facilities, Orion contracts, Soviet programmes, identities, origins or motivations. The contact axis is a *general policy*, and may coexist with opposing relationships toward specific powers.

## B. Pregenerated, editable quick-start

**Cosmist International** is the default pregen faction **proposal**, not a finalized stat block:

| Axis | Suggested starting label |
| --- | --- |
| Economy | Left, collective/commons oriented |
| Culture | Liberal, pluralist |
| AGI / technology | Mixed: favors human augmentation; wary of rogue autonomous AGI |
| NHI contact | Contact-positive **and** pro-human sovereignty |
| PSI / consciousness | Strongly panpsychist, QIP-oriented |

Suggested doctrine/goal TAGs: `AUTONOMIST_MARXIST`, `RUSSIAN_COSMIST`, `COMMONS_ORGANIZER`, `HUMAN_AUGMENTATION`, `QIP_PANPSYCHIST`, `HUMAN_SOVEREIGNTY`, `DISCLOSE_UFO_SECRETS`. Suggested red line for author choice: opposition to coerced assimilation. **Leader:** the previously proposed pre-crisis academic founder; name, skills, stats, assets and detailed biography remain unassigned here. Corporate patron and four-agent roster are editable **blanks**, not invented characters. Proposed relationship entries for both main NHI powers read `unknown/not verified`. Do **not** import GM-secret Soviet/Confederacy/Orion history into its public knowledge.

### Three cross-axis contradiction cards

1. **Materialist remote viewer:** the person has `MATERIALIST` doctrine and a `REMOTE_VIEWER` practiced ability, interprets PSI evidence cautiously, and may reject cosmic idealism.
2. **Anti-AGI augmented activist:** the faction opposes autonomous AGI while supporting BCI access, assistive implants and embodied human augmentation. Technology caution does not imply bio-only politics.
3. **Market-right Confederacy negotiator:** a right-market politician supports commerce and personal liberties but opposes Orion assimilation and seeks independent diplomatic contact with the Confederacy; no deterministic alliance follows.

Other useful test: a left autonomist can distrust the paternalism of the Confederacy despite supporting NHI contact. None of the above determines morality, electoral support, personality or loyalty.

## C. Tabletop creation procedure, without unapproved mathematics

1. Choose the **Cosmist International** pregen card, another authored pregen, or an empty faction card.
2. Write each of the **five** qualitative ideological positions; `mixed` and `unknown` are legitimate.
3. Choose or author distinguishing **typed** doctrine, goal and red-line TAGs; identify which information is public.
4. Add counterpart-specific NHI relationships only on available **in-world evidence**; conceal any GM-only relationship.
5. Create the faction leader as an independent character card. Their convictions can contradict their faction's public programme.
6. Attach a **small, scenario-authored** set of organization, research and government relationship cards. Helsinki-first is the default; distant networks need represented access.
7. Write one contested **demand**, one candidate **nodal signifier**, one antagonism and a communications-network tie. These are political hooks, not predictive laws.
8. Use a short negotiation or recruitment scene to discover tension. The GM asks what happens; no equation turns ideological distance into allegiance.

**Why these fields matter:** Laclau supplies contingent articulation of demands and signifiers, Castells supplies access to communication networks, and Luhmann reminds us that a corporation, a court, a research institute and a religious organization may interpret the same evidence differently. The card must allow that disagreement; it cannot reduce politics to a five-point personality test.

## D. Authored tabletop scene: The Unverified Channel

**Status:** optional example **investigation and diplomacy** scene, not locked chronology or an established new entity. Location is an **existing Helsinki institutional meeting room**; its exact building, participants' names and outcomes are chosen by the GM.

**Opening:** A university researcher circulates an anomalous signal report, and a government liaison asks the player faction to advise on publishing it. A corporate intermediary offers a private technical evaluation in return for exclusivity. A grassroots organizer demands public access and warns of an elite cover-up. All three have partial evidence; none is introduced as secretly an alien agent.

**Legible cards:**
- **Researcher:** seeks reproducibility and institutional credibility; cautious about uncontrolled publicity.
- **Liaison:** seeks public order, legal process and protection of sources; open to a limited inquiry.
- **Intermediary:** favors exclusive commercial testing; legal rights and incentives need scrutiny, not villain coding.
- **Organizer:** wants transparency, public participation and safeguards against secrecy.

**Faction interaction:** compare expressed AGI/NHI/PSI positions with the request but **do not roll against ideological distance**. Relevant doctrine/goal TAGs such as `DISCLOSE_UFO_SECRETS`, `HUMAN_SOVEREIGNTY`, `PSI_RESEARCH` or `BUILD_EFTZ` suggest questions and available approaches. A party with `MATERIALIST` may still request a replication; an `NHI_CONTACT` diplomat may insist on non-disclosure until stronger evidence appears.

**Meaningful choices:** (a) publish raw claims with provenance and caveats; (b) secure an independent investigation with legal safeguards; (c) permit contractual private study with oversight; (d) refuse participation, while others act. Each choice can change **trust, access, institutional relationships and what is known**, narratively. No invented numerical effects or automatic faction realignment.

**Escalation only if the GM uses the rare Science Fantasy branch:** a second witness identifies the source as an apparent **angel** or **djinn**, or a supposed ancient occult scholar offers testimony. These are *witness descriptions*, **not** objective ontological diagnoses. Competing hypotheses remain open: deception, ordinary technical anomaly, PSI/psychotronics, extraterrestrial, interdimensional, extratempestrial or cryptoterrestrial contact. No claim about a real living religion is validated by the fictional scene.

**Consequences to choose in play:** a parliamentary committee debates legal personhood or airspace jurisdiction; scientific institutions disagree on disclosure standards; organizers contest expert secrecy; a communications network amplifies one framing; a possible covert contact requests a follow-up. These are **social/political and scientific** developments first, not combat encounters or spellcasting. The mystery can be left unresolved; no fireball, monster class, random prophecy or mandatory alien reveal is added.

**Playtest prompts:** Can a skeptical faction meaningfully advance research? Can an NHI-friendly faction resist Orion? Does a media/network relationship matter without a deterministic ideology bonus? Does the stranger-than-science witness remain rare and ambiguous? Can the table explain every changed political relationship in ordinary words?

## E. Editorial and implementation gates

- The card and scene meet the **Social Science Fiction primary / plausible Cyberpunk secondary / rare Science Fantasy tertiary** filter. See the shared project invariants rather than introducing a fourth competing tone rulebook.
- Do not confuse the two broad political dimensions with the standard Political Compass. Keep authoritarian/libertarian governance **TAGs** until the author explicitly requests another dimension.
- Do not force any combination of doctrine, identity, religion, gender, ethnicity, class, psychic ability, presumed morality or NHI loyalty.
- Do not expose the game's classified cosmology on the starting card or treat real-world UFO/parapsychology/religious claims as scientific consensus.
- Do not ship a new engine, dice thresholds, numerical recruitment modifiers, diplomacy formulas, mandatory TAG enum or fabricated lore as if approved.
- **Next implementation decision:** review these editable cards and one scene at the table; after the author approves field semantics, represent the same fields in the existing strategy card/data model and integrate, rather than maintaining competing `TAG` classes or parallel faction engines.
- **Review:** prose by editorial review/tabletop playtest, **not** documentation snapshot tests or CI lore assertions (per `AGENTS.md`).
