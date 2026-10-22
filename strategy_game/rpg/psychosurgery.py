"""Consent-aware, ontology-neutral psychosurgery.

Ported from the *Ubiquitous Maniacs* corpus (``archive/ubiquitous-maniacs-2026-10/src/rpg/
psychosurgery.py``) onto this repository's engine, so that the corpus's material and the live
RPG are **one** system rather than two parallel ones.

What it models
--------------

A psychosurgical procedure that changes who somebody is. The module's whole point is the
**consent gate**: revealing something about a patient is a read, and reading is permitted;
*integrating* it into them, treating a consequence, or resonating with another psyche are
writes, and every write requires the patient's consent. Without consent the module refuses.

That refusal is not a safety wrapper bolted on afterwards. It is the setting's premise. NoöPunk
treats mind-altering medicine as ordinary, and the ordinary treatment of an ordinary procedure
is what makes an unconsented one a *crime* rather than an inconvenience. The packaged *Intake*
case (``:mod:`strategy_game.casework.intake``) is built on exactly this: a patient whose
consent form was altered after she signed it.

What it is not
--------------

Not a new rule, and not a second resolution mechanic. It changes **character state** and
records what it did; every uncertain action inside a procedure is still decided by the existing
Fate resolver (:mod:`strategy_game.rpg.fate`). It does not decide whether a patient *was*
treated, and it does not decide what a treatment *means* — the ontology is the fiction's, not the
module's.

The three layers of change map onto the live character sheet without inventing fields:

* a **revealed** aspect is a piece of the patient that came to light — it is recorded on the
  session, not on the sheet, because knowing something about someone is not the same as being
  changed by it;
* an **integrated** aspect is a change to who they are, and it goes on the sheet;
* a **condition** is a status, and a **healed consequence** is removed from the sheet.

The rule that a treatment needs consent is a statement about the *fiction*, not a medical claim.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .fate import Character

__all__ = [
    "PsychosurgeryError",
    "PsychosurgerySession",
]


class PsychosurgeryError(PermissionError):
    """A procedure tried to change the patient without the patient's consent."""


@dataclass
class PsychosurgerySession:
    """One procedure, and everything it did.

    ``patient`` is the live character sheet and is **mutated in place** by the write methods, so
    a session is a record of a change to a person rather than a copy of one.
    """

    patient: Character
    #: Who performed the procedure. A name, not a role — the fiction needs to know who to ask.
    operator: str
    #: The patient's consent. Every write checks it, every time.
    consent: bool
    #: Aspects that came to light during the procedure. Read, not written.
    revealed_aspects: set[str] = field(default_factory=set)
    #: A plain, ordered record of what was done. Nothing is written that is not logged.
    log: list[str] = field(default_factory=list)

    def reveal_aspect(self, aspect: str) -> None:
        """Bring something about the patient to light.

        This is a **read**. It does not change who the patient is, and it is permitted without
        consent — a clinician may notice something, and noticing is not a violation.
        """
        self.revealed_aspects.add(aspect)
        self.log.append(f"revealed:{aspect}")

    def integrate_aspect(self, aspect: str) -> None:
        """Change who the patient is.

        This is a **write**, and it requires consent.
        """
        if not self.consent:
            raise PsychosurgeryError("changing the patient requires the patient's consent")
        self.patient.aspects.append(aspect)
        self.log.append(f"integrated:{aspect}")

    def add_condition(self, condition: str) -> None:
        """Record a clinical condition.

        A condition is a **read** of the patient's state: it is what is now the case about
        them, not a change they undergo. The corpus's own reading is that a condition may be
        recorded without the patient's agreement, and that this asymmetry is the point — it is
        how a procedure becomes a record of what was done *to* someone.
        """
        self.patient.statuses.append(condition)
        self.log.append(f"condition:{condition}")

    def heal_consequence(self, consequence: str) -> bool:
        """Treat an existing consequence.

        A **write**, and it requires consent. Returns whether there was such a consequence to
        treat.
        """
        if not self.consent:
            raise PsychosurgeryError("treating a consequence requires the patient's consent")
        if consequence not in self.patient.consequences:
            return False
        self.patient.consequences.remove(consequence)
        self.log.append(f"healed:{consequence}")
        return True

    def resonate(self, other: str, strength: int = 1) -> None:
        """Contact another psyche from inside the procedure.

        A **write**, and it requires consent: the other party is changed by it, and the patient
        is the one whose body is being used to do it. Neither party can afterwards prove whether
        a memory was carried across or was made between them, and the module does not try.
        """
        if not self.consent:
            raise PsychosurgeryError("resonance requires the patient's consent")
        self.log.append(f"resonance:{other}:{strength}")

    def inspect_state(self) -> dict[str, object]:
        """The session, as plain data: what was revealed, what was written, and in what order."""
        return {
            "patient": self.patient.id,
            "operator": self.operator,
            "consent": self.consent,
            "revealed_aspects": sorted(self.revealed_aspects),
            "aspects": list(self.patient.aspects),
            "statuses": list(self.patient.statuses),
            "consequences": list(self.patient.consequences),
            "log": list(self.log),
        }
