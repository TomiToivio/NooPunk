# DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED

# NoöPunk Europol Rookie: character generation gaps and issued equipment

> **Phase A research + draft (#1137).** Not a rule. Tomi edits, approves or replaces this document. No Python, no
> rulebook change, no CWN modification.

**Read this first:** most of this subsystem is **already canon**. This document is therefore a **gap analysis and
an equipment list**, not a new character-creation system. Duplicating the campaign's existing character rules
would be the exact failure the repository keeps catching.

## 1. What already exists (do not restate, do not fork)

| Already written | Where | Status |
|---|---|---|
| Fixed dossier vs player-built identity; the Wanderer reveal; StO fixed and not a meter | `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` §2.1–2.2 | **Canon / author decision** |
| Starting sheet as a **proposal** (skills only; attribute array deliberately left open) | same, §2.3 | Proposal — "numbers need author approval" |
| Pre-authored three-stage PSI sequence, explicitly **not** a selectable tree | same, §8 | Canon |
| Europol powers and limits — "Europol opens doors; national officers walk through them" | `docs/world/EUROPOL_HELSINKI_1114.md` §3 | Working model; exact legal citations **open** |
| Company housing in Kurvi; issued BCI and defensive psychotronic implant | campaign §2.1; `design/BIONICS.md` | Canon |

**What this draft adds:** the *background, Edge/Foci and equipment* gaps, and the GM-secret flags — nothing else.

## 2. The rule this draft follows

**CWN character generation and progression are preserved.** No parallel attribute system, no new resolution, no
second advancement track. A gap is only a gap if CWN genuinely has no background, Edge or Foci that covers it.

Candidates the issue names, each to be checked against the published CWN background table in
`src/rules/cwn_backgrounds.py` **before** anything is added:

| Candidate background | Is it a real gap? | Draft recommendation |
|---|---|---|
| Europol academy investigator | Likely covered by an existing investigative/law-enforcement background | **Check first.** Only add if no CWN background produces a plausible academy-trained investigator |
| Transnational police analyst | Possibly a gap — analysis, not fieldwork | Candidate addition, framed as a CWN background with an analysis-heavy skill grant |
| Cyberforensics specialist | Likely covered by existing cyber/technical backgrounds | **Check first** |
| Liaison officer | Genuine gap candidate — the Europol-specific competence is *jurisdiction*, not firepower | Candidate addition; its signature is access to institutions, not a combat edge |
| Field investigator | Almost certainly covered | **Do not add** |

**Draft position:** propose **at most two** additions — *transnational police analyst* and *liaison officer* — and
only after someone has read the CWN background table and can show the gap. Everything else should reuse published
material. The repository has repeatedly paid for agents who added a subsystem instead of checking first.

## 3. Issued equipment — four ownership classes

The distinction matters legally and dramatically; it is the point of the list.

| Class | Items | Consequence in play |
|---|---|---|
| **Issued** (Europol property, accountable) | Service sidearm, body armour, secure terminal, **BCI**, **defensive psychotronic implant**, credentials | Loss or misuse is an internal matter; the kit can be taken away |
| **Licensed access** (authorised, revocable) | Database access, joint-investigation-team authority, EU liaison channels, forensic laboratory time | Opens doors; **is not a warrant**; can be revoked mid-case |
| **Personal** | Off-duty clothing, personal comms, anything bought privately | No institutional protection; a personally bought QIP device is a **registration liability** |
| **Agency housing** | The Kurvi apartment | Paid for by the office — "which is itself a leash" (campaign §2.1) |

**No invented prices or stat blocks.** The sidearm, armour and terminal reference canonical CWN equipment. Where
the exact CWN item is unclear, the draft says "reference CWN item TBD" rather than inventing a number.

## 4. Legal limits, stated for play

Carried from `EUROPOL_HELSINKI_1114.md` §3 and not softened here:

- Europol **cannot** arrest, search or detain in Finland on its own authority.
- Europol **cannot** override a national prosecutor or Supo.
- Europol **cannot** compel UNSA, the military or a corporation to hand over material.
- Europol **cannot** declare a person an NHI, a hybrid or a psychic threat — it can request an assessment, and
  the assessment is evidence, not a verdict.

For the rookie, the practical form of this is: **every good idea needs a national officer to agree to it.** That
is the campaign's procedural texture, not an obstacle to be optimised away.

## 5. GM secrets and staged unlocks

The issue requires these as **GM secrets**, not player-facing options:

| Secret | Held by | Revealed |
|---|---|---|
| Dormant PSI capacity | GM | Awakening scene (Act II) |
| Bionic or hybrid marker, if any | GM | Detected by Europol's own medical, or by an outside party |
| Wanderer identity | GM | Act IV |
| True origin of the final revelation | GM | Ending only |

**No free stacking:** a dormant flag does not grant an effect; it moves the character from "cannot" to "can
attempt" at the staged moment, using the same PSI implementation as every other route (§7 of the Psionics draft).

**No unsolicited Wanderer disclosure.** The character does not learn what she is because a test says so.

## 6. Tabletop example

**First session, ten minutes in.** The rookie has credentials, a sidearm she has never drawn, a terminal, and a
BCI she does not fully understand. A Finnish detective will not let her into the scene. The scene is solved by the
liaison skill: she offers something the detective needs — an analysis channel, a Europol database query — and
walks in behind him. No roll required if the offer is genuinely useful; a CWN check if it is a bluff.

That is the character: **authority borrowed, never owned.**

## 7. Python model and interface (design only)

```python
# proposed, NOT implemented
@dataclass(frozen=True)
class IssuedKit:
    issued: tuple[str, ...]        # accountable property
    licensed: tuple[str, ...]      # revocable access
    personal: tuple[str, ...]
    housing: str                   # "kurvi_apartment"

@dataclass(frozen=True)
class RookieSecrets:               # GM-only, never on the player sheet
    dormant_psi: bool
    bionic_marker: str | None
    wanderer: bool
```

Two invariants worth testing in a later phase: a `RookieSecrets` object **must not** be readable from the player
sheet, and `licensed` access must not be usable as a warrant.

## 8. Open decisions for Tomi

1. Are *transnational police analyst* and *liaison officer* real gaps, or does CWN already cover them?
2. Does the rookie get the full issued kit on day one, or is some of it earned?
3. Is the Kurvi apartment a benefit, a leash, or both (the campaign currently says both)?
4. Should the bionic/hybrid marker be rolled at character creation, or authored per campaign?
5. Is the attribute array fixed by the author before play, or produced by the first playtest (current proposal)?

## 9. Bibliography

- `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` (canon and proposals, clearly marked as such there).
- `docs/world/EUROPOL_HELSINKI_1114.md` §3 (powers and limits).
- `design/BIONICS.md` (issued BCI and defensive psychotronic implant).
- CWN Free Edition SRD — backgrounds, equipment, character creation (CC0, immutable).
- `src/rules/cwn_backgrounds.py`, `src/rules/cwn_character.py` — the implementation the gap check must read.
- `docs/rules/CWN_IMMUTABLE_CORE_1068.md`.
