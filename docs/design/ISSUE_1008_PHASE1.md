# Phase 1 delivered: rank, scoped reputation, goals (#1008)

**Status: implemented and tested.** `mud/nopunk_mud/social.py`, `mud/tests/test_social_1008.py` — 15 tests,
all passing, and the whole MUD suite stays green.

> **Citations.** Page references below are the ranges the author's brief supplies (#1008): *SWN Revised Deluxe*
> Factions chapter from printed p. 211, *Houses of the Landsraad* House Management from printed p. 86, CWN
> Deluxe for skills/reactions/schemes/Heat. **This repository holds no copy of those books.** Nothing here is
> quoted, and every page number is recorded as an author-supplied pointer to be verified against the licensed
> text before implementation, not as a verified citation.

## What the code does

**Rank is authority, not skill.** `Membership(organization, rank 0–4)` answers exactly one question: *may this
agent propose and lead a mission of N agents?* Rank 0 → 1 agent, 1 → 2, 2 → 4, 3 and 4 → no head-count limit
because chain of command governs those, not arithmetic. It grants **no** bonus to a CWN check, **no** free skill
level, and **no** extra SWN faction action.

**Promotion is an audited event.** `promote(reason=..., authorized_by=...)` refuses silence: a promotion with no
reason or no authority raises. The history is carried on the membership, so a rank is always explainable.

**Reputation is one value in one scope.** `Reputation(scope, value ∈ −4..+4, visibility ∈ public/private/secret)`.
Scope is a network (`UNSA`, `SipuliVerkko`, `SuomiNet`, `Internet`, `MarsNet Hype`) or a person (`npc:<id>`).
Zero means **unknown**, not hostile.

**Exactly one reputation applies to a reaction.** `reaction_modifier(reputations, chosen_scope=...)` requires the
caller to name the scope, refuses an unknown scope rather than defaulting to zero, and refuses two records for
one scope as ambiguous. Summing is not merely discouraged — it is not an operation the API offers.

**CWN is untouched.** `reaction(dice, charisma_modifier, reputation_value, known=...)` adds the overlay once to
the published 2d6 result and returns the band (`≤2` hostile, `3–5` unfriendly, `6–8` neutral, `9–11`
unusually friendly, `12+` helpful). `known=False` means the NPC does not know the reputation and the overlay
contributes **zero** — reputation shapes initial disposition, it is not mind control.

**Visibility is separate from value.** A secret UNSA record is visible inside UNSA, invisible to SuomiNet, and
visible to an outsider only if `shares_secret`. Knowing *of* a person and knowing *what they did* are different
things, and the code keeps them apart.

**Goals are state, not bonuses.** `Goal(owner, text, kind, status, priority, depends_on)` — a descriptive tag with
a state machine. Nothing here awards a stat for a well-phrased aspiration.

**Persistence** is a JSON dictionary (`SocialRecord.to_dict/from_dict`) with a round-trip test.

## The balance question the issue raises

±4 on 2d6 is enormous: it can move a roll across three bands. Phase 1 ships the raw modifier **and** the `known`
gate, and the design position is that ±4 must be rare and *earned* — a −4 with UNSA should mean wanted or
disowned, not "somewhat disliked". Before any NPC uses it in the campaign, one playtest must confirm that a ±4
encounter reads as an event rather than as a coin flip with extra steps.

## What Phase 1 deliberately does not do

- No Evennia commands yet (`factions`, `rank`, `reputation`, `goals`) — those are thin wrappers over this module,
  and the MUD server does not boot in this environment yet (#966).
- No SWN faction turns, no assets, no FacCreds. Phase 3.
- No ideology. Phase 2.
- No XP or reward pipeline: promotion perks are *permissions*, and CWN's own advancement is the only source of
  levels.
