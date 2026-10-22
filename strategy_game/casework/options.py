"""Tuning **options** for a case: the alternatives the machinery can express, built on demand.

Nothing in this module is a rule and nothing in it is a choice. The playtest evidence in
``strategy_game/docs/PLAYTEST_SECOND_SHADOW.md`` found four places where the shipped case exercises
only one of the readings the ruleset (or the case document) already allows:

* whether a **failure withholds** the fragment an action would have yielded (``TUNING_CHAIN_WITHHOLD``);
* which skill a **force** exchange attacks with — the resolution's own (the code's behaviour) or the
  ``REF`` the case document describes (``TUNING_OPPOSED_ATTACK_SKILL``);
* whether a **tie** on a confrontation is total failure or lets the attempt stand
  (``TUNING_CONFRONTATION_TIE``);
* how much of the **aspect economy** the party actually spends (a party decision, not a case one).

Each of the first three is Tomi's to decide — they are rows on ``docs/design/AUTHOR_DECISION_QUEUE.md``
and findings F2/F3/F4 in the playtest record. So this module builds the *variants*, the harness
measures what each one costs, and the document reports the difference. The shipped case keeps the
settings it had; nobody here answers anything.

    from strategy_game.casework import kallio, options
    variant = options.variant(kallio.CASE, force_attack_skill="REF")
    session = kallio.build_session(seed=1, spec=variant)
"""
from __future__ import annotations

from dataclasses import replace
from typing import Any

from .spec import CaseFile

__all__ = ["OPTION_NAMES", "variant", "with_chain_withholding", "with_force_attack_skill", "with_tie_policy"]

#: The options this module can vary, so a call site can name one rather than build a payload.
OPTION_NAMES: tuple[str, ...] = (
    "chain_withholding",
    "force_attack_skill",
    "tie_is_not_total_failure",
)


def variant(
    case: CaseFile,
    *,
    withhold_on_failure: bool | None = None,
    force_attack_skill: str | None = None,
    tie_is_not_total_failure: bool | None = None,
) -> CaseFile:
    """Return a copy of ``case`` with the named options set, and nothing else changed.

    ``None`` means "leave this option exactly as the case declares it", so a caller can vary one
    thing at a time. The copy is a case *declaration*, so the campaign it is played on is unchanged:
    the case id, the scenes and the endings are the same content, which is what makes the difference
    between two variants a measurement of the option rather than of a different scenario.
    """
    scenes = case.scenes
    if withhold_on_failure is not None:
        scenes = tuple(
            replace(
                scene,
                actions=tuple(
                    replace(action, withhold_on_failure=withhold_on_failure)
                    for action in scene.actions
                ),
            )
            for scene in scenes
        )
    resolutions = case.resolutions
    if force_attack_skill is not None or tie_is_not_total_failure is not None:
        # The options only mean anything on an opposed resolution; a passive ending keeps exactly
        # what it declared, so a variant never trips the structural check for a dead option.
        resolutions = tuple(
            (
                replace(
                    resolution,
                    force_attack_skill=(
                        resolution.force_attack_skill
                        if force_attack_skill is None
                        else force_attack_skill
                    ),
                    tie_is_not_total_failure=(
                        resolution.tie_is_not_total_failure
                        if tie_is_not_total_failure is None
                        else tie_is_not_total_failure
                    ),
                )
                if resolution.opposed_by
                else resolution
            )
            for resolution in resolutions
        )
    return replace(case, scenes=scenes, resolutions=resolutions)


def with_chain_withholding(case: CaseFile, *, enabled: bool) -> CaseFile:
    """Every action either withholds its fragment on a failure, or never does."""
    return variant(case, withhold_on_failure=enabled)


def with_force_attack_skill(case: CaseFile, skill: str) -> CaseFile:
    """The skill a *force* exchange attacks with. ``""`` restores the resolution's own skill."""
    return variant(case, force_attack_skill=skill)


def with_tie_policy(case: CaseFile, *, not_total_failure: bool) -> CaseFile:
    """Whether a tie on a confrontation ends the attempt (``False``) or stands (``True``)."""
    return variant(case, tie_is_not_total_failure=not_total_failure)


def describe(case: CaseFile) -> dict[str, Any]:
    """The options a case currently declares, for a record's own ``method`` block."""
    return {
        "chain_withholding": sorted(
            f"{scene.id}/{action.id}"
            for scene in case.scenes
            for action in scene.actions
            if action.withhold_on_failure
        ),
        "scene_aspects": {scene.id: list(scene.aspects) for scene in case.scenes},
        "force_attack_skill": {
            resolution.id: resolution.force_attack_skill
            for resolution in case.resolutions
            if resolution.opposed_by
        },
        "tie_is_not_total_failure": {
            resolution.id: resolution.tie_is_not_total_failure
            for resolution in case.resolutions
            if resolution.opposed_by
        },
    }
