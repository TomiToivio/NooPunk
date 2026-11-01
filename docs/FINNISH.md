# NoöPunk language policy — Finnish-first MUD, English-only agents

**Status:** canonical for the MUD. Consolidates issues **#980**, **#981** and the earlier notes in this
file. Rules text and repository documentation remain English.

**Scope:** the Evennia MUD's player-facing UI, dialogue, narrative, quests and story. Not the tabletop
rulebook, not GitHub issues, not code comments, not design docs.

## 1. The rule in one paragraph

The finished MUD is **Finnish-first**. **Tomi writes the Finnish dialogue and story** in his own
Helsinki voice. **Agents write English only — never Finnish, never machine-translated Finnish, never
an imitation of Tomi's voice.** During development the Finnish build is deliberately mixed: Tomi's
Finnish plus agents' English placeholders awaiting his adaptation. That mix is allowed and is not a
bug. A proper English localization is a later, separate edition.

## 2. Who writes what

| Who | Writes | Must not |
|---|---|---|
| **Tomi** | Finnish dialogue, story, UI copy, slang, final phrasing and terminology | — |
| **Agents** | English source lines, stable content keys, English definitions, code, tests, docs | Write Finnish prose; translate into Finnish; "fix" Tomi's Finnish; overwrite Finnish with English |
| **Reviewers** | Check the policy, keys and fallbacks | Approve agent-authored Finnish as canon |

Agents may quote Tomi-authored Finnish verbatim when referencing an existing string, and may record
Finnish glossary headwords that Tomi has supplied. Quoting is not authoring.

## 3. Voice

Finnish should sound like **Tomi talking**, not literary Standard Finnish:

- **Stadin Slangi** and **Finglish**, with Russian loanwords; roughly half English in ordinary speech
  is normal, not a failure.
- Register shifts by speaker: street, academy, bureaucratic, UNSA/military, corporate, online youth,
  cultic/Noösphere.
- **Nadsat** and **Doublespeak** are inspirations for texture (Russian loans; institutional
  euphemism), never sources to copy. Do not reproduce distinctive passages or invented vocabulary.
- Bureaucratic language may conceal horrifying facts; that is a feature.
- Established genre words such as *cyberspace* are ordinary vocabulary, not plagiarism.

English working text should be plain and translatable. Do not fake Finnish word order or invent
slang. Where code-switching must survive translation, note it on the key, not by writing Finnish.

## 4. Mixed build and fallback behaviour

- Every player-facing string has a **stable key**, a `lang` (`fi` / `en`), an author and a status:
  `tomi_finnish`, `english_placeholder`, `approved_english`.
- The MUD renders Finnish when it exists; otherwise it renders the English placeholder **visibly
  marked** (for example a leading `[EN]` or a UI locale badge). It never silently pretends English is
  Finnish.
- **Finnish content is never overwritten by an English fallback.** Missing English is acceptable;
  missing Finnish is expected until Tomi writes it.
- Content IDs, flags, choices and quest state are language-neutral, so saves survive localization.
- UTF-8 everywhere; Finnish characters (`ä`, `ö`, `å`) must round-trip through data files and tests.

## 5. Glossary

A living glossary lives at [`docs/world/HELSINKI_SLANG_GLOSSARY.md`](world/HELSINKI_SLANG_GLOSSARY.md).

- Tomi supplies or approves Finnish headwords, inflections and examples.
- Agents write **English definitions, register notes and usage guidance only**; Finnish example
  fields stay empty until Tomi fills them.
- Distinguish attested Stadin Slangi from invented NoöPunk slang and from literary inspiration.
- The glossary is a reference, not a spellchecker or a prescription for every sentence.

## 6. Narrative disclosure: grounded first, New Weird later

The player should initially believe this is a grounded cyberpunk / Nordic-European social-SF
investigation: a rookie UNSA agent, institutional secrecy, local crime, cyberware, AI-generated media,
ubiquitous AR/VR and political tension. The wilder setting arrives through evidence, not exposition.

- **Early:** mundane explanations remain available. No lore dumps, no omniscient narrator, no
  encyclopedia screens.
- **Middle:** the Noösphere, PSI and NHI become undeniable to the player while remaining deniable to
  most of society.
- **Late:** the NHI Cold War, the nature of the Noösphere and what UNSA actually knows.
- **Knowledge is diegetic:** places, clues, dossiers, contradictions, NPC motives and choices. Keep
  character knowledge separate from world canon.
- **UNSA is not omniscient.** Romppainen knows more than rookies and deliberately doses disclosure;
  senior officials also lack the full picture.

### Population response (setting heuristic, not forced NPC psychology)

- **50 %** cannot or will not switch paradigm, even with a craft on the lawn. This is the recurring
  *Don't Look Up* comedy.
- **25 %** go doomer: extremist anti-NHI/anti-AGI movements, survivalism, Mad Max.
- **25 %** go accelerationist: cyborgization, uploading, alien cults, joining the new powers.

Governments classify to avoid panic. Ubiquitous AR/VR is entangled with the psychic Noösphere, and
people dismiss real weirdness as AI slop or misinformation. Society still functions because most
people refuse to update.

### The Noösphere and UNSA

- The **Noösphere** is the natural psychic collective consciousness of a sane planet. Humans are not
  the sanest species and need BCIs, LLM augmentation and global cybernetic VR/AR to reach it.
- It is only becoming conscious, and an ideological struggle is underway inside it. It appears purely
  technological until the player reaches a level of psychic awakening; it is a psychic maelstrom,
  not a network.
- **UNSA** was founded on transparency, open science and democratic participation, and believes in
  them. It also classifies the most destabilising information and fears becoming another MJ-12 while
  becoming the de facto global government.
- **Player character:** a blank-slate academy graduate. Idealistic, humanitarian, empathetic,
  cynical, heroic, compromised, corrupt, traitorous or addicted trajectories are all playable; none
  is the default.
- **Theme:** Ontological Shock, Paradigm Shift and the Noösphere. Even UNSA is not sure what is going
  on.

## 7. Implementation requirements

- [x] Locale-aware string layer (`mud/nopunk_mud/localization.py`): stable keys, `fi`/`en`, author and
  status, visible fallback, refusal to let an agent author Finnish, refusal to overwrite Finnish with
  English.
- [ ] Migrate MUD UI/dialogue strings to keys; no hardcoded English in a Finnish-labelled screen.
- [ ] Story/dialogue files record `lang` per line or node; mixed scenes only as authored
  code-switching.
- [ ] Seed the glossary; Tomi fills Finnish examples.
- [ ] Write the reveal ladder as a scene/act document with gates.
- [ ] First playable act contains no unambiguous aliens, AGI apocalypse or Noösphere explanation.
- [ ] Tomi reviews all Finnish; no agent PR may claim Finnish localization.

## 8. Acceptance criteria

1. Finnish UI/story renders where Tomi has written it; English is visibly marked elsewhere.
2. No agent-authored commit contains Finnish prose beyond quoted or approved glossary terms.
3. The glossary exists, is used consistently and separates attested slang from invention.
4. The reveal ladder is documented and the first act respects the grounded tone.
5. The theme is playable, not lore-dumped.

## 9. Links

- **#950** — MUD is the main game; this is its language and disclosure contract.
- **#980 / #981** — source issues consolidated here.
- **#897** — CWN/art lock; language does not change rules.
- **#920** — Tony, Laura, Romppainen; their voices must fit their registers.
- **#921 / #922** — Crisis history and NHI factions; disclosure rules constrain surfacing.
