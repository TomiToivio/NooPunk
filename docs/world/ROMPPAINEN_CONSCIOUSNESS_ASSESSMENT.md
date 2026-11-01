# The Romppainen–Fujita psychotronic empathy assessment

**Status:** canon. The name and the collaborator were approved by Tomi on 2026-11-01 and supersede the earlier
"working title / Helsinki protocol / unnamed colleague" placeholders in this file. The game has one canonical
Finglish language (#996); agents write English-led player-facing Finglish and preserve Tomi-authored dialogue
verbatim. Non-player-facing documentation is English.

## Origin

UNSA Helsinki uses an original consciousness and empathy assessment: the **Romppainen–Fujita device**, built by
**Dr. Harri S. Romppainen**, UNSA Supervisory Special Agent (SSA) and psychologist, together with his former
lover **Dr. 愛 Fujita** of the **University of Helsinki**.

Romppainen runs the psychotronics programme from the **UNSA underground bunker laboratory** beneath the
Helsinki field office. The register is *Maniac* by way of *Riget*: institutional humour, fluorescent
dread, two brilliant people who finish each other's sentences about things nobody should be measuring.
Dr. Azumi Fujita and Dr. James K. Mantleray are the tonal reference, not templates to copy.

The assessment is an original *Voigt-Kampff* homage in spirit — an interview that reads affect,
narrative coherence, physiology and empathy — not a copy of its script, apparatus or mythology.

## The device

The **Romppainen–Fujita psychotronic empathy device** is retrofuturistic, bulky and faintly ridiculous:
administrator and subject both wear a goofy psychotronic helmet, wired to a console of blinking lights
that makes strange beeping sounds. It is installed **only in the UNSA Helsinki Field Office**.

Field agents start to feel goofy after more than four tests in a row, so the office permits **at most
four tests per agent per day**; a fifth is refused, and readings taken past the limit are not
evidence. The deterministic implementation lives in `mud/nopunk_mud/consciousness.py`
(`DeviceSession`).

## What it measures

Four observed channels, scored by the interviewer:

| Channel | What the interviewer looks for |
|---|---|
| Affect | Appropriate, flattened, simulated or displaced emotional response |
| Narrative coherence | Whether the account holds together under gentle contradiction |
| BCI telemetry | Arousal, hesitation, load and incongruence between stated and measured response |
| Empathy | Perspective-taking and concern, including toward inconvenient subjects |

An optional fifth channel, psychotronic/PSI response, is not used in early cases and is never required
for a valid assessment.

**Consciousness is not intelligence, and neither is empathy.** An eloquent, caring-seeming subject may
be nonconscious; a genuine NHI consciousness may fail anthropocentric empathy criteria. The protocol
reports a *pattern*, not a metaphysical verdict.

## Why UNSA Helsinki prefers it

- Better triage in comparative casework: fewer false classifications than corporate affect suites and
  the older security-services interview.
- It produces investigative leads, not just a label: the strongest channel and its contradictions point
  to the next interview, record or witness.
- It records dissent and uncertainty instead of forcing a binary.
- It is cheap, portable and hard to game with a prepared script — and its absurd helmets put subjects
  off balance in a way polished corporate suites do not.

It is not infallible. Cultural and language bias, interviewer skill, BCI quality, the daily goofiness
limit and the subject's cooperation all move the result. Romppainen knows this best and says so, usually
at length.

## Procedure at the table

1. **Brief** the subject and obtain consent; the assessment is evidence, not interrogation.
2. **Fit both helmets** and run the device in the Helsinki field office; check the daily limit first.
3. **Interview** through a short scripted scene. CWN skill checks (typically Empathy or Cognition,
   difficulty by subject) open channels; a failed check costs time or raises suspicion, never the core
   clue.
4. **Score** the four channels from the observed answers and telemetry.
5. **Classify** into a pattern band with confidence and explicit caveats.
6. **Follow the lead**: the strongest channel names the next investigative step.

### GUMSHOE rule

The **core clue is never behind a roll**. Whatever the check result, the interview yields the fact that
the subject's account contradicts a record, or that a channel is incongruent. Rolls decide how much
extra detail and how much suspicion the interviewer earns, not whether the case can proceed.

## Bands (working values, pending playtest)

| Band | Reading |
|---|---|
| `baseline_human` | Channels consistent with an ordinary human baseline |
| `uncertain` | Mixed signals; repeat or corroborate before acting |
| `atypical` | Coherent but materially outside the baseline; investigate |
| `nonconscious_pattern` | Simulated affect with no coherent interior account |
| `nhi_nonanthropocentric` | Coherent interior account that fails human empathy criteria |

## Bunker secrets — knowledge-gated

The player may eventually learn that the bunker contains more than an empathy lab. Romppainen presents
the **Hiisi project** — reverse-engineering of crash-retrieval technology from **1934 and 1946** — and
only later that **Louhi**, **Lemminkäinen** and **Sampo** are far more secret. These are story gates,
not public dictionary entries; the `dictionary` command must never expose them before the narrative
does.

## Open questions for Tomi

- Whether the PSI channel is canonically part of the device or a separate Noösphere interface.
- How openly UNSA publishes the method; the transparency-versus-classification tension applies.
- Finnish voice for Romppainen's explanation of the test.

The *names* and their *relative secrecy* are canon. **Do not invent or reveal what Louhi, Lemminkäinen and
Sampo actually do** until Tomi establishes it in a design document. And never leak classified project names
through public UI, the player dictionary or early-scene exposition.

Romppainen's conflict sharpens as he ages: intellectual freedom against institutional survival, scientific
curiosity against care for the people he tests. His disclosures are controlled, personal and possibly
unreliable. Dr. 愛 Fujita is a scientist with her own judgement; their former relationship may complicate the
collaboration without prescribing melodrama.

## Open questions for Tomi

- Whether the PSI channel is canonically part of the device or a separate Noösphere interface.
- What Louhi, Lemminkäinen and Sampo actually are.
- How openly UNSA publishes the method; the transparency-versus-classification tension applies.
- Finnish voice for Romppainen's explanation of the test, and for Fujita's.
