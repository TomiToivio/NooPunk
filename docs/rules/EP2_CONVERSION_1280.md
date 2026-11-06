# Borrowing Eclipse Phase hacks into CWN — a GM reference (#1280)

> **Status: author/GM reference, not a rule.** CWN owns hacking resolution. Every conversion below tells you
> which published procedure to use and what the *scene* gains from the EP idea; none of them adds a roll, a
> track or a statistic.
>
> **Licence.** *Eclipse Phase Second Edition* is CC BY-NC-SA 4.0 and is **not importable** into this project.
> Nothing is reproduced here: the page ranges are citations, and every sentence is our own description of a
> concept. See [`docs/sources/GAME_SYSTEM_RIGHTS.md`](../sources/GAME_SYSTEM_RIGHTS.md).
>
> **No numerical conversion exists.** EP percentile ratings, degrees of success and mesh damage have no CWN
> equivalent, and mapping them would invent a rule this project does not have.

## What EP is actually good at

Not the intrusion — the *aftermath*. Someone can hold valid credentials, perform a permitted export, and still
attract an auditor's attention. Security can know something is wrong without knowing who did it. That gap is
where detective work lives: a lead, a contradiction, a reason to interview the relay operator.

Its complexity comes from tracking several things independently — account permissions, intruder status, system
alert, defender actions, persistent access, and the evidence left behind. NoöPunk should borrow the *one* of
those that changes what a character can do next, and drop the rest.

## The conversion schema

For each borrowed idea, write one line:

> **Trigger and objective | physical device and Cyber node | connection and authority | CWN action or valid
> Verb + Subject | published timing, costs and security | one observable EP-inspired consequence |
> duration/end condition and evidence source**

Then decide what kind of thing it is:

1. **Ordinary authorised use** — no roll, the interface permits it.
2. **A published CWN hack** — resolve it once, with the target's own security difficulty taken from the
   operator and infrastructure that actually protect it.
3. **A new rule** — stop. This page does not add one.

Record three separate things that EP tends to merge: a **node is a location**, **account privileges** describe
permitted operations, and **CWN Access** is a spendable hacking resource.

## The conversions

| EP element | Borrow when | What CWN does instead |
| --- | --- | --- |
| PAN, mesh ID, isolated network | the characters need to reach a *device* | Anchor the device to the Physical Graph. Wireless Jack In costs a Move and needs clear sight within the published range; the avatar stays on that node. A wired route or a physical approach reaches the archive. |
| Brute force vs subtle intrusion | a witness is leaving, a shift is ending | Two approaches: act now with the loaded program, or spend fictional time securing an account, port or device model. The actual hack still uses the CWN action and cost. Preparation changes the *street*, not the math. |
| User / security / admin privileges | a login permits one thing and restricts another | Say what this account may do here. A permitted export uses the interface; a protected operation needs the published procedure. One success grants one stated effect. |
| Intruder status, alerts, system defender | who noticed will matter later | Write one fact: "the operator flagged the export; the intruder's identity is unknown." Escalate with the network alert: two failed checks make one Alert the Network action, two actions alert the network (`AlertClock`). CWN's demons and watchdogs (p. 102) would defend a node by themselves, but **this repository does not implement them yet** — until it does, the defender is the operator. |
| Subvert sensors or commands | the outcome is to change what someone sees or does | Pick the exact published effect: Blind + Camera suppresses input; a fabricated feed needs a deception effect; a controlled device uses Issue Command. Say who can observe the result. |
| Logs, tracking, cleanup | tonight's hack becomes tomorrow's evidence | Name the copy and its custodian — terminal log, gateway receipt, human testimony. Copy File or an applicable file program needs a reachable node. Alter one log and the others remain. |
| Backdoor and later patch | the team expects to return | An authored stolen credential or planted maintenance account is a lead with a node, a scope and a revocation condition. If nothing published permits creating it, defer it. |
| Mindware, mesh combat, software damage | a BCI or autonomous system is the target | Identify the digital component and a legal Subject, then use the published program or combat effect. Reading the wearer's experience needs a separate eligible PSI technique. |

The machine-readable version, with the trap attached to each row, is
[`data/rules/ep2_cwn_conversions_1280.json`](../../data/rules/ep2_cwn_conversions_1280.json).

## Where each row lives

| Row | Implemented by |
| --- | --- |
| network topology | `src.world.graphs.CyberGraph`, `src.rules.cwn_hacking.WIRELESS_PENALTY` |
| brute force vs subtle | `src.rules.cwn_hacking.hacking_check` |
| privileges | `src.rules.cwn_hacking.SECURITY_LEVELS` |
| alert state | `src.rules.cwn_hacking.AlertClock` — **demons/watchdogs unimplemented** (`CWN_FE_PARITY_MATRIX.md`) |
| subversion | `src.rules.cwn_program_catalogue.run_program` |
| logs | `src.rules.cwn_program_catalogue` (`Erase`, `Append`, `Replace`, `Datafile`) |
| backdoor | **nothing** — an authored lead, not a capability |
| mindware | `src.rules.cwn_program_catalogue` (`Sabotage`, `Glitch`, `Hijack`, `Frisk`) |

`data/rules/ep2_cwn_conversions_1280.json` carries the same mapping as `implemented_by`, and
`tests/test_ep2_conversions_1280.py` resolves every path: a row may name a mechanic **or** admit it has
none, and nothing in between.

**The arithmetic the page now states**, because it is what a table actually argues about:
`Blind + Camera` costs **2500** (Verb 2000 + Subject 500), requires **Access 1**, has skill modifier **0**,
does not self-terminate, and pays the wireless **−2**.

## Two worked street cases

**The Kurvi camera.** Tony already has a wireless link to a camera watching the witness. He moves with Laura
and spends his Main on Blind + Camera, paying normal program costs and checking security. The camera loses
input for the published effect; the footage it already recorded is on another node. The caretaker notices the
gap and calls Salla. **The program can succeed completely and still produce that consequence.** Out of range,
the link fails and the effect ends — a field deck that waives the wireless penalty changes the check alone.

**The dispatch audit.** A genuine dispatcher account was used before the rendezvous leaked. Laura obtains the
duty supervisor's permission while Tony reaches the local archive terminal. With a valid route and permitted
access he spends a Main to copy the file into deck Memory. Its timestamp does not match the independent relay
receipt. **That mismatch gives Salla a reason to interview the relay operator; it does not identify the
assassin.** If the supervisor refuses, securing the terminal or finding another original is the next scene —
an intrusion is a separate choice with its own cost.

## PSI: borrow the power design, not the system

EP separates self-directed, usually passive psi-chi from active psi-gamma that affects other minds, and its
sleights state target, range, action and duration. What is worth borrowing is that a successful power can
still cost the user personally. NoöPunk PSI keeps its own ontology, Effort and resistance rules; anything that
looks like infection belongs to an explicitly authored exposure or a compromised device.

| EP inspiration | Bounded NoöPunk use | What still decides |
| --- | --- | --- |
| Eco-Empathy | in a Sirian greenhouse, a receptive character senses that an unfamiliar organism thrives near moving water | laboratory work establishes composition and origin |
| Grok | an ESP impression suggests how an unfamiliar psychotronic instrument is operated | Program or Fix and the appropriate access govern operating it |
| Browse Thoughts vs deeper scanning | Telepathy techniques get distinct scopes: a fleeting impression, a consensual exchange, a deliberate search for one memory | each scope needs its own permission and resistance; Astral Body grants none of them |
| Psi Shield / pushing | check Metapsionics and AntiPSI before adding a defence; a Grey-linked prototype may be overdriven at the cost of an identifiable signature | existing Effort, resistance and ward rules |

**Every proposed technique must record**: owner · minimum training or device · eligible target · domain ·
range · action · Effort · resistance or consent · duration · evidentiary limit. A technique without all ten is
not ready to play, let alone to implement.

EP's ego/morph and fork assumptions need a separate review against NoöPunk's conscious-agent continuity —
resleeving is a setting question (#1255), not a hacking one.

## The playtest criterion

Run an ordinary camera hack using **CWN alone**. Then replay it with **one** EP detail — a named auditor, or a
second log. Keep the detail only if it changes the next field decision.

If keeping it requires a second hacking roll, an alert track, or a compulsory PSI subsystem **solely** to
imitate EP, cut it: that is the moment the conversion stops being a scene and becomes a rules engine.

## Sources

- *Eclipse Phase Second Edition* — mesh topology pp. 240–241; permissions p. 246; tracking pp. 256–257;
  intrusion and defence pp. 258–261; subversion and simple hacking pp. 262–263; mesh combat, mindware and
  surveillance pp. 264–271; PSI pp. 272–285. Cited, not reproduced.
- *Cities Without Number Deluxe* — node access and security pp. 92–95; program construction and effects
  pp. 96–99; cyberspace actions and examples pp. 100–101.
