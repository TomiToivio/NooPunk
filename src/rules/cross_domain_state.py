"""Cross-domain state machine — the executable half of issue #225.

`rulebook/18_CROSS_DOMAIN_STATE.md` is the human-readable contract; this module is the
same contract as code, so the invariants can be *executed* rather than only read. It
adds no mechanics of its own: every constant here is one the chapter states.

**Status: PROVISIONAL, not canonical.** `IS_CANONICAL = False` and nothing in the shipped
`src/rules/core.py` check path imports this. Issue #225 asks for the contract and its
invariants; the author owns the calibration of every number. Marking the module
non-canonical is what keeps "provisional" from quietly becoming "shipped".

The three invariants worth executing, because prose cannot stop a later chapter
from breaking them:

* **Single locus.** One consciousness-instance acts in exactly one state at a time.
* **Reach is state-determined.** A non-embodied character cannot take a Physical
  action, however many AP are left.
* **No gateway, no crossing.** A realm-to-realm effect is impossible without a
  declared gateway, and its absence is not a modifier that a good roll can beat.
"""
from __future__ import annotations

from dataclasses import dataclass, field

#: PROVISIONAL. The author owns calibration; this module implements the proposal only.
IS_CANONICAL = False

# --------------------------------------------------------------------------- #
# The four states
# --------------------------------------------------------------------------- #

EMBODIED = "embodied"
CYBER_IMMERSED = "cyber-immersed"
ASTRAL_PROJECTED = "astral-projected"
INVOLUNTARY_DREAM_NDE = "involuntary-dream-nde"

STATES: tuple[str, ...] = (
    EMBODIED,
    CYBER_IMMERSED,
    ASTRAL_PROJECTED,
    INVOLUNTARY_DREAM_NDE,
)

#: States in which the character's body is *not* under the character's control.
#: These are exactly the states that expose the body (chapter: "Physical-body exposure").
PROJECTED_STATES: tuple[str, ...] = (
    CYBER_IMMERSED,
    ASTRAL_PROJECTED,
    INVOLUNTARY_DREAM_NDE,
)

#: The states a character may *choose* to leave. An involuntary state is not a choice,
#: which is why it is excluded here rather than given a special-case exit rule.
VOLUNTARY_EXIT_STATES: tuple[str, ...] = (EMBODIED, CYBER_IMMERSED, ASTRAL_PROJECTED)

# --------------------------------------------------------------------------- #
# Realms
# --------------------------------------------------------------------------- #

PHYSICAL = "physical"
SOCIAL = "social"
PSYCHIC = "psychic"
CYBERNETIC = "cybernetic"
NOOSPACE = "noospace"

REALMS: tuple[str, ...] = (PHYSICAL, SOCIAL, PSYCHIC, CYBERNETIC, NOOSPACE)

#: Which realms a consciousness may act in, given its state.
#:
#: Embodied covers the three spacetime realms — Physical, Social, and *local* Psychic
#: action. Local PSI is not projection, so it does not need Noöspace to act.
ALLOWED_REALMS: dict[str, frozenset[str]] = {
    EMBODIED: frozenset({PHYSICAL, SOCIAL, PSYCHIC}),
    CYBER_IMMERSED: frozenset({CYBERNETIC}),
    ASTRAL_PROJECTED: frozenset({NOOSPACE}),
    INVOLUNTARY_DREAM_NDE: frozenset({NOOSPACE}),
}

#: Legal transitions. Entering a state from another *ends* the old state — a transition,
#: never an addition — so the graph is a set of single edges, not a lattice.
#:
#: Every projected state returns to Embodied; every projected state may be entered from
#: Embodied. Crucially, there is **no direct edge between two projected states**: a
#: character cannot go from a dive straight into a projection without coming back to the
#: body first. Allowing that shortcut is how a single character would gain a second locus.
TRANSITIONS: dict[str, frozenset[str]] = {
    EMBODIED: frozenset({CYBER_IMMERSED, ASTRAL_PROJECTED, INVOLUNTARY_DREAM_NDE}),
    CYBER_IMMERSED: frozenset({EMBODIED}),
    ASTRAL_PROJECTED: frozenset({EMBODIED}),
    INVOLUNTARY_DREAM_NDE: frozenset({EMBODIED}),
}


class CrossDomainError(ValueError):
    """An invariant of the cross-domain contract was violated."""


def _require_state(state: str) -> str:
    if state not in STATES:
        raise CrossDomainError(f"unknown state: {state!r} (expected one of {STATES})")
    return state


def controls_body(state: str) -> bool:
    """True only while embodied. A projected body cannot be actively controlled."""
    return _require_state(state) == EMBODIED


def realms_for(state: str) -> frozenset[str]:
    """The realms a consciousness may act in, given its state."""
    return ALLOWED_REALMS[_require_state(state)]


def can_act_in(state: str, realm: str) -> bool:
    """The state-determined reach: no action in a realm the state does not reach.

    This is the executable form of *"you act in exactly one realm per exchange"* —
    a cyber-immersed character has no Physical reach even with AP unspent.
    """
    return realm in realms_for(state)


def assert_can_act_in(state: str, realm: str) -> None:
    if not can_act_in(state, realm):
        raise CrossDomainError(
            f"a {state} consciousness cannot act in the {realm} realm "
            f"(reachable: {sorted(realms_for(state))})"
        )


def legal_transition(source: str, target: str) -> bool:
    return target in TRANSITIONS[_require_state(source)]


def assert_transition(source: str, target: str) -> None:
    if not legal_transition(source, target):
        raise CrossDomainError(
            f"illegal transition {source} -> {target}: a projected state returns to "
            f"{EMBODIED} before another projected state can be entered"
        )


def single_locus(state: str) -> str:
    """The one state a consciousness-instance is in.

    Takes any number of candidate states and refuses more than one. Exists so a caller
    cannot model "a bit embodied and a bit immersed"; a fork is a *separate instance*,
    not a second locus for this one (chapter: single-locus rule, consequence 4).
    """
    if isinstance(state, (list, tuple, set, frozenset)):
        states = tuple(state)
        if len(states) != 1:
            raise CrossDomainError(
                f"a consciousness-instance has exactly one locus, got {len(states)}: {states}"
            )
        return _require_state(states[0])
    return _require_state(state)


# --------------------------------------------------------------------------- #
# The shared action economy
# --------------------------------------------------------------------------- #

#: PROVISIONAL. All actors spend from one clock, whatever realm they act in.
AP_PER_EXCHANGE = 3

#: PROVISIONAL action costs, from the chapter's action table.
AP_COSTS: dict[str, int] = {
    "act": 1,
    "move": 1,
    "prepare": 1,
    "cover": 1,
    "react": 1,
    "exit": 1,
}


@dataclass
class ActionEconomy:
    """One actor's AP for one exchange, plus reaction debt carried into the next.

    Held AP expires with the exchange; a reaction may borrow from the next one, which
    is what makes reacting repeatedly a real cost rather than a free upgrade.
    """

    ap_per_exchange: int = AP_PER_EXCHANGE
    spent: int = 0
    held: int = 0
    debt: int = 0
    actions: list[str] = field(default_factory=list)

    def reset_for_exchange(self) -> None:
        """Start a new exchange: held AP expires, and last exchange's debt is paid."""
        self.spent = self.debt
        self.held = 0
        self.debt = 0
        self.actions = []

    @property
    def remaining(self) -> int:
        return self.ap_per_exchange - self.spent

    def spend(self, action: str) -> None:
        cost = AP_COSTS.get(action)
        if cost is None:
            raise CrossDomainError(f"unknown action: {action!r} (expected one of {tuple(AP_COSTS)})")
        if cost > self.remaining:
            raise CrossDomainError(
                f"cannot afford {action!r}: {self.remaining} AP left of {self.ap_per_exchange}"
            )
        self.spent += cost
        self.actions.append(action)

    def hold(self) -> None:
        """Reserve one AP for a reaction. Held AP does not survive the exchange."""
        if self.remaining - self.held <= 0:
            raise CrossDomainError("no unspent AP left to hold")
        self.held += 1

    def react(self) -> None:
        """Spend a held AP, or borrow from the next exchange. Never free."""
        if self.held > 0:
            self.held -= 1
        else:
            self.debt += AP_COSTS["react"]
        self.actions.append("react")


# --------------------------------------------------------------------------- #
# Gateways: effects crossing realms
# --------------------------------------------------------------------------- #

#: The gateway that must exist for a crossing, keyed by (from, to). A crossing with no
#: entry is *impossible* — not merely hard — which is why the mapping is sparse.
GATEWAY_REQUIRED: dict[tuple[str, str], str] = {
    (CYBERNETIC, PSYCHIC): "an actual vulnerable connected neural path",
    (PHYSICAL, CYBERNETIC): "physical access to the device or its network",
    (NOOSPACE, PHYSICAL): "a noetic anchor or resonance",
}

#: (from, to) pairs that are *known impossible*: no general gateway exists. Listing them
#: explicitly keeps a later chapter from inventing one by omission.
NO_GATEWAY_EXISTS: frozenset[tuple[str, str]] = frozenset(
    {
        (NOOSPACE, CYBERNETIC),
        (CYBERNETIC, NOOSPACE),
    }
)


def gateway_for(source_realm: str, target_realm: str) -> str | None:
    """The required gateway, or None when the crossing has none and cannot be made."""
    if source_realm == target_realm:
        return None
    if (source_realm, target_realm) in NO_GATEWAY_EXISTS:
        return None
    return GATEWAY_REQUIRED.get((source_realm, target_realm))


def can_cross(source_realm: str, target_realm: str, *, has_gateway: bool) -> bool:
    """Cross-realm reach. Same realm needs nothing; otherwise a gateway is required.

    A missing gateway is a *precondition*, not a penalty: `has_gateway=False` is False
    regardless of any other input, which is the executable form of "no realm reaches
    another without a declared gateway".
    """
    if source_realm == target_realm:
        return True
    if (source_realm, target_realm) in NO_GATEWAY_EXISTS:
        return False
    if (source_realm, target_realm) not in GATEWAY_REQUIRED:
        return False
    return bool(has_gateway)
