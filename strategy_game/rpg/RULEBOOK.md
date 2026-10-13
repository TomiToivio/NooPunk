# NoöPunk: Fate-based RPG Field Manual (playtest edition)

**Scope:** Layer I of the NoöPunk Global Strategy crossover, issue #389. This is an original, compact *tabletop-playable* adaptation of Fate Core for the NoöPunk setting. It is not a reproduction of *Transhumanity's Fate* and is not the legacy NoöPunk RPG. Strategy and political simulation mechanics are not approved.

## 1. Fiction before dice

The GM frames a problem, establishes opposition and the **stakes**, and asks whether the character's training, bodily state, access and equipment make the action possible. Roll only when uncertainty is interesting. A player says what their operative attempts and how. A cyber skill does not permit a remote hack of an isolated machine. PSI is natural, neither infectious nor automatically omnipotent. The opening setting is pre-NHI-Crisis acceleration, not the aftermath of Eclipse Phase's Fall.

## 2. Character card

Name, identity, a **high concept**, a **trouble**, and up to three additional aspects. Each aspect is true in the fiction and can help or complicate things. Keep skills as the Fate ladder; rated abilities add to the dice, unspecified skills default to +0. A conventional starting pyramid is +4 (one skill), +3 (two), +2 (three), +1 (four), but skill selection and NoöPunk vocabulary are playtest choices, not a fixed project-wide catalogue. Record stunts as distinct named exceptions **requiring GM approval**; do not presume any mechanical benefits from names alone. Start a session with at least three Fate points (refresh configurable). Track physical and mental stress separately, with two baseline boxes each in this implementation, plus mild (2), moderate (4) and severe (6) consequences.

Equipment and cybernetic implants are named permissions unless a future authorized rule defines mechanical bonuses. Most people have an original biological body. **Cortical stack and resleeving are optional, costly, uncommon and experimental**, not a creation requirement. Record natural PSI and particular capabilities separately from medical conditions and technology. Devices, cyberware and psychotronics may modify access but never create a virus-based PSI origin.

## 3. Resolving uncertain actions

Throw **four Fate dice**: each displays −1, 0, or +1. Sum them and add the relevant skill to obtain the total. Subtract passive difficulty or active opposition: the difference is **shifts**.

- Negative shifts: failure. In some overcome actions the GM may allow success at a serious cost.
- Zero: tie. An overcome tie may succeed at a minor cost; creating an advantage or defending at a tie can award a fleeting **boost**.
- +1 or +2: success.
- +3 or more: success with style.

Four actions: **Overcome** a problem; **Create an Advantage** to add a useful scene aspect; **Attack** in a permitted conflict; **Defend** against an action. Create advantage success provides one free invocation; style provides two. If the roll fails, the GM determines whether the advantage fails or opposition benefits. An attack's positive shifts become a hit, with style potentially generating a boost. Defense style may grant a boost. The GM handles the narrative effects, and the Python engine reports actionable mechanical signals without fabricating story outcomes.

## 4. Aspects, points and stunts

Spend one Fate point to invoke a relevant aspect for **+2** to the roll or **reroll all four dice**. A tracked scene aspect can supply free invokes, consumed one at a time. Free invokes cannot be conjured from ordinary untracked character aspects. **Compels** introduce a meaningful complication: accept to receive one Fate point; refuse by paying one. Fate points at session start rise to at least refresh, retaining any higher balance. Stunts may eventually modify normal actions when their exact benefits are authorized. An aspect's name is not itself an equipment entitlement, access credential, psi power or stunt.

## 5. Stress, consequences and conceding

After an attack, record the remaining positive shifts as a hit. An unused stress box can absorb a hit no greater than its numbered value, one box per hit. One named consequence may reduce the hit by its severity (2/4/6) and fills that consequence slot; if no legal absorption fits, mark **taken out** and ask the GM to narrate the result. Stress clears after the conflict; consequences require narrative recovery and time. **Conceding** is an explicit player/GM negotiation before being taken out, not a death or reincarnation algorithm. Deadliness is contextual and not a blanket automatic-kill rule. Damage never entails default backup-restoration.

## 6. NoöPunk scenes: investigation example

An operative investigates tampering with a secure local terminal. The GM first establishes whether the operator has actual local credentials, physical access, or a plausible cyber route under the separate connectivity model (#344). If allowed, roll **Infosec + 4dF** against the chosen difficulty using *Overcome*. The GM interprets the result and sets its consequences. An associated witness has a disturbing impression: if they **possess natural PSI and the specific capability**, roll **Psi + 4dF** to *Create an Advantage*, potentially marking a scene clue with one or two free invocations. No disease, virus, stack, network-wide telepathy or automatic revelation is implied.

Run `python -c "from strategy_game.rpg.fate import demo_investigation; print(demo_investigation())"` for the existing two-check scene. The same numerical resolver serves both.

## 7. Three-layer boundary

An RPG check produces agent ID, action, outcome and shifts as a read-only result payload. Faction actions, influence, societal dynamics, travel constraints, network contagion and global resource changes are **not computed** by this rulebook. A future explicit adapter can consume those results after approval. A GM may connect scene events narratively without claiming them to be approved simulator state transitions.

## 8. Source crosswalk and licensing

- *Fate Core* (uploaded edition), chapters **The Basics**, **Aspects and Fate Points**, **Skills and Stunts**, **Actions and Outcomes**, **Challenges, Contests, and Conflicts**: direct CC BY rules foundation. SRD: https://fate-srd.com/fate-core
- *Transhumanity's Fate* (2016, uploaded edition), especially **Creating Your Sentinels**, **Morphs, Bots and Vehicles**, **Technothriller Conflicts**, **Mesh**, **Mind Hacks**: comparative design guidance for embodiment, hacking and PSI. Its default Firewall/mesh/virus history does **not** transfer. CC BY-NC-SA 3.0, so its prose/content is **not included**.
- *Eclipse Phase Second Edition* (uploaded edition), chapters **Game Mechanics**, **Making Characters**, and the technical/PSI/cyber chapters: comparative simulationist reference, **not** imported percentile mechanics or setting. CC BY-NC-SA 4.0.

**Attribution:** This work is based on Fate Core System, a product of Evil Hat Productions, LLC, developed, authored, and edited by Leonard Balsera, Brian Engard, Jeremy Keller, Ryan Macklin, and Mike Olson, licensed under Creative Commons Attribution 3.0 Unported (https://creativecommons.org/licenses/by/3.0/). NoöPunk is independent and is not endorsed by Evil Hat Productions or Posthuman Studios. No source PDFs or licensed NC-SA artwork are bundled.

**Playtest boundary:** This describes a bounded RPG MVP, not a full rule-by-rule implementation of either transhuman sourcebook. The GM remains responsible for narrative permission, opposition, stunts, character advancement, recovery and concessions until separately approved.
