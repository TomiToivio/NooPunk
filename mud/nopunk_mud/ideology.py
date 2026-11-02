"""LaclauGPT as a NooPunk mod on CWN characters (#1042) — the character-level layer, no LLM required.

Three different questions wear the same word "politics" in a game, and this module keeps them apart on purpose:

* **DA (discourse analysis)** — what an actor *said*: a statement about a signifier, with a stance, a demand
  and a source. Speech is not belief and not truth.
* **DNA (discourse network analysis)** — where actors *stand* relative to concepts: chains of equivalence and
  antagonistic frontiers. Position is not friendship.
* **SNA (social network analysis)** — who actually *knows* whom: ties, trust, debts. Relationship is not
  agreement.

The rule the whole design rests on: none of these may be collapsed into one friend/enemy score. An actor can
share every signifier with you and still be your enemy, and the data model has to be able to say so without a
special case. `Relationship` therefore has no ideological field, and `Statement` has no relationship field.

Deterministic by construction: authored statements in, graph arithmetic out. No model call, no sampling, no
hidden state. Two runs over the same fixtures produce the same numbers, which is what makes a faction's
politics arguable rather than oracular.

On top of the three layers the mod carries the two things a *game* needs from them: **goals** (an actor's
personal, institutional and ideological aims, recorded separately so they can disagree) and **append-only
dated profile versions** (a faction that changes its line in March leaves a trace instead of rewriting
February). ``reaction()`` is the one place the layers meet, and it meets them as three separate inputs
with the result carrying which ones were known — a first reaction, not an attitude score.

CWN is untouched. Nothing here resolves a check, changes an attribute or grants a bonus.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

STANCES = ("support", "oppose", "neutral")
VISIBILITY = ("public", "private", "secret")
ACTOR_KINDS = ("faction", "person", "outlet", "collective")

#: What a claim rests on. An assertion is not evidence and must never be counted as one.
#: ``outcome`` is a consequence the *rules* resolved and recorded (a check that failed, a clue that was
#: found, an order that was obeyed) — the one kind that is neither said nor seen by a witness.
EVIDENCE_KINDS = ("document", "testimony", "observation", "outcome", "rumour", "assertion")

#: Why an actor wants what it wants. The three are kept apart because they disagree in practice: an
#: institution's goal may be institutional survival while its officers pursue a personal one.
GOAL_KINDS = ("personal", "institutional", "ideological")

#: Reaction bands, coldest first. A band is a first-reaction *label*, not an attitude score: the
#: caller still owns what the NPC does with it.
REACTION_BANDS = ("hostile", "cold", "guarded", "neutral", "open", "warm")


class IdeologyError(ValueError):
    """A rule was about to be broken: unknown stance, collapsed categories, duplicate ids."""


@dataclass(frozen=True)
class Concept:
    """A signifier. Its meaning is contested by design; the gloss is a label, not a definition."""
    id: str
    gloss: str = ""

    def __post_init__(self):
        if not self.id:
            raise IdeologyError("a concept needs an id")


@dataclass(frozen=True)
class Actor:
    id: str
    kind: str = "faction"
    scope: str = ""          # network this actor speaks within (UNSA, SuomiNet, MarsNet Hype, ...)

    def __post_init__(self):
        if self.kind not in ACTOR_KINDS:
            raise IdeologyError(f"unknown actor kind {self.kind!r}")


@dataclass(frozen=True)
class Statement:
    """One articulation. What was said, about what, on whose authority, at which confidence."""
    actor: str
    concept: str
    stance: str
    demand: str = ""
    source: str = ""
    evidence: str = "assertion"
    confidence: float = 0.5
    visibility: str = "public"
    date: str = ""

    def __post_init__(self):
        if self.stance not in STANCES:
            raise IdeologyError(f"unknown stance {self.stance!r}")
        if self.evidence not in EVIDENCE_KINDS:
            raise IdeologyError(f"unknown evidence kind {self.evidence!r}")
        if not 0.0 <= self.confidence <= 1.0:
            raise IdeologyError("confidence is 0..1")
        if self.visibility not in VISIBILITY:
            raise IdeologyError(f"unknown visibility {self.visibility!r}")

    @property
    def is_evidence_backed(self) -> bool:
        """A rumour is still a claim, and an assertion is only somebody's word. ``outcome`` counts:
        the engine recorded what happened, which is stronger than a witness and weaker than a
        document only in the sense that it needs a date."""
        return self.evidence in ("document", "testimony", "observation", "outcome")


@dataclass(frozen=True)
class Goal:
    """What an actor is trying to get, and in which register.

    Three kinds are recorded separately on purpose. An institution can seek survival
    (``institutional``) while its director seeks vindication (``personal``) and both claim the same
    signifier (``ideological``). Collapsing them into "goals" makes every actor single-minded.
    """
    actor: str
    kind: str
    text: str
    date: str = ""

    def __post_init__(self):
        if self.kind not in GOAL_KINDS:
            raise IdeologyError(f"unknown goal kind {self.kind!r}")
        if not self.text.strip():
            raise IdeologyError("a goal needs a statement of what it wants")


@dataclass(frozen=True)
class ProfileVersion:
    """A dated snapshot of an actor's declared position, kept append-only.

    A shift is traceable only if earlier statements are never rewritten: the model refuses to replace
    a version, so "the faction changed its line in March" is a fact with a date instead of a
    contradiction in the data.
    """
    actor: str
    date: str
    label: str = ""
    concepts: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self):
        if not self.date:
            raise IdeologyError("a profile version needs the date it was recorded")
        object.__setattr__(self, "concepts", tuple(self.concepts))


@dataclass(frozen=True)
class Relationship:
    """SNA. Deliberately has no stance, no concept and no ideology field."""
    a: str
    b: str
    trust: int = 0            # -4..+4, same scale as reputation but a different question
    debt: str = ""            # free text: who owes whom, and what
    visibility: str = "public"

    def __post_init__(self):
        if self.a == self.b:
            raise IdeologyError("a relationship needs two different actors")
        if not -4 <= self.trust <= 4:
            raise IdeologyError("trust is -4..+4")
        if self.visibility not in VISIBILITY:
            raise IdeologyError(f"unknown visibility {self.visibility!r}")


@dataclass
class Discourse:
    """One persistent social/ideological world state."""
    concepts: dict[str, Concept] = field(default_factory=dict)
    actors: dict[str, Actor] = field(default_factory=dict)
    statements: list[Statement] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    goals: list[Goal] = field(default_factory=list)
    profiles: list[ProfileVersion] = field(default_factory=list)

    # ---- authoring -------------------------------------------------------
    def add_concept(self, concept: Concept) -> None:
        if concept.id in self.concepts:
            raise IdeologyError(f"concept {concept.id!r} already exists")
        self.concepts[concept.id] = concept

    def add_actor(self, actor: Actor) -> None:
        if actor.id in self.actors:
            raise IdeologyError(f"actor {actor.id!r} already exists")
        self.actors[actor.id] = actor

    def add_goal(self, goal: Goal) -> None:
        """Record one goal. The same actor may hold one of each kind; an unknown actor is refused."""
        if goal.actor not in self.actors:
            raise IdeologyError(f"unknown actor {goal.actor!r}")
        self.goals.append(goal)

    def goals_of(self, actor: str, kind: str | None = None) -> list[str]:
        """Goal texts for an actor, optionally narrowed to one register."""
        if kind is not None and kind not in GOAL_KINDS:
            raise IdeologyError(f"unknown goal kind {kind!r}")
        return [g.text for g in self.goals
                if g.actor == actor and (kind is None or g.kind == kind)]

    def record_profile(self, version: ProfileVersion) -> None:
        """Append one dated profile version.

        Append-only is the rule, so two things are refused: a version dated earlier than the last one
        already recorded for that actor (that would make the history unreadable) and an exact
        duplicate date with different content (two versions cannot own the same day).
        """
        if version.actor not in self.actors:
            raise IdeologyError(f"unknown actor {version.actor!r}")
        previous = [p for p in self.profiles if p.actor == version.actor]
        if previous:
            last = max(previous, key=lambda p: p.date)
            if version.date < last.date:
                raise IdeologyError(
                    f"{version.actor}: a profile is append-only, {version.date} precedes {last.date}")
            if version.date == last.date and version != last:
                raise IdeologyError(
                    f"{version.actor}: {version.date} already has a different profile version")
        self.profiles.append(version)

    def profile_at(self, actor: str, date: str) -> ProfileVersion | None:
        """The version in force on a date: the latest one recorded on or before it."""
        candidates = [p for p in self.profiles if p.actor == actor and p.date <= date]
        return max(candidates, key=lambda p: p.date) if candidates else None

    def articulate(self, statement: Statement) -> None:
        if statement.actor not in self.actors:
            raise IdeologyError(f"unknown actor {statement.actor!r}")
        if statement.concept not in self.concepts:
            raise IdeologyError(f"unknown concept {statement.concept!r}")
        self.statements.append(statement)

    def relate(self, relationship: Relationship) -> None:
        for who in (relationship.a, relationship.b):
            if who not in self.actors:
                raise IdeologyError(f"unknown actor {who!r}")
        self.relationships.append(relationship)

    # ---- DNA projections (deterministic) ---------------------------------
    def visible(self, viewer_scope: str, *, shares_secret: bool = False) -> list[Statement]:
        """What a viewer may read.

        Three levels, and the difference between the last two is the point:
        ``public``  — everyone.
        ``private`` — the speaker's own network knows it was said; outsiders do not.
        ``secret``  — need-to-know. Even the speaker's own network does not see it without ``shares_secret``,
                      which is the flag for "someone told you".
        """
        out = []
        for s in self.statements:
            if s.visibility == "public":
                out.append(s)
            elif s.visibility == "private":
                if self.actors[s.actor].scope == viewer_scope:
                    out.append(s)
            elif shares_secret and self.actors[s.actor].scope == viewer_scope:
                out.append(s)
        return out

    def positions(self, *, evidence_only: bool = False) -> dict[str, dict[str, int]]:
        """actor -> concept -> net stance. Weighted by confidence, never by relationship."""
        table: dict[str, dict[str, int]] = {}
        for s in self.statements:
            if evidence_only and not s.is_evidence_backed:
                continue
            weight = 1 if s.stance == "support" else -1 if s.stance == "oppose" else 0
            if weight == 0:
                continue
            row = table.setdefault(s.actor, {})
            row[s.concept] = row.get(s.concept, 0) + weight
        return {actor: dict(sorted(row.items())) for actor, row in sorted(table.items())}

    def contested_concepts(self) -> dict[str, dict[str, list[str]]]:
        """Signifiers claimed by both sides — the most useful object in the system, and the plot engine."""
        out: dict[str, dict[str, list[str]]] = {}
        for concept in sorted(self.concepts):
            supporters, opponents = [], []
            for actor, row in self.positions().items():
                net = row.get(concept, 0)
                if net > 0:
                    supporters.append(actor)
                elif net < 0:
                    opponents.append(actor)
            if supporters and opponents:
                out[concept] = {"support": supporters, "oppose": opponents}
        return out

    def overlap(self, a: str, b: str) -> int:
        """How many signifiers two actors read the same way. Agreement, nothing more."""
        pa, pb = self.positions().get(a, {}), self.positions().get(b, {})
        return sum(1 for c in set(pa) & set(pb) if pa[c] == pb[c] and pa[c] != 0)

    def antagonists_are_not_enemies(self, a: str, b: str) -> dict[str, object]:
        """The separation, made checkable: ideological overlap and personal trust are independent."""
        trust = None
        for r in self.relationships:
            if {r.a, r.b} == {a, b}:
                trust = r.trust
                break
        return {"overlap": self.overlap(a, b), "trust": trust}

    def reaction(self, actor: str, viewer: str, *, concept: str | None = None) -> dict:
        """One NPC's first reaction to another actor, from three separate inputs.

        ``concept`` is the signifier in play (the thing being asked about); without it only overlap
        and trust contribute, and the result says so rather than guessing a stance.
        """
        if actor not in self.actors or viewer not in self.actors:
            raise IdeologyError("a reaction needs two known actors")
        stance = None
        if concept is not None:
            pa = self.positions().get(actor, {}).get(concept, 0)
            pv = self.positions().get(viewer, {}).get(concept, 0)
            if pa and pv:
                stance = "support" if (pa > 0) == (pv > 0) else "oppose"
        trust_raw = self.antagonists_are_not_enemies(actor, viewer)["trust"]
        trust = int(trust_raw) if isinstance(trust_raw, int) else None
        return reaction(overlap=self.overlap(actor, viewer), stance=stance, trust=trust)

    # ---- persistence ------------------------------------------------------
    def to_dict(self) -> dict:
        return {
            "concepts": {k: asdict(v) for k, v in sorted(self.concepts.items())},
            "actors": {k: asdict(v) for k, v in sorted(self.actors.items())},
            "statements": [asdict(s) for s in self.statements],
            "relationships": [asdict(r) for r in self.relationships],
            "goals": [asdict(g) for g in self.goals],
            "profiles": [asdict(p) for p in self.profiles],
        }

    @classmethod
    def from_dict(cls, data: dict) -> Discourse:
        d = cls(
            concepts={k: Concept(**v) for k, v in (data.get("concepts") or {}).items()},
            actors={k: Actor(**v) for k, v in (data.get("actors") or {}).items()},
            statements=[Statement(**s) for s in data.get("statements", [])],
            relationships=[Relationship(**r) for r in data.get("relationships", [])],
            goals=[Goal(**g) for g in data.get("goals", [])],
            profiles=[ProfileVersion(**p) for p in data.get("profiles", [])],
        )
        return d


def reaction(*, overlap: int, stance: str | None = None, trust: int | None = None) -> dict:
    """A deterministic NPC first reaction, computed from three inputs kept visibly separate.

    The rule exists because the alternative — one "attitude" number — is how a simulation quietly
    turns politics into like/dislike. Here:

    * **overlap** (DNA) is how many signifiers two actors read the same way: +1 at 2, +2 at 4.
    * **stance** on the signifier actually in play: agreement +2, disagreement −2, silence 0. The
      question on the table weighs more than general agreement, which is what makes a colleague's
      disagreement register instead of being drowned by shared slogans.
    * **trust** (SNA) is the personal tie: its half, rounded toward zero, so ±1 is worth 0.

    Two caps carry the design: without a positive tie the ceiling is ``open`` (warmth is a
    relationship, not an opinion), and with a negative tie the ceiling is ``guarded`` (contempt
    outranks agreement). A colleague who disagrees about the case is therefore ``neutral``, not
    ``hostile``: hostility needs a bad tie, not a dispute.
    The result carries its inputs so a player can be told *why*, and ``trust``/``stance`` being
    unknown is reported as unknown rather than defaulted to friendship.
    """
    if overlap < 0:
        raise IdeologyError("overlap cannot be negative")
    if stance is not None and stance not in STANCES:
        raise IdeologyError(f"unknown stance {stance!r}")
    if trust is not None and not -4 <= trust <= 4:
        raise IdeologyError("trust is -4..+4")

    score = 0
    if overlap >= 4:
        score += 2
    elif overlap >= 2:
        score += 1
    if stance == "support":
        score += 2
    elif stance == "oppose":
        score -= 2
    if trust is not None:
        score += int(trust / 2)          # truncates toward zero: ±1 point of trust is not warmth

    index = max(0, min(len(REACTION_BANDS) - 1, 3 + score))
    # Warmth is a tie, not an opinion: without a positive personal relationship the ceiling is
    # "open". Otherwise a well-briefed stranger would read as a friend, which is precisely the
    # collapse this module exists to prevent.
    if trust is None or trust <= 0:
        index = min(index, REACTION_BANDS.index("open"))
    if trust is not None and trust < 0:
        index = min(index, REACTION_BANDS.index("guarded"))
    band = REACTION_BANDS[index]
    return {
        "band": band,
        "score": score,
        "inputs": {"overlap": overlap, "stance": stance, "trust": trust},
        "unknown": [name for name, value in
                    (("stance", stance), ("trust", trust)) if value is None],
        # The separation the module exists for: a band never implies a relationship or a belief.
        "means": {"band_is_attitude": False, "band_is_trust": False},
    }
