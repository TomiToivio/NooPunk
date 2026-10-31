r"""Cities Without Number: the program catalogue — Verbs, Subjects and what a run costs.

Transcribed from the **Cities Without Number SRD** (CC0) at
<https://cwn.quadrifons.com/hacking/programs/program-verbs/> and
<https://cwn.quadrifons.com/hacking/programs/program-subjects/>.

Why this module exists at all: :mod:`rules.cwn_hacking` models the procedure *around* a hack — the
Access pool, the security ladder, the connection penalties, the alert clock — and says in its own
docstring that Verbs and Subjects are catalogue content it will not invent. That left the Godot
hacking screen with nothing to check legality against. This file is the catalogue, transcribed
rather than invented, so a program that cannot legally run cannot be run.

## The three constraints the table encodes

**A Verb targets a Subject *type*, not a thing.** ``Blind`` may target a Device or a Cyber; ``Terminate``
only a Program. The SRD is explicit: "A Verb cannot be run with an invalid target; you can't Blind a data
file or Delude an avatar." :func:`validate_program` refuses those combinations instead of trusting the
caller.

**Access is spent, and some Verbs give it back.** Most Verbs cost a point of Access; a few cost none.
The ones marked self-terminating (\*) hand their CPU slot back the moment they resolve, so a deck with
one free slot can chain them.

**``Defend`` involves no check.** Its Skill Check Mod is "N/A": it is running continuously against
intrusion, not an action that can fail a roll. Modelling it as ``+0`` would invent a check the book does
not ask for, so the modifier is ``None`` and :func:`requires_check` says so.
"""
from __future__ import annotations

from dataclasses import dataclass

from .cwn_hacking import HackError

SOURCE_URL = "https://cwn.quadrifons.com/hacking/programs/"

#: Subject *types* a Verb may be run against.
SUBJECT_TYPES = frozenset({"Device", "Cyber", "Data", "Avatar", "Program"})


@dataclass(frozen=True)
class Verb:
    """One row of the SRD Verb table."""

    name: str
    cost_usd: int
    target_types: frozenset[str]
    access_cost: int
    #: SRD "Skill Check Mod"; ``None`` where the table says "N/A" (no check is rolled).
    skill_modifier: int | None
    #: SRD "\\*": the program returns its CPU slot immediately after it is run.
    self_terminating: bool


@dataclass(frozen=True)
class Subject:
    """One row of the SRD Subject table."""

    name: str
    cost_usd: int
    subject_type: str


def _v(name: str, cost: int, targets: str, access: int, mod: int | None, self_term: bool) -> Verb:
    return Verb(
        name=name,
        cost_usd=cost,
        target_types=frozenset(targets.split("/")),
        access_cost=access,
        skill_modifier=mod,
        self_terminating=self_term,
    )


#: SRD Verb table, verbatim. ``*`` in the SRD is the ``self_terminating`` column.
VERBS: dict[str, Verb] = {
    v.name: v
    for v in (
        _v("Activate", 1000, "Device/Cyber", 1, 1, True),
        _v("Analyze", 500, "Device/Data", 0, 1, True),
        _v("Append", 500, "Data", 1, 0, True),
        _v("Blind", 2000, "Device/Cyber", 1, 0, False),
        _v("Deactivate", 2000, "Device/Cyber", 1, 1, True),
        _v("Decrypt", 1000, "Data", 1, 0, True),
        _v("Defend", 1000, "Device/Cyber", 0, None, False),
        _v("Delude", 5000, "Device", 1, -1, False),
        _v("Erase", 500, "Data", 1, 1, True),
        _v("Frisk", 500, "Cyber", 0, 1, True),
        _v("Ghost", 2000, "Avatar", 1, 0, False),
        _v("Glitch", 1000, "Device/Cyber", 0, 2, False),
        _v("Hijack", 5000, "Device", 1, -1, False),
        _v("Kill", 5000, "Avatar", 1, 0, True),
        _v("Lock", 1000, "Device/Data", 1, 1, False),
        _v("Paralyze", 2000, "Avatar", 1, -2, False),
        _v("Replace", 1000, "Data", 1, 0, True),
        _v("Sabotage", 2000, "Device/Cyber", 1, -1, True),
        _v("Sense", 1000, "Device/Data", 0, 0, False),
        _v("Siege", 2500, "Device", 1, -2, False),
        _v("Silence", 1000, "Avatar", 1, 1, False),
        _v("Stun", 1000, "Avatar", 0, 0, True),
        _v("Terminate", 500, "Program", 1, 0, True),
        _v("Unlock", 500, "Device/Data", 1, 1, True),
    )
}

#: SRD Subject table, verbatim. A Subject's *type* is what a Verb targets.
SUBJECTS: dict[str, Subject] = {
    s.name: s
    for s in (
        Subject("Avatar", 500, "Avatar"),
        Subject("Barrier", 1000, "Data"),
        Subject("Camera", 500, "Device"),
        Subject("Cyber", 1000, "Cyber"),
        Subject("Datafile", 500, "Data"),
        Subject("Door", 500, "Device"),
        Subject("Drone", 1000, "Device"),
        Subject("Machine", 500, "Device"),
        Subject("Program", 500, "Program"),
        Subject("Sensor", 500, "Device"),
        Subject("Transmission", 1000, "Data"),
        Subject("Turret", 1000, "Device"),
    )
}

#: SRD: a specialized Subject costs twice the base, a unique one four times.
SPECIALIZED_SUBJECT_MULTIPLIER = 2
UNIQUE_SUBJECT_MULTIPLIER = 4


@dataclass(frozen=True)
class ProgramRun:
    """What a legal program run costs, before any die is rolled."""

    verb: str
    subject: str
    access_spent: int
    skill_modifier: int | None
    self_terminating: bool
    cpu_held: int

    @property
    def requires_check(self) -> bool:
        return self.skill_modifier is not None


def validate_program(verb_name: str, subject_name: str) -> tuple[Verb, Subject]:
    """Return the pair, refusing an unknown name or an illegal Verb/Subject combination."""
    verb = VERBS.get(verb_name)
    if verb is None:
        raise HackError(f"unknown Verb: {verb_name!r}")
    subject = SUBJECTS.get(subject_name)
    if subject is None:
        raise HackError(f"unknown Subject: {subject_name!r}")
    if subject.subject_type not in verb.target_types:
        allowed = "/".join(sorted(verb.target_types))
        raise HackError(
            f"{verb.name} cannot target a {subject.name} ({subject.subject_type}); it targets {allowed}"
        )
    return verb, subject


def require_access(verb: Verb, *, access_available: int) -> None:
    """Refuse a run the deck cannot pay for. Access is a pool, never a bonus."""
    if access_available < verb.access_cost:
        raise HackError(
            f"{verb.name} costs {verb.access_cost} Access; {access_available} available"
        )


def run_program(
    verb_name: str,
    subject_name: str,
    *,
    access_available: int,
    cpu_free: int,
) -> ProgramRun:
    """Legality and cost of running one program.

    Raises :class:`HackError` for an illegal target, for insufficient Access, or for no free CPU slot.
    A self-terminating Verb still needs a free slot to run, but returns it immediately, so ``cpu_held``
    is 0 for those.
    """
    verb, subject = validate_program(verb_name, subject_name)
    require_access(verb, access_available=access_available)
    if cpu_free < 1:
        raise HackError(f"no free CPU slot to run {verb.name}")
    return ProgramRun(
        verb=verb.name,
        subject=subject.name,
        access_spent=verb.access_cost,
        skill_modifier=verb.skill_modifier,
        self_terminating=verb.self_terminating,
        cpu_held=0 if verb.self_terminating else 1,
    )


def subject_cost(name: str, *, specialized: bool = False, unique: bool = False) -> int:
    """Base cost from the table, doubled for a specialized Subject, quadrupled for a unique one."""
    subject = SUBJECTS.get(name)
    if subject is None:
        raise HackError(f"unknown Subject: {name!r}")
    if specialized and unique:
        raise HackError("a Subject cannot be both specialized and unique")
    multiplier = UNIQUE_SUBJECT_MULTIPLIER if unique else SPECIALIZED_SUBJECT_MULTIPLIER if specialized else 1
    return subject.cost_usd * multiplier


def program_cost(verb_name: str, subject_name: str) -> int:
    """Buying a Verb and a Subject costs their listed prices; one program is one Verb plus one Subject."""
    verb, subject = validate_program(verb_name, subject_name)
    return verb.cost_usd + subject.cost_usd
