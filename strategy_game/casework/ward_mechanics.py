"""The corpus's mechanics, bound to the *Listening Ward* case.

The *Ubiquitous Maniacs* corpus arrived as two things that did not fit together: a body of
authorial mechanics written against its own Fate kernel, and a scenario that could not be
played because the data it needed was never committed upstream.

Both halves are now in the live system, and this module is where they meet.

* The **mechanics** were ported onto this repository's engine — :mod:`strategy_game.rpg.projection`
  (psyche projection and what it costs), :mod:`strategy_game.rpg.psychosurgery` (consent-gated
  changes to a patient) and :mod:`strategy_game.rpg.psi` (PSI as trajectory steering, on the one
  Fate resolver).
* The **scenario** is the *Listening Ward* case
  (:mod:`strategy_game.casework.ubiquitous_maniacs`), which is the canonical playable
  adaptation of the corpus's treatment-lab premise.

What this module supplies is the part a case file cannot express, because it is **state**
rather than **declaration**:

* a **psychotherapeutic session** for the ward's patient, with the consent gate the case turns
  on;
* a **projection session** for the two witnesses who each saw a different person in the chair
  and are each certain of a different layer;
* the **PSI context** the ward's interior produces, so that a psychical attempt in the records
  room is harder for a *stated* reason.

Why the consent gate is the point
---------------------------------

The case's central fact is that the ward ran a procedure on a patient and the records do not
agree about what was asked. That is not a line of story: it is a **state** that the mechanics
can represent and check. The session's ``consent`` flag is **False**, because nobody asked her.
The party may *read* the patient — reveal what the procedure exposed — without consent; every
call that would *change* her raises
:class:`~strategy_game.rpg.psychosurgery.PsychosurgeryError`. That asymmetry is the setting's
premise, and the case's own resolution already protects the patient's right to give evidence.

Why the two witnesses never agree
---------------------------------

The model's four hypothesis weights — dream, psychedelic state, virtual construction, non-local
noetic projection — are never resolved, because the case never settles what the patient
experienced. One witness believes she was dreaming and one believes she was in a construction,
and the disagreement is the thing the party has to work with.

The boundary
------------

Nothing here decides an outcome. The projection model charges and tracks; the PSI model rolls
through the one resolver; the consent model refuses. What a character *means* by any of it is
still the fiction's, and the case's resolutions still decide what can be *proved*.
"""
from __future__ import annotations

from random import Random

from ..rpg.fate import Character
from ..rpg.projection import ProjectionLayer, ProjectionSession
from ..rpg.psi import PsiActionContext, PsiMode, resolve_psi_action
from ..rpg.psychosurgery import PsychosurgerySession

__all__ = [
    "ARCHIVE_PATH",
    "PATIENT_ID",
    "WITNESS_A_ID",
    "WITNESS_B_ID",
    "attempt_remote_perception",
    "patient_session",
    "ward_context",
    "witness_projections",
]

#: The archive the corpus was imported into, and the case's own recorded provenance.
ARCHIVE_PATH = "archive/ubiquitous-maniacs-2026-10/"

#: The patient. A scenario fiction, not a canon character.
PATIENT_ID = "ward-patient"
#: The two witnesses who each saw a different person in the chair.
WITNESS_A_ID = "ward-witness-a"
WITNESS_B_ID = "ward-witness-b"


def patient_session(patient: Character, *, operator: str = "the ward's attending physician") -> PsychosurgerySession:
    """A psychosurgical session with the consent gate **closed**.

    ``consent=False`` is the whole point: this is what a procedure performed on someone who
    was not asked looks like in the model. The party may call :meth:`reveal_aspect` on the
    returned session and learn what the procedure exposed; every call that would *change* her
    raises :class:`~strategy_game.rpg.psychosurgery.PsychosurgeryError`.
    """
    return PsychosurgerySession(patient=patient, operator=operator, consent=False)


def witness_projections() -> dict[str, ProjectionSession]:
    """The two witnesses' projections, each certain of a different layer.

    The first believes she was dreaming. The second believes she was in a virtual
    construction. The model's four hypothesis weights are left standing, because **the case
    never settles which is true** — and the split between the two witnesses is the
    disagreement the party has to work with.
    """
    dreaming = ProjectionSession()
    dreaming.enter(preparation=0, anchor_support=0)
    dreaming.observe("witness-a: a second figure in the chair", {ProjectionLayer.DREAM: 20})

    constructed = ProjectionSession()
    constructed.enter(preparation=0, anchor_support=0)
    constructed.observe("witness-b: a second figure in the chair", {ProjectionLayer.VIRTUAL: 20})

    return {WITNESS_A_ID: dreaming, WITNESS_B_ID: constructed}


def ward_context(*, psi_rating: int = 0) -> PsiActionContext:
    """The ward's own properties, as a PSI context.

    The records room is a long, semantically distant place: a machine that is old, a procedure
    that means one thing to the patient and another to the paperwork, and a lot of local noise
    from the running equipment. That makes a directed psychical act here *harder* than it
    would be in an ordinary room, for reasons the party can state.
    """
    return PsiActionContext(
        semantic_distance=3,
        corridor_strength=1,
        bifurcation_openness=1,
        affective_salience=2,
        composite_coherence=0,
        instrumentality=3,
        local_noise=2,
        psi_rating=psi_rating,
    )


def attempt_remote_perception(
    actor: Character,
    target: str,
    *,
    difficulty: int = 3,
    rng: Random,
    context: PsiActionContext | None = None,
):
    """A remote-perception attempt in the records room, on the live resolver.

    The actor must carry the ``REMOTE_VIEWER`` capability, or the attempt is refused before any
    dice — the same rule every other capability-gated action in the engine follows.
    """
    return resolve_psi_action(
        actor,
        target,
        PsiMode.REMOTE_PERCEPTION,
        difficulty,
        context=context if context is not None else ward_context(),
        rng=rng,
    )
