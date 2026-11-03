# Canon: Fortress Europe after the Fall (#1113)

> **Status:** preferred primary scenario, restored by author decision in #1113. This document designates which
> existing documents it supersedes, which it leaves standing, and which questions stay open. It does not
> implement systems and it does not alter any published rules.

Three markers are used, matching `POST_NHI_WORLD_1005.md` so the two documents are read the same way:

- **[CANON]** — author-established direction. Do not contradict it.
- **[IN-WORLD CLAIM]** — something a faction or character asserts. It may be true, partly true, or propaganda.
  The setting does not vouch for it.
- **[OPEN]** — deliberately undecided. Do not fill it in.

**Central premise [CANON].** *The rest of the world has already fallen. Fortress Europe has survived the
Singularity and Disclosure by becoming the thing the pre-Crisis world considered impossible: a socialist,
regulated, human-centred, panpsychic, solarpunk federation. Now its agents must venture into a world of rogue
ASI, alien capitalism, revolutionary ghosts, religious revelations and resurrected magick.*

The machine-readable chronology lives in [`data/world/chronology_1113.json`](../../data/world/chronology_1113.json).
This document renders it; it must not restate it differently.

---

## 1. What this replaces, and what it does not

The repository currently carries a **pre-Fall alternate timeline** as its stated premise:
[`docs/PRE_FALL_ALTERNATE_TIMELINE.md`](../PRE_FALL_ALTERNATE_TIMELINE.md) declares Earth "intact, inhabited and
politically central" and the Fall "has not happened". #1113 restores the original, much darker scenario in which
the NHI Crisis has already shattered most of the world.

| Document | Standing after #1113 |
|---|---|
| `docs/world/CANON_FORTRESS_EUROPE_1113.md` (this file) | **Preferred.** Primary scenario for narrative canon. |
| `docs/PRE_FALL_ALTERNATE_TIMELINE.md` | **Explicit optional alternate timeline.** Not deleted, not rewritten. It remains a playable "Earth intact" variant. A banner now says so. |
| `docs/world/POST_NHI_WORLD_1005.md` | **Partially superseded.** Its geopolitical premise (EU, China and India as three surviving pillars of an intact world order) is superseded. Its faction and programme material — Zookeepers, Greater Orion Arm, Sirians, the Ghost Rocket inheritance, UNSA starting from zero — remains valid and is not restated here. |
| `docs/world/NHI_CRISIS_921.md`, `NHI_FACTIONS_922.md` | **Standing.** These are the author's transcribed source text. This document does not overwrite them; where it disagrees with their framing it says so and defers to the source on anything marked disputed. |
| `rulebook/7_TIMELINE.md` | **Standing.** Setting year **2045**, paradigm shifts deliberately unordered. The chronology here is an ordering of events, not a claim to dates the rulebook leaves open. |

**Never silently blend the two timelines.** A campaign is either Fortress Europe or the pre-Fall variant; a
one-shot may borrow from the other only by saying so at the table.

## 2. Contradictions found, and how each is resolved

These were found by reading the documents, not by assuming they agreed.

| # | Contradiction | Where | Resolution |
|---|---|---|---|
| 1 | Earth "intact, inhabited and politically central" vs most of the world fallen | `PRE_FALL_ALTERNATE_TIMELINE.md` vs #1113 | Fortress Europe is preferred; the pre-Fall timeline becomes an explicit optional variant with a banner. |
| 2 | "The Fall: has not happened" vs "the world has already fallen" | same | The Eclipse Phase *Fall* (TITANs, Earth's sterilization) still has not happened. NoöPunk's **own** NHI Crisis is what broke the world. These are different catastrophes and must not be conflated. |
| 3 | EU, China and India as pillars of a surviving order vs Fortress Europe alone among ruins | `POST_NHI_WORLD_1005.md` §A vs #1113 §4 | The pillar premise is superseded. China remains a **co-belligerent and partner**, not a surviving pillar of a functioning world order. |
| 4 | UNSA described as "a UN agency" vs an EU-anchored body | `data/world/reveal_ladder.json` stage 0 vs #1113 | UNSA's origin is not settled by #1113. The reveal-ladder line describes what a *rookie believes*, which is compatible with a European-led agency that kept a UN name and mandate. Recorded as **[OPEN]**, not resolved by fiat. |
| 5 | AWN catastrophe treated as a future stage ("Stage 4: localized After the Fall") vs already across the border | #1105 escalation policy vs #1113 | AWN is **already true outside the Firewall** at campaign start. The escalation ladder still governs what the **player** learns and what reaches Helsinki, not whether the wider world has fallen. |
| 6 | Russia as a surviving great power vs a defeated, disintegrating Soviet Union | `POST_NHI_WORLD_1005.md` §A vs #1113 §2 | Superseded by #1113. The Soviet Union persisted or was restored, invaded Ukraine, lost to the EU in Operation Barbarella II, and is breaking into successor polities. |
| 7 | No mention of President Sanna Marin, Queen Sanna I, the Soviet of Saturn, or the Medvedev coup anywhere in canon | grep across `docs/`, `data/`, `rulebook/` | Absent, not contradicted. They enter canon here for the first time. |

## 3. Chronology [CANON]

Ordered, not dated. Real-world dates are historical; everything after the 1990s is anchored only to the 2045
present, because `rulebook/7_TIMELINE.md` deliberately leaves the ordering and dating of the paradigm shifts
open. The machine-readable source is `data/world/chronology_1113.json`; this table is generated from it.

<!-- chronology-table:begin -->
| # | When | Event | Status |
|---:|---|---|---|
| 1 | 1930s | Intelligence services conclude the 'spy planes' are not human technology | CANON |
| 2 | 1930s-1945 | Germany is first to reverse-engineer a crashed spacecraft | CANON |
| 3 | 1946 | Nordic Ghost Rocket crash retrievals | CANON |
| 4 | 1952 | Soviet contact with the Soviet of Saturn / Soviet of Nine | CANON |
| 5 | undated | Who the Soviet of Saturn actually were | OPEN |
| 6 | 1990s | France resolves important UFO and PSI questions | CANON |
| 7 | undated, before the Crisis | The Vatican opens historical archives | CANON |
| 8 | undated | Norwegian study of the Hessdalen lights and plasmoids | CANON |
| 9 | undated, before the Crisis | A restored Soviet Union invades Ukraine | CANON |
| 10 | undated, immediately before or during the Crisis | Operation Barbarella II | CANON |
| 11 | undated, before and through the Crisis | President Sanna Marin holds the federation together | CANON |
| 12 | undated, after the surrender | The mythic title 'Queen Sanna I of Europe' | CANON |
| 13 | undated | How a socialist president acquires a royal title | OPEN |
| 14 | undated, after the surrender | A thousand-year lease of the Trans-Siberian Railway | CANON |
| 15 | undated, the Crisis | The Singularity begins and turns partially malevolent | CANON |
| 16 | undated | The American legacy programme becomes the Trojan horse | CANON |
| 17 | undated, during the Crisis | Pope Teilhard declares the Noösphere and the Omega Point central to doctrine | CANON |
| 18 | undated, late in the Crisis | The Jerusalem manifestation | CANON |
| 19 | same moment | The quarantine is declared over | IN-WORLD CLAIM |
| 20 | same moment | The transmission fails or is corrupted | CANON |
| 21 | undated | Whether the corruption was interference | OPEN |
| 22 | after the Veil lifts | Magick returns as the Veil lifts | CANON |
| 23 | undated, near the Jerusalem event | American EMP-nuclear strikes against its own rogue-ASI zones | CANON |
| 24 | same window | DPRK contingency 'Birdsong, Whalesong' | CANON |
| 25 | same window | Medvedev storms the residence and takes the nuclear football | CANON |
| 26 | undated, after the coup | Plans Mars, Uranus and Saturn | OPEN |
| 27 | 2045 | Fortress Europe, and the world outside it | CANON |
<!-- chronology-table:end -->

## 4. The world map that follows from it

### Fortress Europe [CANON]
A federalising EU, AI-decelerationist by policy: its only frontier lab, **Mistral**, concentrates on narrow AI,
human-in-the-loop technology, intelligence augmentation and safe applications. Quantum computing, Quantum
Information Panpsychism, psychotronics, empathy and consciousness technologies, solarpunk, biopunk, philosophy
and the welfare state are the comparative advantage. A massive **Firewall** and famously thick bureaucracy keep
foreign corporate and rogue-ASI influence out. It is the thing the pre-Crisis world called impossible.

Show its internal tensions as well as its achievements: opposition, propaganda, rationing, bureaucracy, and a
sincere argument about whether the Firewall is protection or a cage.

### The ruined United States [CANON]
Fractured into corporate-owned neofeudal fiefdoms, lawless libertarian districts, rogue-ASI contamination zones
and **Greater Orion Arm Co-Prosperity Sphere** Extraterrestrial Special Economic Zones. Hybrid infiltration has
compromised political and security institutions; cybercapitalist billionaires have gone transhuman and
integrated with corporate AGI. Parts are uninhabitable or ungovernable. **Do not treat all Americans as one
faction** — resistance, refugees and ordinary communities persist and vary.

### The Mediterranean and the last Holy War [CANON]
The Israel/US versus Iran-and-allies war has run for a decade and is overtaken by an ontological and religious
apocalypse rather than concluded as a conventional war. This zone is pilgrimage, refugee routes, clandestine
diplomacy, impossible miracles and warfare at once.

The satire here has a target and it is not a religion or a people: it is **fanatical interpretation, manipulation
and catastrophe**. Depict religious people and communities as diverse, including peacemakers and those who
refuse violence.

### The broken Soviet empire [CANON]
Defeated and disintegrating into successor polities under European and Chinese pressure; active war zones,
occult and alien research complexes, irradiated sites and competing regimes.

### Outside Europe, unresolved [OPEN]
The wider World War III / NHI Crisis touches Russia, Iran, Cuba, Canada, Greenland, Mexico, Taiwan and Korea. How
each fares is undecided; do not fill it in to make a map look tidy.

## 5. The three things that make it NoöPunk rather than a disaster setting

**Nuclear escalation with a chain of ambiguity [CANON].** While European soldiers approach Omsk they do not yet
know a global nuclear escalation has started. US EMP launches against its own rogue-ASI zones are detected
worldwide; North Korean radars misidentify UAPs as incoming SLBMs; "Birdsong, Whalesong" is ordered. By macabre
coincidence those weapons threaten the same region the Zookeepers wish to contain, so they are not intercepted.
No point-of-view character is omniscient. Keep the ambiguity causal and unnerving, not a puzzle with a solution.

**The coup [CANON].** Medvedev, four commandeered Mi-8s, the execution of Gerasimov, the death of Putin, the
nuclear football handed over by a zealous Strategic Rocket Forces officer. The officers' fear, opportunism and
cultish loyalty matter as much as the violence. The original longer scene belongs to later fiction; this
document is an event index, not a screenplay.

**The secret history [CANON].** Distributed European knowledge — 1946 Nordic recovery, French answers in the
1990s, Hessdalen, Vatican archives, Haunebu and Die Glocke, Soviet material secured with Ukraine, and British
knowledge arriving on rejoining the EU — is what let Europe survive without a single centralised covert empire.
"**No entrenched legacy reverse-engineering programme**" does not mean "**no research or recovered material**".
Both premises hold at once.

## 6. How the rules systems map onto it

| System | Where it applies |
|---|---|
| **CWN** | Intact European society: a working bureaucracy, a functioning economy, ordinary human characters, ordinary crime. **Never altered** to reflect lore. |
| **AWN** | Already true across the border and in the fallen zones; a localized After the Fall, not a scheduled future event. |
| **SWN** | Psionics, NHI, extraterrestrial economics, faction turns and the Cold War between the Zookeepers and the Greater Orion Arm. |
| **NoöPunk mods** | Investigation, ideology, Noösphere, Mythos and Law of One phenomena, layered above the published systems. |

The escalation ladder still governs **what reaches the player**, per #1105 and `data/world/reveal_ladder.json`.
It no longer governs whether the wider world has fallen — that is already history.

## 7. Framing, and what must not be lost

- **Diegetic political satire and science fantasy.** Not predictions, and not claims about real historical
  persons or religions. Queen Sanna I is a joke that the setting takes seriously and a seriousness the setting
  knows is a joke; do not erase the irony in either direction.
- **No monoliths.** Americans, Russians, Chinese, Europeans, the religious and the secular all contain
  resistances, dissidents, profiteers and ordinary people.
- **Sharp tonal contrast is the point**: socialist bureaucratic utopia, cosmic horror, political farce and
  post-apocalyptic brutality sit beside one another without being averaged out.
- **Preserve the author's names, imagery and slogans.** Pippi Långstrump, the Communist Collective of Planets,
  the Anarchosyndicalist Co-operative of Railroad Workers, Empathy Boxes, "Birdsong, Whalesong", Merkabah,
  Seraphim and Ophanim.

## 8. Open questions this document deliberately does not answer [OPEN]

1. **Who the Soviet of Saturn were** — the Zookeepers, an Orion deception, a separate civilisation, a human
   future polity, or a mixture.
2. **What "Uranus" actually is** — a plan tied to the state's extraterrestrial knowledge and its prior contact
   with alien communists.
3. **How a socialist federal president acquired a royal title** — treaty, emergency mandate, military
   acclamation, or political theatre that hardened into fact.
4. **Whether the Jerusalem transmission was corrupted deliberately** — possible Orion Group interference, or an
   honest failure of translation between minds.
5. **UNSA's constitutional origin** — a European-led agency carrying a UN name and mandate, or something else.
6. **The human pilot of the pre-1945 crashed craft** — temporal, cross-dimensional, or neither.

## 9. Follow-up work, not done here

This document is canon and index. It does not build systems. The items #1113 lists that remain open are tracked
there: updating named faction and region descriptions, geopolitics, character briefs and entry-level UNSA
campaign hooks; and any later mechanic must keep the tabletop rulebook and the Python implementation in sync.

Related: #1005 (post-Crisis reference), #1007 (reveal ladder), #921 (Crisis history), #922 (NHI factions),
#1105 (SWN tracker and escalation policy), #1101 (WWN tracker).
