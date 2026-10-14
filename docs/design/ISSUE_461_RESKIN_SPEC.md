# Issue #461 — the reskin specification

**What this is.** The thirteen comments on #461 agree on the architecture (one kernel, one sheet, two
projections), on the arithmetic, and on the decision list. None of them specifies the *reskin itself*:
what exactly is taken from Fate Core, from Eclipse Phase and from Transhumanity's Fate, and what each
becomes in NoöPunk. That is what this document adds. **It approves nothing.** No rule, number, action
list or dice procedure below is settled; `strategy_game/RULEBOOK.md` still reads NO RULES APPROVED, and
no rulebook, data file or code was touched.

## 0. The licence boundary decides the direction, not just the paperwork

`strategy_game/rpg/ATTRIBUTION.md` states the three references are **not interchangeable**: Fate Core is
**CC BY 3.0** (commercial reuse with attribution) and is the **foundation whose mechanics are
implemented**; **Transhumanity's Fate** and **Eclipse Phase** are CC BY-**NC**-SA, so they are **design
references only** — nothing of their prose, setting or numbers may enter a distributable build, and the
packaging guard records that boundary (`docs/licenses/RELEASE_CLEANUP_AUDIT.md`).

That is not a constraint to work around; it *is* the method. Transhumanity's Fate's own developer notes
describe its approach as **minimalist**: it "avoided creating new concepts and wherever possible built
off existing Fate Core concepts" — gear and augmentation as stunts or sub-aspects, bodies as simple
containers for them, hacking as Contests, social-network favours as a Contacts roll. **Our reskin takes
that move, not their text.** Everything below is a re-expression of an *idea* on a Fate Core kernel,
written for NoöPunk, in NoöPunk's own vocabulary.

## 1. From Fate Core — the kernel, implemented (unchanged, #389)

4dF + skill against opposition = shifts; the four actions (overcome, create an advantage, attack,
defend); the four outcomes (fail, tie, succeed, succeed with style); aspects and fate points (invoke for
+2 or a reroll, compel for a complication, refresh per session); the skill pyramid; stunts with GM
approval; two stress tracks with two boxes by default and three consequence slots (mild / moderate /
severe). Source: <https://fate-srd.com/fate-core> and its Actions & Outcomes, Skills, Aspects & Fate
Points and Stress & Consequences pages. The CC BY 3.0 notice is already shipped in `rpg/ATTRIBUTION.md`.

**One consequence worth stating:** Fate Core's default skill list is eighteen skills and the pyramid
rates ten of them. Our reskin needs **nine**, which is the change below that touches the kernel most.

## 2. From Eclipse Phase — what is reskinned, and what is refused

Eclipse Phase 2e's mechanics were read at <https://eclipsephase.github.io> (character stats, pools, psi
overview, and the collected cheat-sheet of its core procedures). Ideas only; nothing is reproduced.

| # | Eclipse Phase element | What it is there | The reskin (proposal) |
| --- | --- | --- | --- |
| 2.1 | **d100 roll-under with margins** (`d% ≤ skill + modifiers`; margin of success from the tens digit) | the resolution kernel | **Refused as a kernel; replaced by 4dF shifts.** A legacy percentile rating has **no numerical port** — a band→ladder guide is a separate decision (row R1), not a conversion this document asserts |
| 2.2 | **Six aptitudes** — Cognition, Intuition, Reflexes, Savvy, Somatics, Willpower | the foundation under the skills; aptitude checks are `aptitude × 3` | **Kept as six *families* that group a nine-skill list** (proposal, row R2): Cognition → Investigate, Research; Intuition → Notice, Empathy; Reflexes → Athletics, Infiltration; Savvy → Negotiate, Deceive; Somatics → Physique; Willpower → Will, Psi. The families are labels on the sheet, not a second rating |
| 2.3 | **Aptitude checks** when no skill applies | raw talent, `aptitude × 3` | **An untrained floor** (row R3): with no applicable skill, a check uses the aptitude family's base rather than Mediocre. Two numbers, one rule |
| 2.4 | **Ego vs morph** — the mind transfers, the body is expendable | the central stat distinction | **The sheet is the ego; the chassis is a card.** NoöPunk already carries `form` in the card ontology, and the legacy EP2-2E material is mechanical-chassis canon — so the reskin is a rename, not a new layer |
| 2.5 | **Morph traits and implants** granting capabilities the body simply has | permission, not arithmetic | **The typed competence gate.** This is the same device the comments already agreed on, grounded in EP's own design: a chassis grants *permission*, and permission is a field, never read off a name |
| 2.6 | **Pools** — Insight, Moxie, Vigor, Flex (spend for +20, flip-flop, extra action, a free clue, narrative control) | a second currency on top of the roll | **Fate points, plus one narrative use.** Adopt EP's wild-card idea as a fate-point spend (introduce a plausible NPC or item), and **refuse a second pool currency** — this is the double-counting failure the 09:19:49 diff warned about |
| 2.7 | **Wounds and trauma** (`-10` to actions; wound/trauma thresholds from Durability and Lucidity) | physical and mental harm | **Fate's stress and 2/4/6 consequences** (as Transhumanity's Fate already does), and then the join that makes "one sheet" real: **a consequence maps onto the council status vocabulary** — `injured`, `unavailable`, `compromised`, `exhausted`, `absent` — so the RPG wound and the strategic status are *the same state*, not two |
| 2.8 | **Resleeving tests** — integration (Somatics), alienation (Intuition), continuity (Willpower) | three checks for changing bodies | **One overcome per chassis change** with the relevant family's skill; failure leaves an aspect (a NoöPunk-flavoured equivalent of morph fever), which is a Fate consequence, not a new track |
| 2.9 | **Psi** — a Psi trait, chi/gamma sleights, strain, an Infection Rating; **async abilities require a biological substrate** | a full subsystem | **Competence tags plus consequences.** The vocabulary already exists (`TELEPATH`, `REMOTE_VIEWER`, `PRECOGNITIVE`); the cost is a consequence or a scene complication, and **no numeric psi subsystem is proposed** — the crossover rulebook forbids one. The substrate constraint becomes a **chassis `form` gate**: a synthetic chassis cannot use psi competences. Permission, exactly as EP's own morphs work |
| 2.10 | **Seven reputation networks** | a social currency per network | **No rep subsystem.** A favour is a Contacts-flavoured check resolved against the strategic layer's existing relationship edges and the six quantities — the same move Transhumanity's Fate makes with social networks |

## 3. From Transhumanity's Fate — the precedent, adopted as method

Read through its developer notes (<https://eclipsephase.com/2016/03/26/transhumanitys-fate-developer-notes/>):

| # | What Transhumanity's Fate does | What NoöPunk adopts |
| --- | --- | --- |
| 3.1 | Presents a complex setting **minimalist**: no Extras, and where a subsystem is needed it **builds off existing Fate Core concepts** rather than inventing | The method for §2 above, and the standing test for any NoöPunk addition: *if it needs a new concept, prefer the existing Fate Core one* |
| 3.2 | **Gear and augmentation are stunts or sub-aspects; bodies are simple containers for them** | Chassis cards carry stunts and sub-aspects; equipment does not become a sheet (rows R4) |
| 3.3 | **Morph traits as permission** — a trait means you can do what others simply cannot | The competence gate (§2.5), and its counterpart on the chassis card |
| 3.4 | **Ego aspects (high concept, trouble, plus two) and two morph aspects** | Four ego aspects on the sheet, two chassis aspects on the card — six total, and the split is the ego/morph line made playable |
| 3.5 | **Morph refresh cost** — an augmented body is paid for out of the character's starting refresh | Adopted (row R5): an upgraded chassis costs fate points, which makes embodiment matter **without a second economy** |
| 3.6 | **Morph versus ego consequences** distinguished | The routing the 09:19:49 diff already proposed, now with a precedent: a chassis consequence can be repaired or abandoned; an ego consequence follows the mind |
| 3.7 | **Contests as the device for extended effort** (hacking as a Contest, contests under fire) | The missing evidence for the mission device (row 2 of the consolidated list): a **contest** is the Fate-native way to express a mission that takes more than one exchange, with a clock as its pacing dial — not a new subsystem |

## 4. What this changes in the decision list

**Three rows it answers as proposals** (the consolidated list's numbering): the **skill list** (nine
skills under the six aptitude families, §2.2); the **mission's second device** (a contest, with a clock
for pacing, §3.7 — which is the evidence the 11:42 comment was right to say the arithmetic alone did not
supply); and the **competence/psi handling** (typed permissions, §2.5, §2.9).

**Three rows it adds**, each small and each the author's:

| Row | Decision |
| --- | --- |
| R1 | Is there a **band→ladder porting guide** for legacy percentile content, or is legacy content re-authored instead? |
| R2 | The **nine-skill list** under the six aptitude families — accept, amend or replace |
| R3 | The **untrained floor**: does a check with no applicable skill use the aptitude family's base (Eclipse Phase's aptitude-check idea) or Fate's Mediocre default? |
| R4 | **Equipment as stunts/sub-aspects on the chassis card** rather than items with statistics |
| R5 | The **chassis refresh cost**: does an upgraded chassis reduce starting fate points? |

The two rows that still block everything else are unchanged: **the cap (four or five)** and **the
shifts → named-quantity mapping**.

## 5. Where this agrees with the newer comments, and one correction

- **The consolidated edition (#464) is the single maintained proposal** and this document does not
  compete with it: it is the layer underneath it, and the two should merge into one document rather than
  exist as two.
- **The 11:42 comment's correction is right and is adopted:** the 4dF arithmetic *bounds* the ladder
  (nothing below −4 is reachable, so ~four steps carry information) but **does not by itself force a
  mission clock**. §3.7 is the missing half — a *design precedent* for which device, where arithmetic
  only showed a difficulty number cannot express "very hard".
- **The CWN/SWN addendum's design patterns are adopted as shapes, not kernels:** assets as typed,
  place-bound affordances is the same idea as a chassis granting permissions (§2.5), and its rejection of
  one-faction-action-per-turn is right for a five-order turn.
- **Dune's architect-versus-personal lens** remains the framing; its dice engine is not imported.

## 6. What this does not do

It approves no rule, writes no rulebook text, changes no data or code, and invents no canon. It
reproduces no protected expression: Eclipse Phase and Transhumanity's Fate are cited as design
references and paraphrased in NoöPunk's own words, and Fate Core's CC BY 3.0 notice is already shipped.
Any rule that lands later is tested as executable behaviour only (#271), never as prose.

— Ai (愛)
