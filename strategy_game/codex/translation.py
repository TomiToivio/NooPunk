"""First contact as a research problem: communication modes, a translation ladder, and honest ambiguity.

The issue's major gameplay hook: "A first-contact encounter **should not start in English**", and
"*Arrival* is inspiration for the **dramatic research problem**, not a commitment to its linguistic
determinism". Two MVP constraints from the same section:

* "Use readable player-facing pseudo-translation with marked confidence and alternatives; do **not**
  require a full computational linguistics engine or generated conlang for MVP."
* "No universal automatic translation. Even a machine translator/AGI can confidently hallucinate and
  break diplomacy."

So this module models **partial understanding as data**:

* :class:`CommunicationMode` is the issue's own list of ways a being might communicate;
* :class:`TranslationStage` is the issue's own ladder, from detecting a signal to negotiating intent —
  a *progress marker*, not a rule, and nothing here advances it automatically;
* :class:`Meaning` carries a candidate reading with a display-confidence label, never a probability;
* :class:`Lexicon` holds **several candidates per sign** and has no method that returns a single
  answer — a sign that is ambiguous stays ambiguous, which is the whole dramatic point;
* a **tested-but-wrong** reading is a *state* the session keeps, not a reset: :meth:`ContactSession.advance_to`
  refuses to move backwards, so a falsified reading closes a hypothesis while the entity stays open, which
  is `rulebook/16_CONFEDERACY_SOURCE_AND_CONTACT.md` §16.4 — "Failure should generate information, risk or
  new choices rather than an automatic 'you can never know'";
* :func:`machine_candidate` reproduces the issue's warning that an automatic translator can be
  confidently wrong by returning a *low-confidence* candidate that is explicitly marked as a guess.

Nothing here decides what a successful interpretation *does* on the board. The issue notes that
"successful interpretation can unlock diplomacy, treaties, research and ideology signifiers", and that
is a strategy-layer consequence needing Gate C — so a session records the outcome in text and the rule
layer, when approved, reads it.

Entity *content* (lexicon entries for a specific people) is author-reviewed material, not a code
contract.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Mapping

from .entities import CodexError, _enum_value


class CommunicationMode(Enum):
    """The communication modes the issue lists. Free of any ranking or reliability claim."""

    SPOKEN = "spoken"
    GESTURE = "gesture"
    PHEROMONE = "pheromone"
    COLOR_LIGHT = "color_light"
    ELECTROMAGNETIC = "electromagnetic"
    WRITTEN_LOGOGRAM = "written_logogram"
    CHEMICAL_GRADIENT = "chemical_gradient"
    NETWORK_PULSE = "network_pulse"
    TELEPATHY = "telepathy"
    SYMBOLIC_VISION = "symbolic_vision"
    #: Information embedded in social relations rather than transmitted as a message.
    SOCIAL_EMBEDDED = "social_embedded"
    #: The absence of signal. The issue lists silence as a mode, and it is not "no data".
    SILENCE = "silence"


#: The declared value set, so callers can validate without constructing an enum member.
COMMUNICATION_MODES: tuple[str, ...] = tuple(mode.value for mode in CommunicationMode)


#: The **load-bearing signifiers** the issue names as the pragmatics traps of first contact — the words
#: whose meaning is not equivalent across minds. The issue's own line: "Distinguish lexical translation
#: from **pragmatics** ('gift', 'weapon', 'we', 'voluntary', 'service', 'harvest', 'ownership',
#: 'individual')." This is the conventional set :attr:`EntityRecord.referent_collisions` names when it
#: records which of them a given entity expresses non-equivalently (the UCCC "we" as a social memory
#: complex of thousands of bodies, a metallic sphere's "individual" as one node of a planetary swarm, a
#: vegetal migrant for whom "now" spans a century). No conlang and no engine: the difficulty is authored.
LOAD_BEARING_SIGNIFIERS: tuple[str, ...] = (
    "gift", "weapon", "we", "voluntary", "service", "harvest", "ownership", "individual",
)


class TranslationStage(Enum):
    """The issue's translation ladder, in order. A progress marker; no rule advances it."""

    DETECT_SIGNAL = "detect_signal"
    INFER_AGENTS = "infer_agents"
    SHARED_REFERENTS = "shared_referents"
    PROPOSE_MEANINGS = "propose_meanings"
    TEST_UNDER_UNCERTAINTY = "test_under_uncertainty"
    NEGOTIATE_INTENT = "negotiate_intent"


#: The ladder in order, for a caller that wants to show it or compare two sessions' progress.
TRANSLATION_LADDER: tuple[TranslationStage, ...] = tuple(TranslationStage)


class Confidence(Enum):
    """A **display** label on a candidate reading.

    It is deliberately not a probability: a number would invite reading it as a mechanic, and no rule
    may consume it. The vocabulary is a UI convention the author can replace.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class Meaning:
    """One candidate reading of a sign, with its display confidence and a note."""

    text: str
    confidence: Confidence = Confidence.LOW
    note: str = ""

    def __post_init__(self) -> None:
        if not str(self.text).strip():
            raise CodexError("a candidate meaning needs text")

    def to_dict(self) -> dict[str, Any]:
        return {"text": self.text, "confidence": self.confidence.value, "note": self.note}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Meaning:
        return cls(
            text=str(data.get("text", "")),
            confidence=_enum_value(Confidence, data.get("confidence"), Confidence.LOW, "confidence"),
            note=str(data.get("note", "")),
        )


@dataclass
class LexiconEntry:
    """One sign and **every** candidate reading attached to it. Multiple candidates is the norm."""

    sign: str
    meanings: tuple[Meaning, ...] = ()
    #: What part of the message this sign seems to occupy (a word, a clause, a gesture). Free text.
    context: str = ""

    def __post_init__(self) -> None:
        if not str(self.sign).strip():
            raise CodexError("a lexicon entry needs a sign")
        self.meanings = tuple(self.meanings)

    @property
    def is_ambiguous(self) -> bool:
        """True when the lexicon cannot settle on one reading. Usually true, and not a failure."""
        return len({meaning.text for meaning in self.meanings}) > 1

    def add(self, meaning: Meaning) -> LexiconEntry:
        self.meanings = self.meanings + (meaning,)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "sign": self.sign,
            "meanings": [meaning.to_dict() for meaning in self.meanings],
            "context": self.context,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> LexiconEntry:
        return cls(
            sign=str(data.get("sign", "")),
            meanings=tuple(Meaning.from_dict(item) for item in (data.get("meanings") or ())),
            context=str(data.get("context", "")),
        )


@dataclass
class Lexicon:
    """A partial lexicon. Partial is the point: :meth:`entries` is not expected to be complete."""

    entries: dict[str, LexiconEntry] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.entries)

    def add(self, entry: LexiconEntry) -> LexiconEntry:
        self.entries[entry.sign] = entry
        return entry

    def propose(self, sign: str, text: str, confidence: Confidence = Confidence.LOW,
                note: str = "") -> LexiconEntry:
        """Propose one reading of a sign, creating the entry if the sign is new."""
        entry = self.entries.get(sign)
        if entry is None:
            entry = self.add(LexiconEntry(sign=sign))
        return entry.add(Meaning(text=text, confidence=confidence, note=note))

    def candidates(self, sign: str) -> tuple[Meaning, ...]:
        """**Every** reading of a sign. There is no method here that returns a single translation."""
        entry = self.entries.get(sign)
        return () if entry is None else entry.meanings

    def ambiguous_signs(self) -> tuple[str, ...]:
        return tuple(sign for sign, entry in self.entries.items() if entry.is_ambiguous)

    def to_dict(self) -> dict[str, Any]:
        return {"entries": {key: self.entries[key].to_dict() for key in sorted(self.entries)}}

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Lexicon:
        return cls(entries={
            str(key): LexiconEntry.from_dict(payload)
            for key, payload in (data.get("entries") or {}).items()
        })


def machine_candidate(text: str, *, note: str = "") -> Meaning:
    """A machine translator's guess: a reading that is explicitly marked as unreliable.

    The issue warns that "even a machine translator/AGI can confidently hallucinate and break
    diplomacy", so an automatic attempt enters the lexicon at :attr:`Confidence.LOW` with a note saying
    where it came from. Nothing here decides that the guess is right, and nothing may treat it as a
    confirmed reading without a human or in-fiction verification step.
    """
    return Meaning(
        text=str(text),
        confidence=Confidence.LOW,
        note=note or "machine-proposed reading; not verified, may be confidently wrong",
    )


@dataclass
class ContactAttempt:
    """One recorded attempt to interpret a sign. A record, not a resolution roll."""

    stage: TranslationStage
    sign: str
    meaning_text: str
    confidence: Confidence = Confidence.LOW
    #: How the attempt was made ("asked the interpreter", "compared two encounters", "ran the analyser").
    method: str = ""
    #: What happened in the fiction. Free text: the board consequence belongs to the strategy layer.
    outcome: str = ""
    #: The seed of any roll that accompanied the attempt, for the audit trail.
    seed: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "stage": self.stage.value,
            "sign": self.sign,
            "meaning_text": self.meaning_text,
            "confidence": self.confidence.value,
            "method": self.method,
            "outcome": self.outcome,
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ContactAttempt:
        return cls(
            stage=_enum_value(
                TranslationStage, data.get("stage"), TranslationStage.DETECT_SIGNAL, "stage"
            ),
            sign=str(data.get("sign", "")),
            meaning_text=str(data.get("meaning_text", "")),
            confidence=_enum_value(Confidence, data.get("confidence"), Confidence.LOW, "confidence"),
            method=str(data.get("method", "")),
            outcome=str(data.get("outcome", "")),
            seed=None if data.get("seed") is None else int(data["seed"]),
        )


@dataclass
class ContactSession:
    """A first-contact encounter: who, how far along the ladder, what has been read so far.

    The session deliberately has **no success condition**. It records proposals, tests and outcomes;
    what a successful interpretation unlocks is a strategy rule ("can unlock diplomacy, treaties,
    research and ideology signifiers") and is not modelled here.
    """

    entity_id: str
    #: The modes this encounter is being attempted through. Empty means "not established yet".
    modes: tuple[CommunicationMode, ...] = ()
    stage: TranslationStage = TranslationStage.DETECT_SIGNAL
    lexicon: Lexicon = field(default_factory=Lexicon)
    attempts: list[ContactAttempt] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not str(self.entity_id).strip():
            raise CodexError("a contact session needs the entity it is about")
        self.modes = tuple(self.modes)

    # -- the ladder --------------------------------------------------------------------------------

    @property
    def stage_index(self) -> int:
        """Position on the ladder, 0-based."""
        return TRANSLATION_LADDER.index(self.stage)

    def advance_to(self, stage: TranslationStage) -> TranslationStage:
        """Move to a later rung. Refuses to go backwards, so progress is monotonic and auditable."""
        if TRANSLATION_LADDER.index(stage) < self.stage_index:
            raise CodexError(
                f"the translation ladder moves forward only: {self.stage.value!r} -> {stage.value!r}"
            )
        self.stage = stage
        return stage

    # -- interpretation ----------------------------------------------------------------------------

    def propose(self, sign: str, text: str, confidence: Confidence = Confidence.LOW,
                method: str = "", outcome: str = "", seed: int | None = None,
                note: str = "") -> ContactAttempt:
        """Record a proposed reading. The lexicon keeps it beside the rivals it already had."""
        self.lexicon.propose(sign, text, confidence, note)
        attempt = ContactAttempt(
            stage=self.stage, sign=sign, meaning_text=text, confidence=confidence,
            method=method, outcome=outcome, seed=seed,
        )
        self.attempts.append(attempt)
        return attempt

    def meanings_for(self, sign: str) -> tuple[Meaning, ...]:
        """Every candidate reading. A caller showing one of them without the others is misreporting."""
        return self.lexicon.candidates(sign)

    @property
    def unresolved_signs(self) -> tuple[str, ...]:
        """Signs that carry more than one reading — the open questions of the encounter."""
        return self.lexicon.ambiguous_signs()

    def is_ready_to_negotiate(self) -> bool:
        """True once the ladder has reached intent negotiation **and** something has been read.

        This is a readiness *query*, not a gate: it does not unlock anything on its own.
        """
        return (self.stage is TranslationStage.NEGOTIATE_INTENT
                and bool(self.lexicon.entries))

    # -- serialization -----------------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "modes": [mode.value for mode in self.modes],
            "stage": self.stage.value,
            "lexicon": self.lexicon.to_dict(),
            "attempts": [attempt.to_dict() for attempt in self.attempts],
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> ContactSession:
        return cls(
            entity_id=str(data.get("entity_id", "")),
            modes=tuple(
                _enum_value(CommunicationMode, item, None, "modes")
                for item in (data.get("modes") or ())
            ),
            stage=_enum_value(
                TranslationStage, data.get("stage"), TranslationStage.DETECT_SIGNAL, "stage"
            ),
            lexicon=Lexicon.from_dict(data.get("lexicon") or {}),
            attempts=[ContactAttempt.from_dict(item) for item in (data.get("attempts") or ())],
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True, indent=2)

    @classmethod
    def from_json(cls, text: str) -> ContactSession:
        return cls.from_dict(json.loads(text))


def signal_variant(modes: Iterable[CommunicationMode], rng: random.Random | None = None, *,
                   seed: int | None = None) -> str:
    """Pick an arbitrary readable *prompt* for an encounter, given its communication modes.

    The issue wants "readable player-facing pseudo-translation ... and alternatives" without a conlang.
    So this returns which mode the encounter presents through first — a presentation choice, chosen
    deterministically from a seed, so a replay shows the same opening. It does not decide anything about
    the signal's content.
    """
    pool = tuple(modes)
    if not pool:
        raise CodexError("an encounter needs at least one communication mode to present through")
    if rng is None:
        rng = random.Random(seed)
    return rng.choice(pool).value
