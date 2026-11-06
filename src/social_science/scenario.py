"""Small synthetic political-discourse scenario for #1286.

The fixture is deliberately fictional and generic: six residents, two civic
organizations, three contested claims and a handful of social ties. It is not
NoöPunk canon, not evidence about any real group, and not a template for
identifying real people.
"""

from __future__ import annotations

from .engine import SocialScienceSimulation
from .model import Actor, Claim, Material, Provenance, SimulationConfig, SocialEdge

__all__ = ["build_synthetic_scenario"]


def _p(source: str = "fixture:synthetic-scenario") -> Provenance:
    return Provenance(
        Material.SYNTHESIZED, source, "synthetic-fixture", 0.0, "PROVISIONAL"
    )


def build_synthetic_scenario(
    *, seed: int = 7, turns: int = 8, intervention: bool = False
) -> SocialScienceSimulation:
    """Build a reproducible control or intervention case.

    ``intervention`` raises one civic organization's attention and gives a
    coalition-minded resident an extra tie. It is an *experiment fixture*, not a
    policy claim; the export records the difference.
    """
    sim = SocialScienceSimulation(config=SimulationConfig(seed=seed, turns=turns))
    claims = (
        Claim(
            "claim.housing",
            "housing is a right",
            kind="demand",
            provenance=_p(),
            uncertainty=0.15,
        ),
        Claim(
            "claim.security",
            "security requires order",
            kind="demand",
            provenance=_p(),
            uncertainty=0.20,
        ),
        Claim(
            "claim.ecology",
            "the river must be restored",
            kind="demand",
            provenance=_p(),
            uncertainty=0.10,
        ),
    )
    for claim in claims:
        sim.add_claim(claim)

    people = (
        ("actor.a", "Resident A", "individual", "tenant union", 0.55, 0.55),
        ("actor.b", "Resident B", "individual", "tenant union", 0.60, 0.45),
        ("actor.c", "Resident C", "individual", "local business", 0.45, 0.35),
        ("actor.d", "Resident D", "individual", "local business", 0.50, 0.30),
        ("actor.e", "Resident E", "individual", "river group", 0.58, 0.50),
        ("actor.f", "Resident F", "individual", "river group", 0.52, 0.40),
    )
    for actor_id, label, kind, affiliation, resources, attention in people:
        sim.add_actor(
            Actor(
                actor_id,
                label,
                kind,
                affiliation,
                resources=resources,
                attention=attention,
                provenance=_p(),
            )
        )
    org_specs = (
        ("org.tenant", "Tenant Union", "tenant union", 0.35, 0.40),
        ("org.city", "City Office", "city", 0.70, 0.65),
    )
    for actor_id, label, affiliation, resources, attention in org_specs:
        sim.add_actor(
            Actor(
                actor_id,
                label,
                "organization",
                affiliation,
                resources=resources,
                attention=attention,
                provenance=_p(),
            )
        )

    # Individual-to-individual and individual-to-organization ties. Organizations
    # can speak to their members, but they are not "people" with private feelings.
    ties = (
        ("actor.a", "actor.b", "neighbour"),
        ("actor.b", "actor.c", "coworker"),
        ("actor.c", "actor.d", "business partner"),
        ("actor.d", "actor.e", "neighbour"),
        ("actor.e", "actor.f", "river group"),
        ("actor.a", "org.tenant", "member"),
        ("actor.b", "org.tenant", "member"),
        ("actor.c", "org.city", "ratepayer"),
        ("actor.e", "org.city", "petitioner"),
        ("org.tenant", "org.city", "civic link"),
        ("org.city", "actor.f", "constituent"),
    )
    if intervention:
        ties = ties + (("actor.f", "actor.a", "intervention bridge"),)
    for source, target, relation in ties:
        sim.add_social_edge(SocialEdge(source, target, relation, 0, _p(), 0.0))

    # Initial dispositions are assumptions, not measurements.
    starting = {
        "actor.a": {"claim.housing": 0.5, "claim.security": -0.1, "claim.ecology": 0.2},
        "actor.b": {"claim.housing": 0.4, "claim.security": 0.0, "claim.ecology": 0.1},
        "actor.c": {
            "claim.housing": -0.2,
            "claim.security": 0.5,
            "claim.ecology": -0.1,
        },
        "actor.d": {
            "claim.housing": -0.3,
            "claim.security": 0.4,
            "claim.ecology": -0.2,
        },
        "actor.e": {"claim.housing": 0.1, "claim.security": -0.2, "claim.ecology": 0.5},
        "actor.f": {"claim.housing": 0.0, "claim.security": -0.1, "claim.ecology": 0.4},
        "org.tenant": {
            "claim.housing": 0.4,
            "claim.security": 0.0,
            "claim.ecology": 0.1,
        },
        "org.city": {"claim.housing": 0.1, "claim.security": 0.3, "claim.ecology": 0.0},
    }
    for actor_id, values in starting.items():
        sim.actors[actor_id].disposition.update(values)
    if intervention:
        sim.actors["org.city"].attention = 0.90
    return sim
