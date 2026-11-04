# DRAFT — TOMI REVIEW REQUIRED — NOT AUTHOR APPROVED

# NoöPunk Character Tags: Personality, Goals, Reputation

> **Phase A research + draft (#1137).** Not a rule. Tomi edits, approves or replaces this document. No Python, no
> rulebook change, no CWN modification.

## 1. The author's requirements

Binding source: [`design/BIONICS.md`](../../design/BIONICS.md) (author-authored, preserved verbatim).

- **Reputation:** positive or negative score, **per faction**, "only add them when a character gets a reputation
  with the faction", range **−4 … +4**.
- **Personality:** "used as guidelines for role-playing the character", may add **small +1 / −1 modifiers**, and
  may **prevent or allow** the character to do something.
- The author's worked examples: **`Pacifist-1`** — cannot start a combat, may only fight defensively, −1 when
  attacking, "tries to subconsciously miss"; **`Pacifist-2`** — "just drops his weapon and runs away if there is a
  combat, or surrenders if he cannot run away". The author writes: **"Pacifist-2 is cool, let's use it."**

That last line is a decision, not a suggestion. This draft keeps it and treats the design consequence as a
review item rather than quietly softening it.

## 2. What already exists — extend, never duplicate

| Component | Module | What it does |
|---|---|---|
| Unified tag model (#51) | `src/rules/tags.py` — `Tag`, `TagStack`, `build_stack`, `stat_rating` | Stacking, keys, stat ratings |
| Tag-based attributes (#821) | `src/rules/noopunk_tags.py`, `data/rules/noopunk_tags.json` | Tag types, modifiers for rolls, conversion proposal |
| **Goal tag (#1119)** | `src/rules/goals.py` — `Goal`, `Progress`, `Award`, `GoalLog`, `record_progress`, `award_xp`, `paper_line` | Goal lifecycle, progress, awards, paper line |
| Fixtures | `src/rules/tag_fixtures.py` | Test doubles |

**The Goal subsystem is already implemented.** This draft proposes **nothing new** for goals beyond what #1119
does; it asks whether short/medium/long horizon should be a field on the existing `Goal`, and nothing more.

## 3. The three tag families

### 3.1 Personality tags — the author's design, taken seriously

| Tier | Effect | Discussion |
|---|---|---|
| **`-1` (mild)** | A small modifier (−1) and a nudge to roleplay | Fully compatible with CWN as a situational modifier |
| **`-2` (strong)** | **An action restriction**: cannot initiate combat; must withdraw or surrender | This is the author's `Pacifist-2` |

**The `Pacifist-2` review item, stated plainly.** A tag that removes the choice to fight is a real restriction on
player agency. The author has approved the idea and called it cool, so the draft adopts it — but three design
questions follow, and they are Tomi's to settle:

1. **Is it opt-in at character creation only, or can it be acquired or lost in play?** Acquiring it involuntarily
   would be the moment the tag stops being characterisation and becomes a mechanic doing something to the player.
2. **What does "cannot" mean procedurally?** Refusal by the player is not needed — the tag simply removes the
   option, like a character with no hands cannot pick a lock. That is clean and it is what the author described.
3. **Does breaking it cost anything?** A character who *does* fight despite `Pacifist-2` has, by the author's own
   description, dropped the weapon and run — so the tag is better modelled as an **override of intent**, not a
   prohibition the player can violate. Keep it that way; it avoids a punishment mechanic entirely.

**Never build a psychology system.** A personality tag is a roleplaying anchor with a small mechanical edge, not a
personality inventory, not a mental-health model, and never mandatory.

### 3.2 Goal tags — already implemented

The existing `Goal` lifecycle covers add → progress → award → log. Draft proposal, pending review: add an
explicit **horizon** field — `short` (this case), `medium` (this act), `long` (the campaign or the character's
life) — because the issue asks for it and the current model may not distinguish.

**A goal is the player's, not the system's.** The system records progress; it does not tell the player what to
want. Abandonment is a legitimate outcome and should be recorded, not penalised.

### 3.3 Reputation tags — per faction, −4 … +4

| Score | Meaning | Practical effect |
|---|---|---|
| +4 | Trusted insider | Doors open without a check; favours are real |
| +2 | Known and respected | Advantage on relevant social checks |
| 0 | No tag at all | **The default: no tag exists until earned** |
| −2 | Known problem | Disadvantage; supervision; access withdrawn |
| −4 | Hostile | The faction acts against the character as an institution |

Three separate things must not be collapsed into one number:

- **Public reputation** — what people say.
- **Institutional reputation** — what the file says (Europol's internal assessment can differ from the public one).
- **Relationship tags** — what a specific person feels, which is not a faction score.

## 4. Hard separation from cosmic alignment

**No lifestyle choice makes the character StS** (campaign §2.2, and the author's canon). Specifically:

| This | Is not this |
|---|---|
| Addiction, dependency, recovery | Polarization loss |
| A dirty arrest, a covered-up mistake | Service-to-Self |
| Political dissent, a relationship the service disapproves of | Density or path change |
| Ordinary cowardice (`Pacifist-2` running away) | Cowardice is not a moral verdict |

The first campaign's protagonist is **always StO and fixed**. Tags describe a person; polarization describes a
cosmic orientation and does not move with them.

## 5. Precedence and anti-stacking

- **One tag, one modifier.** Stacking is handled by the existing `TagStack`; do not add a second stacking rule.
- **Personality beats generic circumstance** where they conflict, or the table agrees otherwise — but pick one and
  write it down. The draft proposes: **situational modifiers stack; personality sets the intent restriction**.
- **Reputation does not modify combat.** It is social and institutional.
- **A tag never silently removes a core CWN capability** except where the author has explicitly said so
  (`Pacifist-2` and combat initiation is the one approved case).
- **Provenance:** every tag records where it came from (scene, session, faction, player declaration). A tag with no
  origin is a bug.

## 6. Tabletop examples

1. **The `Pacifist-1` officer at a door.** A raid is about to start. She may go in and defend herself, but she
   cannot start it, and her first shot is at −1. The table sees the tag doing work without a rules argument.
2. **`Pacifist-2` in a corridor.** Shots fired. The character drops the weapon and runs — the player keeps
   narrating the flight, which is the interesting part. No roll, no penalty, no argument.
3. **Reputation, earned.** The rookie helps Supo close a case. A `Supo +1` reputation tag is created **now** —
   before this, no tag existed. Later, that +1 is a phone call that gets answered.
4. **The file disagrees with the street.** The public reputation is +2, the internal Europol assessment is −1. Same
   character, two audiences, one scene.

## 7. Python model and interface (design only)

```python
# proposed, NOT implemented — extends the existing modules
@dataclass(frozen=True)
class PersonalityTag:
    name: str               # "Pacifist"
    strength: int           # 1 | 2
    restricts: str | None   # "initiate_combat" for strength 2

@dataclass(frozen=True)
class ReputationTag:
    faction: str
    score: int              # -4..+4
    audience: Literal["public", "institutional", "relationship"]
    provenance: str
```

Reuse `goals.Goal` and `tags.TagStack` as they are. The only new invariants worth testing later: reputation score
bounds, per-(faction, audience) uniqueness, and that a `PersonalityTag` with `restricts` set cannot be silently
ignored by an action resolver.

## 8. Campaign-stage relevance

| Stage | Tags |
|---|---|
| Act I | Personality and early reputation; goals are case-sized |
| Act II | Institutional reputation diverges from public; goals lengthen |
| Act III | Corruption and political tags become evidence |
| Act IV | Long-horizon goals pay off or are abandoned; reputation decides who will still take the call |

## 9. Open decisions for Tomi

1. `Pacifist-2` — opt-in at creation only, or acquirable in play?
2. Are reputation tags visible to the player as numbers, or described qualitatively?
3. Should institutional and public reputation both exist, or is one enough for the first campaign?
4. Does `Goal` need an explicit horizon field, or is free text enough?
5. Should tag provenance be printed on the character sheet (the `paper_line` in `goals.py` suggests yes)?

## 10. Bibliography

- Author: `design/BIONICS.md` — the source of `Pacifist-1/2` and the −4…+4 reputation range.
- `docs/campaign/CAMPAIGN_01_EUROPOL_ROOKIE.md` §2.1–2.2 (fixed vs open; "no lifestyle choice makes her StS").
- `src/rules/tags.py` (#51), `src/rules/noopunk_tags.py` + `data/rules/noopunk_tags.json` (#821),
  `src/rules/goals.py` (#1119).
- CWN Free Edition SRD — the check and modifier conventions tags must fit (CC0, immutable).
- `docs/rules/CWN_IMMUTABLE_CORE_1068.md`.
