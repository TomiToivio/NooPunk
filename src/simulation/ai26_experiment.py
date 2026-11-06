"""Paired synthetic contestation experiment. Run with python -m src.simulation.ai26_experiment."""
import argparse
from collections import Counter
import hashlib
import json
import random

from .ai26_input import read_relations
from .events import Event


def trial(seed, probability, population, turns, claims):
    """Compare two organizations competing for affiliations under a contact budget."""
    if population < 2 or turns < 1 or not 0 <= probability <= 1 or len(claims) != 2:
        raise ValueError("Need two projects, two or more members and positive duration")
    rng = random.Random(seed)
    organizations = ["institution:A", "institution:B"]
    members = [f"member:{i}" for i in range(population)]
    affiliation = {m: organizations[i % 2] for i, m in enumerate(members)}
    initial = affiliation.copy()
    events = []
    snapshots = []
    reached = set()
    contacts = Counter()
    run = hashlib.sha256(json.dumps([seed, probability, population, turns, claims]).encode()).hexdigest()

    def emit(turn, actor, target, action, rule, claim):
        event = Event.create(simulation_id=run, turn=turn, actor=actor, target=target,
                             action_type=action, content=json.dumps({"rule": rule, "claim": claim}),
                             source="system", synthetic=True)
        events.append(event.to_dict())

    for turn in range(1, turns + 1):
        sender = organizations[(turn - 1) % 2]
        recipient = rng.choice(members)
        draw = rng.random()
        claim = claims[organizations.index(sender)]
        emit(turn, sender, recipient, "communicate", "alternating institutional outreach", claim)
        reached.add(recipient)
        contacts[recipient] += 1
        if affiliation[recipient] != sender and draw < probability:
            emit(turn, recipient, affiliation[recipient], "disaffiliate", "accepted competing claim", claim)
            affiliation[recipient] = sender
            emit(turn, recipient, sender, "affiliate", "accepted competing claim", claim)
        snapshots.append({"turn": turn, "member_of": affiliation.copy(),
                          "communication_event": next(e["event_id"] for e in reversed(events)
                                                      if e["action_type"] == "communicate"),
                          "reach_fraction": len(reached) / population,
                          "coalition_sizes": {org: list(affiliation.values()).count(org) for org in organizations}})
    return {"origin": "simulated", "seed": seed, "switch_probability": probability,
            "turns": turns, "claims": claims, "organizations": organizations,
            "initial_affiliations": initial, "events": events, "snapshots": snapshots,
            "incoming_contacts": {m: contacts[m] for m in members}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical", help="One reviewed canonical JSON record")
    parser.add_argument("--relation", nargs=2, help="Two distinct researcher-selected competing relation IDs")
    parser.add_argument("--population", type=int, default=12)
    parser.add_argument("--turns", type=int, default=24)
    parser.add_argument("--seeds", nargs="+", type=int, default=[1, 2, 3])
    args = parser.parse_args()
    if bool(args.canonical) != bool(args.relation):
        parser.error("Supply both --canonical and --relation")
    context = read_relations(args.canonical) if args.canonical else None
    claims = args.relation or ["fixture:AI-public-control", "fixture:AI-private-control"]
    if context:
        available = {r["relation_id"] for r in context["relations"]}
        if len(set(claims)) != 2 or not set(claims) <= available:
            parser.error("Select two different reviewed relations from this record")
    runs = [trial(seed, p, args.population, args.turns, claims)
            for seed in args.seeds for p in (0.0, 0.25, 0.75)]
    print(json.dumps({"schema": "ai26-contestation/1", "research_context": context,
                      "claim_origin": "inferred" if context else "synthesized",
                      "runs": runs}, sort_keys=True))


if __name__ == "__main__":
    main()
