"""The crossover sheet's two skill layers, and the context that selects between them (#482).

NoöPunk's crossover has **one character and one Fate kernel**, but a character acts at two scales:

* **as an individual** -- personal encounters, exploration, interrogation, fighting, investigation,
  and other scene-level actions. These checks read one of the **six individual skills** below.
* **as a faction agent** -- an organisational, political, diplomatic, covert, scientific or military
  mission declared on the strategy board. These checks read a **strategic agent skill**.

The two are *different lists on the same sheet*, and the layer a check belongs to is an explicit
:class:`ActionContext` -- **never inferred from the skill's name**. That is the whole point of this
module: a name that belongs to one layer cannot be checked against the other, and an unknown name is
refused rather than silently rated at zero.

Individual skills (author decision, #482)
-----------------------------------------

The six Eclipse Phase 2e *aptitudes* -- Cognition, Intuition, Reflexes, Savvy, Somatics, Willpower --
are used here as **Fate-rated skills**, not percentile attributes and not a second stat layer. They
are the individual half of the sheet; the value scale, allocation and advancement stay the approved
Fate baseline (see ``rpg/RULEBOOK.md``), and nothing in this module changes a rating.

Specialists do not add a seventh attribute. A narrow technical speciality is a **stunt** (a named
exception the GM approves) or a typed ``competence`` **TAG**, both of which already exist on the
sheet; :func:`specialist_supplement` records that rule in one place so no module has to invent a
skill to express it.

Strategic agent skills (proposal, #482)
---------------------------------------

The strategic roster is **not approved**. It is a parameter, not a constant: callers pass a roster of
allowed strategic skill ids (the proposed one lives in ``strategy_game/data/strategic_skills.json``,
read by :mod:`strategy_game.strategic_skills`). With no roster supplied, every faction-agent check is
refused with a message that says the roster is pending -- because guessing one would be inventing a
rule the author has not made.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from random import Random
from typing import Mapping

from .fate import Action, Character, Resolution, resolve

__all__ = [
    "ACTION_CONTEXTS",
    "ActionContext",
    "INDIVIDUAL_SKILLS",
    "INDIVIDUAL_SKILL_NAMES",
    "IndividualSkill",
    "SkillLayerError",
    "check",
    "individual_skill",
    "skill_names",
    "specialist_supplement",
    "validate_skill",
]


class ActionContext(str, Enum):
    """The scale a character is acting at. This is what selects the skill list."""

    INDIVIDUAL = "individual"
    FACTION_AGENT = "faction_agent"


ACTION_CONTEXTS: tuple[ActionContext, ...] = (ActionContext.INDIVIDUAL, ActionContext.FACTION_AGENT)


@dataclass(frozen=True)
class IndividualSkill:
    """One of the six individual skills: a Fate-rated skill with a stated scope.

    ``abbrev`` is the table abbreviation the author set (COG, INT, ...). ``meaning`` is the author's
    scope text, quoted from issue #482 and not paraphrased, because the boundary between, say,
    ``INT`` and ``COG`` is a design decision rather than a dictionary entry.
    """

    abbrev: str
    name: str
    meaning: str
    #: What a Fate Core reader knows this as. Documentation only: it maps no mechanic.
    fate_core_equivalent: str

    @property
    def key(self) -> str:
        """The skill's key on the sheet. The abbreviation is what cards and logs use."""
        return self.abbrev


INDIVIDUAL_SKILLS: tuple[IndividualSkill, ...] = (
    IndividualSkill(
        "COG", "Cognition", "Intelligence, solving problems, logical analysis", "Lore / Investigate"
    ),
    IndividualSkill(
        "INT", "Intuition",
        "Gut instinct, rapid evaluation, awareness, creativity, cleverness, cunning",
        "Notice / Empathy",
    ),
    IndividualSkill(
        "REF", "Reflexes", "Coordination, dexterity, nimbleness, balance, reaction speed",
        "Athletics / Physique",
    ),
    IndividualSkill(
        "SAV", "Savvy", "Social awareness, adaptability, empathy, influence",
        "Rapport / Provoke / Deceive",
    ),
    IndividualSkill(
        "SOM", "Somatics",
        "Exploiting bodily physical capabilities: strength, stamina, movement, sustained positioning",
        "Physique / Athletics",
    ),
    IndividualSkill(
        "WIL", "Willpower", "Self-control, mental fortitude, strength of personality",
        "Will / Empathy",
    ),
)

INDIVIDUAL_SKILL_NAMES: tuple[str, ...] = tuple(skill.key for skill in INDIVIDUAL_SKILLS)


class SkillLayerError(ValueError):
    """A check named a skill the selected layer does not carry."""


def individual_skill(key: str) -> IndividualSkill:
    """Look up one of the six by abbreviation or by full name, case-insensitively."""
    wanted = key.strip().casefold()
    for skill in INDIVIDUAL_SKILLS:
        if wanted in (skill.key.casefold(), skill.name.casefold()):
            return skill
    raise SkillLayerError(
        f"{key!r} is not an individual skill; the six are {', '.join(INDIVIDUAL_SKILL_NAMES)}"
    )


def skill_names(
    context: ActionContext, *, strategic_roster: Mapping[str, object] | None = None
) -> tuple[str, ...]:
    """The skill names the selected layer carries.

    For an individual check that is always the six. For a faction-agent check it is the supplied
    proposal roster -- which may be empty, because no strategic roster is approved yet.
    """
    if context is ActionContext.INDIVIDUAL:
        return INDIVIDUAL_SKILL_NAMES
    return tuple(sorted(strategic_roster or ()))


def validate_skill(
    context: ActionContext,
    skill_name: str,
    *,
    strategic_roster: Mapping[str, object] | None = None,
) -> str:
    """Return the canonical skill name for this context, or refuse with a reason.

    The refusals are the contract:

    * an individual check naming a strategic skill -- *"that skill belongs to the faction-agent
      layer; individual actions read COG/INT/REF/SAV/SOM/WIL"* -- rather than quietly reading it
      at zero, which would look like an untrained character instead of a rules error;
    * a faction-agent check naming an individual skill -- the same refusal, reversed;
    * a faction-agent check with no roster supplied -- refused as *pending author approval*;
    * anything unknown to the selected layer.
    """
    name = str(skill_name).strip()
    if context is ActionContext.INDIVIDUAL:
        try:
            return individual_skill(name).key
        except SkillLayerError as exc:
            if strategic_roster and name in strategic_roster:
                raise SkillLayerError(
                    f"{name!r} is a faction-agent skill: it is checked when the character acts as an "
                    f"agent of their faction, not as an individual. Individual actions read "
                    f"{', '.join(INDIVIDUAL_SKILL_NAMES)}."
                ) from exc
            raise

    roster = strategic_roster or {}
    if name in roster:
        return name
    if name in INDIVIDUAL_SKILL_NAMES:
        raise SkillLayerError(
            f"{name!r} is an individual skill: it is checked when the character acts as a person in "
            "a scene, not as an agent of their faction. A faction-agent mission reads a strategic "
            "skill."
        )
    if not roster:
        raise SkillLayerError(
            f"the strategic agent skill roster is not approved, so {name!r} cannot be checked. "
            "Pass the proposal roster from strategy_game/data/strategic_skills.json, or resolve the "
            "declaration as an individual action instead. Nothing is substituted."
        )
    raise SkillLayerError(
        f"{name!r} is not a strategic agent skill; the proposed roster carries "
        f"{', '.join(sorted(roster))}"
    )


def check(
    actor: Character,
    context: ActionContext,
    action: Action,
    skill_name: str,
    difficulty: int,
    *,
    rng: Random,
    invoked_aspect: str | None = None,
    strategic_roster: Mapping[str, object] | None = None,
) -> Resolution:
    """Resolve one check in its declared context, on the one Fate kernel.

    The rating is read from the sheet the context names -- ``Character.skills`` for an individual
    action, ``Character.strategic_skills`` for a faction-agent mission -- after
    :func:`validate_skill` has accepted the name. An aspect invoke is the one Fate point spend this
    function performs, exactly as ``fate.skill_check`` does.
    """
    name = validate_skill(context, skill_name, strategic_roster=strategic_roster)
    rating = (
        actor.skills.get(name, 0)
        if context is ActionContext.INDIVIDUAL
        else actor.strategic_skills.get(name, 0)
    )
    bonus = actor.invoke(invoked_aspect) if invoked_aspect else 0
    return resolve(action, rating, difficulty, rng=rng, bonus=bonus)


def specialist_supplement(actor: Character, skill_name: str) -> tuple[str, ...]:
    """The sheet's narrow specialities that sit *under* one broad individual skill.

    Issue #482 asks that a specialist addition never become a silent seventh attribute. So a narrow
    speciality is expressed as a ``competence`` TAG or a stunt -- both already on the sheet -- and
    this function returns those that the caller has attached. It reads tags and stunts only: it
    grants no bonus, because a tag that moved a roll would be an unapproved mechanic.
    """
    skill = individual_skill(skill_name)
    wanted = {skill.key.casefold(), skill.name.casefold()}
    supplement: list[str] = []
    for tag in actor.tags_of_kind("competence"):
        if tag.value.split(":", 1)[0].strip().casefold() in wanted:
            supplement.append(tag.value)
    supplement.extend(stunt for stunt in actor.stunts if stunt.split(":", 1)[0].strip().casefold() in wanted)
    return tuple(supplement)
