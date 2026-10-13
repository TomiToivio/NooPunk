"""The RPG layer's runnable worked scene: one seed, three demos, one engine, one printed report.

**Fate Core System © Evil Hat Productions, licensed CC BY 3.0** — see
[`ATTRIBUTION.md`](ATTRIBUTION.md). This module is original NoöPunk code; it reproduces no other
game's text, art or setting content.

What it reports
---------------
Issue #389's worked example is *"one short investigation scene resolving a cyber check and a PSI
check with the same Fate engine"*. That scene exists as
:func:`strategy_game.rpg.fate.demo_investigation`; this module makes it **runnable as code** — the
thing a reader or a playtester actually executes, through
`python -m strategy_game.rpg` — and reports the whole demonstration in one payload:

* the **investigation**: a cyber *overcome* and a PSI *create advantage*, same engine, same seed;
* the two **BCI netrunning** examples, a reachability-first scene and a foothold-first scene — a BCI
  is technology, and neither scene lets it be PSI;
* the **GM boundary**, restated in the payload: an RPG check produces dice, a total, a shift count
  and a ladder rung, and pacing, permission, costs, boosts, consequences and concession stay at the
  table;
* the **seam** this layer is not: the strategy and political layers' exclusions, read from
  :mod:`strategy_game.rpg.boundary` rather than restated, because that module is the single declared
  place where this layer and the strategy engine meet.

No RNG state is kept and no second dice roller is introduced: the demos roll their own seeded
:class:`random.Random`, and this module only reads the results.

Noncanonical and illustrative
-----------------------------
The fiction, the skill names and the difficulties belong to the demos and are the GM's illustrative
choices for an example, not approved crossover rules — the final skill vocabulary and difficulty
scale are among the author's pending decisions in ``strategy_game/RULEBOOK.md``. Nothing here is
scenario canon, nothing names a real institution, and nothing is dated beyond the setting's **20XX**.

Run it::

    python -m strategy_game.rpg            # this report as JSON
    python -m strategy_game.rpg --text    # the same report as reading text
"""
from __future__ import annotations

from typing import Any, Mapping

from . import boundary
from .fate import Action, Outcome, Resolution, demo_investigation, demo_netrunning, demo_netrunning_foothold

__all__ = [
    "DEFAULT_SEED",
    "ENGINE_DOES_NOT_DECIDE",
    "FATE_NOTATION",
    "SCENE_ID",
    "SCENE_REPORT_VERSION",
    "render_report",
    "scene_report",
]

#: Version of this report's shape, so a consumer can refuse a document that is not one.
SCENE_REPORT_VERSION = "rpg-scene-report-1"

#: Identifier of the worked scene. Noncanonical and scenario-free.
SCENE_ID = "noopunk-rpg-worked-scene"

#: The demos are seeded; this is the seed a bare ``python -m strategy_game.rpg`` uses.
DEFAULT_SEED = 42

#: How this engine's dice are written in a rulebook or a playtest note (Fate Core: four dice, each
#: showing -1, 0 or +1).
FATE_NOTATION = "4dF"

#: What a Fate check does **not** decide here. Mirrors ``rpg/RULEBOOK.md`` §1, §3 and §7: the engine
#: reports a ladder rung and a shift count, and every item below stays a GM or table judgement.
ENGINE_DOES_NOT_DECIDE: tuple[str, ...] = (
    "scene pacing and turn order",
    "fictional permission to attempt the action",
    "the connectivity question, answered before any roll (issue #344)",
    "which aspect is invoked or compelled",
    "what a tie costs and whether it is accepted",
    "the name and scope of a boost or scene aspect",
    "whether a consequence is accepted and how it reads",
    "taken out and concession",
    "anything belonging to faction strategy or political simulation",
)

#: ``(scene, key)`` in the order the three demos roll, so the report can name what each check was.
_CHECK_ORDER: tuple[tuple[str, str], ...] = (
    ("investigation", "cyber"),
    ("investigation", "psi"),
    ("netrunning", "approach"),
    ("netrunning", "defend"),
    ("foothold", "access"),
    ("foothold", "intrusion"),
)


def _scenes(seed: int) -> dict[str, Mapping[str, object]]:
    """The three shipped demos, run with one seed so the whole report reproduces."""
    return {
        "investigation": demo_investigation(seed),
        "netrunning": demo_netrunning(seed),
        "foothold": demo_netrunning_foothold(seed),
    }


def _check_payload(scene: str, check: str, result: Resolution) -> dict[str, Any]:
    return {
        "scene": scene,
        "check": check,
        "action": result.action.value,
        "dice": list(result.dice),
        "skill": result.skill,
        "difficulty": result.difficulty,
        "total": result.total,
        "shifts": result.shifts,
        "outcome": result.outcome.value,
    }


def scene_report(seed: int = DEFAULT_SEED) -> dict[str, Any]:
    """Run the layer's demonstrations deterministically and return the whole report as plain data.

    Same seed, same report. A demo may carry a non-check value under one of the reported keys, so
    only :class:`~strategy_game.rpg.fate.Resolution` values become checks; nothing is invented to fill
    a gap.
    """
    scenes = _scenes(seed)
    checks: list[dict[str, Any]] = []
    for scene, check in _CHECK_ORDER:
        candidate = scenes[scene].get(check)
        if isinstance(candidate, Resolution):
            checks.append(_check_payload(scene, check, candidate))

    return {
        "schema_version": SCENE_REPORT_VERSION,
        "scene": SCENE_ID,
        "seed": seed,
        "dice": FATE_NOTATION,
        "engine": {
            "actions": [action.value for action in Action],
            "outcomes": [outcome.value for outcome in Outcome],
            "resolution": "4dF + skill versus difficulty; shifts = total - difficulty",
        },
        "checks": checks,
        "rolls_made": len(checks),
        "engine_does_not_decide": list(ENGINE_DOES_NOT_DECIDE),
        "boundary_excludes": list(boundary.NOT_THIS_LAYER),
        "note": (
            "Noncanonical and illustrative: an example of the engine, not scenario canon. The three "
            "demos are the RPG layer's; faction strategy and political simulation are a different, "
            "unapproved layer and contribute nothing here."
        ),
    }


def render_report(report: Mapping[str, Any]) -> str:
    """The report as text: the checks, the dice as they fell, and the table's own part."""
    lines = [
        f"— {report['scene']} (seed {report['seed']}, {report['dice']}) —",
        "",
    ]
    for check in report["checks"]:
        dice = ",".join(f"{face:+d}" for face in check["dice"])
        lines.append(
            f"{check['scene']}/{check['check']}: {check['action']} "
            f"skill {check['skill']:+d} vs {check['difficulty']} "
            f"[{dice}] = {check['total']:+d} ({check['shifts']:+d} shifts) → {check['outcome']}"
        )
    lines += [
        "",
        f"checks resolved: {report['rolls_made']} (one engine, {report['dice']})",
        "",
        "The table keeps: " + "; ".join(report["engine_does_not_decide"]) + ".",
        "This layer excludes: " + "; ".join(report["boundary_excludes"]) + ".",
        str(report["note"]),
    ]
    return "\n".join(lines)
