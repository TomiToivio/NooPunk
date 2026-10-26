#!/usr/bin/env python3
"""One character sheet, one base system, four environment types — the #615 mixed-genre example.

Author direction (2026-10-26): *"For beginning, use CWN/SWN/AWN/WWN system for everything. Make the
stats, skills, all rules based on them. We will modify later."* So the **default** here is the base
system (`rules.wn`: 2d6 + attribute modifier + skill level), and `--system legacy` runs the same sheet
through the transitional `1d10` layer (`rules.core`) so the difference is visible side by side.

What stays constant across all four scenes, in both systems:

* **one sheet** — printed before the first scene, unchanged after the last;
* **one grammar** — every outcome comes from a single kernel call, never a second dice convention;
* **the four modules** contribute procedure only: a network route, a local scarcity track, a contact
  exchange, a realm's navigation DV.

Deterministic under `--seed`, offline, no model.

Usage:
    python scripts/mixed_genre_demo.py [--seed N] [--system wn|legacy]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.rules import core  # noqa: E402
from src.rules import cross_domain_state as cds  # noqa: E402
from src.rules import noospace_projection as nsp  # noqa: E402
from src.rules import noopunk_social_extensions as social  # noqa: E402
from src.rules import ubiquitous_network as un  # noqa: E402
from src.rules import wn  # noqa: E402

CANON_SKILLS = {
    entry["name"]: entry["stat"]
    for entry in json.loads((ROOT / "data" / "rules" / "skills.json").read_text(encoding="utf-8"))["skills"]
}

#: The one sheet, written in the legacy vocabulary and converted to the base system on the fly, so the
#: demonstration shows the *migration* as well as the play. 1..10 -> 3..18 attributes, 1..10 -> 0..4
#: skill levels, via `rules.wn`.
SHEET: dict[str, Any] = {
    "name": "Vera Kallio",
    "role": "UNSA field analyst, seconded to the Noetic Office",
    "stats": {"FIT": 4, "REF": 5, "INT": 7, "SOC": 6, "CYB": 6, "PSY": 5},
    "skills": {"Program": 4, "Interface": 3, "Infosec": 3, "Perceive": 3,
               "Survival": 2, "ESP": 2, "Psychic Defence": 1},
}


class Scene:
    """Books AP against the shared 3-per-exchange clock and prints one transcript."""

    def __init__(self, rng: random.Random, system: str) -> None:
        self.rng = rng
        self.system = system
        self.ap = 0
        self.exchanges = 1
        self.checks = 0

    def _spend(self, cost: int) -> None:
        if self.ap + cost > cds.AP_PER_EXCHANGE:
            self.ap = 0
            self.exchanges += 1
        self.ap += cost

    def check(self, skill: str, dv: int, *, cost: int = 1) -> bool:
        """Resolve one check on the selected kernel; returns success."""
        self._spend(cost)
        self.checks += 1
        legacy_stat = CANON_SKILLS[skill]

        if self.system == "legacy":
            stat_value = SHEET["stats"][legacy_stat]
            skill_value = SHEET["skills"][skill]
            result = core.resolve_check(stat=stat_value, skill=skill_value, target=dv, rng=self.rng)
            print(f"    check  {legacy_stat} {stat_value} + {skill} {skill_value}"
                  f" + 1d10({result.die}) = {result.total} vs DV {dv}"
                  f" -> {'success' if result.success else 'failure'}"
                  f" (margin {result.total - dv:+d}, AP {cost})")
            return result.success

        code = wn.LEGACY_STAT_MAP[legacy_stat]
        score = wn.from_legacy_stat(SHEET["stats"][legacy_stat])
        level = wn.from_legacy_skill(SHEET["skills"][skill])
        result = wn.resolve_skill_check(attribute=code, score=score, skill_level=level,
                                        difficulty=dv, rng=self.rng)
        dice = ",".join(str(d) for d in result.dice)
        print(f"    check  {code} {score}({result.attribute_modifier:+d}) + {skill} {level}"
              f" + 2d6({dice}) = {result.total} vs DV {dv}"
              f" -> {'success' if result.success else 'failure'}"
              f" (margin {result.margin:+d}, AP {cost})")
        return result.success


def scene_helsinki(scene: Scene, dvs: dict[str, int]) -> None:
    """CWN module: urban cyberpunk. The network is geography, not a matrix."""
    print("\nSCENE 1 — Helsinki, Kallio safehouse (CWN module: urban network cyberpunk)")
    possible, reason = un.reach(target=un.ConnectivityClass.SAFENET_EXPOSED,
                                access=un.AccessClass.SAFENET, era=un.Era.AFTER_CRISIS)
    print(f"    reach  {un.AccessClass.SAFENET.value} -> safenet-exposed: "
          f"{'possible' if possible else 'impossible'} ({reason})")
    inside, inside_reason = un.reach(target=un.ConnectivityClass.PRIVATE_LINKED,
                                     access=un.AccessClass.SAFENET, era=un.Era.AFTER_CRISIS)
    print(f"    reach  {un.AccessClass.SAFENET.value} -> private-linked: "
          f"{'possible' if inside else 'impossible'} ({inside_reason})")
    if not possible:  # pragma: no cover - the canon pairing table says it is possible
        raise SystemExit("canon pairing table refused a route it must allow")

    session = un.IntrusionSession(target=un.ConnectivityClass.SAFENET_EXPOSED,
                                  access=un.AccessClass.SAFENET, era=un.Era.AFTER_CRISIS,
                                  rng=scene.rng)
    step = session.intrude(stat=SHEET["stats"]["CYB"], skill_rating=SHEET["skills"]["Program"],
                           dv=dvs["intrusion"])
    scene._spend(un.TUNING_AP_PER_ACTION)
    scene.checks += 1
    alert = getattr(step.alert, "value", step.alert)
    print(f"    intrude {step.outcome} (margin {step.margin:+d}) -> exposure {step.exposure_total},"
          f" alert {alert}")


def scene_exclusion_zone(scene: Scene, dvs: dict[str, int]) -> None:
    """AWN module: a locally devastated region. Scarcity is local, never a world apocalypse."""
    print("\nSCENE 2 — the Vantaa exclusion zone (AWN module: crisis ruins)")
    crisis = social.LocalCrisis(scarcity=2, trust=1)
    crisis.apply(lost_supplies=2, hazard=1)
    print(f"    tracks scarcity {crisis.scarcity}, trust {crisis.trust}, exposure {crisis.exposure}")
    scene.check("Survival", dvs["survival"])


def scene_alien_outpost(scene: Scene, dvs: dict[str, int]) -> None:
    """SWN module: an NHI outpost. Contact is an exchange, not a reaction roll."""
    print("\nSCENE 3 — an outpost at the edge of the debris belt (SWN module: NHI contact)")
    contact = social.NHIContact(reciprocity=0, autonomy=3)
    contact.exchange(mutual_benefit=2, imposed_dependency=1)
    print(f"    contact reciprocity {contact.reciprocity:+d}, autonomy {contact.autonomy}"
          " (what it costs is a decision, not a die)")
    scene.check("Perceive", dvs["perceive"])


def scene_noetic_realm(scene: Scene, dvs: dict[str, int]) -> None:
    """WWN module: an interdimensional realm. Magic is re-read as PSI; the realm sets the difficulty."""
    print("\nSCENE 4 — the shallows of the noetic realm (WWN module: interdimensional)")
    here = nsp.shift_region(nsp.Region.NEAR, nsp.Direction.DEEPER, steps=2)
    realm_dv = nsp.navigation_dv(region=here, resonance=0.5)
    scale = (f" -> base-system difficulty {dvs['esp']}" if scene.system == "wn" else "")
    print(f"    realm  shifted to {here.value}; the realm's navigation DV {realm_dv}"
          f" at resonance 0.50{scale} (the realm sets the difficulty, not the character's comfort)")
    scene.check("ESP", dvs["esp"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="NoöPunk mixed-genre example (#615)")
    parser.add_argument("--seed", type=int, default=615, help="deterministic dice seed")
    parser.add_argument("--system", choices=("wn", "legacy"), default="wn",
                        help="wn = the base system (default); legacy = the transitional 1d10 layer")
    args = parser.parse_args(argv)

    # The two systems have different ladders, so the same scene is priced on each system's own scale.
    dvs = ({"intrusion": 10, "survival": 8, "perceive": 10, "esp": 12} if args.system == "wn"
           else {"intrusion": 13, "survival": 13, "perceive": 15, "esp": 20})
    kernel = f"{wn.CHECK_DICE} + attribute modifier + skill level" if args.system == "wn" else core.CHECK_DICE

    print(f"NoöPunk mixed-genre example — system {args.system}, seed {args.seed}")
    print("sheet  " + json.dumps(SHEET, ensure_ascii=False, sort_keys=True))
    if args.system == "wn":
        converted = {code: wn.from_legacy_stat(SHEET["stats"][legacy])
                     for legacy, code in wn.LEGACY_STAT_MAP.items()}
        print("attrs  " + json.dumps(converted, sort_keys=True) + f"  (base system {wn.REVISION})")

    scene = Scene(random.Random(args.seed), args.system)
    for run in (scene_helsinki, scene_exclusion_zone, scene_alien_outpost, scene_noetic_realm):
        run(scene, dvs)

    print(f"\nsheet  unchanged: {SHEET['name']}, {len(SHEET['skills'])} skills, one grammar")
    print(f"total  {scene.checks} checks, {scene.exchanges} exchange(s), "
          f"{cds.AP_PER_EXCHANGE} AP each, kernel {kernel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
