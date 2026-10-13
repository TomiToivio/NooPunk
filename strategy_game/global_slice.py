"""Experimental #338 Global vertical slice; NOT approved NoöPunk rules.

Standalone stdlib-only prototype. Keeps the existing strategy_game.WorldState untouched.
Every number and outcome in this module is test scaffolding, not setting canon.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from random import Random


@dataclass(frozen=True)
class Hub:
    id: str
    city: str
    systems: tuple[str, ...]


@dataclass(frozen=True)
class Site:
    id: str
    label: str
    hub_id: str
    kind: str
    discovered: bool = False


@dataclass(frozen=True)
class Agent:
    id: str
    name: str
    skills: dict[str, int]


@dataclass(frozen=True)
class Resource:
    id: str
    label: str
    quantity: int
    quality: int


@dataclass(frozen=True)
class Operation:
    id: str
    label: str
    target_id: str
    skill: str
    approaches: tuple[str, ...]
    category: str


@dataclass
class GlobalSlice:
    hubs: list[Hub]
    links: list[tuple[str, str, str]]
    sites: list[Site]
    agents: list[Agent]
    resources: list[Resource]
    operations: list[Operation]
    completed: list[str] = field(default_factory=list)
    log: list[str] = field(default_factory=list)
    political_reactions: list[str] = field(default_factory=list)

    def available_sites(self) -> list[Site]:
        return [site for site in self.sites if site.discovered]

    def perform(self, operation_id: str, agent_id: str, resource_id: str,
                approach: str, *, die: int) -> dict[str, object]:
        """Illustrative d6 resolution, not an approved game rule.

        Player chooses approach; agent activates a passive asset. Failed checks
        produce complications instead of ending the scenario. Dice are supplied
        externally to make results reproducible and easy to audit.
        """
        op = next((o for o in self.operations if o.id == operation_id), None)
        agent = next((a for a in self.agents if a.id == agent_id), None)
        resource = next((r for r in self.resources if r.id == resource_id), None)
        if op is None or agent is None or resource is None:
            raise ValueError("Unknown mission, agent or resource")
        site = next((s for s in self.sites if s.id == op.target_id), None)
        if site is None or not site.discovered:
            raise ValueError("Mission location not discovered")
        if operation_id in self.completed:
            raise ValueError("Mission already completed")
        if approach not in op.approaches:
            raise ValueError("Unavailable mission choice")
        if not isinstance(die, int) or isinstance(die, bool) or not 1 <= die <= 6:
            raise ValueError("The illustrative die must be 1..6")
        if resource.quantity < 0 or resource.quality < 0:
            raise ValueError("Asset quantity and quality must be nonnegative")

        # Small bounded prototype formula only; a real resolver needs approval.
        asset_contribution = min(3, resource.quantity) + resource.quality
        score = die + agent.skills.get(op.skill, 0) + asset_contribution
        success = score >= 8
        outcome = ("Objective achieved" if success else
                   "Complication: partial evidence, opposition or lost access")
        detail = (f"{op.label} at {site.label}: {agent.name} leads {resource.label} "
                  f"(quantity {resource.quantity}, quality {resource.quality}); "
                  f"{op.skill} check {die}+{agent.skills.get(op.skill, 0)}+"
                  f"{asset_contribution}={score}; choice={approach}. {outcome}.")
        self.completed.append(operation_id)
        self.log.append(detail)
        reaction = (f"Global politics: rival UN-aligned networks debate the "
                    f"{op.category} incident; disclosure and legitimacy remain contested.")
        self.political_reactions.append(reaction)
        if success and operation_id == "investigate_crash":
            self.sites = [Site(s.id, s.label, s.hub_id, s.kind, True)
                          if s.id == "hidden_base" else s for s in self.sites]
        return {"success": success, "score": score, "summary": detail,
                "political_reaction": reaction}


def sample_world() -> GlobalSlice:
    """Fictional teaching scenario; selected real cities are geography only."""
    return GlobalSlice(
        hubs=[
            Hub("nyc", "New York", ("politics", "media", "economy")),
            Hub("geneva", "Geneva", ("law", "politics", "science")),
            Hub("nairobi", "Nairobi", ("politics", "education", "media")),
            Hub("shanghai", "Shanghai", ("economy", "science", "media")),
        ],
        links=[("nyc", "geneva", "diplomacy"), ("geneva", "nairobi", "institutions"),
               ("nairobi", "shanghai", "research"), ("shanghai", "nyc", "capital")],
        sites=[
            Site("crash", "Suspected crash zone", "nairobi", "investigation", True),
            Site("data", "Corporate research archive", "geneva", "infiltration", True),
            Site("hidden_base", "Unknown installation", "shanghai", "anomaly", False),
        ],
        agents=[
            Agent("leader", "Faction leader", {"investigation": 2, "cyber": 1, "command": 1}),
            Agent("analyst", "Network analyst", {"investigation": 1, "cyber": 3, "command": 0}),
            Agent("officer", "Operations officer", {"investigation": 1, "cyber": 0, "command": 3}),
        ],
        resources=[
            Resource("field", "Field investigators", 2, 1),
            Resource("cyber", "Cyber research team", 1, 2),
            Resource("security", "Security detachment", 3, 1),
        ],
        operations=[
            Operation("investigate_crash", "Investigate anomalous wreckage", "crash",
                      "investigation", ("protect witnesses", "share evidence"), "NHI"),
            Operation("archive_heist", "Infiltrate corporate archive", "data", "cyber",
                      ("quiet access", "publish findings"), "AGI"),
            Operation("base_response", "Respond to unknown installation", "hidden_base",
                      "command", ("attempt contact", "abstract assault"), "NHI"),
        ],
    )


def view(world: GlobalSlice, section: str) -> str:
    if section == "map":
        nodes = "\n".join(f"  {h.city}: {', '.join(h.systems)}" for h in world.hubs)
        edges = "\n".join(f"  {a} <-> {b} [{kind}]" for a,b,kind in world.links)
        sites = "\n".join(f"  {s.label} near {s.hub_id}" for s in world.available_sites())
        return f"GLOBAL NETWORK SOCIETY\n{nodes}\nNETWORK LINKS\n{edges}\nDISCOVERED SITES\n{sites}"
    if section == "faction":
        return "FACTION MANAGEMENT\n" + "\n".join(
            [f"  {a.id}: {a.name} {a.skills}" for a in world.agents] +
            [f"  {r.id}: {r.label} x{r.quantity}, quality {r.quality} (passive until assigned)"
             for r in world.resources])
    if section == "politics":
        return ("GLOBAL POLITICS\nUN-centered hegemonic institutions versus emerging minor "
                "factions. Rival narratives of AGI, NHI and PSI.\n" +
                "\n".join(world.political_reactions or ["  No reported consequences yet."]))
    if section == "events":
        return "MISSIONS / RPG EVENTS\n" + "\n".join(
            f"  {o.id}: {o.label} [choices: {', '.join(o.approaches)}]"
            for o in world.operations if o.id not in world.completed
            and any(s.id == o.target_id and s.discovered for s in world.sites))
    raise ValueError("Unknown view")


def demo(seed: int = 338) -> str:
    world = sample_world()
    rng = Random(seed)
    report = [view(world, k) for k in ("map", "faction", "politics", "events")]
    for op, agent, asset, choice in (
        ("investigate_crash", "leader", "field", "protect witnesses"),
        ("archive_heist", "analyst", "cyber", "quiet access"),
    ):
        report.append(str(world.perform(op, agent, asset, choice, die=rng.randint(1, 6))["summary"]))
    report.append(view(world, "politics"))
    return "\n\n".join(report)


if __name__ == "__main__":
    print(demo())
