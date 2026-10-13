"""Model-free demonstration of the #304 boundary: ``python -m strategy_game.controllers``.

Prints one deterministic JSON payload showing that the proposal/recording loop works **with no
provider, no model, no network and no database** -- the whole point of landing this boundary before
any Ollama/Concordia adapter. It records exactly one declaration per leader for a scripted
controller, replays the log, and reports that the replay is exact.

Nothing in it is canon and nothing in it is a rule: the labels are examples, the action codes are
open strings (no action set is approved), and no proposal is compared, spent or applied. The
authoritative world state is printed before *and* after recording so the output itself shows the
state did not move.
"""
from __future__ import annotations

import json
from typing import Any

from ..core import Faction, Leader, WorldState
from .controllers import (
    NullAgentProvider,
    ScriptedAgentProvider,
    ScriptedMove,
    available_controller_adapters,
    controller_from_adapter,
    registry_for,
)
from .proposals import PENDING_AUTHOR_RULINGS, ProposalRecorder


def demo() -> dict[str, Any]:
    """A minimal, illustrative, deterministic round. Not a scenario and not canon."""
    world = WorldState(
        leaders=[
            Leader("leader-one", "First illustrative leader"),
            Leader("leader-two", "Second illustrative leader"),
        ],
        factions=[
            Faction("faction-one", "First illustrative faction", "leader-one"),
            Faction("faction-two", "Second illustrative faction", "leader-two"),
        ],
    )

    null = NullAgentProvider("null")
    scripted = ScriptedAgentProvider(
        "scripted-example",
        script=(
            ScriptedMove("leader-one", "example-action-a", target_id="faction-two",
                         rationale="Illustrative declaration; no action set is approved."),
            ScriptedMove("leader-two", "example-action-b",
                         resources=("example-resource",),
                         rationale="Illustrative declaration; nothing is spent."),
        ),
    )

    registry = registry_for((null, scripted))
    recorder = ProposalRecorder(registry)

    before = world.to_json()
    # One declaration per leader, from the controller that commands it.
    null_proposals = [
        null.propose(world, leader_id="leader-one"),
        null.propose(world, leader_id="leader-two"),
    ]
    for leader_id in scripted.leaders():
        proposal = scripted.propose(world, leader_id=leader_id)
        if proposal is not None:
            recorder.record(proposal)
    after = world.to_json()

    replayed = recorder.replay()
    return {
        "controllers": {
            "null": {"leaders": list(registry.leaders_of(null.controller_id))},
            "scripted-example": {"leaders": list(registry.leaders_of(scripted.controller_id))},
        },
        "null_proposals": null_proposals,
        "recorded": [proposal.to_dict() for proposal in recorder.entries],
        "replay_matches_record": [p.to_dict() for p in replayed]
        == [p.to_dict() for p in recorder.entries],
        "world_state_unchanged_by_recording": before == after,
        "optional_adapters": available_controller_adapters(),
        "adapter_controllers": {
            name: _adapter_status(name) for name in available_controller_adapters()
        },
        "pending_author_rulings": list(PENDING_AUTHOR_RULINGS),
    }


def _adapter_status(name: str) -> str:
    """Report the seam without ever importing: absent, or present-but-refused."""
    try:
        controller = controller_from_adapter(name)
    except NotImplementedError:
        return "present but not implemented here (later, author-gated step)"
    return "absent" if controller is None else "available"


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2, sort_keys=True))
