# Glossary

The official language of NoöPunk is Finglish as spoken in the Helsinki area ("Stadin Slangi"). This glossary contains NoöPunk terminology and common Stadin Slangi expressions. Some of these expressions are real-world Stadin Slangi, some are Nadsat-like language invented for NoöPunk. Note that this is based on modern 21st century Stadin Slangi, not the original version from 20th century. Stadin Slangi and Nadsat are actually quite similar, both have numerous Russian words. 

**This file is the vocabulary source of truth (#1000).** The in-game `dictionary` is generated from it by
`tools/glossary_to_lexicon.py`; do not maintain a second hand-written word list. Definitions below are Tomi's
and are preserved verbatim.

## Headwords

* Bonjata - to understand
* Bönde - Finland that is not Helsinki
* Crusti - crust punk
* Diili - deal
* Dokata - to drink alcohol
* Dänkki - cannabis
* Fiilis - feeling
* Frendi - friend
* Fyrkka - money
* Jepari - cop
* Kännykkä - mobile phone
* Kyttä - cop
* Landepaukku - person who lives outside of Helsinki
* Leffa - movie
* Mesta - place
* Narkata - to use drugs
* Narkkari - junkie
* Nisti - junkie
* Hiisata - to smoke cannabis
* Pummi - bum
* Punkkari - punk rocker
* Rafla - restaurant
* Sika - cop
* Skoude - cop
* Stevari - corporate cop
* Venaa - wait
* Wallah - I swear

## Migrated from the older secondary glossary

These came from `docs/world/HELSINKI_SLANG_GLOSSARY.md`, which is retained only as a pointer to this file. They
are listed here so no vocabulary was dropped in the merge; the definitions are the ones already in the
repository, not new invention.

* Stadi - Helsinki, colloquial city name
* spora - tram
* dösä - bus
* steissi - railway station
* kundi - guy or young man
* tsiga - cigarette
* mutsi - mother
* faija - father
* hima - home
* snadi - small
* jees - okay / nice
* niinku - conversational filler, roughly 'like'
* Finglish - code-switching between Finnish and English
* Stadin slangi - the Helsinki urban slang tradition
* Mä vannon! - I swear!
* Suomi Perkele Saatana! - an emphatic exclamation invoking Finland and Finnish swearing

## Universe and technical terms

* Noösphere - emerging collective psychic consciousness, partly mediated by networks
* ontological shock - crisis of assumptions about reality
* BCI - brain-computer interface
* psychotronics - psi-linked technological practice
* UNSA - global human-security agency
* Supo - Finnish security intelligence service
* Europol - European policing cooperation agency
* NHI - non-human intelligence
* Pleiadian - NHI-related designation
* Construct - synthetic or instantiated being in the setting
* Zookeeper - nickname for a collective-consciousness NHI faction
* cyberdeck - computing/hacking equipment
* cyberspace - connected digital environment

## Classification

Every headword above needs exactly one row here: category, provenance, register, spoiler tier, and a note for
gated terms. `tools/glossary_to_lexicon.py --check` fails if a headword is missing, if a row names a term that
is not a headword, or if a gated term does not say when it unlocks.

Category values: `attested_modern` (current Stadin slangi), `attested_older`, `real_borrowing`,
`noopunk_slang` (futuristic invented slang), `universe` (NoöPunk terminology).
Provenance: `tomi` (supplied or approved by Tomi), `documented` (real, checkable usage), `agent_proposed`.

| Term | Category | Provenance | Register | Spoiler | Note |
| --- | --- | --- | --- | --- | --- |
| Bonjata | attested_modern | tomi | street | public | |
| Bönde | attested_modern | tomi | street | public | |
| Crusti | attested_modern | tomi | subculture | public | |
| Diili | attested_modern | tomi | street | public | |
| Dokata | attested_modern | tomi | street | public | |
| Dänkki | attested_modern | tomi | street | public | |
| Fiilis | attested_modern | tomi | street | public | |
| Frendi | attested_modern | tomi | street | public | |
| Fyrkka | attested_modern | tomi | street | public | |
| Jepari | attested_modern | tomi | street | public | |
| Kännykkä | attested_modern | tomi | everyday | public | |
| Kyttä | attested_modern | tomi | street | public | |
| Landepaukku | attested_modern | tomi | street | public | |
| Leffa | attested_modern | tomi | everyday | public | |
| Mesta | attested_modern | tomi | street | public | |
| Narkata | attested_modern | tomi | street | public | |
| Narkkari | attested_modern | tomi | street | public | |
| Nisti | attested_modern | tomi | street | public | |
| Hiisata | attested_modern | tomi | street | public | |
| Pummi | attested_modern | tomi | street | public | |
| Punkkari | attested_modern | tomi | subculture | public | |
| Rafla | attested_modern | tomi | street | public | |
| Sika | attested_modern | tomi | street | public | |
| Skoude | attested_modern | tomi | street | public | |
| Stevari | attested_modern | tomi | street | public | |
| Venaa | attested_modern | tomi | street | public | |
| Wallah | attested_modern | tomi | urban | public | |
| Stadi | attested_modern | documented | street | public | |
| spora | attested_modern | documented | street | public | |
| dösä | attested_modern | documented | street | public | |
| steissi | attested_modern | documented | street | public | |
| kundi | attested_modern | documented | street | public | |
| tsiga | attested_modern | documented | street | public | |
| mutsi | attested_modern | documented | street | public | |
| faija | attested_modern | documented | street | public | |
| hima | attested_modern | documented | street | public | |
| snadi | attested_modern | documented | street | public | |
| jees | attested_modern | documented | street | public | |
| niinku | attested_modern | documented | street | public | |
| Finglish | universe | tomi | authorial | public | Tomi's term for the game's voice |
| Stadin slangi | attested_modern | documented | dialect | public | Named tradition |
| Mä vannon! | attested_modern | tomi | urban | public | |
| Suomi Perkele Saatana! | attested_modern | tomi | exclamation | public | |
| Noösphere | universe | agent_proposed | canon | gated | Unlocks once the player has met the concept in play; it is the central revelation, not vocabulary |
| ontological shock | universe | agent_proposed | canon | gated | Unlocks after the first paradigm break the player experiences firsthand |
| BCI | universe | agent_proposed | technical | public | |
| psychotronics | universe | agent_proposed | technical | gated | Unlocks once the player meets psi technology in play |
| UNSA | universe | agent_proposed | institutional | public | |
| Supo | universe | documented | institutional | public | Real institution |
| Europol | universe | documented | institutional | public | Real institution |
| NHI | universe | agent_proposed | canon | gated | Unlocks after first confirmed non-human contact |
| Pleiadian | universe | agent_proposed | canon | gated | Unlocks with the later NHI disclosures |
| Construct | universe | agent_proposed | canon | gated | Unlocks when the player encounters one |
| Zookeeper | universe | agent_proposed | canon | gated | Unlocks when the faction is named in play |
| cyberdeck | universe | agent_proposed | technical | public | |
| cyberspace | universe | agent_proposed | technical | public | |

### Known gap, stated rather than guessed

Tomi's introduction says *some* of these expressions are invented for NoöPunk and some are real Stadin slangi,
but does not say which. They are all classified `attested_modern` because he supplied them as glossary
headwords and his introduction calls the base modern Stadin slangi. If any is in fact a NoöPunk invention, its
category should become `noopunk_slang` — an agent must not make that call, because guessing an etymology is
exactly what this file forbids.
