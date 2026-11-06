# Tag families and graphs — the author's decision (#1283)

> **Status: decided.** Cities Without Number is NoöPunk's default tabletop system; a portable tag layer sits on top of
> it; five families start the list and the list stays open. This page records the decision and what the code does with
> it. It implements no resolution rules, because the point is that the host RPG supplies them.

## The decision

**CWN is the chassis.** Skills, action, combat, equipment and hacking are CWN's procedures. Eclipse Phase remains an
occasional source of ideas (#1280); its mechanical detail is heavier than this campaign needs. The same authored scene
should also be runnable under another cyberpunk RPG, using that game's procedure for anything that needs a roll.

**Five starting families.** The list is open: more can be named as the campaign develops.

| family | what it records | record in code |
|---|---|---|
| **Clue** | something the investigators can follow up, with its source | `rules.investigation.Clue` |
| **Social** | a relationship fact that affects an interaction — trust, obligation, access | `world.graphs.Relationship` (the graph edge, read as a tag) |
| **Goal** | an outcome a character or faction is pursuing | `rules.goals.Goal` |
| **Psyche** | inner life: enduring traits, values, fears, habits, temporary states | `rules.scene_tags.PsycheTag` |
| **Astral** | a Noösphere fact that affects what someone can perceive, attempt or change | `rules.scene_tags.AstralTag` |

**Personality became Psyche.** `PersonalityTag` is kept as a deprecated alias in both modules so older code and
documents keep working; new code says `PsycheTag`. The campaign store's richer per-NPC record
(`world.narrative_tags.PsycheTag`: id, npc, trait, lever, under pressure, taboo) keeps its extra fields and projects
onto the portable tag through `to_family_tag()`, so a scene carries the short form while the store keeps the leverage.

**Astral is a family, not a subsystem.** An `AstralTag` has an owner, the fact, **what it acts on** — `perceive`,
`attempt` or `change`, the three the author named — and a `source`, because an entity's testimony and an independently
verified observation are different evidence. The domain field is closed on purpose: a fourth kind of claim belongs in a
new family, not in a quiet amendment to this one.

## Four graphs, unchanged

| graph | what its connections mean |
|---|---|
| **Physical** | routes between places the characters can physically reach |
| **Cyber** | network connections between devices and systems, with each device anchored to a physical location |
| **Story** | relationships and progression among series, episodes and scenes |
| **Social** | ties among people, groups and institutions — and a Social tag says what a tie means today |

There is still **no Astral graph**. #1178 and #1230 deferred it, and #1283 did not reopen it: Astral tags describe what a
character perceives or can attempt, which is a family of tags, not a map. A test asserts `WorldGraphs` has the four
families and no `astral` attribute, so adding one becomes a deliberate change.

## At the table

Use the graphs to find who or what is connected; read the tags to establish what is possible and what matters; when an
action calls for a roll, use the host RPG's procedure. The author's own example is the test case:

> An Astral tag lets Tony hear a presence name a witness. That statement *and its source* become a Clue. The Social
> graph shows who could introduce him; the Physical graph shows where to go; if he goes after corroborating camera
> footage, the Cyber graph locates the recorder and CWN resolves the hack.

Nothing in that chain needs a fifth mechanic. Each step is a graph lookup, a tag read, or a CWN procedure.

## What is enforced, and what is not

Enforced by `tests/test_tag_families_1283.py` (14 tests):

* the five families exist, each with a meaning;
* `psyche` is the name and `personality` is not a family;
* `PersonalityTag is PsycheTag` in both modules, and the store's `personality` view still resolves;
* the list is **open**: `register_family()` adds one, and refuses an empty name, an empty meaning, or a name already
  taken;
* an `AstralTag` cannot claim a fourth domain;
* `WorldGraphs` has four families and no `astral`.

Not enforced, because it is play, not code:

* whether a tag's wording is good, and whether the table remembers to change it only when something lasting happens;
* the playtest question from the issue — can one procedure carry a fleeting impression, an ongoing Social Memory Complex
  and a city-scale psychotronic effect? That answer comes from the table, and it may retire parts of #1261's procedure
  if it does;
* how the same scene reads under another cyberpunk RPG's rules.

## Open, and deliberately so

The issue is kept open for tag wording, examples and playtesting. The one structural question it raises that code cannot
answer: **which distinctions matter in play** — between a momentary impression and a persistent complex, and between an
entity's testimony and a verified fact. The `source` field and the `duration` field are this page's honest placeholders
for those two distinctions; whether they are enough is a table answer.
