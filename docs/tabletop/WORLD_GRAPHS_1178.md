# The four graphs on paper — a tabletop acceptance procedure (#1178)

> **Status: tabletop procedure, not canon and not a rule.** It exists so the graph model can be
> *played* with index cards before any software claims to implement it. If a group cannot run the seven
> checks below in ten minutes, the model is too complicated for the game.
>
> Implementation reference: [`docs/design/FOUR_GRAPH_IMPLEMENTATION_1178.md`](../design/FOUR_GRAPH_IMPLEMENTATION_1178.md).
> Runtime model: `src/world/graphs.py`. CWN resolves every action inside a scene.

## What you need

Four colours of index card (or four corners of one sheet), a pencil, and a handful of coins or sticky
notes for people. Nothing else.

## 1. Physical — *places are cards, people are tokens*

* One card per **place**: world → city → district → location → room, at whatever resolution the table
  cares about tonight.
* Draw **routes** as lines between cards and write the route name on the line. A one-way door gets an
  arrow.
* Put a **token** on the card where each character is. A character is never a card.
* Moving: pick a connected card. If the route is gated, the gate must be open in the fiction (a key, a
  warrant, a person who lets you in) — the graph does not decide; the table does.
* Two characters on the same card can interact. On different cards, they cannot without a route.

## 2. Cyber — *devices are cards, an avatar is a second token*

* One card per **device or service** (camera, terminal, host, turret). Write on it the **physical
  location card** it belongs to.
* Draw **network links** between device cards.
* Each hacker player has a second token — the **avatar** — which moves between device cards.
* The **body token does not move**. Taking the camera does not put the hacker in the corridor; it puts
  their avatar on the camera.
* Anything a device does in the world (a turret firing, a camera recording) is a device action, and CWN
  hacking decides whether the avatar may command it.

## 3. Social — *here characters really are cards*

* One card per **character or faction**.
* Write **relationships on the line** between two cards: a signed number from −4 to +4, plus a word.
  Asymmetric relationships are written twice, once in each direction, and may disagree.
* **No movement.** You cannot travel along a relationship. You can travel *to* where a person is, which
  is a Physical move.
* An unrecorded relationship is **unknown**, not zero. Write "?" rather than 0.

## 4. Story — *series, episode, scenes*

* Three sizes of card: **Series** → **Episode** → **Scene**.
* A scene card lists its **types** (Investigation, Exploration, Action, Social, Cyber; Astral only when
  a scripted dream/NDE scene calls for it) and the **entities it references** — a place card, a device
  card, a person card.
* Write **prerequisites** on the scene card as flags the table can check ("the warrant is signed",
  "the witness has talked"). A scene whose prerequisite is missing is not available; the table does not
  argue with the card.

## The seven checks (run these once, in about ten minutes)

1. **Two characters meet only when they share a place.** Put one token in Kurvi and one in Pasila; ask
   them to talk. They cannot. Move one token; now they can.
2. **Movement follows one route.** Try to move a token to a card with no line. Refuse it. Then draw the
   line and allow it.
3. **A camera is a Cyber card with a Physical reference.** Put the camera card on the corridor card,
   write the corridor's name on it, and confirm that disabling the camera changes nothing about who is
   standing in the corridor.
4. **An avatar moves without moving a body.** Move the avatar token camera → terminal; the body token
   stays where it was. Then have someone knock on the door: the hacker is *there*, not in the network.
5. **Social ties survive travel.** Move a character three places away and confirm the relationship card
   still reads the same, and that nobody had to "carry" the relationship along a route.
6. **A scene transition depends on a flag.** Hold a scene card with a prerequisite until the table marks
   the flag; then allow the transition. Try the reverse: mark the flag first and watch the scene become
   available.
7. **One actor, one sheet.** The same character appears in the Physical, Cyber (as an operator) and
   Social views without a second character sheet, second inventory or second hit-point track.

If check 7 fails, the table has created a second character by accident — the most expensive mistake in
this model, and the one software is most likely to reproduce.

## What this procedure deliberately does not do

* No **Astral graph**: an astral scene is a Story scene with its own types, not a fifth map, until a
  scripted projection scene genuinely needs navigation.
* No tactical grid: ranges are narrated, CWN resolves them.
* No emotion, lie or investigation-point trackers: evidence and testimony are written down as
  statements, and contradictions are pointed at with a pencil.

### First-day Dispatch check

Inspect each issued item and mark any faults on Tony's sheet. Connect the working kit.
Either the radio or the phone can carry Tony's check-in. If both fail, Tony can restore
either inspected device at the kit interface without a roll. Keep the fault on the other
device when saving or passing the sheet to another player.
