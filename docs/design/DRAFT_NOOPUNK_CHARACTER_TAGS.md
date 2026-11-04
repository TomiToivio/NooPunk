# DRAFT — NoöPunk Character Tags: personality, goals and faction reputation

> **DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED**
>
> Phase A of [#1137](https://github.com/TomiToivio/NooPunk/issues/1137). Proposal only: no Python, no rulebook
> chapter, no CWN change. The `Pacifist-2` example is the author's, from
> [`design/BIONICS.md`](../../design/BIONICS.md), and is discussed here rather than quietly replaced.
>
> Companion drafts: [Psionics](DRAFT_NOOPUNK_PSIONICS.md) · [Psychotronics](DRAFT_NOOPUNK_PSYCHOTRONICS.md) ·
> [Bionics](DRAFT_NOOPUNK_BIONICS.md) · [Europol rookie](DRAFT_NOOPUNK_EUROPOL_CHARACTER_GENERATION.md).

---

## 1. What the author already decided

Verbatim from [`design/BIONICS.md`](../../design/BIONICS.md):

> "Reputation should have a negative or positive score. Reputation tags for each faction. Only add them when a
> character gets a reputation with the faction. Positive score indicates the faction likes the character and,
> negative indicates the faction dislikes the character. I think the range should be from -4 to +4."

> "Personality is surprisingly the personality of the character. These would be used as guidelines for
> role-playing the character, could add small +1 or -1 modifiers to some actions, and could prevent or allow the
> character to do something. Like personality tag Pacifist-1 would (in the case of Europol characters) mean the
> character cannot start a combat (can only fight defensively), and would get a -1 modifier when he attacks
> (tries to subconsciously miss the target). Pacifist-2 means the character just drops his weapon and runs away
> if there is a combat, or surrenders if he cannot run away. **Pacifist-2 is cool, let's use it.**"

That is a decision, not a suggestion: **`Pacifist-2` is approved in principle.** The open question is not
whether it exists but **how much agency it removes and who decides**.

---

## 2. What already exists in the repository — do not rebuild it

| piece | where | state |
|---|---|---|
| **Tag model** | `data/rules/noopunk_tags.json` — kinds `attribute`, `skill`, `status`, `other`; fields `kind`, `name`, `value`, `sign`, `duration`, `source`, `stacking`, `exclusive_with`; stacking semantics `stack / replace / highest`; Unicode names | implemented (`src/rules/noopunk_tags.py`, `src/rules/tags.py`) |
| **Goal tag** | [`docs/rules/GOAL_TAG_1119.md`](../rules/GOAL_TAG_1119.md); `src/rules/goals.py`; console verbs `goal/goals/progress/award` | **implemented** — one line on the sheet, horizon short/medium/long, five lifecycle kinds, one event pays once, no attempt farming, no faction XP |
| **Reputation** | *nothing* | **gap** |
| **Personality** | *nothing* (only the author's example) | **gap** |
| **Polarisation (StO/StS)** | campaign canon: the protagonist is **always StO**; `docs/law_of_one/` is a separate game | **not a tag system** and must never become one |

**Conclusion:** this draft adds **two** tag kinds — `personality` and `reputation` — and **reuses** the existing
goal implementation. Anything that would duplicate goals is a defect.

---

## 3. Personality tags

### 3.1 Format

One line per tag, same shape as every other NoöPunk tag:

```
Personality: Pacifist | intensity: 2 | source: play | since: 12.11.
```

* **intensity 1–3** (not 1–2): the author's `-1` is level 1; level 2 is the approved "drop the weapon and run";
  level 3 exists so a character can become *more* than the example, and so the GM has somewhere to go after 2.
* **source** is `play` (earned at the table), `reveal` (a memory), or `canon` (fixed in the pregen).
* **duration** is permanent until the fiction changes it. A personality does not expire with the scene.

### 3.2 What a personality tag may do — three powers, in ascending order

| power | example | rule |
|---|---|---|
| **Guidance** | "Pacifist 1: you do not start fights" | no mechanic; the GM may say "that would break your tag" and the player may accept or spend a scene changing it |
| **A small modifier** | `-1` to an attack the character is reluctant to make | **one** modifier, `±1`, never stacking with another personality tag |
| **A permission or a prohibition** | `Pacifist-2`: if combat begins, the character drops the weapon and runs, or surrenders | an **action restriction**, the strongest and rarest power |

### 3.3 The `Pacifist-2` problem, stated honestly

The author's example removes the player's choice at the moment combat begins. That is **deliberate** and it is
also unusual: most games avoid it because it feels like the GM playing the character. Three readings, all
compatible with the author's sentence:

| reading | what happens | who decides | risk |
|---|---|---|---|
| **A. Hard trigger** (literal) | combat starts → the character flees or surrenders; the player narrates *how*, not *whether* | the tag | loss of agency at the most dramatic moment |
| **B. Checked trigger** | combat starts → a save/check; on failure, flee or surrender; on success, the character stays, shaken | the dice | the tag becomes a coin flip and loses its moral weight |
| **C. Declared trigger** | the player may stay, but at a stated cost (a condition, a lost action, a reputation hit with the unit) | the player | it is no longer the author's example |

**Recommendation: A, with two guard rails.**

1. **The player narrates the flight.** The tag decides *that* she breaks; the player decides whether she runs,
   freezes, or surrenders, and what she says on the way out. That is still agency, and it is where the drama is.
2. **It can be bought down by play, not by points.** A scene in which she stands her ground and pays for it may
   reduce the intensity by one — if the table agrees. The tag is a record of who she is, and people change.

Guard rails matter because `Pacifist-2` on a **Europol officer** is a statement about the character's deepest
commitment, and the campaign is about an institution that will test it.

### 3.4 What personality tags are **not**

* **Not a morality score.** There is no "good" or "bad" personality; a `Cruel-2` and a `Pacifist-2` are both
  playable.
* **Not a skill.** No personality tag ever substitutes for a skill check or grants a re-roll.
* **Not polarisation.** A `Vindictive-1` is a personality; **StS polarisation is a cosmic path the protagonist
  does not have**. Addictions, corruption, cynicism and political dissent are personality and situation, never a
  path change. (Campaign canon: the protagonist is always StO.)

---

## 4. Reputation tags

### 4.1 Format

```
Reputation: Europol Helsinki | score: +2 | visibility: institutional | since: 03.11.
Reputation: Supo | score: -1 | visibility: public | since: 09.11.
```

* **score −4 … +4**, exactly the author's range.
* **created only when the character actually acquires a reputation** with that faction — never pre-listed, never
  a blank row for every faction in the setting.
* **visibility** distinguishes three things the author's note implies but does not separate:
  * `public` — the street, the press, the colleagues who talk;
  * `institutional` — the file, the file's readers, the people who decide postings;
  * `covert` — a faction that knows her and does not say so.
* **per faction, not global.** There is no "reputation" statistic.

### 4.2 What the score does

| use | rule |
|---|---|
| **Reaction** | the score shifts an NPC's starting attitude within the faction; it is **one** modifier, never a stack with personality |
| **Access** | at +3 or better, the faction may grant access it would otherwise refuse — a room, a file, a warning |
| **Refusal** | at −3 or worse, the faction actively obstructs: a delay, a report, a leak |
| **Never** | the score does not buy equipment, grant XP, or substitute for a warrant |

**No economy.** A reputation is a relationship record, not a currency: it does not "spend down" to buy favours,
and it does not tick up for routine politeness. It changes when something *happens* that the faction would hear
about — which is exactly the author's "only add them when a character gets a reputation".

---

## 5. Goals — reuse, do not duplicate

`GOAL_TAG_1119.md` already implements the whole lifecycle: short/medium/long horizons, `progress`,
`contribution`, `completed`, `failed`, `abandoned`, one event pays once, one XP on completion, CWN's XP table.
This draft adds **nothing** here except one line of cross-reference and one question for the author:

* **Does a goal belong to the character or the player?** #1119 allows both (`owner: <character or faction>`);
  the campaign's Act II moral turn may want a *player-stated* goal that the character does not know she has.

---

## 6. Three tabletop examples

**Example A — Pacifist-2 at the tram depot.**
A suspect draws a knife. Combat begins. The tag fires: she drops her weapon and backs away. The player narrates
it: *"I raise both hands, badge still in one, and I say 'I'm not doing this'."* The partner covers her. The
suspect escapes. Nothing was rolled; the scene's consequence is social and professional, and the unit's
reputation tag for her gains a note.

**Example B — reputation earned, not bought.**
She closes a case the Finnish police wanted closed their way. `Reputation: Finnish police −2`, visibility
`public`. Two sessions later a Supo officer refuses a joint interview "because of Helsinki". No dice, no
statistic: a door that was open is now shut, and the player knows why.

**Example C — personality from play.**
Three sessions of choosing to talk instead of draw: the GM offers `Patient-1`. The player accepts. It does
nothing mechanically until a scene where impatience would pay, and then it is a `-1` on the rash action — one
modifier, cited once.

---

## 7. Python model / interface proposal (design only — Phase B)

```
src/rules/noopunk_personality.py
    @dataclass PersonalityTag(name: str, intensity: int, source: str, since: str)
    def modifier(*, tag: PersonalityTag, action: str) -> int        # -1 / 0 / +1, never stacking
    def restricted(*, tags: Sequence[PersonalityTag], situation: str) -> str | None
        # returns "flight" / "surrender" / None — a permission answer, not a roll

src/rules/noopunk_reputation.py
    @dataclass Reputation(faction: str, score: int, visibility: str)
    def clamp(score: int) -> int            # -4..+4
    def modifier(*, rep: Reputation) -> int # single modifier for reaction/access
    def access(*, rep: Reputation, kind: str) -> bool
```

Rules:

* **Extend the existing kinds, do not fork the model.** `data/rules/noopunk_tags.json` gains `personality` and
  `reputation` in `tags.kinds`, with the same field names; a migration note is required because the existing
  kinds are `attribute/skill/status/other`.
* **One modifier per scene, from one tag.** `modifier` must refuse to add two personality tags; a test asserts
  the refusal, mirroring the single-payer rule in the psionics draft.
* **Reputation is clamped at the boundary** and is keyed per faction; a per-faction dict, not a score.
* **No import of the goals module** and no re-implementation of it. If this module needs a goal, it reads the
  existing one.

---

## 8. Interaction and precedence

| with | rule |
|---|---|
| **CWN checks** | a personality modifier is a `±1` applied to a check the CWN rules already allow; it never creates a check |
| **Goals (#1119)** | untouched; this draft adds nothing to it |
| **Polarisation (StO/StS)** | **never** derived from personality, reputation, addiction or politics. The protagonist is StO by canon; the tags describe a person, not a path |
| **Psionics / bionics** | psi conditions and bionic drawbacks are **status tags**; personality is a different kind and does not stack with them |
| **Europol chargen** | the pregen starts with **no** personality tags and **zero** reputation — the campaign earns them |
| **Acts** | I: reputation only. II: first personality tags offered. III: reputation across factions becomes the campaign's social map. IV: the tags are what the ending is *about* — the Officer, the Envoy, the Interpreter are three relationships, not three scores |

---

## 9. Open decisions for Tomi

1. **`Pacifist-2`: reading A (hard trigger), B (checked), or C (declared with cost)?** Recommendation: A with
   player-narrated flight.
2. **Intensity 1–3, or 1–2?** The example only needs 2.
3. **Can a personality tag be reduced by play**, or only by the author/GM?
4. **Does a personality modifier ever exceed ±1** (e.g. `-2` at intensity 3)?
5. **Reputation visibility:** are `public`/`institutional`/`covert` the right three, and does a public score ever
   differ from the institutional one for the same faction?
6. **Who may change a reputation** — the GM alone, or does the table negotiate it like a goal?
7. **Do faction reputations ever transfer** (Europol's standing helping with a national force, or hurting)?
8. **Is `Pacifist` the only restriction tag** the campaign needs, or are there others (Addict, Coward,
   Loyal-to-a-person) that should be defined now?

---

## 10. Sources

| source | status |
|---|---|
| [`design/BIONICS.md`](../../design/BIONICS.md) — reputation −4…+4, Pacifist-1/-2 | read; quoted verbatim above |
| `data/rules/noopunk_tags.json` — tag kinds and fields | read |
| [`GOAL_TAG_1119.md`](../rules/GOAL_TAG_1119.md) + `src/rules/goals.py` | read; goals are implemented, not re-proposed |
| [`CAMPAIGN_01_EUROPOL_ROOKIE.md`](../campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md) — StO canon, Act structure | read |
| CWN SRD §Checks / §Skills | referenced through the repo's CWN modules; **no CWN text reproduced** |
