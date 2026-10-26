# Memo: Northern Noösphere mythology and a psychiatric-origin Europol NHI unit

**Status: exploratory design memo. Not canon, not an implementation ticket, and not a rules proposal.**
Source: [#626](https://github.com/TomiToivio/NooPunk/issues/626), 2026-10-26. The author's own framing is
*"preserve ambiguity, competing interpretations, the Nordic tone, and existing NoöPunk continuity."*

This file exists so the memo is readable from a checkout — issue bodies are not part of the repository, and a
worldbuilding direction this large should not live only in a thread. It records the proposal and the continuity
findings; it does **not** decide anything.

## 1. What the memo proposes

- A **Nordic NHI investigative unit** whose entry point is anomalous psychology, not alien contact: shared
  delusions, dissociative episodes, impossible memories, contagious beliefs, fugue states, cultic behaviour and
  experimental-treatment complications — some of which turn out to be PSI, NHI communication, psychotronics,
  rogue AI, or genuinely ordinary clinical illness.
- A campaign engine, **"Diagnosis or Disclosure?"**: clinical safeguarding first, then forensic/social
  investigation, competing hypotheses held open, escalation, and consequences (stigma, disclosure politics,
  exploitation of witnesses).
- A **Northern Noösphere** premise: myth as culturally mediated interpretation of an incompletely understood
  reality — Väki, haltijat, tietäjät, Tuonela, Pohjola, the Sampo, Väinämöinen's songs, Yggdrasil, seiðr —
  with each tradition kept **distinct** rather than flattened into interchangeable "shamanic" lore.
- The **Sampo Protocol** as a matter–energy–consciousness interface with three rival readings (scientific,
  noetic, political), contested by Orion, the Confederacy, the Swarm and human institutions.
- Tone anchors: *Riget*, *Maniac*, *The X-Files*, *Control/SCP*, Lipton Cockton, and the Nordic social reality of
  working hospitals, EU cross-border policing and digital health systems — explicitly **not** 1980s
  Kaurismäki Finland.

## 2. Continuity findings (verified against the tree, not assumed)

The memo asks that the team be reconciled with established UNSA personnel "rather than automatically overriding
their roles". They already exist, in a different institution:

| Character | Where | Established role |
|---|---|---|
| **Dr. Harri Romppainen** ("Dirty Harry") | `strategy_game/casework/kallio.py:99` | UNSA Helsinki Field Office agent; *"Veteran of Ö-Mappi, transferred with the Supo team"*, *"Reads the report before the room"*, *"Has seen a stack lie before"*; tag `competence: forensic medicine`; COG 4 |
| **Laura Falk** ("Minerva") | `strategy_game/casework/kallio.py:89` | Field Office agent, *"Academy newcomer, three months in the Field Office"* |
| **Sebastian Virtanen** ("Ukuli") | `strategy_game/casework/kallio.py` | Field Office agent (`AGENT_IDS`) |
| **Laura Univaara** | `strategy_game/casework/kallio.py` | Field Office agent (`AGENT_IDS`) |

So the memo's "Europol-associated Nordic NHI unit led by Dr. Inspector Harri Romppainen" **relocates an existing
UNSA field-office veteran into Europol and changes his role**. That is a canon change, not a new character, and
it collides with three things:

1. **Institutional home.** The established team is a *UNSA Helsinki Field Office* unit; the memo proposes a
   *Europol* unit. Both cannot own the same four people without an in-fiction transfer, secondment or joint
   command — and the memo already flags that Europol has no standalone arrest powers in member states.
2. **Romppainen's competence.** Established as forensic medicine with COG 4 — a report-first investigator. The
   memo makes him a clinical/psychiatric lead ("clinical/research competence and police investigative
   authority"). Those are different skills, and the sheet would have to change to match.
3. **Rank and title.** "Dr. Inspector" is new. Established sheets carry no rank; nothing in the tree grants him
   command of a unit.

## 3. Open decisions (author's, recorded not taken)

- **Mandate:** does the unit replace the UNSA Helsinki field office, sit beside it as an Europol analytical cell,
  or form a joint task force where Finnish officers hold local authority? The memo lists these as possibilities
  and does not choose.
- **Romppainen:** same person relocated, a secondment, or a new command role over the existing team? His
  competence and title have to resolve together with his sheet.
- **Maniac touchstone:** Norwegian original, Netflix adaptation, or both — explicitly left open in the memo.
- **Sámi material:** the memo requires Sámi expertise and creators before anything beyond an exploratory outline.
  That is a precondition, not a task.
- **Whether any of this becomes canon at all.** Memo status is exploratory; several proposals (Sampo as
  interface, Tuonela as interface) touch established ontology (#11, #18) and would need a continuity pass
  before adoption.

## 4. What this file does not do

- It does not canonise the unit, the Sampo Protocol, or any mythological correspondence.
- It does not change `kallio.py`, the character sheets, or the scenario data.
- It does not import real-world claims: the memo itself marks the comparative-mythology table as *hypotheses
  inside NoöPunk*, not historical or scientific assertions, and keeps the traditions distinct.

Reading order for anyone picking this up: this file → #626 for the full proposal → `strategy_game/docs/RPG_FIRST_CASE.md`
and `strategy_game/casework/kallio.py` for the established team → `rulebook/12_BEINGS.md` and
`rulebook/18_CROSS_DOMAIN_STATE.md` before touching ontology.
