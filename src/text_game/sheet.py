"""Player-character sheet for the playable slice, backed by the EP2 kernel.

Issue #60's first playable milestone asks for character sheets, EP2-style skill
tests, pools, damage/stress and embodiment **in the playable loop**. The mechanics
already exist in ``src/eclipse_phase_homebrew/`` (#61/#66/#67/#69) and resolve
deterministically; this module is the missing seam that gives an actor in the text
game a sheet and routes an intent through that kernel.

Design rules this module enforces rather than documents:

* **Additive.** ``ActorState`` keeps every field it had. A sheet is optional, so an
  actor without one still plays exactly as before (AGENTS.md: preserve, do not
  replace).
* **Intent in, mechanics out.** A controller (human, scripted, dumb, LLM) chooses
  *what* to attempt; this module decides *whether it works*. No dice value is ever
  taken from a model.
* **No new canon.** Aptitudes and skills are free-form labels here. The final names
  and counts are explicitly not locked by the rulebook, so nothing in this file
  invents them; the fixture sheets below use the EP2 reference labels only as
  non-canonical playtest data.
* **Reproducible.** Every resolution accepts an injected roll or a seeded RNG, so a
  simulation can be replayed exactly.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from eclipse_phase_homebrew import (
    EP2Character,
    EP2HarmState,
    EP2PoolState,
    PoolKind,
    PoolSpend,
    resolve_test,
)
from eclipse_phase_homebrew.embodiment import EP2Embodiment
from eclipse_phase_homebrew.interactions import (
    resolve_combat_attack,
    resolve_hack_action,
    resolve_social_action,
)

#: Action kinds the sheet can resolve. These are *kinds of test*, not new rules:
#: each maps onto a subsystem the kernel already implements.
TEST_KINDS = ("skill", "combat", "social", "mesh")

#: Prototype default difficulty when a caller supplies no modifier. Zero is the
#: neutral value EP2 uses for "no situational modifier", not an invented target.
NEUTRAL_MODIFIER = 0


class SheetError(ValueError):
    """The sheet is malformed, or the requested test cannot be resolved."""


@dataclass(slots=True)
class CharacterSheet:
    """An actor's EP2-derived mechanics, additive to the text-game actor state.

    ``name``/``aptitudes``/``skills`` feed the kernel's ``EP2Character``; ``pools``
    and ``harm`` are the mutable state. ``embodiment`` is optional because the
    kernel models it separately (identity versus body) and the rulebook leaves the
    final relationship open.
    """

    name: str
    aptitudes: dict[str, int] = field(default_factory=dict)
    skills: dict[str, int] = field(default_factory=dict)
    pools: EP2PoolState = field(default_factory=lambda: EP2PoolState())
    harm: EP2HarmState | None = None
    embodiment: EP2Embodiment | None = None

    def __post_init__(self) -> None:
        if not str(self.name).strip():
            raise SheetError("sheet name must not be empty")
        self.aptitudes = {str(k): int(v) for k, v in dict(self.aptitudes).items()}
        self.skills = {str(k): int(v) for k, v in dict(self.skills).items()}
        for label, values in (("aptitude", self.aptitudes), ("skill", self.skills)):
            for key, rating in values.items():
                if not 0 <= rating <= 100:
                    raise SheetError(f"{label} {key!r} rating {rating} must be in 0..100")

    # -- kernel adapters -------------------------------------------------- #

    def character(self) -> EP2Character:
        """The immutable kernel view of this sheet.

        The kernel validates names and 0..100 ratings; going through it rather than
        duplicating the check keeps one source of truth for what a legal rating is.
        """
        return EP2Character(
            name=self.name,
            skills=dict(self.skills),
            aptitudes=dict(self.aptitudes),
            morph=self.embodiment.name if self.embodiment else "",
            durability=self.embodiment.durability if self.embodiment else None,
            wound_threshold=self.embodiment.wound_threshold if self.embodiment else None,
        )

    def target_for(self, *, skill: str = "", aptitude: str = "") -> tuple[int, bool]:
        """The target number for a test, and whether it is defaulted.

        A named skill uses its own rating; otherwise the linked aptitude is used and
        the test is flagged defaulted, which is the kernel's rule and not a
        simplification made here. Unknown labels are refused rather than defaulted to
        a made-up number.
        """
        skill = str(skill).strip()
        aptitude = str(aptitude).strip()
        if skill:
            if skill in self.skills:
                return self.skills[skill], False
            if aptitude and aptitude in self.aptitudes:
                return self.aptitudes[aptitude], True
            raise SheetError(
                f"sheet {self.name!r} has no skill {skill!r}"
                + (f" and no aptitude {aptitude!r} to default to" if aptitude else "")
            )
        if aptitude:
            if aptitude in self.aptitudes:
                return self.aptitudes[aptitude], False
            raise SheetError(f"sheet {self.name!r} has no aptitude {aptitude!r}")
        raise SheetError("a test requires a skill or an aptitude")

    # -- serialisation ---------------------------------------------------- #

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "aptitudes": dict(self.aptitudes),
            "skills": dict(self.skills),
            "pools": {
                "maximum": {k.value: int(v) for k, v in self.pools.maximum.items()},
                "current": {k.value: int(v) for k, v in self.pools.current.items()},
            },
            "harm": (
                {
                    "durability": self.harm.durability,
                    "wound_threshold": self.harm.wound_threshold,
                    "lucidity": self.harm.lucidity,
                    "trauma_threshold": self.harm.trauma_threshold,
                    "damage": self.harm.damage,
                    "wounds": self.harm.wounds,
                    "stress": self.harm.stress,
                    "traumas": self.harm.traumas,
                }
                if self.harm is not None
                else None
            ),
            "embodiment": (
                {
                    "name": self.embodiment.name,
                    "kind": self.embodiment.kind,
                    "durability": self.embodiment.durability,
                    "wound_threshold": self.embodiment.wound_threshold,
                    "traits": list(self.embodiment.traits),
                }
                if self.embodiment is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> CharacterSheet:
        pools_payload = dict(data.get("pools") or {})
        harm_payload = data.get("harm")
        embodiment_payload = data.get("embodiment")
        return cls(
            name=str(data["name"]),
            aptitudes={str(k): int(v) for k, v in dict(data.get("aptitudes") or {}).items()},
            skills={str(k): int(v) for k, v in dict(data.get("skills") or {}).items()},
            pools=EP2PoolState(
                maximum={PoolKind(k): int(v) for k, v in dict(pools_payload.get("maximum") or {}).items()},
                current={PoolKind(k): int(v) for k, v in dict(pools_payload.get("current") or {}).items()},
            ),
            harm=(
                EP2HarmState(
                    durability=int(harm_payload["durability"]),
                    wound_threshold=int(harm_payload["wound_threshold"]),
                    lucidity=int(harm_payload["lucidity"]),
                    trauma_threshold=int(harm_payload["trauma_threshold"]),
                    damage=int(harm_payload.get("damage", 0)),
                    wounds=int(harm_payload.get("wounds", 0)),
                    stress=int(harm_payload.get("stress", 0)),
                    traumas=int(harm_payload.get("traumas", 0)),
                )
                if harm_payload
                else None
            ),
            embodiment=(
                EP2Embodiment(
                    name=str(embodiment_payload["name"]),
                    kind=str(embodiment_payload.get("kind", "biological")),
                    durability=int(embodiment_payload.get("durability", 30)),
                    wound_threshold=int(embodiment_payload.get("wound_threshold", 6)),
                    traits=tuple(str(t) for t in embodiment_payload.get("traits", ())),
                )
                if embodiment_payload
                else None
            ),
        )

    def summary(self) -> str:
        """Human-readable sheet for the text UI (milestone item 4)."""
        lines = [f"Sheet: {self.name}"]
        if self.aptitudes:
            lines.append("  Aptitudes: " + ", ".join(
                f"{k} {v}" for k, v in sorted(self.aptitudes.items())))
        if self.skills:
            lines.append("  Skills: " + ", ".join(
                f"{k} {v}" for k, v in sorted(self.skills.items())))
        if self.pools.maximum:
            lines.append("  Pools: " + ", ".join(
                f"{k.value} {self.pools.current.get(k, 0)}/{v}"
                for k, v in sorted(self.pools.maximum.items(), key=lambda kv: kv[0].value)))
        if self.harm is not None:
            lines.append(
                f"  Harm: damage {self.harm.damage}/{self.harm.durability}"
                f" ({self.harm.wounds} wounds), stress {self.harm.stress}/{self.harm.lucidity}"
                f" ({self.harm.traumas} traumas)")
            if self.harm.incapacitated:
                lines.append("  Incapacitated.")
            elif self.harm.overwhelmed:
                lines.append("  Overwhelmed.")
        if self.embodiment is not None:
            lines.append(f"  Embodiment: {self.embodiment.name} ({self.embodiment.kind})")
        return "\n".join(lines)


@dataclass(frozen=True, slots=True)
class SheetResolution:
    """One resolved test or contest, ready for the narrative layer to describe."""

    kind: str
    detail: dict[str, Any]
    outcome: str

    def as_text(self) -> str:
        if self.kind == "skill":
            result = self.detail["result"]
            verdict = "success" if result["success"] else "failure"
            return (
                f"{self.detail['skill'] or self.detail['aptitude']} test: roll {result['roll']}"
                f" vs {result['target']} -> {verdict} ({result['degree']})"
            )
        contested = self.detail["result"]["opposed"]
        winner = "you win" if contested["winner"] == "attacker" else "you lose"
        extra = ""
        if self.detail["result"].get("effect_amount"):
            extra = f", {self.detail['result']['effect_amount']} damage"
        return (
            f"{self.kind}: attacker {contested['attacker']['roll']}"
            f" vs defender {contested['defender']['roll']} -> {winner}{extra}"
        )

    @property
    def succeeded(self) -> bool:
        if self.kind == "skill":
            return bool(self.detail["result"]["success"])
        return self.detail["result"]["opposed"]["winner"] == "attacker"


def resolve_sheet_test(
    sheet: CharacterSheet,
    *,
    kind: str = "skill",
    skill: str = "",
    aptitude: str = "",
    modifier: int = NEUTRAL_MODIFIER,
    roll: int | None = None,
    rng: Any = None,
    pool_kind: PoolKind | None = None,
    pool_spend: str | None = None,
    defender_sheet: CharacterSheet | None = None,
    defender_skill: str = "",
    defender_aptitude: str = "",
    defender_modifier: int = NEUTRAL_MODIFIER,
    defender_roll: int | None = None,
    damage: int = 0,
) -> SheetResolution:
    """Resolve a playable action through the deterministic EP2 kernel.

    ``skill`` uses the sheet's own rating; ``aptitude`` is the fallback and marks the
    test defaulted. ``kind`` selects how the kernel is invoked:

    * ``"skill"`` — a single test;
    * ``"combat"`` — an opposed contest that applies ``damage`` to the defender on a
      win, mutating the defender's harm state;
    * ``"social"`` / ``"mesh"`` — opposed contests with no invented narrative effect.

    The defender's rolls are injected the same way, so an entire exchange is
    reproducible from a seed.
    """
    kind = str(kind).strip().casefold()
    if kind not in TEST_KINDS:
        raise SheetError(f"unknown test kind {kind!r}; expected one of {list(TEST_KINDS)}")

    target, defaulted = sheet.target_for(skill=skill, aptitude=aptitude)

    if kind == "skill":
        spend = PoolSpend(pool_spend) if pool_spend else PoolSpend.NONE
        result = resolve_test(
            target=target,
            modifier=int(modifier),
            defaulted=defaulted,
            roll=roll,
            rng=rng,
            pools=sheet.pools if pool_kind is not None else None,
            pool_kind=pool_kind,
            pool_spend=spend,
        )
        payload = _test_payload(result)
        return SheetResolution(
            kind="skill",
            detail={"skill": str(skill), "aptitude": str(aptitude), "result": payload},
            outcome=payload["degree"],
        )

    if defender_sheet is None:
        raise SheetError(f"a {kind} test needs a defender sheet")
    defender_target, _defender_defaulted = defender_sheet.target_for(
        skill=defender_skill, aptitude=defender_aptitude
    )

    if kind == "combat":
        if defender_sheet.harm is None:
            raise SheetError("a combat test needs the defender to have harm state")
        interaction = resolve_combat_attack(
            attacker_target=target,
            defender_target=defender_target,
            damage=int(damage),
            defender_harm=defender_sheet.harm,
            attacker_roll=roll,
            defender_roll=defender_roll,
            attacker_modifier=int(modifier),
            defender_modifier=int(defender_modifier),
        )
    else:
        resolver = resolve_social_action if kind == "social" else resolve_hack_action
        interaction = resolver(
            attacker_target=target,
            defender_target=defender_target,
            attacker_roll=roll,
            defender_roll=defender_roll,
            attacker_modifier=int(modifier),
            defender_modifier=int(defender_modifier),
        )

    payload = {
        "opposed": {
            "attacker": _test_payload(interaction.opposed.attacker),
            "defender": _test_payload(interaction.opposed.defender),
            "winner": interaction.opposed.winner,
            "margin": interaction.opposed.margin,
        },
        "effect_applied": interaction.effect_applied,
        "effect_amount": interaction.effect_amount,
        "threshold_events": interaction.threshold_events,
    }
    return SheetResolution(
        kind=kind,
        detail={"skill": str(skill), "aptitude": str(aptitude), "result": payload},
        outcome=interaction.opposed.winner,
    )


def _test_payload(result: Any) -> dict[str, Any]:
    """Serialise an ``EP2TestResult`` for events and the text UI."""
    return {
        "roll": result.roll,
        "base_target": result.base_target,
        "modifier": result.modifier,
        "target": result.target,
        "success": bool(result.success),
        "critical": bool(result.critical),
        "critical_success": bool(result.critical_success),
        "critical_failure": bool(result.critical_failure),
        "superior_successes": result.superior_successes,
        "superior_failures": result.superior_failures,
        "defaulted": bool(result.defaulted),
        "degree": result.degree,
        "pool_kind": result.pool_kind.value if result.pool_kind else "",
        "pool_spend": result.pool_spend.value,
    }


def fixture_sheets() -> dict[str, CharacterSheet]:
    """Non-canonical sheets for the existing fixture actors.

    Ratings are playtest placeholders chosen to exercise success and failure, not
    setting material: the rulebook leaves final attribute names and counts open, so
    nothing here is proposed as canon. Keyed by the actor ids the fixture world uses.
    """
    from .model import FIXTURE_PREFIX

    return {
        FIXTURE_PREFIX + "human": CharacterSheet(
            name="Human player (fixture)",
            aptitudes={"COG": 60, "REF": 55, "SAV": 50, "SOM": 45, "WIL": 50},
            skills={"Perceive": 55, "Interface": 45, "Persuade": 50},
            pools=EP2PoolState(maximum={PoolKind.INSIGHT: 2, PoolKind.MOXIE: 2,
                                        PoolKind.VIGOR: 3, PoolKind.FLEX: 1}),
            harm=EP2HarmState(durability=30, wound_threshold=6, lucidity=25, trauma_threshold=5),
            embodiment=EP2Embodiment(name="fixture baseline morph", kind="biological",
                                     durability=30, wound_threshold=6),
        ),
        FIXTURE_PREFIX + "greeter": CharacterSheet(
            name="Scripted greeter (fixture)",
            aptitudes={"SAV": 50, "WIL": 45, "COG": 40},
            skills={"Persuade": 45, "Interface": 40},
            harm=EP2HarmState(durability=20, wound_threshold=5, lucidity=20, trauma_threshold=4),
        ),
        FIXTURE_PREFIX + "wanderer": CharacterSheet(
            name="Dumb wanderer (fixture)",
            aptitudes={"REF": 40, "SOM": 40, "WIL": 35},
            skills={"Perceive": 35, "Interface": 30},
            harm=EP2HarmState(durability=20, wound_threshold=5, lucidity=20, trauma_threshold=4),
        ),
        FIXTURE_PREFIX + "llm-contact": CharacterSheet(
            name="LLM contact (fixture)",
            aptitudes={"COG": 55, "SAV": 55, "WIL": 50},
            skills={"Persuade": 50, "Interface": 50},
            pools=EP2PoolState(maximum={PoolKind.INSIGHT: 2, PoolKind.MOXIE: 2}),
            harm=EP2HarmState(durability=25, wound_threshold=5, lucidity=25, trauma_threshold=5),
        ),
    }


__all__ = [
    "NEUTRAL_MODIFIER",
    "TEST_KINDS",
    "CharacterSheet",
    "SheetError",
    "SheetResolution",
    "fixture_sheets",
    "resolve_sheet_test",
]
