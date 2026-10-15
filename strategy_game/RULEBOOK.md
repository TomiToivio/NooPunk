# NoöPunk Strategy Game: Rulebook

**Status (issue #389): Fate Core RPG foundation approved.** An original, bounded Fate-based Python RPG implementation and a tabletop-playtest manual exist at [rpg/RULEBOOK.md](rpg/RULEBOOK.md).

**Status (issue #482): the RPG foundation's skill layers are approved, and the strategic roster is not.** #482 adopts the Fate/Transhumanity's Fate RPG baseline, adds **exactly six individual skills** (COG, INT, REF, SAV, SOM, WIL) as Fate-rated skills, and states the crossover's structure — one faction leader and four agents, at most one action per character per turn. It **does not** approve a strategic agent skill roster, a mission list, a probability, or any political-simulation number: those remain proposals awaiting the author (§4, §10). **Faction strategy and political simulation rules are not yet approved.** Separate from the existing NoöPunk legacy RPG rules; do not automatically import their mechanics.

**Tabletop-only design proposals, unchanged by this edition:** the [leader/NPC micro-rule example](docs/LEADER_MICRO_RULES_PROPOSAL.md) (#295) and the [PCM/LaclauGPT faction-hegemony cards, four party sheets and a worked crisis](docs/FACTION_HEGEMONY_TABLETOP_PROPOSAL.md) (#479). Both are human-playtest candidates, **not** approved mechanics, and neither is integrated into the runtime.

---

## 0. The three layers, and what is approved in each

### Layer I: Faction leader, narrative RPG
**Author-selected baseline:** Fate Core four actions, 4dF + skill, character aspects, stunts, Fate points, stress and consequences. First Python slice: [`rpg/fate.py`](rpg/fate.py); licensing and gaps: [`rpg/README.md`](rpg/README.md). PSI is natural and not virus-derived. Most humans remain in original biological bodies: cortical stacks and resleeving are optional, new and rare. NoöPunk lore does not inherit Eclipse Phase's setting.

**Approved by #389 and #482, and implemented in §2–§7 below:** the sheet, the six individual skills (§3), the four actions and outcomes (§5), aspects, Fate points and refresh (§6), stunts, stress and consequences (§7), and the scene-versus-mission split (§8).

**Still unapproved here:** advancement, equipment statistics, the full stunt catalogue, and the GM's narrative adjudication beyond the permissions §5 states.

### Layer II: Network-society political simulation
Reserved: Laclaudian ideological articulation, Castellsian communication power, agents, agency, contested meanings and systemic events. All transition mechanisms **TBD by author**.

Data vocabulary only (no rules): `politics.py` carries `Demand`, `Signifier`, `Formation` and `Frontier`; political relations are ordinary `NetworkEdge` records with a relation-layer label, so the field is one multiplex graph. Design record: [docs/POLITICAL_SIMULATOR_MODEL.md](docs/POLITICAL_SIMULATOR_MODEL.md). The complementary `political.py` vocabulary and the [Gate B design proposal](docs/POLITICAL_SIMULATION_DESIGN.md) introduce standalone articulations, signifier roles and communicative ties; both are containers, **not approved mechanics**.

### Layer III: Faction strategy
Reserved: organizational assets, faction management, strategic operations, resource allocation, spatial and network presence. All mechanics **TBD by author** — except the two **structural** facts #461/#482 state and §2/§8 implement: five seats (one leader, four agents) and one action per character per turn.

**Global factions (author canon, #328/#329):** the seven paradigm factions and their evidence model are in [docs/GLOBAL_FACTIONS.md](docs/GLOBAL_FACTIONS.md) and [`data/global_factions.json`](data/global_factions.json) — setting canon only, no mechanics. **UN parliamentary parties (#470):** the four 2045 UN parties live in [`../data/world/un_parties.yaml`](../data/world/un_parties.yaml) with paradigm stances and qualitative six-quantity profiles; **setting canon only, no magnitude, effect, difficulty, cost, cap or clock**, and whether they sit in the paradigm register is an open decision (D9/D17).

## 1. Scope, sources and licensing

This rulebook covers **rules only**. It uses mechanics from Fate Core and is written in NoöPunk's own vocabulary; it imports **no** Eclipse Phase or Transhumanity's Fate setting material — no Firewall, no Fall, no exsurgent PSI origin, no standard resleeving, no automatic cortical stacks, no EP factions, history or technology baseline. NoöPunk PSI is natural and not virus-derived, and routine resleeving is not presumed. Examples, gear assumptions and narrative material here are NoöPunk's.

| Source | Licence | What it is here |
| --- | --- | --- |
| *Fate Core System* (Evil Hat Productions) | **CC BY 3.0** | the chassis: 4dF, the four actions, aspects, Fate points, stunts, stress and consequences. Implemented. |
| *Transhumanity's Fate* (2016) | **CC BY-NC-SA** | a **design study**: how a transhuman setting is handled *minimally* on a Fate Core kernel. Its prose, setting and numbers are not reproduced and do not enter a distributable build. |
| *Eclipse Phase Second Edition* | **CC BY-NC-SA** | a **design reference**: the six aptitudes (§3) and, later, optional simulationist extensions (§10). Not imported. |

Verified this edition: Fate Core's default list is **18 skills**, and its Great pyramid rates 10 of them ([fate-srd.com/fate-core/skills](https://fate-srd.com/fate-core/skills)); its four actions and the +2-or-reroll invocation are stated on the SRD's own pages. Terra Invicta's councilor model is cited in §4 as a design reference ([wiki.hoodedhorse.com/Terra_Invicta/Councilors](https://wiki.hoodedhorse.com/Terra_Invicta/Councilors)).

**Attribution (required, and shipped):** *Fate Core System*, a product of Evil Hat Productions, LLC, developed, authored and edited by Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin and Mike Olson, licensed under Creative Commons Attribution 3.0 Unported. NoöPunk is independent and is **not endorsed** by Evil Hat Productions or Posthuman Studios. The machine-readable form is [`rpg/attribution.py`](rpg/attribution.py) and the readable form [`rpg/ATTRIBUTION.md`](rpg/ATTRIBUTION.md); the licence NoöPunk itself distributes under remains the author's decision (#200, queue row D10) and is not chosen by this document.

## 2. The character sheet: one character, two scales

A faction fields **one leader and four agents** — five characters, five seats. Each is **one character on one sheet**, and the same character is played at two scales:

* **as an individual**, in scenes: personal encounters, exploration, interrogation, fighting, investigation (§8.1);
* **as a faction agent**, on the strategy board, carrying an organisational, political, diplomatic, covert, scientific or military mission (§8.2).

The sheet carries, for every character: an id and name; a high concept, a trouble and up to three further aspects; the **individual skills** (§3) and a separate **strategic skill** ladder (§4); stunts; Fate points and refresh (§6); a physical and a mental stress track with mild/moderate/severe consequence slots (§7); and hooks that assume nothing — gear, a body, an optional cortical stack, and natural PSI with its particular capabilities. Equipment and cybernetics are **named permissions**, not statistics: a device may modify access, and it never creates PSI or a bonus by name alone.

The two ladders are **independent namespaces on the one sheet**, and which one a check reads is decided by the **context** the check is declared in — never by the skill's name, and never by which list happens to be longer. A high strategic rating buys nothing in a scene, and a high individual rating buys nothing in a mission. The engine refuses a check that names a skill from the other layer rather than rating it at zero, because "untrained" and "wrong list" must not look the same at the table.

## 3. Individual skills (approved, #482)

When a character acts **as an individual**, a check reads one of exactly six skills. These are Eclipse Phase 2e's six *aptitudes* used as **Fate-rated skills**: the value scale, allocation and advancement are the approved Fate baseline, and no percentile value, no second attribute scale and no extra statistic layer is added.

| Skill | Abbrev | Meaning |
| --- | --- | --- |
| **Cognition** | **COG** | Intelligence, solving problems, logical analysis |
| **Intuition** | **INT** | Gut instinct, rapid evaluation, awareness, creativity, cleverness, cunning |
| **Reflexes** | **REF** | Coordination, dexterity, nimbleness, balance, reaction speed |
| **Savvy** | **SAV** | Social awareness, adaptability, empathy, influence |
| **Somatics** | **SOM** | Exploiting bodily physical capabilities: strength, stamina, movement, sustained positioning |
| **Willpower** | **WIL** | Self-control, mental fortitude, strength of personality |

Rate them on the Fate ladder exactly as any Fate skill, using the conventional pyramid (+4 one, +3 two, +2 three, +1 four). Unrated skills are +0. The six are **broad on purpose**: they describe the kinds of thing a person can attempt, not the training a specialist has.

### 3.1 The crosswalk, and the duplicate that must not survive

Fate Core's default list is 18 skills. **NoöPunk's individual layer is six.** That consolidation is the simplification this edition makes, and it is deliberate: the six are the *individual* half of one sheet, so a name that exists only to separate two closely related competences is folded into the broad skill that covers both.

| Fate Core skill | Individual skill | Note |
| --- | --- | --- |
| Lore, Investigate | **COG** | knowledge and finding things out by method |
| Notice, Empathy | **INT** | noticing, and reading what is not said |
| Athletics, Stealth, Drive | **REF** | bodily speed, balance and handling |
| Rapport, Provoke, Deceive, Contacts | **SAV** | moving people, and the access that comes with it |
| Physique, Fight, Shoot | **SOM** | strength, stamina, sustained physical action |
| Will | **WIL** | holding under pressure, strength of personality |

**The duplicate that does not survive.** Transhumanity's Fate carries its own *Somatics* and *Will* alongside the Fate Core skills they overlap with. NoöPunk keeps **exactly one** of each: SOM and WIL are the six-name list's own entries, taken from the aptitude side, and no parallel Fate Core *Physique* or *Will* survives beside them. A character therefore has one strength-and-stamina rating and one self-control rating, not two of either.

### 3.2 Specialists do not add a seventh skill

A narrow technical speciality is expressed on the sheet as **a stunt** (a named exception the GM approves) or as a typed **`competence`** TAG — both of which already exist, and neither of which is an attribute. The tag records *what* the speciality is (for example a competence tag beginning with the broad skill it rides on: `COG: forensic reconstruction`); the stunt is the mechanism, and it is priced in refresh (§6). **A tag never moves a roll by itself**: a tag that added a bonus would be an unapproved mechanic, and the engine reads tags and stunts as a reading list, not as arithmetic.

**A capability is a competence, never a skill of its own.** PSI, netrunning and the other gated abilities are typed capabilities: they decide *whether* an action is available, and then the check reads one of the six. A precognitive impression is *INT*; contesting a mind is *WIL*. There is deliberately **no `Psi` skill** in the crossover — the earlier [rpg/RULEBOOK.md](rpg/RULEBOOK.md) §6 example predates the six-skill decision, and the kernel's own demonstrations use plain skill names because the kernel is setting-independent (§10).

## 4. Strategic agent skills (PROPOSAL — not approved)

When the same character acts **as an agent or leader representing their faction**, a check reads a **strategic skill** instead. This is a **different list on the same sheet**, and issue #482 explicitly leaves the roster open. What follows is a worked proposal with its mapping, offered for design review.

**Design reference, not rules.** Terra Invicta's councilors carry eight attributes — persuasion, investigation, espionage, command, administration, science, security and loyalty — and missions that check them. What is taken is the *shape*: a small consolidated list, each entry mapping to a kind of mission. **Nothing numeric is taken** — no attribute scale, no success probability, no mission weight, no cost, no council size, no XP, no turn cadence. The crossover's structure is #482's own: one leader, four agents, one action per character per turn.

### 4.1 The proposed roster (seven skills)

| Skill | What it covers | Mission kinds that check it |
| --- | --- | --- |
| **Statecraft** | moving people and institutions to the faction's position: negotiation, public argument, institutional access | negotiate, campaign |
| **Fieldcraft** | acting unseen and uninvited: infiltration, surveillance, moving an asset | covert action |
| **Inquiry** | finding out what is hidden, and reading what is already there | investigate |
| **Stewardship** | running the faction as an organisation: members, money, offices, logistics | organize |
| **Command** | leading the faction's people where it counts, including committed violence | field command, campaign |
| **Science** | research and analysis: adopting a technology, understanding a phenomenon | adopt technology, investigate |
| **Security** | surviving and preventing harm to the faction's people and holdings | counter-intelligence, field command |

**Overlapping cases are expected, and are the design question.** A campaign led from the front is *command*; the same campaign won by argument is *statecraft*. Evidence taken covertly is *fieldcraft*; the same evidence requested through a record is *inquiry*. Work done against the faction's own exposure is *security*, and the same tradecraft done for the faction is *fieldcraft*. Choosing which skill a mission reads is a table decision, and a case that feels genuinely ambiguous is a signal that the two skills should be merged — not that a difficulty should be invented to separate them.

### 4.2 The mapping from the Fate-side skills, and the reference's own mission model

All 18 Fate Core skills map onto the seven, with no leftovers. The table, with per-row notes and the caveats, is machine-readable in [`data/strategic_skills.json`](data/strategic_skills.json) (`mapping`), read by [`strategic_skills.py`](strategic_skills.py).

The same file carries the **reference column** — the Terra Invicta mission families whose attribute covers the same ground as each proposed skill (Control Nation, Public Campaign, Inspire and the Enthrall family for statecraft; Purge, Assassinate, the sabotage family and Steal Project for fieldcraft; Investigate Councilor, Detain Councilor and Crackdown for inquiry; Hostile Takeover for stewardship; Coup d'Etat, Increase Unrest, Stabilize Nation, Extract Councilor and the assault missions for command; Advise for science; Protect Target for security). Names only: **no description, no attack/defence pairing and no value** is taken, and the column exists so that the delegation of scope to a reference stays traceable rather than implicit.

Three caveats are part of the record:

* Transhumanity's Fate is a **minimalist Fate Core conversion** — its own developer notes say it "avoided creating new concepts and wherever possible built off existing Fate Core concepts" (quoted in [docs/ISSUE_461_RESKIN_SPEC.md](../docs/design/ISSUE_461_RESKIN_SPEC.md) §3.1). The mapping is therefore expressed against the **verified Fate Core list**, which is the list TF builds on. Confirming TF's own additions or removals against the book is an **open item**: the source rulebook is not in this repository and its CC BY-NC-SA terms forbid reproducing its text.
* Four proposed mission kinds — covert action, counter-intelligence, and field command — are new names; the rest reuse the existing vocabulary in `local_slice.py::MISSIONS`. The proposal says so itself rather than appearing to extend an approved list.
* The reference's own action economy is **not** verified and is **not** relied on: that a councilor attempts exactly one mission per assignment phase is implied by the wiki's intel wording but not stated there, and the crossover's one-action-per-character turn comes from #461/#482. `data/strategic_skills.json::terra_invicta_model` records what was verified and what was not.

### 4.3 Status, stated plainly

No strategic skill, mission kind, mission effect, difficulty or cost is approved. The roster is data with `status: PROPOSAL`, and the engine will not check a strategic skill unless a caller passes the roster in; with none, a faction-agent check is **refused as pending author approval** rather than rated at zero. Changing the roster means editing the data file, and the tests do not depend on its contents.

## 5. Dice, actions and outcomes

Throw **four Fate dice**, each showing −1, 0 or +1; sum them and add the skill rating. Subtract passive difficulty or active opposition: the difference is **shifts**. Negative shifts fail; zero is a tie; +1 or +2 succeeds; +3 or more succeeds **with style**.

The **four actions** are fixed, and the context is where the game lives:

* **Overcome** a problem or hindrance. A tie may succeed at a minor cost.
* **Create an Advantage** to add or discover a scene aspect, with a free invocation (two on style).
* **Attack** in a permitted conflict — the harm may be physical, mental, emotional or social.
* **Defend** against an action, and against an attempt to create an advantage against you.

An attack's positive shifts become a hit (§7); a defence that succeeds with style may grant a **boost** — a one-use, fleeting aspect. **The GM keeps everything else**: whether the action is possible at all, what the opposition is, and what a cost or complication looks like. The dice decide the outcome, not the fiction's permissions, and the engine reports mechanical signals without fabricating story.

**Two permissions are checked before any dice at either scale.** Reachability: a serious intrusion needs local access, a nearby position or a deployed proxy, and no roll grants reach the fiction did not. Capability: a special move needs its competence first — a cyberattack needs a netrunner capability, remote-viewing reconnaissance needs a PSI capability — and an ineligible declaration is **refused, not substituted** for something the character could do.

## 6. Aspects, Fate points and stunts

Each aspect is true in the fiction and can help or complicate. Spend one Fate point to **invoke** a relevant aspect for **+2**, or for a reroll of all four dice; a scene aspect's **free invocations** are consumed one at a time and cannot be conjured from an ordinary untracked character aspect. A **compel** offers a complication: accept it and gain a Fate point, or pay one to refuse.

**Refresh** is the baseline a character returns to: at the start of a session Fate points rise **to at least** the refresh value, and a character holding more keeps the higher balance. Fate points are the **only** metacurrency. Eclipse Phase's pools are not added: reading a pool spend as a flavour of an invoke is a design reference, and a second currency would double the economy.

**Stunts** are named exceptions the GM approves, not entitlements that follow from an aspect's name. A stunt taken beyond the first three reduces refresh by one, which is the price of a capability and the reason a specialist's narrow competence is not free.

## 7. Stress, consequences and recovery

Physical and mental stress are tracked separately, two boxes each by default. An unused box absorbs a hit no greater than its numbered value, one box per hit. A named **consequence** may reduce a hit by its severity — mild 2, moderate 4, severe 6 — and occupies that slot. If nothing legal absorbs the hit, the character is **taken out**, and the GM narrates what that means; **conceding** is a negotiation before that point, not a death or a reincarnation algorithm.

Stress clears when the conflict ends; consequences need narrative recovery and time. Damage never entails a default backup-restoration. **Physical stress belongs to the body and mental stress to the mind** — which is why the body is gear and aspects on the one sheet rather than a resleeving economy: a changed chassis is a scene with a consequence, not a routine that erases harm.

## 8. Play at the two scales

### 8.1 A scene (individual)

The GM frames the problem, establishes the opposition and the stakes, and asks whether training, bodily state, access and equipment make the attempt possible. Roll only when uncertainty is interesting. A scene **settles** a personal action and can also explain or settle a committed mission — it never grants a sixth order (§8.2).

### 8.2 A faction turn (agent)

Five seats: **one leader and four agents**. In a turn each character may take **at most one action** — one declared mission, or a hold. The limit is per **character**, so a character cannot act twice by holding two seats. A mission names its actor, its target and the quantity it aims at; it is declared before any dice, and a declaration that fails a permission check (§5) is refused there and then.

A mission reads a **strategic** skill; the same character's scene checks read the six **individual** skills. Neither list is ever substituted for the other.

### 8.3 A worked turn

A faction's five characters each declare one action. The leader **negotiates** at a committee hearing: *statecraft*, and the negotiation is an *overcome*. An agent **investigates** testimony at a records office: *inquiry*. A third declares a **cyberattack** on a reachable system: with no netrunner capability the declaration is **refused before any dice** and the action is spent on a hold, not converted into an investigation. A fourth proposes **remote-viewing reconnaissance**: without the PSI capability, likewise refused; with it, the check is resolved on the same kernel as every other check and **proves no objective fact** — it yields what the viewer reports. The fifth **organises witnesses**: *stewardship*, creating an advantage the leader can invoke later.

### 8.4 A worked scene

An operative investigates a tampered terminal. The GM first establishes whether they hold local credentials, physical access, or a plausible cyberspace route. If so, **Overcome** on *COG* against the chosen difficulty, and the GM interprets the result. A witness has a disturbing impression: if the character has natural PSI **and** the particular capability (§3.2), **Create an Advantage** on *INT* may mark a scene clue with a free invocation. No disease, stack, network-wide telepathy or automatic revelation is implied.

A scene resolves through the same kernel as a mission — `strategy_game.rpg.skills.check` with `ActionContext.INDIVIDUAL` — so both scales share one arithmetic and differ only in which list they read, what the opposition is, and where the consequences land. The kernel's own demonstrations are run separately:

```bash
python -c "from strategy_game.rpg.fate import demo_investigation; print(demo_investigation())"
```

## 9. Advancement, in brief — and what is deferred

Advancement is **not approved**. The Fate baseline it will start from is milestone-based (a session's significant events raise a skill or refresh by one step), and nothing more is asserted here. Deliberately deferred, and recorded so no reader mistakes silence for a decision:

* the **strategic roster's final names** and its mission kinds (§4 is a proposal);
* every **numeric** question of the strategy layer: mission difficulty, cost, duration, cadence, effect on any of the six quantities, and win conditions (queue rows D3, D11);
* **advancement**, the full stunt catalogue, and equipment statistics;
* the **GM's** narrative adjudication beyond §5's permissions;
* whether EP2e's **simulationist** material is ported at all (the percentile kernel is refused; §2.1 of [docs/ISSUE_461_RESKIN_SPEC.md](../docs/design/ISSUE_461_RESKIN_SPEC.md) records the band→ladder question as row R1, the skill list as R2 and the untrained floor as R3);
* whether a **consequence maps onto the council status vocabulary** — the join that would make "one sheet" literal across both scales.

## 10. Python API and reproducible tests

| Module | What it is |
| --- | --- |
| [`rpg/fate.py`](rpg/fate.py) | the kernel: 4dF, the four actions, the four outcomes, the sheet, Fate points, stress and consequences |
| [`rpg/skills.py`](rpg/skills.py) | the six individual skills, the **action context** that selects a layer, and the refusals that keep the two lists apart |
| [`rpg/roster.py`](rpg/roster.py) | the five seats and the one-action-per-character turn |
| [`strategic_skills.py`](strategic_skills.py) | reads and validates the proposed roster and its mapping from `data/strategic_skills.json` |
| [`rpg/boundary.py`](rpg/boundary.py) | the reserved seam to the unapproved strategy and political layers |

```bash
python -m strategy_game.rpg                                  # the worked scene as JSON
python -m unittest discover -s strategy_game/tests -p "test_*.py"
```

The dice are seeded and the randomness is **injected**, so every check replays exactly. Tests cover executable behaviour only (#271): the dice, the context that selects a skill list, the refusals, the resource spends, the five seats and the one-action turn — never whether this document says a particular thing. Creative material is reviewed editorially and by **playtesting**.
