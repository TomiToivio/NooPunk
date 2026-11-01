# Design canon: cyberpunk first, cosmic second (#1007)

**Status: design decision, 2026-11-01.** This is the *presentation* constitution — the counterpart of
`docs/rules/RULES_CONSTITUTION.md`, which governs the mechanics. One governs what the game is made of;
this one governs what the player is allowed to see, and when.

Its machine-readable half is `data/world/reveal_ladder.json`, guarded by
`tests/test_reveal_ladder.py`. A quest, a scene or an NPC reads a stage; nothing reads this paragraph.

## 1. The formula

**NoöPunk = cyberpunk + Law-of-One-inspired science fantasy**, and the player meets it in that order.

The *experience* begins as pure, recognisable cyberpunk: rain, rent, a shuttered kiosk, a corporation
that owns the thing you need. UFO/NHI, PSI, occult and Noösphere material arrives through
**investigative cases and escalating ontological shocks**, never through exposition. The New Weird and
social-science-fiction identity stays; so does the understated comedy.

**Law of One is fictional-world inspiration, not in-universe proof and not a claim about the real
world.** Factions may use its vocabulary — as an argument — and the game never confirms that any of
them is right.

## 2. The ladder

Four stages, each able to show anything its predecessors allowed and nothing a later stage owns.
The authoritative lists are in `data/world/reveal_ladder.json`; this is the reading.

| # | Stage | What the rookie knows | How a stage ends |
| --- | --- | --- | --- |
| 1 | **street** — cyberpunk | UNSA is an agency with too many files and too few staff. Cyberware, corporate crime, corruption, rationing. | a case that will not close with a mundane explanation, and a superior who will not say why |
| 2 | **anomaly** — PSI | some incidents do not fit; colleagues vary between denial, euphemism and dread | evidence that survives every mundane explanation, and a decision about whether to report it |
| 3 | **disclosure** — partial | NHI exists and has been negotiated with; whose version is true is a live political fight | a case decided by interpretation rather than by evidence |
| 4 | **cosmic** — the open question | the paradigms are public, the answers are not | — (the campaign does not end by proving a metaphysics) |

The test that keeps the ladder honest is that **it only widens**: a later stage may never forbid what an
earlier one allowed, because a rule that could un-teach a player is a contradiction, not a reveal.

**What the ladder forbids, in one line:** no named NHI factions, no density vocabulary and no StO/StS
framing before a case has earned them, and never a confirmation that any faction's cosmology is fact.

## 3. The perspective

**The player character** is a young UNSA Academy rookie field agent in Helsinki: inexperienced,
skeptical, and holding a brief that is partial and sometimes simply wrong. The game never assumes the
character accepts an unbelievable proposition on trust.

**Dr. Harri S. Romppainen** is the supervisor, in the trickster-magician register: vastly more informed
than he reveals, unreliable in *method* rather than in *intent*. He may hint, joke, deflect, stage
puzzling learning experiences, and withhold what he does not know or may not say. He never lectures the
lore, never becomes a walking encyclopedia, and never takes a decision from the player. His secrecy has
to be narratively credible, not arbitrary obstruction.

**Revelation happens through play:** investigations, evidence, conflicting interpretations, witnesses
and consequences. **Ordinary cyberpunk life stays relevant at every stage** — rent, work, corruption and
inequality do not stop being real because the sky is strange.

## 4. Why UNSA exists, in the fiction

Two existential threats, both arriving before UNSA holds real power:

1. **Rogue AI / malevolent ASI risk** — at least one serious fictional incident, inspired by real AI
   alignment concerns.
2. **UFO/UAP disclosure and potential NHI risk** — a fictional partial disclosure, a verified anomaly,
   and full NHI knowledge that stays contested or classified. Inspired by Wendt and Duvall's
   *Sovereignty and the UFO*.

**Do not confuse the fiction with the world.** Real UAP disclosures are not NHI confirmation; real AI
incidents are not a malevolent ASI. That distinction is written into `rulebook/21_PSI_PARADIGM_SHIFT.md`
and `11_ONTOLOGY.md` as well, and it is not negotiable for tone.

UNSA grows from civilian UN scientific coordination into the agency the player joins, and stays
politically contested: it is not a world government and its authority is not a moral endorsement.

## 5. What this does not decide

* Which case opens the campaign, and which stage it ends in — that is scenario work.
* Whether the Law-of-One vocabulary ever appears *unironically* outside a faction's mouth. Today the
  answer is no; a faction may always use it.
* How much Romppainen knows. The ladder says he withholds; it does not say what the truth is.
