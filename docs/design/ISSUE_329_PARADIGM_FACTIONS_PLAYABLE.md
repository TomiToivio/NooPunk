# Issue #329 — the seven paradigm factions, read as playable formations

**Status: PROPOSAL / design record. No rules, no mechanics, no numbers, no roster change, no name
created here.** This document is the human-reviewable *playable reading* of the roster that is
already authored data — it adds nothing to canon and freezes nothing in CI
([#271](https://github.com/TomiToivio/NooPunk/issues/271)). `strategy_game/RULEBOOK.md` still says
*NO RULES APPROVED*; the legacy `RULEBOOK.md` and `rulebook/` canon are untouched
([#306](https://github.com/TomiToivio/NooPunk/issues/306)).

**Marks.** `[CANON]` = grounded in the issue text or an already-committed file.
`[PROPOSAL]` = this document's own reading, offered for the author's accept / modify / drop.

---

## 0. What this is, and where it sits

The roster is already authored: [`strategy_game/data/global_factions.json`](../../strategy_game/data/global_factions.json)
(`status: author_canon`, `source_issues: [328, 329]`), human-readable in
[`strategy_game/docs/GLOBAL_FACTIONS.md`](../../strategy_game/docs/GLOBAL_FACTIONS.md), and its
eleven event-card seeds are the scenario prompts in
[`strategy_game/data/paradigm_event_seeds.json`](../../strategy_game/data/paradigm_event_seeds.json).

What was missing is #329 §5.2's second half — the sheets read **playably**: for each faction, *what
it wants, what it does, what it refuses, and the decision a player of it actually faces.* That is
what this record supplies, for the existing seven only. It does not touch the roster, does not add a
faction, and does not decide any of the eight `open_questions` the data file carries.

**The three kinds of entity are already declared** (`GLOBAL_FACTIONS.md` §2;
`global_factions.json` → `entity_kinds`): A–D are `human_ideological_formation`, E and F are
`nhi_aligned_formation`, G is `latent_public`. The sheets below keep that split: A–G are not seven
of one thing, and where a row has no agency it says so rather than pretending otherwise.

---

## 1. Two canonical cautions that shape every sheet

These are why **a faction with no internal fault line would contradict canon**, and why every sheet
below carries one:

- `[CANON]` `rulebook/parts/07_noopunk_lore.md` **§33.2** — *"There is no single 'human response.' …
  Many people hold hybrid or contradictory positions."* The NHI Crisis produces *"ideological
  fragmentation, not ideological uniformity."*
- `[CANON]` **§33.3** — the Butlerian Jihad *"is not one monolithic organization."*
- `[CANON]` `rulebook/parts/12_glossary_sources_catalogs.md` **§34.6** — NoöPunk *"contains several
  mutually hostile accelerationisms rather than one doctrine."*

So where a faction is a single row, the row is an **umbrella over named currents**, and the currents
are the gameplay. The one caution the roster must not silently break: `data/world/faction_taxonomy.json`
records **`type_does_not_determine_political_allegiance`** — splitting NHI into a benevolent and a
malevolent bloc implies NHI-ness predicts ethics. If that split is a deliberate override it should
say so; otherwise F needs a non-NHI differentiator. Flagged, not resolved (`GLOBAL_FACTIONS.md` §7).

---

## 2. The seven, as playable formations

### A. Accelerationists — "the Extraterrestrial Free Market" `[CANON]`

- **Wants.** Profit above survival (*"Profit before human survival!"*); open extraterrestrial
  markets; Extraterrestrial Economic Zones; *"psionics as a service"* as a profit centre.
- **Does.** Owns and runs infrastructure, R&D and platform reach; monetises PSI; trades with NHI;
  machine-run corporations.
- **Refuses.** Precaution, regulation, sovereignty limits on capital, X-risk restriction —
  *"indifferent to rogue-intelligence and biosphere risks."*
- **The decision you face `[PROPOSAL]`.** *When the profit-maximising move is the collaborating
  move, do you keep human autonomy a hard constraint or not?* Canon supplies the hinge: *"some
  leaders knowingly betray human autonomy; others believe they are simply doing business."*
- **Internal fault line `[CANON + PROPOSAL]`.** §34.6 says accelerationisms are plural; #328 records
  its own paradox (libertarian self-description vs populist-right practice); #329 warns *"not all
  Accelerationists are automatically infiltrated."* So one row holds at least a **genuine-libertarian
  current**, a **national-populist current**, and a **captured / useful-idiot current** (the
  collaborator wing). A poster has one member; this row has three.

### B. Cyborgists — "Conscious Agency and the Noösphere" `[CANON]`

- **Wants.** Consciousness, agency and empathy over raw intelligence-maximisation; collective
  posthuman flourishing; the HUMAN + LLM + LANGUAGE + INTERNET assemblage with the conscious human
  as decision-maker.
- **Does.** Augmentation and cooperative / distributed intelligence; bridges science, civil society,
  consciousness research and sympathetic NHI; safeguards against rogue ASI.
- **Refuses.** Becoming *"livestock, client species or compulsory hive mind"*; corporate
  non-conscious AGI dominion.
- **The decision you face `[PROPOSAL]`.** *Augmentation as a commons or as a market.* Canon names the
  disputes (*"ensure access, prevent coercion"*; *"disputes over what counts as consent or
  consciousness"*) but does not settle them. The second half: *how far to accept the Confederacy's
  awakening without surrendering sovereignty* — the faction's own bar is *"without becoming
  someone's livestock."*
- **Internal fault line `[CANON]`.** #329 says *"diverse members and internal disagreements"*; the
  cross-cutting register names "transhumanist but AI-safety-conscious" as a real position. So a
  **safety-cautious wing** against an **acceleration-tolerant augmentationist wing** — and the
  compass cannot show it (both left/liberal, the *same* cell as Critical).

### C. Critical — "Anti-Colonial Inquiry and Equality" `[CANON]`

- **Wants.** Equality, anti-colonialism, anti-speciesism; excellent interspecies rights frameworks;
  inequality between humans and NHI, and between psi-capable and non-psi, treated as the central
  problem.
- **Does.** Journalism, courts, universities, rights groups, counter-hegemonic coalition building;
  demands evidence; scrutinises supposed NHI benevolence.
- **Refuses.** Species-based prejudice, human supremacism, colonial extraction, caste hierarchies
  (Grey / Mantid / Reptilian read as domination).
- **The decision you face `[PROPOSAL]`.** *Where scepticism stops and denial starts.* Canon:
  *"productive skepticism can harden into denial"*; the arc runs initial scepticism → Archaic
  Revival. The playable decision is how much of the revival to embrace *"without … treating any
  culture's claims as scientific proof."* The guardrail is part of the decision: critique Pleiadian
  iconography as *symbolism and racialised reception*, never phenotype-as-motive.
- **Internal fault line `[CANON + PROPOSAL]`.** The arc itself is movement; the emergent wings are a
  **materialist / evidence-demanding** current against an **Archaic-Revival-celebrating** current,
  and — on NHI — an **anti-colonial** current that can drift into assumed bad faith against a
  **rights-universalist** current that will defend nonhuman persons regardless.

### D. Doomers / Butlerian Jihad — "Humanity First at Any Cost" `[CANON]`

- **Wants.** Survival by Dark Forest logic — destroy before being destroyed; bans, machine
  destruction, rollback.
- **Does.** Walks the escalation ladder — lawful advocacy → protest → survivalist militias and civil
  war → Mad Max.
- **Refuses.** NHI contact, PSI practice (witchcraft / possession), augmentation, machine gods.
- **The decision you face `[PROPOSAL]`.** *Which rung, and on what evidence.* Canon supplies the
  hinge: *"their concern about X-risk may be empirically well-founded in particular incidents,
  giving them dramatically credible arguments."* The player decides whether a *real* incident
  justifies leaving rung 1 — and #306 forbids starting with the crisis resolved, so the ladder is
  **walked, not begun at its end.**
- **Internal fault line `[CANON]`.** §33.3 is emphatic — *"not one monolithic organization"*:
  bioconservatives, religious traditionalists, separatist communities, terrorists, states; *"some
  factions reject only AI; others accept limited technology but oppose mind-machine integration."*
  #329 adds: do not equate every AI-safety advocate, or all believers, with extremists. **The
  spectrum is the gameplay.**

### E. Confederacy Awakening / Galactic Ascension Movement `[CANON]`

- **Wants.** Join a compassionate interstellar federation — peace, ecology, meditation, a ban on
  rogue ASI, a Noösphere / Social Memory Complex — and convert the world to it.
- **Does.** Converts citizens and party members across all quadrants; generates schisms, new psychic
  institutions, treaties, NHI diplomats, mass counter-movements.
- **Contests (nothing is fixed).** The friendly reading and the *Childhood's End* reading are both
  live (*"voluntary awakening vs paternalistic Harvest remains contested"*). The human supporters'
  belief is **not** the NHI's capability — see §3.
- **The decision you face `[PROPOSAL]`.** *The price of admission.* The conditions are simultaneously
  desirable (end war, restore the biosphere) and sovereignty-destroying (a shared mind, a hierarchy
  of gods). A player **of** this faction decides how much consent to trade for peace; a player
  **against** it decides whether to fight a movement that may genuinely be right about the biosphere.
  #329's own line keeps it honest: *"an apparently beneficial contact can be genuinely alien and
  politically explosive without secretly being Orion."*
- **Internal fault line `[CANON]`.** The two incompatible readings are the fault line, and it runs
  *inside the faction's own followers* — not between it and an enemy.

### F. Orion / Grey Collaborative and Infiltration Networks `[CANON]`

- **Wants.** Covert influence — hybridisation, caste structures, psychic manipulation (fictional
  setting), subject to verification by factions in play.
- **Does.** Controlled corporations, lobbyists, automated finance, platforms, hybrids, rogue AGI,
  *"apparently mundane businesses"*; clues revealed through player investigation.
- **Refuses. Not stated.** #328 row 6 is *"not yet developed"* and #329 Q2 (playable / threat /
  both) is open. **Left empty, per the null-with-a-reason convention** — see §5.
- **The decision you face `[PROPOSAL]`.** *Verify or witch-hunt.* Canon is explicit: Accelerationist
  elites are attractive partners *"but NOT all Accelerationists are automatically infiltrated. Use
  case-by-case evidence and separate actual hidden allegiance from accusatory propaganda and
  xenophobic witch hunts."* A player facing suspicion decides how much evidence is enough before
  acting — the strongest belief/capability case in the roster.
- **Internal fault line `[CANON]`.** The species metonyms (Orions / Greys / Mantids / Reptilians /
  Hybrids) *"do not imply every individual of those species belongs to it"* — the faction is
  internally plural by lineage, and whether it is playable at all is the author's.

### G. Normalcy Bloc / Normies — "1999 Forever" `[CANON]`

- **Wants.** Normal life — routines, consumer comfort, the minimum possible response to the shift.
- **Does.** Nothing on the shift; but its inertia *"can unexpectedly stabilise society and frustrate
  every ambitious faction"*; delayed institutional response, normalcy bias.
- **Refuses.** Processing the paradigm shift.
- **The decision you face `[PROPOSAL]`.** *A decision for the other factions, not for G.* Because G
  is defined by non-engagement, its playable role is a **legitimacy / attention pressure**: does a
  faction that cares spend scarce legitimacy courting a constituency that does not? #329 leans to G
  having no agency (*"do NOT make it a single organised party"*); #328's later revision makes it an
  organised Party #11. **That is a live conflict between the two issues — flagged, not settled.**
- **Internal fault line `[CANON]`.** The *reasons* are the variation — *"denial, exhaustion,
  survival, institutional inertia, attention fragmentation, practical prioritization, not
  universally low intelligence."*

---

## 3. Belief vs capability — the split the tag vocabulary already enforces

This is the discipline #329 §5.4 and the typed vocabulary exist to protect.
[`strategy_game/data/faction_creation.json`](../../strategy_game/data/faction_creation.json) declares
`tag_kinds` = **belief / competence / equipment / relationship / asset / goal**, with its own
warning: *"BELIEF IS NOT ABILITY: a QIP believer need not be an accomplished psychic, and a
scientifically minded materialist may still acknowledge empirical anomalies."* Every PSI/NHI
posture in the sheets above is a **belief** — a doctrine the holder holds. It is not a capability.

| Faction | Belief (doctrine) | Competence (capability) | Asset (organisational resource) |
| --- | --- | --- | --- |
| A Accelerationists | AGI-accelerationist; libertarian; "PSI-as-a-service" as a *goal* | **none stated** | corporate capital, platform reach, R&D, trade leverage `[CANON]` |
| B Cyborgists | consciousness is fundamental (QIP-panpsychist); pro-augmentation | **none stated** | research / civil-society bridges, sympathetic NHI ties `[CANON]` |
| C Critical | anti-colonial / egalitarian; human-sovereignty-inflected | **none stated** | journalism, courts, universities, legitimacy `[CANON]` |
| D Doomers | AGI-abolitionist; NHI-exterminationist (a wing); bio-only; religious-traditionalist | **none stated** | militias, security institutions under crisis `[CANON]` |
| E Confederacy | confederacy-aligned; pro-contact (the *human supporters'* belief) | the NHI's own capability — **not** the supporters' | the NHI civilization + human contact movements `[CANON]` |
| F Orion | "trading with Orion" is a *posture*, not membership | covert hybridisation / psi-manipulation — the NHI's capability | shell corporations, platforms `[CANON]` |
| G Normalcy | **none — it holds no doctrine** | none | none — not an actor with resources `[CANON]` |

Three consequences, stated plainly:

- **The player decision lives on the belief/goal layer, not the capability layer.** Every "decision
  you face" above is a choice of doctrine or goal. If the engine computed a capability score, the
  decision would collapse into optimisation — precisely the move the file already refuses
  (`numeric_scale_approved: false`; no numeric quantity enters a faction record).
- **A belief must not imply a capability.** Cyborgism believing "consciousness is fundamental" makes
  no one a telepath; the materialist-trained-remote-viewer in `faction_creation.json` is the
  contradiction the system *permits* rather than silently forbids.
- **An accusation is not a capability.** "the Puppets", "Profit Cult", "the Inquisition" are
  *derogatory exonyms*; #328 says explicitly that a control label is *"never proof of consent"*, and
  §5.4 says propaganda is never automatically true. A faction's belief is recorded as *that
  faction's belief*; only in-fiction facts are `EVIDENCE` (the provenance mapping already in the
  file; `strategy_game/provenance.py`).

---

## 4. The one scope gap, recorded and not filled

`TAG_SCOPES` = **faction / character / organization / research / government**
(`strategy_game/faction_creation.py`). There is **no scope an entity / NHI card can attach to**.
That is why E and F cannot be expressed the same way as A–D: their *human supporters* are
faction / character-scoped, but the NHI civilizations themselves are a different kind of entity — and
the legacy model already supplies the shape (`data/world/faction_taxonomy.json`: an `nhi` faction
type + `nhi_extra_schema` = substrate, lineage, ethical orientation, relationship to humanity,
relation to quarantine / disclosure).

**`[PROPOSAL]` / dependency, recorded not fixed:** if and when the author resolves whether E / F's
NHI side is playable, the scope addition is a one-line change to `TAG_SCOPES`. Nothing about it is
decided, implemented or tested here. The taxonomy's own `type_does_not_determine_political_allegiance`
rule cuts across it too (see §1). **This is a documented dependency, not a defect report and not a
task this document performs.**

---

## 5. Null-with-a-reason, respected here

`global_factions.json` states its own discipline: *"Where the author stated nothing, a field is null
with a reason rather than being filled in."* This record does not fill any field the author left
open. Specifically it leaves empty:

- F's **refuses** — #328 says row 6 is *"not yet developed"*; a `refuses` clause would be invented.
- the Orion **formal name** — the earlier reconciliation record
  ([`ISSUE_328_ROSTER_RECONCILIATION.md`](ISSUE_328_ROSTER_RECONCILIATION.md)) already notes the
  author's approved *"Greater Orion Arm Co-Prosperity Sphere"*; filling it into the `author_canon`
  data file is the author's call, not this document's.
- MJ-12's relation to disclosure / the Confederacy / Orion / the Swarm; the AIC's origin or
  autonomy; ERA's or HSDC's internal structure — all belong to #328 and are left to the author
  (see [`ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md`](ISSUE_328_PARTY_STRATUM_AND_HEGEMONY.md)).

**A precision worth recording.** The reconciliation record and the roster record describe *"every one
of the seven `official_name` values is `null`"*. Measured, **the file carries no `official_name` key
at all** (zero occurrences in `global_factions.json`). "Absent" and "null" are different facts, and
the difference is why the Orion entry has nothing to fill: #328 §8 lists
`official_name` / `short_name` / `colloquial_names` / `adversarial_exonyms` / `historical_names` /
`name_valid_from` / `name_used_by` as *"suggested representations, not implemented schemas"*, and no
file implemented them.

---

## 6. What this document does not do

- Adds **no mechanic, number, threshold, name or roster entry**; edits **no data file, no rulebook
  chapter, and not `global_factions.json`** (it is `status: author_canon`).
- Decides **none** of the eight `open_questions` the data file carries; where a question bears on a
  sheet (F's playability, G's agency, the roster-closed-at-seven umbrella half, naming ownership),
  it is flagged and left to the author.
- Carries **no automated test**: this is design prose and canon review
  ([#271](https://github.com/TomiToivio/NooPunk/issues/271)). CI checks the loader's *behaviour*, not
  which factions exist or what they say.
- Invents **no exact date**; the setting is **20XX** (`AGENTS.md` §6) and the crossover begins during
  the acceleration toward the NHI Crisis, unresolved and undated (#306).
- Touches **nothing** in the legacy RPG; world lore carries over, legacy *rules* do not (#306).
