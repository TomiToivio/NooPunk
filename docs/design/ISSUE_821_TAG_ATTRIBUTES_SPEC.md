# Tag-based attributes, skills and statuses (#821) — specification and audit

**Status:** implemented in data + Python + Godot; **tabletop chapter insertion pending one ruling.**
Tomi's draft is the source of truth. This document is the chapter-ready text and the audit the draft
asks for. It is deliberately *not* written into `rulebook/2_ATTRIBUTES.md` yet: that chapter carries
the approved six STATs (FIT / REF / INT / SOC / PSY / CYB) from the narrative-first edition, and the
draft's seven tags supersede or restructure them. Replacing approved canon without a ruling is exactly
what `rulebook/README.md` forbids. The question is recorded below as **Q7**.

## 1. Everything is a tag

Every character property is a **typed tag**: an explicit `kind` (`attribute`, `skill`, `status`,
`trait`), a name, a number and a sign, plus duration, source, stacking and exclusivity where they
apply. The type is what keeps two identical-looking strings apart:

| tag | kind | reads as |
| --- | --- | --- |
| `Firearms-1` | skill | skill rank **1** — a competence, not a penalty |
| `wounded-1` | status | a **one-point penalty** while it lasts |
| `Cognition+2` | attribute | the attribute modifier **+2** |
| `Noögenetic` | trait | a permanent property with no number |

Unicode names are legal (`Noöware-2`). Every tag serialises to one record and prints on the sheet in
the syntax above.

## 2. The seven attributes

| Attribute | Meaning |
| --- | --- |
| **Fitness** | How athletic, strong and healthy your body is. |
| **Cognition** | Ability to search, process and understand human language data, human culture and the language-encoded database of the Safenet. |
| **Awareness** | Consciousness, awareness, perception, intuition and wisdom. |
| **Agency** | Free will, "coolness", willpower and identity. |
| **Reflexes** | Physical dexterity, agility and coordination. |
| **Cyber** | Technical aptitude, cyberspace abilities, the cyborg side, and the ability to interface with machines. |
| **Empathy** | Loving kindness, empathy and humanity. |

Generation is 3d6, and **only the modifier is stored** — the raw score never reaches the sheet:

| 3d6 | Tag value |
| --- | --- |
| 3 | −2 |
| 4–7 | −1 |
| 8–13 | 0 |
| 14–17 | +1 |
| 18 | +2 |

The human baseline is **−2 … +2**; anything above +2 is **transhuman**. This table is not a
suggestion: no other distribution generates attributes, and the engine reads these bands from
`data/rules/noopunk_tags.json`.

### The Empathy boundary

**Empathy −3 is outside the human range.** Such a character is no longer human and **is not eligible
as a player character**; the 3d6 generator cannot produce it, and the engine refuses to seat one as
the protagonist while allowing it for an NPC. In the setting's ethics framework, low Empathy with high
Agency reads as service-to-self or negative polarity — a fictional mechanic, not a claim about real
psychology, and **no threshold is fixed here** (Q5).

## 3. Skills are tags

Ranks run **0–4** as in CWN, printed as `Name-rank` (`Shoot-1` is *Firearms* at rank 1). Untrained
actions have two supported cases: attempted at **−1**, or **impossible** without the skill. Which
skills fall where is undecided (Q1), so the contract currently lists none as impossible — an untrained
action always rolls at −1 until Tomi rules.

| NoöPunk skill | Attribute | Relation to the CWN baseline |
| --- | --- | --- |
| Administer | Cognition | Bureaucracy and institutions. |
| Connect | Empathy | Networking; NoöPunk design pending (Q3). |
| Drive | Reflexes | As before. |
| Strength | Fitness | Replaces Exert for raw muscular power. *(A skill, not the removed Strength attribute.)* |
| Stamina | Fitness | Replaces Exert for endurance. |
| Hardware | Cyber | Renames Fix. |
| Wetware | Empathy | Renames Heal for biology, medicine, physiology. |
| Software | Cyber | Renames Program; software and LLMs through a brain interface. |
| Noöware | Empathy | New: psychology, psychiatry, psychotherapy, psychic integration. |
| Research | Cognition | Replaces generic Know: find, evaluate, read and understand information; the scientific method. |
| Know | *undecided* | Domain-specific uses under review (Q2). |
| Lead | Agency | As before. |
| Notice | Awareness | As before. |
| Unarmed | Reflexes | Renames Punch. |
| Melee | Reflexes | Renames Stab. |
| Firearms | Reflexes | Renames Shoot. |
| Sneak | Awareness | As before. |
| Survive | Agency | As before. |
| Talk | *contextual* | One skill: +Empathy for rapport and compassion, +Agency for conviction, bluffing and authority. |
| Trade | Agency | As before. |
| Work | *undecided* | Which professional uses survive is Tomi's call (Q2). |

**Worked example.** Reflexes +2, Firearms-1, and `wounded-1` for the scene. Rolling 7 on 2d6 against
difficulty 10: `7 + 2 + 1 − 1 = 9` — a miss, by one. Without the wound it would have been 10 and a
hit. The same character untrained would roll `7 + 2 − 1 = 8`, also a miss.

## 4. Statuses and traits — a minimal general model

A status or trait is a typed tag carrying `duration` (`permanent`, `scene`, `day`, `until_rest`),
`source`, `stacking` (`stack`, `replace`, `highest`) and `exclusive_with`.

- **Stacking.** One mode governs one status name: the mode of the newest application. Three
  `poisoned-1` tags stacked are −3; re-applied as *highest* they are −1.
- **Exclusivity.** Applying `panicked-1` with `exclusive_with: ["stunned"]` removes any live `stunned`.
- **Expiry.** Ending a scene drops its statuses; permanent tags never expire.

Nothing beyond these mechanics is invented: no canon of traits, no fixed list of statuses.

## 5. Audit — what this touches

| surface | file | effect |
| --- | --- | --- |
| contract | `data/rules/noopunk_tags.json` | new; the only place the numbers live |
| layer of record | `src/rules/noopunk_tags.py` | #823 landed the attribute half; this change adds skills, checks, statuses and serialisation to the same module |
| engine | `godot/core/noopunk_tags.gd` | new; same rules, same contract |
| checks | `rules_adapter.gd`, `cwn_character.gd` | **unchanged** — CWN's 2d6 + attribute + skill stays the chassis until the tabletop chapter lands |
| combat | `combat.gd`, `cwn_combat_rules.gd` | unchanged; attribute names reach them through the sheet |
| character creation | `CwnCharacter.create_field_agent()` | unchanged; it produces CWN attributes, which the migration proposal maps |
| saves | campaign v3, `GameState` | unchanged; migration is a proposal, not a rewrite |
| tests | `tests/test_noopunk_tags*.py`, `godot/tests/test_noopunk_tags.gd` | 46 Python, 55 Godot rows |

**Legacy compatibility:** nothing is removed or renamed in the running game. The tag model is additive
so a draft can be built on it, and the CWN path keeps working until the ruling lands.

## 6. Migration from CWN — a proposal, not a rewrite

Wisdom → Agency, Empathy, Awareness; Strength and Constitution → Fitness; Dexterity → Reflexes;
Intelligence → Cognition, Cyber; Charisma → Empathy, Awareness, Agency.

Where two old attributes feed one new tag, `propose_conversion()` keeps the higher old modifier, flags
the case `needs_ruling`, and carries its reasoning. Averaging, taking the highest, or letting the
player assign are all defensible and the draft chooses none of them. **No character or save is
migrated automatically** — `status: awaiting_author_ruling` in the contract (Q6).

## 7. Questions for Tomi

| # | question |
| --- | --- |
| Q1 | Which skills are impossible untrained rather than attempted at −1? |
| Q2 | Which domain-specific Know uses remain, and which professional Work skills survive? |
| Q3 | What is the NoöPunk design for Connect? |
| Q4 | May Talk use an attribute other than Empathy or Agency, and who adjudicates that at the table? |
| Q5 | What threshold (if any) marks "low" Empathy or "high" Agency for the StS characterisation, and does alignment ever change automatically? |
| Q6 | How are existing characters and saves migrated when several old attributes feed one new tag? |
| Q7 | **Does the seven-tag model supersede the six STATs (FIT/REF/INT/SOC/PSY/CYB) in `rulebook/2_ATTRIBUTES.md`, or sit beside them as an advanced layer?** Until this is answered the chapter is not edited. |
