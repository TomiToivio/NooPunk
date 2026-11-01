# The Romppainen–Fujita psychotronic empathy device

**Status:** author-approved device name and collaborator (#985). The game has one canonical Finglish language (#996); agents use English-led Finglish in player-visible text, and preserve all Tomi-authored dialogue verbatim. Non-player-facing documentation is in English.

## Origin

The **Romppainen–Fujita device** was built by **Dr. Harri S. Romppainen** and his former lover and scientific collaborator **Dr. 愛 Fujita**. Romppainen is an UNSA Supervisory Special Agent (SSA), psychologist and, apparently, also qualified as a psychiatrist, neuroscientist and psychotronics engineer. Do not invent explanations for his unusually broad credentials. Dr. 愛 Fujita is a distinct NoöPunk character, not the *Maniac* character Azumi Fujita.

The apparatus is used **only by the Helsinki UNSA Field Office**. Administrator **and** subject must each wear an enormous, rather goofy psychotronic helmet. Retro amber/violet lights blink; it beeps and hums in ways that make an uncomfortable examination briefly resemble a children's science exhibition. The comedy masks a legitimate psychotronic risk: field agents often feel peculiar after repeated tests. **Four assessments per field agent per in-world day** is the hard maximum.

The Evennia command is `assess status`, `assess equip` (helmets on both parties), and `assess run`. Each successful run consumes one use, saved on the agent's attributes; a new `unsa_day` resets the daily count. This per-device rule is **not a change to CWN**. If the limit is reached, ordinary interviews, records and case clues remain available.

The method is a *Voigt-Kampff* homage in spirit only, without copying its questions, equipment or mythology. The psychotronic apparatus is strange and intrusive, not infallible.

## What it measures

Four observed channels, scored by the interviewer:

| Channel | What the interviewer looks for |
|---|---|
| Affect | Appropriate, flattened, simulated or displaced emotional response |
| Narrative coherence | Whether the account holds together under gentle contradiction |
| BCI telemetry | Arousal, hesitation, load and incongruence between stated and measured response |
| Empathy | Perspective-taking and concern, including toward inconvenient subjects |

An optional fifth channel, psychotronic/PSI response, is not used in early cases and is never
required for a valid assessment.

**Consciousness is not intelligence, and neither is empathy.** An eloquent, caring-seeming subject
may be nonconscious; a genuine NHI consciousness may fail anthropocentric empathy criteria. The
protocol reports a *pattern*, not a metaphysical verdict.

## Why UNSA Helsinki prefers it

- Better triage in comparative casework: fewer false classifications than the corporate affect
  suites and the older security-services interview.
- It produces investigative leads, not just a label: the strongest channel and its contradictions
  point to the next interview, record or witness.
- It records dissent and uncertainty instead of forcing a binary.
- It is cheap, portable and hard to game with a prepared script.

It is not infallible. Cultural and language bias, interviewer skill, BCI quality and the subject's
cooperation all move the result. UNSA knows this; Romppainen knows it best.

## Procedure at the table

1. **Brief** the subject and obtain consent; the assessment is evidence, not interrogation.
2. **Interview** through a short scripted scene. Use CWN skill checks (typically Empathy or
   Cognition, difficulty by subject) to open channels; a failed check costs time or raises suspicion,
   never the core clue.
3. **Score** the four channels from the observed answers and telemetry.
4. **Classify** into a pattern band with a confidence value and explicit caveats.
5. **Follow the lead**: the strongest channel names the next investigative step.

### GUMSHOE rule

The **core clue is never behind a roll**. Whatever the check result, the interview yields the fact
that the subject's account contradicts a record, or that a channel is incongruent. Rolls decide how
much extra detail and how much suspicion the interviewer earns, not whether the case can proceed.

## Bands (working values, pending playtest)

| Band | Reading |
|---|---|
| `baseline_human` | Channels consistent with an ordinary human baseline |
| `uncertain` | Mixed signals; repeat or corroborate before acting |
| `atypical` | Coherent but materially outside the baseline; investigate |
| `nonconscious_pattern` | Simulated affect with no coherent interior account |
| `nhi_nonanthropocentric` | Coherent interior account that fails human empathy criteria |

## Open questions for Tomi

- The University of Helsinki affiliation/history of Dr. 愛 Fujita, where applicable; the established name and collaborator are no longer open.
- Whether the PSI channel is canonically part of the protocol or a separate Noösphere interface.
- How openly UNSA publishes the method; the transparency-versus-classification tension applies.
- Finnish voice for Romppainen's explanation of the test.

## Links

- #985 — this design.
- #950 — MUD is the main game.
- #996 / `docs/FINNISH.md` — canonical Finglish, no localizations; preserve Tomi's writing.
- #981 — gradual narrative revelation and spoiler discipline (outdated localization rules superseded by #996).
- #897 — CWN rules lock; this is a mod/procedure, not a new core.

## Underground bunker: gradual campaign discoveries

Beneath the Helsinki UNSA Field Office, Romppainen and Dr. 愛 Fujita conduct a **psychotronic research programme**. Its blend of clinical science, officious bureaucracy, bad fluorescent lighting and unnervingly funny laboratory rituals is informed by the **tone** of *Maniac* and *Riget*, not their characters or dialogue. Rumours of MKULTRA-like abuses require investigation; do not assert unestablished details as facts. Romppainen's strained relationship with UNSA secrecy and his former lover provides conflict without taking choices away from the rookie.

**Spoiler and knowledge ladder (#1007):**

1. **Street:** a routine interview and peculiar institutional equipment. Public descriptions and dictionary entries must not reveal project codenames or the research programme.
2. **Anomaly:** the helmets, unusual aftereffects and unexplained recordings raise questions about the underground programme.
3. **Disclosure:** Romppainen may personally brief the player on **Project Hiisi**, a programme reverse-engineering **crash retrieval technology from 1934 and 1946**. Its link to the Ghost Rocket/Ö-Mappi legacy is investigated rather than handed down as unquestioned truth.
4. **Deeper classified stages:** the player discovers that **Louhi, Lemminkäinen and Sampo** are **more highly classified than Hiisi**. Their actual goals and functions are **not yet defined** and must not be fabricated by agents.

The project names belong to privileged *author/GM knowledge* until the corresponding player revelation. Don't leak them through the early-scene interface, lexicon or loading text.
