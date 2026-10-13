# Attribution and licensing — NoöPunk's Fate-based RPG layer

`rpg/fate.py`'s module docstring points here, and `rpg/README.md` mirrors this. The machine-readable
copy of these statements lives in [`attribution.py`](attribution.py), so a test can assert they are
present rather than trusting a document to stay honest.

## Fate attribution

> This work is based on Fate Core System and Fate Accelerated Edition (found at
> https://www.faterpg.com/), products of Evil Hat Productions, LLC, developed, authored, and edited by
> Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin, Mike Olson, Clark Valentine, Amanda
> Valentine, Fred Hicks, and Rob Donoghue, and licensed for our use under the Creative Commons
> Attribution 3.0 Unported license (https://creativecommons.org/licenses/by/3.0/).

> NoöPunk is an independent fan-developed project and is not sponsored or endorsed by Evil Hat
> Productions or Posthuman Studios.

## The upstream terms, kept apart because they are not interchangeable

| Source | Licence | Role here |
| --- | --- | --- |
| [Fate Core SRD](https://fate-srd.com/fate-core) | **CC BY 3.0** | the resolution foundation: four actions, 4dF + skill, aspects, stunts, Fate points, stress and consequences. Commercial reuse is permitted **with attribution**. |
| [Transhumanity's Fate](https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/176939-sample.pdf) (preview with its own licence declaration) | **CC BY-NC-SA 3.0** | transhuman/cyberpunk adaptation reference. **No text, illustration, setting content or character catalogue is reproduced.** |
| [Eclipse Phase 2e rules](https://eclipsephase.github.io/en/03/00-game-mechanics.html) — [publisher licence](https://eclipsephase.com/cclicense/) | **CC BY-NC-SA 4.0** generally; check each product's exceptions | technical and PSI reference. NoöPunk inherits **no** Eclipse Phase faction, history, the Fall, alien biology, the exsurgent virus, Firewall or mesh assumptions. |

## What this layer may and may not reuse

- **May reuse:** mechanical ideas and techniques from the Fate Core SRD, expressed in original code
  and original NoöPunk language.
- **May not reuse:** protected prose, illustrations, game-world content or proprietary details from
  the NonCommercial-ShareAlike sources. They may be *read* as references; they are not a basis for
  distributed code or content.
- **Not decided here:** the licence under which NoöPunk distributes this code. That decision belongs
  to the author and is tracked by the licence gate (issue #200). This file records only what the
  upstream works require of anyone reusing them.

## NoöPunk's own continuities, restated because they are settings decisions not licence terms

- PSI is **natural** and sometimes trainable; it is **not** caused by a virus, and no illness flag is
  required for a psychic character.
- Most humans keep their **original biological bodies**; cortical stacks and resleeving are new,
  experimental, rare and **never mandated** at character creation.
- Default opening remains the **pre-NHI-Crisis acceleration**, and legacy NoöPunk RPG lore may be
  shared while its old rules are not automatically imported (issue #306).
