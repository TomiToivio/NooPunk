# Cyberspace and connectivity: three eras, reachability and what is illegal (issue #344)

**PROPOSAL. No rule is approved.** `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**. This
record transcribes the author's own connectivity model from issue #344's author-canon clarification
(2026-10-13) and implements the one check its acceptance criteria demand. It defines no probability,
difficulty, detection chance or numeric modifier.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/connectivity.json` | the model as data, transcribed from the issue |
| `strategy_game/cyber.py` | the reader and the access check |
| `strategy_game/tests/test_cyber_access.py` | executable contracts (issue #271: code only) |

Consumed, not restated: `docs/design/ISSUE_224_NOOSPACE_SCOPE.md` (the astral half of the same abstract
operation engine), `rulebook/18_CROSS_DOMAIN_STATE.md` and `src/rules/cross_domain_state.py` (the
cross-domain contract), and `docs/design/ISSUE_222_CYBERSPACE_SCOPE.md` (the cyberspace reservation).

## 1. The clarification that overrides earlier language

The issue's dated update fixes a temporal progression and overrides any earlier implication that the
Blackwall/Slownet world already exists when the campaign opens. **The player starts before the NHI
Crisis.** The internet is useful, and elite netrunners already rely on BCIs, intelligence
augmentation, AI copilots, tailored exploits and dedicated compute.

| Period | Connectivity | Typical hacking and missions |
| --- | --- | --- |
| **Acceleration toward the NHI Crisis** (starting era) | The internet still functions and is useful: public platforms, corporate networks, remote services, cross-border connections. Segmentation grows; no universally imposed Blackwall yet. | Remote intrusion where a reachable path exists; reconnaissance, cyberespionage, attacks on exposed infrastructure, social engineering, local infiltration. |
| **NHI Crisis** | The public internet is down or effectively unusable as a strategic global service. Connectivity varies locally, but reliable global networking must not be portrayed. Travel and logistics are disrupted too. | Local and offline intrusion, on-site access, drones, couriers, surviving isolated LANs, limited ad-hoc links. A netrunner may be skilled and still unable to reach the target. |
| **After the NHI Crisis** | A Blackwall-like barrier quarantines the hostile old internet; people use local high-speed private networks and a deliberately slow, managed Safenet. Sensitive transfers use private cables, microwave or optical links, or physical couriers. | Private organizational LANs, reached through a mismanaged Safenet-facing connection, physical presence, a drone or insider, or a private link or courier. |

**What changes across the eras is reachability, not capability.** The augmentations and the skill
persist; the routes disappear and come back different. That is the issue's narrative payoff: a heavily
augmented netrunner can become *more* technologically capable while becoming *less* globally
connected.

## 2. Connectivity classes

Each target carries a small connectivity tag — the issue's "initial candidate categories, not numerical
rules":

| Class | What it is | Remote intrusion |
| --- | --- | --- |
| `public_gateway` | a service reachable over the era's public network | possible, while that network is up |
| `safenet_exposed` | the organization's own link to the managed public network, mistakenly open | possible |
| `private_linked` | a dedicated private cable, microwave or optical link between selected sites | requires an authorised path |
| `local_only` | a fast local network with no outside route: building WLAN, industrial IoT, local servers | requires local presence |
| `isolated` | no connection at all to anything the operator can reach | **impossible** |

## 3. Access paths, and the one check

The paths are the issue's list and nothing else: a field netrunner on site; a drone or compromised
on-site device; an authorised institutional connection; an insider; a compromised courier shipment; a
remote attack on a public-facing service; and the forbidden route of bridging the quarantined old
internet. `cyber.resolve_access(target, era, path, local_presence=…, authorised=…)` reports whether an
intrusion is **physically and logically possible** — the issue's own words, *before any skill roll* —
and returns a stated reason either way.

Three rules are enforced as behaviour rather than prose:

1. **A truly isolated system refuses every remote path, in every era.** "An inaccessible air-gapped
   machine cannot be hacked remotely by narrative fiat." Reaching it takes a physical entry point: an
   operative at the site, or a device someone has already delivered there. Two independent conditions
   in the code enforce this, so defeating one does not open the door.
2. **A social tie is not a route.** A Castellsian social or institutional edge — `social_tie`,
   `faction_relationship`, `network_edge`, `influence_edge`, `personal_contact` — is refused **by name**
   with an explanatory error, so the mistake is loud instead of silent. On the strategy map, an
   influence edge is never a TCP connection.
3. **The era gate removes reachability.** A remote path stops working the moment the era's public
   network is down, and the assessment says why: *this is now a field operation, not a remote one*.

The check reports no odds. Detection risk, defensive response and the mission's resolution belong to
the author's abstract agent-led mission system, where a named agent commands the operation with
equipment, intelligence and exploits, and the consequences include detection, equipment loss,
institutional crackdown and diplomatic repercussions.

## 4. Two illegalities that must never be merged

The issue insists on the distinction, so the model keeps it as two classes:

- **A mismanaged public-facing exposure** (`infosec_failure`) is a serious, recurring information-security
  failure and a political embarrassment. It is **not** the containment crime.
- **Bridging the quarantined old internet** (`containment_breach`) is a grave international crime in
  every era, triggering automated cyberdefense and multinational law-enforcement response, including
  armed tactical teams.

`ConnectivityModel.is_containment_breach(illegality_id)` answers the question as a function, so a
"cyber crime" tag that merges the two is a defect a test can catch.

## 5. The example mission and the world event

- **One comparable mission across the three periods** — obtaining data from an on-premises research
  lab: remote intrusion through a reachable service while the internet is up; then an expedition,
  because the remote route is gone; then a private LAN reached through a mismanaged Safenet exposure, a
  drone, an insider or a courier. The same faction, the same netrunner, three different problems.
- **One world-level event seed** — a containment breach, a Blackwall political controversy, or a
  trade-off between security and scientific access. A seed, not a scripted outcome: whose gateway
  failed and whether the response is oversight or a crackdown are the questions the setting's
  movements fight over.

Both are data records, not code paths.

## 6. Scope boundaries

- The **quantum-information / panpsychism / psychotronics / Archaic Revival** half of #344's later
  update belongs to the #345 track (the PSI reconciliation landed as PR #350). This record does not
  restate it.
- **No separate network simulator, no mandatory hacking minigame, no unapproved numeric rules.**
  Cyber resolves through the same abstract agent-led operation engine as the astral and physical
  domains.
- The legacy RPG is untouched. This is the crossover package only.

## 7. Reconciliation, and what the author still has to decide

The issue asks that earlier passages stating the internet has already been universally replaced be
annotated as describing the **post-crisis** era. **Searched, and no such passage exists on the default
branch**: `rulebook/5_CYBERNETIC.md` and `rulebook_parts/04_cybernetic_systems.md` carry no three-era
connectivity model, and `docs/design/ISSUE_222_CYBERSPACE_SCOPE.md` is a 2.7 KB reservation record that
predates the era model entirely. The superseded language lives in the issue text, not in the
repository, so there is nothing on `main` to annotate — and the legacy chapters are not this session's
to rewrite (`#306`: never rewrite the legacy RPG). Recommended annotation text for the two legacy
chapters is recorded in the data file's `reconciliation` section; applying it is a one-line edit the
author can direct.

Undecided, and deliberately not decided here:

- The detection, defence and counter-intrusion model: what a hardened target does back.
- Whether Safenet reachability varies by region and faction, and who owns the gateways.
- Which specific cryptography survives the setting's cryptographic catastrophe.
- The mission-level difficulty and cost of each access path — the check says *possible*, never *easy*.
- Whether the containment-breach response is modelled as a world event, a faction asset, or both.
