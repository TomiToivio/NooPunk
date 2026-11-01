# Helsinki slang and NoöPunk universe glossary (MUD)

**Editorial boundary:** This is a glossary of *terms already known in the world or proposed for Tomi's review*. AI agents document meanings in English only. Entries below are word references, **not agent-authored Finnish dialogue, translated lines, or approvals of any Finnish wording**. Tomi controls and authors his own Finnish/Finglish passages and may add examples in his own voice. For player-visible MUD prose only, agents may reuse verified glossary headwords or brief simple Finnish expressions sparingly within English text; this does not authorize modifying Tomi's passages. Internal documentation remains English. See [the binding policy](../FINNISH.md).

**One language, no editions (#996).** NoöPunk ships in canonical Finglish. This glossary exists so that
vocabulary can be *understood*, not so that the game can be translated. Nothing here authorizes a Finnish or
English localization.

## Provenance, and what an agent may claim

Every entry carries a provenance. The distinction is not decoration: an agent must never present a guess as
authentic slang or invention as etymology.

| Provenance | Means | Requires |
| --- | --- | --- |
| `attested` | documented contemporary or historical usage | a **source**; the loader refuses the entry without one |
| `author_neologism` | a term Tomi coined for NoöPunk | his authorship |
| `proposed` | recorded for consideration, not yet canon | nothing — but must not be described as established |

Slang entries below are marked `attested` on the strength of Tomi's own statement in this file ("existing
Helsinki slang"). Universe terms are `proposed` until Tomi attributes them, because an agent cannot certify
that a setting word was coined rather than borrowed.

## Authoring glossary

| Term | English gloss | Register | Provenance | Source / note |
| --- | --- | --- | --- | --- |
| Stadi | Helsinki, colloquial city name | street | attested | Tomi-approved here: "existing local slang" |
| spora | tram | street | attested | Tomi-approved here: "existing Helsinki slang" |
| dösä | bus | street | attested | Tomi-approved here: "existing Helsinki slang" |
| steissi | railway station | street | attested | Tomi-approved here: "existing slang" |
| kundi | guy or young man | street | attested | Tomi-approved here: "existing slang" |
| tsiga | cigarette | street | attested | Tomi-approved here: "existing slang" |
| mutsi | mother | street | attested | Tomi-approved here: "existing slang" |
| faija | father | street | attested | Tomi-approved here: "existing slang" |
| hima | home | street | attested | Tomi-approved here: "existing slang" |
| dokata | drink alcohol | street | attested | Tomi-approved here: "existing slang" |
| fyrkka | money | street | attested | Tomi-approved here: "existing slang" |
| duuni | work or job | street | attested | Tomi-approved here: "existing colloquialism" |
| snadi | small | street | attested | Tomi-approved here: "existing slang" |
| jees | okay / nice | street | attested | Tomi-approved here: "existing colloquialism" |
| niinku | conversational filler, roughly 'like' | street | attested | Tomi-approved here: "existing colloquialism" |
| Finglish | code-switching between Finnish and English | authorial | author_neologism | Tomi's term for the game's voice; never enforce a percentage |
| Stadin slangi | the Helsinki urban slang tradition | dialect | attested | Named tradition, cited here by Tomi |
| Noösphere | emerging collective psychic consciousness, partly mediated by networks | canon | proposed | Universe term; coinage to be attributed by Tomi |
| ontological shock | crisis of assumptions about reality | canon | proposed | Theme; player knowledge gated |
| BCI | brain-computer interface | technical | proposed | Setting usage; generic abbreviation |
| psychotronics | psi-linked technological practice | technical | proposed | Late-stage lore gate |
| UNSA | global human-security agency | institutional | proposed | Setting term |
| Supo | Finnish security intelligence service | institutional | attested | Real institution |
| Europol | European policing cooperation agency | institutional | attested | Real institution |
| NHI | non-human intelligence | canon | proposed | Classified until disclosed |
| Pleiadian | NHI-related designation | canon | proposed | Classified world lore |
| Construct | synthetic or instantiated being in the setting | canon | proposed | Reveal only as encountered |
| Zookeeper | nickname for a collective-consciousness NHI faction | canon | proposed | Classified faction slang |
| cyberdeck | computing/hacking equipment | technical | proposed | Established genre word |
| cyberspace | connected digital environment | technical | proposed | Established generic genre vocabulary |

## Player dictionary (#996)

The glossary is for authors. Players get the in-game **`dictionary`** / **`lexicon`** command, backed by
`mud/nopunk_mud/lexicon.py` and `data/world/lexicon.json`.

- **Gloss, not translation.** Each entry explains a term in a line or two of English. It never carries
  translated scene text, and the dictionary is not a parallel language edition.
- **Provenance is shown.** A player sees "attested usage", "NoöPunk coinage" or "provisional term", so the game
  never passes a guess off as established slang.
- **Spoilers stay shut.** `public` entries are readable from the start; `dossier` entries unlock with progress.
  A locked entry answers exactly as an unknown one does, so the refusal cannot confirm that a secret exists.
- **Deterministic and offline.** No model is consulted; identical input gives identical output. The dictionary
  works with Concordia switched off, like the rest of the solo campaign.

Seeded entries are deliberately all `proposed` — an agent may not assert attested usage. Tomi upgrades an entry
by confirming its provenance and supplying a source; that is the only path from proposal to canon.

## For agents

Record provenance for every new term. Consult Tomi-authored content for speaker-appropriate vocabulary before
reuse. Russian, Chinese, Swedish and other loanwords can appear occasionally in player-facing English-led
Finglish when the situation makes them natural — but no automatic translation, no unverified claim of authentic
slang, and no reproduction of distinctive Nadsat inventions or dialogue.
