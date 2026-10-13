"""The six quantities that must stay distinct (issues #323/#338; ``docs/design/NOOPUNK_GLOBAL.md`` §7).

§7 is the acceptance criterion of the global design record: **opinion/support**, **organizational
membership/resources**, **legislative representation**, **office and government control**,
**institutional access** and **Laclauian discursive hegemony** are six different things, kept in six
different fields with six different component conventions, and **none is interchangeable**. The
document's own explicit non-identities are the reason a single "influence" scalar is refused: a
faction can hold support and lose seats, win seats and not hold office, have a huge membership and no
access, or hold the nodal signifier and lose everything else.

Why the council layer needs this module at all. Issue #323 caps a faction at four leader-led active
moves per turn, and §7 says the six quantities cannot be reduced to one another. Four moves against
six non-identical things means a faction **cannot pursue all of its priorities in a turn**, and that
scarcity — not decoration — is what makes four offices an argument. The mission layer therefore has
to be able to name *which* quantity a move tries to move, and this module is that vocabulary.

Named positions only. Every entry below is a **name** transcribed from §7's table. Nothing here
attaches a value, a weight, a component convention, a range or a derived score to any quantity, and
:func:`unknown_quantities` reports a name it does not know rather than inventing one. "Influence +1"
would collapse exactly the distinctions the criterion exists to preserve, so no such arithmetic exists
in this package.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

__all__ = [
    "QUANTITIES",
    "QUANTITY_IDS",
    "Quantity",
    "quantity",
    "quantity_ids",
    "unknown_quantities",
]


@dataclass(frozen=True)
class Quantity:
    """One of §7's six. ``is_not`` and ``home_in_model`` are §7's own columns, transcribed."""

    identifier: str
    label: str
    is_not: str
    home_in_model: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.identifier,
            "label": self.label,
            "is_not": self.is_not,
            "home_in_model": self.home_in_model,
        }


#: §7's table, in the document's order. The ids are this module's slugs of §7's labels; the labels
#: are the document's. Six entries, no more and no fewer.
QUANTITIES: tuple[Quantity, ...] = (
    Quantity(
        identifier="opinion_support",
        label="opinion / support",
        is_not="not membership; not seats; not hegemony",
        home_in_model="the jurisdiction's own support markers, kept localised",
    ),
    Quantity(
        identifier="membership_resources",
        label="organizational membership / resources",
        is_not="does not buy extra actions: it amplifies a leader-led mission",
        home_in_model="the faction's own pool and tableau",
    ),
    Quantity(
        identifier="legislative_representation",
        label="legislative representation",
        is_not="not opinion; not office",
        home_in_model="seat markers per chamber and jurisdiction",
    ),
    Quantity(
        identifier="office_control",
        label="office and government control",
        is_not="not seats; not access",
        home_in_model="office markers on board slots",
    ),
    Quantity(
        identifier="institutional_access",
        label="institutional access",
        is_not="not ownership of a function system; not seats; not hegemony",
        home_in_model="access tokens attached to institution-interface cards",
    ),
    Quantity(
        identifier="discursive_hegemony",
        label="Laclauian discursive hegemony",
        is_not="not a scalar; not ownership; not popularity; not control",
        home_in_model="the articulation graph itself",
    ),
)

#: The six ids, in §7's order.
QUANTITY_IDS: tuple[str, ...] = tuple(quantity.identifier for quantity in QUANTITIES)

_BY_ID: dict[str, Quantity] = {quantity.identifier: quantity for quantity in QUANTITIES}


def quantity(identifier: str) -> Quantity:
    """The quantity with this id, or :class:`KeyError` — an unknown name is never invented."""
    return _BY_ID[identifier]


def quantity_ids() -> tuple[str, ...]:
    """The six ids. Six distinct names, and deliberately nothing else."""
    return QUANTITY_IDS


def unknown_quantities(names: Iterable[str]) -> tuple[str, ...]:
    """The names in ``names`` that are not one of the six, in order, without raising."""
    return tuple(name for name in names if name not in _BY_ID)
