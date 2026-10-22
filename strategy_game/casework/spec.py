"""Scenario data for the RPG-first vertical slice: scenes, checks, clues and resolutions (#502).

This module is the **declarative half** of the casework layer: a
:class:`CaseFile` says what a case contains — its scenes, the actions available in each, the
individual-skill check an action rolls, the clue it yields, the fragments that must be assembled
into a finding, and the resolutions that close it. :mod:`strategy_game.casework.session` is the
executable half and owns every transition.

What is deliberately *not* here
-------------------------------

**No rule.** A check names one of issue #482's six individual skills and one of Fate Core's own
adjective bands; the band mapping below is the Fate ladder the approved kernel already uses, not a
second scale. Difficulty is the GM's call in Fate (*"the GM supplies difficulty and permission"*),
so every band an author picks is scenario tuning, marked as such. There is no new dice convention,
no new skill, no new outcome rung and no combat subsystem: an action is an ordinary Fate overcome,
create-advantage or attack, and a hit is :func:`strategy_game.rpg.scene.apply_hit`.

**No canon.** A case file is authored scenario content. The one packaged case
(:mod:`strategy_game.casework.kallio`) uses the canonical frame — Helsinki Field Office, UNSA, the
2045 campaign present, the post-Crisis network and the Reptilian raids — and its people, its
incident and its outcome are **fiction, not canon**. Nothing here promotes a name, a date or an
event into the setting.

**No locked solution.** The case file has three resolutions and a deliberate partial path. Which
one is *right* is a fiction decision the player makes, and the case records it; it does not score it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..rpg.fate import Action
from ..rpg.skills import INDIVIDUAL_SKILL_NAMES, individual_skill

__all__ = [
    "CASE_FORMAT",
    "CASE_SCHEMA_VERSION",
    "DIFFICULTY_BANDS",
    "ActionSpec",
    "CaseFile",
    "CaseSpecError",
    "CheckSpec",
    "ClueSpec",
    "Cost",
    "CyberGate",
    "FindingSpec",
    "PsiGate",
    "ResolutionSpec",
    "SceneSpec",
    "band_difficulty",
]

#: The document's own name, so a payload cannot be mistaken for another layer's.
CASE_FORMAT = "noopunk.strategy_game.casework"

#: Bumped only on an incompatible change to the case declaration shape.
CASE_SCHEMA_VERSION = "case-file-1"

#: Fate Core's adjective ladder, as the approved kernel's own scale. A band is how an author states a
#: difficulty readably; the number is what the 4dF kernel takes. *TUNING:* which band an action uses
#: is a scenario author's call, exactly as passive difficulty is the GM's in Fate — not a project
#: rule, and not a balance decision this module makes.
DIFFICULTY_BANDS: dict[str, int] = {
    "Mediocre": 0,
    "Average": 1,
    "Fair": 2,
    "Good": 3,
    "Great": 4,
    "Superb": 5,
    "Fantastic": 6,
}


class CaseSpecError(ValueError):
    """A case declaration that cannot be played as written."""


def band_difficulty(band: str) -> int:
    """The number behind a Fate band name, refusing an off-ladder name rather than guessing."""
    key = str(band).strip().title()
    if key not in DIFFICULTY_BANDS:
        raise CaseSpecError(
            f"{band!r} is not a Fate difficulty band; the ladder here is "
            f"{', '.join(DIFFICULTY_BANDS)}"
        )
    return DIFFICULTY_BANDS[key]


@dataclass(frozen=True)
class Cost:
    """What a tie or a failure costs, in the vocabulary the engine already owns.

    ``complications`` are case-level flags (named, not numeric); ``stress`` marks stress boxes through
    :func:`strategy_game.rpg.scene.apply_hit`; ``consequence`` fills the mild (2) consequence slot with
    a **named injury**. Nothing here is a magnitude on a faction book — that write happens once, at
    :meth:`strategy_game.casework.session.CaseSession.resolve`, through
    :func:`strategy_game.campaign.missions.apply_mission_outcome`.
    """

    complications: tuple[str, ...] = ()
    stress: int = 0
    mental: bool = False
    consequence: str = ""

    def __post_init__(self) -> None:
        if self.stress < 0:
            raise CaseSpecError("a cost cannot remove stress")
        if self.consequence and self.stress > 2:
            raise CaseSpecError("a named consequence already absorbs the mild hit; keep stress <= 2")

    @property
    def empty(self) -> bool:
        return not (self.complications or self.stress or self.consequence)

    def to_dict(self) -> dict[str, Any]:
        return {
            "complications": list(self.complications),
            "stress": self.stress,
            "mental": self.mental,
            "consequence": self.consequence,
        }


#: A cost of nothing, for the paths that charge nothing.
NO_COST = Cost()


@dataclass(frozen=True)
class CheckSpec:
    """One scene action's Fate check: action, individual skill, band, and what a hit means.

    Scene actions are rolled against passive difficulty, which is what Fate leaves to the GM. An
    **active** contest (a confrontation) is not a scene action: it is the closing check of a
    resolution, and :class:`ResolutionSpec` carries its opposition.
    """

    action: Action
    skill: str
    band: str
    #: Which track a consequence lands on. Fate keeps physical and mental stress apart (#389).
    mental: bool = False
    #: The named mild consequence a *hit* writes (combat only).
    consequence: str = ""

    def __post_init__(self) -> None:
        skill = individual_skill(self.skill).key
        if skill not in INDIVIDUAL_SKILL_NAMES:  # pragma: no cover - individual_skill guarantees it
            raise CaseSpecError(f"{skill!r} is not an individual skill")
        band_difficulty(self.band)
        if self.action is Action.DEFEND:
            raise CaseSpecError(
                "a case action is something the party attempts; defense is rolled as the opposition "
                "of an attack, not chosen from the action list"
            )

    @property
    def difficulty(self) -> int:
        return band_difficulty(self.band)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action.value,
            "skill": individual_skill(self.skill).key,
            "band": self.band,
            "difficulty": self.difficulty,
            "mental": self.mental,
            "consequence": self.consequence,
        }


@dataclass(frozen=True)
class CyberGate:
    """The reachability question issue #344 puts **before** any skill roll.

    A cyber action names its target's connectivity class, the era and the access path, and the
    session asks :meth:`strategy_game.cyber.ConnectivityModel.resolve_access`. If the answer is *not
    possible*, the action is refused and **no dice are rolled and no action is spent** — which is the
    whole point of the model. The gate computes no difficulty and no detection chance.
    """

    target_class: str
    era: str
    path: str
    local_presence: bool = True
    authorised: bool = False
    #: The refused alternative the case wants to show the player, e.g. a remote route that cannot work.
    note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_class": self.target_class,
            "era": self.era,
            "path": self.path,
            "local_presence": self.local_presence,
            "authorised": self.authorised,
            "note": self.note,
        }


@dataclass(frozen=True)
class PsiGate:
    """A PSI action's capability gate, on the character who actually holds the capability.

    Issue #482 gates a special move by a ``competence`` tag, and :func:`rpg.skills.require_capability`
    refuses before any dice. In this case the psi-sensitive is the **witness**, not an agent: the
    party supervises her reading, so the gate is applied to her sheet by name. That keeps the case
    from asserting a PSI capability on a canonical party member — which would be a canon claim, not a
    scenario choice.
    """

    witness_id: str
    capability: str

    def to_dict(self) -> dict[str, Any]:
        return {"witness_id": self.witness_id, "capability": self.capability}


@dataclass(frozen=True)
class ActionSpec:
    """One thing the party can attempt in a scene.

    An action is available to **any** seat: ``suggested_actor`` is presentation only. Locking an
    action to one character would let one spent action block the case, and the rulebook's own
    investigation guidance says an essential clue must never depend on one successful check.
    """

    id: str
    label: str
    text: str
    check: CheckSpec | None = None
    #: Clue ids this action yields. A failure still yields them (Fate's "success at a serious cost").
    gives: tuple[str, ...] = ()
    #: Intel record ids this action yields; written into the faction's books at resolution.
    intel: tuple[str, ...] = ()
    #: A scene aspect the action creates on success, with one free invocation (two on style).
    aspect: str = ""
    #: What a tie costs (Fate: "succeed at a minor cost").
    on_tie: Cost = NO_COST
    #: What a failure costs. The clue is still granted; the cost is the failure's price.
    on_fail: Cost = NO_COST
    #: Clue or finding ids that must already be held.
    requires: tuple[str, ...] = ()
    #: A cyber reachability gate, answered before any dice.
    cyber: CyberGate | None = None
    #: A psi capability gate, answered before any dice.
    psi: PsiGate | None = None
    #: A finding the action assembles from held clues, with no dice. The deduction is the action.
    finding: str = ""
    #: **TUNING_CHAIN_WITHHOLD.** *Does a failure still hand over this action's fragment?*
    #: ``False`` (the repository's long-standing behaviour) means the clue is not hostage to the
    #: dice: a tie pays the minor price and a failure the serious one, and both grant it. ``True``
    #: means a **failure** withholds the fragment and charges the price — Fate's other reading of
    #: an overcome, *"you do not get it"* — which is what makes a chain able to end short. It stays
    #: fail-forward because the price still lands, because the case reaches every fragment by more
    #: than one action, and because a short chain still assembles a *partial* finding or closes on
    #: the weaker resolution; it never dead-ends. Which actions carry it is scenario tuning, not a
    #: rule: the resolver simply honours the flag the case declares.
    withhold_on_failure: bool = False
    #: Presentation: the character the scene reads as the natural actor for this action.
    suggested_actor: str = ""
    #: The scene this action moves the party to, if it ends the current one.
    next_scene: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.label.strip() or not self.text.strip():
            raise CaseSpecError("an action needs an id, a label and its scene text")
        if (
            self.check is None
            and not self.gives
            and not self.intel
            and not self.aspect
            and not self.finding
            and not self.next_scene
        ):
            raise CaseSpecError(
                f"action {self.id!r} changes nothing: it has no check, clue, intel, aspect, "
                "finding or scene to move to"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "text": self.text,
            "check": None if self.check is None else self.check.to_dict(),
            "gives": list(self.gives),
            "intel": list(self.intel),
            "aspect": self.aspect,
            "on_tie": self.on_tie.to_dict(),
            "on_fail": self.on_fail.to_dict(),
            "requires": list(self.requires),
            "cyber": None if self.cyber is None else self.cyber.to_dict(),
            "psi": None if self.psi is None else self.psi.to_dict(),
            "finding": self.finding,
            "withhold_on_failure": self.withhold_on_failure,
            "suggested_actor": self.suggested_actor,
            "next_scene": self.next_scene,
        }


@dataclass(frozen=True)
class SceneSpec:
    """One scene: a place, the prose that opens it, and what can be attempted there.

    ``aspects`` are the scene's **declared situation aspects** — the facts the fiction already
    establishes when the party walks in (*"The night report is already too clean"*). They are on the
    scene from its first moment, so any check in it may invoke one for +2 in the resolver's own
    currency: a free invocation if the scene has one to spare (it does not, by default), otherwise a
    Fate point from the character attempting the check. That is Fate's existing invoke rule, not a
    second one; what was missing was a case that *declares* anything to invoke. Aspects a party
    creates with a create-advantage action are added to the same register by the session.
    """

    id: str
    title: str
    location: str
    prose: str
    actions: tuple[ActionSpec, ...]
    #: Declared situation aspects, present from the scene's start with no free invocation.
    aspects: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.actions:
            raise CaseSpecError(f"scene {self.id!r} has no actions")
        ids = [action.id for action in self.actions]
        if len(set(ids)) != len(ids):
            raise CaseSpecError(f"scene {self.id!r} repeats an action id")
        names = [name.strip() for name in self.aspects]
        if any(not name for name in names):
            raise CaseSpecError(f"scene {self.id!r} declares an empty aspect name")
        if len(set(names)) != len(names):
            raise CaseSpecError(f"scene {self.id!r} declares the same aspect twice")
        created = [action.aspect for action in self.actions if action.aspect]
        clash = sorted(set(names) & set(created))
        if clash:
            raise CaseSpecError(
                f"scene {self.id!r} declares {clash} both as a situation aspect and as an aspect an "
                "action creates; the scene's aspect register would hold one entry for two things"
            )

    def action(self, action_id: str) -> ActionSpec:
        for action in self.actions:
            if action.id == action_id:
                return action
        raise CaseSpecError(
            f"scene {self.id!r} has no action {action_id!r}; it offers {[a.id for a in self.actions]}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "location": self.location,
            "prose": self.prose,
            "aspects": list(self.aspects),
            "actions": [action.to_dict() for action in self.actions],
        }


@dataclass(frozen=True)
class ClueSpec:
    """One thing the party can come to know. A clue is evidence, not a conclusion."""

    id: str
    label: str
    text: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "text": self.text}


@dataclass(frozen=True)
class FindingSpec:
    """A conclusion the party must **assemble** from fragments.

    ``requires_all`` are the fragments the reasoning needs and ``requires_one_of`` the set from which
    one is enough (the same fact reached physically or psychically). ``partial_min`` is the smallest
    number of the union that still supports the finding at a price: the case then carries the
    ``unproven-chain`` complication and the resolution's record says the chain was incomplete. The
    deduction is never handed over by a single clue.
    """

    id: str
    label: str
    text: str
    requires_all: tuple[str, ...]
    requires_one_of: tuple[str, ...] = ()
    partial_min: int = 0
    partial_complication: str = "unproven-chain"

    def __post_init__(self) -> None:
        if not self.requires_all:
            raise CaseSpecError(f"finding {self.id!r} must require at least one fragment")
        if self.partial_min < 0:
            raise CaseSpecError("partial_min cannot be negative")

    @property
    def fragments(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys((*self.requires_all, *self.requires_one_of)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "text": self.text,
            "requires_all": list(self.requires_all),
            "requires_one_of": list(self.requires_one_of),
            "partial_min": self.partial_min,
            "partial_complication": self.partial_complication,
        }


@dataclass(frozen=True)
class ResolutionSpec:
    """One way the case can end. The closing check supplies the Fate outcome the record carries."""

    id: str
    label: str
    text: str
    #: The individual skill and band of the closing check.
    skill: str
    band: str
    #: A finding id the resolution needs, or empty when it needs none.
    requires_finding: str = ""
    #: A minimum number of assembled-chain fragments, for acting on partial proof.
    requires_fragments: int = 0
    #: Clues the resolution needs in hand (for a confrontation, the name of the person to confront).
    requires: tuple[str, ...] = ()
    #: Active opposition (a character id) for a confrontation; empty for passive difficulty.
    opposed_by: str = ""
    #: A named mild consequence a lost confrontation writes on the party member.
    consequence: str = ""
    mental: bool = False
    #: **TUNING_OPPOSED_ATTACK_SKILL.** Which skill a *force* exchange attacks with. Empty (the
    #: default, and the shipped case's setting) reads :attr:`skill` — the code's long-standing
    #: behaviour. Naming a skill here reads that one instead, which is what the case document's
    #: *"REF opposed attack"* wording describes. It is an option rather than a change because
    #: choosing between them is author row D-queue F2: the playtest measures both, and this module
    #: does not pick.
    force_attack_skill: str = ""
    #: **TUNING_CONFRONTATION_TIE.** ``False`` (the default, and the shipped case's setting) leaves a
    #: tie on a confrontation where the code has always put it: total failure and a fall back to the
    #: weaker resolution. ``True`` lets the requested resolution stand on a tie and records the tie
    #: as the closing outcome, which is the *shape* of "success at a cost" without inventing the
    #: cost — what a tie should cost is author row D32, so this option deliberately prices nothing.
    tie_is_not_total_failure: bool = False
    #: What the faction's books record when this resolution lands.
    objective: str = ""
    reputation: tuple[str, ...] = ()
    intel: tuple[str, ...] = ()
    resources: tuple[str, ...] = ()
    #: A reputation label used instead when the closing check fails (fail-forward, weaker record).
    on_fail_reputation: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.objective.strip():
            raise CaseSpecError("a resolution needs an id and the objective label it completes")
        individual_skill(self.skill)
        band_difficulty(self.band)
        if self.force_attack_skill:
            individual_skill(self.force_attack_skill)

    @property
    def difficulty(self) -> int:
        return band_difficulty(self.band)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "text": self.text,
            "skill": individual_skill(self.skill).key,
            "band": self.band,
            "difficulty": self.difficulty,
            "requires_finding": self.requires_finding,
            "requires_fragments": self.requires_fragments,
            "requires": list(self.requires),
            "opposed_by": self.opposed_by,
            "consequence": self.consequence,
            "mental": self.mental,
            "force_attack_skill": (
                "" if not self.force_attack_skill else individual_skill(self.force_attack_skill).key
            ),
            "tie_is_not_total_failure": self.tie_is_not_total_failure,
            "objective": self.objective,
            "reputation": list(self.reputation),
            "intel": list(self.intel),
            "resources": list(self.resources),
            "on_fail_reputation": list(self.on_fail_reputation),
        }


@dataclass(frozen=True)
class CaseFile:
    """A complete case: the scenes played, the clues found, the chain assembled, the endings."""

    id: str
    title: str
    core_question: str
    hook: str
    era: str
    era_label: str
    scenes: tuple[SceneSpec, ...]
    clues: tuple[ClueSpec, ...]
    findings: tuple[FindingSpec, ...]
    resolutions: tuple[ResolutionSpec, ...]
    #: The chain's fragment ids, in the order the reasoning uses them (for the reader's progress line).
    chain: tuple[str, ...]
    #: Free-text framing for the demo and the docs; nothing reads it as a rule.
    author_note: str = ""
    detail: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.id.strip() or not self.title.strip() or not self.core_question.strip():
            raise CaseSpecError("a case needs an id, a title and its core question")
        if not self.scenes:
            raise CaseSpecError("a case needs at least one scene")
        ids = [scene.id for scene in self.scenes]
        if len(set(ids)) != len(ids):
            raise CaseSpecError("two scenes share an id")
        clue_ids = [clue.id for clue in self.clues]
        if len(set(clue_ids)) != len(clue_ids):
            raise CaseSpecError("two clues share an id")
        finding_ids = [finding.id for finding in self.findings]
        if len(set(finding_ids)) != len(finding_ids):
            raise CaseSpecError("two findings share an id")
        resolution_ids = [resolution.id for resolution in self.resolutions]
        if len(set(resolution_ids)) != len(resolution_ids):
            raise CaseSpecError("two resolutions share an id")
        if len(self.resolutions) < 2:
            raise CaseSpecError("a case needs at least two ways to end")

    # -- lookups ---------------------------------------------------------------

    def scene(self, scene_id: str) -> SceneSpec:
        for scene in self.scenes:
            if scene.id == scene_id:
                return scene
        raise CaseSpecError(f"no scene {scene_id!r}; the case has {[s.id for s in self.scenes]}")

    def scene_index(self, scene_id: str) -> int:
        for index, scene in enumerate(self.scenes):
            if scene.id == scene_id:
                return index
        raise CaseSpecError(f"no scene {scene_id!r}")

    def clue(self, clue_id: str) -> ClueSpec:
        for clue in self.clues:
            if clue.id == clue_id:
                return clue
        raise CaseSpecError(f"no clue {clue_id!r}")

    def finding(self, finding_id: str) -> FindingSpec:
        for finding in self.findings:
            if finding.id == finding_id:
                return finding
        raise CaseSpecError(f"no finding {finding_id!r}")

    def resolution(self, resolution_id: str) -> ResolutionSpec:
        for resolution in self.resolutions:
            if resolution.id == resolution_id:
                return resolution
        raise CaseSpecError(f"no resolution {resolution_id!r}")

    def next_scene_after(self, scene_id: str) -> SceneSpec | None:
        index = self.scene_index(scene_id)
        if index + 1 < len(self.scenes):
            return self.scenes[index + 1]
        return None

    # -- validation ------------------------------------------------------------

    def structural_problems(self) -> tuple[str, ...]:
        """Everything that would make the case unplayable, reported in a stable order.

        This validates **the declaration**, not the balance: an unknown skill, a clue no action can
        give, a required fragment nothing yields, a scene nothing reaches, or a resolution whose
        requirement can never be met. It makes no statement about difficulty or fairness.
        """
        problems: list[str] = []
        clue_ids = {clue.id for clue in self.clues}
        finding_ids = {finding.id for finding in self.findings}
        produced: set[str] = set()
        scene_ids = {scene.id for scene in self.scenes}
        reached: set[str] = {self.scenes[0].id}
        for index, scene in enumerate(self.scenes):
            if index + 1 < len(self.scenes):
                # Scenes are played in declaration order; the session's end_scene() moves to the
                # next one, so the ordered successor is reachable by construction.
                reached.add(self.scenes[index + 1].id)
            for action in scene.actions:
                if action.finding and action.finding not in finding_ids:
                    problems.append(
                        f"action {scene.id}/{action.id}: assembles unknown finding "
                        f"{action.finding!r}"
                    )
                if action.next_scene and action.next_scene not in scene_ids:
                    problems.append(
                        f"action {scene.id}/{action.id}: next_scene {action.next_scene!r} is no scene"
                    )
                if action.next_scene:
                    reached.add(action.next_scene)
                for clue_id in action.gives:
                    if clue_id not in clue_ids:
                        problems.append(
                            f"action {scene.id}/{action.id}: gives unknown clue {clue_id!r}"
                        )
                    produced.add(clue_id)
                for required in action.requires:
                    if required not in clue_ids and required not in finding_ids:
                        problems.append(
                            f"action {scene.id}/{action.id}: requires unknown clue/finding "
                            f"{required!r}"
                        )
                if action.check is not None:
                    try:
                        individual_skill(action.check.skill)
                    except ValueError as exc:
                        problems.append(f"action {scene.id}/{action.id}: {exc}")
                if action.psi is not None and not action.psi.capability.strip():
                    problems.append(
                        f"action {scene.id}/{action.id}: a psi gate must name the capability"
                    )
        for scene_id in sorted(scene_ids - reached):
            problems.append(f"scene {scene_id!r} is not reachable from the opening scene")
        for clue_id in sorted(clue_ids - produced):
            problems.append(f"clue {clue_id!r} cannot be obtained by any action")
        for finding in self.findings:
            for fragment in finding.fragments:
                if fragment not in clue_ids:
                    problems.append(f"finding {finding.id!r}: unknown fragment {fragment!r}")
            if finding.partial_min and finding.partial_min > len(finding.fragments):
                problems.append(
                    f"finding {finding.id!r}: partial_min {finding.partial_min} exceeds its "
                    f"{len(finding.fragments)} fragments"
                )
        for resolution in self.resolutions:
            if resolution.requires_finding:
                if resolution.requires_finding not in finding_ids:
                    problems.append(
                        f"resolution {resolution.id!r}: unknown finding "
                        f"{resolution.requires_finding!r}"
                    )
                else:
                    finding = self.finding(resolution.requires_finding)
                    if not set(finding.fragments) & produced:
                        problems.append(
                            f"resolution {resolution.id!r}: no fragment of its finding can be found"
                        )
            for required in resolution.requires:
                if required not in clue_ids:
                    problems.append(
                        f"resolution {resolution.id!r}: requires unknown clue {required!r}"
                    )
            if (resolution.force_attack_skill or resolution.tie_is_not_total_failure) and not (
                resolution.opposed_by
            ):
                problems.append(
                    f"resolution {resolution.id!r}: carries a confrontation option but names no "
                    "opposition, so the option could never apply"
                )
            if resolution.requires_fragments and not set(self.chain).intersection(produced):
                problems.append(
                    f"resolution {resolution.id!r}: requires fragments, but no action yields any"
                )
        for fragment in self.chain:
            if fragment not in clue_ids:
                problems.append(f"chain names unknown clue {fragment!r}")
            elif fragment not in produced:
                problems.append(f"chain fragment {fragment!r} cannot be obtained")
        return tuple(problems)

    def validate(self) -> CaseFile:
        """Raise on the first structural problem, so a broken case cannot be loaded and played."""
        problems = self.structural_problems()
        if problems:
            raise CaseSpecError(
                f"case {self.id!r} cannot be played as written:\n  " + "\n  ".join(problems)
            )
        return self

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = dict(self.detail)
        payload.update(
            {
                "format": CASE_FORMAT,
                "schema_version": CASE_SCHEMA_VERSION,
                "id": self.id,
                "title": self.title,
                "core_question": self.core_question,
                "hook": self.hook,
                "era": self.era,
                "era_label": self.era_label,
                "chain": list(self.chain),
                "author_note": self.author_note,
                "scenes": [scene.to_dict() for scene in self.scenes],
                "clues": [clue.to_dict() for clue in self.clues],
                "findings": [finding.to_dict() for finding in self.findings],
                "resolutions": [resolution.to_dict() for resolution in self.resolutions],
            }
        )
        return payload
