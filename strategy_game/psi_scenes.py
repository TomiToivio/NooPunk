"""Two PSI prototypes (issue #345, acceptance criterion 3).

Issue #345's third criterion asks to *"prototype one everyday subtle PSI encounter and one
institutionalized commercial PSI / counter-PSI investigation"*. Both live here, built on the **existing**
Fate engine (``rpg.fate``) and the **existing** PSI seam (``psi_operations``). No second resolution
mechanic, no new vocabulary, no new power.

Why this module sits in ``strategy_game`` rather than ``rpg``
------------------------------------------------------------

The RPG layer is the foundation and the strategy layer consumes it, so the import runs
``strategy_game -> rpg`` and never the reverse. Placing these scenes under ``rpg/`` would have made the
foundation depend on the strategy package and broken the layer boundary that
``strategy_game/tests/test_rpg_boundary.py`` enforces. Location ids are taken from the canonical eight
Ukweli nodes validated by ``map_spec``, so the scenes play in real declared geography.

The fiction this respects
-------------------------

Per #345, **PSI is established mainstream science in NoöPunk**: the mystery is never *whether* PSI
exists, but *which mechanisms, entities and institutions* are involved, who benefits, and what follows.
So nothing here frames PSI as unproven, nothing is a spell, and the most consequential move available
is not a stronger power but a **counter-PSI specialist denying access**. The register is PKD's quotidian
surrealism: unsettling ordinary interactions, deadpan paperwork, and an answer to the client that may
have to be "nothing you can act on".
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Mapping

from .psi_operations import PsiFinding, PsiOperation, PsiOperationLedger
from .rpg import fate
from .rpg.fate import Action, Character, Resolution, skill_check

__all__ = [
    "EVERYDAY_ANOMALIES",
    "CANONICAL_LOCATIONS",
    "EverydayEncounter",
    "everyday_psi_encounter",
    "commercial_counter_psi_investigation",
]

#: The canonical playable nodes from the local scenario map (see map_spec). The scenes play here.
CANONICAL_LOCATIONS: tuple[str, ...] = (
    "civic", "old_harbor", "residential", "campus",
    "port", "outer_island", "airfield_island", "coast",
)

#: The everyday register: unsettling *ordinary* things, not phenomena. Deliberately administrative.
EVERYDAY_ANOMALIES: tuple[str, ...] = (
    "the vending machine dispensed your order before you chose it",
    "the tram announcement apologised for a delay that had not happened yet",
    "a colleague finished your sentence, then asked you to start over",
    "the delivery notice had been signed in your handwriting",
    "the queue parted exactly where you were about to stand",
    "the advert on the platform knew the complaint you had filed that morning",
)


@dataclass(frozen=True)
class EverydayEncounter:
    """One unremarkable day with one unremarkable anomaly. Nothing here proves anything."""

    anomaly: str
    witness: str
    noticing: Resolution
    resistance: Resolution
    what_it_does_not_prove: str


def everyday_psi_encounter(seed: int = 11) -> EverydayEncounter:
    """A routine errand in which something ordinary is quietly wrong.

    Two checks, both plain Fate: **Notice** to catch it at all, and **Will** to decline the nudge. The
    character is not amazed -- PSI is established science and the paperwork for it exists -- which is the
    point: the horror is administrative, not supernatural.
    """
    rng = Random(seed)
    commuter = Character(
        id="everyday-commuter", name="Commuter",
        aspects=["Twenty Years on This Route", "Nothing Notable Ever Happens to Me"],
        skills={"Notice": 2, "Will": 1, "Psi": 0},
        gear=["Season ticket", "Phone with the mandatory PSI-consent settings on"],
        natural_psi=False,
    )
    noticing = skill_check(commuter, Action.OVERCOME, "Notice", 2, rng=rng)
    resistance = skill_check(commuter, Action.DEFEND, "Will", 1, rng=rng)
    return EverydayEncounter(
        anomaly=EVERYDAY_ANOMALIES[seed % len(EVERYDAY_ANOMALIES)],
        witness=commuter.id,
        noticing=noticing,
        resistance=resistance,
        what_it_does_not_prove=(
            "that anyone read the commuter's mind. Precognition, a predictive model, an attentive "
            "human and a filed complaint the operator had already read all fit the same evidence."
        ),
    )


def commercial_counter_psi_investigation(seed: int = 13) -> Mapping[str, object]:
    """A hired telepath, a hired anti-telepath, and a client who wants something usable.

    This is the institutionalized case: PSI as a regulated commercial service, sold by a firm, opposed
    by a competing specialist, and delivered to a client as a *findings report* rather than a fact. The
    counter-PSI specialist is the load-bearing role -- the strongest thing in the scene is not a power
    but a refusal of access, which is why PSI is never unrestricted here.

    The two accounts are deliberately incompatible, and the honest answer to the client may be that
    nothing can be proven.
    """
    rng = Random(seed)
    ledger = PsiOperationLedger()

    reader = Character(
        id="hired-viewer", name="Hired Remote Viewer",
        aspects=["Certified Grade II", "Works to the Contract, Not to the Truth"],
        skills={"Psi": 3, "Investigate": 1, "Will": 1},
        gear=["Licensed amplifier (leased, logged)", "Consent capture form"],
        natural_psi=True, psi_abilities=["remote_viewing"],
    )
    specialist = Character(
        id="hired-anti-telepath", name="Hired Counter-PSI Specialist",
        aspects=["Retained by the Other Side", "Sells Shielding, Not Certainty"],
        skills={"Technology": 2, "Notice": 3, "Will": 2},
        gear=["Detection rig", "Shielding kit (interference is local, not absolute)"],
        natural_psi=False,
    )

    operation = PsiOperation(
        identifier="op-harbour-audit",
        agent_id=reader.id,
        target_id="sealed warehouse manifest",
        location_id="old_harbor",
        approach="remote_viewing",
        asset_ids=(reader.id, "licensed amplifier (leased, logged)"),
        purpose="locate a manifest the client says was never filed",
    )
    ledger.declare(operation, agents={reader.id: reader.id, specialist.id: specialist.id},
                   assets={reader.id: "certified grade II reader",
                           "licensed amplifier (leased, logged)": "leased asset"})

    access = skill_check(reader, Action.OVERCOME, "Psi", 2, rng=rng)
    shielded = skill_check(specialist, Action.DEFEND, "Notice", 2, rng=rng)

    # Access is contested rather than granted: the specialist's defence is the strongest input.
    access_held = access.succeeds and not (shielded.succeeds and shielded.shifts >= access.shifts)
    observation = (
        "a manifest-shaped absence at the north rack, with a hand-written correction"
        if access_held else
        "interference: the north rack returns nothing distinct from three other racks"
    )
    ledger.report(PsiFinding(
        operation_id=operation.identifier,
        observation=observation,
        verification="inconclusive",
        alternative_explanations=(
            "the rack is simply empty and the client misremembered the filing",
            "the shielding worked, and the absence is an artefact of the countermeasures",
            "the manifest was moved by ordinary means during the audit window",
        ),
    ))
    ledger.report(PsiFinding(
        operation_id=operation.identifier,
        observation="the client's own summary contradicts the two licensed readings it cites",
        verification="inconclusive",
        alternative_explanations=(
            "the client is negotiating the fee with a conclusion it already prefers",
            "a clerical error in the client's own filing system",
        ),
    ))

    return {
        "operation": operation.to_dict(),
        "access": access,
        "counter_psi": shielded,
        "access_held": access_held,
        "accounts_agree": False,
        "ledger": ledger.to_dict(),
        "proves_what": (
            "an absence at the north rack, at most, and only if the client accepts that the shielding "
            "could have produced it. Nothing here identifies a reader, a method or a culprit."
        ),
        "client_answer": (
            "You have two licensed readings that disagree, one of which was taken under active "
            "countermeasures. On this evidence the finding is inconclusive; we can re-run with the "
            "shielding logged and the manifest produced, or we can stop."
        ),
    }
