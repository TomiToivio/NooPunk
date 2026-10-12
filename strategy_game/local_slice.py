"""Isolated, provisional local strategy vertical slice (#322/#323/#324).

No change to the unapproved main strategy rulebook or legacy RPG.
All mechanics are small deterministic *playtest assumptions*, not validated social theory.
"""
from __future__ import annotations

import json
import random
from dataclasses import dataclass, field, asdict
from pathlib import Path

PORTFOLIOS = ("politics", "networks", "operations", "research")
MISSIONS = ("campaign", "organize", "negotiate", "adopt_technology", "investigate", "rest")
DATA = Path(__file__).with_name("data") / "ukweli_local.json"


@dataclass
class Leader:
    id: str
    name: str
    faction: str
    location: str
    portfolio: str
    skill: int = 2
    status: str = "ready"
    traits: list[str] = field(default_factory=list)


@dataclass
class Party:
    id: str
    name: str
    leader_ids: list[str]
    treasury: int = 8
    legitimacy: int = 5
    network: int = 2
    technology: int = 0
    claims: list[str] = field(default_factory=list)


@dataclass
class Relationship:
    a: str
    b: str
    trust: int = 0
    tags: list[str] = field(default_factory=list)


@dataclass
class Mission:
    leader: str
    kind: str
    location: str
    target: str = ""
    cost: int = 0


@dataclass
class Game:
    locations: list[dict]
    routes: list[list[str]]
    parties: list[Party]
    leaders: list[Leader]
    relations: list[Relationship]
    shocks: list[dict]
    turn: int = 0
    history: list[dict] = field(default_factory=list)
    support: dict[str, dict[str, int]] = field(default_factory=dict)

    @classmethod
    def from_scenario(cls, path: Path = DATA) -> "Game":
        data = json.loads(path.read_text(encoding="utf-8"))
        game = cls(
            locations=data["locations"], routes=data["routes"],
            parties=[Party(**p) for p in data["parties"]],
            leaders=[Leader(**x) for x in data["leaders"]],
            relations=[Relationship(**x) for x in data["relationships"]],
            shocks=data["shocks"],
            support={loc["id"]: {p["id"]: 2 for p in data["parties"]}
                     for loc in data["locations"]},
        )
        game.validate()
        return game

    def validate(self) -> None:
        places = {x["id"] for x in self.locations}
        assert 5 <= len(places) <= 8
        assert len(places) == len(self.locations)
        ids = [l.id for l in self.leaders]
        assert len(ids) == len(set(ids))
        for p in self.parties:
            assert len(p.leader_ids) == 4 and len(set(p.leader_ids)) == 4
            assert {l.id for l in self.leaders if l.faction == p.id} == set(p.leader_ids)
        for l in self.leaders:
            assert l.location in places and l.portfolio in PORTFOLIOS
        for route in self.routes:
            assert len(route) == 2 and set(route) <= places

    def _relation(self, a: str, b: str) -> int:
        return next((r.trust for r in self.relations if {r.a, r.b} == {a, b}), 0)

    def reassign(self, leader_id: str, portfolio: str) -> None:
        if portfolio not in PORTFOLIOS:
            raise ValueError("invalid portfolio")
        next(l for l in self.leaders if l.id == leader_id).portfolio = portfolio

    def step(self, orders: list[Mission], *, seed: int = 0) -> dict:
        self.validate()
        known = {l.id: l for l in self.leaders}
        place_ids = {p["id"] for p in self.locations}
        party = {p.id: p for p in self.parties}
        seen: set[str] = set()
        # Validate *all* orders before applying state changes.
        for m in orders:
            if m.leader not in known or m.leader in seen:
                raise ValueError("unknown or double-booked leader")
            leader = known[m.leader]
            if leader.status != "ready" or m.kind not in MISSIONS:
                raise ValueError("unavailable leader or invalid mission")
            if m.location not in place_ids or m.cost < 0:
                raise ValueError("invalid location or cost")
            if m.location != leader.location and sorted([m.location, leader.location]) not in [
                    sorted(r) for r in self.routes]:
                raise ValueError("location not reachable within one turn")
            if m.kind == "negotiate" and m.target not in known:
                raise ValueError("negotiation requires known target")
            seen.add(m.leader)
        costs: dict[str, int] = {}
        for m in orders:
            faction = known[m.leader].faction
            costs[faction] = costs.get(faction, 0) + m.cost
        if any(party[k].treasury < c for k, c in costs.items()):
            raise ValueError("insufficient funds")
        rng = random.Random(f"{seed}:{self.turn}")
        shock = self.shocks[self.turn % len(self.shocks)]
        report = {"turn": self.turn + 1, "shock": shock["title"], "actions": [],
                  "portfolios": [], "character_event": None}
        # Passive management occurs whether or not a leader takes a mission.
        for l in self.leaders:
            if l.status != "ready":
                continue
            p = party[l.faction]
            if l.portfolio == "operations":
                p.treasury += 1
                effect = "treasury+1"
            elif l.portfolio == "networks":
                p.network = min(10, p.network + 1)
                effect = "network+1"
            elif l.portfolio == "politics":
                p.legitimacy = min(10, p.legitimacy + 1)
                effect = "legitimacy+1"
            else:
                effect = "research capacity (mission bonus)"
            report["portfolios"].append(f"{l.name}: {effect}")
        for p in self.parties:
            p.legitimacy = max(0, min(10, p.legitimacy + shock.get("legitimacy_delta", 0)))
        for m in sorted(orders, key=lambda x: x.leader):
            l = known[m.leader]
            p = party[l.faction]
            p.treasury -= m.cost
            travel = int(m.location != l.location)
            location = next(x for x in self.locations if x["id"] == m.location)
            relation = self._relation(l.id, m.target) if m.target else 0
            bonus = (p.network // 3 if m.kind == "organize" else
                     relation // 2 if m.kind == "negotiate" else
                     1 if m.kind == "adopt_technology" and l.portfolio == "research" else 0)
            roll = rng.randint(1, 6) + l.skill + bonus - travel - location["pressure"]
            success = m.kind == "rest" or roll >= 5
            if success:
                if m.kind == "campaign":
                    self.support[m.location][p.id] += 2
                elif m.kind == "organize":
                    p.network = min(10, p.network + 1)
                    self.support[m.location][p.id] += 1
                elif m.kind == "negotiate":
                    p.legitimacy = min(10, p.legitimacy + 1)
                elif m.kind == "adopt_technology":
                    p.technology += 1  # adoption, not global invention
                elif m.kind == "investigate":
                    p.network = min(10, p.network + 1)
                elif m.kind == "rest":
                    p.treasury += 1
            l.location = m.location
            report["actions"].append({"leader": l.name, "faction": p.id,
                                      "mission": m.kind, "location": m.location,
                                      "roll": roll, "success": success})
        # At most one sparse relationship choice in the whole game per turn.
        if self.turn % 4 == 2 and self.relations:
            relation = self.relations[0]
            relation.trust = max(-3, min(3, relation.trust + 1))
            report["character_event"] = {"choice": "share evidence",
                                         "actors": [relation.a, relation.b],
                                         "trust_after": relation.trust}
        self.turn += 1
        self.history.append(report)
        return report

    def snapshot(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)


def play(turns: int = 12, seed: int = 2027) -> Game:
    game = Game.from_scenario()
    for index in range(turns):
        orders = []
        for party in game.parties:
            for i, leader_id in enumerate(party.leader_ids):
                l = next(x for x in game.leaders if x.id == leader_id)
                # Each named character has one action; rival factions obey same rules.
                orders.append(Mission(leader_id, ("campaign", "organize",
                              "adopt_technology", "rest")[i], l.location, cost=0))
        game.step(orders, seed=seed)
    return game


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--turns", type=int, default=12)
    parser.add_argument("--seed", type=int, default=2027)
    args = parser.parse_args()
    print(play(args.turns, args.seed).snapshot())
