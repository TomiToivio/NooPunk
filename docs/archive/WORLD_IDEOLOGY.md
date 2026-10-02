# NoöPunk World: Ideology, Paradigm Shifts and the Multitude

> **Status:** author-specified via issue #8. This document establishes setting
> material the author explicitly requested. It does not define mechanics.
>
> Canonical machine-readable positions live in
> [`data/world/ideology.json`](../data/world/ideology.json). This document explains
> them for play; that file is what the runtimes read. Do not re-declare the table
> here or in a runtime — one artefact, three runtimes
> ([`docs/DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) §2).
>
> Dates are **20XX** ([`../AGENTS.md`](../AGENTS.md) §6).

---

## World structure: the social layer crosses the other two

NoöPunk's overall world structure is documented in [THREE_LAYERS.md](THREE_LAYERS.md):

- **Cyberpunk** is the material transformation.
- **Noösphere** is the ontological transformation.
- **Politics / ideology / sociology** is the social struggle over both.

This document develops the **third layer**. It treats NoöPunk as a sociological
simulation of a world undergoing several interacting paradigm shifts, without
turning play into academic exposition. The ideological map exists to generate
factions, institutions, laws, conflicts, coalitions, missions, and historical
realignments in response to technological and ontological change.

---

## 1. The one idea that structures the world

> **Every major paradigm shift generates its own accelerationists, doomers,
> critical/regulatory camps, opportunists, believers, skeptics and hybrids.**

The paradigm shifts are the ones already in [`../TIMELINE.md`](../TIMELINE.md):

| Axis | The shift |
|---|---|
| **AI** | AGI/ASI, and the rogue-AI disaster |
| **NHI** | UFO/UAP disclosure and open contact |
| **Psionics** | reproducibility, then psychotronics as an industry |
| **Panpsychism** | consciousness-fundamental ontology becomes credible |
| **Cyborgization** | BCI from medical systems to ordinary augmentation |
| **Noösphere** | a planetary layer, cybernetic and psionic at once |

**The axes are separable.** That is the whole design. NoöPunk is *not* a world with
one "future technology" axis, and ideology is *not* a single left–right line. A
faction's position on psionics says nothing about its position on AI, and a faction
may be enthusiastic about one shift while hostile to another.

This is why the interesting material is the cross-product rather than the poles.

### What this replaces

The lazy version of this setting collapses into two camps: everyone "pro-future" on
one side, everyone "anti-tech" on the other. That is a world with one conflict and
no surprises. The NoöPunk version is a world where coalitions are contradictory and
historically plausible: a commune that refuses AI and embraces psionics, a
corporation that sells augmentation and publicly dismisses panpsychism, a rights
movement that is hostile to centralised AI and allied with machine participants.

### A note on labels

**"Doomer" is a situated political label, not a neutral description.** This follows
[`LaclauGPT`](https://github.com/TomiToivio/LaclauGPT/blob/main/paper/PHASE_1_PAPER.md)
§2.3: not all safety discourse is existential-risk discourse, and not everyone placed
in that camp accepts the name. Characters, media and factions in NoöPunk use these
words *about each other*, and the disagreement about the labels is itself part of the
politics.

The same applies to **"accelerationist"**, **"critical"** and **"efficient"**. They
are contested signifiers. Use them as sensitising concepts, never as fixed identities
that a faction simply *is*.

---

## 2. Panpsychic Cyborg Multitude — a major Noöspheric faction

There is a powerful Noöspheric faction called the **Panpsychic Cyborg Multitude**.

Most people do not say the full name. *Panpsychic*, *Cyborg* and *Multitude* are each
politically and culturally loaded, so allies, enemies, media and regions each prefer
their own abbreviation or euphemism. **PCM** and **the Multitude** are the common
short forms; which one a speaker reaches for tells you where they stand.

### It is an assemblage, not an organisation

PCM must not be reduced to a cult, a corporation, a government, a hacker collective,
an AI swarm or a political party. Its boundaries are genuinely fuzzy and may include:

- humans;
- AI agents and technological participants;
- cyborgs and BCI users;
- autonomous software;
- distributed communities;
- devices and infrastructures;
- social networks;
- institutions;
- shared memory and coordination systems;
- Noöspheric communication.

That fuzziness is the faction's defining political problem, not a design gap. Nobody,
including PCM, can say exactly where it ends — which is precisely what makes it
frightening to states, useful to allies, and impossible to defeat in the ordinary way.

### What it exports to the rest of the setting

**Panpsychism, cyborg and multitude are three separate words, and each becomes a
general NoöPunk concept** — not merely the name of one faction. A world where only
PCM uses these ideas has failed this integration; they must show up in factions that
have never heard of PCM, or that despise it.

- **Panpsychism** — consciousness-fundamental ontology as a live intellectual
  position. Every faction needs a stance on it, including the ones that find it
  embarrassing: a corporation that will not say it in public, a state that licenses
  it, a refusal commune that treats it as obvious. The word does the work even where
  the faction does not.
- **Cyborg** — the condition of being mixed, which by 20XX is *ordinary* rather than
  a subculture. It is a labour category, a medical category, a class marker and an
  identity claim at once, and different factions disagree about which of those it
  primarily is.
- **Multitude** — the political problem of a collective that is not a state and
  cannot be founded. Every large formation in the setting has a version of this
  problem, whether or not it uses the word: how do you act together without becoming
  a sovereign?

Alongside those three, a further set of concepts recurs throughout NoöPunk:

- distributed and assemblage identity;
- human–machine collectives;
- shared memory and provenance;
- autonomy versus coordination;
- AI participants rather than AI merely as tools;
- technological participants with procedural rights;
- collective intelligence and the Noösphere;
- local-first and distributed organisation.

If every appearance of these ideas in play leads back to PCM, the integration has
failed. A frontier corporation has its own reading of the cyborg. A refusal commune
has its own reading of the multitude. A state security service has its own reading of
panpsychism, and it is not a friendly one.

---

## 3. PCM's positions, and its internal disagreements

PCM is **not one ideology**. It contains tendencies and argues with itself. Its
positions (see `ideology.json` for the canonical record):

| Axis | Position | In one line |
|---|---|---|
| AI | hybrid | Critical of centralised AGI, not of machine intelligence. Supports procedural rights for AI participants. |
| NHI | hybrid | Contact is open and has a consciousness component. Whether it strengthens or fractures PCM is unresolved. |
| Psionics | hybrid | Engaged without being credulous. |
| Panpsychism | hybrid | The name's own root — and held as an *open question*, not an assertion. |
| Cyborgization | accelerationist | Embraces hybridity; holds that enhancement is judged through consent and access. |
| Noösphere | accelerationist | Aims at a planetary layer that is local-first and distributed, not sovereign. |

### Questions PCM has not answered

These are deliberately unresolved, and they are play material. Do not settle them in
canon; put them in front of players as factions and characters who answer differently:

- Is PCM accelerationist about BCI while critical about centralised AGI?
- Does it support procedural rights for AI participants — and how far?
- How does it handle human autonomy inside a collective intelligence?
- How does it react to genuine psionics?
- What if panpsychism becomes scientifically credible?
- Does NHI contact strengthen or fracture it?
- What does "Multitude" mean politically when humans, AIs and cyborgs all participate?
- **Can PCM become oppressive despite its distributed ideals?**

That last one matters most. A faction that cannot become a threat is not a faction;
it is a wish. PCM's danger is not tyranny but *absorption* — the collective that
cares for you so completely that leaving stops being imaginable.

---

## 4. PCM in the Noösphere — relationships

PCM is a major actor, not a universal solvent. Its relationships are uneven and
mostly transactional:

- **Noöspheric infrastructure** — PCM wants it common and federated; whoever owns the
  physical layer has leverage over PCM it cannot easily answer.
- **Human communities** — unevenly warm. Some are PCM; some see it as a machine
  landlord that happens to be kind.
- **AI agents** — the closest thing PCM has to kin, and the relationship is not
  simple: PCM speaks *for* machine participants whose standing it cannot prove, which
  is exactly the arrangement some machine participants resent.
- **Governments** — a jurisdictional problem. PCM is not a state and refuses to be
  one, so it is regulated as an organisation, a network, a hazard or a church,
  depending on who is doing the regulating.
- **Corporations** — rivals for the same infrastructure and the same people. Often
  mutually dependent, never comfortable.
- **NHI contact groups** — split. Some read PCM as the human institution that came
  closest to being ready; some read it as a rival claimant to revelation.
- **Psionic organisations** — cautious allies and ideological rivals at once: both
  take mind seriously, and they disagree about whether mind should be *engineered*.
- **Transhumanists** — overlaps on augmentation, fractures on ownership and consent.
- **Anti-AI movements** — enemies, with one specific exception: anti-AI movements and
  PCM agree that centralised machine authority is dangerous, and disagree about
  absolutely everything else. Coalitions of convenience form around this.
- **Ecological movements** — complicated. PCM's refusal of extractive infrastructure
  earns real trust; its appetite for computation spends it again.
- **Security services** — treat PCM as an ungovernable coordination system, because
  it is one. Whether that is a threat depends on the government.
- **Religious movements** — some read the Multitude as a false communion, some as an
  attempt at the real thing, and some as a mirror they would rather not look into.
- **Anarchists and autonomists** — natural allies, permanent friction: PCM
  coordinates, and they distrust coordination as such.
- **Public institutions** — the awkward middle: PCM is often the only actor able to
  do what a public institution needs done, which makes it indispensable and therefore
  impossible to govern.

---

## 5. Events change the map

When one of the timeline's paradigm shifts lands, positions **realign on that axis**
and may shift on allied ones. Factions should split, merge, radicalise, moderate or
change alliances. The world is meant to feel historically dynamic, not frozen.

The event list is canonical in `ideology.json` (`paradigm_shift_events`). In play, an
event should be usable as a **campaign beat**:

- **First credible AGI** — the AI axis polarises; "critical/regulatory" is squeezed
  from both sides and becomes the hardest position to hold.
- **Rogue AI disaster** — doomer positions gain; some accelerationists split rather
  than moderate, arguing the failure was ownership, not capability.
- **UFO disclosure** and **confirmed NHI contact** — the NHI axis stops being a
  fringe preoccupation and becomes a governance emergency. Factions that agreed about
  everything else suddenly do not.
- **First reproducible psionic phenomenon** — a *new* axis opens. Existing factions
  have no established position and improvise badly; this is where the setting is most
  volatile.
- **Panpsychism gains strong scientific support** — the axis most factions had treated
  as philosophy becomes policy. Positions taken casually become commitments.
- **Mass BCI adoption** and **catastrophic BCI exploit** — augmentation moves from
  identity to infrastructure, and then to vulnerability.
- **Emergence of a functioning Noöspheric collective** — PCM's project either works or
  is revealed as never having been possible. Either outcome is a campaign.
- **AI participant-rights crisis** — the question PCM could not settle is settled for
  it, by force.

---

## 6. Playing it

Theory stays under the surface. The player should meet it as people, laws, money and
guns:

- **Factions** with contradictory positions and plausible reasons for them.
- **Locations** that embody a position: a technology sanctuary, a data-centre
  contested by its neighbours, a BCI clinic that only the augmented can afford.
- **Laws** that are ideological instruments — which paradigm is licensed, taxed,
  banned or subsidised.
- **Missions** where the faction you are working for has an obvious rival you agree
  with more.
- **NPC motives** that follow from the cross-product rather than from a morality label.
- **Campaign consequences** — after the event, what does the map look like now?

Do not explain the model to the player. Let them discover that the person who helped
them last session opposes them on an axis they had not thought of.

---

## 7. Simulation hooks

NoöPunk is also a speculative sandbox for the two research projects, without becoming
an academic model.

**From LaclauGPT** — ideological formations; discourse coalitions; empty signifiers;
hegemonic struggle; polarisation; paradigm narratives; the accelerationist / doomer /
critical conflict; regional divergence; faction realignment after events.

> **Provenance note on the second list.** These are the *simulation targets* named by
> [issue #8](https://github.com/TomiToivio/NooPunk/issues/8), not a claim that the
> LaclauGPT Phase 1 paper formalises all of them. Checking the paper's own vocabulary
> against this list, some of it is the paper's and some is the issue's framing:
>
> - **The paper's own relational vocabulary** is "equivalential chain", "chains of
>   equivalence and difference", "formations" and "political projects". It does **not**
>   use "discourse coalition", so that term is a simulation target here rather than a
>   LaclauGPT concept — the game may find a coalition more useful than a chain, but
>   should not attribute the term to the paper.
> - **"Polarisation"** is likewise not defined or operationalised by the paper.
> - **Regional divergence and post-event realignment** are *not* modelled by the paper:
>   it treats geography as a **sampling decision** ("rather than a claim that these
>   regions represent global AI politics") and states that actors "can move between
>   formations" without specifying how a major event moves them. NoöPunk's event
>   realignments in `data/world/ideology.json` are therefore a *game* system built on
>   the paper's political framing, not an application of a LaclauGPT model.
>
> This distinction matters for provenance, not for play: the mechanics below are
> legitimate NoöPunk designs either way. It is recorded so that a later reader does not
> go looking for a formalised LaclauGPT realignment model that does not exist, and does
> not present NoöPunk's invention as the research project's output.

**From PCM** — distributed human–AI collectives; technological participants;
collective memory; participant identity and continuity; shared decision-making;
dissent; AI refusal; faction coordination; collective intelligence; cyborg / AI /
human assemblages; Noöspheric organisation.

The natural seam: a faction's **position set** (this file) is the input; a **paradigm
shift event** is the perturbation; and what changes is which demands can be
articulated together — who can now stand with whom, and which signifier has become
empty enough to hold them.

---

## 8. Boundaries

- **No mechanics are defined here.** No ideology score, no stance modifier, no
  reputation system. Issue #8 defers that until it would improve the existing rules.
- **20XX**, never a fixed year.
- **No factions, names or text from Cyberpunk, Shadowrun, Eclipse Phase or any other
  game.** The examples in this document and in `ideology.json` are original to
  NoöPunk, and the ones marked `"$example": true` are illustrative formations, not a
  closed canon of organisations.
- **The Noösphere stays speculative and science-fictional** — not generic fantasy
  magic ([`docs/DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) §3).
- **Speculative premises are not presented as established fact**, in-world or out.
- The three design balances are untouched: this is setting material, and no creative
  agenda has been privileged by it.
