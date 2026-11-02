"""Load and read the seeded discourse in game (#1042).

`ideology.py` owns the model and refuses to collapse its layers; this module only moves data into it,
persists it on a character, and renders what a recruit is allowed to read.

Nothing here invents a stance: the seed file carries authored statements, and the render shows which
of them are evidence-backed and which are not. A rumour repeated is still a rumour.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nopunk_mud.ideology import Actor, Concept, Discourse, IdeologyError, Relationship, Statement

SEED_PATH = Path(__file__).resolve().parents[2] / "data" / "world" / "ideology_seed_1042.json"


def seed_discourse(path: Path | None = None) -> Discourse:
    payload = json.loads((path or SEED_PATH).read_text(encoding="utf-8"))
    discourse = Discourse()
    for concept in payload.get("concepts", []):
        discourse.add_concept(Concept(**concept))
    for actor in payload.get("actors", []):
        discourse.add_actor(Actor(**actor))
    for statement in payload.get("statements", []):
        discourse.articulate(Statement(**statement))
    for relationship in payload.get("relationships", []):
        discourse.relate(Relationship(**relationship))
    return discourse


def viewer_scope(path: Path | None = None) -> str:
    payload = json.loads((path or SEED_PATH).read_text(encoding="utf-8"))
    return str(payload.get("viewer_scope") or "")


def discourse_for(store) -> Discourse:
    """This character's discourse, seeded once and persisted after that."""
    raw = getattr(store.db, "discourse", None)
    if raw:
        return Discourse.from_dict(dict(raw))
    discourse = seed_discourse()
    store.db.discourse = discourse.to_dict()
    return discourse


def _stances(row: dict[str, int]) -> str:
    if not row:
        return "no recorded position"
    return ", ".join(f"{concept} {'+' if value > 0 else '-'}{abs(value)}" for concept, value in row.items())


def render_actor(discourse: Discourse, name: str, *, scope: str = "", evidence_only: bool = False) -> str:
    """One actor: what they said, where that puts them, who they actually know."""
    scope = scope or viewer_scope()
    try:
        actor_id = _resolve(discourse, name)
    except IdeologyError as exc:
        return f"{exc}. Use 'dossier' for the list."

    visible = discourse.visible(scope, shares_secret=True)
    said = [s for s in visible if s.actor == actor_id]
    if evidence_only:
        said = [s for s in said if s.is_evidence_backed]

    lines = [f"{actor_id} ({discourse.actors[actor_id].kind}, scope {discourse.actors[actor_id].scope})"]
    if said:
        lines.append("  said:")
        for statement in said:
            backing = "evidence" if statement.is_evidence_backed else "NOT evidence"
            lines.append(
                f"    {statement.concept}: {statement.stance} — \"{statement.demand}\" "
                f"[{statement.evidence}, {backing}, {statement.visibility}]"
            )
    else:
        lines.append("  said: nothing you are cleared to know")

    all_positions = discourse.positions().get(actor_id, {})
    evidence_positions = discourse.positions(evidence_only=True).get(actor_id, {})
    lines.append(f"  positions (all claims):     {_stances(all_positions)}")
    lines.append(f"  positions (evidence only):  {_stances(evidence_positions)}")

    known = [r for r in discourse.relationships if actor_id in (r.a, r.b) and r.visibility != "secret"]
    hidden = [
        r for r in discourse.relationships if actor_id in (r.a, r.b) and r.visibility == "secret"
    ]
    ties = [
        f"    {r.b if r.a == actor_id else r.a}: trust {r.trust:+d}"
        + (f", debt: {r.debt}" if r.debt else "")
        + f" [{r.visibility}]"
        for r in known
    ]
    lines.append("  relationships: " + ("none on record" if not ties else ""))
    lines.extend(ties)
    if hidden:
        lines.append(f"  relationships withheld: {len(hidden)} you are not cleared for")
    return "\n".join(line for line in lines if line != "")


def render_overview(discourse: Discourse, *, scope: str = "") -> str:
    """The whole board: who is on record, and which signifiers are actually contested."""
    lines = ["On record:"]
    for actor in sorted(discourse.actors.values(), key=lambda a: a.id):
        lines.append(f"  {actor.id} ({actor.kind})")
    contested = discourse.contested_concepts()
    if contested:
        lines.append("Contested signifiers:")
        for concept, sides in contested.items():
            lines.append(
                f"  {concept}: for {', '.join(sides['support']) or '-'} / against "
                f"{', '.join(sides['oppose']) or '-'}"
            )
    else:
        lines.append("Contested signifiers: none — nobody disagrees on record yet")
    return "\n".join(lines)


def render_pair(discourse: Discourse, left: str, right: str) -> str:
    """Agreement and trust, side by side, because they are different questions."""
    try:
        a = _resolve(discourse, left)
        b = _resolve(discourse, right)
    except IdeologyError as exc:
        return f"{exc}."
    verdict: dict[str, Any] = discourse.antagonists_are_not_enemies(a, b)
    return (
        f"{a} vs {b}: ideological overlap {verdict.get('overlap')} signifier(s); "
        f"personal trust {verdict.get('trust')}. These do not imply each other."
    )


def _resolve(discourse: Discourse, name: str) -> str:
    wanted = name.strip().casefold()
    hits = [actor_id for actor_id in discourse.actors if actor_id.casefold() == wanted]
    if not hits:
        raise IdeologyError(f"nobody called {name!r} is on record")
    return hits[0]
