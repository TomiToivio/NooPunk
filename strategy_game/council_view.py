"""Read-only faction council assignment board for the strategy MVP (#323).

Shows leadership, portfolios, missions and declared statuses. No turn resolution,
mission permissions, numerical bonuses, AI choices or state mutations.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .council import Council, CouncilModel


def assignment_rows(council: Council) -> tuple[dict[str, str], ...]:
    """One display row per actual leader; keep skips visible and distinct from actions."""
    assignments: dict[str, list[object]] = {}
    for mission in council.missions:
        assignments.setdefault(mission.leader_id, []).append(mission)
    rows = []
    for leader in council.leaders:
        missions = assignments.get(leader.identifier, [])
        rows.append({
            "leader_id": leader.identifier,
            "name": leader.name or leader.identifier,
            "portfolio": leader.portfolio or "unassigned",
            "status": leader.status or "available",
            "location": leader.location_id or "unspecified",
            "assignment": ", ".join(
                f"{m.identifier} ({m.kind or 'unspecified'} at {m.location_id or 'unspecified'}: "
                f"{m.target_id or 'unspecified'})" for m in missions
            ) if missions else "no active mission",
        })
    return tuple(rows)


def render_assignment_board(council: Council, model: CouncilModel) -> str:
    """Text-only God's-eye view; report invalid declarations rather than hiding them."""
    lines = [f"Council: {council.identifier}", "Leaders and declared missions:"]
    for row in assignment_rows(council):
        lines.append(
            f"- {row['name']} [{row['leader_id']}] | portfolio: {row['portfolio']} | "
            f"status: {row['status']} | location: {row['location']} | {row['assignment']}"
        )
    problems = model.structural_problems(council)
    if problems:
        lines.append("Declaration warnings:")
        lines.extend(f"- {problem}" for problem in problems)
    lines.append("Unpursued priorities: " + ", ".join(model.unpursued_quantities(council)))
    lines.append("All missions are declarations only; no outcomes or passive bonuses applied.")
    return "\n".join(lines)
