# Kieli — NoöPunkin kielipolitiikka / the NoöPunk language policy

**Status: binding.** This file is the single source of truth for language in the NoöPunk MUD. It merges
#980 and #981 into one contract. Where this file and any other document disagree, this file wins.

**Scope:** the MUD's user interface, dialogue, quests and story. The rulebook, `RULEBOOK.md`, design docs,
code comments, commit messages, issues and agent instructions stay **English**. This is not a
repository-language change; it is a game-content decision.

*Finglish note: the first version of NoöPunk is deliberately a mix — Tomi's Finnish and the agents'
English — and roughly half of real spoken Finglish is English anyway. Finnish headings and terms, English
working text. A mixed build is the intended first version, not a defect.*

---

## 1. Kuka kirjoittaa mitä / who writes what

| Who | Writes | Never writes |
|---|---|---|
| **Tomi** | Finnish dialogue, story, UI phrasing, slang, in-world terminology | — |
| **Agents** | English only: working text, keys, code, docs | Finnish prose, approximate Finnish, machine translation, imitations of Tomi's voice |

- **Suomi on MUD:n ensisijainen kieli.** English is a working language during development and a proper,
  edited English localization is a **later** deliverable.
- **Agents write only English.** Not "mostly English", not "English with Finnish flavour". If an agent
  cannot express something without inventing Finnish, it writes the English and leaves a note on the key.
- **Tomi is the final editorial authority** on Finnish phrasing, slang, register and characterization.
- **Existing Tomi-authored Finnish is preserved verbatim.** Agents may reference it by key; they do not
  rewrite, "improve" or normalize it.
- **The mix is permitted and expected.** Finnish where Tomi has written it, English where an agent has.
  Do not auto-translate the English. Do not block a playable feature because strings are still English.

The mechanical form of this rule lives in `mud/nopunk_mud/strings.py`: an entry whose status is
`english_placeholder` **cannot** carry Finnish, and `mud/tests/test_strings.py` proves it.

## 2. Ääni / the voice

Tomi writes **like he talks**: Stadin slangi mixed with Finglish, roughly half English in ordinary speech,
with Russian loanwords arriving naturally from Stadin slangi — which is why it sits so close to *Nadsat*.
Bureaucratic newspeak and Doublespeak belong to the institutional voices (UNSA, Supo, Europol, corporate
comms). None of this is a failure to translate; it is the register of the setting.

Guidance for the English an agent writes:

- Keep it **plain and translatable**. Do not fake Finnish word order; do not sprinkle invented slang.
- Mark **code-switching that must survive translation** (a character deliberately using an English
  technical term) in the key's `notes`, not by inventing Finnish.
- Name the **register** — street, academy, bureaucratic, clinical, cultic, corporate — so Tomi knows what
  he is writing into.

## 3. Merkkijonot / the string contract

Player-facing text is externalized from day one. State machines and quests reference **keys**, never text.

- **Stable, language-neutral keys** — `scene.helsinki.steissi`, not `Ratikka rämisee`. Renaming nothing in
  the data lets a save survive localization.
- **`fi` and `en` fields**, plus a **status**: `tomi_finnish` (Tomi wrote it), `english_placeholder`
  (agent text awaiting Tomi), `approved_english` (the later edited localization).
- **Safe fallback**: when `fi` is empty, the player sees `en` and the result is flagged as a fallback.
- **A fallback never overwrites `fi`.** Displaying English must not backfill the Finnish column, and an
  English placeholder is never promoted to Finnish by being shown.
- **UTF-8 throughout**: `ä ö å š ž` survive storage and round trip.
- `pending_finnish()` is the translation queue and `coverage()` reports the mix, so progress is measured
  rather than guessed.

## 4. Sanasto / glossary

A living glossary of Helsinki slang and NoöPunk terminology, seeded in `data/world/finnish_glossary.json`.
Seed terms include *Stadi, spora, dösä, steissi, kundi, tsiga, mutsi, faija, hima, dokata, fyrkka, duuni,
snadi, jees, niinku* alongside game terms such as *Noösphere, ontological shock, BCI, psychotronics, UNSA,
Supo, Europol, NHI, Pleiadian, Construct, Zookeeper, cyberdeck*. Terms are **data**, not prose: each entry
carries the term, its register, a plain English gloss and the Finnish usage note Tomi supplies.

Words like *cyberspace* have been used in the wild for decades — no William Gibson anxiety required.

## 5. Maailma / the world, revealed gradually

The NoöPunk future contains so many **ontological shocks** that it has to arrive slowly. The player should
begin believing this is a fairly realistic mix of cyberpunk and Finnish/Nordic/European social science
fiction, and only later discover the wilder science fiction and fantasy underneath.

- **Most people cannot process the shocks**, and there is a permanent *Don't Look Up* comedy to it. About
  **50%** cannot switch paradigm even if a saucer lands on the lawn.
- **25%** go full doomer and drift toward anti-NHI/anti-AGI extremism, or simply Mad Max.
- **25%** go accelerationist: cyborgs, alien cults, or both.
- Government — UN, EU, Finland — would rather not cause panic and classifies as much as it can. Ubiquitous
  AR/VR has fused with the psychic Noösphere, so the population usually files the weirdness under
  *AI slop* or *misinformation*. That is why society still functions.
- **The player character starts blank**, with room to become idealistic, humanitarian, empathetic,
  cynical, heroic, traitorous, dirty, corrupt or addicted. Ideally the player thinks this is a standard
  Blade Runner scenario at first.
- **The theme is ontological shock, paradigm shift and the Noösphere** — even UNSA is not entirely sure
  what is going on. Veterans like Romppainen know more than they say, and will not destabilize a rookie
  agent too fast.
- **The Noösphere** would be an ordinary psychic collective consciousness on a sane planet. Humans are not
  the sanest species around and need their BCIs, LLM augmentation and global cybernetic VR/AR networks to
  reach it. It is only now becoming conscious, and an ideological struggle is under way: a psychic
  maelstrom that looks entirely technological until the player reaches some level of psychic awakening.
- **UNSA** is the global agency for human security and survival, founded on transparency, open science and
  democratic participation — and it does believe in those things. It also learned very quickly to keep the
  most destabilizing information extremely classified, and it fears becoming another MJ-12 while becoming
  the de facto global government.

## 6. Mitä tämä tarkoittaa agentille / what this means for an agent

1. Read this file before writing any player-facing text.
2. Write English. Use a stable key. If Finnish seems necessary, it is not yours to write — leave a note.
3. Never edit Tomi's Finnish, and never let a fallback overwrite it.
4. Keep rulebook and repository documentation in English.
