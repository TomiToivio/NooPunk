"""NHI entity codex for the NoöPunk × LaclauGPT crossover (issue #348).

Four kinds of entity, one record type, and first contact modelled as a research problem:

* :mod:`strategy_game.codex.entities` — :class:`EntityRecord` and its two independent axes
  (ontology, and form), plus the epistemic register.
* :mod:`strategy_game.codex.codex` — :class:`Codex`, with a player-facing projection that withholds
  GM-only material structurally rather than by convention.
* :mod:`strategy_game.codex.translation` — communication modes, the translation ladder, a lexicon that
  keeps rival readings, and the explicit warning that a machine translator may be confidently wrong.

The data file is ``strategy_game/data/codex.json``.

**What this package is not.** It defines no capability, statistic, mechanic, threshold or effect for any
entity; ``AGENTS.md`` §4 reserves "NHI taxonomy or capabilities", and this is the record layer a later
approved subsystem would read from. Entity *content* is reviewed by the author and by playtesting, never
by a test (#271) — only this code's behaviour is tested.
"""
from .codex import CODEX_PATH, Codex, load_codex
from .entities import (
    ENTITY_ONTOLOGIES,
    KNOWLEDGE_STATUSES,
    CodexError,
    EntityForm,
    EntityOntology,
    EntityRecord,
    KnowledgeStatus,
)
from .translation import (
    COMMUNICATION_MODES,
    TRANSLATION_LADDER,
    CommunicationMode,
    Confidence,
    ContactAttempt,
    ContactSession,
    Lexicon,
    LexiconEntry,
    Meaning,
    TranslationStage,
    machine_candidate,
    signal_variant,
)

__all__ = [
    # entities
    "ENTITY_ONTOLOGIES",
    "KNOWLEDGE_STATUSES",
    "CodexError",
    "EntityForm",
    "EntityOntology",
    "EntityRecord",
    "KnowledgeStatus",
    # codex
    "CODEX_PATH",
    "Codex",
    "load_codex",
    # translation
    "COMMUNICATION_MODES",
    "TRANSLATION_LADDER",
    "CommunicationMode",
    "Confidence",
    "ContactAttempt",
    "ContactSession",
    "Lexicon",
    "LexiconEntry",
    "Meaning",
    "TranslationStage",
    "machine_candidate",
    "signal_variant",
]
