# Faction creation: five axes, typed tags, and NHI diplomacy (issue #346)

**PROPOSAL. Not locked rules, and not a locked taxonomy** — the issue's own words mark every tag family
"examples, not a locked taxonomy". `strategy_game/RULEBOOK.md` still says **NO RULES APPROVED**.

| Artifact | Role |
| --- | --- |
| `strategy_game/data/faction_creation.json` | the vocabulary, transcribed from the issue |
| `strategy_game/faction_creation.py` | the reader, the draft validator and the player/GM split |
| `strategy_game/tests/test_faction_creation.py` | 28 executable contracts (issue #271: code only) |

**Consumed, not restated:** `data/global_factions.json` already declares the two conventional axes
(`economic` left↔right, `social` conservative↔liberal, with the "do not conflate economic liberalism
with social liberalism" note), the `additional_dimensions`, and the **#329 paradigm positions** (`agi`,
`psi`, `nhi`, `confederacy_accession`, `sovereignty_agency_consent`) with the note that two factions can
share a compass cell and still differ entirely. [`LEADER_COUNCIL_SYSTEM.md`](LEADER_COUNCIL_SYSTEM.md)
owns the court half: the four field agents, their portfolios, missions and relationships. This record
adds only what neither carries.

## 1. Named positions first, numbers only after playtesting

The five dimensions the issue names — economic Left↔Right, cultural Liberal↔Conservative, AGI and
technological transformation, NHI contact and integration, and PSI and consciousness ontology — are
expressed as **named qualitative positions**: strongly or moderately toward either pole, or neutral.
`numeric_scale_approved` is `false` in the data, and the validator refuses a number where a named
position belongs, saying why. The issue's own precision is kept: *"liberal/conservative" is a cultural
axis, the conventional Political Compass second axis is authoritarian/libertarian, and they are not
interchangeable* — so governance positions live in governance tags instead.

Two standing warnings are carried in the data: an ideology is **not** a personality, an intelligence, a
moral grade, a psychic power or a predetermined loyalty, and a faction's **publicly advertised position
can differ from its hidden agenda**.

## 2. The typed tag system

The type of a tag is what keeps the vocabulary honest. Belief, competence, equipment, relationship,
asset and goal are declared as kinds, so a `MATERIALIST` doctrine is never read as a `REMOTE_VIEWER`
capability — a materialist trained remote viewer is a contradiction the system *permits* rather than
one it silently forbids. Families are suggested, covering political doctrine, technology doctrine,
consciousness and PSI doctrine, PSI capability, NHI policy, social and governance doctrine, goals and
histories, and organisational assets.

**One definition, different contexts:** `REMOTE_VIEWING_TEAM` is a faction **asset**; `REMOTE_VIEWER` is a
character **competence**. Scopes are declared per tag, the model filters by scope, and a scope that no
vocabulary declares is reported rather than accepted.

## 3. NHI policy is not NHI diplomacy

The issue is emphatic that NHI cannot be captured by one scalar: *"avoid forcing 'pro-NHI' to equal
pro-Confederacy or pro-Orion"*. So there are two fields, and nothing derives one from the other:

- **Policy** is a position on the NHI axis — how welcoming a faction is toward contact in general.
- **Diplomacy** is a separate relation to *each named polity* — hostility, contact, trading, alliance,
  dependence or resistance.

A pro-contact faction may be hostile to both major blocs and still seek relations with independent
origins, and a xenophobic hardliner may seek the extermination of both. Both validate cleanly, and the
sabotage for that guard — adding a rule that refuses a pro-contact faction a hostile relation — turns
the suite red, which is how the separation is proven rather than asserted.

## 4. Fog of war

The starting UI must not reveal classified author canon. `player_view()` withholds the hidden agenda
entirely rather than summarizing it, and a polity the faction does not yet know about is **absent** from
its relations. The pre-generated Cosmist International template carries the issue's proposed positions
and tags, marked as proposed settings rather than frozen stats, and *he* does not begin knowing the
hidden Soviet, Confederacy or Orion history.

## 5. What the author still has to decide

- **The StO bloc's official label.** #348 locks **UCCC** and says not to revert to older
  Confederation/Orion Group names as official labels; this issue's text says **"Confederacy/Zookeepers"**.
  The data uses the locked name and records the other as notation, with the conflict flagged rather than
  decided.
- **The cultural axis**: liberal/conservative alone, or a distinct authoritarian/libertarian value as
  well. `global_factions.json` currently records authoritarian/libertarian under `additional_dimensions`.
- **Whether an ordered scale is ever approved**, and if so its range.
- **The authored diplomacy/recruitment event**, whose shape is recorded as a seed but whose content is
  the author's.
- **Any affinity or tension mechanic**: this module deliberately computes none, because the issue allows
  broad cues only as a later, author-approved aid.
