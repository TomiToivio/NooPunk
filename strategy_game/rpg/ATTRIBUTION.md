# Attribution and licensing notices — the NoöPunk RPG layer

**Status: authored.** This is the file `rpg/fate.py` refers to. It is hand-written, unlike the
*generated* `docs/sources/ATTRIBUTION.md` (a #231/#200 artefact that tracks source-material licences
and must not be edited by hand). `tests/test_rpg_boundary.py` asserts that this file exists, so the
pointer in shipped code cannot dangle again.

---

## Fate Core — the foundation, CC BY 3.0

This work is based on **Fate Core System** and **Fate Accelerated Edition** (found at
<https://www.faterpg.com/>), products of Evil Hat Productions, LLC, developed, authored, and edited by
Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin, Mike Olson, Clark Valentine, Amanda
Valentine, Fred Hicks, and Rob Donoghue, and licensed for our use under the **Creative Commons
Attribution 3.0 Unported** license (<https://creativecommons.org/licenses/by/3.0/>).

Fate Core System © Evil Hat Productions, LLC. Used under CC BY 3.0.

The Fate Core SRD is at <https://fate-srd.com/fate-core>; the official licensing page is
<https://fate-srd.com/official-licensing-fate> and the CC BY 3.0 guidance is
<https://fate-srd.com/official-licensing-fate/cc>.

### What the Fate licence permits

CC BY 3.0 permits **commercial** reuse and adaptation **with attribution**. That is why Fate Core is
this layer's foundation: it is the only one of the three references whose terms are compatible with
distribution under whatever licence this project eventually chooses.

---

## The three references are NOT interchangeable

This distinction is load-bearing and easy to get wrong. These licences are not a spectrum of the same
thing; two of them restrict commercial use and one does not.

| Reference | Licence | Commercial reuse | Role here |
| --- | --- | --- | --- |
| **Fate Core SRD** | CC BY 3.0 | **yes**, with attribution | **the foundation** — mechanics implemented |
| **Transhumanity's Fate** | CC BY-**NC**-SA 3.0 | no | design reference only |
| **Eclipse Phase** (2e rules reference; publisher licence page) | generally CC BY-**NC**-**SA** 4.0 — check each product and every stated exception | no | technical/PSI design reference only |

- Eclipse Phase 2e rules reference (unofficial rendered CC edition):
  <https://eclipsephase.github.io/en/03/00-game-mechanics.html> · publisher licence:
  <https://eclipsephase.com/cclicense/>
- Transhumanity's Fate preview, carrying its own licence declaration:
  <https://d1vzi28wh99zvq.cloudfront.net/pdf_previews/176939-sample.pdf>

**The rule this imposes:** the implementation is **original Python code** written against the Fate Core
SRD. No protected text, illustration, setting content, character catalogue or proprietary detail from
either NC-SA source has been copied, paraphrased or ported. Those works informed *mechanical* thinking
only. Before any distribution, the project's own licence must be decided separately — an NC-SA-derived
element would change what is legally possible, so none is imported.

---

## Unofficial — not endorsed

**This is an unofficial implementation.** It is **not endorsed by, affiliated with, or approved by Evil
Hat Productions, LLC, or Posthuman Studios LLC**, and no claim of such endorsement is made. *Fate*,
*Fate Core* and *Fate Accelerated* are trademarks of Evil Hat Productions, LLC. *Eclipse Phase* and
*Transhumanity's Fate* are the property of Posthuman Studios LLC. References to those works here
identify design influences only.

---

## NoöPunk canon — deliberately not inherited

Per #389 and #306, **no Eclipse Phase setting content is imported.** Specifically, this layer does
**not** inherit Eclipse Phase's factions, history, the Fall, alien biology, the exsurgent virus,
Firewall, its mesh assumptions or its posthuman social baseline. Only mechanical ideas and techniques
inform the implementation.

Three NoöPunk differences are non-negotiable and are enforced in code rather than promised in prose:

1. **PSI is natural**, sometimes trainable, and **is not caused by a virus**. Many humans have natural
   PSI. Psychotronics, QIP and anti-PSI equipment may modify accessibility, control, safety or defence;
   they do not make PSI an infection.
2. **Cortical stacks and resleeving are new, experimental, rare and expensive.** A biological body is
   the default. Most humans keep their original bodies; routine resleeving is **not** normal society.
   Nothing in this layer makes a stack or a resleeving mandatory for character creation.
3. **Legacy NoöPunk RPG rules are not imported.** Per #306 the legacy lore may be shared, but its old
   mechanics are not automatically carried over.

The opening default remains **pre-NHI-Crisis acceleration**.

---

## Licensing status of this project

**Not yet chosen** for the NoöPunk rulebook and original setting — see `docs/sources/ATTRIBUTION.md`
(issue #231, criterion 1) for the project-level position, which is a separate question from the Fate
basis above. Source code is licensed separately from setting text.
