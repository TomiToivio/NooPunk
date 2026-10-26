"""Psionics: the Effort-shaped psychic subsystem (SWN *shape*, NoöPunk content).

**Status: PROVISIONAL.** The pool shape and the discipline list are adopted by author ruling in
``rulebook/WITHOUT_NUMBER_BASELINE.md`` §2 and §6; the technique catalogue in
``data/rules/psionics_techniques.json`` is original NoöPunk content and every number in it belongs
to the author. Nothing here is canonical until an author ruling says so.

What is adopted, and from where:

* **Effort** — one small pool, a lasting effect keeps a point committed, a good night's rest
  returns everything. This pattern is from the *Worlds Without Number* SRD, which is CC0.
* **Core capability before techniques** — level 0 in a discipline grants its core technique and
  the core improves with the skill level; each further level buys one technique. This is the shape
  of *Stars Without Number Revised* psionics. **SWN has no verified SRD licence**
  (``docs/licenses/ISSUE_569_WITHOUT_NUMBER_RIGHTS.md``), so nothing of its text, power names or
  tables is reproduced: the mechanics are re-expressed and the catalogue is authored here.
* **PSI is natural and learnable, never viral, never a class.** NoöPunk canon
  (``rulebook/6_PSYCHIC.md`` §6.1). A character is limited by what they were taught, which is why
  the gate below is a *permission* failure rather than a difficulty penalty.

Resolution stays on the one kernel: an attempted technique that calls for a check is a normal
``2d6 + attribute modifier + skill level`` skill check from :mod:`rules.wn_core`.

Usage::

    psi = Practitioner(attributes={"WIS": 14, "CON": 10, ...}, skills={"Telepathy": 1})
    use = psi.use("surface_read")          # core technique, no Effort
    psi.use("thread")                     # commits one Effort for the scene
"""
from __future__ import annotations

import json
import pathlib
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from . import wn_core

#: The six psionic disciplines, as adopted in the Without Number baseline (§2). They are specialist
#: skills, not a class feature, and they are not available through an ordinary free skill pick.
PSI_DISCIPLINES: tuple[str, ...] = (
    "Biopsionics",
    "Metapsionics",
    "Precognition",
    "Telekinesis",
    "Telepathy",
    "Teleportation",
)

#: Commitment durations. ``instant`` costs nothing to hold; ``scene`` and ``day`` tie Effort up.
EFFORT_DURATIONS: tuple[str, ...] = ("instant", "scene", "day")

#: Torching (pushing past the pool) is dangerous in a way the character cannot train away.
TORCH_RESULTS: dict[int, str] = {
    1: "lose_1_wisdom",
    2: "lose_1_wisdom",
    3: "lose_1_constitution",
    4: "lose_1_constitution",
    5: "lose_1_chosen_attribute",
    6: "no_harm",
}

#: Below this Wisdom score a psychic becomes feral: no longer a player character, and uncurable.
FERAL_WISDOM = 3

CATALOGUE_PATH = pathlib.Path(__file__).resolve().parents[2] / "data" / "rules" / "psionics_techniques.json"


class PsiError(ValueError):
    """A constraint of the psionic subsystem was about to be violated."""


@dataclass(frozen=True)
class Technique:
    """One technique: either a discipline's core or a learned pick."""

    id: str
    name: str
    discipline: str
    min_skill: int
    effort: str            # "none", "commit_scene" or "commit_day"
    duration: str
    effect: str
    check: Mapping[str, Any] | None = None
    consent_required: bool = False
    core: bool = False

    @property
    def commitment(self) -> str | None:
        """``scene`` or ``day`` when using this technique holds Effort, else ``None``."""
        if self.effort == "commit_scene":
            return "scene"
        if self.effort == "commit_day":
            return "day"
        return None


@dataclass(frozen=True)
class Catalogue:
    """The authored technique catalogue, loaded from data."""

    version: str
    disciplines: tuple[str, ...]
    cores: Mapping[str, Technique]
    techniques: Mapping[str, Technique]

    def get(self, technique_id: str) -> Technique:
        if technique_id in self.techniques:
            return self.techniques[technique_id]
        for core in self.cores.values():
            if core.id == technique_id:
                return core
        raise PsiError(f"unknown technique {technique_id!r}")

    def for_discipline(self, discipline: str) -> list[Technique]:
        return [t for t in self.techniques.values() if t.discipline == discipline]


def load_catalogue(path: pathlib.Path | str | None = None) -> Catalogue:
    """Load and validate the authored catalogue.

    Validation is deliberately strict: a technique that names an unknown discipline, a minimum
    skill outside 0..4, or an Effort cost that is not one of the recorded durations is a data bug,
    not a referee's call.
    """
    raw = json.loads(pathlib.Path(path or CATALOGUE_PATH).read_text(encoding="utf-8"))
    disciplines = tuple(raw.get("disciplines") or PSI_DISCIPLINES)
    for discipline in disciplines:
        if discipline not in PSI_DISCIPLINES:
            raise PsiError(f"unknown psionic discipline {discipline!r}")

    cores: dict[str, Technique] = {}
    for discipline, entry in (raw.get("discipline_cores") or {}).items():
        if discipline not in disciplines:
            raise PsiError(f"core technique names unknown discipline {discipline!r}")
        cores[discipline] = Technique(
            id=str(entry["id"]),
            name=str(entry["name"]),
            discipline=discipline,
            min_skill=int(entry.get("min_skill", 0)),
            effort=str(entry.get("effort", "none")),
            duration=str(entry.get("duration", "instant")),
            effect=str(entry.get("effect", "")),
            check=entry.get("check"),
            consent_required=bool(entry.get("consent_required", False)),
            core=True,
        )

    techniques: dict[str, Technique] = {}
    for entry in raw.get("techniques", []):
        technique = Technique(
            id=str(entry["id"]),
            name=str(entry["name"]),
            discipline=str(entry["discipline"]),
            min_skill=int(entry.get("min_skill", 0)),
            effort=str(entry.get("effort", "none")),
            duration=str(entry.get("duration", "instant")),
            effect=str(entry.get("effect", "")),
            check=entry.get("check"),
            consent_required=bool(entry.get("consent_required", False)),
        )
        if technique.discipline not in disciplines:
            raise PsiError(f"{technique.id} names unknown discipline {technique.discipline!r}")
        if technique.id in techniques:
            raise PsiError(f"duplicate technique id {technique.id!r}")
        techniques[technique.id] = technique

    for technique in list(cores.values()) + list(techniques.values()):
        if not 0 <= technique.min_skill <= wn_core.MAX_SKILL_LEVEL:
            raise PsiError(f"{technique.id}: min_skill must be 0..4, got {technique.min_skill}")
        if technique.effort not in ("none", "commit_scene", "commit_day"):
            raise PsiError(f"{technique.id}: unknown effort cost {technique.effort!r}")
        if technique.duration not in EFFORT_DURATIONS:
            raise PsiError(f"{technique.id}: unknown duration {technique.duration!r}")
        if not technique.effect.strip():
            raise PsiError(f"{technique.id}: a technique without effect text is not playable")
    return Catalogue(
        version=str(raw.get("version", "")),
        disciplines=disciplines,
        cores=cores,
        techniques=techniques,
    )


def max_effort(attributes: Mapping[str, int], skills: Mapping[str, int]) -> int:
    """``1 + max(WIS modifier, CON modifier) + the highest psionic skill level``.

    A character with no psionic skill has no pool beyond their attributes: the skill term is 0, not
    the untrained ``-1``, because the penalty describes attempted use, not capacity.
    """
    wisdom = wn_core.attribute_modifier(int(attributes["WIS"]))
    constitution = wn_core.attribute_modifier(int(attributes["CON"]))
    trained = [int(skills[d]) for d in PSI_DISCIPLINES if skills.get(d) is not None]
    best_skill = max(trained) if trained else 0
    best_skill = max(best_skill, 0)
    return 1 + max(wisdom, constitution) + best_skill


class Duration(str, Enum):
    """How long a commitment holds. Adopted from #648's model, which this module supersedes.

    ``ACTIVE`` belongs to an effect that ends when the technique ends, so it may be released
    immediately. ``SCENE`` and ``DAY`` may not be refunded early — that is the whole point of a
    commitment: an ongoing burden is unavailable until its duration is over.
    """

    ACTIVE = "active"
    SCENE = "scene"
    DAY = "day"


@dataclass
class EffortPool:
    """Effort: named commitments held for an active effect, a scene, or a day.

    Named keys (rather than bare counters) are what makes a held power releasable: a caller commits
    ``"thread"`` and later releases ``"thread"``. Torched Effort is extra capacity for the rest of the
    scene and is not part of the maximum.
    """

    maximum: int
    reservations: dict[str, tuple[int, Duration]] = field(default_factory=dict)
    torched: int = 0

    def __post_init__(self) -> None:
        if self.maximum < 0:
            raise PsiError(f"maximum Effort cannot be negative, got {self.maximum}")
        if self.torched < 0:
            raise PsiError("torched Effort cannot be negative")
        for key, (amount, duration) in self.reservations.items():
            if not key:
                raise PsiError("a commitment needs a non-empty key")
            if not isinstance(amount, int) or amount < 1:
                raise PsiError(f"{key}: a commitment is at least one point, got {amount!r}")
            if not isinstance(duration, Duration):
                raise PsiError(f"{key}: an unknown duration {duration!r}")

    @property
    def committed(self) -> int:
        return sum(amount for amount, _ in self.reservations.values())

    @property
    def committed_scene(self) -> int:
        """Everything that ends when the scene does: active and scene commitments."""
        return sum(amount for amount, duration in self.reservations.values()
                   if duration is not Duration.DAY)

    @property
    def committed_day(self) -> int:
        return sum(amount for amount, duration in self.reservations.values()
                   if duration is Duration.DAY)

    @property
    def available(self) -> int:
        return max(0, self.maximum - self.committed) + self.torched

    def can_commit(self, amount: int = 1) -> bool:
        return amount >= 1 and self.available >= amount

    def commit(self, key: str, duration: Duration | str = Duration.SCENE, amount: int = 1) -> None:
        """Commit Effort under a unique name. A power commits exactly one point per use."""
        if not key:
            raise PsiError("a commitment needs a non-empty key")
        if key in self.reservations:
            raise PsiError(f"'{key}' is already committed")
        try:
            resolved = duration if isinstance(duration, Duration) else Duration(str(duration))
        except ValueError as error:
            raise PsiError(f"a commitment is active, scene or day, got {duration!r}") from error
        if amount < 1:
            raise PsiError(f"a commitment is at least one point, got {amount}")
        if not self.can_commit(amount):
            raise PsiError(f"not enough Effort: {self.available} available, {amount} required")
        # Torched Effort is spent first: it is the loosest, shortest-lived point in the pool.
        self.torched -= min(self.torched, amount)
        self.reservations[key] = (amount, resolved)

    def release(self, key: str) -> bool:
        """Release a commitment. Only an ``ACTIVE`` one may end early."""
        if key not in self.reservations:
            return False
        if self.reservations[key][1] is not Duration.ACTIVE:
            raise PsiError(f"'{key}' is committed for the {self.reservations[key][1].value}; it cannot be released early")
        del self.reservations[key]
        return True

    def end_scene(self) -> None:
        """A scene ends: active and scene commitments return; torched Effort is gone."""
        for key in [k for k, (_, duration) in self.reservations.items() if duration is not Duration.DAY]:
            del self.reservations[key]
        self.torched = 0

    def rest(self) -> None:
        """A good night's rest returns everything."""
        self.reservations.clear()
        self.torched = 0

    #: Kept as the name the Godot runtime and GameState already call.
    def night_rest(self) -> None:
        self.rest()

    def snapshot(self) -> dict[str, Any]:
        return {
            "maximum": self.maximum,
            "torched": self.torched,
            "reservations": {
                key: {"amount": amount, "duration": duration.value}
                for key, (amount, duration) in self.reservations.items()
            },
        }

    @classmethod
    def from_snapshot(cls, data: Mapping[str, Any]) -> EffortPool:
        """Rebuild a pool from a save. A malformed record is an error, never a silent reset."""
        try:
            maximum = int(data["maximum"])
            torched = int(data.get("torched", 0))
            reservations: dict[str, tuple[int, Duration]] = {}
            raw = data.get("reservations", {})
            if not isinstance(raw, Mapping):
                raise PsiError("reservations must be a mapping")
            for key, entry in raw.items():
                amount = int(entry["amount"])
                duration = Duration(str(entry["duration"]))
                reservations[str(key)] = (amount, duration)
        except (KeyError, TypeError, ValueError) as error:
            raise PsiError(f"malformed Effort snapshot: {error}") from error
        pool = cls(maximum=maximum, reservations=reservations, torched=torched)
        if pool.committed > pool.maximum + pool.torched:
            raise PsiError("a saved pool cannot commit more Effort than it can hold")
        return pool


@dataclass(frozen=True)
class TorchResult:
    """The price of pushing past the pool."""

    roll: int
    harm: str
    attribute_lost: str | None
    feral: bool

    @property
    def harmless(self) -> bool:
        return self.harm == "no_harm"


@dataclass
class Practitioner:
    """A character's psionic state: which disciplines they were trained in, and their pool."""

    attributes: Mapping[str, int]
    skills: Mapping[str, int] = field(default_factory=dict)
    known: set[str] = field(default_factory=set)
    #: Built from the attributes and disciplines in ``__post_init__``; never caller-supplied, so a
    #: character can never start with a pool that disagrees with their sheet.
    pool: EffortPool = field(init=False)

    def __post_init__(self) -> None:
        for attribute in ("WIS", "CON"):
            score = int(self.attributes[attribute])
            if not wn_core.ATTRIBUTE_MIN <= score <= wn_core.ATTRIBUTE_MAX:
                raise PsiError(f"{attribute} must be {wn_core.ATTRIBUTE_MIN}..{wn_core.ATTRIBUTE_MAX}, got {score}")
        unknown = set(self.skills) - set(PSI_DISCIPLINES)
        if unknown:
            raise PsiError(f"unknown psionic discipline(s): {sorted(unknown)}")
        for discipline in PSI_DISCIPLINES:
            level = self.skills.get(discipline)
            if level is not None and not wn_core.UNTRAINED <= int(level) <= wn_core.MAX_SKILL_LEVEL:
                raise PsiError(f"{discipline} must be -1..4, got {level}")
        self.pool = EffortPool(maximum=max_effort(self.attributes, self.skills))

    def discipline_level(self, discipline: str) -> int:
        """The trained level, or ``UNTRAINED`` for a discipline the character never studied."""
        if discipline not in PSI_DISCIPLINES:
            raise PsiError(f"unknown psionic discipline {discipline!r}")
        return int(self.skills.get(discipline, wn_core.UNTRAINED))

    def may_use(self, technique: Technique) -> bool:
        """The permission gate. Not a difficulty: an untrained character simply cannot do it."""
        return self.discipline_level(technique.discipline) >= max(0, technique.min_skill)

    def learn(self, technique: Technique) -> None:
        """Learn a technique, enforcing the source's minimum skill level."""
        if technique.core:
            raise PsiError(f"{technique.id} is a core technique and is never 'learned'")
        if self.discipline_level(technique.discipline) < technique.min_skill:
            raise PsiError(
                f"{technique.id} needs {technique.discipline}-{technique.min_skill}, "
                f"character has {self.discipline_level(technique.discipline)}"
            )
        self.known.add(technique.id)

    def use(self, technique_id: str, *, catalogue: Catalogue | None = None) -> Technique:
        """Spend what the technique costs, or refuse for the reason the source gives."""
        book = catalogue or load_catalogue()
        technique = book.get(technique_id)
        if not self.may_use(technique):
            raise PsiError(
                f"{technique.name} requires {technique.discipline}-{technique.min_skill}; "
                "the character was never trained in it"
            )
        commitment = technique.commitment
        if commitment is not None:
            self.pool.commit(self._reservation_key(technique.id), Duration(commitment))
        return technique

    def _reservation_key(self, base: str) -> str:
        """A unique commitment name, so the same technique can be held twice."""
        if base not in self.pool.reservations:
            return base
        index = 2
        while f"{base}#{index}" in self.pool.reservations:
            index += 1
        return f"{base}#{index}"

    def torch(self, *, rng: Any = None, die: int | None = None) -> TorchResult:
        """Gain one Effort for the rest of the scene, and pay for it on the d6 table."""
        rolled = int(die) if die is not None else (rng or random.Random()).randint(1, 6)
        if not 1 <= rolled <= 6:
            raise PsiError(f"a torching roll is 1..6, got {rolled}")
        harm = TORCH_RESULTS[rolled]
        lost: str | None = None
        if harm == "lose_1_wisdom":
            lost = "WIS"
        elif harm == "lose_1_constitution":
            lost = "CON"
        elif harm == "lose_1_chosen_attribute":
            lost = "any"
        if lost is not None:
            self.attributes = dict(self.attributes)
            if lost in ("WIS", "CON"):
                self.attributes[lost] = int(self.attributes[lost]) - 1
        feral = int(self.attributes["WIS"]) < FERAL_WISDOM
        self.pool.torched += 1
        return TorchResult(roll=rolled, harm=harm, attribute_lost=lost, feral=feral)

    def check(self, technique: Technique, *, rng: Any = None, dice: Sequence[int] | None = None) -> wn_core.Check:
        """Roll the skill check a technique calls for, on the one kernel."""
        spec = technique.check
        if not spec:
            raise PsiError(f"{technique.name} calls for no check")
        return wn_core.skill_check(
            attribute_score=int(self.attributes[str(spec["attribute"])]),
            skill_level=self.discipline_level(technique.discipline),
            difficulty=int(spec["difficulty"]),
            rng=rng,
            dice=dice,
        )
