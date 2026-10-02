# NoöPunk writing style and modelling conventions

> **Status:** author-requested convention document (issue #41). It defines **how
> NoöPunk material is written, cited and labelled**. It does **not** define setting
> facts, mechanics, or canon. Where a convention would require a mechanical
> decision, it says so and stops.
>
> The design invariants live in [`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md) and
> are referenced here rather than restated. The per-rule theoretical grounding
> lives in [`THEORETICAL_SOURCES.md`](THEORETICAL_SOURCES.md).

## 0. What this document is for

NoöPunk is a hybrid artefact: a tabletop RPG, a speculative social-science
monograph, a future-history document, and fiction. Those four registers have
different obligations — a monograph must be traceable, fiction must be
unreliable — and the project's whole character comes from letting them coexist
*without* laundering one into another.

This document sets the conventions that keep them distinguishable on the page.

A useful statement of the underlying principle:

> **The sourcebook may know the theories. The characters usually do not know which
> theory is true.**

The apparatus is written for the reader who wants to check the reasoning. The
fiction is written from inside a world where the reasoning is unsettled. Neither
register may be used to smuggle claims past the other.

---

## 1. The four registers

Every piece of NoöPunk text belongs to one of these. Register governs voice, and
the register should be obvious without a label.

### 1.1 Expository text — "how this works"

Plain, precise, theory-aware, readable. This is where a rule is stated, a model is
described, or a convention is explained. It may cite freely and should be the
only register that sounds like it is certain of anything.

- Prefer short sentences and concrete nouns.
- State the rule, then the reason, then the edge case.
- If a claim rests on a contested source, say which layer of
  [§4](#4-epistemic-status-of-a-claim) it occupies.

### 1.2 Setting text — "what it feels like to be here"

Concrete and sensory, and **not** an encyclopedic lore dump. Prefer artefacts over
exposition: institutions, procedures, technologies, conflicts, social practices,
advertisements, news fragments, transcripts, reports, leaked documents, eyewitness
accounts.

The test: if a paragraph could be replaced by a bullet list of facts without loss,
it is a lore dump and should be rewritten as an artefact or moved to a sidebar.

### 1.3 Fiction — "what it is like from inside"

Philip K. Dick's high-level qualities, black comedy, institutional absurdity,
human-scale characters. See [§3](#3-fiction-style-philip-k-dick-as-tonal-reference).
The narrator is not omniscient, and the register must not resolve what the setting
deliberately leaves open.

### 1.4 Sidebars — "how we know, and what we chose"

The apparatus lives here, out of the fiction's way. Sidebars carry:

- **real-world theory** — the source and what it actually argues;
- **historical background** — the documented situation being extrapolated from;
- **competing interpretations** — where the field genuinely disagrees;
- **scientific status** — where the claim sits epistemically;
- **designer notes** — why a rule was written this way;
- **simulation notes** — how the rule behaves when sampled many times.

Sidebars are where [§4](#4-epistemic-status-of-a-claim)'s status labels are used
most heavily, because a sidebar is the natural place to admit uncertainty.

---

## 2. Academic worldbuilding rule

### 2.1 Start from something real where possible

Worldbuilding should begin from a real theory, research programme, documented
anomaly, technology or intellectual tradition — not from genre convention. The
author's own list (issue #41) includes Laclau and discourse theory; Castells and
the network society; Luhmann and communication systems; Deleuze/DeLanda and
assemblages; panpsychism; quantum theories of mind; BCI/cyborg research; AI/AGI
research; collective intelligence and noösphere traditions; UFO/UAP and NHI
hypotheses including Vallée-style readings; cybernetics, systems theory,
complexity and network science, social simulation, statistics, cognitive science,
sociology and political economy.

### 2.2 The five-part entry

For any important setting claim or mechanic derived from theory, record five
things — the same shape `THEORETICAL_SOURCES.md` already uses:

1. **Source** — identify the theory or research programme.
2. **Citation** — author and work.
3. **NoöPunk reading** — how the project interprets it.
4. **Extension or disagreement** — what NoöPunk adds, and where it departs.
   Departures are recorded, not hidden.
5. **Mechanical consequence** — what the rule or design constraint actually is.

The five parts must stay **separable on the page**. A reader should be able to tell
where the source stops and NoöPunk begins without reading the whole entry.

### 2.3 Traceable, not arbitrary

The point of the apparatus is that a reader can follow a setting claim back to
something identifiable. A claim whose foundation cannot be named is not
disqualified from fiction — it belongs in fiction, where it does not need a
citation.

---

## 3. Fiction style: Philip K. Dick as tonal reference

`README.md` already states the direction: NoöPunk leans **more toward Philip K.
Dick than William Gibson**. `AGENTS.md` §7 names Dick as a recognised influence to
use as a *high-level tonal reference only*.

### 3.1 The qualities worth taking

- unstable reality and competing ontologies;
- ordinary people trapped inside gigantic systems;
- uncertainty over who or what is acting;
- identity instability;
- bureaucracy, corporations, machines, media, religion, drugs, technology and
  metaphysics colliding;
- dark humour;
- banal everyday life continuing while reality becomes unreliable;
- characters who rarely possess a God's-eye view;
- social systems that are absurd without becoming meaningless;
- revelations that change *interpretation* rather than merely adding lore.

### 3.2 The rule against pastiche

**Do not imitate Dick's prose line-for-line, and do not pastiche his style.**
Capture the high-level literary qualities and the epistemic instability; develop a
distinct NoöPunk voice. This is the same boundary `AGENTS.md` §7 draws around
protected material, applied to a tonal influence rather than a setting one.

### 3.3 Why this fits the project

The PKD qualities are what make epistemic restraint *dramatically useful* rather
than merely honest. A world undergoing several simultaneous paradigm changes is one
where nobody — including the sourcebook's characters — can be sure which framework
is correct. That is exactly the condition Dick's fiction dramatises.

This is also why the fiction must not resolve the setting's open questions. A story
that settles whether psi is real has spent the project's central ambiguity for a
single scene.

---

## 4. Epistemic status of a claim

Every substantive claim about the world is labelled with **one** of these six
levels. The vocabulary is binding; the *visual notation* is not yet decided
([§7](#7-notational-conventions)).

| # | Label | Meaning |
|---|---|---|
| 1 | **Established** | Robustly documented within current science or history. |
| 2 | **Contested** | Legitimate active disagreement among qualified people. |
| 3 | **Speculative** | Weak evidence or an unresolved hypothesis. |
| 4 | **Fringe / anomalous** | Outside current mainstream consensus, but historically or theoretically documented. |
| 5 | **NoöPunk extrapolation** | A deliberately fictional consequence. |
| 6 | **In-world unknown** | The game deliberately refuses to establish one canonical explanation. |

### 4.1 The two levels that carry the most weight

**Fringe / anomalous is not a synonym for false, and not a synonym for true.** It
records that a claim has a documented history and lacks mainstream acceptance.
NoöPunk takes such claims seriously *as worldbuilding material* without
strengthening the present-day evidence for them.

**In-world unknown is a first-class outcome, not a gap.** When the project refuses
to settle a question, that refusal is the canon. It should be stated explicitly so
a later contributor does not "helpfully" resolve it.

This matters most for consciousness, psi, NHI/UAP and quantum-mind themes, where
the temptation to promote a speculative premise into setting fact is strongest.

### 4.2 A worked status statement

The registered example is the psychic-fundamentality claim in
`THEORETICAL_SOURCES.md`. Its shape:

- the Luhmannian four-system architecture — **Established** (as an account of
  Luhmann);
- adding **Cybernetic** as a fourth domain — **NoöPunk extrapolation**;
- the four domains being *ontologically* separate — **in-world unknown /
  deliberately rejected**;
- the psychic domain being fundamental — **Speculative**, stated as setting
  metaphysics and carrying no mechanics.

Note that the entry distinguishes *what Luhmann argues* (established as
scholarship) from *whether it is true* (not asserted). Both distinctions are
needed.

---

## 5. Citation conventions

### 5.1 Where citations go

- **Inline or compact footnote** in the running text, where practical.
- **Full reference** in the book's references section, and in
  `docs/THEORETICAL_SOURCES.md` for rules.
- **Sidebar** when the source needs explanation rather than mere attribution.

### 5.2 What a citation must carry

For a rule or setting claim: author, work, and — where the claim is contested —
enough context that a reader could find the disagreement rather than only the
claim. A citation that makes a contested idea look settled is worse than no
citation.

### 5.3 The status markers

Three markers distinguish the layers of a claim:

- **REAL:** — a documented real-world source.
- **MODEL:** — an interpretation used by the game or simulation.
- **NOÖPUNK:** — a fictional extrapolation.

The markers are used where the distinction could otherwise be lost — especially
where a mechanic looks like a measurement but is a modelling choice. They are
**not** required on every sentence; a fiction passage needs none, and a passage
that is plainly expository does not need to label every clause.

### 5.4 Demonstration

> A NoöPunk network mechanic is derived from a communication-network model.
>
> **REAL:** Castells argues that power in the network society operates through
> networks, and that "switchers" connect otherwise separate networks.
> *(Castells, Communication Power.)*
>
> **MODEL:** NoöPunk treats a character's position in a communication network as a
> modelled parameter rather than as a fictional fact about the world.
>
> **NOÖPUNK:** In 20XX, a switcher's leverage is something a character can be born
> into, sell, or lose to a machine.

The three lines do different jobs. Only the first is a claim about reality.

---

## 6. Statistical and probabilistic rules — an investigation

> **This section is an investigation, not canon.** `RULEBOOK.md` §4 fixes the
> canonical resolution engine; `AGENTS.md` §1 and §4 make inventing or revising
> mechanics out of scope for a documentation task. Nothing below changes a rule.
> Each option is recorded with what it would buy and what it would cost, so the
> author can decide.

### 6.1 The question

Could NoöPunk's rules be *fundamentally* statistical models rather than
game-only mechanics — so that one conceptual model drives tabletop resolution,
multi-agent simulation, computational social science, a Godot runtime, Monte Carlo
world simulation, and scenario balancing?

### 6.2 What already exists

The canonical check is `2d6 + skill level + attribute modifier >= difficulty`
(RULEBOOK §4), with the ladder 6 / 8 / 10 / 12 / 14+. That is already a
probability model; what is missing is an explicit statement of it.

The exact distribution of 2d6 over 36 outcomes, computed rather than asserted:

```text
 2: 1/36   3: 2/36   4: 3/36   5: 4/36   6: 5/36   7: 6/36
 8: 5/36   9: 4/36  10: 3/36  11: 2/36  12: 1/36
mean 7.0 · variance 5.833 · sd 2.415 · mode at 7 · P(2) = P(12) = 1/36
```

Success probability on the canonical ladder at a +0 modifier:

| Difficulty | Meaning (RULEBOOK §4) | P(success) |
|---:|---|---:|
| 6 | Relatively simple, still beyond routine | 0.722 |
| 8 | Significant challenge to a competent professional | 0.417 |
| 10 | Difficult, expected mainly of a skilled expert | 0.167 |
| 12 | Master-level challenge | 0.028 |
| 14+ | Extreme; even a true master will probably fail | 0.000 at +0 |

Two structural facts follow, and both are worth stating explicitly in the rulebook
because they are properties of the numbers rather than of the prose:

1. **The top of the ladder requires a positive modifier to be reachable at all.**
   At difficulty 14 a +0 modifier succeeds with probability zero — the highest
   reachable total with no modifier is 12. Difficulty 12 needs +0 to roll a natural
   12 (1/36). This is consistent with the ladder's stated intent, and it makes the
   value of attributes and skills concrete rather than rhetorical.
2. **2d6 is bounded and triangular, not normal.** P(2) = P(12), and the tails close
   abruptly at ±5 from the mean. A latent-variable model fit to this engine must
   respect the bounds; a logistic fit would be an approximation, exact only in the
   middle.

### 6.3 The candidate approach, and its three levels

The issue suggests a latent-variable interpretation, e.g.

```text
P(success) = logistic(actor capability + skill + tools + situational modifiers
                      + network/social context - task difficulty + noise)
```

Three distinct claims are bundled there, and keeping them apart is what makes the
investigation useful:

**(a) Interpretive.** The canonical 2d6 check *is* a probabilistic model in which
attributes and skills are latent parameters and difficulty is a threshold. This is
a description of what exists. **Cost: none** — it requires no rule change, only a
paragraph in §4. **Value: high**, because it makes the same engine usable in
simulation without forking it.

**(b) Representational.** A logistic (or probit, or ordinal-logit) form is the
*underlying* model, with 2d6 as a bounded tabletop sampler of it. **Cost:
moderate**, because 2d6 cannot reproduce a logistic curve across the full range
(see 6.2 fact 2); the mapping would need an explicitly approximate, clamped,
documented correspondence. **Value: real** if the project wants one closed-form
model shared with non-RPG simulation.

**(c) Replacing.** The rules *become* latent-variable mechanics, with dice as
purely cosmetic. **Cost: high**, and it is a mechanical redesign that requires the
author's explicit decision. **Value: unclear** — it would make tabletop play
mathematically heavy, which the issue's own design constraint warns against.

**A caution about (b) and (c).** The four domains are Social / Physical / Psychic /
Cybernetic, and the psychic domain is explicitly the metaphysically fundamental one
carrying no mechanics. A single latent-variable form fitted uniformly across all
four would quietly assert that the psychic domain is mechanically commensurable
with the others — a metaphysical claim smuggled in as mathematics. **If this route
is taken, commensurability must be an explicit author decision, not a side effect
of a shared formula.**

### 6.4 What keeps tabletop light

If any of this becomes canonical, the constraint from the issue holds: the
mathematical layer stays beneath the table, and players interact only with the
dice-facing interface. A model that must be explained mid-session has failed.

---

## 7. Notational conventions

**The status vocabulary of [§4](#4-epistemic-status-of-a-claim) and the three
markers of [§5.3](#53-the-status-markers) are fixed. Their visual notation is
not** — whether they appear as coloured icons, marginal sigils, typographic weight,
or parenthetical tags is a design decision and is deliberately left open here.

What is fixed is that a reader can determine, for any substantive claim, which of
the six statuses applies and which of the three markers is in play.

---

## 8. The dice ↔ simulation relationship

This describes the **existing** canonical engine; it does not add to it.

The canonical check has a closed-form distribution ([§6.2](#62-what-already-exists)),
so the same model can be sampled directly rather than reimplemented:

- **Tabletop:** roll 2d6, add the modifier, compare to the threshold. The player
  sees only this.
- **Simulation:** draw from the same 36-outcome distribution, or evaluate the
  success probability directly. No dice, no fork in the rules.

The two agree because they are the same model at different resolutions — the dice
*are* the sampler. This is what makes "one conceptual rules model across human play
and machine simulation" achievable without either side inventing mechanics:

- the simulation must **not** invent a probability the tabletop rule does not have;
- the tabletop must **not** require the player to evaluate a probability;
- neither may change the ladder or modifier structure independently.

Where a rule has no closed form (bounded recursion, resplitting, iterative
procedures), the simulation must call the same procedure rather than approximate
it. Approximation that silently becomes canon is the failure mode this convention
exists to prevent.

---

## 9. Modelling systems above the individual

Character-level checks are not the whole of NoöPunk. The setting's paradigm shifts
are *social* events, so the rules must be able to describe systems larger than one
person: a network, an institution, a discourse, a market, a faction, a population.

**This section defines how such a model is written down. It defines no model.** The
mechanics that would drive any of it are unresolved — `AGENTS.md` §4 leaves social
mechanics, factions, economy and detailed simulation mechanics explicitly
undecided — so what follows is the convention a future author-specified model would
follow, not a design.

### 9.1 The rule

> **Every system-level model must be introduced as a model, with its assumptions
> and its limits stated before its results are used.**

A claim about a population is not the same kind of claim as a claim about a
character, and the difference must be visible on the page. The
[§10](#10-conventions-for-describing-a-model) six-part description applies in full;
what is added here is that a *system-level* model needs its **unit of analysis** and
its **scope** named explicitly, because those are the two things readers silently
assume.

State, for every such model:

1. **Unit of analysis** — the individual, the message, the institution, the
   network edge, the population. A model of "belief" means nothing until this is
   fixed.
2. **What is aggregated away** — the individual variation the model deliberately
   discards. Aggregation is always a lossy choice, and naming the loss prevents the
   model being read as a description of every member.
3. **Scope limit** — the domain and scale the model is claimed to hold for.
   A diffusion model fitted to a small sample does not speak for a society.
4. **Whether the model is descriptive or normative** — that a network *is*
   centralised is a different claim from one about whether it *should* be. NoöPunk
   contains a normative political layer (PCM), so this distinction will be
   tempting to blur.

### 9.2 What a system-level model may be about

The issue lists the candidate domains. Recording them here defines the *vocabulary
of the modelling conversation*, not the models:

- **communication and diffusion** — information diffusion, memetic and ideological
  change, technological adoption;
- **formation and alignment** — belief and discourse formation, political
  alignment, collective action;
- **structure and power** — network centrality, institutional power, faction
  behaviour;
- **material conditions** — markets and scarcity, trust and reputation;
- **agents** — AI agents, human–AI assemblages;
- **anomalous coupling** — psionic or anomalous phenomena, **only in scenarios
  where those setting assumptions are explicitly enabled**.

Each of these is a place where a real statistical, social-scientific, cybernetic,
network or agent-based model can be identified and cited. Where no source can be
named, the claim belongs in fiction, where it needs no citation
([§2.3](#23-traceable-not-arbitrary)).

### 9.3 Theory owns a question, not a vocabulary

This is the convention that keeps a system-level model from becoming a theory soup.
Each source is written down as owning **one question**, phrased so it is falsifiable:

| Source | Owns the question | Not responsible for |
|---|---|---|
| Laclau | how demands articulate into equivalential chains and antagonisms | network structure |
| Castells | communication networks and network power | evaluating that power |
| Luhmann | how communication reproduces itself into a system | the content communicated |
| Deleuze / DeLanda | what heterogeneous components are bound together, and how stably | counting edges |
| network science / SNA | the measurable structure of whatever graph exists | what the structure means |
| statistics / social simulation | how a population-level quantity is estimated | whether the fiction is true |
| PCM | governance mechanics for heterogeneous human/AI collectives | declaring an outcome correct |

This mirrors the question-ownership convention already adopted in
[`SIMULATION_ARCHITECTURE_SPEC.md`](SIMULATION_ARCHITECTURE_SPEC.md) §8.2; that
document proposes it for the state model, and this one requires it for any
system-level claim in the prose. **"Owns the question" is deliberately falsifiable
in a way a vocabulary mapping is not.**

The failure mode being prevented: an assemblage is **not** the same thing as a
network community. Graph properties are one measurable aspect of a binding, not its
definition. Writing them as synonyms would collapse two theories into one and lose
the distinction the project needs.

### 9.4 The same model in the rulebook and the simulation

A system-level rule and a simulation of it follow [§8](#8-the-dice--simulation-relationship):

- the **simulation** may report aggregates the tabletop never computes — a diffusion
  curve, a centrality ranking, a distribution of outcomes over many runs;
- the **tabletop** exposes only the interface a person can use at a table — a
  modifier, a threshold, a consequence;
- neither may change the model, and approximation must not silently become canon.

A model that exists only in the simulation is not a NoöPunk rule. It is a research
instrument, and should be documented as one — which is exactly what the
LaclauGPT/PCM coupling is for: **an empirical layer that does not thereby become
canonical fiction** ([`PROJECT_CONVERGENCE.md`](PROJECT_CONVERGENCE.md)).

### 9.5 Why this is a writing convention and not a mechanic

Agents may not invent social mechanics (`AGENTS.md` §1, §4, §13). What they *can*
do is refuse to let an unspecified system be described as though it were settled.
This section therefore constrains **how a claim is worded** — its unit of analysis,
its scope, its source, its status — and constrains nothing about what the
mechanics should be.

---

## 10. Conventions for describing a model

When a model is introduced — statistical, network-theoretic, agent-based — describe
it in this order:

1. **What it is** — the model and its source, with a citation.
2. **What it assumes** — the assumptions are the interesting part; a model with
   unstated assumptions will be over-read.
3. **What it predicts** — concretely, so the claim is falsifiable in principle.
4. **What it does not predict** — the boundary, stated before someone extends it.
5. **Its status** — [§4](#4-epistemic-status-of-a-claim) layer.
6. **Its mechanical role** — whether it is decorative, interpretive, or
   load-bearing in resolution.

A model described without step 4 will be treated as explaining more than it does.

---

## 11. Worked example: one event, two modes

A single event resolved in tabletop mode and simulation mode, using only the
canonical engine. This is the issue's acceptance criterion, and it demonstrates
[§8](#8-the-dice--simulation-relationship) rather than adding a rule.

**Situation.** A character (skill level 2, relevant attribute modifier +1) attempts
to talk a hostile functionary into releasing a record. The GM judges this a
**significant challenge to a competent professional**: difficulty **8**.

### 11.1 Tabletop mode

```text
total = 2d6 + skill 2 + attribute +1
success = total >= 8
```

The player rolls 2d6 and gets 9. Total = 9 + 2 + 1 = **12** ≥ 8 → success. The table
sees one number and a yes.

### 11.2 Simulation mode

The simulation does not re-derive a rule; it samples the same model. The modifier
is +3, so success needs 2d6 ≥ 5: outcomes 5..12, i.e. 4+5+6+5+4+3+2+1 = 30 of 36
outcomes.

```text
P(success) = 30/36 = 0.8333
```

Sampling 100,000 trials from the identical 36-outcome distribution returns
approximately 0.833 — the same model, evaluated rather than rolled.

### 11.3 What this example demonstrates

- The probability is a **property of the canonical rule**, not a new mechanic.
- The tabletop and the simulation share one model, so a balance change is one edit.
- The simulation can report an aggregate the tabletop never needs to compute.
- The worked numbers are checkable by hand from the 2d6 table in §6.2.

---

## 12. Worldbuilding workflow

The desired rhythm, from the issue:

> **theory → model → strange consequence → playable situation**

Concretely:

1. **Theory** — name a real source and what it argues.
2. **Model** — state how the project reads it, with assumptions and limits
   ([§10](#10-conventions-for-describing-a-model)).
3. **Strange consequence** — the extrapolation, marked **NOÖPUNK:**. This is where
   the fiction is allowed to be strange; it is not where the evidence is
   strengthened.
4. **Playable situation** — what a character can actually do, want, fear or lose.
   If step 3 produces nothing playable, it is an essay, not worldbuilding.

`AGENTS.md` §9's constraint applies throughout: RULEBOOK.md is intentionally
incomplete, and a blank section stays blank rather than being filled with a
convention.

---

## 13. Design constraint: do not write a textbook

The academic apparatus supports the fiction **beneath the floorboards**. It must
not sit on the player's chest.

Practical tests:

- **The register test.** Can a reader tell exposition from fiction from sidebar
  without a label?
- **The interruption test.** Does the apparatus interrupt a scene, or does it wait
  in a sidebar?
- **The playability test.** After reading a mechanic, could someone run it? If the
  theory is more memorable than the procedure, the proportion is wrong.
- **The citation test.** Is the citation doing work, or is it decorating a claim
  that would be fine as fiction?

Fiction that stops for a literature review has failed the register test. An
expository passage that cannot be acted on has failed the playability test.

---

## 14. Examples

Each example demonstrates one convention. They are **illustrative, not canon** —
none of them establishes a setting fact or a rule.

### 14.1 A setting paragraph (artefact, not lore dump)

> **FROM THE 20XX MINUTES OF THE MUNICIPAL RECORDS BOARD**
>
> Item 14: The Board notes that the contested transfer of subscriber telemetry has
> been reclassified as *unresolved* for the fourth consecutive quarter. Members are
> reminded that "unresolved" is not "pending" and that the Board is not required to
> produce a finding. The Board further notes that three former members have
> requested that their own records be reclassified likewise, and that the Board has
> approved these requests without discussion.

No exposition, no narrator, and the institutional absurdity is in the procedure
rather than in a joke. Status: **NoöPunk extrapolation**.

### 14.2 A mechanic write-up (expository register)

> **Contested Records.** When a character petitions an institution to release a
> record that has been classified *unresolved*, the GM calls an opposed check. The
> institution rolls `2d6 + its stated procedure modifier`; the character rolls
> `2d6 + relevant skill + attribute`. Player characters win ties. On a failure, the
> record is not refused — it is *reclassified*, and the character must petition
> again from the new status.

The mechanic is stated, the procedure is playable, and the flavour is in the
consequence. This follows `RULEBOOK.md` §4.1's opposed-check procedure and the
player-character tie rule; it does not add a subsystem.

### 14.3 A sidebar (the apparatus, out of the way)

> **Designer note — why "reclassified" instead of "refused".**
>
> **REAL:** Bureaucratic systems often convert an adverse decision into a status
> change rather than a denial, which makes the decision harder to contest.
> **MODEL:** The rule models institutional resistance as *state transition* rather
> than as a probability of refusal, so repeated attempts are not merely retries.
> **NOÖPUNK:** In 20XX, records can be reclassified faster than they can be
> appealed.

### 14.4 A citation block

```text
Castells, M. (2009). Communication Power. Oxford University Press.

Used for: the treatment of networks as the operative structures of power, and the
distinction between "programmers" (who define a network's protocols) and
"switchers" (who connect networks).
Status of the source's claim: Established as a sociological argument; contested in
its generality.
Not used for: any claim about the empirical power of any specific NoöPunk faction.
```

The "not used for" line is the part that keeps a citation from doing more work than
it can bear.

### 14.5 A fictional vignette (PKD register, no pastiche)

> The building had been a hospital, then a data centre, then a church, then
> whatever it was now. Meri worked on the fourth floor answering complaints about
> the building's classification, and she had learned that the fastest way to close
> a complaint was to agree with it. This worked until the day a complaint arrived
> from her own name, filed nine years earlier, describing an event she had no
> memory of attending.
>
> The system offered her three explanations. All three were flagged *unresolved*.

Narrator not omniscient; reality unstable; institution absurd without being
meaningless; the revelation changes interpretation rather than adding lore. No
Dick sentence is imitated.

---

## 15. Follow-ups (not in this task)

The issue lists items to *consider later*. They are recorded here so they are not
lost, and deliberately not built:

- `docs/SOURCES.md`, or a bibliography database;
- BibTeX / CSL-compatible references;
- machine-readable metadata linking setting elements and mechanics to sources;
- a glossary of theory → NoöPunk extrapolation mappings.

Each is a separate unit of work. This document establishes the conventions they
would follow.
