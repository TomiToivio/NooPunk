# Character cards

Reusable, data-driven game pieces for the digital tabletop: RPG characters, faction members,
encounters and investigations, and NHI worldbuilding. Cards are readable at a glance and
expandable in detail, and work in a UI or in text-first play.

**This layer is content and schema, not mechanics.** No statistic is derived, no roll is
compared, no effect is applied and no action is resolved. Gates A–D in
`docs/RULE_SYSTEM_RESEARCH.md` remain open, and `AGENTS.md` §4 reserves resolution, thresholds
and cadence to the author. `to_card()` leaves `prerequisites` and `effects` empty on purpose.

Code: `strategy_game/characters.py` · Content: `strategy_game/data/character_cards.json` ·
Tests: `strategy_game/tests/test_character_cards.py`

## One record, three families

There is one `CharacterCard` record with a `family` discriminator — not three card types.
Adding a card never means adding a class.

| family | what it is | lifecycle |
| --- | --- | --- |
| `canonical` | A unique, persistent, authored character: faction leader, patron, councillor, rival or contact. Canonical identities carry across campaigns; decisions and consequences change their game *state*, never their identity. Provenance `authored`; a stable id no generator may mint. | Never instanced. Must cite `sources`. Refused as an instantiation template. |
| `archetype` | A reusable, unnamed template: faction organizer, corporate security, netrunner, intelligence officer, researcher, activist, soldier, bureaucrat, journalist, commuter, shopkeeper, civilian witness. Provenance `generated`. | Instanced when it becomes important. The instance keeps its `template_id`, so promotion is by addition, never by cloning. |
| `nhi` | A game-facing exemplar of one of the four setting categories — a rendering of the human-facing understanding of an entity, **not a person card**. | Not instanced, and not a template for a person. |

Generic does **not** mean unpersoned. The setting is about who counts as a person, so a
commuter, a shopkeeper or a witness is meaningful to social and investigation play, not combat
filler. Generic means *the author did not name them*.

## Shared schema

Every card carries:

- `identifier` — a stable slug, unique in the roster.
- `family` — `canonical` / `archetype` / `nhi`.
- `display_name`, `role`, `summary` — the readable face.
- `faction_ids` — affiliations, validated against the known faction ids when supplied.
- `tags` — typed tags in issue #346's shared vocabulary: `belief`, `competence`, `equipment`,
  `relationship`, `asset`, `goal`. Occupation and social role live in `role`. On an **NHI card
  only `belief` tags are allowed**: a belief tag reads as *what humans believe about it*, while a
  `competence` or `equipment` tag would stat an entity the setting refuses to stat.
- `declared_actions` — optional labels from `investigation`, `influence`, `recruitment`,
  `espionage`, `field_operations`, `cyber`, `psi`, `combat`. Names only; nothing resolves one.
  **Forbidden on NHI cards**, where a stated capability is a human attribute line by another name.
- `observable_facts` — *what happened*. Evidence-shaped.
- `inferences` — *what a character concludes*. Attribution, never merged into the field above.
- `statuses`, `state` — declared progression fields (injury, loyalty, allegiance). Carried,
  never computed.
- `relationships` — ties to other cards by id and kind label.
- `visibility` — `public` / `private` / `concealed` (display policy; no rule reads it).
- `claim_status` — how well-established a claim is (below).
- `consciousness_status` — `unknown` (default) / `contested` / `asserted_in_world`. Never
  derived, and `asserted_in_world` requires a cited source, because the setting does not settle
  whether a being is conscious.
- `art_ref` — artwork kept outside the card, so placeholder art exists from day one.
- `provenance` — where the content came from, defaulting to `UNKNOWN` so an unrecorded origin
  stays visible instead of reading as fact.
- `sources`, `gm_notes` — citations for authored content, and an author-facing note.

## NHI classification: keep six things apart

An NHI card carries `category`, `form`, `species_ref`, `origin_hypotheses`, `allegiances` and a
certainty, and these are **never** collapsed into one another. A category is not a species, an
entity inside a category is not the category, and affiliation is not ontology — an Orion-aligned
Construct must stay representable without contradiction.

The classification is **derived from `data/codex.json`**, not asserted by a card author:

| card field | codex field |
| --- | --- |
| `category` | `ontology` — `biologic` / `construct` / `noetic` / `plasmoid` |
| `form` | `form` — species / polity / avatar / individual / vessel_or_technology / mythonym |
| `species_ref` | the codex entry `identifier` |
| `contested` | true when `alternative_ontologies` lists another reading |
| `claim_status` | `knowledge_status` |
| `reveal_stage` | `reveal_stage` |
| `origin_hypotheses` | `origin_claims`, quoted verbatim |
| `allegiances` | `faction_relationships`, quoted verbatim |
| `observable_facts` | `manifestations` and `phenotype`, quoted |

`validate(codex=…)` reports any card that contradicts its codex entry, omits the form, references
a species that does not exist, or lists an unknown faction id. So a card cannot promote a rumour
into canon, settle a contested classification, paraphrase an origin claim, or invent what was
seen. Classification may be provisional, contested or redacted — the exemplars include a
contested one on purpose, whose rival readings the codex keeps.

## Visibility and spoilers

Public information, player-known facts, GM-only secrets and uncertain claims are four readable
states. Claim statuses are `canon`, `player_known`, `reported_claim`, `rumour`,
`source_mythology`, `gm_truth` and `unknown`. Uncertain claims stay readable *because* the
setting is about living with uncertainty; `gm_truth` is redacted.

- `render_front(card)` prints the compact face and never prints `gm_notes`. An NHI card's front
  shows its **observable facts** while its identity stays unestablished.
- `render_detail(card, reveal_secrets=False)` prints `observable_facts` and `inferences` as two
  separate lists, withholds a redacted GM note behind `[redacted …]` until the caller asks, and
  expands codex lore with `gm_secrets` removed — the same rule as `Codex.player_view()`, so GM
  material is withheld by the code rather than by a renderer's good intentions.

## Using cards

```python
from strategy_game.characters import load_character_cards, codex_entry_map, render_front, render_detail, to_card

roster = load_character_cards()
codex = codex_entry_map()
roster.validate(codex=codex)                        # () when every card agrees with canon

roster.get("sir_mars_eldrich")                     # the canonical exemplar
roster.filter(family="nhi", category="plasmoid")   # four categories are covered
roster.filter(form="mythonym")                     # form is filterable too
roster.filter(faction="ulp", tag="competence")

netrunner = roster.instantiate("archetype_netrunner", display_name="Mika's Cousin")
netrunner.state["loyalty"] = "bought"              # declared, not computed

print(render_front(netrunner))
print(render_detail(netrunner, reveal_secrets=True))

card = to_card(netrunner)                          # the shared tabletop primitive
```

## Adding a card

1. Add an entry to `strategy_game/data/character_cards.json` (the loader checks `format` and
   `version`).
2. Give it a stable slug id, a family, and what that family requires: `sources` for canonical,
   `tags` for archetypes, a codex-derived classification (`category` **and** `form`) for NHI.
3. For canon, cite where it comes from — an issue number, a repo document, a codex identifier.
   Canon is never invented in a card, and an unresolved question stays unfilled (Sir Mars
   Eldrich's card leaves the Eldrich Island legal question open, because §324 records it as
   undefined).
4. Run the tests:

```bash
python3 -m unittest discover -s strategy_game/tests -p "test_*.py"
```

## Open for the author

- Whether the four NHI categories get their own `CardType` — this layer argues against, because a
  second card type per family is what "adding a card never means adding a class" forbids.
- Whether canonical leaders are ever instanced into another faction's deck.
- Whether a player may see that a card is *canonical*: if yes, players learn where the authored
  weight is; if no, the seam stays invisible.
- `TAG_SCOPES` in `data/faction_creation.json` has no scope for an entity card (it is `faction`,
  `character`, `organization`, `research`, `government`). Adding one — `nhi` or `entity` — is a
  vocabulary decision for the author; until then this layer enforces the restriction itself.

## Deliberately absent

No attribute, skill value, target number, modifier, difficulty, threshold, cost, cadence, win
condition or effect application — and no human attribute line on an entity card. `to_card()`
produces a `persistent_record` character card with empty mechanic slots, and the data file is
checked for mechanic-looking keys. Turning any of this into a rule is gated work, and the design
record for it lives in `docs/RULE_SYSTEM_RESEARCH.md`.
