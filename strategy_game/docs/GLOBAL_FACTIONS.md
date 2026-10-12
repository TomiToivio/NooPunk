# Global paradigm factions — author taxonomy (issues #328 and #329)

**Status: author canon, and no rules.** The roster below is the author's, condensed from
[#328](https://github.com/TomiToivio/NooPunk/issues/328) and
[#329](https://github.com/TomiToivio/NooPunk/issues/329). The machine-readable form is
[`../data/global_factions.json`](../data/global_factions.json), read by
[`../factions.py`](../factions.py). **No mechanics, statistics, thresholds or simulation rules are
implemented here** — #329 §5.7 asks for simulation rules to be proposed and reviewed before any
implementation, and `RULEBOOK.md` still says *NO RULES APPROVED*.

**One roster, not two.** #328 and #329 state the same seven factions under different names. This
document reconciles them into a single list, prefers **#329's** naming where the two differ, and
cites both per entry. It deliberately does *not* create a second competing roster.

## 1. The roster

| # | Faction | Kind | Economic | Social | NHI posture | PSI posture |
|---|---|---|---|---|---|---|
| A | **Accelerationists** — *the Extraterrestrial Free Market* | human formation | extreme right / market-libertarian | tactically right-populist (internally libertarian) | open markets, Extraterrestrial Economic Zones, commercial treaties | patent and monetise; "consciousness-as-a-service" |
| B | **Cyborgists** — *Conscious Agency and the Noösphere* | human formation | left | liberal / solidaristic | careful, compassionate diplomacy **plus** Dark Forest defence | a natural human capacity; train, ensure access, prevent coercion |
| C | **Critical** — *Anti-Colonial Inquiry and Equality* | human formation | left | liberal / progressive | anti-speciesist, and sharply critical of colonial extraction | initial scepticism → possible Archaic Revival |
| D | **Doomers / Butlerian Jihad** — *Humanity First at Any Cost* | human formation | biocentric, not economically defined | conservative / often right-populist | Dark Forest: strike first or be extinguished | infiltration, witchcraft, psychic weapons |
| E | **Confederacy Awakening** — *Galactic Ascension Movement* | NHI-aligned | spans | spans | join a compassionate federation — or *Childhood's End* | awakening in a large segment of the population |
| F | **Orion / Grey Collaborative and Infiltration Networks** | NHI-aligned (covert) | — | — | covert hybridisation, caste structures, manipulation | PSI as a control channel |
| G | **Normalcy Bloc** — *1999 Forever* | latent public | — | — | cannot process the shift | cannot process the shift |

## 2. Three kinds of entity, not one list

#329 §4.2 is the structural ruling: *"Human factions, alien factions, movements, institutions and
latent publics are different kinds of entities. A global ideology can influence a local political
party without replacing it."* The roster's own blanks are the evidence — E spans both axes, F and G
have neither:

- **human ideological formation** (A–D) — the stratum with compass coordinates and paradigm stances;
- **NHI-aligned formation** (E, F) — an external power and/or its human supporters, a different
  entity kind;
- **latent public / sociological tendency** (G) — #329 §3.G: *"do not make it a single organised
  party; treat it as a cross-faction sociological tendency / latent constituency."*

## 3. The compass is two dimensions short of the roster

#327 warns the four AI stances are *"issue frames, not political parties and not a tidy single
left/right scale"*, and #329 §4.1 answers it directly: keep the 2026 economic and cultural compass,
and **separately** encode each actor's stance to AGI, PSI, NHI and Confederacy accession plus
sovereignty/agency/consent — *"These are not deterministically deducible from one another."*

That separation is load-bearing, not bookkeeping. **Cyborgists (B) and Critical (C) land in the same
compass cell** — left/liberal both — and they are the author's first- and second-favourite factions.
What distinguishes them is entirely on the third dimension: B augments and is optimistic about
interoperating with AGI/PSI/NHI; C is sceptical of AI's benefits and reads technocapitalism and NHI
caste structures as domination. A two-axis compass cannot tell them apart.

So the model is **compass (2) + paradigm stance (1)**, orthogonal. The declared paradigm positions
are in `factions.PARADIGM_STANCES`.

### 3.1 Examples that keep the mapping non-deterministic (from #327 and #328)

The author's own named crossings, retained precisely so no one collapses stance into compass:

| Example | Compass | Paradigm stance |
|---|---|---|
| transhumanist but AI-safety-conscious | left / liberal | augment **and** guard |
| economically left but technologically accelerationist | left | accelerationist |
| conservative but pro-military AI | right / conservative | pro-AGI for security |
| libertarian self-description, populist-right practice | libertarian claim → right-populist reality | accelerationist |
| anti-speciesist left that is critical of AI's benefits | left / liberal | Critical |

## 4. Evidence and knowledge model (#329 §5.4)

The author's rule: **never encode propaganda as automatically true.** The categories are objective
in-world facts, disclosed facts, allegations, misinformation, mind control and player-accessible
clues, and the game must distinguish what the game master knows from what factions assert.

That maps onto the repository's existing provenance discipline without new machinery:

| Category | Provenance |
|---|---|
| objective in-world fact | `EVIDENCE` (within the fiction) |
| author-set setting canon | `AUTHORED` |
| a faction's assertion, propaganda, rumour | **not** `EVIDENCE`; recorded as that faction's claim |
| game-generated outcome | `SIMULATED` |
| unclassified or unverified | `UNKNOWN` — the default, never silently promoted |

Consequence worth stating plainly: a faction's PSI/NHI posture **is a belief it holds**, not a claim
the game makes. The Critical faction's guardrail — that blonde/blue-eyed Pleiadian iconography must be
critiqued as *symbolism and racialised reception*, never phenotype as proof of character — is then a
property of the fiction's politics rather than something the game asserts about NHI. The same holds
for the author's recorded verdict that the Accelerationists are "the enemy of humanity": that is
`AUTHORED` framing, not a score the engine computes.

## 5. Ukweli party mapping (#329 §5.6)

Per #329 §5, the MVP keeps its **single-city/Ukweli opening, three local parties and modest leader
roster**; the global factions arrive as tags, event cards, world news, NHI offers, economic pressure
and NPC affiliations — *not* as seven additional national parties.

| Ukweli party | Role | Nearest global current |
|---|---|---|
| Ukweli Communist Party | incumbent national-liberation government | C, with A's economic pressure |
| Identity Party | tribalist / rural populist | D |
| Libertarian Party | small anarchocapitalist accelerationist minority | A |

Parties **borrow** factions' discourse without being identical to them. Which party articulates which
global current — and when that articulation breaks — is the playable question inside the MVP.

## 6. Event-card seeds (#329 §5.5)

The author names eleven; recorded as the authored seed list, with the cards themselves still a design
deliverable:

alien economic zone proposal · PSI-as-a-service IPO · billionaire hybrid rumours · awakening
epidemic · Confederacy accession terms · sphere-network data scandal · Butlerian Jihad raid ·
religious schism · psychic-privacy bill · world government debate · "nothing to see here" media cycle

## 7. Where this meets existing lore

World lore carries over (#306); legacy *rules* do not. The material already exists — cite it rather
than re-deriving it:

- `rulebook_parts/07_lore_and_world.md` **§33.2** already names the Accelerationist, Cyborgist,
  Critical AI and existential-risk positions, and adds the caution the roster must respect:
  *"accelerationisms rather than one doctrine"* — so A is at least two currents, not one.
- **§33.3** already defines the Butlerian Jihad, and is more careful than a single row: *"It is not
  one monolithic organization"*, spanning bioconservatives, religious traditionalists, militants and
  states. That spectrum is the playable ladder.
- **E** leans on §33.6 (PSI/QIP/awakening/Noösphere), §33.8 (the Zoo), §33.9 (Zookeepers and probes),
  §33.11 (Pleiadians, Atlantis), §33.14 (end of quarantine, Day of Disclosure), §33.15 (VALIS).
- **F** leans on §33.6b (rogue machine lineages, Von Neumann threat), §33.12 (Greys, future humans),
  §33.13 (hybridisation, Fourth-Density).
- The legacy faction model (`data/world/faction_taxonomy.json`, #144) already declares `nhi` as a
  faction type with its own `nhi_extra_schema`, and records two rules this roster should not
  contradict silently: **`faction_is_umbrella_concept`** and
  **`type_does_not_determine_political_allegiance`** — the latter matters because splitting NHI into
  a benevolent and a malevolent bloc implies NHI-ness predicts ethics. If that is the author's
  deliberate override, it should say so; otherwise F needs a non-NHI differentiator.

## 8. Open questions carried, not answered

The eight unresolved items travel in `data/global_factions.json` under `open_questions` and are
exposed as `FactionRoster.open_question_ids`, so code never silently decides an author question.
They are: is the roster closed at seven; is F playable, a threat, or both; are A and F one faction
with two wings or two with a dependency; does G have agency; how far along D's escalation ladder may
the game begin (#306 forbids starting with the crisis resolved); the real-person policy; whether this
placement overrides or sits alongside #327's compass; and **which issue owns the canonical names**,
since #328 and #329 disagree.

## 9. Not done here, deliberately

- **No simulation rules.** #329 §5.7 requires them to be proposed and reviewed first; #297 owns the
  lightest rules, and this document adds none.
- **No mechanics, numbers or scores** — the roster is described, not rated, and a test enforces that
  no numeric quantity enters a faction record.
- **No lore-file edits.** #329 §5.8 defers documentation updates until agreement; the legacy
  rulebook and `rulebook/` chapters are untouched.
- **No tests of the roster's content.** Per #271, CI checks the loader's behaviour, not which
  factions exist or what they say.
