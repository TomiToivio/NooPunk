"""The RPG-relationship–to–strategic-consequence **seam** — signatures only, no rules.

Issue #323 asks that important NPC relationships and triggered RPG choices *"change concrete strategy
state, not only dialogue"*. Two separate rulings bear on that, and the seam exists precisely because
they are separate:

* Issue **#389** approves the **RPG layer's** rules basis (Fate Core). The mechanics themselves live in
  ``strategy_game/rpg/`` under that unit, and this module implements **none** of them and imports
  **nothing** from that package.
* The **strategy** and **political-simulation** layers are still unapproved:
  ``strategy_game/RULEBOOK.md`` says **NO RULES APPROVED**. So what a relationship *changes* on the
  strategic side — a modifier, a legality gate, a cost — is a rule the author has not given, and an
  agent must not invent it (``AGENTS.md`` §1, §4).

This module therefore declares the **boundary** between the two layers and nothing else, in the spirit
of ``strategy_game/ports.py``:

* :class:`RPGRelationshipSource` is a **signature-only** :class:`typing.Protocol` — the one way the
  strategic layer is allowed to *read* the personal state the RPG layer owns. It carries no
  implementation, no transition and no effect.
* :class:`NullRelationshipSource` is the default source: it declares nothing. Its emptiness is
  **UNMODELLED, never zero** — the relationship record is sparse, so two records with no authored tie
  are simply not represented (``docs/LEADER_COUNCIL_SYSTEM.md`` §5). Nothing may be read from absence.
* :func:`strategic_consequence_view` **reuses** ``CouncilModel.strategic_consequences`` rather than
  re-implementing it, and attaches the seam's metadata: ``applied: false`` and the owner of the
  mechanics. Nothing is computed but a lookup, and nothing is applied.

The seam is the structure that makes the author's remaining decision *expressible*: once a ruling
exists about what a tie changes, it has a declared slot to land in. Until then it lands nowhere.
"""
from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable

from .council import CouncilModel, MissionDeclaration
from .relationships import RelationshipSet

__all__ = [
    "APPLIED",
    "MECHANICS_OWNER",
    "SEAM_ID",
    "SEAM_METHODS",
    "NullRelationshipSource",
    "RPGRelationshipSource",
    "strategic_consequence_view",
]

#: The seam's identifier, so a reading can name where it came from.
SEAM_ID = "rpg_relationship_to_strategic_consequence"

#: Where the mechanics live. This module implements none of them.
MECHANICS_OWNER = "strategy_game/rpg (issue #389, the Fate Core RPG layer)"

#: Whether any consequence is applied by this seam. It never is: the seam only reads.
APPLIED = False

#: The methods the seam declares. Signature-only: a source supplies state, it does not resolve it.
SEAM_METHODS: tuple[str, ...] = ("relationship_states", "declared_edge_ids")


@runtime_checkable
class RPGRelationshipSource(Protocol):
    """Signature-only. A source of the personal state the strategic layer *reads*.

    A source answers two read-only questions about one record: which named states its ties currently
    carry, and which edge identifiers are declared for it. It resolves nothing, transitions nothing
    and grants nothing — the mechanics that would turn a state into a strategic effect belong to the
    RPG layer (#389) and to the author's unauthored strategy rulings, not to this boundary.
    """

    def relationship_states(self, owner_id: str) -> Mapping[str, str]:
        """The named state of each declared tie held by ``owner_id``. Empty means UNMODELLED."""
        ...

    def declared_edge_ids(self, owner_id: str) -> tuple[str, ...]:
        """The edge identifiers declared for ``owner_id``. Read as names, never followed as a rule."""
        ...


class NullRelationshipSource:
    """The default source: it declares nothing, and says so rather than answering with a number.

    An empty mapping is the honest answer when no authored tie exists — the relationship record is
    sparse, so absence is *unmodelled*, not a neutral-zero edge in a complete graph. A caller that
    reads a magnitude out of this source is reading a rule that was never approved.
    """

    def relationship_states(self, owner_id: str) -> Mapping[str, str]:
        return {}

    def declared_edge_ids(self, owner_id: str) -> tuple[str, ...]:
        return ()


def strategic_consequence_view(
    council: CouncilModel,
    mission: MissionDeclaration,
    edges: RelationshipSet,
    *,
    source: RPGRelationshipSource | None = None,
) -> dict[str, Any]:
    """What the relationship record has to say about a mission, plus the seam's metadata.

    Delegates the reading to :meth:`CouncilModel.strategic_consequences` — the council layer owns it,
    and this seam must not be a second implementation of it — and adds ``applied``, ``seam``,
    ``mechanics_owner`` and the source's own read. It mutates nothing and applies nothing.
    """
    reading = council.strategic_consequences(mission, edges)
    resolved_source = source if source is not None else NullRelationshipSource()
    reading["seam"] = SEAM_ID
    reading["applied"] = APPLIED
    reading["mechanics_owner"] = MECHANICS_OWNER
    reading["source_states"] = dict(resolved_source.relationship_states(mission.leader_id))
    reading["source_edge_ids"] = list(resolved_source.declared_edge_ids(mission.leader_id))
    return reading
