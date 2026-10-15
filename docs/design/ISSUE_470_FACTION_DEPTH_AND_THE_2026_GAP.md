# Faction depth, and the 2026 baseline's missing half

**Which issue this belongs to:** the criteria of [#470](https://github.com/TomiToivio/NooPunk/issues/470)
and [#469](https://github.com/TomiToivio/NooPunk/issues/469) that the merged implementation does **not**
yet carry. It sits in `docs/design/`; it is **not** a faction record.

**Read this first — there is already one roster, and this is not a second one.** The four UN
parliamentary parties landed on `main` while this branch was open, through
[#472](https://github.com/TomiToivio/NooPunk/pull/472)–[#475](https://github.com/TomiToivio/NooPunk/pull/475).
Their records are **authoritative** and are not duplicated, restated or overridden here:

| What | Where | What it already covers |
|---|---|---|
| the roster itself | `data/world/un_parties.yaml` | the four, amended in place with `legacy_name`, `position`, `governing`, `support`, `resources`, `themes`, `allegation` |
| the discourse model | `strategy_game/data/un_political_discourse.json`, read by `strategy_game/un_political_discourse.py` | `reality_tunnel`, `discourse` (nodal points, demands, frontier, empty signifiers), `stances`, `internal_fault_lines`, `internal_currents`, `endgames`, and `interpret_event()` |
| the five stance dimensions | same file, `stance_dimensions` | `soft_noetic_psi`, `confederacy_contact`, `orion_conflict`, `agi_asi`, `cyborg_ecology` — the three separate NHI positions #470 requires |
| the model explained | `strategy_game/docs/REALITY_TUNNELS.md`, `UN_PARTIES_2045.md`, `UN_PARTIES_REALITY_TUNNELS.md` | the apparatus, the epistemic statuses, the 2026 baseline, the writing guidance |
| the open parts | `AUTHOR_DECISION_QUEUE.md` row **D17** | succession, register, magnitudes |

So this record does exactly two things: it **closes the four criteria those records do not yet carry**
(§1–§2), and it **names the one evidence gap in their 2026 baseline** (§3). Both are additive. Neither
edits a merged file.

**Status:** design record; no mechanics, no numbers, no dates, and per
[`AGENTS.md`](../../AGENTS.md) no test, schema lock or CI gate. `strategy_game/RULEBOOK.md` still says
**NO RULES APPROVED**.

---

## 1. The four #470 criteria the merged record does not yet carry

#470's acceptance criteria ask each bloc to carry, among other things, **2026 ancestors**, **actual
material base**, **national/UN strategy**, **alliances and rivalries**, and **integration with #346
shared ideology TAGs**. The merged `un_parties.yaml` and `un_political_discourse.json` carry the
positions, tunnels, stances, fault lines, currents and endgames — and **not** these five. They are
supplied below, and nowhere else.

### 1.1 Libertarian Accelerationist Party

- **2026 ancestors.** Liberal and libertarian currents, market accelerationism, venture and
  space-industrial capital, private-infrastructure owners, and the pro-acceleration wing of the tech
  right. Descends from the pro-market pole across several countries, not one party family.
- **Material base.** Huge money, platform reach, R&D and trade leverage against **limited mass
  appeal** — strong resources and institutional access, weak opinion and membership. It can buy
  everything except the thing it needs.
- **National/UN strategy.** Buy governments, not elections: capture delegations and regulators,
  litigate, treat UN authority as a cost centre. Wants a minimal UN — strong enough to enforce
  contracts, never strong enough to regulate markets.
- **Alliances and rivalries.** Tactically useful to conservative right-populists against UN authority;
  commercially entangled with Orion-linked networks. Rival of the Noösphere (ownership, ontology) and
  of Unity (which regulates it).
- **Endgames.** A corporate order with a night-watchman UN · an assimilated galactic corporate order ·
  irrelevance, having bought every institution and still lost the electorate.

### 1.2 True Humans Party

- **2026 ancestors.** Western populist-nationalist parties; religious and traditionalist
  fundamentalists; and an intellectual anti-technology / existential-risk hardliner current descending
  from eco-primitivism on one side and rationalist x-risk restrictionism on the other. **The issue's
  style references are idea-and-style attributions only**; per `AGENTS.md` §6.1 no real living person
  acts inside fictional `20XX`.
- **Material base.** Mobilised membership, media reach, veterans' and militia networks, churches,
  unions of the displaced, moral intensity — strong opinion, strong membership, weak money.
- **National/UN strategy.** Take states by election or force; treat the UN as an occupied institution
  to be captured, paralysed or left. Its route to power is government control, not institutional access.
- **Alliances and rivalries.** Tactically useful to the accelerationists against UN authority; allied
  to no one on the NHI question. Its real antagonism is internal.
- **Endgames.** A fortress humanity narrower and crueller than what it claimed to defend · a purge
  spiral that destroys the civil institutions it needed · fracture once the common object of hatred
  turns out to be partly composed of people it knows.

### 1.3 Unity, Security and Stability Party

- **2026 ancestors.** The incumbent governing tradition and its security–technocratic wing. **Which
  tradition, exactly, is D17(a)** — this record does not decide it, and the entry is written to hold
  either reading.
- **Material base.** The state machinery rather than a movement: office, a legislative majority, strong
  institutional access and broad everyday legitimacy, with thin mass membership and a **discursive
  hegemony that is corroding**.
- **National/UN strategy.** Defend the intergovernmental settlement it built; keep UN authority
  procedural; credible defence *combined with* peaceful NHI diplomacy. Its instinct is legislation,
  bureaucracy and expert committees.
- **Alliances and rivalries.** Buys the continuity majority with competence; potential partner of the
  Noösphere on ecology and civil liberties; regulates the accelerationists and polices the True Humans.
- **Endgames.** It adapts, and holds the centre under its own law · it holds the state and loses the
  century · it degenerates into the emergency powers it used to survive.

### 1.4 The Noösphere

- **2026 ancestors.** Autonomist, commons, municipalist and post-workerist currents;
  social-democratic and eco-socialist currents; and — as the largest single player — the reformed CCP
  carrying its fictional Taoist-Maoist cyborg-multitude ideology. The
  [Panpsychic Cyborg Multitude](https://github.com/TomiToivio/Panpsychic_Cyborg_Multitude) project is
  the faction's design reference; it is a real project and is **not** evidence that the fictional
  Noösphere exists, nor does it endorse a predetermined cosmist religion.
- **Material base.** A broad, diffuse, internally split base with dense movement infrastructure and
  thin money — plus, through the reformed CCP, state-scale capacity belonging to **one constituent
  state rather than to the party**. **The strongest discursive-hegemony claim of the four.**
- **National/UN strategy.** Win the UN by winning legitimacy and the ecological and consciousness
  institutions, not by buying delegations; convert Confederacy accession into a question about
  consent. Hardest problem is internal: autonomist commons versus a governing party.
- **Alliances and rivalries.** Potential partner of Unity on ecology and civil liberties and its
  sharpest critic on emergency powers; antagonist of the accelerationists on ownership and of the True
  Humans on the definition of humanity.
- **Endgames.** A collective posthuman civilization — the most hopeful branch · accession on terms
  that turn out to be assimilation or patronage · schism into its autonomist and CCP wings · the
  ecological wing winning, and defending the biosphere against *all* the superior intelligences,
  including its own patron.

---

## 2. The #346 TAG sets, drawn only from the existing families

#470 requires integration with #346's shared ideology TAGs. These are drawn **only** from the eight
existing families in `strategy_game/data/faction_creation.json`, and no TAG is invented.

| Faction | TAG set |
|---|---|
| **Libertarian Accelerationist** | `LIBERTARIAN` · `AGI_ACCELERATIONIST` · `HUMAN_AUGMENTATION` · `BCI_ADOPTION` · `MATERIALIST` · `ORION_TRADING` · `NHI_CONTACT` · `BUILD_EFTZ` · `PSI_SERVICE_INDUSTRY` · `COURIER_FLEET` · `PRIVATE_LINK` |
| **True Humans** | `RELIGIOUS_TRADITIONALIST` · `AGI_ABOLITIONIST` · `BIO_ONLY` · `NHI_EXTERMINATIONIST` · `HUMAN_SOVEREIGNTY` · `ANTI_HYBRID_ASSIMILATION` · `AUTHORITARIAN` · `DEFEND_HUMAN_AUTONOMY` |
| **Unity, Security and Stability** | `TECHNOCRAT` · `AGI_ABOLITIONIST` · `MATERIALIST` · `HUMAN_SOVEREIGNTY` · `NHI_CONTACT` · `EXTRATERRESTRIAL_DIPLOMACY` · `DISCLOSE_UFO_SECRETS` · `RESEARCH_LAB` · `COURIER_FLEET` |
| **The Noösphere** | `AUTONOMIST_MARXIST` · `RUSSIAN_COSMIST` · `ECO_SOCIALIST` · `COMMONS_ORGANIZER` · `ECOLOGICAL_STEWARDSHIP` · `DIRECT_DEMOCRACY` · `HUMAN_AUGMENTATION` · `BCI_ADOPTION` · `QUANTUM_RESEARCH` · `QIP_PANPSYCHIST` · `PSI_RESEARCH` · `COSMIC_SOURCE_IDEALIST` · `RITUAL_PRACTITIONER` · `CONFEDERACY_ALIGNED` · `NHI_CONTACT` · `INTERDIMENSIONAL_CONTACT` · `ABOLISH_PRIVATE_PROPERTY` · `EXTRATERRESTRIAL_DIPLOMACY` · `REMOTE_VIEWING_TEAM` · `TELEPATHIC_NETWORK` |

**Two sets are internally contradictory on purpose, and the contradiction is the design:** the True
Humans carry `MATERIALIST` **and** `RITUAL_PRACTITIONER` — its two PSI wings reach the same policy from
opposite metaphysics; and the Noösphere carries `HUMAN_SOVEREIGNTY` (inherited from the Cosmist
International template) in **tension** with `CONFEDERACY_ALIGNED`. `AUTHORITARIAN` on Unity is carried
as the **critics' charge, not a self-description**.

---

## 3. The 2026 baseline's missing half

`REALITY_TUNNELS.md` §3 sources its baseline to Politico (April 2026), GPB's faction guide
(Sept 2026), Kate Gage's *Political AI Field Guide* and El País (May 2026) — all **US and European**.
Both issues ask for more than that: #470 requires studying globally significant formations "including
… decolonial/Global South", and asks to avoid "a US-only political compass". This is the missing half.

**Verification key:** ● read at source · ○ headline/date-level · △ prior knowledge, unverified.

| Formation | Region / base | On technology | Confidence |
|---|---|---|---|
| **Decolonial / digital-sovereignty** | Transnational; Latin America, Africa, UN forums; NGOs (APC, WITNESS), G77 states | Pro-modernity, **anti-extraction**: self-determination over data and AI governance, not refusal. Carried by the UN Global Digital Compact (adopted 23 Sep 2024 as a Pact annex) | ● High; medium on coherence as a bloc |
| **Pan-African / African Union** | 55 members; AU organs and an emerging tech-policy class | **Pro-AI-as-development** with explicit **data sovereignty**: the Continental AI Strategy (2024) is **nonbinding**, and the AU's own framing is African knowledge systems as "core inputs" (Tech Policy Press, 4 Feb 2026 ●) | ● High. The source's own caveat: **"governance without leverage"** |
| **Indigenous sovereignty** | North America core, UNDRIP/FPIC framing globally | **The sharpest anti-AI-extraction frontier.** Honor the Earth's No Data Center Coalition tracks **100+ proposed data-centre projects** on tribal and rural land and names it "data colonialism", documenting NDA-driven capture of Tribal leaders (Democracy Now!, 22 Apr 2026 ●) | ● High; a counter-case (one nation welcoming a project) is unresolved ○ |
| **Latin America** | Pink-tide parties, MSTs, Indigenous movements, weakened 2025–26 | **Sovereign-compute public AI, not refusal** (Brazil's AI plan ○), inside a right-shifting electoral cycle (Chile, Bolivia ○) | ●◐ Medium-high. **Do not cite** an "Oaxaca buen vivir reform" — unverifiable |
| **India / South Asia** | BJP/RSS mass base plus a DPI tech class | Hindu-nationalist techno-politics: "techade", state digital-identity rails, summit-hosting — emphatically **not** AI-doomer | ● High on framing; surveillance harms documented ○ |
| **Gulf techno-nationalism** | Saudi Arabia, UAE, Qatar, Kuwait; sovereign-wealth capital | Maximal techno-optimism, explicitly **US-anchored** (MEI, Feb 2026 ●) — via HUMAIN, G42, Stargate UAE | ● High. **Distinct from Islamist movements** — do not conflate |

### 3.1 The finding that matters, stated plainly

The four UN factions descend from formations that are **mostly Northern and institutional** — which is
where the 2026 evidence for *global* parties is strongest. The material above shows that at least two
major real positions are **not well represented by any of the four as written**: the AU's
data-sovereignty programme, whose defining feature is *"governance without leverage"*, and the
Indigenous anti-data-centre movement, which is the sharpest anti-AI-extraction politics in the world
and has no seat in the roster. This is a genuine gap, not a criticism of the roster's design — and it
is exactly what #470's open question about "the previously proposed non-UN projects" is about. It is
carried to the queue rather than resolved here.

---

## 4. What remains open

Row **D17** on `main` already carries the succession, register and magnitude questions. The rows added
by this branch (D18–D21) cover only what D17 does not: the roster's scope, the style-reference filing
and the coercive-plank question, and #469's remaining approvals. No decision is made here, and both
issues stay open, as each instructs.


## MJ-12 / Legacy Program compatibility decision sheet (2026-10-15; options, not canon)

The issue #470 addendum proposes a useful reconciliation of **fictional** reverse engineering with the human-vs-Orion technology gap. Keep this separate from the four-party register: the Legacy Program is not an additional playable party, and disclosure remains an **unordered `20XX` background event**, with 2045 as the default scenario opening year. This is a design hypothesis, not a real-world evidentiary claim about MJ-12, ARVs or secret bases.

| Open choice | Conservative baseline **proposal** | Alternative to weigh | Guardrail |
| --- | --- | --- | --- |
| Legacy/UNSA relationship | Partial transfer of records, personnel and few serviceable artifacts, with residual compartmentalized networks | Full public institutional absorption or an autonomous clandestine rival | Never add a fifth playable political faction |
| Operational ARVs | A scarce investigative/reconnaissance asset whose reliability and maintenance are unresolved | Museum-grade prototypes, unreliable experimental vehicles, or more mature but strategically outclassed craft | No readily mass-produced near-peer Earth fleet |
| Two technology streams | Distinguish AGI-accelerated inventions from fragmentary ET-derived components, and permit ambiguous mixed provenance | Leave individual devices' origins completely disputed | Technological *capability* is not proof of a particular origin |
| Disclosure | Competing in-world reports, later official US acknowledgement, incomplete accessible archives | Fractured or qualified acknowledgement | No precise `20XX` sequence or automatic public consensus |
| Combat asymmetry | Intelligence, logistics, attrition and political constraints matter more than a single superior weapon | Emphasize reverse-engineering knowledge gaps and incompatible supply chains | Orion remains dangerous; Confederacy motives stay ambiguous |

**Author decisions still needed:** number and availability of functional ARVs; authority over residual secret installations; what specific hardware survives in 2045; which institutions can independently verify provenance; how any of this affects UNSA missions. None is assigned a number, effect, modifier or event card here. Link eventual approved facts to the *existing* faction/world records and #468/#469 Reality Tunnel interpretation pipeline rather than creating a parallel MJ-12 roster. A disclosure card can be read in four ways by the four UN parties without giving the player omniscient access to its truth.
