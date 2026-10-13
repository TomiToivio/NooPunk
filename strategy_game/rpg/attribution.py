"""Attribution and upstream licence references for the Fate-based RPG layer (issue #389).

These constants exist so the attribution is **executable** rather than only prose: a test can assert
that the Fate attribution and the unofficial notice are present in the layer itself. The licence
under which NoöPunk *distributes* this code is a separate decision and belongs to the author — this
module records the **upstream** terms only, and keeps them apart, because they are not
interchangeable.
"""
from __future__ import annotations

#: Fate Core is CC BY 3.0: commercial reuse is allowed *with attribution*. This is the attribution.
FATE_ATTRIBUTION = (
    "This work is based on Fate Core System and Fate Accelerated Edition (found at "
    "https://www.faterpg.com/), products of Evil Hat Productions, LLC, developed, authored, and "
    "edited by Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin, Mike Olson, Clark "
    "Valentine, Amanda Valentine, Fred Hicks, and Rob Donoghue, and licensed for our use under the "
    "Creative Commons Attribution 3.0 Unported license (https://creativecommons.org/licenses/by/3.0/)."
)

#: Stated wherever the layer is described, because it is true.
UNOFFICIAL_NOTICE = (
    "NoöPunk is an independent fan-developed project and is not sponsored or endorsed by Evil Hat "
    "Productions or Posthuman Studios."
)

#: Upstream terms, kept distinct. Only the first is a reuse basis for code.
REFERENCE_LICENCES: dict[str, dict[str, str]] = {
    "fate_core_srd": {
        "url": "https://fate-srd.com/fate-core",
        "licence": "CC BY 3.0",
        "role": "the RPG resolution foundation (four actions, 4dF + skill, aspects, stunts, Fate "
                "points, stress and consequences); commercial reuse permitted with attribution",
    },
    "transhumanitys_fate": {
        "url": "https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/176939-sample.pdf",
        "licence": "CC BY-NC-SA 3.0",
        "role": "transhuman/cyberpunk adaptation reference only; no text, illustration, setting "
                "content or character catalogue is reproduced",
    },
    "eclipse_phase_2e": {
        "url": "https://eclipsephase.github.io/en/03/00-game-mechanics.html",
        "licence": "CC BY-NC-SA 4.0 (generally; check each product's exceptions)",
        "role": "technical and PSI reference only; NoöPunk inherits no Eclipse Phase faction, "
                "history, Fall, alien biology, exsurgent mechanism, Firewall or mesh baseline",
    },
}

#: The decision this module deliberately does not make.
DISTRIBUTION_DECISION = (
    "The licence under which NoöPunk distributes this code is the author's decision and is not made "
    "here (see the licence gate, issue #200). What is recorded here is only what the upstream works "
    "require of anyone reusing them."
)

#: A reuse basis, in one line, for readers in a hurry.
REUSE_BASIS = (
    "Original Python code written against the Fate Core SRD (CC BY 3.0). Transhumanity's Fate and "
    "Eclipse Phase are read as design and technical references; their NonCommercial-ShareAlike terms "
    "are not a basis for this code, and none of their prose, art or setting content is copied."
)
